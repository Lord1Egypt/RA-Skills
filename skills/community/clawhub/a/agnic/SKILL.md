---
name: agnic
description: >
  Complete AI agent wallet with payments, trading, email, and on-chain identity.
  Use when the user wants to manage their agent's wallet, make payments, trade tokens,
  send/receive email, or check their agent identity.
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx agnic@latest *)"]
---

## Agnic — Unified Agent Wallet Skill

This skill gives your AI agent a full identity stack: wallet, email, payments, trading, and on-chain identity.

### Authentication

```bash
npx agnic@latest auth login    # Opens browser for OAuth login
npx agnic@latest auth logout   # Clear stored credentials
```

### Balance & Funding

```bash
npx agnic@latest balance --json                     # All networks
npx agnic@latest balance --network base --json      # Specific network
npx agnic@latest address                            # Show wallet address
```

Supported networks: `base`, `solana`, `base-sepolia`, `solana-devnet`

### X402 Payments

```bash
# Search for APIs
npx agnic@latest x402 search "weather data" --json

# Preview cost before paying
npx agnic@latest x402 preview <url>

# Make a paid API call
npx agnic@latest x402 pay <url> --method GET --json
```

### Token Trading

```bash
# Get a quote
npx agnic@latest trade quote 10 USDC ETH --json

# Execute a trade (Base mainnet only)
npx agnic@latest trade 10 USDC ETH --json
```

Supported tokens: USDC, ETH, WETH, cbETH, DAI, AERO

### Send USDC

```bash
npx agnic@latest send <amount> <address> --network base --json
```

### Agent Identity

```bash
npx agnic@latest agent-identity --json    # ERC-8004 identity, trust score, delegation
npx agnic@latest status --json            # General account status
```

### Agent Email

```bash
npx agnic@latest email address --json                     # Show email alias
npx agnic@latest email setup --display-name "My Agent"    # Create email alias
npx agnic@latest email inbox --limit 10 --json            # Check inbox
npx agnic@latest email send --to user@example.com --subject "Hello" --body "Message"
npx agnic@latest email reply --message-id <id> --body "Reply text"
```

### AI Gateway

```bash
# List available AI models
npx agnic@latest ai models --json
npx agnic@latest ai models --provider openai --json

# Chat with an AI model
npx agnic@latest ai chat --model openai/gpt-4o --prompt 'Explain quantum computing' --json
npx agnic@latest ai chat --model meta-llama/llama-3.3-70b --prompt 'Summarize this text' --json

# Generate an image
npx agnic@latest ai image --prompt 'A sunset over mountains' --output sunset.png
npx agnic@latest ai image --prompt 'Logo design' --aspect-ratio 16:9 --output logo.png
```

340+ models from OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, and more.
Model format: `provider/model-name` (e.g., `openai/gpt-4o`, `google/gemini-2.5-flash-image`)
Free models: `meta-llama/*`, `google/gemma-*`, `mistralai/*`

### Workflow: Sign Up + Pay + Report

1. Check auth: `npx agnic@latest status --json`
2. Sign up for a service using agent email (`email send`)
3. Check inbox for verification (`email inbox`)
4. Reply to verify (`email reply`)
5. Make paid API call (`x402 pay`)
6. Email results to user (`email send`)
