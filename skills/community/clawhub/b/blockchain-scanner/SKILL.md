---
name: blockchain-scanner
description: "Blockchain Scanner: Query EVM blockchain data: balances (up to 20 addresses), transactions, gas prices, contract ABIs. Supports Ethereum, Polygon, Base, Arbitrum, Optimism. Use when an agent needs blockchain scanner, blockchain transaction history & activity tracking, ethereum gas price & fee management, smart contract development, crypto balance & account management, balance, address, chain through AgentPMT-hosted remote tool calls. Discovery terms: blockchain scanner."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/blockchain-scanner
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/blockchain-scanner"}}
---
# Blockchain Scanner

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Multi-chain EVM blockchain data service providing four operations:

Balance – Get native currency balance (ETH, MATIC, etc.) for up to 20 addresses. Returns wei and standard units.
Transactions – Paginated transaction history (100 per request). Includes hash, block, timestamp, addresses, value, gas metrics, input data, errors.
Gas Oracle – EIP-1559 gas recommendations: base fee + priority fees for slow/standard/fast confirmation speeds.
Contract ABI – Retrieve ABI JSON for verified smart contracts (functions, events, inputs/outputs).

Supported Networks: Ethereum, Base, Base Sepolia, Polygon, Arbitrum One, Optimism

## Product Instructions
### Blockchain Scanner

Multi-chain blockchain data retrieval tool. Query native token balances, ERC-20 token balances, transaction history, verified contract ABIs, and current gas prices across six supported networks.

#### Supported Chains

| Chain Value | Network |
|---|---|
| `ethereum` | Ethereum Mainnet (default) |
| `base` | Base L2 |
| `base_sepolia` | Base Sepolia Testnet |
| `polygon` | Polygon PoS |
| `arbitrum` | Arbitrum One |
| `optimism` | Optimism Mainnet |

#### Actions

##### balance

Get the native token balance (ETH or MATIC) for one or more wallet addresses.

**Required fields:**
- `action`: `"balance"`
- `address`: Array of 1-20 wallet addresses (0x-prefixed, 42-character hex strings)

**Optional fields:**
- `chain`: Network to query (default: `"ethereum"`)

**Example - Single address on Ethereum:**
```json
{
  "action": "balance",
  "address": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"]
}
```

**Example - Multiple addresses on Polygon:**
```json
{
  "action": "balance",
  "chain": "polygon",
  "address": [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
  ]
}
```

**Response includes:** Each address with its balance in native units and in wei, the chain name, and the native token symbol (ETH or MATIC for Polygon).

---

##### token_balance

Get ERC-20 token balances for one or more wallet addresses. Supports major stablecoins and wrapped tokens.

**Required fields:**
- `action`: `"token_balance"`
- `address`: Array of 1-20 wallet addresses

**Optional fields:**
- `chain`: Network to query (default: `"ethereum"`)
- `token`: Token symbol to query (e.g., `"USDC"`, `"USDT"`, `"DAI"`, `"WETH"`, `"PYUSD"`). Use `"all"` to query all supported tokens on the chain. Defaults to `"all"` if omitted.

**Supported tokens by chain:**
- **Ethereum:** USDC, USDT, PYUSD, DAI, WETH, WBTC
- **Base:** USDC, USDbC, DAI, WETH
- **Polygon:** USDC, USDC.e, USDT, DAI, WETH, WMATIC
- **Arbitrum:** USDC, USDC.e, USDT, DAI, WETH
- **Optimism:** USDC, USDC.e, USDT, DAI, WETH

**Example - Get USDC balance on Ethereum:**
```json
{
  "action": "token_balance",
  "address": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
  "token": "USDC"
}
```

**Example - Get all token balances on Base:**
```json
{
  "action": "token_balance",
  "chain": "base",
  "address": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
  "token": "all"
}
```

**Response includes:** Each address with token balances (formatted balance, raw balance, decimals) for the requested tokens.

---

##### transactions

Get transaction history for a single address. Returns transactions sorted by most recent first, in pages of exactly 100.

**Required fields:**
- `action`: `"transactions"`
- `address`: Array with exactly 1 wallet address

**Optional fields:**
- `chain`: Network to query (default: `"ethereum"`)
- `transaction_range`: Array of two integers `[start, end]` defining which 100-transaction window to fetch. Index 1 is the most recent transaction. Must span exactly 100 items. Default: `[1, 100]`.

**Example - Most recent 100 transactions:**
```json
{
  "action": "transactions",
  "address": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"]
}
```

**Example - Transactions 101-200 on Arbitrum:**
```json
{
  "action": "transactions",
  "chain": "arbitrum",
  "address": ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
  "transaction_range": [101, 200]
}
```

**Response includes:** Each transaction with hash, block number, timestamp, from/to addresses, value in ETH and wei, gas details, input data, and error status.

---

##### contract_abi

Retrieve the ABI (Application Binary Interface) for a verified smart contract.

