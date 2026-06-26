# OpenAI Models Reference

> Last verified: 2026-04-12
> Source: https://platform.openai.com/docs/models, https://openai.com/pricing

## Current Models

### Text / Chat

| Model | API ID | Released | Input $/MTok | Output $/MTok | Context | Notes |
|-------|--------|----------|-------------|--------------|---------|-------|
| GPT-5.4 | `gpt-5.4` | 2026-03-17 | $2.50 | $15.00 | 272K | Flagship. Native computer-use. |
| GPT-5.4 Pro | `gpt-5.4-pro` | 2026-03-17 | $30.00 | $180.00 | 272K | Enterprise tier. |
| GPT-5.4 Mini | `gpt-5.4-mini` | 2026-03-17 | $0.75 | $4.50 | — | 2x faster than GPT-5 mini. |
| GPT-5.4 Nano | `gpt-5.4-nano` | 2026-03-17 | $0.20 | $1.25 | — | Classification, extraction, sub-agents. |
| GPT-5.3 | `gpt-5.3` | 2026-Q1 | — | — | — | Previous flagship. Instant + Thinking variants. |

### Reasoning (o-series)

| Model | API ID | Released | Input $/MTok | Output $/MTok | Notes |
|-------|--------|----------|-------------|--------------|-------|
| o3 | `o3` | 2025-04 | $2.00 | $8.00 | Most powerful reasoning. |
| o4-mini | `o4-mini` | 2025-04-16 | — | — | Retired from ChatGPT 2026-02-13, still in API. |

### Image Generation

| Model | API ID | Released | Notes |
|-------|--------|----------|-------|
| GPT Image 1.5 | `gpt-image-1.5` | 2026 | Replaces DALL-E 3. |
| GPT Image 1 Mini | `gpt-image-1-mini` | 2026 | Lightweight variant. |

### Audio

| Model | API ID | Type | Notes |
|-------|--------|------|-------|
| GPT-4o Transcribe | `gpt-4o-transcribe` | STT | Improved WER over Whisper v3. |
| GPT-4o Mini Transcribe | `gpt-4o-mini-transcribe` | STT | Lightweight. |
| GPT-4o Mini TTS | `gpt-4o-mini-tts` | TTS | Customizable voice directions. |
| TTS-1 | `tts-1` | TTS | Standard. |
| TTS-1 HD | `tts-1-hd` | TTS | High-definition. |
| Whisper-1 | `whisper-1` | STT | Legacy, being superseded. |

## Recently Deprecated

| Model | API ID | Deprecated | Replacement |
|-------|--------|-----------|-------------|
| GPT-4o | `gpt-4o` | 2026-02-13 | GPT-5.4 |
| GPT-4.1 | `gpt-4.1` | 2026-02-13 | GPT-5.4 |
| GPT-4.1 Mini | `gpt-4.1-mini` | 2026-02 | GPT-5.4-mini |
| GPT-5.1 (ChatGPT) | — | 2026-03-11 | GPT-5.3 |
| DALL-E 2 | `dall-e-2` | 2026-05-12 (scheduled) | gpt-image-1.5 |
| DALL-E 3 | `dall-e-3` | 2026-05-12 (scheduled) | gpt-image-1.5 |

## Upcoming / Announced

| Model | Expected | Notes |
|-------|----------|-------|
| GPT-5.5 ("Spud") | 2026 Q2 | Pretraining completed 2026-03-24. 78% probability by April 30 per Polymarket. |

## Pricing Discounts

| Feature | Discount | Notes |
|---------|----------|-------|
| Prompt Caching | 90% off cached input | Automatic for repeated prefixes. |
| Batch API | 50% off all tokens | 24-hour turnaround. Non-time-sensitive. |
| Regional Processing | +10% uplift | Data residency compliance on 5.4 family. |

## API Quick Start

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.4-mini",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Common Hallucinations

| What LLMs Say | Reality (as of 2026-04-11) |
|---------------|---------------------------|
| "GPT-4o is the latest" | GPT-4o was deprecated 2026-02-13. Current flagship is GPT-5.4. |
| "GPT-4-turbo" | Deprecated. Use gpt-5.4-mini for cost-efficient tasks. |
| "DALL-E 3 for images" | DALL-E 3 shutting down 2026-05-12. Use gpt-image-1.5. |
| Model ID `gpt-5.4-turbo` | Does not exist. The tiers are: nano, mini, standard, pro. |
| "o1 for reasoning" | o1 superseded by o3 and o4-mini. |
