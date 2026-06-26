# Deep Learning Models for Electricity Forecasting

## Overview

Deep learning models excel at capturing complex temporal patterns in electricity load data, especially when you have:
- Large datasets (>2 years of hourly data)
- Multiple input features (weather, calendar, etc.)
- Need for uncertainty quantification
- Multi-horizon forecasting requirements

## Model Architectures

### 1. LSTM (Long Short-Term Memory)

**Best for**: Sequential pattern recognition, moderate dataset sizes

```python
import torch
import torch.nn as nn

class LSTMForecaster(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.fc = nn.Linear(hidden_size, 1)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x):
        # x: (batch, seq_len, features)
        lstm_out, _ = self.lstm(x)
        out = lstm_out[:, -1, :]  # Take last timestep
        out = self.dropout(out)
        out = self.fc(out)
        return out

# Training configuration
model = LSTMForecaster(input_size=20, hidden_size=64, num_layers=2)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

**Key hyperparameters**:
- `hidden_size`: 32-128 (start with 64)
- `num_layers`: 1-3 (deeper doesn't always help)
- `dropout`: 0.1-0.3
- `sequence_length`: 24-168 timesteps (1 day to 1 week)

**Pros**:
- Captures long-term dependencies
- Well-understood, stable training
- Good baseline for deep learning

**Cons**:
- Sequential computation (slow training)
- Can struggle with very long sequences
- Less interpretable than attention models

### 2. GRU (Gated Recurrent Unit)

**Best for**: Similar to LSTM but faster training

```python
class GRUForecaster(nn.Module):
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )
        self.fc = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        gru_out, _ = self.gru(x)
        out = self.fc(gru_out[:, -1, :])
        return out
```

**Comparison with LSTM**:
- Fewer parameters (faster training)
- Similar accuracy in most cases
- Less memory intensive

### 3. Transformer for Time Series

**Best for**: Long sequences, parallel training, attention interpretability

```python
import torch.nn.functional as F

class TransformerForecaster(nn.Module):
    def __init__(self, input_size, d_model=64, nhead=4, num_layers=3, 
                 dim_feedforward=128, dropout=0.1, max_seq_len=168):
        super().__init__()
        
        # Input embedding
        self.input_projection = nn.Linear(input_size, d_model)
        
        # Positional encoding
        self.pos_encoder = PositionalEncoding(d_model, dropout, max_seq_len)
        
        # Transformer encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output head
        self.fc = nn.Linear(d_model, 1)
    
    def forward(self, x):
        # x: (batch, seq_len, features)
        x = self.input_projection(x)
        x = self.pos_encoder(x)
        x = self.transformer(x)
        out = self.fc(x[:, -1, :])  # Predict next timestep
        return out

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=500):
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-np.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        x = x + self.pe[:x.size(0)]
        return self.dropout(x)
```

**Key hyperparameters**:
- `d_model`: 32-128
- `nhead`: 4-8 (must divide d_model)
- `num_layers`: 2-6
- `dim_feedforward`: 2-4 × d_model

**Pros**:
- Parallel training (much faster than LSTM)
- Attention weights provide interpretability
- Excellent for long sequences

**Cons**:
- Requires more data
- More hyperparameters to tune
- Can overfit on small datasets

### 4. Temporal Fusion Transformer (TFT)

**Best for**: Production multi-horizon forecasting with interpretability

TFT is a state-of-the-art architecture specifically designed for time series forecasting with:
- Multi-horizon predictions
- Static and time-varying features
- Interpretable attention mechanisms
- Built-in uncertainty quantification

```python
# Using PyTorch Forecasting library
from pytorch_forecasting import TemporalFusionTransformer, TimeSeriesDataSet

# Prepare dataset
training = TimeSeriesDataSet(
    data[lambda x: x.time_idx <= cutoff],
    time_idx="time_idx",
    target="load",
    group_ids=["series_id"],  # For multi-series
    time_varying_known_reals=["hour_sin", "hour_cos", "temperature", "is_holiday"],
    time_varying_unknown_reals=["lag_1h", "lag_24h", "rolling_mean_24h"],
    static_categoricals=["region_id"],  # Optional
    static_reals=["avg_load"],  # Optional
    max_encoder_length=168,  # 1 week history
    max_prediction_length=24,  # 24h forecast
    target_normalizer=GroupNormalizer(groups=["series_id"]),
)

# Create model
tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.001,
    hidden_size=32,
    attention_head_size=4,
    dropout=0.1,
    hidden_continuous_size=8,
    output_size=7,  # Quantiles: 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99
    loss=QuantileLoss(),
    reduction="mean",
)

# Train
train_dataloader = training.to_dataloader(train=True, batch_size=64)
val_dataloader = training.to_dataloader(train=False, batch_size=64)

