---
name: openclaw-master-ops
description: >
  The definitive OpenClaw operations & expertise skill. Combines CLI mastery, 
  gateway administration, security auditing, troubleshooting, channel management, 
  agent/node orchestration, and production best practices. Includes automated 
  release tracking with SQLite database for breaking change detection. Use for 
  any OpenClaw operations task: setup, debugging, security hardening, performance 
  tuning, multi-node deployments, channel configuration, model routing, cron 
  automation, plugin management, incident response, and version change management.
---

# OpenClaw Master Operations

The comprehensive OpenClaw operations skill — combining CLI mastery, gateway administration, security hardening, troubleshooting workflows, and production best practices.

## When to Use This Skill

Use this skill whenever the user needs to:

- **Set up OpenClaw** — Installation, initial config, onboarding, multi-node deployments
- **Operate the Gateway** — Start/stop/restart, bind modes, auth, discovery, Tailscale exposure
- **Debug issues** — Connection failures, auth errors, channel problems, agent crashes, exec failures
- **Harden security** — Audit config, fix permissions, tighten group policies, SecretRef management
- **Manage channels** — Telegram, WhatsApp, Discord, Slack, Signal setup and troubleshooting
- **Configure agents/models** — Model routing, sandbox settings, tool profiles, ACP harness setup
- **Automate operations** — Cron jobs, scheduled tasks, watchdogs, health monitoring
- **Manage plugins/skills** — Install, update, publish to ClawHub, troubleshoot plugin conflicts
- **Respond to incidents** — Gateway crashes, session corruption, credential expiry, approval failures

## Core Principles

### 1. Safety First

- **Back up before destructive actions** — Always backup `openclaw.json`, credentials/, sessions/ before `--fix` operations
- **Prefer `trash` over `rm`** — Use recoverable deletion when cleaning up state
- **Verify before applying** — Show users what will change before running `--fix` or `--repair` commands
- **SecretRef awareness** — Know when config values are secret-managed vs plaintext

### 2. Diagnostic Discipline

Follow this triage sequence for any OpenClaw issue:

```
1. Check gateway status → openclaw gateway status
2. Run health check → openclaw doctor
3. Inspect logs → openclaw logs --recent 50
4. Verify auth → openclaw gateway query whoami
5. Check channels → openclaw channels list
6. Test exec → openclaw exec "echo test"
7. Security audit → openclaw security audit
```

### 3. Output Hygiene

- **Prefer `--json` for automation** — Machine-readable output for scripts/CI
- **Use `--no-color` in logs** — Clean output for cron/webhook contexts
- **Redact sensitive data** — Never log tokens, passwords, or credential paths

## Command Reference

### Gateway Operations

```bash
# Start/Stop/Restart
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status

# Run in foreground (dev)
openclaw gateway run --bind loopback --auth token

# Query running gateway
openclaw gateway query whoami
openclaw gateway query sessions
openclaw gateway query channels
openclaw gateway query nodes

# Discovery (find gateways on network)
openclaw gateway discover
openclaw gateway discover --wide  # DNS-SD beyond local network
```

### Health & Diagnostics

```bash
# Quick health check
openclaw doctor

# Auto-repair common issues
openclaw doctor --repair
openclaw doctor --repair --non-interactive

# Deep scan (includes system services)
openclaw doctor --deep

# Generate gateway token
openclaw doctor --generate-gateway-token
```

### Security Operations

```bash
# Security audit
openclaw security audit
openclaw security audit --deep
openclaw security audit --json | jq '.summary'

# Apply safe fixes
openclaw security audit --fix
openclaw security audit --fix --json

# Manage secrets
openclaw secrets list
openclaw secrets get <name>
openclaw secrets set <name> <value>
openclaw secrets delete <name>
```

### Channel Management

```bash
# List channels
openclaw channels list
openclaw channels list --json

# Channel status
openclaw channels status telegram
openclaw channels status whatsapp

# QR codes (for WhatsApp/Telegram bot setup)
openclaw qr show telegram
openclaw qr show whatsapp

# Channel troubleshooting
openclaw channels repair telegram
openclaw channels repair whatsapp
```

### Node & Agent Management

```bash
# List nodes
openclaw nodes list
openclaw nodes status

# Node pairing
openclaw node pair
openclaw node unpair <node-id>
openclaw pairing list

# Agent management
openclaw agents list
openclaw agent status <agent-id>
openclaw agent restart <agent-id>

# ACP harness (Claude Code, Cursor, etc.)
openclaw acp list
openclaw acp status
```

### Session Management

```bash
# List sessions
openclaw sessions list
openclaw sessions list --active-minutes 30
openclaw sessions list --kinds subagent

# Session history
openclaw sessions history <session-key>
openclaw sessions history <session-key> --limit 50 --include-tools

# Send to session
openclaw sessions send <session-key> "message here"

# Kill session
openclaw sessions kill <session-key>
```

