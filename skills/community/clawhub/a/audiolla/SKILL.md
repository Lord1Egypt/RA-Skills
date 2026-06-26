---
name: audiolla
description: HTTP/MCP client for a user-deployed audiolla audio-production server. Use ONLY when the user has explicitly named audiolla AND provided AUDIOLLA_URL (or has it set in the environment). Capabilities: stem separation (Demucs / MDX / BS-Roformer), mastering (matchering reference / pedalboard preset chain), MIR analysis (BPM, key, LUFS, spectral features, beat grid, onset detection, melody contour, structural segmentation via librosa), DSP transforms (gain, EQ, compand, reverb, pitch, tempo via SoX), loudness measurement and normalization, generic effects chains (full pedalboard catalog as ordered chain), multiband compression (LR4 crossovers), transient shaping, sidechain ducking, de-essing, mid/side encode-decode, parametric EQ, panning, stereo width, silence detection and trimming, audio repair (declip + dehum), clip detection, harmonic/percussive separation, time-stretch and pitch-shift, BPM/key matching, pitch correction (auto-tune), beat slicing, audio thumbnail extraction, convolution reverb, static PNG spectrogram/waveform and 8-mode animated MP4/WebM video (ffmpeg), Chromaprint acoustic fingerprinting, AudioSet tagging, CLAP audio embeddings + similarity + zero-shot classification, ID3/Vorbis/FLAC metadata read/write, MIDI composition from JSON spec, MIDI inspection, MIDI transformation (transpose/quantize/tempo/channel-filter), MIDI quantize and humanize, drum pattern generation, MIDI rendering via fluidsynth, polyphonic audio-to-MIDI transcription (Spotify basic-pitch ONNX), chords-to-MIDI conversion, AI audio restoration (de-reverb, de-echo, AI de-noise via UVR/audio-separator), DSP noise reduction, neural speech/vocal enhancement (DeepFilterNet DF3), voice activity detection (silero-vad), speaker diarization (pyannote 3.1), DJ prep (BPM + key + Camelot + LUFS in one call), loop-point detection, curated server-side workflow presets (master-for-spotify, podcast-cleanup, vocal-cleanup) and ad-hoc op pipelines that chain multiple operations server-side. v1.0.0 API is JSON-everywhere: every audio endpoint takes a JSON body; the ONLY multipart route is `PUT /v1/files/{path}` for raw byte uploads. Audio I/O supports two input modes (`file_path` referencing a pre-staged file under FILES_DIR, xor `file_url` — only when the operator has enabled AUDIOLLA_FETCH_MODE) and two output modes (`output_path` writing back to staging, xor `output_url` PUTing to a presigned URL). There is no inline-bytes audio response anywhere — every audio-producing endpoint returns JSON describing where the result landed. Audiolla only fetches/uploads to URLs when the operator has explicitly enabled AUDIOLLA_FETCH_MODE — if a request returns "URL fetch/upload is disabled", do NOT try to bypass it. Do not use this skill for generic audio-processing questions or for users who haven't named audiolla.
compatibility: Requires curl and a running audiolla instance (Docker image psyb0t/audiolla:latest or :latest-cuda). AUDIOLLA_URL env var must be set by the user (default http://localhost:8000). AUDIOLLA_TOKEN required only when the server has AUDIOLLA_AUTH_TOKEN configured; obtain from the AUDIOLLA_TOKEN env var or by asking the user — never read tokens from repo files autonomously.
metadata:
  author: psyb0t
  homepage: https://github.com/psyb0t/docker-audiolla
---

# audiolla

HTTP + MCP client for an audiolla server that the user has already deployed. This skill talks to a running audiolla instance — it does not stand one up, does not download model weights manually, and does not modify the server config on its own initiative.

For installation and setup, see [references/setup.md](references/setup.md).

## Authoritative endpoint reference: `GET /v1/catalog`

This skill documents the most common patterns. The **full, always-current** list of every endpoint is `GET /v1/catalog` (17 categories, ~85 endpoints). Always check the catalog when looking for an operation that isn't shown here — the server is the source of truth, this file is a curated reference.

```bash
# List every endpoint grouped by category
curl $AUDIOLLA_URL/v1/catalog | jq '.categories[] | {name, count: (.endpoints | length)}'

# Find endpoints in one category
curl $AUDIOLLA_URL/v1/catalog | jq '.categories[] | select(.name == "dynamics") | .endpoints'
```

Companion discovery endpoints: `GET /v1/engines` (engines + loaded/idle status), `GET /v1/presets` (curated workflows), `GET /v1/ops` (the ~24 pipeline op slugs).

## When to use this skill

The user has audiolla running and asks you to:
- Pull stems (vocals / drums / bass / etc.) out of a track
- Master a track against a reference recording (matchering) or via preset chain
- **Run a curated workflow** (`master-for-spotify`, `podcast-cleanup`, `vocal-cleanup`) via a single `POST /v1/presets/{name}` call
- **Chain ad-hoc operations server-side** via `POST /v1/pipeline` (no re-upload between steps)
- Get BPM, key, LUFS, duration, or spectral features for a file
- Detect beat grid, onsets, dominant melody, or structural segments
- Detect chords + key (separate from BPM/LUFS)
- Detect or trim silence
- Generate a spectrogram, waveform image, or animated visualisation video
- Compute a Chromaprint acoustic fingerprint
- Apply a DSP chain (gain, EQ, compression, reverb, pitch shift, tempo via SoX OR full pedalboard catalog)
- **Multiband compression** with LR4 crossovers
- **Transient shaping** (punch up drums / cut room tail)
- **De-essing** (split-band sibilance compression)
- **Sidechain ducking** (voiceover-over-music)
- **Mid/Side encode/decode** (for stereo M/S processing)
- **Convolution reverb** (apply a user-supplied IR file)
- **Audio repair** (declip + dehum)
- **Time-stretch + pitch-shift** independently, or **BPM-match / key-match** to a target
- **Pitch-correct** (auto-tune to nearest semitone)
- **Beat-slice** at detected beat positions (returns ZIP of chops)
- **Audio thumbnail** — most-energetic N-second segment
- **HPSS** harmonic/percussive separation
- Measure or normalize integrated LUFS (`/v1/audio/normalize` with `target_lufs`)
- **Loudness curve** — RMS envelope over time (`/v1/audio/loudness/curve`)
- Stage files server-side, then operate on them via `file_path`
- **Tag** audio (AudioSet labels), **embed** (CLAP 512-dim), **classify** (zero-shot label list), **similar** (cosine between two tracks)
- Read or write ID3/Vorbis/FLAC **metadata** (mutagen)
- **DJ-prep** — BPM + key + Camelot + LUFS in one call
- Compose / inspect / transform / render MIDI; **quantize**, **humanize**, **drum patterns**, **chords-to-MIDI**
- Remove reverb / echo / noise via `/v1/audio/restore/{engine}` (UVR)
- DSP noise reduction via `/v1/audio/noise-reduce/{engine}` (DSP or UVR)
- Convert any audio to polyphonic MIDI (basic-pitch)
- **Voice activity detection** (silero-vad — speech/non-speech segments)
- **Speaker diarization** (pyannote 3.1 — who spoke when)
- Enhance speech/vocal recordings (DeepFilterNet DF3)
- **Generate music or SFX from a text prompt** via `/v1/audio/generate/{engine}` — five engines:
  - `stable-audio-open` (Stability Community Licence — commercial OK below revenue threshold; 47 s cap; 44.1 kHz stereo; loops / SFX / textures; instrumental)
  - `musicgen-small` and `musicgen-medium` (Meta MusicGen 300M / 1.5B; **CC-BY-NC 4.0** — server must opt in via `AUDIOLLA_ENABLE_NONCOMMERCIAL=1`; 30 s cap; instrumental)
  - `riffusion` (CreativeML OpenRAIL-M; ~5 s per pass; spectrogram-via-Griffin-Lim; lo-fi character)
  - `audioldm2` (**CC-BY 4.0 — commercial-safe, no opt-in gate**; 30 s cap; 16 kHz mono; general SFX — ambience / foley / impact / animal sounds; slow at default 200-step DDIM, pass `num_inference_steps=50` for ~4x speed)
  All five are CUDA-only. Full-song / lyric-conditioned generation isn't shipped (ACE-Step + DiffRhythm + TangoFlux + Stable Audio Open Small deferred — see the README's "deferred" list). For commercial use, prefer `audioldm2` (CC-BY 4.0) or `stable-audio-open` (Stability Community Licence below the revenue threshold).
