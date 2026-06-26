# Setup — OpenClaw

## Language

Communicate with the user in their current conversation language.
Each step requires user confirmation before proceeding.
Sensitive values (PAT token) are written to local config only, never echoed.

## Setup Steps

### Step 1: Verify Memos Service

Check reachability of the Memos server.

- Ask the user for their Memos instance URL.
- Test connectivity: use Bash to run `curl -sf <site_url>/api/v1/status` (macOS/Linux)
  or `Invoke-WebRequest -Uri <site_url>/api/v1/status` (Windows PowerShell).
- If unreachable, ask user to verify the URL and that the Memos server is running.

### Step 2: Configure Environment Variables

Ask the user for their Memos Personal Access Token (format: `memos_pat_*`).

Add to `~/.openclaw/config.json` under `env`:

```json
{
  "env": {
    "MEMOS_URL": "<confirmed_url>",
    "MEMOS_PAT": "<user_provided_token>"
  }
}
```

Paths:
- macOS / Linux: `~/.openclaw/config.json`
- Windows: `%USERPROFILE%\.openclaw\config.json`

Ensure the `.openclaw` directory exists before writing.

### Step 3: Configure MCP

Read `assets/openclaw/mcp.json` in this skill directory.
Substitute `{{MEMOS_URL}}` and `{{MEMOS_PAT}}` with the environment variable references.

Merge the resulting config into `~/.openclaw/openclaw.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "memos": {
      "type": "http",
      "url": "${MEMOS_URL}/mcp",
      "headers": {
        "Authorization": "Bearer ${MEMOS_PAT}"
      }
    }
  }
}
```

OpenClaw resolves `${MEMOS_URL}` and `${MEMOS_PAT}` from the `env` section.

### Step 4: Install Hook (Optional)

For automatic daily-log prompting after sessions:

1. Create hook directory: `~/.openclaw/hooks/fragments-daily-log/`
2. Copy `assets/openclaw/hook/HOOK.md` to that directory.
3. Enable the hook:

```bash
openclaw hooks enable fragments-daily-log
```

4. Restart the gateway:

```bash
openclaw gateway restart
```

### Step 5: Verify

Call `memos_list_tags` via MCP. Confirm success.

## Platform Paths

| Item | macOS / Linux | Windows |
|------|--------------|---------|
| OpenClaw config | `~/.openclaw/config.json` | `%USERPROFILE%\.openclaw\config.json` |
| OpenClaw MCP config | `~/.openclaw/openclaw.json` | `%USERPROFILE%\.openclaw\openclaw.json` |
| OpenClaw hooks | `~/.openclaw/hooks/` | `%USERPROFILE%\.openclaw\hooks\` |

## Configuration File Structure

### ~/.openclaw/config.json

```json
{
  "env": {
    "MEMOS_URL": "https://your-memos-instance.com",
    "MEMOS_PAT": "memos_pat_xxx"
  }
}
```

### ~/.openclaw/openclaw.json (MCP section)

```json
{
  "mcpServers": {
    "memos": {
      "type": "http",
      "url": "${MEMOS_URL}/mcp",
      "headers": {
        "Authorization": "Bearer ${MEMOS_PAT}"
      }
    }
  }
}
```
