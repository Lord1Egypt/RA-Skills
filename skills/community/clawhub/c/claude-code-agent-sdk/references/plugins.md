# Plugins in the SDK

> Load custom plugins via the Agent SDK to extend Claude Code with commands, agents, skills, and hooks.

Plugins are extension packages that can include skills, agents, hooks, and MCP servers.

## Plugin Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin manifest
├── skills/                   # Agent Skills
│   └── my-skill/
│       └── SKILL.md
├── commands/                 # Legacy format (new plugins use skills/)
├── agents/                   # Custom agents
├── hooks/                    # Event handlers
└── .mcp.json                # MCP server definitions
```

`commands/` is the legacy format. New plugins use `skills/`, and Claude Code continues to support both formats for backward compatibility.

## Loading Plugins

The SDK only supports `type: "local"`, loading from local filesystem paths.

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Hello",
  options: {
    plugins: [
      { type: "local", path: "./my-plugin" },
      { type: "local", path: "/absolute/path/to/another-plugin" }
    ]
  }
})) { /* ... */ }
```

```python
from claude_agent_sdk import query, ClaudeAgentOptions

options = ClaudeAgentOptions(
    plugins=[
        {"type": "local", "path": "./my-plugin"},
        {"type": "local", "path": "/absolute/path/to/another-plugin"},
    ]
)
```

Paths can be relative (to cwd) or absolute, and should point to the root directory containing `.claude-plugin/plugin.json`.

## Verifying Installation

```typescript
if (message.type === "system" && message.subtype === "init") {
  console.log("Plugins:", message.plugins);
  console.log("Commands:", message.slash_commands);
  // Example: [{ name: "my-plugin", path: "./my-plugin" }]
}
```

## Using Plugin Skills

Plugin skills use namespace: `plugin-name:skill-name`

```typescript
query({
  prompt: "/my-plugin:greet",  // Namespaced plugin skill
  options: { plugins: [{ type: "local", path: "./my-plugin" }] }
})
```

## Common Use Cases

**Development testing**: `plugins: [{ type: "local", path: "./dev-plugins/my-plugin" }]`

**Project-specific extensions**: `plugins: [{ type: "local", path: "./project-plugins/team-workflows" }]`

**Multiple sources**: Combine plugins from different locations

## Troubleshooting

| Issue | Check |
|:---|:---|
| Plugin not loaded | Path points to root directory (contains `.claude-plugin/`), valid JSON syntax, file permissions |
| Skills not appearing | Use `plugin-name:skill-name` namespace, verify `slash_commands` list, ensure `skills/<name>/SKILL.md` exists |
| Path resolution issues | Relative paths resolve from cwd, consider using absolute paths |

**CLI-installed plugins**: Plugins installed via `/plugin install` live in `~/.claude/plugins/` and can be loaded in the SDK with absolute paths.