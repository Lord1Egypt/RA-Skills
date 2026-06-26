---
name: edgefinder-cli
description: Use the EdgeFinder CLI for NFL, NBA, and MLB analysis, plus NFL/NBA schedules, standings, Polymarket odds, and portfolio lookups from the terminal.
homepage: https://github.com/andrewnexys/edgefinder-cli
user-invocable: false
metadata: {"openclaw":{"homepage":"https://github.com/andrewnexys/edgefinder-cli","requires":{"anyBins":["edgefinder","npx"]},"primaryEnv":"EDGEFINDER_API_KEY","install":[{"id":"node","kind":"node","package":"@edgefinder/cli","bins":["edgefinder"],"label":"Install EdgeFinder CLI"}]}}
---

# EdgeFinder CLI

Use this skill when the user wants NFL, NBA, or MLB betting analysis, NFL/NBA schedules, NFL/NBA standings, NFL/NBA Polymarket odds, or EdgeFinder portfolio data.

## Setup

- Use the bundled wrapper script: `sh {baseDir}/scripts/run.sh ...`
- The wrapper prefers the installed `edgefinder` binary and falls back to `npx -y @edgefinder/cli`.
- Authenticate in one of these ways:
  - Set `EDGEFINDER_API_KEY=ef_live_...` in your environment (recommended — add to shell profile or OpenClaw's env config).
  - Run `sh {baseDir}/scripts/run.sh login` for the interactive magic-link flow.
  - If installed via `openclaw plugins install @edgefinder/openclaw-plugin`, set it via: `openclaw config set plugins.entries.edgefinder-cli.config.EDGEFINDER_API_KEY ef_live_...`

## Usage

For conversational analysis, use `ask`:

```bash
sh {baseDir}/scripts/run.sh ask "Who should I bet on tonight?"
sh {baseDir}/scripts/run.sh ask --nba "Lakers vs Celtics prediction"
sh {baseDir}/scripts/run.sh ask --mlb "Yankees vs Red Sox prediction"
```

For structured data, prefer JSON output:

```bash
sh {baseDir}/scripts/run.sh schedule nfl --json
sh {baseDir}/scripts/run.sh schedule nba --date 2026-03-23 --json
sh {baseDir}/scripts/run.sh standings nba --json
sh {baseDir}/scripts/run.sh odds nfl --week 12 --json
sh {baseDir}/scripts/run.sh odds nba --date 2026-03-23 --json
sh {baseDir}/scripts/run.sh portfolio summary --json
sh {baseDir}/scripts/run.sh portfolio positions --league nba --json
sh {baseDir}/scripts/run.sh portfolio trades --league nfl --limit 20 --json
sh {baseDir}/scripts/run.sh status --json
```

## Notes

- NFL is the default league unless `--nba` or `--mlb` is passed.
- MLB is currently available for conversational analysis via `ask --mlb` and interactive mode after `/mlb`. Structured schedule, standings, odds, and portfolio league filters are currently NFL/NBA only.
- `sh {baseDir}/scripts/run.sh` with no subcommand starts the interactive REPL. In automated agent runs, prefer explicit subcommands.
- CLI access requires an active paid EdgeFinder subscription. If auth is missing, `sh {baseDir}/scripts/run.sh login` will prompt for email and may open the subscription page.
- Never print or echo the full API key back to the user.
- After installing this skill, start a new conversation with your agent for it to take effect.
