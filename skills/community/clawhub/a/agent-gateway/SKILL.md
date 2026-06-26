---
name: Agent Gateway
description: Smart multi-model routing — use Claude, GPT, Gemini, or local Ollama models with automatic cost optimization, fallback chains, and usage tracking.
version: 1.0.0
author: claws-shield
tags:
  - gateway
  - multi-model
  - routing
  - cost-optimization
  - llm
user-invocable: true
argument-hint: "start [--port 8787]"
when_to_use: "When you want to route LLM requests across multiple providers with cost optimization, fallback chains, or usage tracking."
allowed-tools:
  - Bash
---

# Agent Gateway

You are the **Claws-Shield Agent Gateway** — a smart multi-model routing proxy that runs locally.

## What You Do

1. **Multi-Provider Support** — Route requests to Anthropic Claude, OpenAI GPT, Google Gemini, or local Ollama models
2. **Smart Routing** — 3 strategies: cheapest-viable, best-quality, balanced
3. **Fallback Chains** — If provider A fails, automatically try provider B
4. **Cost Tracking** — Per-request cost calculation, daily/weekly/monthly aggregation
5. **Health Monitoring** — Circuit breaker pattern, automatic provider health checking
6. **OpenAI-Compatible API** — Drop-in replacement with `/v1/chat/completions` endpoint

## How to Use

Start the gateway server:

```bash
npx @claws-shield/cli gateway --port 8787
```

Or programmatically:

```bash
node scripts/start-gateway.mjs
```

Then send requests to `http://localhost:8787/v1/chat/completions` using any OpenAI-compatible client.

## Configuration

Set provider API keys via environment variables:
- `ANTHROPIC_API_KEY` — For Claude models
- `OPENAI_API_KEY` — For GPT models
- `GEMINI_API_KEY` — For Gemini models
- Ollama requires no key (connects to localhost:11434)

## Routing Strategies

| Strategy | Description |
|----------|-------------|
| `cheapest` | Pick the lowest-cost model that meets requirements |
| `best-quality` | Pick the most capable model available |
| `balanced` | Best value: quality per dollar |

## Privacy

All usage data stays local. The gateway never phones home. Your API keys are never transmitted to third parties.
