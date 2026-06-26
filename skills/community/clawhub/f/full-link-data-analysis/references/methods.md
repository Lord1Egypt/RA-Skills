# Analysis Methods Library

## I. Descriptive Analysis

### 1. Descriptive Statistics
- **Use**: Data overview, distribution characteristics, central tendency/dispersion
- **Applicable**: First step of any analysis, understanding the overall data landscape
- **Metrics**: Mean, median, standard deviation, quantiles, skewness, kurtosis
- **Python**: `df.describe()`, `df.skew()`, `df.kurt()`

### 2. Funnel Analysis
- **Use**: User behavior path conversion rates, churn node identification
- **Applicable**: Businesses with clear step-by-step processes (signup → activation → payment)
- **Key**: Absolute and relative conversion rates for each step
- **Python**: Calculate ratio of each step / initial step

### 3. Cohort Analysis
- **Use**: Group users by time/attributes, track behavioral changes over time
- **Applicable**: User retention, LTV analysis, product change effect evaluation
- **Key**: Cohort definition dimension + observation period
- **Python**: `df.pivot_table()` to construct retention matrix

### 4. RFM Analysis
- **Use**: Customer segmentation based on consumption behavior
- **Applicable**: User operations, precision marketing, customer lifecycle management
- **Three Dimensions**: Recency / Frequency / Monetary
- **Python**: Calculate R/F/M scores then bin or K-means cluster

## II. Relationship Inference

### 5. Correlation Analysis
- **Use**: Explore linear relationships between variables
- **Applicable**: Discover feature associations, feature engineering
- **Methods**: Pearson (continuous normal), Spearman (ordinal/non-normal), Kendall (small samples)
- **Python**: `df.corr()`, `scipy.stats.pearsonr/spearmanr`

### 6. Regression Analysis
- **Use**: Model causal relationships between variables, prediction, interpretation
- **Applicable**: Scenarios with clear independent/dependent variables
- **Methods**: Linear regression, Logistic regression, Multiple regression, Regularization (Lasso/Ridge)
- **Python**: `statsmodels.OLS/Logit`, `sklearn.linear_model`

### 7. Attribution Analysis
- **Use**: Quantify contribution of each factor to outcome metrics
- **Applicable**: Advertising channel effect attribution, revenue change factor decomposition
- **Methods**: Shapley value, Shap/eXAI, Incremental decomposition
- **Python**: Custom Shapley value, `shap` library (requires installation)

### 8. Causal Inference
- **Use**: Infer causal relationships from observational data
- **Applicable**: Effect evaluation when A/B testing is infeasible
- **Methods**:
  - DID (Difference-in-Differences) — Has pre/post comparison groups
  - IV (Instrumental Variables) — Has endogeneity issues
  - RDD (Regression Discontinuity Design) — Has clear threshold
  - PSM (Propensity Score Matching) — Has treatment/control groups
- **Python**: `statsmodels`, `linearmodels`, custom propensity matching

## III. Pattern Discovery

### 9. Clustering Analysis
- **Use**: Unsupervised grouping, discover naturally forming user/product clusters
- **Applicable**: User segmentation, market segmentation, anomaly detection
- **Methods**: K-means (spherical), DBSCAN (arbitrary shapes), Hierarchical clustering (small data)
- **Python**: `sklearn.cluster.KMeans/DBSCAN/AgglomerativeClustering`

### 10. Anomaly Detection
- **Use**: Identify outliers or anomalous patterns in data
- **Applicable**: Fraud detection, quality monitoring, system alerting
- **Methods**: IQR (simple), Z-score (normal), Isolation Forest (high-dimensional), LOF (density)
- **Python**: `sklearn.ensemble.IsolationForest`, `sklearn.neighbors.LocalOutlierFactor`

### 11. Factor Analysis
- **Use**: Dimensionality reduction, discover latent variable structure
- **Applicable**: Multi-index composite scoring, questionnaire analysis, variable reduction
- **Methods**: PCA (Principal Component Analysis), EFA (Exploratory Factor Analysis)
- **Python**: `sklearn.decomposition.PCA`, `factor_analyzer`

## IV. Time Series & Forecasting

### 12. Time Series Analysis
- **Use**: Analyze patterns, cycles, and trends in time series data
- **Applicable**: Any metric analysis with a time dimension
- **Methods**: Decomposition (trend+seasonal+residual), Stationarity test (ADF), Autocorrelation (ACF/PACF)
- **Python**: `statsmodels.tsa.seasonal_decompose`, `adfuller`

### 13. Forecasting Modeling
- **Use**: Predict future values based on historical data
- **Applicable**: Sales forecasting, traffic prediction, budget planning
- **Methods**: ARIMA/ARIMAX, Prophet (Meta), Exponential smoothing, Simple regression
- **Python**: `statsmodels.tsa.arima`, `prophet` (requires installation), `sklearn` regression

### 14. Hypothesis Testing
- **Use**: Verify whether hypotheses are statistically significant
- **Applicable**: A/B test result judgment, inter-group difference testing
- **Methods**:
  - t-test — Compare means of two groups
  - Chi-square test — Independence of categorical variables
  - ANOVA — Compare means of multiple groups
  - Mann-Whitney — Non-parametric alternative
- **Python**: `scipy.stats.ttest_ind/chisquare/f_oneway`

### 15. Text Analysis
- **Use**: Extract insights from unstructured text
- **Applicable**: Review analysis, customer service tickets, open-ended survey questions
- **Methods**: Word frequency statistics, sentiment analysis, keyword extraction, topic modeling
- **Python**: `collections.Counter`, `jieba` (Chinese word segmentation), `TextBlob`/`snownlp`

## Selection Guide

| I want to know... | Primary Method | Alternative |
|-------------------|----------------|-------------|
| What the data looks like | Descriptive Statistics (1) | — |
| Where is the most churn | Funnel Analysis (4) | Cohort (5) |
| Which users are most valuable | RFM (6) | Clustering (9) |
| Is A related to B | Correlation (7) | Regression (11) |
| What caused the change in X | Attribution (12) | Regression (11), Causal (13) |
| Is the strategy effective | Causal Inference (13) | Hypothesis Testing (8), Before/After |
| How many user types | Clustering (9) | RFM (6) |
| What will happen next month | Forecasting (3) | Time Series (2) |
| Where are the anomalies | Anomaly Detection (10) | Descriptive Statistics (1) |
| A/B test results | Hypothesis Testing (8) | Causal Inference (13) |
| How to reduce metrics | Factor Analysis (14) | Correlation (7) |
| What are users saying | Text Analysis (15) | — |