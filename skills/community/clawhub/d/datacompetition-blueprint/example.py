"""
Competitive Data Science: Baseline to Topline Example
This script demonstrates the complete workflow from baseline to topline solution.
"""

import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold, GroupKFold
from sklearn.metrics import roc_auc_score, f1_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 1. DATA LOADING AND INITIAL EXPLORATION
# ============================================================

def load_data(train_path, test_path):
    """Load and basic exploration"""
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    
    print(f"Train shape: {train.shape}")
    print(f"Test shape: {test.shape}")
    print(f"Target distribution:\n{train['target'].value_counts(normalize=True)}")
    
    return train, test

# ============================================================
# 2. BASELINE MODEL (Simple Feature Set)
# ============================================================

def build_baseline_features(df):
    """Create minimal baseline features"""
    # Basic numerical features
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Basic categorical encoding
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    
    return df

def train_baseline(train, test, target_col='target'):
    """Train baseline LightGBM model"""
    features = [c for c in train.columns if c not in [target_col, 'id']]
    
    # Simple parameters
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'num_leaves': 31,
        'learning_rate': 0.1,
        'feature_fraction': 0.8,
        'verbose': -1
    }
    
    # 5-fold CV
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    oof = np.zeros(len(train))
    preds = np.zeros(len(test))
    
    for fold, (train_idx, val_idx) in enumerate(skf.split(train[features], train[target_col])):
        print(f"Fold {fold + 1}")
        
        X_train, X_val = train[features].iloc[train_idx], train[features].iloc[val_idx]
        y_train, y_val = train[target_col].iloc[train_idx], train[target_col].iloc[val_idx]
        
        train_set = lgb.Dataset(X_train, y_train)
        val_set = lgb.Dataset(X_val, y_val)
        
        model = lgb.train(
            params,
            train_set,
            valid_sets=[val_set],
            num_boost_round=1000,
            callbacks=[lgb.early_stopping(50), lgb.log_evaluation(100)]
        )
        
        oof[val_idx] = model.predict(X_val)
        preds += model.predict(test[features]) / 5
    
    score = roc_auc_score(train[target_col], oof)
    print(f"Baseline AUC: {score:.5f}")
    
    return oof, preds, score

# ============================================================
# 3. ADVANCED FEATURE ENGINEERING
# ============================================================

def create_advanced_features(df, is_train=True):
    """Create advanced features for topline solution"""
    
    # 3.1 Time-based features
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['dayofweek'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
        
        # Cyclical encoding
        df['hour_sin'] = np.sin(df['hour'] / 24 * 2 * np.pi)
        df['hour_cos'] = np.cos(df['hour'] / 24 * 2 * np.pi)
        df['dow_sin'] = np.sin(df['dayofweek'] / 7 * 2 * np.pi)
        df['dow_cos'] = np.cos(df['dayofweek'] / 7 * 2 * np.pi)
    
    # 3.2 Group aggregation features
    if 'user_id' in df.columns:
        # User-level statistics
        for col in ['feature1', 'feature2']:
            if col in df.columns:
                df[f'{col}_user_mean'] = df.groupby('user_id')[col].transform('mean')
                df[f'{col}_user_std'] = df.groupby('user_id')[col].transform('std')
                df[f'{col}_user_max'] = df.groupby('user_id')[col].transform('max')
                df[f'{col}_user_min'] = df.groupby('user_id')[col].transform('min')
                
                # Relative features
                df[f'{col}_user_ratio'] = df[col] / (df[f'{col}_user_mean'] + 1e-8)
    
    # 3.3 Interaction features
    if 'feature1' in df.columns and 'feature2' in df.columns:
        df['f1_f2_ratio'] = df['feature1'] / (df['feature2'] + 1e-8)
        df['f1_f2_diff'] = df['feature1'] - df['feature2']
        df['f1_f2_sum'] = df['feature1'] + df['feature2']
        df['f1_f2_product'] = df['feature1'] * df['feature2']
    
    # 3.4 Lag features for time series
    if 'timestamp' in df.columns and 'user_id' in df.columns:
        df = df.sort_values(['user_id', 'timestamp'])
        for col in ['feature1', 'feature2']:
            if col in df.columns:
                df[f'{col}_lag1'] = df.groupby('user_id')[col].shift(1)
                df[f'{col}_diff1'] = df[col] - df[f'{col}_lag1']
    
    # 3.5 Statistical features
    num_cols = df.select_dtypes(include=[np.number]).columns
    df['row_mean'] = df[num_cols].mean(axis=1)
    df['row_std'] = df[num_cols].std(axis=1)
    df['row_max'] = df[num_cols].max(axis=1)
    df['row_min'] = df[num_cols].min(axis=1)
    
    return df

# ============================================================
# 4. TOPLINE MODEL WITH ADVANCED TECHNIQUES
# ============================================================

def train_topline(train, test, target_col='target'):
    """Train topline model with advanced features and techniques"""
    
    # Feature engineering
    train = create_advanced_features(train, is_train=True)
    test = create_advanced_features(test, is_train=False)
    
    features = [c for c in train.columns if c not in [target_col, 'id', 'timestamp']]
    
    # Advanced parameters
    params = {
        'objective': 'binary',
        'metric': 'auc',
        'num_leaves': 64,
        'learning_rate': 0.05,
        'feature_fraction': 0.8,
        'bagging_fraction': 0.9,
        'bagging_freq': 4,
        'reg_alpha': 0.2,
        'reg_lambda': 0.2,
        'min_child_samples': 20,
        'verbose': -1
    }
    
    # 10-fold CV with multiple seeds
    seeds = [42, 123, 456]
    oof = np.zeros(len(train))
    preds = np.zeros(len(test))
    
    for seed in seeds:
        skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(train[features], train[target_col])):
            X_train, X_val = train[features].iloc[train_idx], train[features].iloc[val_idx]
            y_train, y_val = train[target_col].iloc[train_idx], train[target_col].iloc[val_idx]
            
            train_set = lgb.Dataset(X_train, y_train)
            val_set = lgb.Dataset(X_val, y_val)
            
            model = lgb.train(
                params,
                train_set,
                valid_sets=[val_set],
                num_boost_round=2000,
                callbacks=[lgb.early_stopping(100), lgb.log_evaluation(200)]
            )
            
            oof[val_idx] += model.predict(X_val) / len(seeds)
            preds += model.predict(test[features]) / (len(seeds) * 10)
    
    score = roc_auc_score(train[target_col], oof)
    print(f"Topline AUC: {score:.5f}")
    
    return oof, preds, score

