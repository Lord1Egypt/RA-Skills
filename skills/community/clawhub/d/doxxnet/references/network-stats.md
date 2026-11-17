# doxx.net Network Stats

> **Live schema first.** The doxx.net Config API is agent-descriptive. Fetch `https://config.doxx.net/` for the current manifest (every endpoint, params, returns, auth, side effects): this file is a snapshot. Every POST response also includes a `context` field with per-endpoint docs.

You help users view detailed bandwidth, security alert, and threat statistics for their doxx.net network.


## API convention

**Auth token -- never enters the AI conversation.**

The token is passed to `curl` via shell expansion, so its plaintext value stays on your machine. Two sources, checked in this order:

1. `$DOXXNET_TOKEN` env var (preferred): user exports it before launching the agent.
2. `~/.config/doxxnet/token` file: used automatically if the env var is unset.

curl commands below use `${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}`, so both work transparently. The shell expands the value at exec time -- the plaintext is never emitted in a tool call to the LLM.

**Config API**: POST to `https://config.doxx.net/v1/`:
```
curl -s -X POST https://config.doxx.net/v1/ -d "ENDPOINT=1&param=value&token=${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}"
```

**Stats API**: POST to `https://secure-wss.doxx.net/api/stats/` with `X-Auth-Token` header:
```
curl -s -X POST https://secure-wss.doxx.net/api/stats/ENDPOINT -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "param=value"
```

## Stats API endpoints

### bandwidth
Bandwidth usage over time. Auto-selects granularity based on time range.
```
curl -s -X POST https://secure-wss.doxx.net/api/stats/bandwidth -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "start=ISO8601&end=ISO8601"
```
Optional params: `tunnel_token` (filter to one tunnel), `start`, `end` (ISO 8601).

Auto-granularity: 1s (<5m), 1m (<6h), 5m (<48h), 1h (<30d), 6h (30d+).

Returns: `data[]` with `tunnel_token`, `timestamp`, `peak_in` (Mbps), `peak_out` (Mbps), `samples`. Also `aggregate[]` for combined totals.

### alerts
Security alerts and DNS blocks.
```
curl -s -X POST https://secure-wss.doxx.net/api/stats/alerts -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "last=1d"
```
Optional params: `tunnel_token`, `last` (session/1m/1h/1d/7d/30d), `start`/`end` (ISO 8601), `type` (filter by event type).

Returns: `totals` (counts by type), `block_count`, `category_counts` (ads, tracking, malware, etc.), `data[]` with individual events.

### summary
Peak bandwidth and alert totals for a period.
```
curl -s -X POST https://secure-wss.doxx.net/api/stats/summary -H "X-Auth-Token: ${DOXXNET_TOKEN:-$(cat ~/.config/doxxnet/token)}" -d "days=30"
```
Optional: `tunnel_token`, `days` (default: 30).

Returns: per-tunnel `peak_in_mbps`, `peak_out_mbps` + `alert_totals` by type.

### global (no auth)
Global threat counter across all doxx.net users.
```
curl -s "https://secure-wss.doxx.net/api/stats/global"
```
Returns: `total` (cumulative threats blocked), `ts`.

## Config API endpoints (for context)

- `list_tunnels`: list tunnels with IPs and connection status (useful for identifying tunnel_tokens)

## Alert types

| Type | Description |
|------|-------------|
| `dns_block` | Domain blocked by DNS blocklist |
| `security_event` | Dangerous port access, spoofing, leaks |
| `dangerous_port` | Connection to known dangerous port |
| `dns_bypass` | DNS bypass attempt detected |
| `doh_bypass` | DoH/DoT bypass detected |
| `port_scan` | Port scanning activity |
| `dns_nxdomain` | Non-existent domain query |

## Alert categories (for DNS blocks)

`ads`, `tracking`, `malware`, `security`, `other`

## Common requests

**"Full overview" / "Show me everything":** Call all four endpoints -- global (total threats), bandwidth (last hour), alerts (last 24h with category breakdown), and summary (7-day peaks). Present as a concise dashboard table.

**"Show my bandwidth":** Call bandwidth endpoint with last hour, present per-tunnel and aggregate in Mbps.

**"What's being blocked?":** Call alerts with `last=1d`, focus on `category_counts` and `block_count`.

**"Show security alerts":** Call alerts with `type=security_event` or no type filter, highlight `dangerous_port` and `port_scan`.

**"Give me a summary":** Call summary with `days=30`, show peak bandwidth per tunnel and alert totals.

**"How many threats has doxx blocked?":** Call global endpoint, format the total.

## Time range shortcuts

When users say informal time ranges, map them:
- "today" / "last hour" → `last=1h`
- "today" / "past day" → `last=1d`
- "this week" → `last=7d`
- "this month" → `last=30d`
- Specific range → use `start` and `end` with ISO 8601

## Guidelines

- Present data in clear tables or structured summaries
- Convert bandwidth to human-readable units (Mbps for throughput, GB for totals)
- Group alerts by category and highlight unusual patterns
- When showing bandwidth, include both per-tunnel and aggregate views
- For alert summaries, show the top blocked categories and any security events
- If user has multiple tunnels, offer to filter by specific tunnel or show all
- Call `list_tunnels` first if you need tunnel names to label data
