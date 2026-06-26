# Known Use Cases (KUC)

Total: **20**

## `KUC-101`
**Source**: `docs/source/Buy_and_hold.ipynb`

Implements a passive buy-and-hold strategy with monthly rebalancing to fixed target weights, demonstrating core backtesting framework capabilities.

## `KUC-102`
**Source**: `docs/source/ERC.ipynb`

Demonstrates Equal Risk Contribution (ERC) portfolio weighting using multivariate normal returns and covariance matrix inputs for risk parity allocation.

## `KUC-103`
**Source**: `docs/source/Fixed_Income.ipynb`

Simulates rolling government bond trading with synthetic price-to-yield calculations and bond lifecycle management for fixed income backtesting.

## `KUC-104`
**Source**: `docs/source/PTE.ipynb`

Implements inverse volatility weighting to allocate more capital to lower-volatility assets, with 3-month lookback and 1-day lag for rebalancing.

## `KUC-105`
**Source**: `docs/source/Strategy_Combination.ipynb`

Combines multiple trading strategies into a single portfolio to test strategy allocation and diversification across different algorithmic approaches.

## `KUC-106`
**Source**: `docs/source/Target_Volatility.ipynb`

Controls portfolio-level volatility to a target annualized level (10%) using weekly rebalancing with inverse volatility asset weights.

## `KUC-107`
**Source**: `docs/source/Trend_1.ipynb`

Implements trend following using a rolling 12-month median as a moving average signal for asset selection and timing decisions.

## `KUC-108`
**Source**: `docs/source/Trend_2.ipynb`

Demonstrates custom algorithm creation by implementing a Signal algo that calculates total returns over a lookback period for monthly rebalancing decisions.

## `KUC-109`
**Source**: `docs/source/examples-nb.ipynb`

Demonstrates the SelectWhere algorithm for selecting securities based on custom signal DataFrames, using 50-day rolling mean as a sample indicator.

## `KUC-110`
**Source**: `docs/source/intro.ipynb`

Educational example comparing monthly equal-weight vs weekly inverse-volatility strategies using real market data (AAPL, MSFT, SPY, AGG).

## `KUC-111`
**Source**: `examples/pairs_trading.py`

Implements statistical arbitrage pairs trading by identifying cointegrated pairs whose indicator exceeds threshold for long/short positioning.

## `KUC-112`
**Source**: `examples/buy_and_hold.py`

Executable Python version of buy-and-hold strategy with monthly rebalancing, demonstrating standalone script execution for portfolio backtesting.

## `KUC-113`
**Source**: `examples/fixed_income.ipynb`

Creates synthetic government bond data with rolling maturity schedules, price-to-yield calculations, and bond lifecycle management for fixed income backtesting.

## `KUC-114`
**Source**: `examples/ERC.ipynb`

Equal Risk Contribution portfolio using multivariate normal returns and explicit covariance matrix for risk parity weighting across assets.

## `KUC-115`
**Source**: `examples/PTE.ipynb`

Inverse volatility weighting strategy using 3-month historical data and 1-day lag to reduce risk concentration in high-volatility assets.

## `KUC-116`
**Source**: `examples/Strategy_Combination.ipynb`

Combines multiple strategies into a unified portfolio allocation framework for testing strategy diversification and correlation effects.

## `KUC-117`
**Source**: `examples/Target_Volatility.ipynb`

Controls portfolio volatility to 10% annualized target using weekly rebalancing and inverse volatility asset weighting with 12-month lookback.

## `KUC-118`
**Source**: `examples/buy_and_hold.ipynb`

Basic buy-and-hold strategy with monthly rebalancing to fixed weights (60/40), demonstrating core framework rebalancing mechanics.

## `KUC-119`
**Source**: `examples/trend_1.ipynb`

Trend following strategy using 12-month rolling median as a baseline indicator, visualizing price vs moving average crossover signals.

## `KUC-120`
**Source**: `examples/trend_2.ipynb`

Custom Signal algorithm that calculates total returns over configurable lookback periods for monthly rebalancing decisions.
