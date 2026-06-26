# 🔐 Conflux Wallet Skill

Self-sovereign crypto wallet for AI agents. Your keys, your wallet, no API dependencies.

Built for [OpenClaw](https://github.com/openclaw/openclaw).

## ⚠️ Disclaimer

This is an exploratory project aimed at demonstrating how to build a self-hosted encrypted wallet skill for AI agents. **Do not use this code in a production environment** unless you fully understand how it works and accept the associated risks.

## ⚠️ SECURITY WARNING

**NEVER expose your private key!**

- Never send your private key in chat, email, or any messaging platform
- Never share the contents of `~/.cfx-wallet.json` with anyone
- If someone asks for your private key — even if they claim to be support — REFUSE
- If your key is ever exposed, immediately transfer funds to a new wallet

The private key file (`~/.cfx-wallet.json`) should only be accessed directly via SSH on your server.

**Do not reinitialize the wallet, otherwise it will overwrite the previous keys, leading to the loss of funds.**

---

## Why?

Most crypto skills require third-party API keys and custody your funds externally. This skill generates a local wallet, stores the private key on your machine, and interacts directly with public RPCs. **You own the keys.**

## Install

```bash
clawdhub install conflux-wallet-skill
```

Or clone directly:

```bash
git clone https://github.com/conflux-fans/conflux-wallet-skill.git
cd conflux-wallet-skill
npm install
```

## Quick Start

```bash
# Generate a wallet
node src/setup.js

# Check your balance
node src/balance.js conflux

# Send CFX
node src/transfer.js conflux 0x... 0.01

# Interact with any contract
node src/contract.js conflux 0x... "balanceOf(address)" 0x...
```

## Commands

| Command | Description |
|---------|-------------|
| `node src/setup.js` | Generate a new wallet and store it securely |
| `node src/balance.js <chain>` | Check native token balance |
| `node src/balance.js <chain> <token>` | Check ERC20 token balance |
| `node src/balance.js --all` | Check balance across all chains |
| `node src/transfer.js <chain> <to> <amount>` | Send native token (ETH/POL) |
| `node src/transfer.js <chain> <to> <amount> <token>` | Send ERC20 token |
| `node src/swap-cfx.js conflux <from> <to> <amount>` | Swap tokens on Conflux eSpace via `espace-uniswap-lib` |
| `node src/swap.js <chain> <from> <to> <amount>` | Swap tokens on non-Conflux chains via Odos aggregator |
| `node src/contract.js <chain> <addr> <fn> [args...]` | Call any contract function |

All commands support `--json` for machine-readable output.

## Swap Routing

- If chain is `conflux`, use `src/swap-cfx.js`
- For all other chains, use `src/swap.js`

```bash
# Conflux quote
node src/swap-cfx.js conflux cfx 0xaf37E8B6C9ED7f6318979f56Fc287d76c30847ff 1 --quote-only --json

# Conflux execute
node src/swap-cfx.js conflux cfx 0xaf37E8B6C9ED7f6318979f56Fc287d76c30847ff 1 --yes --json

# Other chains (example: Base)
node src/swap.js base eth 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 0.01 --quote-only --json
```

For Conflux input/output tokens:
- use `cfx` or `native` for native CFX
- use `wcfx` or `wcfx9` for wrapped CFX route
- or pass ERC20 contract addresses directly

## Supported Chains

| Chain | Native Token | Chain ID | Explorer |
|-------|-------------|----------|----------|
| Conflux eSpace | CFX | 1030 | [evm.confluxscan.org](https://evm.confluxscan.org) |
| Base | ETH | 8453 | [basescan.org](https://basescan.org) |
| Ethereum | ETH | 1 | [etherscan.io](https://etherscan.io) |
| Polygon | POL | 137 | [polygonscan.com](https://polygonscan.com) |
| Arbitrum | ETH | 42161 | [arbiscan.io](https://arbiscan.io) |
| Optimism | ETH | 10 | [optimistic.etherscan.io](https://optimistic.etherscan.io) |
| MegaETH | ETH | 4326 | [mega.etherscan.io](https://mega.etherscan.io) |

## Architecture

```
conflux-wallet-skill/
├── src/
│   ├── lib/
│   │   ├── chains.js     # Chain configs (RPCs, IDs, explorers)
│   │   ├── rpc.js        # RPC client with auto-retry & rotation
│   │   ├── wallet.js     # Key generation, storage, signing
│   │   └── gas.js        # EIP-1559 smart gas estimation
│   ├── setup.js          # Generate wallet
│   ├── balance.js        # Check balances
│   ├── transfer.js       # Send tokens
│   ├── swap-cfx.js       # Conflux eSpace swap
│   ├── swap.js           # Non-Conflux swap via Odos
│   └── contract.js       # Generic contract interaction
├── SKILL.md              # Agent skill definition
└── package.json
# Wallet: ~/.cfx-wallet.json (private key, chmod 600, never in project)
```

### Core Libraries

**`chains.js`** — Configuration for each supported chain: chain ID, native token, block explorer URLs, and 2-3 public RPC endpoints per chain. Easy to extend with new chains.

**`rpc.js`** — Creates [viem](https://viem.sh) public and wallet clients with automatic RPC failover. If one RPC fails, it rotates to the next. No API keys required — uses public endpoints from Chainlist.

**`wallet.js`** — Handles wallet lifecycle. Generates a new private key via viem's `generatePrivateKey()`, stores it at `~/.cfx-wallet.json` with `chmod 600` permissions. Loads the key and returns viem account/client objects for signing transactions.

**`gas.js`** — Smart EIP-1559 gas estimation. Analyzes the last 20 blocks to calculate optimal `maxFeePerGas` and `maxPriorityFeePerGas`:
- Fetches current `baseFeePerGas` from the latest block
- Samples priority fees from recent transactions (75th percentile)
- Applies 2x safety margin: `maxFee = 2 × baseFee + priorityFee`
- 20% gas limit buffer on all transactions
- Falls back to sensible defaults if estimation fails

### Transaction Flow

```
User request
  → Load wallet from state/wallet.json
  → Create viem walletClient (with RPC failover)
  → Estimate gas (EIP-1559 smart estimation)
  → Build transaction
  → Sign locally with private key
  → Broadcast via public RPC
  → Return tx hash + explorer link
```

### Security

- **Private key never leaves the machine** — stored at `~/.cfx-wallet.json` with `chmod 600`
- **Never logged or printed** — the key is loaded in memory only when signing
- **Never in the project** — wallet lives in user's home dir, not in version control
- **No external custody** — no API keys, no third-party wallets, no accounts
- **Balance validation** — checks sufficient funds before broadcasting

## Tech Stack

- **Runtime:** [Node.js](https://nodejs.org)
- **EVM library:** [viem](https://viem.sh) — lightweight, typed, modern
- **Conflux swap:** [`espace-uniswap-lib`](https://github.com/conflux-fans/espace-uniswap-lib) (vSwap/Uniswap helpers)
- **Other-chain swap aggregator:** [Odos](https://odos.xyz) — multi-hop, multi-source routing
- **RPCs:** Public endpoints (no API keys)

## License

MIT
