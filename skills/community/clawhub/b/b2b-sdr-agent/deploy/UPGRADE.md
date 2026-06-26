# OpenClaw Upgrade Guide

Safe upgrade procedure for production SDR agents. Follow every step — skipping the backup or verification has caused real outages.

## Pre-Upgrade Checklist

```bash
# 1. Backup config (ALWAYS do this first)
cp -r ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
cp -r ~/.openclaw/exec-approvals.json ~/.openclaw/exec-approvals.json.bak

# 2. Check changelog for breaking changes
openclaw changelog          # or visit https://openclaw.dev/changelog
# Look for: config key renames, removed fields, new required fields,
# permission model changes, plugin API changes

# 3. Note current version
openclaw --version
```

## Upgrade

```bash
# 4. Install new version
npm install -g openclaw@latest

# 5. Refresh gateway service token (required since 2026.4.1)
#    New versions may change internal auth — stale tokens cause
#    exec approval timeouts and tool call failures.
openclaw gateway install --force

# 6. Run doctor (auto-detects and suggests fixes)
openclaw doctor

# 7. Restart gateway
openclaw gateway restart
```

## Post-Upgrade Verification

```bash
# 8. Verify gateway is live
curl -s http://localhost:18789/health
# Expected: {"ok":true,"status":"live"}

# 9. Verify channels
openclaw channels status
# Both Telegram and WhatsApp should show "running"

# 10. Verify exec approvals
openclaw approvals get
# Should show: security=full, ask=off, askFallback=full

# 11. Check for skill warnings
openclaw doctor 2>&1 | grep -i "skip\|error\|warn"
# If you see "Skipping skill path that resolves outside its configured root":
#   find ~/.openclaw/skills -maxdepth 1 -type l | while read l; do
#     target=$(readlink "$l")
#     realpath "$l" 2>/dev/null | grep -q "^$HOME/.openclaw/skills" || echo "external: $l -> $target"
#   done
#   # Remove external symlinks that are no longer valid
```

## Rollback

If anything breaks:

```bash
# Restore config
cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json
cp ~/.openclaw/exec-approvals.json.bak ~/.openclaw/exec-approvals.json

# Downgrade
npm install -g openclaw@<previous-version>

# Restart
openclaw gateway install --force
openclaw gateway restart
```

## Known Issues by Version

### 2026.4.7

| Issue | Symptom | Fix |
|-------|---------|-----|
| `/allowlist` requires owner | `error: permission denied — owner required` when non-owner runs `/allowlist add` | Ensure only owner accounts manage allowlists; update automation that used non-owner accounts for this |
| Env override blocks | Workflows injecting Java/Rust/Git/Kubernetes/cloud credential env vars via model layer silently blocked | Move env var injection to `deploy.sh` or workspace config — out of model instruction path |
| `gateway config.apply` blocked from model | Runtime config patches via AI tool calls fail with `blocked: model-facing write` | Use direct gateway API calls with human approval for config changes |
| Docker bind change | Gateway now auto-binds to `0.0.0.0` inside containers | If you relied on loopback-only binding in Docker, set `bind: loopback` explicitly |

### 2026.4.5

| Issue | Symptom | Fix |
|-------|---------|-----|
| Legacy config aliases removed | Startup warning: `unknown config key: talk.voiceId` (or `talk.apiKey`, `agents.*.sandbox.perSession`, `browser.ssrfPolicy.allowPrivateNetwork`, `hooks.internal.handlers`) | Run `openclaw doctor --fix` to auto-migrate to canonical paths |
| Channel `allow` toggle removed | Warning about unrecognized `allow` field on channel/group/room config | Replace with `dmPolicy` + `allowFrom` — run `openclaw doctor --fix` |

### 2026.4.1

| Issue | Symptom | Fix |
|-------|---------|-----|
| Gateway embedded token stale | `exec approval followup dispatch failed: gateway timeout after 60000ms` | `openclaw gateway install --force` |
| Exec approvals empty defaults | Tools silently fail, agent can't execute commands | Set `exec-approvals.json` defaults to `security: full, ask: off` |
| Telegram dmPolicy default | `dmPolicy: "pairing"` blocks new contacts | Change to `"open"` + add `allowFrom: ["*"]` |
| Skill symlink security check | `Skipping skill path that resolves outside its configured root` (hundreds of warnings) | Remove external symlinks from `~/.openclaw/skills/` |
| Missing tools.profile | Tool calls may be restricted | Add `"tools": {"profile": "full"}` to `openclaw.json` |

## Re-Deploy (Nuclear Option)

If manual fixes aren't enough, re-deploy from template:

```bash
cd b2b-sdr-agent-template/deploy
./deploy.sh <client-name>
# This applies all fixes automatically (v3.3.1+)
```
