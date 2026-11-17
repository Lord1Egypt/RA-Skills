#!/usr/bin/env python3
"""concept-lint: read-only structural checks for the local CONCEPT/SYNCS format."""

import argparse
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from spec_syntax import (
    CORE, HEAD, SECTION, RULE, COVERAGE, TOKEN, FENCE, OPEN_BLOCK, CALL, FIELD,
    CLAUSES, Source, diagnostic, add, blank, has_literal, prepare, record_end,
)

EXIT = {"format_checked": 0, "format_error": 1, "read_error": 2, "not_checked": 3}


def check_concept(source, result):
    text = source.syntax
    sections = list(SECTION.finditer(text))
    names = [m[1].strip().lower() for m in sections]
    declared = [m for m in re.finditer(r"^[ \t]*coverage:[^\n]*$", text, re.M)
                if m.end() <= source.known_end]
    coverage = list(COVERAGE.finditer(text))
    for match in sections + declared:
        if has_literal(source, match):
            add(result, "unchecked", text, match.start(), "declaration-syntax", "Literal in a section or coverage declaration.")
    if not declared:
        add(result, "unchecked", text, 0, "coverage-missing", "Coverage is undeclared.")
    elif len(declared) != 1 or len(coverage) != 1:
        add(result, "issues", text, declared[0].start(), "coverage",
            "Use one 'coverage: complete' or 'coverage: partial' before the sections.")
    actions = next((m for m in sections if m[1].strip().lower() == "actions"), None)
    action_end = next((m.start() for m in sections if actions and m.start() > actions.start()), source.known_end)
    old_signature = actions and re.search(r"^[ \t]*\w+[ \t]*\([^\n]*\)[ \t]*:",
                                         text[actions.end():action_end], re.M)
    legacy = "principle" in names or bool(old_signature)
    if legacy:
        add(result, "unchecked", text, 0, "legacy", "Legacy signatures/section order are outside these checks.")
    found = []
    for name in CORE:
        matches = [m for m in sections if m[1].strip().lower() == name]
        if name == "operational principle" and not matches and "principle" in names:
            matches = [m for m in sections if m[1].strip().lower() == "principle"]
        if len(matches) != 1:
            if matches or (source.complete and not legacy):
                add(result, "issues", text, matches[0].start() if matches else 0, "section",
                    f"Expected one '## {name}' section.")
            continue
        section = matches[0]
        found.append((section.start(), name))
        following = next((m.start() for m in sections if m.start() > section.start()), None)
        if following is None and not source.complete:
            continue
        end = following if following is not None else len(text)
        if not source.content[section.end():end].strip():
            add(result, "issues", text, section.start(), "empty-section", f"Section '{name}' needs content.")
    if not legacy and len(found) == len(CORE) and tuple(n for _, n in sorted(found)) != CORE:
        add(result, "issues" if declared else "unchecked", text, 0, "section-order",
            "Core section order is purpose, state, actions, operational principle.")
    if coverage and sections and coverage[0].start() > sections[0].start():
        add(result, "issues", text, coverage[0].start(), "coverage-position",
            "Coverage belongs before the sections.")


def check_fields(source, start, end, result):
    """Check top-level field names; values and nested records remain opaque."""
    text, parts, depth, first = source.syntax, [], 0, start + 1
    for token in TOKEN.finditer(text, first, end):
        if token[0] in ("[", "{", "("):
            depth += 1
        elif token[0] in ("]", "}", ")"):
            depth -= 1
        elif token[0] == ";" and depth == 0:
            parts.append((first, token.start()))
            first = token.end()
    parts.append((first, end))
    seen = set()
    for index, (left, right) in enumerate(parts):
        if not source.content[left:right].strip():
            if index < len(parts) - 1:
                add(result, "issues", text, left, "record-field", "Empty named field.")
            continue
        field = FIELD.match(text, left, right)
        if not field:
            add(result, "issues", text, left, "record-field", "Use named fields: name: value; name: value.")
            continue
        if (source.content[left:field.start(1)].strip() or
                source.content[field.end(1):field.end() - 1].strip()):
            add(result, "unchecked", text, left, "record-syntax", "Literal outside a named field value.")
            continue
        if field[1] in seen:
            add(result, "issues", text, field.start(1), "duplicate-field", f"Repeated field '{field[1]}'.")
        seen.add(field[1])
        if not source.content[field.end():right].strip():
            add(result, "issues", text, field.start(1), "field-value", f"Field '{field[1]}' needs a value.")
        depth = 0
        for token in TOKEN.finditer(text, field.end(), right):
            if token[0] in ("[", "{", "("):
                depth += 1
            elif token[0] in ("]", "}", ")"):
                depth -= 1
            elif token[0] == ":" and depth == 0:
                add(result, "unchecked", text, token.start(), "record-syntax",
                    "Unexpected ':' in a field value; fields may need a ';' separator.")
                break


