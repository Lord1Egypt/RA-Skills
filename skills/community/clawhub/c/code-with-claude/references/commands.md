# Commands

In-session commands. Type `/` to see all, or `/` + letters to filter.

## Built-in Commands

| Command | Purpose |
|---------|---------|
| `/add-dir <path>` | Add working directory for current session |
| `/agents` | Manage agent configurations |
| `/autofix-pr [prompt]` | Spawn web session to auto-fix PR CI failures and review comments |
| `/batch <instruction>` | **Skill.** Parallel large-scale changes across codebase (5-30 units) |
| `/btw <question>` | Side question without adding to conversation |
| `/chrome` | Configure Chrome integration |
| `/claude-api` | **Skill.** Load Claude API reference for your language |
| `/clear` | Clear conversation. Aliases: `/reset`, `/new` |
| `/color [color]` | Set prompt bar color for session |
| `/compact [instructions]` | Compact conversation with optional focus |
| `/config` | Open Settings. Alias: `/settings` |
| `/context` | Visualize context usage as colored grid |
| `/copy [N]` | Copy last response to clipboard. N for Nth-latest |
| `/cost` | Show token usage statistics |
| `/debug [description]` | **Skill.** Enable debug logging and troubleshoot |
| `/desktop` | Continue session in Desktop app. Alias: `/app` |
| `/diff` | Interactive diff viewer (uncommitted + per-turn diffs) |
| `/doctor` | Diagnose installation and settings |
| `/effort [level]` | Set effort: low/medium/high/max/auto |
| `/exit` | Exit CLI. Alias: `/quit` |
| `/export [filename]` | Export conversation as plain text |
| `/fast [on\|off]` | Toggle fast mode |
| `/feedback [report]` | Submit feedback. Alias: `/bug` |
| `/branch [name]` | Branch conversation at this point. Alias: `/fork` |
| `/help` | Show help |
| `/hooks` | View hook configurations |
| `/ide` | Manage IDE integrations |
| `/init` | Initialize project with CLAUDE.md |
| `/insights` | Analyze session patterns and friction points |
| `/install-github-app` | Set up Claude GitHub Actions |
| `/loop [interval] <prompt>` | **Skill.** Run prompt repeatedly on interval |
| `/mcp` | Manage MCP server connections |
| `/memory` | Edit CLAUDE.md memory files |
| `/model [model]` | Switch model |
| `/permissions` | Manage allow/ask/deny rules. Alias: `/allowed-tools` |
| `/plan [description]` | Enter plan mode |
| `/plugin` | Manage plugins |
| `/remote-control` | Make session available for remote control. Alias: `/rc` |
| `/rename [name]` | Rename session |
| `/resume [session]` | Resume conversation. Alias: `/continue` |
| `/rewind` | Rewind to checkpoint. Alias: `/checkpoint` |
| `/schedule [description]` | Cloud scheduled tasks |
| `/security-review` | Analyze branch changes for vulnerabilities |
| `/simplify [focus]` | **Skill.** Review changed files for reuse/quality/efficiency |
| `/skills` | List available skills |
| `/stats` | Visualize usage, streaks, model preferences |
| `/status` | Version, model, account, connectivity |
| `/tasks` | List/manage background tasks. Alias: `/bashes` |
| `/teleport` | Pull web session into terminal. Alias: `/tp` |
| `/theme` | Change color theme |
| `/ultraplan <prompt>` | Draft plan → review in browser → execute |
| `/voice` | Toggle push-to-talk voice dictation |

## MCP Prompts

MCP servers expose prompts as commands: `/mcp__<server>__<prompt>`. Dynamically discovered from connected servers.
