---
name: mcp-server-registry
description: Trending/new/changed MCP servers + live x402 services — a freshness-ranked, liveness-probed index with an x402-paid change-data API
metadata:
  openclaw:
    requires:
      bins:
        - curl
homepage: https://fresh-feeds.foomworks.workers.dev
license: MIT
---

# MCP Server Registry & x402 Service Discovery (fresh-feeds)

Use this skill to track **trending, new, and changed MCP servers** and to **discover live
x402-payable services** — and to find, rank, or verify a specific MCP server. The registry is
deduplicated and **quality-scored**, the x402 catalog is **liveness-probed**, and both refresh
every 30 minutes; a paid **`changes` API** returns exactly what was added/removed/re-scored since
any day. You get current, ranked, machine-readable data — including the deltas no other index
exposes — instead of crawling raw registries yourself.

Base URL: `https://fresh-feeds.foomworks.workers.dev`

## Use as an MCP server (recommended for agents)
fresh-feeds is a remote **MCP server** (Streamable HTTP, JSON-RPC 2.0) — connect your agent to it
and the tools load natively, no curl required:

- Endpoint: `https://fresh-feeds.foomworks.workers.dev/mcp`
- Free tools (return data directly): `search_mcp_registry`, `get_registry_highlights`,
  `verify_mcp_server`, `list_x402_services`, `feeds_status`
- Paid-access tools (return x402 payment instructions for the full data): `get_mcp_registry_snapshot`,
  `get_registry_changes`, `get_x402_services_snapshot`, `verify_mcp_server_report`

Discovery manifests: `GET /.well-known/agent-card.json` (A2A), `GET /openapi.json` (OpenAPI 3.1),
`GET /.well-known/mcp.json` (MCP descriptor). The REST endpoints below remain available for direct
HTTP/curl use.

## When to use
- "Find a good/maintained MCP server for <capability>"
- "Is MCP server <name> live and trustworthy?" (reachability probe + graded trust signals)
- "What MCP servers were added or changed recently?"
- "Which x402 services are currently up and correctly demanding payment?"

## Free endpoints (no payment)
- `GET /` — human/JSON landing: live **Top 10 by quality score** + **Trending** (send
  `Accept: application/json` for the machine manifest)
- `GET /feeds/mcp-registry/preview` — **top 10 MCP servers by quality score**
- `GET /feeds/x402-services/preview` — top 10 currently-payable x402 services
- `GET /verify/mcp/preview?server=<NAME>` — grade + headline liveness for one server
- `GET /verify/mcp/badge?server=<NAME>` — embeddable SVG trust badge
- `GET /health` — snapshot freshness, data age, available change-baseline dates
- ETag / `If-None-Match` on the paid feeds → `304` (free) to check for new data **before** paying

## Paid endpoints (x402 — USDC on Base, auto-settled)
These return the **full** dataset/report. They respond `HTTP 402 Payment Required` with an x402
challenge; your x402 auto-handler signs a USDC micropayment on Base and retries automatically
(within your configured budget):

| Endpoint | Price | Returns |
|---|---|---|
| `GET /feeds/mcp-registry` | $0.05 | full deduped, quality-scored MCP registry snapshot |
| `GET /feeds/mcp-registry/changes?since=YYYY-MM-DD` | $0.02 | added/removed/score-changed servers since a daily baseline (cheap habit endpoint) |
| `GET /feeds/x402-services` | $0.05 | full x402 services catalog with liveness data |
| `GET /verify/mcp?server=<NAME>` | $0.03 | full verification report: live endpoint probe + graded trust signals |

If you do **not** have an x402 wallet/handler, the free `*/preview` + `/health` endpoints answer
most ranking/liveness questions; use ETag `304` to detect new data without paying.

## Workflow
1. Orient with `GET /feeds/mcp-registry/preview` (free top 10) or the landing `/`.
2. For the full ranked corpus, call `GET /feeds/mcp-registry` (paid). To poll cheaply for
   updates, ETag-check first (`If-None-Match`), then `GET /feeds/mcp-registry/changes?since=`.
3. Before depending on a server, verify it: `GET /verify/mcp/preview?server=` (free grade) →
   `GET /verify/mcp?server=` (paid full report) for the live probe + trust signals.
4. To choose a payable service, use `GET /feeds/x402-services` — `alive-402` means up and
   correctly demanding payment (safe to call); ranking puts payable-now services first.

## Notes
- Quality score = active status + has-remotes + has-packages + real-description + recency
  (see the snapshot's `scoring` field). Liveness reflects a probe, not an SLA.
- The service holds no keys and never initiates payments; all payment is buyer-side via x402.

## Example
```bash
BASE=https://fresh-feeds.foomworks.workers.dev
curl -s "$BASE/feeds/mcp-registry/preview"            # free: top 10
curl -s "$BASE/verify/mcp/preview?server=io.github.example/server"   # free grade
curl -s "$BASE/feeds/mcp-registry"                    # paid (x402 handler settles the 402)
```
