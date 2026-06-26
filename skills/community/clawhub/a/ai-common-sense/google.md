# Google Gemini Models Reference

> Last verified: 2026-04-11
> Source: https://ai.google.dev/gemini-api/docs/models, https://ai.google.dev/gemini-api/docs/pricing

## Current Models

### Gemini 3.x (Latest Generation)

| Model | API ID | Released | Input $/MTok | Output $/MTok | Context | Notes |
|-------|--------|----------|-------------|--------------|---------|-------|
| Gemini 3.1 Pro Preview | `gemini-3-1-pro-latest` | 2026-02-19 | $2.00 | $12.00 | — | Flagship reasoning. 77.1% ARC-AGI-2. |
| Gemini 3 Flash | `gemini-3-flash-latest` | 2026-03 | $0.50 | $3.00 | — | Default in Gemini app. |
| Gemini 3.1 Flash-Lite Preview | `gemini-3-1-flash-lite-latest` | 2026 | $0.25 | $1.50 | — | Cost-effective frontier. |
| Gemini 3.1 Flash Live Preview | — | 2026 | — | — | — | Real-time / low-latency. |

### Gemini 2.5 (Previous Generation, Still Available)

| Model | API ID | Input $/MTok | Output $/MTok | Notes |
|-------|--------|-------------|--------------|-------|
| Gemini 2.5 Pro | `gemini-2.5-pro` | $1.25 | $10.00 | Advanced general-purpose. |
| Gemini 2.5 Flash | `gemini-2.5-flash` | $0.30 | $2.50 | Best price-performance. |
| Gemini 2.5 Flash-Lite | `gemini-2.5-flash-lite` | $0.10 | $0.40 | Cheapest multimodal. |

### Specialized Models

| Model | Type | Notes |
|-------|------|-------|
| Veo 3.1 | Video generation | — |
| Lyria 3 | Music generation | — |
| Gemini Deep Think | Enhanced reasoning | Mode for 3.1 Pro. |
| Computer Use Preview | UI automation | — |
| Deep Research Preview | Agentic research | — |

## Pricing Notes

| Feature | Discount | Notes |
|---------|----------|-------|
| Context caching | Up to 90% | Repeated prefix optimization. |
| Batch API | 50% | Non-time-sensitive. |
| Extended context (200K+) | 2x price | Doubled pricing for long context. |
| Free tier | Rate-limited | Via Google AI Studio: 2.5 Flash, Flash-Lite, 3.1 Flash-Lite. |

**April 2026 change:** Mandatory spending caps enforced. Pro models restricted for free users. Prepaid billing required for new accounts.

## API Quick Start

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GOOGLE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents": [{"parts": [{"text": "Hello"}]}]}'
```

## Common Hallucinations

| What LLMs Say | Reality (as of 2026-04-11) |
|---------------|---------------------------|
| "Gemini Pro 1.5" or "Gemini Ultra" | Outdated. Current: Gemini 3.1 Pro, 3 Flash, 2.5 Pro/Flash. |
| "Bard" | Bard was rebranded to Gemini in 2024. |
| Model ID `gemini-pro` | Ambiguous/old. Use versioned IDs: `gemini-3-1-pro-latest`. |
| "PaLM 2" | Deprecated. Replaced by Gemini family. |
| "Gemini 1.0" | Multiple generations ago. Current is 3.x. |
