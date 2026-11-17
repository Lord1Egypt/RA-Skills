---
name: aidso-human-video-generator
display_name: 爱搜数字人视频生成
display_name_en: AIDSO Digital Human Video Generator
description: 当用户需要绑定 AIDSO、提取参考视频文案，或用用户提供的文案生成并查询数字人视频时使用。
description_zh: 提取参考视频文案，或使用现成文案生成数字人视频并查询结果。
description_en: Extract reference-video text or generate and track an AIDSO digital-human video from user-provided copy.
version: 0.4.7
author: "AIDSO 爱搜"
---

# Aidso Human Video Generator

## Overview

Use this skill to bind an AIDSO account, extract benchmark-video text, and generate digital-human videos through AIDSO Skills API. Do not import, paste, bundle, or display user secrets. On first use, start the AIDSO authorization-link flow and save only the returned local binding file.

Run the commands below from the directory containing this `SKILL.md`. When the shell starts elsewhere, use an absolute path to each script in this skill's `scripts/` directory.

Keep installation and package-delivery output platform-agnostic. Do not report host-specific installation or local binding state in that output. Account binding is handled only when the skill is first used or when the user explicitly asks to check authorization.

## Workflow

1. Ensure runtime authorization. If no local binding exists, follow the two-phase authorization flow below and stop until the user approves it.
2. Collect the digital-human description without requiring body-framing details.
3. Ask the user to choose the generation method: imitation or original with their own video script.
4. Prepare a script source and stop for user confirmation.
5. Collect video configuration: subtitle `on|off`.
6. Ask whether the user wants a preview or direct full generation.
7. For full generation, get the estimated points and explicit user confirmation.
8. Submit the video generation task.
9. Return the `taskId` to the user.
10. Poll the result only when requested or when the user wants the final links.

## Generation Methods

Use one of these paths.

### Imitation

1. Ask for the benchmark video URL.
2. Submit text extraction:

```bash
python scripts/submit_text_extract.py --url "https://www.douyin.com/jingxuan?modal_id=7654800977366715698"
```

3. Poll until `status_message` indicates extraction is complete:

```bash
python scripts/poll_text_extract.py --task-id <extract-task-id>
```

4. Return the extracted `text` to the user as the source script. Do not rewrite it yet.
5. Ask the user to choose one next action:
   - Use as-is: use the extracted text directly for video generation.
   - User edits: wait for the user to provide the modified script.
   - Rewrite: ask for rewrite requirements, then rewrite with the model.
6. Only produce a rewritten script after the user explicitly chooses rewrite. When rewriting, do not copy protected wording verbatim; preserve structure, pacing, and selling logic only if the user asks for imitation.
7. Confirm the final script before direct full generation unless the user explicitly says to proceed.

### Original

1. Ask exactly: `请提供视频文案。`
2. Use the user's video script as provided. Do not require brand knowledge, product facts, audience, tone, or copywriting requirements.
3. Edit or rewrite the script only if the user explicitly asks. Confirm the final script before direct full generation unless the user explicitly says to proceed.

## Video Configuration

Collect:

- `desc`: ask exactly: `请描述你想要的数字人，例如人物类型、年龄感、服装、气质或风格。`
- `subtitle`: `on` or `off`.

The video generation API currently accepts only `text`, `desc`, `subtitle`, and `aspect_ratio`. Put all character and styling requirements in `desc`.
The video aspect ratio is fixed to `Portrait`. Do not ask the user to choose an aspect ratio.
Do not require body framing, camera distance, or pose details. Continue when the user does not provide them.

## Preview Or Direct Generation

Ask whether the user needs a preview:

- Ask exactly: `你需要预览还是直接正式生成？`
- Preview: label this option only as `预览`, then submit with `--preview`, which sends the fixed text `测试`.
- Direct generation: submit with the confirmed final script through `--text`.
- Do not append any point, price, or consumption note to the preview option or preview result.

## Point Confirmation

Before submitting a full generation task, run `scripts/submit_video.py --estimate-only` with the exact final script. Read `required_points` from the result.

Tell the user only:

`正式生成预计消耗 {required_points} 积分，是否确认提交？`

Do not show the source text length, point formula, divisor, rounding method, arithmetic, or calculation process. Do not mention point consumption when offering or returning a preview.

