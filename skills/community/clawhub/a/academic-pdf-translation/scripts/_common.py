from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

# scripts/ 下的命令行入口用 PYTHONPATH=scripts 运行，仓库根目录不在路径上。
# 正式包 academic_pdf_translation 在根目录，这里补一次，让两边都能 import。
# 放在 _common 是因为几乎每个脚本都会先导入它。
_REPO_ROOT = _Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in _sys.path:
    _sys.path.insert(0, str(_REPO_ROOT))

from academic_pdf_translation.contracts.models import (  # noqa: E402
    center_in_bbox as _center_in_bbox,
)

import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections.abc import Iterable
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import perf_trace

SCHEMA_VERSION = "1.0"
ROUTES = {
    "standard-auto",
    "hybrid-complex-pages",
    "custom-layout",
    "scan-custom",
}
COMPLEX_CONTENT_KINDS = {
    "structured-table",
    "chart-or-diagram",
    "figure-with-text",
    "form-or-scale",
    "formula-dense",
    "screenshot-or-interface",
    "scan-or-ocr",
    "rotated-or-mixed-size",
    "reading-order-risk",
    "mixed-complex",
    "other-complex",
}
COMPLEX_CONTENT_METHODS = {
    "structured-table-rebuild",
    "semantic-grid-rebuild",
    "vector-rebuild",
    "image-text-localization",
    "ocr-region-rebuild",
    "custom-page-reflow",
    "manual-reading-order-rebuild",
}
STATES = {
    "initialized",
    "translated",
    "candidate",
    "accepted",
    "finalized",
}


class SkillError(RuntimeError):
    pass


def skill_dir() -> Path:
    return Path(__file__).resolve().parent.parent


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def remove_suppressed_texts(
    text: str,
    suppress_texts: Iterable[Any],
) -> str:
    values = sorted(
        {
            str(value or "").strip()
            for value in suppress_texts
            if str(value or "").strip()
        },
        key=len,
        reverse=True,
    )
    result = text.strip()
    if not result or not values:
        return result
    value_set = set(values)
    if result in value_set:
        return ""

    lines = result.splitlines()
    if len(lines) > 1:
        result = "\n".join(
            line
            for line in lines
            if line.strip() not in value_set
        ).strip()
        if not result:
            return ""

    block_spans: list[tuple[int, int]] = []
    for value in values:
        if len(_content_token(value)) < 60:
            continue
        start = 0
        while True:
            index = result.find(value, start)
            if index < 0:
                break
            end = index + len(value)
            left_boundary = index == 0 or result[index - 1] == "\n"
            right_boundary = end == len(result) or result[end] == "\n"
            if left_boundary and right_boundary:
                block_spans.append((index, end))
            start = end
    if block_spans:
        for start, end in sorted(set(block_spans), reverse=True):
            result = result[:start] + result[end:]
        result = re.sub(r"\n{3,}", "\n\n", result).strip()
        if not result:
            return ""

    spans: list[tuple[int, int]] = []
    for value in values:
        start = 0
        while True:
            index = result.find(value, start)
            if index < 0:
                break
            end = index + len(value)
            if not any(index < prior_end and end > prior_start for prior_start, prior_end in spans):
                spans.append((index, end))
            start = end
    if not spans:
        return result
    covered_chars = sum(
        len(_content_token(result[start:end]))
        for start, end in spans
    )
    total_chars = len(_content_token(result))
    if not total_chars or covered_chars / total_chars < 0.72:
        return result
    for start, end in sorted(spans, reverse=True):
        result = result[:start] + result[end:]
    return re.sub(r"\n{3,}", "\n\n", result).strip()


def _content_token(text: Any) -> str:
    return "".join(
        character
        for character in unicodedata.normalize("NFKC", str(text or ""))
        if unicodedata.category(character)[0] in {"L", "N"}
    )


