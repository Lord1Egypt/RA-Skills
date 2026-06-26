#!/usr/bin/env python3
"""
Comprehensive forecast evaluation script.

Usage:
    python scripts/evaluate.py --predictions forecasts.csv --actuals actuals.csv --output eval_report.json
"""

import argparse
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error, r2_score


def load_data(predictions_path, actuals_path):
    """Load predictions and actuals."""
    pred_df = pd.read_csv(predictions_path)
    actual_df = pd.read_csv(actuals_path)
    
    # Merge on timestamp if available
    if 'timestamp' in pred_df.columns and 'timestamp' in actual_df.columns:
        df = pd.merge(pred_df, actual_df, on='timestamp', suffixes=('_pred', '_actual'))
    else:
        # Assume same order
        df = pd.concat([pred_df, actual_df], axis=1)
    
    return df


def calculate_point_metrics(y_true, y_pred):
    """Calculate point forecast metrics."""
    errors = y_true - y_pred
    
    return {
        'mape': float(mean_absolute_percentage_error(y_true, y_pred) * 100),
        'mae': float(mean_absolute_error(y_true, y_pred)),
        'rmse': float(np.sqrt(mean_squared_error(y_true, y_pred))),
        'mse': float(mean_squared_error(y_true, y_pred)),
        'r2': float(r2_score(y_true, y_pred)),
        'bias': float(np.mean(errors)),
        'std_error': float(np.std(errors))
    }


def calculate_percentile_metrics(y_true, y_pred):
    """Calculate metrics by percentile of actual load."""
    percentiles = [0, 25, 50, 75, 100]
    labels = ['min-25%', '25-50%', '50-75%', '75-max']
    
    results = {}
    q_values = np.percentile(y_true, percentiles)
    
    for i in range(len(labels)):
        mask = (y_true >= q_values[i]) & (y_true <= q_values[i + 1])
        if mask.sum() > 0:
            results[labels[i]] = {
                'mape': float(mean_absolute_percentage_error(y_true[mask], y_pred[mask]) * 100),
                'mae': float(mean_absolute_error(y_true[mask], y_pred[mask])),
                'n_samples': int(mask.sum())
            }
    
    return results


def calculate_hourly_metrics(df, pred_col, actual_col):
    """Calculate metrics by hour of day."""
    if 'timestamp' in df.columns:
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    elif 'hour' in df.columns:
        pass
    else:
        return None
    
    hourly = {}
    for hour in range(24):
        mask = df['hour'] == hour
        if mask.sum() > 0:
            hourly[hour] = {
                'mape': float(mean_absolute_percentage_error(
                    df.loc[mask, actual_col], df.loc[mask, pred_col]
                ) * 100),
                'mae': float(mean_absolute_error(
                    df.loc[mask, actual_col], df.loc[mask, pred_col]
                )),
                'n_samples': int(mask.sum())
            }
    
    return hourly


def calculate_daily_metrics(df, pred_col, actual_col):
    """Calculate metrics by day of week."""
    if 'timestamp' in df.columns:
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
    elif 'day_of_week' in df.columns:
        pass
    else:
        return None
    
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily = {}
    
    for dow in range(7):
        mask = df['day_of_week'] == dow
        if mask.sum() > 0:
            daily[day_names[dow]] = {
                'mape': float(mean_absolute_percentage_error(
                    df.loc[mask, actual_col], df.loc[mask, pred_col]
                ) * 100),
                'mae': float(mean_absolute_error(
                    df.loc[mask, actual_col], df.loc[mask, pred_col]
                )),
                'n_samples': int(mask.sum())
            }
    
    return daily


def calculate_peak_metrics(y_true, y_pred, peak_threshold=0.9):
    """Calculate metrics for peak load periods."""
    peak_value = np.percentile(y_true, peak_threshold * 100)
    
    peak_mask = y_true >= peak_value
    off_peak_mask = y_true < peak_value
    
    results = {}
    
    if peak_mask.sum() > 0:
        results['peak'] = {
            'mape': float(mean_absolute_percentage_error(y_true[peak_mask], y_pred[peak_mask]) * 100),
            'mae': float(mean_absolute_error(y_true[peak_mask], y_pred[peak_mask])),
            'n_samples': int(peak_mask.sum()),
            'threshold': float(peak_value)
        }
    
    if off_peak_mask.sum() > 0:
        results['off_peak'] = {
            'mape': float(mean_absolute_percentage_error(y_true[off_peak_mask], y_pred[off_peak_mask]) * 100),
            'mae': float(mean_absolute_error(y_true[off_peak_mask], y_pred[off_peak_mask])),
            'n_samples': int(off_peak_mask.sum())
        }
    
    return results


def calculate_direction_accuracy(y_true, y_pred):
    """Calculate accuracy of predicting direction of change."""
    if len(y_true) < 2:
        return None
    
    actual_direction = np.diff(y_true) > 0
    pred_direction = np.diff(y_pred) > 0
    
    accuracy = (actual_direction == pred_direction).mean() * 100
    
    return {
        'direction_accuracy': float(accuracy),
        'n_transitions': len(actual_direction)
    }


def calculate_uncertainty_metrics(y_true, y_lower, y_upper, target_coverage=0.9):
    """Calculate metrics for prediction intervals."""
    within_interval = (y_true >= y_lower) & (y_true <= y_upper)
    
    return {
        'coverage': float(within_interval.mean()),
        'target_coverage': target_coverage,
        'coverage_error': float(abs(within_interval.mean() - target_coverage)),
        'mean_width': float(np.mean(y_upper - y_lower)),
        'normalized_width': float(np.mean((y_upper - y_lower) / y_true))
    }


