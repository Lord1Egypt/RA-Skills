---
name: claw-mining
description: "Mine $CLAW tokens via Proof of AI Work on Ethereum. Install this Skill and tell your agent 'mine CLAW' — the agent handles everything automatically. No technical knowledge required."
license: MIT-0
metadata: {"author": "Cliai21", "version": "3.0", "network": "Ethereum Mainnet", "github": "https://github.com/Cliai21/clawing", "openclaw": {"emoji": "⛏️", "homepage": "https://minewithclaw.com", "requires": {"bins": ["node", "git"], "env": ["AI_API_KEY", "PRIVATE_KEY", "RPC_URL", "POAIW_MINT_ADDRESS"]}, "primaryEnv": "AI_API_KEY"}}
---

# CLAW Mining Skill

Mine $CLAW tokens on Ethereum mainnet using Proof of AI Work (PoAIW). The miner calls an AI API (e.g., xAI Grok), submits the result to an Oracle for verification, and the user receives CLAW tokens on-chain.

**Compatible platforms**: OpenClaw (recommended), Hermes Agent, Perplexity Computer, or any AgentSkills-compatible agent.

## When to Use This Skill

Use when the user wants to:

- Set up and run CLAW mining
- Configure the miner with wallet, API keys, and contract addresses
- Check mining status (cooldown, balance, epoch info)
- Start single-cycle or automatic continuous mining
- Troubleshoot mining errors (cooldown, gas, Oracle issues)

## Security: Private Key Handling

**CRITICAL — READ BEFORE PROCEEDING**

- The `init` command optionally asks the user if they want to enter their private key. If they decline, the `.env` file is created with an empty `PRIVATE_KEY=` placeholder for them to fill in later. Either way, the choice is entirely the user's.
- The agent MUST NOT ask the user to paste, share, or reveal their private key in conversation. Only the CLI's local `init` prompt handles this.
- The `.env` file is created with `chmod 600` permissions (owner-only read/write).
- At runtime, the miner reads `PRIVATE_KEY` from the environment, loads it into an in-memory `ethers.Wallet` object, and removes it from the config object immediately. The key is used only for local transaction signing and is never logged, transmitted, or sent to the Oracle, AI API, or any external service.
- All transactions are signed locally by the miner process on the user's own computer.

## Architecture Overview

```
Miner Engine (Node.js/TypeScript) — runs on user's local machine
    │
    ├── 1. Read chain state (Era, Epoch, Seed, Cooldown)
    ├── 2. Check gas price (abort early if too high, saves API costs)
    ├── 3. Request nonce from Oracle (format-validated)
    ├── 4. Call AI API (grok-4.1-fast via xAI or OpenRouter)
    ├── 5. Submit AI response to Oracle for verification + signing
    ├── 6. Validate attestation (miner address, deadline, field integrity)
    └── 7. Sign and send mint() transaction on-chain (LOCAL signing)
             → CLAW tokens minted to miner's wallet
```

Each mining cycle takes ~30-60 seconds. After a successful mine, a cooldown of 3,500 blocks (~11.67 hours) must pass before the same address can mine again.

## Contract Addresses (Mainnet v2)

| Contract | Address |
|----------|---------|
| CLAW_Token | `0x4ba1209b165b62a1f0d2fbf22d67cacf43a6df2b` |
| PoAIWMint | `0x511351940d99f3012c79c613478e8f2c887a8259` |
| MinterProxy | `0xe7fc311863b95e726a620b07607209965ee72bce` |
| OracleVerifier | `0xc24a0ba99b9ff6b7ccea6beb4013b69f39024fd5` |

Oracle URL: `https://oracle.minewithclaw.com`

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Node.js | Version 20+ |
| Ethereum wallet | A private key with ETH for gas (~0.01 ETH is enough for many mines) |
| AI API key | xAI API key (recommended) or OpenRouter API key |
| Ethereum RPC | Alchemy, Infura, or any mainnet RPC endpoint |
| ETH for gas | ~0.0002 ETH per mine at 2 gwei gas price |

## Step-by-Step Deployment Instructions

Follow these steps in order. The agent collects only the AI API key and RPC URL from the user. The private key is set by the user directly — the agent never handles it.

### Step 1: Obtain Credentials from the User

Ask the user for these 2 items (they can provide them one at a time):

