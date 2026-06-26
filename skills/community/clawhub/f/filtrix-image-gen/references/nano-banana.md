# Mode: nano-banana

## Purpose

Fast generation mode.

## Supported Inputs

- `prompt` (required)
- `size`: `1024x1024`, `1536x1024`, `1024x1536`, `auto`
- `idempotency_key`

## Example

```bash
python scripts/generate.py \
  --prompt "anime street scene at dusk" \
  --mode nano-banana \
  --size 1536x1024
```

## Notes

- Optimized for speed.
- `resolution/search-mode/enhance-mode` are ignored for this mode.
