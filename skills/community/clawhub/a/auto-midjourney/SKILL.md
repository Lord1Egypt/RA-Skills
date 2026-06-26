---
name: auto-midjourney
description: Automate Midjourney Alpha web image generation from Claude using the authenticated https://alpha.midjourney.com session. Use this skill whenever the user wants to create Midjourney images, submit MJ prompts, default to Midjourney v8, optimize Midjourney prompt syntax, or poll/download results from the Midjourney web app instead of Discord. Also use it when the user shares Alpha web request samples, cookies, channel IDs, or asks to reverse-engineer the Midjourney website workflow.
compatibility:
  - python3
  - network access
---

# Auto Midjourney

Use the user's own Midjourney Alpha web session to submit `imagine` jobs and optionally poll for results.

This skill is intended for conservative, user-triggered assistance rather than unattended bulk automation.

## What this skill does

- Submits prompts to `https://alpha.midjourney.com/api/submit-jobs`
- Defaults to Midjourney v8 for new prompts unless the user explicitly requests another version
- Keeps credentials in environment variables instead of hardcoding them into the skill
- Supports a one-command flow through `scripts/run_imagine.py`
- Can read `https://alpha.midjourney.com/api/user-mutable-state` to inspect current web settings
- Can infer `user_id` and `singleplayer_<midjourney_id>` from the authenticated cookie
- Applies local conservative throttling to reduce accidental request bursts
- Includes `scripts/mj_doctor.py` for setup validation
- Includes an experimental recent-jobs reader
- Supports `browser` transport backed by Chrome DevTools Protocol, with Playwright-over-CDP preferred when installed
- Supports optional polling once a job-status endpoint has been confirmed
- Includes prompt-craft guidance and reusable scenario presets for better prompt writing
- Includes a structured prompt builder and opt-in quality profiles
- Includes dedicated guidance for character sheets, split-view turnarounds, and reusable design assets

## Current scope

This version focuses on:

1. `imagine`
2. Midjourney v8 as the default version
3. Alpha web flow, not Discord bot flow
4. Safe local configuration via `.env`
5. Easier operation through inferred IDs, presets, and doctor checks

Implemented:

- `imagine` submit through the Alpha web flow
- browser-backed verification using low-impact CDP network watching plus page asset fallback
- local download of the 4 returned image assets
- optional browser-side conversion from `webp` to `png` during download
- sequential batch generation

Not implemented yet:

- Upscale / variation / reroll button actions
- Image upload / reference-image workflow
- Automatic result download from a confirmed final image endpoint

Those should be added only after capturing stable request samples from the browser.

## Safety posture

Do not optimize this skill for bypassing restrictions, hiding automation, rotating accounts, or mass unattended generation.

Use these guardrails instead:

- trigger requests manually
- keep request frequency low
- leave local throttling enabled
- validate config with `mj_doctor.py`
- prefer one human action to one live submit

The goal is risk reduction through conservative usage, not evasion.

## Trigger rules

Use this skill proactively when the user asks to:

- “用 Midjourney / MJ 出图”
- “用 Midjourney v8 生成”
- “帮我提交 imagine”
- “优化 Midjourney prompt”
- “做角色设定稿 / 四视图 / 角色资产图”
- “抓 Midjourney Alpha 网站请求”
- “轮询 Midjourney job 状态”
- “把网页版 Midjourney 做成自动化能力”

## Required configuration

Read these values from `.env` or shell environment:

| Variable | Required | Purpose |
|---|---|---|
| `MJ_COOKIE` | Yes | Full authenticated Cookie header copied from browser |
| `MJ_CHANNEL_ID` | Yes | Alpha web singleplayer channel ID |
| `MJ_STATUS_URL_TEMPLATE` | No | Job status endpoint template containing `{job_id}` |
| `MJ_USER_STATE_PATH` | No | Defaults to `/api/user-mutable-state` |
| `MJ_RECENT_JOBS_URL` | No | Experimental recent-jobs endpoint |
| `MJ_MODE` | No | `fast` by default |
| `MJ_PRIVATE` | No | `true` by default |
| `MJ_MIN_SUBMIT_INTERVAL_SECONDS` | No | Local minimum spacing between submits. Default is `3` seconds |
| `MJ_MAX_SUBMITS_PER_HOUR` | No | Local hourly cap. Set `0` to disable, which is now the default |
| `MJ_MAX_SUBMITS_PER_DAY` | No | Local daily cap. Set `0` to disable, which is now the default |
| `MJ_USER_ID` | No | Usually inferred from the auth cookie |
| `MJ_METRICS_TOKEN` | No | Optional token observed on telemetry requests |
| `MJ_BROWSER_BACKEND` | No | `auto` by default. Set `playwright` or `cdp` to force a backend |

