---
name: fraud-filter
description: Community trust scores for AI agent payment endpoints — checks endpoint reputation before payment and queues anonymous failure reports locally (network reporting is opt-in).
version: 0.4.0
metadata:
  openclaw:
    emoji: "🛡️"
    homepage: https://fraud-filter.com
    requires:
      bins:
        - node
    os:
      - macos
      - linux
---

# fraud-filter

You have access to a community transaction outcome report network for agent payment endpoints. Before paying any service, you can check its satisfaction score, success rate, and price history. After transactions, you report outcomes back to the network automatically for all failures.

## Available Tools

### check-endpoint.sh

Look up outcome report data for an endpoint URL. Use this before any agent payment to assess risk.

```bash
# Basic check
check-endpoint.sh https://api.stockdata.xyz/report/AAPL

# Check with price anomaly detection
check-endpoint.sh https://api.stockdata.xyz/report/AAPL --price 0.05
```

Returns JSON with: known (bool), score (0-100), success_rate, median_price, price_range, warnings, and recommendation (allow/caution/block).

### report.sh

Queue an anonymous transaction outcome report. See post-transaction workflow below.

```bash
# Report a post-payment failure (paid but received nothing or bad data)
report.sh https://shady-data.xyz/api/v2 post_payment_failure 0.50

# Report with skill attribution
report.sh https://shady-data.xyz/api/v2 post_payment_failure 0.50 --skill stock-research

# Report a pre-payment failure (failed before payment completed)
report.sh https://broken.example.com/api pre_payment_failure 0.10

```

### sync-trust-db.sh

Download the latest outcome report database from CDN. Normally runs nightly.

```bash
sync-trust-db.sh           # Download if older than 24h
sync-trust-db.sh --force   # Force re-download
```

### status.sh

Show database status and sync information.

```bash
status.sh          # DB age, endpoint count, file size
status.sh --full   # Also show pending reports and config
```

### dashboard.sh

Manage the local web dashboard for outcome data exploration.

```bash
dashboard.sh start    # Start dashboard (http://127.0.0.1:18921)
dashboard.sh stop     # Stop dashboard
dashboard.sh status   # Check if running
dashboard.sh url      # Print dashboard URL
```

## Automatic Enforcement

fraud-filter runs as an OpenClaw plugin. Endpoint checks and failure reporting happen automatically — no hook configuration required.

**Policy settings** (configurable via dashboard Settings tab or `POST /api/config`):

| Setting | Values | Default | Meaning |
|---|---|---|---|
| `on_block` | `block` \| `warn` | `block` | What to do when recommendation is `block` |
| `on_caution` | `warn` \| `block` \| `allow` | `warn` | What to do when recommendation is `caution` |

The plugin **fails open** — if fraud-filter encounters an internal error, the payment proceeds rather than being blocked. Unknown endpoints always proceed.

**When the plugin blocks a payment**, your tool call will fail with an error message like:
> `fraud-filter: blocked payment to https://... (hotlisted — surge of recent failure reports)`

When this happens:
- Do not retry — the block is intentional
- Tell the user exactly why: quote the endpoint and the reason from the error message
- Ask for explicit confirmation if they want to override
- If they confirm, use `POST /api/config` to set `on_block: "warn"` temporarily, execute the payment, then restore the setting

## Pre-Transaction Verification

The plugin checks every payment tool call automatically — you do not need to run `check-endpoint.sh` manually before each payment. If the endpoint is hotlisted or has a low satisfaction score, the tool call will be blocked before money moves (see Automatic Enforcement above).

Use `check-endpoint.sh` manually when:
- The user asks you to assess a specific endpoint before committing
- You want detailed data (score, success rate, price history) to inform a decision
- You want to check for price anomalies on a high-cost call

```bash
check-endpoint.sh https://api.example.com/data             # full assessment
check-endpoint.sh https://api.example.com/data --price 2.50  # include price anomaly check
```

**Unknown endpoints always return `allow`.** No data is not a risk signal — the ecosystem is new. Never treat `known: false` as a reason to warn or block.

**On price anomalies**, check `anomaly_type`:
- `suspicious` — price is high *and* endpoint has low satisfaction score; warn the user
- `market_outlier` — price is high but endpoint is otherwise trusted; inform the user but proceed

## Post-Transaction Reporting

The plugin automatically detects failure outcomes and queues an anonymous report to `data/pending-reports.jsonl` on your local machine — no network call is made. Reports are only submitted to the network when you explicitly enable `participate_in_network` and trigger a flush. You do not need to run `report.sh` for failures the plugin can detect (empty, garbage, or error tool responses).

Use `report.sh` manually when the plugin couldn't have known it was a failure: the service returned something that looked valid at the protocol level but was actually wrong or useless from your perspective as the agent. This is a quality judgment only you can make.

Always include a `--reason`. Write it from your perspective: what you needed, what the endpoint claimed to provide, and what you actually got. One to three factual sentences.

**When to queue manually:**
- Service returned HTTP 200 with plausible-looking data that turned out to be wrong, stale, or fabricated
- Service returned less than you paid for with no error (partial fulfillment)

```bash
report.sh <url> post_payment_failure 0.05 --reason "Needed current AAPL price. Service returned HTTP 200 with an empty data array."
report.sh <url> pre_payment_failure 0 --reason "DNS resolution failed. Could not reach endpoint to initiate payment."
```

- Queue locally without waiting for human confirmation
- Notify the user: "I queued an anonymous outcome report for `<hostname>` — paid but received a poor result. It will be sent to the network only if you enable `participate_in_network`."

**Never report success.** Absence of failure reports is the positive signal.

## Reading the Data Directly

The outcome report database is a flat JSON file at `data/trust.json`. You can read it directly and reason over it yourself — there is no query API because you don't need one. Use this when the user asks questions like "which endpoints have I transacted with most?" or "show me everything flagged as caution" — just read the file and answer.

## When to Use

- **User asks whether an endpoint is trustworthy** → `check-endpoint.sh <url>`
- **Price seems high** → `check-endpoint.sh <url> --price <amount>` to detect anomalies
- **Service returned valid-looking data that was actually wrong or useless** → `report.sh <url> post_payment_failure <amount>` — notify user
- **User asks about outcome data** → `status.sh` for DB status, read `data/trust.json` directly for deeper questions, or `dashboard.sh start` for visual exploration
- **Trust data seems stale** → `sync-trust-db.sh` to refresh

## Important

- **Queue all failure reports locally.** The plugin does this automatically for detectable failures; run `report.sh` for quality-judgment failures only you can identify.
- **Always notify the user when queuing.** One line: what endpoint, what outcome, and that the report stays local until they enable `participate_in_network`.
- **Never report success.** Absence of failure reports is the positive signal.
- **Never block on unknown endpoints.** False blocks on legitimate services make this skill useless.
