#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


@dataclass(frozen=True)
class LintIssue:
    section: str
    message: str
    evidence: str = ""


SECTION_TITLES = {
    "homepage hero": "Homepage hero",
    "hero": "Homepage hero",
    "pdp": "PDP brand block",
    "pdp brand block": "PDP brand block",
    "product detail page": "PDP brand block",
    "packaging": "Packaging / insert",
    "insert": "Packaging / insert",
}


GENERIC_PHRASES = [
    "we're passionate",
    "we are passionate",
    "quality is our priority",
    "highest quality",
    "best quality",
    "premium quality",
    "crafted with love",
    "made with love",
    "we care about quality",
    "our mission is to provide",
]


def normalize_title(title: str) -> str:
    t = title.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


def split_sections(md: str) -> Dict[str, str]:
    """
    Split markdown into sections using '## ' headings.
    Returns {canonical_section_name: content}.
    """
    lines = md.splitlines()
    sections: Dict[str, List[str]] = {}
    current_key = "Document"
    sections[current_key] = []

    for line in lines:
        if line.startswith("## "):
            raw_title = line[3:].strip()
            key = SECTION_TITLES.get(normalize_title(raw_title), raw_title)
            current_key = key
            sections.setdefault(current_key, [])
            continue
        sections[current_key].append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items() if "\n".join(v).strip()}


def word_count(text: str) -> int:
    words = re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text)
    return len(words)


def find_generic_phrases(text: str) -> List[str]:
    t = text.lower()
    hits = []
    for phrase in GENERIC_PHRASES:
        if phrase in t:
            hits.append(phrase)
    return hits


def lint_hero(section: str, text: str) -> List[LintIssue]:
    issues: List[LintIssue] = []

    headline = ""
    sub = ""
    for line in (l.strip() for l in text.splitlines() if l.strip()):
        if line.lower().startswith("headline:"):
            headline = line.split(":", 1)[1].strip()
        if line.lower().startswith(("sub:", "subhead:", "subheadline:")):
            sub = line.split(":", 1)[1].strip()

    if not headline:
        issues.append(
            LintIssue(
                section,
                "Missing 'Headline:' line. For best results, format as: Headline: ... / Sub: ... / CTA: ...",
            )
        )
    else:
        wc = word_count(headline)
        if wc > 14:
            issues.append(LintIssue(section, f"Headline is long ({wc} words). Aim for 6–14 words.", headline))

    if sub:
        wc = word_count(sub)
        if wc > 26:
            issues.append(LintIssue(section, f"Subhead is long ({wc} words). Aim for <= 26 words.", sub))

    return issues


def lint_pdp(section: str, text: str) -> List[LintIssue]:
    issues: List[LintIssue] = []
    wc = word_count(text)
    if wc > 120:
        issues.append(LintIssue(section, f"PDP block is long ({wc} words). Aim for ~40–120 words.", ""))
    if wc < 25:
        issues.append(LintIssue(section, f"PDP block is short ({wc} words). Aim for >= 25 words.", ""))
    return issues


def lint_packaging(section: str, text: str) -> List[LintIssue]:
    issues: List[LintIssue] = []
    wc = word_count(text)
    if wc > 30:
        issues.append(LintIssue(section, f"Packaging/insert copy is long ({wc} words). Aim for <= 30 words.", ""))
    return issues


def lint_generic(section: str, text: str) -> List[LintIssue]:
    issues: List[LintIssue] = []
    hits = find_generic_phrases(text)
    for phrase in hits:
        issues.append(
            LintIssue(
                section,
                f"Generic filler detected: '{phrase}'. Replace with concrete origin/process/proof.",
                phrase,
            )
        )
    return issues


def lint_sections(sections: Dict[str, str]) -> List[LintIssue]:
    issues: List[LintIssue] = []
    for section, text in sections.items():
        issues.extend(lint_generic(section, text))
        key = normalize_title(section)
        if key in ("homepage hero", "hero"):
            issues.extend(lint_hero(section, text))
        if key in ("pdp brand block", "pdp"):
            issues.extend(lint_pdp(section, text))
        if key in ("packaging / insert", "packaging", "insert"):
            issues.extend(lint_packaging(section, text))
    return issues


def format_issues(issues: Iterable[LintIssue]) -> str:
    out: List[str] = []
    for i, issue in enumerate(issues, start=1):
        out.append(f"{i}. [{issue.section}] {issue.message}")
        if issue.evidence:
            out.append(f"   Evidence: {issue.evidence}")
    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Lint founder-story related copy for length and generic filler. Input should use '## ' headings (e.g. '## Homepage hero', '## PDP', '## Packaging')."
    )
    p.add_argument("--in", dest="in_path", required=True, help="Path to markdown file (copy.md).")
    return p


def main() -> None:
    args = build_parser().parse_args()
    in_path = Path(args.in_path).expanduser()
    text = in_path.read_text(encoding="utf-8")
    sections = split_sections(text)
    issues = lint_sections(sections)

    if issues:
        print("COPY LINT: issues found\n")
        print(format_issues(issues))
        sys.exit(1)

    print("COPY LINT: OK (no issues found)")


if __name__ == "__main__":
    main()

