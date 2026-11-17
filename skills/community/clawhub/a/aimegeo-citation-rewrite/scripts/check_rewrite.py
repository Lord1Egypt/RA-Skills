#!/usr/bin/env python3
"""Check a scoped Markdown rewrite; never generate prose or call a service.

New implementation by aimeGeo, licensed under MIT-0. See ../LICENSE.
"""

import argparse
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
import sys
import unicodedata


class InputError(ValueError):
    """Input cannot be checked unambiguously."""


@dataclass
class Document:
    titles: list
    preamble: str
    sections: list


def parse_document(text):
    """Preserve all original bytes after UTF-8 decoding, including CRLF."""
    titles, starts = [], []
    offset = 0
    fence_char, fence_len = None, 0
    for line in text.splitlines(keepends=True):
        clean = line.rstrip("\r\n")
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", clean)
        if fence_char:
            if fence and fence[1][0] == fence_char and len(fence[1]) >= fence_len and not fence[2].strip():
                fence_char = None
        elif fence:
            fence_char, fence_len = fence[1][0], len(fence[1])
        elif re.match(r"^ {0,3}#\s+\S", clean):
            titles.append(clean)
        elif re.match(r"^ {0,3}##[ \t]+\S", clean):
            starts.append((offset, clean))
        offset += len(line)
    sections = []
    for i, (start, heading) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(text)
        sections.append((heading, text[start:end]))
    return Document(titles, text[:starts[0][0]] if starts else text, sections)


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InputError(label + " must be a nonempty string")
    return value


def items(value, label):
    if not isinstance(value, list):
        raise InputError(label + " must be a list")
    return value


def object_fields(value, required, optional=()):
    if not isinstance(value, dict):
        raise InputError("expected a JSON object")
    missing = set(required) - value.keys()
    unknown = value.keys() - set(required) - set(optional)
    if missing or unknown:
        raise InputError(f"invalid fields: missing={sorted(missing)}, unknown={sorted(unknown)}")


def check_plan(plan, original, doc):
    object_fields(plan, ("schema_version", "editable_sections", "sources", "questions", "numeric_claims"))
    if type(plan["schema_version"]) is not int or plan["schema_version"] != 1:
        raise InputError("schema_version must be integer 1")
    if len(doc.titles) != 1:
        raise InputError("original must contain exactly one ATX H1 title")
    headings = [heading for heading, _ in doc.sections]
    if len(headings) != len(set(headings)):
        raise InputError("original has duplicate H2 headings")
    scopes = items(plan["editable_sections"], "editable_sections")
    if not scopes or any(not isinstance(s, str) or s not in headings for s in scopes):
        raise InputError("editable_sections must name existing H2 heading lines")
    if len(scopes) != len(set(scopes)):
        raise InputError("editable_sections contains duplicates")
    sources = {}
    for source in items(plan["sources"], "sources"):
        object_fields(source, ("id", "kind", "reference", "excerpt"), ("verified_at",))
        for field in ("id", "reference", "excerpt"):
            nonempty(source[field], "source." + field)
        if source["id"] in sources:
            raise InputError("duplicate source id")
        if source["kind"] not in ("original", "user_provided", "verified"):
            raise InputError("source.kind must be original, user_provided or verified")
        if source["kind"] == "original" and source["excerpt"] not in original:
            raise InputError("original source excerpt is absent from the original article")
        if source["kind"] == "verified":
            try:
                date = datetime.fromisoformat(nonempty(source.get("verified_at"), "verified_at").replace("Z", "+00:00"))
                if date.tzinfo is None:
                    raise ValueError("missing timezone")
            except (TypeError, ValueError) as exc:
                raise InputError("verified source needs an ISO 8601 verified_at with timezone") from exc
        sources[source["id"]] = source
    questions = items(plan["questions"], "questions")
    if not questions:
        raise InputError("questions must not be empty")
    seen = set()
    for question in questions:
        object_fields(question, ("question", "section", "answer", "support_ids"))
        for field in ("question", "section", "answer"):
            nonempty(question[field], "question." + field)
        if "\n" in question["question"] or "\r" in question["question"]:
            raise InputError("question must fit a single heading line")
        if question["section"] not in scopes:
            raise InputError("question section must be editable")
        if question["question"] in seen:
            raise InputError("duplicate question")
        seen.add(question["question"])
        support = items(question["support_ids"], "support_ids")
        if any(not isinstance(s, str) or s not in sources for s in support):
            raise InputError("unknown question support id")
    claims = items(plan["numeric_claims"], "numeric_claims")
    seen_claims = set()
    for claim in claims:
        object_fields(claim, ("text", "source_id", "evidence_quote"))
        for field in claim:
            nonempty(claim[field], "numeric_claim." + field)
        if claim["source_id"] not in sources:
            raise InputError("unknown numeric claim source id")
        if claim["text"] in seen_claims:
            raise InputError("duplicate numeric claim text")
        seen_claims.add(claim["text"])
    return sources


