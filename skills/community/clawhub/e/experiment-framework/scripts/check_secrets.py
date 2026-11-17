from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "RunPod token": re.compile(rb"\brpa_[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(rb"\bgh[opsu]_[A-Za-z0-9]{20,}\b"),
    "Hugging Face token": re.compile(rb"\bhf_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "private key": re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
}


def tracked_files() -> list[Path]:
    # Scope scanning to this export, even when it is nested in another repository.
    excluded = {".git", ".venv", "__pycache__", ".ruff_cache", "build", "dist"}
    return [
        path for path in ROOT.rglob("*")
        if path.is_file() and not path.is_symlink()
        and not any(part in excluded or part.endswith(".egg-info") for part in path.relative_to(ROOT).parts)
    ]


def main() -> int:
    findings: list[str] = []
    for path in tracked_files():
        if path.stat().st_size > 5_000_000:
            continue
        data = path.read_bytes()
        for label, pattern in PATTERNS.items():
            if pattern.search(data):
                findings.append(f"{path.relative_to(ROOT)}: {label}")
    if findings:
        print("\n".join(findings), file=sys.stderr)
        return 1
    print(f"secret scan passed ({len(tracked_files())} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