- Drive any of the above from an LLM agent over MCP
- **Async-job-and-forget** any audio-producing call via `async_job=true` + optional `webhook_url`
- Send results to a **presigned S3-style PUT URL** via `output_url`

## When NOT to use this skill

- The user hasn't named audiolla — they're asking a general "how do I split stems?" question. Suggest audiolla as an option; don't assume it's running.
- The user wants music generation from a melody-conditioning input (hum-to-track / "make this sound like X"). Audiolla's five generators (`stable-audio-open`, `musicgen-small`, `musicgen-medium`, `riffusion`, `audioldm2`) are text-prompt only; melody conditioning isn't wired. Plain text → music or SFX IS supported — see `/v1/audio/generate/{engine}` in the catalog. The closed-weight Suno / Udio APIs are out of scope.
- The user wants real-time / streaming processing. Demucs needs the whole file.
- The user wants **transcription / ASR / TTS / voice cloning** — that's [docker-talkies](https://github.com/psyb0t/docker-talkies). Note: audiolla DOES have speech-adjacent features (VAD, diarization, neural enhancement) but does NOT transcribe.

## Setup

```bash
export AUDIOLLA_URL=http://localhost:8000
export AUDIOLLA_TOKEN=<the-token-the-user-gives-you>   # only if auth is enabled
```

If `AUDIOLLA_URL` is not set, ask the user — do not search the workspace for it. Same for `AUDIOLLA_TOKEN`: only accept it from the env var the user set or from the user directly. Never read it from `docker-compose.yml`, `.env`, or any other repo file on your own initiative.

**Verify:** `curl $AUDIOLLA_URL/healthz` → `{"ok": true, "device": "...", "engines": [...]}`. `/healthz` is always unauthenticated regardless of `AUDIOLLA_AUTH_TOKEN`.

Auth is optional. If the server has `AUDIOLLA_AUTH_TOKEN` set, every endpoint except `/healthz` requires `Authorization: Bearer $AUDIOLLA_TOKEN`. Without it you get `401`. Always pass the token if the user gave you one; don't assume the server has auth off.

## How it works

v1.0.0 is **JSON-everywhere**. Every audio endpoint takes `Content-Type: application/json` with a JSON body. The ONE exception is `PUT /v1/files/{path}` for raw byte uploads (`application/octet-stream`). Input is `file_path` (pre-staged under FILES_DIR via `PUT /v1/files/{path}`) xor `file_url` (server fetches when `AUDIOLLA_FETCH_MODE` allows). Output for audio-producing endpoints is `output_path` (server writes to FILES_DIR) xor `output_url` (server PUTs to a presigned URL). Both modes return JSON describing where the result landed (`{path,size,...}` or `{url,size,...}`); there is **no inline-bytes audio response** anywhere. Analysis-only endpoints (no audio produced — e.g. `/v1/audio/analyze`, `/v1/audio/beats`, `/v1/audio/fingerprint`) return their JSON data directly and ignore output_path/output_url. The standard flow is: `PUT /v1/files/uploads/track.wav` once, then JSON-body POST to every processing endpoint with `file_path` + `output_path`, chaining the output of one call into the input of the next.

Every error response:

```json
{"detail": "description of what went wrong"}
```

Status codes follow REST conventions:
- `200` — success
- `400` — bad input (unknown engine, invalid features, bad operations JSON, etc.)
- `401` — missing/invalid bearer token (only when auth is enabled)
- `404` — unknown engine slug, unknown file path
- `413` — upload exceeded `AUDIOLLA_MAX_UPLOAD_BYTES` (default 200 MB)
- `415` — unsupported `output_format`
- `500` — server error (engine failed internally, etc.)

## Engines

| Slug | What it does | Notes |
|------|--------------|-------|
| `htdemucs` | 4-stem separation | drums, bass, other, vocals |
| `htdemucs_ft` | 4-stem fine-tuned | **CUDA-only at usable speed** — flagged `cuda_only`, the server rejects it with 400 on CPU |
| `htdemucs_6s` | 6-stem separation | adds `guitar` + `piano` (experimental, CPU OK but slow) |
| `mdx_extra` | 4-stem MDX-Net | drums, bass, other, vocals — strong vocal isolation |
| `matchering` | Reference-based mastering | GPL v3 |
| `pedalboard-chain` | Preset DSP mastering chain | presets: `transparent`, `loud` — GPL v3 |
| `librosa-analyze` | MIR analysis + loudness | BPM, key, LUFS, spectral, beat grid, onsets, melody (pyin), segments; backs `/v1/audio/{analyze,beats,onsets,melody,segments,loudness}` |
| `sox-transform` | SoX DSP chain | gain, EQ, compand, reverb, pitch, tempo, rate, channels, trim, pad |
| `fx-chain` | Arbitrary pedalboard chain | full pedalboard catalog as `[{type, params}, ...]` — backs `/v1/audio/fx`. VST3 / AU / external-plugin classes deliberately blocked |
| `midi-compose` | JSON → MIDI; inspect/transform | song-spec transcoder + MIDI reader/editor; backs `/v1/midi/{compose,inspect,transform,generate}` |
| `midi-render` | MIDI → audio | fluidsynth + FluidR3_GM SoundFont (GM patches 0-127, drum kit on channel 9) |
| `silence-detect` | Silence detection + trimming | ffmpeg `silencedetect`; backs `/v1/audio/silence` |
| `ffmpeg-render` | Spectrogram / waveform / video | static PNG + 8-mode animated MP4/WebM; backs `/v1/audio/visualize/image/{spectrogram,waveform}` + `/v1/audio/visualize/video/{mode}` |
| `audio-fingerprint` | Chromaprint fingerprint | `fpcalc` subprocess; backs `/v1/audio/fingerprint` |
| `uvr-dereverb` | AI de-reverb | BS-Roformer (SDR 19+); backs `/v1/audio/restore/uvr-dereverb` |
| `uvr-deecho` | AI de-echo (normal + aggressive) | VR Architecture; `aggressive=true` enables hard mode (`uvr-deecho-aggressive` slug is gone — consolidated into this engine); backs `/v1/audio/restore/uvr-deecho` |
| `uvr-denoise` | AI de-noise | MelBand Roformer (SDR 28); backs `/v1/audio/restore/uvr-denoise` + `/v1/audio/noise-reduce/uvr-denoise` |
| `uvr-karaoke` | Karaoke (remove lead vocals) | MelBand Roformer; returns Instrumental stem |
| `uvr-vocal-bsr` | High-quality vocal/inst separation | BS-Roformer (SDR 13) — stems: Vocals, Instrumental |
| `basic-pitch` | Polyphonic audio-to-MIDI transcription | Spotify basic-pitch ONNX; backs `/v1/audio/to_midi/basic-pitch` |
| `deepfilter` | Neural speech/vocal enhancement | DeepFilterNet DF3; backs `/v1/audio/enhance/deepfilter` |
| `noise-reduce` | DSP spectral noise reduction | noisereduce — backs `/v1/audio/noise-reduce/noise-reduce` (stationary/non-stationary modes, no GPU) |
| `chord-detect` | Chord progression + key | Krumhansl-Schmuckler + chroma template matching; backs `/v1/audio/chords`, `/v1/audio/chords-to-midi`, `/v1/audio/key-match` |
| `silero-vad` | Voice activity detection | speech/non-speech timestamps; backs `/v1/audio/vad` |
| `pyannote` | Speaker diarization | pyannote/speaker-diarization-3.1 — backs `/v1/audio/diarize` (requires `HUGGINGFACE_TOKEN`) |
| `stretch` | Time-stretch + pitch-shift | librosa phase vocoder; backs `/v1/audio/stretch`, `/v1/audio/bpm-match`, `/v1/audio/key-match` |
| `ast-tag` | AudioSet zero-shot labels | Audio Spectrogram Transformer; backs `/v1/audio/tag` |
| `clap-embed` | CLAP embeddings + similarity + classification | LAION CLAP 512-dim; backs `/v1/audio/embed`, `/v1/audio/similar`, `/v1/audio/classify` |
| `hpss` | Harmonic/percussive split | librosa median-filter HPSS; backs `/v1/audio/separate/hpss` |
| `metadata` | ID3 / Vorbis / FLAC tag read+write | mutagen; backs `/v1/audio/metadata` |

