# Known Use Cases (KUC)

Total: **9**

## `KUC-101`
**Source**: `scripts/bmg_analyze.py`

Identifies how many stocks from an index fall into each sector and screens for stocks with statistically significant factor regression results based on p-values.

## `KUC-102`
**Source**: `scripts/correlate.py`

Computes correlations between different factors over time to understand factor relationship dynamics and potential multicollinearity issues.

## `KUC-103`
**Source**: `scripts/regression_function.py`

Performs ordinary least squares regression on factor data with comprehensive diagnostic tests including Durbin-Watson, Jarque-Bera, and Breusch-Pagan tests.

## `KUC-104`
**Source**: `scripts/bulk_script.py`

Builds custom Fama-French style factor models by merging stock returns, Fama-French factors, and carbon risk factors into unified datasets for analysis.

## `KUC-105`
**Source**: `scripts/stock_price_function.py`

Downloads historical stock price data from Yahoo Finance with support for daily and monthly frequencies, including automatic retry on timeout.

## `KUC-106`
**Source**: `scripts/bmg_series.py`

Creates Brown-Green (BMG) factor series by calculating the return differential between brown (high carbon) and green (low carbon) stocks for carbon risk analysis.

## `KUC-107`
**Source**: `scripts/get_regressions.py`

Executes factor regression analysis across multiple stocks in parallel using multiprocessing, loading Fama-French and carbon risk factors from database.

## `KUC-108`
**Source**: `scripts/get_stocks.py`

Imports stock return data from CSV or downloads from yfinance, with support for incremental updates to maintain current database with stock returns.

## `KUC-109`
**Source**: `scripts/setup_db.py`

Initializes database schema and imports Fama-French, bond, and carbon risk factors into PostgreSQL tables, including BMG factor data.
