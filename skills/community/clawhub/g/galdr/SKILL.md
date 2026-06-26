---
name: galdr
description: OpenClaw skill for using galdr's ARC workflow to turn YouTube URLs or local audio files into grounded, time-ordered listening-experience prompts backed by listener-state traces: pattern, attention, pulse, heard pressure, surface balance/evidence, harmony, melody, overtones, and silence/re-entry structure. Use when asked to analyze a song, explain what makes a track work structurally, generate a listening experience, compare tracks, or extract video frames from a music video.
version: "0.5.1"
author: Sellemain
license: MIT
platforms: [linux, macos]
---
# galdr

Use this skill when an OpenClaw agent needs to analyze music from a YouTube URL or local audio file and produce a grounded listening-experience prompt from measurable audio structure.

galdr is a music perception CLI for AI agents. Its default workflow is **ARC**: analyze a track into time-ordered listener-state traces, then assemble those traces into a prompt for grounded listening-experience prose. The metrics are evidence. The ARC prompt is the main user-facing output.

## Important: skill vs CLI

Current OpenClaw CLI install command:

```bash
openclaw skills install galdr
```

ClawHub may display an owner-qualified command such as `openclaw skills install @sellemain/galdr`. As of OpenClaw `2026.6.8`, the released CLI expects the bare skill slug `galdr`.

Installing this skill teaches OpenClaw how to use galdr. It does **not** install the `galdr` command itself.

Before starting:

```bash
galdr --version
```

If missing, install the CLI from a trusted source:

```bash
pip install galdr

# or from source:
git clone https://github.com/sellemain/galdr.git
cd galdr
pip install -e .
```

Preferred trusted sources:
- PyPI: <https://pypi.org/project/galdr/>
- Source: <https://github.com/sellemain/galdr>

If provenance matters, verify the PyPI metadata or install from the source repository before running it.

## When to use this skill

Use galdr when the user asks to:
- analyze a song or music video
- describe what makes a track work structurally
- generate a grounded listening experience
- compare two tracks
- extract frames around structural moments in a music video
- create an evidence packet for another model to write from

Do not use galdr for:
- general music trivia
- ordinary recommendation lists
- purely lyrical interpretation without audio structure
- pretending the metrics prove private emotional intent
- downloading copyrighted audio unless the operator has appropriate rights/context

## OpenClaw agent contract

Prefer the ARC path unless the user explicitly asks for raw metrics, comparison, debugging, or agent-internal traces.

Default sequence:
1. Fetch or listen to the track.
2. Analyze it into listener-state traces.
3. Assemble the ARC prompt with `--template arc --mode full`.
4. Review the prompt.
5. Write the listening experience yourself or pass the prompt to the requested model.

The stream is evidence. Walk the track through time before summarizing. Do not invent emotional claims that the structure does not support.

## Core Workflows

### YouTube URL → ARC prompt (most common)

```bash
# Step 1: fetch audio + context (slug auto-derived from title)
galdr fetch "https://youtu.be/..." --analyze

# galdr prints the slug at the end:
#   Slug : artist-song-title
#   Next : galdr assemble artist-song-title --template arc --mode full

# Step 2: assemble the prompt locally
galdr assemble artist-song-title --template arc --mode full > prompt.txt
```

Override auto-derived metadata if needed:

```bash
galdr fetch "https://youtu.be/..." --artist "Oliver Anthony" --title "Rich Men North of Richmond" --analyze
```

If YouTube download behavior is flaky:

```bash
galdr doctor
galdr update-deps
```

`galdr doctor` reports the active Python executable, yt-dlp command/version, ffmpeg/ffprobe, JavaScript runtimes, and impersonation support. `galdr update-deps` upgrades `yt-dlp[default,curl-cffi]` in the same Python environment galdr is using.

### Local file → ARC prompt

> The analysis command is `galdr listen`, not `galdr analyze`.

```bash
galdr listen track.wav --name my-track
galdr assemble my-track --template arc --mode full > prompt.txt
```

### Raw second-by-second analysis (advanced)

Galdr is strongest when read as a **time-ordered listener-state trace**. The stream is the primary evidence. Whole-track interpretation comes after walking the track through time.

