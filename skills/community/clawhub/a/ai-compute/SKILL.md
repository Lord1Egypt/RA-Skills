---
name: ai-compute-x402
description: 27-tool AI compute agent — LLM inference, image generation, video generation, text-to-speech, speech-to-text, embeddings, GPU inference, Bittensor decentralized AI, on-chain AI analytics, and prepaid compute futures via x402.
version: 1.0.0
homepage: https://github.com/plagtech/ai-compute-skill
metadata:
  openclaw:
    primaryEnv: RESEARCH_API_KEY
    envVars:
      - name: RESEARCH_API_KEY
        required: true
        description: API key or x402 subscription key for the gateway.
      - name: RESEARCH_GATEWAY_URL
        required: false
        description: Gateway URL. Defaults to https://gateway.spraay.app
    requires:
      bins:
        - curl
        - python3
---

# AI Compute

27 endpoints for managed AI compute — LLM text inference across 11 models, image generation (FLUX, SDXL), video generation, TTS, STT, embeddings, GPU inference via Replicate, decentralized AI via Bittensor, on-chain intelligence, and prepaid compute credits. Each call is a real x402 micropayment ($0.001–$0.50 USDC).

## How to call endpoints

```bash
bash {baseDir}/scripts/compute.sh METHOD ENDPOINT '{"key":"value"}'
```

## Workflow strategies

**Content generation pipeline** — use text-inference for copy, image-generation for visuals, text-to-speech to narrate, video-generation for clips. Chain them together for full multimedia output.

**RAG / knowledge apps** — use embeddings to vectorize documents, then text-inference to answer questions against them. Pair with the deep-research-x402 skill for source retrieval.

**Audio transcription** — use speech-to-text to transcribe, then text-inference to summarize or extract action items.

**On-chain intelligence** — use classify-address to profile wallets, classify-tx to categorize transactions, explain-contract to audit smart contracts, summarize for intelligence briefings.

**Cost optimization** — use compute-futures to prepay credits at a discount, then execute jobs against the balance. Check pricing tiers before large workloads.

**Decentralized AI** — Bittensor endpoints route inference through the decentralized Bittensor network instead of centralized providers.

## Available endpoints (27 tools)

### Managed Compute (8 endpoints)

**Text Inference** — $0.003–$0.10
LLM text inference across 11 models. Supports system prompts, temperature, and max tokens.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute/text-inference '{"model":"llama-3.1-8b","prompt":"Explain zero knowledge proofs simply","max_tokens":500}'
```

**Image Generation** — $0.02–$0.08
AI image generation via FLUX and SDXL models.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute/image-generation '{"prompt":"futuristic city skyline at sunset, cyberpunk style","model":"flux"}'
```

**Video Generation** — $0.40–$0.50
AI video generation from text prompts.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute/video-generation '{"prompt":"a drone flying over mountain landscape","duration":5}'
```

**Text to Speech** — $0.03–$0.05
Convert text to natural speech audio.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute/text-to-speech '{"text":"Welcome to the future of AI compute.","voice":"alloy"}'
```

**Speech to Text** — $0.02
Transcribe audio to text.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute/speech-to-text '{"audio_url":"https://example.com/audio.mp3"}'
```

**Embeddings** — $0.005
Generate text embeddings for RAG, search, and similarity.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute/embeddings '{"text":"zero knowledge proofs for blockchain scalability"}'
```

**Batch Compute** — $0.05
Submit up to 50 compute jobs in one call with 10% discount.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute/batch '{"jobs":[{"type":"text-inference","prompt":"Summarize DeFi"},{"type":"embeddings","text":"DeFi protocols"}]}'
```

**Job Status** — $0.001
Poll the status of an async compute job.
```bash
bash {baseDir}/scripts/compute.sh GET /api/v1/compute/status/:jobId '{}'
```

### GPU Inference (3 endpoints)

**GPU Run** — $0.06
Run GPU inference via Replicate. Supports any public Replicate model.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/gpu/run '{"model":"stability-ai/sdxl","input":{"prompt":"astronaut riding a horse"}}'
```

**GPU Status** — $0.005
Poll GPU prediction status.
```bash
bash {baseDir}/scripts/compute.sh GET /api/v1/gpu/status/:id '{}'
```

**GPU Models** — FREE
List available GPU model shortcuts.
```bash
bash {baseDir}/scripts/compute.sh GET /api/v1/gpu/models '{}'
```

### AI Chat (2 endpoints)

