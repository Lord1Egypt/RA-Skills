#!/usr/bin/env python3
"""
Data preparation script for electricity forecasting.

Usage:
    python scripts/prepare_data.py --input data/raw/load.csv --output data/processed/

Features:
    - Load and validate raw data
    - Handle missing values
    - Create temporal features
    - Create lag features
    - Create rolling statistics
    - Merge weather data
    - Save processed dataset
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime


def load_data(input_path):
    """Load raw electricity load data."""
    print(f"Loading data from {input_path}")
    
    # Try different formats
    if input_path.endswith('.csv'):
        df = pd.read_csv(input_path)
    elif input_path.endswith('.parquet'):
        df = pd.read_parquet(input_path)
    else:
        raise ValueError(f"Unsupported file format: {input_path}")
    
    # Standardize column names
    column_mapping = {
        'timestamp': 'timestamp',
        'datetime': 'timestamp',
        'time': 'timestamp',
        'load_mw': 'load',
        'load': 'load',
        'consumption': 'load',
        'demand': 'load',
        'temperature': 'temperature',
        'temp': 'temperature',
        'humidity': 'humidity',
    }
    
    df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    
    # Parse timestamp
    if 'timestamp' not in df.columns:
        raise ValueError("No timestamp column found. Expected one of: timestamp, datetime, time")
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    
    print(f"Loaded {len(df)} records from {df.index.min()} to {df.index.max()}")
    return df


def validate_data(df):
    """Validate data quality."""
    print("Validating data quality...")
    
    issues = []
    
    # Check for missing values
    missing_pct = df['load'].isna().mean() * 100
    if missing_pct > 0:
        issues.append(f"Missing values: {missing_pct:.2f}%")
    
    # Check for negative values
    if 'load' in df.columns:
        negative_pct = (df['load'] < 0).mean() * 100
        if negative_pct > 0:
            issues.append(f"Negative values: {negative_pct:.2f}%")
    
    # Check for outliers (simple z-score)
    if 'load' in df.columns and df['load'].notna().any():
        mean = df['load'].mean()
        std = df['load'].std()
        outlier_mask = np.abs(df['load'] - mean) > 4 * std
        outlier_pct = outlier_mask.mean() * 100
        if outlier_pct > 0:
            issues.append(f"Potential outliers (>4σ): {outlier_pct:.2f}%")
    
    # Check for gaps
    if len(df) > 1:
        expected_freq = pd.infer_freq(df.index)
        if expected_freq is None:
            issues.append("Cannot infer frequency - possible gaps in data")
        else:
            print(f"Data frequency: {expected_freq}")
    
    if issues:
        print("Data quality issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Data quality check passed")
    
    return issues


def handle_missing_values(df, max_gap_hours=4):
    """Handle missing values in load data."""
    print("Handling missing values...")
    
    df = df.copy()
    df['load_original'] = df['load']
    
    # Identify gaps
    missing_mask = df['load'].isna()
    
    if not missing_mask.any():
        print("No missing values to handle")
        return df
    
    # Calculate gap sizes
    gap_id = (~missing_mask).cumsum()
    gap_sizes = missing_mask.groupby(gap_id).transform('sum')
    
    # Short gaps: linear interpolation
    short_gaps = missing_mask & (gap_sizes <= max_gap_hours)
    n_short = short_gaps.sum()
    if n_short > 0:
        df.loc[short_gaps, 'load'] = df['load'].interpolate(method='linear')
        print(f"  Interpolated {n_short} short gaps (≤{max_gap_hours}h)")
    
    # Medium gaps: use same hour previous day
    medium_gaps = missing_mask & (gap_sizes > max_gap_hours) & (gap_sizes <= 24)
    n_medium = medium_gaps.sum()
    if n_medium > 0:
        for idx in df[medium_gaps].index:
            prev_day = idx - pd.Timedelta(days=1)
            if prev_day in df.index and not pd.isna(df.loc[prev_day, 'load']):
                df.loc[idx, 'load'] = df.loc[prev_day, 'load']
        print(f"  Filled {n_medium} medium gaps with previous day values")
    
    # Long gaps: flag but don't fill
    long_gaps = missing_mask & (gap_sizes > 24)
    n_long = long_gaps.sum()
    if n_long > 0:
        df.loc[long_gaps, 'load_quality_flag'] = 'MISSING_LONG_GAP'
        print(f"  Flagged {n_long} long gaps (>24h) for review")
    
    # Report remaining missing
    remaining = df['load'].isna().sum()
    if remaining > 0:
        print(f"  Warning: {remaining} values still missing")
    
    return df


def create_temporal_features(df):
    """Create temporal features."""
    print("Creating temporal features...")
    
    df = df.copy()
    
    # Basic temporal features
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['day_of_month'] = df.index.day
    df['month'] = df.index.month
    df['day_of_year'] = df.index.dayofyear
    df['week_of_year'] = df.index.isocalendar().week
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_month_start'] = df.index.is_month_start.astype(int)
    df['is_month_end'] = df.index.is_month_end.astype(int)
    
    # Cyclical encoding
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    return df


def create_lag_features(df, lags=None):
    """Create lag features."""
    if lags is None:
        lags = [1, 2, 3, 6, 12, 24, 48, 72, 168, 336]
    
    print(f"Creating lag features: {lags}")
    
    df = df.copy()
    for lag in lags:
        df[f'lag_{lag}h'] = df['load'].shift(lag)
    
    return df


def create_rolling_features(df):
    """Create rolling statistics."""
    print("Creating rolling features...")
    
    df = df.copy()
    
    # Mean features
    df['rolling_mean_6h'] = df['load'].shift(1).rolling(6).mean()
    df['rolling_mean_24h'] = df['load'].shift(1).rolling(24).mean()
    df['rolling_mean_168h'] = df['load'].shift(1).rolling(168).mean()
    
    # Standard deviation
    df['rolling_std_24h'] = df['load'].shift(1).rolling(24).std()
    df['rolling_std_168h'] = df['load'].shift(1).rolling(168).std()
    
    # Min/max
    df['rolling_min_24h'] = df['load'].shift(1).rolling(24).min()
    df['rolling_max_24h'] = df['load'].shift(1).rolling(24).max()
    
    # EMA
    df['ema_12h'] = df['load'].shift(1).ewm(span=12).mean()
    df['ema_24h'] = df['load'].shift(1).ewm(span=24).mean()
    
    return df


def create_weather_features(df, weather_df=None):
    """Create weather features."""
    print("Creating weather features...")
    
    df = df.copy()
    
    if weather_df is not None:
        # Merge weather data
        df = df.join(weather_df.set_index('timestamp'), how='left')
        print(f"  Merged weather data with {len(weather_df)} records")
    
    # Temperature features (if available)
    if 'temperature' in df.columns:
        df['temp_squared'] = df['temperature'] ** 2
        
        # Heating and Cooling Degree Days
        base_temp = 18
        df['hdd'] = np.maximum(base_temp - df['temperature'], 0)
        df['cdd'] = np.maximum(df['temperature'] - base_temp, 0)
        
        # Temperature changes
        df['temp_change_1h'] = df['temperature'].diff(1)
        df['temp_change_6h'] = df['temperature'].diff(6)
        
        print("  Created temperature-derived features")
    
    return df


def create_holiday_features(df, country='CN'):
    """Create holiday features."""
    print("Creating holiday features...")
    
    df = df.copy()
    
    try:
        import holidays
        cn_holidays = holidays.CountryHoliday(country, years=range(2020, 2030))
        
        df['is_holiday'] = df.index.map(lambda x: 1 if x in cn_holidays else 0)
        
        # Holiday proximity
        def days_to_holiday(dt):
            holiday_dates = list(cn_holidays.keys())
            if not holiday_dates:
                return 30
            return min([abs((dt - d).days) for d in holiday_dates])
        
        df['days_to_holiday'] = df.index.map(days_to_holiday)
        df['is_holiday_eve'] = (df['days_to_holiday'] == 1).astype(int)
        
        print(f"  Identified {df['is_holiday'].sum()} holidays")
    except ImportError:
        print("  Warning: holidays package not installed, skipping holiday features")
        df['is_holiday'] = 0
    
    return df


def save_processed_data(df, output_dir, config):
    """Save processed data and configuration."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save processed data
    data_path = output_path / 'processed_data.parquet'
    df.to_parquet(data_path)
    print(f"Saved processed data to {data_path}")
    
    # Save feature configuration
    feature_columns = [c for c in df.columns if c != 'load']
    config['feature_columns'] = feature_columns
    config['n_features'] = len(feature_columns)
    config['processed_at'] = datetime.now().isoformat()
    
    config_path = output_path / 'feature_config.json'
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Saved feature config to {config_path}")
    
    # Save data statistics
    stats = {
        'n_records': len(df),
        'date_range': {
            'start': str(df.index.min()),
            'end': str(df.index.max())
        },
        'load_stats': {
            'mean': float(df['load'].mean()),
            'std': float(df['load'].std()),
            'min': float(df['load'].min()),
            'max': float(df['load'].max()),
            'median': float(df['load'].median())
        },
        'missing_pct': float(df['load'].isna().mean() * 100),
        'n_features': len(feature_columns)
    }
    
    stats_path = output_path / 'data_stats.json'
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"Saved data statistics to {stats_path}")
    
    return data_path


