# Feature Engineering Guide

## Overview

Feature engineering is the most critical factor in electricity forecasting accuracy. Well-designed features often matter more than model selection.

## Required Features

### 1. Temporal Features

```python
def create_temporal_features(df):
    """Extract time-based features from datetime index."""
    df['hour'] = df.index.hour
    df['day_of_week'] = df.index.dayofweek
    df['day_of_month'] = df.index.day
    df['month'] = df.index.month
    df['day_of_year'] = df.index.dayofyear
    df['week_of_year'] = df.index.isocalendar().week
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    df['is_month_start'] = df.index.is_month_start.astype(int)
    df['is_month_end'] = df.index.is_month_end.astype(int)
    
    # Cyclical encoding (preserves continuity)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['dow_sin'] = np.sin(2 * np.pi * df['day_of_week'] / 7)
    df['dow_cos'] = np.cos(2 * np.pi * df['day_of_week'] / 7)
    df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
    df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
    
    return df
```

**Why cyclical encoding?** Hour 23 and hour 0 are close in time, but numerically far apart (23 vs 0). Sin/cos encoding preserves this temporal proximity.

### 2. Lag Features

```python
def create_lag_features(df, target_col='load', lags=None):
    """Create lagged versions of target variable."""
    if lags is None:
        # Standard lags for hourly electricity data
        lags = [1, 2, 3, 6, 12, 24, 48, 72, 168, 336, 504, 672]
        # Same hour yesterday, 2 days ago, week ago, 2 weeks ago, 3 weeks ago, 4 weeks ago
    
    for lag in lags:
        df[f'lag_{lag}h'] = df[target_col].shift(lag)
    
    return df
```

**Key lags for electricity**:
- `lag_1h`: Immediate autoregression
- `lag_24h`: Same hour yesterday (daily seasonality)
- `lag_168h`: Same hour last week (weekly seasonality)
- `lag_336h`: Same hour 2 weeks ago

### 3. Rolling Statistics

```python
def create_rolling_features(df, target_col='load'):
    """Create rolling window statistics."""
    # Mean features
    df['rolling_mean_6h'] = df[target_col].shift(1).rolling(6).mean()
    df['rolling_mean_24h'] = df[target_col].shift(1).rolling(24).mean()
    df['rolling_mean_168h'] = df[target_col].shift(1).rolling(168).mean()
    
    # Standard deviation (volatility)
    df['rolling_std_24h'] = df[target_col].shift(1).rolling(24).std()
    df['rolling_std_168h'] = df[target_col].shift(1).rolling(168).std()
    
    # Min/max (range)
    df['rolling_min_24h'] = df[target_col].shift(1).rolling(24).min()
    df['rolling_max_24h'] = df[target_col].shift(1).rolling(24).max()
    
    # Exponential moving average (more weight on recent)
    df['ema_12h'] = df[target_col].shift(1).ewm(span=12).mean()
    df['ema_24h'] = df[target_col].shift(1).ewm(span=24).mean()
    
    return df
```

### 4. Weather Features

```python
def create_weather_features(df, weather_df):
    """Merge and transform weather data."""
    # Merge on timestamp
    df = df.join(weather_df.set_index('timestamp'))
    
    # Temperature features
    df['temp_squared'] = df['temperature'] ** 2  # U-shaped load-temp relationship
    df['temp_change_1h'] = df['temperature'].diff(1)
    df['temp_change_6h'] = df['temperature'].diff(6)
    
    # Heating and Cooling Degree Days
    base_temp = 18  # °C, adjust for your region
    df['hdd'] = np.maximum(base_temp - df['temperature'], 0)
    df['cdd'] = np.maximum(df['temperature'] - base_temp, 0)
    
    # Rolling weather stats
    df['temp_rolling_mean_6h'] = df['temperature'].rolling(6).mean()
    df['temp_rolling_mean_24h'] = df['temperature'].rolling(24).mean()
    
    # Humidity features
    if 'humidity' in df.columns:
        df['heat_index'] = calculate_heat_index(df['temperature'], df['humidity'])
    
    # Wind features
    if 'wind_speed' in df.columns:
        df['wind_chill'] = calculate_wind_chill(df['temperature'], df['wind_speed'])
    
    return df
```

