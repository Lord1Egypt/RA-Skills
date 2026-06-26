import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from torch.nn import BCELoss
import torch.nn.functional as F
from GINEmbedding_with_Molecular_Set_Representation_Learning.GNNmodel import GINEmbedding
from graph_process.graph_encoder import GraphEncoder_MSRL_BLIP
# Load and preprocess data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    X = df['X']
    Y = df['Y']
    return X, Y
# Prepare graph input for GIN model
def get_gin_input(seq, pyg_method):
    nx_data = pyg_method.smiles_to_nx(seq)
    pyg_data = pyg_method.nx_to_pyg(nx_data)
    return pyg_data.x, pyg_data.edge_index
# Define the GINE model
class GINE_(torch.nn.Module):
    def __init__(self, graphx_dim=133, hidden_dim=64, output_dim=128):
        super(GINE_, self).__init__()
        self.graphnn_64_128 = GINEmbedding(input_dim=graphx_dim, hidden_dim=hidden_dim, output_dim=output_dim)
        self.linear = torch.nn.Linear(output_dim, output_dim) 
        self.property_map = torch.nn.Linear(output_dim, 1)
    def get_GINEmbedding(self, graph_x, graph_edge):
        embedding = self.graphnn_64_128(graph_x, graph_edge)
        embedding = F.relu(embedding)
        embedding = self.linear(embedding)
        return F.relu(embedding)  
    def forward(self, graph_x, graph_edge):
        out = self.get_GINEmbedding(graph_x, graph_edge)
        out = self.property_map(out)
        return F.sigmoid(out)
# Training the model
def train_model(model, optimizer, criterion, X_train, y_train, epochs=10):
    model.train()
    epoch_loss_list = []
    yy_train = torch.tensor(y_train).to(torch.float32) 
    for epoch in range(epochs):
        total_loss = 0
        for idx in tqdm(range(len(X_train))):
            mol = X_train[idx]
            node_features, edge_index = get_gin_input(mol, pyg_method)
            outputs = model(node_features, edge_index)
            y_label = yy_train[idx].reshape([1])
            
            loss_fn = criterion(outputs, y_label)
            optimizer.zero_grad()
            loss_fn.backward()
            optimizer.step()
            total_loss += loss_fn.item()      
        epoch_loss = total_loss / len(X_train)
        epoch_loss_list.append(epoch_loss)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {epoch_loss:.4f}")   
    return epoch_loss_list
# Evaluate the model
def evaluate_model(model, X_test, y_test):
    model.eval()
    y_pred = []
    yy_test = torch.tensor(y_test).to(torch.float32)
    with torch.no_grad():
        for mol in tqdm(X_test):
            graphx, graph_edge = get_gin_input(mol, pyg_method)
            pred_label = model(graphx, graph_edge)
            pred_label = (pred_label > 0.5).float().detach().numpy()
            y_pred.append(pred_label)
    print("Classification Report:\n", classification_report(yy_test, y_pred))
    print("Accuracy Score:", accuracy_score(yy_test, y_pred))
# Main function to orchestrate training and evaluation
def main():
    # Load data
    X, Y = load_data('../classification_dataset/XY-c2.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    # Initialize model, optimizer, and loss function
    pyg_method = GraphEncoder_MSRL_BLIP()
    model = GINE_()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = BCELoss()
    # Train the model
    train_model(model, optimizer, criterion, X_train, y_train, epochs=10)
    # Evaluate the model
    evaluate_model(model, X_test, y_test)
if __name__ == "__main__":
    main()