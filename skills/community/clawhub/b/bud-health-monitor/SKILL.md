---
name: health-monitor
description: "Monitor system health (RAM, disk, CPU, services). Auto-detect issues and attempt fixes. Essential for keeping Raspberry Pi running stable."
metadata:
  {
    "version": "1.0.0",
    "openclaw": {
      "requires": { "bins": ["ps", "df", "top"] },
      "depends": ["sudo-tool"],
      "install": []
    },
    "license": "MIT",
    "homepage": "https://github.com/stigg86/health-monitor",
    "allowed-tools": ["exec", "read"]
  }
---

# Health Monitor 🩺

**System health monitoring with auto-fix capabilities.** Monitors RAM, disk, CPU, and services. Detects problems before they crash your Pi.

Designed for Raspberry Pi and home server setups where resources are limited.

---

## Quick Start

```bash
# Check system health
python3 ~/.openclaw/health-monitor/health_monitor.py status

# Watch continuously (refreshes every 30s)
python3 ~/.openclaw/health-monitor/health_monitor.py watch

# Auto-fix low RAM issues
python3 ~/.openclaw/health-monitor/health_monitor.py fix
```

---

## What It Monitors

| Resource | Warning | Critical |
|----------|---------|----------|
| RAM | 80% | 90% |
| Disk | 85% | 95% |
| CPU | 85% | 95% |

---

## Commands

### `status` — Show health report
Shows current usage for RAM, disk, CPU, load average, uptime, and top processes by RAM usage.

### `watch` — Continuous monitoring
Refreshes every 30 seconds. Use Ctrl+C to stop.

### `fix` — Auto-fix low RAM
Terminates processes using >5% RAM (except critical system services). Also drops caches to free memory.

### `json` — Machine-readable output
Outputs full status as JSON for integration with other tools.

---

## Auto-Fix Capabilities

When RAM gets critical, the skill can:
1. **Terminate processes** using too much RAM (SIGTERM → SIGKILL)
2. **Drop system caches** (`sync && echo 3 > /proc/sys/vm/drop_caches`)
3. **Log events** to `~/.openclaw/health-monitor/health.log`

Requires `sudo-tool` to be installed for full functionality.

---

## Alert Thresholds

Alerts are shown when thresholds are exceeded:

- 🟡 **WARNING** — resource above warning threshold
- 🔴 **CRITICAL** — resource above critical threshold

---

## Integration

Add to cron for automated health checks:

```bash
# Check every 5 minutes, log if issues found
*/5 * * * * python3 ~/.openclaw/health-monitor/health_monitor.py status | grep -q "ALERTS" && echo "Health issue detected" | mail -s "Pi Alert"
```

Or trigger a fix automatically when RAM gets critical:

```bash
# At RAM critical, run fix
0 * * * * python3 ~/.openclaw/health-monitor/health_monitor.py json | python3 -c "import sys,json; exit(1 if json.load(sys.stdin)['ram']['percent'] > 90 else 0)" && python3 ~/.openclaw/health-monitor/health_monitor.py fix
```

---

## Files

```
~/.openclaw/health-monitor/
├── health_monitor.py   # Main script
├── health.log           # Event log
├── state.json          # Last known state (optional)
└── config.json          # Configuration (optional)
```

---

## Required By

- **vpn-mesh** — keeps node running stable
- **OANDA bot** — prevents crashes from RAM exhaustion
- **Any heavy workload** — automated health management

---

## Known Issues

- Disk at 91% on this system — needs cleanup
- Some processes cannot be killed without root (but sudo-tool handles this)