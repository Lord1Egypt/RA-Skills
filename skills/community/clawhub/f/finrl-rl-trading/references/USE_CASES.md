# Known Use Cases (KUC)

Total: **14**

## `KUC-101`
**Source**: `examples/FinRL_Ensemble_StockTrading_ICAIF_2020.ipynb`

Executing automated stock trading using an ensemble of multiple DRL agents (A2C, DDPG, PPO, TD3, SAC) to reduce individual agent weakness and improve risk-adjusted returns.

## `KUC-102`
**Source**: `examples/FinRL_GPM_Demo.ipynb`

Optimizing stock portfolios using Graph Neural Networks (GPM architecture) that capture temporal and relational relationships between stocks in the NASDAQ market.

## `KUC-103`
**Source**: `examples/FinRL_PaperTrading_Demo.ipynb`

Executing simulated real-time stock trading with Alpaca paper trading API using a custom PPO neural network architecture to test strategies without financial risk.

## `KUC-104`
**Source**: `examples/FinRL_PaperTrading_Demo_refactored.py`

Production-ready paper trading script using Alpaca API with command-line argument parsing for automated DOW 30 stock trading.

## `KUC-105`
**Source**: `examples/FinRL_PortfolioOptimizationEnv_Demo.ipynb`

Optimizing cryptocurrency or stock portfolios using EIIE (Environment-Informed Investment Encoder) architecture for Brazilian market stocks.

## `KUC-106`
**Source**: `examples/FinRL_StockTrading_2026_1_data.py`

Fetching and processing stock market data from Yahoo Finance with technical indicators for automated stock trading model development.

## `KUC-107`
**Source**: `examples/FinRL_StockTrading_2026_2_train.py`

Training deep reinforcement learning agents (A2C, DDPG, PPO, SAC, TD3) for automated stock trading using the StockTradingEnv environment.

## `KUC-108`
**Source**: `examples/FinRL_StockTrading_2026_3_Backtest.py`

Backtesting multiple trained DRL agents against baseline strategies (MVO, DJIA) to evaluate and compare ensemble trading performance.

## `KUC-109`
**Source**: `finrl/applications/Stock_NeurIPS2018/Stock_NeurIPS2018_1_Data.ipynb`

Fetching DOW 30 stock data with VIX fear index and turbulence indicators for robust market condition modeling in stock trading.

## `KUC-110`
**Source**: `finrl/applications/Stock_NeurIPS2018/Stock_NeurIPS2018_2_Train.ipynb`

Training A2C reinforcement learning agent for automated stock trading with technical indicators and trading cost considerations.

## `KUC-111`
**Source**: `finrl/applications/Stock_NeurIPS2018/Stock_NeurIPS2018_3_Backtest.ipynb`

Evaluating and comparing multiple DRL trading agents (A2C, DDPG, PPO, SAC, TD3) through backtesting against market baselines.

## `KUC-112`
**Source**: `finrl/applications/imitation_learning/Imitation_Sandbox.ipynb`

Experimental sandbox for testing imitation learning algorithms (TD3+BC) combined with market factor models for stock portfolio management.

## `KUC-113`
**Source**: `finrl/applications/imitation_learning/Stock_Selection.ipynb`

Using imitation learning techniques to learn stock selection strategies from expert behavior combined with technical indicators.

## `KUC-114`
**Source**: `finrl/applications/imitation_learning/Weight_Initialization.ipynb`

Investigating weight initialization strategies for imitation learning models to improve stock portfolio management performance.
