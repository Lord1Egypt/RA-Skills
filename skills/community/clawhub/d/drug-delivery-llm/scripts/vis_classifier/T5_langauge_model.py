import pandas as pd
import torch
from torch import nn
from torch.optim import Adam
from transformers import T5ForConditionalGeneration
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from peft import LoraConfig, get_peft_model
from seq_process.seq_encoder import get_seq_token
from torch.nn.functional import relu, sigmoid
# 数据
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    X, Y = df['X'], df['Y']
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
    return X_train, X_test, y_train, y_test
# 初始化
def initialize_model():
    pre_trained_model_path = "laituan245/molt5-base"
    model = T5ForConditionalGeneration.from_pretrained(pre_trained_model_path)
    lora_config = LoraConfig(
        peft_type="LORA",
        r=16, lora_alpha=16, lora_dropout=0.1, bias="none",
        target_modules=["q", "v", "lm_head", "shared"]
    )
    language_model = get_peft_model(model, lora_config)
    class SimpleMLP(nn.Module):
        def __init__(self, input_size=768):
            super(SimpleMLP, self).__init__()
            self.fc1 = nn.Linear(input_size, 512)
            self.fc2 = nn.Linear(512, 32)
            self.fc3 = nn.Linear(32, 1)
        def forward(self, x):
            x = relu(self.fc1(x))
            x = relu(self.fc2(x))
            return sigmoid(self.fc3(x))
    class T5Classifier(nn.Module):
        def __init__(self):
            super(T5Classifier, self).__init__()
            self.model = T5ForConditionalGeneration.from_pretrained(pre_trained_model_path)
            self.language_model = get_peft_model(self.model, lora_config)
            self.mlp = SimpleMLP()
        def forward(self, seq_token):
            embeddings = self.language_model.encoder(seq_token).last_hidden_state
            return self.mlp(embeddings.mean(dim=1))
    model = T5Classifier()
    optimizer = Adam(model.parameters(), lr=0.001)
    criterion = nn.BCELoss()
    return model, optimizer, criterion
# 运行
def train_model(model, optimizer, criterion, X_train, y_train, epochs=20):
    model.train()
    y_train_tensor = torch.tensor(y_train.values).float()
    for epoch in range(epochs):
        total_loss = 0
        for idx in range(len(X_train)):
            seq_token = get_seq_token(X_train.iloc[idx])
            output = model(seq_token)
            loss = criterion(output, y_train_tensor[idx].reshape(1, 1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(X_train):.4f}")
# 评估
def evaluate_model(model, X_test, y_test):
    model.eval()
    y_pred = []
    with torch.no_grad():
        for idx in range(len(X_test)):
            seq_token = get_seq_token(X_test.iloc[idx])
            pred = model(seq_token)
            y_pred.append((pred > 0.5).float().item())
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Accuracy Score:", accuracy_score(y_test, y_pred))
def main():
    # Load data
    X_train, X_test, y_train, y_test = load_data('classification_dataset/XY-c2.csv')
    model, optimizer, criterion = initialize_model()
    train_model(model, optimizer, criterion, X_train, y_train, epochs=1)
    evaluate_model(model, X_test, y_test)
if __name__ == "__main__":
    main()