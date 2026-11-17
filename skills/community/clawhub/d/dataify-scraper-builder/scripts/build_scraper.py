#!/usr/bin/env python3
"""Inspect a target and generate a bounded Dataify Web Unlocker scraper starter."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dataify_client import content_from_response, normalize_url, token_from_environment, unlock


PREBUILT = {
    "amazon.": "dataify-amazon-product", "ebay.": "dataify-ebay-products",
    "walmart.": "dataify-walmart-products", "linkedin.com": "dataify-linkedin-company-information-by-url",
    "instagram.com": "dataify-instagram-profiles", "facebook.com": "dataify-facebook-post-by-url",
    "reddit.com": "dataify-reddit-posts", "youtube.com": "dataify-youtube-video-post",
    "youtu.be": "dataify-youtube-product-by-id", "tiktok.com": "dataify-tiktok-comment-by-url",
    "booking.com": "dataify-booking-hotellist", "airbnb.": "dataify-airbnb-product-by-searchurl",
    "indeed.": "dataify-indeed-job-listings", "glassdoor.": "dataify-glassdoor-company-by-url",
    "crunchbase.com": "dataify-crunchbase-company-by-url", "github.com": "dataify-github-repository-by-repo-url",
    "play.google.com": "dataify-google-play-store-reviews-by-url", "google.com/maps": "dataify-google-map-details",
}


class Profiler(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts = []
        self.json_ld = 0
        self.links = []
        self.forms = 0
        self.password_inputs = 0
        self.meta = {}

    def handle_starttag(self, tag, attrs):
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "script":
            source = values.get("src", "")
            if source:
                self.scripts.append(source)
            if values.get("type", "").lower() == "application/ld+json":
                self.json_ld += 1
        elif tag.lower() == "a":
            self.links.append({"href": values.get("href", ""), "rel": values.get("rel", "")})
        elif tag.lower() == "form":
            self.forms += 1
        elif tag.lower() == "input" and values.get("type", "").lower() == "password":
            self.password_inputs += 1
        elif tag.lower() == "meta":
            key = (values.get("name") or values.get("property") or "").lower()
            if key:
                self.meta[key] = values.get("content", "")


def prebuilt_for(url: str) -> str | None:
    parts = urlsplit(url)
    host = (parts.hostname or '').lower().removeprefix('www.')
    if host == 'linkedin.com' and not parts.path.startswith('/company/'):
        return None
    for marker, skill in PREBUILT.items():
        domain, _, path = marker.partition('/')
        matches = host == domain or host.endswith('.' + domain)
        if domain.endswith('.'):
            matches = bool(re.fullmatch(re.escape(domain) + r'[a-z]{2,3}(?:\.[a-z]{2})?', host))
        if matches and (not path or parts.path == '/' + path or parts.path.startswith('/' + path + '/')):
            return skill
    return None


def profile_html(url: str, html: str) -> dict:
    parser = Profiler()
    parser.feed(html)
    lower = html.lower()
    framework = next((name for name, markers in {
        "nextjs": ("__next_data__", "/_next/"), "nuxt": ("__nuxt__", "/_nuxt/"),
        "react": ("data-reactroot", "react-dom"), "vue": ("data-v-", "vue.js"),
        "angular": ("ng-version", "angular.js"),
    }.items() if any(marker in lower for marker in markers)), "unknown")
    pagination = any(
        "next" in item["rel"].lower() or re.search(r"(?:page|cursor|offset)=", item["href"], re.I)
        for item in parser.links
    ) or any(marker in lower for marker in ("load more", "infinite scroll", "下一页", "加载更多"))
    interaction = bool(parser.password_inputs or any(marker in lower for marker in ("captcha", "infinite scroll", "load more")))
    shell_only = len(re.sub(r"<[^>]+>", " ", html).strip()) < 120
    route = "browser_required" if interaction or (framework != "unknown" and shell_only) else "web_unlocker"
    return {
        "url": url, "host": urlsplit(url).netloc, "framework": framework,
        "script_count": len(parser.scripts), "json_ld": parser.json_ld > 0,
        "json_ld_blocks": parser.json_ld, "link_count": len(parser.links),
        "form_count": parser.forms, "pagination_signals": bool(pagination),
        "password_input_count": parser.password_inputs, "interaction_signals": interaction, "recommended_route": route,
    }


def validate_sample(records: list[dict], fields: list[str]) -> dict:
    total = len(records) * len(fields)
    present = sum(record.get(field) not in (None, "", [], {}) for record in records for field in fields)
    per_field = {
        field: round(sum(record.get(field) not in (None, "", [], {}) for record in records) / max(1, len(records)), 3)
        for field in fields
    }
    return {
        "record_count": len(records),
        "field_completeness": round(present / max(1, total), 3),
        "per_field": per_field,
        "incomplete_fields": [field for field, ratio in per_field.items() if ratio < 1.0],
        "accepted": bool(records) and present / max(1, total) >= 0.9,
    }


def common_sample(html: str, fields: list[str]) -> dict:
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    description = re.search(r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"']([^\"']*)", html, re.I)
    canonical = re.search(r"<link[^>]+rel=[\"'][^\"']*canonical[^\"']*[\"'][^>]+href=[\"']([^\"']*)", html, re.I)
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    known = {
        "title": re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else None,
        "description": description.group(1).strip() if description else None,
        "canonical": canonical.group(1).strip() if canonical else None,
        "h1": re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else None,
    }
    json_values = []
    for raw in re.findall(r"<script[^>]+type=[\"']application/ld\+json[\"'][^>]*>(.*?)</script>", html, re.I | re.S):
        try:
            json_values.append(json.loads(raw))
        except json.JSONDecodeError:
            continue

    def lookup(value, field):
        if isinstance(value, dict):
            for key, item in value.items():
                if key.lower().replace("_", "") == field.lower().replace("_", "") and not isinstance(item, (dict, list)):
                    return item
            for item in value.values():
                found = lookup(item, field)
                if found not in (None, ""):
                    return found
        elif isinstance(value, list):
            for item in value:
                found = lookup(item, field)
                if found not in (None, ""):
                    return found
        return None

    return {field: known.get(field) if known.get(field) not in (None, "") else next((value for tree in json_values if (value := lookup(tree, field)) not in (None, "")), None) for field in fields}


def generated_source(fields: list[str]) -> str:
    field_literal = repr(fields)
    return '''#!/usr/bin/env python3
"""Generated Dataify Web Unlocker scraper starter."""
import argparse, json, os, re, sys, urllib.error, urllib.request
from html.parser import HTMLParser

FIELDS = {fields}
ENDPOINT = "https://webunlocker.dataify.com/request"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.title = ""; self.in_title = False; self.meta = {{}}; self.canonical = ""; self.h1 = []; self.in_h1 = False; self.json_ld = []; self.in_json_ld = False; self.json_buffer = []
    def handle_starttag(self, tag, attrs):
        tag = tag.lower(); values = {{(key or "").lower(): value or "" for key, value in attrs}}
        if tag == "title": self.in_title = True
        if tag == "meta":
            key = (values.get("name") or values.get("property") or "").lower()
            if key: self.meta[key] = values.get("content", "")
        if tag == "link" and "canonical" in values.get("rel", "").lower(): self.canonical = values.get("href", "")
        if tag == "h1": self.in_h1 = True
        if tag == "script" and values.get("type", "").lower() == "application/ld+json": self.in_json_ld = True; self.json_buffer = []
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
        if tag == "h1": self.in_h1 = False
        if tag == "script" and self.in_json_ld:
            try: self.json_ld.append(json.loads("".join(self.json_buffer)))
            except json.JSONDecodeError: pass
            self.in_json_ld = False
    def handle_data(self, data):
        if self.in_title: self.title += data
        if self.in_h1: self.h1.append(data)
        if self.in_json_ld: self.json_buffer.append(data)

def lookup(value, field):
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower().replace("_", "") == field.lower().replace("_", "") and not isinstance(item, (dict, list)): return item
        for item in value.values():
            found = lookup(item, field)
            if found not in (None, ""): return found
    elif isinstance(value, list):
        for item in value:
            found = lookup(item, field)
            if found not in (None, ""): return found
    return None

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--url", required=True); args = ap.parse_args()
    token = os.environ.get("DATAIFY_API_TOKEN", "").strip()
    if not token: print("DATAIFY_API_TOKEN is not configured", file=sys.stderr); return 1
    payload = json.dumps({{"url": args.url, "type": "html", "js_render": "True", "clean_content": "false", "follow_redirect": "True", "isjson": "1"}}).encode("utf-8")
    request = urllib.request.Request(ENDPOINT, data=payload, headers={{"Authorization": "Bearer " + token, "Content-Type": "application/json"}}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response: body = response.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError) as exc: print("Request failed: " + str(exc), file=sys.stderr); return 2
    try:
        decoded = json.loads(body); html = decoded
        for _ in range(4):
            if isinstance(html, str): break
            if not isinstance(html, dict): break
            html = next((html[key] for key in ("content", "html", "body", "result", "data") if key in html), body)
        if not isinstance(html, str): html = json.dumps(html, ensure_ascii=False)
    except json.JSONDecodeError: html = body
    parser = Parser(); parser.feed(html)
    known = {{"title": parser.title.strip(), "description": parser.meta.get("description"), "canonical": parser.canonical or None, "h1": " ".join(parser.h1).strip() or None}}
    output = {{}}
    for field in FIELDS:
        output[field] = known.get(field)
        if output[field] in (None, ""):
            output[field] = next((value for tree in parser.json_ld if (value := lookup(tree, field)) not in (None, "")), None)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if output and all(value not in (None, "", [], {{}}) for value in output.values()) else 2

if __name__ == "__main__": raise SystemExit(main())
'''.format(fields=field_literal)


def write_json(path: Path, payload) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    if args.scope != 'single-page':
        raise ValueError('Only single-page generation is supported; listing/site traversal is not implemented.')
    url = normalize_url(args.url)
    fields = list(dict.fromkeys(item.strip() for item in args.fields.split(",") if item.strip()))
    if not fields:
        raise ValueError("--fields must contain at least one output field")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prebuilt = prebuilt_for(url)
    spec = {"target": url, "fields": fields, "scope": args.scope, "prebuilt_skill": prebuilt}
    if prebuilt and not args.force_custom:
        routed = {**spec, "status": "routed_to_prebuilt", "route": "prebuilt_skill"}
        write_json(args.output_dir / "scraper_spec.json", routed)
        print(json.dumps(routed, ensure_ascii=False, indent=2))
        return 0
    if args.dry_run:
        write_json(args.output_dir / "scraper_spec.json", spec)
        print(json.dumps(spec, ensure_ascii=False, indent=2))
        return 0
    token = token_from_environment()
    response = unlock(url, token, args.geography, clean_content=False)
    if not response["ok"]:
        write_json(args.output_dir / "scraper_spec.json", {**spec, "status": "failed", "error": response["error"]})
        print(response["error"]["message"], file=sys.stderr)
        return 2
    html = content_from_response(response["body"])
    (args.output_dir / "sample.html").write_text(html, encoding="utf-8")
    profile = profile_html(url, html)
    if prebuilt:
        profile["recommended_route"] = "prebuilt_skill"
    write_json(args.output_dir / "site_profile.json", profile)
    sample = common_sample(html, fields)
    validation = validate_sample([sample], fields)
    unsupported = [field for field in fields if field not in {"title", "description", "canonical", "h1"}]
    status = "ready" if validation["accepted"] else "needs_selector_refinement"
    write_json(args.output_dir / "sample_output.json", sample)
    write_json(args.output_dir / "validation.json", {**validation, "unsupported_fields": unsupported})
    write_json(args.output_dir / "scraper_spec.json", {**spec, "status": status, "route": profile["recommended_route"], "unsupported_fields": unsupported})
    generated = args.output_dir / "generated_scraper.py"
    generated.write_text(generated_source(fields), encoding="utf-8")
    result = {"status": status, "route": profile["recommended_route"], "prebuilt_skill": prebuilt, "profile": str(args.output_dir / "site_profile.json"), "validation": str(args.output_dir / "validation.json"), "scraper": str(generated)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--fields", required=True)
    parser.add_argument("--scope", choices=("single-page", "listing", "site"), default="single-page")
    parser.add_argument("--geography", default="us")
    parser.add_argument("--output-dir", type=Path, default=Path("generated-scraper"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-custom", action="store_true", help="Build anyway after reviewing the prebuilt Skill recommendation.")
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
