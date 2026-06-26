# ChainStream AI Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

On-chain data intelligence and DeFi execution for AI agents across Solana, BSC, and Ethereum.

## Skills

| Skill | Coverage | Pattern |
|-------|----------|---------|
| [chainstream-data](chainstream-data/) | Token search, market trending, wallet PnL, WebSocket | Tool |
| [chainstream-graphql](chainstream-graphql/) | Custom GraphQL queries, cross-cube JOINs, aggregations, 25 on-chain cubes (3 chain groups) | Tool |
| [chainstream-defi](chainstream-defi/) | Token swap, cross-chain bridge, launchpad, transaction broadcast | Process |

## When to Use Which

```
User intent involves reading data?
  Standard queries (token info, market trends, wallet analysis)?
    → chainstream-data (REST API / MCP — pre-built endpoints)
  Custom analytics (cross-cube JOIN, aggregation, complex filters)?
    → chainstream-graphql (GraphQL — flexible queries on 25 cubes in 3 chain groups)

User intent involves executing a transaction?
  → chainstream-defi (swap, bridge, create token, send tx)
```

## Installation

### Cursor

Skills are automatically discovered via `.cursor-plugin/` configuration. Install the CLI:

```bash
npx @chainstream-io/cli login
```

### Claude Code

```
/plugin install chainstream
```

### Codex

See [.codex/INSTALL.md](.codex/INSTALL.md).

### OpenCode

See [.opencode/INSTALL.md](.opencode/INSTALL.md).

### Gemini CLI

```bash
gemini extensions install https://github.com/chainstream-io/skills
```

## Authentication

**IMPORTANT: Run `chainstream login` before any CLI command.** This creates a wallet and enables authentication. Without it, all commands will fail with "Not authenticated".

| Method | Command | Use Case |
|--------|---------|----------|
| Wallet (default) | `chainstream login` | Creates ChainStream Wallet (TEE), no email needed. **Run this first.** |
| Import key | `chainstream wallet set-raw --chain base` (EVM) or `--chain sol` (Solana) | Use your own private key |
| Email login | `chainstream login --email user@example.com` | Recover wallet on new device |
| Bind email | `chainstream bind-email user@example.com` | Optional, for account recovery |
| API Key | `chainstream config set --key apiKey --value <key>` | Read-only, dashboard users |
| x402 (USDC) | Interactive on 402 | CLI prompts for plan selection, pays with USDC (Base/Solana). Quota is in **CU (Compute Units)**, not call count |
| x402 → API Key | Interactive on 402 | Same as above — also returns API Key for MCP/SDK use |

> **Free trial**: `chainstream login` auto-grants a nano plan ($1, 50K CU, 30 days). `bind-email` or `login --email` auto-upgrades to micro plan ($5, 350K CU, 30 days). Dedup by email — same email only grants once. No manual purchase needed for trial.

## Usage Examples

Natural language prompts you can send to any AI assistant with ChainStream skills:

```
search for meme tokens on Solana
is <token_address> safe to buy?
show top holders of <token_address>
what tokens are trending on SOL right now?
show my wallet PnL on Solana
check my current subscription status
swap 0.1 SOL for <token_address>
check job status <job_id>
show K-line chart for <token_address>
what cubes are available in the GraphQL schema?
query the top 50 tokens by 24h volume using GraphQL
```

## CLI

Install via npx (no global install needed):

```bash
npx @chainstream-io/cli token search --keyword PUMP --chain sol
npx @chainstream-io/cli market trending --chain sol --duration 1h
npx @chainstream-io/cli wallet pnl --chain sol --address <addr>
npx @chainstream-io/cli dex route --chain sol --from <wallet> --input-token SOL --output-token <addr> --amount 1000000
npx @chainstream-io/cli graphql schema --summary
npx @chainstream-io/cli graphql query --query 'query { Solana { DEXTradeByTokens(where: {Trade: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}, limit: {count: 10}, orderBy: {descending: Block_Time}) { Block { Time } Trade { Currency { Symbol } Amount AmountInUSD Side { Type } } } } }'
```

## MCP Server

```json
{
  "mcpServers": {
    "chainstream": {
      "url": "https://mcp.chainstream.io/mcp",
      "headers": { "X-API-KEY": "<your-api-key>" }
    }
  }
}
```

## Supported Chains

| Chain | ID | Data | DeFi | WebSocket |
|-------|----|------|------|-----------|
| Solana | `sol` | Yes | Yes | Yes |
| BSC | `bsc` | Yes | Yes | Yes |
| Ethereum | `eth` | Yes | Yes | Yes |

## Resources

- [Documentation](https://docs.chainstream.io)
- [Dashboard](https://app.chainstream.io)
- [CLI README](https://github.com/chainstream-io/cli)
- [API Reference](https://docs.chainstream.io/api-reference)

## License

[MIT](LICENSE)