def main():
    parser = argparse.ArgumentParser(description='Prepare electricity load data for forecasting')
    parser.add_argument('--input', required=True, help='Input raw data file (CSV or Parquet)')
    parser.add_argument('--output', required=True, help='Output directory for processed data')
    parser.add_argument('--weather', help='Optional weather data file')
    parser.add_argument('--country', default='CN', help='Country code for holidays (default: CN)')
    parser.add_argument('--max-gap-hours', type=int, default=4, help='Max gap hours for interpolation')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Electricity Load Data Preparation")
    print("=" * 60)
    
    # Load data
    df = load_data(args.input)
    
    # Validate
    issues = validate_data(df)
    
    # Handle missing values
    df = handle_missing_values(df, max_gap_hours=args.max_gap_hours)
    
    # Create features
    df = create_temporal_features(df)
    df = create_lag_features(df)
    df = create_rolling_features(df)
    
    # Weather features
    weather_df = None
    if args.weather:
        weather_df = load_data(args.weather)
    df = create_weather_features(df, weather_df)
    
    # Holiday features
    df = create_holiday_features(df, country=args.country)
    
    # Drop rows with NaN in target (from lag features at start)
    initial_count = len(df)
    df = df.dropna(subset=['load'])
    dropped = initial_count - len(df)
    if dropped > 0:
        print(f"Dropped {dropped} rows with missing target values")
    
    # Save
    config = {
        'input_file': args.input,
        'weather_file': args.weather,
        'country': args.country,
        'max_gap_hours': args.max_gap_hours,
    }
    
    save_processed_data(df, args.output, config)
    
    print("=" * 60)
    print("Data preparation completed successfully!")
    print(f"Output: {args.output}")
    print(f"Features: {len(df.columns) - 1}")
    print("=" * 60)


if __name__ == '__main__':
    main()