trainer = pl.Trainer(
    max_epochs=100,
    gradient_clip_val=0.1,
    early_stop_callback=True,
    enable_progress_bar=True,
)

trainer.fit(
    tft,
    train_dataloaders=train_dataloader,
    val_dataloaders=val_dataloader,
)
```

**Key features**:
- **Variable selection networks**: Automatically learn which features matter
- **Interpretable multi-head attention**: See which timesteps the model attends to
- **Gating mechanisms**: Skip unnecessary components
- **Quantile outputs**: Native uncertainty quantification

**Interpretability outputs**:
```python
# Get feature importances
interpretation = tft.interpret(val_dataloader, mode="variables")
tft.plot_interpretation(interpretation)

# Get attention weights
attention = tft.attention(val_dataloader, mode="attention")
tft.plot_attention(attention)
```

**Pros**:
- State-of-the-art accuracy
- Built-in interpretability
- Multi-horizon in single model
- Native uncertainty quantification

**Cons**:
- Complex implementation
- Longer training time
- More hyperparameters

### 5. N-BEATS (Neural Basis Expansion Analysis)

**Best for**: Pure deep learning baseline, interpretable decomposition

```python
from pytorch_forecasting import NBeats

nbeats = NBeats.from_dataset(
    training,
    learning_rate=0.001,
    stack_types=["trend", "seasonality"],
    nb_blocks=3,
    widths=[32, 512],
    sharing=[True, False],
    expansion_coefficient_lengths=[3, 7],
    prediction_length=24,
    context_length=168,
)
```

**Architecture insight**: N-BEATS decomposes forecast into:
- **Trend component**: Long-term direction
- **Seasonality component**: Repeating patterns

**Pros**:
- Strong baseline performance
- Interpretable decomposition
- Simpler than Transformer

**Cons**:
- Less flexible than TFT
- No native uncertainty

### 6. iTransformer (2023-2024 SOTA)

**Best for**: Best-in-class accuracy, research/production hybrid

iTransformer inverts the standard Transformer architecture:
- Applies attention on **features** instead of time dimension
- Better captures multivariate correlations
- State-of-the-art on many benchmarks

```python
# Using iTransformer implementation
class iTransformer(nn.Module):
    def __init__(self, seq_len, pred_len, features, d_model=512, n_heads=8, 
                 e_layers=3, dropout=0.1):
        super().__init__()
        self.seq_len = seq_len
        self.pred_len = pred_len
        
        # Embedding per feature
        self.embeddings = nn.ModuleList([
            nn.Linear(1, d_model) for _ in range(features)
        ])
        
        # Transformer on feature dimension
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_model*4,
            dropout=dropout,
            batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=e_layers)
        
        # Output projection
        self.projection = nn.Linear(seq_len, pred_len)
    
    def forward(self, x):
        # x: (batch, seq_len, features)
        x = x.permute(0, 2, 1)  # (batch, features, seq_len)
        
        # Embed each feature
        embedded = []
        for i, emb in enumerate(self.embeddings):
            embedded.append(emb(x[:, i:i+1, :].unsqueeze(-1)).squeeze(-1))
        x = torch.stack(embedded, dim=1)  # (batch, features, d_model)
        
        # Transformer on features
        x = self.encoder(x)
        
        # Project to prediction length
        x = self.projection(x)  # (batch, features, pred_len)
        x = x.permute(0, 2, 1)  # (batch, pred_len, features)
        
        return x
```

**Pros**:
- Current SOTA on many benchmarks
- Efficient multivariate modeling
- Good for long sequences

**Cons**:
- Recent architecture (less battle-tested)
- Requires careful tuning

## Training Best Practices

### Data Preparation

```python
class TimeSeriesDataset(Dataset):
    def __init__(self, data, seq_len, pred_len, stride=1):
        self.data = data
        self.seq_len = seq_len
        self.pred_len = pred_len
        self.stride = stride
        
        # Calculate number of samples
        self.n_samples = (len(data) - seq_len - pred_len) // stride + 1
    
    def __len__(self):
        return self.n_samples
    
    def __getitem__(self, idx):
        start = idx * self.stride
        end = start + self.seq_len + self.pred_len
        
        x = self.data[start:start + self.seq_len]
        y = self.data[start + self.seq_len:end]
        
        return torch.FloatTensor(x), torch.FloatTensor(y)

# Create datasets
train_dataset = TimeSeriesDataset(train_data, seq_len=168, pred_len=24)
val_dataset = TimeSeriesDataset(val_data, seq_len=168, pred_len=24)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=64, shuffle=False)
```

### Normalization Strategies

```python
from sklearn.preprocessing import RobustScaler, StandardScaler

# Option 1: Global normalization (simplest)
scaler = RobustScaler()
train_scaled = scaler.fit_transform(train_data)
test_scaled = scaler.transform(test_data)

