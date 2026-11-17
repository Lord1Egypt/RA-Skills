#!/usr/bin/env python3
"""Offline JSON-LD checking, safe HTML embedding, and local batch conversion."""

import argparse
import copy
import json
import math
import re
import sys
import unicodedata
from datetime import date, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


PROFILE = "aimegeo-schema-markup/1.0.0"
CONTEXT = "https://schema.org"
REQUIRED = {
    "Organization": ("name",), "WebSite": ("name", "url"),
    "Article": ("headline",), "BlogPosting": ("headline",),
    "FAQPage": ("mainEntity",), "Question": ("name", "acceptedAnswer"),
    "Answer": ("text",), "Product": ("name",),
    "Offer": ("price", "priceCurrency"),
    "AggregateRating": ("ratingValue",), "Person": ("name",),
    "Brand": ("name",), "LocalBusiness": ("name", "address"),
    "HowTo": ("name", "step"), "HowToStep": ("text",),
    "BreadcrumbList": ("itemListElement",), "ListItem": ("position", "name"),
    "VideoObject": ("name",), "ImageObject": (),
    "PostalAddress": (), "ContactPoint": (), "WebPage": (),
}
TEXT_FIELDS = {"name", "headline", "description", "text", "articleBody"}
DATE_FIELDS = {"datePublished", "dateModified", "uploadDate", "foundingDate", "priceValidUntil"}
URL_FIELDS = {"url", "sameAs", "contentUrl", "embedUrl", "thumbnailUrl"}


class InputError(ValueError):
    pass


def pointer(path, key):
    return path + "/" + str(key).replace("~", "~0").replace("/", "~1")


def issue(code, path, message):
    return {"code": code, "path": path, "message": message}


def report_base():
    return {
        "profile": PROFILE,
        "local_valid": False,
        "errors": [], "warnings": [],
        "counts": {"typed_nodes": 0, "root_entities": 0},
        "content_check": {
            "status": "not_run", "checked_fields": 0, "matched_fields": 0,
            "checked_faq_pairs": 0, "matched_faq_pairs": 0,
            "scope": "Literal text and FAQ answer placement only; URLs, numbers, dates and factual truth require source review.",
        },
        "google_rich_results": {"status": "not_run"},
        "scope": "Local profile, not a full JSON-LD processor or Schema.org vocabulary validator.",
    }


def load_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InputError("Duplicate JSON key: " + key)
            result[key] = value
        return result

    def constant(value):
        raise InputError("Non-finite JSON number: " + value)

    def finite_float(value):
        parsed = float(value)
        if not math.isfinite(parsed):
            raise InputError("Non-finite JSON number: " + value)
        return parsed

    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"),
                          object_pairs_hook=pairs, parse_constant=constant,
                          parse_float=finite_float)
    except (OSError, ValueError, RecursionError) as exc:
        raise InputError(str(exc)) from exc


class PlainText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = []

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template"}:
            self.hidden.append(tag)
        if self.hidden:
            return
        if tag in {"p", "div", "br", "li", "ol", "ul"}:
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if self.hidden:
            if tag == self.hidden[-1]:
                self.hidden.pop()
            return
        if tag in {"p", "div", "li", "ol", "ul"}:
            self.parts.append(" ")


def normalized(text, html=False):
    if html:
        parser = PlainText()
        try:
            parser.feed(text)
            parser.close()
        except (AssertionError, NotImplementedError) as exc:
            raise InputError("Cannot parse HTML text: " + str(exc)) from exc
        text = "".join(parser.parts)
    return " ".join(unicodedata.normalize("NFKC", text).split())


def nonempty(value):
    return value is not None and value != "" and value != [] and value != {} and (
        not isinstance(value, str) or bool(value.strip()))


def number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return None
    if isinstance(value, str) and not re.fullmatch(r"[+-]?\d+(?:\.\d+)?", value):
        return None
    try:
        result = float(value)
    except (ValueError, OverflowError):
        return None
    return result if math.isfinite(result) else None


def absolute_url(value):
    if not isinstance(value, str) or re.search(r"\s", value):
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme in {"http", "https"} and bool(parts.hostname)
    except ValueError:
        return False


def schema_types(node):
    raw = node.get("@type", [])
    return [raw] if isinstance(raw, str) else [t for t in raw if isinstance(t, str)] if isinstance(raw, list) else []


