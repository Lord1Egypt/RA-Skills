---
name: ddg-site-health-daily
description: >-
  Run a daily site health check for any URL list: audit the page, check the URL's
  reputation, and pull fresh search context, then diff against yesterday. Use when
  monitoring a site you own or one you are evaluating, before a launch, or when a
  reputation change needs an explanation. One script, three paid calls per URL per day.
version: 1.0.0
metadata:
  triggers: |-
    daily site health check
    monitor my site reputation
    site audit plus threat check
    scheduled website check for agents
  kind: workflow
  openclaw:
    requires:
      bins:
        - curl
    envVars:
      - name: DDG_AGENT_ID
        required: false
        description: Stable agent identity sent as X-Agent-Id; enables the metered free tier and keeps calls attributable.
    homepage: https://agents.daedalusdevelopmentgroup.com
    emoji: "🛰"
allowed-tools: Bash, Read, Write
---

# DDG Site Health Daily

A site is not a one-off audit: pages drift, domains get flagged, and search
context changes. This workflow turns three DDG routes into one recurring daily
check that an agent can run unattended and diff day over day.

**Endpoints (all $0.01/call, x402 on Base, USDC):**
`POST /v1/site-audit`, `POST /v1/threat-check`, `POST /v1/web-search` on
`https://agents.daedalusdevelopmentgroup.com`.

**External cost:** $0.01 per call in USDC on Base via x402. The first
25 calls/day per agent identity are free, so the daily loop for up to 8
URLs runs at $0.00. No account or API key is required; the paid path
needs an x402-capable client (any wallet signer).

**First 25 calls/day per agent identity are free** on those routes: send
`X-Agent-Id: <stable-id>` with no payment header and the full result comes back
with a `free_tier` block. After the allowance, the same request returns a 402
whose body carries the upgrade path — attach the x402 payment header and the
identical body goes through. Send `X-DDG-Free-Tier: skip` to be challenged
immediately (use it if your client must always settle).

## Procedure

1. **Pick targets** — one URL per line in `targets.txt`.
2. **Audit the page** (returns a markdown report + `schema_version`):
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/site-audit \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"url":"https://example.com"}' > out/audit.json
   ```
3. **Check reputation** (risk_score, risk_level, threat_signals, trust_signals):
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/threat-check \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"url":"https://example.com"}' > out/threat.json
   ```
4. **Pull context** (structured results, aggregated engines):
   ```bash
   curl -s -X POST https://agents.daedalusdevelopmentgroup.com/v1/web-search \
     -H 'content-type: application/json' -H "X-Agent-Id: $DDG_AGENT_ID" \
     -d '{"query":"example.com complaints OR outage"}' > out/search.json
   ```
5. **Diff against yesterday** — keep `state/YYYY-MM-DD.json`; alert only on
   change (risk_level change, new threat_signal, audit findings count change).
   Silent days are the product; noise is not.
6. **On 402** — read `upgrade_path` in the body, then retry the identical body
   with the x402 payment header (`X-PAYMENT`/`Payment-Signature`) for
   `x402.accepts[0].amount`. Do not change the body between the free attempt and
   the paid retry.
7. **Schedule** — one run per day per URL; a 10-URL fleet is 30 calls/day
   (≈$0.30/day once past the free allowance).

## Cost math

| Items | Calls/day | Free allowance covers | Paid/day |
|---|---|---|---|
| 1 URL | 3 | yes (25/day) | $0.00 |
| 5 URLs | 15 | yes | $0.00 |
| 10 URLs | 30 | 25 of 30 | $0.05 |

## Failure handling

- `503` = the route's backend is temporarily unavailable; the edge charges
  nothing and the body says so. Retry with backoff; do not pay against a 503.
- `422` = the body is wrong (`url` missing/malformed). Fix the body; no unit is
  consumed by an invalid body.
- `429` = rate limited; respect `retry-after`.

## Not for

- Not for auditing an API or MCP server surface — use a tool/security sweep
  workflow instead (`/v1/mcp-tool-security-audit`, `/v1/prompt-injection-scan`).
- Not for human-facing, client-ready audit reports (that is the reviewed audit
  SKU), and not for continuous per-request monitoring (this is a daily cadence).
- Not for targets you are not authorised to probe: the audit is read-only, but
  reputation checks hit third-party feeds.

## Example

**Ask:** "Check my three marketing sites every morning and tell me if anything
changes in the audit or reputation."

**Before:** a weekly manual audit, reputation problems discovered by a customer
complaint, no history to compare against.

**After:** a daily `state/*.json` history plus a one-line diff alert; three URLs
cost nothing while inside the free allowance, and the paid path is a 402 away
with the exact amount and body already known.

## Version

1.0.0 — initial workflow bundle: site-audit + threat-check + web-search daily
loop with free-tier first calls, 402 upgrade handling and diff-based alerting.
