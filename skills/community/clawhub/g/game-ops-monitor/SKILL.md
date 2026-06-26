---
name: game-ops-monitor
description: "Game server real-time monitoring: query TPS, online users, JVM heap from Scouter Collector; detect alerts; send notifications; generate reports. Use when asked to check game server health, monitor TPS, or alert on performance issues."
version: 1.0.0
author: Hermes Agent + GameOps Team
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [curl, jq]
  environment:
    - SCOUTER_COLLECTOR_URL: "Scouter Collector HTTP API base URL (e.g. http://<collector-ip>:6188)"
    - SCOUTER_OBJ_TYPE: "Object type filter for queries (default: Java)"
metadata:
  openclaw:
    tags: [game-ops, monitoring, scouter, tps, jvm, alert, game-server]
    homepage: https://github.com/openclaw/openclaw
    upstream_source: Scouter (https://github.com/scouter-project/scouter)
    requires:
      bins: [curl, jq]
      env:
        - SCOUTER_COLLECTOR_URL
        - SCOUTER_OBJ_TYPE
  hermes:
    tags: [game-ops, monitoring, scouter, tps, jvm, alert, game-server]
    homepage: https://github.com/scouter-project/scouter
    related_skills: [game-alert, scouter-deploy, scouter-troubleshoot, scouter-tuning]
---

# Game Ops Monitor — Real-Time Game Server Monitoring

Query game server JVM performance metrics from Scouter Collector. Supports batch querying of TPS, online users, and memory across thousands of game processes. Designed for large-scale game operations (7000+ processes across 900+ machines).

---

## Overview

This skill provides a unified interface for game operations teams to monitor JVM-based game servers in real-time. It wraps the Scouter Collector's HTTP API and returns human-readable formatted output.

**What it monitors:**
- **TPS** (Transactions Per Second) — game server throughput
- **Online Users** — current active player count
- **JVM Heap** — memory usage and utilization percentage

**Alert thresholds (configurable):**

| Metric | 🔴 Critical | ⚠️ Warning | ✅ OK |
|--------|------------|------------|------|
| TPS | < 100 | 100–300 | > 300 |
| Heap % | > 90% | 75–90% | < 75% |
| Online Users | < 10 (server up but empty) | — | ≥ 10 |

**Scale:** Tested with 7000+ game processes across 900+ physical machines. Single Collector (8-core 16GB) handles this with room to spare.

---

## When to Use

**Triggers (natural language / slash commands):**

- `"各服 TPS 怎么样"` / `"check all server TPS"`
- `"现在各服状态"` / `"game server status"`
- `"帮我看看在线人数"` / `"how many players online"`
- `"各服内存怎么样"` / `"check server memory"`
- `"哪几服 TPS 告警了"` / `"any TPS alerts"`
- `"生成今天各服性能报表"` / `"generate performance report"`
- `"帮我看看 xy_s11649 的状态"` / `"check server xy_s11649"`
- `/game-monitor` (OpenClaw slash command)

**Do NOT use for:**
- OS-level monitoring (use Zabbix for server metrics)
- Game server restart operations (use game-ops-restart skill)
- Player data operations (use GM后台)
- Version deployment (use deployment skill)

---

## Configuration

Set the following environment variables or configuration:

```bash
# Required — replace <collector-ip> with your Scouter Collector IP
export SCOUTER_COLLECTOR_URL=http://<collector-ip>:6188

# Optional (defaults shown)
SCOUTER_OBJ_TYPE=Java

# Alert thresholds
TPS_CRITICAL=100
TPS_WARNING=300
HEAP_CRITICAL=90
HEAP_WARNING=75
```

---

## API Reference

### Base URL

```
http://{SCOUTER_COLLECTOR_URL}/scouter/v1
```

### Endpoints Used

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/objects` | GET | List all monitored objects |
| `/object/{objHash}/counter/tps` | GET | Get TPS for one object |
| `/object/{objHash}/counter/active` | GET | Get online user count |
| `/object/{objHash}/counter/heap/used` | GET | Get heap bytes used |
| `/object/{objHash}/counter/heap/max` | GET | Get heap max bytes |
| `/status` | GET | Collector health check |

### Object Response Shape

```json
[
  {
    "objHash": "abc123def456",
    "objName": "xy_s11649",
    "objType": "Java",
    "address": "192.168.1.100",
    "state": "ACTIVE"
  }
]
```

### Counter Response Shape

```json
{
  "objHash": "abc123def456",
  "counter": "tps",
  "value": 823000,
  "unit": "",
  "timestamp": 1714281600000
}
```

**Note:** TPS `value` is in micro-ticks. Divide by 1000 to get real TPS. Online user count (`active`) is returned as-is.

---

## Workflows

### Workflow 1: Batch Query All Servers

**Input:** `"各服 TPS 怎么样"`

**Steps:**

```bash
# 1. Health check
curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/status"
# Expect: {"status":"ok"}

# 2. Get all Java objects (game servers)
curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/objects?type=${SCOUTER_OBJ_TYPE}"

# 3. For each object, fetch metrics in parallel
#    ⚠️ objHash is from network; validate it is hex before use
objHash="<value-from-json>"
if ! echo "$objHash" | grep -qE '^[0-9a-fA-F]+$'; then
  echo "[WARN] objHash validation failed: $objHash — skipping"
  continue
fi
# TPS
curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/tps"
# Active users
curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/active"
# Heap
curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/heap/used"
curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/heap/max"

# 4. Parse and format output
# - TPS: value / 1000 (round to integer)
# - Heap %: (used / max) * 100
# - Sort by TPS ascending
# - Color code: 🔴 < 100, ⚠️ 100-300, ✅ > 300
```

**Security note:** The `objHash` field returned by the Collector is a hex string. The validation above rejects any value containing non-hex characters, preventing shell injection via a malicious or compromised Collector response.

**Output:**

```
========== Game Server Health ==========
Time: 2026-04-28 14:00
Total servers: 6,847

========== TPS Alerts ==========
🔴 Critical (<100 TPS):
  xy_s20133   89 TPS / 412 online / Heap 67%
  xy_s20132  156 TPS / 891 online / Heap 45%

⚠️ Warning (100-300 TPS):
  xy_s11647  287 TPS / 3,521 online / Heap 55%

✅ OK (>300 TPS): 6,812 servers

========== Memory Alerts ==========
🔴 Critical (Heap >90%):
  xy_s20140  Heap 95% (3.8G/4G)
  xy_s20141  Heap 92% (3.7G/4G)
```

---

### Workflow 2: Single Server Query

**Input:** `"帮我看看 xy_s11649 的状态"`

**Steps:**

```bash
# 1. Find object hash by name
objHash=$(curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/objects?type=${SCOUTER_OBJ_TYPE}" | \
  jq -r '.[] | select(.objName=="xy_s11649") | .objHash')

# ⚠️ Validate objHash is safe hex before using in curl URLs
if ! echo "$objHash" | grep -qE '^[0-9a-fA-F]+$'; then
  echo "[ERROR] objHash validation failed: $objHash"
  exit 1
fi

# 2. Fetch all metrics
tps=$(curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/tps" | \
  jq -r '.value / 1000 | floor')
active=$(curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/active" | \
  jq -r '.value')
heap_used=$(curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/heap/used" | \
  jq -r '.value')
heap_max=$(curl -s "http://${SCOUTER_COLLECTOR_URL}/scouter/v1/object/${objHash}/counter/heap/max" | \
  jq -r '.value')

# 3. Calculate heap percentage
heap_pct=$(echo "scale=1; ${heap_used} * 100 / ${heap_max}" | bc)
heap_used_gb=$(echo "scale=2; ${heap_used} / 1024 / 1024 / 1024" | bc)
heap_max_gb=$(echo "scale=2; ${heap_max} / 1024 / 1024 / 1024" | bc)
```

**Output:**

```
========== xy_s11649 Status ==========
TPS:       ✅ 823
Online:    2,847
Heap:      2.10G / 4.00G (52.5%) ✅
Status:    Normal
```

---

### Workflow 3: Performance Report

**Input:** `"生成今天各服性能报表"`

**Output:**

```
========== Game Server Performance Report ==========
Date: 2026-04-28

一、Overview
Total servers: 6,847
Normal: 6,812 (99.5%)
Alerting: 35 (0.5%)

二、TPS Distribution
>1000 TPS:   1,234 servers (18%)
500-1000:    2,456 servers (36%)
300-500:     2,122 servers (31%)
100-300:     1,023 servers (15%)
<100 TPS:       12 servers (0.2%) ← action required

三、Memory Alerts
>90% Heap:   23 servers ← schedule restart
75-90% Heap: 87 servers ← monitor

四、Top 10 TPS
  xy_s11649  2,384 TPS / 2,847 online
  xy_s11650  2,201 TPS / 2,103 online
  ...

五、Top 10 Online
  xy_s11649  2,847 online / TPS 2,384
  xy_s11650  2,654 online / TPS 2,201
  ...
```

---

### Workflow 4: Alert Detection Only

**Input:** `"哪几服 TPS 告警了"`

**Output:**

```
========== TPS Alerts ==========
Time: 2026-04-28 14:00

🔴 Critical (<100 TPS): 2 servers
  xy_s20133   89 TPS / 412 online
  xy_s20132  156 TPS / 891 online

⚠️ Warning (100-300 TPS): 1 server
  xy_s11647  287 TPS / 3,521 online
```

---

## Query Dimension Detection

Auto-detect query scope from input:

| Input contains | Query scope |
|----------------|-------------|
| `"TPS"` | All servers, TPS column only |
| `"在线人数"` / `"online"` | All servers, active column only |
| `"内存"` / `"heap"` / `"memory"` | All servers, heap column only |
| Server ID (e.g. `"xy_s11649"`) | Single server, all metrics |
| `"报表"` / `"report"` | All servers, full report |

---

## Common Pitfalls

1. **TPS value is 0 or static**
   - Normal if server has no activity
   - Check: send a test player action, re-query
   - Cause: agent sampling rate may be 0

2. **Server not appearing in results**
   - Server not registered yet: wait 30s after startup
   - Wrong `type` parameter: try without `type` filter
   - Agent not loaded: check server start logs for Scouter

3. **Collector API timeout**
   - Too many objects: implement pagination or reduce query frequency
   - Collector overloaded: check memory/CPU, consider clustering

4. **Online count mismatch**
   - Scouter `active` counts active connections/threads, not unique players
   - If game has its own online counter, compare and calibrate

5. **Heap percentage > 100%**
   - `heap/used` can exceed `heap/max` during GC cycle
   - Normal behavior, not an error

---

## Scouter Architecture

```
┌─────────────────────────────────────────────────────┐
│              Scouter Collector                       │
│              Port 6180 (TCP agent→collector)         │
│              Port 6188 (HTTP API)                    │
└─────────────┬─────────────┬─────────────┬───────────┘
              │             │             │
    ┌─────────┴───┐ ┌───────┴───┐ ┌───────┴───┐
    │ Physical A  │ │ Physical B │ │ Physical C │
    │ 8 processes │ │ 7 processes│ │ 8 processes│
    │ JavaAgent   │ │ JavaAgent  │ │ JavaAgent  │
    └─────────────┘ └───────────┘ └───────────┘
```

**Components:**
- **Java Agent** (`-javaagent:scouter-agent.jar`): loaded with game server process, collects JVM metrics
- **Collector**: receives metrics from agents, exposes HTTP API, stores data
- **Web UI / Client**: visualize data (optional; this skill uses HTTP API only)

---

## Setup

### 1. Deploy Scouter Collector

```bash
# Download
wget https://github.com/scouter-project/scouter/releases/download/v2.10.0/scouter-all-2.10.0.tar.gz
tar -xzf scouter-all-2.10.0.tar.gz -C /opt/

# Start collector
cd /opt/scouter/server/
./startup.sh

# Verify
curl http://localhost:6188/scouter/v1/status
# {"status":"ok"}
```

### 2. Deploy Java Agent on Game Servers

Add to game server startup script (`ServerMain.sh`):

```bash
JAVA_OPTS="-Xms256M -Xmx${MAX_MEMORY}M \
  -javaagent:lib/scouter/scouter-agent.jar \
  -Dscouter.agent.objName=${serverId}"
```

Where `serverId` is the unique server identifier (e.g., `xy_s11649`).

### 3. Configure Collector Address in Agent

Create `lib/scouter/scouter.conf`:

```properties
scouter.server=<collector-ip>:6180
log_level=info
```

### 4. Verify Deployment

```bash
# From collector, check registered objects
curl http://<collector-ip>:6188/scouter/v1/objects?type=Java | jq length

# Should return number > 0 (count of game processes registered)
```

---

## Integration with Alerting

To send alerts on critical thresholds, see `game-alert` skill. The alert skill:
- Runs as a cronjob every 5 minutes
- Queries all servers via this skill's API
- Sends notifications via Feishu/DingTalk webhook when thresholds exceeded
- Implements cooldown to avoid duplicate alerts

---

## Attribution

- **Scouter**: Scouter Project (https://github.com/scouter-project/scouter) — JVM monitoring tool designed for game servers, widely used in Korean gaming industry
- **Skill adaptation**: Hermes Agent team

---

## See Also

- `game-alert` — Alert notification workflow
- `scouter-deploy` — Deployment checklist and verification
- `scouter-troubleshoot` — Common issues and diagnosis
- `scouter-tuning` — Capacity planning and performance tuning
