#!/usr/bin/env python3
"""
verify_job.py — independent verification of a completed narration job.

Re-checks a job directory against its manifest WITHOUT re-rendering:
  * manifest present and schema-compatible
  * every chunk segment file listed in the manifest exists
  * segment count matches chunk count (no dropped/extra segments)
  * assembled master duration == sum of segment durations (within
    stream-copy rounding tolerance) — catches dropped/duplicated audio
  * declared outputs (master WAV, MP3) exist and decode cleanly

Usage:
    python3 verify_job.py --job-dir ./out
Exit 0 if all checks pass, 1 otherwise.
"""

import argparse
import json
import subprocess
import sys
import wave
from pathlib import Path

TOLERANCE_SEC = 0.5


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "r") as w:
        return w.getnframes() / float(w.getframerate())


def decodes(path: Path) -> bool:
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "null", "-"],
                       capture_output=True, text=True, check=False)
    return r.returncode == 0 and not r.stderr.strip()


def main():
    ap = argparse.ArgumentParser(description="Verify a narration job dir.")
    ap.add_argument("--job-dir", type=Path, required=True)
    args = ap.parse_args()

    d = args.job_dir
    manifest = d / "manifest.json"
    fails = []

    if not manifest.is_file():
        print(f"[fail] no manifest at {manifest}", file=sys.stderr)
        sys.exit(1)
    m = json.loads(manifest.read_text())

    if m.get("schema_version") != 1:
        fails.append(f"unexpected schema_version {m.get('schema_version')}")

    chunks = m.get("chunks", [])
    seg_paths = [d / c["segment"] for c in chunks]
    missing = [str(p) for p in seg_paths if not p.is_file()]
    if missing:
        fails.append(f"{len(missing)} segment file(s) missing: {missing[:3]}")

    if m.get("chunk_count") != len(chunks):
        fails.append("chunk_count != len(chunks)")

    present = [p for p in seg_paths if p.is_file()]
    seg_sum = round(sum(wav_duration(p) for p in present), 2) if present else 0.0

    master = d / m["outputs"]["master_wav"]
    if not master.is_file():
        fails.append(f"master WAV missing: {master.name}")
    else:
        asm = round(wav_duration(master), 2)
        if abs(asm - seg_sum) > TOLERANCE_SEC:
            fails.append(f"duration mismatch: master {asm}s vs segments {seg_sum}s")
        if not decodes(master):
            fails.append("master WAV fails full decode")

    mp3_name = m["outputs"].get("mp3")
    if mp3_name:
        mp3 = d / mp3_name
        if not mp3.is_file():
            fails.append(f"declared MP3 missing: {mp3_name}")
        elif not decodes(mp3):
            fails.append("MP3 fails full decode")

    print(f"[verify] job={d} chunks={len(chunks)} segments_present={len(present)} "
          f"segment_sum={seg_sum}s")
    if fails:
        for f in fails:
            print(f"  [fail] {f}", file=sys.stderr)
        sys.exit(1)
    print("[verify] all checks passed")


if __name__ == "__main__":
    main()
