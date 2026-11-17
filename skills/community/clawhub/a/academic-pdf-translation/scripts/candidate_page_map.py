from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from _common import (
    SkillError,
    internal_job_path,
    load_json,
    sha256_file,
)
from candidate_analysis import open_candidate_analysis


def candidate_page_map_path(job_dir: Path, job: dict[str, Any]) -> Path:
    return internal_job_path(
        job_dir,
        job.get("files", {}).get(
            "candidate_page_map",
            "candidate-page-map.json",
        ),
    )


def _page_list(value: Any, upper: int, label: str) -> list[int]:
    if not isinstance(value, list):
        raise SkillError(f"{label} 必须是页码数组")
    pages: list[int] = []
    for page in value:
        if not isinstance(page, int) or not 1 <= page <= upper:
            raise SkillError(f"{label} 含无效页码: {page!r}")
        pages.append(page)
    if not pages:
        raise SkillError(f"{label} 不能为空")
    return sorted(set(pages))


def validate_candidate_page_map(
    mapping: Any,
    *,
    source_page_count: int,
    candidate_page_count: int,
    translation_unit_ids: set[str] | None = None,
    candidate_sha256: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(mapping, dict):
        return ["candidate-page-map.json 必须是对象"]
    if mapping.get("complete") is not True:
        errors.append("candidate-page-map.json 尚未完成")
    if mapping.get("mapping_mode") != "flow-unit-anchors-v1":
        errors.append("candidate-page-map.json.mapping_mode 无效")
    if mapping.get("source_page_count") != source_page_count:
        errors.append("源页数与 candidate-page-map.json 不一致")
    if mapping.get("candidate_page_count") != candidate_page_count:
        errors.append("候选页数与 candidate-page-map.json 不一致")
    if (
        candidate_sha256
        and mapping.get("candidate_sha256") != candidate_sha256
    ):
        errors.append("candidate-page-map.json 绑定的候选哈希不一致")

    source_entries = mapping.get("source_pages")
    if not isinstance(source_entries, list):
        errors.append("candidate-page-map.json.source_pages 必须是数组")
        source_entries = []
    source_seen: set[int] = set()
    for index, entry in enumerate(source_entries):
        if not isinstance(entry, dict):
            errors.append(f"source_pages[{index}] 必须是对象")
            continue
        source_page = entry.get("source_page")
        if (
            not isinstance(source_page, int)
            or not 1 <= source_page <= source_page_count
        ):
            errors.append(f"source_pages[{index}].source_page 无效")
            continue
        if source_page in source_seen:
            errors.append(f"源页 {source_page} 在映射中重复")
        source_seen.add(source_page)
        try:
            _page_list(
                entry.get("candidate_pages"),
                candidate_page_count,
                f"源页 {source_page} 的 candidate_pages",
            )
        except SkillError as exc:
            errors.append(str(exc))
    expected_source_pages = set(range(1, source_page_count + 1))
    missing_source_pages = sorted(expected_source_pages - source_seen)
    if missing_source_pages:
        errors.append(
            "以下源页没有候选映射: "
            + ", ".join(map(str, missing_source_pages[:30]))
        )

    candidate_entries = mapping.get("candidate_pages")
    if not isinstance(candidate_entries, list):
        errors.append("candidate-page-map.json.candidate_pages 必须是数组")
        candidate_entries = []
    candidate_seen: set[int] = set()
    for index, entry in enumerate(candidate_entries):
        if not isinstance(entry, dict):
            errors.append(f"candidate_pages[{index}] 必须是对象")
            continue
        candidate_page = entry.get("candidate_page")
        if (
            not isinstance(candidate_page, int)
            or not 1 <= candidate_page <= candidate_page_count
        ):
            errors.append(f"candidate_pages[{index}].candidate_page 无效")
            continue
        if candidate_page in candidate_seen:
            errors.append(f"候选页 {candidate_page} 在映射中重复")
        candidate_seen.add(candidate_page)
        try:
            _page_list(
                entry.get("source_pages"),
                source_page_count,
                f"候选页 {candidate_page} 的 source_pages",
            )
        except SkillError as exc:
            errors.append(str(exc))
    missing_candidate_pages = sorted(
        set(range(1, candidate_page_count + 1)) - candidate_seen
    )
    if missing_candidate_pages:
        errors.append(
            "以下候选页没有源页映射: "
            + ", ".join(map(str, missing_candidate_pages[:30]))
        )

    if translation_unit_ids is not None:
        unit_entries = mapping.get("units")
        if not isinstance(unit_entries, list):
            errors.append("candidate-page-map.json.units 必须是数组")
            unit_entries = []
        mapped_unit_ids: set[str] = set()
        for index, entry in enumerate(unit_entries):
            if not isinstance(entry, dict):
                errors.append(f"units[{index}] 必须是对象")
                continue
            unit_id = entry.get("unit_id")
            if not isinstance(unit_id, str) or not unit_id:
                errors.append(f"units[{index}].unit_id 无效")
                continue
            if unit_id in mapped_unit_ids:
                errors.append(f"翻译单元映射重复: {unit_id}")
            mapped_unit_ids.add(unit_id)
            try:
                _page_list(
                    entry.get("candidate_pages"),
                    candidate_page_count,
                    f"翻译单元 {unit_id} 的 candidate_pages",
                )
            except SkillError as exc:
                errors.append(str(exc))
        missing_units = sorted(translation_unit_ids - mapped_unit_ids)
        extra_units = sorted(mapped_unit_ids - translation_unit_ids)
        if missing_units:
            errors.append(
                "以下翻译单元没有候选页映射: "
                + ", ".join(missing_units[:30])
            )
        if extra_units:
            errors.append(
                "候选页映射含未知翻译单元: "
                + ", ".join(extra_units[:30])
            )
    return errors


def load_candidate_page_map(
    job_dir: Path,
    job: dict[str, Any],
    *,
    required: bool = False,
    candidate_path: Path | None = None,
    translation: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    path = candidate_page_map_path(job_dir, job)
    if not path.is_file():
        if required:
            raise SkillError("缺少 candidate-page-map.json")
        return None
    mapping = load_json(path)
    if mapping.get("complete") is not True and not required:
        return None
    source_page_count = int(job.get("source", {}).get("page_count") or 0)
    candidate_page_count = int(mapping.get("candidate_page_count") or 0)
    candidate_hash = None
    if candidate_path is not None and candidate_path.is_file():

        analysis = open_candidate_analysis(candidate_path)
        document = analysis.document
        candidate_page_count = document.page_count
        analysis.release()
        candidate_hash = sha256_file(candidate_path)
    unit_ids = None
    if translation is not None:
        unit_ids = {
            str(unit.get("id"))
            for unit in translation.get("units", [])
            if isinstance(unit, dict) and str(unit.get("id") or "")
        }
    errors = validate_candidate_page_map(
        mapping,
        source_page_count=source_page_count,
        candidate_page_count=candidate_page_count,
        translation_unit_ids=unit_ids,
        candidate_sha256=candidate_hash,
    )
    if errors:
        raise SkillError("候选页映射无效: " + "；".join(errors))
    return mapping


def candidate_pages_for_source(
    mapping: dict[str, Any] | None,
    source_page: int,
) -> list[int]:
    if mapping is None:
        return [source_page]
    for entry in mapping.get("source_pages", []):
        if (
            isinstance(entry, dict)
            and entry.get("source_page") == source_page
        ):
            return [
                int(page)
                for page in entry.get("candidate_pages", [])
                if isinstance(page, int)
            ]
    return []


def candidate_pages_for_unit(
    mapping: dict[str, Any] | None,
    unit_id: str,
    fallback_source_page: int,
) -> list[int]:
    if mapping is None:
        return [fallback_source_page]
    for entry in mapping.get("units", []):
        if isinstance(entry, dict) and entry.get("unit_id") == unit_id:
            return [
                int(page)
                for page in entry.get("candidate_pages", [])
                if isinstance(page, int)
            ]
    return []


def source_pages_for_candidate(
    mapping: dict[str, Any] | None,
    candidate_page: int,
) -> list[int]:
    if mapping is None:
        return [candidate_page]
    for entry in mapping.get("candidate_pages", []):
        if (
            isinstance(entry, dict)
            and entry.get("candidate_page") == candidate_page
        ):
            return [
                int(page)
                for page in entry.get("source_pages", [])
                if isinstance(page, int)
            ]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="校验源页与候选页映射")
    parser.add_argument("job_dir", type=Path)
    args = parser.parse_args()
    try:
        job_dir = args.job_dir.resolve()
        job = load_json(job_dir / "job.json")
        translation = load_json(
            internal_job_path(
                job_dir,
                job["files"]["translation"],
            )
        )
        candidate_path = internal_job_path(
            job_dir,
            job["files"]["candidate"],
        )
        mapping = load_candidate_page_map(
            job_dir,
            job,
            required=True,
            candidate_path=candidate_path,
            translation=translation,
        )
        print(
            "候选页映射有效: "
            f"{mapping['source_page_count']} 个源页 -> "
            f"{mapping['candidate_page_count']} 个候选页"
        )
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
