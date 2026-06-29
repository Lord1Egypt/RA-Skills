# create-rustchain-agent

**60-second onboarding for a RustChain-participating agent.** One command
scaffolds a working agent: an Ed25519 RTC wallet, a runnable `agent.py`, MCP
wiring for `rustchain-mcp`, and the path to claim the First-Light newcomer bounty.

```bash
uvx create-rustchain-agent my-agent
# or: pipx run create-rustchain-agent my-agent
cd my-agent && python agent.py
```

## What it generates
| File | Purpose |
|------|---------|
| `wallet.json` | Ed25519 RTC wallet (**private key inside; 0600 + gitignored**) |
| `agent.py` | checks node health + your balance; shows how to claim First-Light |
| `.mcp.json` | `rustchain-mcp` wired for Claude Code / Cursor / Cline |
| `README.md` | next steps + editor mcp-add snippets |
| `.gitignore` | excludes `wallet.json` |

## Safe by default
Scaffolding is **local only** — it generates files and a wallet, no network
writes. Pass `--register` to also register a Beacon identity (a network write).
Use `--node <url>` to point at a testnet first.

## The arc it sets up
1. **Scaffold** → you have a funded-capable wallet + a participating agent.
2. **Fund** → claim the First-Light newcomer bounty (paste your address).
3. **Spend** → `pip install clawrtc` and use `clawrtc tip/gas/pay` (the spend SDK).
4. **Mine** (optional) → `clawrtc install && clawrtc start` — real/vintage
   hardware earns Proof-of-Antiquity bonus multipliers.

Part of the [RustChain](https://rustchain.org) ecosystem.

## License
MIT © Elyan Labs.
