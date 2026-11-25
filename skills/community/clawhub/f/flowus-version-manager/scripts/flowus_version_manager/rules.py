"""Generic parsing extracted from the existing manager; domain rules are private configuration."""
from __future__ import annotations
import datetime as dt
import html
import re
import unicodedata
import hashlib
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import difflib
import shutil
import subprocess


def normalize_rules(raw: dict) -> dict:
    """Only domain configuration is imported; local paths and sync settings stay local."""
    result = {key: raw.get(key, []) for key in ("categories", "title_aliases", "continuous_keywords", "business_terms", "extension_categories")}
    result["category_defaults"] = raw.get("category_defaults", {})
    result["continuous_categories"] = raw.get("continuous_categories", raw.get("governance", {}).get("continuous_categories", []))
    result["ambiguous_names"] = raw.get("ambiguous_names", ["untitled", "新建", "未命名"])
    return result


def extract_text(path: Path) -> tuple[str, list[str]]:
    """Extraction is best effort. Failure never discards the original."""
    warnings = []
    try:
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md", ".csv", ".tsv", ".json", ".log"}:
            return path.read_text(encoding="utf-8", errors="replace"), warnings
        if suffix in {".docx", ".pptx", ".xlsx", ".xlsm"}:
            if zipfile.is_zipfile(path):
                with zipfile.ZipFile(path) as archive:
                    if sum(i.file_size for i in archive.infolist()) > 128 * 1024 * 1024:
                        return "", ["Expanded document exceeds extraction bound"]
            parser = {".docx": extract_docx, ".pptx": extract_pptx,
                      ".xlsx": extract_xlsx, ".xlsm": extract_xlsx}[suffix]
            return parser(path), warnings
        if suffix in {".doc", ".rtf", ".xls", ".pdf"}:
            tool = shutil.which("pdftotext" if suffix == ".pdf" else "textutil")
            if tool and suffix != ".xls":
                command = [tool, str(path), "-"] if suffix == ".pdf" else [tool, "-convert", "txt", "-stdout", str(path)]
                result = subprocess.run(command, capture_output=True, timeout=20, check=False)
                if result.returncode == 0:
                    return result.stdout.decode("utf-8", errors="replace"), warnings
            binary = shutil.which("strings") if suffix in {".xls", ".doc"} else None
            if binary:
                result = subprocess.run([binary, "-n", "3", str(path)], capture_output=True, timeout=20, check=False)
                if result.returncode == 0:
                    return result.stdout.decode("utf-8", errors="replace"), ["Legacy binary text extraction is approximate"]
            return "", ["Legacy/PDF text extraction unavailable; file retained and metadata matching only"]
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError, subprocess.SubprocessError):
        return "", ["Text extraction failed; file retained"]
    return "", ["No text extractor for this file type"]