# Option 2: Per-series normalization (for multi-site)
scalers = {}
for site in sites:
    scalers[site] = RobustScaler()
    train_data[site] = scalers[site].fit_transform(train_data[site])

# Option 3: Target normalization only (for deep learning)
target_scaler = StandardScaler()
y_train_scaled = target_scaler.fit_transform(y_train.reshape(-1, 1))
```

### Training Loop with Early Stopping

```python
def train_model(model, train_loader, val_loader, epochs=100, patience=10):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5
    )
    
    best_val_loss = float('inf')
    patience_counter = 0
    best_model_state = None
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
            optimizer.zero_grad()
            pred = model(X_batch)
            loss = criterion(pred, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            
            train_loss += loss.item()
        
        train_loss /= len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                pred = model(X_batch)
                val_loss += criterion(pred, y_batch).item()
        
        val_loss /= len(val_loader)
        scheduler.step(val_loss)
        
        print(f"Epoch {epoch+1}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}")
        
        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_model_state = model.state_dict().copy()
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping at epoch {epoch+1}")
                break
    
    # Load best model
    model.load_state_dict(best_model_state)
    return model
```

### Hyperparameter Tuning with Optuna

```python
import optuna

def objective(trial):
    # Suggest hyperparameters
    hidden_size = trial.suggest_categorical('hidden_size', [32, 64, 128, 256])
    num_layers = trial.suggest_int('num_layers', 1, 4)
    dropout = trial.suggest_float('dropout', 0.1, 0.3)
    learning_rate = trial.suggest_float('lr', 1e-4, 1e-2, log=True)
    
    # Create model
    model = LSTMForecaster(
        input_size=20,
        hidden_size=hidden_size,
        num_layers=num_layers,
        dropout=dropout
    )
    
    # Train (simplified)
    val_loss = quick_train_and_evaluate(model, learning_rate)
    
    return val_loss

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=50, timeout=3600)

print(f"Best params: {study.best_params}")
print(f"Best val loss: {study.best_value}")
```

## Uncertainty Quantification

### Quantile Regression

```python
class QuantileLoss(nn.Module):
    def __init__(self, quantiles):
        super().__init__()
        self.quantiles = quantiles
    
    def forward(self, preds, target):
        losses = []
        for i, q in enumerate(self.quantiles):
            errors = target - preds[:, i]
            losses.append(torch.max((q - 1) * errors, q * errors))
        return torch.mean(torch.sum(torch.cat(losses, dim=1), dim=1))

# Model with multiple quantile outputs
class QuantileForecaster(nn.Module):
    def __init__(self, input_size, n_quantiles=7):
        super().__init__()
        self.lstm = nn.LSTM(input_size, 64, 2, batch_first=True)
        self.fc = nn.Linear(64, n_quantiles)
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

# Quantiles: 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99
quantiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
model = QuantileForecaster(input_size=20, n_quantiles=len(quantiles))
criterion = QuantileLoss(quantiles)
```

### Monte Carlo Dropout

```python
def predict_with_uncertainty(model, x, n_samples=50):
    """Use MC dropout to estimate prediction uncertainty."""
    model.train()  # Enable dropout
    predictions = []
    
    with torch.no_grad():
        for _ in range(n_samples):
            pred = model(x)
            predictions.append(pred)
    
    predictions = torch.stack(predictions)
    mean = predictions.mean(dim=0)
    std = predictions.std(dim=0)
    
    model.eval()
    return mean, std

# Usage
mean_pred, uncertainty = predict_with_uncertainty(model, test_data)
confidence_interval_95 = (mean_pred - 1.96 * uncertainty, mean_pred + 1.96 * uncertainty)
```

## Model Comparison Summary

| Model | Data Required | Training Time | Accuracy | Uncertainty | Interpretability | Production Ready |
|-------|--------------|---------------|----------|-------------|------------------|------------------|
| LSTM | >1 year | Medium | Good | MC Dropout | Low | Yes |
| GRU | >1 year | Medium-Fast | Good | MC Dropout | Low | Yes |
| Transformer | >2 years | Fast | Very Good | Attention | Medium | Yes |
| TFT | >2 years | Slow | Excellent | Native | High | Yes |
| N-BEATS | >1 year | Medium | Very Good | No | Medium | Yes |
| iTransformer | >2 years | Fast | SOTA | No | Low | Emerging |

## Recommended Starting Points

**For production STLF**:
```
Start with: LightGBM (fast, accurate)
Upgrade to: TFT (if you need uncertainty + interpretability)
```

**For research/SOTA**:
```
Start with: iTransformer or TFT
Ensemble with: LightGBM + SARIMA
```

**For limited data**:
```
Start with: SARIMA or simple LSTM
Avoid: Large Transformers
```
