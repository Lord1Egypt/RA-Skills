---
name: aliyun-speech-transcriber
description: Transcribe publicly accessible audio or video URLs with Aliyun speech services. Use when the user wants speech-to-text via Aliyun DashScope, needs transcript JSON or extracted plain text, or wants to process a cloud-accessible media URL (including signed Qiniu URLs) into transcription results.
homepage: https://dashscope.aliyun.com/
metadata: {"clawdbot":{"emoji":"🎤","requires":{"env":["ASR_DASHSCOPE_API_KEY"]},"tags":["speech","transcription","asr","audio","aliyun","dashscope"]}}
---

# Aliyun Speech Transcriber

Use this skill to turn externally accessible media URLs into transcript results.

## Current scope

Current implementation focuses on **DashScope file transcription** using the `paraformer-v2` model, aligned with the existing Java service pattern.

## Required environment variables

- `ASR_DASHSCOPE_API_KEY`

Fallback supported:

- `DASHSCOPE_API_KEY`

Optional:

- `ALIYUN_SPEECH_MODEL` - defaults to `paraformer-v2`
- `ALIYUN_SPEECH_LANG_HINTS` - defaults to `zh,en`
- `ALIYUN_SPEECH_POLL_SECONDS` - defaults to `5`
- `ALIYUN_SPEECH_TIMEOUT_SECONDS` - defaults to `1800`

## Inputs

Pass one or more externally accessible URLs:

```powershell
node scripts/transcribe.js --file-url "https://example.com/audio.mp3"
```

Multiple files:

```powershell
node scripts/transcribe.js --file-url "https://a.com/1.mp3" --file-url "https://a.com/2.mp3"
```

## Output

The script returns JSON with:

- `success`
- `provider`
- `engine`
- `taskId`
- `requestId`
- `results`
- `text`

`text` is a best-effort plain-text extraction from the final JSON result.

## Chaining from Qiniu

Typical workflow:

1. Use `qiniu-upload` to upload a local file.
2. Prefer a signed private URL if the domain is not anonymously readable.
3. Pass the returned URL into this skill.

## Safety rules

- Never hardcode Aliyun credentials.
- Fail fast if `DASHSCOPE_API_KEY` is missing.
- Only send URLs the user intends to transcribe.
