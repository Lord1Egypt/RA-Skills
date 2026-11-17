---
name: galdr
description: OpenClaw skill for using galdr's ARC workflow to turn local audio files into grounded, time-ordered listening-experience prompts backed by timed audio-derived proxies for pattern, attention, heard pressure, surface balance/evidence, harmony, melody, overtones, and silence/re-entry structure, plus report-level pulse evidence. These are interpretation cues, not measured listener responses. Use when asked to analyze a song, explain what makes a track work structurally, generate a listening experience.
version: "0.8.0"
author: Sellemain
license: MIT-0
platforms: [linux, macos]
---
# galdr

Use this skill when an OpenClaw agent needs to analyze music from a local audio file and produce a grounded listening-experience prompt from measurable audio structure.

galdr is a music perception CLI for AI agents. Its default workflow is **ARC**: analyze a track into time-ordered listener-state traces, then assemble those traces into a prompt for grounded listening-experience prose. The metrics are evidence. The ARC prompt is the main user-facing output.

## Important: skill vs CLI

Current OpenClaw CLI install command:

```bash
openclaw skills install galdr
```

ClawHub may display an owner-qualified command such as `openclaw skills install @sellemain/galdr`. As of OpenClaw `2026.6.8`, the released CLI expects the bare skill slug `galdr`.

Installing this skill teaches OpenClaw how to use galdr. It does **not** install the `galdr` command itself.

This skill packaging revision is 0.8.0 and targets the separately installed galdr CLI 0.8.0. The skill is licensed MIT-0; the CLI remains MIT-licensed.

The PyPI wheel contains the runtime CLI/library and bundled prompt templates. The OpenClaw skill is distributed separately through ClawHub so agent instructions can stay a clean skill artifact instead of being installed as Python package data.

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
- analyze a local audio recording
- describe what makes a track work structurally
- generate a grounded listening experience
- create an evidence packet for another model to write from

Do not use galdr for:
- general music trivia
- ordinary recommendation lists
- pretending the metrics prove private emotional intent
- acquiring source media; the caller supplies a local audio file

## OpenClaw agent contract

Prefer the ARC path unless the user explicitly asks for raw metrics, debugging, or agent-internal traces.

Default sequence:
1. Confirm the supplied local audio file is readable.
2. Run `galdr listen` to generate listener-state traces.
3. Assemble the ARC prompt with `--template arc`.
4. Review the prompt.
5. Write the listening experience yourself or pass the prompt to the requested model.

The stream is evidence. Walk the track through time before summarizing. Do not invent emotional claims that the structure does not support.

When a user wants to configure another agent or project to use Galdr, point them to `docs/AGENT-ONBOARDING.md` and `examples/agent/AGENTS.md`. Those files contain the public, copy-pasteable agent instruction path.

Use the ARC prompt family when the user asks for a specific reading mode:

```bash
galdr assemble my-track --template arc-family --lens sound > sound.txt
galdr assemble my-track --template arc-family --lens dance > dance.txt
galdr assemble my-track --template arc-family --lens meaning > meaning.txt
galdr assemble my-track --template arc-family --lens structure > structure.txt
galdr assemble my-track --template arc-family --lens classical > classical.txt
galdr assemble my-track --template arc-family --lens ritual > ritual.txt
```

Lens guide:
- `default` — general public listening page
- `sound` — sound as physical shape, pressure, density, space, body, and motion
- `dance` — movement contract: groove, repetition, build/drop, and bodily use
- `structure` — compact mechanical/form witness
- `meaning` — human situation carried by sound
- `classical` — instrumental/classical/large-form attention over time
- `ritual` — private ritual reading with weak-fit boundary behavior

## Core Workflows

### Local audio file → ARC prompt

```bash
galdr listen "audio/track.flac" --name my-track
galdr assemble my-track --template arc > prompt.txt
```

