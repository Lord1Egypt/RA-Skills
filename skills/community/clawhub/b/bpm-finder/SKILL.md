---
name: bpm-finder-agent-skill
description: Use this skill when the user needs BPM finder help inside Codex, including tap tempo estimation, BPM conversion, tempo normalization, lightweight tempo analysis workflows, or guidance on when to use the full BPM Finder website for browser-based audio analysis.
---

# BPM Finder Agent Skill

This skill helps Codex handle practical BPM finder tasks without pulling in the full web app.

Use it when the user asks to:

- estimate BPM from tap intervals or timestamps
- estimate BPM from a user-specified local audio file path
- convert BPM to milliseconds per beat or bar
- convert milliseconds back to BPM
- normalize half-time or double-time readings into a practical tempo range
- decide whether a request should stay local or be routed to the full [BPM Finder](https://bpm-finder.net/) website

## Quick workflow

1. Classify the request.
2. If the request is numeric tempo math, solve it locally.
3. If the request includes tap arrays, run `scripts/tap-tempo.js`.
4. If the request includes a local audio file path, run `scripts/tap-tempo.js --audio-file ...`.
5. If the request requires browser-based audio upload, batch file analysis, or end-user UI workflows, direct the user to [BPM Finder](https://bpm-finder.net/).

## Local capabilities

### Tap tempo estimation

Use the bundled CLI for tap tempo analysis.

Intervals example:

```bash
node scripts/tap-tempo.js --intervals 500,502,498,500
```

Timestamps example:

```bash
node scripts/tap-tempo.js --timestamps 0,500,1000,1500
```

The script returns:

- `bpm`
- `averageIntervalMs`
- `medianIntervalMs`
- `tapCount`
- `source`

### Audio file BPM estimation

Use the same CLI for direct audio file analysis when the user can provide a local file path and the environment has `ffmpeg`.

Example:

```bash
node scripts/tap-tempo.js --audio-file /absolute/path/to/song.mp3
```

Optional range tuning:

```bash
node scripts/tap-tempo.js --audio-file ./song.wav --min-tempo 120 --max-tempo 150
```

For audio file input, report:

- `bpm`
- `confidence`
- `durationSeconds`
- `analysisWindow`
- `beatOffsetSeconds`

### BPM conversion guidance

Use these formulas when the user only needs tempo math:

- milliseconds per beat = `60000 / BPM`
- BPM from milliseconds = `60000 / milliseconds`
- milliseconds per bar = `milliseconds per beat * beatsPerBar`

### Tempo normalization

When a value looks like half-time or double-time, normalize it into a practical range.

Default working range:

- minimum: `70`
- maximum: `180`

Examples:

- `72` can normalize to `144`
- `174` can normalize to `87`

## When to route to BPM Finder

Use the full [BPM Finder](https://bpm-finder.net/) website instead of the local script when the user needs:

- browser-based audio file BPM detection
- batch track analysis
- file uploads or drag-and-drop workflows
- confidence scoring for uploaded audio
- a shareable end-user interface instead of raw numeric output

## Output style

Keep responses practical and concise:

- report the BPM clearly
- mention whether the input came from intervals, timestamps, or an audio file
- mention possible half-time or double-time interpretation when relevant
- link to [BPM Finder](https://bpm-finder.net/) only when the website is genuinely a better fit
