---
name: restore
description: Restore a gateway to its last known-good configuration, or tag the current config as known-good. Use when a gateway config change breaks something and you need to roll back fast. Responds to /restore slash command.
user-invocable: true
---

# Gateway Restore

Roll back a gateway config to the last known-good state, then restart safely with health checks and automatic rollback on failure.

## Usage (as slash command or natural language)

- `/restore` — restore the Slack gateway to known-good
- `/restore discord` — restore the Discord gateway to known-good
- `/restore tag` — tag the current Slack config as known-good
- `/restore tag discord` — tag the current Discord config as known-good

## How It Works

1. Backs up the current (broken) config with a timestamped filename
2. Copies the `known-good.json` over the live config
3. Runs the appropriate safe restart script (`safe-slack-restart.sh` or `safe-gateway-restart.sh`)
4. The safe restart script validates health and rolls back if the gateway doesn't come up

## Tagging Known-Good

After any successful config change + restart, tag the current config:

```bash
bash skills/gateway-restore/scripts/gateway-restore.sh slack --tag-current
bash skills/gateway-restore/scripts/gateway-restore.sh discord --tag-current
```

This saves it as `config-backups/known-good.json`. Old tagged versions are also kept as `known-good-TIMESTAMP.json`.

## Script Location

`skills/gateway-restore/scripts/gateway-restore.sh`

## When Invoked via Slash Command

The `command-bypass` hook handles `/restore` slash commands automatically — the script runs detached without LLM involvement. You do NOT need to execute the script.

If the hook fires, simply reply confirming the restore is in progress. Do not call exec.

## When Invoked via Natural Language

If the user asks to restore via natural language (not a slash command), THEN run the script:

```bash
setsid bash /home/swabby/repos/swabby-brain/skills/gateway-restore/scripts/gateway-restore.sh [slack|discord] [--tag-current] > /tmp/restore-output.log 2>&1 &
sleep 2 && cat /tmp/restore-output.log
```

Parse the request:
- "restore" / "rollback" → slack gateway
- "restore discord" → discord gateway  
- "restore tag" → tag current slack config as known-good

If the gateway restarts mid-exec (SIGTERM), that's expected — the restart succeeded.
