#!/usr/bin/env python3
"""Run a bounded technical SEO audit using Dataify Web Unlocker."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.robotparser
import xml.etree.ElementTree as ET
import sys
from urllib.parse import urljoin, urlsplit

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dataify_client import content_from_response, normalize_url, parse_json, search, token_from_environment, unlock


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self._title = False
        self.meta = {}
        self.canonical = []
        self.h1 = 0
        self.json_ld = []
        self.hreflang = []
        self.links = []
        self._json_ld = False
        self._script = []

    def handle_starttag(self, tag, attrs):
        values = {key.lower(): value or "" for key, value in attrs}
        if tag.lower() == "title":
            self._title = True
        elif tag.lower() == "meta":
            key = (values.get("name") or values.get("property") or "").lower()
            if key:
                self.meta[key] = values.get("content", "")
        elif tag.lower() == "link" and "canonical" in values.get("rel", "").lower():
            self.canonical.append(values.get("href", ""))
        elif tag.lower() == "link" and "alternate" in values.get("rel", "").lower() and values.get("hreflang"):
            self.hreflang.append(values["hreflang"].lower())
        elif tag.lower() == "a" and values.get("href"):
            self.links.append(values["href"])
        elif tag.lower() == "h1":
            self.h1 += 1
        elif tag.lower() == "script" and values.get("type", "").lower() == "application/ld+json":
            self._json_ld = True
            self._script = []

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._title = False
        elif tag.lower() == "script" and self._json_ld:
            self.json_ld.append("".join(self._script).strip())
            self._json_ld = False

    def handle_data(self, data):
        if self._title:
            self.title += data
        if self._json_ld:
            self._script.append(data)


ISSUE_GUIDE = {
    "missing_title": ("on_page", "P0", "Search engines and users lack a reliable page label.", "Add one unique, descriptive title."),
    "title_length": ("on_page", "P2", "An extreme title length may truncate or dilute relevance.", "Rewrite the title for clarity and intent."),
    "missing_meta_description": ("on_page", "P1", "The page gives search engines no preferred result summary.", "Add a useful, page-specific meta description."),
    "description_length": ("on_page", "P2", "The description may truncate or communicate too little.", "Rewrite it as a concise result-page summary."),
    "missing_canonical": ("technical", "P1", "Duplicate URL variants may consolidate inconsistently.", "Add a self-referencing canonical when appropriate."),
    "missing_h1": ("on_page", "P1", "The main page topic is not expressed in a primary heading.", "Add one descriptive H1."),
    "multiple_h1": ("on_page", "P2", "Multiple primary headings can weaken document hierarchy.", "Use one primary H1 and subordinate headings."),
    "noindex": ("crawlability_indexation", "P0", "The page explicitly requests exclusion from search results.", "Remove noindex if the page should be indexed."),
    "malformed_json_ld": ("technical", "P1", "Invalid structured data cannot be interpreted reliably.", "Validate and correct the JSON-LD block."),
    "missing_open_graph": ("technical", "P2", "Shared links may have weak or inconsistent previews.", "Add at least og:title and og:description."),
    "robots_disallow_all": ("crawlability_indexation", "P0", "Robots rules block all compliant crawlers.", "Remove `Disallow: /` for user-agent * if public indexing is intended."),
}


def issue(code: str, severity: str, message: str, evidence: str = "") -> dict:
    layer, priority, impact, fix = ISSUE_GUIDE.get(code, ("technical", "P2", message, "Review and correct the affected signal."))
    return {"code": code, "severity": severity, "message": message, "layer": layer, "priority": priority, "impact": impact, "evidence": evidence or message, "fix": fix}


def audit_html(url: str, html: str) -> dict:
    parser = PageParser()
    parser.feed(html)
    issues = []
    title = parser.title.strip()
    description = parser.meta.get("description", "").strip()
    robots = parser.meta.get("robots", "").lower()
    open_graph = {key: value for key, value in parser.meta.items() if key.startswith("og:")}
    host = urlsplit(url).netloc
    internal_links = [urljoin(url, link) for link in parser.links if urlsplit(urljoin(url, link)).netloc == host]
    if not title:
        issues.append(issue("missing_title", "error", "Page has no non-empty title."))
    elif len(title) < 15 or len(title) > 65:
        issues.append(issue("title_length", "warning", "Title length is {} characters.".format(len(title))))
    if not description:
        issues.append(issue("missing_meta_description", "warning", "Page has no meta description."))
    elif len(description) < 50 or len(description) > 170:
        issues.append(issue("description_length", "info", "Description length is {} characters.".format(len(description))))
    if not parser.canonical or not parser.canonical[0]:
        issues.append(issue("missing_canonical", "warning", "Page has no canonical URL."))
    if parser.h1 == 0:
        issues.append(issue("missing_h1", "warning", "Page has no H1."))
    elif parser.h1 > 1:
        issues.append(issue("multiple_h1", "warning", "Page has {} H1 headings.".format(parser.h1)))
    if "noindex" in robots:
        issues.append(issue("noindex", "error", "Page declares noindex."))
    malformed = 0
    for value in parser.json_ld:
        try:
            json.loads(value)
        except json.JSONDecodeError:
            malformed += 1
    if malformed:
        issues.append(issue("malformed_json_ld", "warning", "{} JSON-LD blocks are malformed.".format(malformed)))
    if not open_graph:
        issues.append(issue("missing_open_graph", "info", "Page has no Open Graph metadata."))
    return {"url": url, "title": title, "description": description, "canonical": parser.canonical[:1], "h1_count": parser.h1, "json_ld_blocks": len(parser.json_ld), "hreflang": sorted(set(parser.hreflang)), "open_graph": open_graph, "internal_link_count": len(set(internal_links)), "issues": issues}


def sitemap_urls(base: str, text: str, limit: int) -> list[str]:
    host = urlsplit(base).netloc
    result = []
    for candidate in re.findall(r"<loc>\s*(https?://[^<]+)\s*</loc>", text, re.I):
        if urlsplit(candidate).netloc == host and candidate not in result:
            result.append(candidate)
        if len(result) >= limit:
            break
    return result


def discover_sitemap(base, text, token, geography, max_documents=5):
    pending=[text]
    seen=set()
    pages=[]
    errors=[]
    while pending:
        document=pending.pop(0)
        try:
            root=ET.fromstring(document)
        except ET.ParseError:
            errors.append('Invalid sitemap XML')
            continue
        urls=[node.text.strip() for node in root.iter() if node.tag.rsplit('}',1)[-1]=='loc' and node.text]
        if root.tag.rsplit('}',1)[-1]=='sitemapindex':
            for url in urls:
                if urlsplit(url).netloc != urlsplit(base).netloc or url in seen:
                    continue
                if len(seen)>=max_documents:
                    errors.append('Sitemap document limit reached')
                    break
                seen.add(url)
                reply=unlock(url,token,geography,clean_content=False)
                if reply['ok']:
                    pending.append(content_from_response(reply['body']))
                else:
                    errors.append('Sitemap fetch failed: '+url)
        elif root.tag.rsplit('}',1)[-1]=='urlset':
            pages.extend(url for url in urls if urlsplit(url).netloc==urlsplit(base).netloc)
        else:
            errors.append('Unsupported sitemap document')
    return list(dict.fromkeys(pages))[:500],errors


def stratified_sample(base: str, urls: list[str], limit: int) -> list[str]:
    """Sample across top-level path groups instead of taking sitemap prefix order."""
    selected = [base]
    groups: dict[str, list[str]] = {}
    for url in urls:
        if url == base:
            continue
        parts = [part for part in urlsplit(url).path.split("/") if part]
        group = parts[0].lower() if parts else "home"
        groups.setdefault(group, []).append(url)
    ordered = sorted(groups, key=lambda key: (key not in {"pricing", "docs", "products", "blog"}, key))
    while len(selected) < limit and ordered:
        progressed = False
        for group in ordered:
            if groups[group] and len(selected) < limit:
                selected.append(groups[group].pop(len(groups[group]) // 2))
                progressed = True
        if not progressed:
            break
    return selected[:limit]


def write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(args: argparse.Namespace) -> int:
    base = normalize_url(args.url)
    if not 1 <= args.max_pages <= 50:
        raise ValueError("--max-pages must be between 1 and 50")
    origin = "{}://{}".format(urlsplit(base).scheme, urlsplit(base).netloc)
    plan = {"url": base, "max_pages": args.max_pages, "robots": urljoin(origin, "/robots.txt"), "sitemap": urljoin(origin, "/sitemap.xml")}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write(args.output_dir / "plan.json", plan)
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    token = token_from_environment()
    support = {}
    for key in ("robots", "sitemap"):
        response = unlock(plan[key], token, args.geography, clean_content=False)
        support[key] = response
    pages = [base]
    sitemap_errors=[]
    if support["sitemap"]["ok"]:
        candidates,sitemap_errors = discover_sitemap(base, content_from_response(support['sitemap']['body']), token, args.geography)
        pages = stratified_sample(base, candidates, args.max_pages)
    audited = []
    failures = []
    raw_dir = args.output_dir / "evidence"
    raw_dir.mkdir(exist_ok=True)
    for index, url in enumerate(pages, 1):
        response = unlock(url, token, args.geography, clean_content=False)
        if not response["ok"]:
            failures.append({"url": url, "error": response["error"]})
            continue
        html = content_from_response(response["body"])
        (raw_dir / "page-{:02d}.html".format(index)).write_text(html, encoding="utf-8")
        audited.append(audit_html(url, html))
    summary = {"error": 0, "warning": 0, "info": 0}
    for page in audited:
        for item in page["issues"]:
            summary[item["severity"]] += 1
    robots_text = content_from_response(support["robots"]["body"]) if support["robots"]["ok"] else ""
    site_findings = []
    robots_parser = urllib.robotparser.RobotFileParser()
    robots_parser.parse(robots_text.splitlines())
    if robots_text.strip() and not robots_parser.can_fetch('*', base):
        site_findings.append(issue("robots_disallow_all", "error", "robots.txt blocks the entire site.", "User-agent: * / Disallow: /"))
        summary["error"] += 1
    serp_checks = []
    queries = ["site:{}".format(urlsplit(base).netloc)]
    queries.extend(item.strip() for item in args.keywords.split(",") if item.strip())
    for query in queries:
        response = search(query, token, args.geography)
        payload = parse_json(response["body"]) if response["ok"] else None
        organic = payload.get("organic", []) if isinstance(payload, dict) else []
        serp_checks.append({"query": query, "ok": response["ok"], "result_count": len(organic), "top_results": [{"position": item.get("position"), "title": item.get("title"), "link": item.get("link")} for item in organic[:10]], "error": response["error"]})
    report = {"status": "complete" if audited else "failed", "audited_at": datetime.now(timezone.utc).isoformat(), "site": base, "pages": audited, "site_findings": site_findings, "serp_checks": serp_checks, "failures": failures, "summary": summary, "support": {key: {"ok": value["ok"], "status": value["status"], "error": value["error"]} for key, value in support.items()}}
    write(args.output_dir / "report.json", report)
    report['sitemap_errors']=sitemap_errors
    incomplete = bool(sitemap_errors or failures or any(not value['ok'] for value in support.values()) or any(not value['ok'] for value in serp_checks))
    if audited and incomplete:
        report['status'] = 'partial'
    write(args.output_dir / 'report.json', report)
    lines = ["# SEO audit", "", "- Site: {}".format(base), "- Pages audited: {}".format(len(audited)), "- Errors: {}; warnings: {}; info: {}".format(summary["error"], summary["warning"], summary["info"]), "", "## Findings", ""]
    for page in audited:
        lines.append("### {}".format(page["url"]))
        lines.extend("- **{} / {}** `{}` — {} Impact: {} Evidence: {} Fix: {}".format(item["priority"], item["layer"], item["code"], item["message"], item["impact"], item["evidence"], item["fix"]) for item in page["issues"])
    lines.extend(['', '## Coverage and collection failures', '', 'Status: ' + report['status'], json.dumps({'failures':failures, 'support':report['support'], 'site_findings':site_findings, 'serp_checks':serp_checks}, ensure_ascii=False, indent=2)])
    (args.output_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "pages": len(audited), "summary": summary, "report": str(args.output_dir / "report.md")}, ensure_ascii=False))
    return 0 if report['status'] == 'complete' else 2


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--max-pages", type=int, default=5)
    parser.add_argument("--geography", default="us")
    parser.add_argument("--output-dir", type=Path, default=Path("seo-audit"))
    parser.add_argument("--keywords", default="", help="Optional comma-separated target keywords for live ranking evidence.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
