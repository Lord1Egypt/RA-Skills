# Known Use Cases (KUC)

Total: **31**

## `KUC-101`
**Source**: `docs/fix_package_titles.py`

Automates extraction of descriptive titles and docstrings from Python packages to improve Sphinx API documentation readability.

## `KUC-102`
**Source**: `docs/source/conf.py`

Configures Sphinx documentation builder with extensions for auto-summary, autodoc, and graphviz visualization.

## `KUC-103`
**Source**: `examples/00-quickstart.ipynb`

Introduces new users to the Darts time series library with basic operations like series creation, loading datasets, and simple transformations.

## `KUC-104`
**Source**: `examples/01-multi-time-series-and-covariates.ipynb`

Demonstrates forecasting multiple related time series simultaneously using covariates and multivariate models like VARIMA and NBEATS.

## `KUC-105`
**Source**: `examples/02-data-processing.ipynb`

Shows how to build reusable data processing pipelines with transformers for scaling, filling missing values, and other transformations.

## `KUC-106`
**Source**: `examples/03-FFT-examples.ipynb`

Uses Fast Fourier Transform for frequency-based time series forecasting, ideal for seasonal patterns.

## `KUC-107`
**Source**: `examples/04-RNN-examples.ipynb`

Demonstrates recurrent neural network models (RNN, LSTM, GRU) for time series forecasting with seasonality detection.

## `KUC-108`
**Source**: `examples/05-TCN-examples.ipynb`

Uses Temporal Convolutional Networks for high-performance time series forecasting with dilated convolutions.

## `KUC-109`
**Source**: `examples/06-Transformer-examples.ipynb`

Applies Transformer architecture with self-attention mechanisms for capturing long-range dependencies in time series.

## `KUC-110`
**Source**: `examples/07-NBEATS-examples.ipynb`

Uses NBEATS (Neural Basis Expansion Analysis) for interpretable deep learning time series forecasting.

## `KUC-111`
**Source**: `examples/08-DeepAR-examples.ipynb`

Implements DeepAR for probabilistic forecasting with uncertainty quantification using Gaussian likelihood.

## `KUC-112`
**Source**: `examples/09-DeepTCN-examples.ipynb`

Combines Deep TCN architecture with probabilistic prediction using quantile regression and Gaussian likelihood.

## `KUC-113`
**Source**: `examples/10-Kalman-filter-examples.ipynb`

Applies Kalman filtering for state estimation and noise reduction in time series with known state-space models.

## `KUC-114`
**Source**: `examples/11-GP-filter-examples.ipynb`

Uses Gaussian Process regression for flexible non-parametric filtering and noise reduction in time series.

## `KUC-115`
**Source**: `examples/12-Dynamic-Time-Warping-example.ipynb`

Computes similarity between time series using Dynamic Time Warping algorithm for pattern matching and comparison.

## `KUC-116`
**Source**: `examples/13-TFT-examples.ipynb`

Uses TFT for interpretable multi-horizon forecasting with attention visualization and quantile predictions.

## `KUC-117`
**Source**: `examples/14-transfer-learning.ipynb`

Demonstrates transferring knowledge from pre-trained models across different time series datasets (M3, M4 competitions).

## `KUC-118`
**Source**: `examples/15-static-covariates.ipynb`

Shows how to incorporate static (time-invariant) covariates into time series models for multivariate forecasting.

## `KUC-119`
**Source**: `examples/16-hierarchical-reconciliation.ipynb`

Demonstrates hierarchical forecasting with MinT reconciliation to ensure consistency across aggregation levels.

## `KUC-120`
**Source**: `examples/17-hyperparameter-optimization.ipynb`

Uses Optuna for automated hyperparameter tuning of forecasting models with early stopping and visualization.

## `KUC-121`
**Source**: `examples/18-TiDE-examples.ipynb`

Implements TiDE (Time-series Dense Encoder) for efficient long-sequence time series forecasting.

## `KUC-122`
**Source**: `examples/19-EnsembleModel-examples.ipynb`

Combines multiple forecasting models using ensemble techniques like naive ensembling and regression ensembling.

## `KUC-123`
**Source**: `examples/20-SKLearnModel-examples.ipynb`

Uses scikit-learn compatible models (Linear Regression, Random Forest, XGBoost, LightGBM) with SHAP explainability.

## `KUC-124`
**Source**: `examples/21-TSMixer-examples.ipynb`

Uses TSMixer for multi-variate time series forecasting with feature mixing and quantile regression.

## `KUC-125`
**Source**: `examples/22-anomaly-detection-examples.ipynb`

Detects anomalies in time series using scoring methods like KMeans, Wasserstein distance, and forecasting-based models.

## `KUC-126`
**Source**: `examples/23-Conformal-Prediction-examples.ipynb`

Provides distribution-free uncertainty quantification using conformal prediction with calibration sets.

## `KUC-127`
**Source**: `examples/24-SKLearnClassifierModel-examples.ipynb`

Classifies time series segments into categories using gradient-based features and CatBoost classifier.

## `KUC-128`
**Source**: `examples/25-Chronos-2-examples.ipynb`

Uses Chronos-2, a pre-trained time series foundation model, for zero-shot and fine-tuned forecasting.

## `KUC-129`
**Source**: `examples/26-NeuralForecast-examples.ipynb`

Integrates NeuralForecast models (from Nixtla) with Darts for advanced neural network time series forecasting.

## `KUC-130`
**Source**: `examples/27-Torch-and-Foundation-Model-Fine-Tuning-examples.ipynb`

Fine-tunes pre-trained foundation models like Chronos-2 and TiDE on custom time series data.

## `KUC-131`
**Source**: `examples/utils/utils.py`

Provides utility functions for managing Python paths when running Darts examples locally.
