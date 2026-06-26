import pandas as pd
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from peft import LoraConfig, get_peft_model
from transformers import T5ForConditionalGeneration, Blip2ForConditionalGeneration, Blip2Config
from graph_process.graph_encoder import GraphEncoder_MSRL_BLIP
from seq_process.seq_encoder import get_seq_token
from torch_geometric.nn import GINConv
from torch.nn import TransformerEncoder, TransformerEncoderLayer
# Load and prepare data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    X, Y = df['X'], df['Y']
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test
# Prepare graph input for GIN model
def get_gin_input(seq, pyg_method):
    nx_data = pyg_method.smiles_to_nx(seq)
    pyg_data = pyg_method.nx_to_pyg(nx_data)
    return pyg_data.x, pyg_data.edge_index
# Combined initialization of graph and T5 models
def initialize_models(pre_trained_model_path='laituan245/molt5-base',
                      pre_trained_graph_path='model_embedding_epoch_25_AS_9544.pth',
                      drug_lora_config):
    # Initialize Graph Encoder
    graph_model = GINE_()
    graph_model.load_state_dict(torch.load(pre_trained_graph_path)) 
    # Initialize T5 model with PEFT
    drug_model = T5ForConditionalGeneration.from_pretrained(pre_trained_model_path)
    language_model = get_peft_model(drug_model, drug_lora_config)    
    # Initialize BLIP2 model
    blip2conf = Blip2Config()
    blip2_model = Blip2ForConditionalGeneration(blip2conf)
    blip2_model.vision_model = None  # Disable vision model
    # Return initialized models
    return language_model, graph_model, blip2_model
# Model to fuse graph and drug embeddings
class BLIP_based_Graph_Classifier(nn.Module):
    def __init__(self, language_model, graph_model, blip2_model):
        super().__init__()
        self.model = blip2_model
        self.model.language_model = language_model
        self.model.graph_encoder = graph_model
        self.projection_graph = nn.Linear(128, 256)
        self.projection_drug = nn.Linear(768, 256)
        self.fusion_model = SelfAttentionFusion(d_model=256, nhead=8, num_layers=1, pool='avg')
        self.property_mlp = MLP(256, 128, 1)
    def get_embeddings_outputs(self, seq_token, graph_x, graph_edge):
        smiles_embeddings = self.model.language_model.encoder(seq_token).last_hidden_state
        features_drug = self.projection_drug(smiles_embeddings)
        graph_embeddings = self.model.graph_encoder.get_GINEmbedding(graph_x, graph_edge)
        graph_embeddings = graph_embeddings.reshape([1, 1, 128])
        features_graph = self.projection_graph(graph_embeddings)
        embeddings_outputs = self.fusion_model(features_drug, features_graph)
        return embeddings_outputs
    def forward(self, seq_token, graph_x, graph_edge):
        embeddings = self.get_embeddings_outputs(seq_token, graph_x, graph_edge)
        pred_label = self.property_mlp(embeddings)
        return pred_label
# Self-attention fusion layer
class SelfAttentionFusion(nn.Module):
    def __init__(self, d_model, nhead, num_layers, pool):
        super(SelfAttentionFusion, self).__init__()
        encoder_layers = TransformerEncoderLayer(d_model, nhead)
        self.transformer_encoder = TransformerEncoder(encoder_layers, num_layers)
        self.pool = pool    
    def forward(self, features_text, features_graph):
        features_text = features_text.transpose(0, 1)
        features_graph = features_graph.transpose(0, 1)
        sequence = torch.cat([features_text, features_graph], dim=0)
        output = self.transformer_encoder(sequence)
        output = output.transpose(0, 1).transpose(1, 2)
        if self.pool == 'avg':
            features = F.avg_pool1d(output, output.shape[2]).squeeze(2)
        else:
            features = F.max_pool1d(output, output.shape[2]).squeeze(2)
        return features
# MLP for final prediction
class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout_prob=0.5):
        super(MLP, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout_prob),
            nn.Linear(hidden_size, output_size)
        )
    def forward(self, x):
        return F.sigmoid(self.layers(x))
# Training loop
def train_model(model, optimizer, criterion, X_train, y_train, epochs=20):
    model.train()
    yy_ = torch.tensor(y_train).to(torch.float32)
    for epoch in range(epochs):
        total_loss = 0
        for idx_ in tqdm(range(len(X_train))):
            mol = X_train[idx_]
            seq_token = get_seq_token(mol)
            graphx, graph_edge = get_gin_input(mol, pyg_method)
            outputs = model(seq_token, graphx, graph_edge)
            y_label = yy_[idx_].reshape([1, 1])
            loss = criterion(outputs, y_label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(X_train):.4f}")
# Evaluation function
def evaluate_model(model, X_test, y_test):
    model.eval()
    yy_pred = []
    yy_true = torch.tensor(y_test).to(torch.float32)
    with torch.no_grad():
        for idx in tqdm(range(len(X_test))):
            mol = X_test[idx]
            seq_token = get_seq_token(mol)
            graphx, graph_edge = get_gin_input(mol, pyg_method)
            pred_label = model(seq_token, graphx, graph_edge)
            yy_pred.append(pred_label.item())
    # Compute metrics
    yy_pred = [1 if x > 0.5 else 0 for x in yy_pred]
    print("Classification Report:\n", classification_report(yy_true, yy_pred))
    print("Accuracy Score:", accuracy_score(yy_true, yy_pred))
# Main function to control flow
def main(csv_path):   
    # Load data
    X_train, X_test, y_train, y_test = load_data(csv_path)   
    # Define LoRA config
    drug_lora_config = LoraConfig(
        peft_type="LORA",
        r=16,
        lora_alpha=16,
        target_modules=["q", "v", "lm_head", "shared"],
        lora_dropout=0.1,
        bias="none"
    )   
    # Initialize models
    language_model, graph_model, blip2_model = initialize_models(drug_lora_config) 
    # Initialize BLIP-based Graph Classifier
    model = BLIP_based_Graph_Classifier(language_model, graph_model, blip2_model)  
    # Set up optimizer and loss function
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.BCEWithLogitsLoss()
    # Train the model
    train_model(model, optimizer, criterion, X_train, y_train, epochs=1)
    # Evaluate the model
    evaluate_model(model, X_test, y_test)
# Run the main function
if __name__ == "__main__":
    main('classification_dataset/XY-c2.csv')