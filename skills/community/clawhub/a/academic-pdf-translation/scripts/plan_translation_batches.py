"""把冻结的原文单元编成翻译批次。

检查层不变：`source_units.json` 的单元 ID、原文、页码和坐标全部保持原样。
本模块只决定“一次交给模型多少个单元”，并为每个批次准备完整上下文。

分批规则：

- 按章节、标题和页面顺序推进，不重排单元；
- 标题不与它后面的第一段拆开；
- 图题、表题与相邻说明尽量同批；
- 跨页续句必须同批；
- 每批默认 8～20 个单元、约 8000～12000 字符。
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import perf_trace
from _common import SkillError, load_json, sha256_file, write_json
from translation_cache import (
    DEFAULT_PROMPT_VERSION,
    TRANSLATION_STRATEGY_VERSION,
    batch_cache_key,
    terminology_hash,
    unit_content_hash,
)
from translation_truthfulness import KEEP_SOURCE_CODES

PLAN_SCHEMA_VERSION = "1.0"
PLAN_FILE_NAME = "translation-plan.json"
BATCH_DIR_NAME = "translation-batches"

DEFAULT_MIN_UNITS = 8
DEFAULT_MAX_UNITS = 20
DEFAULT_TARGET_CHARS = 10000
DEFAULT_MAX_CHARS = 12000
CONTEXT_UNITS = 2
CONTEXT_CHARS = 320

SENTENCE_END_RE = re.compile(r"[.!?。！？][\"'”’)\]]*\s*$")
CAPTION_KINDS = {"figure-or-caption", "table-or-caption"}


def _kind(unit: dict[str, Any]) -> str:
    return str(unit.get("kind") or unit.get("kind_hint") or "body").lower()


def _source(unit: dict[str, Any]) -> str:
    return str(unit.get("source") or "")


def _unit_page(unit: dict[str, Any]) -> int:
    try:
        return int(unit.get("page") or 0)
    except (TypeError, ValueError):
        return 0


def _continues_across_pages(
    previous: dict[str, Any],
    following: dict[str, Any],
) -> bool:
    """上一单元在页末断句、下一单元在下一页续写时视为同一句。"""

    if _kind(previous) != "body" or _kind(following) != "body":
        return False
    if _unit_page(following) != _unit_page(previous) + 1:
        return False
    return not SENTENCE_END_RE.search(_source(previous).rstrip())


def _may_break_before(
    previous: dict[str, Any],
    following: dict[str, Any],
) -> bool:
    """判断能否在两个单元之间切开批次。"""

    if _kind(previous) == "heading":
        return False
    if _kind(previous) in CAPTION_KINDS and _kind(following) not in {
        "heading"
    }:
        return False
    return not _continues_across_pages(previous, following)


def _document_outline(units: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "unit_id": str(unit.get("id") or ""),
            "page": _unit_page(unit),
            "heading_level": unit.get("heading_level"),
            "text": _source(unit),
        }
        for unit in units
        if _kind(unit) == "heading"
    ]


def _document_title(units: list[dict[str, Any]]) -> str:
    first_page = min((_unit_page(unit) for unit in units), default=0)
    opening = [unit for unit in units if _unit_page(unit) == first_page]
    for unit in opening:
        if _kind(unit) == "heading" and _source(unit).strip():
            return _source(unit).strip()
    for unit in opening:
        if _source(unit).strip():
            return _source(unit).strip()
    return ""


def _abstract_excerpt(units: list[dict[str, Any]], limit: int = 900) -> str:
    first_page = min((_unit_page(unit) for unit in units), default=0)
    body = [
        _source(unit)
        for unit in units
        if _unit_page(unit) <= first_page + 1
        and _kind(unit) == "body"
        and _source(unit).strip()
    ]
    return " ".join(body)[:limit]


def _section_for(
    unit_index: int,
    units: list[dict[str, Any]],
) -> str:
    for index in range(unit_index, -1, -1):
        if _kind(units[index]) == "heading":
            return _source(units[index]).strip()
    return ""


def _context_slice(
    units: list[dict[str, Any]],
    *,
    from_end: bool,
) -> list[dict[str, Any]]:
    selected = units[-CONTEXT_UNITS:] if from_end else units[:CONTEXT_UNITS]
    return [
        {
            "id": str(unit.get("id") or ""),
            "kind": _kind(unit),
            "source": (
                _source(unit)[-CONTEXT_CHARS:]
                if from_end
                else _source(unit)[:CONTEXT_CHARS]
            ),
        }
        for unit in selected
    ]


def group_units(
    units: list[dict[str, Any]],
    *,
    min_units: int = DEFAULT_MIN_UNITS,
    max_units: int = DEFAULT_MAX_UNITS,
    target_chars: int = DEFAULT_TARGET_CHARS,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> list[list[int]]:
    """返回每批的单元下标列表，顺序与原文一致。"""

    if not units:
        return []
    groups: list[list[int]] = []
    current: list[int] = []
    current_chars = 0

    for index, unit in enumerate(units):
        length = len(_source(unit))
        if current:
            previous = units[current[-1]]
            breakable = _may_break_before(previous, unit)
            over_units = len(current) >= max_units
            over_chars = current_chars + length > max_chars
            at_section_start = (
                _kind(unit) == "heading"
                and current_chars >= target_chars
                and len(current) >= min_units
            )
            if breakable and (over_units or over_chars or at_section_start):
                groups.append(current)
                current = []
                current_chars = 0
        current.append(index)
        current_chars += length

    if current:
        groups.append(current)
    return groups


def _timed_plan_translation_batches(
    job_dir: Path,
    *,
    min_units: int = DEFAULT_MIN_UNITS,
    max_units: int = DEFAULT_MAX_UNITS,
    target_chars: int = DEFAULT_TARGET_CHARS,
    max_chars: int = DEFAULT_MAX_CHARS,
    model: str | None = None,
    prompt_version: str = DEFAULT_PROMPT_VERSION,
    require_terminology_review: bool = True,
) -> dict[str, Any]:
    job_dir = Path(job_dir).resolve()
    job = load_json(job_dir / "job.json")
    files = job.get("files", {})
    translation_path = job_dir / files["translation"]
    source_units_path = job_dir / files.get(
        "source_units",
        "source_units.json",
    )
    if not source_units_path.is_file():
        raise SkillError("缺少 source_units.json，请先初始化作业")
    translation = load_json(translation_path)
    units = [
        unit
        for unit in translation.get("units", [])
        if isinstance(unit, dict) and str(unit.get("id") or "")
    ]
    if not units:
        raise SkillError("translation.json 没有可编排的单元")
    terminology_reviewed = translation.get("terminology_reviewed") is True
    if require_terminology_review and not terminology_reviewed:
        raise SkillError(
            "translation.terminology_reviewed 尚未设为 true；"
            "术语表确认之前不得正式编排或执行翻译批次。"
            "只想预览分批时用 --preview。"
        )

    terminology = translation.get("terminology", [])
    terminology_sha256 = terminology_hash(terminology)
    target_language = str(translation.get("target_language") or "")
    source_language = str(translation.get("source_language") or "")
    title = _document_title(units)
    outline = _document_outline(units)
    abstract = _abstract_excerpt(units)

    groups = group_units(
        units,
        min_units=min_units,
        max_units=max_units,
        target_chars=target_chars,
        max_chars=max_chars,
    )
    batch_dir = job_dir / BATCH_DIR_NAME
    batch_dir.mkdir(parents=True, exist_ok=True)
    # 旧批次文件不先删：先算出新计划，再删掉不在新计划里的文件。
    # 先删再按译文内容反推历史，会把“已完成”这件事变成猜测。
    previous_plan = (
        load_json(job_dir / PLAN_FILE_NAME)
        if (job_dir / PLAN_FILE_NAME).is_file()
        else {}
    )
    previous_by_key = {
        str(entry.get("cache_key") or ""): entry
        for entry in previous_plan.get("batches", [])
        if isinstance(entry, dict) and entry.get("status") == "applied"
    }

    entries: list[dict[str, Any]] = []
    for order, indices in enumerate(groups, 1):
        batch_units = [units[index] for index in indices]
        batch_id = f"batch-{order:04d}"
        unit_hashes = [unit_content_hash(unit) for unit in batch_units]
        cache_key = batch_cache_key(
            unit_hashes=unit_hashes,
            target_language=target_language,
            terminology_sha256=terminology_sha256,
            prompt_version=prompt_version,
            model=model,
        )
        previous_units = [units[index] for index in groups[order - 2]] if order > 1 else []
        next_units = (
            [units[index] for index in groups[order]]
            if order < len(groups)
            else []
        )
        payload = {
            "schema_version": PLAN_SCHEMA_VERSION,
            "batch_id": batch_id,
            "index": order,
            "batch_count": len(groups),
            "cache_key": cache_key,
            "source_language": source_language,
            "target_language": target_language,
            "document": {
                "title": title,
                "abstract_excerpt": abstract,
                "outline": outline,
            },
            "section_heading": _section_for(indices[0], units),
            "terminology": terminology,
            "terminology_reviewed": bool(
                translation.get("terminology_reviewed")
            ),
            "context": {
                "previous_tail": _context_slice(
                    previous_units,
                    from_end=True,
                ),
                "next_head": _context_slice(next_units, from_end=False),
            },
            "instructions": [
                "只翻译 units 中的每一条，保持整篇上下文和统一术语。",
                "不得修改 id、source、page 或 source_bbox。",
                "每个单元恰好返回一次，数量必须与 units 一致。",
                "required_anchors 中的数字、统计量、引文编号、缩写、"
                "DOI 和 URL 必须在译文中保留。",
                "普通正文、摘要、标题和章节标题必须给出目标语言译文，"
                "不能整单元保留原文，也不能把原文原样填进 translation。",
                "确需保留原文时，把 translation 留空，填写结构化 "
                "keep_source_code（取值见 keep_source_codes），"
                "keep_source_reason 只作补充说明，单独不能豁免。",
                "context 只用于理解上下文，不要翻译其中的内容。",
            ],
            "keep_source_codes": list(KEEP_SOURCE_CODES),
            "response_format": {
                "type": "array",
                "item": {
                    "id": "<units[] 中的单元 id>",
                    "translation": "<目标语言译文，或保留原文时为 null>",
                    "keep_source_code": (
                        "<null 或 keep_source_codes 中的一个取值>"
                    ),
                    "keep_source_reason": "<null 或补充说明>",
                    "review_flags": [],
                },
            },
            "units": [
                {
                    "id": str(unit.get("id") or ""),
                    "page": _unit_page(unit),
                    "kind": _kind(unit),
                    # 元素角色随批次一起下发：写回时的真实性检查按它免除
                    # 作者、单位、出版元数据和题录的目标语言占比门槛。
                    # 批次文件里没有它，这些单元在写回那一关就无处可查。
                    "element_role": str(unit.get("element_role") or ""),
                    "heading_level": unit.get("heading_level"),
                    "source": _source(unit),
                    # 坐标必须随批次一起给出：写回时要用它核对
                    # keep_source_code=bibliography-entry 的保留区域证据。
                    "source_bbox": unit.get("source_bbox"),
                    "required_anchors": unit.get("required_anchors") or {},
                    "review_flags": unit.get("review_flags") or [],
                }
                for unit in batch_units
            ],
        }
        batch_path = batch_dir / f"{batch_id}.json"
        write_json(batch_path, payload)
        entry = {
            "batch_id": batch_id,
            "index": order,
            "file": f"{BATCH_DIR_NAME}/{batch_id}.json",
            "cache_key": cache_key,
            "unit_count": len(batch_units),
            "source_chars": sum(
                len(_source(unit)) for unit in batch_units
            ),
            "first_unit_id": str(batch_units[0].get("id") or ""),
            "last_unit_id": str(batch_units[-1].get("id") or ""),
            "pages": sorted({_unit_page(unit) for unit in batch_units}),
            "section_heading": payload["section_heading"],
            "status": "pending",
            "applied_at": None,
            "retries": 0,
            "applied_model": None,
            "applied_unit_ids": [],
        }
        # 完成过的批次凭 cache_key 与单元边界继承既有证据，
        # 不看 translation.json 里现在有没有译文。
        carried = previous_by_key.get(cache_key)
        if (
            carried is not None
            and carried.get("unit_count") == entry["unit_count"]
            and carried.get("first_unit_id") == entry["first_unit_id"]
            and carried.get("last_unit_id") == entry["last_unit_id"]
        ):
            for key in (
                "status",
                "applied_at",
                "retries",
                "applied_model",
                "applied_unit_ids",
                "elapsed_seconds",
                "input_tokens",
                "output_tokens",
            ):
                if key in carried:
                    entry[key] = carried[key]
        entries.append(entry)

    keep = {f"{entry['batch_id']}.json" for entry in entries}
    for stale in batch_dir.glob("batch-*.json"):
        if stale.name not in keep:
            stale.unlink()

    plan = {
        "schema_version": PLAN_SCHEMA_VERSION,
        "strategy_version": TRANSLATION_STRATEGY_VERSION,
        "prompt_version": prompt_version,
        "model": model,
        "terminology_reviewed": terminology_reviewed,
        "cache_scope": (
            "model-bound" if model else "disabled-no-model-recorded"
        ),
        "source_units_sha256": sha256_file(source_units_path),
        "translation_sha256": sha256_file(translation_path),
        "terminology_sha256": terminology_sha256,
        "source_language": source_language,
        "target_language": target_language,
        "unit_count": len(units),
        "batch_count": len(groups),
        "batching": {
            "min_units": min_units,
            "max_units": max_units,
            "target_chars": target_chars,
            "max_chars": max_chars,
        },
        "batches": entries,
        "note": (
            "逐单元校验，按批次翻译。单元 ID 与原文保持冻结；"
            "批次只决定一次交给模型多少内容。"
        ),
    }
    write_json(job_dir / PLAN_FILE_NAME, plan)
    return plan


def load_plan(job_dir: Path) -> dict[str, Any]:
    path = Path(job_dir).resolve() / PLAN_FILE_NAME
    if not path.is_file():
        raise SkillError(
            "缺少 translation-plan.json，请先运行 plan_translation_batches.py"
        )
    return load_json(path)



def plan_translation_batches(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("plan_batches"):
        return _timed_plan_translation_batches(*args, **kwargs)



#: 并行翻译代理数上限。翻译是并行收益最大的一段；超过 5 个
#: 术语与文风的协调成本开始超过节省的时间。
MAX_TRANSLATORS = 5


def assign_batches(batch_ids: list[str], translators: int) -> list[dict]:
    """把批次按原顺序切成连续段，分给 N 个翻译代理。

    连续分配（不是轮转）：每个代理拿到的是相邻页面的连续段落，
    文风更容易保持一致。术语一致性不靠分配方式——术语表在编排时
    已冻结并钉哈希，写回一关还会校验。
    """

    n = max(1, min(MAX_TRANSLATORS, int(translators)))
    n = min(n, len(batch_ids)) or 1
    base, extra = divmod(len(batch_ids), n)
    assignments: list[dict] = []
    start = 0
    for index in range(n):
        size = base + (1 if index < extra else 0)
        assignments.append(
            {
                "translator": index + 1,
                "batch_ids": batch_ids[start : start + size],
            }
        )
        start += size
    return assignments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--min-units", type=int, default=DEFAULT_MIN_UNITS)
    parser.add_argument("--max-units", type=int, default=DEFAULT_MAX_UNITS)
    parser.add_argument(
        "--target-chars",
        type=int,
        default=DEFAULT_TARGET_CHARS,
    )
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument(
        "--model",
        help="实际执行翻译的模型标识；不提供时不会生成可复用的正式缓存",
    )
    parser.add_argument(
        "--translators",
        type=int,
        default=None,
        help="并行翻译代理数（1..5）。翻译可以并行，写回必须串行："
        "每个代理只写自己批次的结果文件，最后由唯一写回者按序执行",
    )
    parser.add_argument("--status", action="store_true")
    parser.add_argument(
        "--preview",
        action="store_true",
        help="术语表确认之前预览分批结果，不写任何文件",
    )
    args = parser.parse_args()
    try:
        if args.status:
            plan = load_plan(args.job_dir)
        elif args.preview:
            job_dir = args.job_dir.resolve()
            translation = load_json(
                job_dir
                / load_json(job_dir / "job.json")["files"]["translation"]
            )
            units = [
                unit
                for unit in translation.get("units", [])
                if isinstance(unit, dict)
            ]
            groups = group_units(
                units,
                min_units=args.min_units,
                max_units=args.max_units,
                target_chars=args.target_chars,
                max_chars=args.max_chars,
            )
            print(f"预览：单元 {len(units)} 个，将编成 {len(groups)} 批")
            for order, indices in enumerate(groups, 1):
                chars = sum(len(_source(units[i])) for i in indices)
                print(
                    f"  batch-{order:04d}  单元 {len(indices):>3}"
                    f"  字符 {chars:>6}"
                )
            print("预览不写文件。确认术语表后再正式编排。")
            return 0
        else:
            if not 1 <= args.min_units <= args.max_units <= 200:
                raise SkillError("单元数范围必须满足 1 <= min <= max <= 200")
            if not 1000 <= args.target_chars <= args.max_chars <= 40000:
                raise SkillError(
                    "字符范围必须满足 1000 <= target <= max <= 40000"
                )
            plan = plan_translation_batches(
                args.job_dir,
                min_units=args.min_units,
                max_units=args.max_units,
                target_chars=args.target_chars,
                max_chars=args.max_chars,
                model=args.model,
            )
        if args.translators is not None:
            if not 1 <= args.translators <= MAX_TRANSLATORS:
                raise SkillError(
                    f"--translators 必须在 1..{MAX_TRANSLATORS} 之间；"
                    "翻译并行、写回串行，超过 5 个协调成本盖过收益"
                )
            assignments = assign_batches(
                [batch["batch_id"] for batch in plan["batches"]],
                args.translators,
            )
            plan["assignments"] = assignments
            plan_path = args.job_dir / "translation-plan.json"
            write_json(plan_path, plan)
            print(f"并行分配（{len(assignments)} 个翻译代理，写回仍须串行）:")
            for item in assignments:
                print(
                    f"  代理 {item['translator']}: "
                    + ", ".join(item["batch_ids"])
                )
        pending = [
            batch
            for batch in plan["batches"]
            if batch["status"] != "applied"
        ]
        print(
            f"单元 {plan['unit_count']} 个，批次 {plan['batch_count']} 个，"
            f"待翻译 {len(pending)} 批"
        )
        for batch in plan["batches"]:
            print(
                f"  {batch['batch_id']}  {batch['status']:<8}"
                f"  单元 {batch['unit_count']:>3}"
                f"  字符 {batch['source_chars']:>6}"
                f"  页 {batch['pages']}"
            )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
