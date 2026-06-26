from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

from lxml import etree


NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
FILE_GROUPS = {
    "slides": "ppt/slides/",
    "notes": "ppt/notesSlides/",
    "layouts": "ppt/slideLayouts/",
    "masters": "ppt/slideMasters/",
}
LANG_PATTERNS = {
    "zh": re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]"),
    "ja": re.compile(r"[\u3040-\u30ff\u31f0-\u31ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]"),
    "ko": re.compile(r"[\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]"),
}
LATIN_LANGS = {
    "en",
    "fr",
    "de",
    "es",
    "it",
    "pt",
    "nl",
    "pl",
    "sv",
    "da",
    "no",
    "fi",
    "ro",
    "cs",
    "sk",
    "hu",
    "tr",
}
LATIN_RE = re.compile(r"[A-Za-z]")


def pattern_for(lang: str | None) -> re.Pattern[str]:
    if not lang or lang == "auto":
        return LANG_PATTERNS["zh"]
    return LANG_PATTERNS.get(lang.lower(), LANG_PATTERNS["zh"])


def matches_source_lang(text: str, lang: str | None) -> bool:
    if not text:
        return False
    if not lang or lang == "auto":
        return bool(pattern_for("zh").search(text))
    lowered = lang.lower()
    if lowered in LANG_PATTERNS:
        return bool(pattern_for(lowered).search(text))
    if lowered in LATIN_LANGS:
        letters = LATIN_RE.findall(text)
        return len(letters) >= 3 and any(ch.islower() for ch in text if ch.isalpha())
    return bool(pattern_for("zh").search(text))


def normalize_text(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()


def paragraph_text(paragraph: etree._Element) -> str:
    parts = []
    for child in paragraph:
        local = etree.QName(child).localname
        if local in {"r", "fld"}:
            node = child.find("a:t", namespaces=NS)
            if node is not None and node.text:
                parts.append(node.text)
        elif local == "br":
            parts.append("\n")
    return normalize_text("".join(parts))


def enabled_prefixes(args: argparse.Namespace) -> list[str]:
    prefixes = [FILE_GROUPS["slides"]]
    if args.include_notes:
        prefixes.append(FILE_GROUPS["notes"])
    if args.include_layouts:
        prefixes.append(FILE_GROUPS["layouts"])
    if args.include_masters:
        prefixes.append(FILE_GROUPS["masters"])
    return prefixes


def scan_pptx(path: Path, prefixes: list[str], lang: str | None) -> dict:
    pattern = pattern_for(lang)
    unique = Counter()
    files = Counter()

    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if not name.endswith(".xml") or not any(name.startswith(prefix) for prefix in prefixes):
                continue
            root = etree.fromstring(archive.read(name))
            matched = 0
            for paragraph in root.findall(".//a:p", namespaces=NS):
                text = paragraph_text(paragraph)
                if text and matches_source_lang(text, lang):
                    unique[text] += 1
                    matched += 1
            if matched:
                files[name] += matched

    return {
        "input": str(path),
        "source_lang": lang or "auto",
        "matched_files": len(files),
        "matched_paragraph_instances": sum(files.values()),
        "unique_paragraphs": len(unique),
        "top_files": files.most_common(20),
        "top_paragraphs": unique.most_common(50),
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Scan editable PPTX text for source-language content.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--source-lang", default="zh")
    parser.add_argument("--include-notes", action="store_true")
    parser.add_argument("--include-layouts", action="store_true")
    parser.add_argument("--include-masters", action="store_true")
    args = parser.parse_args()

    report = scan_pptx(args.input, enabled_prefixes(args), args.source_lang)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
