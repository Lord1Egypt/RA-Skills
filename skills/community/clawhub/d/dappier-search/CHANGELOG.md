# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## 1.0.0 - 2026-01-11

Initial public release of the **Dappier** skill.

### Added

- Skill documentation and usage examples in [`SKILL.md`](SKILL.md).
- Real-time web search CLI tool in [`scripts/realtime-search.mjs`](scripts/realtime-search.mjs).
  - Posts queries to Dappier Real Time Search AI model.
  - Prints a markdown-formatted "## Real Time Search Results" section.
- Stock market CLI tool in [`scripts/stock-market.mjs`](scripts/stock-market.mjs).
  - Posts ticker-based financial queries to the Dappier Stock Market AI model.
  - Prints a markdown-formatted "## Stock Market Data" section.
- Sports news recommendations tool in [`scripts/sports-news.mjs`](scripts/sports-news.mjs).
  - Supports `--top_k` and `--algorithm` (`most_recent`, `semantic`, `most_recent_semantic`, `trending`).
  - Prints a markdown-formatted list of results including author, date, source, URL, image, relevance, and summary.
- Benzinga financial news recommendations tool in [`scripts/benzinga-news.mjs`](scripts/benzinga-news.mjs).
  - Supports `--top_k` and `--algorithm`.
  - Prints a markdown-formatted list of results with key metadata and summaries.
- Lifestyle news recommendations tool in [`scripts/lifestyle-news.mjs`](scripts/lifestyle-news.mjs).
  - Supports `--top_k` and `--algorithm`.
  - Prints a markdown-formatted list of results with key metadata and summaries.
- Research paper search CLI tool in [`scripts/research-papers.mjs`](scripts/research-papers.mjs).
  - Posts scholarly queries to the Dappier Research Papers Search AI model.
  - Prints a markdown-formatted "## Research Papers Search" section.
- Stellar AI (solar & roof analysis) CLI tool in [`scripts/stellar-ai.mjs`](scripts/stellar-ai.mjs).
  - Posts a residential address query to the Dappier Stellar AI model.
  - Prints a markdown-formatted "## Stellar AI (Solar & Roof Analysis)" section.

### Security

- API credentials are supplied via the `DAPPIER_API_KEY` environment variable (not stored in the repo).

### Setup

- Get your API key from Dappier:
  - Sign in at https://platform.dappier.com
  - Go to https://platform.dappier.com/profile/api-keys
  - Create/copy an API key and set it as `DAPPIER_API_KEY` in your environment.
