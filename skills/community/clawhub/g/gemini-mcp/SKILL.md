---
name: gemini-mcp
description: Generate and edit images with Google Gemini image models via MCP. Use when the user asks to generate, create, or edit images using Gemini or Nano Banana models, wants to produce a consistent set of images from a prompt, or needs to compose/blend multiple images. Triggers on phrases like "generate an image of", "edit this image with Gemini", "create a set of consistent images", "use Nano Banana to make", or any request to produce images via the Gemini image API. Requires the @chrischall/gemini-mcp package installed and the gemini server registered (see Setup below).
---

# gemini-mcp

MCP server for Google Gemini image generation and editing — natural-language image creation via the Gemini API (Nano Banana / Nano Banana Pro models).

- **npm:** [npmjs.com/package/@chrischall/gemini-mcp](https://www.npmjs.com/package/@chrischall/gemini-mcp)
- **Source:** [github.com/chrischall/gemini-mcp](https://github.com/chrischall/gemini-mcp)

## Setup

### Option A — npx (recommended)

Add to `.mcp.json` in your project or `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "npx",
      "args": ["-y", "@chrischall/gemini-mcp"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Option B — from source

```bash
git clone https://github.com/chrischall/gemini-mcp
cd gemini-mcp
npm install && npm run build
```

Then add to `.mcp.json`:

```json
{
  "mcpServers": {
    "gemini": {
      "command": "node",
      "args": ["/path/to/gemini-mcp/dist/index.js"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or use a `.env` file in the project directory with `GEMINI_API_KEY=<value>`.

### Getting your API key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Create an API key (requires a Google account)
3. Copy the key and set it as `GEMINI_API_KEY`

Note: Image generation requires a billing-enabled Google Cloud project.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key |
| `GEMINI_IMAGE_MODEL` | No | Override the default image model (default: `gemini-3-pro-image`) |
| `GEMINI_OUTPUT_DIR` | No | Default directory for saved images (default: current working directory) |
| `GEMINI_INPUT_DIR` | No | Directory to resolve bare input-image filenames against (e.g. point at Cowork's `uploads/` folder so `images: ["house.jpg"]` works) |

## Tools

### Models
| Tool | Description |
|------|-------------|
| `gemini_list_models` | List available Gemini image models and the current default |

### Image Generation
| Tool | Description |
|------|-------------|
| `gemini_generate_image(prompt, count?, images?, images_base64?, video_url?, video_path?, google_search?, seed?, filename?, model?, aspect_ratio?, image_size?, thinking_level?, output_dir?, inline?)` | Generate image(s) from a text prompt (optionally image-conditioned via `images`/`images_base64`, or video-conditioned via `video_url`/`video_path`) |
| `gemini_edit_image(prompt, images?, images_base64?, google_search?, seed?, filename?, model?, aspect_ratio?, image_size?, thinking_level?, output_dir?, inline?)` | Edit or compose input image(s) — by **path** (`images`) or **value** (`images_base64`: data URI or raw base64) — with a text instruction. Requires ≥1 input |
| `gemini_generate_set(master_prompt, scenes? \| count?, reference_mode?, master_images?, master_images_base64?, google_search?, seed?, basename?, model?, thinking_level?, ...)` | Master image (optionally seeded from a reference photo) plus N consistent images referencing it |

### Multi-turn (Interactions API — Beta)
| Tool | Description |
|------|-------------|
| `gemini_interact(input, previous_interaction_id?, images?, images_base64?, video_url?, video_path?, google_search?, model?, aspect_ratio?, image_size?, thinking_level?, filename?, output_dir?, inline?)` | Generate/edit via Gemini's **Interactions API**. Returns an `interaction_id`; pass it back as `previous_interaction_id` to **iteratively refine the same image** conversationally — the recommended way to make incremental edits. Output is **JPEG**. (Beta API.) |

## Workflows

**Generate a single image:**
```
gemini_generate_image(prompt: "a red maple leaf on white background, studio photo")
→ returns path to saved PNG
```

**Generate multiple variations:**
```
gemini_generate_image(prompt: "a cartoon fox", count: 4, output_dir: "/tmp/foxes")
→ returns paths to 4 PNG files
```

**Edit an existing image:**
```
gemini_edit_image(prompt: "make the background blue", images: ["/path/to/image.png"])
→ returns path to edited PNG
```

**Generate a consistent set (master + scenes):**
```
gemini_generate_set(
  master_prompt: "a cartoon fox named Rusty, orange fur, blue scarf",
  scenes: ["Rusty waving hello", "Rusty eating an apple", "Rusty sleeping"]
)
→ returns paths to master + 3 scene images, all consistent
```

**Generate variations of a concept:**
```
gemini_generate_set(
  master_prompt: "minimalist logo for a coffee shop",
  count: 5
)
→ returns master + 5 variations
```

**Use a reference photo by value (when you have the bytes):**
```
gemini_edit_image(
  prompt: "place this house on a vintage travel-poster background",
  images_base64: ["data:image/jpeg;base64,/9j/4AAQ..."]   // or raw base64
)
→ returns path to the edited image
```
`images_base64` is for bytes you actually have — a file you `Read`/encode, a URL
you fetch, or a `data:` URI the user pastes as **text**.

**Iterate on ONE image conversationally (multi-turn):**
```
r1 = gemini_interact(input: "a cozy reading nook, watercolor")
   → { images: [...], interaction_id: "v1_abc…" }
r2 = gemini_interact(input: "add a sleeping cat on the chair",
                     previous_interaction_id: r1.interaction_id)
   → refined image that preserves r1; returns a NEW interaction_id
```
Prefer this over re-running `gemini_edit_image` when you're making a *series* of incremental edits — the model keeps the prior result in context.
**⚠️ Chat-pasted/attached images can't be fed to these tools directly.** A pasted
image reaches the assistant as a *vision* block — the assistant can SEE it but
never receives the original bytes, and the host doesn't write it to disk. So
neither `images` (no file exists) nor `images_base64` (the bytes can't be
reconstructed from a downscaled vision rendering) is obtainable from a paste.
To use a real reference photo, the **user** must make the bytes available: save
the file and give its **path** (→ `images`), drop it into the project dir, paste
it as a **`data:` URI in text**, or host it at a **URL** (fetch → base64 →
`images_base64`). This is a host/Cowork limitation, not an MCP one.

Two built-in ways to get past the unreachable-paste problem without any manual
extraction:
- **`from_clipboard: true`** (macOS) — the tool reads the image off the system
  clipboard itself (osascript), downscales it, and uses it. The user just needs
  to **copy** the image (⌘C — distinct from pasting it inline into chat, which
  doesn't keep it on the clipboard). Works on every image tool:
  `gemini_edit_image(prompt: "…", from_clipboard: true)`.
- **`GEMINI_INPUT_DIR`** — point it at a folder (e.g. Cowork's `uploads/`); then a
  **bare filename** resolves against it: `gemini_edit_image(prompt: "…", images: ["house.jpg"])`.

## Notes

- **Input images** accept either file **paths** (`images` / `master_images`) or **base64/data-URI values** (`images_base64` / `master_images_base64`).
- **`seed`** makes a result reproducible; it's echoed in the result metadata (a random one is chosen + echoed when omitted). `count>1` uses `seed, seed+1, …` so the images differ. Determinism isn't fully guaranteed by the model.
- **`filename`/`basename`** set the output name (extension stripped); names never overwrite (a `-2`, `-3` suffix is added). The result echoes the absolute path(s), `model`, `seed`, and aspect/size.
- **No edit-strength control.** Gemini exposes no denoise/strength knob, and Nano Banana over-preserves the input — big structural edits ("move/remove/shrink", add a mat border) are often ignored. Workarounds: reroll with a different `seed`, raise `thinking_level` to `high`, use forceful wording, do layout changes (padding/borders) externally, or use `gemini_interact` multi-turn.
- **`thinking_level`** (`minimal`/`high`, Gemini 3 models) controls reasoning depth — `high` can improve complex compositions/edits at higher latency/cost.
- **Model text.** When the model returns a caption/explanation (mostly Gemini 3 **Pro**), it's surfaced as `text` in the result metadata.
- **`google_search: true`** grounds the image in live Google Search (current events, weather, real data — great for infographics). The result metadata includes `grounding` with the `queries` run and the `sources` (`{uri, title}`) used. (`gemini_interact` surfaces `grounding.queries` only — the Interactions API returns no clean source list.)
- **`video_url`** (a public YouTube URL, on `gemini_generate_image` / `gemini_interact`) generates an image from a video reference — **requires a Flash model** (e.g. `model: "gemini-3.1-flash-image"`). For a **local video file**, use **`video_path`** instead: the file is uploaded to the Gemini Files API (streamed from disk, 2 GB max), waited to `ACTIVE`, and referenced by its `files/…` uri. The result metadata echoes `video_file` (`{uri, name, expires}`, ~48h retention) — reuse that uri as `video_url` in later calls to skip re-uploading.
- **`gemini_interact`** is the multi-turn path: it returns an `interaction_id`; thread it back via `previous_interaction_id` for conversational refinement. Output is **JPEG only**. It's a **Beta** API (separate from the stable `generate`/`edit`/`set` tools).
- `output_dir` per-call overrides `$GEMINI_OUTPUT_DIR` overrides cwd. `inline: true` returns bytes (with a metadata text block) instead of writing.
- `count` and `scenes` are mutually exclusive in `gemini_generate_set`; `reference_mode: "chain"` references the previous image instead of the master.
- Aspect ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `2:3`, `3:2`, … · Image sizes: `512` (0.5K, Flash only), `1K`, `2K`, `4K`. `4K` is the max native output — true 18×24 in @ 300 DPI (5400×7200) needs an external upscale step.
- All generated images carry a **SynthID** watermark (Google).
- The model can mis-render text/Roman numerals (e.g. years) — verify any text in the output; it's a model limitation, not a tool setting.
- Server logs to stderr only — stdout is reserved for JSON-RPC.