Do not submit a full generation task until the user explicitly confirms the displayed estimate. The `submit_video.py` script enforces this with `--confirm-points`; without confirmation, it returns the estimated points and exits without creating a task.

Preview example:

```bash
python scripts/submit_video.py \
  --preview \
  --desc "商务男主播，稳重专业" \
  --subtitle on
```

Direct generation example:

```bash
python scripts/submit_video.py \
  --text "爱搜数字人视频生成测试" \
  --desc "商务男主播，稳重专业" \
  --subtitle on \
  --confirm-points <confirmed-points>
```

Always return the `taskId` to the user so they can manually poll if an automated poll fails.

## Poll Result

Use `scripts/poll_video.py` when the user wants the result for a known task.

```bash
python scripts/poll_video.py --task-id a562665671304e29b1f378b65b5d9cd9
python scripts/poll_video.py --task-id a562665671304e29b1f378b65b5d9cd9 --once
```

On success, return only the useful result fields to the user:

- `video_url`
- `preview_url`

If polling times out or fails, return the `taskId` and explain that it can be retried.

## Legacy Minimal Flow

For a user who already provides final text and all video configuration:

1. Ensure account authorization.
2. Estimate point cost with `scripts/submit_video.py --estimate-only`.
3. Ask the user to confirm the required point spend.
4. Submit with `scripts/submit_video.py --confirm-points <confirmed-points>`.
5. Poll with `scripts/poll_video.py`.

## Authorization

Use `scripts/auth.py` when the user asks to bind, check, or repair AIDSO authorization.

```bash
python scripts/auth.py --start
python scripts/auth.py --complete
python scripts/auth.py --status
```

`--status` reports whether a local binding exists, authorization is pending or expired, or no binding exists. It never displays the credential and does not verify server-side validity.

Use this two-phase flow:

1. Run `python scripts/auth.py --start`. It creates a fresh authorization link and exits immediately.
2. Return the exact `authorization_url` to the user at once as a clickable link. Tell the user it expires in about 10 minutes.
3. Do not fetch, pre-open, inspect, or validate the link with a plain HTTP request. The authorization page is a JavaScript application; HTTP 200 does not prove that the request is valid.
4. Stop and wait for the user to approve the link in a JavaScript-enabled browser.
5. After the user says authorization is complete, run `python scripts/auth.py --complete` once.
6. If the result is `pending`, ask the user to finish approval using the same unexpired link. Do not generate another link.
7. If the link is expired or the page says the request is invalid, run `--start` again and immediately return only the newly generated link.
8. After `--complete` returns `authorized`, retry the original video or text-extraction command.

Never run a blocking authorization poll while waiting for user interaction. Other scripts may generate the same fresh-link response when no local binding exists; surface that link immediately, then use `auth.py --complete` after approval.

Credential rules:

- Treat authorization as runtime-only. Installation must not check whether a local binding file already exists.
- Installation summaries must present authorization as a first-use runtime step.
- Select and probe a writable local binding path before generating the authorization link.
- Default to `./.aidso/credentials.json`; fall back to the installed skill directory or a temporary runtime path if the working directory is not writable.
- Never ask the user to paste a key in chat.
- Never print or summarize the key, even masked, in install or status messages.
- Never ship, preload, or directly import a key through environment variables or package files.
- Read the local binding file only after it was created by the authorization flow.
- Store pending authorization state locally with file mode `0600` before writing its contents; do not expose the standalone `code` in user-facing output.
- When no local binding is available, generate a fresh authorization link, return it immediately, then query by `code` only after the user confirms approval.
- Save the returned credential atomically with file mode `0600` and never include its value in command output.

All authorization, text extraction, video generation, and result polling requests use the production AIDSO API at `https://api.aidso.com`. Do not switch to a test, staging, or custom API base URL.

## Resources

- `manifest.yaml`: supplementary capability summary; WorkBuddy reads the frontmatter above for skill metadata.
- `scripts/_aidso.py`: shared HTTP, credential, and authorization helpers.
- `scripts/auth.py`: account binding and status check.
- `scripts/submit_text_extract.py`: create a benchmark-video text extraction task.
- `scripts/poll_text_extract.py`: poll text extraction and return extracted `text`.
- `scripts/submit_video.py`: create a video generation task.
- `scripts/poll_video.py`: poll a task for `video_url` and `preview_url`.

Read the API details, payload conventions, and examples when verifying endpoint behavior or payloads:

@references/api-spec.md
