# Known Use Cases (KUC)

Total: **9**

## `KUC-101`
**Source**: `Paper Trading/Automated_Paper_Trading.ipynb`

Execute simulated paper trades in real-time using a trained PPO reinforcement learning agent connected to Alpaca brokerage API, enabling risk-free strategy validation before live deployment.

## `KUC-102`
**Source**: `examples/Aarons_portfolio_optimization_example.ipynb`

Optimize portfolio allocation across multiple assets using Markowitz mean-variance optimization to maximize risk-adjusted returns, balancing expected return against portfolio volatility.

## `KUC-103`
**Source**: `examples/FinRL_Ensemble_StockTrading_ICAIF_2020.ipynb`

Train and evaluate an ensemble of deep reinforcement learning agents for stock trading, combining multiple model predictions to improve robustness and performance across varying market conditions.

## `KUC-104`
**Source**: `examples/FinRL_PaperTrading_Demo.ipynb`

Demonstrate live paper trading execution using a PPO neural network agent connected to Alpaca's paper trading API, enabling real-time trade simulation with market data feeds.

## `KUC-105`
**Source**: `examples/FinRL_PortfolioOptimizationEnv_Demo.ipynb`

Train deep reinforcement learning agents for portfolio allocation across Brazilian stocks (B3 exchange), using custom portfolio environment with deep neural network policies to optimize multi-asset holdings.

## `KUC-106`
**Source**: `examples/Stock_NeurIPS2018_SB3.ipynb`

Implement stock trading strategies using StableBaselines3 library's DRL implementations (A2C, PPO, SAC) with feature engineering on technical indicators for training and evaluation on historical market data.

## `KUC-107`
**Source**: `examples/run_markowitz_portfolio_optimization.py`

Execute Markowitz mean-variance portfolio optimization algorithm as a standalone Python script, computing optimal asset weights based on historical returns covariance and expected returns to minimize portfolio variance.

## `KUC-108`
**Source**: `examples/run_rl_portfolio_optimization.py`

Train and run reinforcement learning agent (A2C) for portfolio optimization using StockPortfolioEnv, enabling adaptive portfolio allocation that learns from market interactions rather than static optimization.

## `KUC-109`
**Source**: `meta/env_execution_optimizing/order_execution_qlib/workflow_by_code.ipynb`

Optimize order execution using Qlib's LightGBM model to predict stock movements and implement TopkDropoutStrategy, improving trade execution quality by timing orders based on predicted signals.
