"""译文真实性检查：判断一个单元是否真的被翻译，或者是否真的可以保留原文。

这个模块只做可重复的程序判断，不做语义评价。它回答两个问题：

1. 译文是不是目标语言？跨语言任务里，标准化后与原文相同的普通正文和标题
   一律拒绝，目标语言字符太少也拒绝。
2. 保留原文的理由站不站得住？保留必须给出结构化的 ``keep_source_code``，
   每个 code 只能用在允许的单元类型或明确的原文片段上。自由文本
   ``keep_source_reason`` 只是补充说明，单独不能获得豁免。

检查分三层：单元、批次、文档。任何一层不过，整篇的完整性状态就不能算通过。
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from _common import resolve_language_profile, target_character_count
from content_anchors import DOI_RE, URL_RE

SCHEMA_VERSION = "1.0"

#: 允许的结构化保留原文理由。自由文本理由不在此列，不能单独豁免。
KEEP_SOURCE_CODES = (
    "person-name",
    "official-product-name",
    "acronym",
    "formula-or-statistical-symbol",
    "doi-or-url",
    "citation",
    "bibliography-entry",
    "required-original-term",
    "publication-front-matter",
)

#: 普通正文类单元：这些类型不允许整单元保留原文。
PROSE_KINDS = ("body", "heading", "abstract", "title", "section-heading")

#: 署名区单元：作者、单位、出版元数据、DOI/URL。
FRONT_MATTER_KINDS = (
    "author-block",
    "affiliation",
    "publication-metadata",
    "doi-url",
)

#: 这些单元本来就以原文形态存在：人名、单位、DOI、网址、题录。
#: 拿正文的目标语言占比门槛去量它们，只会逼出"本文共有三位作者……"
#: 这种硬凑的解释句。门槛不该管人名和网址，所以这里免除比例检查。
#: 正文、标题、摘要不在此列，它们的门槛一字不动。
SOURCE_FORM_KINDS = FRONT_MATTER_KINDS + ("reference", "bibliography")

#: 同样的判断，按 unit_bindings.json 给出的元素角色表达。
#: 角色由原文元素清单算出，比 kind_hint 可靠，两者取其一命中即可。
FRONT_MATTER_ROLES = ("author", "affiliation", "publication-metadata")
REFERENCE_ROLES = ("reference-entry",)
SOURCE_FORM_ROLES = FRONT_MATTER_ROLES + REFERENCE_ROLES

#: 目标语言字符占比下限。三层分别收紧，不允许只看全篇一个比例。
UNIT_TARGET_SCRIPT_RATIO_MIN = 0.50
BATCH_TARGET_SCRIPT_RATIO_MIN = 0.70
DOCUMENT_TARGET_SCRIPT_RATIO_MIN = 0.80

#: 全篇保留原文的字符占比上限。超过它的作业不是译本。
DOCUMENT_KEEP_SOURCE_CONTENT_RATIO_MAX = 0.50

#: 判定“散文”所需的最少实词数量。低于它的单元只做等同检查，不做比例检查。
PROSE_WORD_MIN = 3
PROSE_WORD_CHAR_MIN = 3

#: 各 code 允许的最长原文片段长度。
FRAGMENT_LIMITS = {
    "person-name": 80,
    "official-product-name": 80,
    "acronym": 24,
    "formula-or-statistical-symbol": 200,
    "doi-or-url": 200,
    "citation": 60,
    "required-original-term": 80,
}

REFERENCE_KIND_PREFIXES = ("reference", "bibliography")
FRONT_MATTER_KIND_PREFIXES = FRONT_MATTER_KINDS
#: 与 retained_source.py 的 REFERENCE_CATEGORIES 保持一致，
#: 但本模块不导入 PyMuPDF，因此在这里重新声明常量。
REFERENCE_CATEGORIES = frozenset({"references", "bibliography"})

ACRONYM_TOKEN_RE = re.compile(r"(?<![A-Za-z0-9-])[A-Z][A-Z0-9-]{1,12}(?![A-Za-z0-9-])")
#: 邮箱、arXiv 编号和 URL、DOI 一样是持久标识符，不是散文。
#: 翻译时本来就该原样保留，不能算成"没翻的英文"。
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
ARXIV_RE = re.compile(
    r"arxiv\s*:\s*(?:[a-z-]+(?:\.[A-Z]{2})?/)?\d{4}\.?\d{4,5}(?:v\d+)?",
    re.IGNORECASE,
)
CITATION_BRACKET_RE = re.compile(r"\[[^\]]{0,40}\]")
ACRONYM_FULL_RE = re.compile(r"[A-Z0-9][A-Z0-9\-/&.]{0,23}")
AUTHOR_YEAR_CITATION_RE = re.compile(
    r"\((?:[^()]{0,80})(?:19|20)\d{2}[a-z]?(?:[^()]{0,20})\)"
)
NUMERIC_CITATION_RE = re.compile(r"\[\s*\d+(?:\s*[-–,;]\s*\d+)*\s*\]")
SENTENCE_INSIDE_RE = re.compile(r"[.!?。！？][\s\"'”’)\]]")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ'-]*")
#: 任意语言的一个字母。整段没有字母的单元没有可译的内容。
LETTER_RE = re.compile(r"[^\W\d_]", re.UNICODE)
CONTENT_RE = re.compile(r"[\w㐀-鿿]", re.UNICODE)


class TruthfulnessError(ValueError):
    """输入结构本身不合法，检查无法进行。"""


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def normalize_for_comparison(text: str) -> str:
    """标准化：NFKC、去零宽、折叠空白、去首尾标点、casefold。"""

    value = unicodedata.normalize("NFKC", text or "")
    for char in ("​", "⁠", "­", "﻿"):
        value = value.replace(char, "")
    value = re.sub(r"\s+", " ", value).strip()
    value = value.strip(" .,;:!?\"'()[]{}“”‘’·—–-")
    return value.casefold()


def _prose_words(text: str) -> list[str]:
    return [
        word
        for word in WORD_RE.findall(text or "")
        if len(word) >= PROSE_WORD_CHAR_MIN
    ]


def is_prose(source: str) -> bool:
    """这一段是不是真的散文。

    判断前先剥掉 URL、DOI、邮箱、缩写和引文标记：一行作者邮箱加主页链接，
    拆开看有十几个"单词"，但它一句话都没有，不该按散文要求目标语言占比。
    """

    return len(_prose_words(_protected_stripped(source, ()))) >= PROSE_WORD_MIN


def _protected_stripped(text: str, terminology_terms: tuple[str, ...]) -> str:
    value = URL_RE.sub(" ", text or "")
    value = DOI_RE.sub(" ", value)
    value = EMAIL_RE.sub(" ", value)
    value = ARXIV_RE.sub(" ", value)
    value = CITATION_BRACKET_RE.sub(" ", value)
    value = ACRONYM_TOKEN_RE.sub(" ", value)
    for term in terminology_terms:
        if term:
            value = re.sub(re.escape(term), " ", value, flags=re.IGNORECASE)
    return value


def residual_latin_letters(
    text: str,
    terminology_terms: tuple[str, ...] = (),
) -> int:
    """译文里既不是目标语言、也不属于豁免片段的拉丁字母数量。"""

    return len(
        re.findall(
            r"[A-Za-zÀ-ÖØ-öø-ÿ]",
            _protected_stripped(text, terminology_terms),
        )
    )


def target_script_ratio(
    text: str,
    writing_system: str,
    terminology_terms: tuple[str, ...] = (),
) -> float | None:
    """目标文字字符在“有意义字母”里的占比；无法判定时返回 None。"""

    target = target_character_count(text, writing_system)
    residual = residual_latin_letters(text, terminology_terms)
    total = target + residual
    if total == 0:
        return None
    return target / total


def content_length(text: str) -> int:
    return len(CONTENT_RE.findall(text or ""))


def base_language(code: str) -> str:
    return str(code or "").split("-")[0].strip().lower()


def is_cross_language(source_language: str, target_language: str) -> bool:
    source = base_language(source_language)
    target = base_language(target_language)
    if not source or not target:
        return True
    return source != target


def _terminology_terms(terminology: Any) -> tuple[str, ...]:
    terms: list[str] = []
    for entry in terminology or []:
        if not isinstance(entry, dict):
            continue
        for key in ("source", "target", "preferred", "translation"):
            value = _text(entry.get(key))
            if value:
                terms.append(value)
        for value in entry.get("allowed_variants", []) or []:
            if isinstance(value, str) and value.strip():
                terms.append(value.strip())
        for value in entry.get("source_variants", []) or []:
            if isinstance(value, str) and value.strip():
                terms.append(value.strip())
    # 长词优先剥离，避免短词先吃掉长词的一部分。
    return tuple(sorted(set(terms), key=len, reverse=True))


def _keep_original_terms(terminology: Any) -> set[str]:
    """target 与 source 相同的术语，才是“必须保留原文”的术语。"""

    keep: set[str] = set()
    for entry in terminology or []:
        if not isinstance(entry, dict):
            continue
        source = _text(entry.get("source"))
        target = _text(
            entry.get("target")
            or entry.get("preferred")
            or entry.get("translation")
        )
        if not source or not target:
            continue
        if normalize_for_comparison(source) != normalize_for_comparison(target):
            continue
        keep.add(normalize_for_comparison(source))
        for value in entry.get("source_variants", []) or []:
            if isinstance(value, str) and value.strip():
                keep.add(normalize_for_comparison(value))
    return keep


def _bbox(value: Any) -> tuple[float, float, float, float] | None:
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        return None
    try:
        x0, y0, x1, y1 = (float(item) for item in value)
    except (TypeError, ValueError):
        return None
    return (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def _covered_by_reference_region(
    unit: dict[str, Any],
    reference_regions: list[dict[str, Any]],
) -> str | None:
    """单元是否落在某个已登记的参考文献保留区域里；返回区域 ID。"""

    unit_box = _bbox(unit.get("source_bbox"))
    if unit_box is None:
        return None
    try:
        page = int(unit.get("page") or 0)
    except (TypeError, ValueError):
        return None
    ux0, uy0, ux1, uy1 = unit_box
    unit_area = max((ux1 - ux0) * (uy1 - uy0), 1e-6)
    for region in reference_regions:
        if int(region.get("page") or 0) != page:
            continue
        region_box = _bbox(region.get("effective_bbox") or region.get("bbox"))
        if region_box is None:
            continue
        rx0, ry0, rx1, ry1 = region_box
        overlap = max(0.0, min(ux1, rx1) - max(ux0, rx0)) * max(
            0.0, min(uy1, ry1) - max(uy0, ry0)
        )
        if overlap / unit_area >= 0.80:
            return str(region.get("id") or f"p{page:04d}-retained")
    return None


def reference_regions(retained: Any) -> list[dict[str, Any]]:
    """从 retained_source.json 或已展开的 payload 中取出参考文献区域。

    只接受同时有页码、坐标和参考文献类别的记录，缺一不可。
    """

    if isinstance(retained, dict):
        raw = retained.get("regions", [])
    elif isinstance(retained, list):
        raw = retained
    else:
        raw = []
    regions: list[dict[str, Any]] = []
    for index, region in enumerate(raw):
        if not isinstance(region, dict):
            continue
        if str(region.get("category") or "") not in REFERENCE_CATEGORIES:
            continue
        if _bbox(region.get("effective_bbox") or region.get("bbox")) is None:
            continue
        try:
            page = int(region.get("page"))
        except (TypeError, ValueError):
            continue
        entry = dict(region)
        entry["page"] = page
        entry.setdefault("id", f"p{page:04d}-retained-{index + 1:03d}")
        regions.append(entry)
    return regions


def has_translatable_letters(source: str) -> bool:
    """这段原文里有没有可译的内容。

    坐标轴刻度 "0 5 10 15"、页码 "561"、纯符号片段没有字母，任何语言写
    出来都是同一串字符。要求它们"必须和原文不同"，只会逼出把数字改写成
    中文数字这种破坏图表的做法。正文一定含字母，这条门槛碰不到它。
    """

    return bool(LETTER_RE.search(source or ""))


def unit_kind(unit: dict[str, Any]) -> str:
    return str(unit.get("kind") or unit.get("kind_hint") or "").lower()


def unit_element_role(unit: dict[str, Any]) -> str:
    """单元绑定到的原文元素角色，由 unit_bindings.json 算出。"""

    return str(unit.get("element_role") or "").lower()


def _is_reference_kind(unit: dict[str, Any]) -> bool:
    return unit_kind(unit).startswith(REFERENCE_KIND_PREFIXES) or (
        unit_element_role(unit) in REFERENCE_ROLES
    )


def _is_front_matter_kind(unit: dict[str, Any]) -> bool:
    return unit_kind(unit).startswith(FRONT_MATTER_KIND_PREFIXES) or (
        unit_element_role(unit) in FRONT_MATTER_ROLES
    )


def is_source_form_kind(unit: dict[str, Any]) -> bool:
    """这个单元本来就该以原文形态出现吗。"""

    return unit_kind(unit).startswith(SOURCE_FORM_KINDS) or (
        unit_element_role(unit) in SOURCE_FORM_ROLES
    )


def _fragment_problem(code: str, source: str) -> str | None:
    limit = FRAGMENT_LIMITS.get(code)
    if limit is not None and len(source) > limit:
        return f"{code} 只能用于不超过 {limit} 字符的原文片段，当前 {len(source)} 字符"
    return None


def _check_person_or_product(code: str, source: str) -> str | None:
    problem = _fragment_problem(code, source)
    if problem:
        return problem
    if SENTENCE_INSIDE_RE.search(source):
        return f"{code} 不能用于含完整句子的单元"
    words = WORD_RE.findall(source)
    if not words:
        return f"{code} 需要至少一个词形，当前原文没有可识别的词"
    capitalized = sum(1 for word in words if word[:1].isupper())
    if capitalized / len(words) < 0.6:
        return f"{code} 要求原文以专名形式出现（多数词首字母大写）"
    return None


def _check_acronym(source: str) -> str | None:
    if not ACRONYM_FULL_RE.fullmatch(source):
        return "acronym 只能用于整段就是缩写本身的单元"
    return None


def _check_formula(source: str) -> str | None:
    problem = _fragment_problem("formula-or-statistical-symbol", source)
    if problem:
        return problem
    prose = [word for word in _prose_words(source) if not word.isupper()]
    if len(prose) > 2:
        return (
            "formula-or-statistical-symbol 只能用于公式或统计符号片段，"
            f"当前含 {len(prose)} 个普通词"
        )
    return None


def _check_doi_or_url(source: str) -> str | None:
    problem = _fragment_problem("doi-or-url", source)
    if problem:
        return problem
    stripped = DOI_RE.sub(" ", URL_RE.sub(" ", source))
    if not (URL_RE.search(source) or DOI_RE.search(source)):
        return "doi-or-url 需要原文中真的含 DOI 或 URL"
    if content_length(stripped) > 12:
        return "doi-or-url 只能用于基本只有 DOI 或 URL 的单元"
    return None


def _check_citation(source: str) -> str | None:
    problem = _fragment_problem("citation", source)
    if problem:
        return problem
    stripped = NUMERIC_CITATION_RE.sub(" ", source)
    stripped = AUTHOR_YEAR_CITATION_RE.sub(" ", stripped)
    if stripped.strip() == source.strip():
        return "citation 需要原文本身就是引文标记"
    if content_length(stripped) > 8:
        return "citation 只能用于基本只有引文标记的单元"
    return None


def _check_required_original_term(
    source: str,
    keep_original_terms: set[str],
) -> str | None:
    problem = _fragment_problem("required-original-term", source)
    if problem:
        return problem
    if normalize_for_comparison(source) not in keep_original_terms:
        return (
            "required-original-term 需要 translation.terminology 中登记一条"
            "target 与 source 相同的术语"
        )
    return None


def check_keep_source(
    unit: dict[str, Any],
    code: str,
    *,
    reference_regions_list: list[dict[str, Any]],
    keep_original_terms: set[str],
) -> tuple[str | None, dict[str, Any]]:
    """返回 (问题说明或 None, 证据)。"""

    source = _text(unit.get("source"))
    evidence: dict[str, Any] = {"keep_source_code": code}
    if code not in KEEP_SOURCE_CODES:
        return (
            "keep_source_code 必须取自固定枚举: " + ", ".join(KEEP_SOURCE_CODES),
            evidence,
        )
    if code == "bibliography-entry":
        if _is_reference_kind(unit):
            evidence["basis"] = "reference-unit-kind"
            return None, evidence
        region_id = _covered_by_reference_region(unit, reference_regions_list)
        if region_id:
            evidence["basis"] = "retained-source-region"
            evidence["retained_region_id"] = region_id
            return None, evidence
        return (
            "bibliography-entry 需要单元类型是 reference/bibliography、"
            "元素角色是 reference-entry，"
            "或 retained_source.json 中有覆盖该单元坐标的参考文献区域",
            evidence,
        )
    if code == "publication-front-matter":
        if _is_front_matter_kind(unit):
            evidence["basis"] = "front-matter-unit-kind"
            return None, evidence
        return (
            "publication-front-matter 只能用在作者、单位、出版元数据或 "
            "DOI/URL 单元上（单元类型或元素角色任一命中即可）",
            evidence,
        )
    if code in {"person-name", "official-product-name"}:
        return _check_person_or_product(code, source), evidence
    if code == "acronym":
        return _check_acronym(source), evidence
    if code == "formula-or-statistical-symbol":
        return _check_formula(source), evidence
    if code == "doi-or-url":
        return _check_doi_or_url(source), evidence
    if code == "citation":
        return _check_citation(source), evidence
    return _check_required_original_term(source, keep_original_terms), evidence


def check_translation_language(
    unit: dict[str, Any],
    translation: str,
    *,
    cross_language: bool,
    writing_system: str,
    terminology_terms: tuple[str, ...],
) -> list[dict[str, Any]]:
    """跨语言任务里，译文必须真的是目标语言。"""

    problems: list[dict[str, Any]] = []
    source = _text(unit.get("source"))
    if not cross_language:
        return problems
    if not has_translatable_letters(source):
        # 纯数字或纯符号：照抄就是正确译法。
        return problems
    if normalize_for_comparison(translation) == normalize_for_comparison(source):
        problems.append(
            {
                "code": "TRANSLATION_EQUALS_SOURCE",
                "message": "标准化后译文与原文相同；跨语言任务不接受原样照抄",
            }
        )
        return problems
    if writing_system == "latin":
        # 目标语言同为拉丁字母时，字符集无法区分语种，只做等同检查。
        return problems
    if not is_prose(source):
        return problems
    if is_source_form_kind(unit):
        # 人名、单位、DOI、网址、题录：原文形态本身就是正确形态。
        return problems
    target_chars = target_character_count(translation, writing_system)
    if target_chars == 0:
        problems.append(
            {
                "code": "TARGET_LANGUAGE_ABSENT",
                "message": "译文里没有任何目标语言字符",
            }
        )
        return problems
    ratio = target_script_ratio(translation, writing_system, terminology_terms)
    if ratio is not None and ratio < UNIT_TARGET_SCRIPT_RATIO_MIN:
        problems.append(
            {
                "code": "TARGET_LANGUAGE_RATIO_LOW",
                "message": (
                    f"目标语言字符占比 {ratio:.2f} 低于单元下限 "
                    f"{UNIT_TARGET_SCRIPT_RATIO_MIN:.2f}"
                ),
                "ratio": round(ratio, 4),
            }
        )
    return problems


def evaluate_unit(
    unit: dict[str, Any],
    *,
    cross_language: bool,
    writing_system: str,
    terminology_terms: tuple[str, ...],
    keep_original_terms: set[str],
    reference_regions_list: list[dict[str, Any]],
) -> dict[str, Any]:
    """判定单个单元：translated / kept-source / invalid。"""

    unit_id = str(unit.get("id") or "")
    source = _text(unit.get("source"))
    translation = _text(unit.get("translation"))
    keep_code = _text(unit.get("keep_source_code"))
    keep_reason = _text(unit.get("keep_source_reason"))
    problems: list[dict[str, Any]] = []
    evidence: dict[str, Any] = {}

    if translation and (keep_code or keep_reason):
        problems.append(
            {
                "code": "TRANSLATION_AND_KEEP_SOURCE_CONFLICT",
                "message": "不能同时给出译文和保留原文声明",
            }
        )
    elif translation:
        problems.extend(
            check_translation_language(
                unit,
                translation,
                cross_language=cross_language,
                writing_system=writing_system,
                terminology_terms=terminology_terms,
            )
        )
    elif keep_code or keep_reason:
        if not keep_code:
            problems.append(
                {
                    "code": "KEEP_SOURCE_CODE_MISSING",
                    "message": (
                        "保留原文必须填写结构化 keep_source_code；"
                        "自由文本 keep_source_reason 不能单独豁免。"
                        "旧作业请为每个保留单元补写 keep_source_code，"
                        "或改为提供译文"
                    ),
                }
            )
        else:
            problem, keep_evidence = check_keep_source(
                unit,
                keep_code,
                reference_regions_list=reference_regions_list,
                keep_original_terms=keep_original_terms,
            )
            evidence.update(keep_evidence)
            if problem:
                problems.append(
                    {
                        "code": "KEEP_SOURCE_CODE_NOT_ALLOWED_FOR_UNIT",
                        "message": problem,
                    }
                )
    else:
        problems.append(
            {
                "code": "UNIT_NOT_TRANSLATED",
                "message": "既没有译文，也没有结构化的保留原文声明",
            }
        )

    if problems:
        state = "invalid"
    elif translation:
        state = "translated"
    else:
        state = "kept-source"
    return {
        "unit_id": unit_id,
        "page": unit.get("page"),
        "kind": str(unit.get("kind") or unit.get("kind_hint") or ""),
        "state": state,
        "source_content_chars": content_length(source),
        "problems": [dict(problem, unit_id=unit_id) for problem in problems],
        "evidence": evidence,
    }


def _aggregate_ratio(
    translations: list[str],
    writing_system: str,
    terminology_terms: tuple[str, ...],
) -> float | None:
    target = sum(
        target_character_count(text, writing_system) for text in translations
    )
    residual = sum(
        residual_latin_letters(text, terminology_terms) for text in translations
    )
    if target + residual == 0:
        return None
    return target / (target + residual)


class _Context:
    """一次检查共用的语言、术语和保留区域上下文。"""

    __slots__ = (
        "source_language",
        "target_language",
        "writing_system",
        "cross_language",
        "terminology_terms",
        "keep_original_terms",
        "reference_regions",
    )

    def __init__(
        self,
        translation_document: dict[str, Any],
        retained_source: Any = None,
    ) -> None:
        if not isinstance(translation_document, dict):
            raise TruthfulnessError("translation 必须是对象")
        self.source_language = str(
            translation_document.get("source_language") or ""
        )
        self.target_language = str(
            translation_document.get("target_language") or ""
        )
        _, profile = resolve_language_profile(self.target_language)
        self.writing_system = str(profile.get("writing_system") or "latin")
        self.cross_language = is_cross_language(
            self.source_language,
            self.target_language,
        )
        terminology = translation_document.get("terminology", [])
        self.terminology_terms = _terminology_terms(terminology)
        self.keep_original_terms = _keep_original_terms(terminology)
        self.reference_regions = reference_regions(retained_source)

    def evaluate(self, unit: dict[str, Any]) -> dict[str, Any]:
        return evaluate_unit(
            unit,
            cross_language=self.cross_language,
            writing_system=self.writing_system,
            terminology_terms=self.terminology_terms,
            keep_original_terms=self.keep_original_terms,
            reference_regions_list=self.reference_regions,
        )

    def ratio(self, translations: list[str]) -> float | None:
        if not self.cross_language or self.writing_system == "latin":
            return None
        if not translations:
            return None
        return _aggregate_ratio(
            translations,
            self.writing_system,
            self.terminology_terms,
        )


def evaluate_batch(
    units: list[dict[str, Any]],
    *,
    translation_document: dict[str, Any],
    retained_source: Any = None,
    batch_id: str = "",
) -> dict[str, Any]:
    """写回前的批次检查：逐单元判定，再看整批的目标语言占比。

    只做单元层和批次层。文档层留给完整性审查，因为单个批次可以合法地
    整批都是参考文献题录。
    """

    context = _Context(translation_document, retained_source)
    verdicts = [context.evaluate(unit) for unit in units]
    problems = [
        problem for verdict in verdicts for problem in verdict["problems"]
    ]
    # 署名、DOI、题录即使被翻了，也不该拉低整批的目标语言占比：
    # 它们的正确形态本来就含大量原文字符。
    translated = [
        _text(unit.get("translation"))
        for unit, verdict in zip(units, verdicts, strict=True)
        if verdict["state"] == "translated" and not is_source_form_kind(unit)
    ]
    ratio = context.ratio(translated)
    if ratio is not None and ratio < BATCH_TARGET_SCRIPT_RATIO_MIN:
        problems.append(
            {
                "code": "BATCH_TARGET_LANGUAGE_RATIO_LOW",
                "batch_id": batch_id,
                "message": (
                    f"整批译文的目标语言字符占比 {ratio:.2f} 低于批次下限 "
                    f"{BATCH_TARGET_SCRIPT_RATIO_MIN:.2f}"
                ),
            }
        )
    return {
        "schema_version": SCHEMA_VERSION,
        "batch_id": batch_id,
        "unit_count": len(units),
        "target_script_ratio": None if ratio is None else round(ratio, 4),
        "units": verdicts,
        "problems": problems,
        "accepted": not problems,
    }


def evaluate_translation(
    translation_document: dict[str, Any],
    *,
    retained_source: Any = None,
    batches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """对整篇 translation.json 做单元、批次、文档三层检查。

    ``batches`` 是可选的批次划分，形如 ``[{"batch_id": ..., "unit_ids": [...]}]``。
    """

    if not isinstance(translation_document, dict):
        raise TruthfulnessError("translation 必须是对象")
    units = [
        unit
        for unit in translation_document.get("units", [])
        if isinstance(unit, dict)
    ]
    source_language = str(translation_document.get("source_language") or "")
    target_language = str(translation_document.get("target_language") or "")
    _, profile = resolve_language_profile(target_language)
    writing_system = str(profile.get("writing_system") or "latin")
    cross_language = is_cross_language(source_language, target_language)
    terminology = translation_document.get("terminology", [])
    terminology_terms = _terminology_terms(terminology)
    keep_original_terms = _keep_original_terms(terminology)
    regions = reference_regions(retained_source)

    verdicts = [
        evaluate_unit(
            unit,
            cross_language=cross_language,
            writing_system=writing_system,
            terminology_terms=terminology_terms,
            keep_original_terms=keep_original_terms,
            reference_regions_list=regions,
        )
        for unit in units
    ]
    by_id = {verdict["unit_id"]: verdict for verdict in verdicts}
    by_unit_id = {str(unit.get("id") or ""): unit for unit in units}
    translation_by_id = {
        str(unit.get("id") or ""): _text(unit.get("translation"))
        for unit in units
    }
    problems = [problem for verdict in verdicts for problem in verdict["problems"]]

    # 批次层：每个批次的译文合起来也必须是目标语言。
    batch_reports: list[dict[str, Any]] = []
    for batch in batches or []:
        unit_ids = [str(value) for value in batch.get("unit_ids", [])]
        texts = [
            translation_by_id.get(unit_id, "")
            for unit_id in unit_ids
            if by_id.get(unit_id, {}).get("state") == "translated"
            and not is_source_form_kind(by_unit_id.get(unit_id, {}))
        ]
        ratio = (
            _aggregate_ratio(texts, writing_system, terminology_terms)
            if cross_language and writing_system != "latin" and texts
            else None
        )
        entry = {
            "batch_id": str(batch.get("batch_id") or ""),
            "unit_count": len(unit_ids),
            "translated_units": len(texts),
            "target_script_ratio": None if ratio is None else round(ratio, 4),
        }
        if ratio is not None and ratio < BATCH_TARGET_SCRIPT_RATIO_MIN:
            problem = {
                "code": "BATCH_TARGET_LANGUAGE_RATIO_LOW",
                "batch_id": entry["batch_id"],
                "message": (
                    f"批次 {entry['batch_id']} 目标语言字符占比 {ratio:.2f} "
                    f"低于批次下限 {BATCH_TARGET_SCRIPT_RATIO_MIN:.2f}"
                ),
            }
            problems.append(problem)
            entry["problem"] = problem["code"]
        batch_reports.append(entry)

    # 文档层：全篇比例，以及保留原文的字符占比上限。
    translated_texts = [
        translation_by_id.get(verdict["unit_id"], "")
        for verdict in verdicts
        if verdict["state"] == "translated"
        and not is_source_form_kind(by_unit_id.get(verdict["unit_id"], {}))
    ]
    document_ratio = (
        _aggregate_ratio(translated_texts, writing_system, terminology_terms)
        if cross_language and writing_system != "latin" and translated_texts
        else None
    )
    if (
        document_ratio is not None
        and document_ratio < DOCUMENT_TARGET_SCRIPT_RATIO_MIN
    ):
        problems.append(
            {
                "code": "DOCUMENT_TARGET_LANGUAGE_RATIO_LOW",
                "message": (
                    f"全篇目标语言字符占比 {document_ratio:.2f} 低于文档下限 "
                    f"{DOCUMENT_TARGET_SCRIPT_RATIO_MIN:.2f}"
                ),
            }
        )

    total_chars = sum(verdict["source_content_chars"] for verdict in verdicts)
    kept_chars = sum(
        verdict["source_content_chars"]
        for verdict in verdicts
        if verdict["state"] == "kept-source"
    )
    keep_ratio = kept_chars / total_chars if total_chars else 0.0
    if keep_ratio > DOCUMENT_KEEP_SOURCE_CONTENT_RATIO_MAX:
        problems.append(
            {
                "code": "DOCUMENT_KEEP_SOURCE_RATIO_HIGH",
                "message": (
                    f"保留原文的字符占比 {keep_ratio:.2f} 超过上限 "
                    f"{DOCUMENT_KEEP_SOURCE_CONTENT_RATIO_MAX:.2f}；"
                    "这不是一份译本"
                ),
            }
        )

    validated_translated = sum(
        1 for verdict in verdicts if verdict["state"] == "translated"
    )
    validated_kept = sum(
        1 for verdict in verdicts if verdict["state"] == "kept-source"
    )
    invalid = sum(1 for verdict in verdicts if verdict["state"] == "invalid")
    document_level_failed = any(
        problem.get("code", "").startswith(("DOCUMENT_", "BATCH_"))
        for problem in problems
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "source_language": source_language,
        "target_language": target_language,
        "writing_system": writing_system,
        "cross_language": cross_language,
        "unit_count": len(units),
        "validated_translated_units": validated_translated,
        "validated_kept_source_units": validated_kept,
        "invalid_or_unverified_units": invalid,
        "complete": bool(units) and invalid == 0 and not document_level_failed,
        "document_target_script_ratio": (
            None if document_ratio is None else round(document_ratio, 4)
        ),
        "kept_source_content_ratio": round(keep_ratio, 4),
        "thresholds": {
            "unit_target_script_ratio_min": UNIT_TARGET_SCRIPT_RATIO_MIN,
            "batch_target_script_ratio_min": BATCH_TARGET_SCRIPT_RATIO_MIN,
            "document_target_script_ratio_min": DOCUMENT_TARGET_SCRIPT_RATIO_MIN,
            "document_keep_source_content_ratio_max": (
                DOCUMENT_KEEP_SOURCE_CONTENT_RATIO_MAX
            ),
        },
        "batches": batch_reports,
        "units": verdicts,
        "problems": problems,
    }


#: 覆盖率 scope_note 的三种状态，避免翻译完成后还显示“等待翻译”。
SCOPE_NOTE_PENDING = "原文单元已冻结，等待逐单元翻译或登记合法保留原文声明。"
SCOPE_NOTE_INVALID = (
    "存在未通过译文真实性检查的单元；完整性状态不能算通过，请修复后重跑。"
)
SCOPE_NOTE_COMPLETE = (
    "全部原文单元已通过译文真实性检查：译文为目标语言，"
    "保留原文的单元均有结构化 keep_source_code 与证据。"
)


def refresh_coverage(
    translation_document: dict[str, Any],
    *,
    retained_source: Any = None,
    batches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """按真实性判定重写 coverage，并返回它。

    ``complete`` 只在所有单元通过检查、且批次层与文档层都没有问题时为 true。
    """

    report = evaluate_translation(
        translation_document,
        retained_source=retained_source,
        batches=batches,
    )
    units = [
        unit
        for unit in translation_document.get("units", [])
        if isinstance(unit, dict)
    ]
    coverage = translation_document.setdefault("coverage", {})
    coverage["source_units_total"] = len(units)
    coverage["translated_units"] = sum(
        1 for unit in units if _text(unit.get("translation"))
    )
    coverage["kept_source_units"] = sum(
        1
        for unit in units
        if not _text(unit.get("translation"))
        and (
            _text(unit.get("keep_source_code"))
            or _text(unit.get("keep_source_reason"))
        )
    )
    coverage["validated_translated_units"] = report["validated_translated_units"]
    coverage["validated_kept_source_units"] = report[
        "validated_kept_source_units"
    ]
    coverage["invalid_or_unverified_units"] = report[
        "invalid_or_unverified_units"
    ]
    coverage["complete"] = report["complete"]
    coverage["truthfulness_problem_codes"] = sorted(
        {problem["code"] for problem in report["problems"]}
    )
    if report["complete"]:
        coverage["scope_note"] = SCOPE_NOTE_COMPLETE
    elif report["invalid_or_unverified_units"] or report["problems"]:
        coverage["scope_note"] = SCOPE_NOTE_INVALID
    else:
        coverage["scope_note"] = SCOPE_NOTE_PENDING
    return coverage
