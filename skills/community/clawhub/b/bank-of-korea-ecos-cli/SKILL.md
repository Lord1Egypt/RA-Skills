---
name: Bank of Korea ECOS CLI
slug: bank-of-korea-ecos-cli
version: 0.1.0
summary: CLI for Bank of Korea ECOS Open API — list statistic tables and fetch time series (A/S/Q/M/D)
license: MIT
tags: [latest]
metadata:
  openclaw:
    requires:
      env:
        - BOK_API_KEY
    primaryEnv: BOK_API_KEY
---

# Bank of Korea ECOS CLI

Minimal command-line client for the Bank of Korea Economic Statistics System (ECOS) Open API.

- List available statistic tables
- Fetch time series by statistic code and frequency (A,S,Q,M,D)
- JSON output, suitable for piping to jq or saving to files

## Installation

Clone and run in a virtualenv (or install once on your host/agent image):

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

## Usage

Environment variables:
- BOK_API_KEY (required) — your ECOS API key
- BOK_LANG (optional) — `kr` or `en` (default: `kr`)

Examples:

```bash
# Help
ecos-cli -h

# List statistic tables (first 1000)
ecos-cli table-list | jq '.[] | .[]? // .'

# Fetch a monthly time series for a statistic code between start/end dates
ecos-cli series 722Y001 M 202001 202412 | jq .
```

Notes:
- Date formats depend on the cycle: `YYYY` for A/S, `YYYYQQ` for Q (ECOS accepts `YYYYQ#` in some cases), `YYYYMM` for M, `YYYYMMDD` for D.
- Output structure is a direct passthrough of the ECOS JSON response.

## API references
- ECOS API portal: https://ecos.bok.or.kr/api/
- StatisticTableList: `/StatisticTableList/{API_KEY}/json/{lang}/{start}/{end}/`
- StatisticSearch: `/StatisticSearch/{API_KEY}/json/{lang}/{start}/{end}/{STAT_CODE}/{CYCLE}/{START}/{END}/`
