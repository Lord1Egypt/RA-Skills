from __future__ import annotations

import sys
from pathlib import Path

# 按 README 的写法 `python3 scripts/X.py` 运行时，sys.path 里只有 scripts/，
# 没有仓库根，academic_pdf_translation 包就 import 不到。先把根加进去。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
import re  # noqa: E402
import unicodedata  # noqa: E402
from difflib import SequenceMatcher  # noqa: E402
from pathlib import Path  # noqa: E402
from typing import Any  # noqa: E402

from academic_pdf_translation.contracts.enums import (  # noqa: E402
    QUALITY_MODE_TO_REVIEW_MODE,
    QualityMode,
)
from academic_pdf_translation.verify.render_contract import (  # noqa: E402
    complex_view_is_current,
)

import perf_trace  # noqa: E402
from _common import (  # noqa: E402
    COMPLEX_CONTENT_KINDS,
    COMPLEX_CONTENT_METHODS,
    ROUTES,
    SCHEMA_VERSION,
    STATES,
    SkillError,
    complex_payload_replaced_unit_ids,
    internal_job_path,
    is_nonsemantic_source_furniture_unit,
    load_json,
    remove_suppressed_texts,
    resolve_language_profile,
    sha256_file,
    write_json,
)
from candidate_analysis import open_candidate_analysis  # noqa: E402
from candidate_page_map import (  # noqa: E402
    candidate_pages_for_unit,
    load_candidate_page_map,
)
from i18n import all_messages  # noqa: E402
from review_policy import (  # noqa: E402
    REVIEW_MODE_LIMITS,
    validate_post_repair_confirmation,
)
from semantic_markers import infer_review_flags, validate_terminology  # noqa: E402
from set_complex_payload import validate_complex_payload_item  # noqa: E402
from translation_truthfulness import (  # noqa: E402
    TruthfulnessError,
    evaluate_translation,
)

STAGE_ORDER = {
    "draft": 0,
    "translated": 1,
    "candidate": 2,
    "accepted": 3,
    "finalized": 4,
}

CRITICAL_TRANSLATION_REVIEW_FLAGS = {
    "semantic-boundary",
    "semantic-high-risk",
    "statistics-or-sample",
    "instrument-item-or-scoring",
}

REFERENCE_HEADING_PATTERN = re.compile(
    r"(?im)^\s*(references|bibliography|literature cited|works cited|参考文献)\s*$"
)

UNSOURCED_REVIEW_COMMENTARY_GUARDS = [
    (
        re.compile(r"本(?:项目|毕设)"),
        re.compile(r"\b(?:project|thesis|dissertation|capstone)\b", re.I),
        "项目或毕设视角",
    ),
    (
        re.compile(r"(?:不能|无法|不可|不应).{0,10}(?:外推|推广|泛化)"),
        re.compile(
            r"(?:cannot|can not|could not|should not|not).{0,100}"
            r"(?:generali[sz]|extrapolat|apply|extend|transfer)"
            r"|(?:generali[sz]|extrapolat|apply|extend|transfer).{0,100}"
            r"(?:cannot|can not|could not|should not|not)",
            re.I | re.S,
        ),
        "外推限制",
    ),
    (
        re.compile(
            r"(?:不能|无法|并不|不足以|而不是).{0,12}(?:直接)?"
            r"(?:证明|证实|推断).{0,48}"
            r"(?:因果|机制|效果|有效|伤害|相同|等同|产品|干预)"
        ),
        re.compile(
            r"(?:cannot|can not|could not|does not|do not|did not|rather than|"
            r"not|no evidence|insufficient|unable to).{0,140}"
            r"(?:caus|mechanism|effect|effic|harm|equival|same|"
            r"product|intervention|prove|establish|infer)"
            r"|(?:caus|mechanism|effect|effic|harm|equival|same|"
            r"product|intervention|prove|establish|infer).{0,140}"
            r"(?:cannot|can not|could not|does not|do not|did not|rather than|"
            r"not|no evidence|insufficient|unable to)",
            re.I | re.S,
        ),
        "证据边界判断",
    ),
    (
        re.compile(
            r"(?:不是|并非).{0,32}(?:直接检验|直接证明).{0,32}"
            r"(?:机制|因果|效果|结论)"
        ),
        re.compile(
            r"(?:not|did not|does not).{0,100}(?:direct|directly).{0,80}"
            r"(?:test|examine|prove|establish|mechanism|caus)"
            r"|(?:direct|directly).{0,80}(?:test|examine|prove|establish|"
            r"mechanism|caus).{0,100}(?:not|did not|does not)",
            re.I | re.S,
        ),
        "直接检验限制",
    ),
]

READING_VERSION_LABELS = {
    re.sub(r"\s+", "", value)
    for value in all_messages("reading_version")
}


def _validate_complex_content_policy(
    route: dict[str, Any],
    page_count: int,
    stage: str,
    errors: list[str],
) -> None:
    policy = route.get("complex_content")
    if policy is None:
        return
    if not isinstance(policy, dict):
        errors.append("job.route.complex_content 必须是对象")
        return

    heuristic_pages = policy.get("heuristic_candidate_pages", [])
    if not isinstance(heuristic_pages, list):
        errors.append("complex_content.heuristic_candidate_pages 必须是数组")
        heuristic_pages = []
    for page in heuristic_pages:
        if not isinstance(page, int) or not 1 <= page <= page_count:
            errors.append(f"画像候选复杂页页码无效: {page!r}")

    if STAGE_ORDER[stage] < STAGE_ORDER["translated"]:
        return
    if policy.get("classification_confirmed") is not True:
        errors.append("进入 translated 阶段前必须目视确认全部原文页的复杂内容分类")
    if policy.get("review_scope") != "all-source-pages":
        errors.append("复杂内容分类必须覆盖全部原文页")

    confirmed_pages = policy.get("confirmed_pages")
    if not isinstance(confirmed_pages, list):
        errors.append("complex_content.confirmed_pages 必须是数组")
        return

    seen_pages: set[int] = set()
    for item in confirmed_pages:
        if not isinstance(item, dict):
            errors.append("complex_content.confirmed_pages 每项必须是对象")
            continue
        page = item.get("page")
        kind = item.get("kind")
        method = item.get("method")
        reason = item.get("reason")
        if not isinstance(page, int) or not 1 <= page <= page_count:
            errors.append(f"确认复杂页页码无效: {page!r}")
        elif page in seen_pages:
            errors.append(f"复杂页重复登记: {page}")
        else:
            seen_pages.add(page)
        if kind not in COMPLEX_CONTENT_KINDS:
            errors.append(f"第 {page!r} 页复杂内容类型无效: {kind!r}")
        if method not in COMPLEX_CONTENT_METHODS:
            errors.append(f"第 {page!r} 页复杂内容处理方式无效: {method!r}")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"第 {page!r} 页复杂内容缺少专用处理理由")

    if confirmed_pages and route.get("selected") == "standard-auto":
        errors.append(
            "已确认存在复杂内容页，实际路线不得选择 standard-auto；"
            "第一次生成必须走混合或定制重建"
        )
    notes = policy.get("notes")
    if heuristic_pages and not confirmed_pages:
        if not isinstance(notes, str) or not notes.strip():
            errors.append(
                "画像提示候选复杂页但最终确认无复杂页时，必须记录目视排除依据"
            )


def _has_reference_heading(text: str) -> bool:
    return bool(REFERENCE_HEADING_PATTERN.search(text))


def _has_source_citation_block(text: str) -> bool:
    citation_like_lines = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        has_year = bool(
            re.search(r"(?:\(|\b)(?:18|19|20)\d{2}[a-z]?(?:\)|\.|\b)", stripped)
        )
        has_author_prefix = bool(
            re.match(
                r"^[A-Z][A-Za-zÀ-ÖØ-öø-ÿ' -]+"
                r"(?:,\s*(?:[A-Z]\.\s*)+|\s+(?:[A-Z]{1,3}\s*)+)",
                stripped,
            )
        )
        if has_year and has_author_prefix:
            citation_like_lines += 1
            if citation_like_lines >= 2:
                return True
    return False


def _requires_exact_candidate_presence(
    unit: dict,
    source_language: str = "und-Latn",
) -> bool:
    kind = str(unit.get("kind") or "").lower()
    if kind in {"title", "subtitle", "heading"}:
        return True
    review_flags = unit.get("review_flags")
    if not isinstance(review_flags, list):
        review_flags = []
    flags = {
        flag for flag in review_flags if isinstance(flag, str)
    }
    flags.update(
        infer_review_flags(
            str(unit.get("source") or ""),
            kind,
            source_language,
        )
    )
    if any(
        flag == "instrument-item-or-scoring"
        or flag.endswith("-item-or-scoring")
        for flag in flags
    ):
        return True
    if kind in {"table", "figure", "reference"}:
        return False
    return bool(flags & CRITICAL_TRANSLATION_REVIEW_FLAGS)


def _replace_page_unit_pages(
    complex_content: dict[str, Any] | None,
) -> set[int]:
    if not isinstance(complex_content, dict):
        return set()
    return {
        int(item["page"])
        for item in complex_content.get("items", [])
        if isinstance(item, dict)
        and isinstance(item.get("page"), int)
        and item.get("status") == "ready"
        and isinstance(item.get("payload"), dict)
        and item["payload"].get("render_policy") == "replace-page-units"
    }


def _unsourced_review_commentary(unit: dict) -> list[tuple[str, str]]:
    source = str(unit.get("source") or "")
    translated = str(unit.get("translation") or "")
    hits: list[tuple[str, str]] = []
    for translation_pattern, source_pattern, label in (
        UNSOURCED_REVIEW_COMMENTARY_GUARDS
    ):
        match = translation_pattern.search(translated)
        if match and not source_pattern.search(source):
            hits.append((label, match.group(0)))
    return hits


