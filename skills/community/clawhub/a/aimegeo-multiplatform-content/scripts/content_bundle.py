#!/usr/bin/env python3
"""Offline checks and handoff aggregation. This module never writes articles."""

import argparse
import csv
import io
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlsplit


class BundleError(ValueError):
    def __init__(self, code, detail):
        super().__init__(detail)
        self.code = code


def require(condition, code, detail):
    if not condition:
        raise BundleError(code, detail)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def local_path(root, value):
    require(nonempty(value), "PATH", "A nonempty relative path is required")
    path = Path(value)
    require(not path.is_absolute() and ".." not in path.parts, "PATH", value)
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()), "PATH", value)
    return resolved


def read_text(path):
    # Preserve CRLF in existing manuscripts instead of normalizing the body.
    return path.read_bytes().decode("utf-8")


def load_json(path):
    obj = json.loads(read_text(path))
    require(isinstance(obj, dict), "SCHEMA", f"Object required: {path.name}")
    return obj


def objects(value, label):
    require(isinstance(value, list) and all(isinstance(x, dict) for x in value),
            "SCHEMA", f"{label} must be an array of objects")
    return value


def strings(value, label):
    require(isinstance(value, list) and all(nonempty(x) for x in value),
            "SCHEMA", f"{label} must be an array of nonempty strings")
    require(len(value) == len(set(value)), "SCHEMA", f"Duplicate item: {label}")
    return value


def indexed(value, label):
    result = {}
    for obj in objects(value, label):
        key = obj.get("id")
        require(nonempty(key) and key not in result, "SCHEMA", f"Invalid/duplicate {label} id")
        result[key] = obj
    return result


def leading_title(body):
    """Locate only the document's first visible ATX/Setext H1 title text."""
    lines = body.splitlines(keepends=True)
    offset = 0
    for index, line in enumerate(lines):
        clean = line.rstrip("\r\n")
        if not clean.strip():
            offset += len(line)
            continue
        atx = re.fullmatch(r"( {0,3}#)(?:([ \t]+)(.*))?", clean)
        if atx:
            content = atx[3] or ""
            # Optional closing hashes and trailing spaces are Markdown syntax.
            content = re.sub(r"[ \t]+#+[ \t]*$", "", content).rstrip(" \t")
            if re.fullmatch(r"#+", content):
                content = ""
            start = offset + len(atx[1]) + len(atx[2] or "")
            return content, start, start + len(content), offset, offset + len(line)
        if (index + 1 < len(lines) and not clean.startswith(("    ", "\t"))
                and not re.match(r" {0,3}(?:#{1,6}(?:[ \t]|$)|>|[-+*][ \t]|\d+[.)][ \t]|`{3}|~{3})", clean)
                and re.fullmatch(r" {0,3}=+[ \t]*", lines[index + 1].rstrip("\r\n"))):
            content = clean.strip(" \t")
            start = offset + len(clean) - len(clean.lstrip(" \t"))
            return content, start, start + len(content), offset, offset + len(line) + len(lines[index + 1])
        # A later heading, including one in a code fence, is article body.
        return None
    return None


def body_without_title_text(body):
    title = leading_title(body)
    return (body[:title[1]], body[title[2]:]) if title else (body, None)


def visible_title_bytes(body):
    title = leading_title(body)
    return body[title[3]:title[4]] if title else None


