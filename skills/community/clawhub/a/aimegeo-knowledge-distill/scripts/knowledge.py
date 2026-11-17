#!/usr/bin/env python3
"""Index local text and validate/render agent-authored, evidence-linked FAQs.

Standard library only. No network, model calls, shell execution or text generation.
"""

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import unicodedata
from pathlib import Path


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


def keys(value, expected, where):
    need(isinstance(value, dict), f"{where}: expected object")
    need(set(value) == set(expected), f"{where}: fields must be {', '.join(expected)}")


def string(value, where, inline=False):
    need(isinstance(value, str) and value.strip(), f"{where}: nonempty text required")
    need(not inline or ('\n' not in value and '\r' not in value), f"{where}: use one line")
    return value


def array(value, where):
    need(isinstance(value, list), f"{where}: expected array")
    return value


def identifier(value, where):
    string(value, where, inline=True)
    need(re.fullmatch(r"[A-Z][A-Z0-9-]{0,31}", value), f"{where}: invalid ID")
    return value


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        need(key not in obj, f"JSON: duplicate key {key}")
        obj[key] = value
    return obj


def reject_constant(value):
    raise Invalid(f"JSON: invalid constant {value}")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object, parse_constant=reject_constant)


def paragraphs(text, markdown):
    """Blank-delimited blocks; preserve physical line numbers and heading context."""
    blocks, buffer, start = [], [], None
    headings, fence = [], None

    def flush(end):
        nonlocal start
        if buffer:
            blocks.append({"location": " / ".join(h for _, h in headings) or "正文",
                           "line_start": start, "line_end": end,
                           "text": "\n".join(buffer)})
            buffer.clear()
            start = None

    lines = text.splitlines()
    for number, line in enumerate(lines, 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line) if markdown else None
        heading = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line) if markdown else None
        if heading and fence is None:
            flush(number - 1)
            depth = len(heading[1])
            headings[:] = [(d, h) for d, h in headings if d < depth]
            headings.append((depth, heading[2]))
            continue
        if not line.strip() and fence is None:
            flush(number - 1)
            continue
        if start is None:
            start = number
        buffer.append(line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
    flush(len(lines))
    for block in blocks:
        yield block


def make_index(root):
    root = Path(root).resolve()
    need(root.is_dir(), "sources: directory required")
    sources = []
    for path in sorted(root.rglob("*")):
        need(not path.is_symlink(), "sources: symbolic links are not supported")
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt"}:
            continue
        relative = path.relative_to(root).as_posix()
        need(not any(c in relative for c in '\r\n'), "sources: newline in filename")
        raw = path.read_bytes()
        content = raw.decode("utf-8-sig")
        need('\x00' not in content, f"sources: binary content in {relative}")
        source_id = "S-" + hashlib.sha256(relative.encode("utf-8")).hexdigest()[:12]
        locators = list(paragraphs(content, path.suffix.lower() == ".md"))
        if not locators:
            continue
        for number, block in enumerate(locators, 1):
            block["id"] = f"{source_id}:P{number:03d}"
        title_match = re.search(r"^#\s+(.+?)\s*$", content, re.M) if path.suffix.lower() == ".md" else None
        sources.append({"id": source_id, "title": title_match[1] if title_match else path.stem,
                        "path": relative, "sha256": hashlib.sha256(raw).hexdigest(),
                        "locators": locators})
    need(sources, "sources: no nonempty UTF-8 .md/.txt material")
    return {"schema_version": 1, "sources": sources}


def verified_index(index_path, root):
    saved = read_json(index_path)
    current = make_index(root)
    need(saved == current, "index: stale or modified; re-index current source files and review citations")
    return current


def validate(bundle, index):
    keys(bundle, ["schema_version", "questions", "issues"], "bundle")
    need(type(bundle["schema_version"]) is int and bundle["schema_version"] == 1,
         "bundle: schema_version must be 1")
    questions = array(bundle["questions"], "questions")
    issues = array(bundle["issues"], "issues")
    need(questions or issues, "bundle: at least one question or open issue required")
    locators = {p["id"]: p for s in index["sources"] for p in s["locators"]}
    usage = {locator: set() for locator in locators}
    ids, question_map, issue_map = set(), {}, {}
    conflict_evidence = {}

    def register(item, fields, where):
        keys(item, fields, where)
        item_id = identifier(item["id"], where + ".id")
        need(item_id not in ids, f"{where}: duplicate ID {item_id}")
        ids.add(item_id)
        return item_id

    def refs(items, owner):
        seen, spans = set(), set()
        for ref in array(items, owner + ".refs"):
            keys(ref, ["locator", "quote"], owner + ".ref")
            locator = string(ref["locator"], owner + ".locator", inline=True)
            need(locator in locators, f"{owner}: unknown locator {locator}")
            quote = string(ref["quote"], owner + ".quote")
            source_text = locators[locator]["text"]
            start = source_text.find(quote)
            need(start >= 0, f"{owner}: quote not found in {locator}")
            need((locator, quote) not in seen, f"{owner}: duplicate citation")
            seen.add((locator, quote))
            usage[locator].add(owner)
            # No offset field: every occurrence is possible until context disambiguates it.
            while start >= 0:
                spans.add((locator, start, start + len(quote)))
                start = source_text.find(quote, start + 1)
        return spans

    for issue in issues:
        iid = register(issue, ["id", "kind", "topic", "detail", "needed", "question_ids", "refs"], "issue")
        need(issue["kind"] in ("missing", "conflict"), f"{iid}: unknown issue kind")
        for field in ("topic", "detail", "needed"):
            string(issue[field], iid + "." + field)
        qids = array(issue["question_ids"], iid + ".question_ids")
        for qid in qids:
            identifier(qid, iid + ".question_id")
        need(len(qids) == len(set(qids)), f"{iid}: duplicate question link")
        issue_evidence = refs(issue["refs"], iid)
        need(issue["kind"] != "conflict" or len(issue["refs"]) >= 2,
             f"{iid}: conflict requires at least two distinct source passages")
        if issue["kind"] == "conflict":
            conflict_evidence[iid] = issue_evidence
        issue_map[iid] = issue

    seen_questions = set()
    for question in questions:
        qid = register(question, ["id", "question", "status", "claims", "issue_ids"], "question")
        text = string(question["question"], qid + ".question", inline=True)
        normalized = re.sub(r"\s+", "", unicodedata.normalize("NFKC", text).casefold())
        # Only sentence endings are cosmetic; internal dots distinguish 1.5/15
        # and version identifiers such as v1.5.0/v15.0.
        normalized = normalized.rstrip("?.!。")
        need(normalized not in seen_questions, f"{qid}: duplicate question")
        seen_questions.add(normalized)
        status = question["status"]
        need(status in ("answered", "partial", "conflict", "missing"), f"{qid}: unknown status")
        links = array(question["issue_ids"], qid + ".issue_ids")
        for iid in links:
            identifier(iid, qid + ".issue_id")
            need(iid in issue_map, f"{qid}: unknown issue {iid}")
        need(len(links) == len(set(links)), f"{qid}: duplicate issue link")
        kinds = {issue_map[iid]["kind"] for iid in links}
        claims = array(question["claims"], qid + ".claims")
        evidence = set()
        for claim in claims:
            keys(claim, ["text", "refs"], qid + ".claim")
            string(claim["text"], qid + ".claim.text")
            supported = refs(claim["refs"], qid)
            need(supported, f"{qid}: each claim requires evidence")
            evidence.update(supported)
        if status == "answered":
            need(claims and not links, f"{qid}: answered requires claims and no unresolved issues")
        elif status == "partial":
            need(claims and kinds == {"missing"}, f"{qid}: partial requires claims and a missing issue")
        elif status == "missing":
            need(not claims and kinds == {"missing"}, f"{qid}: missing cannot contain factual answers")
        else:
            need("conflict" in kinds, f"{qid}: conflict status requires a conflict issue")
        # Only overlapping quoted spans carry a registered conflict, not the whole paragraph.
        for iid, conflicting in conflict_evidence.items():
            if any(locator == other_locator and start < other_end and other_start < end
                   for locator, start, end in evidence
                   for other_locator, other_start, other_end in conflicting):
                need(iid in links and status == "conflict",
                     f"{qid}: conflicting evidence must link {iid} and use conflict status")
        question_map[qid] = question

    for iid, issue in issue_map.items():
        actual = {qid for qid, q in question_map.items() if iid in q["issue_ids"]}
        need(set(issue["question_ids"]) == actual, f"{iid}: question links must match both directions")
    return usage


def citation_lines(refs, lookup):
    lines = []
    for ref in refs:
        source, locator = lookup[ref["locator"]]
        lines.append(f"- 来源：{source['path']} · {locator['location']} · "
                     f"L{locator['line_start']}-L{locator['line_end']} · `{locator['id']}`")
        lines.extend("> " + line for line in ref["quote"].splitlines())
    return lines


def render(bundle, index, usage):
    lookup = {p["id"]: (s, p) for s in index["sources"] for p in s["locators"]}
    names = {"answered": "可回答", "partial": "部分可答", "conflict": "资料冲突", "missing": "待补资料"}
    faq = ["# 常见问答", "", f"共 {len(bundle['questions'])} 个问题；问题数量按现有资料确定。", ""]
    if not bundle["questions"]:
        faq.extend(["当前资料尚无可确认的问答，待补项见《待补及冲突信息》。", ""])
    for q in bundle["questions"]:
        faq.extend([f"## {q['id']} {q['question']}", "", f"状态：{names[q['status']]}", ""])
        for claim in q["claims"]:
            faq.extend([claim["text"], ""])
            faq.extend(citation_lines(claim["refs"], lookup))
            faq.append("")
        if q["issue_ids"]:
            faq.extend(["待核实：" + "、".join(q["issue_ids"]) + "（见《待补及冲突信息》）。", ""])
    notes = ["# 待补及冲突信息", ""]
    if not bundle["issues"]:
        notes.append("本次整理未记录待补或冲突项；这不表示资料覆盖了所有客户问题。")
    for issue in bundle["issues"]:
        kind = "冲突" if issue["kind"] == "conflict" else "待补"
        notes.extend([f"## {issue['id']} [{kind}] {issue['topic']}", "",
                      issue["detail"], "", "需要补充或确认：" + issue["needed"], "",
                      "关联问答：" + ("、".join(issue["question_ids"]) or "暂不列入问答"), ""])
        notes.extend(citation_lines(issue["refs"], lookup))
        notes.append("")
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["source_id", "title", "path", "sha256", "locator_id", "location", "line_start", "line_end", "used_by"])
    for source in index["sources"]:
        for p in source["locators"]:
            row = [source["id"], source["title"], source["path"], source["sha256"], p["id"], p["location"],
                   p["line_start"], p["line_end"], ";".join(sorted(usage[p["id"]]))]
            # Avoid treating an untrusted filename/title as a spreadsheet formula.
            writer.writerow(["'" + v if isinstance(v, str) and v.lstrip().startswith(("=", "+", "-", "@")) else v for v in row])
    return {"常见问答.md": "\n".join(faq).rstrip() + "\n",
            "资料索引.csv": stream.getvalue(),
            "待补及冲突信息.md": "\n".join(notes).rstrip() + "\n"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("index", help="index UTF-8 .md/.txt source paragraphs")
    build.add_argument("--sources", required=True)
    build.add_argument("--out", required=True)
    for name in ("check", "export"):
        cmd = sub.add_parser(name, help="validate" if name == "check" else "validate and convert authored content")
        cmd.add_argument("--sources", required=True)
        cmd.add_argument("--index", required=True)
        cmd.add_argument("--bundle", required=True)
        if name == "export":
            cmd.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "index":
            index = make_index(args.sources)
            out = Path(args.out)
            need(out.suffix.lower() == ".json", "index: --out must end in .json")
            with out.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(index, ensure_ascii=False, indent=2) + "\n")
            result = {"ok": True, "sources": len(index["sources"]),
                      "paragraphs": sum(len(s["locators"]) for s in index["sources"])}
        else:
            index = verified_index(args.index, args.sources)
            bundle = read_json(args.bundle)
            usage = validate(bundle, index)
            if args.command == "export":
                files = render(bundle, index, usage)
                out = Path(args.out)
                need(not out.resolve().is_relative_to(Path(args.sources).resolve()),
                     "export: --out must be outside the source directory")
                out.mkdir(exist_ok=False)
                written = []
                try:
                    for name, content in files.items():
                        path = out / name
                        with path.open("x", encoding="utf-8", newline="") as handle:
                            written.append(path)
                            handle.write(content)
                except OSError:
                    for path in written:
                        path.unlink()
                    out.rmdir()
                    raise
            result = {"ok": True, "questions": len(bundle["questions"]),
                      "claims": sum(len(q["claims"]) for q in bundle["questions"]),
                      "missing": sum(i["kind"] == "missing" for i in bundle["issues"]),
                      "conflicts": sum(i["kind"] == "conflict" for i in bundle["issues"])}
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (Invalid, OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
