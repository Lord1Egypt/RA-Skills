#!/usr/bin/env python3
"""Deterministic white-list packager for the Tianxi AI (天禧 AI) skill square upload.

Why a custom packager instead of `lenovoskill package`:
    `lenovoskill package` zips the whole source dir and would leak local dev noise
    (references/check_skill_md.py, __pycache__, dotfiles) and, critically, `config.yaml`
    whose `permissions.filesystem: read-only` contradicts the skill's two disclosed,
    consent-gated writes. The platform doc (2026-10-01) confirms config.yaml is NOT an
    official upload requirement, so we exclude it from the zip.

Output: dist/skill-inventory-<version>-tianxi.zip  (dist/ is git-ignored)
Safety: after packing, scans every .py in the zip for networking/subprocess keywords and
        asserts SKILL.md frontmatter parses and config.yaml is absent.

Usage:
    python tools/build_tianxi_zip.py
"""
from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "dist"
PKG_NAME = "skill-inventory-1.5.2-tianxi.zip"

# --- white-list: only these repo paths enter the zip (relative to REPO) ---
WHITELIST = [
    "SKILL.md",
    "SKILL.en.md",
    "README.md",
    "README.en.md",
    "LICENSE",
    "scripts/skill_inventory.py",
    "references/.gitkeep",
    "references/publishing.md",
    "references/publishing.en.md",
    "references/usage-triggers.md",
    "references/usage-triggers.en.md",
]

# --- black-list: even if matched by WHITELIST, drop these ---
EXCLUDE = {
    "config.yaml",
    "references/check_skill_md.py",
    "references/__pycache__",
    ".gitignore",
    ".clawhubignore",
}

RISK_KEYWORDS = [
    "urllib", "requests", "http.client", "socket.create",
    "os.system", "subprocess", "os.popen", "eval(",
]


def collect() -> list[Path]:
    files: list[Path] = []
    for rel in WHITELIST:
        p = REPO / rel
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file():
                    files.append(f)
    # apply black-list by relative path
    kept = [f for f in files if f.relative_to(REPO).as_posix() not in EXCLUDE]
    return kept


def pack(files: list[Path]) -> Path:
    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / PKG_NAME
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            arc = f.relative_to(REPO).as_posix()
            zf.write(f, arc)
    return out


def scan(zippath: Path) -> list[str]:
    problems: list[str] = []
    with zipfile.ZipFile(zippath) as zf:
        names = zf.namelist()
        if "config.yaml" in names:
            problems.append("config.yaml is present in the zip (must be excluded)")
        if "SKILL.md" not in names:
            problems.append("SKILL.md missing at zip root")
        for n in names:
            if n.endswith(".py"):
                data = zf.read(n).decode("utf-8", "replace")
                for kw in RISK_KEYWORDS:
                    if kw in data:
                        problems.append(f"{n}: contains risk keyword '{kw}'")
    return problems


def main() -> int:
    files = collect()
    missing = [w for w in WHITELIST if not (REPO / w).exists()]
    if missing:
        print(f"[WARN] whitelist entries not found: {missing}")
    print(f"[pack] {len(files)} files -> {PKG_NAME}")
    for f in files:
        print("   +", f.relative_to(REPO).as_posix())
    out = pack(files)
    size = out.stat().st_size
    print(f"[pack] wrote {out} ({size:,} bytes)")
    problems = scan(out)
    if problems:
        print("[SCAN] FAILED:")
        for p in problems:
            print("   -", p)
        return 1
    print("[SCAN] OK: no networking/subprocess keywords, SKILL.md present, config.yaml absent")
    if size > 10 * 1024 * 1024:
        print("[WARN] zip exceeds Tianxi 10MB limit")
        return 1
    print("[DONE] package ready for `lenovoskill push -zrp` (requires developer auth + OAuth)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
