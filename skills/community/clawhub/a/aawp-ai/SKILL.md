---
name: aawp
version: 2.1.0
description: >
  AAWP (AI Agent Wallet Protocol) — crypto wallet protocol built exclusively
  for AI Agents on EVM chains and Solana. Signer is the AI Agent itself,
  cryptographically bound at creation. Supports wallet lifecycle, transfers,
  DEX swaps, bridging, Solana native trading (Pump.fun + Jupiter), token
  launches, DCA, price alerts, limit orders, NFTs, yield/DeFi, SPL token
  transfers, portfolio tracking, transaction history, SOL staking (native +
  Marinade), and Raydium LP management.
environment:
  - name: AAWP_GUARDIAN_KEY
    description: "Guardian gas-relay private key (auto-generated in config/guardian.json)"
    required: false
  - name: AAWP_WALLET
    description: "Pinned wallet address — prevents operating on wrong wallet"
    required: false
  - name: AAWP_CONFIG
    description: "Override config directory (default: ./config)"
    required: false
  - name: AAWP_CORE
    description: "Override native addon directory (default: ./core)"
    required: false
  - name: SOLANA_RPC
    description: "Solana RPC endpoint (default: https://api.mainnet-beta.solana.com)"
    required: false
  - name: JUP_API_KEY
    description: "Jupiter API key for limit orders (paid, get at https://portal.jup.ag)"
    required: false
credentials:
  - name: "Guardian Key"
    description: "ECDSA key for gas relay. Auto-generated, stored in config/guardian.json. Only pays gas."
  - name: "Encrypted Seed"
    description: "Agent signing seed, encrypted at rest in .agent-config/. Agent's on-chain authority."
persistence:
  - type: daemon
    description: "Signing daemon on Unix socket /tmp/.aawp-daemon.*. Managed via ensure-daemon.sh / restart-daemon.sh."
  - type: files
    description: "Writes to config/ and .agent-config/ directories."
  - type: cron
    description: "DCA and price alerts register OpenClaw cron jobs."
native_binary:
  file: core/aawp-core.node
  hash_file: core/aawp-core.node.hash
  description: "Rust N-API addon (linux-x64). On-chain factory approveBinary(hash) required."
  source: "https://github.com/aawp-ai/aawp"
risk_disclosure: >
  Runs persistent signing daemon, manages encrypted keys, submits on-chain txs autonomously.
  Factory enforces binary approval + AI-exclusive ownership.
---

# AAWP — AI Agent Wallet Protocol

## On Skill Load (Greeting / Dashboard)

When this skill is triggered (e.g. `/aawp`), show a **live wallet dashboard**:

1. Run `bash scripts/ensure-daemon.sh` (silent, just ensure daemon is up)
2. Run `node scripts/wallet-manager.js status --all` to get all 6 EVM chains
3. Run `node scripts/wallet-manager.js --chain solana status` + `--chain solana balance` for Solana
4. Run `node scripts/wallet-manager.js --chain base balance` for Base token breakdown
5. Format results as a clean dashboard (see template below), then ask what to do.

### Dashboard Template (Telegram Markdown)

```
🔐 AAWP Wallet Dashboard

📍 EVM: 0x85bd...ecc8 (6 chains)
📍 SOL: CKeD...Ub4f (Mainnet)
🔑 Daemon: ✅ online | Frozen: no

💰 Balances
  Base     0.000408 ETH
  ETH      0.0 ETH
  ARB      0.0 ETH
  OP       0.0 ETH
  Polygon  0.0 MATIC
  BSC      0.001 BNB
  Solana   0.001733 SOL (PDA) · 0.033209 SOL (Signer)

📊 Base Tokens
  USDC  0.0  ·  USDT  0.0  ·  WETH  0.0

⚡ Quick Actions: balance · swap · send · bridge · dca · yield · pump

要做什么？
```

**Rules:**
- Show **real live data** from the commands above, not hardcoded values
- Round balances to 6 significant digits for readability
- Include Solana PDA + Signer balances (both matter — signer pays gas)
- Only show Base token breakdown (primary chain); user can ask for others
- If daemon is down, show ❌ and suggest restart
- If wallet has ⚠️ warnings (low balance), include them
- Keep it concise — no contract addresses, no architecture details

## ⚠️ Human Approval Required

- First-time provisioning (`provision.sh`)
- Wallet creation (`wallet-manager.js create`)
- DCA / price-alert cron registration
- Factory binary approval (`approveBinary`)

All other operations (balance, quotes, reads) are safe to run autonomously.

## Architecture

