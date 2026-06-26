# Data Scientist — Code Examples

## Example 1

```python
import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import ttest_ind, chi2_contingency, mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

class StatisticalAnalyzer:
    def __init__(self, data):
        self.data = data
        self.results = {}
    
    def descriptive_statistics(self, columns=None):
        """Generate comprehensive descriptive statistics"""
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns
        
        stats_summary = {}
        for col in columns:
            stats_summary[col] = {
                'count': self.data[col].count(),
                'mean': self.data[col].mean(),
                'median': self.data[col].median(),
                'std': self.data[col].std(),
                'min': self.data[col].min(),
                'max': self.data[col].max(),
                'q25': self.data[col].quantile(0.25),
                'q75': self.data[col].quantile(0.75),
                'skewness': stats.skew(self.data[col].dropna()),
                'kurtosis': stats.kurtosis(self.data[col].dropna())
            }
        
        return pd.DataFrame(stats_summary).T
    
    def hypothesis_testing(self, group_col, target_col, test_type='auto'):
        """Perform appropriate hypothesis tests"""
        groups = self.data[group_col].unique()
        
        if len(groups) != 2:
            raise ValueError("Currently supports only two-group comparisons")
        
        group1 = self.data[self.data[group_col] == groups[0]][target_col].dropna()
        group2 = self.data[self.data[group_col] == groups[1]][target_col].dropna()
        
        # Normality tests
        _, p_norm1 = stats.shapiro(group1.sample(min(5000, len(group1))))
        _, p_norm2 = stats.shapiro(group2.sample(min(5000, len(group2))))
        
        # Equal variance test
        _, p_var = stats.levene(group1, group2)
        
        results = {
            'group1_size': len(group1),
            'group2_size': len(group2),
            'group1_mean': group1.mean(),
            'group2_mean': group2.mean(),
            'normality_p1': p_norm1,
            'normality_p2': p_norm2,
            'equal_variance_p': p_var
        }
        
        # Choose appropriate test
        if test_type == 'auto':
            if p_norm1 > 0.05 and p_norm2 > 0.05:
                # Both normal, use t-test
                if p_var > 0.05:
                    # Equal variances
                    stat, p_value = ttest_ind(group1, group2)
                    test_used = "Independent t-test (equal variances)"
                else:
                    # Unequal variances
                    stat, p_value = ttest_ind(group1, group2, equal_var=False)
                    test_used = "Welch's t-test (unequal variances)"
            else:
                # Non-normal, use Mann-Whitney U
                stat, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
                test_used = "Mann-Whitney U test"
        
        results.update({
            'test_used': test_used,
            'test_statistic': stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'effect_size': self._calculate_effect_size(group1, group2)
        })
        
        return results
    
    def _calculate_effect_size(self, group1, group2):
        """Calculate Cohen's d for effect size"""
        pooled_std = np.sqrt(((len(group1) - 1) * group1.var() + 
                             (len(group2) - 1) * group2.var()) / 
                            (len(group1) + len(group2) - 2))
        return (group1.mean() - group2.mean()) / pooled_std
```

## Example 2

