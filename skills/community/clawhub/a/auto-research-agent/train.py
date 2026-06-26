#!/usr/bin/env python3
"""
Autonomous Research - Example Train.py
这是Agent可以修改的实验文件
默认是一个简单的GPT-like模型
"""

import torch
import torch.nn as nn
import numpy as np

# ========== 可修改的配置 ==========
CONFIG = {
    # 模型参数
    "vocab_size": 512,
    "seq_len": 128,
    "hidden_dim": 128,
    "num_layers": 3,
    "num_heads": 4,
    "dropout": 0.1,
    
    # 训练参数
    "batch_size": 32,
    "learning_rate": 1e-3,
    "weight_decay": 0.01,
    "epochs": 10,
    
    # 评估指标
    "metric": "val_loss",
}

# ========== 简单的Transformer模型 ==========
class TinyTransformer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        self.embedding = nn.Embedding(config["vocab_size"], config["hidden_dim"])
        self.pos_embedding = nn.Embedding(config["seq_len"], config["hidden_dim"])
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=config["hidden_dim"],
            nhead=config["num_heads"],
            dim_feedforward=config["hidden_dim"] * 4,
            dropout=config["dropout"],
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=config["num_layers"])
        self.lm_head = nn.Linear(config["hidden_dim"], config["vocab_size"])
        
        # 权重共享
        self.lm_head.weight = self.embedding.weight
        
    def forward(self, x):
        B, T = x.shape
        pos = torch.arange(T, device=x.device).unsqueeze(0)
        x = self.embedding(x) + self.pos_embedding(pos)
        x = self.transformer(x)
        logits = self.lm_head(x)
        return logits
    
    @property
    def num_params(self):
        return sum(p.numel() for p in self.parameters())


def generate_random_data(config, num_samples=1000):
    """生成随机训练数据"""
    vocab_size = config["vocab_size"]
    seq_len = config["seq_len"]
    
    X = torch.randint(0, vocab_size, (num_samples, seq_len))
    y = torch.randint(0, vocab_size, (num_samples, seq_len))
    
    return X, y


def train_epoch(model, X, y, optimizer, config):
    """训练一个epoch"""
    model.train()
    total_loss = 0
    num_batches = 0
    
    criterion = nn.CrossEntropyLoss()
    
    for i in range(0, len(X), config["batch_size"]):
        batch_x = X[i:i+config["batch_size"]]
        batch_y = y[i:i+config["batch_size"]]
        
        optimizer.zero_grad()
        logits = model(batch_x)
        loss = criterion(logits.view(-1, config["vocab_size"]), batch_y.view(-1))
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        num_batches += 1
    
    return total_loss / num_batches


@torch.no_grad()
def evaluate(model, X, y, config):
    """评估模型"""
    model.eval()
    criterion = nn.CrossEntropyLoss()
    
    total_loss = 0
    num_batches = 0
    
    for i in range(0, len(X), config["batch_size"]):
        batch_x = X[i:i+config["batch_size"]]
        batch_y = y[i:i+config["batch_size"]]
        
        logits = model(batch_x)
        loss = criterion(logits.view(-1, config["vocab_size"]), batch_y.view(-1))
        total_loss += loss.item()
        num_batches += 1
    
    return total_loss / num_batches


def run_experiment():
    """运行实验"""
    print("=" * 50)
    print("Autonomous Research Experiment")
    print("=" * 50)
    print(f"\nConfiguration:")
    for k, v in CONFIG.items():
        print(f"  {k}: {v}")
    
    # 设置设备
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\nDevice: {device}")
    
    # 生成数据
    print("\nGenerating data...")
    train_X, train_y = generate_random_data(CONFIG, num_samples=5000)
    val_X, val_y = generate_random_data(CONFIG, num_samples=500)
    
    train_X, train_y = train_X.to(device), train_y.to(device)
    val_X, val_y = val_X.to(device), val_y.to(device)
    
    # 初始化模型
    model = TinyTransformer(CONFIG).to(device)
    print(f"\nModel parameters: {model.num_params:,}")
    
    # 优化器
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=CONFIG["learning_rate"],
        weight_decay=CONFIG["weight_decay"]
    )
    
    # 训练循环
    print("\nTraining...")
    best_val_loss = float('inf')
    
    for epoch in range(CONFIG["epochs"]):
        train_loss = train_epoch(model, train_X, train_y, optimizer, CONFIG)
        val_loss = evaluate(model, val_X, val_y, CONFIG)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            marker = " ✅"
        else:
            marker = ""
        
        print(f"  Epoch {epoch+1}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}{marker}")
    
    print(f"\n{'=' * 50}")
    print(f"Best val_loss: {best_val_loss:.4f}")
    print(f"{'=' * 50}")
    
    return {
        "config": CONFIG.copy(),
        "best_val_loss": best_val_loss,
        "num_params": model.num_params,
    }


if __name__ == "__main__":
    run_experiment()
