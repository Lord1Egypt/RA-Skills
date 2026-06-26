# Excalidraw Render

OpenClaw skill for creating, editing, and rendering Excalidraw diagrams to PNG and PDF.

## Author

Scott Glover <scottgl@gmail.com>  
ClawHub: [@scottgl9](https://clawhub.ai/scottgl9)

## Features

- **Quick path** — DSL-based flowcharts via `@swiftlysingh/excalidraw-cli`
- **Full path** — hand-crafted JSON diagrams with element templates and layout rules
- **PNG rendering** — Playwright + headless Chromium renders `.excalidraw` files to PNG
- **PDF export** — convert PNG to PDF via ImageMagick

## Setup

```bash
cd <skill-dir>
uv sync
uv run playwright install chromium
```

## Usage

```bash
# Render a diagram to PNG
cd <skill-dir>
uv run python render_excalidraw.py diagram.excalidraw

# With options
uv run python render_excalidraw.py diagram.excalidraw --output out.png --scale 3
```

## References

- `references/color-palette.md` — color values for all element types
- `references/element-templates.md` — copy-paste JSON for shapes, arrows, text
- `references/layout-rules.md` — anti-overlap spacing and text-sizing rules
- `references/json-schema.md` — full Excalidraw JSON property reference

## Requirements

- Python 3.11+
- `uv` package manager
- Chromium (installed via `uv run playwright install chromium`)

## License

MIT-0 — free to use, modify, and redistribute without attribution.
