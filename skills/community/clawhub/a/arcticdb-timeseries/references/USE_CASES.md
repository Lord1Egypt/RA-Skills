# Known Use Cases (KUC)

Total: **17**

## `KUC-101`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_aws_public_blockchain.ipynb`

Setting up AWS credentials to enable secure access to public blockchain data stored in S3, allowing integration with ArcticDB for time-series storage.

## `KUC-102`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_billion_row_challenge.ipynb`

Demonstrates ArcticDB's ability to handle massive datasets (1 billion rows of temperature data) with efficient aggregation, serving as a performance benchmark for large-scale data operations.

## `KUC-103`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_concat.ipynb`

Demonstrates efficient concatenation of multiple DataFrames stored in ArcticDB using lazy loading to minimize memory consumption during batch operations.

## `KUC-104`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_equity_analytics.ipynb`

Demonstrates downloading historical equity market data from yfinance and storing it in ArcticDB for analytics, enabling time-series analysis of stock prices and volumes across multiple symbols.

## `KUC-105`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_equity_options.ipynb`

Demonstrates storing and querying equity options data including expiry analysis and option Greeks, supporting options strategy research and analysis workflows.

## `KUC-106`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_lazydataframe.ipynb`

Demonstrates reading large datasets (10M-1B rows) efficiently using ArcticDB's lazy loading to reduce memory usage while selecting specific columns.

## `KUC-107`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_lmdb.ipynb`

Demonstrates basic storage operations (write, read, append, update) with ArcticDB using LMDB backend, including version management and subframe reading capabilities.

## `KUC-108`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_querybuilder.ipynb`

Demonstrates efficient querying of large datasets (up to 1B rows) with specific column selection, optimizing read performance by avoiding unnecessary data loading.

## `KUC-109`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_read_as_arrow.ipynb`

Demonstrates reading ArcticDB data into Arrow and Polars formats for interoperability with modern data science tooling, enabling seamless integration with downstream processing pipelines.

## `KUC-110`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_recursive_normalizers.ipynb`

Demonstrates storing complex nested data structures including DataFrames within dictionaries using recursive normalizers, enabling preservation of hierarchical data relationships.

## `KUC-111`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_resample.ipynb`

Demonstrates resampling high-frequency time-series data (12M rows at second frequency) to lower frequencies (1-minute) using built-in aggregation, optimizing storage and query performance.

## `KUC-112`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_demo_snapshots.ipynb`

Demonstrates creating and managing data snapshots for point-in-time recovery, enabling reproducibility and audit trails for time-series data in ArcticDB.

## `KUC-113`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_merge.ipynb`

Demonstrates merging new data with existing datasets using merge strategies (update, do_nothing) for handling price corrections and data synchronization in financial applications.

## `KUC-114`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_pythagorean_won_loss_formula_notebook.ipynb`

Demonstrates sports data analytics using the Pythagorean expectation formula to analyze team performance, including data storage, visualization, and OLS statistical modeling.

## `KUC-115`
**Source**: `docs/mkdocs/docs/notebooks/ArcticDB_staged_data_with_tokens.ipynb`

Demonstrates staging data from multiple concurrent writers before finalizing with tokens, enabling distributed data ingestion workflows with proper synchronization.

## `KUC-116`
**Source**: `docs/mkdocs/docs/notebooks/styling.py`

Provides styling functions for DataFrame visualization with custom themes, color schemes, and export capabilities for creating professional data presentations.

## `KUC-117`
**Source**: `docs/mkdocs/docs/technical/release_checks.py`

Provides automated release validation tests that verify basic ArcticDB functionality including library creation, data write/read operations, and library deletion.
