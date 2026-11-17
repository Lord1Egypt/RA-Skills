# RPC and Alchemy

For EVM reads, choose the required chain and explicit endpoint before collecting balances or contract state. Pin comparable reads to the same block. A recent block does not prove finality, archive support, simulation support or provider independence. Verify these separately when the task needs them; public fallbacks must agree on chain ID and have their own rate limits.

Alchemy offers both a hosted MCP and an official CLI. The [MCP documentation](https://www.alchemy.com/docs/alchemy-mcp-server) specifies Streamable HTTP at `https://mcp.alchemy.com/mcp`, with OAuth 2.1 PKCE. Do not invent an API-key header for that connection. Use `select_app` before RPC/data tools. The server includes account administration, wallet submission and session creation, so connection alone must not expose every tool as an approved read.

The [CLI documentation](https://www.alchemy.com/docs/alchemy-cli) supports `ALCHEMY_API_KEY` and `ALCHEMY_NETWORK` for direct API access. These are distinct from MCP OAuth. For scripts, use `--json --no-interactive`; the installed CLI's `agent-prompt` and help describe its actual surface. Verified package: `@alchemy/cli@0.24.0`, Node 22 or later.

```bash
alchemy --json --no-interactive evm network list --search base
alchemy --json --no-interactive evm block latest --network base-mainnet
alchemy --json --no-interactive agent-prompt
```

An operator can authorize browser login with `alchemy auth`, or remote login with `alchemy auth login --device-code`. Do not print an API key or use `--reveal` in agent diagnostics. `DEFI_RPC_URL` is this pack's endpoint variable, not an Alchemy-defined variable; store the selected full URL privately rather than passing it in command arguments.
