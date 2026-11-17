---
name: empiriolabs-music
description: Generate music and sound effects with EmpirioLabs AI from a text description, with optional lyrics on models that sing, wait for the result, and save the audio file. Use when the user asks to compose a song, a backing track, a jingle, or a film score, to create a sound effect or ambience, or to check on an audio job that is still running. Runs a bundled Python script that picks a model from the live catalog (or the one you name) and saves the file to the path you choose.
license: MIT-0
compatibility: Requires Python 3.8 or later, network access to api.empiriolabs.ai, and an EmpirioLabs AI API key in the EMPIRIOLABS_API_KEY environment variable.
metadata:
  author: EmpirioLabs AI
  version: "1.0.0"
  short-description: Generate music and sound with EmpirioLabs AI
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
      - music-generation
      - sound-effects
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

# EmpirioLabs AI music and sound generation

Make music and sound effects from a description with the [EmpirioLabs AI](https://empiriolabs.ai) audio generation API. The bundled script submits the request, waits until the audio is ready, and saves the file. To read text aloud, use the `empiriolabs-speech` skill instead.

## Setup

1. Create an API key at https://platform.empiriolabs.ai/dashboard/api-keys. Keys start with `sk-empiriolabs-`.
2. Make the key available as `EMPIRIOLABS_API_KEY` in the environment where commands run. Never paste the key into a prompt or a file in the project.
3. Python 3.8 or later. There is nothing to install.

Script paths below are relative to this skill's folder. On Windows, use `python` instead of `python3`.

## Make a track

```bash
python3 scripts/music.py "an upbeat synthwave track with a driving bassline" --duration 30 --out ./audio/track.mp3
```

The file extension in `--out` selects the audio format when the model offers it (`.mp3`, `.wav`, `.flac`, `.ogg`). The script prints progress to stderr, then a JSON summary:

```json
{
  "model": "MODEL_ID",
  "job_id": "...",
  "files": ["/home/me/project/audio/track.mp3"],
  "urls": ["https://media.empiriolabs.ai/..."]
}
```

## Sing lyrics

On models that take lyrics, pass them as text or from a file:

```bash
python3 scripts/music.py "a gentle folk song with acoustic guitar" --lyrics-file ./lyrics.txt --out ./audio/song.mp3
```

## Make a sound effect

Choose a sound effect model with `--list-models`, then describe the sound:

```bash
python3 scripts/music.py "footsteps on gravel, then a door closing" --model MODEL_ID --duration 5 --out ./audio/steps.wav
```

## Long jobs

```bash
python3 scripts/music.py "a film score that swells slowly" --no-wait     # prints the job id
python3 scripts/music.py --job-id JOB_ID --out ./audio/score.mp3          # waits, then downloads
```

If `--timeout` (default 1800 seconds) runs out, the job keeps running. The script exits with code 3 and prints the `--job-id` command that resumes it.

## Options

| Option | Meaning |
|---|---|
| `--model ID` | Use a specific model. |
| `--lyrics TEXT` / `--lyrics-file FILE` | Lyrics to sing, on models that take them. |
| `--duration N` | Length in seconds. Supported values depend on the model. |
| `--param key=value` | Any other model parameter, for example `--param seed=7`. |
| `--out PATH` | File or directory to save to (default: current directory). |
| `--no-wait` | Submit the job, print its id, and exit. |
| `--job-id ID` | Wait for an earlier job and download its result. |
| `--no-download` | Print the hosted URL without saving the file. |
| `--overwrite` | Replace an existing file. By default a numeric suffix is added instead. |

## Choose a model and check prices

Audio is billed per generated second or per request, depending on the model. Check before long runs, and confirm costly runs with the user:

```bash
python3 scripts/music.py --list-models
```

`*` marks the model used when `--model` is omitted. For a model's durations, formats, and other parameters, use the `empiriolabs-models` skill (`models.py --show MODEL_ID`).

## Exit codes and errors

- `0` success, `1` the request failed (the message says why), `2` invalid arguments, `3` still running when `--timeout` ran out.
- `HTTP 401`: the key is missing or invalid. `HTTP 402`: add credits at https://platform.empiriolabs.ai/dashboard/billing.

## Other ways to connect

The same models are available through the EmpirioLabs AI remote MCP server at `https://mcp.empiriolabs.ai/mcp` (OAuth sign-in, or the API key as a bearer token). Setup: https://docs.empiriolabs.ai/mcp. API reference: https://docs.empiriolabs.ai.
