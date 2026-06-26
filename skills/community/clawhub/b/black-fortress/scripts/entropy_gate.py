#!/usr/bin/env python3
"""
Black-Fortress Layer 3: Entropy Gate

Shannon entropy analysis on all output artifacts.
Any text field exceeding 6.0 bits/byte is flagged as a potential encoded payload.

Usage:
    python entropy_gate.py --input <output_dir> --threshold 6.0

What it does:
    1. Scans all files in the output directory
    2. Computes Shannon entropy per field/string
    3. Flags fields exceeding the threshold
    4. Returns JSON report with pass/fail verdict
"""

import os
import sys
import json
import math
import argparse
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from collections import Counter
from dataclasses import dataclass, asdict


# ─── Entropy Calculation ───────────────────────────────────────

def shannon_entropy(data: str) -> float:
    """Calculate Shannon entropy in bits per character."""
    if not data:
        return 0.0
    counter = Counter(data)
    length = len(data)
    entropy = 0.0
    for count in counter.values():
        probability = count / length
        if probability > 0:
            entropy -= probability * math.log2(probability)
    return entropy


def is_base64_pattern(s: str) -> bool:
    """Detect if a string looks like base64 encoding."""
    if len(s) < 16:
        return False
    import re
    # Base64 pattern: alphanumeric + /+=, no spaces, length multiple of 4
    if re.match(r'^[A-Za-z0-9+/]+=*$', s) and len(s) % 4 == 0:
        return True
    return False


def is_hex_pattern(s: str) -> bool:
    """Detect if a string looks like hex encoding."""
    if len(s) < 16:
        return False
    import re
    return bool(re.match(r'^[0-9a-fA-F]+$', s)) and len(s) % 2 == 0


def detect_encoding(s: str) -> str:
    """Detect potential encoding patterns."""
    if is_base64_pattern(s):
        return "base64"
    if is_hex_pattern(s):
        return "hex"
    return "none"


# ─── Artifact Analysis ─────────────────────────────────────────

@dataclass
class FieldReport:
    file: str
    field_path: str
    value_preview: str
    length: int
    entropy: float
    encoding_detected: str
    flagged: bool
    reason: str


@dataclass
class EntropyReport:
    status: str  # "pass" or "fail"
    threshold: float
    total_fields: int
    flagged_fields: int
    flagged_details: List[FieldReport]
    file_hashes: Dict[str, str]


def analyze_json_file(filepath: str, threshold: float) -> List[FieldReport]:
    """Analyze all string fields in a JSON file."""
    flagged = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return [FieldReport(
            file=filepath, field_path="<root>",
            value_preview="[unreadable]", length=0,
            entropy=0.0, encoding_detected="none",
            flagged=True, reason="File is not valid JSON"
        )]

    def walk(obj, path="$"):
        if isinstance(obj, str):
            entropy = shannon_entropy(obj)
            encoding = detect_encoding(obj)
            is_flagged = entropy > threshold or encoding != "none"
            reason = ""
            if entropy > threshold:
                reason = f"Entropy {entropy:.2f} > threshold {threshold}"
            if encoding != "none":
                reason += f" | {encoding} encoding detected"
            flagged.append(FieldReport(
                file=filepath, field_path=path,
                value_preview=obj[:80] + ("..." if len(obj) > 80 else ""),
                length=len(obj), entropy=round(entropy, 3),
                encoding_detected=encoding,
                flagged=is_flagged, reason=reason.strip(" |")
            ))
        elif isinstance(obj, dict):
            for key, val in obj.items():
                walk(val, f"{path}.{key}")
        elif isinstance(obj, list):
            for i, val in enumerate(obj):
                walk(val, f"{path}[{i}]")

    walk(data)
    return flagged


def analyze_text_file(filepath: str, threshold: float) -> List[FieldReport]:
    """Analyze a plain text file for high-entropy segments."""
    flagged = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        return [FieldReport(
            file=filepath, field_path="<binary>",
            value_preview="[binary file]", length=0,
            entropy=0.0, encoding_detected="none",
            flagged=True, reason="Binary file in output"
        )]

    for i, line in enumerate(lines):
        line = line.rstrip("\n")
        if not line or len(line) < 10:
            continue
        entropy = shannon_entropy(line)
        encoding = detect_encoding(line)
        is_flagged = entropy > threshold or encoding != "none"
        reason = ""
        if entropy > threshold:
            reason = f"Line {i+1}: entropy {entropy:.2f} > {threshold}"
        if encoding != "none":
            reason += f" | {encoding} encoding"
        if is_flagged:
            flagged.append(FieldReport(
                file=filepath, field_path=f"line[{i+1}]",
                value_preview=line[:80],
                length=len(line), entropy=round(entropy, 3),
                encoding_detected=encoding,
                flagged=True, reason=reason.strip(" |")
            ))
    return flagged


def analyze_directory(input_dir: str, threshold: float) -> EntropyReport:
    """Analyze all files in a directory."""
    all_flagged = []
    total_fields = 0
    file_hashes = {}

    for filepath in Path(input_dir).rglob("*"):
        if not filepath.is_file():
            continue
        if filepath.name.startswith("."):
            continue

        # Hash every file
        try:
            content = filepath.read_bytes()
            file_hashes[str(filepath)] = hashlib.sha256(content).hexdigest()
        except Exception:
            continue

        if filepath.suffix.lower() == ".json":
            fields = analyze_json_file(str(filepath), threshold)
            total_fields += len(fields)
            all_flagged.extend(f for f in fields if f.flagged)
        elif filepath.suffix.lower() in (".txt", ".csv", ".log", ".md", ".yaml", ".yml", ".toml"):
            fields = analyze_text_file(str(filepath), threshold)
            total_fields += len(fields)
            all_flagged.extend(f for f in fields if f.flagged)
        elif filepath.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
            # Images are handled by Layer 4 (babel_output_filter)
            # Just hash them here
            pass

    status = "fail" if all_flagged else "pass"
    return EntropyReport(
        status=status,
        threshold=threshold,
        total_fields=total_fields,
        flagged_fields=len(all_flagged),
        flagged_details=all_flagged,
        file_hashes=file_hashes
    )


def main():
    parser = argparse.ArgumentParser(description="Black-Fortress Entropy Gate")
    parser.add_argument("--input", required=True, help="Directory to scan")
    parser.add_argument("--threshold", type=float, default=6.0,
                        help="Entropy threshold in bits/byte (default: 6.0)")
    parser.add_argument("--output", help="Write report to file (default: stdout)")
    args = parser.parse_args()

    if not os.path.isdir(args.input):
        print(json.dumps({"status": "error", "message": f"Not a directory: {args.input}"}))
        sys.exit(2)

    report = analyze_directory(args.input, args.threshold)
    report_json = json.dumps(asdict(report), indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report_json)
    else:
        print(report_json)

    sys.exit(0 if report.status == "pass" else 1)


if __name__ == "__main__":
    main()