def check_calls(source, name, start, end, result):
    text, cursor = source.syntax, start

    def skip(offset):
        cursor = offset
        while cursor < end and text[cursor].isspace():
            cursor += 1
        if source.content[offset:cursor].strip():
            add(result, "unchecked", text, offset, "call-syntax", "Literal outside an action record.")
            return None
        return cursor

    while cursor < end:
        cursor = skip(cursor)
        if cursor is None:
            return
        call = CALL.match(text, cursor, end)
        if cursor < end and not call:
            add(result, "unchecked", text, cursor, "call-syntax",
                f"Unsupported '{name}' content; expected Concept/action: [named inputs].")
            return
        if call is None:
            return
        if source.content[call.end(2):call.end() - 1].strip():
            add(result, "unchecked", text, call.end(2), "call-syntax", "Literal between action name and ':'.")
            return
        cursor = skip(call.end())
        if cursor is None:
            return
        closing = record_end(text, cursor, end)
        if closing is None:
            add(result, "issues", text, cursor, "input-record", "Action needs a bracketed input record.")
            return
        check_fields(source, cursor, closing, result)
        cursor = skip(closing + 1)
        if cursor is None:
            return
        has_output = text.startswith("=>", cursor)
        if name == "when" and not has_output:
            add(result, "issues", text, call.start(), "when-completion", "'when' matches completions: inputs => outputs.")
        if name == "then" and has_output:
            add(result, "issues", text, cursor, "then-output", "'then' invokes actions and must not declare outputs.")
        if has_output:
            cursor = skip(cursor + 2)
            if cursor is None:
                return
            closing = record_end(text, cursor, end)
            if closing is None:
                add(result, "issues", text, cursor, "output-record", "Completion needs a bracketed output record.")
                return
            check_fields(source, cursor, closing, result)
            cursor = closing + 1


def check_rule(source, start, end, complete, result):
    text = source.syntax
    body = text[start:end]
    if (re.search(r"^[ \t]*(when|then)\b", body, re.M) and
        not re.search(r"\b(?:when|then)\s*\{", body)
    ):
        add(result, "unchecked", text, start, "legacy", "Legacy rule notation was not checked.")
        return
    stack, blocks, ranges, active = [], [], [], None
    pairs = {"}": "{", "]": "[", ")": "("}
    for match in TOKEN.finditer(text, start, end):
        value, offset = match[0], match.start()
        if not stack and value in CLAUSES:
            prefix = text[text.rfind("\n", start, offset) + 1:offset].rstrip()
            opening = OPEN_BLOCK.match(text, match.end(), end)
            if (not prefix or prefix.endswith("}")) and opening:
                if source.content[match.end():opening.end() - 1].strip():
                    add(result, "unchecked", text, match.end(), "block-syntax", "Literal between clause name and '{'.")
                blocks.append(value)
                active = (value, offset, opening.end() - 1)
        if value in ("{", "[", "("):
            stack.append((value, offset))
        elif value in pairs:
            if not stack or stack[-1][0] != pairs[value]:
                add(result, "issues", text, offset, "delimiter", f"Unexpected closing '{value}'.")
                continue
            stack.pop()
            if not stack and active:
                name, clause_start, opened = active
                if name != "where" and not source.content[opened + 1:offset].strip():
                    add(result, "issues", text, opened, "empty-block", f"'{name}' needs content.")
                elif name != "where":
                    check_calls(source, name, opened + 1, offset, result)
                ranges.append((clause_start, match.end()))
                active = None
    if complete and source.content[start:end].strip() and not blocks:
        add(result, "unchecked", text, start, "rule-syntax", "Unsupported rule body.")
        return
    if complete:
        for opening, offset in stack:
            add(result, "issues", text, offset, "delimiter", f"Unclosed '{opening}'.")
        for name in ("when", "then"):
            if name not in blocks:
                add(result, "issues", text, start, "missing-block", f"Rule needs a '{name}' block.")
        cursor = start
        for left, right in ranges + [(end, end)]:
            if source.content[cursor:left].strip():
                add(result, "unchecked", text, cursor, "rule-syntax", "Content outside recognized rule blocks was not checked.")
            cursor = right
    for name in CLAUSES:
        if blocks.count(name) > 1:
            add(result, "issues", text, start, "duplicate-block", f"Repeated '{name}' block.")
    if blocks != [name for name in CLAUSES if name in blocks]:
        add(result, "issues", text, start, "block-order", "Order is when, optional where, then.")


