---
name: douyin-upload-skill
description: Login and publish Douyin (China mainland) videos from local files with OAuth, local speech-to-text, and generated caption drafts. Use when users ask to authorize Douyin accounts, upload local videos, auto-generate title/description from video audio, confirm content, and publish via official Douyin OpenAPI with fallback export when publish permissions are missing.
---

# Douyin Upload Skill

## Overview

Use this skill to publish local videos to Douyin with a deterministic CLI flow:
1. Validate local dependencies and env.
2. OAuth authorize and store encrypted token locally.
3. Prepare video metadata and transcript from local audio.
4. Generate 3 caption candidates in chat from transcript.
5. Confirm or edit caption, then publish.
6. If official publish permission is unavailable, export an outbox package for manual publish.

Use the script at `<skill_root>/scripts/douyin.js`.

## Required Environment

Set these environment variables before `auth` or `publish`:
- `DOUYIN_CLIENT_KEY`
- `DOUYIN_CLIENT_SECRET`
- `DOUYIN_REDIRECT_URI`

Optional overrides:
- `DOUYIN_SCOPE`
- `DOUYIN_TOKEN_ENC_KEY`
- `DOUYIN_ASR_MODE` (`api` / `whisper-gpu` / `whisper-cpu`)
- `DOUYIN_ASR_API_URL`
- `DOUYIN_ASR_API_MODEL`
- `DOUYIN_ASR_API_KEY`
- `DOUYIN_WHISPER_BIN`
- `DOUYIN_WHISPER_MODEL_PATH`
- `DOUYIN_FFMPEG_BIN`
- `DOUYIN_FFPROBE_BIN`

## Workflow

1. Run dependency checks:
```bash
node <skill_root>/scripts/douyin.js doctor
```

2. Authorize account (manual code paste flow):
```bash
node <skill_root>/scripts/douyin.js auth
```

3. Prepare transcript and metadata from a local video path. Accept both Linux and Windows path formats.
```bash
node <skill_root>/scripts/douyin.js prepare --video "E:\\videos\\demo.mp4"
```

4. Create 3 caption candidates from `transcript.text` with this structure:
- Line 1: title hook
- Line 2-3: concise description
- Final line: 2-5 hashtags

5. Ask user to select or edit one final caption.

6. Publish with explicit visibility and confirmation policy:
```bash
node <skill_root>/scripts/douyin.js publish \
  --video "E:\\videos\\demo.mp4" \
  --text "<final caption>" \
  --private-status 0 \
  --auto-confirm false
```

## Command Behavior

- `doctor`: reports dependency and env readiness plus install hints.
- `auth`: opens OAuth URL, accepts pasted callback URL or `code`, stores encrypted token.
- `prepare`: returns metadata, transcript, and ASR failure detail (without stopping publish flow).
- `publish`: uploads and creates video via official API. If permission-like API errors occur, writes fallback files under outbox and returns `mode: fallback`.
- `config`: stores persistent settings (`defaultPrivateStatus`, `autoConfirm`, `whisperBin`, `whisperModelPath`, `outboxDir`, etc.).

## Caption Rules

Before publish:
- Keep final text length <= 1000.
- Always show the final draft to the user.
- If `auto-confirm` is false, require explicit user confirmation in terminal.

## Output Contracts

Treat script stdout as JSON. Always parse and branch by:
- `ok`
- `command`
- `mode` (`official` or `fallback` for `publish`)
- `asrError` (optional in `prepare`)
