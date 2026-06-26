# Cohere Models Reference

> Last verified: 2026-04-11
> Source: https://cohere.com/pricing, https://docs.cohere.com/changelog

## Current Models

### Text Generation

| Model | Released | Params | Context | Notes |
|-------|----------|--------|---------|-------|
| Command A Reasoning | 2026 | 111B | 256K | Hybrid reasoning for agentic tasks. 23 languages. |
| Command A Translate | 2026 | — | — | State-of-the-art machine translation. 23 languages. |

### Audio

| Model | Released | Params | Notes |
|-------|----------|--------|-------|
| Cohere Transcribe | 2026-03-26 | 2B | #1 on HuggingFace Open ASR Leaderboard (5.42% WER). Open source. Runs locally. |

### Other

| Model | Type | Notes |
|-------|------|-------|
| Rerank 4.0 | Ranking | Latest ranking model. |
| Tiny Aya | Multilingual | 70+ languages. Open-weight. Runs on laptops. Released Feb 2026. |
| Embed v3 | Embeddings | Multilingual embeddings. |

## Pricing

- Per-token pricing (input/output differentiated)
- Trial API key: Free with rate limits
- Production: Pay-as-you-go
- Command A Reasoning: ~$6.25/MTok estimated (aggregate)
- Available through Cohere API and cloud providers

## API Quick Start

```bash
curl https://api.cohere.com/v2/chat \
  -H "Authorization: Bearer $COHERE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "command-a-reasoning",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## Common Hallucinations

| What LLMs Say | Reality (as of 2026-04-11) |
|---------------|---------------------------|
| "Command R+" or "Command R" | Previous generation. Current: Command A Reasoning. |
| "Cohere is text-only" | Has Transcribe (audio), Embed (embeddings), Rerank (search). |
| "Cohere doesn't have open-source models" | Transcribe and Tiny Aya are open-source. |
