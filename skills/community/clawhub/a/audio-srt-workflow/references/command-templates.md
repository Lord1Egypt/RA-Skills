# Command Templates

Set skill path first:

```bash
# Codex default:
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/audio-srt-workflow"
# OpenClaw/ClawHub example:
# SKILL_DIR="<your-workdir>/skills/audio-srt-workflow"
```

## Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
# Review dependencies first:
cat "$SKILL_DIR/scripts/requirements.txt"
pip install -r "$SKILL_DIR/scripts/requirements.txt"
```

## Mode A (Audio + Transcript)

```bash
python3 "$SKILL_DIR/scripts/align_to_srt.py" \
  --audio "input.wav" \
  --text "transcript.txt" \
  --output "output.srt" \
  --model small \
  --language zh
```

## Mode A With Date Suffix

```bash
python3 "$SKILL_DIR/scripts/align_to_srt.py" \
  --audio "input.wav" \
  --text "transcript.txt" \
  --output "output.srt" \
  --date-suffix
```

## Mode B (Audio Only, GUI)

```bash
python3 "$SKILL_DIR/scripts/gui_app.py"
```

## Quality Check

```bash
python3 "$SKILL_DIR/scripts/srt_stats.py" --srt "output.srt"
python3 "$SKILL_DIR/scripts/srt_stats.py" --srt "output.srt" --warn-duration 8 --warn-gap 0.8
```

## Preview Video

```bash
python3 "$SKILL_DIR/scripts/make_preview_mp4.py" \
  --audio "input.wav" \
  --srt "output.srt" \
  --output "preview_check.mp4"
```
