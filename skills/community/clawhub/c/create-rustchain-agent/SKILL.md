# create-rustchain-agent

**60-second onboarding for a RustChain-participating agent.** One command
scaffolds a working agent: an Ed25519 RTC wallet, a runnable `agent.py`, MCP
wiring for `rustchain-mcp`, and the path to claim the First-Light bounty.

## Use
```
uvx create-rustchain-agent my-agent
cd my-agent && python agent.py
```

## Capabilities
- Generates an Ed25519 RTC wallet (0600, gitignored)
- Writes `.mcp.json` wiring rustchain-mcp for Claude Code / Cursor / Cline
- Emits a runnable agent that checks node health + balance + First-Light bounty
- `--register` registers a Beacon identity; `--node` targets a testnet

## Limitations
Scaffolding is local-only by default (no network writes unless `--register`).
Requires `cryptography`.

Part of the RustChain ecosystem · pip: create-rustchain-agent · MIT.
