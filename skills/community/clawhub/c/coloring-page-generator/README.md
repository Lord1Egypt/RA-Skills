# Coloring Page Generator

Generate printable black and white coloring pages from text descriptions using AI. Describe any scene, character, pattern, or subject and receive clean line art ready for printing — kids coloring sheets, adult coloring book pages, mandala coloring pages, animal coloring pages, fantasy coloring pages, and more.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/coloring-page-generator
```

**Via ClawHub:**
```bash
clawhub install coloring-page-generator
```

---

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

```bash
node coloringpagegenerator.js "<description>" --token YOUR_TOKEN [--size <size>] [--ref <uuid>]
```

### Examples

```bash
# Simple kids coloring page
node coloringpagegenerator.js "a friendly elephant holding a bunch of balloons" --token "$NETA_TOKEN"

# Adult mandala coloring page
node coloringpagegenerator.js "intricate geometric mandala with floral patterns" --token "$NETA_TOKEN" --size square

# Fantasy scene in landscape orientation
node coloringpagegenerator.js "a dragon perched on a castle tower at sunset" --token "$NETA_TOKEN" --size landscape

# Tall portrait coloring page
node coloringpagegenerator.js "a fairy standing in an enchanted forest" --token "$NETA_TOKEN" --size tall

# With a style reference image
node coloringpagegenerator.js "underwater ocean scene with fish and coral" --token "$NETA_TOKEN" --ref abc123-uuid
```

### Output

Returns a direct image URL. Download or open it in your browser to view and print.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--token` | string | *(required)* | Your Neta API token |
| `--ref` | UUID string | *(none)* | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width × Height |
|------|---------------|
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

---

## Default Style

When no custom prompt suffix is added, images are generated with the default coloring page style:

> black and white line art coloring page, clean outlines, no shading, no color fills, white background, detailed illustration suitable for coloring, bold clear lines, printable coloring book style

You can override this by crafting your own descriptive prompt.

