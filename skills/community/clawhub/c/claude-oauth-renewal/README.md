# Claude OAuth Renewal — OpenClaw Skill

Automatically detect and renew expired [Claude Code](https://docs.anthropic.com/en/docs/claude-code) OAuth tokens via [OpenClaw](https://github.com/openclaw/openclaw) heartbeat. Prevents agent downtime caused by token expiration.

## How It Works

```
Heartbeat → check-claude-oauth.sh
  │
  ├─ Token OK (>6h) → silent exit
  │
  ├─ Tier 1: claude auth status (refresh token auto-renew)
  │   └─ Handles most cases silently
  │
  ├─ Tier 2: Chrome browser automation
  │   ├─ Start claude auth login → opens browser
  │   ├─ osascript clicks "Authorize" on claude.ai
  │   ├─ Extracts auth code from callback page
  │   └─ Feeds code back to CLI via expect
  │
  └─ Tier 3: Alert user via agent channel
```

## Requirements

| Dependency | Purpose |
|-----------|---------|
| macOS | Keychain token storage |
| Claude Code | `claude` CLI authenticated |
| python3 | Token expiry parsing |
| Google Chrome | Tier 2 browser automation |
| expect | CLI interaction automation |

**Chrome setup (for Tier 2):** View → Developer → Allow JavaScript from Apple Events

## Install

```bash
# In your OpenClaw workspace
cp -r skills/claude-oauth-renewal/scripts/check-claude-oauth.sh scripts/
chmod +x scripts/check-claude-oauth.sh
```

Add to `HEARTBEAT.md`:

```markdown
0. Run `bash scripts/check-claude-oauth.sh` — if output, relay as P0 alert
```

## Test

```bash
# Normal check (silent if healthy)
bash scripts/check-claude-oauth.sh

# Force trigger (set threshold higher than remaining hours)
WARN_HOURS=24 bash scripts/check-claude-oauth.sh
```

## Configuration

| Env Variable | Default | Description |
|-------------|---------|-------------|
| `WARN_HOURS` | `6` | Hours before expiry to start renewal |

## Token Details

Claude Code stores OAuth credentials in macOS Keychain:

- **Service:** `Claude Code-credentials`
- **Key fields:** `accessToken`, `refreshToken`, `expiresAt` (ms timestamp)
- **Read:** `security find-generic-password -s "Claude Code-credentials" -g`

> Note: Uses `-g` flag and regex extraction because `-w` truncates long JSON values.

## License

MIT
