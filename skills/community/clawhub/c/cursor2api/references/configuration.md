# Configuration Reference

## OpenClaw Configuration

### Scenario A: OpenClaw & cursor2api on Same Machine

> ⚠️ Note: Local Node.js version defaults to port **3010** (not Docker's 3000)

Add to `~/.zshrc` or `~/.bashrc`:

```bash
export ANTHROPIC_BASE_URL="http://localhost:3010/v1"
export ANTHROPIC_API_KEY="your_workos_cursor_session_token"
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
```

Verify:
```bash
openclaw gateway restart
openclaw logs --tail 50
```

### Scenario B: cursor2api in Docker on Desktop, OpenClaw on Host

```bash
export ANTHROPIC_BASE_URL="http://host.docker.internal:3010/v1"
export ANTHROPIC_API_KEY="your_workos_cursor_session_token"
```

### Scenario C: cursor2api on Remote Server

```bash
export ANTHROPIC_BASE_URL="http://your-server-ip:3010/v1"
export ANTHROPIC_API_KEY="your_workos_cursor_session_token"
```

## Claude Code Configuration

```bash
# ~/.zshrc

cursor-proxy() {
  export ANTHROPIC_BASE_URL="http://localhost:3010/v1"
  export ANTHROPIC_AUTH_TOKEN="your_token"
  export ANTHROPIC_API_KEY="your_token"
  export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
  echo "✅ Claude Code → cursor2api"
}

cursor-reset() {
  unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN ANTHROPIC_API_KEY
  echo "✅ Claude Code → Official Anthropic API"
}

alias cursor-up='docker start cursor-api && cursor-proxy'
alias cursor-down='docker stop cursor-api && cursor-reset'
```

```bash
source ~/.zshrc
cursor-proxy     # Enable proxy
cursor-reset     # Switch back to official
```

## CC Switch Configuration

| Config Key | Value |
|------------|-------|
| **Provider Name** | `cursor2api` |
| **API Type** | `Anthropic` |
| **Base URL** | `http://localhost:3010/v1` |
| **API Key** | `WorkosCursorSessionToken` |
| **Model** | `claude-sonnet-4-6` |

JSON config:

```json
{
  "providers": {
    "cursor2api": {
      "type": "anthropic",
      "baseURL": "http://localhost:3010/v1",
      "apiKey": "your_token",
      "models": {
        "sonnet": "claude-sonnet-4-6",
        "opus": "claude-opus-4-20250514"
      }
    }
  },
  "activeProvider": "cursor2api"
}
```

## Environment File (~/.cursor2apirc)

```bash
CURSOR_API_URL="http://localhost:3010/v1"
CURSOR_TOKEN="your_workos_cursor_session_token"
CURSOR_MODEL="claude-sonnet-4-6"
```

```bash
source ~/.cursor2apirc
```

## Available Endpoints

| Endpoint | Format | Compatible With |
|----------|--------|-----------------|
| `http://localhost:3010/v1/messages` | Anthropic Messages API | OpenClaw, Claude Code |
| `http://localhost:3010/v1/chat/completions` | OpenAI Chat Completions | CC Switch, Universal |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Verify container: `docker ps \| grep cursor-api` |
| 401 Unauthorized | Token expired, refresh needed |
| 502 Bad Gateway | Container error, check: `docker logs cursor-api` |
