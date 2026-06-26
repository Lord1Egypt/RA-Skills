# Security Policy

## Overview

Fintech Research Toolkit is a 100% self-hosted, free equity research tool for Claude Code. This document describes the security posture of the project, network behavior, and how reported issues are handled.

## Network Behavior

This project makes outbound HTTPS connections **only** to the following official, free, public financial data APIs:

| Destination | Domain | Purpose | Protocol | Authentication |
|-------------|--------|---------|----------|----------------|
| Yahoo Finance (via yfinance library) | Various Yahoo Finance domains | Stock quotes, fundamentals, historical prices | HTTPS (library-managed) | None |
| SEC EDGAR | `www.sec.gov` | US company filings (10-K, 10-Q, 8-K) | HTTPS GET | None (public API) |
| HKEX News | `www1.hkexnews.hk` | Hong Kong regulatory announcements | HTTPS GET | None (public access) |
| FRED API | `api.stlouisfed.org` | US macroeconomic data (rates, CPI, employment) | HTTPS GET | Optional free API key |
| NewsAPI | `newsapi.org` | Financial news headlines | HTTPS GET | Optional free API key (100 req/day) |
| RSS Feeds | Reputable financial news domains | News aggregation | HTTPS GET | None |

### Key Security Features

- **No executable downloads**: This project does not download or execute external binaries
- **No shell command execution**: All network operations use Python's `requests` library
- **SSL verification enabled**: All HTTPS requests use certificate verification (`verify=True`)
- **Input validation**: All user-provided inputs (tickers, stock codes, queries) are validated against strict allowlists
- **Response size limits**: All HTTP responses are capped (1-2MB) to prevent memory exhaustion
- **Rate limiting**: Built-in delays between requests (2s for HKEX)
- **No persistent credentials**: Optional API keys are read from environment variables only

## Input Validation

| Input Type | Validation Rule | Example |
|------------|----------------|---------|
| US Ticker | `^[A-Z]{1,5}$` | `AAPL`, `TSLA` |
| HK Stock Code | `^\d{4,5}$` | `0700`, `9988` |
| FRED Series ID | Alphanumeric with dash/underscore | `DGS10`, `CPIAUCSL` |
| Search Query | Sanitized, max 200 chars, dangerous chars removed | `Tencent earnings` |
| Form Types | Allowlist against SEC form codes | `10-K`, `10-Q`, `8-K` |

## Dependency Security

All dependencies are open-source and available from PyPI (Python Package Index):

```
yfinance>=0.2.54    # Yahoo Finance client (MIT license)
pandas>=2.0.0       # Data manipulation (BSD license)
requests>=2.31.0    # HTTP client (Apache 2.0)
beautifulsoup4>=4.12.0  # HTML parsing (MIT license)
feedparser>=6.0.10  # RSS parsing (BSD license)
mcp>=1.0.0          # MCP SDK (MIT license)
httpx>=0.27.0       # HTTP client (BSD license)
```

These are standard, widely-used Python packages in the data science ecosystem. The `vcruntime140.dll` reference that may appear in security scans is a standard Microsoft C++ runtime library required by pandas/numpy's compiled extensions — it is not related to DLL sideloading attacks.

## Reporting Security Issues

If you discover a security issue, please email the project maintainer or open a private issue on GitHub. We aim to respond within 48 hours.

## Version History

| Version | Security Changes |
|---------|-----------------|
| v2.1.0 | Added SSL verification, input validation, response size limits, User-Agent identity headers |
| v2.0.2 | Removed all external paid service references |
| v2.0.0 | Replaced paid MCP with self-hosted local server |
