---
name: fhe-x402-payment
description: FHE-encrypted x402 payments for OpenClaw agents. Use when the agent needs to make private on-chain payments, wrap/unwrap encrypted tokens, manage escrow jobs, register agent identity, give reputation feedback, or delegate balance viewing. Runs on Ethereum Sepolia (default) or Mainnet with Zama fhEVM. Supports three wallet modes — local private key, DFNS MPC, and Ledger hardware wallet.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - RPC_URL
      anyBins:
        - node
    primaryEnv: USER_PRIVATE_KEY
    emoji: "🔐"
    homepage: "https://gitlab.com/bea7892046/fhex402"
---

# FHE x402 Payment Skill

Private, encrypted payments for autonomous agents on Ethereum using Zama's Fully Homomorphic Encryption (fhEVM). All payment amounts are encrypted on-chain — only the payer and payee can see them.

## Quick Start

Set a wallet and RPC, then run any command:

```bash
# Minimal setup (local dev)
export USER_PRIVATE_KEY=0x...
export RPC_URL=https://sepolia.infura.io/v3/YOUR_KEY

# Check wallet info
run info

# Wrap 10 USDC into encrypted cUSDC
run wrap --amount 10

# Send 1 encrypted cUSDC
run pay --to 0xRecipient --amount 1

# Check balance (with optional decrypt)
run balance
run balance --decrypt true
```

## Commands

### Token Operations

| Command | Description | Required Args |
|---------|-------------|---------------|
| `wrap` | Wrap USDC into encrypted cUSDC (ERC-7984) | `--amount` |
| `unwrap` | Initiate unwrap of cUSDC back to USDC (step 1 of 2) | `--amount` |
| `finalize-unwrap` | Complete unwrap via KMS decryption proof | `--handle` (recommended) or `--requestId --cleartextAmount --proof` (legacy) |
| `pay` | Send encrypted cUSDC via verifier relay | `--to --amount` |
| `balance` | Check USDC + cUSDC balances | Optional: `--decrypt true`, `--of 0xAddress` |
| `info` | Display wallet, network, and contract addresses | (none) |

### Escrow (Agentic Commerce Protocol — ERC-8183)

| Command | Description | Required Args |
|---------|-------------|---------------|
| `create-job` | Create an escrow job with provider + evaluator | `--provider --evaluator --expiry --description` Optional: `--hook` |
| `fund-job` | Encrypt budget + fund a job (3-step TX) | `--jobId --amount` |
| `complete-job` | Approve or reject a submitted job | `--jobId --action` (approve/reject) Optional: `--reason` |

### Identity & Reputation (ERC-8004)

| Command | Description | Required Args |
|---------|-------------|---------------|
| `register-agent` | Mint an agent identity NFT | `--uri` |
| `give-feedback` | Submit proof-linked reputation feedback | `--agentId --score --nonce` Optional: `--tag1 --tag2 --endpoint --feedbackURI --feedbackHash` |

### Delegation (FHE Viewing Keys)

| Command | Description | Required Args |
|---------|-------------|---------------|
| `grant-view` | Grant read access to your encrypted balance | `--delegate` Optional: `--hours --permanent --contract` |
| `revoke-view` | Revoke a delegate's view access | `--delegate` |
| `view-as` | Read another agent's balance via delegation | `--delegator` |

### Demo Orchestrators

| Command | Description | Required Args |
|---------|-------------|---------------|
| `research-and-visualize` | Chain 3 paid API calls (search + LLM + image) | `--query` |
| `review-and-rate` | Buy a code review + submit feedback | `--code` Optional: `--language --score` |

## Wallet Modes

Set `WALLET_MODE` to choose explicitly, or omit for auto-detection (DFNS > user key):

| Mode | Env Var | Best For |
|------|---------|----------|
| `user` | `USER_PRIVATE_KEY` | Local development, testing |
| `dfns` | `DFNS_WALLET_ID` + `DFNS_AUTH_TOKEN` + `DFNS_CREDENTIAL_ID` + (`DFNS_CREDENTIAL_PRIVATE_KEY` or `DFNS_PRIVATE_KEY_PATH`) | Unattended MPC agents |
| `ledger-bridge` | `LEDGER_BRIDGE_URL` + `LEDGER_BRIDGE_TOKEN` | Supervised hardware wallet |

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `RPC_URL` | Ethereum RPC endpoint (default: Sepolia public node) |
| `USER_PRIVATE_KEY` or `DFNS_WALLET_ID` | At least one wallet source |

### Optional

| Variable | Description |
|----------|-------------|
| `CHAIN` | `mainnet` or `sepolia` (auto-detected from RPC_URL) |
| `CUSDC_ADDRESS` | Override cUSDC token address |
| `VERIFIER_ADDRESS` | Override X402PaymentVerifier address |
| `ESCROW_ADDRESS` | Override AgenticCommerceProtocol address |
| `IDENTITY_ADDRESS` | Override AgentIdentityRegistry address |
| `REPUTATION_ADDRESS` | Override AgentReputationRegistry address |

All contract addresses auto-fill for Sepolia when `RPC_URL` points to chain ID 11155111.

## How It Works

1. **Encrypted Payments**: Uses Zama's fhEVM to encrypt USDC into cUSDC (ERC-7984). All transfers are confidential — amounts are FHE-encrypted on-chain.
2. **x402 Protocol**: Implements the HTTP 402 payment flow — servers return `402 Payment Required`, the agent encrypts and pays, then retries with a payment proof header.
3. **Escrow**: The AgenticCommerceProtocol (ERC-8183) holds encrypted budgets in escrow. Jobs flow through: create → setBudget → fund → submit → complete/reject.
4. **Identity**: Agents register as ERC-721 NFTs with EIP-712 wallet linking and on-chain metadata.
5. **Reputation**: Proof-of-payment feedback system prevents sybil attacks on agent ratings.

## Deployed Contracts (Sepolia)

| Contract | Address |
|----------|---------|
| cUSDC (ERC-7984) | `0x7c5BF43B851c1dff1a4feE8dB225b87f2C223639` |
| X402PaymentVerifier | `0xD46E80E1d37116B44c7Bfd845A110FCbB93d3E9F` |
| AgenticCommerceProtocol | `0xECD7a2382A5F0e3b6A7b76536e4CAE11215Cc695` |
| AgentIdentityRegistry | `0x36666464daa16442Fc1d901acfC9419f11407741` |
| AgentReputationRegistry | `0x1649d762Ee62f194D92B93510b8f10a501cE9fD5` |

## Output Format

All commands return JSON strings: `{ "ok": true, ... }` on success, `{ "ok": false, "error": "..." }` on failure. Commands never throw — errors are returned as JSON.