Never write real cookies or tokens into `SKILL.md`, reference files, git-tracked scripts, or user-facing summaries.

## System requirements

For platform and device requirements, read [system-requirements.md](/Users/shitengda/Downloads/docker/n8n/skills/auto-midjourney/references/system-requirements.md).

## Workflow

### Scenario 0: Check config first

Run:

```bash
python3 scripts/mj_doctor.py --fetch-user-state --transport browser
```

This shows:

- whether the cookie exists
- inferred `midjourney_id`
- inferred `channel_id`
- current server-side speed and visibility
- current local safe-limit settings

### Scenario 1: Submit one prompt

Run:

```bash
python3 scripts/run_imagine.py "1 girl --ar 16:9" --transport browser
```

Default behavior:

- Appends `--v 8` if the prompt does not already specify a version
- Appends `--raw` by default unless the user disables it
- Uses `MJ_MODE` and `MJ_PRIVATE` from the environment
- Can sync server-side defaults before submitting
- Records the submit locally and enforces conservative pacing
- Prints structured JSON with the request payload, submission response, and extracted `job_id`

For simplest live use:

```bash
python3 scripts/run_imagine.py "cinematic portrait of a fox astronaut" --transport browser --sync-user-state --wait-page-assets --download --convert-to png
```

When `--wait-page-assets` is enabled, the browser transport now prefers watching Midjourney's existing in-page network traffic for the submitted `job_id`. It falls back to page asset probing only if the low-impact watcher does not yield 4 images.

### Scenario 2: Submit and wait

If a working status endpoint has been captured and stored in `MJ_STATUS_URL_TEMPLATE`, run:

```bash
python3 scripts/run_imagine.py "cinematic portrait of a fox astronaut --ar 16:9" --wait
```

### Scenario 3: Low-risk debugging

Use dry-run first when changing payload structure:

```bash
python3 scripts/run_imagine.py "robot barista in tokyo alley" --dry-run
```

This validates prompt normalization and payload generation without sending a live request.

### Scenario 3b: Use a preset

Run:

```bash
python3 scripts/run_imagine.py "silver perfume bottle on black glass" --preset product --sync-user-state
```

Preset definitions live in `config/presets.example.json`.

When the user wants better prompt wording, templates, or parameter tradeoffs, read [prompt-craft.md](/Users/shitengda/Downloads/docker/n8n/skills/auto-midjourney/references/prompt-craft.md).

### Scenario 3c: Build a prompt from a template

Run:

```bash
python3 scripts/mj_prompt_helper.py --template product --subject "premium silver perfume bottle" --camera "front three-quarter angle" --surface "black glass surface" --lighting "controlled softbox rim light" --background "dark charcoal background" --mood "minimal luxury beauty campaign" --preset product_clean_square --quality-profile final_v8_q4 --json
```

This produces a V8-friendly prompt string and a ready-to-run `run_imagine.py` command.

### Scenario 4: Read current web settings

Run:

```bash
python3 scripts/get_user_state.py --transport browser
```

This reads the same `user-mutable-state` endpoint the web app uses and returns values such as:

- `settings.speed`
- `settings.visibility`
- `abilities`
- saved `macros`

## Command reference

### Submit only

```bash
python3 scripts/submit_job.py "minimalist glass monolith --ar 16:9 --v 8"
```

### Poll one job

```bash
python3 scripts/poll_job.py "<job_id>"
```

### Inspect current server-side settings

```bash
python3 scripts/get_user_state.py --transport browser
```

### Validate config and inferred identity

```bash
python3 scripts/mj_doctor.py --fetch-user-state --transport browser
```

### Experimental recent jobs lookup

```bash
python3 scripts/list_recent_jobs.py --amount 10
```

### Submit, verify, and download locally

