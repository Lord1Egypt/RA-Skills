---
name: audio-srt-workflow
description: Generate or align SRT subtitles from audio using this repository. Use when the user asks for subtitle generation, transcript-to-audio alignment, timing cleanup, SRT quality checks, or subtitle preview video rendering.
license: MIT
compatibility: Requires Python 3.10+, ffmpeg in PATH, and faster-whisper runtime support.
metadata:
  owner: Sariel2018
  repository: audio-srt-aligner
---

# Audio SRT Workflow

Use this skill for end-to-end subtitle work.

This package is self-contained for runtime entrypoints:

- `scripts/align_to_srt.py`
- `scripts/gui_app.py`
- `scripts/srt_stats.py`
- `scripts/make_preview_mp4.py`
- `scripts/requirements.txt`

## Scope

- Mode A: audio + reference text -> aligned SRT
- Mode B: audio only -> auto subtitle SRT
- Timing QA with `srt_stats.py`
- Burned preview generation with `make_preview_mp4.py`

## Inputs To Collect First

1. Audio path (`wav`, `mp3`, `m4a`, ...)
2. Whether a reference transcript is available
3. Output SRT path (or output directory)
4. Language hint (`zh`, `en`, ...)
5. Preferred run style: CLI, GUI, or Python API

## Decision Rule

- If transcript exists, run Mode A (`align_to_srt.py --text ...`).
- If transcript does not exist, run Mode B via GUI or Python API (`run_auto_subtitle_pipeline`).

## Workflow

1. Validate environment and paths.
2. Choose Mode A or Mode B by transcript availability.
3. Run subtitle generation from packaged scripts.
4. Run timing diagnostics (`srt_stats.py`).
5. If needed, render a preview mp4 with burned subtitles.

## Resolve Skill Script Path

Set a local variable to your installed skill directory.

Codex default path:

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/audio-srt-workflow"
```

OpenClaw/ClawHub install path example:

```bash
SKILL_DIR="<your-workdir>/skills/audio-srt-workflow"
```

## Environment Checks

Run these checks before execution:

```bash
python3 --version
ffmpeg -version
python3 -c "import faster_whisper; print('ok')"
```

If `faster-whisper` import fails:

```bash
# Review dependencies before installing:
cat "$SKILL_DIR/scripts/requirements.txt"
pip install -r "$SKILL_DIR/scripts/requirements.txt"
```

## Mode A Command Template (Audio + Transcript)

```bash
python3 "$SKILL_DIR/scripts/align_to_srt.py" \
  --audio "<input_audio>" \
  --text "<transcript_txt>" \
  --output "<output_srt>" \
  --model small \
  --language zh
```

## Mode B Command Template (Audio Only)

GUI:

```bash
python3 "$SKILL_DIR/scripts/gui_app.py"
```

Or use Python API in scripts:

- Build config with `build_alignment_config(...)`
- Run `run_auto_subtitle_pipeline(...)`

See command details in `references/command-templates.md`.

## QA And Preview

Timing stats:

```bash
python3 "$SKILL_DIR/scripts/srt_stats.py" --srt "<output_srt>"
```

Preview video:

```bash
python3 "$SKILL_DIR/scripts/make_preview_mp4.py" \
  --audio "<input_audio>" \
  --srt "<output_srt>" \
  --output "<preview_mp4>"
```

## Output Conventions

- Default output uses `.srt` extension.
- Prefer dated naming for batch runs (for example `output_YYYYMMDD.srt`).
- Keep intermediate checks in a separate folder from final delivery files.

## Notes

- For Chinese output (`zh`), the pipeline strips commas/periods only.
- If timings look off, inspect waveform snap related arguments before changing model size.
- This skill requires explicit invocation (`allow_implicit_invocation: false`).
