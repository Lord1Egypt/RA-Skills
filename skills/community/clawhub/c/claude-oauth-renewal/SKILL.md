---
name: claude-oauth-renewal
description: "Automatically detect and renew expired Claude Code OAuth tokens via heartbeat. 3-tier renewal: refresh token → Chrome browser automation → user alert."
homepage: https://github.com/anthropics/claude-code
metadata: { "openclaw": { "emoji": "🔑", "requires": { "bins": ["claude", "security", "python3"], "platform": "macos" } } }
---

# Claude Code OAuth Auto-Renewal

Automatically detect and renew expired Claude Code OAuth tokens during OpenClaw heartbeat cycles. Prevents agent downtime caused by token expiration.

## When to Use

✅ **USE this skill when:**

- Your OpenClaw agent uses Claude Code as the AI provider
- You want uninterrupted agent operation without manual token renewal
- You're running OpenClaw on macOS with Chrome browser

## How It Works

### 3-Tier Renewal Strategy

```
Heartbeat triggers check-claude-oauth.sh
  │
  ├─ Token healthy (>6h remaining) → silent exit ✓
  │
  ├─ Tier 1: claude auth status (refresh token)
  │   ├─ Success → silent exit ✓
  │   └─ Fail ↓
  │
  ├─ Tier 2: Browser automation (osascript + Chrome JXA)
  │   ├─ Start claude auth login
  │   ├─ Auto-click "Authorize" on claude.ai
  │   ├─ Extract auth code from callback page
  │   ├─ Feed code back to CLI via expect
  │   ├─ Success → silent exit ✓
  │   └─ Fail ↓
  │
  └─ Tier 3: Alert user → agent notifies via configured channel
```

### Token Storage

Claude Code stores OAuth tokens in **macOS Keychain** under the service name `Claude Code-credentials`. The token JSON includes:

- `accessToken` — API access token (prefix `sk-ant-oat01-`)
- `refreshToken` — Used for automatic renewal (prefix `sk-ant-ort01-`)
- `expiresAt` — Unix timestamp in milliseconds

### Prerequisites

1. **macOS** with `security` CLI (Keychain access)
2. **Claude Code** installed and previously authenticated
3. **Google Chrome** with `View → Developer → Allow JavaScript from Apple Events` enabled (for Tier 2)
4. **python3** available in PATH
5. **expect** available (ships with macOS)

## Setup

### 1. Copy the script

```bash
cp skills/claude-oauth-renewal/scripts/check-claude-oauth.sh scripts/check-claude-oauth.sh
chmod +x scripts/check-claude-oauth.sh
```

### 2. Add to HEARTBEAT.md

Add as the first step in your heartbeat execution:

```markdown
## Execution Order

0. Run `bash scripts/check-claude-oauth.sh` — if output exists, relay as highest priority alert
1. (your other heartbeat checks...)
```

### 3. Test

```bash
# Normal check (silent if token healthy)
bash scripts/check-claude-oauth.sh

# Force trigger by setting high threshold
WARN_HOURS=24 bash scripts/check-claude-oauth.sh
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `WARN_HOURS` | `6` | Hours before expiry to start renewal attempts |

## Troubleshooting

### "无法读取 Claude Code token"
- Run `claude auth login` manually to establish initial credentials
- Verify keychain access: `security find-generic-password -s "Claude Code-credentials" -a "$(whoami)" -g`

### Tier 2 (browser automation) not working
- Enable Chrome JXA: `View → Developer → Allow JavaScript from Apple Events`
- Or via CLI: `defaults write com.google.Chrome AppleScriptEnabled -bool true` (restart Chrome)
- Ensure you're logged into claude.ai in Chrome

### JSON parsing errors
- The script uses regex extraction (not `json.loads`) to handle truncated keychain output
- If `security -w` truncates long values, the `-g` flag is used as fallback

## Notes

- Tier 1 (refresh token) handles most cases silently
- Tier 2 (browser) is only needed when refresh token itself expires (typically weeks)
- Tier 3 (alert) is the last resort when no automated renewal is possible
- The script never stores or logs actual token values