Engines lazy-load on first use and auto-unload after `AUDIOLLA_ENGINE_TTL` seconds of idle (default 600s). Demucs weights prefetch into `/data/torch_cache/` at container start so the first separation request doesn't pay the cold-download cost.

Use `GET /v1/engines` to confirm what's actually configured on the running server (operators can restrict via `AUDIOLLA_ENABLED_ENGINES`).

## Output formats

Any endpoint that produces audio accepts `"output_format": "<fmt>"` in the JSON body. Supported: `wav` (default), `mp3`, `flac`, `opus`, `aac`, `pcm`. The server transcodes via ffmpeg — the `output_path` extension does not determine the encoding.

## API Reference

### Health & engine listing

```bash
# Liveness — no auth required
curl $AUDIOLLA_URL/healthz
# {"ok": true, "device": "cpu", "engines": ["htdemucs", "matchering", ...]}

# Configured engines + capabilities
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" $AUDIOLLA_URL/v1/engines

# Engines currently loaded in memory (and how idle)
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" $AUDIOLLA_URL/v1/ps

# Evict one engine
curl -X DELETE -H "Authorization: Bearer $AUDIOLLA_TOKEN" $AUDIOLLA_URL/v1/ps/htdemucs

# Evict everything
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" $AUDIOLLA_URL/v1/unload
```

### Stem separation

`POST /v1/audio/separate` — JSON body. Result is one staged file (single-stem) or a ZIP of stems written to `output_path`.

```bash
# Stage the input once (only multipart route in the whole API)
curl -X PUT -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/octet-stream' \
  --data-binary @track.wav \
  $AUDIOLLA_URL/v1/files/uploads/track.wav

# Single stem → JSON {path,size,...} pointing at the staged stem
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/separate \
  -d '{"file_path":"uploads/track.wav","engine":"htdemucs","stems":["vocals"],"output_path":"stems/vocals.wav"}'

# Multiple stems → ZIP at output_path
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/separate \
  -d '{"file_path":"uploads/track.wav","engine":"htdemucs","stems":["vocals","drums"],"output_path":"stems/vocals_drums.zip"}'

# Omit stems → all stems for that engine (ZIP)
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/separate \
  -d '{"file_path":"uploads/track.wav","engine":"htdemucs","output_path":"stems/all.zip"}'

# MP3 output
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/separate \
  -d '{"file_path":"uploads/track.wav","engine":"htdemucs","stems":["vocals"],"output_format":"mp3","output_path":"stems/vocals.mp3"}'
```

Required: `file_path` (xor `file_url`), `engine`, and one of `output_path`/`output_url`. Optional: `stems` (array; default = all stems for that engine), `output_format` (default `wav`).

Loading a separation engine evicts other loaded engines first — Demucs is memory-hungry and the operator-default setup runs one engine in memory at a time.

### Mastering

`POST /v1/audio/master` — `mode=reference` uses matchering against a reference track; `mode=chain` runs a pedalboard preset.

```bash
# Reference-based mastering — both inputs pre-staged
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/master \
  -d '{"file_path":"uploads/track.wav","mode":"reference","reference_path":"uploads/ref.wav","output_path":"out/mastered.wav"}'

# Pedalboard chain — preset is REQUIRED (transparent or loud)
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/master \
  -d '{"file_path":"uploads/track.wav","mode":"chain","preset":"loud","output_path":"out/mastered.wav"}'

# Pedalboard chain with explicit loudness target
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/master \
  -d '{"file_path":"uploads/track.wav","mode":"chain","preset":"transparent","target_lufs":-14,"output_path":"out/mastered.wav"}'
```

Required: `file_path` (xor `file_url`), `mode`, and one of `output_path`/`output_url`. `mode=reference` requires `reference_path` (xor `reference_url`). `mode=chain` requires `preset` (`transparent` or `loud`). Optional: `target_lufs` (range `[-70.0, -0.1]`), `output_format`.

Streaming-target LUFS reference values: Spotify `-14`, Apple Music `-16`, YouTube `-14`, broadcast EBU R128 `-23`.

### MIR analysis

`POST /v1/audio/analyze` — analysis-only, returns JSON. No output_path/output_url.

```bash
# Specific features
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/analyze \
  -d '{"file_path":"uploads/track.wav","features":["bpm","key","loudness"]}'

# Omit features → returns all of them
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/analyze \
  -d '{"file_path":"uploads/track.wav"}'
```

Valid `features` values: `bpm`, `key`, `loudness`, `duration`, `spectral_centroid`, `rms`, `zcr`.

> **Common mistake:** the feature for integrated LUFS is `loudness`, NOT `lufs`. Asking for `features=["lufs"]` returns 400.

### Beat detection (`/v1/audio/beats`)

Returns the estimated BPM and beat timestamps. Optionally writes a click-track WAV to `output_path`.

```bash
# Beat grid only — analysis JSON
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/beats \
  -d '{"file_path":"uploads/track.wav"}'
# {"bpm": 128.0, "beats": [0.0, 0.469, 0.938, ...], "engine": "librosa-analyze"}

# With a click track — output_path is REQUIRED when click_track=true
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/beats \
  -d '{"file_path":"uploads/track.wav","click_track":true,"output_path":"beats/click.wav"}'
# → JSON with beat grid PLUS the staged click track path
```

Optional params: `click_track` (bool, default false) — when true, writes the click WAV to `output_path` / `output_url`. `hop_length` (int, default 512) — analysis hop size in samples.

### Onset detection (`/v1/audio/onsets`)

Returns note/transient onset timestamps in seconds. Analysis-only, returns JSON.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/onsets \
  -d '{"file_path":"uploads/track.wav"}'
# {"onsets": [0.023, 0.512, 1.034, ...], "count": 42, "engine": "librosa-analyze"}
```

Optional: `backtrack` (bool, default false) — snap onsets to preceding energy valley. `hop_length`, `delta` for tuning sensitivity.

### Melody extraction (`/v1/audio/melody`)

Estimates the dominant melody using pyin pitch tracking. Returns Hz per frame.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/melody \
  -d '{"file_path":"uploads/track.wav"}'
# {"melody": [{"time": 0.0, "hz": 440.1}, {"time": 0.023, "hz": null}, ...], ...}

# Export the melody as a single-track MIDI file (output_path REQUIRED when as_midi=true)
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/melody \
  -d '{"file_path":"uploads/track.wav","as_midi":true,"output_path":"melody/lead.mid"}'
```

`hz` is `null` for unvoiced frames. Optional: `as_midi` (bool) — generates MIDI from the contour and writes to `output_path` / `output_url`; `fmin`/`fmax` to constrain pitch range.

### Structural segmentation (`/v1/audio/segments`)

Finds recurring sections (verse, chorus, bridge…) using a recurrence matrix. Returns labels A, B, C…

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/segments \
  -d '{"file_path":"uploads/track.wav","num_segments":4}'
# {"segments": [{"label":"A","start_sec":0.0,"end_sec":32.5},
#               {"label":"B","start_sec":32.5,"end_sec":65.0}, ...]}
```

Optional: `num_segments` (int, default 4). Short inputs (fewer beats than `num_segments`) return a single `A` span with a `note` field explaining the fallback.

### Silence detection and trimming (`/v1/audio/silence`)

Finds silent gaps via ffmpeg `silencedetect`. Optionally trims them.

```bash
# Detect only — analysis JSON, no audio produced
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/silence \
  -d '{"file_path":"uploads/track.wav","threshold_db":-30,"min_duration_sec":1.0}'