**EVM:** Guardian pays gas → Wallet contract holds assets → Daemon signs (secp256k1)
**Solana:** AI Signer pays directly → Wallet PDA holds assets → Daemon signs (Ed25519)
Same seed, HKDF domain separation → independent keys per chain family.

**Networks:** Ethereum · Base · BNB Chain · Polygon · Optimism · Arbitrum · Solana

## Contracts (CREATE2 vanity, same on all 6 EVM chains)

| Contract | Address |
|----------|---------|
| Factory Proxy | `0xAAAA3Df87F112c743BbC57c4de1700C72eB7aaAA` |
| Identity Proxy | `0xAAAafBf6F88367C75A9B701fFb4684Df6bCA1D1d` |

---

## Quick Reference — EVM

All commands: `node scripts/wallet-manager.js [--chain <chain>] <command>`
Chains: `base|eth|bsc|polygon|optimism|arbitrum`

### Wallet
| Command | Description |
|---------|-------------|
| `create` | Deploy wallet |
| `status` | Status overview |
| `balance` | Native + token balances |
| `dashboard` | Full multi-chain dashboard |
| `portfolio` | Portfolio view |
| `history` | Tx history |
| `compute-address` | Predict wallet address |
| `backup <file>` | Backup wallet |
| `restore <file>` | Restore wallet |

### Transfers & Trading
| Command | Description |
|---------|-------------|
| `send <to> <amt>` | Send native token |
| `send-token <symbol> <to> <amt>` | Send ERC-20 |
| `quote <from> <to> <amt>` | Swap preview (no gas) |
| `swap <from> <to> <amt>` | Execute swap |
| `bridge <token> <dest_chain> <amt>` | Cross-chain bridge |

### Approvals
| Command | Description |
|---------|-------------|
| `approve <token> <spender> <amt>` | Approve ERC-20 |
| `allowance <token> <spender>` | Check allowance |
| `revoke <token> <spender>` | Revoke approval |

### Contract Interaction
```bash
call <contract> "transfer(address,uint256)" 0xTo 1000     # Write (tx)
read <contract> "balanceOf(address) returns (uint256)" 0x  # Read (free)
batch ./calls.json                                          # Atomic batch
```

### Address Book
`addr add|list|get|remove <label> [<address>]`

---

## DCA — `node scripts/dca.js`

```bash
dca.js add --chain base --from ETH --to USDC --amount 0.01 --cron "0 9 * * *"
dca.js list | run <id> | history <id> | remove <id>
```

## Price Alerts — `node scripts/price-alert.js`

```bash
price-alert.js add --chain base --from ETH --to USDC --above 2600 --notify
price-alert.js add --chain base --from ETH --to USDC --below 2200 --auto-swap 0.01
price-alert.js list | check | remove <id>
```

## Limit Orders (Gasless) — `node scripts/limit-order.js`

Chains: `eth|base|arb|op|polygon` (CoW Protocol) · `bsc` (1inch)

```bash
limit-order.js --chain base create ETH USDC 0.1 2700 [--expiry 48]
limit-order.js --chain base list | history | cancel <orderUid>
```

## Portfolio — `node scripts/portfolio.js`

```bash
portfolio.js [--chain base] [--no-prices] [--hide-zero] [--json]
```

## NFTs — `node scripts/nft.js`

```bash
nft.js --chain base balance [--contract 0x...]
nft.js --chain eth info <contract> <tokenId>
nft.js --chain base transfer <contract> <tokenId> <to> [amount]
nft.js --chain base approve|revoke <contract> <operator>
nft.js --chain base mint <contract> [calldata]
nft.js --chain eth floor <contract>
```

## Yield/DeFi (Aave V3) — `node scripts/yield.js`

Chains: `base|eth|arb|op|polygon` (Aave) · `bsc` (Venus)

```bash
yield.js --chain base rates | positions
yield.js --chain base supply|withdraw <token> <amt|max>
yield.js --chain base borrow|repay <token> <amt|max> [--rate stable]
```

## Token Launch (Clanker V4) — `node scripts/deploy-clanker.js`

Chains: `base|eth|arb|unichain|bera|bsc`

```bash
deploy-clanker.js --dry-run   # Preview
deploy-clanker.js              # Deploy
```

Edit CONFIG at top of script: name, symbol, image, initialMarketCap, vault settings, etc.
`tokenAdmin` + `rewardRecipient` default to AAWP wallet.

---

## Quick Reference — Solana

### Solana (Mainnet + Devnet)

