#!/usr/bin/env python3
"""Validate PII-safe indexes. English is normative; ZH-CN is paired. / 验证索引不包含 PII 文档；英文为规范文本，简体中文为配对译文。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import runtime_paths


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_generated(out_dir: Path) -> list[str]:
    errors = []
    manifest_path = out_dir / "manifest.json"
    documents_path = out_dir / "documents.jsonl"
    if not manifest_path.exists():
        return [f"Missing manifest / 缺少 manifest: {manifest_path}"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    excluded = set(manifest.get("excluded_pii_paths", []))
    for document in load_jsonl(documents_path):
        path = document.get("path", "")
        source_paths = set(document.get("source_paths", [path]))
        tags = {str(tag).lower() for tag in document.get("tags", [])}
        if path in excluded:
            errors.append(f"PII-excluded path is indexed / 已索引应排除的 PII 路径: {path}")
        leaked_sources = source_paths & excluded
        if leaked_sources:
            errors.append(
                f"PII-excluded source path is indexed / 已索引应排除的 PII 源路径 in {document.get('record_id', path)}: "
                + ", ".join(sorted(leaked_sources))
            )
        if "pii" in tags:
            errors.append(f"PII tag is indexed / 已索引 PII 标签: {path}")
        searchable = json.dumps(
            {
                "summary": document.get("summary", ""),
                "key_points": document.get("key_points", []),
                "search_text": document.get("search_text", ""),
                "display_snippet": document.get("display_snippet", ""),
            },
            ensure_ascii=False,
        )
        for excluded_path in excluded:
            if excluded_path and excluded_path in searchable:
                errors.append(
                    f"PII-excluded path leaks into searchable fields / 应排除的 PII 路径泄漏到可检索字段 for "
                    f"{document.get('record_id', path)}: {excluded_path}"
                )
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--generated",
        type=Path,
        default=runtime_paths.DEFAULT_PATHS.index_dir,
        help="Generated index directory. / 生成的索引目录。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    errors = validate_generated(args.generated)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        raise SystemExit(1)
    print("Privacy validation passed. / 隐私验证通过。")


if __name__ == "__main__":
    main()
