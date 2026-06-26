#!/usr/bin/env python3
"""
Time series backtesting script with cross-validation.

Usage:
    python scripts/backtest.py --model lightgbm --data data/processed/ --cv-splits 5 --horizon 24
"""

import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error


def load_data(data_dir):
    """Load processed data."""
    data_path = Path(data_dir) / 'processed_data.parquet'
    config_path = Path(data_dir) / 'feature_config.json'
    
    df = pd.read_parquet(data_path)
    with open(config_path, 'r') as f:
        config = json.load(f)
    
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


def time_series_split(n_samples, n_splits, test_size):
    """Generate time series cross-validation splits."""
    splits = []
    
    for i in range(n_splits):
        # Expanding window
        train_end = n_samples - (n_splits - i) * test_size - test_size
        val_start = train_end
        val_end = train_end + test_size
        test_start = val_end
        test_end = test_start + test_size
        
        if test_end > n_samples:
            break
        
        splits.append({
            'train': (0, train_end),
            'val': (val_start, val_end),
            'test': (test_start, test_end)
        })
    
    return splits


def train_model(model_type, X_train, y_train, X_val, y_val):
    """Train a model."""
    X_train_flat = X_train.reshape(-1, X_train.shape[-1])
    y_train_flat = y_train.flatten()
    X_val_flat = X_val.reshape(-1, X_val.shape[-1])
    y_val_flat = y_val.flatten()
    
    if model_type == 'lightgbm':
        import lightgbm as lgb
        model = lgb.LGBMRegressor(
            objective='regression',
            metric='mape',
            num_leaves=31,
            learning_rate=0.05,
            n_estimators=1000,
            early_stopping_rounds=50,
            verbose=-1
        )
        model.fit(X_train_flat, y_train_flat, eval_set=[(X_val_flat, y_val_flat)])
    
    elif model_type == 'xgboost':
        import xgboost as xgb
        model = xgb.XGBRegressor(
            objective='reg:squarederror',
            eval_metric='mape',
            max_depth=6,
            learning_rate=0.05,
            n_estimators=1000,
            early_stopping_rounds=50
        )
        model.fit(X_train_flat, y_train_flat, eval_set=[(X_val_flat, y_val_flat)], verbose=False)
    
    elif model_type == 'random_forest':
        from sklearn.ensemble import RandomForestRegressor
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            n_jobs=-1
        )
        model.fit(X_train_flat, y_train_flat)
    
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    return model


def calculate_metrics(y_true, y_pred):
    """Calculate forecast metrics."""
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    # Calculate metrics by hour of day (for insight)
    return {
        'mape': mape,
        'mae': mae,
        'rmse': rmse
    }


def run_backtest(model_type, X, y, n_splits, test_size, horizon):
    """Run time series backtest."""
    splits = time_series_split(len(X), n_splits, test_size)
    
    results = []
    fold_metrics = []
    
    print(f"Running {len(splits)}-fold time series cross-validation...")
    print("-" * 60)
    
    for i, split in enumerate(splits):
        train_start, train_end = split['train']
        val_start, val_end = split['val']
        test_start, test_end = split['test']
        
        X_train = X[train_start:train_end]
        y_train = y[train_start:train_end]
        X_val = X[val_start:val_end]
        y_val = y[val_start:val_end]
        X_test = X[test_start:test_end]
        y_test = y[test_start:test_end]
        
        # Train model
        model = train_model(model_type, X_train, y_train, X_val, y_val)
        
        # Predict
        X_test_flat = X_test.reshape(-1, X_test.shape[-1])
        y_test_flat = y_test.flatten()
        y_pred = model.predict(X_test_flat)
        
        # Calculate metrics
        metrics = calculate_metrics(y_test_flat, y_pred)
        fold_metrics.append(metrics)
        
        print(f"Fold {i+1}: MAPE={metrics['mape']:.2f}%, MAE={metrics['mae']:.2f}, RMSE={metrics['rmse']:.2f}")
        
        # Store predictions for analysis
        results.append({
            'fold': i + 1,
            'predictions': y_pred,
            'actuals': y_test_flat,
            'metrics': metrics
        })
    
    # Aggregate results
    avg_metrics = {
        'mape': np.mean([m['mape'] for m in fold_metrics]),
        'mae': np.mean([m['mae'] for m in fold_metrics]),
        'rmse': np.mean([m['rmse'] for m in fold_metrics]),
        'mape_std': np.std([m['mape'] for m in fold_metrics]),
        'mae_std': np.std([m['mae'] for m in fold_metrics]),
        'rmse_std': np.std([m['rmse'] for m in fold_metrics])
    }
    
    return results, avg_metrics, fold_metrics


