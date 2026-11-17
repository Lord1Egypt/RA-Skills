"""登记术语表并确认锁定。

`translation.terminology_reviewed` 必须先变成 `true`，编排批次的命令才肯
正式生成批次。这里是它唯一的写入口，不需要手改 `translation.json`。

用法::

    # 只确认术语表（可以为空）
    python3 scripts/set_terminology.py /path/to/job --reviewed

    # 先登记术语，再确认
    python3 scripts/set_terminology.py /path/to/job \\
      --term "meaning in life=人生意义" \\
      --term "PIL=PIL" \\
      --reviewed

术语写成 `原文=译文`。译文与原文相同表示这一条按原文保留，翻译时可以对
它使用 `keep_source_code=required-original-term`。

术语表在编排批次之前锁定，锁定后不在批次之间改动。批次计划已经存在时改动
术语会让已完成批次与新批次用上两套术语，命令直接拒绝；确需重来时显式加
`--force`，然后重新编排全部批次。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import SkillError, load_json, write_json  # noqa: E402

PLAN_FILE_NAME = "translation-plan.json"


def _parse_term(value: str) -> dict[str, str]:
    if "=" not in value:
        raise SkillError(f"术语格式必须是 原文=译文，收到: {value!r}")
    source, target = value.split("=", 1)
    source = source.strip()
    target = target.strip()
    if not source or not target:
        raise SkillError(f"术语的原文和译文都不能为空: {value!r}")
    return {"source": source, "target": target}


def _merge_terms(
    existing: list[Any],
    added: list[dict[str, str]],
) -> list[dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}
    for entry in existing:
        if isinstance(entry, dict) and str(entry.get("source") or "").strip():
            merged[str(entry["source"]).strip()] = {
                "source": str(entry["source"]).strip(),
                "target": str(entry.get("target") or "").strip(),
            }
    for entry in added:
        merged[entry["source"]] = entry
    return [merged[key] for key in sorted(merged)]


def set_terminology(
    job_dir: Path,
    terms: list[str],
    *,
    reviewed: bool = False,
    force: bool = False,
) -> dict[str, Any]:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    translation_path = job_dir / job["files"]["translation"]
    if not translation_path.is_file():
        raise SkillError("缺少 translation.json，请先初始化作业")
    translation = load_json(translation_path)

    parsed = [_parse_term(value) for value in terms]
    before = translation.get("terminology") or []
    after = _merge_terms(before, parsed) if parsed else list(before)
    if parsed and after != before and not force:
        if (job_dir / PLAN_FILE_NAME).is_file():
            raise SkillError(
                "批次计划已经存在；术语表锁定后不在批次之间改动。"
                "确需重来时加 --force，并重新编排全部批次"
            )
    translation["terminology"] = after
    if reviewed:
        translation["terminology_reviewed"] = True
    write_json(translation_path, translation)
    return {
        "terminology": after,
        "terminology_reviewed": bool(translation.get("terminology_reviewed")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="登记术语表并把 terminology_reviewed 设为 true"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--term",
        action="append",
        default=[],
        metavar="原文=译文",
        help="可重复使用",
    )
    parser.add_argument(
        "--reviewed",
        action="store_true",
        help="确认术语表已锁定；编排批次之前必须执行一次",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="批次计划已存在时仍改动术语；改完必须重新编排全部批次",
    )
    args = parser.parse_args()
    try:
        result = set_terminology(
            args.job_dir,
            args.term,
            reviewed=args.reviewed,
            force=args.force,
        )
        print(f"术语条目: {len(result['terminology'])}")
        print(
            "术语表已确认"
            if result["terminology_reviewed"]
            else "术语表尚未确认；编排批次前请加 --reviewed"
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
