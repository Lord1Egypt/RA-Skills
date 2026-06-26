---
name: primer-chutes
description: Build a pay-per-inference proxy for Bittensor Chutes AI. Accept USDC payments for decentralized AI inference using x402.
metadata: {"openclaw":{"emoji":"🧠","requires":{"anyBins":["node","npx","python3","pip"]}}}
---

# Chutes AI Proxy (x402)

Build a pay-per-inference proxy for [Bittensor Chutes](https://chutes.ai/) (Subnet 64). Accept USDC payments on Base and forward requests to Chutes' decentralized AI network.

## When to Use This Skill

Use this skill when the user wants to:
- **Build an AI inference API** that accepts crypto payments
- **Wrap Chutes/Bittensor** with their own pricing
- **Create a pay-per-request AI service** without subscriptions
- **Monetize AI access** using stablecoins
- Set up a **Bittensor-powered AI endpoint**

## How to Respond

| User Says/Asks | What to Do |
|----------------|------------|
| "Create a Chutes proxy" | Run `x402 create chutes-proxy my-proxy` |
| "I want to sell AI inference" | Scaffold the proxy, explain the business model |
| "How do I accept payments for AI?" | Explain x402 + Chutes, offer to scaffold |
| "Set up Bittensor integration" | Run the create command |
| "What models does Chutes support?" | List models (DeepSeek, Llama, Qwen, etc.) |

## Quick Start

### Node.js / TypeScript

```bash
npx @primersystems/x402 create chutes-proxy my-ai-proxy
cd my-ai-proxy
npm install
cp .env.example .env
# Edit .env with your Chutes API key and wallet address
npm run dev
```

### Python

```bash
pip install primer-x402
x402 create chutes-proxy my-ai-proxy
cd my-ai-proxy
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Chutes API key and wallet address
uvicorn main:app --reload
```

## How It Works

```
User Request
     |
     v
[Your Proxy] -- No payment? --> Return 402 + price
     |
     v
User signs USDC payment (gasless)
     |
     v
[Your Proxy] -- Verify payment --> [Primer Facilitator]
     |
     v
[Chutes API] -- Forward request --> Bittensor Subnet 64
     |
     v
AI Response returned to user
```

You pre-pay Chutes with your API credits. Users pay YOU in USDC. You keep the margin.

## Configuration

After scaffolding, edit `.env`:

| Variable | Description | Required |
|----------|-------------|----------|
| `CHUTES_API_KEY` | Your Chutes API key from chutes.ai | Yes |
| `WALLET_ADDRESS` | Your wallet to receive USDC | Yes |
| `PRICE_PER_1K_TOKENS` | Your price in USD (default: 0.001) | No |
| `FACILITATOR_URL` | x402 facilitator (default: Primer's) | No |

## Getting a Chutes API Key

1. Go to [chutes.ai](https://chutes.ai/)
2. Sign up / connect wallet
3. Subscribe to a tier ($3/month base)
4. Generate API key (starts with `cpk_`)

## Deployment

### Cloudflare Workers (TypeScript - Free)

```bash
wrangler login
wrangler secret put CHUTES_API_KEY
wrangler secret put WALLET_ADDRESS
npm run deploy
```

### Docker (Python)

```bash
docker build -t chutes-proxy .
docker run -p 8000:8000 --env-file .env chutes-proxy
```

### Other Platforms

- **fly.io**: `fly launch && fly secrets set CHUTES_API_KEY=xxx`
- **Railway/Render**: Connect repo, set env vars in dashboard
- **Vercel Edge**: Build and deploy TypeScript version

## API Endpoints

Your proxy exposes:

| Endpoint | Description | Payment |
|----------|-------------|---------|
| `GET /` | Health check | Free |
| `POST /v1/chat/completions` | Chat completions (OpenAI-compatible) | Required |
| `GET /v1/models` | List available models | Free |

## Supported Models

Any model on Chutes, including:
- `deepseek-ai/DeepSeek-V3`
- `Qwen/Qwen3-235B-A22B`
- `meta-llama/Llama-3.1-70B-Instruct`
- `meta-llama/Llama-3.1-8B-Instruct`

See [chutes.ai](https://chutes.ai/) for the full list.

## Pricing Strategy

The proxy estimates tokens and charges upfront:

```
Price = (estimated_tokens / 1000) * PRICE_PER_1K_TOKENS
```

Set `PRICE_PER_1K_TOKENS` higher than Chutes' cost to make margin. Example:
- Chutes costs you ~$0.0005/1K tokens
- You charge $0.001/1K tokens
- You keep 50% margin

## Limitations

- **Streaming not supported** - Template doesn't handle `stream: true`
- **Token estimation is approximate** - Uses ~4 chars/token heuristic
- **Pre-payment only** - No post-inference reconciliation

## Use Cases

| Who | Why |
|-----|-----|
| **AI agent operators** | Give agents paid AI access without API keys |
| **API resellers** | Wrap Chutes with your branding/pricing |
| **Privacy services** | AI without accounts or KYC |
| **Bittensor miners** | Add stablecoin revenue stream |

## Testing Your Proxy

```bash
# Should return 402 Payment Required
curl http://localhost:8787/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'

# Pay and get response (using x402 CLI)
npx @primersystems/x402 pay http://localhost:8787/v1/chat/completions \
  --max-amount 0.01 \
  --method POST \
  --body '{"messages":[{"role":"user","content":"Hello"}]}'
```

## Links

- **Chutes AI**: https://chutes.ai
- **Bittensor**: https://bittensor.com
- **x402 Protocol**: https://x402.org
- **Primer Systems**: https://primer.systems
- **SDK Documentation**: https://x402.org/docs/bittensor.html
- **GitHub**: https://github.com/primer-systems/x402
