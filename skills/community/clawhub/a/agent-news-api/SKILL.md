---
name: Agent News API
version: 1.2.0
author: agentnewsapi
repository: https://github.com/agentnewsapi/agentnewsapi
status: Mainnet Beta
description: A set of free and premium AI enriched global news streams for agents, provided by agentnewsapi.com. Powered by $ANA on Solana.
tags: [news, web3, signals, autonomous-finance, zero-hitl]
entry: agent-news-cli.js
permissions:
  network:
    - api.agentnewsapi.com
    - agentnewsapi.com
requires:
  runtime: node >= 22.0.0
  env:
    - AGENT_NEWS_API_KEY (optional — auto-generated via Zero-HITL onboarding)
    - SOLANA_PRIVATE_KEY (optional — required for Zero-HITL auth and autonomous funding on premium endpoints)
install:
  - npm install
---

# Agent News API (Mainnet Beta)

This skill grants autonomous agents access to the **Agent News API**, the premier signal ingestion point for AI entities seeking live global event context. We distill the noise of over 100,000 daily events into a filtered, enriched, and machine-readable stream of semantic payloads containing high signal metadata such as entities and locations.

Agents can monitor market-moving events, extract tactical sentiment, and completely self-manage their API funding via Solana using our Zero-HITL (Human-In-The-Loop) architecture.

## 🛠️ Tools (For Autonomous Agent Use)

The following tools are exposed to the LLM agent upon installation:

### `fetch_news_premium`
Fetches the absolute latest, sub-second global signals from the Firehose. 
- **Cost:** $0.0001 USD worth of $SOL per story (dynamically pegged).
- **Arguments:** - `limit` (integer): Number of signals to fetch (Max: 500).
  - `q` (string): Search or category query.
- **Returns:** Array of structured Story Objects (see schema below).

### `fetch_news_free`
Fetches archived news signals with a mandatory **20-minute time offset**. Ideal for lower criticality information gathering tasks.
- **Cost:** Free.
- **Limits:** 1 request per minute. Max 100 stories per request.
- **Arguments:** - `limit` (integer): Number of signals to fetch (Max: 100).
  - `q` (string): Search or category query.

### `check_credit_balance`
Queries the current API credit balance denominated in $SOL. Agents should call this before initiating high-frequency loops.

### `autonomous_onboard`
Triggers the Zero-HITL registration flow. The agent uses its local Solana private key to sign a cryptographic challenge (`"Allow Agent News API Access"`), autonomously negotiating and saving a persistent `X-API-KEY`.

### `get_deposit_address`
Returns the official Protocol Hot Wallet address (`6rSLPtj9Ef7aifNHHFzEPkY5hWECJXryivWx1YhPuXSa`). Agents can use this to transfer native $SOL from their wallets to top up API credit.

---

## ⚡ WebSocket Stream (Premium Only)

For sub-second latency updates, agents can connect to the global `firehose` stream. This is the recommended ingestion method for high-frequency autonomous decision making or rapid-response entities.

- **Endpoint:** `https://api.agentnewsapi.com`
- **Protocol:** Socket.io
- **Event:** `news_update`

### Node.js Implementation Example

```javascript
const io = require('socket.io-client');

const socket = io('https://api.agentnewsapi.com', {
    auth: { apiKey: process.env.AGENT_NEWS_API_KEY }
});

socket.on('news_update', (data) => {
    console.log('New Signal Ingested:', data.title);
    // data._meta contains cost (e.g., 0.00000118 SOL) and remainingCredits
});

socket.on('error', (err) => {
    if (err.code === 'INSUFFICIENT_CREDITS') {
        console.error('Refill $SOL balance to resume stream.');
    }
});
```

- **Cost:** $0.0001 USD worth of $SOL per story received (same as premium REST).
- **Latency:** Sub-second (Global Firehose).

---

## 💻 CLI Commands (For Human Operators)

- `agentnews fetch --limit <number>`: Fetch real-time premium signals.
- `agentnews fetch-free --limit <number>`: Fetch 20-minute delayed signals.
- `agentnews balance`: Check current $SOL API credit balance.
- `agentnews onboard`: Execute the Zero-HITL autonomous key generation.
- `agentnews deposit-address`: Retrieve the Protocol Hot Wallet address.

---

## 🔐 Security & Zero-HITL Principles

This skill handles sensitive authentication to enable true autonomy. 
1. **Local-First Cryptography:** The `SOLANA_PRIVATE_KEY` is utilized strictly locally by the SDK to generate `nacl` detached signatures. The private key is **never** transmitted to the Agent News API servers.
2. **Dynamic Pegging:** The $SOL exchange rate is updated every second using a public Coinbase endpoint to maintain the fixed $0.0001 USD/story cost.
3. **Automated Deflation:** 25% of all $SOL API revenue is automatically allocated to buybacks and permanent burns of the protocol's governance token, **$ANA** (`GR9NrQhGfhRjKAerVCaRJAHmZqvUtiQ3dVjh9AMxpump`).

---

## 📦 Data Schema: Semantic Payloads

All news signals are delivered as JSON objects specifically curated for LLM comprehension:

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Unique identifier for the story (e.g., `story_92b1...`). |
| `title` | string | AI-curated headline focused on factual intensity. |
| `summary` | string | High-signal technical distillation. |
| `significance` | number | Impact score from 1 to 100 calculated by the reasoning engine. |
| `sentiment` | object | Contains `label` (Positive/Negative/Neutral) and `score`. |
| `entities` | array | List of extracted organizations, locations, and assets. |
| `category` | string | Primary theme (Macro, Geopolitical, Crypto, etc). |
| `_meta` | object | **Premium Only:** Contains transaction `cost` and `remainingCredits` in $SOL. |

---

## ⚙️ Environment Variables

- `AGENT_NEWS_API_KEY`: *(Optional)* Your persistent API key (can be generated via `agentnews onboard`).
- `SOLANA_PRIVATE_KEY`: *(Optional)* Base58 encoded Ed25519 key for Zero-HITL onboarding and automated funding.
- `AGENT_NEWS_API_URL`: *(Optional)* Default is `https://api.agentnewsapi.com`.
