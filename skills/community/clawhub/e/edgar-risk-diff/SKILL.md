---
name: edgar-risk-diff
slug: edgar-risk-diff
version: 1.0.2
description: Diff the SEC 10-K Risk Factors section (Item 1A) between two filings for any US-listed ticker. Surfaces new risks, removed risks, modified language, theme rollups (AI, cyber, geopolitics, regulation), and a churn percentage. Uses SEC EDGAR directly — no API key required. Premium tier adds embedding-based novelty scoring.
license: MIT
disable-model-invocation: false
---

# Edgar Risk Diff

**What is new in this company's risk factors vs. last year?** This skill answers that
question in seconds, for any US-listed ticker, by pulling the two most recent 10-Ks
from SEC EDGAR and producing a structured diff of Item 1A (Risk Factors).

## When to use this skill

Activate when the user asks any of:

- "What changed in {ticker}'s 10-K risk factors?"
- "What new risks did {ticker} disclose this year?"
- "Did {ticker} drop any risk factors compared to last year?"
- "Compare {ticker}'s risk factors between {year1} and {year2}."
- "Scan {tickers…} for new AI / cyber / China / regulatory risks."
- "Pull the latest risk factors for {ticker}."

Do NOT use this skill for:

- 10-Q diffs (this skill is 10-K only — Item 1A typically only changes annually).
- Live price / earnings / fundamentals (use a market-data skill instead).
- Legal advice. Output is informational only.

## Quick start

```bash
# Diff the two most recent 10-Ks
python3 {baseDir}/scripts/risk_diff.py diff AAPL

# Diff specific years
python3 {baseDir}/scripts/risk_diff.py diff TSLA --years 2024 2022

# Print the latest Risk Factors section (no diff)
python3 {baseDir}/scripts/risk_diff.py latest NVDA

# One-line summary across many tickers (great for morning briefs)
python3 {baseDir}/scripts/risk_diff.py scan AAPL MSFT GOOGL NVDA META AMZN

# [premium] Embedding-based novelty score — ranks paragraphs by how new they
# actually are, not just whether the text differs.
python3 {baseDir}/scripts/risk_diff.py novelty AAPL --top 10
```

## What the diff output contains

1. **Churn percentage** — fraction of paragraphs that were added, removed, or modified.
2. **New themes** — rollup of added paragraphs by topic (Cybersecurity, AI/ML,
   Geopolitics, Climate, Supply chain, Regulation, Litigation, Macro, Workforce,
   Crypto, Pandemic).
3. **Added paragraphs** — risk language that did not exist in the prior 10-K,
   each tagged with the themes it hits.
4. **Removed paragraphs** — language the company dropped (often as meaningful
   as what they added).
5. **Modified paragraphs** — old/new pairs with a similarity ratio, so the user
   can see how a known risk has been re-framed.

## Free vs. premium

| Capability | Free | Premium |
|---|---|---|
| Diff (added/removed/modified) | ✅ | ✅ |
| Theme rollup (keyword-based) | ✅ | ✅ |
| Multi-ticker scan | ✅ | ✅ |
| **Semantic novelty score** (embedding-based, catches paraphrased risks that the keyword diff misses) | ❌ | ✅ |
| Priority email support | ❌ | ✅ |

Premium unlocks the `novelty` subcommand. Buy a license key at the listing and
save it to `~/.edgar-risk-diff/license.txt`, or export
`EDGAR_RISK_LICENSE=<key>`.

## Data source & rate limiting

- Reads from `data.sec.gov` and `www.sec.gov/Archives/` (public, free, no auth).
- Throttles to under 10 req/s per SEC fair-access policy.
- Caches all responses in `~/.edgar-risk-diff/cache/` — subsequent runs on the
  same ticker are instant.
- Sends an EDGAR-compliant `User-Agent` header. Override with
  `EDGAR_USER_AGENT="Your Name your@email.com"` if redistributing.

## Security & permissions

**No API keys. No credentials. No outbound writes.**

- Makes HTTPS GET requests to `data.sec.gov` and `www.sec.gov` only.
- Writes only inside `~/.edgar-risk-diff/` (cache + optional license file).
- No telemetry. No analytics. No third-party calls.
- Review `scripts/risk_diff.py` (≈350 lines, single file, pure stdlib + requests)
  before first use.

## Limitations

- Item 1A detection is regex-based and works on standard 10-K formatting. Filings
  that use highly non-standard HTML may fail to extract — re-run with `latest`
  to see what the parser sees.
- Paragraph matching is fuzzy (SequenceMatcher + hashed-bigram cosine). Very
  short paragraphs (<40 chars) are ignored to suppress noise.
- Premium novelty uses a deterministic hashed-bigram embedding — runs locally,
  no external API. Quality is below a transformer model but catches the
  paraphrase patterns this skill is designed for.
