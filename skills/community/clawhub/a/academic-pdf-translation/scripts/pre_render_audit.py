from __future__ import annotations

import sys
from pathlib import Path

# 按 README 的写法 `python3 scripts/X.py` 运行时，sys.path 里只有 scripts/，
# 没有仓库根，academic_pdf_translation 包就 import 不到。先把根加进去。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from typing import Any  # noqa: E402

from academic_pdf_translation.render.flowables import (  # noqa: E402
    DRAWABLE_FIGURE_KEYS,
    figure_payload_is_drawable,
)
from academic_pdf_translation.verify.render_contract import (  # noqa: E402
    complex_view_is_current,
    planning_issues,
)
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402

import perf_trace  # noqa: E402
from _common import (
    SkillError,
    internal_job_path,
    load_json,
    resolve_language_profile,
    sha256_file,
    utc_now,
    write_json,
)
from audit_translation_completeness import build_completeness_audit
from renderer_identity import renderer_build_id
from retained_source import retained_region_ids
from validate_job import validate_job

VISIBLE_MARKUP_RE = re.compile(
    r"<\s*/?\s*(?:br|p|div|span|font|table|tr|td|th)\b",
    re.IGNORECASE,
)
PLACEHOLDER_RE = re.compile(
    r"(?:\bTODO\b|\bTBD\b|\bFIXME\b|\bPLACEHOLDER\b|待翻译|未翻译|翻译中)",
    re.IGNORECASE,
)
def _ids_sha256(ids: list[str]) -> str:
    payload = "\n".join(ids).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _source_units_hash(
    source_units_path: Path,
    translation_path: Path,
) -> str:
    if source_units_path.is_file():
        return sha256_file(source_units_path)
    payload = (
        "legacy-manual\n" + sha256_file(translation_path)
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _walk_strings(value: Any, path: str = "$") -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    if isinstance(value, str):
        hits.append((path, value))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_walk_strings(item, f"{path}[{index}]"))
    elif isinstance(value, dict):
        for key, item in value.items():
            hits.extend(_walk_strings(item, f"{path}.{key}"))
    return hits


def _vector_payload_issues(
    complex_content: dict[str, Any],
) -> list[dict[str, Any]]:
    """vector-rebuild 载荷必须画得出真实绘图对象。

    画不出来时渲染器会退回把标签排成几行字：候选里一根线都没有，
    构建、QA 和对账却全绿。静默失败必须变成硬失败，宁可停下也不交。
    """

    issues: list[dict[str, Any]] = []
    for item in complex_content.get("items", []):
        if not isinstance(item, dict):
            continue
        if str(item.get("method") or "") != "vector-rebuild":
            continue
        payload = item.get("payload")
        figures = (payload or {}).get("figures") if isinstance(payload, dict) else None
        undrawable = [
            index
            for index, figure in enumerate(figures or [], 1)
            if not figure_payload_is_drawable(figure)
        ]
        if not figures or undrawable:
            issues.append(
                {
                    "code": "VECTOR_REBUILD_PAYLOAD_NOT_DRAWABLE",
                    "page": item.get("page"),
                    "figure_indexes": undrawable,
                    "drawable_keys": list(DRAWABLE_FIGURE_KEYS),
                    "message": (
                        "vector-rebuild 载荷里没有可绘制的结构，渲染出来只会是"
                        "几行标签文字。改用元素管线的保留策略把原图整块留下，"
                        "或把载荷补成上列任一种结构。"
                    ),
                }
            )
    return issues