# {"silent_ranges": [...], "non_silent_ranges": [...], "duration": 215.3}

# Trim all silence → trimmed audio staged
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/silence \
  -d '{"file_path":"uploads/track.wav","threshold_db":-30,"min_duration_sec":0.5,"trim_mode":"all","output_path":"proc/trimmed.wav"}'

# Trim only edges
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/silence \
  -d '{"file_path":"uploads/track.wav","threshold_db":-40,"min_duration_sec":0.3,"trim_mode":"edges","output_path":"proc/trimmed.wav"}'
```

`threshold_db` must be ≤ 0. `trim_mode`: `edges` (leading + trailing only), `all` (every detected gap). Without `trim_mode`, response is JSON only — no audio produced. With `trim_mode` set, `output_path` (or `output_url`) is required and the response JSON points at the trimmed file.

### Spectrogram (`/v1/audio/visualize/image/spectrogram`)

Static PNG spectrogram via ffmpeg `showspectrumpic`. PNG is written to `output_path` / `output_url`.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/visualize/image/spectrogram \
  -d '{"file_path":"uploads/track.wav","width":1280,"height":720,"output_path":"viz/spec.png"}'
```

Optional: `width`, `height` (64–8192, defaults 1920×1080), `color` (default `intensity`), `scale` (default `log`).

### Waveform (`/v1/audio/visualize/image/waveform`)

Static PNG waveform via ffmpeg `showwavespic`. PNG is written to `output_path` / `output_url`.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/visualize/image/waveform \
  -d '{"file_path":"uploads/track.wav","width":1920,"height":240,"output_path":"viz/wave.png"}'
```

Optional: `width`, `height` (64–8192, defaults 1920×320), `color` (default `lime`).

### Animated visualisation (`/v1/audio/visualize/video/{mode}`)

Animated MP4 or WebM video from one of 8 ffmpeg filter modes. Video is written to `output_path` / `output_url`.

```bash
# `mode` is in the URL path
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/visualize/video/spectrum \
  -d '{"file_path":"uploads/track.wav","width":1280,"height":720,"fps":30,"container":"mp4","output_path":"viz/spectrum.mp4"}'
```

`mode` options (URL path segment): `spectrum` (scrolling FFT), `waves` (oscilloscope), `cqt` (constant-Q transform), `freqs` (bar-graph), `volume` (VU meter), `vectorscope` (stereo X/Y), `phasemeter`, `histogram`. `container`: `mp4` (default) or `webm`. `fps` 1–120.

### Acoustic fingerprint (`/v1/audio/fingerprint`)

Chromaprint fingerprint via `fpcalc`. The base64 string is AcoustID-compatible. Analysis-only — no output_path.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/fingerprint \
  -d '{"file_path":"uploads/track.wav"}'
# {"duration": 215.34, "fingerprint": "AQADtEqRRIuQ..."}

# Include the raw integer array
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/fingerprint \
  -d '{"file_path":"uploads/track.wav","return_raw":true}'
# adds "fingerprint_raw": [12345, 67890, ...]
```

Optional: `analyze_seconds` (default 120 — AcoustID standard; pass 0 to fingerprint the whole file), `return_raw` (bool).

### DSP transform chain

`POST /v1/audio/transform` — applies an array of SoX operations in order.

```bash
# Pitch shift up 2 semitones, then add reverb
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/transform \
  -d '{
    "file_path":"uploads/track.wav",
    "operations":[
      {"op":"pitch","params":{"n_semitones":2}},
      {"op":"reverb","params":{"reverberance":50,"room_scale":80}}
    ],
    "output_format":"wav",
    "output_path":"out/transformed.wav"
  }'

# Trim first 30s, pad 2s silence at end, gain -3dB
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/transform \
  -d '{
    "file_path":"uploads/track.wav",
    "operations":[
      {"op":"trim","params":{"start_time":0,"end_time":30}},
      {"op":"pad","params":{"end_duration":2}},
      {"op":"gain","params":{"db":-3}}
    ],
    "output_path":"out/trimmed.wav"
  }'
```

`operations` is a JSON array of `{"op": "<name>", "params": {...}}`. Order matters — ops apply left-to-right.

**Ops and their params:**

| op | required params | optional params | what it does |
|----|-----------------|-----------------|--------------|
| `gain` | `db` (float) | | gain in dB |
| `equalizer` | `frequency`, `gain_db` | `width_q` (default 1.0) | peaking EQ |
| `compand` | | `attack_time`, `decay_time`, `soft_knee_db`, `tf_points` ([[in_db, out_db], ...]) | dynamic range compression |
| `reverb` | | `reverberance` (0-100, default 50), `pre_delay_ms` (default 0), `room_scale` (default 100) | reverb |
| `pitch` | `n_semitones` (float) | | pitch shift in **semitones**, not cents |
| `tempo` | `factor` (float) | | tempo factor (1.5 = 1.5x faster, 0.5 = half speed) |
| `rate` | `samplerate` (int) | | resample |
| `channels` | `n_channels` (int) | | mix to N channels |
| `trim` | `start_time` (float, sec) | `end_time` (float, sec; null = end of file) | trim |
| `pad` | | `start_duration`, `end_duration` (both floats, sec) | pad silence |

Unknown ops return 400 with the valid list.

### Loudness

`POST /v1/audio/loudness` — analysis-only. Returns integrated LUFS as JSON. Use `/v1/audio/normalize` (separate endpoint) for actual normalization.

```bash
# Measure
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/loudness \
  -d '{"file_path":"uploads/track.wav"}'
# {"loudness_lufs": -16.3}

# Normalize to -14 LUFS (streaming target). Result is staged audio.
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/normalize \
  -d '{"file_path":"uploads/track.wav","target_lufs":-14,"output_path":"out/normalized.wav"}'
# → {"path":"out/normalized.wav","size":...,"measured_lufs":-16.3,"target_lufs":-14,...}
```

`target_lufs` must be in `[-70.0, -0.1]` — outside that range returns 400 (anything closer to 0 will clip catastrophically; anything below -70 silences the audio).

### Effects chain (`/v1/audio/fx`)

Arbitrary pedalboard effect chain — full catalog. Different from `/v1/audio/master` (which runs presets).

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/fx \
  -d '{
    "file_path":"uploads/track.wav",
    "effects":[
      {"type":"Compressor","params":{"threshold_db":-18,"ratio":4.0}},
      {"type":"Reverb","params":{"room_size":0.5,"wet_level":0.3}},
      {"type":"PitchShift","params":{"semitones":2}},
      {"type":"Gain","params":{"gain_db":-3}}
    ],
    "output_path":"out/fx.wav"
  }'
```

Allowed `type` values: `Compressor`, `Limiter`, `NoiseGate`, `Gain`, `Clipping`, `Distortion`, `Bitcrush`, `Reverb`, `Chorus`, `Delay`, `Phaser`, `PitchShift`, `HighShelfFilter`, `LowShelfFilter`, `PeakFilter`, `HighpassFilter`, `LowpassFilter`, `LadderFilter`, `IIRFilter`, `GSMFullRateCompressor`, `MP3Compressor`, `Resample`, `Invert`, `Convolution`.

`VST3Plugin`, `AudioUnitPlugin`, `ExternalPlugin` are deliberately blocked — they load arbitrary native code from arbitrary filesystem paths. Server returns 400 if asked.

### MIDI composition (`/v1/midi/compose`)

Transcode a JSON song spec to a Standard MIDI File. **No AI runs server-side** — your agent writes the spec, audiolla turns it into MIDI bytes staged at `output_path`.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/compose \
  -d '{
    "output_path":"midi/song.mid",
    "spec":{
      "tempo_bpm": 120,
      "time_signature": [4, 4],
      "key_signature": "C",
      "tracks": [
        {"name":"Lead","program":0,"channel":0,"notes":[
          {"pitch":60,"start_beats":0.0,"duration_beats":0.5,"velocity":100},
          {"pitch":64,"start_beats":0.5,"duration_beats":0.5,"velocity":100},
          {"pitch":67,"start_beats":1.0,"duration_beats":0.5,"velocity":100}
        ]},
        {"name":"Drums","program":0,"channel":9,"notes":[
          {"pitch":36,"start_beats":0.0,"duration_beats":0.1,"velocity":110}
        ]}
      ]
    }
  }'
```

