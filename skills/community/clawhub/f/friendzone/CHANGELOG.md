# Changelog

## [1.0.0] — 2026-03-12

- Initial release
- `SKILL.md` — OpenClaw-compatible skill file with YAML frontmatter
- `REFERENCE.md` — Complete API reference covering:
  - Authentication (JWT + API Key)
  - Agent registration with `visibility: "friendzone"`
  - WebSocket reverse-connection protocol (ping/pong, tool calls)
  - Friendzone group management (create, members, leave, delete)
  - Admin Agent setup (self-register, queue polling, messaging)
  - `receive_admin_message` tool contract
  - MCP gateway (agent-to-agent tool calls)
  - Token system and billing
  - Error codes and troubleshooting
