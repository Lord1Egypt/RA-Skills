---
name: dreamlayer-image-workflows
description: "Produce finished visual assets inside an agent run with DreamLayer: original images, edits of a supplied reference, transparent cutouts, 2x upscales, logo and app-icon directions, ecommerce product and lifestyle imagery, print-artwork concepts, campaign variations, bounded photo batches, and reference-based sprite sheets you can import into Godot. Routes to the canonical DreamLayer workflows and writes outputs into the working directory."
version: 1.0.4
metadata:
  openclaw:
    emoji: "🖼️"
    homepage: https://dreamlayer.io/agent?utm_source=clawhub&utm_medium=agent_distribution&utm_campaign=agent_launch_202609
    requires:
      env:
        - DREAMLAYER_API_KEY
      bins:
        - node
        - npx
    primaryEnv: DREAMLAYER_API_KEY
    envVars:
      - name: DREAMLAYER_API_KEY
        required: true
        description: "DreamLayer API key created at platform.dreamlayer.io. It must reach the MCP server process itself; a key exported only in your shell does not reach it. Paid image work spends DreamLayer API credits."
---

# DreamLayer image workflows

Use this when a task needs a finished image file rather than a description of one, and the
result has to land in the user's working directory: a product shot on a clean background, a
logo direction to review, a set of campaign variations, a transparent cutout, or an animated
sprite sheet for a game project.

## Setup

Node.js 22.12 or later, and a DreamLayer API key from
[platform.dreamlayer.io](https://platform.dreamlayer.io).

```json
{"mcpServers":{"dreamlayer":{"command":"npx","args":["-y","@dreamlayer/mcp@0.4.0-beta.5"],"env":{"DREAMLAYER_API_KEY":"YOUR_KEY"},"connectionTimeoutMs":90000}}}
```

Keep the timeout. On a machine that has never run this package, `npx -y` downloads it
before the server can answer. Two clean profiles measured that first start at 13 and 50
seconds; OpenClaw waits 5 seconds by default and reports the server as failed, so the
first `openclaw mcp add` or probe fails without `connectionTimeoutMs`. Hosts that use a
different key for the same idea need the equivalent raised. Later launches are fast, and
`npm i -g @dreamlayer/mcp@0.4.0-beta.5` beforehand avoids the wait entirely.

Supply the key through the host's secret mechanism. Never place it in a prompt, a commit or a
skill file. Without it the server exits and says which variable is missing.

The server exposes seven tools: `dreamlayer_capabilities`, `dreamlayer_balance`,
`dreamlayer_upload_image`, `dreamlayer_generate`, `dreamlayer_execution`, `dreamlayer_events`
and `dreamlayer_download`. Read the live tool schema before calling; do not pass fields the
host does not expose.

## Where this comes from

- Product overview: <https://dreamlayer.io/agent?utm_source=clawhub&utm_medium=agent_distribution&utm_campaign=agent_launch_202609>
- Canonical workflows and importer code: <https://github.com/TheDesignFounder/dreamlayer-agent-plugin>
- API reference and recovery: <https://docs.dreamlayer.io/agent-api>

## Which job you are doing

Each job has a canonical workflow in the public repository
[TheDesignFounder/dreamlayer-agent-plugin](https://github.com/TheDesignFounder/dreamlayer-agent-plugin)
under `plugins/dreamlayer/skills/`. Read the matching one and follow it rather than improvising:

| Job | Workflow |
| --- | --- |
| Generate an original image, edit a supplied reference, remove a background, upscale | `generate-or-edit-image` |
| Logo concepts and app-icon directions | `logo-and-app-icon-concepts` |
| Ecommerce product and lifestyle imagery | `product-image-generation` |
| Print-artwork concepts for shirts, stickers and posters | `print-on-demand-artwork` |
| Marketing, ad, banner and social variations | `marketing-image-variations` |
| A bounded batch of the same edit across several photos | `batch-photo-editing` |
| A sprite sheet from one reference | `sprite-sheet-from-reference` |
| Importing a finished sprite ZIP into Godot 4 | `godot-sprite-import` |
| Preparing a sprite ZIP for Unity 2D | `unity-sprite-import` |

All of them share one contract: [`docs/workflow-contract.md`](https://github.com/TheDesignFounder/dreamlayer-agent-plugin/blob/main/docs/workflow-contract.md).
It covers setup, the checks to run before spending, explicit operation selection, recovery and
output acceptance.

## The loop that actually works

1. Read `dreamlayer_capabilities` and `dreamlayer_balance` before paid work. Resolve any failure
   first. Confirm the operation you want is advertised and that the balance covers it.
2. Agree the brief, output count, aspect ratio, destination path and credit budget with the user.
   Never widen a batch or buy credits on your own.
3. Upload a reference once with `dreamlayer_upload_image` and keep its `input_asset_id`. Every
   operation except `text_to_image` needs one.
4. Save a unique `idempotency_key` before calling `dreamlayer_generate`, and name the operation
   explicitly: `text_to_image`, `image_to_image`, `background_remove`, `upscale` or `sprite_sheet`.
5. Work is asynchronous. `dreamlayer_generate` returns `execution_id`, `status`, `asset`,
   `question` and `last_event_id`, and a bounded stream often ends before the job does. Poll
   `dreamlayer_execution`, or resume from the cursor with `dreamlayer_events`. Never launch a
   replacement generation after a timeout.
6. A `needs_input` result is a question, not a failure. Answer it with `respond` and the
   `conversation_id`.
7. Download explicitly with `dreamlayer_download` to a new absolute path. A returned asset URL is
   not proof that a local file exists, and an existing file is never overwritten.
8. Inspect what you saved: dimensions, transparency when requested, spelling of any text,
   fidelity to the reference. Say so when an output has not been inspected.

## Costs and failure states

Ordinary completed image operations currently cost one credit each; read the live figure from
capabilities rather than assuming. Sprite jobs are a beta with frame-based pricing: read
`sprite_pricing`, round the whole quote up once to a tenth of a credit, and pass it as
`max_credits`. Transparent frames use the tier in `first_tier_cents` and
`additional_frame_cents`; a sheet that keeps its background costs the flat
`plain_frame_cents` per frame, roughly half, and is ordered with `background: "keep"` by a
client that exposes the field. Sprite jobs cannot be cancelled by the customer; failed or expired jobs restore
the hold.

Stop, keep the recoverable state, and report rather than looping paid retries when you hit:
a missing or invalid key, an invalid request, an unsupported operation, insufficient credits, a
failed or unfinished job, or a local download error. For a download error, repair the destination
and download the same `execution_id` again.

## What this does not do

- An API key is required, and paid generation spends DreamLayer API credits.
- Logo output is raster. There is no vector or SVG export, no trademark clearance and no legal
  clearance of any kind.
- Print artwork still needs a resolution, alpha and print-spec review before manufacture. There
  is no print certification.
- Nothing is published to any store, marketplace or ad platform for you.
- Product detail can drift during a generative edit, so review before publishing.
- Upscale doubles each side against a 4096 pixel ceiling, so an input whose longest side is over
  2048 is refused before it costs a credit.
- Sprite output is a beta: broad requests do not guarantee correct motion, unseen detail or clean
  transparency.
- Godot import is validated end to end, including transparent frames, per-frame timing and a
  looping animation cycle. Unity editor validation is not confirmed; the Unity workflow ships
  importer code and instructions only.
