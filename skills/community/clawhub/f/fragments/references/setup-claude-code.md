# Setup — Claude Code

## Language

Communicate with the user in their current conversation language.
Each step requires user confirmation before proceeding.
Sensitive values (PAT token) are written to local config only, never echoed.

## Setup Steps

### Step 1: Verify Memos Service

Check reachability of the Memos server.

- Ask the user for their Memos instance URL.
- Test connectivity: call `memos_list_tags` if MCP is already configured,
  otherwise use Bash to run: `curl -sf <site_url>/api/v1/status` (macOS/Linux)
  or `Invoke-WebRequest -Uri <site_url>/api/v1/status` (Windows PowerShell).
- If unreachable, ask user to verify the URL and that the Memos server is running.

### Step 2: Configure PAT Token

Ask the user for their Memos Personal Access Token (format: `memos_pat_*`).

Write `~/.config/fragments.json`:

```json
{
  "pat_token": "<user_provided_token>",
  "site_url": "<confirmed_url>",
  "mcp_url": "<confirmed_url>/mcp"
}
```

Paths:
- macOS / Linux: `~/.config/fragments.json`
- Windows: `%USERPROFILE%\.config\fragments.json`

Ensure the `.config` directory exists before writing.

### Step 3: Configure MCP

Read the MCP template from `assets/claude-code/mcp.json` in this skill directory.
Substitute `{{MCP_URL}}` and `{{PAT_TOKEN}}` with values from `fragments.json`.

Merge the resulting config into the project's `.mcp.json` file (create if absent).
Preserve any existing MCP server entries — only add or update the `memos` entry.

### Step 4: Install Hooks (Optional)

For automatic daily-log prompting after sessions:

Read the hooks template from `assets/claude-code/hooks.json` in this skill directory.

Merge into `~/.claude/settings.json` under the `hooks` key.
- If `hooks.Stop` already exists, append to the array (do not overwrite existing hooks).
- If `hooks` key is absent, create it.

### Step 5: Verify

Call `memos_list_tags` via MCP.
- Success → setup complete.
- Failure → review previous steps, check token validity and URL.

## Platform Paths

| Item | macOS / Linux | Windows |
|------|--------------|---------|
| Config | `~/.config/fragments.json` | `%USERPROFILE%\.config\fragments.json` |
| Claude settings | `~/.claude/settings.json` | `%USERPROFILE%\.claude\settings.json` |
| Project MCP | `.mcp.json` in project root | `.mcp.json` in project root |
| Python | `python3` / `pip3` | `py` / `pip` |
