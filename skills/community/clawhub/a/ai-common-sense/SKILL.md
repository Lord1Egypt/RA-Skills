---
name: ai-common-sense
description: |
  Use when user mentions model names, versions, pricing, API IDs,
  "which model should I use", "what's the latest model",
  "model comparison", "API pricing", "what models are available",
  "哪個模型最新", "模型比較", "API 定價",
  or when generating code that references specific AI model IDs.
version: 0.1.1
allowed-tools: Bash, Read, WebSearch, WebFetch
---

# AI Common Sense: Stop Hallucinating Model Names

LLMs frequently hallucinate model names, versions, pricing, and API identifiers because their training data has a cutoff date. This skill provides a verified quick reference and teaches AI agents how to self-verify when the reference may be stale.

## Why This Exists

| What LLMs Commonly Get Wrong | Example |
|------------------------------|---------|
| **Outdated flagship models** | Saying "GPT-4o" when GPT-5.4 is current |
| **Deprecated model IDs** | Using `claude-3-5-sonnet-20241022` (deprecated Jan 2026) |
| **Wrong pricing** | Quoting old rates that changed months ago |
| **Phantom models** | Referencing "GPT-4-turbo" or "Gemini Ultra" (deprecated/renamed) |
| **Wrong API format** | Using `Authorization: Bearer` for Anthropic (should be `x-api-key`) |
| **Stale deprecation status** | Not knowing DALL-E 3 is shutting down |

## Quick Reference (Last verified: 2026-04-12)

### Current Flagship Models

| Provider | Flagship | API ID | Input $/MTok | Output $/MTok | Released |
|----------|----------|--------|-------------|--------------|----------|
| **OpenAI** | GPT-5.4 | `gpt-5.4` | $2.50 | $15.00 | 2026-03-17 |
| **OpenAI** | GPT-5.4 Mini | `gpt-5.4-mini` | $0.75 | $4.50 | 2026-03-17 |
| **OpenAI** | GPT-5.4 Nano | `gpt-5.4-nano` | $0.20 | $1.25 | 2026-03-17 |
| **OpenAI** | o3 (reasoning) | `o3` | $2.00 | $8.00 | 2025-04 |
| **Anthropic** | Claude Opus 4.6 | `claude-opus-4-6` | $5.00 | $25.00 | 2026-02-05 |
| **Anthropic** | Claude Sonnet 4.6 | `claude-sonnet-4-6` | $3.00 | $15.00 | 2026-02-17 |
| **Anthropic** | Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | $1.00 | $5.00 | 2025-10 |
| **Google** | Gemini 3.1 Pro | `gemini-3-1-pro-latest` | $2.00 | $12.00 | 2026-02-19 |
| **Google** | Gemini 3 Flash | `gemini-3-flash-latest` | $0.50 | $3.00 | 2026-03 |
| **Google** | Gemini 2.5 Flash-Lite | `gemini-2.5-flash-lite` | $0.10 | $0.40 | 2025 |
| **Meta** | Llama 4 Maverick | `meta-llama/llama-4-maverick` | varies | varies | 2026-04-05 |
| **Mistral** | Small 4 | `mistral-small-latest` | $0.15 | $0.60 | 2026-03-16 |
| **Mistral** | Large 3 | `mistral-large-latest` | $2.00 | $6.00 | 2025-12 |
| **DeepSeek** | V3 | `deepseek-chat` | $0.32 | $0.89 | 2025 |
| **DeepSeek** | R1 (reasoning) | `deepseek-reasoner` | — | — | 2025 |
| **Cohere** | Command A Reasoning | `command-a-reasoning` | ~$6.25 | — | 2026 |

### Recently Deprecated (Do NOT Use)

| Model | Provider | Deprecated | Replacement |
|-------|----------|-----------|-------------|
| GPT-4o | OpenAI | 2026-02-13 | GPT-5.4 |
| GPT-4.1 | OpenAI | 2026-02-16 | GPT-5.4 |
| DALL-E 2 & 3 | OpenAI | 2026-05-12 | gpt-image-1.5 |
| Claude 3.5 Sonnet | Anthropic | 2026-01-05 | Sonnet 4.6 |
| Claude Haiku 3.5 | Anthropic | 2026-02-19 | Haiku 4.5 |
| Claude Haiku 3 | Anthropic | 2026-04-20 | Haiku 4.5 |

### Upcoming / Announced (NOT Yet Available)

| Model | Provider | Expected | Notes |
|-------|----------|----------|-------|
| GPT-5.5 "Spud" | OpenAI | 2026 Q2 | Pretraining done 2026-03-24. |
| Claude Mythos | Anthropic | Preview only | Invitation-only. Cybersecurity. |
| DeepSeek V4 | DeepSeek | 2026 | ~1T params, 1M context. |
| Grok 5 | xAI | 2026 Q2 | ~6T params. |
| Muse Spark | Meta | 2026-04 | Meta's first proprietary/closed-source model. |

## How to Use This Reference

### For AI Agents

1. **Before generating code with model IDs**: Check this reference for the correct API ID.
2. **Before quoting pricing**: Check this reference. Pricing changes frequently.
3. **Staleness check**: If the "Last verified" date is older than 30 days, use WebSearch to verify before trusting these numbers.
4. **When uncertain**: Say "based on my last verified reference from [date]" rather than stating as current fact.