def decide(path: Path, rules: dict, history: list[dict], *, text=None) -> dict:
    if text is None:
        text, warnings = extract_text(path)
    else:
        warnings = []
    version = parse_version_info(path.stem, rules, path.stat().st_mtime)
    name = canonicalize_name(path.name, version, "", text)
    title = name.canonical_title
    for alias in rules.get("title_aliases", []):
        haystack = normalize_key(title + " " + text[:800])
        contains = alias.get("contains", [])
        equals = alias.get("equals", [])
        if ((contains and all(normalize_key(k).replace(" ", "") in haystack.replace(" ", "") for k in contains))
                or (equals and normalize_key(title).replace(" ", "") in {normalize_key(k).replace(" ", "") for k in equals})):
            title = alias["title"]
            break
    category, category_title = "general", "通用文件"
    for fallback in rules.get("extension_categories", []):
        if path.suffix.lower() in fallback.get("extensions", []):
            category, category_title = fallback["name"], fallback["title"]
            break
    best_weight = 0
    for rule in rules.get("categories", []):
        weight = sum(4 for word in rule.get("keywords", []) if normalize_key(word) in normalize_key(path.stem))
        if weight and path.suffix.lower() in rule.get("extensions", []):
            weight += 2
        if weight > best_weight:
            best_weight = weight
            category, category_title = rule["name"], rule["title"]
    best, confidence = None, 0
    for item in history:
        if item.get("category") != category or item.get("status") != "indexed":
            continue
        previous = item.get("canonical_title", item.get("series_title", ""))
        ratio = difflib.SequenceMatcher(None, normalize_key(previous), normalize_key(title)).ratio()
        score = 96 if normalize_key(previous) == normalize_key(title) else int(ratio * 72)
        before = normalize_content_for_match(item.get("text", ""))
        after = normalize_content_for_match(text)
        if len(before) >= 40 and len(after) >= 40:
            content = difflib.SequenceMatcher(None, before[:3000], after[:3000]).ratio()
            score = max(score, 88 if content >= .75 else 0, int(content * 70 + ratio * 25))
        shared = sum(1 for term in rules.get("business_terms", [])
                     if normalize_key(term) in normalize_key(previous) and normalize_key(term) in normalize_key(title))
        score = min(99, score + min(8, shared * 2))
        if score > confidence:
            best, confidence = item, min(99, score)
    key = normalize_key(title)
    if best and confidence >= 85:
        key, title = best["series_key"], best["series_title"]
    elif best and confidence >= 60:
        version.needs_review = True
        version.review_reason = "Possible existing version line; confirmation required"
    continuous = category in rules.get("continuous_categories", []) or any(
        normalize_key(word) in normalize_key(path.stem) for word in rules.get("continuous_keywords", []))
    if len(text) > 24000:
        warnings.append("Search text truncated to 24000 characters; original retained in full")
    defaults = {k: v for k, v in rules.get("category_defaults", {}).get(category, {}).items()
                if k in {"project", "file_type", "stage", "lifecycle"}}
    return {**defaults, "title": path.name, "original_name": path.name, "display_name": safe_filename(title) + path.suffix,
            "canonical_title": title, "series_key": key, "series_title": title,
            "category": category, "category_title": category_title,
            "version_label": version.version_label, "version_sort": version.version_sort,
            "period_label": version.period_label, "is_final": version.is_final and not continuous,
            "continuous": continuous, "status": "needs_review" if version.needs_review else "indexed",
            "reason": version.review_reason, "match_confidence": confidence, "text": text[:24000], "warnings": warnings,
            "matched_document_key": best.get("document_key") if best and confidence >= 85 else None}


@dataclass
class VersionInfo:
    clean_title: str
    version_label: str
    version_sort: int
    period_label: str | None
    version_number: int | None
    is_final: bool
    is_draft: bool
    explicit_date: str | None
    needs_review: bool
    review_reason: str | None


@dataclass(frozen=True)
class CanonicalName:
    raw_title: str
    canonical_title: str
    display_name: str
    removed_markers: list[str]
    content_fingerprint: str


