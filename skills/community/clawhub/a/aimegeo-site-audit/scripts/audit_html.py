#!/usr/bin/env python3
"""Read-only inventory of supplied HTML snapshots; no ranking or recommendation."""

import argparse
import csv
import hashlib
import json
import re
import sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlsplit

MAX_BYTES = 2 * 1024 * 1024
CSV_FIELDS = ["page_url", "state", "source_kind", "captured_at", "http_status", "reason", "sha256",
              "titles", "headings", "description", "canonicals", "robots", "noindex_directives",
              "links", "json_ld_error_count", "images", "images_without_alt", "evidence_ref"]
STATES = {"provided", "login_required", "fetch_failed", "not_run"}


def one_of(value, choices):
    return isinstance(value, str) and value in choices


def clean(value):
    return " ".join(value.split())


def absolute_url(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("page.url must be an absolute HTTP(S) URL")
    parts = urlsplit(value)
    if (parts.scheme not in {"http", "https"} or not parts.hostname
            or parts.username is not None or parts.password is not None
            or re.search(r"[\s\x00-\x1f]", value)):
        raise ValueError("page.url must be HTTP(S), without credentials or whitespace")
    _ = parts.port  # Validate malformed ports without contacting the host.
    return urldefrag(value)[0]


def bounded_read(path):
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("file exceeds 2 MiB")
    return data


def reject_json_constant(value):
    raise ValueError("JSON-LD contains non-standard constant " + value)


class EvidenceParser(HTMLParser):
    # Define these independently of the installed stdlib version: older parsers
    # only include script/style. RCDATA alone decodes character references.
    RAWTEXT_ELEMENTS = {"script", "style", "iframe", "xmp", "noembed", "noframes"}
    TEXT_ELEMENTS = {"title", "textarea"}
    LITERAL_ELEMENTS = RAWTEXT_ELEMENTS | TEXT_ELEMENTS | {"plaintext"}
    CDATA_CONTENT_ELEMENTS = tuple(sorted(LITERAL_ELEMENTS))

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.titles, self.headings, self.text = [], [], []
        self.metas, self.canonicals, self.links, self.jsonld = [], [], [], []
        self.base = None
        self.images = self.missing_alt = 0
        self.password = False
        self.title_parts = None
        self.heading = None
        self.excluded = []
        self.script_parts = None
        self.foreign = []

    def set_cdata_mode(self, elem, **options):
        if elem == "title" and self.foreign:
            return
        # Decode RCDATA ourselves, keeping RAWTEXT/plaintext literally unchanged.
        super().set_cdata_mode(elem)
        if elem == "plaintext":
            # Unlike RAWTEXT, even </plaintext> cannot end plaintext mode.
            self.interesting = re.compile(r"(?!)")
        elif elem in self.LITERAL_ELEMENTS:
            self.interesting = re.compile(r"</%s(?=[\t\n\r\f />])" % re.escape(elem),
                                          re.IGNORECASE | re.ASCII)

    def parse_endtag(self, index):
        if (self.cdata_elem in self.LITERAL_ELEMENTS - {"plaintext"}
                and self.rawdata.find(">", index + 2) >= 0):
            # Older CDATA parsing rejects matching end tags with attributes or a
            # trailing slash. Parse them as ordinary end tags once complete.
            self.clear_cdata_mode()
        return super().parse_endtag(index)

    def handle_starttag(self, tag, attrs):
        a = {key: value or "" for key, value in attrs}
        if self.excluded:
            if tag in {"script", "style", "template", "noscript"}:
                self.excluded.append(tag)
            return
        if tag in {"script", "style", "template", "noscript"}:
            self.excluded.append(tag)
            if tag == "script" and a.get("type", "").lower().strip() == "application/ld+json":
                self.script_parts = []
            return
        if tag in {"svg", "math"}:
            self.foreign.append(tag)
        if tag == "title" and not self.foreign:
            self.title_parts = []
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.heading = (tag, [])
        if tag == "meta":
            self.metas.append({"name": a.get("name", "").lower(),
                               "content": a.get("content", "")})
        if tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        if tag == "base" and self.base is None:
            self.base = a.get("href", "")
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images += 1
            self.missing_alt += int("alt" not in a)
        if tag == "input" and a.get("type", "").lower() == "password":
            self.password = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in self.LITERAL_ELEMENTS:
            # These are non-void HTML elements: a trailing slash cannot close them.
            self.set_cdata_mode(tag)
            return
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in self.foreign:
            index = len(self.foreign) - 1 - self.foreign[::-1].index(tag)
            del self.foreign[index:]
        if self.excluded:
            if tag == self.excluded[-1]:
                self.excluded.pop()
                if not self.excluded and self.script_parts is not None:
                    self.jsonld.append("".join(self.script_parts))
                    self.script_parts = None
            return
        if tag == "title" and not self.foreign and self.title_parts is not None:
            self.titles.append(clean(" ".join(self.title_parts)))
            self.title_parts = None
        if self.heading and tag == self.heading[0]:
            self.headings.append({"tag": tag, "text": clean(" ".join(self.heading[1]))})
            self.heading = None

    def handle_data(self, data):
        if self.cdata_elem in self.TEXT_ELEMENTS:
            data = unescape(data)
        if self.excluded:
            if self.script_parts is not None:
                self.script_parts.append(data)
            return
        if self.title_parts is not None:
            self.title_parts.append(data)
            return
        if self.heading:
            self.heading[1].append(data)
        if data.strip():
            self.text.append(data)

    def close(self):
        super().close()
        # Older parsers retain unterminated literal-element contents at EOF.
        if self.cdata_elem in self.LITERAL_ELEMENTS and self.rawdata:
            self.handle_data(self.rawdata)
            self.rawdata = ""


def extract(html, url):
    parser = EvidenceParser()
    parser.feed(html)
    parser.close()
    jsonld, errors = [], []
    for index, raw in enumerate(parser.jsonld):
        try:
            value = json.loads(raw, parse_constant=reject_json_constant)
            if not isinstance(value, (dict, list)):
                raise ValueError("JSON-LD root must be an object or array")
            # A numeric literal such as 1e999 can also overflow to infinity.
            json.dumps(value, allow_nan=False)
            jsonld.append(value)
        except (ValueError, RecursionError) as exc:
            errors.append({"block": index + 1, "reason": str(exc)})
    url_errors = []
    try:
        base = urljoin(url, parser.base or "")
    except ValueError:
        url_errors.append({"field": "base", "value": parser.base, "reason": "invalid_url"})
        base = url
    canonicals = []
    for index, href in enumerate(parser.canonicals):
        try:
            canonicals.append(urljoin(base, href) if href else "")
        except ValueError:
            # Preserve the malformed field as evidence; do not lose the page.
            canonicals.append(href)
            url_errors.append({"field": "canonical", "index": index,
                               "value": href, "reason": "invalid_url"})
    links = []
    for href in parser.links:
        try:
            resolved = absolute_url(urljoin(base, href))
        except ValueError:
            continue
        if resolved not in links:
            links.append(resolved)
    text = clean(" ".join(parser.text))
    robots = [m for m in parser.metas if m["name"] in {"robots", "googlebot", "bingbot"}]
    noindex = [m for m in robots if {"noindex", "none"} & set(
        re.split(r"[\s,;]+", re.sub(r"\s*:\s*", ":", m["content"].lower())))]
    return {
        "titles": parser.titles,
        "description": [m["content"] for m in parser.metas if m["name"] == "description"],
        "headings": parser.headings,
        "robots": robots, "noindex_directives": noindex,
        "canonicals": canonicals,
        "links": links, "images": parser.images, "images_without_alt": parser.missing_alt,
        "json_ld": jsonld, "json_ld_errors": errors,
        "password_input": parser.password,
        "text_excerpt": text[:12000], "text_truncated": len(text) > 12000,
        **({"url_errors": url_errors} if url_errors else {}),
    }


def load_input(path):
    data = json.loads(bounded_read(path).decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    allowed = {"schema_version", "dataset_kind", "pages"}
    if set(data) - allowed:
        raise ValueError("unknown input fields: " + ", ".join(sorted(set(data) - allowed)))
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    if not one_of(data.get("dataset_kind"), {"user_provided", "synthetic_fixture"}):
        raise ValueError("dataset_kind must be user_provided or synthetic_fixture")
    pages = data.get("pages")
    if not isinstance(pages, list) or not 1 <= len(pages) <= 1000:
        raise ValueError("pages must contain 1..1000 entries")
    fields = {"url", "html", "state", "http_status", "reason", "source_kind",
              "captured_at"}
    for index, page in enumerate(pages):
        if not isinstance(page, dict) or set(page) - fields:
            raise ValueError(f"pages[{index}] has invalid or unknown fields")
        absolute_url(page.get("url"))
        state = page.get("state", "provided")
        if not one_of(state, STATES):
            raise ValueError(f"pages[{index}].state is invalid")
        if not one_of(page.get("source_kind", "saved_html"), {"saved_html", "rendered_dom"}):
            raise ValueError(f"pages[{index}].source_kind is invalid")
        status = page.get("http_status")
        if status is not None and (type(status) is not int or not 100 <= status <= 599):
            raise ValueError(f"pages[{index}].http_status must be an integer 100..599")
        for key in {"html", "reason", "captured_at"} & set(page):
            if not isinstance(page[key], str) or not page[key].strip():
                raise ValueError(f"pages[{index}].{key} must be a nonempty string")
        if state != "provided" and not page.get("reason"):
            raise ValueError(f"pages[{index}] requires a reason for {state}")
        # Reject unsafe file references before processing any page, even beyond the cap.
        if "html" in page:
            relative = Path(page["html"])
            resolved = (path.parent / relative).resolve()
            if relative.is_absolute() or not resolved.is_relative_to(path.parent.resolve()):
                raise ValueError(f"pages[{index}].html must stay inside the input directory")
            if relative.suffix.lower() not in {".html", ".htm"}:
                raise ValueError(f"pages[{index}].html must be an HTML file")
        if (state == "provided" and (status is None or 200 <= status < 300)
                and "html" not in page):
            raise ValueError(f"pages[{index}] requires html for a provided page")
    return data


def audit(path, max_pages=5):
    """Build a bounded inventory of supplied HTML snapshots; make no recommendations."""
    if type(max_pages) is not int or not 1 <= max_pages <= 20:
        raise ValueError("max_pages must be 1..20")
    data = load_input(path)
    pages, seen = [], set()
    attempted = 0
    for index, item in enumerate(data["pages"]):
        page = {"url": item["url"], "http_status": item.get("http_status"),
                "source_kind": item.get("source_kind", "saved_html"),
                "captured_at": item.get("captured_at"), "state": "not_verified",
                "reason_code": None, "reason": None}
        pages.append(page)
        normalized = absolute_url(item["url"])
        if normalized in seen:
            page.update(state="skipped", reason_code="duplicate_url", reason="Duplicate URL; not read twice")
            continue
        seen.add(normalized)
        if attempted >= max_pages:
            page.update(state="skipped", reason_code="page_cap", reason=f"Reached {max_pages}-page limit")
            continue
        attempted += 1
        state = item.get("state", "provided")
        if state != "provided":
            page.update(reason_code=state, reason=item["reason"])
            continue
        status = item.get("http_status")
        if status is not None and not 200 <= status < 300:
            page.update(reason_code=f"http_{status}", reason=f"Input reports HTTP {status}; page content not verified")
            continue
        try:
            raw = bounded_read(path.parent / item["html"])
            signals = extract(raw.decode("utf-8-sig"), normalized)
        except (OSError, ValueError, RecursionError) as exc:
            detail = str(exc) if isinstance(exc, (ValueError, UnicodeError)) else type(exc).__name__
            page.update(reason_code="html_unreadable", reason=f"Could not read {item['html']} ({detail})")
            continue
        page.update(state="observed", html=item["html"], sha256=hashlib.sha256(raw).hexdigest(), signals=signals)
    observed = sum(p["state"] == "observed" for p in pages)
    skipped = sum(p["state"] == "skipped" for p in pages)
    return {
        "schema_version": 1, "dataset_kind": data["dataset_kind"],
        "status": "empty" if not observed else "complete" if observed == len(pages) else "partial",
        "summary": {"input_pages": len(pages), "max_pages": max_pages, "attempted_pages": attempted,
                    "observed_pages": observed, "not_verified_pages": len(pages) - observed - skipped,
                    "skipped_pages": skipped},
        "limitations": ["Only supplied HTML is parsed; no network requests or page scripts are executed",
                        "HTTP status and capture time come from the input record",
                        "No ranking, indexation, speed, off-site or AI response measurement is performed",
                        "A static snapshot does not describe rendered pages or the full site"],
        "pages": pages,
    }


def csv_rows(result):
    rows = []
    for index, page in enumerate(result["pages"]):
        signals = page.get("signals", {})
        rows.append({
            "page_url": page["url"], "state": page["state"], "source_kind": page.get("source_kind"),
            "captured_at": page.get("captured_at"), "http_status": page.get("http_status"),
            "reason": page.get("reason"), "sha256": page.get("sha256"),
            "titles": json.dumps(signals.get("titles", []), ensure_ascii=False),
            "headings": json.dumps(signals.get("headings", []), ensure_ascii=False),
            "description": json.dumps(signals.get("description", []), ensure_ascii=False),
            "canonicals": json.dumps(signals.get("canonicals", []), ensure_ascii=False),
            "robots": json.dumps(signals.get("robots", []), ensure_ascii=False),
            "noindex_directives": json.dumps(signals.get("noindex_directives", []), ensure_ascii=False),
            "links": json.dumps(signals.get("links", []), ensure_ascii=False),
            "json_ld_error_count": len(signals.get("json_ld_errors", [])),
            "images": signals.get("images"), "images_without_alt": signals.get("images_without_alt"),
            "evidence_ref": f"/pages/{index}/signals" if signals else f"/pages/{index}/reason",
        })
    return rows


def write_outputs(result, output):
    names = ["observations.json", "页面观察.csv"]
    if any((output / name).exists() for name in names):
        raise ValueError("output files already exist; choose a new --out directory")
    output.mkdir(parents=True, exist_ok=True)
    (output / names[0]).write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    with (output / names[1]).open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows({k: spreadsheet_safe(row[k]) for k in CSV_FIELDS} for row in csv_rows(result))


def spreadsheet_safe(value):
    text = str(value)
    return "'" + text if text.lstrip().startswith(("=", "+", "-", "@")) else text



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON input; HTML paths resolve relative to this file")
    parser.add_argument("--out", type=Path, required=True, help="directory for observation JSON and CSV")
    parser.add_argument("--max-pages", type=int, default=5, help="page attempts, 1..20 (default: 5)")
    args = parser.parse_args()
    try:
        result = audit(args.input.resolve(), args.max_pages)
        write_outputs(result, args.out)
    except (OSError, ValueError, RecursionError) as exc:
        text = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        print(json.dumps({"status": "invalid_input", "error": text}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps({"status": result["status"], **result["summary"]}, ensure_ascii=False))
    return 2 if result["status"] == "empty" else 0


if __name__ == "__main__":
    sys.exit(main())
