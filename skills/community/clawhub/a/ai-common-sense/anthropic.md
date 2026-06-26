# Anthropic Models Reference

> Last verified: 2026-04-12
> Source: https://docs.anthropic.com/en/docs/about-claude/models, https://docs.anthropic.com/en/docs/about-claude/pricing

## Current Models

| Model | API ID | Released | Input $/MTok | Output $/MTok | Context | Max Output | Knowledge Cutoff |
|-------|--------|----------|-------------|--------------|---------|-----------|-----------------|
| Claude Opus 4.6 | `claude-opus-4-6` | 2026-02-05 | $5.00 | $25.00 | 1M | 128K (300K batch) | May 2025 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 2026-02-17 | $3.00 | $15.00 | 1M | 64K (300K batch) | Aug 2025 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 2025-10 | $1.00 | $5.00 | 200K | 64K | Feb 2025 |

### Cross-Platform IDs

| Model | Claude API | AWS Bedrock | GCP Vertex AI |
|-------|-----------|-------------|---------------|
| Opus 4.6 | `claude-opus-4-6` | `anthropic.claude-opus-4-6-v1` | `claude-opus-4-6` |
| Sonnet 4.6 | `claude-sonnet-4-6` | `anthropic.claude-sonnet-4-6` | `claude-sonnet-4-6` |
| Haiku 4.5 | `claude-haiku-4-5-20251001` | `anthropic.claude-haiku-4-5-20251001-v1:0` | `claude-haiku-4-5@20251001` |

### Research Preview

| Model | Status | Notes |
|-------|--------|-------|
| Claude Mythos Preview | Invitation-only | Available via Project Glasswing. Defensive cybersecurity only. Announced 2026-04-07. |

## Recently Deprecated

| Model | API ID | Deprecated | Replacement |
|-------|--------|-----------|-------------|
| Claude Haiku 3.5 | `claude-3-5-haiku-20241022` | 2026-02-19 | Haiku 4.5 |
| Claude Sonnet 3.5 | `claude-3-5-sonnet-20241022` | 2026-01-05 | Sonnet 4.6 |
| Claude Sonnet 3.7 | — | 2025-10-28 | Sonnet 4.5 |
| Claude Opus 3 | `claude-3-opus-20240229` | 2026-01-05 | Opus 4.6 |
| Claude Haiku 3 | `claude-3-haiku-20240307` | 2026-04-20 (scheduled) | Haiku 4.5 |

## Pricing Details

| Feature | Multiplier | Notes |
|---------|-----------|-------|
| 5-min cache write | 1.25x input | Cached prefix reuse. |
| 1-hour cache write | 2x input | Longer cache TTL. |
| Cache read (hit) | 0.1x input | 90% savings on cached input. |
| Batch API | 0.5x all | 50% discount. Non-time-sensitive. |
| Fast Mode (Opus 4.6) | 6x all | $30/$150 MTok. Beta. |

## API Quick Start

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-6",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Common Hallucinations

| What LLMs Say | Reality (as of 2026-04-11) |
|---------------|---------------------------|
| "Claude 3.5 Sonnet" or "Claude 3 Opus" | Deprecated. Current: Opus 4.6, Sonnet 4.6, Haiku 4.5. |
| Model ID `claude-3-opus` | Old format. Current: `claude-opus-4-6` (no "3" prefix). |
| "Claude 4" (no sub-version) | Ambiguous. Specify: Opus 4.6, Sonnet 4.6, or Haiku 4.5. |
| "100K context window" | Opus/Sonnet have 1M tokens. Haiku has 200K. |
| Header `Authorization: Bearer` | Wrong. Anthropic uses `x-api-key` header, not Bearer token. |
| "Claude Sonnet is cheaper than Haiku" | Wrong. Haiku $1/$5, Sonnet $3/$15. Haiku is cheapest. |
