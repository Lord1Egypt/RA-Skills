---
name: bilibili-audio-transcribe
description: Download audio from Bilibili or b23.tv links and transcribe it into txt, srt, and segment JSON with yt-dlp, ffmpeg, and faster-whisper. Use when a user asks to turn a Bilibili link into text, subtitles, a transcript, or speech-to-text output, especially for Chinese-language videos.
---

# Bilibili Audio Transcribe

Convert a Bilibili link into local transcript files. Prefer this skill for Bilibili and `b23.tv` URLs only; do not use it for YouTube or generic web pages.

## Quick start

1. Ensure `ffmpeg` and `ffprobe` are on `PATH`.
2. If Python dependencies are missing, run `scripts/bootstrap_env.sh` or install `yt-dlp` and `faster-whisper` manually.
3. Run `scripts/transcribe_bilibili.py` with the target URL.
4. Return the generated transcript artifacts or summarize them if the user asked for analysis rather than raw text.

Example:

```bash
python scripts/transcribe_bilibili.py "https://b23.tv/SSx810h" \
  --out-dir ./downloads/bilibili-audio \
  --model-size base \
  --beam-size 3
```

## Workflow

### 1. Validate the request

Accept only `bilibili.com` or `b23.tv` URLs. If the URL points elsewhere, stop and say this skill is the wrong tool.

### 2. Prefer the bundled script

Use `scripts/transcribe_bilibili.py` instead of rewriting yt-dlp / whisper glue code in the session. The script:
- downloads the best available audio
- probes audio duration with `ffprobe`
- transcribes with `faster-whisper`
- writes `.txt`, `.srt`, and `.segments.json`
- prints coarse ETA / progress during ASR

### 3. Use sensible defaults

Default to:
- `--model-size base`
- `--beam-size 3`
- `--language zh`
- VAD enabled

These defaults are optimized for Chinese Bilibili speech. If the video is clearly non-Chinese or mixed-language, rerun with `--language auto` or a specific language code.

### 4. Keep outputs predictable

By default the script writes into `downloads/bilibili-audio/` relative to the current working directory. Keep all three artifacts unless the user explicitly asks for fewer outputs:
- transcript text: `.txt`
- subtitles: `.srt`
- segment metadata: `.segments.json`

### 5. Handle failures directly

If a run fails:
- missing `ffmpeg` / `ffprobe` → install system dependency first
- missing Python packages → run `scripts/bootstrap_env.sh`
- extractor or redirect issues → retry with the resolved canonical Bilibili URL
- poor transcript quality → rerun with `--language auto`, a larger model, or `--no-vad` when speech is clipped

Read `references/troubleshooting.md` when dependency setup or extraction fails.

## Resources

### scripts/

- `transcribe_bilibili.py` — main downloader + ASR pipeline
- `bootstrap_env.sh` — create a virtualenv and install Python dependencies
- `requirements.txt` — Python package list for the bootstrap script

### references/

- `troubleshooting.md` — dependency and extraction failure playbook
