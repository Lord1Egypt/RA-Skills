# Image Generation CLI

Every slide image comes from `scripts/image_gen.py`, which calls the dLazy tool API. This document owns the commands, runtime setup, image-input limits, editing, and troubleshooting.

Let `{skill_root}` mean the directory containing `SKILL.md`.

## Runtime Setup

Image commands and `scripts/assemble_ppt.py` use the shared runtime environment. If `~/.dlazy-ppt/.venv/bin/python` is missing, or importing script dependencies fails, create or refresh the environment:

```bash
python3 {skill_root}/scripts/dlazy_ppt_runtime.py bootstrap
```

This is an internal setup step for the skill. Do not ask the user to run it unless dependency installation fails and user approval or troubleshooting is required.

The CLI loads `~/.dlazy-ppt/.env` automatically for `DLAZY_API_KEY`, `DLAZY_BASE_URL`, and `DLAZY_PPT_IMAGE_MODEL`. Do not manually parse `.env`. For API key, base URL, model, and config troubleshooting, read `image-model-configuration.md` only after the CLI reports missing or invalid configuration, when the user explicitly wants to change those settings, or when a real API call reports an authentication, permission, credit, or model availability failure.

## Generate One Slide

Basic generation command:

```bash
~/.dlazy-ppt/.venv/bin/python {skill_root}/scripts/image_gen.py generate \
  --prompt-file {prompt_file} \
  --size 2048x1152 \
  --quality medium \
  --out {base_dir}/{deck_name}/origin_image/slide_01.png
```

When generating from saved `prompts/slide_XX.json` files, use the job's `prompt` field only when the job does not require input images:

```bash
python3 -c 'import json, pathlib; print(json.loads(pathlib.Path("{base_dir}/{deck_name}/prompts/slide_01.json").read_text())["prompt"])' | \
~/.dlazy-ppt/.venv/bin/python {skill_root}/scripts/image_gen.py generate \
  --prompt-file - \
  --size 2048x1152 \
  --quality medium \
  --out {base_dir}/{deck_name}/origin_image/slide_01.png
```

Before using this text-only `generate` path, inspect the assigned `prompts/slide_XX.json`. If `input_images` is non-empty or `requires_context_images` is true, this command is not sufficient because it does not attach those images: use `edit` with every required source image passed as `--image`. If a required image is missing, stop and report a blocker. Do not generate a text-only replacement for a strict input asset.

## Generate A Whole Deck

`generate-batch` runs one job per line of a JSONL file, concurrently:

```bash
~/.dlazy-ppt/.venv/bin/python {skill_root}/scripts/image_gen.py generate-batch \
  --input {base_dir}/{deck_name}/prompts/jobs.jsonl \
  --out-dir {base_dir}/{deck_name}/origin_image \
  --concurrency 5
```

Each line is either a prompt string or an object whose keys override the shared flags (`prompt`, `size`, `quality`, `out`). Rate limits and server errors are retried per job (`--max-attempts`, default 3); a rejected prompt is not retried, because it never succeeds on a second try.

## Sizes And Limits

The tool accepts a fixed set of sizes: `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`, `auto`. Anything else is rejected before the call is spent.

- Slides are 16:9, so use `2048x1152` (the default) or `3840x2160`.
- Use `--size 3840x2160 --quality high` only when the user asks for 4K, text-heavy slides need sharper output, or the default result is blurry. It costs noticeably more credits per page.
- `2160x3840` is portrait; use it only if the user requests portrait output.

The `prompt` is capped at 2000 characters. The CLI rejects a longer prompt locally rather than paying for a 400. A prompt cannot be split the way narration can — half a description renders half a slide — so shorten the description or drop optional prompt fields (`--scene`, `--materials`, `--negative`) instead.

At most 5 input images can be attached to one call.

## Editing Slides

If a slide is mostly correct but has a localized issue, edit it instead of regenerating:

```bash
~/.dlazy-ppt/.venv/bin/python {skill_root}/scripts/image_gen.py edit \
  --image {slide_path} \
  --prompt {edit_prompt} \
  --out {new_slide_path}
```

`--image` may be repeated, up to 5 images. Local files are uploaded to dLazy storage first; the model reads them from there. Replace the final slide only after validating the edited output.

## Transparent Backgrounds

The image tool has no transparency parameter. For transparent assets, generate on a flat chroma-key background and remove it locally with `scripts/remove_chroma_key.py`. This works well for simple opaque subjects and is the only supported path.

## Assembly And Doctor

`assemble_ppt.py` supports `16:9` and `4:3`. Use `16:9` unless the user requests otherwise.

Check the runtime and API access with:

```bash
python3 {skill_root}/scripts/dlazy_ppt_runtime.py doctor --check-api
```

It verifies the shared venv, reports the effective configuration, and confirms the key works and the configured model is available on the account.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `DLAZY_API_KEY is not set` | No key configured | `dlazy_ppt_runtime.py config --api-key <key>` |
| HTTP 401 / `unauthorized` | Key invalid or revoked | Get a new key at https://dlazy.com/dashboard/organization/api-key |
| `insufficient_balance` | Organization out of credits | Top up at https://dlazy.com/dashboard/organization/settings?tab=credits |
| HTTP 426 | Server requires a newer CLI contract | Raise `CLI_VERSION` in `scripts/dlazy_client.py` |
| `prompt is N characters` | Prompt over 2000 chars | Shorten the slide description |
| `invalid choice: '2560x1440'` | Size not in the tool's list | Use `2048x1152` or `3840x2160` |
