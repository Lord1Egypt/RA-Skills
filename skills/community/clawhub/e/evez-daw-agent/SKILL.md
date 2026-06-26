---
name: evez-daw-agent
description: Autonomous music generation DAW — breakcore, dubstep, phonk, 404 architecture. Synthesizes drums, bass, and FX from pure code. Voice sample chopping and machine voice synthesis. No samples needed.
---

# EVEZ DAW Agent

Fast autonomous music generation engine with voice manipulation.

## What It Does

- **Synthesizes drums** from scratch: kicks, snares, hats, claps, rimshots
- **5 bass engines**: Sub, Reese, Wobble, Phonk 808, Scream
- **7 FX**: Distortion, Bitcrush, Reverb, Delay, Lowpass, Highpass, Formant
- **5 beat presets**: Breakcore 170, Dubstep 140, Phonk 130, Amen Break, 404 Architecture 200
- **Voice chopping**: Load any audio, chop, rearrange, distort, bitcrush
- **Machine voice synthesis**: Formant-based vowel synthesis, gear grind, digital flow
- **Drumkit generator**: Auto-generate full kits as WAV files

## Quick Start

```bash
python3 evez_daw.py --port 9112
```

## API

- `POST /api/render` — Generate a full track
- `POST /api/drumkit` — Generate drumkit WAV files
- `POST /api/chop` — Chop and rearrange audio
- `GET /api/presets` — List presets
- `GET /api/health` — Health check

## Cost

$0 — all synthesis is local, no API calls.