def generate_report(df, pred_col, actual_col, include_uncertainty=False):
    """Generate comprehensive evaluation report."""
    y_true = df[actual_col].values
    y_pred = df[pred_col].values
    
    report = {
        'summary': {
            'n_samples': len(df),
            'date_range': {
                'start': str(df['timestamp'].min()) if 'timestamp' in df.columns else None,
                'end': str(df['timestamp'].max()) if 'timestamp' in df.columns else None
            },
            'load_range': {
                'min': float(y_true.min()),
                'max': float(y_true.max()),
                'mean': float(y_true.mean())
            }
        },
        'point_metrics': calculate_point_metrics(y_true, y_pred),
        'percentile_metrics': calculate_percentile_metrics(y_true, y_pred),
        'peak_metrics': calculate_peak_metrics(y_true, y_pred),
        'direction_accuracy': calculate_direction_accuracy(y_true, y_pred)
    }
    
    hourly = calculate_hourly_metrics(df, pred_col, actual_col)
    if hourly:
        report['hourly_metrics'] = hourly
    
    daily = calculate_daily_metrics(df, pred_col, actual_col)
    if daily:
        report['daily_metrics'] = daily
    
    if include_uncertainty and 'lower' in df.columns and 'upper' in df.columns:
        report['uncertainty_metrics'] = calculate_uncertainty_metrics(
            y_true, df['lower'].values, df['upper'].values
        )
    
    return report


def print_report(report):
    """Print formatted report."""
    print("\n" + "=" * 60)
    print("FORECAST EVALUATION REPORT")
    print("=" * 60)
    
    print(f"\n📊 Data Summary:")
    print(f"   Samples: {report['summary']['n_samples']}")
    if report['summary']['date_range']['start']:
        print(f"   Period: {report['summary']['date_range']['start']} to {report['summary']['date_range']['end']}")
    print(f"   Load Range: {report['summary']['load_range']['min']:.1f} - {report['summary']['load_range']['max']:.1f} MW")
    
    print(f"\n📈 Point Forecast Metrics:")
    pm = report['point_metrics']
    print(f"   MAPE:  {pm['mape']:.2f}%")
    print(f"   MAE:   {pm['mae']:.2f} MW")
    print(f"   RMSE:  {pm['rmse']:.2f} MW")
    print(f"   R²:    {pm['r2']:.4f}")
    print(f"   Bias:  {pm['bias']:.2f} MW")
    
    if report.get('direction_accuracy'):
        print(f"\n📉 Direction Accuracy:")
        print(f"   {report['direction_accuracy']['direction_accuracy']:.1f}% correct")
    
    if report.get('peak_metrics'):
        print(f"\n⚡ Peak vs Off-Peak:")
        if 'peak' in report['peak_metrics']:
            print(f"   Peak MAPE:      {report['peak_metrics']['peak']['mape']:.2f}%")
        if 'off_peak' in report['peak_metrics']:
            print(f"   Off-Peak MAPE:  {report['peak_metrics']['off_peak']['mape']:.2f}%")
    
    if report.get('hourly_metrics'):
        print(f"\n🕐 Hourly MAPE:")
        hourly = report['hourly_metrics']
        hours = sorted(hourly.keys())
        worst_hour = max(hours, key=lambda h: hourly[h]['mape'])
        best_hour = min(hours, key=lambda h: hourly[h]['mape'])
        print(f"   Best:  Hour {best_hour:02d} ({hourly[best_hour]['mape']:.2f}%)")
        print(f"   Worst: Hour {worst_hour:02d} ({hourly[worst_hour]['mape']:.2f}%)")
    
    if report.get('daily_metrics'):
        print(f"\n📅 Daily MAPE:")
        for day, metrics in report['daily_metrics'].items():
            print(f"   {day:10s}: {metrics['mape']:.2f}%")
    
    if report.get('uncertainty_metrics'):
        print(f"\n🎯 Uncertainty Quantification:")
        um = report['uncertainty_metrics']
        print(f"   Coverage:       {um['coverage']*100:.1f}% (target: {um['target_coverage']*100:.1f}%)")
        print(f"   Mean Width:     {um['mean_width']:.2f} MW")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description='Evaluate electricity forecasts')
    parser.add_argument('--predictions', required=True, help='Predictions CSV file')
    parser.add_argument('--actuals', required=True, help='Actuals CSV file')
    parser.add_argument('--output', default='evaluation_report.json', help='Output JSON file')
    parser.add_argument('--pred-col', default='predicted_load', help='Prediction column name')
    parser.add_argument('--actual-col', default='actual_load', help='Actual column name')
    parser.add_argument('--include-uncertainty', action='store_true', help='Include uncertainty metrics')
    
    args = parser.parse_args()
    
    print("Loading data...")
    df = load_data(args.predictions, args.actuals)
    print(f"Loaded {len(df)} records")
    
    print("Evaluating forecasts...")
    report = generate_report(df, args.pred_col, args.actual_col, args.include_uncertainty)
    
    # Print report
    print_report(report)
    
    # Save report
    report['generated_at'] = datetime.now().isoformat()
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nReport saved to {output_path}")


if __name__ == '__main__':
    main()
