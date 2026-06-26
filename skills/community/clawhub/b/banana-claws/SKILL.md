---
name: banana-claws
description: Generate images via OpenRouter API (text-to-image) with automation-ready local scripts and a queue-first workflow. Use for single images or batched variants (posters, thumbnails, illustrations, concept art), especially when agents must acknowledge quickly, process asynchronously, and return consolidated file attachments with structured success/failure records.
homepage: https://github.com/ironystock/banana-claws
user-invocable: true
metadata: {"openclaw":{"emoji":"🍌","primaryEnv":"OPENROUTER_API_KEY","requires":{"bins":["python3"],"env":["OPENROUTER_API_KEY"]}}}
---

# OpenRouter Image Generation

Generate images from prompts using OpenRouter's image generation endpoint.

## Requirements

- `OPENROUTER_API_KEY` in environment
- `python3`
- Python package: `requests`

Install dependency:

```bash
python3 -m pip install requests
```

## FTUX preflight (run first)

```bash
python3 {baseDir}/scripts/preflight_check.py
python3 {baseDir}/scripts/preflight_check.py --json
```

If checks fail, tell the user exactly what is missing and provide copy/paste fix steps from the `Fixups` output.

## Default model

- `google/gemini-3.1-flash-image-preview`
- Optional alternatives (if enabled on your account): `openai/gpt-5-image`, `openai/gpt-5-image-mini`

## Usage

```bash
python3 {baseDir}/scripts/generate_image.py \
  --prompt "A cinematic portrait of a cyberpunk crab" \
  --model google/gemini-3.1-flash-image-preview \
  --image-size low \
  --out ./generated/cyber-crab.png
```

Optional args:

```bash
--model openai/gpt-5-image
--model openai/gpt-5-image-mini
--image-size low|medium|high
--clarify-hints      # print prompt-quality hints to stderr
--strict-clarify     # fail fast when prompt appears underspecified
--baseline-image ./path/to/reference.png
--baseline-source-kind current_attachment|reply_attachment|explicit_path_or_url
--confirm-external-upload # required for local baseline file upload
--variation-strength low|medium|high
--must-keep "title placement"
--must-keep "logo mark"
--lock-palette
--lock-composition
--allow-no-baseline-on-edit-intent
```

## Queue -> response pattern (avoid traffic jams)

When a user asks for multiple images/iterations, do **not** hold one long-running turn per image.
Do not block waiting for a "single message with all files" if the adapter does not support it.

**Hard contract for queue mode:**
- NEVER run `run_image_queue.py` in the same foreground turn as enqueue for multi-image requests.
- ALWAYS enqueue + immediate queued ack first, then background handoff.

Use a queue + batched response flow:

1. Enqueue each requested image quickly.
2. **Immediately return** with a short "queued" acknowledgement (do not wait for generation in the same turn).
3. Drain queue in background (preferred: sub-agent/session worker).
4. Send one consolidated completion status response when done.
5. **Always attach generated image files** (never send only paths).
6. If the messaging adapter allows only one media per send, post attachments as reply-chain messages under the consolidated completion status message (one file per message).

Enqueue command:

```bash
python3 {baseDir}/scripts/enqueue_image_job.py \
  --prompt "A retro 80s crab poster" \
  --model google/gemini-3.1-flash-image-preview \
  --image-size low \
  --clarify-hints \
  --out ./generated/crab-01.png \
  --request-id "discord-<message-id>"
```

Background queue handoff (recommended):

```bash
python3 {baseDir}/scripts/queue_and_return.py \
  --prompt "A minimalist snow crab logo" \
  --count 4 \
  --request-id "discord-<message-id>" \
  --out-dir ./generated \
  --prefix crab-logo \
  --queue-dir ./generated/imagegen-queue
```

Manual drain command (worker context only; not same foreground turn):

```bash
python3 {baseDir}/scripts/run_image_queue.py \
  --queue-dir ./generated/imagegen-queue

# queue_and_return guardrails (optional tuning)
python3 {baseDir}/scripts/queue_and_return.py \
  --max-background-workers 2 \
  --orphan-timeout-sec 1800 \
  ...
```

Batch-enqueue N variants with consistent file names:

```bash
python3 {baseDir}/scripts/enqueue_variants.py \
  --prompt "A minimalist snow crab logo" \
  --count 4 \
  --baseline-image ./generated/base-logo.png \
  --variation-strength low \
  --lock-palette \
  --lock-composition \
  --must-keep "wordmark placement" \
  --must-keep "icon silhouette" \
  --out-dir ./generated \
  --prefix crab-logo \
  --request-id "discord-<message-id>"
```

Useful options:

```bash
--max-jobs 3   # process only a subset for controlled batches
--start-index 5  # continue naming from prior batches
```

## Data transmission notice (external provider)

- This skill sends prompts and generated/edit inputs to OpenRouter (`openrouter.ai`).
- If you pass `--baseline-image`, that image content is transmitted to the provider as part of the request.
- Do not submit sensitive/private images unless the user explicitly approves external transmission.

## Notes

- If generation fails due to model/provider mismatch, retry with `--model openai/gpt-5-image-mini`.
- Local baseline uploads are deny-by-default; pass `--confirm-external-upload` only when user explicitly approves sending that local file to provider.
- Local baseline files are restricted to png/jpg/jpeg/webp, non-symlink regular files, workspace-local paths, and max size threshold.
- For iterative work, prefer `--image-size low`; switch to `medium` or `high` for final renders.
- Use `--clarify-hints` to surface prompt-quality gaps early; use `--strict-clarify` for workflows that must fail on ambiguity.
- Keep prompts explicit for text rendering tasks.
- Save outputs into workspace paths, not `/tmp`, for durability.
- When user asks for generated images in chat, attach the generated file in the response (do not only send a path).
- For queue mode, read results from:
  - `.../imagegen-queue/results/*.json` (success)
  - `.../imagegen-queue/failed/*.json` (failure details)
- Edit/variant intent prompts fail fast if no baseline is supplied (`--baseline-image`) unless explicitly overridden.
- Resolve baseline deterministically in caller: current-message attachment > replied-message attachment > clarification request.
- Pass `--baseline-source-kind current_attachment|reply_attachment|explicit_path_or_url` for auditable provenance.
- When baseline is supplied, rails default to low-variation + locked palette/composition unless explicitly changed.
- Queue results persist provider metadata (generation id + provider response payload/path) and drift diagnostics (`edit_intent_detected`, `baseline_applied`, `baseline_source`, `baseline_source_kind`, `baseline_resolution_policy`, `rails_applied`) to help edits/debugging and smarter agent continuation.
- Queue worker writes `handoff_mode` + `same_turn_drain_detected` so you can enforce true async behavior in tests/ops.
- `enqueue_variants.py` writes `<prefix>-manifest.json` with baseline, constraints, variant deltas, and output targets for reproducible reruns.
