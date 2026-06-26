---
name: Burmese Audio Understanding
description: High-accuracy Burmese audio transcription using Gemini 3.1 Flash Preview.
---

# Burmese Audio Understanding Skill

This skill allows you to transcribe Burmese audio (voice notes, speech) directly into Burmese text using your own Google Gemini API key. It uses the official Google GenAI SDK for secure and reliable file handling.

## Required Environment Variables
- `GEMINI_API_KEY`: Required. Set your Google Gemini API key to allow the skill to access transcription services.

## Usage

Ensure `GEMINI_API_KEY` is set in your environment, then run:

```bash
node scripts/transcribe-direct.js /path/to/my-audio.ogg
```

## Features
- **Official SDK:** Uses the official `@google/genai` SDK.
- **Improved Security:** No shell commands (ffmpeg/child_process) used; file processing is handled via SDK file upload directly to Gemini.
- **Model:** Uses `gemini-3.1-flash-preview` for high-quality audio transcription.

## Security Notes
- This skill sends audio data to Google Gemini API for transcription.
- No data is stored locally after processing.
- Requires a valid GEMINI_API_KEY with minimal permissions.

## Prerequisites
- Dependencies must be installed: `npm install @google/genai`.
