# Mode: gpt-image-1

## Purpose

Default mode for high-quality general image generation.

## Supported Inputs

- `prompt` (required)
- `size`: `1024x1024`, `1536x1024`, `1024x1536`, `auto`
- `idempotency_key`

## Example

```bash
python scripts/generate.py \
  --prompt "a cinematic portrait, dramatic lighting" \
  --mode gpt-image-1 \
  --size 1024x1536
```

## Notes

- Best default for most users.
- `resolution/search-mode/enhance-mode` are ignored for this mode.
