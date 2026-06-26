# fraud-filter — Technical Architecture

## Design Decisions

### Zero dependencies

Like spend-ledger, fraud-filter uses only Node.js built-in modules. No npm packages. This eliminates supply chain risk and keeps the skill self-contained.

### Localhost-only binding

The dashboard server binds to `127.0.0.1`, never `0.0.0.0`. Security through network isolation — only local processes can access the API.

### Unknown endpoints return `allow`, not `caution`

An endpoint with no data in the trust DB gets `recommendation: "allow"`. The payment ecosystem is new; most endpoints will be unknown for a long time. Treating unknown as `caution` would make the skill actively hostile to agent spending and would get it removed. Absence of reports is not evidence of bad behavior — it just means nobody has reported yet.

The hotlist (see below) handles the real-time threat: a brand-new scam endpoint will appear there within hours of the first wave of failure reports, before it ever accumulates enough history for a satisfaction score.

### Hotlist for fast blocking

The nightly trust.json rebuild is too slow to catch exit scams or endpoint compromises that happen intra-day. A separate `hotlist.json` is computed dynamically from the last 24 hours of signals: any endpoint with ≥ 3 unique reporters flagging it as failed gets added. Skills fetch this hourly and check it before the trust DB lookup. A hotlist match returns `recommendation: "block"` immediately, regardless of any stored satisfaction score.

The hotlist is intentionally aggressive — it's a tripwire for sudden surges, not a nuanced score. False positives are possible (a flaky endpoint during an outage), but a temporary block is less harmful than an undetected scam.

The hotlist is fetched on plugin startup and refreshed hourly. This is a **download only** — no user data is sent. The request carries only a `User-Agent: fraud-filter-skill/1.0` header; the response is the same public file served to every client. To disable automatic hotlist syncing (e.g., in an air-gapped or fully offline environment), set `sync_hotlist: false` in `data/config.json`. Endpoint hash lookups will continue to work against the last cached `data/hotlist.json`.

### Nightly sync, not real-time

Satisfaction scores update daily, not per-transaction. This is intentional:

1. **Privacy**: Prevents the server from learning transaction patterns ("agent X checked endpoint Y at 3:47pm")
2. **Simplicity**: A static JSON file on CDN is simpler than a real-time query API
3. **Sufficiency**: Service quality doesn't change minute-to-minute

### URL hashing

Endpoint URLs are SHA-256 hashed in the trust database and signals. The `url_hint` field contains only the hostname. This prevents the trust database from becoming a directory of every paid API endpoint on the internet.

### Price bucketing

Exact transaction amounts are bucketed into ranges before reporting. A $0.05 transaction becomes `0.01-0.10`. This preserves enough signal for price anomaly detection without revealing exact spending.

### Two-phase reporting: queue vs. submit

All reporting follows a strict two-phase model. The two phases are independent and controlled by separate mechanisms.

**Phase 1 — Queue (always local, no network)**
When the plugin detects a payment failure via `tool_result_persist`, it calls `queueReport()`, which appends an anonymous signal to `data/pending-reports.jsonl` (mode `0600`). No network connection is made in this phase. The file never leaves the machine. The agent notifies the user that a report was queued.