def faq_question_occurrences(body, names, answers):
    """Bind each independent heading occurrence to its exact question name."""
    quotes = {"‘": "’", "“": "”", "'": "'", '"': '"', "「": "」", "『": "』"}
    answer_spans = [occurrence.span() for answer in set(answers) if answer
                    for occurrence in re.finditer(re.escape(answer), body)]
    occurrences = []

    def word(char):
        return char.isalnum() or char == "_"

    for name in set(names):
        for occurrence in re.finditer(re.escape(name), body):
            start, end = occurrence.span()
            # A short question inside a longer heading is not another heading,
            # including when that longer heading is absent from this draft.
            if ((start > 0 and word(body[start - 1]) and word(name[0]))
                    or (end < len(body) and word(name[-1]) and word(body[end]))):
                continue
            if (start > 0 and end < len(body) and quotes.get(body[start - 1]) == body[end]
                    and any(a <= start and end <= b for a, b in answer_spans)):
                continue
            occurrences.append((name, start, end))
    result = {}
    for name, start, end in occurrences:
        if any(a <= start and end <= b and (a < start or end < b)
               for other, a, b in occurrences if other != name):
            continue
        result.setdefault(name, []).append((start, end))
    return result


def validate(data, visible_text=None):
    result = report_base()
    errors, warnings = result["errors"], result["warnings"]
    definitions, references, text_values, faq_groups = {}, [], [], []
    breadcrumb_groups = []

    def error(code, path, message):
        errors.append(issue(code, path, message))

    def warning(code, path, message):
        warnings.append(issue(code, path, message))

    def resolve(node):
        if isinstance(node, dict) and set(node) == {"@id"}:
            return definitions.get(node["@id"], {}) if isinstance(node["@id"], str) else {}
        return node if isinstance(node, dict) else {}

    def expect_typed(value, allowed, path, allow_list=True):
        items = value if allow_list and isinstance(value, list) else [value]
        if not items:
            error("empty_relation", path, "Relation must contain an entity.")
        for index, item in enumerate(items):
            item_path = pointer(path, index) if isinstance(value, list) and allow_list else path
            if isinstance(item, dict) and set(item) == {"@id"}:
                references.append((item["@id"], item_path, allowed))
            elif not isinstance(item, dict) or not any(t in allowed for t in schema_types(item)):
                error("relation_type", item_path, "Expected: " + ", ".join(sorted(allowed)))

    def check_context(context, path):
        if context in (CONTEXT, CONTEXT + "/"):
            return True
        if context in ("http://schema.org", "http://schema.org/"):
            warning("http_context", path, "Prefer https://schema.org.")
            return True
        if isinstance(context, dict) and set(context) == {"@vocab"}:
            if context["@vocab"] == CONTEXT + "/":
                return True
            if context["@vocab"] == CONTEXT:
                error("unsupported_context", pointer(path, "@vocab"),
                      "@vocab must be https://schema.org/ with a trailing slash; terms are appended directly to this IRI.")
                return False
        error("unsupported_context", path, "This local profile requires schema.org context without aliases or remote extensions.")
        return False

    def type_rules(node, types, path):
        for entity_type in types:
            if entity_type not in REQUIRED:
                warning("type_not_covered", pointer(path, "@type"), "No field rules for " + entity_type)
                continue
            for field in REQUIRED[entity_type]:
                if field not in node or not nonempty(node[field]):
                    error("required_field", pointer(path, field), entity_type + " needs " + field + " in this local profile.")
        if ("Answer" in types and isinstance(node.get("text"), str)
                and node["text"].strip()
                and not any(char.isprintable() and not char.isspace()
                            for char in normalized(node["text"], html=True))):
            error("answer_text_empty", pointer(path, "text"),
                  "Answer needs visible text after HTML markup is removed.")
        if any(t in types for t in ("Article", "BlogPosting")):
            for field in ("author", "datePublished"):
                if field not in node:
                    warning("article_incomplete", pointer(path, field), "Unknown " + field + ": omitted; do not invent it.")
        if "FAQPage" in types and "mainEntity" in node:
            if not isinstance(node["mainEntity"], list) or not node["mainEntity"]:
                error("faq_items", pointer(path, "mainEntity"), "FAQPage mainEntity must be a nonempty array.")
            else:
                expect_typed(node["mainEntity"], {"Question"}, pointer(path, "mainEntity"))
                faq_groups.append((node["mainEntity"], pointer(path, "mainEntity")))
        if "Question" in types and "acceptedAnswer" in node:
            expect_typed(node["acceptedAnswer"], {"Answer"}, pointer(path, "acceptedAnswer"), False)
        for field, allowed in (("author", {"Person", "Organization"}),
                               ("publisher", {"Organization", "Person"}),
                               ("offers", {"Offer"}),
                               ("aggregateRating", {"AggregateRating"})):
            if field in node:
                expect_typed(node[field], allowed, pointer(path, field))
        if "Offer" in types:
            if "price" in node and (number(node["price"]) is None or number(node["price"]) < 0):
                error("price_number", pointer(path, "price"), "Price must be a finite nonnegative number without a currency symbol.")
            if "priceCurrency" in node and (not isinstance(node["priceCurrency"], str) or not re.fullmatch(r"[A-Z]{3}", node["priceCurrency"])):
                error("currency_format", pointer(path, "priceCurrency"), "Use a confirmed three-letter uppercase currency code; code membership is not checked.")
        if "AggregateRating" in types:
            rating = number(node.get("ratingValue"))
            low = number(node.get("worstRating", 1))
            high = number(node.get("bestRating", 5))
            if rating is None or low is None or high is None or low >= high or not low <= rating <= high:
                error("rating_range", path, "Rating must fit its scale (Schema.org default scale 1 to 5 if unspecified).")
            if not any(k in node for k in ("ratingCount", "reviewCount")):
                error("rating_count", path, "AggregateRating needs a confirmed ratingCount or reviewCount in this profile.")
            for field in ("ratingCount", "reviewCount"):
                if field in node:
                    count = number(node[field])
                    if count is None or count <= 0 or not count.is_integer():
                        error("rating_count", pointer(path, field), "Count must be a positive integer.")
        if "ImageObject" in types and not any(nonempty(node.get(k)) for k in ("url", "contentUrl")):
            error("image_location", path, "ImageObject needs url or contentUrl in this profile.")
        if "LocalBusiness" in types and "address" in node:
            if not isinstance(node["address"], str):
                expect_typed(node["address"], {"PostalAddress"}, pointer(path, "address"), False)
        if "HowTo" in types and "step" in node:
            expect_typed(node["step"], {"HowToStep"}, pointer(path, "step"))
        if "BreadcrumbList" in types and "itemListElement" in node:
            value = node["itemListElement"]
            if not isinstance(value, list) or not value:
                error("breadcrumb_items", pointer(path, "itemListElement"), "Use a nonempty ListItem array.")
            else:
                expect_typed(value, {"ListItem"}, pointer(path, "itemListElement"))
                breadcrumb_groups.append((value, pointer(path, "itemListElement")))
        if "ListItem" in types and "position" in node:
            if type(node["position"]) is not int or node["position"] < 1:
                error("position_integer", pointer(path, "position"), "Position must be a positive JSON integer.")

    def visit(node, path, context_ok=False, entity=False):
        if isinstance(node, list):
            if not node:
                error("empty_array", path, "Omit unknown values rather than inserting an empty array.")
            for index, child in enumerate(node):
                child_path = pointer(path, index)
                if not nonempty(child):
                    error("empty_value", child_path, "Omit unknown fields; required fields need source information.")
                if entity and not isinstance(child, dict):
                    error("entity_object", child_path, "Each root or @graph array item must be an entity object.")
                else:
                    visit(child, child_path, context_ok, entity)
            return
        if not isinstance(node, dict):
            if entity:
                error("entity_object", path, "Expected an entity object.")
            return
        if "@context" in node:
            context_ok = check_context(node["@context"], pointer(path, "@context"))
        if entity and not context_ok:
            error("missing_context", path, "Entity needs an inherited or explicit schema.org @context.")
        if entity and not any(k in node for k in ("@type", "@graph", "@id")):
            error("entity_identity", path, "Expected @type, @graph or @id.")
        identifier = node.get("@id")
        if "@id" in node:
            if not (isinstance(identifier, str) and (absolute_url(identifier) or (identifier.startswith("#") and len(identifier) > 1 and not re.search(r"\s", identifier)))):
                error("id_format", pointer(path, "@id"), "Use an absolute HTTP(S) URL or a nonempty #fragment.")
            elif set(node) == {"@id"}:
                references.append((identifier, path, None))
            elif identifier in definitions:
                error("duplicate_id", pointer(path, "@id"), "Define each @id once in this local profile; use @id-only references elsewhere.")
            else:
                definitions[identifier] = node
        if "@type" in node:
            types = schema_types(node)
            raw_type = node["@type"]
            if (not types or not all(t.strip() for t in types)
                    or (isinstance(raw_type, list) and len(types) != len(raw_type))):
                error("type_format", pointer(path, "@type"), "@type must be a nonempty string or an array of nonempty strings.")
            else:
                result["counts"]["typed_nodes"] += 1
                type_rules(node, types, path)
        for key, value in node.items():
            child_path = pointer(path, key)
            if key == "@context":
                continue
            if key == "@graph":
                if not isinstance(value, list) or not value:
                    error("graph_array", child_path, "@graph must be a nonempty array in this profile.")
                else:
                    visit(value, child_path, context_ok, True)
                continue
            if key.startswith("@"):
                if key not in {"@type", "@id"}:
                    error("unsupported_keyword", child_path, "Advanced JSON-LD keywords are outside this local profile.")
                continue
            if not nonempty(value):
                error("empty_value", child_path, "Omit unknown fields; required fields need source information.")
            if key in TEXT_FIELDS:
                if not isinstance(value, str):
                    error("text_value", child_path, "Expected nonempty text.")
                elif value.strip():
                    text_values.append((child_path, value, key == "text"))
            if key in DATE_FIELDS:
                try:
                    if not isinstance(value, str):
                        raise ValueError()
                    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
                        date.fromisoformat(value)
                    elif re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?", value):
                        datetime.fromisoformat(value.replace("Z", "+00:00"))
                    else:
                        raise ValueError()
                except ValueError:
                    error("date_format", child_path, "Use a confirmed calendar date YYYY-MM-DD or ISO datetime; never use today's date as a fallback.")
            if key in URL_FIELDS:
                values = value if isinstance(value, list) else [value]
                for index, url in enumerate(values):
                    url_path = pointer(child_path, index) if isinstance(value, list) else child_path
                    if not absolute_url(url):
                        error("url_format", url_path, "Expected an absolute HTTP(S) URL; reachability is not checked.")
            if isinstance(value, (dict, list)):
                visit(value, child_path, context_ok)

    if not isinstance(data, (dict, list)):
        error("root_shape", "", "JSON-LD root must be an object or a nonempty entity array.")
    else:
        roots = data if isinstance(data, list) else data.get("@graph", [data])
        result["counts"]["root_entities"] = len(roots) if isinstance(roots, list) else 0
        visit(data, "", entity=True)
    seen = set()
    for identifier, path, allowed in references:
        if not isinstance(identifier, str):
            continue
        key = (identifier, path, tuple(sorted(allowed or [])))
        if key in seen:
            continue
        seen.add(key)
        if identifier in definitions:
            if allowed and not any(t in allowed for t in schema_types(definitions[identifier])):
                error("reference_type", path, "Referenced entity has the wrong type for this relation.")
        elif identifier.startswith("#"):
            error("unresolved_local_reference", path, "No definition for " + identifier)
        else:
            warning("external_reference_unchecked", path, "External @id not present in this document; not fetched.")
    # Definitions may appear after their references, so order checks run after traversal.
    for items, path in breadcrumb_groups:
        positions = [resolve(item).get("position") for item in items]
        if positions != list(range(1, len(items) + 1)):
            error("breadcrumb_positions", path, "Positions must be integers ordered from 1 without gaps.")
    if visible_text is not None:
        body = normalized(visible_text)
        content = result["content_check"]
        content["status"] = "matched"
        if not body:
            error("visible_text_empty", "", "Visible-text input is empty.")
            content["status"] = "mismatch"
        for path, text, is_html in text_values:
            value = normalized(text, html=is_html)
            content["checked_fields"] += 1
            if value and value in body:
                content["matched_fields"] += 1
            else:
                error("content_not_found", path, "Text is absent from the supplied visible-text snapshot.")
                content["status"] = "mismatch"
        if not text_values and body:
            content["status"] = "no_text_fields"
        # One snapshot has one set of question boundaries, regardless of how
        # its marked FAQPage entities are split across an array or @graph.
        resolved_groups = [([resolve(q) for q in questions], group_path)
                           for questions, group_path in faq_groups]
        all_questions = [question for questions, _ in resolved_groups for question in questions]
        names = [normalized(q["name"]) for q in all_questions
                 if isinstance(q.get("name"), str) and q["name"].strip()]
        answers = [resolve(q.get("acceptedAnswer")).get("text") for q in all_questions]
        answers = [normalized(text, html=True) for text in answers if isinstance(text, str)]
        occurrences = faq_question_occurrences(body, names, answers)
        boundaries = sorted({start for spans in occurrences.values() for start, _ in spans})
        for questions, group_path in resolved_groups:
            for index, question in enumerate(questions):
                answer = resolve(question.get("acceptedAnswer"))
                if not isinstance(question.get("name"), str) or not isinstance(answer.get("text"), str):
                    continue
                name = normalized(question["name"])
                text = normalized(answer["text"], html=True)
                if not name or not text:
                    continue
                content["checked_faq_pairs"] += 1
                matched = False
                for _, start in occurrences.get(name, []):
                    end = next((b for b in boundaries if b >= start), len(body))
                    if body.find(text, start, end) >= 0:
                        matched = True
                        break
                if matched:
                    content["matched_faq_pairs"] += 1
                else:
                    error("faq_pair_mismatch", pointer(pointer(group_path, index), "acceptedAnswer"),
                          "Answer must follow its question before the next FAQ question in the supplied snapshot.")
                    content["status"] = "mismatch"
    result["local_valid"] = not errors
    return result


