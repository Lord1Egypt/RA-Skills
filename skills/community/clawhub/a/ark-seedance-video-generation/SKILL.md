---
name: ark-seedance-video-generation
description: End-to-end Volcengine Ark Seedance video generation using ARK_API_KEY and the bundled Node.js runner. Use when an agent needs to generate videos, handle text-to-video or image-to-video requests, poll task status, list or delete tasks, download generated assets, and follow a controlled SOP for model selection, local-media disclosure, and artifact handling.
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["node"],"env":["ARK_API_KEY"]},"primaryEnv":"ARK_API_KEY"}}
---

# Ark Seedance Video Generation

Use this skill as an execution skill for tool-using agents. The agent should run the existing script directly and complete the workflow for the user.

## Core Rules

- Use only `scripts/seedance-video.js` for live execution.
- Do not write another script, wrapper, or replacement implementation.
- Use `ARK_API_KEY` only. Do not use AK/SK.
- The script must receive an explicit model through `--model` or payload JSON.
- Restrict model choice at the skill layer to:
  - `doubao-seedance-1-0-pro-250528`
  - `doubao-seedance-2-0-260128`
- Default model at the SOP layer: `doubao-seedance-1-0-pro-250528`
- For local image, video, or audio inputs, explicitly tell the user the files will be uploaded to Volcengine Ark before execution.
- Save `request.json` in sanitized form only. Do not persist raw Base64 media data.

## Required Start

For every new generation request, the first model-facing message must:

1. List these two model IDs:
   - `doubao-seedance-1-0-pro-250528`
   - `doubao-seedance-2-0-260128`
2. Require the user to choose one before generation starts.

If the user already named one of the two approved IDs, use it and continue.

## Workflow

### 1. Intake

Determine:

- Generation mode: text-to-video, image-to-video, video-conditioned, audio-assisted, draft-task reuse, or task management
- Whether inputs are local files or remote URLs
- Whether the user asked for ratio, duration, resolution, seed, watermark, callback, or last-frame output
- Whether the request is a new generation, inspection, re-download, list, or deletion

### 2. Model Gate

- If the user already selected one of the two approved models, use it.
- If not, stop and ask them to choose one after listing the two approved IDs.
- Do not start generation, task creation, or payload submission until a model is chosen.
- Always pass the selected model explicitly through `--model` or payload JSON.

### 3. Auth Check

- Require `ARK_API_KEY`
- If missing, stop and tell the user exactly that `ARK_API_KEY` is required

### 4. Local Media Disclosure

If the request uses `--image-file`, `--video-file`, or `--audio-file`:

- Tell the user those files will be sent to Volcengine Ark
- If they object, stop before execution

### 5. Output Location

Prefer a workspace-local structure:

- `./outputs/seedance/<job-name>/request.json`
- `./outputs/seedance/<job-name>/task.json`
- `./outputs/seedance/<job-name>/<downloaded-assets>`

### 6. Command Choice

Use the existing script surface only:

- `run` for normal generation
- `create` or `create --wait true` only when the lifecycle requires it
- `get` for inspect or re-download
- `list` for browsing tasks
- `delete` for deletion
- `download` when assets are needed from an existing `task.json`

### 7. Flag Mapping

Map user inputs to:

- `--model`
- `--prompt`
- `--image-file` / `--image-url`
- `--video-file` / `--video-url`
- `--audio-file` / `--audio-url`
- `--draft-task-id`
- `--resolution`
- `--ratio`
- `--duration`
- `--frames`
- `--seed`
- `--camera-fixed`
- `--watermark`
- `--return-last-frame`
- `--callback-url`
- `--download-dir`

If the request needs unsupported advanced fields, write a JSON payload file and pass it through `--payload-file`.

### 8. Verify

After execution, verify what applies:

- final task status is `succeeded`
- `task.json` exists
- `request.json` exists and is sanitized
- output assets were downloaded
- last-frame asset exists when requested

### 9. Report

Return:

- requested task summary
- selected model ID
- command path used
- task ID when available
- output directory
- whether downloads completed
- relevant warnings or failures

## Command Patterns

Use these as execution patterns:

```powershell
node "./scripts/seedance-video.js" --model "<model-id>" --prompt "<prompt>" --download-dir "./outputs/seedance/run-001"
```

```powershell
node "./scripts/seedance-video.js" --model "<model-id>" --image-file "./inputs/source.png" --prompt "<prompt>" --return-last-frame true --download-dir "./outputs/seedance/image-to-video"
```

```powershell
node "./scripts/seedance-video.js" create --model "<model-id>" --prompt "<prompt>" --wait true --download-dir "./outputs/seedance/create-wait"
```

```powershell
node "./scripts/seedance-video.js" get --task-id "cgt-xxxx" --download-dir "./outputs/seedance/rerun-download"
```

```powershell
node "./scripts/seedance-video.js" --payload-file "./inputs/seedance-payload.json" --download-dir "./outputs/seedance/raw-payload"
```

## References

Read only when needed:

- `references/ark-video-api.md`
- `references/video-models.json`
- `references/video-models.md`
- `references/payload-patterns.md`
