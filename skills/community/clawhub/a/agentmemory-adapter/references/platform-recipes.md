# Platform Recipes

## Durable Local Install

Use this when global npm is not writable or `npx` stalls:

```bash
npm install --prefix ~/.agentmemory/npm @agentmemory/agentmemory@0.9.22 --omit=optional
mkdir -p ~/.local/bin
ln -sfn ~/.agentmemory/npm/node_modules/.bin/agentmemory ~/.local/bin/agentmemory
```

Start the server in a long-lived terminal:

```bash
agentmemory
```

Verify:

```bash
curl -fsS http://localhost:3111/agentmemory/livez
curl -fsS http://localhost:3111/agentmemory/health
agentmemory status
agentmemory doctor --dry-run
```

## Codex MCP

```bash
codex mcp remove agentmemory 2>/dev/null || true
codex mcp add agentmemory \
  --env AGENTMEMORY_URL=http://localhost:3111 \
  --env AGENTMEMORY_TOOLS=all \
  -- ~/.local/bin/agentmemory mcp
```

If `agentmemory connect codex --with-hooks --force` is used, check whether it rewrote MCP back to `npx`; if so, re-run the `codex mcp add` recipe.

## Codex Plugin Skills

For a local marketplace:

```text
~/.agentmemory/codex-marketplace/
  .agents/plugins/marketplace.json
  plugins/agentmemory/
```

Marketplace entry:

```json
{
  "name": "agentmemory-local",
  "interface": { "displayName": "AgentMemory local" },
  "plugins": [
    {
      "name": "agentmemory",
      "source": { "source": "local", "path": "./plugins/agentmemory" },
      "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
      "category": "Memory"
    }
  ]
}
```

Patch `plugins/agentmemory/.mcp.json` to use the local command:

```json
{
  "mcpServers": {
    "agentmemory": {
      "command": "~/.local/bin/agentmemory",
      "args": ["mcp"],
      "env": {
        "AGENTMEMORY_URL": "http://localhost:3111",
        "AGENTMEMORY_TOOLS": "all"
      }
    }
  }
}
```

Install:

```bash
codex plugin marketplace add ~/.agentmemory/codex-marketplace
codex plugin add agentmemory@agentmemory-local
```

## OpenClaw MCP

```bash
openclaw mcp set agentmemory '{"command":"'"$HOME"'/.local/bin/agentmemory","args":["mcp"],"env":{"AGENTMEMORY_URL":"http://localhost:3111","AGENTMEMORY_TOOLS":"all"}}'
```

## OpenClaw Memory Plugin

Put the plugin in a durable path:

```bash
mkdir -p ~/.agentmemory
cp -a integrations/openclaw ~/.agentmemory/openclaw-plugin
openclaw plugins install -l ~/.agentmemory/openclaw-plugin
```

Expected config shape:

```json
{
  "plugins": {
    "load": { "paths": ["~/.agentmemory/openclaw-plugin"] },
    "entries": {
      "agentmemory": {
        "enabled": true,
        "config": {
          "base_url": "http://localhost:3111",
          "token_budget": 2000,
          "min_confidence": 0.5,
          "fallback_on_error": true,
          "timeout_ms": 5000
        }
      }
    },
    "slots": { "memory": "agentmemory" }
  }
}
```

Remove stale temp paths from `plugins.load.paths`; a duplicated plugin id can cause the wrong source to win.

## ClawHub Publishing

Do not publish without explicit owner/version approval. Keep the skill license and homepage explicit in the frontmatter.

Recommended review sequence:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py ./agentmemory-adapter
clawhub whoami
CLAWSCAN_NOTE="This skill configures a local AgentMemory MCP/server integration and may inspect local Codex/OpenClaw config files. It does not require credentials; AGENTMEMORY_SECRET is optional and must never be printed. Network access is limited to the user-configured AgentMemory URL and public package/registry endpoints when installing dependencies."
clawhub skill publish ./agentmemory-adapter --version 1.0.3 --clawscan-note "$CLAWSCAN_NOTE"
```

Recommended ClawScan note:

```text
This skill configures a local AgentMemory MCP/server integration and may inspect local Codex/OpenClaw config files. It does not require credentials; AGENTMEMORY_SECRET is optional and must never be printed. Network access is limited to the user-configured AgentMemory URL and public package/registry endpoints when installing dependencies.
```
