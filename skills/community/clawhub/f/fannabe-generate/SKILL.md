---
version: 0.1.5
name: fannabe-generate
description: |
  Generate images, videos, and voice for your AI models via Fannabe.
  Use when: "generate an image", "make a video of my model",
  "animate this photo", "image-to-video", "motion control / transfer this
  dance onto my model", "character swap", "edit/restyle this image",
  "caption this video", "improve/rewrite this prompt", "describe this photo
  as a prompt", "show my gallery", "download my latest render", or
  "how many credits do I have". Wraps the `fannabe` CLI, which runs the same
  AI engines, settings, and credit pricing as the Fannabe web studio.
  NOT for: training new models (done in the web studio), or non-Fannabe
  providers.
argument-hint: "[what-to-generate] [--model <name-or-id>] [--ai <id>]"
homepage: https://www.fannabe.com
allowed-tools: Bash
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["node"] }
      }
  }
---

# Fannabe Generate

Create AI-model images, videos, and voice from the terminal. This skill drives the `fannabe` CLI, which talks to the Fannabe API and spends the signed-in user's credits.

## Step 0 — Bootstrap (before anything else)

1. If `fannabe` is not on `$PATH`, install it:
   ```bash
   npm install -g @fannabe/cli
   ```
2. If a command fails with a "Not logged in" / 401 error, ask the user to run `fannabe auth login` (opens a browser) and wait for confirmation. The token is cached in `~/.fannabe`.

Every command supports `--help`, and output is plain text meant to be parsed.

## Concepts: model vs. AI

Two different things are both called "model" colloquially:

- **Model** (`fannabe models`, `--model <modelId>`): the user's own AI persona — who the content is of.
- **AI** (`fannabe ai`, an `<aiId>` like `nano-banana-2-single-image`): the generation engine that renders it — what renders it.

Every `generate create` call takes both.

## Core workflow

```bash
fannabe models list                           # pick a model (id, name, appearance)
fannabe ai list --media-type image            # pick an AI (first column is the id)
fannabe ai schema <aiId>                       # discover that AI's fields + source slots
fannabe generate create <aiId> \
  --model <modelId> --media-type image \
  --prompt "golden hour rooftop portrait, cinematic" \
  --set aspectRatio=9:16 --set resolution=1k \
  --wait --download ./output                  # prints cost, blocks until done, saves the file
```

- Match the user's wording to a model with `fannabe models list --search "<text>"` (matches name and appearance, e.g. "redhead").
- Set any AI field with repeatable `--set key=value` (see `ai schema <aiId>`), or a full `--settings '<json>'`.
- Preview spend first with `fannabe generate cost <aiId> --media-type image --model <modelId> --set resolution=1k`.

## When the user describes an outfit or scene in plain words

Prefer the curated Theme/Outfit presets over a long hand-written prompt. See [references/easy-mode.md](references/easy-mode.md).

## Image-to-video, edits, motion control, character swap

These attach source media to AI slots. The two id kinds are NOT interchangeable. See [references/source-media.md](references/source-media.md).

## Prompt assistance

`fannabe prompt improve|ai-edit|from-image`, or inline `--enhance-prompt` / `--from-image` / `--ai-edit`. See [references/prompt-tools.md](references/prompt-tools.md).

## Async jobs and downloads

```bash
fannabe jobs list --ongoing
fannabe jobs wait <taskId> --timeout 15m
fannabe jobs download <taskId> --output ./output/result.mp4
fannabe caption-on-video <videoContentId> --text "..." --model <modelId>
fannabe video frame <videoContentIdOrFile> --time 1.5 --upload   # still frame -> imageId
```

## Costs and account

Priced in Fannabe credits, identical to the web studio. `fannabe account` shows the balance.

## References (read as needed)

- [references/ai.md](references/ai.md) — choosing an AI per media type
- [references/easy-mode.md](references/easy-mode.md) — Theme/Outfit presets
- [references/source-media.md](references/source-media.md) — source slots, the two id kinds, motion control, character swap
- [references/prompt-tools.md](references/prompt-tools.md) — prompt improve / AI edit / from-image
- [references/troubleshooting.md](references/troubleshooting.md) — auth, environments, common errors

## Rules for agents

- Generation is async: only completed jobs have downloadable media; use `--wait` or `jobs wait`.
- Never guess AI fields — read `ai schema <aiId>` and `--help`.
- The estimated cost prints before every generation; surface it to the user for anything non-trivial.
