# Model Selection Guide

## Decision Framework

### Step 1: Define Your Requirements

Answer these questions before selecting a model:

1. **Forecast horizon**: How far ahead do you need to predict?
   - Short-term (1-48h): Most models work well
   - Medium-term (1 week - 1 month): Consider SARIMA, Prophet, TFT
   - Long-term (1-12 months): Focus on trend modeling, SARIMA, Prophet

2. **Data availability**: How much historical data do you have?
   - < 6 months: Statistical models (ARIMA, SARIMA)
   - 6 months - 2 years: ML models (XGBoost, LightGBM)
   - > 2 years: Deep learning becomes viable

3. **Accuracy requirements**: What MAPE is acceptable?
   - < 2%: Ensemble of multiple models
   - 2-5%: LightGBM/XGBoost with good features
   - 5-10%: Single ML model or SARIMA
   - > 10%: Start with data quality improvement

4. **Latency requirements**: How fast must predictions be?
   - < 1 second: XGBoost, LightGBM, simple statistical
   - 1-10 seconds: Most ML models, small neural networks
   - > 10 seconds: Large deep learning models acceptable

5. **Interpretability needs**: Do you need to explain predictions?
   - High: SARIMA, Prophet, linear models, tree-based with SHAP
   - Medium: XGBoost/LightGBM with feature importance
   - Low: Deep learning models (LSTM, Transformer)

### Step 2: Model Recommendations by Scenario

#### Scenario A: Production STLF System (Utility Company)

**Requirements**: Hourly forecasts, 24-48h horizon, MAPE < 3%, sub-second latency

**Recommended stack**:
```
Primary: LightGBM with weather features
Backup: SARIMA for fallback
Ensemble: Weighted average (0.7 LightGBM + 0.3 SARIMA)
```

**Feature set**:
- Lag features: t-1, t-24, t-48, t-168
- Rolling statistics: 24h mean, 7d mean, 24h std
- Weather: temperature, humidity, apparent_temperature
- Calendar: hour, day_of_week, is_weekend, is_holiday
- Interaction: temperature × hour (capture AC/heating patterns)

**Expected performance**: MAPE 1.5-2.5%, RMSE depends on load scale

#### Scenario B: Energy Trading Desk

**Requirements**: 15-minute intervals, 1-6h horizon, uncertainty quantification critical

**Recommended stack**:
```
Primary: Quantile LightGBM (predict 0.1, 0.5, 0.9 quantiles)
Alternative: Conformalized XGBoost
Deep learning: TFT for multi-horizon
```

**Key considerations**:
- Predict full distribution, not just point forecast
- Calibrate prediction intervals using validation data
- Monitor interval coverage ratio (should match confidence level)

#### Scenario C: Research / SOTA Performance

**Requirements**: Best possible accuracy, computational cost secondary

**Recommended stack**:
```
Primary: Temporal Fusion Transformer (TFT)
Alternative: iTransformer or PatchTST
Ensemble: TFT + LightGBM + SARIMA
```

**Expected improvement**: 10-20% reduction in MAPE vs single LightGBM

**Trade-offs**:
- Training time: hours to days vs minutes
- Data requirements: > 2 years high-quality data
- Hyperparameter sensitivity: requires careful tuning

#### Scenario D: Limited Data (< 1 year)

**Requirements**: Reasonable forecasts with minimal history

**Recommended stack**:
```
Primary: SARIMA with automatic parameter selection
Backup: Exponential smoothing (ETS)
Avoid: Deep learning (will overfit)
```

**Data augmentation strategies**:
- Use synthetic data for similar days
- Transfer learning from similar locations
- Focus on strong seasonal patterns

#### Scenario E: Multi-site Forecasting

**Requirements**: Forecast 100+ locations simultaneously

**Recommended stack**:
```
Primary: Global LightGBM (train on all sites with site embedding)
Alternative: Hierarchical reconciliation (bottom-up or top-down)
Consider: Panel data methods, N-BEATSx
```

**Key insight**: Global models often outperform per-site models due to shared patterns

### Step 3: Comparison Matrix

