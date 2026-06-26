---
name: electricity-forecasting
description: Comprehensive electricity load and demand forecasting framework. Supports statistical methods (ARIMA, SARIMA), machine learning (XGBoost, LightGBM, Random Forest), and deep learning (LSTM, GRU, Transformer, TFT). Use when building short-term load forecasting (STLF) systems, predicting electricity demand for energy trading, analyzing consumption patterns, integrating weather features, evaluating forecasts with MAPE/RMSE/MAE, or deploying production pipelines with uncertainty quantification.
---

# Electricity Forecasting Framework

## Overview

This skill provides end-to-end support for electricity load/demand forecasting projects, from data preprocessing to model deployment. It covers traditional statistical methods, modern machine learning approaches, and state-of-the-art deep learning architectures.

## Quick Start

### 1. Define Your Forecasting Task

| Horizon | Type | Typical Use |
|---------|------|-------------|
| 1-48 hours | Short-term (STLF) | Grid operations, unit commitment |
| 1 week - 1 month | Medium-term | Maintenance scheduling, fuel planning |
| 1-12 months | Long-term (LTLF) | Capacity planning, infrastructure investment |

### 2. Prepare Your Data

```bash
# Run the data preparation script
python scripts/prepare_data.py --input raw_load.csv --output processed/
```

Required data columns:
- `timestamp`: Datetime index (hourly or sub-hourly)
- `load`: Target variable (MW or kWh)
- `temperature`: Weather feature (°C)
- Optional: humidity, wind_speed, solar_radiation, holiday_flag

### 3. Select Your Model

See [references/model-selection.md](references/model-selection.md) for detailed guidance.

**Quick recommendation:**
- **Baseline**: Start with `persistence` or `seasonal-naive`
- **Production STLF**: Use `XGBoost` or `LightGBM` with weather features
- **Research/SOTA**: Try `Temporal Fusion Transformer (TFT)` or `iTransformer`

### 4. Train and Evaluate

```bash
python scripts/train_model.py --model xgboost --data processed/ --horizon 24
```

Key metrics to track:
- **MAPE** (%): Mean Absolute Percentage Error - business interpretability
- **RMSE** (MW): Root Mean Square Error - penalizes large errors
- **MAE** (MW): Mean Absolute Error - robust to outliers
- **Coverage** (%): Prediction interval coverage probability

## Core Workflows

### Data Preprocessing

1. **Load raw data** with proper datetime parsing
2. **Handle missing values**: Forward-fill for short gaps, interpolate for longer
3. **Feature engineering**:
   - Temporal: hour, day_of_week, month, is_weekend, is_holiday
   - Lag features: load_t-1, load_t-24, load_t-168 (weekly)
   - Rolling stats: rolling_mean_24h, rolling_std_7d
   - Weather: temperature, humidity, apparent_temperature
4. **Normalization**: RobustScaler or MinMaxScaler for deep learning models

See [references/feature-engineering.md](references/feature-engineering.md) for complete feature list.

### Model Training

```python
# Example training workflow
from electricity_forecasting import ForecastPipeline

pipeline = ForecastPipeline(
    model_type="xgboost",
    horizon=24,
    lookback=168  # 1 week of history
)

pipeline.fit(train_data, val_data)
predictions, uncertainty = pipeline.predict(test_data)
metrics = pipeline.evaluate(predictions, actuals)
```

### Hyperparameter Tuning

Use `scripts/hyperparameter_search.py` for automated tuning:

```bash
python scripts/hyperparameter_search.py \
  --model lightgbm \
  --data processed/ \
  --n-trials 50 \
  --study-name stlf-tuning
```

### Uncertainty Quantification

For risk-aware decision making:

- **Quantile Regression**: Predict multiple quantiles (0.1, 0.5, 0.9)
- **Conformal Prediction**: Distribution-free uncertainty bounds
- **Ensemble Methods**: Model disagreement as uncertainty proxy
- **Monte Carlo Dropout**: For neural networks

See [references/uncertainty.md](references/uncertainty.md) for implementation details.

## Model Reference

### Statistical Models

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| ARIMA | Stable series | Interpretable, fast | Assumes linearity |
| SARIMA | Strong seasonality | Captures daily/weekly patterns | Manual parameter tuning |
| Prophet | Multiple seasonalities | Handles holidays well | Less accurate for STLF |
| TBATS | Complex seasonality | Automatic parameter selection | Slower training |

