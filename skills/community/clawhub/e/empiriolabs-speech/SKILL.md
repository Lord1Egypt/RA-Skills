---
name: empiriolabs-speech
description: Turn text into natural speech with EmpirioLabs AI and save the audio file (MP3, WAV, and other formats). Use when the user asks to read text aloud, create a voiceover, narration, or audio version of a script, or try different voices and languages. Runs a bundled Python script that picks a text-to-speech model from the live catalog (or the one you name) and saves the audio to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Text to speech with EmpirioLabs AI
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
      - text-to-speech
      - voiceover
      - empiriolabs
    related_skills:
      - empiriolabs-transcribe
      - empiriolabs-models
required_environment_variables:
  - name: EMPIRIOLABS_API_KEY
    prompt: EmpirioLabs AI API key (starts with sk-empiriolabs-)
    help: "Create a key at https://platform.empiriolabs.ai/dashboard/api-keys"
    required_for: every request to the EmpirioLabs AI API
---

# EmpirioLabs AI text to speech

Turn text into speech with the [EmpirioLabs AI](https://empiriolabs.ai) speech API. The bundled script picks a voice model, requests the audio, and saves the file.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Speak a line of text

```bash
python3 scripts/speech.py "Welcome to the weekly product update." --out ./audio/welcome.mp3
```

The file extension in `--out` selects the audio format when the model offers it (`.mp3`, `.wav`, `.ogg`, `.flac`). The script prints a JSON summary:

```json
{
  "model": "tts-2",
  "files": ["/home/me/project/audio/welcome.mp3"],
  "urls": ["https://media.empiriolabs.ai/..."]
}
```

Some models return the audio directly, in which case `urls` is empty and the saved file is the only copy.

## Longer scripts, voices, and languages

```bash
python3 scripts/speech.py --text-file ./script.txt --voice Olivia --out ./audio/narration.wav
python3 scripts/speech.py "Bonjour et bienvenue." --language fr-FR --out ./audio/bonjour.mp3
python3 scripts/speech.py --list-voices --model tts-2
```

Each model has a per-request text limit (for example 2,000 characters). The script stops with a clear message when the text is longer; split long scripts at sentence boundaries and generate one file per part.

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model, for example `tts-2` or `qwen-audio-3-0-tts`. |
| `--voice NAME` | Voice for the chosen model. See `--list-voices`. |
| `--language CODE` | Language or locale, for example `en-US`, on models that accept it. |
| `--format FMT` | Audio format such as `mp3` or `wav`. Default: taken from `--out`. |
| `--speed X` | Speaking rate on models that accept it (`1.0` is normal). |
| `--text-file PATH` | Read the text from a UTF-8 file. |
| `--param key=value` | Any other model parameter, for example `--param temperature=0.8`. |
| `--out PATH` | File or directory to save to (default: current directory). |
| `--overwrite` | Replace an existing file. By default a numeric suffix is added instead. |

## Choose a model and check prices

```bash
python3 scripts/speech.py --list-models
```

Speech is billed by characters or tokens at the model's listed price. `*` marks the model used when `--model` is omitted. For a model's voices, formats, and limits, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments or text over the model's limit.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.