def _required_mapping(
    data: Any,
    keys: list[str],
    label: str,
    errors: list[str],
) -> dict:
    if not isinstance(data, dict):
        errors.append(f"{label} 必须是对象")
        return {}
    for key in keys:
        if key not in data:
            errors.append(f"{label} 缺少字段 {key!r}")
    return data


def _review_mode(job: dict, errors: list[str]) -> str:
    review = job.get("review")
    if review is None:
        return "legacy-double"
    review = _required_mapping(
        review,
        ["mode", "choice_recorded"],
        "job.review",
        errors,
    )
    mode = review.get("mode")
    if mode not in {"independent", "none", "precise"}:
        errors.append(f"无效检查方式: {mode!r}")
        return "independent"
    if review.get("choice_recorded") is not True:
        errors.append("开始翻译前必须记录用户选择的检查方式")
    # 质量档位与复审模式必须一致：review.mode 由 quality_mode 派生。
    quality_mode = job.get("quality_mode")
    if quality_mode:
        try:
            expected_mode = QUALITY_MODE_TO_REVIEW_MODE[
                QualityMode.parse(quality_mode)
            ]
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if expected_mode != str(mode):
                errors.append(
                    f"job.quality_mode={quality_mode!r} 派生的复审模式是 "
                    f"{expected_mode!r}，与 job.review.mode={mode!r} 不一致"
                )
    expected_review_rounds, expected_repair_rounds = REVIEW_MODE_LIMITS[
        str(mode)
    ]
    max_review_rounds = review.get("max_review_rounds")
    max_repair_rounds = review.get("max_repair_rounds")
    if (
        max_review_rounds is not None
        and max_review_rounds != expected_review_rounds
    ):
        errors.append("job.review.max_review_rounds 与质量档位不一致")
    if (
        max_repair_rounds is not None
        and max_repair_rounds != expected_repair_rounds
    ):
        errors.append("job.review.max_repair_rounds 与质量档位不一致")
    return str(mode)


def _load_job_file(
    job_dir: Path,
    job: dict,
    key: str,
    errors: list[str],
) -> tuple[Path, Any | None]:
    files = job.get("files", {})
    value = files.get(key)
    if not isinstance(value, str) or not value:
        errors.append(f"job.files 缺少 {key!r}")
        return job_dir / "__missing__", None
    try:
        path = internal_job_path(job_dir, value)
    except SkillError as exc:
        errors.append(str(exc))
        return job_dir / "__invalid__", None
    try:
        return path, load_json(path)
    except SkillError as exc:
        errors.append(str(exc))
        return path, None


def _validate_translation(
    translation: Any,
    page_count: int,
    target_language: str,
    errors: list[str],
    retained_source: Any = None,
) -> dict:
    translation = _required_mapping(
        translation,
        ["schema_version", "source_language", "target_language", "units"],
        "translation.json",
        errors,
    )
    if not translation:
        return {}
    if translation.get("target_language") != target_language:
        errors.append("translation.json 的目标语言与 job.json 不一致")
    units = translation.get("units")
    if not isinstance(units, list) or not units:
        errors.append("translation.json 必须包含至少一个翻译单元")
        return translation
    seen: set[str] = set()
    translated_count = 0
    kept_count = 0
    for index, unit in enumerate(units):
        label = f"translation.units[{index}]"
        if not isinstance(unit, dict):
            errors.append(f"{label} 必须是对象")
            continue
        for key in ("id", "page", "kind", "source"):
            if key not in unit:
                errors.append(f"{label} 缺少字段 {key!r}")
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or not unit_id.strip():
            errors.append(f"{label}.id 必须是非空字符串")
        elif unit_id in seen:
            errors.append(f"翻译单元 ID 重复: {unit_id}")
        else:
            seen.add(unit_id)
        page = unit.get("page")
        if not isinstance(page, int) or not 1 <= page <= page_count:
            errors.append(f"{label}.page 超出 1..{page_count}")
        source = unit.get("source")
        if not isinstance(source, str) or not source.strip():
            errors.append(f"{label}.source 不能为空")
        translated = unit.get("translation")
        keep_code = unit.get("keep_source_code")
        keep_reason = unit.get("keep_source_reason")
        has_translation = isinstance(translated, str) and translated.strip()
        has_keep_code = isinstance(keep_code, str) and keep_code.strip()
        has_keep_reason = isinstance(keep_reason, str) and keep_reason.strip()
        if not has_translation and not has_keep_code:
            if has_keep_reason:
                # 旧作业迁移：自由文本理由不能单独豁免，必须补写结构化 code。
                errors.append(
                    f"{label} 只有自由文本 keep_source_reason，缺少结构化 "
                    "keep_source_code。旧作业请为每个保留单元补写 "
                    "keep_source_code（取值见 translation_truthfulness."
                    "KEEP_SOURCE_CODES），或改为提供译文"
                )
            else:
                errors.append(f"{label} 既没有译文，也没有保留原文声明")
        elif has_translation and has_keep_code:
            errors.append(f"{label} 不能同时给出译文和 keep_source_code")
        elif has_translation:
            translated_count += 1
            for issue_label, excerpt in _unsourced_review_commentary(unit):
                errors.append(
                    f"{label} 含源文无依据的{issue_label}: {excerpt!r}；"
                    "译文正文不得加入审查者、产品或毕设视角的证据边界说明，"
                    "需要时应放入独立证据笔记"
                )
        else:
            kept_count += 1

    terminology = translation.get("terminology", [])
    if translation.get("terminology_reviewed") is True:
        errors.extend(validate_terminology(terminology, units))
    elif "terminology_reviewed" in translation:
        errors.append(
            "translation.terminology_reviewed 尚未设为 true；"
            "翻译前应确认术语表，即使最终为空"
        )

    coverage = _required_mapping(
        translation.get("coverage"),
        [
            "complete",
            "source_units_total",
            "translated_units",
            "kept_source_units",
            "minimum_source_text_coverage_ratio",
            "minimum_candidate_text_presence_ratio",
            "scope_note",
        ],
        "translation.coverage",
        errors,
    )
    # 不相信作业自报的 complete：这里独立重算一次译文真实性。
    truthfulness = None
    try:
        truthfulness = evaluate_translation(
            translation,
            retained_source=retained_source,
        )
    except (TruthfulnessError, SkillError) as exc:
        errors.append(f"译文真实性检查无法执行: {exc}")
    if truthfulness is not None:
        for problem in truthfulness["problems"][:60]:
            location = problem.get("unit_id") or problem.get("batch_id") or "全篇"
            errors.append(
                f"译文真实性检查未通过 [{problem['code']}] {location}: "
                f"{problem['message']}"
            )
        if truthfulness["invalid_or_unverified_units"]:
            errors.append(
                "存在未通过译文真实性检查的单元 "
                f"{truthfulness['invalid_or_unverified_units']} 个；"
                "完整性状态不能算通过"
            )

    if coverage:
        if coverage.get("complete") is not True:
            errors.append("translation.coverage.complete 尚未设为 true")
        if truthfulness is not None:
            if coverage.get("complete") is True and not truthfulness["complete"]:
                errors.append(
                    "translation.coverage.complete 自报为 true，"
                    "但独立重算的译文真实性检查未通过"
                )
            for key in (
                "validated_translated_units",
                "validated_kept_source_units",
                "invalid_or_unverified_units",
            ):
                if key not in coverage:
                    errors.append(f"translation.coverage 缺少字段 {key!r}")
                elif coverage.get(key) != truthfulness[key]:
                    errors.append(
                        f"translation.coverage.{key} 与独立重算结果不一致: "
                        f"{coverage.get(key)} != {truthfulness[key]}"
                    )
        if coverage.get("source_units_total") != len(units):
            errors.append("translation.coverage.source_units_total 与单元数不一致")
        if coverage.get("translated_units") != translated_count:
            errors.append("translation.coverage.translated_units 与实际译文数不一致")
        if coverage.get("kept_source_units") != kept_count:
            errors.append("translation.coverage.kept_source_units 与保留原文数不一致")
        minimum_ratio = coverage.get("minimum_source_text_coverage_ratio")
        if not isinstance(minimum_ratio, (int, float)) or not 0.5 <= float(
            minimum_ratio
        ) <= 1.0:
            errors.append(
                "translation.coverage.minimum_source_text_coverage_ratio "
                "必须位于 0.5..1.0"
            )
        candidate_ratio = coverage.get("minimum_candidate_text_presence_ratio")
        if not isinstance(candidate_ratio, (int, float)) or not 0.5 <= float(
            candidate_ratio
        ) <= 1.0:
            errors.append(
                "translation.coverage.minimum_candidate_text_presence_ratio "
                "必须位于 0.5..1.0"
            )
        if not isinstance(coverage.get("scope_note"), str) or not coverage.get(
            "scope_note", ""
        ).strip():
            errors.append("translation.coverage.scope_note 不能为空")
    for previous_id, current_id, overlap in _adjacent_translation_overlaps(
        units
    ):
        errors.append(
            "相邻翻译单元存在源文未对应的重复译文: "
            f"{previous_id} → {current_id}，重复 {overlap} 个归一化字符；"
            "跨栏或跨页续句应按真实源文边界拆分，候选中只出现一次"
        )
    return translation