**Why temperature squared?** Electricity demand has a U-shaped relationship with temperature:
- Cold weather → heating load increases
- Hot weather → cooling load increases
- Mild weather → minimum demand

### 5. Holiday and Special Events

```python
def create_holiday_features(df, country='CN'):
    """Add holiday and special day indicators."""
    import holidays
    
    # Create holiday calendar
    cn_holidays = holidays.CountryHoliday(country, years=range(2020, 2030))
    
    # Basic holiday flag
    df['is_holiday'] = df.index.map(lambda x: 1 if x in cn_holidays else 0)
    
    # Holiday proximity (demand often changes before/after holidays)
    df['days_to_holiday'] = df.index.map(lambda x: min(
        [abs((x - d).days) for d in cn_holidays.keys()], default=30
    ))
    df['is_holiday_eve'] = (df['days_to_holiday'] == 1).astype(int)
    df['is_holiday_next'] = (df['days_to_holiday'] == 0).astype(int)
    df['is_holiday_after'] = df['is_holiday'].shift(1).fillna(0).astype(int)
    
    # Special events (customize for your region)
    # Chinese New Year - extended holiday period
    df['is_cny_period'] = df['day_of_year'].between(1, 15).astype(int)  # Adjust dates
    
    # Summer vacation period (lower commercial load)
    df['is_summer_vacation'] = ((df['month'] == 7) | (df['month'] == 8)).astype(int)
    
    # Heating season (November-March in northern China)
    df['is_heating_season'] = df['month'].isin([11, 12, 1, 2, 3]).astype(int)
    
    return df
```

### 6. Interaction Features

```python
def create_interaction_features(df):
    """Create interaction terms between key features."""
    # Temperature × Time interactions (AC/heating patterns vary by hour)
    df['temp_x_hour'] = df['temperature'] * df['hour']
    df['temp_x_is_weekend'] = df['temperature'] * df['is_weekend']
    df['cdd_x_hour'] = df['cdd'] * df['hour']
    df['hdd_x_hour'] = df['hdd'] * df['hour']
    
    # Lag × Weather interactions
    df['lag_24h_x_temp'] = df['lag_24h'] * df['temperature']
    
    # Holiday × Time interactions
    df['is_holiday_x_hour'] = df['is_holiday'] * df['hour']
    
    return df
```

## Domain-Specific Features

### Industrial Load Patterns

```python
def create_industrial_features(df, industrial_schedule):
    """Features for areas with significant industrial load."""
    # Shift patterns
    df['is_shift_1'] = df['hour'].isin([6, 7, 8, 9, 10, 11, 12, 13, 14]).astype(int)
    df['is_shift_2'] = df['hour'].isin([14, 15, 16, 17, 18, 19, 20, 21, 22]).astype(int)
    df['is_shift_3'] = df['hour'].isin([22, 23, 0, 1, 2, 3, 4, 5, 6]).astype(int)
    
    # Workday indicator (industrial load drops on weekends)
    df['is_workday'] = ((df['day_of_week'] < 5) & (df['is_holiday'] == 0)).astype(int)
    
    # Month-end effect (production ramp-up)
    df['is_month_end_production'] = df['day_of_month'].between(25, 31).astype(int)
    
    return df
```

### Commercial/Office Load

```python
def create_commercial_features(df):
    """Features for commercial/office dominated areas."""
    # Business hours
    df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 18)).astype(int)
    df['is_business_hours_weekday'] = (
        df['is_business_hours'] & (df['day_of_week'] < 5) & (df['is_holiday'] == 0)
    ).astype(int)
    
    # Lunch dip
    df['is_lunch_hour'] = df['hour'].isin([12, 13]).astype(int)
    
    # After-hours HVAC
    df['is_after_hours_hvac'] = ((df['hour'] >= 18) & (df['hour'] <= 22)).astype(int)
    
    return df
```