def _complex_target_strings(value: Any, key: str = "") -> list[str]:
    if isinstance(value, str):
        if (
            key.startswith("source")
            or key
            in {
                "id",
                "type",
                "method",
                "status",
                "render_policy",
                "insert_before_unit_id",
                "insert_after_unit_id",
            }
        ):
            return []
        return [value]
    if isinstance(value, list):
        return [
            text
            for item in value
            for text in _complex_target_strings(item, key)
        ]
    if isinstance(value, dict):
        return [
            text
            for child_key, item in value.items()
            for text in _complex_target_strings(item, str(child_key))
        ]
    return []


def _complex_payload_target_token(item: dict[str, Any]) -> str:
    payload = item.get("payload")
    if not isinstance(payload, dict):
        return ""
    return _content_token(
        "".join(_complex_target_strings(payload))
    )


def _unit_target_token(unit: dict[str, Any]) -> str:
    return _content_token(
        unit.get("translation") or unit.get("source") or ""
    )


def _token_coverage(text: str, container: str) -> float:
    if not text or not container:
        return 0.0
    if text in container:
        return 1.0
    matcher = SequenceMatcher(
        None,
        text,
        container,
        autojunk=False,
    )
    covered = sum(
        block.size for block in matcher.get_matching_blocks()
    )
    return covered / len(text)


def _complex_item_source_pages(item: dict[str, Any]) -> set[int]:
    pages: set[int] = set()
    if isinstance(item.get("page"), int):
        pages.add(int(item["page"]))
    payload = item.get("payload")
    if not isinstance(payload, dict):
        return pages

    def collect(value: Any) -> None:
        if isinstance(value, list):
            for child in value:
                collect(child)
            return
        if not isinstance(value, dict):
            return
        source_pages = value.get("source_pages")
        if isinstance(source_pages, list):
            pages.update(
                int(page)
                for page in source_pages
                if isinstance(page, int)
            )
        source_bboxes = value.get("source_bboxes")
        if isinstance(source_bboxes, list):
            pages.update(
                int(box["page"])
                for box in source_bboxes
                if (
                    isinstance(box, dict)
                    and isinstance(box.get("page"), int)
                )
            )
        if (
            isinstance(value.get("page"), int)
            and (
                "source_bbox" in value
                or "xref" in value
                or "source_text" in value
            )
        ):
            pages.add(int(value["page"]))
        for key in (
            "tables",
            "figures",
            "regions",
            "components",
        ):
            collect(value.get(key))

    collect(payload)
    return pages


def _complex_item_source_regions(
    item: dict[str, Any],
) -> dict[int, list[list[float]]]:
    regions: dict[int, list[list[float]]] = {}
    item_page = item.get("page")
    payload = item.get("payload")
    if not isinstance(payload, dict):
        return regions

    def add_region(page: Any, bbox: Any) -> None:
        if (
            not isinstance(page, int)
            or not isinstance(bbox, list)
            or len(bbox) != 4
            or not all(
                isinstance(value, (int, float))
                for value in bbox
            )
        ):
            return
        normalized = [float(value) for value in bbox]
        if normalized not in regions.setdefault(int(page), []):
            regions[int(page)].append(normalized)

    def collect(value: Any, default_page: Any) -> None:
        if isinstance(value, list):
            for child in value:
                collect(child, default_page)
            return
        if not isinstance(value, dict):
            return
        page = (
            value.get("page")
            if isinstance(value.get("page"), int)
            else default_page
        )
        add_region(page, value.get("source_bbox"))
        source_bboxes = value.get("source_bboxes")
        if isinstance(source_bboxes, list):
            for box in source_bboxes:
                if isinstance(box, dict):
                    add_region(
                        box.get("page", page),
                        box.get("bbox"),
                    )
        for key in (
            "tables",
            "figures",
            "regions",
            "components",
        ):
            collect(value.get(key), page)

    collect(payload, item_page)
    return regions


def _unit_center_in_source_regions(
    unit: dict[str, Any],
    regions: dict[int, list[list[float]]],
) -> bool:
    page = unit.get("page")
    bbox = unit.get("source_bbox")
    if (
        not isinstance(page, int)
        or not isinstance(bbox, list)
        or len(bbox) != 4
        or not all(
            isinstance(value, (int, float))
            for value in bbox
        )
    ):
        return False
    center_x = (float(bbox[0]) + float(bbox[2])) / 2
    center_y = (float(bbox[1]) + float(bbox[3])) / 2
    return any(
        region[0] <= center_x <= region[2]
        and region[1] <= center_y <= region[3]
        for region in regions.get(page, [])
    )


