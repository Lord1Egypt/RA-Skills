# edgar-risk-diff

> **What is *new* in this company's 10-K Risk Factors vs. last year?**
> Get the answer in 8 seconds, for any US-listed ticker, with theme tags and a churn score.

A Claude / OpenClaw skill for diffing the SEC 10-K **Item 1A (Risk Factors)** section between two filings. No API key. No subscription. Uses SEC EDGAR directly.

## Why this exists

Equity analysts, B-school students, and serious retail investors spend hours every winter manually diffing 10-K risk sections to find what a company is newly worried about. The signal is real — companies are required to flag *material* new risks, so additions to Item 1A often precede formal guidance changes. But the diffing work is tedious, error-prone, and most existing tools either gate it behind a $1k/yr terminal or charge per filing.

This skill does that work locally for free, with one command.

## Install (ClawHub)

```bash
openclaw skills install edgar-risk-diff
```

Or clone this repo and drop it into your skills directory.

## Usage

```bash
# 1. Diff the two most recent 10-Ks for a ticker
python3 scripts/risk_diff.py diff AAPL

# 2. Diff specific years
python3 scripts/risk_diff.py diff TSLA --years 2024 2022

# 3. Print the latest Item 1A section as-is
python3 scripts/risk_diff.py latest NVDA

# 4. Sweep across many tickers (markdown table, perfect for morning briefs)
python3 scripts/risk_diff.py scan AAPL MSFT GOOGL NVDA META AMZN

# 5. [premium] Embedding-based novelty score
python3 scripts/risk_diff.py novelty AAPL --top 10
```

## Example output (AAPL 2024 → 2025)

```
# AAPL — Risk Factors Diff
_2024 10-K  →  2025 10-K_  (2024-11-01 → 2025-10-31)

**Churn:** 90.5%  ·  **Added:** 4  ·  **Removed:** 5  ·  **Modified:** 10  ·  **Unchanged:** 2

## New themes
- **Regulation** — 3 new paragraphs
- **Litigation** — 3 new paragraphs
- **Workforce** — 2 new paragraphs
- **Cybersecurity** — 1 new paragraph
- **AI / ML** — 1 new paragraph
...
```

## What you get

- **Churn percentage** — how much of the risk section changed
- **Theme rollup** — added paragraphs bucketed by AI, cyber, geopolitics, regulation, supply chain, climate, etc.
- **Added / Removed / Modified** paragraphs with similarity ratios
- **Multi-ticker scan** — one-line summary table across a watchlist
- **(Premium) Semantic novelty score** — ranks new paragraphs by how genuinely new they are, catching paraphrased risks the keyword diff alone misses

## Premium tier

A one-time $19 license key unlocks the `novelty` subcommand and priority email support. Buy a key at the ClawHub listing → save to `~/.edgar-risk-diff/license.txt`.

The free tier is fully functional on its own.

## How it works

1. Resolves ticker → CIK via `sec.gov/files/company_tickers.json`
2. Pulls the filings list via the `data.sec.gov/submissions/` API
3. Downloads the two most recent 10-K primary documents
4. Strips HTML, slices out Item 1A between `Item 1A. Risk Factors` and `Item 1B`/`Item 2`
5. Segments into paragraphs, matches across years (exact key → fuzzy), classifies as added / removed / modified
6. Tags added paragraphs by theme using a curated keyword dictionary
7. Premium: hashed-bigram cosine embedding for semantic novelty ranking

All deps: `python ≥ 3.9`, `requests`. No transformers, no API keys, no per-request cost.

## Data source

SEC EDGAR. Public domain. Skill respects EDGAR fair-access rate limits (under 10 req/s) and identifies itself via `User-Agent`.

## Limitations

- 10-K only (not 10-Q — Item 1A changes annually in practice).
- Item 1A regex extraction works on standard formatting. Some filings use non-standard HTML; if extraction fails, run `latest` to inspect.
- Not legal or investment advice. This is a research tool.

## License

MIT for the skill code. Premium license key gates the `novelty` subcommand only.
