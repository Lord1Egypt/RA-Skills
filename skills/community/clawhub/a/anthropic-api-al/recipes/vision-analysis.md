# Recipe — Vision Analysis

## Goal

Have Claude analyze an image (chart, screenshot, photo, diagram) and answer questions about it.

## When

Extracting text/data from images, describing visuals, reading charts/screenshots, OCR-style tasks.

## Inputs

- `model` — Sonnet for solid vision quality; Opus for the hardest visual reasoning; Haiku for simple checks.
- `max_tokens` — **required**.
- `messages` — a user turn containing a `text` block + one or more `image` blocks.

## Steps

1. Encode the image as base64 (or use a URL source).
2. **Downscale** the image to the smallest size that preserves needed detail — images cost input tokens by size.
3. Build a user message with a `text` instruction and `image` block(s).
4. Call `anthropic_messages`.
5. Read the text response; record `usage`.

## Output

```json
{
  "content": [{ "type": "text", "text": "The chart shows revenue rising from $2M to $5M over four quarters." }],
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 1180, "output_tokens": 40 }
}
```

## Example

Base64 source:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 300,
  "messages": [{
    "role": "user",
    "content": [
      { "type": "text", "text": "What trend does this chart show? Give the start and end values." },
      { "type": "image", "source": { "type": "base64", "media_type": "image/png", "data": "<BASE64_PNG>" } }
    ]
  }]
}
```

URL source:

```json
{ "type": "image", "source": { "type": "url", "url": "https://example.com/chart.png" } }
```

## Edge cases

- Very large images → high token cost and possible size limits; downscale first.
- Multiple images → include several `image` blocks; reference them in the prompt ("the first image...").
- Unsupported media type → use PNG/JPEG/WebP/GIF (verify supported types).
- For PDFs, use a `document` block instead of `image`.

> Verification needed: confirm supported image media types and size limits at https://docs.anthropic.com/en/docs/build-with-claude/vision

## Production notes (incl. cost)

- **Cost:** image tokens scale with resolution — downscaling is the cheapest optimization.
- Use `anthropic_count_tokens` to estimate image-heavy prompts before sending.
- Cache a repeated instruction `system` prompt with `cache_control` for batch image jobs.
- For bulk image analysis, use Batches (~50% off) via `anthropic_request`.
