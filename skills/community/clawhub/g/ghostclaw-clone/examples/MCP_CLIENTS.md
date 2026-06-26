# Ghostclaw MCP Server — Client Configuration Examples

Ghostclaw provides an MCP (Model Context Protocol) server (`ghostclaw-mcp`) that can be integrated into various AI-enabled IDEs and clients.

This directory contains example configuration files for popular MCP clients.

---

## Claude Desktop

**File:** `claude_desktop_config.json`

Configuration for [Claude Desktop](https://claude.ai/download) (macOS/Windows).

### Setup

1. Open Claude Desktop settings (Cmd/Ctrl + ,)
2. Navigate to **Developer** → **Edit Config**
3. Add or merge the `mcpServers` section:

```json
{
  "mcpServers": {
    "ghostclaw": {
      "command": "ghostclaw-mcp",
      "args": [],
      "env": {
        "GHOSTCLAW_REPO_PATH": "/path/to/your/repo",
        "GHOSTCLAW_USE_QMD": "1"
      }
    }
  }
}
```

### Options

- `GHOSTCLAW_REPO_PATH`: Path to the repository to analyze (required if not set globally)
- `GHOSTCLAW_USE_QMD`: Set to `1` or `true` to enable QMD backend (optional)
- `GHOSTCLAW_API_KEY`: Your OpenRouter/OpenAI/Anthropic API key (if not set globally)

### After Configuration

Restart Claude Desktop. You should see Ghostclaw tools available:

- `ghostclaw_analyze`
- `ghostclaw_memory_search`
- `ghostclaw_memory_get_run`
- `ghostclaw_memory_list_runs`
- `ghostclaw_memory_diff_runs`
- `ghostclaw_knowledge_graph`
- `ghostclaw_refactor_plan`

---

## Cursor IDE

**File:** `cursor_mcp_config.json`

Configuration for [Cursor IDE](https://cursor.sh/) (which supports MCP via settings).

### Setup

1. Open Cursor settings (Cmd/Ctrl + Shift + J)
2. Go to **Features** → **MCP Servers**
3. Click **Add Server** and configure:

```json
{
  "name": "ghostclaw",
  "command": "ghostclaw-mcp",
  "args": [],
  "env": {
    "GHOSTCLAW_REPO_PATH": "/path/to/your/repo"
  }
}
```

Alternatively, edit the MCP config file directly (location varies by OS).

### Notes

- Cursor may require you to enable MCP in experimental features first.
- Ghostclaw tools will appear in the Cursor agent tool palette.

---

## VS Code (with MCP Extension)

**File:** `vscode_mcp_config.json`

Configuration for Visual Studio Code with an MCP extension (e.g., "MCP Client" by Microsoft or community).

### Setup

1. Install an MCP client extension from VS Code marketplace
2. Open extension settings (Cmd/Ctrl + , → search "MCP")
3. Add server configuration:

```json
{
  "mcpServers": {
    "ghostclaw": {
      "type": "stdio",
      "command": "ghostclaw-mcp",
      "args": [],
      "env": {
        "GHOSTCLAW_REPO_PATH": "${workspaceFolder}"
      }
    }
  }
}
```

### Using Workspace Variables

`${workspaceFolder}` automatically resolves to the currently opened project directory.

You can also set a fixed path if you always analyze the same repo.

---

## OpenCode

**File:** `opencode_mcp_config.yaml`

Configuration for [OpenCode](https://github.com/openclaw/opencode) agent framework (YAML format).

### Setup

1. Create or edit `opencode.yaml` in your project root:
2. Add an MCP server section:

```yaml
agents:
  - name: "ghostclaw"
    mcp_servers:
      - name: "ghostclaw"
        command: "ghostclaw-mcp"
        env:
          GHOSTCLAW_REPO_PATH: "."
          GHOSTCLAW_USE_QMD: "true"
    tools:
      - "ghostclaw_analyze"
      - "ghostclaw_memory_search"
      - "ghostclaw_refactor_plan"
```

### Notes

- OpenCode will spawn the MCP server as a subprocess.
- Tools become available to the agent automatically.
- Use `${PWD}` or relative paths for repo location.

---

## Antigravity (MCP Shell)

**File:** `antigravity_config.json`

Configuration for [Antigravity](https://antigravity.io/) or other MCP-compatible shells.

### Setup

In your Antigravity MCP server config:

```json
{
  "servers": [
    {
      "name": "ghostclaw",
      "command": "ghostclaw-mcp",
      "transport": "stdio",
      "env": {
        "GHOSTCLAW_REPO_PATH": "/absolute/path/to/repo"
      }
    }
  ]
}
```

---

## Generic MCP Client (stdin/stdout)

Any MCP client that supports stdio can use Ghostclaw by invoking:

```bash
ghostclaw-mcp
```

Set environment variables as needed:

```bash
export GHOSTCLAW_REPO_PATH="/path/to/repo"
export GHOSTCLAW_USE_QMD="1"
ghostclaw-mcp
```

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GHOSTCLAW_REPO_PATH` | Path to repository to analyze | Yes (unless configured per-client) |
| `GHOSTCLAW_USE_QMD` | Enable QMD backend (`1`, `true`) | No |
| `GHOSTCLAW_API_KEY` | API key for AI synthesis (if `use_ai` enabled) | Only if AI used and not in config |
| `GHOSTCLAW_LOG_LEVEL` | Logging level (`DEBUG`, `INFO`, `WARNING`) | No |
| `GHOSTCLAW_MCP_DEBUG` | Enable MCP debug logging (`1`) | No |

---

## Troubleshooting

### "Command not found: ghostclaw-mcp"

Ensure Ghostclaw is installed and the `ghostclaw-mcp` script is in your PATH:

```bash
which ghostclaw-mcp
# If not found, install: pip install ghostclaw
# Or run from source: python -m ghostclaw_mcp.server
```

### Tools not appearing in client

- Check the MCP server logs for errors during initialization.
- Ensure `ghostclaw-mcp` runs without errors from the command line.
- Verify the `repo_path` exists and is a git repository.

### Ghost Engine fails (API key missing)

If you try to use AI synthesis (`ghostclaw_analyze` with `use_ai`), set `GHOSTCLAW_API_KEY` or add it to your global config (`~/.ghostclaw/ghostclaw.json`).

### Delta mode not working in MCP

The `ghostclaw_analyze` tool currently performs a full analysis. Delta mode can be triggered by passing CLI flags in the `args` array of the MCP server config:

```json
{
  "command": "ghostclaw-mcp",
  "args": ["--delta", "--base", "HEAD~1"]
}
```

(Note: This applies to all analyses; for per-call delta, you'll need to enhance the MCP tool arguments in a future version.)

---

## Advanced: Custom Server Arguments

You can pass additional CLI flags to `ghostclaw-mcp` via the `args` array:

```json
{
  "command": "ghostclaw-mcp",
  "args": ["--log-level", "DEBUG", "--no-cache"]
}
```

This affects all tools provided by this server instance.

---

## See Also

- **MCP Tools Reference**: See `src/ghostclaw_mcp/server.py` for available tools and parameters.
- **Ghostclaw Docs**: `README.md`, `docs/`
- **MCP Specification**: https://modelcontextprotocol.io/

---

**Last updated:** 2026-03-12 (Ghostclaw v0.2.0)
