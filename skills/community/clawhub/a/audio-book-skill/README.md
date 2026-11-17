# audio-book-skill

Convert a text/Markdown manuscript into clean, long-form spoken narration
(MP3, optional MP4) fully locally with **Kokoro-82M** via **MLX**. No cloud
API, no per-character billing, no network at run time. Text-to-speech only.

See `SKILL.md` for the agent-facing workflow. This README covers install,
verified versions, licenses, and hardware.

---

## Hardware assumptions

- **Apple Silicon Mac** (M-series). MLX is Apple-Silicon-only; Kokoro-82M
  runs on the integrated GPU via Metal.
- Kokoro-82M is small (~330 MB in bf16). It runs comfortably in a few GB.
  The practical constraint is contention: another large local model server
  holding most of unified memory can OOM Kokoro's Metal buffer. Stop such a
  process before rendering.
- ffmpeg for assembly/encoding (CPU; negligible).

Non-Apple-Silicon hosts are out of scope for the proven path. The Kokoro
model and the chunking/assembly logic are portable in principle, but only
the MLX/`mlx-audio` path is verified here.

## Install (verified commands)

Use a dedicated virtualenv on **Python 3.12** (not 3.13+). Kokoro's G2P
frontend (`misaki` → spaCy → thinc → blis) has historically lacked prebuilt
wheels for the newest Python, failing to compile. If `pip install` dies with
a Cython error in `blis/py.pyx`, that's the cause — use 3.12.

```bash
# 1) Python 3.12 (Homebrew example)
brew install python@3.12

# 2) dedicated venv
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip

# 3) engine + English G2P frontend
pip install mlx-audio          # pulls in the MLX Kokoro pipeline
pip install "misaki[en]"       # English grapheme-to-phoneme frontend

# 4) ffmpeg (Homebrew)
brew install ffmpeg
```

The Kokoro model weights and voice files download automatically on first
synthesis into the HuggingFace cache
(`~/.cache/huggingface/hub/models--mlx-community--Kokoro-82M-bf16/`). They
are NOT committed to this repo.

## Verified dependency versions

Authored and end-to-end tested against:

| Component | Version |
|-----------|---------|
| Python | 3.12.14 |
| mlx-audio | 0.5.3 |
| mlx | 0.32.2 |
| misaki | 0.9.4 |
| torch | 2.14.0 (pulled by mlx-audio) |
| spaCy | 3.8.16 |
| numpy | 2.5.3 |
| ffmpeg | 8.0.1 |
| model | `mlx-community/Kokoro-82M-bf16` |

Newer versions may work; these are the confirmed-good pins.

## Quick start

```bash
mkdir -p out

python3 scripts/prepare_manuscript.py \
    --input example/example_manuscript.md \
    --output out/narration.txt \
    --drop-sources

python3 scripts/narrate.py \
    --input out/narration.txt \
    --out-dir out \
    --voice af_heart --lang a

# optional: still image + audio -> MP4
python3 scripts/assemble_video.py \
    --audio out/narration.mp3 \
    --image path/to/still.jpg \
    --output out/narration.mp4

# re-verify a finished job
python3 scripts/verify_job.py --job-dir out
```

If the interpreter running the scripts is different from the venv that has
`mlx-audio`, point `narrate.py` at the right one: `--python /path/to/.venv/bin/python3`.

## Scripts

| Script | Role |
|--------|------|
| `prepare_manuscript.py` | Source → narration-safe text. Never edits the source. Configurable heading/URL/citation/bibliography handling; applies verified pacing fixes. |
| `narrate.py` | Narration text → ordered MP3 + WAV master + manifest. Sentence-aware chunking, `--resume`, duration verification. |
| `assemble_video.py` | Optional still + MP3 → verified MP4. |
| `verify_job.py` | Re-verify a finished job dir against its manifest. |

## Configuration surface (all explicit, no machine-specific paths baked in)

- Manuscript, output dir, voice, language, model, speed, chunk size:
  command-line flags.
- Heading / URL / citation / bibliography treatment: `prepare_manuscript.py`
  flags (`--url-mode`, `--citation-mode`, `--drop-sources`). Meaningful
  attribution is retained by default; dropping sources from narration
  relocates them (keep them in a description/companion file).

## Licenses

- **This skill's code:** MIT (see `LICENSE`).
- **Kokoro-82M model:** Apache-2.0 (per the model's HuggingFace card).
  Verify the license on the model card you download before redistribution.
- **mlx-audio / MLX:** MIT (verify on the upstream repositories).
- **misaki / spaCy:** MIT (verify upstream).
- **Example manuscript** (`example/example_manuscript.md`): original,
  released into the public domain for this skill's tests and demos.

You are responsible for the rights to any manuscript you narrate and for
complying with the model and dependency licenses in your context.

## What this skill does NOT do

No transcription/STT, no automatic publishing or upload, no release
scheduling, no thumbnail/artwork generation, no background music, and no
paid-service dependency for the proven local workflow.

## Do not commit

Credentials, private manuscripts, generated audio/video, or downloaded model
weights. See `.gitignore`.