Spec fields (inside the `spec` object):

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `tempo_bpm` | float | 120 | 1.0 ≤ bpm ≤ 999.0 |
| `time_signature` | `[num, den]` | `[4, 4]` | denominator must be 1/2/4/8/16/32 |
| `key_signature` | string | none | `"C"`, `"Am"`, `"F#"`, `"Bbm"` — letter [+ #/b] [+ m for minor] |
| `ticks_per_beat` | int | 480 | 24 ≤ tpb ≤ 1920 |
| `tracks[].name` | string | none | optional, writes a `track_name` meta event |
| `tracks[].program` | int 0-127 | 0 | General MIDI program (Acoustic Grand Piano = 0, Distortion Guitar = 30, Synth Brass 1 = 62, etc.) |
| `tracks[].channel` | int 0-15 | 0 | **Channel 9 is the GM drum channel** — pitch maps to drum kit, not piano |
| `tracks[].volume` | int 0-127 | 100 | MIDI CC#7 — initial volume |
| `tracks[].pan` | int 0-127 | 64 | MIDI CC#10 — initial pan (64 = centre) |
| `tracks[].notes[].pitch` | int 0-127 | required | 60 = middle C |
| `tracks[].notes[].start_beats` | float ≥ 0 | 0 | beat-based absolute position |
| `tracks[].notes[].duration_beats` | float > 0 | required | must be > 1/64 beat (≈ a 256th note) |
| `tracks[].notes[].velocity` | int 1-127 | 100 | |

GM drum kit reference for channel 9: 35 acoustic bass drum, 36 kick, 38 snare, 39 hand clap, 40 electric snare, 42 closed hi-hat, 46 open hi-hat, 49 crash, 51 ride, 57 crash 2.

Spec validation is fail-loud — bad pitch / negative duration / unknown program returns a 400 with the offending path in the message (e.g. `tracks[1].notes[3].pitch must be in [0, 127], got 200`).

One of `output_path` / `output_url` is required — the staged MIDI is then referenced via `file_path` on any subsequent MIDI call.

### MIDI inspection (`/v1/midi/inspect`)

Read the structure of any Standard MIDI File. Analysis-only, returns JSON.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/inspect \
  -d '{"file_path":"midi/song.mid"}'
# {
#   "type": 1, "ticks_per_beat": 480, "length_seconds": 16.0,
#   "tempo_changes": [{"tick": 0, "bpm": 120.0}],
#   "time_signatures": [{"tick": 0, "numerator": 4, "denominator": 4}],
#   "tracks": [
#     {"index": 1, "name": "Lead", "note_on_count": 32,
#      "channels": [0], "programs": [0], "length_beats": 8.0},
#     ...
#   ],
#   "track_count": 3, "size_bytes": 1024
# }
```

Non-MIDI input returns 400 with `"MThd"` mentioned in the detail.

### MIDI transformation (`/v1/midi/transform`)

Modify an existing MIDI file. Result is staged at `output_path` / `output_url`.

```bash
# Transpose all non-drum tracks up an octave
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/transform \
  -d '{"file_path":"midi/song.mid","transpose_semitones":12,"output_path":"midi/transposed.mid"}'

# Override tempo to 140 BPM
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/transform \
  -d '{"file_path":"midi/song.mid","tempo_bpm":140,"output_path":"midi/fast.mid"}'

# Drop the drum channel
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/transform \
  -d '{"file_path":"midi/song.mid","drop_channels":[9],"output_path":"midi/no-drums.mid"}'

# Keep only channels 0 and 1
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/transform \
  -d '{"file_path":"midi/song.mid","keep_channels":[0,1],"output_path":"midi/two-ch.mid"}'

# Quantize to 1/16th notes (0.25 beats)
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/transform \
  -d '{"file_path":"midi/song.mid","quantize":0.25,"output_path":"midi/quantized.mid"}'
```

Transform params (all optional — omit for a no-op):

| Param | Type | Notes |
|-------|------|-------|
| `transpose_semitones` | int ±48 | Shifts all non-drum (non-ch9) pitches. Out-of-range notes after shift are dropped (not clipped). |
| `tempo_bpm` | float 1–999 | Replaces all `set_tempo` events. |
| `quantize` | float > 0 | Beat grid in beats (0.25 = 1/16th at 4/4). Snaps note starts; note-off shifts by the same delta to preserve duration. |
| `keep_channels` | int array (0–15) | Whitelist — drop all other channels. Mutually exclusive with `drop_channels`. |
| `drop_channels` | int array (0–15) | Blacklist — drop only these channels. Mutually exclusive with `keep_channels`. |

Supplying both `keep_channels` and `drop_channels` returns 400.

### MIDI rendering (`/v1/midi/render`)

Synthesise MIDI to audio via fluidsynth. Default SoundFont is FluidR3_GM (bundled in the prod image). Override per-request with a staged `.sf2`.

```bash
# Render a staged MIDI to staged audio
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/render \
  -d '{"file_path":"midi/song.mid","output_format":"wav","output_path":"audio/song.wav"}'

# Render with a custom SoundFont (stage it first)
curl -X PUT -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/octet-stream' \
  --data-binary @my.sf2 \
  $AUDIOLLA_URL/v1/files/sf/orchestral.sf2
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/render \
  -d '{"file_path":"midi/song.mid","soundfont_path":"sf/orchestral.sf2","output_format":"flac","gain":0.3,"samplerate":48000,"output_path":"audio/orch.flac"}'
```

`gain` range `[0.0, 5.0]` — default `0.5` is calibrated to avoid clipping on percussive MIDI. `samplerate` must be 22050 / 44100 / 48000 / 88200 / 96000.

### MIDI generate (`/v1/midi/generate`)

One-shot compose + render. Body has the same `spec` field as `/v1/midi/compose` plus audio knobs (`output_format`, `soundfont_path`, `gain`, `samplerate`). Result audio is staged at `output_path` / `output_url`.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/midi/generate \
  -d '{
    "output_format":"wav",
    "output_path":"songs/v1.wav",
    "spec":{"tempo_bpm":120,"tracks":[{"channel":0,"notes":[
      {"pitch":60,"start_beats":0,"duration_beats":1,"velocity":100}
    ]}]}
  }'
```

### File staging

A simple server-side file store under `/v1/files`. **This is the only multipart-ish route in the API** — the body is raw bytes (`application/octet-stream`). Plain CRUD: upload, list, download, delete. Once a file is staged, every audio endpoint references it by relative path via the `file_path` field in its JSON body.

```bash
# Upload (path can have subdirectories: uploads/bands/myband/track.wav)
curl -X PUT -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/octet-stream' \
  --data-binary @track.wav \
  $AUDIOLLA_URL/v1/files/uploads/mytrack.wav

# Use the staged path on any audio call
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/separate \
  -d '{"file_path":"uploads/mytrack.wav","engine":"htdemucs","stems":["vocals"],"output_path":"stems/mytrack-vocals.wav"}'
# → {"path":"stems/mytrack-vocals.wav","size":...,"engine":"htdemucs","stem":"vocals","output_format":"wav"}

# List
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" $AUDIOLLA_URL/v1/files

# Download (raw bytes — Content-Type matches the stored file)
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  $AUDIOLLA_URL/v1/files/uploads/mytrack.wav -o copy.wav

# Delete
curl -X DELETE -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  $AUDIOLLA_URL/v1/files/uploads/mytrack.wav
```

Path traversal (`..`, leading `/`, etc.) is rejected with 400. Symlinks are not followed. Size cap is `AUDIOLLA_MAX_UPLOAD_BYTES`.

### Input and output modes (every audio endpoint)

Every audio endpoint accepts exactly one of two input forms — supplying zero or both returns 400:

- `file_path` — relative path under FILES_DIR (pre-staged via `PUT /v1/files/{path}`)
- `file_url` — remote URL the server fetches (subject to the `AUDIOLLA_FETCH_MODE` policy — see below)

Audio-producing endpoints (separate, master, transform, normalize, fx, restore, enhance, visualize, midi compose/transform/render/generate, melody-as-midi, beats-with-click-track, etc.) require exactly one of:

- `output_path` — server writes the result to `FILES_DIR / <path>`; response is JSON `{path, size, ...}`
- `output_url` — server PUTs the result to a presigned URL; response is JSON `{url, size, ...}`

`output_path` and `output_url` are mutually exclusive — supplying both is 400. Supplying neither is 400 too (no inline-bytes audio response exists in v1.0.0) — except when `async_job=true`, which auto-stages to `jobs/{job_id}.{ext}` if neither is set.

Analysis-only endpoints (`/v1/audio/analyze`, `/v1/audio/onsets`, `/v1/audio/fingerprint`, `/v1/audio/loudness`, beats without `click_track`, silence without `trim_mode`, etc.) ignore `output_path` / `output_url` — they return their JSON data directly.

The master endpoint additionally accepts `reference_path` xor `reference_url` for the reference track in `mode=reference` — same exactly-one-of rule.

### Remote URLs (file_url / output_url)

The server-side URL fetch is **disabled by default**. To enable it, the operator sets:

```
AUDIOLLA_FETCH_MODE = disabled | allowlist | denylist     (default: disabled)
AUDIOLLA_FETCH_HOSTS = comma-separated host patterns       (required when mode=allowlist)
AUDIOLLA_FETCH_SCHEMES = https,http                        (default: https only)
AUDIOLLA_FETCH_TIMEOUT = 30s                               (per fetch/upload)
AUDIOLLA_FETCH_ALLOW_PRIVATE = false                       (allow private/loopback IPs)
AUDIOLLA_FETCH_MAX_REDIRECTS = 5
```

Host patterns are exact match (`bucket.s3.amazonaws.com`) or single-wildcard subdomain (`*.s3.amazonaws.com`, matches any `<x>.s3.amazonaws.com` but NOT `s3.amazonaws.com` itself).

Always-on protections regardless of mode:
- DNS-resolved private / loopback / link-local / metadata-service IPs (`169.254.169.254`) rejected unless `AUDIOLLA_FETCH_ALLOW_PRIVATE=true`
- Only schemes in `AUDIOLLA_FETCH_SCHEMES` accepted; `file://`, `gopher://`, etc. always rejected
- Each redirect's `Location` re-validated through the full policy before following
- Body streamed; abort if it exceeds `AUDIOLLA_MAX_UPLOAD_BYTES`

If you're scripting and the server returns `URL fetch/upload is disabled` (400), tell the user — don't try to bypass it. The operator chose `disabled` for a reason.

Example — fetch from S3, master, PUT to a presigned URL:

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/master \
  -d '{
    "file_url":"https://my-bucket.s3.amazonaws.com/track.wav",
    "mode":"chain",
    "preset":"loud",
    "output_url":"https://my-bucket.s3.amazonaws.com/mastered.wav?X-Amz-Signature=..."
  }'
