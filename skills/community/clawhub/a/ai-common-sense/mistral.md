# Mistral AI Models Reference

> Last verified: 2026-04-12
> Source: https://docs.mistral.ai/getting-started/models, https://mistral.ai/pricing

## Current Models

### Frontier Generalist

| Model | API ID | Released | Input $/MTok | Output $/MTok | Params | Context | Notes |
|-------|--------|----------|-------------|--------------|--------|---------|-------|
| Mistral Large 3 | `mistral-large-latest` | 2025-12 | $2.00 | $6.00 | 675B total / 41B active | 128K | MoE. Most capable. |
| Mistral Medium 3.1 | `mistral-medium-latest` | 2025-08 | $0.40 | $2.00 | — | 128K | Frontier multimodal. |
| Mistral Small 4 | `mistral-small-latest` | 2026-03-16 | $0.15 | $0.60 | — | 128K | Unified: reasoning + multimodal + coding. Configurable reasoning effort. |

### Smaller Models

| Model | API ID | Notes |
|-------|--------|-------|
| Mistral Small 3.2 | `mistral-small-3.2` | Efficient. |
| Ministral 14B | — | 2025-12 variant. |
| Ministral 8B | — | Lightweight. |
| Ministral 3B | — | Edge/mobile. |

### Specialist Models

| Model | Type | Released | Notes |
|-------|------|----------|-------|
| Devstral 2 | Code | 2026 | Frontier software engineering. |
| Voxtral TTS | Text-to-speech | 2026-03-26 | Zero-shot voice cloning. 9 languages. Open source. |
| Voxtral Mini Transcribe | Speech-to-text | 2026 | — |
| Codestral | Code generation | 2025 | — |
| Magistral | Reasoning | 2025 | — |
| Pixtral | Multimodal/vision | 2025 | — |
| Mistral Embed | Embeddings | — | — |
| Mistral OCR 3 | OCR | 2026 | Optical character recognition. |

## Key Features

- All models: 128K context, vision capable, 40+ languages
- Apache 2.0 license for all models
- GDPR-compliant EU hosting (free tier available)

## API Quick Start

```bash
curl https://api.mistral.ai/v1/chat/completions \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-small-latest",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Common Hallucinations

| What LLMs Say | Reality (as of 2026-04-11) |
|---------------|---------------------------|
| "Mistral 7B" or "Mixtral 8x7B" | Several generations old. Current: Small 4, Medium 3.1, Large 3. |
| "Mistral is only open source" | Mistral has both open-source models and a commercial API platform. |
| "Mistral Large has 70B params" | Large 3 has 675B total / 41B active (MoE). |
| Model ID `mistral-tiny` | Outdated. Current smallest is Ministral 3B. |