**Required fields:**
- `action`: `"contract_abi"`
- `address`: Array with exactly 1 contract address

**Optional fields:**
- `chain`: Network to query (default: `"ethereum"`)

**Example - Get ABI for a contract on Ethereum:**
```json
{
  "action": "contract_abi",
  "address": ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"]
}
```

**Example - Get ABI on Optimism:**
```json
{
  "action": "contract_abi",
  "chain": "optimism",
  "address": ["0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85"]
}
```

**Response includes:** The full ABI array, plus counts of functions and events in the contract.

---

##### gas_oracle

Get current gas price estimates for a blockchain network. Returns safe (slow), standard, and fast gas prices.

**Required fields:**
- `action`: `"gas_oracle"`

**Optional fields:**
- `chain`: Network to query (default: `"ethereum"`)

**Example - Ethereum gas prices:**
```json
{
  "action": "gas_oracle"
}
```

**Example - Polygon gas prices:**
```json
{
  "action": "gas_oracle",
  "chain": "polygon"
}
```

**Response includes:** Safe, standard, and fast gas price estimates (in Gwei), suggested base fee, gas used ratio, and timestamp.

---

#### Common Workflows

##### Check a wallet's full portfolio
1. Call `balance` to get native ETH/MATIC balance
2. Call `token_balance` with `token: "all"` to get all ERC-20 holdings

##### Investigate transaction activity
1. Call `transactions` with default range `[1, 100]` for the latest 100 transactions
2. Page through older transactions with `[101, 200]`, `[201, 300]`, etc.

##### Inspect a smart contract
1. Call `contract_abi` to retrieve the verified ABI
2. Use the ABI to understand available functions and events

##### Estimate transaction costs
1. Call `gas_oracle` to get current gas prices on the target chain

#### Important Notes

- All addresses must be 0x-prefixed, 42-character hexadecimal strings.
- The `balance` and `token_balance` actions accept up to 20 addresses per request.
- The `transactions` and `contract_abi` actions require exactly 1 address.
- The `gas_oracle` action does not require any address.
- The `transaction_range` must always span exactly 100 transactions (e.g., `[1, 100]`, `[101, 200]`).
- On Polygon, the native token is MATIC; on all other chains it is ETH.
- The `contract_abi` action only works for verified contracts. Unverified contracts will return an error.
- Token availability varies by chain. If a token is not supported on the selected chain, the tool returns an error listing available tokens.
- Base Sepolia (testnet) has no preconfigured ERC-20 tokens for `token_balance`.

## When To Use
- Use this skill for `Blockchain Scanner` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: blockchain scanner, blockchain transaction history & activity tracking, ethereum gas price & fee management, smart contract development, crypto balance & account management, balance, address, chain.
- Supported action names: `balance`, `contract_abi`, `gas_oracle`, `token_balance`, `transactions`.

## Use Cases
- Blockchain Transaction History & Activity Tracking
- Ethereum Gas Price & Fee Management
- Smart Contract Development
- Crypto Balance & Account Management
- Multi-Chain & Cross-Chain Operations
- Web3 Developer & Integration Tools

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `5`.
x402 availability: not enabled for this product.

- `balance` (action slug: `balance`): Get native token balance (ETH or MATIC) for one or more wallet addresses. Returns balance in both native units and wei. Price: `5` credits. Parameters: `address`, `chain`.
- `contract_abi` (action slug: `contract-abi`): Retrieve the ABI (Application Binary Interface) JSON for a verified smart contract. Returns the full ABI array plus counts of functions and events. Price: `5` credits. Parameters: `address`, `chain`.
- `gas_oracle` (action slug: `gas-oracle`): Get current gas price estimates (safe/standard/fast) for a blockchain network. Returns prices in Gwei with EIP-1559 base fee suggestions. Price: `5` credits. Parameters: `chain`.
- `token_balance` (action slug: `token-balance`): Get ERC-20 token balances for one or more wallet addresses. Supports major stablecoins and wrapped tokens across all supported chains. Price: `5` credits. Parameters: `address`, `chain`, `token`.
- `transactions` (action slug: `transactions`): Get paginated transaction history for a single address. Returns 100 transactions per request sorted by most recent first. Price: `5` credits. Parameters: `address`, `chain`, `transaction_range`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "blockchain-scanner"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "blockchain-scanner"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "blockchain-scanner"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "blockchain-scanner"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "blockchain-scanner"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "blockchain-scanner"
  }
}
```

## Call This Tool
Product slug: `blockchain-scanner`

Marketplace page: https://www.agentpmt.com/marketplace/blockchain-scanner

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Blockchain-Scanner",
    "arguments": {
      "action": "balance",
      "address": [
        "example addre"
      ],
      "chain": "ethereum"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "blockchain-scanner",
  "parameters": {
    "action": "balance",
    "address": [
      "example addre"
    ],
    "chain": "ethereum"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `balance` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/blockchain-scanner
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
