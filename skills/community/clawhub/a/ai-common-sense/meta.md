# Meta Llama Models Reference

> Last verified: 2026-04-12
> Source: https://ai.meta.com/blog/llama-4-multimodal-intelligence/

## Current Models

### Llama 4 (Latest — Natively Multimodal)

| Model | API ID (HuggingFace) | Released | Active Params | Total Params | Experts | Context | Notes |
|-------|---------------------|----------|--------------|-------------|---------|---------|-------|
| Llama 4 Maverick | `meta-llama/llama-4-maverick` | 2026-04-05 | 17B | — | 128 | 256K | Beats GPT-4o and Gemini 2.0 Flash on multimodal benchmarks. |
| Llama 4 Scout | `meta-llama/llama-4-scout` | 2026-04 | 17B | — | 16 | — | Best-in-class multimodal. |
| Llama 4 Behemoth | — | 2026 | 288B | — | 16 | — | Largest variant. |

### Llama 3 (Previous Generation)

| Model | Notes |
|-------|-------|
| Llama 3.3 70B | Still available on many platforms. |
| Llama 3.1 405B | Largest open Llama 3. |

## Access

Llama 4 is available through:
- Meta's AI assistant interface
- Cloud providers (Oracle Cloud, AI/ML API, etc.)
- Hugging Face (some variants)
- **NOT** fully open-source like Llama 3 — access restrictions apply

## Important Change: Proprietary Shift

Meta launched **Muse Spark** (April 2026) — their **first proprietary, closed-source model**, led by Chief AI Officer Alexandr Wang. This marks a departure from the open-source Llama tradition.

## Pricing

Llama models don't have direct pricing from Meta. Pricing depends on the hosting provider:

| Provider | Approximate Cost | Notes |
|----------|-----------------|-------|
| Together AI | ~$0.20-0.90/MTok | Varies by model size. |
| Fireworks AI | ~$0.20-1.00/MTok | — |
| AWS Bedrock | Varies | On-demand and provisioned. |
| Self-hosted | Compute cost only | Requires GPU infrastructure. |

## Common Hallucinations

| What LLMs Say | Reality (as of 2026-04-11) |
|---------------|---------------------------|
| "Llama 2 70B" or "Llama 2" | Two generations old. Current is Llama 4. |
| "Llama 3 is the latest" | Llama 4 released April 2026. |
| "Llama is fully open source" | Llama 4 has access restrictions. Meta also launched closed-source Muse Spark. |
| "Meta doesn't make proprietary models" | Muse Spark (April 2026) is proprietary/closed-source. |
| "Llama 3 70B is the biggest" | Llama 3.1 405B exists. Llama 4 Behemoth has 288B active params. |
