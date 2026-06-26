---
name: acmilan-match-monitor
description: Check if AC Milan played yesterday and send the result. Uses ESPN public API — no token, no region restrictions. Works with curl directly. Silent if no match. Perfect for daily 8:30 AM cron push.
---

# AC Milan Match Monitor

Check yesterday's AC Milan match result using ESPN's public API.

## Why ESPN API?

- ✅ No API key required
- ✅ No region restrictions (works anywhere)
- ✅ Direct curl, no browser needed
- ❌ Don't use web_search (region-blocked)
- ❌ Don't use acmilan.com (React SPA, curl gets empty shell)
- ❌ Don't use sofascore API (returns 403)

## Setup

Place `scripts/check_match.py` in your skill folder. No dependencies beyond Python 3 stdlib.

## Usage

Run the script via `nodes.run` or locally:

```bash
python3 scripts/check_match.py
```

**Output (if match yesterday):**
```
⚽ AC Milan ✅ Win
Score: AC Milan 3 - 2 Torino
Competition: Serie A
```

**Output (if no match):** silent, no output.

## Cron Integration

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "Run the AC Milan match check script via nodes.run:\n[\"/usr/bin/python3\", \"/path/to/skills/acmilan-match-monitor/scripts/check_match.py\"]\n\nIf output exists, forward it to the user.\nIf no output, end silently.",
    "model": "dashscope/qwen-plus",
    "timeoutSeconds": 60
  },
  "schedule": { "kind": "cron", "expr": "30 8 * * *", "tz": "Asia/Shanghai" }
}
```

## Key Info

- AC Milan ESPN ID: **103**
- League code: **ita.1** (Serie A)
- API endpoint: `https://site.api.espn.com/apis/site/v2/sports/soccer/ita.1/teams/103/schedule?limit=5`
