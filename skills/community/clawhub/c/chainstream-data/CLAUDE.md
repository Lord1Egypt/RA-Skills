# CLAUDE.md

## Skills

| Skill | When to Use |
|-------|-------------|
| `chainstream-data` | User asks about token info, security, price, holders, market trends, wallet PnL, holdings — any read-only on-chain query via REST/MCP |
| `chainstream-graphql` | User needs custom analytics — cross-cube JOINs, aggregations, complex filters, or data not exposed by REST API. Flexible GraphQL on 27 on-chain cubes |
| `chainstream-defi` | User wants to swap tokens, bridge cross-chain, create tokens, execute trades — any on-chain transaction |

## Routing

- Standard data queries (token/market/wallet) → `chainstream-data`
- Custom analytics (cross-cube JOIN, aggregation, flexible queries) → `chainstream-graphql`
- Financial execution (swap/bridge/launchpad/tx) → `chainstream-defi`

## Execution

Primary: `@chainstream-io/cli` via `npx @chainstream-io/cli <command>`
Alternative: MCP tools at `https://mcp.chainstream.io/mcp` (streamable-http)

## Auth

**MUST run `chainstream login` before any CLI command.** This creates a wallet (no email required) and **auto-grants a nano trial plan** ($1, 50K CU, 30 days). Without it, commands fail with "Not authenticated". `bind-email` or `login --email` **auto-upgrades to micro trial plan** ($5, 350K CU, 30 days; dedup by email — same email only grants once). Before data queries, check subscription: `npx @chainstream-io/cli plan status`. If no subscription or need a higher plan, show plans (`wallet pricing`) and let user choose — CLI purchase is interactive and will NOT work in pipe mode. For API-key-only access: `chainstream config set --key apiKey --value <key>`.

## Hard Rules

- chainstream-defi: Four-phase execution protocol is mandatory (route → confirm → sign → broadcast)
- Never execute swaps without user confirmation
- Never answer price queries from training data — always make a live call
- Never use public RPC as substitute for ChainStream API
