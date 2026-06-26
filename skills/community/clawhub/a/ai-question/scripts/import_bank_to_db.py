#!/usr/bin/env python3
"""将 JSON 或 Excel 题库导入 SQLite 刷题数据库。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _quizai_root import quizai_root

ROOT = quizai_root()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.database import SessionLocal, init_db  # noqa: E402
from app.services.ai_generator import prepare_export_questions  # noqa: E402
from app.services.bank_io import parse_import_file  # noqa: E402
from app.services.bank_store import save_bank_payload  # noqa: E402


def _load_json_payload(path: Path, *, shuffle: bool) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("JSON 根节点必须是对象")
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise ValueError("questions 必须是非空数组")
    data["questions"] = prepare_export_questions(questions, shuffle=shuffle)
    data.setdefault("source_files", "skill-import")
    return data


def _load_payload(path: Path, *, shuffle: bool) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return _load_json_payload(path, shuffle=shuffle)
    if suffix in {".xlsx", ".xlsm"}:
        payload = parse_import_file(path.name, path.read_bytes())
        payload["source_files"] = "skill-import"
        return payload
    raise ValueError("仅支持 .json、.xlsx、.xlsm 文件")


def main() -> int:
    parser = argparse.ArgumentParser(description="导入题库到 SQLite 刷题系统")
    parser.add_argument("input", help="题库 JSON 或 Excel 路径")
    parser.add_argument(
        "--no-shuffle",
        action="store_true",
        help="JSON 导入时不打乱选项（Excel 按文件内容导入）",
    )
    args = parser.parse_args()

    src = Path(args.input).expanduser().resolve()
    if not src.is_file():
        print(f"错误: 文件不存在 {src}", file=sys.stderr)
        return 1

    try:
        payload = _load_payload(src, shuffle=not args.no_shuffle)
        init_db()
        with SessionLocal() as db:
            bank = save_bank_payload(db, payload)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return 1

    print(f"已导入刷题系统: {bank.title}")
    print(f"  题库 ID: {bank.id}")
    print(f"  分类: {bank.category}")
    print(f"  题数: {bank.question_count}")
    print(f"  我的题库: http://127.0.0.1:8000/banks")
    print(f"  开始刷题: http://127.0.0.1:8000/practice/{bank.id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