def _validate_frozen_source_units(
    job_dir: Path,
    job: dict,
    translation: dict,
    errors: list[str],
) -> None:
    if (
        job.get("translation", {}).get("mapping_mode")
        != "frozen-source-units-v1"
    ):
        return
    source_units_path, source_units = _load_job_file(
        job_dir,
        job,
        "source_units",
        errors,
    )
    if not isinstance(source_units, dict):
        return
    if source_units.get("mapping_mode") != "frozen-source-units-v1":
        errors.append("source_units.json.mapping_mode 不正确")
    if translation.get("mapping_mode") != "frozen-source-units-v1":
        errors.append("translation.json 必须使用冻结原文单元映射")
    if translation.get("source_units_sha256") != sha256_file(source_units_path):
        errors.append("translation.json 绑定的 source_units.json 哈希不一致")

    frozen_units = source_units.get("units")
    if not isinstance(frozen_units, list) or not frozen_units:
        errors.append("source_units.json 必须包含非空 units")
        return
    frozen_by_id = {
        str(unit.get("id")): unit
        for unit in frozen_units
        if isinstance(unit, dict) and str(unit.get("id") or "")
    }
    if len(frozen_by_id) != len(frozen_units):
        errors.append("source_units.json 含无效或重复单元 ID")
    maximum = source_units.get("max_unit_source_chars")
    if isinstance(maximum, int):
        oversized = [
            unit_id
            for unit_id, unit in frozen_by_id.items()
            if len(str(unit.get("source") or "")) > maximum + 20
        ]
        if oversized:
            errors.append(
                "冻结原文单元超过声明的最大长度: "
                + ", ".join(oversized[:20])
            )

    used: dict[str, str] = {}
    for unit in translation.get("units", []):
        unit_id = str(unit.get("id") or "?")
        source_ref = unit.get("source_ref")
        if not isinstance(source_ref, str) or not source_ref:
            errors.append(f"{unit_id} 缺少 source_ref")
            continue
        if source_ref in used:
            errors.append(
                f"冻结原文单元被重复使用: {source_ref} "
                f"({used[source_ref]}, {unit_id})"
            )
            continue
        used[source_ref] = unit_id
        frozen = frozen_by_id.get(source_ref)
        if frozen is None:
            errors.append(f"{unit_id}.source_ref 不存在: {source_ref}")
            continue
        if str(unit.get("source") or "") != str(frozen.get("source") or ""):
            errors.append(f"{unit_id}.source 与冻结原文单元不一致")
        if unit.get("page") != frozen.get("page"):
            errors.append(f"{unit_id}.page 与冻结原文单元不一致")
        if unit.get("source_bbox") != frozen.get("source_bbox"):
            errors.append(f"{unit_id}.source_bbox 与冻结原文单元不一致")
    missing = sorted(set(frozen_by_id) - set(used))
    if missing:
        errors.append(
            "以下冻结原文单元没有译文或合法保留记录: "
            + ", ".join(missing[:20])
            + (" ..." if len(missing) > 20 else "")
        )


def _validate_complex_content_payload(
    job_dir: Path,
    job: dict,
    route: dict,
    errors: list[str],
) -> None:
    if (
        job.get("translation", {}).get("mapping_mode")
        != "frozen-source-units-v1"
    ):
        return
    _, data = _load_job_file(
        job_dir,
        job,
        "complex_content_payload",
        errors,
    )
    if not isinstance(data, dict):
        return
    if data.get("classification_complete") is not True:
        errors.append("复杂内容载荷尚未完成分类")
    # 视图是否由当前渲染计划派生。派生视图里，计划就是权威：
    # 计划补进的保留条目和重建表会让页码多于人工确认页，这不是错。
    plan_path = job_dir / "render_plan.json"
    derived_current = plan_path.is_file() and complex_view_is_current(
        data, sha256_file(plan_path)
    )
    expected = {
        int(item["page"]): item
        for item in route.get("complex_content", {}).get(
            "confirmed_pages",
            [],
        )
        if isinstance(item, dict) and isinstance(item.get("page"), int)
    }
    actual = {
        int(item["page"]): item
        for item in data.get("items", [])
        if isinstance(item, dict) and isinstance(item.get("page"), int)
    }
    if derived_current:
        # 人工确认过的复杂页一页都不能少；计划派生的多出来的页是合法的。
        missing_pages = set(expected) - set(actual)
        if missing_pages:
            errors.append(
                "确认过的复杂页在派生载荷里缺失: "
                + "、".join(str(page) for page in sorted(missing_pages))
            )
    elif set(expected) != set(actual):
        errors.append("复杂内容载荷页码与确认复杂页不一致")
    for page, route_item in expected.items():
        item = actual.get(page)
        if not item:
            continue
        if not derived_current:
            # 派生视图里 kind/method 由渲染计划决定，与旧确认表不逐字比对；
            # 非派生（手写）载荷仍按旧规矩逐项对齐。
            if item.get("kind") != route_item.get("kind"):
                errors.append(f"第 {page} 页复杂内容载荷类型不一致")
            if item.get("method") != route_item.get("method"):
                errors.append(f"第 {page} 页复杂内容载荷处理方式不一致")
    # 每个条目的内容质量检查对派生与否一视同仁：ready 状态与载荷合法性
    # 是产出门槛，一条都不放松。
    for item in data.get("items", []):
        if not isinstance(item, dict) or not isinstance(item.get("page"), int):
            continue
        page = int(item["page"])
        if item.get("status") != "ready":
            errors.append(f"第 {page} 页复杂内容载荷尚未 ready")
            continue
        for error in validate_complex_payload_item(item):
            errors.append(f"第 {page} 页复杂内容载荷: {error}")


def _bbox_within_page(unit: dict[str, Any], source_doc: Any) -> bool:
    """单元坐标是否落在所属页面内且非退化。"""

    bbox = unit.get("source_bbox")
    page_number = unit.get("page")
    if (
        not isinstance(page_number, int)
        or not isinstance(bbox, list)
        or len(bbox) != 4
        or not all(isinstance(value, (int, float)) for value in bbox)
    ):
        return False
    try:
        rect = source_doc[page_number - 1].rect
    except Exception:
        return False
    x0, y0, x1, y1 = (float(value) for value in bbox)
    if x1 <= x0 or y1 <= y0:
        return False
    return (
        x0 >= float(rect.x0) - 1.0
        and y0 >= float(rect.y0) - 1.0
        and x1 <= float(rect.x1) + 1.0
        and y1 <= float(rect.y1) + 1.0
    )


def _normalize_source_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(
        character
        for character in normalized
        if (
            unicodedata.category(character)[0] in {"L", "N"}
            and not unicodedata.combining(character)
        )
    )


def _is_nonsemantic_divider_source(text: str) -> bool:
    stripped = str(text or "").strip()
    if not stripped:
        return False
    allowed_symbols = {"=", ".", "*", "·", "•", "…"}
    return all(
        character.isspace()
        or unicodedata.category(character) in {"Pd", "Pc"}
        or character in allowed_symbols
        for character in stripped
    )


def _source_bbox_fuzzy_match(source_text: str, bbox_text: str) -> bool:
    if len(source_text) < 30 or len(bbox_text) < 30:
        return False
    length_ratio = min(len(source_text), len(bbox_text)) / max(
        len(source_text),
        len(bbox_text),
    )
    if length_ratio < 0.9:
        return False
    return SequenceMatcher(None, source_text, bbox_text).ratio() >= 0.96


def _adjacent_translation_overlaps(
    units: list[Any],
    minimum_overlap_chars: int = 12,
) -> list[tuple[str, str, int]]:
    reference_kinds = {"reference", "references", "bibliography"}
    overlaps: list[tuple[str, str, int]] = []
    for previous, current in zip(units, units[1:]):
        if not isinstance(previous, dict) or not isinstance(current, dict):
            continue
        previous_page = previous.get("page")
        current_page = current.get("page")
        if (
            not isinstance(previous_page, int)
            or not isinstance(current_page, int)
            or current_page < previous_page
            or current_page - previous_page > 1
        ):
            continue
        if (
            str(previous.get("kind", "")).lower() in reference_kinds
            or str(current.get("kind", "")).lower() in reference_kinds
        ):
            continue
        previous_text = _normalize_source_text(
            str(previous.get("translation") or "")
        )
        current_text = _normalize_source_text(
            str(current.get("translation") or "")
        )
        maximum = min(len(previous_text), len(current_text))
        if maximum < minimum_overlap_chars:
            continue
        overlap = 0
        for size in range(maximum, minimum_overlap_chars - 1, -1):
            if previous_text[-size:] == current_text[:size]:
                overlap = size
                break
        if not overlap:
            continue
        shorter_length = min(len(previous_text), len(current_text))
        if overlap < 16 and overlap / max(shorter_length, 1) < 0.35:
            continue
        previous_source = _normalize_source_text(str(previous.get("source", "")))
        current_source = _normalize_source_text(str(current.get("source", "")))
        source_overlap = min(
            overlap,
            len(previous_source),
            len(current_source),
        )
        if (
            source_overlap >= minimum_overlap_chars
            and previous_source[-source_overlap:]
            == current_source[:source_overlap]
        ):
            continue
        overlaps.append(
            (
                str(previous.get("id", "?")),
                str(current.get("id", "?")),
                overlap,
            )
        )
    return overlaps


def _full_page_reference_pages(source_doc: Any, retained: dict) -> set[int]:
    pages: set[int] = set()
    for region in retained.get("regions", []):
        if region.get("category") not in {"references", "bibliography"}:
            continue
        page_number = region.get("page")
        bbox = region.get("bbox")
        if (
            not isinstance(page_number, int)
            or not 1 <= page_number <= source_doc.page_count
            or not isinstance(bbox, list)
            or len(bbox) != 4
        ):
            continue
        page = source_doc[page_number - 1]
        page_area = max(float(page.rect.width * page.rect.height), 1.0)
        x0, y0, x1, y1 = map(float, bbox)
        region_area = max(0.0, x1 - x0) * max(0.0, y1 - y0)
        if region_area / page_area >= 0.8:
            pages.add(page_number)
    return pages


