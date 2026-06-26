# Known Use Cases (KUC)

Total: **4**

## `KUC-101`
**Source**: `finmarketpy_examples/finmarketpy_notebooks/arcticdb_example.ipynb`

Provides persistent storage for high-frequency tick market data using ArcticDB, supporting both local LMDB and S3 cloud storage backends for efficient time series data management.

## `KUC-102`
**Source**: `finmarketpy_examples/finmarketpy_notebooks/backtest_example.ipynb`

Enables historical backtesting of FX trading strategies using G10 currency pairs with technical indicator-based signal generation to evaluate strategy performance.

## `KUC-103`
**Source**: `finmarketpy_examples/finmarketpy_notebooks/market_data_example.ipynb`

Fetches economic and financial market data from external vendors like Quandl, demonstrating how to request and cache market data with specific fields and date ranges.

## `KUC-104`
**Source**: `finmarketpy_examples/finmarketpy_notebooks/s3_bucket_example.ipynb`

Demonstrates writing and reading tick market data to/from AWS S3 cloud storage using Parquet format for efficient compression and retrieval of historical FX tick data.