```python
from sklearn.model_selection import cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, precision_recall_curve
import xgboost as xgb
import lightgbm as lgb

class MLPipeline:
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.models = {}
        self.best_model = None
        self.feature_importance = None
    
    def feature_engineering(self, X, y=None, numeric_features=None, categorical_features=None):
        """Advanced feature engineering"""
        X_engineered = X.copy()
        
        # Numeric feature engineering
        if numeric_features:
            for col in numeric_features:
                # Log transformation for skewed features
                if X[col].skew() > 1:
                    X_engineered[f'{col}_log'] = np.log1p(X[col])
                
                # Polynomial features for important variables
                X_engineered[f'{col}_squared'] = X[col] ** 2
                X_engineered[f'{col}_sqrt'] = np.sqrt(X[col])
                
                # Binning for non-linear relationships
                X_engineered[f'{col}_binned'] = pd.cut(X[col], bins=5, labels=False)
        
        # Categorical feature engineering
        if categorical_features:
            for col in categorical_features:
                # Target encoding (if y is provided)
                if y is not None:
                    target_mean = y.groupby(X[col]).mean()
                    X_engineered[f'{col}_target_encoded'] = X[col].map(target_mean)
                
                # Frequency encoding
                freq_map = X[col].value_counts(normalize=True)
                X_engineered[f'{col}_frequency'] = X[col].map(freq_map)
        
        # Interaction features
        if len(numeric_features) >= 2:
            for i, col1 in enumerate(numeric_features):
                for col2 in numeric_features[i+1:]:
                    X_engineered[f'{col1}_{col2}_interaction'] = X[col1] * X[col2]
                    X_engineered[f'{col1}_{col2}_ratio'] = X[col1] / (X[col2] + 1e-8)
        
        return X_engineered
    
    def model_comparison(self, X_train, X_test, y_train, y_test):
        """Compare multiple ML algorithms"""
        models = {
            'Logistic Regression': LogisticRegression(random_state=self.random_state),
            'Random Forest': RandomForestClassifier(random_state=self.random_state),
            'Gradient Boosting': GradientBoostingClassifier(random_state=self.random_state),
            'XGBoost': xgb.XGBClassifier(random_state=self.random_state),
            'LightGBM': lgb.LGBMClassifier(random_state=self.random_state)
        }
        
        results = {}
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        
        for name, model in models.items():
            # Cross-validation
            cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='roc_auc')
            
            # Fit and predict
            model.fit(X_train, y_train)
            y_pred = model.predict_proba(X_test)[:, 1]
            test_auc = roc_auc_score(y_test, y_pred)
            
            results[name] = {
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std(),
                'test_auc': test_auc,
                'model': model
            }
            
            self.models[name] = model
        
        # Select best model
        best_model_name = max(results.keys(), key=lambda x: results[x]['test_auc'])
        self.best_model = self.models[best_model_name]
        
        return results
    
    def hyperparameter_tuning(self, X_train, y_train, model_type='xgboost'):
        """Advanced hyperparameter tuning"""
        if model_type == 'xgboost':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 4, 5, 6],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0],
                'colsample_bytree': [0.8, 0.9, 1.0]
            }
            model = xgb.XGBClassifier(random_state=self.random_state)
        
        elif model_type == 'lightgbm':
            param_grid = {
                'n_estimators': [100, 200, 300],
                'max_depth': [3, 4, 5, 6],
                'learning_rate': [0.01, 0.1, 0.2],
                'feature_fraction': [0.8, 0.9, 1.0],
                'bagging_fraction': [0.8, 0.9, 1.0]
            }
            model = lgb.LGBMClassifier(random_state=self.random_state)
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        grid_search = GridSearchCV(
            model, param_grid, cv=cv, scoring='roc_auc', 
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        self.best_model = grid_search.best_estimator_
        
        return grid_search.best_params_, grid_search.best_score_
```

## Example 3

```python
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class TimeSeriesAnalyzer:
    def __init__(self, data, date_col, value_col):
        self.data = data.copy()
        self.data[date_col] = pd.to_datetime(self.data[date_col])
        self.data = self.data.set_index(date_col).sort_index()
        self.ts = self.data[value_col]
        self.forecast = None
    
    def exploratory_analysis(self):
        """Comprehensive time series EDA"""
        results = {}
        
        # Basic statistics
        results['basic_stats'] = {
            'start_date': self.ts.index.min(),
            'end_date': self.ts.index.max(),
            'total_observations': len(self.ts),
            'missing_values': self.ts.isnull().sum(),
            'mean': self.ts.mean(),
            'std': self.ts.std(),
            'trend': 'increasing' if self.ts.iloc[-1] > self.ts.iloc[0] else 'decreasing'
        }
        
        # Stationarity test
        adf_result = adfuller(self.ts.dropna())
        results['stationarity'] = {
            'adf_statistic': adf_result[0],
            'p_value': adf_result[1],
            'is_stationary': adf_result[1] < 0.05,
            'critical_values': adf_result[4]
        }
        
        # Seasonal decomposition
        if len(self.ts) >= 24:  # Need at least 2 seasons
            decomposition = seasonal_decompose(self.ts.dropna(), period=12)
            results['seasonality'] = {
                'seasonal_strength': np.var(decomposition.seasonal) / np.var(self.ts.dropna()),
                'trend_strength': np.var(decomposition.trend.dropna()) / np.var(self.ts.dropna())
            }
        
        return results
    
    def arima_modeling(self, max_p=5, max_d=2, max_q=5):
        """Automatic ARIMA model selection"""
        best_aic = np.inf
        best_params = None
        best_model = None
        
        for p in range(max_p + 1):
            for d in range(max_d + 1):
                for q in range(max_q + 1):
                    try:
                        model = ARIMA(self.ts.dropna(), order=(p, d, q))
                        fitted_model = model.fit()
                        
                        if fitted_model.aic < best_aic:
                            best_aic = fitted_model.aic
                            best_params = (p, d, q)
                            best_model = fitted_model
                    except:
                        continue
        
        return best_model, best_params, best_aic
    
    def forecast_evaluation(self, model, test_size=0.2):
        """Evaluate forecasting performance"""
        split_point = int(len(self.ts) * (1 - test_size))
        train_data = self.ts[:split_point]
        test_data = self.ts[split_point:]
        
        # Fit model on training data
        model_fit = ARIMA(train_data, order=model.order).fit()
        
        # Generate forecasts
        forecast = model_fit.forecast(steps=len(test_data))
        
        # Calculate metrics
        mae = mean_absolute_error(test_data, forecast)
        mse = mean_squared_error(test_data, forecast)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((test_data - forecast) / test_data)) * 100
        
        return {
            'MAE': mae,
            'MSE': mse,
            'RMSE': rmse,
            'MAPE': mape,
            'forecast': forecast,
            'actual': test_data
        }
```