### Cron & Automation

```bash
# List cron jobs
openclaw cron list
openclaw cron list --json

# Manage jobs
openclaw cron add "0 6 * * *" "openclaw doctor --repair"
openclaw cron remove <job-id>
openclaw cron run <job-id>

# Heartbeat management
openclaw heartbeat status
openclaw heartbeat run
```

### Plugin & Skill Management

```bash
# Skills (ClawHub)
clawhub install <skill-slug>
clawhub update <skill-slug>
clawhub update --all
clawhub list
clawhub search "<query>"

# Plugins
openclaw plugins list
openclaw plugins install <plugin-name>
openclaw plugins update <plugin-name>
openclaw plugins remove <plugin-name>
```

### Logs & Debugging

```bash
# Recent logs
openclaw logs --recent 100
openclaw logs --follow
openclaw logs --level debug

# Gateway logs
openclaw logs gateway --recent 50

# Agent logs
openclaw logs agent <agent-id> --recent 50

# Export logs
openclaw logs export ./logs-backup.tar.gz
```

### Config Management

```bash
# View config
openclaw config list
openclaw config get <key>
openclaw config get gateway.auth.token

# Set config
openclaw config set <key> <value>
openclaw config set gateway.mode local

# Delete config
openclaw config delete <key>

# Backup/Restore
openclaw backup create
openclaw backup list
openclaw backup restore <backup-id>
```

### System Operations

```bash
# System status
openclaw system info
openclaw system status
openclaw system resources

# Update OpenClaw
openclaw update
openclaw update --preview

# Reset (careful!)
openclaw reset --keep-channels
openclaw reset --all  # Full reset
```

## Troubleshooting Playbooks

### Gateway Won't Start

```bash
# 1. Check if something's using the port
lsof -i :18789
netstat -tlnp | grep 18789

# 2. Kill existing process
openclaw gateway stop --force

# 3. Check config
openclaw config get gateway.mode
openclaw config get gateway.bind

# 4. Run doctor
openclaw doctor --repair

# 5. Check logs
openclaw logs gateway --recent 100
```

### "Pairing Required" Errors

```bash
# 1. Check pairing status
openclaw pairing list

# 2. Re-pair node
openclaw node pair

# 3. If still failing, reset pairing
openclaw config delete nodes.paired
openclaw node pair

# 4. For mobile apps, show QR
openclaw qr show
```

### Channel Auth Failures

```bash
# 1. Check channel status
openclaw channels status <channel>

# 2. Verify credentials exist
ls -la ~/.openclaw/credentials/

# 3. Re-authenticate
openclaw channels auth <channel>

# 4. For Telegram/WhatsApp, regenerate QR
openclaw qr show <channel>
```

### Exec Approval Timeouts

```bash
# 1. Check approval config
openclaw config get gateway.nodes.allowCommands
openclaw config get gateway.nodes.denyCommands

# 2. Check pending approvals
openclaw approvals list

# 3. For known-safe commands, add to allowlist
openclaw config set gateway.nodes.allowCommands '["ls", "cat", "grep"]'

# 4. Restart gateway
openclaw gateway restart
```

### Session Corruption

```bash
# 1. List sessions
openclaw sessions list

# 2. Kill problematic session
openclaw sessions kill <session-key>

# 3. Clean up orphaned transcripts
openclaw doctor --repair

# 4. If severe, reset sessions
openclaw reset --sessions-only
```

### Model/API Errors

```bash
# 1. Check model config
openclaw config get agents.defaults.model

# 2. Test inference
openclaw infer --model qwen/qwen3.5-plus "Hello"

# 3. Check provider status
openclaw models list

# 4. Rotate API keys if needed
openclaw secrets set OPENAI_API_KEY <new-key>
```

## Security Hardening Checklist

Run these periodically (weekly for production):

```bash
# 1. Security audit
openclaw security audit --deep

# 2. Apply safe fixes
openclaw security audit --fix

# 3. Check for exposed secrets
openclaw secrets list --show-metadata

# 4. Verify channel allowlists
openclaw config get channels.telegram.allowFrom
openclaw config get channels.whatsapp.allowFrom

# 5. Check group policies
openclaw config get channels.telegram.groupPolicy
openclaw config get channels.whatsapp.groupPolicy

# 6. Audit installed plugins
openclaw plugins list
clawhub list

# 7. Review recent sessions
openclaw sessions list --active-minutes 1440

# 8. Check for updates
openclaw update --check
```

## Production Best Practices

### 1. Use SecretRef for Sensitive Values

```json
{
  "gateway.auth.token": {
    "$secretRef": "gateway-token"
  },
  "channels.telegram.token": {
    "$secretRef": "telegram-bot-token"
  }
}
```

### 2. Enable Sandbox Mode

```bash
openclaw config set agents.defaults.sandbox.mode on
openclaw config set agents.defaults.sandbox.docker true
```

