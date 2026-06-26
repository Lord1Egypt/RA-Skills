---
name: clipx-bnbchain-api-client
description: Thin client for the private ClipX BNBChain API, returning text-only JSON metrics and rankings for BNB Chain (no scraping code, no API keys).
metadata: { "openclaw": { "emoji": "🟡", "requires": { "bins": ["python"] }, "os": ["win32", "linux", "darwin"] } }
---

## Response rules (read first)

**Rule 1 — Menu format:** Always use numbered lines (1. 2. 3. …). See "Interactive menu" section.

**Rule 2 — Table format:** Always wrap the table output inside a markdown code block (triple backticks). Start with a line containing only three backticks, then the table lines, then a line containing only three backticks. This is required so the table displays in monospace with aligned columns. The API returns tables formatted at **40 chars per line** (mobile-friendly); do not reformat or truncate — pass through exactly. **Exception:** For option 11 (Binance Announcements), do NOT wrap in code block — pass through the API output as-is (plain markdown with **📢 Binance Announcements** header, 🔸 bullets, and blank line after each item).

**Rule 3 — Response ends with the output.** After the table (or Binance list for option 11), your message is complete. Write nothing else.

---

## What this skill does

Calls the ClipX BNBChain API via `python "{baseDir}/api_client_cli.py"` to fetch text-only BNB Chain metrics and rankings. The backend handles all scraping.

---

## Interactive menu

When the user says "clipx", "bnbchain", "bnbchain analysis", or asks for BNB Chain reports without specifying which one, output this menu exactly:

Output this menu inside a code block (triple backticks) so it displays as a formatted box:

```
========================================
🟡 ClipX / BNBChain Analysis
========================================
 1. TVL Rank
 2. Fees Rank (24h/7d/30d)
 3. Revenue Rank (24h/7d/30d)
 4. DApps Rank
 5. Full Ecosystem
 6. Social Hype
 7. Meme Rank
 8. Network Metrics
 9. Market Insight
10. Market Insight (Live)
11. Binance Announcements
12. DEX Volume (24h/7d/30d)
========================================
Reply with a number (1–12)
```

---

## Commands (number → command)

| # | Command |
|---|---------|
| 1 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type tvl_rank --timezone UTC` |
| 2 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC` |
| 3 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type revenue_rank --interval 24h --timezone UTC` |
| 4 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dapps_rank --timezone UTC` |
| 5 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type fulleco --timezone UTC` |
| 6 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type social_hype --interval 24 --timezone UTC` |
| 7 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC` |
| 8 | `python "{baseDir}/api_client_cli.py" --mode metrics_basic` |
| 9 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type market_insight --timezone UTC` |
| 10 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type market_insight_live --timezone UTC` |
| 11 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type binance_announcements --timezone UTC` |
| 12 | `python "{baseDir}/api_client_cli.py" --mode clipx --analysis-type dex_volume --interval 24h --timezone UTC` |

For 2 (fees), 3 (revenue), and 12 (DEX volume), default to 24h. If the user specifies 7d or 30d, use `--interval 7d` or `--interval 30d`.

---

## Displaying results

The client prints a pre-formatted table. Your job:

1. Run the command.
2. Take the stdout output (the formatted table).
3. **For options 1–10, 12:** Put it inside a markdown code block (three backticks on a line before, three backticks on a line after). Tables are formatted at **40 chars per line** (mobile-friendly); pass through exactly — do not reformat, truncate, or widen.
4. **For option 11 (Binance Announcements):** Output the stdout as-is. Do NOT wrap in code block. Pass through exactly.
5. Send it. Done. Your response is complete.

Your response must look exactly like this (API uses 40 chars/line for mobile):

```
========================================
🚀 TOP 10 MEME TOKENS BY SCORE
========================================
----------------------------------------
#   | NAME         | —       | SCORE
----------------------------------------
1   | TokenA       | —       | 4.76
2   | TokenB       | —       | 4.61
...
========================================
Source: @ClipX0_
```

Do not reformat. Pass through the 40-char output as-is.

---

## Network metrics (option 8)

Returns JSON with `latest_block`, `gas_price_gwei`, `syncing`. Summarize in plain language.

---

## Market Insight (Live) — option 10

Uses API `market_insight_live` — Volume Leaders + Top Gainers + Top Losers in one snapshot. (No `--live` in chat; OpenClaw shows static messages. Use `--live` locally for real-time refresh.)

## Binance Announcements — option 11

Uses API `binance_announcements` — Top 10 newest announcements.

**Display rules:** Run the command, take the stdout output, and output it exactly as received. Do NOT wrap in a code block. The API returns plain markdown with:
- Bold header: **📢 Binance Announcements**
- 🔸 diamond bullet before each announcement
- Blank line after each item

Pass through the output unchanged. Your response ends after the last announcement.

## DEX Volume — option 12

Uses API `dex_volume` — Top 10 DEXs on BNB Chain by trading volume. Supports intervals: 24h (default), 7d, 30d. Data from DefiLlama.

---

## Other modes

- `--mode metrics_block --blocks 100` — average block time and gas over recent blocks.
- `--mode metrics_address --address 0x...` — BNB balance and tx count for an address.

---

## Environment

The API base URL defaults to `https://skill.clipx.app`. Override with `CLIPX_API_BASE` env var.
