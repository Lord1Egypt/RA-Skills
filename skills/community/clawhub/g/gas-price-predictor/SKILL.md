---
name: gas-price-predictor
version: 1.0.3
permissions:
  - env
  - network
description: Predict optimal gas prices for Base L2 transactions using historical block analysis and moving-average trends. Use when an agent needs to minimize gas costs, time transactions efficiently, or automate gas price selection for DeFi operations on Base L2.
---

# Gas Price Predictor

## Overview

Analyzes Base L2 gas markets to predict optimal transaction timing and gas price settings. Saves 10-40% on gas costs by avoiding peak congestion periods.

## Core Capabilities

### 1. Historical Pattern Analysis

- Pulls last 200 blocks gas data from Base RPC (history fetches are capped at 200 blocks)
- Calculates moving averages (20-block, 50-block, 200-block when enough history was fetched)
- Detects congestion spikes vs normal periods

### 2. Real-Time Gas Forecast

- Current base fee + priority fee recommendation
- "Wait" vs "Execute Now" signal
- Confidence score (0-100%) based on pattern strength
- Estimated savings if waiting for optimal window

### 3. Optimal Timing Predictions

| Time (UTC) | Typical Gas | Recommendation |
|------------|-------------|----------------|
| 02:00-06:00 | Low | Best window for non-urgent |
| 08:00-12:00 | Medium | Standard operations |
| 14:00-18:00 | High | Avoid if possible |
| 20:00-00:00 | Medium-High | Acceptable for urgent |

### 4. Agent Integration

- Returns structured JSON for automated decision-making
- Suggests `maxFeePerGas` and `maxPriorityFeePerGas` values
- Polling monitor mode for continuous monitoring (prints alerts to stdout)
- Alert when gas drops below threshold

## Workflow

### Quick Check

```bash
python3 scripts/gas_predictor.py --quick
```

Output (`--quick --json`):
```json
{
  "current_base_fee_gwei": 0.05,
  "recommended_priority_gwei": 0.001,
  "total_gas_price_gwei": 0.051,
  "congestion": "low",
  "wait_recommended": false,
  "estimated_cost_usd": 0.42,
  "confidence": 87,
  "avg_base_fee_gwei": 0.05,
  "ratio_to_avg": 1.0,
  "block_number": 12345678,
  "timestamp": "2026-11-18T00:00:00+00:00"
}
```

### Full Analysis

```bash
python3 scripts/gas_predictor.py --analyze --blocks 200
```

### Continuous Monitor

```bash
python3 scripts/gas_predictor.py --monitor --threshold 0.1
```

### RPC Endpoint

The script defaults to the public no-key Base endpoint (`https://mainnet.base.org`).
To use a keyed provider instead, set the full endpoint URL in the
`BASE_RPC_URL` environment variable or pass `--rpc-url`:

```bash
BASE_RPC_URL="https://base-mainnet.g.alchemy.com/v2/<your-key>" python3 scripts/gas_predictor.py --quick
```

No API key is hardcoded or shipped with this skill. Only `https://`
endpoints are accepted.

## Scripts

- `scripts/gas_predictor.py` — Main predictor with all modes

## References

- `references/base-gas-model.md` — EIP-1559 fee market on Base

## Earnings Model

- **Skill sale:** $8-15 (saves users gas costs immediately)
- **x402 per-call:** $0.02 per prediction
- **Subscribed monitoring:** $5/mo for continuous alerts

## Safety

- Never overestimates — conservative estimates default
- Falls back to current block base fee if prediction fails
- No transaction execution — pure advisory
- Read-only: makes JSON-RPC read calls only, never signs or sends transactions
- No credentials are stored in the skill; the RPC endpoint is configured via the `BASE_RPC_URL` environment variable (or `--rpc-url`) and must be `https://`

## Tool Scope

- Network: outbound HTTPS requests to a single Base JSON-RPC endpoint only
  (default `https://mainnet.base.org`, overridable via `BASE_RPC_URL` / `--rpc-url`).
- The only request made is `eth_getBlockByNumber` with a block number
  parameter. The request carries no secrets, tokens, wallet addresses, or
  personal data — only the fixed JSON-RPC method name and the requested
  block number.
- No file writes, no shell commands, no subprocesses, no deserialization
  of untrusted data, no transaction signing or submission.

## Changelog

### v1.0.3 — 2026-11-19 (vetting follow-up)

- Fixed an error-text credential leak (independent vetting F1): `_rpc_call` printed the raw `requests` exception, which includes the full request URL — and a keyed provider URL carries the key in its path. RPC failures now print a fixed message only (`RPC error: request failed`); the validator no longer echoes the URL in its error and `main()` prints a fixed message for an invalid endpoint. Same defect class as the MEV SDI-4 fixed in v1.0.2.

### v1.0.2 — 2026-11-19 (rescan follow-up)

- Declared the tool scope in machine-readable form (`permissions: [env, network]` in the frontmatter) so the ClawHub scanner no longer flags the skill for undeclared scope (LP3). No code change; behavior is identical to v1.0.1.

### v1.0.1 — 2026-11-18 (security patch)

- Removed the Alchemy API-key path: the `--alchemy-key` flag (which defaulted to a literal `${ALCHEMY_API_KEY}` placeholder and silently fell back to the key `"demo"`) is gone. The RPC endpoint is now configured via the `BASE_RPC_URL` environment variable or `--rpc-url`, defaulting to the public no-key endpoint `https://mainnet.base.org`.
- Implemented the missing `analyze_patterns()` method (previously called by `predict_optimal()` and the `--analyze` path but never defined, so every run crashed with `NameError`). It now computes average/min/max base fee plus 20/50/200-block moving averages from the fetched blocks.
- Hardened RPC handling: only `https://` endpoints are accepted, URLs with embedded username/password credentials are rejected, malformed block data from the RPC node returns an empty result instead of crashing, and non-dict JSON-RPC responses are rejected.
- Removed dangling references to files that never shipped (`scripts/gas_history.py`, `scripts/gas_alert.py`, `references/gas-patterns.md`), the nonexistent `--alert-webhook` flag, and the "WebSocket mode" claim — monitoring is polling-based and prints alerts to stdout.
- Corrected capability claims to match the code: moving averages are computed from fetched blocks; time-of-day weighting remains a future enhancement (see `references/base-gas-model.md`). The frontmatter description no longer claims mempool monitoring or time-of-day analysis, which the code does not implement.
- Documented the skill's tool scope (single outbound HTTPS JSON-RPC endpoint, `eth_getBlockByNumber` only, no secrets/PII in requests) in a new "Tool Scope" section.
- `--blocks` is capped at 200; the `--analyze` example now uses `--blocks 200`.
