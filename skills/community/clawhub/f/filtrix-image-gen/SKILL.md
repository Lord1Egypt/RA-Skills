---
name: filtrix-image-gen
description: Generate and edit images through Filtrix Remote MCP. Use when users ask to create images or refine existing ones. Supports gpt-image-1, nano-banana, and nano-banana-2 through one MCP endpoint.
---

# Filtrix Image Gen (MCP)

This skill is MCP-only.

- Endpoint: `https://mcp.filtrix.ai/mcp`
- Auth: `Authorization: Bearer <FILTRIX_MCP_API_KEY>`
- Primary tools:
  - `generate_image_text`
  - `edit_image_text`
  - `get_account_credits`

Available MCP tools:

- `get_account_credits`
- `generate_image_text`
- `edit_image_text`

## Setup

Required:
- `FILTRIX_MCP_API_KEY`

Optional:
- `FILTRIX_MCP_URL` (default: `https://mcp.filtrix.ai/mcp`)

## Generate

```bash
python scripts/generate.py \
  --prompt "..." \
  [--mode gpt-image-1|nano-banana|nano-banana-2] \
  [--size 1024x1024|1536x1024|1024x1536|auto] \
  [--resolution 1K|2K|4K] \
  [--search-mode] \
  [--enhance-mode] \
  [--idempotency-key KEY] \
  [--output PATH]
```

## Edit

Use this when user wants iterative refinement, style transfer, background changes, object replacement, etc.

```bash
python scripts/edit.py \
  --prompt "make the sky sunset orange and add volumetric light" \
  (--image-path /path/to/input.png | --image-url https://...) \
  [--mode gpt-image-1|nano-banana|nano-banana-2] \
  [--size 1024x1024|1536x1024|1024x1536|auto] \
  [--resolution 1K|2K|4K] \
  [--search-mode] \
  [--enhance-mode] \
  [--idempotency-key KEY] \
  [--output PATH]
```

## Mode Mapping

- `gpt-image-1`: general quality route
- `nano-banana`: fast generation route
- `nano-banana-2`: advanced generation route

## Recommended Workflow

1. First pass with `generate_image_text` (`scripts/generate.py`).
2. Use `edit_image_text` (`scripts/edit.py`) for targeted changes.
3. Use a new `idempotency_key` for each new edit intent.

## Idempotency

`idempotency_key` prevents duplicate billing on retries.
If omitted, scripts auto-generate one UUID-based key.

## References

- [MCP Tools Reference](references/mcp-tools.md)
- [gpt-image-1 Mode](references/gpt-image-1.md)
- [nano-banana Mode](references/nano-banana.md)
- [nano-banana-2 Mode](references/nano-banana-2.md)
- [Prompt Guide](references/prompts.md)