### Staleness Detection

```
IF (today - last_verified_date) > 30 days:
  → WebSearch "[provider] models pricing [current year]"
  → Cross-reference with this table
  → Note any discrepancies
  → Flag to user: "My reference is [N] days old, I verified via web search"
```

### When NOT to Trust This Reference

- Model pricing can change without notice
- New models may launch between updates
- Deprecation dates may shift
- "Upcoming" models may be delayed or cancelled

## Verification Commands

When you need to verify current model information, use these tools:

**Web search queries** (use WebSearch tool):
- OpenAI models: `site:platform.openai.com models`
- Anthropic models: `site:docs.anthropic.com models`
- Google Gemini: `site:ai.google.dev models`
- Pricing (any provider): `[provider] API pricing [current year]`
- Specific model ID: `"[exact-model-id]" API`
- Deprecation status: `[provider] model deprecation [current year]`

### SDK Version Check

```bash
# OpenAI
npm info openai version
pip show openai | grep Version

# Anthropic
npm info @anthropic-ai/sdk version
pip show anthropic | grep Version

# Google
npm info @google/generative-ai version
pip show google-generativeai | grep Version
```

## Cost Comparison (Budget → Premium)

Sorted by input cost per million tokens:

| Rank | Model | Provider | Input $/MTok | Best For |
|------|-------|----------|-------------|----------|
| 1 | Gemini 2.5 Flash-Lite | Google | $0.10 | Cheapest multimodal |
| 2 | Mistral Small 4 | Mistral | $0.15 | Cheap + reasoning + vision |
| 3 | GPT-5.4 Nano | OpenAI | $0.20 | Classification, extraction |
| 4 | DeepSeek V3 | DeepSeek | $0.32 | Coding, long context |
| 5 | Gemini 3 Flash | Google | $0.50 | Balanced Google option |
| 6 | GPT-5.4 Mini | OpenAI | $0.75 | OpenAI balanced |
| 7 | Claude Haiku 4.5 | Anthropic | $1.00 | Fast Anthropic option |
| 8 | Gemini 2.5 Pro | Google | $1.25 | Advanced Google |
| 9 | Gemini 3.1 Pro | Google | $2.00 | Frontier reasoning |
| 10 | Mistral Large 3 | Mistral | $2.00 | 675B MoE |
| 11 | o3 | OpenAI | $2.00 | Complex reasoning |
| 12 | GPT-5.4 | OpenAI | $2.50 | OpenAI flagship |
| 13 | Claude Sonnet 4.6 | Anthropic | $3.00 | Anthropic balanced |
| 14 | Claude Opus 4.6 | Anthropic | $5.00 | Most capable coding/agents |

## Architecture Quick Facts

| Architecture | Models Using It | Why It Matters |
|-------------|----------------|----------------|
| **MoE (Mixture of Experts)** | Mistral Large 3 (675B/41B), DeepSeek V3 (671B/37B), Llama 4 Maverick (17B/128 experts) | Massive total params but only a fraction active per token → cheaper inference. |
| **Dense Transformer** | GPT-5.4, Claude Opus 4.6, Gemini 3.1 Pro | All params active. Higher per-token cost but potentially more consistent. |

## Common Discount Mechanisms

| Mechanism | Discount | Available On |
|-----------|----------|-------------|
| **Prompt Caching** | 75-90% on cached input | OpenAI, Anthropic, Google |
| **Batch API** | 50% on all tokens | OpenAI, Anthropic, Google |
| **Committed Use** | Varies | Enterprise agreements |

## Per-Provider Deep Dives

For detailed model specs, deprecation timelines, cross-platform IDs, and API quick-start examples, see the `references/` directory in the GitHub repo:

- `references/openai.md` — Full OpenAI model catalog + audio/image models
- `references/anthropic.md` — Cross-platform IDs (Bedrock, Vertex) + cache pricing
- `references/google.md` — Gemini 3.x + 2.5 + specialized models
- `references/meta.md` — Llama 4 MoE details + access methods
- `references/mistral.md` — Full specialist model catalog (Devstral, Voxtral, OCR)
- `references/deepseek.md` — V3 MoE details + V4 roadmap
- `references/xai.md` — Grok versions + corporate context
- `references/cohere.md` — Command A + open-source models (Transcribe, Tiny Aya)

## How to Update This Reference

This reference gets stale. Here's how to help:

1. **Found an error?** Open an Issue on GitHub with the correction and source URL.
2. **New model released?** Submit a PR updating the relevant `references/*.md` file.
3. **Pricing changed?** Submit a PR with the new price and a link to the official pricing page.

Every update must include:
- The source URL (official docs preferred)
- The date you verified the information
- What changed and why

## Tips

- The more confident an LLM sounds about a model name, the more likely it's hallucinating from training data.
- "I'm not sure which model is current — let me check" is always better than a confident wrong answer.
- Model IDs are exact strings. `gpt-5.4` works; `GPT-5.4` or `gpt5.4` may not.
- Always test API calls with the actual model ID before deploying.