| Model | Data Needed | Training Time | Inference Time | MAPE Range | Uncertainty | Interpretability |
|-------|-------------|---------------|----------------|------------|-------------|------------------|
| Persistence | Any | None | <1ms | 5-15% | No | N/A |
| Seasonal Naive | >1 month | None | <1ms | 3-10% | No | High |
| ARIMA | >6 months | Seconds | <10ms | 3-8% | Yes (confidence) | High |
| SARIMA | >6 months | Seconds-minutes | <10ms | 2-6% | Yes (confidence) | High |
| Prophet | >6 months | Minutes | <100ms | 3-7% | Yes (intervals) | High |
| XGBoost | >6 months | Minutes | <10ms | 1.5-5% | No (need quantile) | Medium |
| LightGBM | >6 months | Minutes | <5ms | 1.5-4% | Yes (quantile) | Medium |
| Random Forest | >6 months | Minutes | <50ms | 2-6% | No | Medium |
| LSTM | >1 year | Hours | <50ms | 1.5-4% | Yes (MC dropout) | Low |
| GRU | >1 year | Hours | <50ms | 1.5-4% | Yes (MC dropout) | Low |
| Transformer | >2 years | Hours-days | <100ms | 1-3% | Yes (attention) | Low |
| TFT | >2 years | Hours-days | <200ms | 1-3% | Yes (native) | Medium |
| N-BEATS | >1 year | Hours | <50ms | 1.5-4% | No | Medium |
| iTransformer | >2 years | Hours-days | <100ms | 1-2.5% | No | Low |

### Step 4: Ensemble Strategies

For production systems, ensembles often provide the best balance:

#### Simple Averaging
```python
forecast = 0.4 * lightgbm_pred + 0.35 * sarima_pred + 0.25 * persistence_pred
```

#### Weighted by Recent Performance
```python
# Calculate weights based on last 7 days MAPE
weights = calculate_inverse_mape_weights(models, validation_data, window=168)
forecast = weighted_average(predictions, weights)
```

#### Stacking (Meta-learner)
```python
# Level 1: Train diverse base models
base_predictions = train_base_models(train_data)

# Level 2: Train meta-learner on base predictions
meta_model = XGBRegressor()
meta_model.fit(base_predictions[val], actuals[val])
final_forecast = meta_model.predict(base_predictions[test])
```

**Recommended base models for stacking**:
1. LightGBM (captures nonlinear patterns)
2. SARIMA (captures linear autocorrelation)
3. Neural network (captures complex temporal patterns)
4. Persistence/naive (robust baseline)

## Model-Specific Guidance

### LightGBM Best Practices

```python
import lightgbm as lgb

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
    'early_stopping_rounds': 50
}

# For quantile regression (uncertainty)
params_quantile = {
    'objective': 'quantile',
    'alpha': 0.9,  # or 0.1, 0.5 for different quantiles
    **params
}
```

### SARIMA Parameter Selection

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Automatic selection
from pmdarima import auto_arima

model = auto_arima(
    y,
    seasonal=True,
    m=24,  # hourly data, daily seasonality
    start_p=1,
    start_q=1,
    max_p=3,
    max_q=3,
    start_P=0,
    start_Q=0,
    max_P=2,
    max_Q=2,
    D=1,
    trace=True,
    error_action='ignore',
    suppress_warnings=True,
    n_jobs=-1
)
```

### TFT Configuration

```python
from pytorch_forecasting import TemporalFusionTransformer

tft = TemporalFusionTransformer.from_dataset(
    training,
    learning_rate=0.001,
    hidden_size=10,
    attention_head_size=4,
    dropout=0.1,
    hidden_continuous_size=8,
    output_size=7,  # 7 quantiles
    loss=QuantileLoss(),
    reduction="mean",
)
```

## When to Retrain

Monitor these signals:

1. **Performance degradation**: MAPE increases >20% from baseline
2. **Data drift**: Feature distribution shifts (PSI > 0.2)
3. **Concept drift**: Relationship between features and target changes
4. **Seasonal transition**: Quarterly retraining recommended
5. **Grid changes**: New major consumers/generators connected

**Retraining schedule**:
- High-frequency models: Weekly retrain with expanding window
- Standard production: Monthly full retrain
- Stable environments: Quarterly with monitoring

## Further Reading

- [Feature Engineering](feature-engineering.md) - Complete feature list and transformations
- [Deep Learning Models](deep-learning-models.md) - Architecture details
- [Uncertainty Quantification](uncertainty.md) - Prediction intervals and calibration
