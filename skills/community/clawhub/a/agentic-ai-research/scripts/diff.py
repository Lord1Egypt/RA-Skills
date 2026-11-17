"""diff.py — 哈希比对 → new/changed + 受影响已有页清单

用法:
    python diff.py [--root <wiki-root>]

输出 JSON：
{
  "schema_version_changed": bool,
  "new": [file, ...],
  "changed": [file, ...],
  "unchanged": [file, ...],
  "affected_pages": [page_path, ...]   # 受影响已有页（仅 changed 时非空）
}
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _root import detect_wiki_root, normalize_path

DEFAULT_ROOT = detect_wiki_root()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def list_raw_files(raw_dir: Path) -> list[Path]:
    if not raw_dir.exists():
        return []
    return sorted(p for p in raw_dir.iterdir() if p.is_file() and not p.name.startswith("."))


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def diff(root: Path) -> dict:
    raw_dir = root / "raw"
    wiki_dir = root / "wiki"
    manifest = load_json(wiki_dir / ".manifest.json", {"files": {}, "schema_version": "v1"})
    graph = load_json(
        wiki_dir / ".graph.json",
        {"entities": {}, "page_to_sources": {}, "source_to_pages": {}},
    )

    files_state = manifest.get("files", {})
    new_files, changed_files, unchanged_files = [], [], []

    for f in list_raw_files(raw_dir):
        rel = f"raw/{f.name}"
        h = sha256(f)
        prev = files_state.get(rel)
        if prev is None:
            new_files.append(rel)
        elif prev.get("sha256") != h:
            changed_files.append(rel)
        else:
            unchanged_files.append(rel)

    # 受影响已有页：仅 changed 文件触发的级联
    source_to_pages = graph.get("source_to_pages", {})
    affected = set()
    for src in changed_files:
        for page in source_to_pages.get(src, []):
            affected.add(page)

    # schema 版本变更 → 全量重编译
    schema_path = wiki_dir / "SCHEMA.md"
    schema_version = "v1"
    if schema_path.exists():
        for line in schema_path.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("schema_version:"):
                schema_version = line.split(":", 1)[1].strip()
                break

    schema_changed = manifest.get("schema_version", "v1") != schema_version
    if schema_changed:
        # schema 变更视为全量 new
        all_files = [f"raw/{f.name}" for f in list_raw_files(raw_dir)]
        new_files = all_files
        changed_files = []

    return {
        "schema_version_changed": schema_changed,
        "new_schema_version": schema_version,
        "new": new_files,
        "changed": changed_files,
        "unchanged": unchanged_files,
        "affected_pages": sorted(affected),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="raw 文件哈希比对")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    args = parser.parse_args()
    result = diff(normalize_path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