def analyze_by_hour(results, horizon):
    """Analyze forecast accuracy by hour of day."""
    hour_errors = {h: [] for h in range(24)}
    
    for fold_result in results:
        predictions = fold_result['predictions']
        actuals = fold_result['actuals']
        
        for i in range(len(predictions)):
            hour = i % horizon  # Hour within forecast horizon
            error = abs(predictions[i] - actuals[i]) / actuals[i] * 100 if actuals[i] != 0 else 0
            hour_errors[hour].append(error)
    
    hour_summary = {}
    for hour, errors in hour_errors.items():
        if errors:
            hour_summary[hour] = {
                'mape_mean': np.mean(errors),
                'mape_std': np.std(errors),
                'n_samples': len(errors)
            }
    
    return hour_summary


def analyze_by_fold(fold_metrics):
    """Analyze performance stability across folds."""
    return {
        'mape_by_fold': [m['mape'] for m in fold_metrics],
        'mae_by_fold': [m['mae'] for m in fold_metrics],
        'rmse_by_fold': [m['rmse'] for m in fold_metrics]
    }


def save_backtest_results(results, avg_metrics, hour_analysis, fold_analysis, output_dir, config):
    """Save backtest results."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save summary
    summary = {
        'average_metrics': avg_metrics,
        'n_folds': len(results),
        'config': config,
        'completed_at': datetime.now().isoformat()
    }
    
    with open(output_path / 'backtest_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Save fold-level results
    fold_results = []
    for r in results:
        fold_results.append({
            'fold': r['fold'],
            'metrics': r['metrics']
        })
    
    with open(output_path / 'fold_results.json', 'w') as f:
        json.dump(fold_results, f, indent=2)
    
    # Save hour analysis
    with open(output_path / 'hour_analysis.json', 'w') as f:
        json.dump(hour_analysis, f, indent=2)
    
    # Save fold analysis
    with open(output_path / 'fold_analysis.json', 'w') as f:
        json.dump(fold_analysis, f, indent=2)
    
    # Save detailed predictions (sample)
    sample_predictions = []
    for r in results[:1]:  # Just first fold for brevity
        sample_predictions.append({
            'fold': r['fold'],
            'predictions': r['predictions'][:100].tolist(),
            'actuals': r['actuals'][:100].tolist()
        })
    
    with open(output_path / 'sample_predictions.json', 'w') as f:
        json.dump(sample_predictions, f, indent=2)
    
    print(f"\nResults saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Time series backtesting')
    parser.add_argument('--model', required=True,
                       choices=['lightgbm', 'xgboost', 'random_forest'],
                       help='Model type')
    parser.add_argument('--data', required=True, help='Processed data directory')
    parser.add_argument('--cv-splits', type=int, default=5, help='Number of CV splits')
    parser.add_argument('--horizon', type=int, default=24, help='Forecast horizon')
    parser.add_argument('--lookback', type=int, default=168, help='Lookback window')
    parser.add_argument('--output', default='backtest_results', help='Output directory')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"Backtesting {args.model.upper()} Model")
    print("=" * 60)
    
    # Load data
    df, config = load_data(args.data)
    
    # Create sequences
    X, y = create_sequences(df, config['feature_columns'], 'load', args.lookback, args.horizon)
    print(f"Created {len(X)} sequences")
    
    # Calculate test size
    test_size = len(X) // (args.cv_splits + 2)  # Reserve some for test
    
    # Run backtest
    results, avg_metrics, fold_metrics = run_backtest(
        args.model, X, y, args.cv_splits, test_size, args.horizon
    )
    
    print("-" * 60)
    print(f"Average Results ({args.cv_splits}-fold CV):")
    print(f"  MAPE: {avg_metrics['mape']:.2f}% ± {avg_metrics['mape_std']:.2f}%")
    print(f"  MAE:  {avg_metrics['mae']:.2f} ± {avg_metrics['mae_std']:.2f}")
    print(f"  RMSE: {avg_metrics['rmse']:.2f} ± {avg_metrics['rmse_std']:.2f}")
    
    # Analyze by hour
    hour_analysis = analyze_by_hour(results, args.horizon)
    
    # Analyze fold stability
    fold_analysis = analyze_by_fold(fold_metrics)
    
    # Save results
    backtest_config = {
        'model_type': args.model,
        'cv_splits': args.cv_splits,
        'horizon': args.horizon,
        'lookback': args.lookback,
        'test_size': test_size
    }
    
    save_backtest_results(results, avg_metrics, hour_analysis, fold_analysis, args.output, backtest_config)
    
    # Print hour analysis summary
    print("\nForecast Accuracy by Hour:")
    print("-" * 60)
    for hour in sorted(hour_analysis.keys()):
        h = hour_analysis[hour]
        print(f"  Hour {hour:2d}: MAPE = {h['mape_mean']:.2f}% ± {h['mape_std']:.2f}%")
    
    print("=" * 60)
    print("Backtesting completed!")
    print("=" * 60)


if __name__ == '__main__':
    main()
