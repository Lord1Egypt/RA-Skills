#!/usr/bin/env python3
"""
narrate.py — portable long-form text-to-speech narration (Kokoro-82M / MLX).

Converts a plain-text narration script into a single MP3 (and a lossless
WAV master), fully locally. No cloud API, no per-character billing.
Sentence-aware chunking, resumable execution, and a job manifest recording
inputs / settings / outputs / verification for reproducibility.

Proven engine: the `mlx_audio.tts.generate` CLI (the same invocation used
to render real multi-part long-form narration). This wrapper adds
deterministic sentence-aware chunk boundaries, resume, ordered lossless
assembly, and a manifest around that CLI — it does not replace it.

This script does NOT rewrite your manuscript. Prepare a narration script
first with prepare_manuscript.py (or supply your own plain text).

Normal manuscript-to-MP3 workflow (one command):
    python3 narrate.py --input narration.txt --out-dir ./out \
        --voice af_heart --lang a

Key flags:
    --input PATH     Plain-text narration script (required).
    --out-dir DIR    Output directory (required). Created if missing.
    --voice NAME     Kokoro voice id (default: af_heart). See --list-voices.
    --lang CODE      Kokoro G2P/language code (default: a = American English;
                     b = British English; see Kokoro docs for the rest).
    --model REPO     MLX model repo (default: mlx-community/Kokoro-82M-bf16).
    --python BIN     Python interpreter that has mlx-audio installed
                     (default: the interpreter running this script).
    --speed FLOAT    Speaking rate multiplier (default: 1.0).
    --max-chars INT  Soft chunk-size cap in characters (default: 600).
    --resume         Reuse existing chunk WAVs when text + engine/model +
                     voice + synthesis settings match the manifest.
    --no-mp3         Stop after the lossless WAV master (skip MP3 encode).
    --list-voices    Print downloaded voice ids for the model and exit.

Exit codes: 0 ok, 2 bad args, 3 dependency/model error, 4 synthesis error.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import wave
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1
DEFAULT_MODEL = "mlx-community/Kokoro-82M-bf16"
DEFAULT_VOICE = "af_heart"
DEFAULT_LANG = "a"
DEFAULT_MAX_CHARS = 600


# ----------------------------- helpers ---------------------------------

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def dep_versions(python_bin: str) -> dict:
    """Best-effort dependency version capture for the manifest."""
    out = {}
    probe = (
        "import sys,json;"
        "d={'python':sys.version.split()[0]};"
        "\nfor m in ('mlx','mlx_audio','misaki'):\n"
        "    try:\n        mod=__import__(m);"
        "d[m]=getattr(mod,'__version__','unknown')\n"
        "    except Exception:\n        d[m]='not-importable'\n"
        "print(json.dumps(d))"
    )
    try:
        r = subprocess.run([python_bin, "-c", probe],
                           capture_output=True, text=True, check=False)
        line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "{}"
        out.update(json.loads(line))
    except Exception:
        out["python"] = "unknown"
    try:
        ff = subprocess.run(["ffmpeg", "-version"],
                            capture_output=True, text=True, check=False)
        out["ffmpeg"] = ff.stdout.splitlines()[0] if ff.stdout else "unknown"
    except FileNotFoundError:
        out["ffmpeg"] = "not-found"
    return out


# --------------------------- chunking ----------------------------------

# Conservative sentence splitter: break on . ! ? (plus an optional closing
# quote/paren) followed by whitespace and a capital/quote/digit. Kept
# conservative so it does not shatter abbreviations the preprocessor
# already neutralized.
_SENTENCE_END = re.compile(
    r'(?<=[.!?])["\'\u201d\u2019\)\]]?\s+(?=[A-Z0-9"\'\u201c\u2018])'
)


def split_sentences(paragraph: str) -> list:
    parts = _SENTENCE_END.split(paragraph.strip())
    return [p.strip() for p in parts if p.strip()]


def hard_split_oversized(sentence: str, max_chars: int) -> list:
    """A single sentence longer than max_chars is split at the clause
    boundary (; : , —) nearest the cap, never mid-word; if no clause
    boundary exists, fall back to a word boundary. Documented behavior:
    oversized sentences are broken at the nearest safe boundary, never
    truncated."""
    if len(sentence) <= max_chars:
        return [sentence]
    chunks, remaining = [], sentence
    while len(remaining) > max_chars:
        window = remaining[:max_chars]
        cut = max(window.rfind("; "), window.rfind(": "),
                  window.rfind(", "), window.rfind("\u2014"))
        if cut <= 0:
            cut = window.rfind(" ")
        if cut <= 0:
            cut = max_chars - 1
        chunks.append(remaining[:cut + 1].strip())
        remaining = remaining[cut + 1:].strip()
    if remaining:
        chunks.append(remaining)
    return chunks


def build_chunks(text: str, max_chars: int) -> list:
    """Sentence-aware chunking: accumulate whole sentences up to max_chars
    so every chunk boundary falls between sentences (never mid-sentence),
    which prevents clipped words and unnatural joins. A blank-line
    paragraph break forces a boundary."""
    chunks = []
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        buf = ""
        for sentence in split_sentences(para):
            for piece in hard_split_oversized(sentence, max_chars):
                if not buf:
                    buf = piece
                elif len(buf) + 1 + len(piece) <= max_chars:
                    buf = f"{buf} {piece}"
                else:
                    chunks.append(buf)
                    buf = piece
        if buf:
            chunks.append(buf)
    return chunks


# --------------------------- synthesis ---------------------------------

def synth_chunk(python_bin, model, voice, lang, speed, text, seg_dir, prefix):
    """Synthesize one chunk to a single WAV via the proven CLI.

    We drive the CLI once per chunk with --join_audio so its output is
    exactly one WAV per chunk (deterministic naming), letting THIS script
    own chunk order, resume, and assembly rather than the CLI's internal
    auto-chunker."""
    cmd = [
        python_bin, "-m", "mlx_audio.tts.generate",
        "--model", model,
        "--voice", voice,
        "--lang_code", lang,
        "--speed", str(speed),
        "--join_audio",
        "--audio_format", "wav",
        "--output_path", str(seg_dir),
        "--file_prefix", prefix,
    ]
    r = subprocess.run(cmd, input=text, capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise RuntimeError(
            f"CLI exit {r.returncode}: {r.stderr.strip().splitlines()[-1:]}"
        )
    # Locate the produced WAV for this prefix.
    produced = sorted(seg_dir.glob(f"{prefix}*.wav"))
    if not produced:
        raise RuntimeError(f"no WAV produced for prefix {prefix}")
    # If the CLI emitted more than one (join failed), concat them here.
    target = seg_dir / f"{prefix}.wav"
    if len(produced) == 1:
        if produced[0] != target:
            produced[0].rename(target)
    else:
        _concat_wavs(produced, target)
        for p in produced:
            if p != target:
                p.unlink(missing_ok=True)
    return target


def preflight(python_bin: str, model: str) -> None:
    """Fail fast with a clear message if the engine is not importable."""
    r = subprocess.run(
        [python_bin, "-c", "import mlx_audio.tts.generate"],
        capture_output=True, text=True, check=False,
    )
    if r.returncode != 0:
        print("[dep-error] mlx-audio is not importable by the chosen Python.\n"
              f"  python: {python_bin}\n"
              "  fix: install into that interpreter (see README):\n"
              "       pip install mlx-audio 'misaki[en]'\n"
              f"  detail: {r.stderr.strip().splitlines()[-1:] }",
              file=sys.stderr)
        sys.exit(3)


# ----------------------------- assembly --------------------------------

def wav_duration(path: Path) -> float:
    with wave.open(str(path), "r") as w:
        return w.getnframes() / float(w.getframerate())


def _concat_wavs(segments: list, master: Path):
    """Loss-less ordered concatenation via ffmpeg concat demuxer (stream
    copy — no re-encode, so no repeated lossy generation loss)."""
    listfile = master.with_suffix(".concat.txt")
    with open(listfile, "w") as f:
        for seg in segments:
            f.write(f"file '{Path(seg).resolve()}'\n")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
         "-c", "copy", str(master)],
        check=True, capture_output=True, text=True,
    )
    listfile.unlink(missing_ok=True)


def encode_mp3(master: Path, mp3: Path):
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(master),
         "-codec:a", "libmp3lame", "-qscale:a", "2", str(mp3)],
        check=True, capture_output=True, text=True,
    )


# ------------------------------- main ----------------------------------

def list_voices(model_repo: str):
    hub = Path.home() / ".cache/huggingface/hub"
    slug = "models--" + model_repo.replace("/", "--")
    vdirs = list((hub / slug).glob("snapshots/*/voices"))
    if not vdirs:
        print("No downloaded voices found yet. Voices download on first "
              "synthesis; run one short narration to populate the cache.")
        return
    voices = sorted(p.stem for p in vdirs[0].glob("*.safetensors"))
    print(f"{len(voices)} voices for {model_repo}:")
    print(" ".join(voices))


def main():
    ap = argparse.ArgumentParser(description="Portable Kokoro long-form narration.")
    ap.add_argument("--input", type=Path)
    ap.add_argument("--out-dir", type=Path)
    ap.add_argument("--voice", default=DEFAULT_VOICE)
    ap.add_argument("--lang", default=DEFAULT_LANG)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--python", default=sys.executable, dest="python_bin")
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--no-mp3", action="store_true")
    ap.add_argument("--list-voices", action="store_true")
    args = ap.parse_args()

    if args.list_voices:
        list_voices(args.model)
        return

    if not args.input or not args.out_dir:
        ap.error("--input and --out-dir are required (unless --list-voices)")
    if not args.input.is_file():
        ap.error(f"input not found: {args.input}")

    preflight(args.python_bin, args.model)

    out_dir = args.out_dir
    seg_dir = out_dir / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    text = args.input.read_text(encoding="utf-8")
    text_hash = sha256_text(text)
    chunks = build_chunks(text, args.max_chars)
    if not chunks:
        print("[error] no narratable text after chunking", file=sys.stderr)
        sys.exit(4)

    sig_basis = json.dumps({
        "text_hash": text_hash, "voice": args.voice, "lang": args.lang,
        "model": args.model, "speed": args.speed, "max_chars": args.max_chars,
        "schema": SCHEMA_VERSION,
    }, sort_keys=True)
    settings_sig = sha256_text(sig_basis)

    manifest_path = out_dir / "manifest.json"
    prior = None
    if manifest_path.is_file():
        try:
            prior = json.loads(manifest_path.read_text())
        except Exception:
            prior = None

    can_resume = (
        args.resume and prior is not None
        and prior.get("settings_sig") == settings_sig
        and prior.get("chunk_count") == len(chunks)
    )
    if args.resume and not can_resume:
        print("[resume] text/settings changed since last run — re-rendering all.")

    print(f"[plan] {len(chunks)} chunks | voice={args.voice} lang={args.lang} "
          f"model={args.model} speed={args.speed}")

    segments = []
    for i, chunk in enumerate(chunks):
        prefix = f"seg_{i:04d}"
        seg = seg_dir / f"{prefix}.wav"
        chunk_hash = sha256_text(chunk)
        reuse = (
            can_resume and seg.is_file()
            and i < len(prior.get("chunks", []))
            and prior["chunks"][i]["hash"] == chunk_hash
        )
        if reuse:
            segments.append(seg)
            continue
        try:
            seg = synth_chunk(args.python_bin, args.model, args.voice,
                              args.lang, args.speed, chunk, seg_dir, prefix)
        except Exception as e:  # noqa: BLE001
            print(f"[synth-error] chunk {i}: {e}", file=sys.stderr)
            sys.exit(4)
        segments.append(seg)
        print(f"  [{i + 1}/{len(chunks)}] {seg.name}")

    stem = args.input.stem
    master = out_dir / f"{stem}_MASTER.wav"
    _concat_wavs(segments, master)
    total = round(wav_duration(master), 2)

    mp3 = None
    if not args.no_mp3:
        mp3 = out_dir / f"{stem}.mp3"
        encode_mp3(master, mp3)

    # Verification: assembled duration vs sum of chunk durations (detects
    # dropped/duplicated/clipped segments).
    seg_sum = round(sum(wav_duration(s) for s in segments), 2)
    dur_delta = round(abs(total - seg_sum), 3)
    verify_ok = dur_delta < 0.5  # ffmpeg stream-copy rounding tolerance

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "input": {"path": str(args.input), "sha256": text_hash,
                  "chars": len(text)},
        "engine": {"kind": "mlx_audio.tts.generate CLI",
                   "model": args.model, "voice": args.voice,
                   "lang": args.lang, "speed": args.speed,
                   "sample_rate_hz": 24000},
        "settings_sig": settings_sig,
        "chunk_count": len(chunks),
        "max_chars": args.max_chars,
        "chunks": [{"index": i, "hash": sha256_text(c), "chars": len(c),
                    "segment": f"segments/seg_{i:04d}.wav"}
                   for i, c in enumerate(chunks)],
        "outputs": {"master_wav": master.name,
                    "mp3": (mp3.name if mp3 else None),
                    "duration_sec": total},
        "verification": {"segment_sum_sec": seg_sum,
                         "assembled_sec": total,
                         "delta_sec": dur_delta,
                         "ordered_join_ok": verify_ok},
        "dependencies": dep_versions(args.python_bin),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))

    status = "OK" if verify_ok else "WARN(duration-mismatch)"
    print(f"[done] {status}  duration={total}s  master={master.name}"
          + (f"  mp3={mp3.name}" if mp3 else "")
          + f"  manifest={manifest_path.name}")
    if not verify_ok:
        print(f"[verify] assembled {total}s vs segment-sum {seg_sum}s "
              f"(delta {dur_delta}s) — inspect segments for drop/dupe.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
