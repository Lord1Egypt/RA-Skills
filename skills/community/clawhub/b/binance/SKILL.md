---
name: Binance API
slug: binance
version: 1.0.0
homepage: https://clawic.com/skills/binance
description: Operate Binance Spot APIs through safe REST, WebSocket, and SDK workflows with signed requests, rate-limit control, and testnet-first execution.
changelog: Initial release with production-safe Binance Spot API workflows for REST, WebSocket, signing, and testnet validation.
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["curl","openssl","jq"],"env":["BINANCE_API_KEY","BINANCE_API_SECRET"]},"os":["linux","darwin","win32"]}}
---

# Binance Spot API Operations

## Setup

On first use, read `setup.md` for integration preferences and safe environment defaults.

## When to Use

User needs to read Binance market data, place or manage Spot orders, or troubleshoot signed API calls from terminal workflows. Agent handles request signing, filter validation, rate-limit safety, and WebSocket reconciliation.

## Architecture

Memory lives in `~/binance/`. See `memory-template.md` for structure.

```text
~/binance/
├── memory.md            # API mode, symbols, and execution preferences
├── runbooks.md          # Repeatable workflows that worked in production
├── incidents.md         # Failures, response codes, and fixes
└── snapshots/           # Symbol filters and pre-trade validation captures
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup behavior | `setup.md` |
| Memory template | `memory-template.md` |
| Fast start commands | `quickstart.md` |
| Auth and signatures | `auth-signing.md` |
| Market data patterns | `market-data.md` |
| Streams and WS API | `websocket.md` |
| SDK and CLI options | `sdk-cli.md` |
| Limits and error handling | `errors-limits.md` |
| Spot testnet operations | `testnet.md` |
| Incident recovery | `troubleshooting.md` |

## Requirements

- `curl`
- `openssl`
- `jq`
- `BINANCE_API_KEY` and `BINANCE_API_SECRET` for signed Spot requests
- Optional: `BINANCE_BASE_URL`, `BINANCE_WS_BASE`, and `BINANCE_TESTNET=1`

Never commit API keys or secrets to repository files.

## Data Storage

- `~/binance/memory.md` for preferences and environment mode
- `~/binance/runbooks.md` for proven workflows
- `~/binance/incidents.md` for outage and error history
- `~/binance/snapshots/` for `exchangeInfo` and filter captures

## Core Rules

### 1. Start in Spot Testnet by Default
- Use production only after explicit confirmation in the current conversation.
- Run the same flow in testnet first for every new order or account workflow.

### 2. Enforce Timestamp and Signature Correctness
- Sync server time before signed calls and keep `recvWindow` realistic.
- Sort params before signing and include every signed field in the canonical string.

### 3. Validate Symbol Filters Before Creating Orders
- Read symbol filters from `exchangeInfo` and enforce `PRICE_FILTER`, `LOT_SIZE`, and `MIN_NOTIONAL`.
- Reject order payloads locally before sending requests that will fail.

### 4. Use Test Order Before Real Order
- For every new payload shape, call `POST /api/v3/order/test` first.
- Promote to `POST /api/v3/order` only when payload and filters are confirmed.

### 5. Reconcile Every Order Through User Events
- Treat placement response as provisional when network quality is poor.
- Confirm final state through `executionReport` events and REST queries.

### 6. Respect Rate Limits and Back Off Fast
- Parse `rateLimits` in responses and throttle proactively.
- On `429` or `418`, pause, back off exponentially, and avoid hammering retries.

### 7. Keep Scope Tight and Transparent
- Use only declared Binance endpoints and symbols requested by the user.
- Never modify this skill or unrelated local files.

## Binance Traps

- Using local clock drifted by seconds causes `-1021` and fake auth failures.
- Reusing old signatures after changing params causes `-1022`.
- Sending quantity not aligned to `stepSize` fails despite valid account balance.
- Assuming order status from placement response misses partial fills and cancels.
- Opening long-lived market data sockets past 24h leads to silent disconnect behavior.
- Ignoring `429` weight responses can trigger temporary automated bans.

## External Endpoints

Only official Binance API surfaces below are used by this skill.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://api.binance.com` and `https://api-gcp.binance.com` | Signed trade/account params, market query params | Spot REST production |
| `https://api1.binance.com` to `https://api4.binance.com` | Same as Spot REST | Alternative production REST hosts |
| `https://data-api.binance.vision` | Public market data params only | Spot public market data |
| `wss://stream.binance.com:9443` and `wss://stream.binance.com:443` | Stream subscribe payloads and listenKey stream data | Spot market/user streams |
| `wss://data-stream.binance.vision` | Market stream subscriptions only | Public market streams |
| `wss://ws-api.binance.com:443/ws-api/v3` | WS API signed and unsigned request payloads | Spot WebSocket API |
| `https://testnet.binance.vision`, `wss://stream.testnet.binance.vision`, `wss://ws-api.testnet.binance.vision/ws-api/v3` | Test order/account payloads | Spot testnet validation |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- API key identifier and signed params for account and trading endpoints
- Requested symbols, intervals, and market stream subscriptions

**Data that stays local:**
- Operational memory and incident logs in `~/binance/`
- Local helper scripts and runbooks created during sessions

**This skill does NOT:**
- Send data to undeclared services
- Place production orders without explicit confirmation
- Store API secrets in repository files
- Modify this skill definition file

## Trust

By using this skill, request data is sent to Binance infrastructure.
Only install if you trust Binance with your operational trading metadata.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` - Build and debug robust HTTP API request workflows
- `auth` - Handle API auth models, signatures, and credential safety
- `bash` - Automate shell workflows with safer command composition
- `bitcoin` - Add BTC domain context when analyzing crypto execution

## Feedback

- If useful: `clawhub star binance`
- Stay updated: `clawhub sync`