def _validate_source_text_coverage(
    source_path: Path,
    translation: dict,
    retained: dict,
    errors: list[str],
    warnings: list[str],
) -> None:
    if not translation:
        return
    try:
        source_handle = open_candidate_analysis(
            source_path,
            role="source",
        )
        source_doc = source_handle.document
    except Exception as exc:
        errors.append(f"无法计算原文覆盖率: {exc}")
        return
    excluded_pages = _full_page_reference_pages(source_doc, retained)
    page_texts = {
        index: _normalize_source_text(page.get_text("text"))
        for index, page in enumerate(source_doc, 1)
        if index not in excluded_pages
    }
    covered = {
        page: bytearray(len(text)) for page, text in page_texts.items()
    }
    unmatched: list[str] = []
    symbol_only: list[str] = []
    sources_by_page: dict[int, list[tuple[str, str, str]]] = {}
    for unit in translation.get("units", []):
        page_number = unit.get("page")
        source_text = _normalize_source_text(str(unit.get("source", "")))
        if isinstance(page_number, int) and source_text:
            sources_by_page.setdefault(page_number, []).append(
                (
                    str(unit.get("id", "?")),
                    source_text,
                    str(unit.get("kind", "")),
                )
            )
    for page_number, entries in sources_by_page.items():
        if len(entries) < 2 or page_number in excluded_pages:
            continue
        page_text = page_texts.get(page_number, "")
        repeated: dict[str, list[str]] = {}
        for unit_id, source_text, _ in entries:
            repeated.setdefault(source_text, []).append(unit_id)
        duplicated_large_sources = [
            unit_ids
            for source_text, unit_ids in repeated.items()
            if len(unit_ids) > 1 and len(source_text) >= 80
        ]
        if duplicated_large_sources:
            examples = ", ".join(
                "/".join(unit_ids[:3])
                for unit_ids in duplicated_large_sources[:3]
            )
            errors.append(
                f"第 {page_number} 页多个翻译单元重复绑定同一大段原文: "
                f"{examples}；应按真实语义段落或区域拆分"
            )
        if page_text:
            near_full_page_units = [
                unit_id
                for unit_id, source_text, kind in entries
                if kind not in {"reference", "references", "bibliography"}
                and len(source_text) / len(page_text) >= 0.8
            ]
            if near_full_page_units:
                errors.append(
                    f"第 {page_number} 页存在多个单元时，不得让单元重复绑定"
                    "接近整页的原文: "
                    + ", ".join(near_full_page_units[:10])
                )
    for unit in translation.get("units", []):
        page_number = unit.get("page")
        if page_number in excluded_pages:
            continue
        page_text = page_texts.get(page_number, "")
        raw_source_text = str(unit.get("source", ""))
        if _is_nonsemantic_divider_source(raw_source_text):
            continue
        source_text = _normalize_source_text(raw_source_text)
        if source_text == "" and raw_source_text.strip():
            # 整段只有符号（公式定界符、感叹号、控制字符等），归一化后没有
            # 任何字母或数字，靠文本匹配本来就定位不了。改用坐标核对：
            # bbox 必须落在页面内且非退化，否则仍然算没定位上。
            if _bbox_within_page(unit, source_doc):
                symbol_only.append(str(unit.get("id", "?")))
            else:
                unmatched.append(str(unit.get("id", "?")))
            continue
        if not page_text or not source_text:
            unmatched.append(str(unit.get("id", "?")))
            continue
        starts = []
        offset = 0
        while True:
            position = page_text.find(source_text, offset)
            if position < 0:
                break
            starts.append(position)
            offset = position + 1
        if not starts:
            bbox = unit.get("source_bbox")
            if (
                isinstance(page_number, int)
                and isinstance(bbox, list)
                and len(bbox) == 4
                and all(isinstance(value, (int, float)) for value in bbox)
            ):
                try:
                    from _common import import_fitz

                    fitz = import_fitz()
                    bbox_text = _normalize_source_text(
                        source_doc[page_number - 1].get_text(
                            "text",
                            clip=fitz.Rect(*map(float, bbox)),
                        )
                    )
                except Exception:
                    bbox_text = ""
                bbox_start = page_text.find(bbox_text) if bbox_text else -1
                source_in_bbox = (
                    bbox_text.find(source_text) if bbox_text else -1
                )
                if bbox_start >= 0 and source_in_bbox >= 0:
                    start = bbox_start + source_in_bbox
                    covered[page_number][
                        start : start + len(source_text)
                    ] = b"\x01" * len(source_text)
                    continue
                if (
                    bbox_start >= 0
                    and _source_bbox_fuzzy_match(source_text, bbox_text)
                ):
                    covered[page_number][
                        bbox_start : bbox_start + len(bbox_text)
                    ] = b"\x01" * len(bbox_text)
                    continue
            unmatched.append(str(unit.get("id", "?")))
            continue
        start = max(
            starts,
            key=lambda position: sum(
                1
                for marker in covered[page_number][
                    position : position + len(source_text)
                ]
                if marker == 0
            ),
        )
        covered[page_number][start : start + len(source_text)] = b"\x01" * len(
            source_text
        )

    total_chars = sum(len(text) for text in page_texts.values())
    covered_chars = sum(sum(markers) for markers in covered.values())
    ratio = covered_chars / total_chars if total_chars else 1.0
    minimum_ratio = float(
        translation.get("coverage", {}).get(
            "minimum_source_text_coverage_ratio", 0.85
        )
    )
    warnings.append(
        f"原文文本覆盖率: {ratio:.3f} "
        f"({covered_chars}/{total_chars}, 最低 {minimum_ratio:.3f})"
    )
    if ratio < minimum_ratio:
        errors.append(
            f"原文文本覆盖率不足: {ratio:.3f} < {minimum_ratio:.3f}"
        )
    if unmatched:
        errors.append(
            "以下翻译单元无法在对应原文页定位: "
            + ", ".join(unmatched[:20])
            + (" ..." if len(unmatched) > 20 else "")
        )
    if symbol_only:
        warnings.append(
            "以下翻译单元只含符号，按坐标核对通过，未做文本定位: "
            + ", ".join(symbol_only[:20])
            + (" ..." if len(symbol_only) > 20 else "")
        )
    source_handle.release()


def _validate_candidate_text_presence(
    candidate_path: Path,
    translation: dict,
    candidate_mapping: dict[str, Any] | None,
    errors: list[str],
    warnings: list[str],
    complex_content: dict[str, Any] | None = None,
    retained_payloads: list[dict[str, Any]] | None = None,
    source_path: Path | None = None,
) -> None:
    if not translation or not candidate_path.is_file():
        return
    try:
        candidate_handle = open_candidate_analysis(candidate_path)
        candidate_doc = candidate_handle.document
    except Exception as exc:
        errors.append(f"无法计算候选译文覆盖率: {exc}")
        return
    page_texts = {}
    for index, page in enumerate(candidate_doc, 1):
        page_texts[index] = _candidate_page_text(page)
    source_page_sizes: dict[int, tuple[float, float]] = {}
    try:
        if source_path is None:
            raise FileNotFoundError
        source_handle = open_candidate_analysis(
            source_path,
            role="source",
        )
        source_page_sizes = {
            index: (float(page.rect.width), float(page.rect.height))
            for index, page in enumerate(source_handle.document, 1)
        }
        source_handle.release()
    except Exception:
        source_page_sizes = {}
    total_chars = 0
    present_chars = 0
    missing_units: list[str] = []
    missing_critical_units: list[str] = []
    suppressed_by_page: dict[int, list[str]] = {}
    replaced_pages = _replace_page_unit_pages(complex_content)
    complex_items = (
        [
            item
            for item in complex_content.get("items", [])
            if isinstance(item, dict)
        ]
        if isinstance(complex_content, dict)
        else []
    )
    complex_replaced_unit_ids = complex_payload_replaced_unit_ids(
        translation.get("units", []),
        complex_items,
    )
    mapped_reference_pages = {
        int(entry["source_page"])
        for entry in (
            candidate_mapping.get("retained_regions", [])
            if isinstance(candidate_mapping, dict)
            else []
        )
        if isinstance(entry, dict)
        and isinstance(entry.get("source_page"), int)
        and str(entry.get("category") or "").lower()
        in {"references", "bibliography"}
        and any(
            isinstance(region, dict)
            and isinstance(region.get("candidate_page"), int)
            and isinstance(region.get("bbox"), list)
            and len(region["bbox"]) == 4
            for region in entry.get("candidate_regions", [])
        )
    }

    def collect_suppressions(payload: Any) -> list[str]:
        if not isinstance(payload, dict):
            return []
        values = [
            str(value)
            for value in payload.get("suppress_texts", [])
            if str(value).strip()
        ]
        for component in payload.get("components", []):
            if isinstance(component, dict):
                values.extend(
                    collect_suppressions(
                        component.get("payload") or component
                    )
                )
        return values

    if isinstance(complex_content, dict):
        for item in complex_content.get("items", []):
            if not isinstance(item, dict) or not isinstance(item.get("page"), int):
                continue
            suppressed_by_page.setdefault(int(item["page"]), []).extend(
                collect_suppressions(item.get("payload"))
            )
    for unit in translation.get("units", []):
        source_page = int(unit.get("page") or 0)
        kind = str(unit.get("kind") or "").lower()
        if (
            source_page in mapped_reference_pages
            and (
                kind in {"reference", "references", "bibliography"}
                or bool(unit.get("keep_source_reason"))
            )
        ):
            continue
        if source_page in replaced_pages:
            continue
        source_page_width, source_page_height = source_page_sizes.get(
            source_page,
            (None, None),
        )
        if is_nonsemantic_source_furniture_unit(
            unit,
            page_width=source_page_width,
            page_height=source_page_height,
        ):
            continue
        if str(unit.get("id") or "") in complex_replaced_unit_ids:
            continue
        expected = str(
            unit.get("translation") or unit.get("source") or ""
        )
        expected = remove_suppressed_texts(
            expected,
            suppressed_by_page.get(source_page, []),
        )
        expected_blocks = [
            _normalize_source_text(block)
            for block in re.split(r"\n\s*\n", str(expected))
            if _normalize_source_text(block)
        ]
        if not expected_blocks:
            continue
        unit_id = str(unit.get("id", "?"))
        mapped_pages = candidate_pages_for_unit(
            candidate_mapping,
            unit_id,
            source_page,
        )
        page_text = "".join(
            page_texts.get(page, "") for page in mapped_pages
        )
        block_total = sum(len(block) for block in expected_blocks)
        block_present = sum(
            len(block) for block in expected_blocks if block in page_text
        )
        total_chars += block_total
        present_chars += block_present
        unit_ratio = block_present / block_total if block_total else 1.0
        if unit_ratio < 0.95:
            missing_units.append(unit_id)
            if (
                _requires_exact_candidate_presence(
                    unit,
                    str(translation.get("source_language") or "und-Latn"),
                )
                and unit_ratio < 0.98
            ):
                missing_critical_units.append(unit_id)
    ratio = present_chars / total_chars if total_chars else 1.0
    minimum_ratio = float(
        translation.get("coverage", {}).get(
            "minimum_candidate_text_presence_ratio", 0.85
        )
    )
    warnings.append(
        f"候选译文文本出现率: {ratio:.3f} "
        f"({present_chars}/{total_chars}, 最低 {minimum_ratio:.3f})"
    )
    if ratio < minimum_ratio:
        errors.append(
            f"候选 PDF 未体现足够译文: {ratio:.3f} < {minimum_ratio:.3f}"
        )
    if missing_units and ratio < 1.0:
        warnings.append(
            "候选中未精确定位的译文单元: "
            + ", ".join(missing_units[:20])
            + (" ..." if len(missing_units) > 20 else "")
        )
    if missing_critical_units:
        errors.append(
            "候选 PDF 未精确体现以下高风险译文单元: "
            + ", ".join(missing_critical_units[:20])
            + (" ..." if len(missing_critical_units) > 20 else "")
        )

    retained_mapping = {
        str(entry.get("retained_region_id") or ""): entry
        for entry in (
            candidate_mapping.get("retained_regions", [])
            if isinstance(candidate_mapping, dict)
            else []
        )
        if isinstance(entry, dict)
    }
    source_page_mapping = {
        int(entry["source_page"]): [
            page
            for page in entry.get("candidate_pages", [])
            if isinstance(page, int)
        ]
        for entry in (
            candidate_mapping.get("source_pages", [])
            if isinstance(candidate_mapping, dict)
            else []
        )
        if isinstance(entry, dict)
        and isinstance(entry.get("source_page"), int)
    }
    retained_total = 0
    retained_present = 0
    missing_retained: list[str] = []
    for payload in retained_payloads or []:
        if (
            not isinstance(payload, dict)
            or payload.get("resolution")
            == "translated-nonreference-region"
        ):
            continue
        retained_id = str(payload.get("id") or "")
        entry = retained_mapping.get(retained_id)
        retained_candidate_pages = (
            [
                page
                for page in entry.get("candidate_pages", [])
                if isinstance(page, int)
            ]
            if isinstance(entry, dict)
            else []
        )
        candidate_pages = sorted(
            set(retained_candidate_pages)
            | set(
                source_page_mapping.get(
                    int(payload.get("page") or 0),
                    [],
                )
            )
        )
        candidate_text = "".join(
            page_texts.get(page, "") for page in candidate_pages
        )
        block_missing = False
        for block in payload.get("blocks", []):
            if (
                not isinstance(block, dict)
                or block.get("role") == "heading"
            ):
                continue
            expected = _normalize_source_text(
                str(block.get("text") or "")
            )
            if not expected:
                continue
            retained_total += len(expected)
            if expected in candidate_text:
                retained_present += len(expected)
            else:
                block_missing = True
        if block_missing or (payload.get("blocks") and not candidate_pages):
            missing_retained.append(retained_id or "?")
    if retained_total:
        retained_ratio = retained_present / retained_total
        warnings.append(
            f"候选保留题录文本出现率: {retained_ratio:.3f} "
            f"({retained_present}/{retained_total})"
        )
    if missing_retained:
        errors.append(
            "候选 PDF 未完整体现以下保留原文区域: "
            + ", ".join(missing_retained[:20])
            + (" ..." if len(missing_retained) > 20 else "")
        )
    candidate_handle.release()