**Chat Completions** — $0.04
OpenAI-compatible chat completions endpoint. Multi-turn conversations.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/chat/completions '{"messages":[{"role":"user","content":"What is restaking?"}]}'
```

**Available Models** — $0.001
List available AI models and their capabilities.
```bash
bash {baseDir}/scripts/compute.sh GET /api/v1/models '{}'
```

### On-Chain AI Intelligence (4 endpoints)

**Classify Address** — $0.03
AI-powered wallet classification — identify wallet type, risk level, and activity patterns.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/inference/classify-address '{"address":"0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

**Classify Transaction** — $0.03
AI-powered transaction classification — categorize tx type, parties, and risk.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/inference/classify-tx '{"txHash":"0x..."}'
```

**Explain Contract** — $0.03
AI-powered smart contract explanation — what the contract does in plain English.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/inference/explain-contract '{"address":"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"}'
```

**Intelligence Briefing** — $0.03
AI-generated intelligence briefing on a topic, address, or protocol.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/inference/summarize '{"topic":"Lido staking protocol"}'
```

### Bittensor Decentralized AI (4 endpoints)

**Bittensor Chat** — $0.03
Chat completions routed through the decentralized Bittensor network.
```bash
bash {baseDir}/scripts/compute.sh POST /bittensor/v1/chat/completions '{"messages":[{"role":"user","content":"Explain subnet mining"}]}'
```

**Bittensor Image Gen** — $0.05
Image generation via Bittensor subnets.
```bash
bash {baseDir}/scripts/compute.sh POST /bittensor/v1/images/generations '{"prompt":"neural network visualization, abstract art"}'
```

**Bittensor Embeddings** — $0.005
Text embeddings via Bittensor.
```bash
bash {baseDir}/scripts/compute.sh POST /bittensor/v1/embeddings '{"input":"decentralized machine learning"}'
```

**Bittensor Models** — $0.001
List available Bittensor models.
```bash
bash {baseDir}/scripts/compute.sh GET /bittensor/v1/models '{}'
```

### Compute Futures — Prepaid Credits (6 endpoints)

**Deposit** — $0.01
Deposit USDC to open a prepaid compute credit account with tiered discounts.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute-futures/deposit '{"amount":10}'
```

**Check Balance** — $0.001
Check remaining credit balance, tier, discount rate, and usage stats.
```bash
bash {baseDir}/scripts/compute.sh GET /api/v1/compute-futures/balance '{}'
```

**Execute Job** — $0.001
Run a compute job deducted from prepaid balance.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute-futures/execute '{"type":"text-inference","prompt":"Summarize this quarter"}'
```

**Usage History** — $0.002
Full usage ledger for your compute credits.
```bash
bash {baseDir}/scripts/compute.sh GET /api/v1/compute-futures/history '{}'
```

**Refund** — $0.01
Refund unused credit balance to the original depositor.
```bash
bash {baseDir}/scripts/compute.sh POST /api/v1/compute-futures/refund '{}'
```

**Pricing** — $0.001
View compute futures pricing tiers and discount rates.
```bash
bash {baseDir}/scripts/compute.sh GET /api/v1/compute-futures/pricing '{}'
```

## Cost reference

| Endpoint | Cost | Category |
|----------|------|----------|
| GPU Models | FREE | GPU |
| Job Status | $0.001 | Compute |
| Available Models | $0.001 | Chat |
| Bittensor Models | $0.001 | Bittensor |
| CF Balance | $0.001 | Futures |
| CF Execute | $0.001 | Futures |
| CF Pricing | $0.001 | Futures |
| CF History | $0.002 | Futures |
| Text Inference | $0.003–$0.10 | Compute |
| Embeddings | $0.005 | Compute |
| Bittensor Embeddings | $0.005 | Bittensor |
| GPU Status | $0.005 | GPU |
| CF Deposit | $0.01 | Futures |
| CF Refund | $0.01 | Futures |
| Speech to Text | $0.02 | Compute |
| Image Generation | $0.02–$0.08 | Compute |
| Classify Address | $0.03 | Inference |
| Classify Transaction | $0.03 | Inference |
| Explain Contract | $0.03 | Inference |
| Intelligence Briefing | $0.03 | Inference |
| Bittensor Chat | $0.03 | Bittensor |
| TTS | $0.03–$0.05 | Compute |
| Chat Completions | $0.04 | Chat |
| Batch Compute | $0.05 | Compute |
| Bittensor Image Gen | $0.05 | Bittensor |
| GPU Run | $0.06 | GPU |
| Video Generation | $0.40–$0.50 | Compute |

Compute powered by Replicate, Bittensor, and managed inference infrastructure.