def complex_payload_replaces_unit(
    unit: dict[str, Any],
    complex_items: Iterable[dict[str, Any]],
    *,
    minimum_chars: int = 20,
    minimum_coverage: float = 0.90,
) -> bool:
    unit_page = unit.get("page")
    unit_text = _unit_target_token(unit)
    if not isinstance(unit_page, int) or len(unit_text) < minimum_chars:
        return False
    for item in complex_items:
        if (
            not isinstance(item, dict)
            or item.get("status") != "ready"
            or unit_page not in _complex_item_source_pages(item)
        ):
            continue
        payload_text = _complex_payload_target_token(item)
        if len(payload_text) < minimum_chars:
            continue
        if _token_coverage(unit_text, payload_text) >= minimum_coverage:
            return True
    return False


def complex_payload_replaced_unit_ids(
    units: Iterable[dict[str, Any]],
    complex_items: Iterable[dict[str, Any]],
    *,
    minimum_unit_chars: int = 20,
    minimum_group_chars: int = 20,
    minimum_coverage: float = 0.90,
) -> set[str]:
    unit_list = [
        unit for unit in units if isinstance(unit, dict)
    ]
    item_list = [
        item
        for item in complex_items
        if (
            isinstance(item, dict)
            and item.get("status") == "ready"
            and isinstance(item.get("page"), int)
        )
    ]
    replaced: set[str] = set()

    for item in item_list:
        source_regions = _complex_item_source_regions(item)
        item_replaced = {
            str(unit.get("id") or "")
            for unit in unit_list
            if (
                _unit_center_in_source_regions(
                    unit,
                    source_regions,
                )
                or complex_payload_replaces_unit(
                    unit,
                    [item],
                    minimum_chars=minimum_unit_chars,
                    minimum_coverage=minimum_coverage,
                )
            )
        }
        payload_text = _complex_payload_target_token(item)
        if len(payload_text) < minimum_group_chars:
            replaced.update(item_replaced)
            continue
        payload = item.get("payload")
        anchor_id = (
            str(payload.get("insert_before_unit_id") or "")
            if isinstance(payload, dict)
            else ""
        )
        for page in sorted(_complex_item_source_pages(item)):
            page_units = [
                unit for unit in unit_list if unit.get("page") == page
            ]
            run: list[tuple[dict[str, Any], str]] = []

            def commit_run() -> None:
                if not run:
                    return
                aggregate_chars = sum(
                    len(token) for _, token in run
                )
                has_seed = any(
                    str(unit.get("id") or "") in item_replaced
                    or "table"
                    in str(unit.get("kind") or "").casefold()
                    or "caption"
                    in str(unit.get("kind") or "").casefold()
                    for unit, _ in run
                )
                if (
                    aggregate_chars >= minimum_group_chars
                    and has_seed
                ):
                    item_replaced.update(
                        str(unit.get("id") or "")
                        for unit, _ in run
                    )

            for unit in page_units:
                unit_text = _unit_target_token(unit)
                if (
                    unit_text
                    and _token_coverage(unit_text, payload_text)
                    >= minimum_coverage
                ):
                    run.append((unit, unit_text))
                    continue
                commit_run()
                run = []
            commit_run()

            indexed_units = list(enumerate(page_units))
            anchor_indices = [
                index
                for index, unit in indexed_units
                if str(unit.get("id") or "") == anchor_id
            ]
            structured_anchor_span = bool(
                anchor_indices
                and str(item.get("method") or "")
                in {
                    "structured-table-rebuild",
                    "semantic-grid-rebuild",
                }
            )
            if structured_anchor_span:
                anchor_index = anchor_indices[0]
                for index, unit in indexed_units:
                    if (
                        index < anchor_index
                        and not _unit_center_in_source_regions(
                            unit,
                            source_regions,
                        )
                    ):
                        item_replaced.discard(
                            str(unit.get("id") or "")
                        )
            seed_indices = [
                index
                for index, unit in indexed_units
                if str(unit.get("id") or "") in item_replaced
            ]
            if not seed_indices:
                continue
            start_index = (
                anchor_indices[0]
                if structured_anchor_span
                else min(seed_indices)
            )
            end_index = max(seed_indices)
            for index, unit in indexed_units:
                if index < start_index or index > end_index:
                    continue
                unit_text = _unit_target_token(unit)
                if (
                    structured_anchor_span
                    and not str(
                        unit.get("keep_source_reason") or ""
                    ).strip()
                ):
                    item_replaced.add(str(unit.get("id") or ""))
                    continue
                if len(unit_text) >= 2 and unit_text in payload_text:
                    item_replaced.add(str(unit.get("id") or ""))
        replaced.update(item_replaced)
    return {unit_id for unit_id in replaced if unit_id}


