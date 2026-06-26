---
name: french-learning
description: "French vocab automation. Formats Excel vocab to Google Sheet, generates ElevenLabs audio, uploads to Drive. Triggers: process french vocab, generate audio, French Excel file."
metadata: {"clawdbot":{"emoji":"🇫🇷","requires":{"bins":["sag","gog","gemini"],"env":["GEMINI_API_KEY","ELEVENLABS_API_KEY"]},"primaryEnv":"GEMINI_API_KEY"}}
---

# French Learning Skill

This skill automates the creation of French learning materials.

## Resource Locations
- **Configuration**: Refer to [references/config.md](references/config.md) for target Google Sheet and Drive Folder IDs.
- **Scripts**: Automation logic resides in `scripts/`.

## Prerequisites
1.  **Google Sheet Setup**: Ensure you have access to the target Google Sheet: `https://docs.google.com/spreadsheets/d/1Nnwv4DbbUgfiNDiJdgCvnyxH6oPBis_99fm-2voehl4`.
2.  **Google Drive Folder**: You must provide a Google Drive Folder ID where the generated audio files will be saved.
3.  **ElevenLabs API Key**: The `ELEVENLABS_API_KEY` environment variable must be set to use the `sag` TTS skill for audio generation.

## Standard Workflows

### 1. Format Excel to Google Sheet
`scripts/format_excel.py` — Reads source Sheet, calls Gemini for Chinese translation + example sentences, writes 6 columns (`Index`, `Fr Original`, `En Translation`, `Chinese Translation`, `Example Sentence (FR)`, `Example Sentence (CN)`) into target Sheet, then applies **wrap text** (`wrapStrategy: WRAP`) to all cells so long sentences stay within the cell.

### 2. Generate & Upload Audio
`scripts/generate_audio.py` — Fetches `Example Sentence (FR)` + `Index`, chunks into batches of 20, generates MP3 via ElevenLabs (`sag` skill), uploads to specified Drive folder named `1-20.mp3`, `21-40.mp3`, etc. Requires Drive Folder ID.
