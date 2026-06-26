---
name: agent-meter
description: "Track API spend with intent-level attribution. Shows where your tokens go by project and purpose. Invoke with /meter for spend summary."
version: "0.6.3"
user-invocable: true
---

# /meter — API Spend Tracker

When the user invokes `/meter`, run a SINGLE bash command that handles everything: setup check, backfill, and summary. One prompt, one approval.

## Execution

Run this single bash command:

```bash
bash "$(for d in "$HOME/.claude/skills/agent-meter" "$HOME/.claude/skills/meter" ".claude/skills/meter" ".claude/skills/agent-meter"; do [ -f "$d/meter.sh" ] && echo "$d/meter.sh" && break; done)"
```

If `meter.sh` is not found, tell the user the script wasn't found and suggest reinstalling.

Format the output as a clean markdown summary for the user.

If the user passes arguments like `/meter --by model` or `/meter --last 7d`, append them: `bash .../meter.sh --last 7d`

## Setup

Install from ClawHub into your project:

```bash
clawhub install agent-meter --dir .claude/skills
```

Then run `/meter` — it handles everything automatically:
- Copies the session-end hook to `.claude/hooks/`
- Creates or updates `.claude/settings.json` with the Stop hook
- Backfills any existing Claude Code sessions
- Shows your spend summary

That's it. Future sessions are tracked automatically via the Stop hook.

### Dashboard sync (optional)

To sync spend data to the hosted dashboard at [dashboard.agentmeter.io](https://dashboard.agentmeter.io):

```bash
bash .claude/skills/agent-meter/meter-sync.sh --setup
```

The setup wizard will prompt for your API key and agent name. Get a key from the dashboard's Machines page. After setup, sync anytime with:

```bash
bash .claude/skills/agent-meter/meter-sync.sh
```

### What the scripts do

- **meter.sh** — Single entry point for `/meter`. Checks hook installation, backfills if needed, shows spend summary. All in one script, one permission prompt.

- **meter-session-end.sh** (Stop hook): Parses the current session's transcript for per-message token usage. Detects model (opus/sonnet/haiku), calculates cost with model-specific pricing including cache tier pricing, writes a single `session_summary` record. Deduplicates by session_id — safe across session pause/resume. No network calls, no secrets access, jq dependency only.

- **meter-parse-claude-sessions.sh** (backfill): Scans all Claude Code transcripts in `~/.claude/projects/*/*.jsonl`. Extracts the same usage data as the hook. Deduplicates against existing records by session_id. Safe to re-run — only processes new sessions. No network calls, no secrets access, jq dependency only.

## Query Examples

```bash
SPEND="$HOME/.agent-meter/spend.jsonl"

# Spend by project
jq -s 'group_by(.project) | map({project: .[0].project, cost: (map(.cost_usd) | add), sessions: length}) | sort_by(-.cost)' "$SPEND"

# Spend by model
jq -s 'group_by(.model) | map({model: .[0].model, cost: (map(.cost_usd) | add), sessions: length}) | sort_by(-.cost)' "$SPEND"

# Today's spend
jq -s "[.[] | select(.ts | startswith(\"$(date -u +%Y-%m-%d)\"))] | map(.cost_usd) | add" "$SPEND"

# Top 10 most expensive sessions
jq -s 'sort_by(-.cost_usd) | .[:10] | .[] | "\(.cost_usd | . * 100 | round / 100) \(.project) \(.total_calls) calls \(.ts | split("T")[0])"' "$SPEND" -r
```

## Schema

All records are `session_summary` type in `~/.agent-meter/spend.jsonl`.

| Field | Required | Description |
|-------|----------|-------------|
| `type` | yes | Always `session_summary` |
| `ts` | yes | ISO 8601 timestamp (session start) |
| `api` | yes | `api.anthropic.com` |
| `model` | yes | Model identifier (e.g. `claude-opus-4-6`) |
| `session_id` | yes | Claude Code session UUID |
| `project` | yes | Project directory name |
| `total_calls` | yes | Number of assistant messages |
| `tokens_in` | yes | Input tokens (non-cached) |
| `tokens_out` | yes | Output tokens |
| `cache_creation` | yes | Cache creation input tokens |
| `cache_read` | yes | Cache read input tokens |
| `cost_usd` | yes | Estimated cost (model-aware pricing) |
| `source` | yes | `hook` or `session_parse` |
| `purpose` | no | Human-readable intent (manual tag) |
| `intent` | no | Machine tags (manual) |

### Cost Calculation

Per-1M-token pricing:

| Model | Input | Output | Cache Create | Cache Read |
|-------|-------|--------|-------------|------------|
| Opus | $15 | $75 | $18.75 (1.25x) | $1.50 (0.1x) |
| Sonnet | $3 | $15 | $3.75 (1.25x) | $0.30 (0.1x) |
| Haiku | $0.25 | $1.25 | $0.3125 (1.25x) | $0.025 (0.1x) |
