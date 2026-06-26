from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path

from deep_translator import GoogleTranslator
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
MESSAGES = {
    "en": {
        "done": "Translation finished.",
        "clean": "No remaining source-language text found in the requested editable objects.",
        "leftover": "Some source-language text still remains in editable objects.",
    },
    "zh": {
        "done": "翻译完成。",
        "clean": "指定范围内的可编辑文本对象中未发现残留源语言文本。",
        "leftover": "指定范围内的部分可编辑文本对象仍有源语言文本残留。",
    },
}
TRANSLATOR_LANG_ALIASES = {
    "zh": "zh-CN",
    "zh-cn": "zh-CN",
    "zh-tw": "zh-TW",
    "cn": "zh-CN",
}


def ui_messages(ui_lang: str) -> dict[str, str]:
    return MESSAGES["zh"] if ui_lang.lower().startswith("zh") else MESSAGES["en"]


def normalize_translator_lang(lang: str) -> str:
    if not lang:
        return "auto"
    if lang == "auto":
        return "auto"
    return TRANSLATOR_LANG_ALIASES.get(lang.lower(), lang)


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


def enabled_prefixes(args: argparse.Namespace) -> list[str]:
    prefixes = [FILE_GROUPS["slides"]]
    if args.include_notes:
        prefixes.append(FILE_GROUPS["notes"])
    if args.include_layouts:
        prefixes.append(FILE_GROUPS["layouts"])
    if args.include_masters:
        prefixes.append(FILE_GROUPS["masters"])
    return prefixes


def iter_text_files(names: list[str], prefixes: list[str]) -> list[str]:
    return sorted(
        name for name in names if name.endswith(".xml") and any(name.startswith(prefix) for prefix in prefixes)
    )


def paragraph_text_nodes(paragraph: etree._Element) -> tuple[str, list[etree._Element]]:
    parts: list[str] = []
    nodes: list[etree._Element] = []
    for child in paragraph:
        local = etree.QName(child).localname
        if local in {"r", "fld"}:
            node = child.find("a:t", namespaces=NS)
            if node is not None:
                parts.append(node.text or "")
                nodes.append(node)
        elif local == "br":
            parts.append("\n")
    return normalize_text("".join(parts)), nodes


def split_text_across_nodes(text: str, nodes: list[etree._Element]) -> None:
    if not nodes:
        return
    if len(nodes) == 1:
        nodes[0].text = text
        return
    original_lengths = [len(node.text or "") for node in nodes]
    total = sum(original_lengths)
    if total <= 0:
        nodes[0].text = text
        for node in nodes[1:]:
            node.text = ""
        return
    cursor = 0
    for index, node in enumerate(nodes):
        if index == len(nodes) - 1:
            node.text = text[cursor:]
        else:
            share = round(len(text) * original_lengths[index] / total)
            node.text = text[cursor : cursor + share]
            cursor += share


def load_glossary(path: Path | None, target_lang: str) -> dict[str, str]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    glossary = {}
    default_terms = data.get("default", {})
    lang_terms = data.get(target_lang, {})
    if isinstance(default_terms, dict):
        glossary.update({normalize_text(k): v for k, v in default_terms.items()})
    if isinstance(lang_terms, dict):
        glossary.update({normalize_text(k): v for k, v in lang_terms.items()})
    return glossary


def load_skip_patterns(path: Path | None) -> list[re.Pattern[str]]:
    if path is None:
        return []
    patterns = []
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip()
        if not item or item.startswith("#"):
            continue
        patterns.append(re.compile(item))
    return patterns


def should_skip(text: str, skip_patterns: list[re.Pattern[str]]) -> bool:
    return any(pattern.search(text) for pattern in skip_patterns)


def make_translator(source_lang: str, target_lang: str) -> GoogleTranslator:
    source = normalize_translator_lang(source_lang)
    target = normalize_translator_lang(target_lang)
    return GoogleTranslator(source=source, target=target)


def collect_unique_paragraphs(
    files: dict[str, bytes],
    prefixes: list[str],
    source_lang: str,
    skip_patterns: list[re.Pattern[str]],
) -> list[str]:
    source_pattern = pattern_for(source_lang)
    found: Counter[str] = Counter()
    for name in iter_text_files(list(files), prefixes):
        root = etree.fromstring(files[name])
        for paragraph in root.findall(".//a:p", namespaces=NS):
            text, _ = paragraph_text_nodes(paragraph)
            if text and matches_source_lang(text, source_lang) and not should_skip(text, skip_patterns):
                found[text] += 1
    return [text for text, _ in found.most_common()]


def translate_paragraphs(
    texts: list[str],
    translator: GoogleTranslator,
    glossary: dict[str, str],
) -> tuple[dict[str, str], int]:
    mapping: dict[str, str] = {}
    glossary_hits = 0
    for text in texts:
        if text in glossary:
            mapping[text] = glossary[text]
            glossary_hits += 1
        else:
            mapping[text] = translator.translate(text)
    return mapping, glossary_hits