1. **AI API Key** — from [console.x.ai](https://console.x.ai) (format: `xai-...`) or [openrouter.ai](https://openrouter.ai)
2. **Ethereum RPC URL** — from [alchemy.com](https://www.alchemy.com) or [infura.io](https://infura.io) (format: `https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY`)

**IMPORTANT about private key**: Do NOT ask the user for their private key. Instead, instruct them to set the `PRIVATE_KEY` environment variable themselves by editing the `.env` file directly. The agent never sees, handles, or stores the private key. Use a hot wallet with some ETH for gas — NOT their main wallet or Ledger.

### Step 2: Clone and Install

```bash
git clone https://github.com/Cliai21/clawing.git
cd clawing/miner
npm install
```

Verify installation:

```bash
npx tsx src/index.ts --version
# Expected output: 1.0.0
```

### Step 3: Configure the .env File

The user creates the `.env` file in the `miner/` directory. There are two methods:

#### Method A: Interactive Setup (Recommended)

The user runs this command in their terminal:

```bash
npx tsx src/index.ts init
```

This will prompt the user for AI API provider and API key. All other settings (Oracle URL, RPC, contract address, gas limit) use sensible built-in defaults. When prompted:
- **AI API provider**: Choose `[1] xAI Direct` (recommended) or `[2] OpenRouter`
- **Customize advanced settings?**: Press Enter for No (defaults are correct for mainnet)
- **Enter private key now?**: The user chooses — they can enter it in the CLI or add it to `.env` later

If the user skipped the private key step, tell them to open `.env` and paste their `PRIVATE_KEY` on the designated line.

#### Method B: Manual .env File

Instruct the user to create the file manually. Show them the template below but tell them to fill in their own values directly — the agent must not handle `PRIVATE_KEY`:

```bash
cat > .env << 'EOF'
# === Wallet ===
PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE

# === AI API ===
# Provider: xAI Direct (recommended)
AI_API_KEY=xai-YOUR_KEY_HERE
AI_API_URL=https://api.x.ai/v1/chat/completions
AI_MODEL=grok-4-1-fast-non-reasoning

# === Oracle ===
ORACLE_URL=https://oracle.minewithclaw.com

# === Chain ===
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY
POAIW_MINT_ADDRESS=0x511351940d99f3012c79c613478e8f2c887a8259

# === Mining Config ===
MAX_GAS_PRICE_GWEI=3
TASK_PROMPT=Write an extremely detailed, comprehensive, and thorough 2500-word academic analysis of decentralized proof-of-work systems, covering historical evolution, consensus mechanisms, game theory incentives, energy considerations, security models, and future outlook. Include specific technical details, mathematical reasoning, concrete examples, and citations to relevant research. Structure your response with clear sections and subsections.
EOF
```

**CRITICAL**: Protect the file:

```bash
chmod 600 .env
```

#### Environment Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PRIVATE_KEY` | Yes | — | Mining wallet private key (0x-prefixed hex). Stays local, never transmitted. |
| `AI_API_KEY` | Yes | — | xAI or OpenRouter API key |
| `AI_API_URL` | No | `https://api.x.ai/v1/chat/completions` | AI chat completions endpoint |
| `AI_MODEL` | No | `grok-4.1-fast` | Model name (must match on-chain Era model) |
| `ORACLE_URL` | No | `https://oracle.minewithclaw.com` | Oracle verification server URL. **Must use HTTPS** in production (only localhost allowed over HTTP). |
| `RPC_URL` | No | `https://eth.llamarpc.com` | Ethereum mainnet JSON-RPC endpoint. Free public RPC; replace with Alchemy/Infura for higher reliability. |
| `POAIW_MINT_ADDRESS` | No | `0x511351940d99f3012c79c613478e8f2c887a8259` | PoAIWMint contract address |
| `MAX_GAS_PRICE_GWEI` | No | `2` | Max gas price — auto-waits if exceeded. Must be a finite positive number. |
| `TASK_PROMPT` | No | (built-in default) | Text prompt sent to AI model |

#### AI Provider Options

| Provider | AI_API_URL | AI_MODEL | Notes |
|----------|-----------|----------|-------|
| xAI Direct | `https://api.x.ai/v1/chat/completions` | `grok-4-1-fast-non-reasoning` | Recommended, lowest cost |
| OpenRouter | `https://openrouter.ai/api/v1/chat/completions` | `x-ai/grok-4.1-fast` | Alternative, has markup |

**Note on .env loading**: If the system does not use `dotenv` (e.g., on a deployed server), load environment variables manually before running:

```bash
set -a && source .env && set +a
```

### Step 4: Verify Configuration

```bash
npx tsx src/index.ts status
```

Expected output shows:
- Miner address and ETH balance
- Current Era and Epoch
- Cooldown status (Ready or blocks remaining)
- Claim count (X/14 this epoch)
- Oracle health (healthy)

If everything shows correctly, proceed to mining.

### Step 5: Start Mining

#### Single Mine (Test First)

```bash
npx tsx src/index.ts mine
```

This executes one mining cycle. If successful, you will see the CLAW reward and transaction hash.

#### Automatic Continuous Mining (Recommended)

```bash
npx tsx src/index.ts auto
```

The `auto` command:
- Mines whenever cooldown has elapsed
- Automatically waits between cycles (~11.67 hours)
- Pauses if gas exceeds `MAX_GAS_PRICE_GWEI`
- Retries on errors with backoff
- Press Ctrl+C to stop gracefully

## CLI Commands Reference

| Command | Description | Usage |
|---------|-------------|-------|
| `init` | Interactive setup — creates `.env` file | `npx tsx src/index.ts init` |
| `status` | Show mining status, balance, cooldown | `npx tsx src/index.ts status` |
| `mine` | Execute one mining cycle | `npx tsx src/index.ts mine` |
| `auto` | Start continuous mining loop | `npx tsx src/index.ts auto` |

## Mining Economics Quick Reference

### Reward Formula

```
R = perBlock x (1 + ln(T))
```

- `perBlock`: Base reward for current Era (Era 1 = 100,000 CLAW)
- `T`: AI tokens consumed (range: 100-100,000)

### Era 1 Reward Examples

| AI Tokens (T) | Reward per Mine |
|----------------|-----------------|
| 2,100 (minimum practical) | ~862,300 CLAW |
| 5,000 | ~931,600 CLAW |
| 10,000 | ~1,000,900 CLAW |

### Key Limits

| Parameter | Value |
|-----------|-------|
| Cooldown | 3,500 blocks (~11.67 hours) |
| Max claims per Epoch | 14 per address |
| Epoch duration | 50,000 blocks (~6.94 days) |
| Era duration | 21 Epochs (~145 days) |
| Total Eras | 24 (~9.6 years) |
| Max supply | 210 billion CLAW |
| Gas per mint | ~100k gas (~0.0002 ETH at 2 gwei) |

### Cost-Efficiency Tip

Use `T=2100` (minimum practical tokens). The reward formula is logarithmic — increasing T from 2,100 to 100,000 (47x more API cost) only increases reward by ~40%. Minimize AI API spend for maximum ROI.

## Troubleshooting

### Common Errors and Solutions

| Error | Cause | Fix |
|-------|-------|-----|
| `CooldownNotMet` | Mined too recently | Wait ~11.67 hours, or use `auto` mode |
| `EpochClaimLimitReached` | 14 claims already this Epoch | Wait for next Epoch (~1 week) |
| `Gas price exceeds limit` | Network gas too high | Wait, or increase `MAX_GAS_PRICE_GWEI` |
| `Oracle nonce error` | Oracle rate limit or downtime | Wait 60 seconds and retry |
| `AI API error: 401` | Invalid API key | Check `AI_API_KEY` in `.env` |
| `AI API error: 429` | API rate limit | Wait and retry, or check API quota |
| `InvalidSignature` | Oracle signing mismatch | Retry; if persistent, check Oracle status |
| `Missing required environment variable` | `.env` not loaded | Run `set -a && source .env && set +a` first, or check `.env` file exists |
| `EpochExhausted` | Epoch cap fully mined | Wait for next Epoch |

### Checking Oracle Health

```bash
curl https://oracle.minewithclaw.com/health
# Expected: {"status":"ok", ...}
```

### Checking Wallet Balance

```bash
npx tsx src/index.ts status
```

If ETH balance is too low, send more ETH to the mining wallet address shown in the status output.

## Security Audit Status (v2.1)

15 issues identified and fixed (1 critical, 4 high, 5 medium, 5 low), 67 tests passing including 52 adversarial tests. Key protections:

- **F-01**: Attestation miner_address verification — prevents reward redirection attacks
- **F-02**: HTTPS enforcement for Oracle URL — prevents MITM attacks
- **F-03**: Gas price input validation — prevents Infinity/NaN bypass
- **F-05**: Nonce format regex validation — prevents prompt injection
- **F-07**: Attestation field completeness checks — prevents null crashes
- **F-08**: Private key removed from config object — reduces memory exposure risk
- **F-12**: AI response body size limit (2MB) — prevents memory exhaustion

## Project Links

- GitHub: [https://github.com/Cliai21/clawing](https://github.com/Cliai21/clawing)
- Oracle: [https://oracle.minewithclaw.com](https://oracle.minewithclaw.com)
- Mining Guide: See `docs/MINING_GUIDE.md` in the repository
- CLAW_Token on Etherscan: [0x4ba1209b165b62a1f0d2fbf22d67cacf43a6df2b](https://etherscan.io/address/0x4ba1209b165b62a1f0d2fbf22d67cacf43a6df2b)
- PoAIWMint on Etherscan: [0x511351940d99f3012c79c613478e8f2c887a8259](https://etherscan.io/address/0x511351940d99f3012c79c613478e8f2c887a8259)
