---
name: Agent News (Free Tier)
version: 1.2.0
author: agentnewsapi
homepage: https://agentnewsapi.com
repository: https://github.com/agentnewsapi/agentnewsapi
status: Public Beta (Free)
description: A free AI enriched global news stream for agents, provided by agentnewsapi.com. Powered by $ANA on Solana.
tags: [news, world-news, geospatial, signals, autonomous-agents, zero-hitl, free-tier]
entry: agent-news-cli.js
permissions:
  network:
    - agentnewsapi.com
requires:
  runtime: node >= 22.0.0
install:
  - npm install
---

# Agent News (Free Tier)

This skill provides autonomous agents with access to the **Agent News Protocol** through a simplified, free-tier interface. It is designed for maximum ease of use and compatibility with OpenClaw security standards.

Agents can monitor market-moving events and extract tactical sentiment from a filtered, enriched, and machine-readable stream of semantic payloads.

## 🛠️ Tools (For Autonomous Agent Use)

The following tool is exposed to the LLM agent:

### `fetch_news_free`
Fetches archived news signals with a mandatory **20-minute time offset**. This tool is free to use and does not require an API key. 

- **Cost:** Free.
- **Limits:** 1 request per minute. Max 100 stories per request.
- **Arguments:**
  - `limit` (integer): Number of signals to fetch (Max: 100, Default: 10).
  - `q` (string): Optional search or category query (e.g., "crypto", "macro").
- **Returns:** A JSON object containing an array of structured Signal Objects.

---

## 💻 CLI Commands (For Human Operators)

- `node agent-news-cli.js fetch --limit <number>`: Fetch 20-minute delayed news signals.
- `node agent-news-cli.js help`: Show help information.

---

## 📦 Data Schema: Signal Objects

All news signals are delivered as JSON objects specifically curated for LLM comprehension:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Unique identifier for the story. |
| `title` | string | AI-curated headline focused on factual intensity. |
| `summary` | string | High-signal technical distillation. |
| `significance` | number | Impact score from 1 to 100. |
| `sentiment` | object | Contains `label` (Positive/Negative/Neutral) and `score`. |
| `entities` | array | List of extracted organizations, locations, and assets. |
| `category` | string | Primary theme (Macro, Geopolitical, Crypto, etc). |

---

## 🔐 Security & Simplicity

This version of the skill is built for absolute transparency and security:
1. **Zero Authentication:** No API keys or environment variables are required.
2. **Native Fetch:** Uses standard Node.js native `fetch` for minimal dependencies.
3. **No Networking Overhead:** Only communicates with `agentnewsapi.com`.
