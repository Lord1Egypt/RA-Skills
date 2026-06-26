# Quick Start — game-ops-monitor

5-minute setup guide to get game server monitoring working.

---

## Prerequisites

- Scouter Collector deployed and running
- Game servers have Java Agent loaded
- `curl` and `jq` available on the system running this skill

---

## Step 1: Verify Collector

```bash
# Replace with your Collector IP
export SCOUTER_COLLECTOR_URL=http://<collector-ip>:6188

# Health check
curl -s "${SCOUTER_COLLECTOR_URL}/scouter/v1/status"
# Expected: {"status":"ok"}
```

If this fails, deploy Scouter first. See `references/scouter-deploy-guide.md`.

---

## Step 2: Verify Agent Registration

```bash
# Count registered game servers
curl -s "${SCOUTER_COLLECTOR_URL}/scouter/v1/objects?type=Java" | jq length

# Expected: number > 0 (your game process count)
```

---

## Step 3: Query Your First Metrics

```bash
# Quick TPS check
curl -s "${SCOUTER_COLLECTOR_URL}/scouter/v1/objects?type=Java" | \
  jq -r '.[0] | "Server: \(.objName), Hash: \(.objHash)"'

# Replace HASH with actual hash from above, then:
curl -s "${SCOUTER_COLLECTOR_URL}/scouter/v1/object/HASH/counter/tps"
# TPS = value / 1000
```

---

## Step 4: Configure Alerting

See `references/alert-workflow.md` for alert setup.

---

## Common Commands

| What you want | What to say |
|---------------|-------------|
| Check all TPS | `"各服 TPS 怎么样"` |
| Single server | `"帮我看看 xy_s11649"` |
| Online users | `"现在有多少人在线"` |
| Memory check | `"各服内存"` |
| Performance report | `"生成今天各服报表"` |
| Alert check | `"哪几服告警了"` |

---

## Troubleshooting

| Problem | Solution |
|---------|---------|
| `Connection refused` | Check Collector is running and IP is correct |
| `[]` empty result | Agents not registered yet; wait 30s after server start |
| TPS always 0 | Server has no activity, or sampling rate is 0 |
| Value > heap_max | Normal during GC; not an error |