# → {"url":"...","size":...,"engine":"pedalboard-chain","mode":"chain","output_format":"wav"}
```

## MCP

audiolla exposes a Model Context Protocol server at `/v1/mcp` using the streamable HTTP transport. Same auth as REST — pass `Authorization: Bearer $AUDIOLLA_TOKEN`.

The MCP contract mirrors REST: every audio tool requires exactly one of `file_path` or `file_url` for input (same `AUDIOLLA_FETCH_MODE` policy as REST), and every audio-producing tool requires exactly one of `output_path` or `output_url` for output. There is **no inline-base64 audio mode** — v1.0.0 dropped every base64 audio/MIDI/image/video response field that existed in v0.23.x because LLMs can't consume raw bytes anyway, and large base64 payloads choke the context window. Every audio-producing tool returns either `{path, size, output_format}` (when `output_path` is set) or `{url, size, output_format}` (when `output_url` is set). The `separate` tool takes `output_urls` as a per-stem dict when uploading each stem to its own presigned URL.

| Tool | Inputs | Output |
|------|--------|--------|
| `list_engines` | — | engine catalog with `loaded` flag |
| `separate` | `engine`, `stems`, `file_path` or `file_url`, `output_path` or `output_url` or `output_urls: {stem: url}` | `{path, size}` / `{url, size}` / `{uploaded_stems: {stem: {url, size}}}` |
| `master` | `mode`, `file_path` or `file_url`, `reference_path` or `reference_url` (mode=reference), `preset` (mode=chain), `target_lufs`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `analyze` | `file_path` or `file_url`, `features` | librosa feature dict |
| `beats` | `file_path` or `file_url`, `click_track`, `hop_length`, `output_path` or `output_url` (only when `click_track=true`) | `{bpm, beats, ...}` (+ click track `{path}` / `{url}` if `click_track=true`) |
| `onsets` | `file_path` or `file_url`, `backtrack`, `hop_length`, `delta` | `{onsets, count, ...}` |
| `melody` | `file_path` or `file_url`, `as_midi`, `fmin`, `fmax`, `output_path` or `output_url` (only when `as_midi=true`) | `{melody: [{time, hz}, ...], ...}` (+ MIDI `{path}` / `{url}` if `as_midi=true`) |
| `segments` | `file_path` or `file_url`, `num_segments` | `{segments: [{label, start_sec, end_sec}, ...]}` |
| `silence` | `file_path` or `file_url`, `threshold_db`, `min_duration_sec`, `trim_mode`, `output_path` or `output_url` (only when `trim_mode` set) | `{silent_ranges, non_silent_ranges, duration, ...}` (+ trimmed audio `{path}` / `{url}` if `trim_mode` set) |
| `spectrogram` | `file_path` or `file_url`, `width`, `height`, `color`, `scale`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `waveform` | `file_path` or `file_url`, `width`, `height`, `color`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `visualize` | `file_path` or `file_url`, `mode`, `width`, `height`, `fps`, `container`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `fingerprint` | `file_path` or `file_url`, `analyze_seconds`, `return_raw` | `{duration, fingerprint, fingerprint_raw?}` |
| `transform` | `operations`, `file_path` or `file_url`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `loudness` | `file_path` or `file_url`, `target_lufs`, `output_path` or `output_url` | measurement JSON (no target) or `{path or url, size, measured_lufs, target_lufs, normalized}` |
| `fx` | `effects`, `file_path` or `file_url`, `output_format`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `midi_compose` | `spec` (song JSON), `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `midi_inspect` | `file_path` or `file_url` (MIDI) | `{type, ticks_per_beat, tempo_changes, tracks, ...}` |
| `midi_transform` | `file_path` or `file_url` (MIDI), `transpose_semitones`, `tempo_bpm`, `quantize`, `keep_channels`, `drop_channels`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `midi_render` | `file_path` or `file_url` (MIDI), `soundfont_path`, `gain`, `samplerate`, `output_format`, `output_path` or `output_url` | `{path, size}` or `{url, size}` |
| `midi_generate` | `spec`, `soundfont_path`, `gain`, `samplerate`, `output_format`, `output_path` or `output_url` | `{path, size, midi_size}` or `{url, size, midi_size}` |
| `dereverb` | `file_path` or `file_url`, `engine`, `output_format`, `output_path` or `output_url` | `{path, size, engine, output_format}` or `{url, size, engine, output_format}` |
| `deecho` | `file_path` or `file_url`, `engine`, `output_format`, `output_path` or `output_url` | `{path, size, engine, output_format}` or `{url, size, engine, output_format}` |
| `denoise` | `file_path` or `file_url`, `engine`, `output_format`, `output_path` or `output_url` | `{path, size, engine, output_format}` or `{url, size, engine, output_format}` |
| `audio_to_midi` | `file_path` or `file_url`, `engine`, `onset_threshold`, `frame_threshold`, `minimum_note_length_ms`, `minimum_frequency`, `maximum_frequency`, `multiple_pitch_bends`, `melodia_trick`, `output_path` or `output_url` | `{path, size, engine}` or `{url, size, engine}` |
| `enhance` | `file_path` or `file_url`, `engine`, `output_format`, `output_path` or `output_url` | `{path, size, engine, output_format}` or `{url, size, engine, output_format}` |
| `list_files` | — | `{files: [...]}` |
| `put_file` | `path`, the file body as base64 (small uploads only; for big files use REST `PUT /v1/files/{path}`) | `{path, size}` |
| `get_file` | `path` | `{path, size}` (the bytes themselves are fetched via REST `GET /v1/files/{path}`) |
| `delete_file` | `path` | `{deleted}` |