Galdr does not download audio, videos, lyrics, or captions. `galdr doctor` checks the local Python and ffmpeg/ffprobe setup. Existing analysis and manually supplied background can still be read; legacy lyric and visual fields are ignored.

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
- `galdr assemble <slug>`

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
jq '.stream[0:12]' analysis/my-track/my-track_stream.json
jq '.summary' analysis/my-track/my-track_perception.json
galdr assemble my-track > prompt.txt
```

### Send the ARC prompt to another model

Only do this if the operator explicitly wants model-written prose. Review the assembled ARC prompt before piping it to `claude`, `llm`, or any other external model endpoint.

```bash
galdr assemble my-track --template arc | claude
galdr assemble my-track --template arc | llm
```

### Optional Python agent pattern

```python
from galdr import listen

analysis = listen("audio/track.flac", name="my-track")
prompt = analysis.to_prompt(template="arc")
# Review prompt before sending it to an external model.
```

### Context and template inputs

Assembly includes audio-derived evidence by default. For repeatable supplied metadata,
background, or custom data, use `--context-file notes.json`; the JSON object is labeled
as caller-supplied, not Galdr measurement. For one-off work, combine context with the
assembled output in your agent. Use `--template path/to/prompt.md` for custom prompt
instructions. Do not quietly promote supplied claims to audio evidence.

`--template arc` prepends the default listening-experience rules: tone, format, interpretation bounds, and the instruction to walk the track through time. `--template arc-family --lens <name>` uses the shared prompt-family base plus one deliberate reading lens. Omit templates only when you want a raw data block.

## Interpreting galdr output

ARC is the default output path. The metrics exist to keep that prose grounded: use them as evidence for what changes, returns, releases, locks, or breaks over time.

See [references/metrics.md](references/metrics.md) for full metric reference.

**Quick read:**
- `pattern` near 1.0 → little detected disruption; lower values → more beat/spectral/energy disruption, not proof of a listener’s state
- `surface_balance` negative → harmonic-side energy dominant; positive → percussive-side energy dominant. HPSS balance does not identify voice or instruments; confirm heard sources by listening.
- This signed rule applies to stream/ARC and `surface_balance_signed`; legacy report/catalog `surface_balance` is an unsigned percussive fraction.
- `chroma_motion_semantics: absolute_cosine_distance_v1` marks absolute adjacent-frame motion; untagged older values were track-relative and must not be compared directly.
- `pitch_grid` is 12-class chroma concentration, not tuning accuracy; `overtone_fit` combines matched-slot coverage and closeness, not purity.
- `harmonic_pull` is normalized to each track’s own peak; read local movement, not absolute dissonance or cross-track tension.
- Pressure summary shares count active `pressure_state` labels, excluding silence states/flags and unknown; ARC spans use a coarser classifier.
- Top-level stream `pressure_state` and active-frame summary percentages → pressure-motion labels; nested `surface_evidence.pressure_state` describes thin/held/pressurized surface texture instead
- `pattern_breaks` is a typed event list (`time`/`type`); clustered candidate breaks or silences near the end may support a release reading after audio confirmation
- `silences` carry `start`/`end`/`duration`/relative `depth_db`; `silence_reentries` separately carry `post_attention`/`recovered`. These are algorithmic candidates, not proof of listener re-lock

## Writing ARC experience prose yourself

When writing experience prose yourself from galdr evidence, prefer `galdr assemble <slug> --template arc`. If you are writing from raw assembled output without the template:
- First-person listener perspective, present tense
- Timestamps only at structural pivots: silences, pattern breaks, major energy shifts
- Translate metrics; describe what they mean, do not quote numbers
- LUFS/pressure values are evidence, not prose; write “pressure comes forward / holds / releases / empties”
- Body anchors such as chest, jaw, sternum sparingly; two or three for the whole piece
- End at the final sound event; no aftermath, no reflection
- Around 800 words, no section headers

## Other commands

```bash
galdr doctor                           # inspect local audio decoder health
galdr catalog                          # local analysis index (operator tooling)
galdr catalog --track NAME             # summary card for one track
```
