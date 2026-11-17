from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import perf_trace
from _common import SkillError, load_json, sha256_file, write_json
from content_anchors import required_anchors
from semantic_markers import infer_review_flags
from translation_truthfulness import SCOPE_NOTE_PENDING

SENTENCE_BREAK_RE = re.compile(r"(?<=[.!?])(?:[\"')\]]+)?\s+")
SPACE_RE = re.compile(r"\s+")


def _clean_block_text(text: str) -> str:
    lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
    merged: list[str] = []
    for line in lines:
        if (
            merged
            and merged[-1].endswith("-")
            and line[:1].islower()
            and merged[-1][-2:-1].isalpha()
        ):
            merged[-1] = merged[-1][:-1] + line
        else:
            merged.append(line)
    return SPACE_RE.sub(" ", " ".join(merged)).strip()


def _split_text(text: str, max_chars: int) -> list[str]:
    text = _clean_block_text(text)
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    sentences = [
        sentence.strip()
        for sentence in SENTENCE_BREAK_RE.split(text)
        if sentence.strip()
    ]
    if len(sentences) <= 1:
        return [
            text[start : start + max_chars].strip()
            for start in range(0, len(text), max_chars)
            if text[start : start + max_chars].strip()
        ]
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        proposed = f"{current} {sentence}".strip()
        if current and len(proposed) > max_chars:
            chunks.append(current)
            current = sentence
        else:
            current = proposed
    if current:
        chunks.append(current)
    return chunks


def _timed_build_source_units(
    structure: dict[str, Any],
    *,
    max_chars: int = 900,
) -> dict[str, Any]:
    units: list[dict[str, Any]] = []
    for page in structure.get("pages", []):
        page_number = int(page["page"])
        page_table = bool(page.get("signals", {}).get("table"))
        page_figure = bool(page.get("signals", {}).get("figure"))
        layout = page.get("layout", {})
        # 阅读顺序以 reading_order 为准：它已经在两种顺序打架时选好了
        # 看得懂的那一份。老作业没有这个字段，退回自带顺序。
        ordered_ids = layout.get("reading_order") or layout.get(
            "native_order", []
        )
        by_id = {
            int(block["id"]): block
            for block in page.get("blocks", [])
            if not block.get("page_furniture")
        }
        if not ordered_ids:
            ordered_ids = sorted(by_id)
        unit_index = 0
        for block_id in ordered_ids:
            block = by_id.get(int(block_id))
            if not block:
                continue
            segments = block.get("segments")
            if not isinstance(segments, list) or not segments:
                segments = [
                    {
                        "index": 0,
                        "role": (
                            "heading"
                            if block.get("likely_heading")
                            else "body"
                        ),
                        "heading_level": (
                            1 if block.get("likely_heading") else None
                        ),
                        "text": str(block.get("text") or ""),
                        "bbox": block.get("bbox"),
                    }
                ]
            for segment in segments:
                text = str(segment.get("text") or "")
                chunks = _split_text(text, max_chars)
                for chunk_index, chunk in enumerate(chunks, 1):
                    unit_index += 1
                    role = str(segment.get("role") or "body")
                    heading_level = segment.get("heading_level")
                    kind_hint = "heading" if role == "heading" else "body"
                    if page_table and re.match(
                        r"(?i)^\s*(table|tab\.|表)\s*\d+",
                        chunk,
                    ):
                        kind_hint = "table-or-caption"
                    elif page_figure and re.match(
                        r"(?i)^\s*(fig(?:ure)?\.?|图)\s*\d+",
                        chunk,
                    ):
                        kind_hint = "figure-or-caption"
                    units.append(
                        {
                            "id": f"p{page_number:04d}-u{unit_index:04d}",
                            "page": page_number,
                            "kind_hint": kind_hint,
                            "heading_level": (
                                int(heading_level)
                                if kind_hint == "heading"
                                and isinstance(heading_level, int)
                                else None
                            ),
                            "source": chunk,
                            "source_block_ids": [int(block_id)],
                            "source_segment_index": int(
                                segment.get("index") or 0
                            ),
                            "source_bbox": segment.get("bbox")
                            or block.get("bbox"),
                            "required_anchors": required_anchors(chunk),
                            "chunk_index_in_block": chunk_index,
                            "chunk_count_in_block": len(chunks),
                        }
                    )
    return {
        "schema_version": "1.0",
        "mapping_mode": "frozen-source-units-v1",
        "source_sha256": structure.get("source_sha256"),
        "source_structure_schema_version": structure.get("schema_version"),
        "unit_count": len(units),
        "max_unit_source_chars": max_chars,
        "units": units,
    }


#: 元素角色说这是一条参考文献题录时，单元类型就写 reference。
#: 题录默认保留原文，排版也按题录那一套走；类型停在 body，
#: 保留原文这条路在批次写回那一关就走不通。
REFERENCE_ROLE_KINDS = {"reference-entry": "reference"}


