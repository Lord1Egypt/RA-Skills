---
title: "Troubleshooting"
source:
  - https://docs.github.com/en/copilot/how-tos/copilot-cli/troubleshoot-copilot-cli
category: reference
---

Common Copilot CLI issues, root causes, and fixes.

## Authentication Issues

| Issue | Fix |
|-------|-----|
| 401 Unauthorized | Re-authenticate; ensure **Copilot Requests** permission on PAT |
| 403 / policy denied | Check Copilot subscription; ask org admin to enable CLI policy |
| Classic PAT (`ghp_`) rejected | Use fine-grained PAT (`github_pat_`) instead |
| Wrong account | Unset unintended env vars (`COPILOT_GITHUB_TOKEN`, `GH_TOKEN`); use `/user switch` |
| Keychain unavailable (Linux) | Install `libsecret`: `sudo apt install libsecret-1-0 gnome-keyring`; or accept plaintext |

### Keychain Diagnostics

```bash
# macOS
security find-generic-password -s copilot-cli
security delete-generic-password -s copilot-cli   # remove and re-auth

# Linux
command -v secret-tool
secret-tool search copilot-cli
```

## Rate Limits

- **Claude Code** has daily/hourly limits **separate** from Copilot CLI
- **Fallback:** switch to Copilot CLI with `-p --yolo --no-ask-user`
- **Mitigation:** space out large spawns 30+ min apart
- Copilot CLI uses premium requests (per-prompt, model multiplier varies by model)
- **Autopilot cost:** each autonomous continuation shows `Continuing autonomously (N premium requests)` — use `--max-autopilot-continues=N` to cap
- **Fleet cost:** each subagent uses premium requests independently — faster but potentially more expensive
- Check usage: `/usage` shows session stats, `/model` shows current model and multiplier

## EPIPE Errors in Non-Interactive Mode

**Symptom:** `write EPIPE` errors, process crashes when run via `exec()` without TTY.

**Root cause:** Copilot writes ANSI-formatted output to stdout. When stdout is piped/redirected, the pipe closes before Copilot finishes writing → EPIPE → crash.

**Fix:** Always run with PTY emulation. In OpenClaw, set `pty: true` on exec calls.

## OpenClaw Exec Integration

When driving Copilot CLI from OpenClaw (or any agent orchestrator), three things are required:

| Requirement | Solution | Why |
|-------------|----------|-----|
| TTY | `pty: true` | Prevents EPIPE crashes on stdout writes |
| Timeout | `timeout: 120+` | MCP startup (3s) + inference (25s+) = 30s minimum |
| Permissions | `--allow-all` | `--no-ask-user` alone doesn't grant file write access |

```bash
# Minimal working invocation from OpenClaw exec
copilot -p "<prompt>" --no-ask-user --allow-all --max-autopilot-continues 3
# exec options: pty=true, timeout=120
```

**Common failure modes:**
- Missing `pty: true` → EPIPE, SIGKILL
- Timeout too short (<30s) → SIGKILL before response
- Missing `--allow-all` → "Permission denied and could not request permission from user"

## SIGTERM Kills (Timeout Too Short)

**Symptom:** Task killed mid-execution, partial output. **Fix:** Size timeouts by complexity:

| Complexity | Timeout |
|------------|---------|
| Simple (review, small fix) | 120–300s |
| Medium (single component) | 300–600s |
| Large (research + build) | 900–1800s |
| Very large (full redesign) | 1800s+ |

**Rule:** when in doubt, 1800s.

## PTY Output Fragmentation

**Symptom:** JSON truncated or mixed with ANSI codes.

**Fixes:** Poll with 60–90s timeout; use `-s` for clean output; `--output-format json` for JSONL; multiple polls normal for long tasks.

## Background Server Lifecycle

Servers die between exec spawns. Always restart:

```bash
lsof -ti:PORT | xargs kill -9 2>/dev/null
python3 -m http.server PORT &>/dev/null &
```

## Folder Trust Prompt

`--yolo` does NOT bypass trust. Pre-trust:

```bash
python3 -c "
import json
p = '$HOME/.copilot/config.json'
c = json.load(open(p))
c.setdefault('trusted_folders',[]).append('/tmp/mydir')
json.dump(c, open(p,'w'), indent=2)
"
```

## Git Init Gotchas

Copilot requires a git repo. For temp directories:

```bash
dir=$(mktemp -d) && cd "$dir"
git init && git config user.email "bot@example.com" && git config user.name "Bot"
```

Don't re-init existing repos.

## `-i` Flag Hangs

`-i` starts interactive mode and waits for input. **Always use `-p` for automation.**

## Config Gotchas

| Gotcha | Detail |
|--------|--------|
| No `copilot config set` | Edit `~/.copilot/config.json` manually |
| `copilot providers` is a help topic | Use `copilot help providers` |
| `--model` names differ | Between Claude Code and Copilot CLI — test first |
| Temp dirs vanish | `/tmp` cleaned periodically — copy to permanent storage |
| Port numbers | Specify explicitly in prompts |

## Model Availability

Only GitHub-routed models work: `claude-opus-4.6` (default), `claude-sonnet-4`. For others: use BYOK env vars (`COPILOT_PROVIDER_BASE_URL`, `COPILOT_PROVIDER_TYPE`, `COPILOT_MODEL`). Enterprise policies can restrict available models — users only see enterprise-enabled models via `/model`.

## Autopilot Runaway Prevention

**Symptom:** Autopilot loops endlessly or burns through premium requests.

**Fix:** Always set `--max-autopilot-continues=N` (e.g., 10) in automation. In interactive sessions, press `Ctrl+C` to stop. CI/CD should always include this limit.

## Enterprise Access Issues

| Issue | Fix |
|-------|-----|
| Developers can't access CLI | Verify Copilot seat assignment; check enterprise/org-level policy |
| Policy set to "Let organizations decide" | CLI must be enabled in at least one org granting the user's license |
| `/delegate` not working | Both CLI and cloud agent policies must be enabled |
| Missing models | Enterprise model selection restricts available models |

## Diagnostic Steps

1. **Auth:** `copilot login` or verify env vars
2. **Model:** `copilot help` for available model strings; `/model` to check current
3. **Trust:** check `~/.copilot/config.json` → `trusted_folders`
4. **Logs:** set `log_level: "debug"` in config; logs at `~/.copilot/logs/`
5. **Version:** `copilot --version` and `copilot update`
6. **Session store:** `/chronicle reindex` if history queries fail or after recovering sessions
7. **Hooks:** verify JSON in `.github/hooks/`, correct shebang, executable scripts
8. **MCP:** `/mcp show` to check server status; `/mcp enable NAME` if disabled