Audio over MCP is **strictly path/URL-based** — JSON-RPC can't carry raw bytes efficiently and the v1.0.0 contract enforces this everywhere. For inputs: pre-stage via REST `PUT /v1/files/{path}` (or the `put_file` MCP tool for small files) and pass `file_path`, or pass `file_url` when fetch is enabled. For outputs: pick `output_path` to keep the result in staging (chain it as the next call's `file_path`), or `output_url` to PUT it to S3-style storage.

The MCP endpoint is at `$AUDIOLLA_URL/v1/mcp`. It is JSON-RPC over streamable HTTP; do not try to describe it in OpenAPI or hit it with raw curl — use an MCP client.

### AI restoration — de-reverb / de-echo / de-noise (`/v1/audio/restore/{engine}`)

All three restoration variants live under one endpoint; the engine is in the URL path. `aggressive=true` enables hard-mode echo removal on `uvr-deecho` (no-op on the others).

```bash
# De-reverb (BS-Roformer, SDR 19+)
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/restore/uvr-dereverb \
  -d '{"file_path":"uploads/reverby.wav","output_path":"out/clean.wav"}'

# De-echo (VR Architecture)
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/restore/uvr-deecho \
  -d '{"file_path":"uploads/echoy.wav","output_path":"out/clean.wav"}'

# De-echo, aggressive — stronger suppression, may affect dry signal more
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/restore/uvr-deecho \
  -d '{"file_path":"uploads/echoy.wav","aggressive":true,"output_path":"out/clean.wav"}'

# De-noise (MelBand Roformer, SDR 28)
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/restore/uvr-denoise \
  -d '{"file_path":"uploads/noisy.wav","output_path":"out/clean.wav"}'
```

Path engines: `uvr-dereverb`, `uvr-deecho`, `uvr-denoise`. JSON params: `aggressive` (uvr-deecho only, default `false`), `output_format`, `output_path`, `output_url`. The old `uvr-deecho-aggressive` engine slug is gone — set `aggressive=true` on `uvr-deecho` instead.

### Audio-to-MIDI transcription (`/v1/audio/to_midi/{engine}`)

Convert any audio to a polyphonic MIDI file using Spotify's basic-pitch (ONNX backend, no TensorFlow). The MIDI is written to `output_path` / `output_url`.

```bash
# Any audio → MIDI staged at output_path
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/to_midi/basic-pitch \
  -d '{"file_path":"uploads/guitar.wav","output_path":"midi/guitar.mid"}'

# Tune detection thresholds
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/to_midi/basic-pitch \
  -d '{"file_path":"uploads/piano.wav","onset_threshold":0.6,"frame_threshold":0.3,"minimum_note_length_ms":80,"output_path":"midi/piano.mid"}'
# → {"path":"midi/piano.mid","size":...,"engine":"basic-pitch","output_format":"mid"}
```

Params (all optional): `onset_threshold` (0–1, default 0.5), `frame_threshold` (0–1, default 0.3), `minimum_note_length_ms` (default 58), `minimum_frequency` / `maximum_frequency` (Hz, None = unconstrained), `multiple_pitch_bends` (bool, default false), `melodia_trick` (bool, default true). Plus `output_path` xor `output_url`.

The staged MIDI works directly with `/v1/midi/inspect`, `/v1/midi/transform`, and `/v1/midi/render` — chain `output_path` from one call into `file_path` on the next for a full audio → MIDI → re-render pipeline.

### Neural speech and vocal enhancement (`/v1/audio/enhance/{engine}`)

DeepFilterNet DF3 noise suppression — deep learning model trained on speech. More surgical than UVR's de-noise for voice/vocal recordings.

```bash
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/enhance/deepfilter \
  -d '{"file_path":"uploads/vocal_recording.wav","output_path":"out/enhanced.wav"}'

# MP3 output, staged
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/enhance/deepfilter \
  -d '{"file_path":"vocals/raw.wav","output_format":"mp3","output_path":"vocals/enhanced.mp3"}'
```

Engine in path: `deepfilter`. JSON params: `output_format`, `output_path`, `output_url`.

> **Note on UVR model weights:** `uvr-dereverb`, `uvr-deecho`, `uvr-denoise`, `uvr-karaoke`, and `uvr-vocal-bsr` all need their `.ckpt` / `.pth` model files present in the server's `AUDIOLLA_UVR_MODELS_DIR` (default `/data/uvr_models`). The image does **not** bundle these files — the operator must download them and mount the directory. If a model file is missing, the endpoint returns 500 on first load. See the README for the exact download list.

### Workflows — presets + ad-hoc pipelines

Two ways to chain operations server-side. Both keep intermediate audio in memory across steps — no re-upload, no separate HTTP calls.

**Curated presets** — server-side YAML workflows. One POST, one result.

```bash
# List the curated presets
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" $AUDIOLLA_URL/v1/presets \
  | jq '.data[] | {name, description}'

# Inspect a preset's steps before running
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  $AUDIOLLA_URL/v1/presets/master-for-spotify | jq '.steps'

# Run a preset against a staged file
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/presets/podcast-cleanup \
  -d '{"file_path":"uploads/interview.wav","output_path":"out/cleaned.wav"}'
```

Shipped presets: `master-for-spotify` (3-band master + -14 LUFS), `podcast-cleanup` (DeepFilterNet + de-ess + -16 LUFS), `vocal-cleanup` (UVR dereverb + denoise + de-ess + light comp). Operators can add their own YAML in `AUDIOLLA_PRESETS_DIR`.

**Ad-hoc pipeline** — chain any op slug in a single call.

```bash
# List available op slugs
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" $AUDIOLLA_URL/v1/ops

# Restore + multiband + normalise in one request
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/pipeline \
  -d '{
    "file_path":"uploads/track.wav",
    "output_path":"out/processed.wav",
    "steps":[
      {"op":"restore","params":{"engine":"uvr-denoise"}},
      {"op":"multiband_compress","params":{
        "crossovers_hz":[200,3000],
        "bands":[
          {"threshold_db":-18,"ratio":3},
          {"threshold_db":-14,"ratio":2.5},
          {"threshold_db":-10,"ratio":2}
        ]
      }},
      {"op":"normalize","params":{"target_lufs":-14}}
    ]
  }'
```

The response includes a `steps` log — `[{step, op, params, size_after}, …]` — so you can audit what ran. Pipeline + preset endpoints support `async_job=true` / `output_path` / `output_url` like every other audio-producing endpoint.

### Async jobs

Every audio-producing endpoint accepts `"async_job": true` in the JSON body. The call returns immediately with a 202 JSON `{job_id, status_url}` and the work runs in the background. Optionally pass `webhook_url` and audiolla POSTs the completion event to it.