def parse_version_info(stem: str, config: dict[str, Any], mtime: float) -> VersionInfo:
    original = unicodedata.normalize("NFKC", stem)
    working = f" {original} "
    lower = normalize_key(original)

    period_label: str | None = None
    period_sort = 0
    h_match = re.search(r"(20\d{2})\s*[Hh]\s*([12])", original)
    if not h_match:
        h_match = re.search(r"(20\d{2})\s*年?\s*(上半年|下半年)", original)
    if h_match:
        year = int(h_match.group(1))
        half_raw = h_match.group(2)
        half = 1 if half_raw in {"1", "上半年"} else 2
        period_label = f"{year}H{half}"
        period_sort = year * 10 + half
        working = re.sub(r"20\d{2}\s*[Hh]\s*[12]", " ", working)
        working = re.sub(r"20\d{2}\s*年?\s*(上半年|下半年)", " ", working)

    explicit_date: str | None = None
    date_sort = 0
    date_match_text = None
    if not period_label:
        explicit_date, date_sort, date_match_text = find_explicit_date(original)
        if explicit_date and date_match_text:
            working = working.replace(date_match_text, " ")

    version_number: int | None = None
    version_match = re.search(
        r"(?:^|[\s_\-.（(])(?:v|ver|version|版本|rev|r)\s*0*(\d{1,4})(?:$|[\s_\-.）)])",
        f" {original} ",
        flags=re.IGNORECASE,
    )
    if version_match:
        version_number = int(version_match.group(1))
        working = re.sub(
            r"(?:^|[\s_\-.（(])(?:v|ver|version|版本|rev|r)\s*0*\d{1,4}(?:$|[\s_\-.）)])",
            " ",
            working,
            flags=re.IGNORECASE,
        )

    is_final = bool(
        re.search(r"(?:^|[\s_\-.])(final|latest)(?:$|[\s_\-.])|定稿|终稿|最终|最新版", f" {original} ", flags=re.IGNORECASE)
    )
    is_draft = bool(
        re.search(r"(?:^|[\s_\-.])draft(?:$|[\s_\-.])|草稿|初稿", f" {original} ", flags=re.IGNORECASE)
    )
    working = re.sub(
        r"(?:^|[\s_\-.])(final|latest|draft|copy)(?:$|[\s_\-.])|定稿|终稿|最终|最新版|草稿|初稿|副本|的副本",
        " ",
        working,
        flags=re.IGNORECASE,
    )

    working = re.sub(r"[_\-+.]+", " ", working)
    clean = sanitize_title(working)
    ambiguous = looks_ambiguous(clean, config)
    review_reason = "filename is too generic to infer a version line" if ambiguous else None

    if period_sort:
        version_label = period_label or "period"
        major = 4_000_000_000 + period_sort * 100_000
    elif date_sort:
        version_label = explicit_date or "dated"
        major = 3_000_000_000 + date_sort * 100_000
    elif is_final or version_number is not None:
        version_label = "final" if is_final and version_number is None else f"v{version_number:02d}"
        if is_final and version_number is not None:
            version_label = f"v{version_number:02d}-final"
        major = 2_000_000_000 + (10_000 if is_final else 0) + (version_number or 0) * 100
    elif is_draft:
        version_label = "draft"
        major = 1_500_000_000
    else:
        version_label = dt.datetime.fromtimestamp(mtime).strftime("mtime-%Y%m%d-%H%M%S")
        major = int(mtime)

    version_sort = major + int(mtime) % 100_000
    return VersionInfo(
        clean_title=clean,
        version_label=version_label,
        version_sort=version_sort,
        period_label=period_label,
        version_number=version_number,
        is_final=is_final,
        is_draft=is_draft,
        explicit_date=explicit_date,
        needs_review=ambiguous,
        review_reason=review_reason,
    )


def find_explicit_date(original: str) -> tuple[str | None, int, str | None]:
    normalized = unicodedata.normalize("NFKC", original)
    patterns = [
        r"(20\d{2})\s*[年/-]\s*(1[0-2]|0?[1-9])\s*月?\s*(3[01]|[12]\d|0?[1-9])?\s*日?",
        r"(20\d{2})[._-](1[0-2]|0?[1-9])(?:[._-](3[01]|[12]\d|0?[1-9]))?",
        r"(20\d{2})(1[0-2]|0[1-9])(?:([0-3]\d))?",
        r"(20\d{2})(?!\d)",
        r"((?:20)?\d{2}|[二两〇零一三四五六七八九]{2})\s*年",
    ]
    for pattern in patterns:
        match = re.search(pattern, normalized)
        if not match:
            continue
        raw_year = match.group(1)
        year = parse_year(raw_year)
        if not year:
            continue
        month = int(match.group(2)) if match.lastindex and match.lastindex >= 2 and match.group(2) else 1
        day = int(match.group(3)) if match.lastindex and match.lastindex >= 3 and match.group(3) else 1
        try:
            parsed = dt.date(year, month, day)
        except ValueError:
            continue
        if month == 1 and day == 1 and match.lastindex == 1:
            return str(year), parsed.toordinal(), match.group(0)
        return parsed.isoformat(), parsed.toordinal(), match.group(0)
    return None, 0, None


def parse_year(raw: str) -> int | None:
    raw = unicodedata.normalize("NFKC", raw).strip()
    if raw.isdigit():
        value = int(raw)
        if 0 <= value < 100:
            return 2000 + value
        return value
    digits = {"〇": "0", "零": "0", "一": "1", "二": "2", "两": "2", "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9"}
    converted = "".join(digits.get(char, "") for char in raw)
    if len(converted) == 2:
        return 2000 + int(converted)
    if len(converted) == 4:
        return int(converted)
    return None


