---
name: audio-book-skill
description: >
  Convert a text or Markdown manuscript into clean, long-form spoken
  narration (MP3, optional MP4) fully locally with Kokoro-82M via MLX.
  Use when asked to narrate a document, make an audiobook, read a manuscript
  aloud, or produce spoken-word audio/video from written text. Sentence-aware
  chunking, resumable jobs, configurable voices/languages, verifiable outputs.
  Text-to-speech only (not transcription).
version: 1.0.0
license: MIT
---

# audio-book-skill

Turn a manuscript into long-form narration, locally and reproducibly.

The proven engine is **Kokoro-82M** (an 82M-parameter open TTS model) run
through the **`mlx-audio`** CLI on Apple Silicon (MLX). Synthesis costs no
per-character fees and needs no network at run time. This skill wraps that
engine with deterministic chunking, resume, lossless assembly, and a job
manifest so any capable agent can reproduce a render.

## When to use

Triggers: "narrate this," "turn this into an audiobook," "read this aloud,"
"make an audio/spoken version of X," "produce a narration MP3/MP4 from this
document."

Not this skill: speech-to-text/transcription; music or background scoring;
automatic publishing or upload; thumbnail/artwork generation.

## What you get

- `scripts/prepare_manuscript.py` — source manuscript → narration-safe text
  (never edits the source; configurable heading/URL/citation/bibliography
  handling; applies the verified pacing fixes).
- `scripts/narrate.py` — narration text → ordered MP3 + lossless WAV master
  + `manifest.json`. Sentence-aware chunking, `--resume`, verification.
- `scripts/assemble_video.py` — OPTIONAL still image + MP3 → verified MP4.
- `scripts/verify_job.py` — re-verify a finished job against its manifest.
- `references/FIXES.md` — verified vs. suspected quality fixes.
- `example/` — an original public-domain example manuscript.
- `README.md` — install commands, versions, licenses, hardware assumptions.

## The one verified command (manuscript → MP3)

After setup (see README), from the skill directory:

```bash
# 1) prepare a narration-safe script (does not touch the source)
python3 scripts/prepare_manuscript.py \
    --input example/example_manuscript.md \
    --output out/narration.txt \
    --drop-sources

# 2) synthesize to MP3 (+ lossless WAV master + manifest)
python3 scripts/narrate.py \
    --input out/narration.txt \
    --out-dir out \
    --voice af_heart \
    --lang a
```

Output: `out/narration.mp3`, `out/narration_MASTER.wav`, `out/manifest.json`,
`out/segments/`. This exact chain was run end-to-end during authoring.

## Voices and language (choose deliberately)

Voice id prefixes encode accent+gender; the `--lang` G2P code MUST match:

| Family | `--lang` | Example voice ids |
|--------|----------|-------------------|
| American English | `a` | `af_heart`, `af_bella`, `am_michael` |
| British English  | `b` | `bf_emma`, `bf_alice`, `bm_george`, `bm_lewis` |

Accent is a **voice choice**, not a post-filter. A British `bf_` voice under
`--lang a` will use American phonemization (mismatch). Set `--lang b` for a
British voice. List what's downloaded:

```bash
python3 scripts/narrate.py --list-voices
```

Tested during authoring: `af_heart` (American, `--lang a`) and `bf_emma`
(British, `--lang b`). Others are available; test a short excerpt before a
full render. Do not hardcode a voice — pass `--voice`/`--lang` per job.

## Chunking, order, and joins

`narrate.py` splits on sentence boundaries and packs whole sentences up to
`--max-chars` (default 600) so a chunk never breaks mid-sentence. Oversized
single sentences are split at the nearest clause boundary (`; : , —`), never
mid-word. Segments are assembled **in numeric order** via ffmpeg stream-copy
(no re-encode), and the manifest records chunk order + a duration check that
flags any dropped/duplicated/clipped audio.

## Resume

`--resume` reuses existing chunk WAVs only when the input text, model, voice,
language, speed, and max-chars all still match the manifest signature. Any
change re-renders. Interrupted jobs resume from the last completed chunk.

## The manifest

`out/manifest.json` records: input SHA-256 + size, engine/model/voice/lang/
speed, per-chunk hashes and order, output paths + duration, a verification
block, and captured dependency versions. It is the reproducibility record —
keep it with the outputs.

## Verified quality fixes (see references/FIXES.md)

1. **Mid-sentence pauses** = surviving soft line breaks in wrapped prose;
   fixed by unwrapping to full paragraphs (biggest single fix).
2. **Abbreviation periods** (`U.S.`, `e.g.`, `Dr.`) read as full stops;
   converted to spoken forms.
3. **Accent** is a native voice + matching `--lang`, not a filter.
4. **Sources/bibliography** narrated unintentionally; optional
   `--drop-sources` relocates them to a description/companion file.
5. **Lossless intermediate**, single final MP3 encode (no repeated loss).
6. Long renders: background them, poll at 30–60s; don't SIGKILL mid-write.
7. Apple Silicon: stop other large local model servers first (GPU OOM).

Suspected/defensive behaviors (Roman-numeral labels, slash alternatives,
the benign phonemizer warning) are documented separately in FIXES.md — do
not treat them as guaranteed.

## Safety / hygiene

- The source manuscript is never modified; narration is a separate file.
- Do not commit credentials, private manuscripts, generated media, or model
  weights (see `.gitignore`). Weights download to the HuggingFace cache.
- No cloud dependency for the proven local workflow.
