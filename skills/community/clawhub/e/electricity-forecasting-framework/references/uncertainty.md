# Uncertainty Quantification Guide

## Why Uncertainty Matters

Point forecasts alone are insufficient for decision-making in electricity systems:

- **Grid operations**: Need to know worst-case scenarios for reserve planning
- **Energy trading**: Risk management requires probability distributions
- **Maintenance scheduling**: Confidence intervals inform scheduling flexibility
- **Renewable integration**: Variability quantification essential for balancing

## Methods Overview

| Method | Type | Coverage Accuracy | Computational Cost | Calibration Required |
|--------|------|-------------------|-------------------|---------------------|
| Quantile Regression | Distributional | High | Low | Minimal |
| Conformal Prediction | Distribution-free | Guaranteed | Low | Yes |
| MC Dropout | Bayesian approximation | Medium | Medium | Yes |
| Deep Ensembles | Bayesian approximation | High | High | Yes |
| Gaussian Processes | Probabilistic | High | Very High | Minimal |
| NGBoost | Distributional | High | Medium | Minimal |

## 1. Quantile Regression

### Concept

Instead of predicting a single value, predict multiple quantiles of the distribution:

```python
quantiles = [0.05, 0.25, 0.5, 0.75, 0.95]
# Output: [5th percentile, 25th, median, 75th, 95th]
# Interpretation: 90% prediction interval = [5th, 95th]
```

### Implementation with LightGBM

```python
import lightgbm as lgb
import numpy as np

class QuantileLightGBM:
    def __init__(self, quantiles=[0.1, 0.5, 0.9]):
        self.quantiles = quantiles
        self.models = {}
    
    def fit(self, X_train, y_train, **kwargs):
        """Train separate model for each quantile."""
        for q in self.quantiles:
            model = lgb.LGBMRegressor(
                objective='quantile',
                alpha=q,
                n_estimators=1000,
                learning_rate=0.05,
                num_leaves=31,
                **kwargs
            )
            model.fit(X_train, y_train)
            self.models[q] = model
        return self
    
    def predict(self, X):
        """Predict all quantiles."""
        predictions = {}
        for q, model in self.models.items():
            predictions[q] = model.predict(X)
        return predictions
    
    def predict_interval(self, X, confidence=0.9):
        """Get prediction interval."""
        alpha = (1 - confidence) / 2
        lower_q = alpha
        upper_q = 1 - alpha
        
        lower = self.models[lower_q].predict(X)
        upper = self.models[upper_q].predict(X)
        median = self.models[0.5].predict(X)
        
        return median, lower, upper

# Usage
model = QuantileLightGBM(quantiles=[0.1, 0.25, 0.5, 0.75, 0.9])
model.fit(X_train, y_train)

median, lower, upper = model.predict_interval(X_test, confidence=0.8)
```

### Implementation with PyTorch

```python
import torch
import torch.nn as nn

class QuantileLoss(nn.Module):
    def __init__(self, quantiles):
        super().__init__()
        self.quantiles = quantiles
    
    def forward(self, preds, target):
        """
        preds: (batch, n_quantiles)
        target: (batch,)
        """
        losses = []
        for i, q in enumerate(self.quantiles):
            errors = target.unsqueeze(1) - preds[:, i:i+1]
            loss_q = torch.max((q - 1) * errors, q * errors)
            losses.append(loss_q)
        
        return torch.mean(torch.cat(losses, dim=1))

class QuantileNN(nn.Module):
    def __init__(self, input_size, n_quantiles=5):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, 64),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, n_quantiles)
        )
    
    def forward(self, x):
        return self.network(x)

# Training
quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
model = QuantileNN(input_size=20, n_quantiles=len(quantiles))
criterion = QuantileLoss(quantiles)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

### Evaluation: Coverage Probability

```python
def calculate_coverage(y_true, y_lower, y_upper, confidence=0.9):
    """Calculate actual coverage of prediction interval."""
    within_interval = (y_true >= y_lower) & (y_true <= y_upper)
    actual_coverage = within_interval.mean()
    return actual_coverage

def calculate_sharpness(y_lower, y_upper):
    """Calculate average interval width (sharper = better)."""
    return np.mean(y_upper - y_lower)

# Evaluate
coverage = calculate_coverage(y_test, lower, upper, confidence=0.8)
sharpness = calculate_sharpness(lower, upper)

