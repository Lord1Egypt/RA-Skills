# Known Use Cases (KUC)

Total: **13**

## `KUC-101`
**Source**: `scripts/create_database_snapshot_optimized.py`

Creates optimized database backups by partitioning hot (<90 days) and cold (>90 days) data into appropriate storage formats with ZSTD compression and incremental exports.

## `KUC-102`
**Source**: `scripts/compact_database.py`

Optimizes database performance by running VACUUM, rebuilding indexes, and deduplicating records within retention windows while measuring compression savings.

## `KUC-103`
**Source**: `scripts/verify_api_keys.py`

Verifies the API key management feature implementation is working correctly by testing module imports, credential initialization, and key storage/retrieval.

## `KUC-104`
**Source**: `scripts/refresh_data.py`

Fetches each economic data from FRED and Yahoo Finance APIs daily and stores results in cache for dashboard consumption.

## `KUC-105`
**Source**: `scripts/cleanup_old_data.py`

Archives data older than retention periods to Parquet files and deletes old records from main tables to reduce database size while maintaining historical access.

## `KUC-106`
**Source**: `scripts/quickstart_api_keys.py`

Provides a quick start guide for initializing and testing API key management, storing and verifying FRED API keys securely.

## `KUC-107`
**Source**: `scripts/setup_credentials.py`

Initializes and stores API credentials (FRED API key) securely in encrypted form for authenticated data access.

## `KUC-108`
**Source**: `scripts/move_fred_data.py`

Organizes FRED-related data files and scripts by moving them into a dedicated directory structure.

## `KUC-109`
**Source**: `scripts/generate_sample_data.py`

Generates sample datasets for offline mode testing, including FRED, Yahoo Finance, and World Bank sample data.

## `KUC-110`
**Source**: `scripts/init_database.py`

Initializes the DuckDB database by creating each required tables and indexes for the Economic Dashboard.

## `KUC-111`
**Source**: `scripts/fetch_sentiment_data.py`

Fetches news articles and sentiment data for specified stock symbols, including Google Trends data for sentiment analysis.

## `KUC-112`
**Source**: `scripts/migrate_pickle_to_duckdb.py`

Migrates existing pickle cache files containing FRED and Yahoo Finance data to the new DuckDB database format.

## `KUC-113`
**Source**: `scripts/refresh_data_smart.py`

Intelligently refreshes economic data based on natural update frequencies and SLAs, respecting rate limits and only fetching data when needed.
