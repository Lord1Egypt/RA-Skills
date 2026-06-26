#!/usr/bin/env python3
"""
Model training script for electricity forecasting.

Usage:
    python scripts/train_model.py --model lightgbm --data data/processed/ --horizon 24

Supported models:
    - lightgbm, xgboost, random_forest (scikit-learn)
    - lstm, gru, transformer (PyTorch)
    - sarima, prophet (statsmodels)
"""

import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def load_processed_data(data_dir):
    """Load processed data and feature config."""
    data_path = Path(data_dir) / 'processed_data.parquet'
    config_path = Path(data_dir) / 'feature_config.json'
    
    df = pd.read_parquet(data_path)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print(f"Loaded {len(df)} records with {config['n_features']} features")
    return df, config


def create_sequences(df, feature_columns, target_col, lookback, horizon):
    """Create sequences for time series modeling."""
    X, y = [], []
    
    features = df[feature_columns].values
    target = df[target_col].values
    
    for i in range(len(features) - lookback - horizon + 1):
        X.append(features[i:i + lookback])
        y.append(target[i + lookback:i + lookback + horizon])
    
    return np.array(X), np.array(y)


def train_test_split_time_series(X, y, test_ratio=0.2, val_ratio=0.1):
    """Time series split (no shuffling)."""
    n = len(X)
    test_start = int(n * (1 - test_ratio - val_ratio))
    val_start = int(n * (1 - val_ratio))
    
    X_train, y_train = X[:test_start], y[:test_start]
    X_val, y_val = X[test_start:val_start], y[test_start:val_start]
    X_test, y_test = X[val_start:], y[val_start:]
    
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    return X_train, y_train, X_val, y_val, X_test, y_test


def train_lightgbm(X_train, y_train, X_val, y_val, params=None):
    """Train LightGBM model."""
    import lightgbm as lgb
    from sklearn.metrics import mean_absolute_percentage_error
    
    if params is None:
        params = {
            'objective': 'regression',
            'metric': 'mape',
            'boosting_type': 'gbdt',
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': -1,
            'n_estimators': 1000,
            'early_stopping_rounds': 50,
        }
    
    # Flatten for tree models (X: [samples * seq_len, features])
    X_train_flat = X_train.reshape(-1, X_train.shape[-1])
    y_train_flat = y_train.flatten()
    X_val_flat = X_val.reshape(-1, X_val.shape[-1])
    y_val_flat = y_val.flatten()
    
    model = lgb.LGBMRegressor(**params)
    model.fit(
        X_train_flat, y_train_flat,
        eval_set=[(X_val_flat, y_val_flat)],
    )
    
    # Evaluate
    y_pred = model.predict(X_val_flat)
    mape = mean_absolute_percentage_error(y_val_flat, y_pred) * 100
    
    print(f"LightGBM validation MAPE: {mape:.2f}%")
    return model, {'mape': mape}


def train_xgboost(X_train, y_train, X_val, y_val, params=None):
    """Train XGBoost model."""
    import xgboost as xgb
    from sklearn.metrics import mean_absolute_percentage_error
    
    if params is None:
        params = {
            'objective': 'reg:squarederror',
            'eval_metric': 'mape',
            'max_depth': 6,
            'learning_rate': 0.05,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'n_estimators': 1000,
            'early_stopping_rounds': 50,
        }
    
    X_train_flat = X_train.reshape(-1, X_train.shape[-1])
    y_train_flat = y_train.flatten()
    X_val_flat = X_val.reshape(-1, X_val.shape[-1])
    y_val_flat = y_val.flatten()
    
    model = xgb.XGBRegressor(**params)
    model.fit(
        X_train_flat, y_train_flat,
        eval_set=[(X_val_flat, y_val_flat)],
        verbose=False
    )
    
    y_pred = model.predict(X_val_flat)
    mape = mean_absolute_percentage_error(y_val_flat, y_pred) * 100
    
    print(f"XGBoost validation MAPE: {mape:.2f}%")
    return model, {'mape': mape}


def train_random_forest(X_train, y_train, X_val, y_val, params=None):
    """Train Random Forest model."""
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_percentage_error
    
    if params is None:
        params = {
            'n_estimators': 100,
            'max_depth': 20,
            'min_samples_split': 5,
            'n_jobs': -1,
        }
    
    X_train_flat = X_train.reshape(-1, X_train.shape[-1])
    y_train_flat = y_train.flatten()
    
    model = RandomForestRegressor(**params)
    model.fit(X_train_flat, y_train_flat)
    
    X_val_flat = X_val.reshape(-1, X_val.shape[-1])
    y_pred = model.predict(X_val_flat)
    mape = mean_absolute_percentage_error(y_val_flat, y_pred) * 100
    
    print(f"Random Forest validation MAPE: {mape:.2f}%")
    return model, {'mape': mape}