def _candidate_page_text(page: Any) -> str:
    page_height = max(float(page.rect.height), 1.0)
    retained_blocks: list[str] = []
    for block in page.get_text("blocks"):
        if len(block) < 5:
            continue
        y0 = float(block[1])
        y1 = float(block[3])
        text = str(block[4] or "").strip()
        if not text:
            continue
        compact = re.sub(r"\s+", "", text)
        if (
            compact
            in READING_VERSION_LABELS
            and y1 <= page_height * 0.08
        ):
            continue
        if (
            y0 >= page_height * 0.92
            and re.fullmatch(r"\d{1,4}", compact)
        ):
            continue
        retained_blocks.append(text)
    return _normalize_source_text("\n".join(retained_blocks))


def _validate_figure_inventory(
    inventory: Any,
    require_resolved: bool,
    expected_candidate_hash: str | None,
    errors: list[str],
) -> None:
    inventory = _required_mapping(
        inventory,
        [
            "schema_version",
            "inventory_complete",
            "candidate_sha256",
            "scope_note",
            "items",
        ],
        "figure_inventory.json",
        errors,
    )
    items = inventory.get("items", []) if inventory else []
    if not isinstance(items, list):
        errors.append("figure_inventory.items 必须是数组")
        return
    allowed = {"translated", "not-applicable", "unresolved"}
    allowed_policies = {
        "translate-embedded-text",
        "translate-caption-only",
        "preserve-original",
        "omit-nonsemantic",
    }
    seen: set[str] = set()
    for index, item in enumerate(items):
        label = f"figure_inventory.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} 必须是对象")
            continue
        item_id = item.get("id")
        status = item.get("text_status")
        policy = item.get("translation_policy")
        if not isinstance(item_id, str) or not item_id:
            errors.append(f"{label}.id 不能为空")
        elif item_id in seen:
            errors.append(f"图表清单 ID 重复: {item_id}")
        else:
            seen.add(item_id)
        if status not in allowed:
            errors.append(f"{label}.text_status 必须是 {sorted(allowed)} 之一")
        if policy not in allowed_policies:
            errors.append(
                f"{label}.translation_policy 必须是 "
                f"{sorted(allowed_policies)} 之一"
            )
        elif policy == "translate-embedded-text" and status != "translated":
            errors.append(
                f"{label} 选择 translate-embedded-text 时必须完成图内文字翻译"
            )
        elif policy != "translate-embedded-text" and status not in {
            "not-applicable",
            "unresolved",
        }:
            errors.append(
                f"{label} 保留或省略原图时 text_status 应为 not-applicable"
            )
        if policy in {
            "translate-caption-only",
            "preserve-original",
            "omit-nonsemantic",
        } and not str(item.get("translation_policy_reason") or "").strip():
            errors.append(f"{label} 必须说明图片无需翻译或可以省略的理由")
        if require_resolved and status == "unresolved":
            errors.append(f"{label} 仍有未解决图内文字")
    if require_resolved:
        if inventory.get("inventory_complete") is not True:
            errors.append("figure_inventory.inventory_complete 尚未设为 true")
        if not isinstance(inventory.get("scope_note"), str) or not inventory.get(
            "scope_note", ""
        ).strip():
            errors.append("figure_inventory.scope_note 不能为空")
        if inventory.get("candidate_sha256") != expected_candidate_hash:
            errors.append("figure_inventory 对应的候选哈希不一致")


def _validate_review(
    review: Any,
    expected_role: str,
    expected_source_hash: str,
    expected_candidate_hash: str,
    errors: list[str],
    *,
    expected_page_count: int | None = None,
    require_all_pages: bool = False,
    require_pass: bool = True,
) -> None:
    required_keys = [
        "schema_version",
        "reviewer_role",
        "reviewer_id",
        "decision",
        "source_sha256",
        "candidate_sha256",
        "coverage",
        "issues",
    ]
    if require_all_pages:
        required_keys.append("reviewed_pages")
    review = _required_mapping(
        review,
        required_keys,
        f"{expected_role} review",
        errors,
    )
    if not review:
        return
    if review.get("reviewer_role") != expected_role:
        errors.append(f"{expected_role} review 的 reviewer_role 不一致")
    if not isinstance(review.get("reviewer_id"), str) or not review.get(
        "reviewer_id", ""
    ).strip():
        errors.append(f"{expected_role} review 缺少 reviewer_id")
    decision = review.get("decision")
    if require_pass:
        if decision != "PASS":
            errors.append(f"{expected_role} review 尚未 PASS")
    elif decision not in {"PASS", "FAIL"}:
        errors.append(f"{expected_role} review 尚未完成")
    if review.get("source_sha256") != expected_source_hash:
        errors.append(f"{expected_role} review 对应的原文哈希不一致")
    if review.get("candidate_sha256") != expected_candidate_hash:
        errors.append(f"{expected_role} review 对应的候选哈希不一致")
    coverage = review.get("coverage")
    if not isinstance(coverage, list) or not coverage:
        errors.append(f"{expected_role} review 缺少可核验 coverage")
    if require_all_pages:
        reviewed_pages = review.get("reviewed_pages")
        if not isinstance(reviewed_pages, list) or not all(
            isinstance(page, int) for page in reviewed_pages
        ):
            errors.append(f"{expected_role} review.reviewed_pages 必须是整数数组")
        elif expected_page_count is None:
            errors.append(f"{expected_role} review 缺少预期页数")
        else:
            expected_pages = set(range(1, expected_page_count + 1))
            actual_pages = set(reviewed_pages)
            if len(reviewed_pages) != len(actual_pages):
                errors.append(f"{expected_role} review.reviewed_pages 含重复页码")
            if actual_pages != expected_pages:
                missing = sorted(expected_pages - actual_pages)
                extra = sorted(actual_pages - expected_pages)
                errors.append(
                    f"{expected_role} review 未覆盖全部页面；"
                    f"缺少 {missing[:20]}，越界 {extra[:20]}"
                )
    issues = review.get("issues")
    if not isinstance(issues, list):
        errors.append(f"{expected_role} review 的 issues 必须是数组")
    else:
        for index, issue in enumerate(issues):
            if not isinstance(issue, dict):
                errors.append(f"{expected_role} review issue[{index}] 必须是对象")
            elif require_pass and issue.get("status") != "resolved":
                errors.append(
                    f"{expected_role} review issue[{index}] 尚未 resolved"
                )
        if not require_pass and decision == "FAIL" and not issues:
            errors.append(f"{expected_role} review 判为 FAIL 但没有记录问题")
    if not isinstance(review.get("reviewed_at"), str) or not review.get(
        "reviewed_at", ""
    ).strip():
        errors.append(f"{expected_role} review 缺少 reviewed_at")
    residual_risks = review.get("residual_risks")
    if not isinstance(residual_risks, list):
        errors.append(f"{expected_role} review 的 residual_risks 必须是数组")
    elif require_pass and residual_risks:
        errors.append(f"{expected_role} review 仍有未清零 residual_risks")


