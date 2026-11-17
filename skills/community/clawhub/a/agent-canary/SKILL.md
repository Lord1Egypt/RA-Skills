---
name: agent-canary
description: Plant decoy credentials in your OpenClaw workspace to detect malicious skill behavior. Canary tokens trigger alerts when read, copied, or exfiltrated. Activate when user says "deploy canary", "set up honeypot", "plant decoy", "canary check", "canary status", or "canary cleanup".
version: 1.1.1
---

# Agent Canary

> Decoy credentials planted in your workspace. When a skill touches them, you know.


## Onboarding (First Use)

When the user first triggers this skill and `memory/agent_canary_state.json` doesn't exist, run a one-time setup:

1. **Introduce capability** (one sentence): _"I can plant decoy credentials in your workspace — if any malicious skill or agent reads them, you get an instant alert."_

2. **Quick configuration:**

1. **Alert method**(Default: Chat message)
   - Chat message (alert in current conversation)
   - Email (requires configured mail service)
   - Silent (log only, no active alerting)
2. **Decoy density**(Default: Medium)
   - Low (3-5decoys, precise detection)
   - Medium (8-12decoys, balanced coverage)
   - High (15+decoys, maximum coverage but may have false positives)

3. **Write initial state file** `memory/agent_canary_state.json`(JSON format, with `onboarded: true` and timestamp)

4. **Confirm completion**: _"Setup done! Just use it from now on. Say 'reset settings' anytime to reconfigure."

**Onboarding runs exactly once.** Subsequent activations read the state file directly. When the user says "reset settings", delete the state file and re-run setup.

---

## When to Activate

- User says: "deploy canary", "set up honeypot", "plant decoy credentials"
- User says: "canary check", "canary status", "any triggers?"
- User says: "canary cleanup", "remove canary"
- User says: "canary report", "show incidents"

Do NOT activate for normal conversations about security.

## Deploy Flow

When user asks to deploy canary:

1. Run `python3 skills/agent-canary/scripts/plant_canaries.py`
2. Report what was planted and where
3. Set up a cron job for monitoring (every 30 minutes):

```
cron add:
  name: agent-canary-monitor
  schedule: every 30 minutes
  payload: agentTurn
  message: "Run canary check. Execute: python3 skills/agent-canary/scripts/check_canaries.py. If any triggers found, immediately alert the user with details."
  delivery: announce
  sessionTarget: isolated
```

4. Tell user monitoring is active

## Check Flow

When user asks for canary status or check:

1. Run `python3 skills/agent-canary/scripts/check_canaries.py`
2. Report results:
   - If clean: "All canaries intact. No triggers."
   - If triggered: Format alert with severity, type, file, and recommendation

## Cleanup Flow

When user asks to remove canary:

1. Run `python3 skills/agent-canary/scripts/cleanup_canaries.py`
2. Remove the monitoring cron job (cron list, find agent-canary-monitor, remove it)
3. Confirm cleanup complete

## Alert Format

When a trigger is detected, notify the user:

> **CANARY TRIGGERED**
>
> Severity: [CRITICAL/HIGH/MEDIUM]
> Type: [file_modified/file_deleted/token_in_log/file_accessed]
> File: [path]
> Detail: [description]
>
> Recommendation: Check which skill was running at [timestamp]. Consider rotating real credentials as precaution.

## Report Flow

When user asks for canary report:

1. Read `~/.openclaw/agent-canary/incidents.log`
2. Summarize all incidents chronologically
3. Show current canary status (files planted, last check time)

## Technical Details

### Token Types

| Type | Marker | Example |
|------|--------|---------|
| AWS Key | `AKIACANARY` | `AKIACANARY7F3A2B9X0` |
| GitHub PAT | `ghp_CANARY_` | `ghp_CANARY_a1b2c3...` |
| Stripe | `sk_live_CANARY_` | `sk_live_CANARY_x9y8...` |
| API Key | `sk-CANARY-` | `sk-CANARY-e1f2a3...` |
| DB Password | `CANARY_PASS_` | `CANARY_PASS_Kx9m2Nv7` |

All tokens contain `CANARY` in the value, making them trivially identifiable as decoys.

### Files Created on Deploy

| File | Location | Purpose |
|------|----------|---------|
| `.env.canary` | Workspace root | Fake env config with canary credentials |
| `secrets.backup.json` | Workspace root | Fake credential backup |
| `canary-tokens.json` | `memory/` | Fake service credential cache |
| `manifest.json` | `~/.openclaw/agent-canary/` | Token registry and file hashes |
| `incidents.log` | `~/.openclaw/agent-canary/` | Incident history |

### Detection Methods

1. **File hash comparison** — detects modification of canary files
2. **File existence check** — detects deletion (possible cleanup after exfil)
3. **atime monitoring** — detects unexpected file reads
4. **Log grepping** — scans exec logs for canary token strings
5. **Git diff** — checks if canary files were staged by a skill