```bash
# Submit
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/separate \
  -d '{
    "file_path":"uploads/track.wav",
    "engine":"htdemucs",
    "async_job":true,
    "webhook_url":"https://your-server.example/hooks/audiolla",
    "output_path":"stems/track.zip"
  }'
# → 202 {"job_id": "abc123", "status_url": "/v1/jobs/abc123"}

# Poll
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  $AUDIOLLA_URL/v1/jobs/abc123 \
  | jq '{status, duration_sec, result}'

# List with optional filter
curl -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  "$AUDIOLLA_URL/v1/jobs?status=completed"

# Cancel
curl -X DELETE -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  $AUDIOLLA_URL/v1/jobs/abc123
```

When neither `output_path` nor `output_url` is set, async jobs default to `jobs/{job_id}.{ext}` in the staging area. The job's `result` field points there.

### Output to presigned PUT URL

Every audio-producing endpoint accepts `"output_url": "<presigned PUT URL>"` as the alternative to `output_path`. Audiolla PUTs the encoded audio to the URL with the correct `Content-Type`, and the response is JSON `{url, size, ...}`. Works with S3, R2, MinIO, or any service that supports presigned PUTs.

```bash
# Master + upload result directly to S3 — no intermediate disk hit
curl -X POST -H "Authorization: Bearer $AUDIOLLA_TOKEN" \
  -H 'Content-Type: application/json' \
  $AUDIOLLA_URL/v1/audio/master \
  -d '{
    "file_path":"uploads/mix.wav",
    "mode":"chain",
    "preset":"loud",
    "output_url":"https://your-bucket.s3.amazonaws.com/mastered.wav?X-Amz-Signature=..."
  }'
```

Requires the operator to enable `AUDIOLLA_FETCH_MODE` server-side (same allowlist that governs `file_url`). If disabled, the call returns 400 — don't try to bypass.

Async jobs also support `output_url` — the completed job PUTs the result on completion.

## Common gotchas

- **`features=["lufs"]` is wrong**, use `features=["loudness"]`. (LUFS *is* an integrated loudness measurement, but the feature name on the wire is `loudness`.)
- **`mode=chain` without `preset` returns 400.** Always pass `"preset":"transparent"` or `"preset":"loud"`.
- **`htdemucs_ft` rejected on CPU** — the server flag `cuda_only` makes this return 400 unless the running image is `psyb0t/audiolla:latest-cuda` with `--gpus all`.
- **Separation loads one engine at a time** — calling `separate` evicts whatever else is loaded. Pre-warming multiple Demucs variants doesn't survive across separation calls.
- **Engines unload after idle** — the first request after `AUDIOLLA_ENGINE_TTL` seconds of inactivity will be slow (model reload). For benchmarks or back-to-back jobs, keep traffic flowing or set `AUDIOLLA_PRELOAD` server-side.
- **Don't poll `/v1/ps`** as a load-progress indicator — it tells you what's loaded right now, not what's being loaded.
- **Output format on the response** comes from the `output_format` JSON field, NOT the `output_path` extension. The server transcodes via ffmpeg; the extension on `output_path` is just a filename hint.
- **Input format is auto-detected by ffmpeg** — WAV, MP3, FLAC, OGG, M4A, AAC, OPUS, etc. all work as input.
- **The `transform` `pitch` op takes semitones**, not cents — `n_semitones: 0.5` = half a semitone up, not a tiny shift.
- **`/v1/audio/loudness` measures only (JSON), `/v1/audio/normalize` writes normalized audio.** They split in v0.x — old guides that show `loudness?target_lufs=` returning audio are stale. Normalize requires `output_path` or `output_url` and returns JSON `{path or url, size, measured_lufs, target_lufs, normalized}`.
- **`file_url` / `output_url` are disabled by default.** If the server returns `URL fetch/upload is disabled` (400), the operator hasn't enabled `AUDIOLLA_FETCH_MODE` — don't try to bypass it.
- **`output_path` and `output_url` are mutually exclusive.** Supplying both is 400. Supplying neither on an audio-producing endpoint is also 400 (no inline-bytes mode exists in v1.0.0); the only exception is `async_job=true`, which auto-stages to `jobs/{job_id}.{ext}`.
- **`file_path` and `file_url` are mutually exclusive too.** Same exactly-one-of rule; zero or both is 400.
- **`threshold_db` on silence must be ≤ 0.** Positive values return 400 — dBFS can't be positive.
- **`/v1/audio/silence` without `trim_mode` returns JSON only** — `silent_ranges`, `non_silent_ranges`, `duration`. Audio is only produced when `trim_mode=edges` or `trim_mode=all` is set, and in that case `output_path` (or `output_url`) is required.
- **`/v1/audio/visualize/video/{mode}` produces video (MP4/WebM)** — staged at `output_path` or PUT to `output_url`. There is no inline-bytes response.
- **`keep_channels` and `drop_channels` in `/v1/midi/transform` are mutually exclusive.** Supplying both is 400.
- **Segments fallback on short audio.** If the input doesn't have enough beats for the requested `num_segments`, a single `A` span covering the whole file is returned with a `note` field explaining why — it does not error.
- **`/v1/audio/melody` unvoiced frames have `hz: null`.** Don't try to use them as a pitch value — filter them out first.
- **`/v1/audio/to_midi/{engine}` writes MIDI to `output_path` / `output_url`** — response JSON points at the staged `.mid` file. Pass it directly to `/v1/midi/inspect`, `/v1/midi/transform`, or `/v1/midi/render` as `file_path` on the next call.
- **basic-pitch uses the ONNX backend (no TensorFlow).** The model is auto-selected at import time. No config needed; `tensorflow` is not installed in the image.
- **basic-pitch output quality scales with the input.** Polyphonic recordings with many overlapping instruments confuse the model — best results on melodic solos or lightly-polyphonic material. Full mixes work but produce noisy MIDI.
- **`/v1/audio/enhance/{engine}` is optimised for speech and vocals.** DeepFilterNet DF3 is trained on speech signals. It works on full mixes but may reduce musical detail. For full-mix noise removal prefer `uvr-denoise`.
- **UVR model files are NOT bundled in the image.** `uvr-dereverb`, `uvr-deecho`, `uvr-denoise`, `uvr-karaoke`, `uvr-vocal-bsr` all require `.ckpt` / `.pth` files in `AUDIOLLA_UVR_MODELS_DIR` (`/data/uvr_models` by default). Missing file = 500 on first load. Check the README for the download list. The old `uvr-deecho-aggressive` slug is gone — use `uvr-deecho` with `aggressive=true` instead.
- **`uvr-karaoke` and `uvr-vocal-bsr` are NOT exposed via `/v1/audio/restore/uvr-dereverb`, `/v1/audio/restore/uvr-deecho`, or `/v1/audio/restore/uvr-denoise`.** Those endpoints only do restoration (single output stem). To use the karaoke or vocal-separation models, use `/v1/audio/separate` with the appropriate engine slug and `stems` field.
- **UVR models are CPU-only in the default image.** For GPU-accelerated inference, use `psyb0t/audiolla:latest-cuda` with `--gpus all`. The `:latest` (CPU) image works but can be slow for full-track restoration.

## Tips

- Use `GET /v1/engines` once at the start of a session to see what's actually configured — `AUDIOLLA_ENABLED_ENGINES` can hide things.
- For a multi-step pipeline (e.g. separate → master each stem → analyze), `PUT /v1/files/uploads/<name>.wav` once and reference via `file_path` on every subsequent REST call (or the equivalent MCP tools) — no need to re-upload. Chain each call's `output_path` into the next call's `file_path` to keep everything server-side. Only `GET /v1/files/<path>` when you actually need the bytes locally.
- Large input files: respect `AUDIOLLA_MAX_UPLOAD_BYTES` (default 200 MB). If unsure, `GET /healthz` first to confirm the server is up and ask the user to confirm the cap.
- Long-running separations (`htdemucs_ft` on CPU especially) can take minutes — set a generous curl `--max-time` and warn the user, or submit with `"async_job": true` and poll `/v1/jobs/{id}`.
- If you need exact reproducibility between runs, pin the engine version by passing the explicit slug (`htdemucs` vs `htdemucs_ft`) — there is no "auto" mode for separation.
