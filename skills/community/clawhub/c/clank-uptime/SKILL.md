---
name: clank-uptime
description: Track website uptime, response times, and availability. CSV-based history, 24h stats with visual bars, avg/min/max latency. Lightweight alternative to paid monitoring services.
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "bins": ["curl", "python3"] },
      },
  }
---

# clank-uptime

Lightweight CLI for tracking website uptime and response times over time.

## When to use (trigger phrases)

Use this skill when the user asks any of:

- "Is my site up?"
- "Check if website X is online"
- "Monitor my site's uptime"
- "What's the response time for..."
- "Show availability stats"

## Quick start

```bash
# Add sites
clank-uptime add https://example.com --name "My Site"
clank-uptime add https://api.example.com --name "API"

# Check all sites now
clank-uptime check

# Show 24h availability stats
clank-uptime stats

# List monitored sites
clank-uptime list

# Remove a site
clank-uptime remove https://example.com
```

## Commands

| Command | Description |
|---------|-------------|
| `add <URL> [--name NAME]` | Add site to monitoring |
| `check` | Check all sites, append to history |
| `stats` | Show 24h availability & latency stats |
| `list` | List all monitored sites |
| `remove <URL>` | Remove site from monitoring |

## Output examples

### Check
```
🔍 Checking 3 sites...

  ✅ My Site: 200 (0.092s)
  ✅ API: 200 (0.056s)
  ⚠️ Old Site: 503 (1.234s)

📊 Checked at 2026-03-29T04:22:38Z
```

### Stats
```
📊 Uptime Statistics (last 24h)
==================================================

  My Site
    [████████████████████] 100.0% (12/12 checks)
    ⚡ Avg: 0.089s | Min: 0.056s | Max: 0.142s

  API
    [██████████████████░░] 91.7% (11/12 checks)
    ⚡ Avg: 0.067s | Min: 0.041s | Max: 0.098s
```

## Data storage

```
~/.clank-uptime/
├── sites.json          # Site configuration
└── history/
    └── <site-id>/
        └── checks.csv  # timestamp,status,response_time
```

## Automating with cron

```bash
# Check every 5 minutes
*/5 * * * * clank-uptime check > /dev/null 2>&1

# Daily stats report
0 8 * * * clank-uptime stats | mail -s "Daily Uptime Report" you@email.com
```

## Tips

- Run `check` periodically (cron or heartbeat) to build history data
- `stats` requires at least a few hours of data for meaningful results
- Use `--name` for readability; defaults to URL
- History is CSV-based — easy to parse or visualize with other tools
