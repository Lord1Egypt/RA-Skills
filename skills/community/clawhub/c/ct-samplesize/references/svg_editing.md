# SVG Editing Tools

> **Unified spec**: the ct- figure-rendering spec (§19.11 (same origin as `meta-analysis`). The `figures[].svg` produced by this skill is written to `CTSS_OUTPUT_DIR` (default `./outputs`) by `adapters/rendering.py` (figure-rendering reference implementation); you can further edit it here or convert it to journal formats.

| Tool | Use case | How to get |
|------|----------|------------|
| **PowerPoint / Word 2016+** | Drag in and edit directly (right-click → Ungroup to modify text / colors / shapes) | Already have Office |
| **Inkscape** | Open-source vector editor; adjust layout, export PDF / EPS / high-DPI TIFF | [inkscape.org](https://inkscape.org/) (free) |
| **Adobe Illustrator** | Publication-grade fine-tuning (fonts, colors, layers) | Adobe subscription |
| **Affinity Designer** | One-time purchase, close to AI | Microsoft Store |

## Submission Format Conversion

(Inkscape command line):

```bash
# SVG → EPS (required by most medical journals)
inkscape input.svg --export-type=eps --export-filename=input.eps

# SVG → PDF (JAMA / The Lancet, etc.)
inkscape input.svg --export-type=pdf --export-filename=input.pdf

# SVG → TIFF 600dpi (NEJM / British Medical Journal, etc.)
inkscape input.svg --export-type=png --export-dpi=600 --export-filename=input.tiff
```

> Prefer EPS / PDF for journal vector graphics; bitmaps are accepted only as high-DPI TIFF (≥300; NEJM / BMJ often require 600). Rasterizing loses editable text, so complete all text / color corrections in the vector stage.