def _collect_completed_review_rounds(job_dir: Path, job: dict) -> list[dict]:
    records: list[dict] = []
    files = job.get("files", {})
    rounds_relative = files.get("review_rounds", "reviews/rounds.json")
    try:
        rounds_path = internal_job_path(job_dir, rounds_relative)
    except SkillError:
        rounds_path = job_dir / "__invalid_review_rounds__"
    if rounds_path.is_file():
        try:
            ledger = load_json(rounds_path)
            rounds = ledger.get("rounds", [])
            if isinstance(rounds, list):
                records.extend(item for item in rounds if isinstance(item, dict))
        except SkillError:
            pass

    for review_path in sorted(
        (job_dir / "history").glob("iteration-*/reviews/independent.json")
    ):
        try:
            records.append(load_json(review_path))
        except SkillError:
            continue

    current_relative = files.get(
        "independent_review",
        "reviews/independent.json",
    )
    try:
        current_path = internal_job_path(job_dir, current_relative)
        if current_path.is_file():
            records.append(load_json(current_path))
    except SkillError:
        pass

    unique: dict[tuple[str, str, str], dict] = {}
    for record in records:
        if record.get("decision") not in {"PASS", "FAIL"}:
            continue
        key = (
            str(record.get("candidate_sha256") or ""),
            str(record.get("reviewer_id") or ""),
            str(record.get("reviewed_at") or ""),
        )
        unique[key] = record
    return sorted(
        unique.values(),
        key=lambda item: (
            str(item.get("reviewed_at") or ""),
            int(item.get("round_number") or 0),
        ),
    )


def _validate_review_policy(
    job_dir: Path,
    job: dict,
    review_mode: str,
    source_hash: str,
    candidate_hash: str,
    provenance: Any,
    page_count: int,
    errors: list[str],
) -> None:
    review_settings = (
        job.get("review")
        if isinstance(job.get("review"), dict)
        else {}
    )
    producer_id = str(review_settings.get("producer_id") or "").strip()
    if not producer_id:
        errors.append("平衡档或精细档必须记录制作人 ID")
        return
    if not isinstance(provenance, dict):
        errors.append("候选缺少可核验的生成记录")
        return
    if provenance.get("producer_id") != producer_id:
        errors.append("候选生成记录中的制作人 ID 与作业不一致")

    required_rounds = {
        "independent": 1,
        "precise": 1,
    }[review_mode]
    records = _collect_completed_review_rounds(job_dir, job)
    if len(records) < required_rounds:
        errors.append(
            f"当前质量档位需要 {required_rounds} 轮完整独立复审；"
            f"目前只有 {len(records)} 轮"
        )
        return

    selected = records[-required_rounds:]
    for index, record in enumerate(selected, start=1):
        reviewer_id = str(record.get("reviewer_id") or "").strip()
        if reviewer_id == producer_id:
            errors.append(f"第 {index} 轮制作人与独立复审人不能相同")
        record_hash = str(record.get("candidate_sha256") or "")
        _validate_review(
            record,
            "independent",
            source_hash,
            record_hash,
            errors,
            expected_page_count=page_count,
            require_all_pages=True,
            require_pass=False,
        )
        if record.get("decision") == "PASS" and (
            record.get("issues") or record.get("residual_risks")
        ):
            errors.append(f"第 {index} 轮 PASS 复审仍保留问题或残余风险")

    last = selected[-1]
    last_hash = str(last.get("candidate_sha256") or "")
    last_decision = last.get("decision")
    if last_hash == candidate_hash:
        if last_decision != "PASS":
            errors.append("最后一轮复审未通过，且尚未完成本轮集中返修")
        return

    supersedes = (
        provenance.get("supersedes_candidate_sha256")
        if isinstance(provenance, dict)
        else None
    )
    if supersedes != last_hash or last_decision != "FAIL":
        errors.append(
            "最终候选必须是最后一轮复审通过的版本，"
            "或是紧接该轮 FAIL 后一次性集中返修得到的版本"
        )
        return

    files = job.get("files", {})
    evidence_paths: dict[str, Path] = {}
    for key, default in (
        ("post_repair_confirmation", "reviews/post-repair.json"),
        ("qa", "qa.json"),
    ):
        try:
            evidence_paths[key] = internal_job_path(
                job_dir,
                files.get(key, default),
            )
        except SkillError as exc:
            errors.append(str(exc))
    evidence_paths["completeness"] = (
        job_dir / "reviews" / "completeness-audit.json"
    )
    evidence_paths["comparison"] = (
        job_dir / "comparisons" / "manifest.json"
    )
    missing = [
        label
        for label, path in evidence_paths.items()
        if not path.is_file()
    ]
    if missing:
        errors.append(
            "集中返修后缺少确认依据: " + ", ".join(missing)
        )
        return
    try:
        confirmation = load_json(evidence_paths["post_repair_confirmation"])
    except SkillError as exc:
        errors.append(str(exc))
        return
    errors.extend(
        validate_post_repair_confirmation(
            confirmation,
            mode=review_mode,
            producer_id=producer_id,
            reviewer_id=str(last.get("reviewer_id") or "").strip(),
            source_hash=source_hash,
            base_candidate_hash=last_hash,
            candidate_hash=candidate_hash,
            page_count=page_count,
            qa_hash=sha256_file(evidence_paths["qa"]),
            completeness_hash=sha256_file(
                evidence_paths["completeness"]
            ),
            comparison_manifest_hash=sha256_file(
                evidence_paths["comparison"]
            ),
        )
    )


def _validate_retained_source(
    retained: Any,
    source_path: Path,
    page_count: int,
    require_reference_boundary: bool,
    errors: list[str],
) -> None:
    retained = _required_mapping(
        retained,
        ["schema_version", "items", "regions"],
        "retained_source.json",
        errors,
    )
    if not retained:
        return
    items = retained.get("items")
    regions = retained.get("regions")
    if not isinstance(items, list):
        errors.append("retained_source.items 必须是数组")
        items = []
    if not isinstance(regions, list):
        errors.append("retained_source.regions 必须是数组")
        regions = []

    allowed_categories = {
        "person-name",
        "proper-noun",
        "official-name",
        "abbreviation",
        "formula",
        "statistics",
        "code",
        "doi-url",
        "citation",
        "references",
        "bibliography",
        "source-term",
    }
    broad_regexes = {".*", ".+", "^.*$", "^.+$", r"[\s\S]*", r"[\s\S]+"}
    for index, item in enumerate(items):
        label = f"retained_source.items[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{label} 必须是对象")
            continue
        if item.get("category") not in allowed_categories:
            errors.append(f"{label}.category 不在允许范围")
        if not isinstance(item.get("reason"), str) or not item.get(
            "reason", ""
        ).strip():
            errors.append(f"{label}.reason 不能为空")
        value = item.get("pattern") or item.get("text")
        if not isinstance(value, str) or not value:
            errors.append(f"{label} 缺少 text 或 pattern")
        if item.get("is_regex"):
            if value in broad_regexes:
                errors.append(f"{label} 使用了过宽正则")
            if item.get("page") is None:
                errors.append(f"{label} 的正则保留项必须限定页码")
        if item.get("page") is not None and (
            not isinstance(item["page"], int)
            or not 1 <= item["page"] <= page_count
        ):
            errors.append(f"{label}.page 超出 1..{page_count}")

    reference_start = None
    source_doc = None
    source_handle = None
    if require_reference_boundary and source_path.is_file():
        try:

            source_handle = open_candidate_analysis(
                source_path,
                role="source",
            )
            source_doc = source_handle.document
            for index, page in enumerate(source_doc, 1):
                text = page.get_text("text")
                if _has_reference_heading(text):
                    reference_start = index
                    break
        except Exception as exc:
            errors.append(f"无法确认参考文献边界: {exc}")

    for index, region in enumerate(regions):
        label = f"retained_source.regions[{index}]"
        if not isinstance(region, dict):
            errors.append(f"{label} 必须是对象")
            continue
        page = region.get("page")
        bbox = region.get("bbox")
        category = region.get("category")
        if not isinstance(page, int) or not 1 <= page <= page_count:
            errors.append(f"{label}.page 超出 1..{page_count}")
        if (
            not isinstance(bbox, list)
            or len(bbox) != 4
            or not all(isinstance(value, (int, float)) for value in bbox)
            or float(bbox[2]) <= float(bbox[0])
            or float(bbox[3]) <= float(bbox[1])
        ):
            errors.append(f"{label}.bbox 必须是有效的 [x0, y0, x1, y1]")
        if category not in allowed_categories:
            errors.append(f"{label}.category 不在允许范围")
        if not isinstance(region.get("reason"), str) or not region.get(
            "reason", ""
        ).strip():
            errors.append(f"{label}.reason 不能为空")
        if (
            require_reference_boundary
            and category in {"references", "bibliography"}
            and isinstance(page, int)
            and (reference_start is None or page < reference_start)
        ):
            evidence = region.get("boundary_evidence")
            citation_block_confirmed = False
            if (
                evidence == "source-citation-block"
                and source_doc is not None
                and 1 <= page <= source_doc.page_count
            ):
                source_text = source_doc[page - 1].get_text("text")
                citation_block_confirmed = _has_source_citation_block(source_text)
            if not citation_block_confirmed:
                errors.append(f"{label} 位于无法确认的参考文献范围之前")
    if source_handle is not None:
        source_handle.release()


