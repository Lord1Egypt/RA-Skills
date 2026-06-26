# eth-labels

Look up 170,000+ labeled crypto addresses and tokens across EVM chains (Ethereum, Base, Arbitrum, Optimism, BSC, and more). Identify who owns an address, search for labeled accounts, check balances, and discover token metadata — all via the eth-labels MCP server.

## When to use

Use this skill when:
- User asks "who owns this address" or "what is this address"
- Looking up wallet labels (exchanges, protocols, DAOs, known entities)
- Identifying token contracts and metadata
- Searching for addresses by label/name
- Checking balances across EVM chains
- Researching crypto transactions or addresses

## Setup

### Install via GitHub (recommended)

Clone the repository and build the MCP server:

```bash
git clone https://github.com/dawsbot/eth-labels.git
cd eth-labels/mcp
npm install
npm run build
```

Then add to your MCP client config (e.g., Claude Desktop `~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "eth-labels": {
      "command": "node",
      "args": ["/path/to/eth-labels/mcp/dist/index.js"]
    }
  }
}
```

Replace `/path/to/eth-labels` with the actual path where you cloned the repo.

### Alternative: Run directly from source

For development or testing, you can run the MCP server directly without building:

```bash
cd eth-labels/mcp
npx tsx index.ts
```

Add to MCP config:

```json
{
  "mcpServers": {
    "eth-labels": {
      "command": "npx",
      "args": ["tsx", "/path/to/eth-labels/mcp/index.ts"]
    }
  }
}
```

## Available tools (via MCP)

The MCP server provides these tools:

### `lookup_account`
Look up an address to find its label and metadata.

**Parameters:**
- `address` (string, required): Ethereum address (0x...)
- `chainId` (number, optional): Chain ID to filter results (1=Ethereum, 8453=Base, 42161=Arbitrum, 10=Optimism, 56=BSC)

**Returns:** Array of account labels with chain info

### `lookup_token`
Look up a token contract address to get metadata (name, symbol, website, image).

**Parameters:**
- `address` (string, required): Token contract address (0x...)
- `chainId` (number, optional): Chain ID to filter results

**Returns:** Array of token metadata

### `search_labels`
Search for addresses by label/name (e.g., "Coinbase", "Uniswap").

**Parameters:**
- `query` (string, required): Search term (case-insensitive, partial match supported)
- `chainId` (number, optional): Chain ID to filter results
- `limit` (number, optional): Max results to return (default: 20)

**Returns:** Array of matching accounts

### `get_balance`
Check ETH balance for an address on any EVM chain.

**Parameters:**
- `address` (string, required): Address to check
- `chainId` (number, optional): Chain ID (default: 1 for Ethereum mainnet)
- `rpcUrl` (string, optional): Custom RPC endpoint

**Returns:** Balance in ETH (formatted)

## Supported chains

- **Ethereum** (chainId: 1)
- **Base** (chainId: 8453)
- **Arbitrum** (chainId: 42161)
- **Optimism** (chainId: 10)
- **Binance Smart Chain** (chainId: 56)

View all labeled accounts by chain at: https://eth-labels.com/accounts

## Public API alternative

If you prefer REST API over MCP, use the public API:
- **Swagger docs:** https://eth-labels.com/swagger
- **View labeled accounts:** https://eth-labels.com/accounts?chainId=1

## Data sources

Labels are scraped from blockchain explorers (Etherscan, Basescan, Arbiscan, Optimistic Etherscan, BscScan) and refreshed regularly.

## Examples

**Look up Vitalik's address:**
```
lookup_account(address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", chainId=1)
```

**Search for Coinbase addresses:**
```
search_labels(query="Coinbase", limit=10)
```

**Check balance on Base:**
```
get_balance(address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", chainId=8453)
```

## Repository

https://github.com/dawsbot/eth-labels

## License

MIT
