#!/usr/bin/env python3
"""从资料文件提取纯文本，供对话框模型阅读出题。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _quizai_root import quizai_root

ROOT = quizai_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.parser import SUPPORTED, extract_text  # noqa: E402

SKILL_INPUT = {".pdf", ".doc", ".docx", ".txt", ".md"}


def main() -> int:
    parser = argparse.ArgumentParser(description="提取资料文本")
    parser.add_argument("inputs", nargs="+", help="资料文件路径")
    parser.add_argument("-o", "--output", help="输出 txt 路径（默认打印到 stdout）")
    args = parser.parse_args()

    parts: list[str] = []
    for raw in args.inputs:
        path = Path(raw).expanduser().resolve()
        if not path.is_file():
            print(f"错误: 文件不存在 {path}", file=sys.stderr)
            return 1
        suffix = path.suffix.lower()
        if suffix not in SKILL_INPUT or suffix not in SUPPORTED:
            allowed = ", ".join(sorted(SKILL_INPUT))
            print(f"错误: 不支持 {suffix}，允许: {allowed}", file=sys.stderr)
            return 1
        try:
            text = extract_text(path).strip()
            if text:
                parts.append(f"=== {path.name} ===\n{text}")
        except Exception as e:
            print(f"错误: 解析 {path.name} 失败: {e}", file=sys.stderr)
            return 1

    full = "\n\n".join(parts).strip()
    if not full:
        print("错误: 未能提取有效文本", file=sys.stderr)
        return 1

    if args.output:
        out = Path(args.output).expanduser().resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(full, encoding="utf-8")
        print(f"已提取文本: {out} ({len(full)} 字)")
    else:
        print(full)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