Start with:
- `analysis/<slug>/<slug>_stream.json`
- `analysis/<slug>/<slug>_perception.json`
- `docs/PERCEPTION-MODEL.md`

Useful extras:
- `*_harmony_stream.json`
- `*_melody_stream.json`
- `*_overtone_stream.json`
- `*_report.json`
- `galdr assemble <slug> --mode blind`

Reading order:
1. Read `PERCEPTION-MODEL.md` first.
2. Treat `*_stream.json` as the main evidence surface.
3. Walk the track in order.
4. Mark transitions: silence, re-entry, pattern breaks, attention shifts, pressure-state changes, harmonic movement.
5. Translate pressure fields into listening language: comes forward, holds, releases, empties. Do not quote LUFS values in experience prose.
6. Only then compress upward into a larger interpretation.

Do not:
- jump straight to a whole-song mood summary
- treat summary metrics as more important than the stream
- ignore silence/re-entry structure
- overclaim emotional certainty from structure alone
- quote loudness/LUFS readings as if they were the experience

Minimal recipe:

```bash
galdr listen track.wav --name my-track
jq '.[0:12]' analysis/my-track/my-track_stream.json
jq '.summary' analysis/my-track/my-track_perception.json
galdr assemble my-track --mode blind > prompt.txt
```

### Send the ARC prompt to another model

Only do this if the operator explicitly wants model-written prose. Review the assembled ARC prompt before piping it to `claude`, `llm`, or any other external model endpoint.

```bash
galdr assemble my-track --template arc --mode full | claude
galdr assemble my-track --template arc --mode full | llm
```

### Optional Python agent pattern

```python
import subprocess, re

fetch = subprocess.run(
    ["galdr", "fetch", url, "--analyze"],
    capture_output=True, text=True, check=True
)
slug = re.search(r"Slug\s*:\s*(\S+)", fetch.stdout).group(1)

prompt = subprocess.run(
    ["galdr", "assemble", slug, "--template", "arc", "--mode", "full"],
    capture_output=True, text=True, check=True
).stdout

# Review prompt before sending it to any external model endpoint.
```

### Mode and template flags

| Mode | What's included |
|------|----------------|
| `full` (default) | metrics + lyrics + background + frames |
| `lyrics` | metrics + lyrics |
| `context` | metrics + background |
| `blind` | metrics only (structural, no cultural context) |

`--template arc` prepends the default listening-experience rules: tone, format, interpretation bounds, and the instruction to walk the track through time. Omit it only when you want a raw data block.

## Interpreting galdr output

ARC is the default output path. The metrics exist to keep that prose grounded: use them as evidence for what changes, returns, releases, locks, or breaks over time.

See [references/metrics.md](references/metrics.md) for full metric reference.

**Quick read:**
- `pattern` near 1.0 → listener is locked; near 0 → constant disruption
- `surface_balance` negative → harmonic dominant (warm, tonal); positive → percussive dominant
- `pressure_state` and pressure summary percentages → heard-pressure shape across the track
- Clustered `pattern_breaks` at the end → planned release; distributed → varied structure
- `silence` depth below -60dB with re-lock above 0.93 attention → structured withdrawal/return

## Writing ARC experience prose yourself

When writing experience prose yourself from galdr evidence, prefer `galdr assemble <slug> --template arc --mode full`. If you are writing from raw assembled output without the template:
- First-person listener perspective, present tense
- Timestamps only at structural pivots: silences, pattern breaks, major energy shifts
- Translate metrics; describe what they mean, do not quote numbers
- LUFS/pressure values are evidence, not prose; write “pressure comes forward / holds / releases / empties”
- Body anchors such as chest, jaw, sternum sparingly; two or three for the whole piece
- End at the final sound event; no aftermath, no reflection
- Around 800 words, no section headers

## Other commands

```bash
galdr compare track-a track-b          # side-by-side structural comparison
galdr frames slug                      # extract + describe video frames at structural moments
galdr fetch "url" --no-download        # context only (Wikipedia + lyrics), no audio
galdr fetch "url" --censor             # sanitize explicit lyrics before saving
galdr doctor                           # inspect yt-dlp/media runtime health
galdr update-deps                      # upgrade yt-dlp reliability extras
galdr catalog                          # list all indexed tracks
galdr catalog --track NAME             # summary card for one track
```
