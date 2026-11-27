#!/usr/bin/env python3
"""审计准备导入 FastGPT 或兼容自托管实例的 Markdown 与文本知识库。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SIGNED_URL_PATTERN = re.compile(r"https?://[^\s)>'\"]+[?&](?:x-amz-signature|signature|token|expires|authkey|ossaccesskeyid)=", re.I)
RAW_CITATION_PATTERN = re.compile(r"(?:\b[0-9a-f]{20,}\b|\(CITE\)|\[[0-9a-f]{12,})", re.I)
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME)\b|待补充|仅供测试", re.I)
PRIVATE_IPV4_PATTERN = re.compile(r"(?<!\d)(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})(?!\d)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="待导入知识库目录")
    parser.add_argument("--max-chars", type=int, default=2500)
    parser.add_argument("--min-chars", type=int, default=60)
    parser.add_argument("--extensions", default=".md,.txt")
    parser.add_argument("--flag-private-ip", action="store_true", help="按项目安全策略选择性标记私网 IPv4；默认不检查")
    parser.add_argument("--json", action="store_true", dest="json_output")
    parser.add_argument("--strict", action="store_true", help="把 warning 也视为失败")
    return parser.parse_args()


def issue(code: str, severity: str, message: str, path: str = "", suggested_fix: str = "") -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message, "path": path, "suggested_fix": suggested_fix}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def audit(args: argparse.Namespace) -> dict[str, Any]:
    root = args.directory.resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    extensions = {item.strip().lower() for item in args.extensions.split(",") if item.strip()}
    files = sorted(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in extensions)
    diagnostics: list[dict[str, str]] = []
    items: list[dict[str, Any]] = []
    hashes: dict[str, list[str]] = defaultdict(list)
    basenames: dict[str, list[str]] = defaultdict(list)

    if not files:
        diagnostics.append(issue("KB001", "error", "目录下未找到知识文件", str(root), "检查目录和 --extensions"))

    for path in files:
        relative = path.relative_to(root).as_posix()
        basenames[path.name.lower()].append(relative)
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            diagnostics.append(issue("KB002", "error", f"不是有效 UTF-8：{exc}", relative, "转换为 UTF-8 后重新审计"))
            continue

        digest = hashlib.sha256(normalize(text).encode("utf-8")).hexdigest()
        hashes[digest].append(relative)
        character_count = len(text.strip())
        heading_count = sum(1 for line in text.splitlines() if line.lstrip().startswith("#"))

        if character_count < args.min_chars:
            diagnostics.append(issue("KB010", "warning", f"文档过短：{character_count} 字符", relative, "确认主题是否完整，或合并到同一决策主题"))
        if character_count > args.max_chars:
            diagnostics.append(issue("KB011", "warning", f"文档过长：{character_count} > {args.max_chars} 字符", relative, "按用户决策拆成语义完整的主题文档"))
        if path.suffix.lower() == ".md" and heading_count == 0:
            diagnostics.append(issue("KB012", "warning", "Markdown 没有标题", relative, "增加包含用户常用词和主题的标题"))
        if SIGNED_URL_PATTERN.search(text):
            diagnostics.append(issue("KB020", "error", "包含疑似签名或临时 URL", relative, "替换为稳定官方 URL 或完整菜单路径"))
        if RAW_CITATION_PATTERN.search(text):
            diagnostics.append(issue("KB021", "warning", "包含原始 ID 或 CITE 标记", relative, "移除内部引用标记，使用平台真实引用元数据"))
        if PLACEHOLDER_PATTERN.search(text):
            diagnostics.append(issue("KB022", "warning", "包含占位或测试用语", relative, "补全或从发布知识集中移除"))
        if args.flag_private_ip and PRIVATE_IPV4_PATTERN.search(text):
            diagnostics.append(issue("KB023", "warning", "包含私网 IPv4", relative, "根据项目安全策略确认是否允许；对外样例应使用保留示例地址"))

        items.append({"path": relative, "characters": character_count, "headings": heading_count, "sha256": digest})

    for paths in [paths for paths in hashes.values() if len(paths) > 1]:
        diagnostics.append(issue("KB030", "error", f"正文归一化后完全重复：{paths}", ", ".join(paths), "每个主题只保留一个维护版本并重建索引"))
    for paths in [paths for paths in basenames.values() if len(paths) > 1]:
        diagnostics.append(issue("KB031", "warning", f"不同目录存在同名文件：{paths}", ", ".join(paths), "确认是否为重复版本或增加明确领域名称"))

    counts = Counter(item["severity"] for item in diagnostics)
    summary = {
        "root": str(root),
        "files": len(items),
        "characters": sum(item["characters"] for item in items),
        "largest": sorted(items, key=lambda item: item["characters"], reverse=True)[:5],
        "diagnostic_counts": dict(counts),
    }
    return {"schema_version": "1.0", "summary": summary, "diagnostics": diagnostics}


def main() -> int:
    args = parse_args()
    try:
        report = audit(args)
    except Exception as exc:
        report = {
            "schema_version": "1.0",
            "summary": {"diagnostic_counts": {"error": 1}},
            "diagnostics": [issue("KB000", "error", f"{type(exc).__name__}: {exc}", str(args.directory), "检查目录、权限和编码")],
        }

    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        for item in report["diagnostics"]:
            print(f"[{item['severity'].upper()}][{item['code']}][{item['path']}] {item['message']}")
            if item["suggested_fix"]:
                print(f"  修复建议：{item['suggested_fix']}")

    has_errors = any(item["severity"] == "error" for item in report["diagnostics"])
    has_warnings = any(item["severity"] == "warning" for item in report["diagnostics"])
    return 1 if has_errors or (args.strict and has_warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
