#!/usr/bin/env python3
"""
Hyperparameter optimization script using Optuna.

Usage:
    python scripts/hyperparameter_search.py --model lightgbm --data data/processed/ --n-trials 50
"""

import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
import optuna
from datetime import datetime


def load_data(data_dir):
    """Load processed data."""
    data_path = Path(data_dir) / 'processed_data.parquet'
    config_path = Path(data_dir) / 'feature_config.json'
    
    df = pd.read_parquet(data_path)
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return df, config


def create_sequences(df, feature_columns, target_col, lookback, horizon):
    """Create sequences for training."""
    X, y = [], []
    features = df[feature_columns].values
    target = df[target_col].values
    
    for i in range(len(features) - lookback - horizon + 1):
        X.append(features[i:i + lookback])
        y.append(target[i + lookback:i + lookback + horizon])
    
    return np.array(X), np.array(y)


def objective_lightgbm(trial, X_train, y_train, X_val, y_val):
    """Optuna objective for LightGBM."""
    import lightgbm as lgb
    from sklearn.metrics import mean_absolute_percentage_error
    
    params = {
        'objective': 'regression',
        'metric': 'mape',
        'boosting_type': trial.suggest_categorical('boosting_type', ['gbdt', 'dart']),
        'num_leaves': trial.suggest_int('num_leaves', 16, 128),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'feature_fraction': trial.suggest_float('feature_fraction', 0.5, 1.0),
        'bagging_fraction': trial.suggest_float('bagging_fraction', 0.5, 1.0),
        'bagging_freq': trial.suggest_int('bagging_freq', 1, 10),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
        'n_estimators': 1000,
        'early_stopping_rounds': 50,
        'verbose': -1,
    }
    
    X_train_flat = X_train.reshape(-1, X_train.shape[-1])
    y_train_flat = y_train.flatten()
    X_val_flat = X_val.reshape(-1, X_val.shape[-1])
    y_val_flat = y_val.flatten()
    
    model = lgb.LGBMRegressor(**params)
    model.fit(X_train_flat, y_train_flat, eval_set=[(X_val_flat, y_val_flat)])
    
    y_pred = model.predict(X_val_flat)
    mape = mean_absolute_percentage_error(y_val_flat, y_pred) * 100
    
    return mape


def objective_xgboost(trial, X_train, y_train, X_val, y_val):
    """Optuna objective for XGBoost."""
    import xgboost as xgb
    from sklearn.metrics import mean_absolute_percentage_error
    
    params = {
        'objective': 'reg:squarederror',
        'eval_metric': 'mape',
        'max_depth': trial.suggest_int('max_depth', 3, 12),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-8, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-8, 10.0, log=True),
        'n_estimators': 1000,
        'early_stopping_rounds': 50,
    }
    
    X_train_flat = X_train.reshape(-1, X_train.shape[-1])
    y_train_flat = y_train.flatten()
    X_val_flat = X_val.reshape(-1, X_val.shape[-1])
    y_val_flat = y_val.flatten()
    
    model = xgb.XGBRegressor(**params)
    model.fit(X_train_flat, y_train_flat, eval_set=[(X_val_flat, y_val_flat)], verbose=False)
    
    y_pred = model.predict(X_val_flat)
    mape = mean_absolute_percentage_error(y_val_flat, y_pred) * 100
    
    return mape


def objective_lstm(trial, X_train, y_train, X_val, y_val):
    """Optuna objective for LSTM."""
    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader, TensorDataset
    
    hidden_size = trial.suggest_categorical('hidden_size', [32, 64, 128, 256])
    num_layers = trial.suggest_int('num_layers', 1, 4)
    dropout = trial.suggest_float('dropout', 0.1, 0.4)
    learning_rate = trial.suggest_float('learning_rate', 1e-4, 1e-2, log=True)
    batch_size = trial.suggest_categorical('batch_size', [32, 64, 128])
    
    input_size = X_train.shape[-1]
    epochs = 50  # Reduced for search
    patience = 10
    
    class LSTMModel(nn.Module):
        def __init__(self, input_size, hidden_size, num_layers, dropout):
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                               batch_first=True, dropout=dropout if num_layers > 1 else 0)
            self.fc = nn.Linear(hidden_size, 1)
        
        def forward(self, x):
            lstm_out, _ = self.lstm(x)
            return self.fc(lstm_out[:, -1, :])
    
    model = LSTMModel(input_size, hidden_size, num_layers, dropout)
    
    train_dataset = TensorDataset(
        torch.FloatTensor(X_train),
        torch.FloatTensor(y_train[:, -1:])
    )
    val_dataset = TensorDataset(
        torch.FloatTensor(X_val),
        torch.FloatTensor(y_val[:, -1:])
    )
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    best_val_loss = float('inf')
    patience_counter = 0
    
    for epoch in range(epochs):
        model.train()
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()
            pred = model(X_batch)
            loss = criterion(pred, y_batch)
            loss.backward()
            optimizer.step()
        
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
        else:
            patience_counter += 1
            if patience_counter >= patience:
                break
    
    return best_val_loss