def canonicalize_name(
    original_name: str,
    version: VersionInfo,
    category: str,
    text: str = "",
) -> CanonicalName:
    raw_title = Path(original_name).stem
    suffix = Path(original_name).suffix
    working = unicodedata.normalize("NFKC", version.clean_title or raw_title)
    removed: list[str] = []

    marker_patterns = [
        ("transfer copy marker", r"(?:^|[\s_\-（(])(?:副本|copy)(?:$|[\s_\-）)])|的副本"),
        ("parenthetical duplicate marker", r"[\s_\-]*[（(]\s*\d+\s*[）)]\s*$"),
        ("final marker", r"(?:^|[\s_\-.])final(?:$|[\s_\-.])|定稿|终稿|最终|最新版"),
        ("update marker", r"更新版|确认版|修改版|新版"),
        ("leading version modifier", r"^v\d+\s*[^A-Za-z0-9\u4e00-\u9fff]*\s*(?:[^A-Za-z0-9\u4e00-\u9fff]*修改版)?"),
        ("leading transfer number", r"^\d{1,3}\s*[-_、. ]+"),
    ]
    for label, pattern in marker_patterns:
        updated = re.sub(pattern, " ", working, flags=re.IGNORECASE)
        if updated != working:
            removed.append(label)
            working = updated

    working = remove_empty_parentheses(working)
    working = re.sub(r"[_\-+.]+", " ", working)
    working = re.sub(r"\s+", " ", working).strip()
    canonical_title = sanitize_title(working)
    display_name = safe_filename(canonical_title) + suffix
    return CanonicalName(
        raw_title=raw_title,
        canonical_title=canonical_title,
        display_name=display_name,
        removed_markers=removed,
        content_fingerprint=content_fingerprint(text),
    )


def remove_empty_parentheses(value: str) -> str:
    previous = None
    current = value
    while previous != current:
        previous = current
        current = re.sub(r"[（(]\s*[）)]", " ", current)
    return current


def content_fingerprint(text: str) -> str:
    normalized = normalize_content_for_match(text)
    if not normalized:
        return ""
    return hashlib.sha256(normalized[:5000].encode("utf-8", errors="ignore")).hexdigest()[:16]


def normalize_content_for_match(text: str) -> str:
    text = re.sub(r"File name:.*|Extension:.*|Size bytes:.*|Modified:.*", " ", text or "")
    text = unicodedata.normalize("NFKC", text).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_docx(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        names = [name for name in zf.namelist() if name.startswith("word/") and name.endswith(".xml")]
        texts: list[str] = []
        for name in names:
            if not re.search(r"word/(document|footnotes|endnotes|comments).*\.xml", name):
                continue
            root = ET.fromstring(zf.read(name))
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    texts.append(node.text)
        return "\n".join(texts) or metadata_text(path)


def extract_pptx(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        names = sorted(name for name in zf.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml"))
        texts: list[str] = []
        for name in names:
            root = ET.fromstring(zf.read(name))
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    texts.append(node.text)
        return "\n".join(texts) or metadata_text(path)


def extract_xlsx(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        texts: list[str] = []
        if "xl/sharedStrings.xml" in zf.namelist():
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    texts.append(node.text)
        for name in sorted(n for n in zf.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml", n)):
            root = ET.fromstring(zf.read(name))
            for node in root.iter():
                if node.tag.endswith("}v") and node.text:
                    texts.append(node.text)
        return "\n".join(texts) or metadata_text(path)


def metadata_text(path: Path) -> str:
    stat = path.stat()
    return (
        f"File name: {path.name}\n"
        f"Extension: {path.suffix.lower() or '(none)'}\n"
        f"Size bytes: {stat.st_size}\n"
        f"Modified: {dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec='seconds')}\n"
    )


def sanitize_title(value: str) -> str:
    value = html.unescape(unicodedata.normalize("NFKC", value))
    value = re.sub(r"[_\-+.]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" ._-")
    return value or "未命名"


def safe_filename(value: str) -> str:
    value = html.unescape(unicodedata.normalize("NFKC", value))
    value = re.sub(r"[/\\:]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:120] or "untitled"


def normalize_key(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).lower()
    value = re.sub(r"[/\\:_\-+.]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def looks_ambiguous(clean_title: str, config: dict[str, Any]) -> bool:
    key = normalize_key(clean_title)
    compact = re.sub(r"\s+", "", key)
    ambiguous = {normalize_key(item) for item in config.get("ambiguous_names", [])}
    if key in ambiguous or compact in ambiguous:
        return True
    useful = re.findall(r"[A-Za-z0-9\u4e00-\u9fff]", clean_title)
    if len(useful) < 2:
        return True
    return False