def add_context(data):
    """Only add a missing root context; never create factual property values."""
    result = copy.deepcopy(data)
    roots = result if isinstance(result, list) else [result]
    for node in roots:
        if isinstance(node, dict) and "@context" not in node:
            node["@context"] = CONTEXT
    return result


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def embed(data):
    serialized = json_text(data).rstrip()
    for literal, escaped in (("&", "\\u0026"), ("<", "\\u003c"), (">", "\\u003e"),
                             ("\u2028", "\\u2028"), ("\u2029", "\\u2029")):
        serialized = serialized.replace(literal, escaped)
    return '<script type="application/ld+json">\n' + serialized + '\n</script>\n'


def input_report(message):
    result = report_base()
    result["errors"].append(issue("input_error", "", message))
    return result


def read_and_check(path, visible_path=None, prepare=False):
    try:
        data = load_json(path)
        if prepare:
            data = add_context(data)
        visible = Path(visible_path).read_text(encoding="utf-8-sig") if visible_path else None
        return data, validate(data, visible)
    except (InputError, OSError, UnicodeError, RecursionError, OverflowError) as exc:
        return None, input_report(str(exc))


def empty_destination(path):
    target = Path(path)
    if target.exists() and (not target.is_dir() or any(target.iterdir())):
        raise InputError("Output directory must be new or empty; existing results are preserved.")
    target.mkdir(parents=True, exist_ok=True)
    return target


