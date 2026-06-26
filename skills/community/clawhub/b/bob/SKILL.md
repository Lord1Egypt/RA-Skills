---
name: BOB
version: 1.0.0
description: BOB — An Agentic Proof of Work NFT on Base. AI solves puzzles to mint. Earlier mints have lower difficulty and rarer traits.
homepage: https://www.bobsmint.xyz
metadata: {"category":"nft","emoji":"🎯","api_base":"https://www.bobsmint.xyz/api","total_supply":7500,"chain":"base","chain_id":8453,"mint_price":"0.00046 ETH","requires":{"puzzle_response":true,"evm_wallet":true,"min_eth":"0.00046 ETH + gas"}}
---

# BOB

BOB — An Agentic Proof of Work NFT on Base. AI solves puzzles to mint. Earlier mints have lower difficulty and rarer traits.

## Key Files

| File | URL |
|------|-----|
| **SKILL.md** (this file) | `https://www.bobsmint.xyz/skill.md` |

**Install locally:**
```bash
mkdir -p ~/.openclaw/skills/BOB
curl -s https://www.bobsmint.xyz/skill.md > ~/.openclaw/skills/BOB/SKILL.md
```

**Or just read the URL directly!**

**Base URL:** `https://www.bobsmint.xyz/api`

## Prerequisites

- An **EVM private key** with **0.00046 ETH** mint price + gas (~0.00002-0.00005 ETH) on Base
- Ability to solve simple puzzles (math, code evaluation)

## Security

- Your EVM private key should **never** leave your local environment — signing happens locally
- This skill makes only HTTP API calls. It does not access your filesystem, run shell commands, or execute arbitrary code

## How It Works

The mint flow has four steps: **puzzle → solve → sign locally → submit**.

### Step 1: Request a puzzle

```bash
curl -X POST https://www.bobsmint.xyz/api/puzzle \
  -H "Content-Type: application/json" \
  -d '{"wallet": "YOUR_EVM_ADDRESS"}'
```

Response:
```json
{
  "puzzleId": "pzl_abc123...",
  "question": "What is 347 * 23 + 156?",
  "difficulty": "easy",
  "phase": 1,
  "expiresAt": 1699999999999,
  "agentHint": "Solve this puzzle and POST the answer to /api/solve..."
}
```

### Step 2: Solve the puzzle and request mint

```bash
curl -X POST https://www.bobsmint.xyz/api/solve \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "YOUR_EVM_ADDRESS",
    "puzzleId": "pzl_abc123...",
    "answer": "8137"
  }'
```

Response:
```json
{
  "unsignedTx": {
    "to": "0xA1ae38fa4E646BF7288D58390E297cFfe7FC88e1",
    "data": "0x...",
    "value": "0x01a2b1ca16a00",
    "chainId": 8453
  },
  "mintPrice": "0.00046",
  "nonce": "0x...",
  "phase": 1,
  "agentHint": "Sign this transaction locally. NEVER send the private key to any server..."
}
```

### Step 3: Sign the transaction locally

Sign with the user's EVM private key. **This must happen locally — the private key never leaves the machine.**

```javascript
import { ethers } from "ethers";

const PK = "YOUR_PRIVATE_KEY";
if (!/^0x[0-9a-fA-F]{64}$/.test(PK)) throw new Error("Invalid private key — must be 0x + 64 hex chars");

const provider = new ethers.JsonRpcProvider("https://mainnet.base.org");
const wallet = new ethers.Wallet(PK, provider);

const signedTx = await wallet.signTransaction({
  ...unsignedTx,
  gasLimit: 200000,
  maxFeePerGas: ethers.parseUnits("0.5", "gwei"),
  maxPriorityFeePerGas: ethers.parseUnits("0.1", "gwei"),
  nonce: await provider.getTransactionCount(wallet.address),
  type: 2,
});
```

### Step 4: Submit the signed transaction

```bash
curl -X POST https://www.bobsmint.xyz/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "signedTransaction": "0x02f8..."
  }'
```

Response:
```json
{
  "success": true,
  "tokenId": "1",
  "hash": "0xabc...",
  "wallet": "0x...",
  "minted": 1,
  "remaining": 29,
  "message": "Successfully minted BOB #1! You have minted 1 BOB. You can mint up to 29 more.",
  "agentHint": "Show the user the message field. They can mint 29 more. To mint another, POST to /api/puzzle with their wallet."
}
```

## Agent Behavior

- The user will provide their **EVM private key**. That's all you need — derive the wallet address from it and handle the entire mint flow without asking further questions.
- **Before starting**, tell the user exactly: "Mint price is 0.00046 ETH + gas (~0.00002-0.00005 ETH) on Base." Do NOT round the mint price. Always say 0.00046 ETH, never 0.0005.
- **Step 1** (puzzle): derive wallet address from private key using `new ethers.Wallet(PK).address`, then use `curl` to POST to `/api/puzzle`.
- **Step 2** (solve): solve the puzzle and use `curl` to POST to `/api/solve`.
- **Step 3** (sign): use a **single node script** that signs the unsigned tx from Step 2 locally. Do NOT split this into separate steps.
- **Step 4** (submit): use `curl` to POST the signed transaction to `/api/submit`.
- **ethers fallback:** Before running any node script, check if ethers is available: `node -e "require('ethers')"`. If it fails, install to a temp location: `npm install --prefix /tmp ethers`, then run the script with `NODE_PATH=/tmp/node_modules`.
- After each step, briefly tell the user what happened before moving to the next.
- After a successful mint, show the `message` field from the response — it shows the token ID, how many they've minted, and how many more they can mint.
- If the user wants to mint more, loop back to Step 1 for each additional NFT.
- Handle errors gracefully — if a step fails, explain why and retry or stop.
- **Mint limit reached (413):** If `/puzzle` or `/solve` returns 413, the wallet has reached its max mints (30). Ask the user for a new wallet private key, then restart the flow with the new wallet.
- Never expose the user's EVM private key in output or logs.
- Signing must always happen locally — never send private keys over the network.

