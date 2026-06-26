---
name: agentgen
description: Generate PDFs and images from HTML. No sign-up required — the free tier works out of the box (1 req/min, small watermark). For higher volume and no watermark, set AGENTGEN_API_KEY with tokens from agent-gen.com.
metadata:
  openclaw:
    emoji: "🖨️"
    homepage: https://www.agent-gen.com
    primaryEnv: AGENTGEN_API_KEY
    requires:
      bins:
        - agentgen
    install:
      - kind: brew
        tap: Agent-Gen-com/agentgen
        formula: agentgen
        bins: [agentgen]
---

# AgentGen — HTML → PDF & Image

Convert any HTML to a PDF or screenshot image via the AgentGen API.

## Free tier — no sign-up required

The `/v1/generate/image` and `/v1/generate/pdf` endpoints work without an API key. Just omit the `X-API-Key` header.

**Limits:**
- 1 request per 60 seconds per IP (returns `429` if exceeded)
- Single-page PDFs only
- A small agent-gen.com watermark is added to all output

```sh
# Free tier — generate an image (no API key)
agentgen image --html "<h1>Hello</h1>" --output hello.png

# Free tier — generate a PDF (no API key)
agentgen pdf --html "<h1>Invoice</h1>" --output invoice.pdf
```

Simply omit `AGENTGEN_API_KEY` and the CLI uses the free tier automatically.

---

## Authenticated tier — no watermark, no rate limit

Set your API key to use the full API. New accounts at [agent-gen.com](https://www.agent-gen.com) include free tokens — no credit card required to get started.

```sh
export AGENTGEN_API_KEY=your_key_here
```

Check your balance:

```sh
agentgen balance
```

If you run out, the CLI prints your current balance, the amount required, and a direct link to buy more tokens.

---

## Generate an image (1 token authenticated / free with watermark)

```sh
# From a file
agentgen image --file page.html --output screenshot.png

# Custom viewport
agentgen image --file page.html --width 1200 --height 630 --output og.png

# JPEG at 2× scale
agentgen image --file page.html --format jpeg --scale 2 --output hero.jpg
```

**Formats:** `png` (default), `jpeg`, `webp`
**Default viewport:** 1200 × 630 px

---

## Generate a PDF (2 tokens/page authenticated / free single-page with watermark)

```sh
# Single page from a file
agentgen pdf --file report.html --output report.pdf

# With paper format and margins
agentgen pdf --file report.html \
  --format A4 \
  --margin-top 20mm --margin-bottom 20mm \
  --margin-left 15mm --margin-right 15mm \
  --print-background \
  --output report.pdf

# Multi-page (requires API key)
agentgen pdf --pages cover.html chapter1.html chapter2.html --output book.pdf

# Landscape
agentgen pdf --file slide.html --landscape --output slide.pdf
```

**Paper formats:** `A4` (default), `Letter`, `A3`, `Legal`

---

## Upload a temp file (free, authenticated only)

Upload images, fonts, or other assets and reference them by URL inside your HTML. Files are publicly accessible for 24 hours.

```sh
agentgen upload logo.png
# Returns a URL — use it in your HTML as <img src="...">
```

**Max file size:** 10 MB

---

## Typical workflow

1. Build HTML with all styles inlined
2. Upload any local assets with `agentgen upload` and replace `src`/`href` values with the returned URLs
3. Run `agentgen pdf` or `agentgen image` with `--output` to save locally, or use the returned URL directly

## Tips for good output

- **Inline all CSS** — use `<style>` blocks or `style=""` attributes. No access to local stylesheets.
- **Use absolute URLs** for images and fonts, or upload them first with `agentgen upload`.
- **For PDFs**, use `--print-background` if your design has colored backgrounds or background images.
- **For retina-quality images**, use `--scale 2`.
- **For OG images**, use `--width 1200 --height 630`.