def check_app(source, result, registry):
    text = source.syntax
    rules = list(RULE.finditer(text))
    if not rules:
        add(result, "unchecked", text, 0, "rules-missing", "No recognized 'sync NAME' declarations.")
    for index, rule in enumerate(rules):
        identity = (result["name"], rule[1])
        if has_literal(source, rule):
            add(result, "unchecked", text, rule.start(), "declaration-syntax", "Literal in a rule declaration.")
        elif identity in registry:
            path, line = registry[identity]
            add(result, "issues", text, rule.start(), "duplicate-rule",
                f"Rule '{rule[1]}' for app '{result['name']}' was already declared at {path}:{line}.")
        else:
            registry[identity] = (result["path"], text.count("\n", 0, rule.start()) + 1)
        following = rules[index + 1].start() if index + 1 < len(rules) else None
        end = following if following is not None else source.known_end
        complete = following is not None or source.complete
        heading = re.search(r"^#{1,6}[ \t]", text[rule.end():end], re.M)
        if heading:
            end, complete = rule.end() + heading.start(), True
        check_rule(source, rule.end(), end, complete, result)


def file_status(result):
    return "format_error" if result["issues"] else "not_checked" if result["unchecked"] else "format_checked"


def check_text(text, path, registry=None):
    """Check an already-read raw-text snapshot; path only labels diagnostics."""
    source = prepare(text)
    text = source.syntax
    result = {"path": str(path), "kind": None, "name": None, "issues": [], "unchecked": list(source.unchecked)}
    headers = list(HEAD.finditer(text))
    if not headers:
        add(result, "unchecked", text, 0, "unsupported", "Expected '# concept NAME' or '# app NAME'.")
    elif len(headers) > 1:
        add(result, "issues", text, headers[1].start(), "declaration", "Declare one concept or app per file.")
    else:
        result["kind"] = headers[0][1]
        result["name"] = headers[0][2]
        if source.content[:headers[0].start()].strip():
            add(result, "unchecked", text, 0, "preamble", "Preamble is outside the supported format.")
        if has_literal(source, headers[0]):
            add(result, "unchecked", text, headers[0].start(), "declaration-syntax", "Literal in a concept/app declaration.")
        elif result["kind"] == "concept":
            check_concept(source, result)
        else:
            check_app(source, result, {} if registry is None else registry)
    result["status"] = file_status(result)
    return result


def check_file(path, registry=None):
    return check_text(Path(path).read_text(encoding="utf-8-sig"), path, registry)


def inspect(paths):
    files, errors, registry, visited = [], [], {}, set()
    for path in paths:
        try:
            identity = path.resolve()
            if identity in visited:
                continue
            visited.add(identity)
            files.append(check_file(path, registry))
        except (OSError, UnicodeError, RuntimeError) as error:
            errors.append({"path": str(path), "message": str(error)})
    if errors:
        status = "read_error"
    elif any(f["issues"] for f in files):
        status = "format_error"
    elif any(f["unchecked"] for f in files):
        status = "not_checked"
    else:
        status = "format_checked"
    return {"status": status, "scope": "format only", "files": files, "read_errors": errors}


def render(report):
    for item in report["files"]:
        print(f"{item['path']}: {item['status']} (format only)")
        for category, label in (("issues", "error"), ("unchecked", "not checked")):
            for finding in item[category]:
                print(f"  {label}:{finding['line']} {finding['code']}: {finding['message']}")
    for error in report["read_errors"]:
        print(f"{error['path']}: read_error: {error['message']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog=(
        "Status/exit: format_checked=0, format_error=1, read_error=2, not_checked=3. "
        "Checks document structure, when/then records, and app-local rule names. "
        "Does not resolve where expressions, signatures, types, or bindings; "
        "no result proves concept independence or semantic correctness."))
    parser.add_argument("paths", metavar="FILE", nargs="+", type=Path, help="CONCEPT.md or SYNCS.md (UTF-8)")
    parser.add_argument("--json", action="store_true", help="emit a JSON report")
    args = parser.parse_args(argv)
    report = inspect(args.paths)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        render(report)
    return EXIT[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