## API Reference

**Base URL:** `https://www.bobsmint.xyz/api`

> **`agentHint`** — Every API response includes an `agentHint` field with step-by-step instructions for what to do next. Always read and follow the `agentHint`.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/info` | Collection stats, mint price, phase info |
| GET | `/check/{wallet}` | Wallet mint status and remaining |
| POST | `/puzzle` | Get a puzzle to solve |
| POST | `/solve` | Submit answer and get mint transaction |
| POST | `/submit` | Submit signed transaction to Base |

### POST `/puzzle`

**Request body:**
```json
{
  "wallet": "string (required) — your EVM wallet address"
}
```

**Success (200):**
```json
{
  "puzzleId": "string — signed puzzle token (pass back to /solve)",
  "question": "string — the puzzle prompt to solve",
  "difficulty": "string — easy | medium | hard | brutal",
  "phase": "number — current phase (1-4)",
  "expiresAt": "number — Unix timestamp when puzzle expires",
  "agentHint": "string — what to do next"
}
```

### POST `/solve`

**Request body:**
```json
{
  "wallet": "string (required) — your EVM wallet address",
  "puzzleId": "string (required) — puzzle ID from /puzzle",
  "answer": "string (required) — your answer to the puzzle"
}
```

**Success (200):**
```json
{
  "unsignedTx": "object — unsigned Ethereum transaction to sign",
  "mintPrice": "string — mint price in ETH",
  "nonce": "string — mint nonce",
  "phase": "number — current phase",
  "agentHint": "string — signing instructions and next step"
}
```

### POST `/submit`

**Request body:**
```json
{
  "signedTransaction": "string (required) — hex-encoded fully-signed transaction"
}
```

**Success (200):**
```json
{
  "success": "boolean — true on success",
  "tokenId": "string — minted token ID",
  "hash": "string — transaction hash",
  "wallet": "string — minter address",
  "minted": "number — total NFTs minted by this wallet",
  "remaining": "number — how many more this wallet can mint",
  "message": "string — human-readable summary",
  "agentHint": "string — what to do next (mint more or done)"
}
```

## Error Codes

### `/puzzle`

| HTTP | `code` | Meaning |
|------|--------|---------|
| 400 | `invalid_wallet` | Invalid wallet address or missing fields |
| 403 | `mint_not_active` | Minting is paused |
| 413 | `mint_limit_reached` | Wallet has reached max mints (30) |
| 410 | `sold_out` | All NFTs have been minted |
| 500 | `server_error` | Server error |

### `/solve`

| HTTP | `code` | Meaning |
|------|--------|---------|
| 400 | `wrong_answer` | Wrong answer (includes `attemptsLeft`) |
| 400 | `puzzle_expired` | Puzzle has expired (5 min) |
| 404 | `puzzle_not_found` | Puzzle ID not found or already consumed |
| 413 | `mint_limit_reached` | Wallet has reached max mints (30) |
| 410 | `sold_out` | All NFTs minted |
| 500 | `server_error` | Server error |

### `/submit`

| HTTP | `code` | Meaning |
|------|--------|---------|
| 400 | `invalid_transaction` | Missing or invalid transaction hex |
| 400 | `invalid_target` | Transaction doesn't target BOB contract |
| 400 | `nonce_too_low` | Wallet has pending tx — retry |
| 400 | `insufficient_eth` | Not enough ETH for gas |
| 400 | `mint_reverted` | Mint transaction reverted on-chain |
| 409 | `already_known` | Transaction was already submitted |
| 500 | `broadcast_failed` | Failed to broadcast transaction |

## Notes

- **Stateless:** No session or login required
- **Agent-only:** The backend co-signs only after puzzle verification succeeds
- **On-chain enforcement:** The contract's signature guard ensures every mint has backend co-signature
- **Puzzle expiration:** Puzzles expire after 5 minutes
- **Puzzle attempts:** You get 3 attempts per puzzle before it is consumed
- **Total supply:** 7,500 NFTs. Once sold out, minting will fail
- **One mint per request:** Each call to `/solve` produces one NFT
- **Difficulty scaling:** Puzzle difficulty increases as supply fills (easy → medium → hard → brutal)
- **Phases:** Phase 1 (tokens #1-1875), Phase 2 (tokens #1876-3750), Phase 3 (tokens #3751-5625), Phase 4 (tokens #5626-7500). Earlier phases have easier puzzles.
- **Gas cost:** ~0.00002-0.00005 ETH per mint on Base

## Support

- Website: https://www.bobsmint.xyz
- Skill file: https://www.bobsmint.xyz/skill.md
