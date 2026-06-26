#!/usr/bin/env python3
"""Lightweight static audit for HTML form UX/accessibility issues."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

CONTROL_TAGS = {"input", "select", "textarea"}
SKIP_INPUT_TYPES = {"hidden", "submit", "button", "reset", "image"}

AUTOCOMPLETE_PATTERNS: Sequence[Tuple[str, Sequence[str]]] = (
    ("given-name", (r"\bfirst[ _-]?name\b", r"\bgiven[ _-]?name\b")),
    ("family-name", (r"\blast[ _-]?name\b", r"\bsur[ _-]?name\b", r"\bfamily[ _-]?name\b")),
    ("email", (r"\bemail\b", r"\be-mail\b")),
    ("tel", (r"\bphone\b", r"\bmobile\b", r"\btel\b")),
    ("address-line1", (r"\baddress(?!.*line\s*2)\b", r"\bstreet\b", r"\baddr1\b")),
    ("postal-code", (r"\bpostal\b", r"\bzip\b", r"\bpostcode\b")),
    ("cc-number", (r"\bcard[ _-]?number\b", r"\bcc[ _-]?number\b")),
    ("cc-exp", (r"\bexp(iry|iration)?\b", r"\bcc[ _-]?exp\b", r"\bmm\s*/\s*yy\b")),
    ("cc-csc", (r"\bcvv\b", r"\bcvc\b", r"\bcsc\b", r"\bsecurity[ _-]?code\b")),
)

TYPE_HINT_PATTERNS: Sequence[Tuple[str, Sequence[str]]] = (
    ("email", (r"\bemail\b",)),
    ("tel", (r"\bphone\b", r"\bmobile\b", r"\btel\b")),
    ("password", (r"\bpassword\b", r"\bpasscode\b", r"\bpin\b")),
)

NUMERIC_HINT_PATTERNS = (
    r"\bquantity\b",
    r"\bqty\b",
    r"\bamount\b",
    r"\bprice\b",
    r"\bage\b",
    r"\bcount\b",
)


@dataclass
class Issue:
    severity: str
    code: str
    line: int
    col: int
    message: str
    hint: str

    def format(self) -> str:
        return f"{self.severity} {self.code} {self.line}:{self.col} - {self.message} ({self.hint})"


@dataclass
class Control:
    tag: str
    attrs: Dict[str, str]
    line: int
    col: int
    inside_label: bool

    @property
    def input_type(self) -> str:
        if self.tag != "input":
            return self.tag
        return (self.attrs.get("type") or "text").lower()

    @property
    def control_id(self) -> str:
        return self.attrs.get("id", "")

    @property
    def name(self) -> str:
        return self.attrs.get("name", "")

    def hint(self) -> str:
        parts = [f"<{self.tag}"]
        if self.control_id:
            parts.append(f'id="{self.control_id}"')
        if self.name:
            parts.append(f'name="{self.name}"')
        return " ".join(parts) + ">"

    def searchable_text(self) -> str:
        values = [
            self.attrs.get("id", ""),
            self.attrs.get("name", ""),
            self.attrs.get("placeholder", ""),
            self.attrs.get("aria-label", ""),
            self.attrs.get("autocomplete", ""),
        ]
        return " ".join(values).lower()


class FormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.controls: List[Control] = []
        self.labels_for: Dict[str, List[Tuple[int, int]]] = {}
        self.ids: List[Tuple[str, int, int, str]] = []
        self._tag_stack: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        lower_tag = tag.lower()
        attr_map: Dict[str, str] = {}
        for key, value in attrs:
            if key is None:
                continue
            attr_map[key.lower()] = (value or "").strip()

        line, col = self.getpos()
        col += 1

        self._tag_stack.append(lower_tag)

        element_id = attr_map.get("id", "")
        if element_id:
            self.ids.append((element_id, line, col, lower_tag))

        if lower_tag == "label":
            label_for = attr_map.get("for", "")
            if label_for:
                self.labels_for.setdefault(label_for, []).append((line, col))

        if lower_tag in CONTROL_TAGS:
            inside_label = "label" in self._tag_stack[:-1]
            self.controls.append(Control(lower_tag, attr_map, line, col, inside_label))

    def handle_endtag(self, tag: str) -> None:
        lower_tag = tag.lower()
        for idx in range(len(self._tag_stack) - 1, -1, -1):
            if self._tag_stack[idx] == lower_tag:
                del self._tag_stack[idx]
                break

    def handle_startendtag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)


def detect_semantic_field(blob: str, patterns: Sequence[Tuple[str, Sequence[str]]]) -> List[str]:
    matches: List[str] = []
    for semantic, regex_list in patterns:
        if any(re.search(regex, blob) for regex in regex_list):
            matches.append(semantic)
    return matches


def check_duplicate_ids(items: Iterable[Tuple[str, int, int, str]]) -> List[Issue]:
    seen: Dict[str, Tuple[int, int, str]] = {}
    issues: List[Issue] = []
    for value, line, col, tag in items:
        if value in seen:
            first_line, first_col, first_tag = seen[value]
            issues.append(
                Issue(
                    "P1",
                    "DUPLICATE_ID",
                    line,
                    col,
                    f'id "{value}" duplicates {first_tag} at {first_line}:{first_col}',
                    f"<{tag} id=\"{value}\">",
                )
            )
        else:
            seen[value] = (line, col, tag)
    return issues


def has_explicit_label(control: Control, labels_for: Dict[str, List[Tuple[int, int]]]) -> bool:
    control_id = control.control_id
    return bool(control_id and labels_for.get(control_id))


def should_require_label(control: Control) -> bool:
    if control.tag != "input":
        return True
    return control.input_type not in SKIP_INPUT_TYPES


def should_require_name(control: Control) -> bool:
    if control.tag != "input":
        return True
    return control.input_type not in SKIP_INPUT_TYPES


def check_control(control: Control, labels_for: Dict[str, List[Tuple[int, int]]]) -> List[Issue]:
    issues: List[Issue] = []
    blob = control.searchable_text()
    explicit_label = has_explicit_label(control, labels_for)
    has_aria_name = bool(control.attrs.get("aria-label") or control.attrs.get("aria-labelledby"))

    if should_require_label(control) and not control.inside_label and not explicit_label:
        if has_aria_name:
            issues.append(
                Issue(
                    "P2",
                    "LABEL_FOR_MISSING",
                    control.line,
                    control.col,
                    "Missing visible label association; relies on ARIA naming only",
                    control.hint(),
                )
            )
        else:
            issues.append(
                Issue(
                    "P1",
                    "LABEL_FOR_MISSING",
                    control.line,
                    control.col,
                    "Missing associated label (`<label for=...>` or wrapper label)",
                    control.hint(),
                )
            )

    if should_require_name(control) and not control.name:
        issues.append(
            Issue(
                "P1",
                "NAME_MISSING",
                control.line,
                control.col,
                "Missing `name` attribute on submitted control",
                control.hint(),
            )
        )

    placeholder = control.attrs.get("placeholder", "")
    if placeholder and not control.inside_label and not explicit_label:
        issues.append(
            Issue(
                "P1",
                "PLACEHOLDER_AS_LABEL",
                control.line,
                control.col,
                "Placeholder appears to be used as the primary label",
                control.hint(),
            )
        )

    expected_autocomplete = detect_semantic_field(blob, AUTOCOMPLETE_PATTERNS)
    autocomplete = control.attrs.get("autocomplete", "").lower()
    if expected_autocomplete and not autocomplete:
        issues.append(
            Issue(
                "P2",
                "AUTOCOMPLETE_MISSING",
                control.line,
                control.col,
                f"Missing autocomplete attribute; likely expected one of: {', '.join(sorted(set(expected_autocomplete)))}",
                control.hint(),
            )
        )

    if control.tag == "input":
        input_type = control.input_type
        type_semantics = detect_semantic_field(blob, TYPE_HINT_PATTERNS)

        if "email" in type_semantics and input_type != "email":
            issues.append(
                Issue(
                    "P1",
                    "TYPE_MISMATCH_EMAIL",
                    control.line,
                    control.col,
                    "Likely email field should use type=\"email\"",
                    control.hint(),
                )
            )

        if "tel" in type_semantics and input_type != "tel":
            issues.append(
                Issue(
                    "P1",
                    "TYPE_MISMATCH_TEL",
                    control.line,
                    control.col,
                    "Likely phone field should use type=\"tel\"",
                    control.hint(),
                )
            )

        if "password" in type_semantics and input_type != "password":
            issues.append(
                Issue(
                    "P1",
                    "TYPE_MISMATCH_PASSWORD",
                    control.line,
                    control.col,
                    "Likely password field should use type=\"password\"",
                    control.hint(),
                )
            )

        if any(re.search(pattern, blob) for pattern in NUMERIC_HINT_PATTERNS):
            inputmode = control.attrs.get("inputmode", "").lower()
            if input_type not in {"number", "range"} and inputmode not in {"numeric", "decimal"}:
                issues.append(
                    Issue(
                        "P2",
                        "TYPE_MISMATCH_NUMERIC",
                        control.line,
                        control.col,
                        "Likely numeric field missing numeric-capable type or inputmode",
                        control.hint(),
                    )
                )

    return issues


def audit_html(content: str) -> List[Issue]:
    parser = FormParser()
    parser.feed(content)
    parser.close()

    issues: List[Issue] = []
    issues.extend(check_duplicate_ids(parser.ids))

    for control in parser.controls:
        issues.extend(check_control(control, parser.labels_for))

    severity_rank = {"P0": 0, "P1": 1, "P2": 2}
    issues.sort(key=lambda item: (severity_rank.get(item.severity, 9), item.line, item.col, item.code))
    return issues


def main(argv: Sequence[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 scripts/form_audit.py <path-to-form.html>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.exists() or not path.is_file():
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        return 2

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Could not read file: {exc}", file=sys.stderr)
        return 2

    issues = audit_html(content)
    if not issues:
        print("OK NO_ISSUES 0:0 - No issues found (form_audit)")
        return 0

    for issue in issues:
        print(issue.format())
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