def is_nonsemantic_source_furniture_unit(
    unit: dict[str, Any],
    *,
    page_width: float | None = None,
    page_height: float | None = None,
) -> bool:
    if not str(unit.get("keep_source_reason") or "").strip():
        return False
    text = str(unit.get("source") or "").strip()
    if re.fullmatch(r"\d(?:\s+\d){1,3}", text):
        return True
    bbox = unit.get("source_bbox")
    if (
        isinstance(bbox, list)
        and len(bbox) == 4
        and all(isinstance(value, (int, float)) for value in bbox)
    ):
        width = abs(float(bbox[2]) - float(bbox[0]))
        height = abs(float(bbox[3]) - float(bbox[1]))
        if 0 < width <= 40.0 and height / width >= 8.0:
            return True
        if page_height is not None and float(page_height) > 0:
            compact_edge_band = max(12.0, float(page_height) * 0.025)
            entirely_in_edge_band = (
                float(bbox[3]) <= compact_edge_band
                or float(bbox[1])
                >= float(page_height) - compact_edge_band
            )
            if (
                entirely_in_edge_band
                and height <= max(18.0, float(page_height) * 0.035)
            ):
                return True
        if (
            page_height is not None
            and float(page_height) > 0
            and re.fullmatch(r"\d{1,4}|[ivxlcdm]{1,8}", text, re.I)
        ):
            edge_band = max(18.0, float(page_height) * 0.18)
            near_page_edge = (
                float(bbox[3]) <= edge_band
                or float(bbox[1]) >= float(page_height) - edge_band
            )
            compact_marker = bool(
                height <= max(18.0, float(page_height) * 0.035)
            )
            if near_page_edge and compact_marker:
                return True
    return False


class ArtifactFingerprintCache:
    """进程内文件 SHA-256 缓存。

    缓存键是 (绝对路径, 文件大小, mtime_ns)。三者任一变化就重新读取，
    因此不会把“路径没变”当作“内容没变”。缓存只存在于当前进程，
    正式哈希仍然写入各自的结果文件。
    """

    def __init__(self) -> None:
        self._entries: dict[tuple[str, int, int], str] = {}

    def clear(self) -> None:
        self._entries.clear()

    def digest(self, path: Path, chunk_size: int = 1024 * 1024) -> str:
        resolved = Path(path).resolve()
        try:
            status = resolved.stat()
            key: tuple[str, int, int] | None = (
                str(resolved),
                int(status.st_size),
                int(status.st_mtime_ns),
            )
        except OSError:
            key = None
        if key is not None:
            cached = self._entries.get(key)
            if cached is not None:
                perf_trace.count(perf_trace.COUNTER_SHA256_CACHE_HIT)
                return cached

        perf_trace.count(perf_trace.COUNTER_SHA256_READ)
        digest = hashlib.sha256()
        with resolved.open("rb") as handle:
            while chunk := handle.read(chunk_size):
                digest.update(chunk)
        value = digest.hexdigest()
        if key is not None:
            self._entries[key] = value
        return value


FINGERPRINT_CACHE = ArtifactFingerprintCache()