**Phase 2 — Submit (opt-in network, triggered explicitly)**
`submitPendingReports()` checks `participate_in_network` at the top of the function before doing anything else. With the default `participate_in_network: false`, it returns immediately with `{ reason: "network_participation_disabled" }` — no data leaves the machine. With `participate_in_network: true`, a flush is triggered by the user (or the agent at the user's direction) via `POST /api/reports/flush` or `report.sh --flush`. There is no automatic submission timer.

### Reporting policy by outcome type

For negative outcomes, the plugin always queues a local signal automatically:

- **post_payment_failure**: Queued locally without confirmation — paid and received nothing is unambiguous. Submission to the network requires explicit opt-in.
- **pre_payment_failure**: Queued locally. Technical false positives (timeouts, misconfigured agents) are filtered downstream by deduplication and the 3-reporter hotlist threshold.

With `participate_in_network: false` (the default), failure reports accumulate in `data/pending-reports.jsonl` for local review and are never sent anywhere. The user decides when and whether to submit.

## Data Model

### Outcome Report Database (`trust.json`)

Flat JSON keyed by SHA-256 hash of normalized endpoint URL. See `references/signal-format.md` for full schema.

Key properties per endpoint:
- `report_count`, `success_rate`: Aggregate outcome data
- `median_price_usd`, `price_p10_usd`, `price_p90_usd`: Price distribution
- `first_seen`, `last_success`, `last_failure`: Timeline
- `failure_types`: Breakdown by `post_payment` vs `pre_payment`
- `warnings`: Derived flags (high_failure_rate, volatile_pricing, etc.)
- `score`: Composite satisfaction score 0-100

### Pending Reports (`pending-reports.jsonl`)

Append-only JSONL file. Each line is a signal with status tracking:
- `pending`: Queued, not yet sent
- `sent`: Successfully submitted to reporting endpoint
- `failed`: Submission failed (will retry on next flush)

Sent reports older than 7 days are pruned automatically.

### Configuration (`config.json`)

Generated on first run with a random `install_id` (used only for reporter hash derivation). User-configurable fields:
- `trust_db_url`: CDN URL for trust database
- `report_endpoint`: URL for signal submission
- `sync_interval_hours`: How often to check for updates
- `participate_in_network`: Enable/disable sending signals
- `auto_positive_signals`: Auto-report successful transactions

## Score Calculation

Satisfaction score (0-100) is computed from five weighted factors. Higher means more positive transaction outcomes reported by the community:

| Factor | Range | Description |
|---|---|---|
| Base | 50 | Starting point for any endpoint with reports |
| Success | -40 to +40 | `(success_rate - 0.5) * 80` |
| Volume | 0 to +10 | `min(10, log10(report_count) * 5)` |
| Recency | -20 to 0 | Penalty for failures within 7 days |
| Stability | -10 to 0 | Penalty for volatile pricing (p90/p10 ratio) |
| Age | -15 to 0 | Penalty for endpoints less than 30 days old |

Full formula documented in `references/signal-format.md`.

### Recommendation mapping

| Score | Recommendation |
|---|---|
| 70-100 | `allow` |
| 40-69 | `caution` |
| 0-39 | `block` |
| hotlisted | `block` (overrides score) |
| unknown | `allow` (no outcome reports is not a risk signal) |

## Price Anomaly Types

`checkPriceAnomaly` returns an `anomaly_type` field to distinguish between two cases that require different responses:

| `anomaly_type` | Meaning | Recommended action |
|---|---|---|
| `suspicious` | Price is high *and* endpoint has score < 60 | Warn user; do not auto-proceed |
| `market_outlier` | Price is high but endpoint is otherwise trusted | Inform user; proceed normally |

This prevents blocking a surge-priced but legitimate service (e.g. a high-token-count LLM response) while still flagging anomalous prices on already-questionable endpoints.

## Known Limitations

### ETLD+1 normalization (subdomain bypass)

URL normalization currently hashes the full path after stripping query params and fragments. A bad actor could register multiple subdomains (`api-v1.bad.com`, `api-v2.bad.com`) to avoid a trust score tied to a specific URL. Correct defense requires ETLD+1 (registrable domain) normalization using a Public Suffix List, which would introduce an external dependency contrary to the zero-dependency design. This is tracked as a future improvement; for now the hotlist provides a faster mitigation path since all subdomains of a compromised provider will generate failure reports quickly.

### Sybil attack resistance (planned for future version)

Anonymous reporting is vulnerable to coordinated false reports against a legitimate service. The current defense is rate limiting (100 signals per reporter hash per day) and requiring 3 unique reporters before hotlisting. A stronger defense — planned for a future version — is to require reports to reference a transaction hash from the reporter's agent-budget log, providing proof of actual payment. This ties reports to real economic activity and makes Sybil attacks expensive rather than just inconvenient.

## API Endpoints

All served on `127.0.0.1:18921` (configurable via `FRAUD_FILTER_PORT`).

### Read endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Dashboard HTML |
| GET | `/api/check?url=<url>` | Trust assessment for a single endpoint |
| GET | `/api/check-price?url=<url>&price=<usd>` | Price anomaly check |
| GET | `/api/search?q=<query>` | Search endpoints by hostname or hash prefix |
| GET | `/api/endpoints?sort=score&order=desc&limit=50` | List all endpoints (paginated) |
| GET | `/api/status` | DB status, pending reports, participation level |
| GET | `/api/reports` | List pending reports |
| GET | `/api/config` | Current configuration (install_id excluded) |

### Write endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/api/reports` | Queue a new anonymous report |
| POST | `/api/reports/flush` | Submit all pending reports to server |
| POST | `/api/reports/prune` | Remove sent reports older than 7 days |
| POST | `/api/config` | Update configuration |

## Security & Privacy

### What fraud-filter NEVER sends

- Individual transaction details (exact amounts, timestamps, services, sessions)
- Wallet addresses or balances
- User identity or API keys
- spend-ledger's transaction log
- Full endpoint URLs (only SHA-256 hashes)

### What fraud-filter sends (only with opt-in)

- Anonymous outcome signals (success/failure + bucketed price range + day)
- Manual reports (human-confirmed, same anonymous format)

### What fraud-filter downloads

- `trust.json` from CDN (public, same file for everyone)
- No cookies, no tracking, no user-specific content

### Reporter privacy

- `reporter_hash` is a one-way hash of the installation ID
- The installation ID is generated locally and never sent to the server
- Deduplication uses the hash: one report per endpoint per installation per day

### File permissions

All data files written with mode `0o600` (owner read/write only).

## Testing

Run tests with:

```bash
npm test
# or
node --test test/test.js
```

Tests cover:
- **trust-db**: URL normalization, hashing, score computation, warning derivation, endpoint lookup, price anomaly detection, configuration, search
- **reporter**: Signal construction, queueing, deduplication, pending status, pruning
- **server API**: Endpoint check, search, report submission, configuration, status

All tests use temporary directories and clean up after themselves.

## Server-Side Components

Hosted at `api.fraud-filter.com` ([github.com/mattpolly/fraud-filter.com](https://github.com/mattpolly/fraud-filter.com)):

### Reporting endpoint

`POST https://api.fraud-filter.com/reports` — Accepts anonymous signals. Validates format, checks rate limits (100 signals per `reporter_hash` per day), inserts into SQLite via `INSERT OR IGNORE` (deduplicates on reporter + endpoint + day).

### Aggregation pipeline

`aggregate.py` runs nightly via cron:
1. Read all signals from SQLite
2. Recompute per-endpoint stats: report count, success rate, price distribution, failure types, score, warnings
3. Atomic write of new `trust.json` (temp file + rename)

### Trust database delivery

`GET https://api.fraud-filter.com/trust.json` — served directly by nginx with `Cache-Control: public, max-age=3600`. Clients sync daily by default.