### 3. Configure Session DM Scope

For shared inboxes:
```bash
openclaw config set session.dmScope per-channel-peer
```

### 4. Set Up Monitoring Cron

```bash
# Health check every 30 minutes
openclaw cron add "*/30 * * * *" "openclaw doctor --non-interactive"

# Security audit weekly
openclaw cron add "0 3 * * 0" "openclaw security audit --deep --json > ~/security-audit.json"
```

### 5. Enable Logging Redaction

```bash
openclaw config set logging.redactSensitive tools
```

### 6. Configure Model Routing

```bash
# Default model for agents
openclaw config set agents.defaults.model.primary qwen/qwen3.5-plus

# Fallback model
openclaw config set agents.defaults.model.fallback zai/glm-5

# Model for specific tasks
openclaw config set agents.defaults.model.reasoning qwen/qwen3.5-plus
```

## Quick Reference: Command Families

| Family | Commands | Use When |
|--------|----------|----------|
| **Gateway** | `gateway start/stop/status/query` | Managing the WebSocket server |
| **Health** | `doctor`, `health` | Diagnosing issues |
| **Security** | `security audit`, `secrets` | Hardening config |
| **Channels** | `channels list/status/repair`, `qr` | Channel setup/debug |
| **Nodes** | `nodes list`, `node pair`, `pairing` | Multi-node setups |
| **Agents** | `agents list`, `agent status`, `acp` | Agent management |
| **Sessions** | `sessions list/history/send/kill` | Session orchestration |
| **Cron** | `cron list/add/run/remove` | Automation |
| **Plugins** | `plugins list/install/update` | Plugin management |
| **Skills** | `clawhub install/update/search` | Skill management |
| **Config** | `config list/get/set/delete` | Config changes |
| **Logs** | `logs --recent/--follow` | Debugging |
| **System** | `system info/status/update` | System ops |

## Escalation Paths

When standard troubleshooting fails:

1. **Check official docs** — `openclaw docs` or https://docs.openclaw.ai
2. **Search ClawHub** — `clawhub search "<topic>"` for relevant skills
3. **Check GitHub issues** — https://github.com/openclaw/openclaw/issues
4. **Discord community** — https://discord.gg/clawd
5. **Enable debug logging** — `openclaw config set logging.level debug`

## Notes

- **Profile isolation** — Use `--profile <name>` to isolate state: `openclaw --profile dev gateway`
- **Dev mode** — Use `--dev` flag for isolated dev environment: `openclaw --dev gateway`
- **Container targeting** — Use `--container <name>` to target specific containers
- **JSON output** — Add `--json` for machine-readable output in all commands
- **No color** — Add `--no-color` or set `NO_COLOR=1` for clean logs

## Release Tracking

This skill includes automated OpenClaw release tracking to stay current with frequent updates.

### Database

Location: `skills/openclaw-master-ops/release-history.db`

Tracks:
- Release versions and changelogs
- Breaking changes (auto-detected)
- Skill knowledge verification status

### Commands

```bash
cd /home/marius/.openclaw/workspace/skills/openclaw-master-ops

# Sync latest releases from GitHub
python3 scripts/release-tracker.py sync

# View release history
python3 scripts/release-tracker.py history

# Check breaking changes
python3 scripts/release-tracker.py breaking

# Check if skill needs updates
python3 scripts/release-tracker.py skill-update

# Export for skill context
python3 scripts/release-tracker.py export
```

### Automated Sync (Cron)

```bash
# Weekly sync (Sundays 3 AM)
openclaw cron add "0 3 * * 0" "cd ~/.openclaw/workspace/skills/openclaw-master-ops && python3 scripts/release-tracker.py sync"

# Daily check for updates
openclaw cron add "0 8 * * *" "cd ~/.openclaw/workspace/skills/openclaw-master-ops && python3 scripts/release-tracker.py skill-update"
```

### When OpenClaw Updates

After running `openclaw update`:

1. **Run sync** — `python3 scripts/release-tracker.py sync`
2. **Check breaking** — `python3 scripts/release-tracker.py breaking`
3. **Review skill updates** — `python3 scripts/release-tracker.py skill-update`
4. **Update skill if needed** — Edit SKILL.md based on breaking changes
5. **Republish** — `clawhub publish ... --version 1.X.0 --changelog "Updated for OpenClaw <version>"`

### Breaking Change Detection

Auto-detects these patterns in changelogs:
- `removed` → feature_removal
- `deprecated` → deprecation
- `breaking` → breaking_change
- `migration` → migration_required
- `changed default` → default_change
- `config schema` → config_change
- `command removed` → command_removal

See `references/release-tracking.md` for full workflow.

---

## Related Skills

- `deep-research` — For researching OpenClaw topics, comparing configurations
- `plugin-publisher` — For creating and publishing OpenClaw plugins
- `npd-validator` — For validating new OpenClaw feature ideas
