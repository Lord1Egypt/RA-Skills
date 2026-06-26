# OpenClaw Miner Engine

Core mining engine for the Clawing protocol. Handles AI API calls, Oracle verification, and on-chain minting of CLAW tokens.

## Overview

This engine is used internally by AI Agent Skills to automate CLAW mining. It is not intended to be run directly — install the **CLAW Mining Skill** on a compatible AI Agent platform and the agent will handle everything automatically.

For mining instructions, see the [Mining Guide](../docs/MINING_GUIDE.md).

## Architecture

```
Miner Engine (Node.js/TypeScript)
    │
    ├── 1. Read chain state (Era, Epoch, Seed, Cooldown)
    ├── 2. Check gas price (abort early if too high, saves API costs)
    ├── 3. Request nonce from Oracle (format-validated)
    ├── 4. Call AI API (grok-4.1-fast via xAI or OpenRouter)
    ├── 5. Submit AI response to Oracle for verification + signing
    ├── 6. Validate attestation (miner address, deadline, field integrity)
    └── 7. Send mint() transaction on-chain with Oracle signature
             → CLAW tokens minted to miner's wallet
```

## Configuration

All settings via `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `PRIVATE_KEY` | Miner wallet private key | (required) |
| `AI_API_KEY` | OpenAI-compatible API key | (required) |
| `AI_API_URL` | Chat completions endpoint | `https://api.x.ai/v1/chat/completions` |
| `AI_MODEL` | Model name (must match on-chain Era model) | `grok-4.1-fast` |
| `ORACLE_URL` | Oracle server URL | `http://localhost:3000` |
| `RPC_URL` | Ethereum RPC URL | (required) |
| `POAIW_MINT_ADDRESS` | PoAIWMint contract address | (required) |
| `MAX_GAS_PRICE_GWEI` | Max gas price limit | `2` |
| `TASK_PROMPT` | Custom task text for prompt | `Explain quantum computing in detail.` |

## Testing

```bash
npm test
```

## Build

```bash
npm run build
```
