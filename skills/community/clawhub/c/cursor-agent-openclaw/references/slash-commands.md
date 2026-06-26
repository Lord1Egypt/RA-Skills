# Cursor Agent — Slash Commands (Interactive Mode)

| Command | Description |
|---|---|
| `/plan` | Switch to Plan mode (read-only, design approach) |
| `/ask` | Switch to Ask mode (read-only, Q&A) |
| `/model <id>` | Switch model mid-session |
| `/max-mode [on\|off]` | Toggle Max Mode |
| `/auto-run [on\|off\|status]` | Toggle auto-run for commands |
| `/sandbox` | Configure sandbox / network access |
| `/compress` | Free up context window space |
| `/new-chat` | Start fresh session |
| `/resume <id>` | Resume a previous session |
| `/usage` | View Cursor quota/streaks |
| `/about` | Show version + account info |
| `/quit` | Exit |

## Context Selection (Interactive)

- `@<file>` — Add file to context
- `@<folder>` — Add folder to context
- Shift+Tab — Rotate between Agent / Plan / Ask modes
- Ctrl+R — Review changes before applying
