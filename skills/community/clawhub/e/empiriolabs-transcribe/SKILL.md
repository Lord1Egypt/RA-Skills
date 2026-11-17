---
name: empiriolabs-transcribe
description: Transcribe audio or video files to text with EmpirioLabs AI, from an https URL or a local file. Use when the user asks for a transcript of a recording, meeting, interview, podcast, voice note, or video, wants speaker-labeled text, or needs the spoken words as text for notes, summaries, or captions. Runs a bundled Python script that picks a transcription model from the live catalog (or the one you name) and waits for the result.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Transcribe audio and video with EmpirioLabs AI
  openclaw:
    primaryEnv: EMPIRIOLABS_API_KEY
    requires:
      env:
        - EMPIRIOLABS_API_KEY
      anyBins:
        - python3
        - python
    envVars:
      - name: EMPIRIOLABS_API_KEY
        required: true
        description: "EmpirioLabs AI API key (starts with sk-empiriolabs-). Create one at https://platform.empiriolabs.ai/dashboard/api-keys"
    homepage: https://empiriolabs.ai
  hermes:
    tags:
      - transcription
      - speech-to-text
      - empiriolabs
    related_skills:
      - empiriolabs-speech
      - empiriolabs-models
required_environment_variables:
  - name: EMPIRIOLABS_API_KEY
    prompt: EmpirioLabs AI API key (starts with sk-empiriolabs-)
    help: "Create a key at https://platform.empiriolabs.ai/dashboard/api-keys"
    required_for: every request to the EmpirioLabs AI API
---

# EmpirioLabs AI transcription

Turn speech in an audio or video file into text with the [EmpirioLabs AI](https://empiriolabs.ai) transcription API. Transcription runs as a job: the bundled script submits the file, waits, and prints the transcript.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Transcribe a file

```bash
python3 scripts/transcribe.py https://example.com/interview.mp3
python3 scripts/transcribe.py ./recordings/meeting.m4a --out ./notes/meeting.txt
```

The source can be an https URL to an audio or video file, or a local file, which the script uploads. Without `--out`, the transcript is printed to stdout. With `--out`, it is saved (a `.json` path saves the full result, including timing data where the model returns it) and a JSON summary is printed:

```json
{
  "model": "whisper-large-v3-turbo",
  "job_id": "...",
  "file": "/home/me/project/notes/meeting.txt",
  "characters": 5321
}
```

## Speakers, languages, and full results

```bash
python3 scripts/transcribe.py https://example.com/panel.mp4 --model deepgram-nova-3 --diarize --out ./panel.json
python3 scripts/transcribe.py ./voice-note.ogg --language es
python3 scripts/transcribe.py ./call.wav --json        # full result with segments and words
```

## Long recordings

```bash
python3 scripts/transcribe.py https://example.com/webinar.mp3 --no-wait   # prints the job id
python3 scripts/transcribe.py --job-id JOB_ID --out ./webinar.txt           # waits, then saves
```

If `--timeout` (default 1800 seconds) runs out, the job keeps running. The script exits with code 3 and prints the `--job-id` command that resumes it.

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model, for example `whisper-large-v3-turbo` or `deepgram-nova-3`. |
| `--language CODE` | Spoken language hint, for example `en`, on models that accept it. |
| `--diarize` | Label speakers, on models that support it. |
| `--param key=value` | Any other model parameter, for example `--param smart_format=true`. |
| `--out PATH` | Save the transcript (`.txt`) or the full result (`.json`). |
| `--json` | Print the full result as JSON instead of plain text. |
| `--no-wait` / `--job-id ID` | Submit and return, then resume later. |

## Choose a model and check prices

```bash
python3 scripts/transcribe.py --list-models
```

Transcription is billed by audio length at the model's listed price. `*` marks the model used when `--model` is omitted. For a model's options, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments or a missing file, `3` still running when `--timeout` ran out.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing. `HTTP 413`: the upload is too large; pass an https URL to the file instead.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.