def _text_input_issues(
    translation: dict[str, Any],
    complex_content: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = _vector_payload_issues(complex_content)
    samples = []
    target_text = {
        "units": [
            {
                "id": unit.get("id"),
                "translation": unit.get("translation"),
                "keep_source_reason": unit.get("keep_source_reason"),
            }
            for unit in translation.get("units", [])
            if isinstance(unit, dict)
        ],
        "terminology": translation.get("terminology", []),
    }
    for path, text in _walk_strings(
        {
            "translation": target_text,
            "complex_content": complex_content,
        }
    ):
        codes = []
        if "\x00" in text:
            codes.append("NULL_CHARACTER")
        if "\ufffd" in text:
            codes.append("REPLACEMENT_CHARACTER")
        if VISIBLE_MARKUP_RE.search(text):
            codes.append("VISIBLE_MARKUP")
        if PLACEHOLDER_RE.search(text):
            codes.append("PLACEHOLDER")
        if codes:
            samples.append(
                {
                    "path": path,
                    "codes": codes,
                    "sample": text[:180],
                }
            )
    if samples:
        issues.append(
            {
                "code": "TEXT_INPUT_NOT_CLEAN",
                "message": "译文或复杂页数据仍含空字符、替换字符、可见标记或占位文字。",
                "samples": samples[:40],
            }
        )
    return issues


def _font_file_issues(
    selected_fonts: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, str]], list[str]]:
    """只检查冻结字体文件本身，不涉及排版器合同。

    这些问题在渲染前就能判定，因此属于输入就绪检查。
    """

    issues: list[dict[str, Any]] = []
    evidence: list[dict[str, str]] = []
    if not isinstance(selected_fonts, list) or not selected_fonts:
        return (
            [
                {
                    "code": "SELECTED_FONTS_MISSING",
                    "message": "导出前必须冻结实际使用的字体文件。",
                }
            ],
            evidence,
            [],
        )

    normalized: list[str] = []
    for index, value in enumerate(selected_fonts):
        if not isinstance(value, str) or not value.strip():
            issues.append(
                {
                    "code": "FONT_PATH_INVALID",
                    "message": f"selected_fonts[{index}] 不是有效路径。",
                }
            )
            continue
        path = Path(value).expanduser().resolve()
        normalized.append(str(path))
        if not path.is_file():
            issues.append(
                {
                    "code": "FONT_FILE_MISSING",
                    "path": str(path),
                }
            )
            continue
        try:
            TTFont(f"PreRenderAuditFont{index}", str(path))
        except Exception as exc:
            issues.append(
                {
                    "code": "FONT_FILE_UNREADABLE",
                    "path": str(path),
                    "message": str(exc),
                }
            )
            continue
        evidence.append(
            {
                "path": str(path),
                "sha256": sha256_file(path),
            }
        )
    return issues, evidence, normalized


#: 排版器会在进入 PDF 之前规范化掉的字符，覆盖检查不重复报。
RENDERER_NORMALIZED_CHARACTERS = frozenset(
    [chr(code) for code in range(0x00, 0x09)]
    + [chr(code) for code in range(0x0B, 0x20)]
    + [chr(0x7F)]
    + [chr(code) for code in range(0xFB00, 0xFB07)]
)


def _font_coverage_issues(
    normalized: list[str],
    translation: dict[str, Any],
) -> list[dict[str, Any]]:
    """冻结字体合起来能不能画出全部待排文字。

    画不出的字符在候选里会退化成 \x00，最后以 NULL_CHARACTERS 的形式
    出现在 QA 里——那时只知道"有几个空字符"，不知道是哪个字符、哪一段。
    这里在渲染之前就把字符和单元指出来。
    """

    if not normalized:
        return []
    covered: set[int] = set()
    for index, path in enumerate(normalized):
        try:
            face = TTFont(f"CoverageProbe{index}", path).face
        except Exception:
            return []
        mapping = getattr(face, "charToGlyph", None)
        if not isinstance(mapping, dict) or not mapping:
            return []
        covered.update(mapping)

    missing: dict[str, list[str]] = {}
    for unit in translation.get("units", []):
        if not isinstance(unit, dict):
            continue
        text = str(unit.get("translation") or "")
        if not text:
            # 保留原文的单元同样要排进候选，一并检查。
            text = str(unit.get("source") or "")
        for character in text:
            if character.isspace() or ord(character) in covered:
                continue
            if character in RENDERER_NORMALIZED_CHARACTERS:
                # 排版器会先删掉控制字符、把连字还原成普通字母，
                # 这些字符不会以原样进入候选，不算覆盖缺口。
                continue
            missing.setdefault(character, []).append(
                str(unit.get("id") or "?")
            )
    if not missing:
        return []
    return [
        {
            "code": "FONT_CHARACTER_COVERAGE_GAP",
            "message": (
                "冻结字体无法画出以下字符，候选里会退化成空字符。"
                "请改用覆盖这些字符的字体，或在译文中换用等价写法。"
            ),
            "characters": [
                {
                    "character": character,
                    "codepoint": f"U+{ord(character):04X}",
                    "unit_ids": sorted(set(unit_ids))[:10],
                    "occurrences": len(unit_ids),
                }
                for character, unit_ids in sorted(missing.items())
            ][:40],
        }
    ]


