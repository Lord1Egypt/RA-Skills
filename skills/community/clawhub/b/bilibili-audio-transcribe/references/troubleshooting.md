# Troubleshooting

## Missing ffmpeg / ffprobe

Symptom:
- `未找到 ffmpeg 或 ffprobe`

Fix:
- macOS (Homebrew): `brew install ffmpeg`
- Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y ffmpeg`
- Verify: `ffmpeg -version` and `ffprobe -version`

## Missing Python packages

Symptom:
- `ModuleNotFoundError: No module named 'yt_dlp'`
- `ModuleNotFoundError: No module named 'faster_whisper'`

Fix:
1. Run `scripts/bootstrap_env.sh`
2. Activate the environment
3. Re-run the transcription command

Recommendation:
- Prefer Python 3.10+ for new environments. `yt-dlp` is deprecating Python 3.9 support, so old interpreters may still work today but are a future footgun.

## URL rejected

This skill intentionally supports only:
- `bilibili.com`
- `b23.tv`

If the user gives a YouTube or generic URL, use a different skill/workflow.

## Extraction fails on a short link

If `b23.tv` extraction behaves oddly, retry with the resolved canonical `https://www.bilibili.com/video/...` URL. yt-dlp usually follows redirects, but a manual retry can simplify debugging.

## Transcript quality is weak

Try one or more of:
- `--language auto`
- larger model size such as `small` or `medium`
- `--no-vad` when speech is clipped or over-segmented

## Slow CPU transcription

`faster-whisper` on CPU can still take minutes for longer videos. The bundled script prints rough progress and ETA. If the user only needs a summary, finish transcription first and summarize the generated `.txt` file instead of retrying multiple extraction paths.

## CLI mismatch gotcha

The bundled script accepts both:
- `--out-dir`
- `--output-dir`

and both:
- `--model-size`
- `--model`

This is intentional to reduce caller friction.
