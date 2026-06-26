#!/usr/bin/env python3
"""将非标准格式题库资料转换为规范 Excel 题库。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _quizai_root import quizai_root

ROOT = quizai_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.bank_io import export_bank_xlsx  # noqa: E402
from app.services.bank_normalizer import normalize_bank_from_file  # noqa: E402

SUPPORTED = {".pdf", ".doc", ".docx", ".txt", ".md", ".xlsx", ".xlsm"}


def _infer_title(path: Path, payload: dict) -> str:
    if payload.get("title"):
        return str(payload["title"])
    return path.stem[:200] or "规范题库"


def main() -> int:
    parser = argparse.ArgumentParser(description="规范非标准题库为 Excel 格式")
    parser.add_argument("input", help="输入文件（pdf/doc/docx/txt/md/xlsx）")
    parser.add_argument("-o", "--output", required=True, help="输出 .xlsx 路径")
    parser.add_argument("--title", default="", help="题库名称")
    parser.add_argument("--category", default="未分类", help="分类")
    args = parser.parse_args()

    path = Path(args.input).expanduser().resolve()
    if not path.is_file():
        print(f"错误: 文件不存在 {path}", file=sys.stderr)
        return 1
    if path.suffix.lower() not in SUPPORTED:
        allowed = ", ".join(sorted(SUPPORTED))
        print(f"错误: 不支持 {path.suffix}，允许: {allowed}", file=sys.stderr)
        return 1

    try:
        payload = normalize_bank_from_file(
            path,
            title=args.title.strip(),
            category=args.category.strip() or "未分类",
        )
    except Exception as e:
        print(f"错误: 规范转换失败: {e}", file=sys.stderr)
        return 1

    questions = payload.get("questions") or []
    if not questions:
        print("错误: 未识别到有效题目", file=sys.stderr)
        return 1

    title = args.title.strip() or _infer_title(path, payload)
    category = payload.get("category") or "未分类"
    description = payload.get("description") or f"规范转换 · {len(questions)} 道题"

    data = export_bank_xlsx(title, category, description, questions)
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)

    type_count = {}
    for q in questions:
        type_count[q["q_type"]] = type_count.get(q["q_type"], 0) + 1

    print(f"已规范题库: {out}")
    print(f"  名称: {title}")
    print(f"  题数: {len(questions)}")
    print(f"  题型: 单选 {type_count.get('single', 0)} / 判断 {type_count.get('judge', 0)} / 多选 {type_count.get('multiple', 0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
