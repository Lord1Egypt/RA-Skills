---
name: code-card-sync
description: "Sync your AI coding stats to Code Card - beautiful, shareable developer profiles"
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": {
          "bins": ["node", "npx"]
        }
      }
  }
---

# Code Card Sync

Sync your AI coding stats (Claude Code, Codex, OpenClaw) to [Code Card](https://www.codecard.dev) - beautiful, shareable developer profiles.

## First-Time Setup

Check if already configured:

```bash
cat ~/.claude/.codecard 2>/dev/null
```

If it prints `CC_API_KEY=cc_...`, skip to the **Sync** section.

If not configured, run:

```bash
npx code-card@latest
```

This will print a URL and a code like:

```
Go to:     https://www.codecard.dev/link
Enter code: ABCD-1234
```

Tell the user to visit that URL and enter the code in their browser. They will log in or create an account there. Once they complete it, the CLI finishes automatically and syncs all sessions.

## Sync

Incremental sync (fast, only new sessions):

```bash
npx code-card@latest sync -i
```

Full resync (recomputes everything):

```bash
npx code-card@latest sync
```

## Other Commands

| Command | What it does |
|---------|-------------|
| `npx code-card@latest stats` | Show stats summary |
| `npx code-card@latest profile` | Open profile in browser |

## Recommended Cron Schedule

Daily incremental + weekly full:

```
cron add --name "code-card-daily" --schedule "0 6 * * *" --tz "America/New_York" --isolated --message "Run an incremental Code Card sync by executing: npx code-card@latest sync -i"
```

```
cron add --name "code-card-weekly" --schedule "0 7 * * 0" --tz "America/New_York" --isolated --message "Run a full Code Card sync by executing: npx code-card@latest sync"
```

## More Info

- Website: https://www.codecard.dev
- npm: https://www.npmjs.com/package/code-card
- Requires Node.js 18+