def read_article(path):
    match = re.fullmatch(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", read_text(path), re.S)
    require(match is not None, "FRONTMATTER", path.name)
    meta = {}
    for line in match[1].splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        require(sep and re.fullmatch(r"[a-z_]+", key) and key not in meta,
                "FRONTMATTER", f"Invalid/duplicate field: {path.name}: {key}")
        try:
            meta[key] = json.loads(value.strip())
        except json.JSONDecodeError as exc:
            raise BundleError("FRONTMATTER", f"Use JSON values in YAML fields: {key}") from exc
    for key in ("platform", "content_type", "title", "topic"):
        require(nonempty(meta.get(key)), "FRONTMATTER", f"Missing {key}: {path.name}")
    for key in ("fact_ids", "asset_ids"):
        strings(meta.get(key), key)
    body = match[2]
    require(bool(body.strip()), "EMPTY_ARTICLE", path.name)
    title = leading_title(body)
    require(title is None or title[0] == meta["title"], "TITLE_MISMATCH",
            f"{path.name}: metadata title differs from the leading H1")
    return meta, body


def http_url(value):
    if not isinstance(value, str):
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme in ("https", "http") and bool(parts.netloc)
    except ValueError:
        return False


def geo_summary(observations, sources, source_text):
    counts = {key: 0 for key in ("observed", "simulated", "not_run", "query_failed")}
    mentions = citations = 0
    for item in objects(observations, "geo_observations"):
        status = item.get("status")
        require(nonempty(status) and status in counts, "GEO_STATUS", "Unknown GEO status")
        counts[status] += 1
        if status != "observed":
            require(item.get("mention_count") is None and item.get("native_citations") is None,
                    "GEO_UNKNOWN_COUNT", f"{status} counts must be null")
            if status == "simulated":
                require(nonempty(item.get("answer")), "GEO_EVIDENCE", "Label the simulated answer")
            else:
                require(item.get("answer") is None, "GEO_EVIDENCE", "No answer collected")
            if status == "query_failed":
                require(nonempty(item.get("error")), "GEO_EVIDENCE", "Missing query error")
            continue
        for field in ("engine", "query", "collected_at", "answer", "evidence_source_id"):
            require(nonempty(item.get(field)), "GEO_EVIDENCE", f"Missing {field}")
        try:
            stamp = datetime.fromisoformat(item["collected_at"].replace("Z", "+00:00"))
            require(stamp.tzinfo is not None, "GEO_EVIDENCE", "A timezone is required")
        except ValueError as exc:
            raise BundleError("GEO_EVIDENCE", "Invalid collected_at") from exc
        sid = item["evidence_source_id"]
        require(sid in sources and item["answer"] in source_text[sid],
                "GEO_EVIDENCE", "Answer missing from the supplied record")
        terms = strings(item.get("brand_terms"), "brand_terms")
        require(bool(terms), "GEO_EVIDENCE", "Missing literal brand terms")
        pattern = "|".join(re.escape(term) for term in sorted(terms, key=len, reverse=True))
        actual_mentions = len(re.findall(pattern, item["answer"]))
        require(type(item.get("mention_count")) is int and item["mention_count"] == actual_mentions,
                "GEO_MENTIONS", "Literal mention count differs from the supplied answer")
        native = objects(item.get("native_citations"), "native_citations")
        urls = []
        for citation in native:
            url = citation.get("url")
            require(http_url(url) and url in source_text[sid] and citation.get("kind") == "native",
                    "GEO_EVIDENCE", "Native citation URL must be in the supplied native-source record")
            urls.append(url)
        require(len(urls) == len(set(urls)), "GEO_EVIDENCE", "Duplicate native citation URL")
        mentions += actual_mentions
        citations += len(urls)
    return {
        "samples_by_status": counts,
        "observed_mention_count": mentions if counts["observed"] else None,
        "observed_native_citation_count": citations if counts["observed"] else None,
    }


def validate_bundle(root):
    root = Path(root).resolve()
    request = load_json(root / "request.json")
    ledger = load_json(root / "事实与来源清单.json")
    require(request.get("schema_version") == 1 and ledger.get("schema_version") == 1,
            "SCHEMA", "schema_version must be 1")
    require(nonempty(request.get("task")), "SCHEMA", "Missing current task")
    assignments = objects(request.get("articles"), "articles")
    require(bool(assignments), "SCHEMA", "At least one article is required")
    articles = {}
    for assignment in assignments:
        filename = assignment.get("file")
        path = local_path(root, filename)
        require(filename not in articles, "SCHEMA", "Duplicate article file")
        meta, body = read_article(path)
        for key in ("platform", "content_type"):
            require(meta[key] == assignment.get(key), "ASSIGNMENT", f"{filename}: {key}")
        operation = assignment.get("operation")
        require(operation in ("new", "preserve", "edit"), "AUTHORIZATION", str(filename))
        if operation != "new":
            original, original_body = read_article(local_path(root, assignment.get("original")))
            allowed = strings(assignment.get("allowed_changes", []), "allowed_changes")
            require(set(allowed) <= {"title", "body"}, "AUTHORIZATION", "Unknown edit scope")
            if operation == "preserve":
                require(not allowed, "AUTHORIZATION", "preserve cannot allow edits")
            else:
                require(bool(allowed) and nonempty(assignment.get("change_request")),
                        "AUTHORIZATION", "edit needs scope and the current change request")
            require("title" in allowed or (meta["title"] == original["title"]
                    and visible_title_bytes(body) == visible_title_bytes(original_body)),
                    "PRESERVE_TITLE", filename)
            # A title-only edit covers its visible H1 text as well as metadata;
            # every other character, including heading syntax/newlines, stays.
            preserved_body = (body_without_title_text(body) == body_without_title_text(original_body)
                              if "title" in allowed else body == original_body)
            require("body" in allowed or preserved_body, "PRESERVE_BODY", filename)
        articles[filename] = (meta, body)

    sources = indexed(ledger.get("sources"), "sources")
    source_text = {}
    for sid, source in sources.items():
        require(nonempty(source.get("label")), "SOURCE", sid)
        kind = source.get("kind")
        if kind == "local_file":
            source_text[sid] = read_text(local_path(root, source.get("path")))
        elif kind == "provided_excerpt":
            require(nonempty(source.get("text")) and nonempty(source.get("locator")), "SOURCE", sid)
            source_text[sid] = source["text"]
        else:
            raise BundleError("SOURCE", f"Unknown source kind: {sid}")

    facts = indexed(ledger.get("facts"), "facts")
    declared = {filename: set() for filename in articles}
    article_sources = {filename: set() for filename in articles}
    for fid, fact in facts.items():
        sid, canonical, quote = fact.get("source_id"), fact.get("canonical"), fact.get("source_quote")
        require(nonempty(sid) and sid in sources and nonempty(canonical) and nonempty(quote), "FACT_SOURCE", fid)
        require(canonical in quote and quote in source_text[sid], "FACT_SOURCE", fid)
        occurrences = objects(fact.get("occurrences"), "occurrences")
        for occurrence in occurrences:
            filename, fragment = occurrence.get("article"), occurrence.get("quote")
            require(nonempty(filename) and filename in articles and nonempty(fragment), "FACT_REFERENCE", fid)
            require(canonical in fragment and fragment in articles[filename][1],
                    "FACT_MISMATCH", f"{filename}: {fid}")
            require(fid not in declared[filename], "FACT_REFERENCE", f"Duplicate occurrence: {fid}")
            declared[filename].add(fid)
            article_sources[filename].add(sid)
    for filename, (meta, _) in articles.items():
        require(set(meta["fact_ids"]) == declared[filename], "FACT_REFERENCE", filename)

    assets = indexed(ledger.get("assets"), "assets")
    for aid, asset in assets.items():
        require(nonempty(asset.get("brief")), "ASSET", aid)
        state = asset.get("state")
        require(state in ("available", "pending_creation"), "ASSET", aid)
        if state == "pending_creation":
            require(asset.get("path") is None, "ASSET", "Pending assets have no deliverable file")
        else:
            image_path = local_path(root, asset.get("path"))
            require(image_path.is_file(), "ASSET_FILE", aid)
            with image_path.open("rb") as image_file:
                head = image_file.read(12)
            require(head.startswith(b"\x89PNG\r\n\x1a\n") or head.startswith(b"\xff\xd8\xff")
                    or (head.startswith(b"RIFF") and head[8:12] == b"WEBP"),
                    "ASSET_FILE", f"Not a PNG/JPEG/WebP header: {aid}")

    rules = {}
    for rule in objects(ledger.get("platform_rules"), "platform_rules"):
        platform = rule.get("platform")
        require(nonempty(platform) and platform not in rules, "RULES", "Invalid/duplicate platform")
        require(rule.get("state") in ("confirmed", "pending_confirmation"), "RULES", platform)
        require(nonempty(rule.get("note")), "RULES", platform)
        if rule["state"] == "confirmed":
            require(nonempty(rule.get("basis")) and nonempty(rule.get("checked_at")), "RULES", platform)
            try:
                date.fromisoformat(rule["checked_at"])
            except ValueError as exc:
                raise BundleError("RULES", f"Invalid checked_at: {platform}") from exc
        rules[platform] = rule
    require(set(rules) == {meta["platform"] for meta, _ in articles.values()}, "RULES", "Platform coverage")

    rows, warnings, used_assets = [], [], set()
    for filename, (meta, _) in articles.items():
        aids = meta["asset_ids"]
        require(set(aids) <= set(assets), "ASSET_REFERENCE", filename)
        used_assets.update(aids)
        pending_assets = any(assets[aid]["state"] == "pending_creation" for aid in aids)
        pending_rules = rules[meta["platform"]]["state"] == "pending_confirmation"
        status = ("待素材及规则确认" if pending_assets and pending_rules else
                  "待素材" if pending_assets else "待规则确认" if pending_rules else "可交接")
        notes = [assets[aid]["brief"] for aid in aids if assets[aid]["state"] == "pending_creation"]
        if pending_rules:
            notes.append(rules[meta["platform"]]["note"])
        rows.append({
            "platform": meta["platform"], "content_type": meta["content_type"],
            "title": meta["title"], "article": filename, "text_status": "complete",
            "asset_status": "pending_creation" if pending_assets else "available" if aids else "not_requested",
            "rules_status": rules[meta["platform"]]["state"], "handoff_status": status,
            "source_ids": ";".join(sorted(article_sources[filename])),
            "pending_actions": "；".join(notes),
        })
        if pending_assets or pending_rules:
            warnings.append({"article": filename, "handoff_status": status})
    require(used_assets == set(assets), "ASSET_REFERENCE", "Unused asset records")
    geo = geo_summary(ledger.get("geo_observations"), sources, source_text)
    report = {"valid": True, "article_count": len(articles), "fact_count": len(facts),
              "warnings": warnings, "geo": geo}
    return report, rows


FIELDS = ["platform", "content_type", "title", "article", "text_status", "asset_status",
          "rules_status", "handoff_status", "source_ids", "pending_actions"]


def handoff_csv(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    # Prevent spreadsheet formula execution without changing manuscript text.
    writer.writerows({key: "'" + str(value) if str(value).startswith(("=", "+", "-", "@", "\t", "\r"))
                     else value for key, value in row.items()} for row in rows)
    return stream.getvalue()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="Check a completed local bundle").add_argument("bundle", type=Path)
    handoff = sub.add_parser("handoff", help="Check, then export the handoff CSV")
    handoff.add_argument("bundle", type=Path)
    handoff.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        report, rows = validate_bundle(args.bundle)
        if args.command == "handoff":
            target = args.output.resolve()
            bundle_root = args.bundle.resolve()
            if target.is_relative_to(bundle_root):
                require(target == bundle_root / "发布交接清单.csv", "OUTPUT_PATH",
                        "Inside a bundle, only 发布交接清单.csv may be written")
            require(target.suffix.lower() == ".csv", "OUTPUT_PATH", "Output must be a CSV file")
            # Validation finishes before opening the destination.
            target.write_text(handoff_csv(rows), encoding="utf-8", newline="")
            report["exported"] = str(args.output)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (BundleError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": getattr(exc, "code", "INPUT"),
                          "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