print(f"Target coverage: 80%")
print(f"Actual coverage: {coverage*100:.1f}%")
print(f"Average interval width: {sharpness:.2f} MW")
```

### Calibration

If coverage doesn't match target, calibrate:

```python
def calibrate_quantiles(y_true, y_pred_quantiles, target_coverage=0.9):
    """Adjust quantile levels to achieve target coverage."""
    from scipy.optimize import brentq
    
    def coverage_error(alpha):
        lower_q = alpha / 2
        upper_q = 1 - alpha / 2
        lower = y_pred_quantiles[lower_q]
        upper = y_pred_quantiles[upper_q]
        coverage = (y_true >= lower) & (y_true <= upper)
        return coverage.mean() - target_coverage
    
    # Find alpha that gives target coverage
    optimal_alpha = brentq(coverage_error, 0.01, 0.5)
    return optimal_alpha
```

## 2. Conformal Prediction

### Concept

Conformal prediction provides **guaranteed coverage** under minimal assumptions (exchangeability).

### Split Conformal for Regression

```python
class ConformalPredictor:
    def __init__(self, base_model, confidence=0.9):
        self.base_model = base_model
        self.confidence = confidence
        self.quantile_residual = None
    
    def fit(self, X_train, y_train, X_cal, y_cal):
        """
        Fit base model on training data.
        Calibrate on separate calibration set.
        """
        # Fit base model
        self.base_model.fit(X_train, y_train)
        
        # Get predictions on calibration set
        cal_preds = self.base_model.predict(X_cal)
        
        # Calculate absolute residuals
        residuals = np.abs(y_cal - cal_preds)
        
        # Find quantile of residuals
        n = len(residuals)
        q_level = np.ceil((n + 1) * (1 - self.confidence)) / n
        q_level = min(q_level, 1.0)
        
        self.quantile_residual = np.quantile(residuals, q_level)
        return self
    
    def predict(self, X):
        """Predict with conformal interval."""
        point_pred = self.base_model.predict(X)
        lower = point_pred - self.quantile_residual
        upper = point_pred + self.quantile_residual
        return point_pred, lower, upper

# Usage with cross-conformal (more efficient)
from sklearn.model_selection import KFold

def cross_conformal_prediction(model_class, X, y, confidence=0.9, n_splits=5):
    """Cross-conformal prediction for better data efficiency."""
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    residuals = np.zeros(len(y))
    predictions = np.zeros(len(y))
    
    for train_idx, cal_idx in kf.split(X):
        X_train, X_cal = X[train_idx], X[cal_idx]
        y_train, y_cal = y[train_idx], y[cal_idx]
        
        model = model_class()
        model.fit(X_train, y_train)
        
        cal_preds = model.predict(X_cal)
        residuals[cal_idx] = np.abs(y_cal - cal_preds)
        predictions[cal_idx] = cal_preds
    
    # Calculate conformal quantile
    n = len(residuals)
    q_level = np.ceil((n + 1) * (1 - confidence)) / n
    quantile_residual = np.quantile(residuals, min(q_level, 1.0))
    
    return quantile_residual

# Apply to new data
quantile_r = cross_conformal_prediction(LGBMRegressor, X_train, y_train)
point_pred = final_model.predict(X_test)
lower = point_pred - quantile_r
upper = point_pred + quantile_r
```

### Conformalized Quantile Regression (CQR)

Combines quantile regression with conformal calibration:

```python
class CQRPredictor:
    def __init__(self, quantile_model, confidence=0.9):
        self.quantile_model = quantile_model
        self.confidence = confidence
        self.correction = 0
    
    def fit(self, X_train, y_train, X_cal, y_cal):
        """Fit quantile model and calibrate."""
        # Fit quantile model
        self.quantile_model.fit(X_train, y_train)
        
        # Get quantile predictions on calibration set
        cal_preds = self.quantile_model.predict(X_cal)
        cal_lower = cal_preds[0.1]  # Example: 10th percentile
        cal_upper = cal_preds[0.9]  # Example: 90th percentile
        
        # Calculate conformity scores
        scores = np.maximum(cal_lower - y_cal, y_cal - cal_upper)
        
        # Find correction quantile
        n = len(scores)
        q_level = np.ceil((n + 1) * (1 - self.confidence)) / n
        self.correction = np.quantile(scores, min(q_level, 1.0))
        
        return self
    
    def predict(self, X):
        """Predict with conformalized interval."""
        preds = self.quantile_model.predict(X)
        lower = preds[0.1] - self.correction
        upper = preds[0.9] + self.correction
        return preds[0.5], lower, upper