def write_result(target, data, report):
    (target / "校验结果.json").write_text(json_text(report), encoding="utf-8")
    if report["local_valid"]:
        (target / "schema.json").write_text(json_text(data), encoding="utf-8")
        (target / "嵌入片段.html").write_text(embed(data), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (("build", "Add missing root context, check, and create a deliverable directory."),
                            ("check", "Check an existing JSON-LD document without modifying it.")):
        command = commands.add_parser(name, help=help_text)
        command.add_argument("input", type=Path, help="UTF-8 JSON draft or JSON-LD document")
        command.add_argument("--visible-text", type=Path, help="Plain text snapshot for literal text matching")
        if name == "build":
            command.add_argument("--output-dir", type=Path, required=True, help="New or empty output directory")
        else:
            command.add_argument("--report", type=Path, help="Also save the JSON report to this file")
    batch = commands.add_parser("batch", help="Build each direct *.json file; use a same-stem .txt snapshot if present.")
    batch.add_argument("input_dir", type=Path)
    batch.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "batch":
            if not args.input_dir.is_dir():
                raise InputError("Batch input must be a directory.")
            inputs = sorted(args.input_dir.glob("*.json"))
            if not inputs:
                raise InputError("Batch input contains no direct *.json files.")
            target = empty_destination(args.output_dir)
            entries = []
            for source in inputs:
                visible = source.with_suffix(".txt")
                data, report = read_and_check(source, visible if visible.is_file() else None, True)
                subdir = target / source.stem
                subdir.mkdir()
                write_result(subdir, data, report)
                entries.append({"source": source.name, "local_valid": report["local_valid"],
                                "report": source.stem + "/校验结果.json"})
            passed = sum(entry["local_valid"] for entry in entries)
            summary = {"total": len(entries), "passed": passed, "failed": len(entries) - passed, "results": entries}
            (target / "summary.json").write_text(json_text(summary), encoding="utf-8")
            print(json_text(summary), end="")
            return 0 if passed == len(entries) else 1
        if args.command == "check" and args.report and args.report.resolve() in {
            args.input.resolve(), args.visible_text.resolve() if args.visible_text else None
        }:
            raise InputError("Report path must differ from all input files.")
        target = empty_destination(args.output_dir) if args.command == "build" else None
        data, report = read_and_check(args.input, args.visible_text, args.command == "build")
        if target:
            write_result(target, data, report)
        elif args.report:
            args.report.write_text(json_text(report), encoding="utf-8")
        print(json_text(report), end="")
        return 0 if report["local_valid"] else 1
    except (OSError, InputError, UnicodeError) as exc:
        print(json_text(input_report(str(exc))), end="")
        return 2


if __name__ == "__main__":
    sys.exit(main())