def _stale_font_evidence_issues(
    quality: dict[str, Any],
    observed: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """冻结时记下的字体哈希与当前磁盘内容是否一致。

    字体被替换或升级后哈希会变；此时必须重新解析，不能继续用旧记录。
    """

    recorded = quality.get("selected_font_evidence")
    if not isinstance(recorded, list) or len(recorded) != len(observed):
        return [
            {
                "code": "SELECTED_FONT_EVIDENCE_MISSING",
                "message": (
                    "job.quality.selected_font_evidence 缺失或与冻结字体数量"
                    "不一致；请运行 font_preparation.py 重新冻结字体。"
                ),
            }
        ]
    def _same_file(left: str, right: str) -> bool:
        # /Library/Fonts 是 /System/Library/Fonts/Supplemental 的符号链接：
        # 同一个文件两个路径写法，按字符串比会误判成"字体被换了"。
        if left == right:
            return True
        try:
            return Path(left).resolve() == Path(right).resolve()
        except OSError:
            return False

    changed = [
        entry["path"]
        for entry, record in zip(observed, recorded, strict=True)
        if not isinstance(record, dict)
        or not _same_file(str(record.get("path") or ""), entry["path"])
        or record.get("sha256") != entry["sha256"]
    ]
    if changed:
        return [
            {
                "code": "SELECTED_FONT_FILE_CHANGED",
                "message": (
                    "字体文件内容与冻结记录不一致；请运行 font_preparation.py "
                    "--force 重新解析。"
                ),
                "paths": changed,
            }
        ]
    return []


def _font_contract_issues(
    normalized: list[str],
    contract: dict[str, Any],
) -> list[dict[str, Any]]:
    """只检查排版器声明的字体是否与冻结字体一致。"""

    contract_fonts = contract.get("font_paths")
    if not isinstance(contract_fonts, list) or sorted(
        str(Path(path).expanduser().resolve())
        for path in contract_fonts
        if isinstance(path, str)
    ) != sorted(normalized):
        return [
            {
                "code": "RENDERER_FONT_CONTRACT_MISMATCH",
                "message": "排版器声明的字体与 job.json 冻结字体不一致。",
            }
        ]
    return []


def _font_issues(
    selected_fonts: Any,
    contract: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    file_issues, evidence, normalized = _font_file_issues(selected_fonts)
    if not isinstance(selected_fonts, list) or not selected_fonts:
        return file_issues, evidence
    return (
        file_issues + _font_contract_issues(normalized, contract),
        evidence,
    )


def _layout_contract_issues(
    layout_log: dict[str, Any],
    translation: dict[str, Any],
    complex_content: dict[str, Any],
    retained: dict[str, Any],
    target_language: str,
    selected_fonts: Any,
    *,
    complex_view_current: bool = True,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if layout_log.get("renderer") == "academic-pdf-layout":
        recorded_build = str(
            layout_log.get("renderer_build_id") or ""
        )
        if recorded_build != renderer_build_id():
            issues.append(
                {
                    "code": "RENDERER_BUILD_ID_MISMATCH",
                    "message": "排版日志与当前统一生成器代码不一致。",
                }
            )
    contract = layout_log.get("render_contract")
    if not isinstance(contract, dict):
        return (
            [
                {
                    "code": "RENDER_CONTRACT_MISSING",
                    "message": (
                        "排版器没有提交导出前合同，无法证明全部翻译单元和文字区域"
                        "已经参与试排。"
                    ),
                }
            ],
            {},
        )

    units = [
        unit
        for unit in translation.get("units", [])
        if isinstance(unit, dict) and isinstance(unit.get("id"), str)
    ]
    unit_ids = [str(unit["id"]) for unit in units]
    expected_ids_hash = _ids_sha256(unit_ids)
    expected_count = len(unit_ids)
    if (
        contract.get("all_units_consumed") is not True
        or contract.get("unit_count") != expected_count
        or contract.get("unit_ids_sha256") != expected_ids_hash
    ):
        issues.append(
            {
                "code": "RENDER_UNIT_COVERAGE_INCOMPLETE",
                "message": "排版器没有证明所有冻结译文单元都已进入版式。",
                "expected_unit_count": expected_count,
                "actual_unit_count": contract.get("unit_count"),
            }
        )
    retained_ids = retained_region_ids(retained)
    expected_retained_hash = _ids_sha256(retained_ids)
    if (
        contract.get("all_retained_regions_consumed") is not True
        or contract.get("retained_region_count") != len(retained_ids)
        or contract.get("retained_region_ids_sha256") != expected_retained_hash
    ):
        issues.append(
            {
                "code": "RENDER_RETAINED_SOURCE_NOT_CONSUMED",
                "message": (
                    "排版器没有证明全部保留原文区域已真正进入候选版式。"
                ),
                "expected_retained_region_count": len(retained_ids),
                "actual_retained_region_count": contract.get(
                    "retained_region_count"
                ),
            }
        )
    if contract.get("all_text_regions_measured") is not True:
        issues.append(
            {
                "code": "UNMEASURED_TEXT_REGIONS",
                "regions": contract.get("unmeasured_text_regions") or [],
                "message": "仍有标题、脚注、图注、声明或其他文字区域未做导出前试排。",
            }
        )
    complex_ids = [
        str(item.get("id"))
        for item in complex_content.get("items", [])
        if isinstance(item, dict) and str(item.get("id") or "")
    ]
    expected_complex_hash = _ids_sha256(complex_ids)
    if (
        contract.get("all_complex_items_consumed") is not True
        or contract.get("complex_item_count") != len(complex_ids)
        or contract.get("complex_item_ids_sha256") != expected_complex_hash
    ):
        if complex_view_current:
            issues.append(
                {
                    "code": "RENDER_COMPLEX_CONTENT_NOT_CONSUMED",
                    "message": (
                        "排版器没有证明全部复杂页载荷已真正进入候选版式。"
                    ),
                    "expected_complex_item_count": len(complex_ids),
                    "actual_complex_item_count": contract.get(
                        "complex_item_count"
                    ),
                }
            )
        else:
            # 视图不是当前计划派生的：错在视图旧了，不在排版器。
            # 旧手写条目数不许再顶着"没消化"的名义拦一版合法的新计划。
            issues.append(
                {
                    "code": "COMPLEX_CONTENT_VIEW_STALE",
                    "message": (
                        "complex_content.json 不是由当前渲染计划派生的视图，"
                        "重新构建候选即可自动再生；它的条目数不作为消化判据。"
                    ),
                    "view_complex_item_count": len(complex_ids),
                    "generator_complex_item_count": contract.get(
                        "complex_item_count"
                    ),
                }
            )
    if contract.get("heading_checks_performed") is not True:
        issues.append(
            {
                "code": "HEADING_PLACEMENT_NOT_CHECKED",
                "message": "排版器没有提交标题与首段同页检查结果。",
            }
        )
    for field, code in (
        ("overflow_regions", "PRE_RENDER_OVERFLOW"),
        ("orphan_regions", "PRE_RENDER_ORPHAN_LINE"),
    ):
        values = contract.get(field)
        if not isinstance(values, list):
            issues.append(
                {
                    "code": "RENDER_CONTRACT_FIELD_MISSING",
                    "field": field,
                }
            )
        elif values:
            issues.append({"code": code, "regions": values})

    _, profile = resolve_language_profile(target_language)
    if (
        profile.get("writing_system") in {"han", "japanese"}
        and contract.get("cjk_kinsoku_enabled") is not True
    ):
        issues.append(
            {
                "code": "CJK_KINSOKU_NOT_ENABLED",
                "message": "目标语言排版器尚未启用 CJK 行首行末禁则。",
            }
        )
    font_issues, font_evidence = _font_issues(selected_fonts, contract)
    issues.extend(font_issues)
    return issues, {
        "contract": contract,
        "font_evidence": font_evidence,
        "expected_unit_count": expected_count,
        "expected_unit_ids_sha256": expected_ids_hash,
        "expected_complex_item_count": len(complex_ids),
        "expected_complex_item_ids_sha256": expected_complex_hash,
        "expected_retained_region_count": len(retained_ids),
        "expected_retained_region_ids_sha256": expected_retained_hash,
    }


#: 只缓存两项昂贵结果，并且只在同一进程内有效。
#: 键刻意排除 `quality.selected_fonts`：`build_candidate` 会把冻结字体解析成
#: 实际字体文件后写回 job.json，但 translated 阶段校验与完整性审计都不读这个
#: 字段（由 self_test 守护）。字体本身的检查不走本缓存，每次单独执行；
#: 排版合同检查也始终从磁盘重新读取 job.json，避免拿到解析前的旧字体。
_EXPENSIVE_AUDIT_CACHE: dict[str, dict[str, Any]] = {}
_EXPENSIVE_AUDIT_VERSION = "expensive-audit-2"


def _font_independent_key(job_dir: Path, job: dict[str, Any]) -> str:
    trimmed = json.loads(json.dumps(job))
    quality = trimmed.get("quality")
    if isinstance(quality, dict):
        quality.pop("selected_fonts", None)
    files = job.get("files", {})
    parts = [
        _EXPENSIVE_AUDIT_VERSION,
        str(job_dir),
        hashlib.sha256(
            json.dumps(trimmed, ensure_ascii=False, sort_keys=True).encode(
                "utf-8"
            )
        ).hexdigest(),
    ]
    for relative in (
        job["source"]["job_path"],
        files.get("source_units", "source_units.json"),
        files["translation"],
        files.get("complex_content_payload", "complex_content.json"),
        files["retained_source"],
        files["figure_inventory"],
        files["layout_overrides"],
    ):
        path = internal_job_path(job_dir, relative)
        parts.append(sha256_file(path) if path.is_file() else "")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _expensive_audits(
    job_dir: Path,
    job: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """translated 阶段校验与无候选完整性审计，同输入只算一次。"""

    key = _font_independent_key(job_dir, job)
    cached = _EXPENSIVE_AUDIT_CACHE.get(key)
    if cached is not None:
        perf_trace.count("expensive_audit_cache_hit")
        return cached["validation"], cached["completeness"]
    validation = validate_job(
        job_dir,
        "translated",
        status_override="translated",
    )
    completeness = build_completeness_audit(
        job_dir,
        include_candidate=False,
    )
    _EXPENSIVE_AUDIT_CACHE.clear()
    _EXPENSIVE_AUDIT_CACHE[key] = {
        "validation": validation,
        "completeness": completeness,
    }
    return validation, completeness


def _translated_validation(job_dir: Path) -> dict[str, Any]:
    return validate_job(
        job_dir,
        "translated",
        status_override="translated",
    )


def _content_audit_without_candidate(job_dir: Path) -> dict[str, Any]:
    return build_completeness_audit(
        job_dir,
        include_candidate=False,
    )


def _audit_context(job_dir: Path) -> dict[str, Any]:
    """加载两类检查共用的作业输入，只读一次。

    不缓存跨调用结果：`build_candidate` 会把冻结字体解析成实际字体文件后
    写回 `job.json`，因此渲染前后的输入审计读到的是不同输入，重跑是必要的，
    不是冗余。
    """

    job = load_json(job_dir / "job.json")
    files = job.get("files", {})
    source_path = internal_job_path(job_dir, job["source"]["job_path"])
    source_units_path = internal_job_path(
        job_dir,
        files.get("source_units", "source_units.json"),
    )
    translation_path = internal_job_path(job_dir, files["translation"])
    complex_path = internal_job_path(
        job_dir,
        files.get("complex_content_payload", "complex_content.json"),
    )
    layout_path = internal_job_path(job_dir, files["layout_overrides"])
    retained_path = internal_job_path(job_dir, files["retained_source"])
    inventory_path = internal_job_path(job_dir, files["figure_inventory"])

    validation, completeness = _expensive_audits(job_dir, job)
    translation = load_json(translation_path)
    complex_content = load_json(complex_path)

    validation_issues = [
        {
            "code": "JOB_DATA_INVALID",
            "message": error,
        }
        for error in validation.get("errors", [])
    ]
    text_issues = _text_input_issues(translation, complex_content)

    inventory = load_json(inventory_path)
    unresolved = [
        item.get("id") or item.get("page")
        for item in inventory.get("items", [])
        if isinstance(item, dict)
        and str(item.get("status") or "").lower() == "unresolved"
    ]
    inventory_issues: list[dict[str, Any]] = []
    if (
        inventory.get("inventory_complete") is not True
        or not str(inventory.get("scope_note") or "").strip()
        or unresolved
    ):
        inventory_issues.append(
            {
                "code": "FIGURE_INVENTORY_NOT_READY",
                "unresolved": unresolved,
                "message": "图表、截图和复杂视觉内容尚未在导出前清点完。",
            }
        )
    completeness_issues: list[dict[str, Any]] = []
    if completeness.get("decision") == "NEEDS_REPAIR":
        completeness_issues.append(
            {
                "code": "TRANSLATION_DATA_NEEDS_REPAIR",
                "pages": completeness.get("repair_pages", []),
                "tasks": completeness.get("repair_plan", {}).get("tasks", []),
            }
        )

    # 元素级合同：必需元素每个都要有处理计划。这是核心判据，
    # 复杂条目"数量"只剩视图一致性的辅助角色。
    element_plan_issues: list[dict[str, Any]] = []
    complex_view_current = True
    plan_path = job_dir / "render_plan.json"
    elements_path = job_dir / "source_elements.json"
    if plan_path.is_file() and elements_path.is_file():
        element_plan_issues = planning_issues(
            load_json(elements_path), load_json(plan_path)
        )
        complex_view_current = complex_view_is_current(
            complex_content, sha256_file(plan_path)
        )

    context = {
        "job": job,
        "files": files,
        "paths": {
            "source": source_path,
            "source_units": source_units_path,
            "translation": translation_path,
            "complex_content": complex_path,
            "layout_overrides": layout_path,
            "retained_source": retained_path,
            "layout_log": job_dir / "generator-layout-log.json",
        },
        "translation": translation,
        "complex_content": complex_content,
        "validation": validation,
        "completeness": completeness,
        "validation_issues": validation_issues,
        "text_issues": text_issues,
        "inventory_issues": inventory_issues,
        "completeness_issues": completeness_issues,
        "element_plan_issues": element_plan_issues,
        "complex_view_current": complex_view_current,
    }
    return context


def _completeness_warnings(completeness: dict[str, Any]) -> list[dict[str, Any]]:
    if not completeness.get("review_pages"):
        return []
    return [
        {
            "code": "CONTENT_REVIEW_SIGNAL",
            "pages": completeness.get("review_pages", []),
            "flag_counts": completeness.get("flag_counts", {}),
        }
    ]


def build_input_readiness_audit(job_dir: Path) -> dict[str, Any]:
    """渲染前的输入就绪检查。

    只判断翻译数据、术语、图表清单、复杂页载荷、字体文件、保留原文区域和
    作业状态。它不读取 `generator-layout-log.json`，因此可以在调用
    `build_candidate()` 之前运行；输入不完整时不会先浪费时间生成 PDF。
    """

    job_dir = job_dir.resolve()
    context = _audit_context(job_dir)
    paths = context["paths"]
    quality = context["job"].get("quality", {})
    font_issues, font_evidence, _ = _font_file_issues(
        quality.get("selected_fonts")
    )
    if not font_issues:
        font_issues.extend(_stale_font_evidence_issues(quality, font_evidence))
        font_issues.extend(
            _font_coverage_issues(
                [str(entry["path"]) for entry in font_evidence],
                context["translation"],
            )
        )

    issues: list[dict[str, Any]] = [
        *context["validation_issues"],
        *context["text_issues"],
        *font_issues,
        *context["inventory_issues"],
        *context["completeness_issues"],
    ]
    completeness = context["completeness"]
    report = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "audit_scope": "input-readiness",
        "status": "READY_TO_RENDER" if not issues else "BLOCKED",
        "issue_count": len(issues),
        "issues": issues,
        "warnings": _completeness_warnings(completeness),
        "input_hashes": {
            "source_sha256": sha256_file(paths["source"]),
            "source_units_sha256": _source_units_hash(
                paths["source_units"],
                paths["translation"],
            ),
            "translation_sha256": sha256_file(paths["translation"]),
            "complex_content_sha256": sha256_file(paths["complex_content"]),
            "retained_source_sha256": sha256_file(paths["retained_source"]),
            "layout_overrides_sha256": sha256_file(paths["layout_overrides"]),
        },
        "font_evidence": font_evidence,
        "validation_warnings": context["validation"].get("warnings", []),
        "completeness_decision": completeness.get("decision"),
        "completeness_repair_pages": completeness.get("repair_pages", []),
        "completeness_review_pages": completeness.get("review_pages", []),
    }
    write_json(job_dir / "staging" / "input-readiness.json", report)
    return report


def build_render_contract_audit(job_dir: Path) -> dict[str, Any]:
    """候选生成后的排版合同检查。

    只判断排版器是否真的消费了全部冻结单元、保留区域和复杂页载荷，以及
    溢出、孤行、标题位置、实际字体和 CJK 禁则。
    """

    job_dir = job_dir.resolve()
    context = _audit_context(job_dir)
    paths = context["paths"]
    layout_log = load_json(paths["layout_log"])
    retained = load_json(paths["retained_source"])
    current_job = load_json(job_dir / "job.json")
    issues, contract_evidence = _layout_contract_issues(
        layout_log,
        context["translation"],
        context["complex_content"],
        retained,
        str(current_job["translation"]["target_language"]),
        current_job.get("quality", {}).get("selected_fonts"),
        complex_view_current=context["complex_view_current"],
    )
    issues = [*context["element_plan_issues"], *issues]
    report = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "audit_scope": "render-contract",
        "status": "READY_TO_RENDER" if not issues else "BLOCKED",
        "issue_count": len(issues),
        "issues": issues,
        "contract_evidence": contract_evidence,
        "input_hashes": {
            "generator_layout_log_sha256": sha256_file(paths["layout_log"]),
        },
    }
    write_json(job_dir / "staging" / "render-contract.json", report)
    return report


def build_pre_render_audit(job_dir: Path) -> dict[str, Any]:
    """导出前总检查：输入就绪与排版合同的合并结论。

    问题顺序与错误码与拆分前一致，外部调用不受影响。
    """

    job_dir = job_dir.resolve()
    context = _audit_context(job_dir)
    files = context["files"]
    paths = context["paths"]
    layout_log = load_json(paths["layout_log"])
    retained = load_json(paths["retained_source"])
    completeness = context["completeness"]

    # 字体必须从磁盘重读：build_candidate 会在渲染时把冻结字体解析成实际
    # 字体文件写回 job.json，用上下文里的旧值会误报字体合同不一致。
    current_job = load_json(job_dir / "job.json")
    contract_issues, contract_evidence = _layout_contract_issues(
        layout_log,
        context["translation"],
        context["complex_content"],
        retained,
        str(current_job["translation"]["target_language"]),
        current_job.get("quality", {}).get("selected_fonts"),
        complex_view_current=context["complex_view_current"],
    )
    issues: list[dict[str, Any]] = [
        *context["validation_issues"],
        *context["text_issues"],
        *context["element_plan_issues"],
        *contract_issues,
        *context["inventory_issues"],
        *context["completeness_issues"],
    ]

    report = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "status": "READY_TO_RENDER" if not issues else "BLOCKED",
        "issue_count": len(issues),
        "issues": issues,
        "warnings": _completeness_warnings(completeness),
        "input_hashes": {
            "source_sha256": sha256_file(paths["source"]),
            "source_units_sha256": _source_units_hash(
                paths["source_units"],
                paths["translation"],
            ),
            "translation_sha256": sha256_file(paths["translation"]),
            "complex_content_sha256": sha256_file(paths["complex_content"]),
            "retained_source_sha256": sha256_file(paths["retained_source"]),
            "layout_overrides_sha256": sha256_file(paths["layout_overrides"]),
            "generator_layout_log_sha256": sha256_file(paths["layout_log"]),
        },
        "contract_evidence": contract_evidence,
        "validation_warnings": context["validation"].get("warnings", []),
        "completeness_decision": completeness.get("decision"),
        "completeness_repair_pages": completeness.get("repair_pages", []),
        "completeness_review_pages": completeness.get("review_pages", []),
    }
    output_path = internal_job_path(
        job_dir,
        files.get("render_readiness", "staging/render-readiness.json"),
    )
    write_json(output_path, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="在生成 PDF 文件前一次性检查全部输入数据和排版器试排合同"
    )
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--scope",
        choices=("full", "input", "contract"),
        default="full",
        help=(
            "full 为导出前总检查；input 只检查渲染前的输入就绪；"
            "contract 只检查候选生成后的排版合同"
        ),
    )
    args = parser.parse_args()
    try:
        builder = {
            "full": build_pre_render_audit,
            "input": build_input_readiness_audit,
            "contract": build_render_contract_audit,
        }[args.scope]
        report = builder(args.job_dir)
        if args.output:
            write_json(args.output.resolve(), report)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "READY_TO_RENDER" else 2
    except SkillError as exc:
        print(f"错误: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