```

## 3. Monte Carlo Dropout

### Concept

Use dropout at inference time to generate multiple predictions, treating variance as uncertainty.

```python
def enable_dropout(model):
    """Enable dropout layers during inference."""
    for module in model.modules():
        if isinstance(module, nn.Dropout):
            module.train()

def mc_dropout_predict(model, X, n_samples=50):
    """Generate predictions with MC dropout."""
    enable_dropout(model)
    
    predictions = []
    with torch.no_grad():
        for _ in range(n_samples):
            pred = model(X)
            predictions.append(pred.cpu().numpy())
    
    predictions = np.stack(predictions, axis=0)
    mean = predictions.mean(axis=0)
    std = predictions.std(axis=0)
    
    return mean, std

# Calculate prediction interval
mean, std = mc_dropout_predict(model, X_test, n_samples=50)
lower = mean - 1.96 * std  # 95% interval
upper = mean + 1.96 * std
```

### Calibration for MC Dropout

MC dropout intervals often need calibration:

```python
def calibrate_mc_dropout(y_true, mean_pred, std_pred, target_coverage=0.95):
    """Find scaling factor for MC dropout uncertainty."""
    from scipy.optimize import minimize_scalar
    
    def calibration_loss(scale):
        lower = mean_pred - scale * std_pred
        upper = mean_pred + scale * std_pred
        coverage = ((y_true >= lower) & (y_true <= upper)).mean()
        return (coverage - target_coverage) ** 2
    
    result = minimize_scalar(calibration_loss, bounds=(0.5, 3.0), method='bounded')
    return result.x

# Apply calibration
scale_factor = calibrate_mc_dropout(y_val, mean_val, std_val)
lower_calibrated = mean_test - scale_factor * std_test
upper_calibrated = mean_test + scale_factor * std_test
```

## 4. Deep Ensembles

### Concept

Train multiple models with different random seeds and aggregate predictions.

```python
class DeepEnsemble:
    def __init__(self, model_class, n_models=5, **model_kwargs):
        self.model_class = model_class
        self.n_models = n_models
        self.models = []
        self.model_kwargs = model_kwargs
    
    def fit(self, X_train, y_train, X_val, y_val):
        """Train ensemble with early stopping."""
        for i in range(self.n_models):
            # Different random seed for each model
            torch.manual_seed(42 + i)
            np.random.seed(42 + i)
            
            model = self.model_class(**self.model_kwargs)
            trained_model = train_with_early_stopping(
                model, X_train, y_train, X_val, y_val
            )
            self.models.append(trained_model)
        
        return self
    
    def predict(self, X):
        """Predict with uncertainty."""
        predictions = []
        for model in self.models:
            pred = model.predict(X)
            predictions.append(pred)
        
        predictions = np.stack(predictions, axis=0)
        mean = predictions.mean(axis=0)
        std = predictions.std(axis=0)
        
        # For 95% interval, use t-distribution with n_models-1 dof
        from scipy.stats import t
        t_value = t.ppf(0.975, df=self.n_models - 1)
        lower = mean - t_value * std
        upper = mean + t_value * std
        
        return mean, lower, upper, std
```

## 5. NGBoost (Natural Gradient Boosting)

### Concept

Gradient boosting for probabilistic prediction with proper scoring rules.

```python
from ngboost import NGBRegressor
from ngboost.distns import Normal, LogNormal
from ngboost.scores import MLE

# Fit probabilistic model
ngb = NGBRegressor(
    Dist=Normal,  # or LogNormal for positive-only targets
    Score=MLE,
    n_estimators=500,
    learning_rate=0.01,
    verbose=True
)

ngb.fit(X_train, y_train)

# Predict distribution parameters
params = ngb.pred_dist(X_test)
mean = params.loc  # Mean
std = params.scale  # Standard deviation

