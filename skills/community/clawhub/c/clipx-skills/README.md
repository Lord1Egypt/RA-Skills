# ClipX Skills

> BNB Chain analytics for OpenClaw — TVL, fees, revenue, DApps, market insight, and more. Thin client, no API keys, no scraping on the client.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-green.svg)](https://openclaw.ai)
[![BNB Chain](https://img.shields.io/badge/BNB%20Chain-BSC-yellow.svg)](https://bnbchain.org)

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Menu Options](#menu-options)
- [Quick Start](#quick-start)
- [File Structure](#file-structure)
- [API Reference](#api-reference)
- [Local Testing](#local-testing)
- [Configuration](#configuration)
- [Server-Side API](#server-side-api)
- [Publishing](#publishing)
- [Troubleshooting](#troubleshooting)

---

## Overview

**ClipX Skills** is a thin HTTP client for the ClipX BNBChain API. It lets OpenClaw agents fetch BNB Smart Chain metrics and rankings via a simple CLI. All scraping, Playwright, and heavy logic run on the private API — this skill only calls HTTP endpoints.

| Category | Capabilities |
|----------|--------------|
| **Rankings** | TVL, fees, revenue, DApps, full ecosystem, social hype, meme rank |
| **Market** | Volume leaders, gainers/losers, Binance announcements |
| **Network** | Block, gas, sync state, block stats, address balance |
| **Output** | Text-only JSON, pre-formatted tables, monospace code blocks |

**Design:** Thin client · Text-only · Zero secrets (no API keys required)

---

## Architecture

```
User → OpenClaw Agent → api_client_cli.py → ClipX API (VPS) → DefiLlama / DappBay / Binance
                                                                    ↓
User ← OpenClaw Agent ← formatted table / JSON ← api_client_cli.py ←
```

Flow: User says "clipx" or "bnbchain" → Agent shows menu → User replies with number → Agent runs CLI → CLI calls API → API returns formatted table → Agent displays in code block.

---

## Menu Options

| # | Analysis | Description |
|---|----------|-------------|
| 1 | TVL Rank | Top 10 protocols by Total Value Locked |
| 2 | Fees Rank | Top 10 by fees paid (24h / 7d / 30d) |
| 3 | Revenue Rank | Top 10 by revenue (24h / 7d / 30d) |
| 4 | DApps Rank | Top 10 DApps by users (7d) |
| 5 | Full Ecosystem | DeFi, Games, Social, NFTs, AI, Infra, RWA leaders |
| 6 | Social Hype | Top 10 social hype tokens |
| 7 | Meme Rank | Top 10 meme tokens by score |
| 8 | Network metrics | Latest block, gas price, sync state |
| 9 | Market Insight | Binance 24h volume leaders (snapshot) |
| 10 | Market Insight (Live) | Volume + Top Gainers + Top Losers (snapshot) |
| 11 | Binance Announcements | Top 10 newest announcements |
| 12 | DEX Volume | Top 10 DEXs by volume on BNB Chain (24h / 7d / 30d) |

---

## Quick Start

### 1. Install

```bash
pip install -r requirements.txt
```

Requires only `requests`. No Playwright or heavy dependencies.

### 2. Publish to ClawHub

```bash
cd ClipX_Skills
clawhub publish . \
  --slug clipx-bnbchain-api-client \
  --name "ClipX BNBChain Metrics & Rankings (API Client)" \
  --version 1.0.0 \
  --tags latest,bnbchain,metrics,clipx
```

### 3. Use in OpenClaw

1. Install the skill from ClawHub.
2. Say **"clipx"** or **"bnbchain"**.
3. Agent shows numbered menu (1–12).
4. Reply with a number (e.g. `7` for meme rank, `12` for DEX volume).
5. Agent runs the command and displays the formatted table.

---

## File Structure

| File | Purpose |
|------|---------|
| `SKILL.md` | OpenClaw metadata, menu format, table display rules, command mapping |
| `api_client_cli.py` | HTTP client — calls ClipX API, prints JSON or formatted table |
| `format_box.py` | Local helper — fetches or reads JSON, prints box-style table |
| `requirements.txt` | Dependencies (`requests` only) |

---

## API Reference

### Modes

| Mode | Description |
|------|-------------|
| `metrics_basic` | Network status (block, gas, sync) |
| `metrics_block` | Block stats over N blocks (`--blocks 100`) |
| `metrics_address` | Balance and tx count (`--address 0x...`) |
| `clipx` | ClipX rankings (requires `--analysis-type`) |

### ClipX Analysis Types

| Type | Interval | Description |
|------|----------|-------------|
| `tvl_rank` | — | Top protocols by TVL |
| `fees_rank` | 24h, 7d, 30d | Top by fees paid |
| `revenue_rank` | 24h, 7d, 30d | Top by revenue |
| `dapps_rank` | — | Top DApps by users (7d) |
| `fulleco` | — | Full ecosystem leaders |
| `social_hype` | 24 | Social hype tokens |
| `meme_rank` | 24 | Meme token scores |
| `market_insight` | — | Binance 24h volume leaders |
| `market_insight_live` | — | Volume + gainers + losers |
| `binance_announcements` | — | Top 10 newest announcements |
| `dex_volume` | 24h, 7d, 30d | Top DEXs by volume on BNB Chain |

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--analysis-type` | (required for clipx) | One of the types above |
| `--interval` | 24h | For fees_rank, revenue_rank, social_hype, meme_rank, dex_volume |
| `--timezone` | UTC | Timestamp timezone |
| `--formatted` | default | Print server-formatted table |
| `--no-formatted` | — | Print raw JSON |
| `--live` | — | For market_insight_live: refresh in real time (Ctrl+C to stop) |

### Example Commands

```bash
# Network metrics
python api_client_cli.py --mode metrics_basic
python api_client_cli.py --mode metrics_block --blocks 100
python api_client_cli.py --mode metrics_address --address 0x0000000000000000000000000000000000000000

# ClipX rankings
python api_client_cli.py --mode clipx --analysis-type tvl_rank --timezone UTC
python api_client_cli.py --mode clipx --analysis-type fees_rank --interval 24h --timezone UTC
python api_client_cli.py --mode clipx --analysis-type dex_volume --interval 7d --timezone UTC
python api_client_cli.py --mode clipx --analysis-type market_insight_live --timezone UTC
```

---

## Local Testing

### Direct CLI (recommended)

```bash
python api_client_cli.py --mode clipx --analysis-type tvl_rank --timezone UTC
python api_client_cli.py --mode clipx --analysis-type meme_rank --interval 24 --timezone UTC
python api_client_cli.py --mode clipx --analysis-type dex_volume --interval 24h --timezone UTC
```

The client prints the server-formatted table by default.

### Using format_box.py

Fetch and format in one command:

```bash
python format_box.py --analysis-type tvl_rank
python format_box.py --analysis-type fees_rank --interval 7d
```

Or pipe from the client (useful when using `--no-formatted`):

```bash
python api_client_cli.py --mode clipx --analysis-type tvl_rank --no-formatted | python format_box.py
```

Without `--analysis-type`, `format_box.py` reads JSON from stdin (UTF-8 or UTF-8 BOM).

### Timeouts

Options 1–3, 8–12: typically &lt; 10 seconds. Options 4–7 (DappBay scraping): 30–180 seconds. Default HTTP timeout: 180s.

---

## Configuration

| Variable | Description |
|----------|-------------|
| `CLIPX_API_BASE` | ClipX API base URL. Default: `https://skill.clipx.app` |

**Linux / macOS:** `export CLIPX_API_BASE="https://your-api.com"`  
**Windows (PowerShell):** `$env:CLIPX_API_BASE = "https://your-api.com"`  
**Windows (cmd):** `set CLIPX_API_BASE=https://your-api.com`

---

## Server-Side API

This skill calls a **private ClipX API** hosted separately. The API is not published to ClawHub.

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/bnb/metrics/basic` | Network metrics |
| `GET /api/bnb/metrics/block-stats?blocks=N` | Block statistics |
| `GET /api/bnb/metrics/address?address=0x...` | Address balance and tx count |
| `GET /api/clipx/analysis?t=TYPE&interval=24h&tz=UTC` | ClipX rankings |

### ClipX Analysis Response

```json
{
  "ok": true,
  "analysis_type": "tvl_rank",
  "timestamp": "2026-03-03T17:03:08.394Z",
  "caption": "...",
  "source": "@ClipX0_",
  "formatted_table": "...",
  "items": [
    { "rank": 1, "name": "PancakeSwap AMM", "category": "Dexs", "metric_label": "TVL", "metric_value": "$1.92B" }
  ],
  "meta": { "interval": "24h" }
}
```

On error: `{ "ok": false, "error": "Human-readable error" }`

---

## Publishing

From the `ClipX_Skills` folder:

```bash
clawhub publish . \
  --slug clipx-bnbchain-api-client \
  --name "ClipX BNBChain Metrics & Rankings (API Client)" \
  --version 1.0.0 \
  --tags latest,bnbchain,metrics,clipx
```

Only the thin client and `SKILL.md` are published. API logic stays private.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Menu shows bullets instead of numbers | Re-publish the skill |
| Table not in monospace | Agent should wrap output in triple backticks. Ensure SKILL.md is up to date |
| HTTP read timeout | Default 180s. Options 4–7 may take up to 3 minutes |
| `Connection refused` / `Network error` | Check `CLIPX_API_BASE`; ensure API is running and reachable |
| `analysis-type required` | For clipx mode, always pass `--analysis-type` with a valid value |

---

## License

This skill is provided as-is. The ClipX API and backend logic are maintained separately.
