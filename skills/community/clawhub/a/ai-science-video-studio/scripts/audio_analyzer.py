#!/usr/bin/env python3
"""
Audio QA Analyzer — Detect audio issues in video files.

Performs second-by-second mean/peak analysis, gap detection, and clipping
detection on audio tracks extracted from video files.

Usage:
    python3 audio_analyzer.py output.mp4
    python3 audio_analyzer.py output.mp4 --threshold -50 --gap-min 0.05
"""

import argparse
import json
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path


def extract_audio_wav(video_path, output_path):
    """Extract audio as 16-bit PCM WAV for analysis."""
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "48000",
        "-ac", "2",
        output_path,
    ], check=True, capture_output=True)


def analyze_wav(wav_path, threshold_db=-60, gap_min_sec=0.08):
    """
    Analyze WAV file and return a report.

    Parameters:
        wav_path: path to 16-bit PCM WAV file
        threshold_db: dB threshold for silence detection
        gap_min_sec: minimum silence duration (seconds) to report as a gap
    """
    with wave.open(wav_path, "rb") as wf:
        n_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        n_frames = wf.getnframes()
        duration = n_frames / frame_rate

        raw = wf.readframes(n_frames)
        fmt = f"<{n_frames * n_channels}h"
        samples = struct.unpack(fmt, raw)

    # De-interleave channels
    left = samples[0::2]
    right = samples[1::2]

    threshold_abs = int(10 ** (threshold_db / 20) * 32768)

    results = {
        "file": str(wav_path),
        "duration": round(duration, 3),
        "sample_rate": frame_rate,
        "channels": n_channels,
        "issues": [],
        "per_second": [],
    }

    # Per-second analysis
    for t in range(int(duration)):
        start = t * frame_rate
        end = min(start + frame_rate, n_frames)

        l_chunk = [abs(left[i]) for i in range(start, end)]
        r_chunk = [abs(right[i]) for i in range(start, end)]

        l_mean = sum(l_chunk) / len(l_chunk) if l_chunk else 0
        r_mean = sum(r_chunk) / len(r_chunk) if r_chunk else 0
        l_peak = max(l_chunk) if l_chunk else 0
        r_peak = max(r_chunk) if r_chunk else 0

        second_info = {
            "time": t,
            "left_mean": round(l_mean, 1),
            "right_mean": round(r_mean, 1),
            "left_peak": l_peak,
            "right_peak": r_peak,
        }

        # Clipping detection
        if l_peak > 32000 or r_peak > 32000:
            second_info["warning"] = "CLIPPING"
            results["issues"].append({
                "type": "clipping",
                "severity": "P0",
                "time": t,
                "left_peak": l_peak,
                "right_peak": r_peak,
                "detail": f"Peak {max(l_peak, r_peak)}/32768 at {t}s — near clipping"
            })
        elif l_peak > 30000 or r_peak > 30000:
            second_info["warning"] = "HIGH"
            results["issues"].append({
                "type": "high_level",
                "severity": "P1",
                "time": t,
                "detail": f"High level {max(l_peak, r_peak)}/32768 at {t}s"
            })

        # Channel imbalance detection
        if l_chunk and r_chunk:
            l_rms = (sum(x * x for x in l_chunk) / len(l_chunk)) ** 0.5
            r_rms = (sum(x * x for x in r_chunk) / len(r_chunk)) ** 0.5
            if max(l_rms, r_rms) > 500:  # Only check when there's actual audio
                ratio = l_rms / r_rms if r_rms > 0 else float("inf")
                if ratio > 2 or ratio < 0.5:
                    second_info["warning"] = "IMBALANCE"

        results["per_second"].append(second_info)

    # Gap detection
    gap_start = None
    for t, info in enumerate(results["per_second"]):
        is_silent = info["left_mean"] < threshold_abs and info["right_mean"] < threshold_abs
        if is_silent and gap_start is None:
            gap_start = t
        elif not is_silent and gap_start is not None:
            gap_duration = t - gap_start
            if gap_duration >= gap_min_sec:
                results["issues"].append({
                    "type": "gap",
                    "severity": "P1",
                    "time": gap_start,
                    "duration": gap_duration,
                    "detail": f"Silence gap from {gap_start}s to {t}s ({gap_duration:.2f}s)"
                })
            gap_start = None

    # Overall stats
    all_peaks = [max(info["left_peak"], info["right_peak"]) for info in results["per_second"]]
    results["max_peak"] = max(all_peaks) if all_peaks else 0
    results["max_peak_db"] = round(20 * (results["max_peak"] / 32768).__log10__(), 1) if all_peaks else -999

    p0_count = sum(1 for i in results["issues"] if i["severity"] == "P0")
    p1_count = sum(1 for i in results["issues"] if i["severity"] == "P1")

    results["summary"] = {
        "total_issues": len(results["issues"]),
        "p0_count": p0_count,
        "p1_count": p1_count,
        "max_peak": results["max_peak"],
        "max_peak_db": results["max_peak_db"],
        "verdict": "PASS" if p0_count == 0 else "FAIL",
    }

    return results


def print_report(results):
    """Print a human-readable analysis report."""
    s = results["summary"]
    print(f"\n{'='*60}")
    print(f"  Audio QA Report: {results['file']}")
    print(f"{'='*60}")
    print(f"  Duration: {results['duration']}s | {results['sample_rate']}Hz | {results['channels']}ch")
    print(f"  Max Peak: {s['max_peak']}/32768 ({s['max_peak_db']}dB)")
    print(f"  Issues: {s['total_issues']} (P0: {s['p0_count']}, P1: {s['p1_count']})")
    print(f"  Verdict: {s['verdict']}")
    print(f"{'='*60}")

    if results["issues"]:
        print(f"\n  Issues Found:")
        for issue in results["issues"]:
            marker = "🔴" if issue["severity"] == "P0" else "🟡"
            print(f"  {marker} [{issue['severity']}] {issue['detail']}")
    else:
        print(f"\n  ✅ No issues detected.")

    # Print per-second summary (warnings only)
    warnings = [info for info in results["per_second"] if "warning" in info]
    if warnings:
        print(f"\n  Per-Second Warnings:")
        for info in warnings:
            print(f"  ⚠️  {info['time']:3d}s: {info['warning']} "
                  f"(L peak={info['left_peak']}, R peak={info['right_peak']})")


def main():
    parser = argparse.ArgumentParser(description="Audio QA Analyzer")
    parser.add_argument("input", type=str, help="Video or audio file path")
    parser.add_argument("--threshold", type=float, default=-60,
                        help="Silence threshold in dB (default: -60)")
    parser.add_argument("--gap-min", type=float, default=0.08,
                        help="Minimum silence gap duration in seconds (default: 0.08)")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON instead of human-readable")

    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = Path(tmpdir) / "extracted.wav"
        extract_audio_wav(args.input, str(wav_path))
        results = analyze_wav(str(wav_path), args.threshold, args.gap_min)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_report(results)

    # Exit with non-zero if P0 issues found
    if results["summary"]["p0_count"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