# Get prediction intervals
lower = params.ppf(0.05)  # 5th percentile
upper = params.ppf(0.95)  # 95th percentile
```

## Evaluation Metrics

### Coverage Probability

```python
def coverage_probability(y_true, y_lower, y_upper):
    """Fraction of observations within prediction interval."""
    within = (y_true >= y_lower) & (y_true <= y_upper)
    return within.mean()
```

### Interval Width (Sharpness)

```python
def mean_interval_width(y_lower, y_upper):
    """Average width of prediction intervals."""
    return np.mean(y_upper - y_lower)
```

### Continuous Ranked Probability Score (CRPS)

```python
from properscoring import crps_quadrature

def calculate_crps(y_true, pred_dist):
    """
    Calculate CRPS for probabilistic forecasts.
    Lower is better.
    """
    crps_values = []
    for i in range(len(y_true)):
        crps = crps_quadrature(
            x=y_true[i],
            cdf_or_dist=pred_dist[i]
        )
        crps_values.append(crps)
    return np.mean(crps_values)
```

### Pinball Loss (for Quantile Forecasts)

```python
def pinball_loss(y_true, y_pred, quantile):
    """Calculate pinball loss for a single quantile."""
    errors = y_true - y_pred
    loss = np.maximum((quantile - 1) * errors, quantile * errors)
    return loss.mean()

def mean_pinball_loss(y_true, y_pred_quantiles):
    """Average pinball loss across all quantiles."""
    losses = []
    for q, preds in y_pred_quantiles.items():
        losses.append(pinball_loss(y_true, preds, q))
    return np.mean(losses)
```

## Complete Uncertainty Pipeline

```python
class UncertaintyPipeline:
    """Complete uncertainty quantification pipeline."""
    
    def __init__(self, method='quantile', confidence=0.9):
        self.method = method
        self.confidence = confidence
        self.model = None
    
    def fit(self, X_train, y_train, X_val, y_val):
        if self.method == 'quantile':
            self.model = QuantileLightGBM(
                quantiles=[0.1, 0.25, 0.5, 0.75, 0.9]
            )
            self.model.fit(X_train, y_train)
        
        elif self.method == 'conformal':
            from sklearn.model_selection import train_test_split
            X_tr, X_cal, y_tr, y_cal = train_test_split(
                X_train, y_train, test_size=0.2
            )
            base_model = lgb.LGBMRegressor()
            self.model = ConformalPredictor(base_model, self.confidence)
            self.model.fit(X_tr, y_tr, X_cal, y_cal)
        
        elif self.method == 'ensemble':
            self.model = DeepEnsemble(LSTMForecaster, n_models=5)
            self.model.fit(X_train, y_train, X_val, y_val)
        
        return self
    
    def predict(self, X):
        if self.method == 'quantile':
            preds = self.model.predict(X)
            median = preds[0.5]
            lower = preds[0.1]
            upper = preds[0.9]
        
        elif self.method == 'conformal':
            median, lower, upper = self.model.predict(X)
        
        elif self.method == 'ensemble':
            median, lower, upper, _ = self.model.predict(X)
        
        return {
            'median': median,
            'lower': lower,
            'upper': upper,
            'width': upper - lower
        }
    
    def evaluate(self, y_true, predictions):
        coverage = coverage_probability(y_true, predictions['lower'], predictions['upper'])
        width = mean_interval_width(predictions['lower'], predictions['upper'])
        
        return {
            'coverage': coverage,
            'target_coverage': self.confidence,
            'coverage_error': abs(coverage - self.confidence),
            'mean_width': width
        }
```

## Recommendations by Use Case

| Use Case | Recommended Method | Reason |
|----------|-------------------|--------|
| Production STLF | Quantile LightGBM | Fast, well-calibrated, easy |
| Energy Trading | CQR | Guaranteed coverage, sharp |
| Grid Operations | Deep Ensemble | Robust, captures model uncertainty |
| Research/SOTA | TFT with quantiles | Native uncertainty, interpretable |
| Limited Data | Conformal | Distribution-free guarantees |

## Common Pitfalls

1. **Using training data for calibration**: Always use held-out calibration set
2. **Ignoring coverage-sharpness tradeoff**: Wider intervals = higher coverage but less useful
3. **No recalibration over time**: Recalibrate quarterly as data distribution shifts
4. **Assuming normality**: Electricity load is often skewed - use quantile methods
5. **Not evaluating coverage**: Always verify actual coverage matches target
