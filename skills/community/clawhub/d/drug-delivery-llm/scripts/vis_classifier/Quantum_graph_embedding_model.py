import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch_geometric
import numpy as np
import pandas as pd
import networkx as nx
import torch.optim as optim
from sklearn.model_selection import train_test_split
from graph_process.graph_encoder import GraphEncoder_MSRL
import braket
from braket import circuits
from qml_tools import simu_expecval_2qbit, partial_trace, dag, ptrace_8qbit_lists
import math
import os
from torch import Tensor
from torch.nn import Parameter
from torch_geometric.nn.conv import MessagePassing
from torch_geometric.nn.inits import zeros
from torch_geometric.typing import Adj, OptTensor
from torch_geometric.utils import add_remaining_self_loops
from torch_geometric.utils.num_nodes import maybe_num_nodes
from itertools import combinations
def simu_expecval_2qbit(state):
    cir = circuits.circuit.Circuit()
    cir.i(0)
    cir.z(1)
    H = cir.to_unitary()
    H = torch.tensor(H)
    expecval = torch.trace(state @ H)
    return (expecval.real + 1) / 2
def simu_expecval_1qbit(state):
    cir = circuits.circuit.Circuit()
    cir.z(0)
    H = cir.to_unitary()
    H = torch.tensor(H)
    expecval = torch.trace(state @ H)
    return (expecval.real + 1) / 2
def partial_trace(rho, N, trace_lst):
    if abs(torch.trace(rho) - 1) > 1e-4:
        raise ValueError("Trace of density matrix must be 1.")
    if rho.shape[0] != 2**N:
        raise ValueError("Density matrix dimension mismatch.")
    if len(trace_lst) != 0 and max(trace_lst) > N - 1:
        raise ValueError('Elements in trace_lst must be less than N-1.')
    trace_lst.sort()
    rho = rho + 0j
    if len(trace_lst) == 0:
        return rho + 0j
    i = int(trace_lst[0])
    index_lst0, index_lst1 = [], []
    for idx in range(2**i):
        for idy in range(2**(N-i-1)):
            index_lst0.append(idx * (2**(N-i)) + idy)
            index_lst1.append(idx * (2**(N-i)) + idy + 2**(N-i-1))
    M00 = rho.index_select(0, torch.tensor(index_lst0)).index_select(1, torch.tensor(index_lst0))
    M11 = rho.index_select(0, torch.tensor(index_lst1)).index_select(1, torch.tensor(index_lst1))
    rho_nxt = M00 + M11
    new_lst = [i-1 for i in trace_lst[1:]]
    return partial_trace(rho_nxt, N-1, new_lst) + 0j
def dag(x):
    return torch.conj(x).permute(1, 0)
class AmplitudeEncoding(object):
    def __init__(self, N, input_lst):
        if 2**N < len(input_lst):
            raise ValueError("Number of inputs must be less than dimension 2^N")
        self.nqubits = N
        self.input_lst = input_lst
        self.state0 = torch.zeros(2**self.nqubits)
        self.state0[0] = 1
        self.state0 += 0j
        self.rho0 = torch.zeros([2**self.nqubits, 2**self.nqubits])
        self.rho0[0][0] = 1
        self.rho0 += 0j
    def encoded_state(self):
        num = len(self.input_lst)
        norm = torch.sum(torch.abs(self.input_lst)**2)
        input_lst = (1.0 / torch.sqrt(norm)) * self.input_lst
        state = torch.zeros([2**self.nqubits]) + 0j
        state[:num] = input_lst
        return state + 0j
class qmlp_2qbit(torch.nn.Module):
    def __init__(self, num_paras=28*6, gain=2**0.5, use_wscale=True, lrmul=1):
        super(qmlp_2qbit, self).__init__()
        he_std = gain * 5**(-0.5)
        if use_wscale:
            init_std = 1.0 / lrmul
            self.w_mul = he_std * lrmul
        else:
            init_std = he_std / lrmul
            self.w_mul = lrmul
        self.weight = nn.Parameter(nn.init.uniform_(torch.empty(num_paras), a=0.0, b=2 * np.pi) * init_std)
    def reset_parameters(self):
        nn.init.uniform_(self.weight, a=0.0, b=2 * np.pi)
    def cir_2qbit(self, para_list):
        cir = circuits.circuit.Circuit()
        cir.rx(0, para_list[0])
        cir.ry(0, para_list[1])
        cir.rz(0, para_list[2])
        cir.rx(0, para_list[3])
        cir.ry(0, para_list[4])
        cir.rz(0, para_list[5])
        cir.cnot(1, 0)
        cir.cnot(0, 1)
        U = cir.to_unitary()
        return torch.tensor(U).reshape([4, 4])
    def forward(self, x):
        x_mini_sets = get_8qbit_ptrace_set(x)
        out = torch.empty(0)
        for item in range(len(x_mini_sets)):
            x_item = x_mini_sets[item]
            para_idx = self.weight[0 + item*6:6 + item*6]
            apply_u = self.cir_2qbit(para_idx)
            apply_u = apply_u.to(torch.complex128)
            x_item = x_item.to(torch.complex128)
            x_qml = apply_u @ x_item @ dag(apply_u)
            out_item = simu_expecval_2qbit(x_qml)
            out_item = out_item.reshape(1).to(torch.float32)
            out = torch.cat([out, out_item])
        return out
