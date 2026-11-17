from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path

from _common import (
    SkillError,
    import_fitz,
    internal_job_path,
    load_json,
    write_json,
)
from candidate_analysis import open_candidate_analysis
from candidate_page_map import (
    candidate_pages_for_source,
    load_candidate_page_map,
)
from content_anchors import anchors_present, required_anchors
from retained_source import (
    extract_retained_regions,
    retained_regions_by_page,
    strip_retained_blocks,
)
from semantic_markers import infer_review_flags

YEAR_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:18|19|20)\d{2}(?:[’']?s|[a-z])?(?![A-Za-z0-9])",
    re.I,
)
SUSPICIOUS_SEARCH_CHARS = {
    "\u00ad": "SOFT_HYPHEN",
    "\ufb00": "LATIN_LIGATURE_FF",
    "\ufb01": "LATIN_LIGATURE_FI",
    "\ufb02": "LATIN_LIGATURE_FL",
    "\ufb03": "LATIN_LIGATURE_FFI",
    "\ufb04": "LATIN_LIGATURE_FFL",
    "\ufb05": "LATIN_LIGATURE_LONG_ST",
    "\ufb06": "LATIN_LIGATURE_ST",
}


def _content_length(text: str) -> int:
    return len(re.sub(r"[\s\W_]+", "", text or "", flags=re.UNICODE))


def _year_present(year: str, target_text: str) -> bool:
    normalized_year = re.sub(r"[’']", "", year.casefold())
    candidate_years = {
        re.sub(r"[’']", "", value.casefold())
        for value in YEAR_RE.findall(target_text)
    }
    if normalized_year in candidate_years:
        return True
    decade = re.fullmatch(r"((?:18|19|20)\d{2})s", normalized_year, re.I)
    if not decade:
        return False
    start = int(decade.group(1))
    chinese_decade = f"{start // 100 + 1}世纪{start % 100}年代"
    return chinese_decade in re.sub(r"\s+", "", target_text)


def _source_text_outside_retained(
    page,
    payloads: list[dict],
) -> str | None:
    regions = [
        payload.get("effective_bbox") or payload.get("bbox")
        for payload in payloads
        if payload.get("resolution") != "translated-nonreference-region"
        and payload.get("blocks")
    ]
    regions = [
        list(map(float, region))
        for region in regions
        if isinstance(region, list) and len(region) == 4
    ]
    if not regions:
        return None

    chunks: list[str] = []
    page_height = float(page.rect.height)
    for block in page.get_text("blocks", sort=True):
        text = str(block[4] or "").strip()
        if not text:
            continue
        x0, y0, x1, y1 = map(float, block[:4])
        if (
            y1 <= page_height * 0.065
            or y0 >= page_height * 0.92
        ) and len(text) <= 240:
            continue
        area = max((x1 - x0) * (y1 - y0), 1.0)
        center_x = (x0 + x1) / 2
        center_y = (y0 + y1) / 2
        covered = False
        for rx0, ry0, rx1, ry1 in regions:
            if rx0 <= center_x <= rx1 and ry0 <= center_y <= ry1:
                covered = True
                break
            overlap_width = max(0.0, min(x1, rx1) - max(x0, rx0))
            overlap_height = max(0.0, min(y1, ry1) - max(y0, ry0))
            if overlap_width * overlap_height / area >= 0.5:
                covered = True
                break
        if not covered:
            chunks.append(text)
    return "\n".join(chunks).strip()


def _is_textual_unit(unit: dict) -> bool:
    if (
        not str(unit.get("translation") or "").strip()
        and str(unit.get("keep_source_reason") or "").strip()
    ):
        return False
    kind = str(unit.get("kind") or "").lower()
    excluded = (
        "reference",
        "table",
        "figure",
        "metadata",
        "header",
        "footer",
        "page-furniture",
        "publisher-frontmatter",
    )
    return not any(kind.startswith(prefix) for prefix in excluded)


def _running_values(
    value_pages: dict[str, set[int]],
    textual_page_count: int,
) -> set[str]:
    minimum_pages = max(4, math.ceil(textual_page_count * 0.6))
    return {
        value
        for value, page_numbers in value_pages.items()
        if len(page_numbers) >= minimum_pages
    }


def build_review_risk_report(job_dir: Path) -> dict:
    job_dir = job_dir.resolve()
    job = load_json(job_dir / "job.json")
    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    candidate_path = internal_job_path(
        job_dir,
        job["files"]["candidate"],
    )
    if not candidate_path.is_file():
        raise SkillError("作业尚未注册候选 PDF")

    translation = load_json(
        internal_job_path(job_dir, job["files"]["translation"])
    )
    retained = load_json(
        internal_job_path(job_dir, job["files"]["retained_source"])
    )
    units_by_page: dict[int, list[dict]] = defaultdict(list)
    semantic_units_by_page: dict[int, list[dict]] = defaultdict(list)
    source_language = str(
        job.get("translation", {}).get("source_language") or "und-Latn"
    )
    for unit in translation.get("units", []):
        page = unit.get("page")
        if isinstance(page, int):
            units_by_page[page].append(unit)
            explicit_flags = unit.get("review_flags")
            semantic_flags = {
                str(flag)
                for flag in explicit_flags
                if isinstance(flag, str)
            } if isinstance(explicit_flags, list) else set()
            semantic_flags.update(
                infer_review_flags(
                    str(unit.get("source") or ""),
                    str(unit.get("kind") or ""),
                    source_language,
                )
            )
            if semantic_flags:
                semantic_units_by_page[page].append(
                    {
                        "unit_id": unit.get("id"),
                        "flags": sorted(semantic_flags),
                    }
                )

    fitz = import_fitz()
    source_handle = open_candidate_analysis(source_path, role="source")
    candidate_handle = open_candidate_analysis(candidate_path)
    source_doc = source_handle.document
    candidate_doc = candidate_handle.document
    candidate_mapping = (
        load_candidate_page_map(
            job_dir,
            job,
            required=(
                "candidate_page_map" in job.get("files", {})
            ),
            candidate_path=candidate_path,
            translation=translation,
        )
        if (
            "candidate_page_map" in job.get("files", {})
            or (job_dir / "candidate-page-map.json").is_file()
        )
        else None
    )
    if candidate_mapping is None and source_doc.page_count != candidate_doc.page_count:
        raise SkillError("源文与候选页数不一致，无法生成逐页风险报告")
    retained_payloads_by_page = retained_regions_by_page(
        extract_retained_regions(
            source_doc,
            retained,
            translation,
        )
    )

    unit_stats: dict[
        int,
        tuple[int, int, float | None, bool, str, str],
    ] = {}
    document_ratios: list[float] = []
    for page_number in range(1, source_doc.page_count + 1):
        text_units = [
            unit
            for unit in units_by_page.get(page_number, [])
            if _is_textual_unit(unit)
        ]
        raw_unit_source = "\n".join(
            str(unit.get("source") or "") for unit in text_units
        )
        page_retained = retained_payloads_by_page.get(page_number, [])
        translated_anchor_source = strip_retained_blocks(
            raw_unit_source,
            page_retained,
        )
        coordinate_source = _source_text_outside_retained(
            source_doc[page_number - 1],
            page_retained,
        )
        unit_source = (
            coordinate_source
            if coordinate_source is not None
            else strip_retained_blocks(raw_unit_source, page_retained)
        )
        unit_translation = "\n".join(
            str(unit.get("translation") or "") for unit in text_units
        )
        source_len = _content_length(unit_source)
        translation_len = _content_length(unit_translation)
        ratio = (
            round(translation_len / source_len, 3)
            if source_len
            else None
        )
        has_text_units = bool(text_units)
        unit_stats[page_number] = (
            source_len,
            translation_len,
            ratio,
            has_text_units,
            unit_source,
            translated_anchor_source,
        )
        if source_len >= 600 and ratio is not None and ratio > 0:
            document_ratios.append(ratio)
    document_ratio_median = (
        statistics.median(document_ratios) if document_ratios else None
    )
    summary_risk_threshold = (
        max(0.12, document_ratio_median * 0.78)
        if document_ratio_median is not None
        else 0.12
    )
    textual_page_count = sum(
        1 for stats in unit_stats.values() if stats[3]
    )
    year_pages: dict[str, set[int]] = defaultdict(set)
    url_pages: dict[str, set[int]] = defaultdict(set)
    doi_pages: dict[str, set[int]] = defaultdict(set)
    for page_number, stats in unit_stats.items():
        for year in set(YEAR_RE.findall(stats[5])):
            year_pages[year].add(page_number)
        page_anchors = required_anchors(stats[5])
        for url in page_anchors["urls"]:
            url_pages[str(url).casefold()].add(page_number)
        for doi in page_anchors["dois"]:
            doi_pages[str(doi).casefold()].add(page_number)
    running_years = _running_values(year_pages, textual_page_count)
    running_urls = _running_values(url_pages, textual_page_count)
    running_dois = _running_values(doi_pages, textual_page_count)
    candidate_texts = [
        candidate_doc[index].get_text("text")
        for index in range(candidate_doc.page_count)
    ]

    pages: list[dict] = []
    for page_number in range(1, source_doc.page_count + 1):
        mapped_pages = candidate_pages_for_source(
            candidate_mapping,
            page_number,
        )
        candidate_text = "\n".join(
            candidate_texts[candidate_page - 1]
            for candidate_page in mapped_pages
            if 1 <= candidate_page <= len(candidate_texts)
        )
        (
            source_len,
            translation_len,
            ratio,
            has_text_units,
            unit_source,
            translated_anchor_source,
        ) = unit_stats[page_number]

        # Only inspect years that belong to translated content. Full-page text
        # also contains running headers and publisher furniture that a rebuilt
        # translation may intentionally omit.
        source_years = (
            set(YEAR_RE.findall(translated_anchor_source)) - running_years
            if has_text_units
            else set()
        )
        neighbor_source_pages = range(
            max(1, page_number - 1),
            min(source_doc.page_count, page_number + 1) + 1,
        )
        neighbor_candidate_pages = sorted(
            {
                candidate_page
                for source_page in neighbor_source_pages
                for candidate_page in candidate_pages_for_source(
                    candidate_mapping,
                    source_page,
                )
            }
        )
        candidate_neighbor_text = "\n".join(
            candidate_texts[candidate_page - 1]
            for candidate_page in neighbor_candidate_pages
            if 1 <= candidate_page <= len(candidate_texts)
        )
        missing_years = sorted(
            year
            for year in source_years
            if not _year_present(year, candidate_neighbor_text)
        )

        missing_link_anchors = (
            anchors_present(
                required_anchors(translated_anchor_source),
                candidate_text,
            )
            if has_text_units
            else {"urls": [], "dois": []}
        )
        missing_urls = [
            value
            for value in missing_link_anchors["urls"]
            if str(value).casefold() not in running_urls
        ]
        missing_dois = [
            value
            for value in missing_link_anchors["dois"]
            if str(value).casefold() not in running_dois
        ]
        suspicious_chars = {
            label: candidate_text.count(char)
            for char, label in SUSPICIOUS_SEARCH_CHARS.items()
            if char in candidate_text
        }

        flags: list[str] = []
        if (
            has_text_units
            and source_len >= 600
            and ratio is not None
            and ratio < summary_risk_threshold
        ):
            flags.append("POSSIBLE_SUMMARY_OR_OMISSION")
        if missing_years:
            flags.append("YEAR_CITATION_LOSS")
        if missing_urls:
            flags.append("URL_SEARCH_LOSS")
        if missing_dois:
            flags.append("DOI_SEARCH_LOSS")
        if suspicious_chars:
            flags.append("SEARCH_LAYER_COMPATIBILITY_CHARS")
        semantic_units = semantic_units_by_page.get(page_number, [])
        if semantic_units:
            flags.append("SEMANTIC_REVIEW_REQUIRED")

        pages.append(
            {
                "page": page_number,
                "candidate_pages": mapped_pages,
                "source_unit_chars": source_len,
                "translation_unit_chars": translation_len,
                "translation_source_ratio": ratio,
                "missing_years": missing_years,
                "missing_urls": missing_urls,
                "missing_dois": missing_dois,
                "suspicious_search_chars": suspicious_chars,
                "semantic_review_units": semantic_units,
                "flags": flags,
            }
        )

    source_handle.release()
    candidate_handle.release()
    high_priority_flags = {
        "POSSIBLE_SUMMARY_OR_OMISSION",
        "URL_SEARCH_LOSS",
        "DOI_SEARCH_LOSS",
        "SEARCH_LAYER_COMPATIBILITY_CHARS",
    }
    risky_pages = [page["page"] for page in pages if page["flags"]]
    high_priority_pages = [
        page["page"]
        for page in pages
        if high_priority_flags.intersection(page["flags"])
    ]
    return {
        "job_id": job.get("job_id"),
        "page_count": len(pages),
        "risky_page_count": len(risky_pages),
        "risky_pages": risky_pages,
        "high_priority_page_count": len(high_priority_pages),
        "high_priority_pages": high_priority_pages,
        "document_translation_source_ratio_median": document_ratio_median,
        "summary_risk_threshold": round(summary_risk_threshold, 3),
        "ignored_running_years": sorted(running_years),
        "ignored_running_urls": sorted(running_urls),
        "ignored_running_dois": sorted(running_dois),
        "pages": pages,
        "interpretation": (
            "该报告只负责提前暴露风险，不能证明语义正确，"
            "也不能替代按质量档位执行的完整独立复审。"
        ),
    }


def _markdown(report: dict) -> str:
    lines = [
        "# 复审风险报告",
        "",
        f"- 作业：`{report.get('job_id')}`",
        f"- 页数：{report['page_count']}",
        f"- 高优先风险页：{report['high_priority_page_count']}",
        f"- 其他核对页："
        f"{report['risky_page_count'] - report['high_priority_page_count']}",
        "",
        "| 页码 | 风险 | 译源字量比 | 缺失年份 | URL/DOI |",
        "|---:|---|---:|---|---|",
    ]
    for page in report["pages"]:
        if not page["flags"]:
            continue
        links = len(page["missing_urls"]) + len(page["missing_dois"])
        lines.append(
            "| {page} | {flags} | {ratio} | {years} | {links} |".format(
                page=page["page"],
                flags=", ".join(page["flags"]),
                ratio=page["translation_source_ratio"],
                years=", ".join(page["missing_years"]) or "-",
                links=links or "-",
            )
        )
    lines.extend(["", report["interpretation"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="生成逐页语义完整性、引文与检索层风险报告"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()
    try:
        report = build_review_risk_report(args.job_dir)
        if args.output_json:
            write_json(args.output_json.resolve(), report)
        if args.output_md:
            path = args.output_md.resolve()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(_markdown(report), encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