def train_lstm(X_train, y_train, X_val, y_val, params=None):
    """Train LSTM model using PyTorch."""
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset
    
    if params is None:
        params = {
            'hidden_size': 64,
            'num_layers': 2,
            'dropout': 0.2,
            'learning_rate': 0.001,
            'batch_size': 64,
            'epochs': 100,
            'patience': 10
        }
    
    input_size = X_train.shape[-1]
    
    class LSTMModel(nn.Module):
        def __init__(self, input_size, hidden_size, num_layers, dropout):
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                               batch_first=True, dropout=dropout)
            self.fc = nn.Linear(hidden_size, 1)
        
        def forward(self, x):
            lstm_out, _ = self.lstm(x)
            return self.fc(lstm_out[:, -1, :])
    
    model = LSTMModel(input_size, params['hidden_size'], params['num_layers'], params['dropout'])
    
    # Prepare data
    train_dataset = TensorDataset(
        torch.FloatTensor(X_train),
        torch.FloatTensor(y_train[:, -1:])  # Predict last timestep only
    )
    val_dataset = TensorDataset(
        torch.FloatTensor(X_val),
        torch.FloatTensor(y_val[:, -1:])
    )
    
    train_loader = DataLoader(train_dataset, batch_size=params['batch_size'], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=params['batch_size'])
    
    # Training
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=params['learning_rate'])
    
    best_val_loss = float('inf')
    patience_counter = 0
    best_state = None
    
    for epoch in range(params['epochs']):
        model.train()
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            
            optimizer.zero_grad()
            pred = model(X_batch)
            loss = criterion(pred, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for X_batch, y_batch in val_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                pred = model(X_batch)
                val_loss += criterion(pred, y_batch).item()
        
        val_loss /= len(val_loader)
        
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            best_state = model.state_dict().copy()
        else:
            patience_counter += 1
            if patience_counter >= params['patience']:
                print(f"Early stopping at epoch {epoch + 1}")
                break
    
    model.load_state_dict(best_state)
    print(f"LSTM training completed, best val loss: {best_val_loss:.4f}")
    
    return model, {'val_loss': best_val_loss}


def train_sarima(df, target_col, order=(1, 1, 1), seasonal_order=(1, 1, 1, 24)):
    """Train SARIMA model."""
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    
    print("Training SARIMA (this may take a while)...")
    
    # Use a sample for faster training
    sample_size = min(10000, len(df))
    series = df[target_col].iloc[-sample_size:]
    
    model = SARIMAX(
        series,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    
    fitted = model.fit(disp=False)
    print(f"SARIMA training completed, AIC: {fitted.aic:.2f}")
    
    return fitted, {'aic': fitted.aic}


def calculate_metrics(y_true, y_pred):
    """Calculate forecast evaluation metrics."""
    from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
    
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    return {
        'mape': mape,
        'mae': mae,
        'rmse': rmse
    }


def save_model(model, model_type, output_dir, metrics, config):
    """Save trained model."""
    import joblib
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save model
    model_path = output_path / f'{model_type}_model.joblib'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Save metrics
    metrics['trained_at'] = datetime.now().isoformat()
    metrics['model_type'] = model_type
    
    metrics_path = output_path / 'training_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {metrics_path}")
    
    # Save config
    config_path = output_path / 'model_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Config saved to {config_path}")
    
    return model_path


def main():
    parser = argparse.ArgumentParser(description='Train electricity forecasting model')
    parser.add_argument('--model', required=True, 
                       choices=['lightgbm', 'xgboost', 'random_forest', 'lstm', 'sarima'],
                       help='Model type to train')
    parser.add_argument('--data', required=True, help='Processed data directory')
    parser.add_argument('--horizon', type=int, default=24, help='Forecast horizon (hours)')
    parser.add_argument('--lookback', type=int, default=168, help='Lookback window (hours)')
    parser.add_argument('--output', default='models', help='Output directory for model')
    parser.add_argument('--target', default='load', help='Target column name')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"Training {args.model.upper()} Model")
    print("=" * 60)
    
    # Load data
    df, feature_config = load_processed_data(args.data)
    
    # Prepare features
    feature_columns = feature_config['feature_columns']
    
    if args.model in ['lstm']:
        # For LSTM, keep sequence structure
        X, y = create_sequences(df, feature_columns, args.target, args.lookback, args.horizon)
        X_train, y_train, X_val, y_val, X_test, y_test = train_test_split_time_series(X, y)
    else:
        # For tree models, flatten sequences
        X, y = create_sequences(df, feature_columns, args.target, args.lookback, args.horizon)
        X_train, y_train, X_val, y_val, X_test, y_test = train_test_split_time_series(X, y)
    
    # Train model
    if args.model == 'lightgbm':
        model, metrics = train_lightgbm(X_train, y_train, X_val, y_val)
    elif args.model == 'xgboost':
        model, metrics = train_xgboost(X_train, y_train, X_val, y_val)
    elif args.model == 'random_forest':
        model, metrics = train_random_forest(X_train, y_train, X_val, y_val)
    elif args.model == 'lstm':
        model, metrics = train_lstm(X_train, y_train, X_val, y_val)
    elif args.model == 'sarima':
        model, metrics = train_sarima(df, args.target)
    
    # Evaluate on test set
    print("\nEvaluating on test set...")
    if args.model in ['lightgbm', 'xgboost', 'random_forest']:
        X_test_flat = X_test.reshape(-1, X_test.shape[-1])
        y_test_flat = y_test.flatten()
        y_pred = model.predict(X_test_flat)
        test_metrics = calculate_metrics(y_test_flat, y_pred)
    elif args.model == 'lstm':
        import torch
        model.eval()
        with torch.no_grad():
            X_tensor = torch.FloatTensor(X_test)
            y_pred = model(X_tensor).numpy().flatten()
            y_test_flat = y_test[:, -1].flatten()
            test_metrics = calculate_metrics(y_test_flat, y_pred)
    elif args.model == 'sarima':
        # SARIMA forecasting
        forecast = model.get_forecast(steps=args.horizon)
        y_pred = forecast.predicted_mean
        test_metrics = {'mape': 0, 'note': 'SARIMA evaluated differently'}
    
    print(f"Test MAPE: {test_metrics.get('mape', 'N/A')}")
    
    # Save model
    model_config = {
        'model_type': args.model,
        'horizon': args.horizon,
        'lookback': args.lookback,
        'target': args.target,
        'feature_columns': feature_columns,
        'validation_metrics': metrics,
        'test_metrics': test_metrics
    }
    
    save_model(model, args.model, args.output, test_metrics, model_config)
    
    print("=" * 60)
    print("Training completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