def _kind_for(unit: dict[str, Any], element_role: str) -> str:
    """单元类型：元素角色能定的按角色定，其余沿用扫描时的推断。"""

    return REFERENCE_ROLE_KINDS.get(
        str(element_role or "").lower(),
        str(unit["kind_hint"]),
    )


def build_translation_skeleton(
    source_units: dict[str, Any],
    *,
    source_language: str,
    target_language: str,
    source_units_sha256: str,
    roles_by_unit: dict[str, str] | None = None,
) -> dict[str, Any]:
    """搭出待翻译骨架。

    ``roles_by_unit`` 是 ``unit_bindings.json`` 算出的元素角色。它决定
    哪些单元本来就该保留原文形态（作者、单位、出版元数据、题录），
    检查据此免除这些单元的目标语言占比门槛。角色本身作为附加字段写进
    每个单元；只有题录角色同时改写 ``kind``，因为题录的排版本来就自成
    一套。作者与署名区的 ``kind`` 不动，排版按原样走。
    """

    roles = roles_by_unit or {}
    units = [
        {
            "id": unit["id"],
            "source_ref": unit["id"],
            "page": unit["page"],
            "kind": _kind_for(unit, roles.get(str(unit["id"]), "")),
            "element_role": roles.get(str(unit["id"]), ""),
            "heading_level": unit.get("heading_level"),
            "source": unit["source"],
            "source_bbox": unit["source_bbox"],
            "required_anchors": unit.get("required_anchors")
            or required_anchors(str(unit.get("source") or "")),
            "translation": None,
            "keep_source_code": None,
            "keep_source_reason": None,
            "review_flags": infer_review_flags(
                str(unit.get("source") or ""),
                str(unit.get("kind_hint") or ""),
                source_language,
            ),
        }
        for unit in source_units["units"]
    ]
    return {
        "schema_version": "1.0",
        "mapping_mode": "frozen-source-units-v1",
        "source_units_sha256": source_units_sha256,
        "source_language": source_language,
        "target_language": target_language,
        "terminology": [],
        "terminology_reviewed": False,
        "coverage": {
            "complete": False,
            "source_units_total": len(units),
            "translated_units": 0,
            "kept_source_units": 0,
            "validated_translated_units": 0,
            "validated_kept_source_units": 0,
            "invalid_or_unverified_units": len(units),
            "minimum_source_text_coverage_ratio": 0.85,
            "minimum_candidate_text_presence_ratio": 0.85,
            "scope_note": SCOPE_NOTE_PENDING,
        },
        "units": units,
    }


def prepare_translation_units(
    job_dir: Path,
    *,
    max_chars: int = 900,
    force: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    structure_path = job_dir / job.get("files", {}).get(
        "source_structure",
        "source_structure.json",
    )
    if not structure_path.is_file():
        raise SkillError("缺少 source_structure.json，请先提取原文结构")
    translation_path = job_dir / job["files"]["translation"]
    if translation_path.is_file() and not force:
        current = load_json(translation_path)
        if current.get("units"):
            raise SkillError(
                "translation.json 已有单元；为避免覆盖译文，未重新生成。"
                "确需重建时显式使用 --force"
            )
    structure = load_json(structure_path)
    source_units = build_source_units(structure, max_chars=max_chars)
    source_units_path = job_dir / job.get("files", {}).get(
        "source_units",
        "source_units.json",
    )
    write_json(source_units_path, source_units)
    # 元素角色沿用初始化时算好的那一份：重建骨架不该把角色丢掉，
    # 丢了角色，参考文献和署名区就又只能被当普通正文量占比。
    bindings_path = job_dir / "unit_bindings.json"
    roles_by_unit: dict[str, str] = {}
    if bindings_path.is_file():
        roles_by_unit = {
            str(binding.get("unit_id") or ""): str(
                binding.get("element_role") or ""
            )
            for binding in load_json(bindings_path).get("bindings") or []
            if isinstance(binding, dict) and binding.get("unit_id")
        }
    translation = build_translation_skeleton(
        source_units,
        source_language=str(job["translation"]["source_language"]),
        target_language=str(job["translation"]["target_language"]),
        source_units_sha256=sha256_file(source_units_path),
        roles_by_unit=roles_by_unit,
    )
    write_json(translation_path, translation)
    return source_units, translation



def build_source_units(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("prepare_translation_units"):
        return _timed_build_source_units(*args, **kwargs)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="从原文结构生成冻结的逐段翻译单元和 translation.json 骨架"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--max-chars", type=int, default=900)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        if not 400 <= args.max_chars <= 1600:
            raise SkillError("--max-chars 必须位于 400..1600")
        source_units, translation = prepare_translation_units(
            args.job_dir,
            max_chars=args.max_chars,
            force=args.force,
        )
        print(f"原文单元: {source_units['unit_count']}")
        print(f"翻译骨架: {len(translation['units'])}")
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
