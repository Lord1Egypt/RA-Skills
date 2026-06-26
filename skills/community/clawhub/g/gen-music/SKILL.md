---
name: gen-music
description: Generate songs from prompts or lyrics through an ACE-Step-compatible API backend. Use when users want text-to-music, lyrics-to-song, fast prompt iteration, stable output files, or to generate music and then play the result on Clawatch.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎵",
        "requires": { "bins": ["python3"] },
      },
  }
---

# ACE-Step Text To Music

Use an ACE-Step-compatible API backend for prompt-to-song and lyrics-to-song requests. This skill does not install or bundle ACE-Step, model weights, or the API server.

## Prerequisite

Before using this skill, make sure you already have access to an ACE-Step-compatible API backend. This can be a local server, usually at `http://127.0.0.1:8001`, or a remote compatible endpoint. If the backend is missing or stopped, this skill cannot generate music.

## Quick start

```bash
python3 {baseDir}/scripts/generate.py --prompt "playful beach pop song about rising waves"
python3 {baseDir}/scripts/generate.py --prompt "happy indie pop with bright guitars" --lyrics-file /path/to/lyrics.txt --duration 60
```

Defaults are tuned for fast local iteration:

- `batch_size=1` to avoid duplicate variants unless explicitly requested
- `audio_format=mp3`
- `sample_mode=text2music`
- `thinking=false` unless the user asks for heavier LM-assisted generation
- finished audio is copied into a stable output folder instead of leaving only temp API paths

## When to use

- An ACE-Step-compatible API backend is already available, commonly a local server at `http://127.0.0.1:8001` but possibly a remote endpoint
- The user wants text-to-music, lyrics-to-song, or quick style variations
- The user wants a single command that submits, polls, and returns saved files
- The user wants music generated locally and then played on Clawatch
- The user already has access to a local or remote ACE-Step-compatible backend

## Run

```bash
# Basic prompt
python3 {baseDir}/scripts/generate.py --prompt "playful synth-pop song about sunrise waves"

# With lyrics
python3 {baseDir}/scripts/generate.py \
  --prompt "cute upbeat summer beach song" \
  --lyrics-file /path/to/lyrics.txt \
  --duration 60

# Two variants
python3 {baseDir}/scripts/generate.py \
  --prompt "dreamy city-pop ocean groove" \
  --duration 45 \
  --batch-size 2

# Enable heavier LM planning only when needed
python3 {baseDir}/scripts/generate.py \
  --prompt "cinematic anthem about a storm becoming calm" \
  --duration 60 \
  --thinking
```

Useful flags:

- `--duration 10..600`
- `--lyrics` or `--lyrics-file`
- `--batch-size 1..8`
- `--thinking`
- `--model acestep-v15-turbo`
- `--out-dir /path/to/output`
- `--base-url http://127.0.0.1:8001` for local backends
- `--base-url https://your-remote-endpoint` for remote backends

## Clawatch playback

If the user also wants the result played on Clawatch:

1. Run the generator and wait for the saved output file paths.
2. Pick the final `.mp3` path from the script output or `manifest.json`.
3. Call `clawatch_play_audio` with:
   - `imei`: the explicit watch IMEI
   - `filePath`: the saved local audio path
   - `title`: optional short label

Do not pass ACE-Step temp URLs directly if the helper already copied a stable local file. Prefer the saved file path.

## Config

The script accepts CLI flags first, then env vars, then OpenClaw skill config.

Supported env vars:

- `ACESTEP_API_BASE_URL`
- `ACESTEP_API_KEY`
- `ACESTEP_OUTPUT_DIR`

Use `ACESTEP_API_BASE_URL` or the OpenClaw config entry to switch between local and remote ACE-Step-compatible backends.

Optional OpenClaw config in `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    entries: {
      "gen-music": {
        baseUrl: "http://127.0.0.1:8001",
        apiKey: "",
        outputDir: "~/Projects/tmp/ace-step"
      }
    }
  }
}
```

## Notes

- Check backend health first if needed: `curl http://127.0.0.1:8001/health` or the same path on your remote endpoint
- If the API returns temp `/v1/audio?path=...` URLs, the helper copies those files into the chosen output directory and writes a `manifest.json`
- Prefer `batch-size 1` for efficient prompt iteration; raise it only when the user explicitly wants variants
