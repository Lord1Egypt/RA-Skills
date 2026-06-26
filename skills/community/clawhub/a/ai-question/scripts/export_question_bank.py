#!/usr/bin/env python3
"""将对话框模型生成的 JSON 题库导出为规范 Excel。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _quizai_root import quizai_root

ROOT = quizai_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.ai_generator import prepare_export_questions  # noqa: E402
from app.services.bank_io import export_bank_xlsx  # noqa: E402


def _load_payload(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("JSON 根节点必须是对象")
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("questions 必须是非空数组")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="导出 JSON 题库为 Excel")
    parser.add_argument("input", help="题库 JSON 文件路径")
    parser.add_argument("-o", "--output", required=True, help="输出 .xlsx 路径")
    parser.add_argument("--no-shuffle", action="store_true", help="不打乱选项顺序")
    args = parser.parse_args()

    src = Path(args.input).expanduser().resolve()
    if not src.is_file():
        print(f"错误: 文件不存在 {src}", file=sys.stderr)
        return 1

    try:
        payload = _load_payload(src)
        questions = prepare_export_questions(
            payload["questions"],
            shuffle=not args.no_shuffle,
        )
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

    title = str(payload.get("title") or "AI 生成题库").strip()[:200]
    category = str(payload.get("category") or "未分类").strip()[:100]
    description = str(payload.get("description") or f"基于资料自动生成 · {len(questions)} 道题")[:500]

    data = export_bank_xlsx(title, category, description, questions)
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)

    type_count: dict[str, int] = {}
    for q in questions:
        t = q.get("q_type", "single")
        type_count[t] = type_count.get(t, 0) + 1

    print(f"已导出题库: {out}")
    print(f"  名称: {title}")
    print(f"  题数: {len(questions)}")
    print(f"  题型: 单选 {type_count.get('single', 0)} / 判断 {type_count.get('judge', 0)} / 多选 {type_count.get('multiple', 0)}")
    print("  下一步: 询问用户是否导入刷题系统 (import_bank_to_db.py)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
