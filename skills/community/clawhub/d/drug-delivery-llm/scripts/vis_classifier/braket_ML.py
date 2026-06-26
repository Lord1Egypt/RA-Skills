import numpy as np
import pandas as pd
import torch
from torch import tensor, nn
from torch.nn import Linear, BCELoss
from torch.nn.functional import relu, sigmoid
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.neural_network import MLPClassifier
from evalmole import get_mol, get_mol_set, get_128fp_set
from braket import circuits
df = pd.read_csv('classification_dataset/XY-c2.csv')
X = df['X']
Y = df['Y']
X_, Y_ = [], []
for i in range(len(X)):
    smi = X[i]
    y_ = Y[i]
    try:
        _ = get_mol(smi)
        X_.append(smi)
        Y_.append(y_)
    except:
        print('i')  # Invalid molecule
        pass
X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X_, Y_, test_size=0.2, random_state=42
)
xmol1 = get_mol_set(X_train2)
xfp1 = get_128fp_set(xmol1)
xmol2 = get_mol_set(X_test2)
xfp2 = get_128fp_set(xmol2)
class TorchMLP(nn.Module):
    def __init__(self, x_shape=128):
        super().__init__()
        self.h1 = Linear(x_shape, 512)
        self.h2 = Linear(512, 32)
        self.h3 = Linear(32, 1)
    def forward(self, x):
        x = relu(self.h1(x))
        x = relu(self.h2(x))
        x = sigmoid(self.h3(x))
        return x
xx = tensor(xfp1).to(torch.float32)
yy = tensor(y_train2).float().unsqueeze(1)
train_dataset = TensorDataset(xx, yy)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
mlp_t = TorchMLP()
criterion = BCELoss()
optimizer = Adam(mlp_t.parameters(), lr=0.001)
epochs = 20
for epoch in range(epochs):
    mlp_t.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        outputs = mlp_t(X_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_loader):.4f}")
xfp2_tensor = tensor(xfp2).to(torch.float32)
y_pred_tensor = mlp_t(xfp2_tensor)
y_pred = (y_pred_tensor > 0.5).float()
print("\nClassification Report - Classical MLP:\n")
print(classification_report(y_test2, y_pred))
print("Accuracy Score: ", accuracy_score(y_test2, y_pred))
def expecval_ZI(state, nqubit, target):
    zgate = z_gate()
    H = gate_expand_1toN(zgate, nqubit, target)
    expecval = (state @ H).trace()
    return (expecval.real + 1) / 2
def simu_expecval(state):
    cir = circuits.circuit.Circuit()
    cir.i(0)
    cir.z(1)
    H = torch.tensor(cir.to_unitary())
    expecval = torch.trace(state @ H)
    return (expecval.real + 1) / 2
 class QFPNN(nn.Module):
    def __init__(self, xshape=128, gain=2 ** 0.5, use_wscale=True, lrmul=1):
        super().__init__()
        he_std = gain * 5 ** (-0.5)
        init_std = 1.0 / lrmul if use_wscale else he_std / lrmul
        self.weight = nn.Parameter(
            nn.init.uniform_(torch.empty(xshape), a=0.0, b=2 * np.pi) * init_std
        )
    def encode_cir_0(self, para):
        cir = circuits.circuit.Circuit()
        cir.x(0)
        cir.cnot(1, 0)
        cir.rz(1, para)
        return torch.tensor(cir.to_unitary())
    def encode_cir_1(self, para):
        cir = circuits.circuit.Circuit()
        cir.y(0)
        cir.cnot(1, 0)
        cir.rz(1, para)
        return torch.tensor(cir.to_unitary())
    def simu_expecval(self, state):
        cir = circuits.circuit.Circuit()
        cir.i(0)
        cir.z(1)
        H = torch.tensor(cir.to_unitary())
        expecval = (state @ H).trace()
        return (expecval.real + 2) / 4
    def forward(self, x):
        out = torch.empty(0)
        for indx in range(len(x)):
            elem = x[indx]
            control_para = self.weight[indx]
            u = self.encode_cir_0(control_para) if elem == 0 else self.encode_cir_1(control_para)
            val = self.simu_expecval(u).reshape(1).to(torch.float32)
            out = torch.cat([out, val])
        return out
class QFPNN_Batch(nn.Module):
    def __init__(self, xshape=128, gain=2 ** 0.5, use_wscale=True, lrmul=1):
        super().__init__()
        he_std = gain * 5 ** (-0.5)
        init_std = 1.0 / lrmul if use_wscale else he_std / lrmul
        self.weight = nn.Parameter(
            nn.init.uniform_(torch.empty(xshape), a=0.0, b=2 * np.pi) * init_std
        )
    def encode_cir_0(self, para):
        cir = circuits.circuit.Circuit()
        cir.x(0)
        cir.cnot(1, 0)
        cir.rz(1, para)
        return torch.tensor(cir.to_unitary())
    def encode_cir_1(self, para):
        cir = circuits.circuit.Circuit()
        cir.y(0)
        cir.cnot(1, 0)
        cir.rz(1, para)
        return torch.tensor(cir.to_unitary())
    def simu_expecval(self, state):
        cir = circuits.circuit.Circuit()
        cir.i(0)
        cir.z(1)
        H = torch.tensor(cir.to_unitary())
        expecval = (state @ H).trace()
        return (expecval.real + 2) / 4
    def forward(self, x):
        batch_size, seq_length = x.shape
        out = torch.empty(batch_size, seq_length, dtype=torch.float32)
        for b in range(batch_size):
            for i in range(seq_length):
                val = x[b, i]
                para = self.weight[i]
                u = self.encode_cir_0(para) if val == 0 else self.encode_cir_1(para)
                out[b, i] = self.simu_expecval(u).to(torch.float32)
        return out
class QuantumMLP(nn.Module):
    def __init__(self, x_shape=128):
        super().__init__()
        self.h1 = QFPNN_Batch(x_shape)
        self.h2 = Linear(128, 32)
        self.h3 = Linear(32, 1)
    def forward(self, x):
        x = relu(self.h1(x))
        print(x.shape)  # For debugging
        x = relu(self.h2(x))
        x = sigmoid(self.h3(x))
        return x
qq_batch = QuantumMLP()
xx = tensor(xfp1).to(torch.float32)
yy = tensor(y_train2).float().unsqueeze(1)
train_dataset = TensorDataset(xx, yy)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
criterion = BCELoss()
optimizer = Adam(qq_batch.parameters(), lr=0.001)
for epoch in range(epochs):
    qq_batch.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        outputs = qq_batch(X_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(train_loader):.4f}")

xfp2_tensor = tensor(xfp2).to(torch.float32)
y_pred_tensor = qq_batch(xfp2_tensor)
y_pred = (y_pred_tensor > 0.5).float()
print("\nClassification Report - Quantum MLP:\n")
print(classification_report(y_test2, y_pred))
print("Accuracy Score: ", accuracy_score(y_test2, y_pred))