### Machine Learning Models

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| XGBoost | Production STLF | Fast, accurate, handles missing | No native uncertainty |
| LightGBM | Large datasets | Faster than XGBoost, memory efficient | Sensitive to hyperparameters |
| Random Forest | Baseline ML | Robust, easy to tune | Lower accuracy than boosting |
| CatBoost | Categorical features | Handles categoricals natively | Slower training |

### Deep Learning Models

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| LSTM | Sequential patterns | Captures long-term dependencies | Slow training, hard to tune |
| GRU | Similar to LSTM | Faster convergence | Similar limitations |
| Transformer | Long sequences | Parallel training, attention | Data-hungry, complex |
| TFT | Multi-horizon | Interpretable attention, uncertainty | Complex implementation |
| N-BEATS | Pure deep learning | Strong baseline, interpretable | Less flexible than TFT |
| iTransformer | SOTA performance | Inverted transformer architecture | Recent, less battle-tested |

See [references/deep-learning-models.md](references/deep-learning-models.md) for architecture details and PyTorch implementations.

## Evaluation Best Practices

### Time Series Cross-Validation

Never use random k-fold! Use expanding or sliding window:

```python
# Expanding window CV
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5, test_size=168)  # 1 week test
for train_idx, test_idx in tscv.split(data):
    train, test = data[train_idx], data[test_idx]
    # Train and evaluate
```

### Backtesting Framework

```bash
python scripts/backtest.py \
  --model xgboost \
  --data processed/ \
  --cv-splits 5 \
  --horizon 24 \
  --metrics mape,rmse,mae
```

### Benchmark Comparison

Always compare against:
1. **Persistence**: load_t = load_t-1
2. **Seasonal Naive**: load_t = load_t-24 (for hourly data)
3. **Weekly Naive**: load_t = load_t-168

## Deployment

### Production Pipeline

1. **Model serialization**: Save with joblib or ONNX
2. **Feature pipeline**: Ensure identical preprocessing at inference
3. **Scheduling**: Cron or Airflow for automated forecasts
4. **Monitoring**: Track forecast drift and retrain triggers

See [references/deployment.md](references/deployment.md) for MLOps patterns.

### Real-time Inference

```python
from electricity_forecasting import DeploymentModel

model = DeploymentModel.load("models/xgboost-stlf.joblib")
features = prepare_features(latest_data)
prediction = model.predict(features, return_uncertainty=True)
```

## Common Pitfalls

1. **Data leakage**: Ensure no future information in features
2. **Holiday handling**: Special days need explicit modeling
3. **Temperature nonlinearity**: Use heating/cooling degree days
4. **Concept drift**: Retrain quarterly or when MAPE degrades >20%
5. **Peak prediction**: Models often under-predict peaks - consider quantile loss

## Resources

- [Feature Engineering Guide](references/feature-engineering.md)
- [Model Selection Guide](references/model-selection.md)
- [Deep Learning Architectures](references/deep-learning-models.md)
- [Uncertainty Quantification](references/uncertainty.md)
- [Deployment Patterns](references/deployment.md)
- [Datasets Reference](references/datasets.md)

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/prepare_data.py` | Data cleaning and feature engineering |
| `scripts/train_model.py` | Model training with validation |
| `scripts/hyperparameter_search.py` | Automated hyperparameter optimization |
| `scripts/backtest.py` | Time series cross-validation |
| `scripts/evaluate.py` | Comprehensive metric calculation |
| `scripts/deploy_model.py` | Export model for production |

## Example Usage

```bash
# Complete workflow example
# 1. Prepare data
python scripts/prepare_data.py --input data/load_2024.csv --output data/processed/

# 2. Train model
python scripts/train_model.py --model lightgbm --data data/processed/ --horizon 48

# 3. Hyperparameter tuning
python scripts/hyperparameter_search.py --model lightgbm --data data/processed/ --n-trials 100

# 4. Backtest
python scripts/backtest.py --model lightgbm-best --data data/processed/ --cv-splits 5

# 5. Deploy
python scripts/deploy_model.py --model lightgbm-best --output models/production/
```
