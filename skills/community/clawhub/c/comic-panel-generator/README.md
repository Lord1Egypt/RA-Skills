# Comic Panel Generator

Generate AI comic book panels, manga strips, and graphic novel art from text descriptions. Describe a scene, character, or moment and receive a fully rendered comic illustration with bold ink outlines, dynamic compositions, and anime-style cel shading.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

---

## Install

**Via npx skills:**
```bash
npx skills add blammectrappora/comic-panel-generator
```

**Via ClawHub:**
```bash
clawhub install comic-panel-generator
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
node comicpanelgenerator.js "PROMPT" --token YOUR_TOKEN [--size SIZE] [--ref UUID]
```

### Examples

```bash
# Portrait manga panel (default)
node comicpanelgenerator.js "a samurai standing on a rooftop at night, rain falling, dramatic lighting" --token "$NETA_TOKEN"

# Landscape action scene
node comicpanelgenerator.js "two heroes facing off in a neon-lit city alley, dynamic angles, bold outlines" --token "$NETA_TOKEN" --size landscape

# Tall vertical panel
node comicpanelgenerator.js "a wizard casting a spell, magical energy swirling, manga style" --token "$NETA_TOKEN" --size tall

# Square panel with style reference
node comicpanelgenerator.js "cyberpunk street scene, futuristic fashion" --token "$NETA_TOKEN" --size square --ref SOME_UUID
```

### Output

Returns a direct image URL.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | — | **Required.** Your Neta API token |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image dimensions |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size dimensions

| Size | Width | Height |
|------|-------|--------|
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `square` | 1024 | 1024 |
| `tall` | 704 | 1408 |

---

## Default Prompt

If no prompt is provided, the following default is used:

> comic book panel illustration, bold ink outlines, dynamic composition, manga style, expressive characters, cel shading, dramatic lighting, professional comic art, sequential storytelling panel

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