## Example 4

```python
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.power import ttest_power
from statsmodels.stats.proportion import proportions_ztest

class ABTestAnalyzer:
    def __init__(self):
        self.results = {}
    
    def sample_size_calculation(self, baseline_rate, minimum_effect, alpha=0.05, power=0.8):
        """Calculate required sample size for A/B test"""
        effect_size = minimum_effect / np.sqrt(baseline_rate * (1 - baseline_rate))
        
        n_per_group = ttest_power(effect_size, power, alpha) / 4
        total_sample_size = n_per_group * 2
        
        return {
            'samples_per_group': int(np.ceil(n_per_group)),
            'total_sample_size': int(np.ceil(total_sample_size)),
            'effect_size': effect_size,
            'assumptions': {
                'baseline_rate': baseline_rate,
                'minimum_effect': minimum_effect,
                'alpha': alpha,
                'power': power
            }
        }
    
    def analyze_ab_test(self, control_data, treatment_data, metric_type='conversion'):
        """Comprehensive A/B test analysis"""
        results = {}
        
        if metric_type == 'conversion':
            # Conversion rate analysis
            control_conversions = control_data.sum()
            control_visitors = len(control_data)
            treatment_conversions = treatment_data.sum()
            treatment_visitors = len(treatment_data)
            
            control_rate = control_conversions / control_visitors
            treatment_rate = treatment_conversions / treatment_visitors
            
            # Statistical test
            counts = np.array([treatment_conversions, control_conversions])
            nobs = np.array([treatment_visitors, control_visitors])
            
            z_stat, p_value = proportions_ztest(counts, nobs)
            
            # Confidence interval for difference
            se_diff = np.sqrt(
                (control_rate * (1 - control_rate) / control_visitors) +
                (treatment_rate * (1 - treatment_rate) / treatment_visitors)
            )
            
            diff = treatment_rate - control_rate
            ci_lower = diff - 1.96 * se_diff
            ci_upper = diff + 1.96 * se_diff
            
            results = {
                'control_rate': control_rate,
                'treatment_rate': treatment_rate,
                'absolute_lift': diff,
                'relative_lift': diff / control_rate,
                'z_statistic': z_stat,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'confidence_interval': (ci_lower, ci_upper),
                'sample_sizes': {'control': control_visitors, 'treatment': treatment_visitors}
            }
        
        elif metric_type == 'continuous':
            # Continuous metric analysis
            control_mean = control_data.mean()
            treatment_mean = treatment_data.mean()
            
            # T-test
            t_stat, p_value = stats.ttest_ind(treatment_data, control_data)
            
            # Effect size (Cohen's d)
            pooled_std = np.sqrt(((len(control_data) - 1) * control_data.var() + 
                                 (len(treatment_data) - 1) * treatment_data.var()) / 
                                (len(control_data) + len(treatment_data) - 2))
            
            cohens_d = (treatment_mean - control_mean) / pooled_std
            
            # Confidence interval
            se_diff = pooled_std * np.sqrt(1/len(control_data) + 1/len(treatment_data))
            diff = treatment_mean - control_mean
            ci_lower = diff - 1.96 * se_diff
            ci_upper = diff + 1.96 * se_diff
            
            results = {
                'control_mean': control_mean,
                'treatment_mean': treatment_mean,
                'absolute_difference': diff,
                'relative_difference': diff / control_mean,
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'cohens_d': cohens_d,
                'confidence_interval': (ci_lower, ci_upper),
                'sample_sizes': {'control': len(control_data), 'treatment': len(treatment_data)}
            }
        
        return results
    
    def sequential_testing(self, control_conversions, control_visitors, 
                          treatment_conversions, treatment_visitors, alpha=0.05):
        """Sequential analysis for early stopping"""
        # Calculate current rates
        control_rate = control_conversions / control_visitors
        treatment_rate = treatment_conversions / treatment_visitors
        
        # Z-test for current data
        counts = np.array([treatment_conversions, control_conversions])
        nobs = np.array([treatment_visitors, control_visitors])
        
        z_stat, p_value = proportions_ztest(counts, nobs)
        
        # Adjusted alpha for sequential testing (Bonferroni correction)
        adjusted_alpha = alpha / np.log(max(control_visitors, treatment_visitors))
        
        return {
            'current_p_value': p_value,
            'adjusted_alpha': adjusted_alpha,
            'can_stop': p_value < adjusted_alpha,
            'recommendation': 'Stop test' if p_value < adjusted_alpha else 'Continue test',
            'control_rate': control_rate,
            'treatment_rate': treatment_rate,
            'sample_sizes': {'control': control_visitors, 'treatment': treatment_visitors}
        }
```

