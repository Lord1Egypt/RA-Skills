---
name: flowtriq-monitor
description: >
  Monitor and manage Flowtriq DDoS detection in real time using the Flowtriq
  API. Use this skill whenever the user asks about active attacks, node status,
  incident history, traffic metrics, PCAP captures, agent config, or mitigation
  status on their Flowtriq-monitored infrastructure. Triggers on phrases like
  "check my nodes", "any attacks", "what's hitting my server", "show incidents",
  "is anything under attack", "flowtriq status", "check traffic", "pull my
  incidents", or any mention of Flowtriq combined with monitoring, alerts,
  status, or traffic. Requires FLOWTRIQ_API_KEY and FLOWTRIQ_NODE_UUID env vars.
metadata:
  openclaw:
    requires:
      env:
        - FLOWTRIQ_API_KEY
        - FLOWTRIQ_NODE_UUID
---

# Flowtriq Monitor Skill

This skill lets you monitor your Flowtriq-protected infrastructure directly
from your OpenClaw agent. Ask natural language questions and the agent will
query the Flowtriq API and interpret the results for you.

**Base URL:** `https://flowtriq.com`
**Auth headers required on all agent endpoints:**
```
Authorization: Bearer $FLOWTRIQ_API_KEY
X-Node-UUID: $FLOWTRIQ_NODE_UUID
```

---

## What You Can Ask

- "Are any of my nodes under attack right now?"
- "What's the current traffic on my server?"
- "Show me recent incidents"
- "What was the peak PPS in the last attack?"
- "Is my agent online?"
- "Pull my node config and thresholds"
- "Any IOC matches recently?"

---

## API Calls Reference

### Check Agent Health / Node Status
```
GET https://flowtriq.com/api/health
```
No auth needed. Returns `{ "status": "ok" }`. Use this first to confirm
the Flowtriq platform is reachable before making authenticated calls.

---

### Get Node Config + Current Thresholds
```
GET https://flowtriq.com/api/v1/agent/config
Headers: Authorization + X-Node-UUID
```
Returns the node's current PPS threshold, baseline stats (p99, mean),
loaded IOC patterns, and any pending commands queued for the agent.

Key fields to surface to the user:
- `pps_threshold` — what PPS level triggers an incident
- `baseline.p99_pps` — the node's normal p99 traffic level
- `baseline.mean_pps` — average baseline
- `ioc_patterns` — count how many are loaded
- `pending_commands` — flag any that exist, user may want to review

---

### Get Latest Metrics (Current Traffic)
```
POST https://flowtriq.com/api/v1/agent/metrics
Headers: Authorization + X-Node-UUID
```
The agent POSTs metrics to this endpoint every second. To read current
traffic state, use the dashboard API. Since the dashboard endpoints require
session auth, instruct the user to check `https://flowtriq.com/dashboard`
for a live view, or pull from config endpoint for baseline context.

---

### Submit / Check Incidents
```
POST https://flowtriq.com/api/v1/agent/incident
Headers: Authorization + X-Node-UUID
```
The agent uses this to open and update incidents. When interpreting incident
data returned or confirmed by the user, extract and explain:

| Field | What to tell the user |
|---|---|
| `attack_family` | Plain English: "UDP flood", "SYN flood", etc. |
| `severity` | Low / Medium / High / Critical |
| `peak_pps` | "peaked at X packets per second" |
| `peak_bps` | Convert to Gbps/Mbps for readability |
| `source_ip_count` | "came from X unique source IPs" |
| `geo_breakdown` | Top countries by volume |
| `ioc_matches` | Named botnet/pattern matches |
| `spoofing_detected` | Warn user if true |
| `botnet_detected` | Warn user if true |

**Attack family plain-English map:**
- `udp_flood` = UDP Flood
- `syn_flood` = SYN Flood
- `http_flood` = HTTP Flood
- `icmp_flood` = ICMP/Ping Flood
- `dns_flood` = DNS Amplification
- `multi_vector` = Multi-Vector (combined attack types)
- `unknown` = Unclassified

**Severity guidance:**
- `low` = below 2x baseline, informational
- `medium` = 2-5x baseline, monitor closely
- `high` = 5-20x baseline, mitigation likely active
- `critical` = 20x+ baseline, full response mode

---

### Register a New Node (if user asks)
```
POST https://flowtriq.com/api/deploy
Headers: Authorization: Bearer YOUR_DEPLOY_TOKEN
Body: { "name": "node-name", "ip": "x.x.x.x" }
```
Note: this uses a **deploy token** not the node API key. The user must
provide their deploy token separately. Returns a new `node_uuid` and
`api_key` for the registered node.

---

## Interpreting Results for the User

Always translate raw API data into plain NOC-style summaries. Example patterns:

**All clear:**
> "Your node is online. Baseline p99 is 12,000 PPS, threshold set at
> 50,000 PPS. No active incidents. 8 IOC patterns loaded."

**Active attack:**
> "Active incident on [node]. SYN flood, critical severity. Peaked at
> 47,821 PPS (1.7 Gbps). 3,241 source IPs, spoofing detected. IOC match:
> mirai-variant (94% confidence). Mitigation should be active — check your
> dashboard for FlowSpec rule status."

**Degraded / agent offline:**
> "The Flowtriq platform is reachable but your node hasn't sent a heartbeat
> recently. Your agent may be down. Run `sudo systemctl status ftagent` on
> the server to check."

---

## Error Handling

| HTTP | Meaning | Tell the user |
|---|---|---|
| 401 | Bad API key | "Your API key looks wrong or expired. Rotate it in the Flowtriq dashboard." |
| 402 | Payment issue | "Your Flowtriq subscription may have lapsed. Check billing." |
| 409 | Duplicate node name | "A node with that name already exists in your workspace." |
| 400 | Missing fields | Show which fields are missing and ask user to provide them |
| 5xx | Platform error | "Flowtriq returned a server error. Check https://flowtriq.com/status for outages." |

---

## Setup Reminder (if user hasn't configured env vars)

If `FLOWTRIQ_API_KEY` or `FLOWTRIQ_NODE_UUID` are missing, tell the user:

> "To use this skill you need two environment variables set in OpenClaw:
> - `FLOWTRIQ_API_KEY` — find this in your Flowtriq dashboard under
>   Settings > API Keys
> - `FLOWTRIQ_NODE_UUID` — find this on your node's settings page
>
> Add them to your OpenClaw env config and reload the agent."

---

## Reference Files

- `references/attack-types.md` — detailed breakdown of all 8 attack
  families, what causes them, and recommended responses
- `references/api-endpoints.md` — full endpoint reference with all
  parameters for quick lookup during complex tasks