def numbers(text):
    """Conservative surface count, not semantic proof of numeric truth."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"https?://[^\s<>\])]+", "", text)
    text = re.sub(r"(?m)^\s*(?:>\s*)*\d+[.)][ \t]+", "", text)
    arabic = re.findall(r"[+-]?\d+(?:,\d{3})*(?:\.\d+)?%?", text)
    chinese = re.findall(
        r"百分之[零〇一二三四五六七八九十百千万亿两点]+|"
        r"[零〇一二三四五六七八九十百千万亿两]+(?:点[零〇一二三四五六七八九]+)?"
        r"(?:个|次|天|小时|分钟|秒|倍|元|条|篇|人|账号)", text
    )
    return Counter(n.replace(",", "") for n in arabic + chinese)


def question_present(section, question, answer):
    """Match a real H3 block, ignoring headings inside fenced code."""
    active, blocks = None, []
    fence_char, fence_len = None, 0
    for line in section.splitlines(keepends=True):
        clean = line.rstrip("\r\n")
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", clean)
        if fence_char:
            if fence and fence[1][0] == fence_char and len(fence[1]) >= fence_len and not fence[2].strip():
                fence_char = None
            if active is not None:
                blocks[active][1] += line
        elif fence:
            fence_char, fence_len = fence[1][0], len(fence[1])
            if active is not None:
                blocks[active][1] += line
        elif re.match(r"^ {0,3}#{1,3}[ \t]+", clean):
            if clean == "### " + question:
                blocks.append([clean, ""])
                active = len(blocks) - 1
            else:
                active = None
        elif active is not None:
            blocks[active][1] += line
    return len(blocks) == 1 and answer in blocks[0][1]


def validate(original, revised, plan):
    before, after = parse_document(original), parse_document(revised)
    sources = check_plan(plan, original, before)
    errors = []

    def fail(code, detail):
        errors.append({"code": code, "detail": detail})

    if after.titles != before.titles:
        fail("title_changed", "H1 title must be preserved exactly")
    old_headings = [h for h, _ in before.sections]
    new_headings = [h for h, _ in after.sections]
    if new_headings != old_headings:
        fail("section_structure_changed", "H2 heading lines and order must be preserved")
    if before.preamble != after.preamble:
        fail("out_of_scope_change", "preamble changed")
    new_sections = dict(after.sections)
    scopes = set(plan["editable_sections"])
    changed = []
    for heading, body in before.sections:
        if new_sections.get(heading) != body:
            changed.append(heading)
            if heading not in scopes:
                fail("out_of_scope_change", heading)
    coverage = []
    for question in plan["questions"]:
        present = question_present(new_sections.get(question["section"], ""), question["question"], question["answer"])
        supported = bool(question["support_ids"])
        if not present:
            fail("question_not_covered", question["question"])
        if not supported:
            fail("missing_answer_support", question["question"])
        coverage.append({"question": question["question"], "section": question["section"], "covered": present,
                         "support_kinds": sorted({sources[s]["kind"] for s in question["support_ids"]})})
    allowed_numbers = Counter()
    for claim in plan["numeric_claims"]:
        quote, text = claim["evidence_quote"], claim["text"]
        valid = True
        if text not in revised:
            fail("claim_not_in_revision", text)
            valid = False
        if quote not in sources[claim["source_id"]]["excerpt"]:
            fail("quote_not_in_source", claim["source_id"])
            valid = False
        if numbers(text) - numbers(quote):
            fail("claim_number_not_in_evidence", text)
            valid = False
        if valid:
            for token, count in numbers(text).items():
                allowed_numbers[token] += count * revised.count(text)
    introduced = numbers(revised) - numbers(original)
    for token, count in (introduced - allowed_numbers).items():
        fail("unbacked_numeric", {"token": token, "unsupported_occurrences": count})
    return {"ok": not errors, "errors": errors, "changed_sections": changed,
            "covered_questions": sum(row["covered"] for row in coverage),
            "total_questions": len(coverage), "coverage": coverage,
            "introduced_numbers": dict(introduced), "assessment": "mechanical_text_check_only"}


def reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise InputError("duplicate JSON key: " + key)
        obj[key] = value
    return obj


def read_text(path):
    return Path(path).read_bytes().decode("utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--revised", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        original, revised = read_text(args.original), read_text(args.revised)
        if not original.strip() or not revised.strip():
            raise InputError("articles must not be empty")
        plan = json.loads(read_text(args.plan), object_pairs_hook=reject_duplicate_keys)
        result = validate(original, revised, plan)
    except (OSError, UnicodeError, ValueError) as exc:
        result = {"ok": False, "errors": [{"code": "invalid_input", "detail": str(exc)}]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