def sha256_file(
    path: Path,
    chunk_size: int = 1024 * 1024,
    *,
    use_cache: bool = True,
) -> str:
    if not use_cache:
        perf_trace.count(perf_trace.COUNTER_SHA256_READ)
        digest = hashlib.sha256()
        with Path(path).open("rb") as handle:
            while chunk := handle.read(chunk_size):
                digest.update(chunk)
        return digest.hexdigest()
    return FINGERPRINT_CACHE.digest(Path(path), chunk_size)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SkillError(f"缺少文件: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SkillError(f"JSON 无法解析: {path}: {exc}") from exc


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as handle:
        handle.write(payload)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def import_fitz():
    try:
        import fitz
    except ImportError as exc:
        raise SkillError(
            "缺少 PyMuPDF。请使用当前工作区 Python，或安装 pymupdf。"
        ) from exc
    return fitz


def open_pdf(path: Path, *, role: str = "pdf"):
    """打开 PDF 并记一次打开计数。

    role 只用于性能基线区分原文与候选，不影响返回值。
    """

    fitz = import_fitz()
    path = Path(path)
    if not path.is_file():
        raise SkillError(f"PDF 不存在: {path}")
    try:
        document = fitz.open(path)
    except Exception as exc:
        raise SkillError(f"无法打开 PDF: {path}: {exc}") from exc
    perf_trace.count(perf_trace.COUNTER_PDF_OPEN)
    if role == "source":
        perf_trace.count(perf_trace.COUNTER_SOURCE_PDF_OPEN)
    elif role == "candidate":
        perf_trace.count(perf_trace.COUNTER_CANDIDATE_PDF_OPEN)
    return document


def language_profiles() -> dict[str, dict[str, Any]]:
    data = load_json(skill_dir() / "assets" / "language-profiles.json")
    return data["profiles"]


def resolve_language_profile(code: str) -> tuple[str, dict[str, Any]]:
    profiles = language_profiles()
    if code in profiles:
        return code, profiles[code]
    for canonical, profile in profiles.items():
        if code in profile.get("aliases", []):
            return canonical, profile
    supported = ", ".join(sorted(profiles))
    raise SkillError(f"不支持的目标语言 {code!r}。当前配置: {supported}")


def character_counts(text: str) -> dict[str, int]:
    return {
        "han": len(re.findall(r"[\u3400-\u9fff]", text)),
        "hiragana_katakana": len(
            re.findall(r"[\u3040-\u30ff\u31f0-\u31ff]", text)
        ),
        "hangul": len(re.findall(r"[\uac00-\ud7af\u1100-\u11ff]", text)),
        "latin": len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]", text)),
        "digits": len(re.findall(r"\d", text)),
    }


def target_character_count(text: str, writing_system: str) -> int:
    counts = character_counts(text)
    if writing_system == "han":
        return counts["han"]
    if writing_system == "japanese":
        return counts["han"] + counts["hiragana_katakana"]
    if writing_system == "hangul":
        return counts["hangul"] + counts["han"]
    return counts["latin"]


def infer_source_language(text: str) -> str:
    counts = character_counts(text)
    if counts["hangul"] > max(counts["han"], counts["latin"]):
        return "ko"
    if counts["hiragana_katakana"] > 20:
        return "ja"
    if counts["han"] > counts["latin"]:
        return "zh"
    if counts["latin"] > 0:
        return "und-Latn"
    return "und"


def internal_job_path(job_dir: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise SkillError(f"作业内部路径不能是绝对路径: {value}")
    resolved_job = job_dir.resolve()
    resolved = (resolved_job / path).resolve()
    try:
        resolved.relative_to(resolved_job)
    except ValueError as exc:
        raise SkillError(f"作业内部路径越出作业目录: {value}") from exc
    return resolved


def ensure_nonempty_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SkillError(f"{label} 必须是非空字符串")
    return value.strip()


# 定义已搬进 academic_pdf_translation.contracts.models，这里保留同名再导出，
# 所有既有调用方一个字都不用改。
center_in_bbox = _center_in_bbox
