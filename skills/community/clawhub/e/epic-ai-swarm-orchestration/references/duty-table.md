# Duty Table — Dynamic Model Assignment

`duty-table.json` maps swarm roles to model-provider CLIs. Prefer role-based task specs; let the table pick the actual vendor/model.

## Structure

```json
{
  "assessedAt": "ISO timestamp or null",
  "nextAssessment": "ISO timestamp or null",
  "dutyTable": {
    "architect": {
      "agent": "codex",
      "model": "gpt-5.5",
      "nonInteractiveCmd": "codex exec --model gpt-5.5 --full-auto",
      "fallback": { "agent": "gemini", "model": "gemini-2.5-pro" }
    },
    "builder": {
      "agent": "deepseek",
      "model": "deepseek-v4-pro-max",
      "nonInteractiveCmd": "deepseek -m deepseek-v4-pro-max -y -p",
      "fallback": { "agent": "codex", "model": "gpt-5.5" }
    }
  },
  "history": []
}
```

Required roles:

- `architect` — planning/design
- `builder` — implementation
- `reviewer` — review + fixes
- `integrator` — merge/conflict/build verification

## Role resolution flow

When `spawn-agent.sh` receives a role such as `builder`:

1. Read `duty-table.json`.
2. Run `fallback-swap.sh` for that role if available.
3. `fallback-swap.sh` probes the primary model via `try-model.sh`.
4. If primary fails and a fallback exists, promote fallback and demote the failed primary.
5. Spawn tmux session using the resolved agent/model.

## assess-models.sh

`assess-models.sh` probes configured model CLIs and updates duty assignments.

```bash
cd ~/workspace/swarm
bash assess-models.sh --dry-run   # probe without changing duty-table.json
bash assess-models.sh             # update duty-table.json
```

It uses a simple “Reply with HELLO” probe with a 45-second timeout. It may consume provider quota, so run deliberately.

## Scheduling

Use cron or OpenClaw cron. Cron example:

```bash
0 12 * * 6 $HOME/workspace/swarm/assess-models.sh >> $HOME/workspace/swarm/logs/weekly-assessment.log 2>&1
```

Write cron expressions in the host’s intended local timezone.

## model-fallback.sh — mid-run failover

When the runner detects token/rate/quota errors, it calls:

```bash
bash model-fallback.sh <role> <failed-agent> <failed-model>
```

Current fallback chain priority:

| Role | Chain |
|------|-------|
| architect | codex/gpt-5.5 → gemini/gemini-2.5-pro → deepseek/deepseek-v4-pro-max → codex/gpt-5.3-codex |
| builder | deepseek/deepseek-v4-pro-max → codex/gpt-5.5 → gemini/gemini-2.5-pro → codex/gpt-5.3-codex |
| reviewer | deepseek/deepseek-v4-pro-max → gemini/gemini-2.5-pro → codex/gpt-5.5 → codex/gpt-5.3-codex |
| integrator | codex/gpt-5.5 → gemini/gemini-2.5-pro → deepseek/deepseek-v4-pro-max → codex/gpt-5.3-codex |

Output format:

```text
agent|model|nonInteractiveCmd
```

## Error detection patterns

```text
rate.limit | 429 | quota | token.limit | exceeded.*limit |
capacity.*exceeded | too.many.requests | billing | budget |
overloaded | model.*limit
```

## Manual override

If an operator pins duties, preserve that choice unless explicitly told to reassess or reset.

Example marker:

```json
{
  "manualOverride": {
    "enabled": true,
    "setBy": "operator",
    "note": "Pinned during provider outage; do not auto-reset without approval."
  }
}
```
