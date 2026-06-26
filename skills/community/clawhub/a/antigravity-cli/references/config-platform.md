# Configuration and Platform

## CLI vs Antigravity 2.0

Antigravity CLI is the terminal-first TUI surface. It is optimized for speed, keyboard-heavy local iteration, SSH, tmux, terminal multiplexers, and low resource overhead.

Antigravity 2.0 is the visual desktop editor/IDE surface. It is optimized for visual orchestration, multi-panel project management, and richer artifact review.

Both surfaces share the same agent harness, so improvements to reasoning, tool use, and code comprehension apply across both.

## Local files

| Purpose | Path |
| --- | --- |
| Settings | `~/.gemini/antigravity-cli/settings.json` |
| Keybindings | `~/.gemini/antigravity-cli/keybindings.json` |
| MCP config | `~/.gemini/antigravity-cli/mcp_config.json` |
| Conversations | `~/.gemini/antigravity-cli/conversations/` |
| History | `~/.gemini/antigravity-cli/history.jsonl` |

Prefer TUI editors before direct JSON edits:

- `/config` or `/settings`
- `/permissions`
- `/model`
- `/keybindings`
- `/mcp`

## Common settings keys

Use `/config` first. If editing JSON directly, validate syntax before restarting the CLI.

Common keys:

- `colorScheme`: terminal theme such as `terminal`, `light`, `dark`, `tokyo night`, or accessibility variants.
- `altScreenMode`: terminal buffer behavior.
- `toolPermission`: permission preset such as `request-review`, `proceed-in-sandbox`, `always-proceed`, or `strict`.
- `artifactReviewPolicy`: artifact approval behavior such as `asks-for-review`, `agent-decides`, or `always-proceed`.
- `enableTerminalSandbox`: enable native terminal sandbox containment.

## Skills paths

| Scope | Path |
| --- | --- |
| Global shared | `~/.gemini/antigravity-cli/skills/` |
| Workspace project | `.agents/skills/` |

## Platform notes

- Antigravity CLI is the lightweight TUI surface sharing the same agent core as Antigravity 2.0.
- Preferences, permissions, and security config synchronize between CLI and Antigravity 2.0.
- Active CLI conversations can be exported to Antigravity 2.0 for visual orchestration.
- Native SSH, tmux, and terminal multiplexer workflows are supported for headless/server use.
- The main agent controls which tools and permissions subagents receive, including MCP tool access and file write capabilities.

## Auth and first launch

- First launch prompts for color scheme, rendering mode, and workspace trust.
- Auth uses OS native keyring where available, such as Apple Keychain or Linux Secret Service.
- Browser OAuth is the fallback.
- SSH sessions may use manual URL authorization: print URL, open in browser, paste code back.
- Exit prints the exact resume command, such as `agy --continue` or `agy --conversation <id>`.

## Plugins, skills, hooks, and MCP

Plugins are installed under:

```text
~/.gemini/antigravity-cli/plugins/<plugin_name>/
```

A plugin can include:

- `plugin.json`
- `mcp_config.json`
- `hooks.json`
- `skills/`
- `agents/`
- `rules/`

Use `agy plugin` or `agy plugins` subcommands to list, install, enable, disable, validate, and uninstall plugins.

Skills become slash commands in the TUI. Workspace-local skills live in `.agents/skills/`; global skills live in `~/.gemini/antigravity-cli/skills/`.

Hooks can run pre-flight or post-generation checks and can be inspected with `/hooks`.

MCP configuration:

- Global: `~/.gemini/antigravity-cli/mcp_config.json`
- Workspace: `.agents/mcp_config.json`

Use `/mcp` to inspect server status, reload configs, and check connection logs. For remote SSE or websocket MCP connections, prefer the documented `serverUrl` field over legacy URL keys.

## Migration and docs

- Migration from Gemini CLI: `agy plugin import gemini`.
- Migrating from Gemini CLI: https://antigravity.google/docs/gcli-migration
- CLI reference: https://antigravity.google/docs/cli-reference
- CLI features: https://antigravity.google/docs/cli-features
- Using AGY CLI: https://antigravity.google/docs/cli-using
- Prompting and interaction: https://antigravity.google/docs/cli-prompting
- Reviewing artifacts: https://antigravity.google/docs/cli-artifacts
- Plugins and skills: https://antigravity.google/docs/cli-plugins
- Permissions: https://antigravity.google/docs/cli-permissions
- Sandbox: https://antigravity.google/docs/cli-sandbox
- Best practices: https://antigravity.google/docs/cli-best-practices
