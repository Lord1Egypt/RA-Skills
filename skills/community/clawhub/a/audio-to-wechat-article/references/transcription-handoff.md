# Transcription Handoff

## Goal
Connect audio transcription output into the article-writing flow cleanly.

## Recommended source of truth
Use the transcript text file, not raw subtitle timing, as the main writing input.

## Preferred upstream workflow
Run transcription with the existing meeting-minutes workflow first.

Example:

```bash
python3 skills/meeting-minutes-whisper/scripts/transcribe_and_minutes.py <audio.m4a> --language Chinese --model tiny --output-dir ./outgoing
```

For first-pass workflow validation, prefer `tiny` or `base` so the end-to-end pipeline closes faster. Upgrade to a larger model only when transcript quality is the bottleneck.

This usually gives:
- transcript `.txt`
- subtitles `.srt`
- draft minutes `.md`

## What to pass downstream
For article generation, prefer:
1. transcript `.txt`
2. draft minutes `.md` as support context
3. optional screenshots / QR code image path

## Rule
Do not write directly from raw audio assumptions. Always write from transcript or cleaned notes.