## Example 5

```python
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class DataVisualization:
    def __init__(self, style='seaborn'):
        plt.style.use(style)
        self.colors = sns.color_palette("husl", 8)
    
    def correlation_analysis(self, data, method='pearson'):
        """Advanced correlation analysis with visualization"""
        # Calculate correlations
        corr_matrix = data.corr(method=method)
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, ax=axes[0,0])
        axes[0,0].set_title('Correlation Heatmap')
        
        # Clustermap for hierarchical clustering
        g = sns.clustermap(corr_matrix, cmap='coolwarm', center=0, 
                          square=True, figsize=(8, 6))
        plt.setp(g.ax_heatmap.get_xticklabels(), rotation=45)
        plt.setp(g.ax_heatmap.get_yticklabels(), rotation=0)
        
        # Network graph of strong correlations
        strong_corr = corr_matrix.abs() > 0.7
        edges = []
        for i in range(len(strong_corr.columns)):
            for j in range(i+1, len(strong_corr.columns)):
                if strong_corr.iloc[i, j]:
                    edges.append((strong_corr.columns[i], strong_corr.columns[j], 
                                corr_matrix.iloc[i, j]))
        
        return corr_matrix, edges
    
    def distribution_analysis(self, data, column):
        """Comprehensive distribution analysis"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        
        # Histogram with KDE
        sns.histplot(data[column], kde=True, ax=axes[0,0])
        axes[0,0].set_title(f'Distribution of {column}')
        
        # Box plot
        sns.boxplot(y=data[column], ax=axes[0,1])
        axes[0,1].set_title(f'Box Plot of {column}')
        
        # Q-Q plot
        stats.probplot(data[column].dropna(), dist="norm", plot=axes[0,2])
        axes[0,2].set_title(f'Q-Q Plot of {column}')
        
        # Violin plot
        sns.violinplot(y=data[column], ax=axes[1,0])
        axes[1,0].set_title(f'Violin Plot of {column}')
        
        # ECDF
        x = np.sort(data[column].dropna())
        y = np.arange(1, len(x) + 1) / len(x)
        axes[1,1].plot(x, y, marker='.', linestyle='none')
        axes[1,1].set_xlabel(column)
        axes[1,1].set_ylabel('ECDF')
        axes[1,1].set_title(f'ECDF of {column}')
        
        # Summary statistics
        stats_text = f"""
        Mean: {data[column].mean():.2f}
        Median: {data[column].median():.2f}
        Std: {data[column].std():.2f}
        Skewness: {data[column].skew():.2f}
        Kurtosis: {data[column].kurtosis():.2f}
        """
        axes[1,2].text(0.1, 0.5, stats_text, fontsize=12, 
                      verticalalignment='center')
        axes[1,2].axis('off')
        
        plt.tight_layout()
        return fig
    
    def interactive_dashboard(self, data, target_col):
        """Create interactive Plotly dashboard"""
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Feature Importance', 'Prediction Distribution', 
                          'Residual Analysis', 'Feature Correlation'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Feature importance (assuming we have a model)
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        correlations = data[numeric_cols].corrwith(data[target_col]).abs().sort_values(ascending=False)
        
        fig.add_trace(
            go.Bar(x=correlations.values[:10], y=correlations.index[:10], 
                  orientation='h', name='Correlation with Target'),
            row=1, col=1
        )
        
        # Target distribution
        fig.add_trace(
            go.Histogram(x=data[target_col], name='Target Distribution'),
            row=1, col=2
        )
        
        # Scatter plot of top correlated feature vs target
        top_feature = correlations.index[1]  # Skip target itself
        fig.add_trace(
            go.Scatter(x=data[top_feature], y=data[target_col], 
                      mode='markers', name=f'{top_feature} vs {target_col}'),
            row=2, col=1
        )
        
        # Correlation heatmap
        corr_matrix = data[numeric_cols].corr()
        fig.add_trace(
            go.Heatmap(z=corr_matrix.values, 
                      x=corr_matrix.columns, 
                      y=corr_matrix.columns,
                      colorscale='RdBu', zmid=0),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False, 
                         title_text="Data Science Dashboard")
        return fig
```
