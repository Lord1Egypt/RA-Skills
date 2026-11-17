#!/usr/bin/env python3
"""Build the GitHub, SkillHub and ClawHub packages from one manifest spec."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (2026, 11, 10, 0, 0, 0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> Dict:
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))


def collect(entries: Iterable[str], excludes: Iterable[str]) -> List[str]:
    patterns = list(excludes)
    found: List[str] = []
    for entry in entries:
        path = ROOT / entry
        if path.is_dir():
            found.extend(p.relative_to(ROOT).as_posix() for p in path.rglob("*") if p.is_file())
        elif path.is_file():
            found.append(path.relative_to(ROOT).as_posix())
        else:
            raise SystemExit("missing include entry: {}".format(entry))
    kept = []
    for rel in sorted(set(found)):
        if any(fnmatch.fnmatchcase(rel, pattern) for pattern in patterns):
            continue
        kept.append(rel)
    return kept


def check_skill(skill_text: str, version: str) -> None:
    match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.S)
    if not match:
        raise SystemExit("SKILL.md frontmatter is missing")
    fields = dict(re.findall(r"^([A-Za-z_]+):\s*(.+)$", match.group(1), re.M))
    if fields.get("name") != "agent-slim":
        raise SystemExit("SKILL.md name must be agent-slim")
    if fields.get("version") != version:
        raise SystemExit("SKILL.md version does not match manifest")


def apply_renames(files: List[str], renames: Dict[str, str]) -> List[tuple]:
    """Map source paths to archive paths; platform-only renames never touch the source tree."""
    return [(rel, renames.get(rel, rel)) for rel in files]


def build_zip(target: Path, items: List[tuple], prefix: str) -> Dict:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for src, arc in items:
            info = zipfile.ZipInfo((prefix + arc) if prefix else arc, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, (ROOT / src).read_bytes())
    return {"name": target.name, "files": len(items), "bytes": target.stat().st_size, "sha256": sha256(target)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Agent Slim release packages.")
    parser.add_argument("--out", default=str(ROOT / "dist"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest()
    version = manifest["version"]
    check_skill((ROOT / "SKILL.md").read_text(encoding="utf-8"), version)
    out = Path(args.out)
    packages = manifest["release"]["packages"]
    results = []
    for platform in ("github", "skillhub", "clawhub"):
        spec = packages[platform]
        files = collect(spec["include"], spec.get("exclude", []))
        required = {"SKILL.md", "README.md", "manifest.json"}
        missing = sorted(required - set(files))
        if missing:
            raise SystemExit("{} package misses {}".format(platform, ", ".join(missing)))
        filename = "agent-slim-{}-v{}.zip".format(platform, version)
        items = apply_renames(files, spec.get("renames", {}))
        results.append(build_zip(out / filename, items, spec.get("prefix", "")))

    sums = out / "SHA256SUMS.txt"
    sums.write_text("".join("{}  {}\n".format(item["sha256"], item["name"]) for item in results), encoding="utf-8")
    summary = {"version": version, "out": str(out), "packages": results, "sums": str(sums)}
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print("{name} files={files} bytes={bytes} sha256={sha256}".format(**item))
        print("SHA256SUMS.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
