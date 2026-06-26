---
name: bratification
description: Generate brat-style text cover images and sticker-like WhatsApp-safe outputs from custom text. Use when the user asks to make a brat or brat-gen style cover, wants !brat command behavior, needs white-background Arial Narrow renders, or wants square 512x512 sticker-like image replies with PNG fallback and optional WEBP artifacts.
---

# Bratification

Generate brat-style images from text using the bundled Python scripts.

## Quick start

- For a plain render, run `scripts/render_brat.py`.
- For command-style parsing like `!brat hello world`, run `scripts/handle_brat_command.py`.
- Prefer white background, Arial Narrow bold (with cross-platform font fallback), centered composition, word wrapping without cutting words, and automatic font shrink to fit.
- `handle_brat_command.py` now sanitizes slug/output naming and always writes into its managed `scripts/out` directory tree.

## Workflow

1. Decide whether the request is direct text rendering or `!brat` command parsing.
2. Use `scripts/handle_brat_command.py` for command-style input.
3. Use `scripts/render_brat.py` for direct text-to-image rendering.
4. For WhatsApp-safe sticker-like delivery, prefer `--size 512 --sticker-size 512` and send the generated PNG with no caption.
5. Treat WEBP as an optional artifact unless the channel has verified native sticker upload support.

## Commands

### Render text directly

```bash
python scripts/render_brat.py "hello world" --png out/hello-world.png --webp out/hello-world.webp
```

### Parse a `!brat` command

```bash
python scripts/handle_brat_command.py "!brat hello world"
```

### Sticker-like WhatsApp-safe output

```bash
python scripts/handle_brat_command.py --size 512 --sticker-size 512 "!brat hello world"
```

## Output handling

- Use PNG as the primary reliable delivery format.
- Use WEBP as a secondary artifact for future native-sticker-capable channels.
- If the input is only `!brat` with no text, ask briefly for the text.
- If generation fails, apologize briefly and say the brat render failed.

## Scripts

- `scripts/render_brat.py`: deterministic renderer for PNG/WEBP output
- `scripts/handle_brat_command.py`: parser for `!brat`-style input that emits JSON with generated paths
