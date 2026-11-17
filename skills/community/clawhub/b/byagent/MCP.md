# byagent MCP (stdio)

Agent-fetchable surface for byagent: list/get artifacts and work comments via MCP tools. Implements the library half of the skill (CLI remains the publisher for now).

Server lives in the private app repo: [`anup-a/artifacts`](https://github.com/anup-a/artifacts) → `cmd/byagent-mcp`  
Tracking: [artifacts#29](https://github.com/anup-a/artifacts/issues/29) · PR: [artifacts#31](https://github.com/anup-a/artifacts/pull/31)

## Tools (P0)

| Tool | Purpose |
| --- | --- |
| `artifact_list` | List workspace artifacts (`limit`, `cursor`, `project`, `end_user`) |
| `artifact_get` | Get one artifact by id |
| `artifact_comments` | List threads (`status`: open \| resolved \| all) |
| `artifact_reply` | Owner reply `{ body }` |
| `artifact_resolve` | Resolve a thread |
| `collection_list` | Every project label as a collection, most recently active first |
| `collection_get` | One collection's artifacts in reading order |
| `brief_get` | A collection's brief (`byagent brief push`): Markdown, url, version, open comments |

**No full-text search tool.** Filter with `project` / `end_user` on list only.  
**Publish** stays on the CLI (`byagent publish`, `byagent brief push`) until MCP publish ships.

## Auth

Same keys as the CLI — create one at https://app.byagent.dev/app/keys:

```bash
export ARTIFACTS_API=https://app.byagent.dev
export ARTIFACTS_TOKEN=…          # or BYAGENT_API_KEY
# or: byagent login → ~/.artifacts/config.json
```

## Build

```bash
git clone git@github.com:anup-a/artifacts.git   # private
cd artifacts
go build -o "$HOME/bin/byagent-mcp" ./cmd/byagent-mcp
```

Put the binary on your `PATH`, or use an absolute path in the configs below.

## Claude Code

```bash
claude mcp add byagent --env ARTIFACTS_TOKEN=… --env ARTIFACTS_API=https://app.byagent.dev -- byagent-mcp
```

Or in `~/.claude.json` / project `.mcp.json`:

```json
{
  "mcpServers": {
    "byagent": {
      "command": "byagent-mcp",
      "env": {
        "ARTIFACTS_TOKEN": "YOUR_KEY",
        "ARTIFACTS_API": "https://app.byagent.dev"
      }
    }
  }
}
```

## Cursor

Settings → MCP, or `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "byagent": {
      "command": "byagent-mcp",
      "env": {
        "ARTIFACTS_TOKEN": "YOUR_KEY",
        "ARTIFACTS_API": "https://app.byagent.dev"
      }
    }
  }
}
```

## Codex

In `~/.codex/config.toml`:

```toml
[mcp_servers.byagent]
command = "byagent-mcp"

[mcp_servers.byagent.env]
ARTIFACTS_TOKEN = "YOUR_KEY"
ARTIFACTS_API = "https://app.byagent.dev"
```

## Notes

- Stdio only for P0; hosted HTTP MCP later.
- Never paste API keys into chat; use env / config file.
