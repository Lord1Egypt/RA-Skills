# Mode: nano-banana-2

## Purpose

Advanced generation mode with extra controls.

## Supported Inputs

- `prompt` (required)
- `size`: `1024x1024`, `1536x1024`, `1024x1536`, `auto`
- `resolution`: `1K`, `2K`, `4K`
- `search-mode` (flag)
- `enhance-mode` (flag)
- `idempotency_key`

## Example

```bash
python scripts/generate.py \
  --prompt "futuristic city at blue hour" \
  --mode nano-banana-2 \
  --size 1536x1024 \
  --resolution 2K \
  --enhance-mode
```

## Notes

- Use when quality control matters more than speed.
- `search-mode` and `enhance-mode` only apply to this mode.
