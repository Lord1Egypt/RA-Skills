---
name: affogato-generate
description: Generate images, video and audio with Affogato (affogato.ai) from a coding agent — list models, quote the credit price, create a generation, wait for it and download the outputs — using an Affogato API key or the Affogato MCP server. Use when the user wants an AI image, video, voiceover, lipsync, headshot or product shot made with Affogato, or asks about Affogato models and prices.
license: MIT
metadata:
  author: Affogato
  version: "0.1.0"
  homepage: https://affogato.ai/developers
---

# Affogato: generate media from an agent

Affogato serves 100+ image, video and audio models (Flux, Seedream, Nano
Banana, Kling, Seedance, Veo, Wan, ElevenLabs, …) plus studio tools
(lipsync, talking heads, headshots, cast swaps, product shots) behind one
API, billed in the credits of the user's Affogato plan.

Two ways in:

- **MCP server** (`https://api.affogato.ai/mcp`): if the host already has
  the Affogato connector, prefer its tools (`list_models`, `estimate_cost`,
  `generate`, `wait_for_generation`, …). They carry the same contract as
  below and enforce the user's spend limits.
- **REST API** with an API key: `scripts/affogato.py` wraps it. The key is
  read from `AFFOGATO_API_KEY` (never paste a key into chat or commit it).
  The user creates keys at https://affogato.ai/app/developers (paid plans).

## Workflow

1. **Pick a model.** `python scripts/affogato.py models --feature image-generation`
   (features: `image-generation`, `image-editing`, `text-to-video`,
   `image-to-video`, `lipsync`, `text-to-speech`, `music-generation`, …).
   `models --output-type video` lists everything that makes video.
2. **Read its contract.** `python scripts/affogato.py model <id>` prints the
   parameters (enums, ranges, defaults, which ones change the price), the
   file input slots, and an example request.
3. **Quote first.** `python scripts/affogato.py estimate <id> --input '{"prompt": "..."}'`
   returns the credits. Tell the user the price before spending more than
   a trivial amount, and never loop on expensive video models without
   asking.
4. **Generate.** `python scripts/affogato.py generate <id> --input '{...}' --wait`
   creates the job and waits (long-polls in 25 s rounds) until it ends.
   Output URLs are printed; `--download DIR` saves the files.
5. **Inputs.** Upload a local file with `python scripts/affogato.py upload path/to/file.png`
   (or `--url https://…`) and pass the returned file id in the model's
   input slot (`model <id>` → `inputs`). Outputs of one generation are files
   too: pass their id straight into the next model.

Statuses: `queued → processing → succeeded | failed | cancelled`. Failed and
cancelled generations are refunded in full. A 429 carries `Retry-After`;
back off and retry.

## Rules of thumb

- One continuous scene per video prompt; describe camera movement
  explicitly. See `references/prompting.md`.
- Image edits: put the source in the image slot and describe the change,
  not the whole picture.
- Keep `num_images` small while iterating; raise it for the final pass.
- Do not retry a `failed` generation blindly: read `error.code`
  (`content_policy` means the prompt or image was refused).
- Credits are real money: quote, confirm, then generate.

## Reference

- API docs: https://affogato.ai/developers · OpenAPI: https://api.affogato.ai/v1/openapi.json
- Agent summary: https://affogato.ai/developers/llms.txt
- MCP setup: https://affogato.ai/mcp