### Residential Load

```python
def create_residential_features(df):
    """Features for residential dominated areas."""
    # Morning peak (getting ready for work)
    df['is_morning_peak'] = df['hour'].isin([6, 7, 8, 9]).astype(int)
    
    # Evening peak (returning home)
    df['is_evening_peak'] = df['hour'].isin([18, 19, 20, 21, 22]).astype(int)
    
    # Night (minimum load)
    df['is_night'] = df['hour'].isin([0, 1, 2, 3, 4, 5]).astype(int)
    
    # Cooking times
    df['is_cooking_time'] = df['hour'].isin([7, 8, 12, 13, 18, 19]).astype(int)
    
    return df
```

## Feature Selection

### Importance-Based Selection

```python
from sklearn.feature_selection import SelectFromModel
from lightgbm import LGBMRegressor

def select_important_features(X_train, y_train, threshold='median'):
    """Select features based on importance."""
    model = LGBMRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    selector = SelectFromModel(model, threshold=threshold, prefit=True)
    selected_features = X_train.columns[selector.get_support()]
    
    return selected_features
```

### Correlation-Based Pruning

```python
def remove_highly_correlated_features(df, threshold=0.95):
    """Remove features that are highly correlated with each other."""
    corr_matrix = df.corr().abs()
    
    # Select upper triangle
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )
    
    # Find features with correlation above threshold
    to_drop = [column for column in upper.columns 
               if any(upper[column] > threshold)]
    
    return df.drop(columns=to_drop)
```

## Complete Feature Pipeline

```python
class FeatureEngineer:
    """Complete feature engineering pipeline for electricity forecasting."""
    
    def __init__(self, lags=None, holiday_country='CN'):
        self.lags = lags or [1, 24, 48, 168, 336]
        self.holiday_country = holiday_country
        self.feature_columns = None
    
    def fit_transform(self, df, weather_df=None):
        """Fit and transform training data."""
        df = df.copy()
        
        # Temporal features
        df = self._add_temporal_features(df)
        
        # Lag features
        df = self._add_lag_features(df)
        
        # Rolling features
        df = self._add_rolling_features(df)
        
        # Weather features
        if weather_df is not None:
            df = self._add_weather_features(df, weather_df)
        
        # Holiday features
        df = self._add_holiday_features(df)
        
        # Interaction features
        df = self._add_interaction_features(df)
        
        # Store feature columns (exclude target and timestamp)
        self.feature_columns = [c for c in df.columns 
                                if c not in ['load', 'timestamp']]
        
        return df
    
    def transform(self, df, weather_df=None):
        """Transform new data using fitted pipeline."""
        # Same transformations as fit_transform
        # Ensure same feature columns in same order
        df = self._apply_all_features(df, weather_df)
        return df[self.feature_columns]
```

## Feature Importance Analysis

After training, analyze which features matter most:

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_feature_importance(model, feature_names, top_n=20):
    """Visualize feature importance."""
    importance = pd.DataFrame({
        'feature': feature_names,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 8))
    sns.barplot(data=importance.head(top_n), x='importance', y='feature')
    plt.title('Top Feature Importances')
    plt.tight_layout()
    plt.show()
    
    return importance
```

## Common Mistakes

1. **Data leakage**: Using future information (e.g., rolling stats that include current timestep)
   - Fix: Always shift rolling features by 1

2. **Inconsistent preprocessing**: Training and inference use different feature calculations
   - Fix: Use sklearn Pipeline or custom FeatureEngineer class

3. **Too many features**: Model overfits, becomes slow
   - Fix: Use feature selection, keep top 50-100 features

4. **Ignoring domain knowledge**: Generic features miss electricity-specific patterns
   - Fix: Add temperature interactions, holiday effects, load-type specific features

5. **Not handling missing data**: Weather data gaps cause forecast failures
   - Fix: Impute missing weather with historical averages or nearby stations
