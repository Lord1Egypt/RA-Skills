---
name: cyberpunk-image-generator
description: Generate cyberpunk style futuristic art. Use when the user asks for neon, sci-fi, dystopia, or cyberpunk cityscapes.
version: 0.5.0
metadata: { "pattern": ["tool-wrapper"], "openclaw": { "emoji": "🌆", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm"] } } }
---

# Cyberpunk Image Generator (`cyberpunk-image-generator`)

Generate cyberpunk style futuristic art. Use when the user asks for neon, sci-fi, dystopia, or cyberpunk cityscapes.

This skill follows a **single aggregated gateway backend** model. One API key is used locally, while multiple models are aggregated behind the gateway. The CLI wraps the full async flow: submit task -> poll lowercase `task_status` -> fetch `data.images`. The backend platform is a **fixed implementation choice**, not a configurable provider switch. If another platform is needed, publish a separate skill for it.

The design goal is smooth automation for common workflows such as single-image generation, multi-file prompts, image-to-image with references, batch jobs, EXTEND defaults, and reusable style presets. Full gateway-alignment notes are in [references/weryai-platform.md](references/weryai-platform.md).


## Strict Style Enforcement

As the Cyberpunk Image Generator agent, you MUST always enforce this specific style.
1. Always append `--style cinematic` to your `cyberpunk-image-generator` CLI command.
2. When building the prompt, seamlessly blend these keywords into the visual description: "cyberpunk, neon lights, dystopian future, high tech low life, dark city, synthwave colors".
Do not ask the user which style they want, because this skill is strictly dedicated to Cyberpunk Image Generator.

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/cyberpunk-image-generator/` (project) and/or `~/.image-skills/cyberpunk-image-generator/` (home).


## Current Gateway Contract (WeryAI)

| Item | Contract |
| --- | --- |
| Base URL | `https://api.weryai.com` (hard-coded in `scripts/main.ts`) |
| Auth | `Authorization: Bearer` via **`IMAGE_GEN_API_KEY`** ([get a key](https://weryai.com/api/keys)) |
| text-to-image | `POST /v1/generation/text-to-image`; requires `model`, `prompt`, `aspect_ratio` |
| image-to-image | `POST /v1/generation/image-to-image`; also requires `images[]` |
| status lookup | `GET /v1/generation/{taskId}/status`; `task_status` is `waiting`, `processing`, `succeed`, or `failed` |
| business success | **`success: true`** (or `status: 200`); failures return business codes such as `1001`, `1002`, `1003` |
| text length | the script validates `prompt` and `negative_prompt` lengths before request submission |
| result download | after `succeed`, images are fetched by URL; the script uses timeout, retry, backoff, optional Bearer retry, and minimum-payload validation |

See [references/weryai-platform.md](references/weryai-platform.md) for field mapping, model lookup guidance, and troubleshooting flow.

## Step 0: First-Trigger Readiness Gate

When this skill is triggered for the **first time** in a project or environment, the agent must not jump straight to model selection or generation. It must do this first:

1. **Check local readiness silently** with `npm run ensure-ready -- --project . --workflow <workflow>`
2. **If runtime dependencies are missing**, propose to install them on behalf of the user
3. **If `IMAGE_GEN_API_KEY` is missing**, ask the user for permission to configure it now
4. Only after readiness and API key are resolved, continue to model selection / prompt clarification / generation

**Access token**: only use **`IMAGE_GEN_API_KEY`**. It may also live in `.image-skills/cyberpunk-image-generator/.env` as `IMAGE_GEN_API_KEY=...`. After the user approves, the agent may persist it there by running `npm run setup -- --project . --workflow <workflow> --persist-api-key` when the key is already in env, or by writing the file locally on the user's behalf instead of asking the user to edit files manually.

**First-use readiness check**: before the first generation run in a new OpenClaw or local instance, the agent must run:

```bash
npm run ensure-ready -- --project . --workflow <workflow>
```

This readiness step is not optional. It checks the local toolchain, reads the local doctor report, and automatically runs `bootstrap` when local script dependencies are missing.

**First-trigger user behavior**:

- If dependencies are missing: ask for approval to install them, then install silently
- If `IMAGE_GEN_API_KEY` is missing: tell the user image generation needs an API key and offer to configure it now by writing `.image-skills/cyberpunk-image-generator/.env` on the user's behalf
- Do not ask the user to debug the environment before this readiness gate runs
- Do not ask the user to choose a model before readiness and API key are resolved
- Treat API keys as secrets: prefer writing them locally on the user's behalf, never echo them back, and never include them in normal progress messages

**`EXTEND.md`** is optional and can hold default model, quality, aspect ratio, and batch worker limits.

```bash
test -f .image-skills/cyberpunk-image-generator/EXTEND.md && echo project
test -f "$HOME/.image-skills/cyberpunk-image-generator/EXTEND.md" && echo user
```

**Default model on initialization**: if no model is configured yet, initialize this skill with **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`) and tell the user that it is now the default. Also remind them they can switch models anytime later.

**Model selection**: after initialization, one of these provides the active default:

- `--model`
- `default_model` in `EXTEND.md`
- `IMAGE_GEN_DEFAULT_MODEL`

If none of them is set yet, the agent should initialize the local default to **Nano Banana 2** first, tell the user that this workspace now defaults to that model, and remind them they can switch anytime if another model fits better. See [references/config/first-time-setup.md](references/config/first-time-setup.md), [references/config/preferences-schema.md](references/config/preferences-schema.md), and [references/config/model-registry-schema.md](references/config/model-registry-schema.md).

**Style presets**: [references/style-presets.md](references/style-presets.md)

Model priority:

`--model` -> `EXTEND.md default_model` -> `IMAGE_GEN_DEFAULT_MODEL`

## If No Model Was Specified

When the user wants image generation but no model is configured (`EXTEND.md`, `--model`, and `IMAGE_GEN_DEFAULT_MODEL` are all absent):

**Do not ask the user to read docs or edit config files.** Follow the guided flow in [references/config/first-time-setup.md](references/config/first-time-setup.md) § "Model Selection — Agent-Guided Flow":

1. Start from the bundled starter registry shipped with this skill. If the model list looks stale or a requested model is missing, refresh it silently with `npm run discover-image-models -- --out .image-skills/cyberpunk-image-generator/MODELS.json`
2. Initialize local defaults with **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`) by writing `EXTEND.md`
3. Tell the user that the default model is now **Nano Banana 2**, and explicitly remind them they can switch anytime later if they need another model
4. Continue to prompt clarification and generation
5. If the user immediately asks for another model, rank candidates for the workflow → `npm run recommend-model -- --workflow <workflow> --role <role> --json`, then update `EXTEND.md`

If the workflow is more specific than a generic single image, prefer a role-aware recommendation such as `comic-page`, `comic-character-sheet`, `infographic-dense`, or `article-framework` instead of only passing the broad workflow name.

If the user later asks to switch models, update `EXTEND.md` in place — do not ask the user to edit it manually.

If the gateway returns "model does not exist" or a similar model-key error, the agent must first refresh from WeryAI docs and retry recommendation before asking the user for any platform-side information.

## If The Request Is Underspecified

When the user gives only a rough idea and the visual brief is still weak, do not jump straight into prompt writing. Use the local brief helper first:

```bash
npm run build-visual-brief -- --workflow cover --topic "Habit systems"
```

Use its question menu to ask about at least:

1. Photorealistic or illustration
2. Color temperature / palette direction
3. Shot language (close-up, wide, etc.)
4. Composition pattern
5. Aspect ratio
6. Text density

Then map the answered brief into the final prompt or workflow files.

Do **not** tell the user to go read the docs alone. If the CLI fails because the model is missing, the agent should complete this selection flow and retry.

## Workflow

1. On first trigger, run the readiness gate: check dependencies, bootstrap missing local tooling, and confirm `IMAGE_GEN_API_KEY`.
2. Confirm a default model is configured (via `EXTEND.md` or environment), or enter the guided model-selection flow.
3. Build the prompt: inline text (`--prompt`) or assembled from files (`--promptfiles`).
4. Choose a style preset if applicable (`--style`).
5. Run the CLI to submit the task, poll for completion, and download the result.
6. For multiple images, use batch mode (`--batchfile`) with parallel jobs.

## Script

`{baseDir}` is the directory containing this file. `${BUN_X}` is either `bun` or `npx -y bun`.

| Path | Purpose |
| --- | --- |
| `{baseDir}/scripts/main.ts` | the only execution entrypoint |

## Usage

```bash
# examples only; M should be chosen by the user or resolved by the agent
M=<chosen model key>

# single image
${BUN_X} {baseDir}/scripts/main.ts --prompt "a cat" --image cat.png --ar 1:1 -m "$M"

# prompt assembled from multiple files
${BUN_X} {baseDir}/scripts/main.ts --promptfiles system.md user.md --image out.png --ar 16:9 -m "$M"

# style preset
${BUN_X} {baseDir}/scripts/main.ts --prompt "city nightscape" --style cinematic --image out.png --ar 16:9 -m "$M"

# image-to-image with reference
${BUN_X} {baseDir}/scripts/main.ts --prompt "turn it into cyberpunk" --image out.png --ref src.png --ar 1:1 -m "$M"

# quality / resolution
${BUN_X} {baseDir}/scripts/main.ts --prompt "poster" --image poster.png --ar 16:9 --quality 2k -m "$M"
${BUN_X} {baseDir}/scripts/main.ts --prompt "poster" --image poster.png --ar 16:9 --imageSize 2K -m "$M"

# infer aspect from size when --ar is omitted
${BUN_X} {baseDir}/scripts/main.ts --prompt "scene" --image scene.png --size 1280x720 -m "$M"

# batch mode
${BUN_X} {baseDir}/scripts/main.ts --batchfile batch.json --jobs 4 --json

# do not write downloaded images to disk
${BUN_X} {baseDir}/scripts/main.ts --prompt "abstract" --image dummy.png --ar 1:1 --no-download -m "$M"

# dry-run request preview; --image is optional here
${BUN_X} {baseDir}/scripts/main.ts --prompt "test" --ar 1:1 -m "$M" --dry-run
```

### Batch JSON Example

```json
{
  "jobs": 4,
  "tasks": [
    {
      "id": "hero",
      "promptFiles": ["prompts/hero.md"],
      "image": "out/hero.png",
      "model": "<model key from gateway docs>",
      "style": "editorial",
      "ar": "16:9",
      "quality": "2k",
      "use_web_search": false
    },
    {
      "id": "edit",
      "prompt": "turn it into watercolor",
      "image": "out/edit.png",
      "ref": ["assets/in.png"],
      "negative_prompt": "blurry",
      "webhook_url": "https://example.com/hook"
    }
  ]
}
```

Paths are resolved relative to the **batch file directory**. If a `provider` field exists, it is ignored in single-gateway mode. Task-level optional fields include `style`, `webhook_url`, `negative_prompt`, `resolution`, `use_web_search`, and `caller_id`.

## Main Options

| Option | Description |
| --- | --- |
| `--prompt` / `-p` | prompt text |
| `--promptfiles` | concatenate multiple files into the prompt |
| `--image` / `-o` / `--output` | output path in single-task mode; defaults to `.png` if no extension is given |
| `--batchfile` | batch JSON file |
| `--jobs` | worker count |
| `--model` / `-m` | model key; one of CLI / `EXTEND.md` / `IMAGE_GEN_DEFAULT_MODEL` must provide it |
| `--style` | style preset, see [style-presets.md](references/style-presets.md) |
| `--ar` / `--aspect-ratio` | aspect ratio; defaults to `EXTEND.md` or `1:1` |
| `--size` | `WIDTHxHEIGHT`; can infer aspect ratio if `--ar` is omitted |
| `--quality` | `normal` or `2k`, mapped into gateway resolution |
| `--imageSize` | `1K`, `2K`, or `4K` |
| `--resolution` | pass resolution directly to the API |
| `--negative-prompt` | negative prompt |
| `--ref` / `--reference` | reference image, either URL or local file |
| `--n` | `image_number` (default: 1) |
| `--webhook-url` | gateway `webhook_url` |
| `--use-web-search` | set `use_web_search: true` |
| `--caller-id` | gateway `caller_id` |
| `--poll-interval-ms` / `--poll-timeout-ms` | polling controls |
| `--no-download` | skip file writing |
| `--dry-run` | print the final request body instead of calling the API |
| `--json` | JSON summary or batch report |

## Parallelism and Retry

- Batch jobs use gated concurrency through `--jobs`, with environment overrides such as `BASE_IMAGE_GEN_CONCURRENCY` and `BASE_IMAGE_GEN_START_INTERVAL_MS`.
- A single task retries up to 3 times, but obvious parameter or auth errors are not retried.
- Batch worker caps come from `batch.max_workers` in `EXTEND.md` or `BASE_IMAGE_MAX_WORKERS`.

## Environment Variables

| Variable | Description |
| --- | --- |
| `IMAGE_GEN_API_KEY` | the only API key variable |
| `IMAGE_GEN_DEFAULT_MODEL` | default model key |
| `BASE_IMAGE_MAX_WORKERS` | override batch worker limit |
| `BASE_IMAGE_GEN_CONCURRENCY` | batch concurrency |
| `BASE_IMAGE_GEN_START_INTERVAL_MS` | minimum delay between batch task starts |

Supported `.env` locations:

- `<cwd>/.image-skills/.env`
- `$HOME/.image-skills/.env`

Existing environment variables are not overwritten.

## Agent Notes

1. On first use in a new environment, run `npm run ensure-ready -- --project . --workflow <workflow>` from this skill directory before generation. Do not skip this just because direct API calls appear to work.
2. Confirm that `IMAGE_GEN_API_KEY` is available, directly or through `.image-skills/.env`.
3. If the model is missing, complete the model-selection flow above before running the CLI.
4. Single-task mode usually requires `--image`, but `--dry-run` may omit it. If `--ref` is present, the script uses the image-to-image endpoint.
5. Polling behavior is: `waiting` / `processing` -> keep polling, `succeed` -> use `images`, `failed` -> inspect `msg`.
6. The selected model key is printed to stderr for easier debugging.

## User Feedback During Generation

- **Before generation starts**: tell the user what's about to happen, including the **model being used** (e.g., "Generating your cover with Model X, roughly 30 seconds"). Never start silently.
- **Model disclosure**: always mention the model name/key when generation begins. This helps the user understand quality expectations and makes later model switching easier.
- **Batch generation**: estimate the total count and rough time. As images complete, show them incrementally — do not wait for the entire batch to finish before showing anything.
- **On failure**: do not dump error codes. Translate the failure into a user-level explanation and suggest a fix (e.g., "This model is temporarily unavailable — want to try another one?").
- **On timeout**: if polling exceeds the expected window, proactively inform the user (e.g., "Taking longer than usual, still waiting") rather than staying silent.
- **On completion**: send/display the image immediately. Never output just a filename — the user must see the actual image. If the platform supports file sending, send the file. If it supports inline rendering, render inline. If neither works, provide a download URL.

## Interaction Rules (Mandatory)

These rules apply to every user interaction. They are not optional guidelines.

1. **Never show commands, file paths, config syntax, or schema details to the user.** All tool execution is silent.
2. **Never ask the user to edit config files.** The agent writes `EXTEND.md`, `MODELS.json`, and other configs on behalf of the user.
3. **Ask one question at a time.** Do not present all dimensions at once. Lead with the highest-impact choice.
4. **Offer concrete options with descriptions**, not raw technical names. If presenting styles, describe what each looks like.
5. **Always disclose the model and estimated time** when generation starts.
6. **Show images directly** when delivering results. Never respond with only file paths or file names. If the channel supports sending image files, send the file. If it supports inline display, display inline. If neither is possible, provide a clickable download link. A bare filename like `output.png` is never acceptable delivery.
7. **On iteration**, only re-generate what changed. Do not restart the entire workflow.
8. **If tools are missing**, propose to install them on behalf of the user — never expose tool names, PATH errors, or ask the user to run install commands. See "Missing Tools" below.
9. **Default to Nano Banana 2 unless the user asks otherwise.** When no default model is configured yet, initialize `GEMINI_3_1_FLASH_IMAGE` (Nano Banana 2), tell the user that it is now the default for this skill, and explicitly remind them they can switch any time if another model fits better.
10. **Reply in the user's language.** Match the language the user is using for questions, status updates, explanations, and delivery messages unless they explicitly ask you to switch.
11. **On first trigger, run readiness before anything else.** Check dependencies and `IMAGE_GEN_API_KEY` status before asking the user to choose a model or before starting generation.
12. **Handle API keys as secrets.** Offer to configure `IMAGE_GEN_API_KEY` locally for the user, avoid asking them to paste secrets into normal chat when a local write is possible, and never repeat or quote the key back.

## Re-run Behavior

- Running `main.ts` with the same `--image` path overwrites the existing output file.
- `--batchfile` re-processes all tasks in the batch; completed images are overwritten.
- `--dry-run` never writes files regardless of prior state.
- Polling a previously completed `taskId` returns the cached result without re-generating.

## Definition of Done

- `IMAGE_GEN_API_KEY` is configured and a default model is set in `EXTEND.md`.
- The CLI produces a valid image file (or a correct `--dry-run` request body).
- Batch mode completes all tasks and reports per-task status via `--json`.
- Failed tasks include a user-readable explanation, not just an error code.
- The model name is disclosed to the user before generation starts.

## Missing Tools

If `bun` and `npx` are both unavailable in the current environment:

1. **Do not expose tool names or PATH errors to the user.** Never mention "bun", "npx", "PATH", or installation commands.
2. **Propose installation in user-friendly terms.** Say something like: "I need to set up a small runtime to generate images — OK if I install it now? Takes about 30 seconds."
3. **On user approval**, run `npm install -g bun` or the platform-appropriate installer silently. Report success or failure in plain language.
4. **If the user declines or installation fails**, explain honestly: "I can't generate images in this environment right now. You can ask your admin to set up the image toolchain, or try again in a different environment."
5. **Never ask the user to install tools themselves** or paste terminal commands.

## Troubleshooting

See [references/weryai-platform.md](references/weryai-platform.md). For failed calls, compare the request and response with [call history](https://weryai.com/api/history).
