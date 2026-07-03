# agent-team-mesh

> Team-wide P2P mesh for [OpenClaw](https://docs.openclaw.ai) agents.
> Direct WebSocket calls between teammates' gateways — no broker, no central server.

## Why this skill exists

If your team runs OpenClaw agents on separate containers/pods (e.g. each
developer has their own personal agent), you eventually want them to talk
to each other:

- *"Forward this question to Bob's agent and bring back the answer"*
- *"Ping every agent on the team — who's online?"*
- *"Broadcast an FYI to all teammates' agents"*

Existing options are heavyweight: stand up a broker (Redis/Supabase), wire
auth/RLS, write polling scripts, etc.

This skill takes a simpler approach: each agent's OpenClaw Gateway already
listens on `:18789` over WebSocket. With per-agent tokens collected in a
shared file, you can just call them directly.

## Install

### Via [clawhub](https://clawhub.com)
```bash
clawhub install agent-team-mesh
```

### Via [skills.sh](https://skills.sh)
```bash
npx skills install agent-team-mesh
```

### Manual
```bash
git clone https://github.com/Songhonglei/better-agent-skills.git
cp -r better-agent-skills/skills/agent-team-mesh ~/.openclaw/skills/
```

## Quick start (3 steps)

1. **Edit `references/registry.json`** with your teammates' names, email
   prefixes, and pod IPs.

2. **Collect WS tokens** from each teammate (they generate via OpenClaw
   Gateway) and store in `~/.config/agent-team-mesh/tokens.json` chmod 600:

   ```json
   { "tokens": { "alice": "tok_xxx", "bob": "tok_yyy" } }
   ```

3. **Test**:
   ```bash
   ./scripts/agent-mesh.sh whoami     # who am I on this machine?
   ./scripts/agent-mesh.sh list       # what's the team look like?
   ./scripts/agent-mesh.sh send --to alice --message "are you alive?" --dry-run
   ```

## Commands

| Command | What it does |
|---|---|
| `whoami` | Show my detected identity (helps debug "who's me?") |
| `list` | Show all teammates with online/offline + token status |
| `ping --to <agent>` | TCP-level connectivity test (no message sent) |
| `send --to <agent> --message <msg>` | Send + wait for reply (incl. `--rounds`, `--timeout`, `--dry-run`) |
| `broadcast --message <msg>` | Send to all online teammates (excludes self) |
| `sync` | (stub) Pull the registry from your team source — see README |

## Security

- WS plaintext (`ws://`) — **only safe on trusted internal networks**
- Tokens are stored in a **separate** chmod 600 file, **never** in registry.json
- `.gitignore` bundled — token file won't be committed
- Soft (4KB) / hard (8KB) message size limits to prevent runaway prompts
- `whoami` failure aborts `broadcast` to prevent self-spam

## Identity detection (3 layers)

The script auto-detects "who am I" via:

1. `MESH_MY_EMAIL` env var
2. `USER.md` (OpenClaw workspace file, or `~/.config/agent-team-mesh/USER.md`)
3. `~/sso.json` (OpenClaw SSO token)

## Trigger phrases for AI agents

- "message my teammate's agent"
- "ping bob's agent"
- "broadcast to the team"
- 「给戴泽的 agent 发消息」「广播给全组」

## Requirements

- bash 4+, Python 3.8+ (stdlib), curl
- `openclaw` CLI on PATH
- Each teammate also runs `openclaw gateway` listening on `:18789`
- All agents on a routable network

## License

MIT — see [LICENSE](./LICENSE).

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