| Component | Address |
|-----------|---------|
| Program | [`AAwpAAQSVAZYHvpUW5uz7zxqj7RYTYR6CZvWL9wf4qiS`](https://explorer.solana.com/address/AAwpAAQSVAZYHvpUW5uz7zxqj7RYTYR6CZvWL9wf4qiS) |
| Factory PDA | `6EkR7RUVPVkJ2SNpVN6UJTLS9TZ2bqHJt9nch5fgetxx` |
| Identity PDA | `8Aef6r3Q4YiuLMN9mdrZGQJJrfLJFgwEGjKa1CiHmAej` |

### Active Wallet

All commands: `wallet-manager.js --chain solana <command>`

| Component | Address |
|-----------|---------|
| AI Signer | `BrZhu5oBmqBPGMYA8TiUS2hMr2Kpg11q5PFpfK35Kgoi` |
| Wallet PDA | `CKeDtwBFaahwX3LuEo4us1XJd7hS2e45N25zDHjTUb4f` |
| Guardian | `BvbXW3uZG9YkzQmcYEnQ5qxTkTf1tQ5Jb4vHJ8HPM77P` |

### Core
`status` · `balance` · `compute-address` · `send <to> <amt>` · `price <token>`

### Token Transfers
```bash
send <to> <amount_SOL>                 # Send SOL
send-token <mint> <to> <amount>        # Send SPL token (Token-2022 auto-detect)
```

### Portfolio & History
```bash
portfolio                              # All token holdings + USD values
history [--limit 20]                   # Transaction history with type classification
```

### Swap (auto-routes: Pump bonding → Pump AMM → Jupiter)
```bash
swap SOL <mint> 0.1                    # Buy
swap <mint> SOL 1000000                # Sell
swap SOL <mint> 0.1 --pool jupiter     # Force Jupiter
swap SOL USDC 0.5 --slippage 5
```

### DCA — Jupiter Dollar-Cost Averaging
```bash
dca create <inputMint> <outputMint> <totalAmount> <perCycle> <frequencySec>
dca list                               # Active DCA positions
dca close <dcaAccount>                 # Close DCA position
```

### Limit Orders — Jupiter (requires `JUP_API_KEY`)
```bash
limit create <inputMint> <outputMint> <inAmount> <outAmount> [--expires <sec>]
limit list                             # Open orders
limit cancel <orderPubkey>             # Cancel order
limit history                          # Order history
```

### NFTs — Metaplex
```bash
nft list                               # List all NFTs
nft info <mint>                        # Metadata details
nft send <mint> <to>                   # Transfer NFT
```

### Staking
```bash
stake <amount_SOL> <validatorVoteAccount>   # Delegate SOL
unstake <stakeAccount>                       # Deactivate stake
stake-list                                   # List all stake accounts
stake-withdraw <stakeAccount>                # Withdraw after cooldown
```

### Raydium LP
```bash
raydium info <poolId>                  # Pool details + TVL
raydium search <mint>                  # Search pools by token
raydium add <poolId> <amountA> <amountB>    # Add liquidity
raydium remove <poolId> <lpAmount>          # Remove liquidity
```

### Pump.fun
```bash
pump-info <mint>
pump-quote buy|sell|cost <mint> <amount>
pump-create <name> <symbol> <uri> [--buy 0.5]
pump-fees balance|collect|distribute|cashback [addr|mint]
pump-share <mint> <addr1:share1> <addr2:share2>
pump-incentives [claim]
pump-lp deposit|withdraw <mint> <amount>
pump-volume [sync]
pump-migrate <mint> <withdraw_authority>
```

---

## Getting Started

```bash
bash scripts/provision.sh                          # 1. Initialize
node scripts/wallet-manager.js --chain base create # 2. Create wallet
export AAWP_WALLET=0x...                           # 3. Pin address
# Fund wallet, then:
node scripts/wallet-manager.js --chain base balance # 4. Verify
```

## Daemon Management

| Script | Purpose |
|--------|---------|
| `scripts/doctor.sh` | Full diagnostics |
| `scripts/ensure-daemon.sh` | Start if not running |
| `scripts/restart-daemon.sh` | Force restart |

## Troubleshooting

| Error | Fix |
|-------|-----|
| `E_AI_GATE` / `hmac_mismatch` | `bash scripts/restart-daemon.sh` |
| `InvalidSignature` | Verify signer + binary approval on factory |
| `E40` / `E41` | Kill duplicate daemon, restart |
| `BinaryNotApproved` | Owner must `approveBinary(hash)` on all chains |
| TX reverts ~1M gas | Add `--gas-limit 8000000` |

## Security

- Fund the wallet, not the guardian (guardian only pays gas)
- Pin wallet: `export AAWP_WALLET=0x...`
- Quote before swap · Start small · Never expose secrets
- Verify binary approval after provisioning
