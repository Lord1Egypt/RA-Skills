# DeepSeek Models Reference

> Last verified: 2026-04-12
> Source: https://deepseek.com, third-party pricing aggregators

## Current Models

| Model | Type | Params (Total/Active) | Input $/MTok | Output $/MTok | Context | Notes |
|-------|------|----------------------|-------------|--------------|---------|-------|
| DeepSeek-R1 | Reasoning | — | — | — | — | OpenAI o1-level reasoning. |
| DeepSeek-V3 | General | 671B / 37B active | $0.32 | $0.89 | 200K | MoE. Superior coding. |
| DeepSeek-V3.2-Speciale | Advanced | — | — | — | — | Peak human-expert proficiency. |
| DeepSeek-VL2 | Multimodal | — | — | — | — | Efficient vision-language. |

## Upcoming / Announced

| Model | Expected | Notes |
|-------|----------|-------|
| DeepSeek V4 | 2026 Q1-Q2 | ~1T params MoE, ~37B active. 1M context (Engram memory). Native multimodal. Claims to outperform Claude/ChatGPT on long-context coding. |

## Key Features

- **Cost leadership**: Input at $0.32/MTok, significantly cheaper than most competitors
- **MoE efficiency**: 671B total but only 37B active per token
- **Long context**: 200K tokens (V4 targeting 1M)
- **Partially open**: Some models available on Hugging Face

## Access

Available through:
- DeepSeek API (api.deepseek.com)
- Multiple third-party providers
- Self-hosting (open-weight variants)

## API Quick Start

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Common Hallucinations

| What LLMs Say | Reality (as of 2026-04-11) |
|---------------|---------------------------|
| "DeepSeek Coder" as separate model | DeepSeek-V3 handles coding. DeepSeek Coder was an earlier release. |
| "DeepSeek is expensive" | Among the cheapest: $0.32/MTok input (standard rate). |
| "DeepSeek V2 is latest" | V3 and V3.2-Speciale are current. V4 upcoming. |
| "DeepSeek only does text" | VL2 is multimodal. V4 will be natively multimodal. |
