# MGO — Multi-chain Gas Optimizer

Use this skill when the agent needs to find the cheapest EVM chain for a transaction, compare gas prices across chains, or optimize transaction costs.

## When to use
- "Which chain is cheapest for gas right now?"
- "Compare gas prices across EVM chains"
- "I want to send a transaction — where should I do it?"
- "Find the cheapest chain to deploy a contract"
- "How much will this transaction cost on Base vs Ethereum?"

## Base URL
https://api.mgo.chain-ops.xyz

## Endpoints

All paid endpoints use x402 protocol on Base (USDC). No API key needed.

### GET /gas/demo — Free
Raw gas prices for 4 chains. Rate limited (10/hr per IP).

### GET /gas/basic — $0.001 USDC
4-chain gas comparison with cheapest chain recommendation and savings calculation.
Chains: Ethereum, Base, Optimism, Arbitrum

### GET /gas/premium — $0.002 USDC
Full 9-chain comparison including BNB, Polygon, Avalanche, zkSync, Hyperliquid.

## Payment (x402)
Protocol: x402
Network: Base (eip155:8453)
Token: USDC

## Links
- Dashboard: https://mgo.chain-ops.xyz
- llms.txt: https://api.mgo.chain-ops.xyz/llms.txt
- GitHub: https://github.com/dlrjsdl200-byte/x402-gas-api