# ============================================================
# 5. MODEL FUSION (Ensemble)
# ============================================================

def create_ensemble(models_dict, test_df):
    """Create ensemble from multiple models"""
    # models_dict: {'model_name': (oof, preds, score)}
    
    # Rank-based fusion
    final_preds = np.zeros(len(test_df))
    total_weight = 0
    
    for name, (oof, preds, score) in models_dict.items():
        # Weight by performance
        weight = score
        final_preds += preds * weight
        total_weight += weight
    
    final_preds /= total_weight
    
    return final_preds

# ============================================================
# 6. MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("COMPETITIVE DATA SCIENCE: BASELINE TO TOPLINE")
    print("=" * 60)
    
    # Load data (replace with actual paths)
    # train, test = load_data('data/train.csv', 'data/test.csv')
    
    # For demonstration, create sample data
    np.random.seed(42)
    n_train, n_test = 1000, 500
    
    train = pd.DataFrame({
        'id': range(n_train),
        'feature1': np.random.randn(n_train),
        'feature2': np.random.randn(n_train),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_train),
        'user_id': np.random.randint(1, 100, n_train),
        'timestamp': pd.date_range('2024-01-01', periods=n_train, freq='H'),
        'target': np.random.randint(0, 2, n_train)
    })
    
    test = pd.DataFrame({
        'id': range(n_test),
        'feature1': np.random.randn(n_test),
        'feature2': np.random.randn(n_test),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_test),
        'user_id': np.random.randint(1, 100, n_test),
        'timestamp': pd.date_range('2024-01-15', periods=n_test, freq='H')
    })
    
    print("\n1. BASELINE MODEL")
    print("-" * 40)
    baseline_oof, baseline_preds, baseline_score = train_baseline(train.copy(), test.copy())
    
    print("\n2. TOPLINE MODEL")
    print("-" * 40)
    topline_oof, topline_preds, topline_score = train_topline(train.copy(), test.copy())
    
    print("\n3. PERFORMANCE COMPARISON")
    print("-" * 40)
    print(f"Baseline AUC: {baseline_score:.5f}")
    print(f"Topline AUC: {topline_score:.5f}")
    print(f"Improvement: {(topline_score - baseline_score) * 100:.2f}%")
    
    # Example ensemble
    print("\n4. ENSEMBLE (if multiple models available)")
    print("-" * 40)
    models_dict = {
        'baseline': (baseline_oof, baseline_preds, baseline_score),
        'topline': (topline_oof, topline_preds, topline_score)
    }
    ensemble_preds = create_ensemble(models_dict, test)
    print(f"Ensemble predictions created: {len(ensemble_preds)} samples")
    
    print("\n" + "=" * 60)
    print("WORKFLOW COMPLETE")
    print("=" * 60)