class Quantum_GCNConv_Embedding(MessagePassing):
    def __init__(self, normalize=True, improved=False, add_self_loops=True, bias=False):
        super(Quantum_GCNConv_Embedding, self).__init__(aggr='add')
        self.normalize = normalize
        self.improved = improved
        self.add_self_loops = add_self_loops
        self.bias = bias
        self.qmlp = qmlp_2qbit()
        if bias:
            self.bias = Parameter(torch.Tensor(in_channels))
        self.reset_parameters()
    def reset_parameters(self):
        self.qmlp.reset_parameters()
        zeros(self.bias)
    def forward(self, x: Tensor, edge_index: Adj, edge_weight: OptTensor = None) -> Tensor:
        if self.normalize:
            edge_index, edge_weight = gcn_norm(edge_index, edge_weight, x.size(self.node_dim), self.improved, self.add_self_loops)
        x_deal = torch.empty(0)
        for item in x:
            item_qvector = AmplitudeEncoding(8, item).encoded_state()
            item_qvector = item_qvector.reshape([256, 1])
            item_dm = item_qvector @ item_qvector.conj().T
            item_qml = self.qmlp(item_dm)
            x_deal = torch.cat([x_deal, item_qml], dim=0)
        x_deal = x_deal.reshape([len(x), 28])
        out = self.propagate(edge_index, x=x_deal, edge_weight=edge_weight)
        if self.bias is not None:
            out += self.bias
        return out
    def message(self, x_j: Tensor, edge_weight: OptTensor):
        return x_j if edge_weight is None else edge_weight.view(-1, 1) * x_j
class Quantum_GCNConv(nn.Module):
    def __init__(self, graphx_dim=None):
        super(Quantum_GCNConv, self).__init__()
        self.graphnn = Quantum_GCNConv_Embedding()
        self.linear = nn.Linear(28*28, 128)
        self.property_map = nn.Linear(128, 1)
    def get_embeddings_outputs(self, graph_x, graph_edge):
        out = self.graphnn(graph_x, graph_edge)
        out = F.relu(out)
        out = (out.T @ out).reshape([1, 28*28])
        out = self.linear(out)
        return F.relu(out)
    def forward(self, graph_x, graph_edge):
        out = self.get_embeddings_outputs(graph_x, graph_edge)
        out = self.property_map(out)
        return F.sigmoid(out)
pyg_method = GraphEncoder_MSRL()
ddsmi = pd.read_csv('YOUR_PATH.csv')
X_train, X_test, y_train, y_test = train_test_split(smi_with_MSRL, label_with_MSRL, test_size=0.9, random_state=42)
model = Quantum_GCNConv()
optimizer = optim.SGD(model.parameters(), lr=0.01)
criterion = torch.nn.MSELoss()
# Model Training
def train_model(model, optimizer, criterion, X_train, y_train, epochs=10):
    model.train()
    total_loss = 0
    for epoch in range(epochs):
        for idx in tqdm(range(len(X_train))):
            mol = X_train[idx]
            graphx, graph_edge = get_gin_input(mol)
            pred_label = model(graphx, graph_edge)
            y = torch.tensor(y_train[idx]).to(torch.float32).reshape([1, 1])
            loss = criterion(pred_label, y)         
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()       
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss / len(X_train):.4f}")
# Model Evaluation
def evaluate_model(model, X_test, y_test):
    model.eval()
    y_pred = []
    with torch.no_grad():
        for mol in tqdm(X_test):
            graphx, graph_edge = get_gin_input(mol)
            pred_label = model(graphx, graph_edge)
            pred_label = (pred_label > 0.5).float().detach().numpy()
            y_pred.append(pred_label)
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Accuracy Score:", accuracy_score(y_test, y_pred))
# Main function to execute everything
def main():
    # Load data
    smi_with_MSRL = pd.read_csv('YOUR_PATH.csv')['SMILES']
    label_with_MSRL = pd.read_csv('YOUR_PATH.csv')['Labels']  
    X_train, X_test, y_train, y_test = train_test_split(smi_with_MSRL, label_with_MSRL, test_size=0.9, random_state=42)  
    # Initialize model, optimizer, and loss function
    model = Quantum_GCNConv()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    criterion = torch.nn.MSELoss()    
    # Train the model
    train_model(model, optimizer, criterion, X_train, y_train, epochs=10)   
    # Evaluate the model
    evaluate_model(model, X_test, y_test)   
    # Save the model
    torch.save(model.state_dict(), 'QuantumGCNEmbedding_model_weights.pth')
if __name__ == "__main__":
    main()