def _timed_validate_job(
    job_dir: Path,
    stage: str,
    advance: bool = False,
    *,
    status_override: str | None = None,
    qa_report: dict | None = None,
) -> dict:
    """校验作业是否满足某个阶段的门槛。

    `qa_report` 只接受调用方在同一进程里刚对同一份候选跑出的自动 QA 结果。
    传入时不再重跑 QA，但哈希绑定检查照旧执行：候选或原文哈希对不上仍然
    判定过期。不传入时行为不变，仍然自己重跑一次，因此单独调用本入口的
    外部使用者不会被降低门槛。
    """

    job_dir = job_dir.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        job = load_json(job_dir / "job.json")
    except SkillError as exc:
        return {"valid": False, "stage": stage, "errors": [str(exc)], "warnings": []}
    if status_override is not None:
        if status_override not in STATES:
            return {
                "valid": False,
                "stage": stage,
                "errors": [f"无效 status_override: {status_override!r}"],
                "warnings": [],
            }
        job["status"] = status_override

    job = _required_mapping(
        job,
        [
            "schema_version",
            "job_id",
            "status",
            "source",
            "translation",
            "route",
            "quality",
            "files",
            "integration",
        ],
        "job.json",
        errors,
    )
    if job.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"不支持的 schema_version: {job.get('schema_version')!r}")
    if job.get("status") not in STATES:
        errors.append(f"无效 job.status: {job.get('status')!r}")

    source = _required_mapping(
        job.get("source"),
        ["original_path", "job_path", "sha256", "page_count"],
        "job.source",
        errors,
    )
    translation_config = _required_mapping(
        job.get("translation"),
        ["source_language", "target_language"],
        "job.translation",
        errors,
    )
    route = _required_mapping(
        job.get("route"),
        ["recommended", "selected", "decision_reason"],
        "job.route",
        errors,
    )
    quality = _required_mapping(
        job.get("quality"),
        [
            "profile",
            "body_font_min_pt",
            "body_font_target_pt",
            "leading_target",
            "leading_exception_min",
        ],
        "job.quality",
        errors,
    )
    review_mode = _review_mode(job, errors)

    target_language = translation_config.get("target_language", "")
    try:
        canonical, _ = resolve_language_profile(target_language)
        if canonical != target_language:
            errors.append("job.json 必须保存规范化后的目标语言代码")
        if quality.get("profile") != canonical:
            errors.append("job.quality.profile 与目标语言不一致")
    except SkillError as exc:
        errors.append(str(exc))

    try:
        source_path = internal_job_path(
            job_dir, str(source.get("job_path", "source.pdf"))
        )
    except SkillError as exc:
        errors.append(str(exc))
        source_path = job_dir / "__invalid_source__"
    if not source_path.is_file():
        errors.append(f"缺少作业原文: {source_path}")
    else:
        actual_hash = sha256_file(source_path)
        if actual_hash != source.get("sha256"):
            errors.append("作业原文 SHA-256 与 job.json 不一致")
        try:
            handle = open_candidate_analysis(source_path, role="source")
            page_count = handle.document.page_count
            handle.release()
            if page_count != source.get("page_count"):
                errors.append("作业原文页数与 job.json 不一致")
        except Exception as exc:
            errors.append(f"无法复核作业原文页数: {exc}")

    if route.get("recommended") not in ROUTES:
        errors.append(f"无效建议路线: {route.get('recommended')!r}")
    _validate_complex_content_policy(
        route,
        int(source.get("page_count") or 0),
        stage,
        errors,
    )

    allowed_statuses = {
        "draft": {"initialized"},
        "translated": {"initialized", "translated"},
        "candidate": {"translated", "candidate"},
        "accepted": {"candidate", "accepted"},
        "finalized": {"accepted", "finalized"},
    }[stage]
    if job.get("status") not in allowed_statuses:
        errors.append(
            f"阶段状态不连续: {job.get('status')!r} 不能校验为 {stage!r}"
        )

    translation_data = None
    if STAGE_ORDER[stage] >= STAGE_ORDER["translated"]:
        if route.get("selected") not in ROUTES:
            errors.append("进入 translated 阶段前必须选择实际路线")
        if not isinstance(route.get("decision_reason"), str) or not route.get(
            "decision_reason", ""
        ).strip():
            errors.append("进入 translated 阶段前必须记录路线选择理由")
        _, translation_data = _load_job_file(
            job_dir, job, "translation", errors
        )
        _, retained_for_translation = _load_job_file(
            job_dir, job, "retained_source", errors
        )
        translation_data = _validate_translation(
            translation_data,
            int(source.get("page_count") or 0),
            target_language,
            errors,
            retained_source=retained_for_translation,
        )
        _validate_frozen_source_units(
            job_dir,
            job,
            translation_data,
            errors,
        )
        _validate_complex_content_payload(
            job_dir,
            job,
            route,
            errors,
        )

    _, retained = _load_job_file(job_dir, job, "retained_source", errors)
    if retained is not None:
        _validate_retained_source(
            retained,
            source_path,
            int(source.get("page_count") or 0),
            STAGE_ORDER[stage] >= STAGE_ORDER["accepted"],
            errors,
        )
        if STAGE_ORDER[stage] >= STAGE_ORDER["translated"]:
            _validate_source_text_coverage(
                source_path,
                translation_data or {},
                retained,
                errors,
                warnings,
            )

    expected_inventory_candidate_hash = None
    try:
        inventory_candidate_path = internal_job_path(
            job_dir, job.get("files", {}).get("candidate", "candidate.pdf")
        )
        if inventory_candidate_path.is_file():
            expected_inventory_candidate_hash = sha256_file(
                inventory_candidate_path
            )
    except SkillError:
        pass
    _, inventory = _load_job_file(job_dir, job, "figure_inventory", errors)
    _validate_figure_inventory(
        inventory,
        STAGE_ORDER[stage] >= STAGE_ORDER["accepted"],
        expected_inventory_candidate_hash,
        errors,
    )
    _load_job_file(job_dir, job, "layout_overrides", errors)

    if STAGE_ORDER[stage] >= STAGE_ORDER["candidate"]:
        candidate_mapping = None
        try:
            candidate_path = internal_job_path(
                job_dir, job.get("files", {}).get("candidate", "candidate.pdf")
            )
        except SkillError as exc:
            errors.append(str(exc))
            candidate_path = job_dir / "__invalid_candidate__"
        if not candidate_path.is_file():
            errors.append(f"缺少候选 PDF: {candidate_path}")
        elif (
            "candidate_page_map" in job.get("files", {})
            or (job_dir / "candidate-page-map.json").is_file()
        ):
            try:
                candidate_mapping = load_candidate_page_map(
                    job_dir,
                    job,
                    required=True,
                    candidate_path=candidate_path,
                    translation=translation_data or {},
                )
            except SkillError as exc:
                errors.append(str(exc))
        _, provenance = _load_job_file(
            job_dir, job, "candidate_provenance", errors
        )
        if provenance is not None:
            iteration = provenance.get("iteration")
            if not isinstance(iteration, int) or iteration < 1:
                errors.append("candidate_provenance.iteration 必须是正整数")
            renderer = provenance.get("renderer")
            if not isinstance(renderer, str) or not renderer.strip():
                errors.append("candidate_provenance.renderer 尚未记录")
            elif renderer == "academic-pdf-layout" and not re.fullmatch(
                r"[a-f0-9]{64}",
                str(provenance.get("renderer_build_id") or ""),
            ):
                errors.append(
                    "统一生成器候选缺少有效 renderer_build_id"
                )
            original_candidate = provenance.get("original_candidate_path")
            if not isinstance(original_candidate, str) or not original_candidate:
                errors.append(
                    "candidate_provenance.original_candidate_path 尚未记录"
                )
            if candidate_path.is_file() and provenance.get(
                "candidate_sha256"
            ) != sha256_file(candidate_path):
                errors.append("候选 PDF 与 candidate_provenance.json 哈希不一致")
            translation_path = internal_job_path(
                job_dir, job["files"]["translation"]
            )
            if provenance.get("translation_sha256") != sha256_file(
                translation_path
            ):
                errors.append("候选 PDF 对应的 translation.json 已发生变化")
            layout_path = internal_job_path(
                job_dir, job["files"]["layout_overrides"]
            )
            if provenance.get("layout_overrides_sha256") != sha256_file(
                layout_path
            ):
                errors.append("候选 PDF 对应的 layout_overrides.json 已发生变化")
            if candidate_mapping is not None:
                map_path = internal_job_path(
                    job_dir,
                    job.get("files", {}).get(
                        "candidate_page_map",
                        "candidate-page-map.json",
                    ),
                )
                if provenance.get(
                    "candidate_page_map_sha256"
                ) != sha256_file(map_path):
                    errors.append(
                        "候选 PDF 对应的 candidate-page-map.json 已发生变化"
                    )
        selected_fonts = quality.get("selected_fonts")
        if not isinstance(selected_fonts, list) or not selected_fonts:
            warnings.append("job.quality.selected_fonts 尚未记录实际使用字体")
        qa = None
        if qa_report is not None:
            qa = qa_report
        elif candidate_path.is_file():
            try:
                from qa_pdf import run_qa

                qa = run_qa(job_dir)
            except Exception as exc:
                errors.append(f"重新执行自动 QA 失败: {exc}")
        if qa is not None:
            if qa.get("automatic_decision") != "READY_FOR_HUMAN_REVIEW":
                errors.append("自动 QA 尚未允许进入人工审查")
            if candidate_path.is_file() and qa.get("candidate_sha256") != sha256_file(
                candidate_path
            ):
                errors.append("qa.json 对应的候选哈希已经过期")
            if qa.get("source_sha256") != source.get("sha256"):
                errors.append("qa.json 对应的原文哈希不一致")
        retained_payloads = None
        if retained is not None and source_path.is_file():
            try:
                from retained_source import extract_retained_regions

                retained_payloads = extract_retained_regions(
                    source_path,
                    retained,
                    translation_data or {},
                )
            except Exception as exc:
                errors.append(f"无法复核候选保留原文完整性: {exc}")
        _validate_candidate_text_presence(
            candidate_path,
            translation_data or {},
            candidate_mapping,
            errors,
            warnings,
            (
                load_json(
                    internal_job_path(
                        job_dir,
                        job.get("files", {}).get(
                            "complex_content_payload",
                            "complex_content.json",
                        ),
                    )
                )
                if internal_job_path(
                    job_dir,
                    job.get("files", {}).get(
                        "complex_content_payload",
                        "complex_content.json",
                    ),
                ).is_file()
                else None
            ),
            retained_payloads,
            source_path=source_path,
        )

    if STAGE_ORDER[stage] >= STAGE_ORDER["accepted"]:
        accepted_candidate_path = candidate_path
        accepted_candidate_hash = (
            sha256_file(accepted_candidate_path)
            if accepted_candidate_path.is_file()
            else ""
        )
        if review_mode == "legacy-double":
            _, independent = _load_job_file(
                job_dir, job, "independent_review", errors
            )
            _validate_review(
                independent,
                "independent",
                str(source.get("sha256", "")),
                accepted_candidate_hash,
                errors,
                expected_page_count=int(source.get("page_count") or 0),
                require_all_pages=False,
            )
        elif review_mode in {"independent", "precise"}:
            _validate_review_policy(
                job_dir,
                job,
                review_mode,
                str(source.get("sha256", "")),
                accepted_candidate_hash,
                provenance,
                int(source.get("page_count") or 0),
                errors,
            )

        if review_mode in {"legacy-double", "independent", "precise"}:
            comparison_manifest_path = (
                job_dir / "comparisons" / "manifest.json"
            )
            if not comparison_manifest_path.is_file():
                errors.append("缺少逐页对照图 manifest.json")
            else:
                try:
                    comparison_manifest = load_json(
                        comparison_manifest_path
                    )
                    if comparison_manifest.get(
                        "source_sha256"
                    ) != source.get("sha256"):
                        errors.append("逐页对照图对应的原文哈希不一致")
                    if comparison_manifest.get(
                        "candidate_sha256"
                    ) != accepted_candidate_hash:
                        errors.append("逐页对照图对应的候选哈希不一致")
                    expected_pages = int(source.get("page_count") or 0)
                    if comparison_manifest.get(
                        "page_count"
                    ) != expected_pages:
                        errors.append("逐页对照图页数记录不一致")
                    if comparison_manifest.get("schema_version") == "2.0":
                        sheet_files = comparison_manifest.get("sheet_files")
                        sheet_hashes = comparison_manifest.get("sheet_sha256")
                        sheet_index = comparison_manifest.get("sheet_index")
                        sheet_count = comparison_manifest.get("sheet_count")
                        if (
                            not isinstance(sheet_files, list)
                            or not isinstance(sheet_hashes, dict)
                            or not isinstance(sheet_index, list)
                            or sheet_count != len(sheet_files)
                            or sheet_count != len(sheet_index)
                            or sheet_count < 1
                        ):
                            errors.append("审查图包索引结构不完整")
                        else:
                            indexed_pages: list[int] = []
                            indexed_files: list[str] = []
                            for item in sheet_index:
                                if not isinstance(item, dict):
                                    errors.append("审查图包索引项必须是对象")
                                    continue
                                relative = item.get("file")
                                pages = item.get("pages")
                                if (
                                    not isinstance(relative, str)
                                    or not relative
                                    or not isinstance(pages, list)
                                    or not pages
                                    or not all(
                                        isinstance(page, int)
                                        for page in pages
                                    )
                                ):
                                    errors.append("审查图包索引项缺少文件或页码")
                                    continue
                                try:
                                    sheet_path = internal_job_path(
                                        job_dir / "comparisons",
                                        relative,
                                    )
                                except SkillError as exc:
                                    errors.append(str(exc))
                                    continue
                                if not sheet_path.is_file():
                                    errors.append(f"缺少审查图: {relative}")
                                elif sheet_hashes.get(relative) != sha256_file(
                                    sheet_path
                                ):
                                    errors.append(f"审查图哈希不一致: {relative}")
                                indexed_files.append(relative)
                                indexed_pages.extend(pages)
                            if indexed_files != sheet_files:
                                errors.append("审查图文件列表与索引顺序不一致")
                            if indexed_pages != list(
                                range(1, expected_pages + 1)
                            ):
                                errors.append(
                                    "审查图包未按顺序且无遗漏地覆盖全部页面"
                                )
                    else:
                        source_renders = list(
                            (job_dir / "renders" / "source").glob(
                                "page-*.png"
                            )
                        )
                        candidate_renders = list(
                            (job_dir / "renders" / "candidate").glob(
                                "page-*.png"
                            )
                        )
                        comparisons = list(
                            (job_dir / "comparisons").glob("page-*.png")
                        )
                        if not (
                            len(source_renders)
                            == len(candidate_renders)
                            == len(comparisons)
                            == expected_pages
                        ):
                            errors.append("逐页渲染或对照图数量不完整")
                    review_pdf_path = (
                        job_dir
                        / "comparisons"
                        / "source-vs-candidate.pdf"
                    )
                    if not review_pdf_path.is_file():
                        errors.append("缺少 source-vs-candidate.pdf")
                    elif comparison_manifest.get(
                        "review_pdf_sha256"
                    ) != sha256_file(review_pdf_path):
                        errors.append("source-vs-candidate.pdf 哈希不一致")
                except SkillError as exc:
                    errors.append(str(exc))

        if review_mode == "legacy-double":
            _, producer = _load_job_file(
                job_dir, job, "producer_review", errors
            )
            _validate_review(
                producer,
                "producer",
                str(source.get("sha256", "")),
                accepted_candidate_hash,
                errors,
            )
            if (
                isinstance(producer, dict)
                and isinstance(independent, dict)
                and producer.get("reviewer_id")
                and producer.get("reviewer_id")
                == independent.get("reviewer_id")
            ):
                errors.append(
                    "制作人自审与独立复审不能使用同一 reviewer_id"
                )

    if STAGE_ORDER[stage] >= STAGE_ORDER["finalized"]:
        _, finalization = _load_job_file(job_dir, job, "finalization", errors)
        if finalization is not None:
            if review_mode != "legacy-double" and finalization.get(
                "review_mode"
            ) != review_mode:
                errors.append("正式记录中的检查方式与作业选择不一致")
            formal_value = finalization.get("formal_pdf")
            if not isinstance(formal_value, str) or not formal_value:
                errors.append("finalization.formal_pdf 尚未记录")
            else:
                formal_path = Path(formal_value)
                workspace = job.get("workspace")
                if isinstance(workspace, dict):
                    output_value = workspace.get("output")
                    if not isinstance(output_value, str) or not output_value:
                        errors.append("job.workspace.output 尚未记录")
                    elif (
                        formal_path.expanduser().resolve().parent
                        != Path(output_value).expanduser().resolve()
                    ):
                        errors.append(
                            "正式译本必须直接写入当前批次的 output 目录"
                        )
                if not formal_path.is_file():
                    errors.append(f"正式译本不存在: {formal_path}")
                elif finalization.get("sha256") != sha256_file(formal_path):
                    errors.append("正式译本哈希与 finalization.json 不一致")
                else:
                    _, final_qa = _load_job_file(job_dir, job, "qa", errors)
                    if final_qa is not None and finalization.get(
                        "sha256"
                    ) != final_qa.get("candidate_sha256"):
                        errors.append("正式译本不是通过 QA 的候选文件")
            if job.get("integration", {}).get("zotero_required", True):
                zotero = _required_mapping(
                    finalization.get("zotero"),
                    [
                        "parent_item",
                        "source_attachment",
                        "translation_attachment",
                        "source_index_check",
                        "translation_index_check",
                    ],
                    "finalization.zotero",
                    errors,
                )
                for key in (
                    "parent_item",
                    "source_attachment",
                    "translation_attachment",
                ):
                    if not isinstance(zotero.get(key), str) or not zotero.get(key):
                        errors.append(f"Zotero 字段 {key!r} 尚未记录")
                if zotero.get("source_index_check") is not True:
                    errors.append("Zotero 原文索引尚未读回验证")
                if zotero.get("translation_index_check") is not True:
                    errors.append("Zotero 译文索引尚未读回验证")

    report = {
        "valid": not errors,
        "stage": stage,
        "job_dir": str(job_dir),
        "errors": errors,
        "warnings": warnings,
    }
    if report["valid"] and advance:
        stage_status = {
            "draft": "initialized",
            "translated": "translated",
            "candidate": "candidate",
            "accepted": "accepted",
            "finalized": "finalized",
        }[stage]
        job["status"] = stage_status
        write_json(job_dir / "job.json", job)
        report["advanced_to"] = stage_status
    return report



def validate_job(*args, **kwargs):
    """计时包装：阶段耗时进入性能基线，行为与实现完全一致。"""

    with perf_trace.stage("validate_job"):
        return _timed_validate_job(*args, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser(description="校验学术 PDF 译制作业的阶段完整性")
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--stage",
        choices=list(STAGE_ORDER),
        default="draft",
    )
    parser.add_argument(
        "--advance",
        action="store_true",
        help="校验通过后将 job.status 推进到对应状态",
    )
    args = parser.parse_args()
    report = validate_job(args.job_dir, args.stage, args.advance)
    print(f"阶段: {report['stage']}")
    print(f"结果: {'PASS' if report['valid'] else 'FAIL'}")
    for warning in report["warnings"]:
        print(f"警告: {warning}")
    for error in report["errors"]:
        print(f"错误: {error}")
    if report.get("advanced_to"):
        print(f"状态已推进: {report['advanced_to']}")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
