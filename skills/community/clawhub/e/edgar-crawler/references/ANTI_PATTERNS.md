# Anti-Patterns (Cross-Project)

Total: **14**

## finance-bp-070--edgartools (2)

### `AP-DATA-SOURCING-004` — Invalidating XBRL period types for balance sheet analysis <sub>(high)</sub>

Balance sheets represent point-in-time snapshots (instant periods), not ranges (duration periods). Using duration periods for balance sheet statements causes stockholder equity and other line items to show nonsensical date ranges, corrupting financial calculations that depend on accurate period associations.

### `AP-DATA-SOURCING-012` — Large document parsing without streaming causing OOM errors <sub>(high)</sub>

SEC filings can exceed 160MB, and parsing large documents in memory without streaming causes OOM errors that crash the entire service for all users. Documents exceeding 10MB require switching to streaming parsers to prevent extreme memory usage.

## finance-bp-070--edgartools, finance-bp-079--akshare, finance-bp-084--eastmoney, finance-bp-114--edgar-crawler (1)

### `AP-DATA-SOURCING-002` — Ignoring external API rate limits causing IP blocking <sub>(high)</sub>

Multiple financial data sources (SEC EDGAR, Sina, Eastmoney, TuShare) enforce strict rate limits (10 req/sec, 120 calls/minute). Exceeding these triggers temporary IP blocks lasting 10-60 minutes, causing complete data unavailability. Immediate retry attempts during blocks extend the block duration significantly.

## finance-bp-070--edgartools, finance-bp-114--edgar-crawler (1)

### `AP-DATA-SOURCING-001` — Missing or invalid User-Agent headers for SEC API requests <sub>(high)</sub>

SEC EDGAR requires valid User-Agent identity with contact information in headers. Without this, requests are rejected with 403 Forbidden errors, completely blocking all filing access. Both edgartools and edgar-crawler enforce this constraint as fundamental to any data retrieval operation.

## finance-bp-079--akshare (4)

### `AP-DATA-SOURCING-003` — No HTTP timeout configuration causing indefinite hangs <sub>(high)</sub>

HTTP requests to external financial data sources (Yahoo, Sina, Eastmoney) without timeout values can hang indefinitely on blocked connections. This freezes the entire application and prevents data collection from all other sources, creating cascading failures across the system.

### `AP-DATA-SOURCING-005` — Malformed or empty JSON responses causing silent failures <sub>(medium)</sub>

Financial API responses containing malformed JSON raise unhandled ValueError exceptions, crashing downstream processing. Similarly, empty JSON responses (empty dict, list, null) masquerading as valid data cause silent failures producing empty DataFrames or misleading results in financial analysis.

### `AP-DATA-SOURCING-006` — Source-specific symbol mapping errors causing data corruption <sub>(high)</sub>

Stock symbols require source-specific formatting (sh/sz prefixes for Sina, numeric codes for THS, etc.). Incorrect symbol mapping causes API calls to return empty results or wrong data, corrupting financial datasets with missing records or entirely incorrect tickers being stored.

### `AP-DATA-SOURCING-013` — Column mapping length mismatch causing DataFrame errors <sub>(medium)</sub>

Column mapping constants with length mismatch against actual API response columns cause ValueError exceptions during DataFrame construction. Raw field names (f1, f2, f12) must be mapped to meaningful names (最新价, 涨跌幅) with exact column count alignment.

## finance-bp-103--ArcticDB (3)

### `AP-DATA-SOURCING-007` — Using unsupported DataFrame types with time-series storage <sub>(high)</sub>

ArcticDB does not support MultiIndex columns, PyArrow-backed pandas DataFrames, or timedelta64 columns. Attempting to write these DataFrame types raises ArcticDbNotYetImplemented exceptions, causing write failures and permanent data loss if not properly handled before storage operations.

### `AP-DATA-SOURCING-008` — Non-atomic storage writes causing concurrent access corruption <sub>(high)</sub>

Storage backends without atomic write_if_none operations can cause data corruption under concurrent multi-writer access. Similarly, updating reference keys before atom keys complete allows readers to access incomplete or missing data, breaking version chain integrity.

### `AP-DATA-SOURCING-014` — Pruning snapshot-protected versions breaking point-in-time recovery <sub>(high)</sub>

Deleting or pruning versions that are referenced by existing snapshots breaks historical data access. Snapshots provide point-in-time recovery capabilities, and removing their referenced versions causes read failures when users attempt to access data from specific snapshots.

## finance-bp-114--edgar-crawler (1)

### `AP-DATA-SOURCING-010` — 8-K filing item numbering scheme mismatch for historical filings <sub>(medium)</sub>

8-K filings use obsolete item numbering (1-12) before 2004-08-23 and new numbering (1.01-9.01) after. Using the wrong numbering scheme causes no matches for historical filings, resulting in empty item sections and complete extraction failure for pre-2004 data.

## finance-bp-128--yfinance (2)

### `AP-DATA-SOURCING-009` — Missing timezone-aware DatetimeIndex causing DST offset errors <sub>(high)</sub>

Price history DataFrames returned without timezone-aware DatetimeIndex cause incorrect timestamp interpretation when combined with other timezone-aware data. This leads to 23-25 hour offset errors during daylight saving time transitions, corrupting historical price calculations.

### `AP-DATA-SOURCING-011` — Yahoo Finance missing crumb authentication causing 401/403 errors <sub>(high)</sub>

Yahoo Finance API requires crumb and cookie authentication with every request. Without proper crumb management, API calls return 401 Unauthorized or HTML error pages instead of JSON data, breaking all downstream price and financial data processing.