def run_hyperparameter_search(model_type, X_train, y_train, X_val, y_val, n_trials, study_name):
    """Run hyperparameter search."""
    
    if model_type == 'lightgbm':
        objective = lambda trial: objective_lightgbm(trial, X_train, y_train, X_val, y_val)
    elif model_type == 'xgboost':
        objective = lambda trial: objective_xgboost(trial, X_train, y_train, X_val, y_val)
    elif model_type == 'lstm':
        objective = lambda trial: objective_lstm(trial, X_train, y_train, X_val, y_val)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    # Create study
    study = optuna.create_study(
        study_name=study_name,
        direction='minimize',
        load_if_exists=True
    )
    
    # Run optimization
    print(f"Starting hyperparameter search with {n_trials} trials...")
    study.optimize(objective, n_trials=n_trials, timeout=3600 * 4)  # 4 hour timeout
    
    print(f"\nBest trial:")
    print(f"  Value: {study.best_value:.4f}")
    print(f"  Params: {study.best_params}")
    
    return study


def save_results(study, output_dir, model_type):
    """Save optimization results."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save best params
    results = {
        'best_value': study.best_value,
        'best_params': study.best_params,
        'n_trials': len(study.trials),
        'model_type': model_type,
        'completed_at': datetime.now().isoformat()
    }
    
    with open(output_path / 'best_params.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save all trials
    trials_df = study.trials_dataframe()
    trials_df.to_csv(output_path / 'all_trials.csv', index=False)
    
    print(f"\nResults saved to {output_path}")
    
    # Plot (if matplotlib available)
    try:
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Optimization history
        optuna.visualization.matplotlib.plot_optimization_history(study)
        plt.savefig(output_path / 'optimization_history.png')
        
        # Parameter importances
        optuna.visualization.matplotlib.plot_param_importances(study)
        plt.savefig(output_path / 'param_importances.png')
        
        print("Plots saved")
    except ImportError:
        print("Matplotlib not available, skipping plots")


def main():
    parser = argparse.ArgumentParser(description='Hyperparameter optimization')
    parser.add_argument('--model', required=True, 
                       choices=['lightgbm', 'xgboost', 'lstm'],
                       help='Model type')
    parser.add_argument('--data', required=True, help='Processed data directory')
    parser.add_argument('--n-trials', type=int, default=50, help='Number of trials')
    parser.add_argument('--output', default='models/hyperparam_search', help='Output directory')
    parser.add_argument('--study-name', default=None, help='Optuna study name')
    parser.add_argument('--horizon', type=int, default=24, help='Forecast horizon')
    parser.add_argument('--lookback', type=int, default=168, help='Lookback window')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"Hyperparameter Search for {args.model.upper()}")
    print("=" * 60)
    
    # Load data
    df, config = load_data(args.data)
    
    # Create sequences
    X, y = create_sequences(df, config['feature_columns'], 'load', args.lookback, args.horizon)
    
    # Split data
    n = len(X)
    test_start = int(n * 0.7)
    val_start = int(n * 0.85)
    
    X_train, y_train = X[:test_start], y[:test_start]
    X_val, y_val = X[test_start:val_start], y[test_start:val_start]
    
    print(f"Train: {len(X_train)}, Val: {len(X_val)}")
    
    # Run search
    study_name = args.study_name or f"{args.model}_stlf"
    study = run_hyperparameter_search(
        args.model, X_train, y_train, X_val, y_val,
        args.n_trials, study_name
    )
    
    # Save results
    save_results(study, args.output, args.model)
    
    print("=" * 60)
    print("Hyperparameter search completed!")
    print(f"Best MAPE: {study.best_value:.2f}%")
    print("=" * 60)


if __name__ == '__main__':
    main()