def collect_leftover(
    files: dict[str, bytes],
    prefixes: list[str],
    source_lang: str,
) -> dict[str, list[str]]:
    source_pattern = pattern_for(source_lang)
    remaining: dict[str, list[str]] = {}
    for name in iter_text_files(list(files), prefixes):
        root = etree.fromstring(files[name])
        values = []
        for node in root.findall(".//a:t", namespaces=NS):
            value = node.text or ""
            if value and matches_source_lang(value, source_lang):
                values.append(value)
        if values:
            remaining[name] = sorted(set(values))
    return remaining


def rewrite_pptx(
    input_path: Path,
    output_path: Path,
    backup_suffix: str,
    source_lang: str,
    target_lang: str,
    prefixes: list[str],
    glossary: dict[str, str],
    skip_patterns: list[re.Pattern[str]],
    dry_run: bool,
) -> dict:
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    same_path = input_path.resolve() == output_path.resolve()
    backup_path = None
    if same_path:
        backup_path = input_path.with_name(input_path.name + backup_suffix)
        if backup_path.exists():
            backup_path.chmod(0o666)
            backup_path.unlink()
        shutil.copy2(input_path, backup_path)

    for candidate in (output_path, temp_path):
        if candidate.exists():
            if same_path and candidate.resolve() == input_path.resolve():
                continue
            candidate.chmod(0o666)
            candidate.unlink()
    shutil.copy2(input_path, temp_path)
    temp_path.chmod(0o666)

    with zipfile.ZipFile(temp_path, "r") as src:
        files = {name: src.read(name) for name in src.namelist()}

    paragraphs = collect_unique_paragraphs(files, prefixes, source_lang, skip_patterns)
    if paragraphs:
        translator = make_translator(source_lang, target_lang)
        translations, glossary_hits = translate_paragraphs(paragraphs, translator, glossary)
    else:
        translations, glossary_hits = {}, 0

    translated_instances = 0
    updated = dict(files)
    for name in iter_text_files(list(files), prefixes):
        root = etree.fromstring(files[name])
        changed = False
        for paragraph in root.findall(".//a:p", namespaces=NS):
            text, nodes = paragraph_text_nodes(paragraph)
            if text in translations:
                split_text_across_nodes(translations[text], nodes)
                translated_instances += 1
                changed = True
        if changed:
            updated[name] = etree.tostring(root, encoding="UTF-8", xml_declaration=True, standalone="yes")

    leftover = {}
    if not dry_run:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED) as dst:
            for name, payload in updated.items():
                dst.writestr(name, payload)
        temp_path.replace(output_path)
        output_path.chmod(0o666)
        with zipfile.ZipFile(output_path, "r") as verify_zip:
            verify_files = {name: verify_zip.read(name) for name in verify_zip.namelist()}
        leftover = collect_leftover(verify_files, prefixes, source_lang)
    else:
        if temp_path.exists():
            temp_path.unlink()

    return {
        "translated_paragraph_instances": translated_instances,
        "unique_paragraphs": len(paragraphs),
        "glossary_hits": glossary_hits,
        "leftover": leftover,
        "backup_path": str(backup_path) if backup_path else None,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Translate editable PPTX text into a chosen target language.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-lang", default="auto")
    parser.add_argument("--target-lang", required=True)
    parser.add_argument("--ui-lang", default="en")
    parser.add_argument("--glossary-file", type=Path)
    parser.add_argument("--skip-pattern-file", type=Path)
    parser.add_argument("--report-file", type=Path)
    parser.add_argument("--backup-suffix", default=".bak")
    parser.add_argument("--include-notes", action="store_true")
    parser.add_argument("--include-layouts", action="store_true")
    parser.add_argument("--include-masters", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    prefixes = enabled_prefixes(args)
    glossary = load_glossary(args.glossary_file, args.target_lang)
    skip_patterns = load_skip_patterns(args.skip_pattern_file)
    report = rewrite_pptx(
        input_path=args.input,
        output_path=args.output,
        backup_suffix=args.backup_suffix,
        source_lang=args.source_lang,
        target_lang=args.target_lang,
        prefixes=prefixes,
        glossary=glossary,
        skip_patterns=skip_patterns,
        dry_run=args.dry_run,
    )

    msg = ui_messages(args.ui_lang)
    summary = {
        "message": msg["done"],
        "verification": msg["clean"] if not report["leftover"] else msg["leftover"],
        "input": str(args.input),
        "output": str(args.output),
        "source_lang": args.source_lang,
        "target_lang": args.target_lang,
        "ui_lang": args.ui_lang,
        "included_scopes": prefixes,
        "glossary_file": str(args.glossary_file) if args.glossary_file else None,
        "skip_pattern_file": str(args.skip_pattern_file) if args.skip_pattern_file else None,
        "dry_run": args.dry_run,
        **report,
    }

    if args.report_file:
        args.report_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if args.dry_run or not report["leftover"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
