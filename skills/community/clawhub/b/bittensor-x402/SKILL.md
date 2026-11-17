---
name: bittensor-x402
description: "Decentralized AI inference via Bittensor SN64 (43+ chat models) and SN19 (image gen) plus embeddings — OpenAI-compatible, paid in USDC on Base/Solana via Spraay x402. No Bittensor wallet needed. Censorship-resistant, keyless."
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - bash
        - curl
---

# Bittensor Decentralized AI 🧬

Decentralized AI inference routed through the Bittensor network — **no Bittensor wallet, no TAO, no subnet registration required**. Your agent pays USDC per call via x402 and the Spraay gateway handles the Bittensor routing.

- **SN64 (Chutes)** — 43+ chat models, fully OpenAI `/v1/chat/completions` compatible
- **SN19 (Nineteen AI)** — image generation, OpenAI `/v1/images/generations` compatible
- **Embeddings** — text embeddings, OpenAI `/v1/embeddings` compatible

Every response comes from decentralized miners competing on quality. Same API shape as OpenAI, different infrastructure underneath.

## ⚠️ Before you install

> **This skill sends your prompts and data to the Bittensor decentralized network** via the Spraay x402 gateway (`gateway.spraay.app`).
>
> - **External transmission:** Prompts, text, and image requests leave your local environment and are routed to Bittensor subnet miners through the gateway. The gateway operator and Bittensor miners process your inputs.
> - **Real money:** Each call costs USDC via x402 micropayments. Your agent's wallet is debited per request ($0.001–$0.05 per call).
> - **Decentralized routing:** Responses come from competing miners on the Bittensor network. Response quality and latency may vary more than centralized providers. Model availability depends on active miners.
> - **Privacy:** The gateway operator and Bittensor validators/miners may see your prompts and inputs. Do not send sensitive or proprietary content unless you accept this.
>
> **Use a dedicated wallet with limited funds for testing.**

## How to call endpoints

```bash
bash {baseDir}/scripts/bittensor.sh METHOD ENDPOINT '{"key":"value"}'
```

The script requires `bash` and `curl`. All calls go to `https://gateway.spraay.app`.

## Why Bittensor over centralized inference?

- **Censorship-resistant** — no single provider can block or filter your requests
- **Competitive quality** — miners compete for rewards, driving model quality up
- **No vendor lock-in** — OpenAI-compatible API shape means easy swap-in
- **Different aesthetic** — image generation via SN19 produces a distinct visual style from FLUX/SDXL
- **Decentralization signal** — relevant for agents operating in Web3/crypto contexts where decentralized infrastructure matters

## When to use this skill

Use this skill when the user explicitly wants decentralized or Bittensor-specific inference:

- "Use Bittensor", "decentralized AI", "SN64", "SN19", "Chutes", "Nineteen AI"
- "Run this through a decentralized model"
- "I want censorship-resistant inference"
- "Generate an image on Bittensor"

For centralized compute with more models and predictable latency, use the **Spraay Compute & Futures** skill instead.

## Available endpoints (4 tools)

### List Models — $0.001

List all available decentralized models on Bittensor. Returns model IDs, capabilities, and pricing. Call this first to see what's available.

```bash
bash {baseDir}/scripts/bittensor.sh GET /bittensor/v1/models '{}'
```

OpenAI `/v1/models` compatible response format.

### Chat Completions — $0.03

Chat completions via Bittensor SN64 (Chutes). 43+ models including Llama, Mistral, DeepSeek, Qwen, and more. Fully OpenAI-compatible — supports system prompts, temperature, max_tokens, and multi-turn conversation.

```bash
bash {baseDir}/scripts/bittensor.sh POST /bittensor/v1/chat/completions '{
  "model": "hugging-quants/Meta-Llama-3.1-70B-Instruct-AWQ-INT4",
  "messages": [
    {"role": "system", "content": "You are a helpful DeFi analyst."},
    {"role": "user", "content": "Explain impermanent loss in two sentences."}
  ],
  "max_tokens": 200,
  "temperature": 0.7
}'
```

**Tips:**
- Use `model` from the `/bittensor/v1/models` list — model availability depends on active miners
- Multi-turn works — pass the full conversation history in `messages`
- Response format matches OpenAI: `choices[0].message.content`

### Image Generation — $0.05

Image generation via Bittensor SN19 (Nineteen AI). OpenAI `/v1/images/generations` compatible. Produces a distinct visual style compared to centralized FLUX/SDXL.

```bash
bash {baseDir}/scripts/bittensor.sh POST /bittensor/v1/images/generations '{
  "prompt": "a neon-lit cyberpunk street market at night, rain-slicked pavement, volumetric fog",
  "n": 1,
  "size": "1024x1024"
}'
```

**Tips:**
- Returns a URL to the generated image
- Good for: artistic/stylized images, concept art, social media visuals
- Different aesthetic from FLUX — try both and compare for your use case

### Embeddings — $0.005

Text embeddings via Bittensor. OpenAI `/v1/embeddings` compatible. Use for semantic search, RAG pipelines, document clustering, and similarity matching.

```bash
bash {baseDir}/scripts/bittensor.sh POST /bittensor/v1/embeddings '{
  "input": "Decentralized AI inference via Bittensor subnet miners"
}'
```

Returns a vector array compatible with any vector database (Pinecone, Weaviate, ChromaDB, pgvector).

## Cost reference

| Endpoint         | Method | Price  | Bittensor Subnet |
| ---------------- | ------ | ------ | ---------------- |
| Models           | GET    | $0.001 | —                |
| Chat Completions | POST   | $0.03  | SN64 (Chutes)    |
| Image Generation | POST   | $0.05  | SN19 (Nineteen)  |
| Embeddings       | POST   | $0.005 | Bittensor        |

**Total cost for a typical workflow** (list models + chat + image): ~$0.08 USDC

## Workflows

**Decentralized content creation** — use chat completions for copy, image generation for visuals. Fully decentralized pipeline with no centralized AI provider in the loop.

**RAG with decentralized embeddings** — embed documents via Bittensor, store in a vector DB, retrieve and answer with Bittensor chat completions. End-to-end decentralized knowledge pipeline.

**A/B testing against centralized models** — run the same prompt through Bittensor chat and through the centralized Spraay Compute text-inference endpoint, compare quality and latency.

**Web3-native agents** — agents operating in crypto/DeFi contexts where using decentralized infrastructure is a feature, not just a choice. Useful for trust signaling and alignment with decentralization values.

## Changelog

### v1.0.0

- Initial release with 4 Bittensor endpoints: models, chat completions (SN64), image generation (SN19), embeddings.

## Related terms

Bittensor, SN64, SN19, Chutes, Nineteen AI, decentralized AI, decentralized inference,
censorship-resistant AI, TAO, OpenAI compatible, agent inference, x402 payments,
USDC micropayments, keyless AI, Web3 AI, decentralized embeddings, subnet mining