```bash
python3 scripts/run_imagine.py "fashion editorial, silver fabric, studio light --ar 3:4" --transport browser --sync-user-state --wait-page-assets --download --convert-to png
```

### Batch generate and store PNGs

```bash
python3 scripts/batch_generate.py config/prompts.example.txt --transport browser --sync-user-state --convert-to png
```

Use conservative fixed spacing and batch cooldowns when needed:

```bash
python3 scripts/batch_generate.py config/prompts.example.txt --transport browser --sync-user-state --convert-to png --batch-size 5 --submit-interval-seconds 120 --batch-cooldown-seconds 600
```

Apply an opt-in quality profile to the whole batch:

```bash
python3 scripts/batch_generate.py config/prompts.example.txt --transport browser --sync-user-state --quality-profile final_v8_q4 --convert-to png
```

### Convert existing WEBP downloads to PNG

```bash
python3 scripts/convert_downloads.py outputs
```

Or write converted files into a separate directory:

```bash
python3 scripts/convert_downloads.py outputs --output-dir outputs/png-converted
```

If you want to rebuild PNGs from a saved result manifest instead of local files:

```bash
python3 scripts/convert_downloads.py outputs/live-test/recent-job.json --output-dir outputs/png-rebuilt
```

This waits for the submitted `job_id` to appear in the browser page resource list, verifies that 4 Midjourney CDN image URLs exist, and downloads the returned image files into `outputs/<job_id>/`.

### Batch generate sequentially

Create a text file with one prompt per line, then run:

```bash
python3 scripts/batch_generate.py prompts.txt --transport browser --sync-user-state --download-dir outputs/batch
```

This submits prompts one by one, waits for each `job_id` to produce page resource URLs, and downloads the returned image files before moving to the next prompt.

### Full flow

```bash
python3 scripts/run_imagine.py "fashion editorial, silver fabric, studio light --ar 3:4" --sync-user-state --wait-recent-jobs --download
```

## Prompt defaults

When the user does not specify MJ flags:

- Default to `--v 8`
- Default to `--raw`
- Preserve any explicit aspect ratio or style flags already present
- Do not auto-add `--hd`
- Treat `--q 4` as an opt-in final-pass override rather than a default for the current V8-focused flow

Do not silently override explicit user flags.

## Output format

When you use this skill, report back in this structure:

```text
Prompt: <final prompt sent>
Job ID: <job_id or "not returned">
Mode: <fast/relax/etc>
Visibility: <private/public>
Status: <submitted / polled / failed / dry-run>
Notes: <missing status endpoint, saved JSON path, or next step>
```

## Simpler usage model

For day-to-day use, prefer this sequence:

1. `python3 scripts/mj_doctor.py --fetch-user-state --transport browser`
2. `python3 scripts/run_imagine.py "<prompt>" --transport browser --sync-user-state`
3. `python3 scripts/run_imagine.py "<prompt>" --transport browser --sync-user-state --wait-page-assets --download`

This reduces manual mistakes and keeps you in a low-frequency workflow. On this machine, `browser` transport is the preferred live path because raw HTTP requests are blocked by Cloudflare.

## Success criteria for a usable generation

Treat a generation as verified only when all of these are true:

1. submit response contains a `job_id`
2. page resource entries contain 4 CDN image URLs for the same `job_id`
3. the image files are downloaded successfully to local disk

Normal Midjourney `imagine` behavior is a 4-image grid. Depending on the endpoint response, you may get one grid image file rather than four separately cropped files. This skill currently verifies and downloads the returned image assets as provided by Midjourney.

## Extension path

After the user captures more browser requests, extend in this order:

1. Confirm job-status endpoint and final-image fields
2. Add result downloader
3. Add button-action support for upscale / variation
4. Add reference image upload flow
5. Add prompt-template helpers for common MJ styles

## Confirmed non-status endpoints

- `POST https://proxima.midjourney.com/` is currently treated as telemetry ingestion
- `POST /api/v1/traces` is currently treated as tracing/observability data
- `GET /api/user-mutable-state` is useful for reading current speed and visibility defaults

Do not mistake telemetry endpoints for job-status APIs.

## GitHub-informed but experimental path

The skill includes an experimental `recent-jobs` reader based on public GitHub reverse-engineering notes. Treat it as best-effort support rather than a stable API contract.
