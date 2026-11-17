#!/usr/bin/env python3
"""Plan, run, and resume a bounded Dataify competitive-intelligence evidence collection."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from research_outputs import build_report, normalize
from analyze_evidence import build_worksheet


SKILL_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_DIR.parents[1]
SEARCH_SCRIPT = REPO_ROOT / "skills" / "serp-google-search" / "scripts" / "google_search.py"
UNLOCKER_SCRIPT = REPO_ROOT / "skills" / "dataify-web-unlocker" / "scripts" / "invoke-dataify-web-unlocker.py"
MODES = {"quick": 5, "standard": 12, "deep": 20}
MODULES = ("snapshot", "product", "pricing", "reviews", "hiring", "landscape", "battlecard")
PLATFORM_ROUTES = (
    ("github.com", "scraper-github-repository-by-repo-url", "github_repository_by-repo-url"),
    ("crunchbase.com", "scraper-crunchbase-company-by-url", "crunchbase_company_by-url"),
    ("linkedin.com/company", "scraper-linkedin-company-information-by-url", "linkedin_company_information_by-url"),
    ("glassdoor.com", "scraper-glassdoor-company-by-url", "glassdoor_company_by-url"),
    ("play.google.com", "scraper-google-play-store-reviews-by-url", "google-play-store_reviews_by-url"),
)
TOOL_URL_PARAMETERS = {
    "github_repository_by-repo-url": "repo_url",
}


def slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-").lower()
    return cleaned or "entity"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--company", help="Company or product being analyzed.")
    result.add_argument("--company-domain", help="Verified official domain for the company.")
    result.add_argument("--competitor", action="append", default=[], help="Competitor; repeat as needed.")
    result.add_argument("--competitor-domain", action="append", default=[], metavar="NAME=DOMAIN", help="Verified competitor domain; repeat as needed.")
    result.add_argument("--decision", default="Identify evidence-backed competitive priorities.")
    result.add_argument("--audience", default="Product and engineering team")
    result.add_argument("--module", action="append", choices=MODULES, default=[])
    result.add_argument("--geography", default="US")
    result.add_argument("--freshness", default="12 months")
    result.add_argument("--mode", choices=tuple(MODES), default="quick")
    result.add_argument("--max-actions", type=int, help="Hard collection-action limit.")
    result.add_argument("--output-dir", type=Path, default=Path("competitive-intelligence-run"))
    result.add_argument("--resume", type=Path, help="Resume an existing state.json without resubmitting successes.")
    result.add_argument("--retry-failed-safe", action="store_true", help="Retry failed discovery/page actions; never retries scraper submissions.")
    result.add_argument("--dry-run", action="store_true", help="Print and save the plan without API calls.")
    result.add_argument("--checkpoint", action="store_true", help="Stop after the first successful action.")
    result.add_argument("--autopilot", action="store_true", help="Continue through the bounded plan without a checkpoint.")
    result.add_argument("--concurrency", type=int, default=4, help="Maximum independent actions to run concurrently.")
    return result


def queries(company: str, competitors: list[str], modules: list[str], geography: str, freshness: str, domains: dict[str, str] | None = None) -> list[dict[str, Any]]:
    entities = [company, *competitors]
    actions: list[dict[str, Any]] = []
    seen: set[str] = set()
    domains = domains or {}

    def add(entity: str, module: str, query: str) -> None:
        if domains.get(entity):
            query = f'site:{domains[entity]} {query}'
        key = query.casefold()
        if key in seen:
            return
        seen.add(key)
        actions.append({
            "id": f"a{len(actions) + 1:02d}",
            "entity": entity,
            "module": module,
            "type": "discover",
            "capability": "dataify-google-search",
            "query": query,
            "url": None,
            "depends_on": [],
            "status": "pending",
            "output": None,
            "error": None,
            "attempts": 0,
        })

    for module in modules:
        for entity in entities:
            if module == "snapshot":
                subject = "" if domains.get(entity) else f"{entity} "
                add(entity, "snapshot", f"{subject}official website products positioning {geography}")
            elif module == "product":
                add(entity, "product", f'{entity} official product documentation API features')
            elif module == "pricing":
                add(entity, "pricing", f'{entity} official pricing billing usage limits')
            elif module == "reviews":
                add(entity, "reviews", f'{entity} customer reviews complaints alternatives {freshness}')
            elif module == "hiring":
                add(entity, "hiring", f'{entity} careers jobs hiring {geography} {freshness}')
            elif module == "battlecard":
                add(entity, "battlecard", f'{entity} official case studies customers product comparison')
        if module == "landscape":
            names = " ".join(entities)
            add(company, "landscape", f'{company} competitors alternatives market landscape {names} {geography}')
    return actions


def save(state_path: Path, state: dict[str, Any]) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def canonical_url(value: str) -> str | None:
    try:
        parts = urlsplit(value.strip())
    except ValueError:
        return None
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        return None
    if not re.fullmatch(r"[A-Za-z0-9.-]+(?::\d+)?", parts.netloc):
        return None
    path = parts.path.rstrip("/") or "/"
    query = urlencode([
        (key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in {"fbclid", "gclid"}
    ])
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ""))


def extract_urls(payload: str) -> list[str]:
    values: list[str] = []
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        parsed = payload

    def visit(item: Any) -> None:
        if isinstance(item, dict):
            for value in item.values():
                visit(value)
        elif isinstance(item, list):
            for value in item:
                visit(value)
        elif isinstance(item, str):
            for candidate in re.findall(r"https?://[^\s\"'<>]+", item):
                normalized = canonical_url(candidate.rstrip(".,);]"))
                if normalized and normalized not in values:
                    values.append(normalized)

    visit(parsed)
    return values


def classify_url(url: str) -> tuple[str, str, str | None]:
    lowered = url.lower()
    for marker, folder, tool_sign in PLATFORM_ROUTES:
        if marker in lowered:
            return "scrape", folder, tool_sign
    if "amazon." in lowered and "/dp/" in lowered:
        return "scrape", "scraper-amazon-comment", None
    if "google." in lowered and "/maps" in lowered:
        return "scrape", "scraper-google-maps-reviews", None
    if "indeed." in lowered and ("/viewjob" in lowered or "jk=" in lowered):
        return "scrape", "scraper-indeed-job-listings", None
    return "fetch", "dataify-web-unlocker", None


def rank_urls(urls: list[str], parent: dict[str, Any]) -> list[str]:
    entity_tokens = [token for token in re.split(r"\W+", parent["entity"].lower()) if len(token) > 2]
    module_tokens = {
        "pricing": ("pricing", "plans", "billing"),
        "product": ("product", "docs", "api", "features"),
        "reviews": ("review", "g2", "capterra", "reddit"),
        "hiring": ("career", "jobs", "indeed", "glassdoor", "linkedin"),
        "snapshot": ("about", "company", "product"),
        "battlecard": ("customers", "case-studies", "compare"),
        "landscape": ("alternatives", "competitors", "market"),
    }.get(parent["module"], ())

    def score(url: str) -> tuple[int, str]:
        lowered = url.lower()
        host = urlsplit(url).netloc
        if ("google." in host or "googleusercontent." in host) and "/maps" not in lowered:
            return (-100, url)
        if parent["module"] != "landscape" and entity_tokens and not any(token in lowered for token in entity_tokens):
            return (-50, url)
        value = sum(5 for token in entity_tokens if token in host)
        value += sum(3 for token in module_tokens if token in lowered)
        value += 2 if any(marker in lowered for marker, _, _ in PLATFORM_ROUTES) else 0
        return (value, url)

    return [url for url in sorted(urls, key=score, reverse=True) if score(url)[0] >= 0]


def expand_discovered_actions(state: dict[str, Any], parent: dict[str, Any], payload: str) -> None:
    existing = {action.get("url") for action in state["actions"] if action.get("url")}
    remaining = max(0, int(state["max_actions"]) - len(state["actions"]))
    expanded_parents = {dependency for action in state["actions"] for dependency in action.get("depends_on", [])}
    parents_left = sum(
        1 for action in state["actions"]
        if action.get("type", "discover") == "discover" and action["id"] not in expanded_parents
    )
    allowance = min(remaining, max(1, (remaining + max(parents_left, 1) - 1) // max(parents_left, 1)))
    for url in rank_urls(extract_urls(payload), parent)[:allowance]:
        if url in existing:
            continue
        action_type, capability, tool_sign = classify_url(url)
        state["actions"].append({
            "id": f'a{len(state["actions"]) + 1:02d}',
            "entity": parent["entity"],
            "module": parent["module"],
            "type": action_type,
            "capability": capability,
            "query": None,
            "url": url,
            "tool_sign": tool_sign,
            "depends_on": [parent["id"]],
            "status": "pending",
            "output": None,
            "error": None,
            "attempts": 0,
        })
        existing.add(url)
        remaining -= 1
        if remaining <= 0:
            break


def command_for(action: dict[str, Any]) -> list[str]:
    action_type = action.get("type", "discover")
    if action_type == "discover":
        return [sys.executable, str(SEARCH_SCRIPT), "--q", action["query"], "--json", "1"]
    if action_type == "fetch":
        return [sys.executable, str(UNLOCKER_SCRIPT), "--url", action["url"], "--clean-content", "true"]
    folder = action["capability"]
    scripts = sorted((REPO_ROOT / "skills" / folder / "scripts").glob("*.py"))
    scripts = [path for path in scripts if "preview" not in path.name]
    if not scripts:
        raise FileNotFoundError(f"No executable script for {folder}")
    script = scripts[0]
    if action.get("tool_sign"):
        parameter = TOOL_URL_PARAMETERS.get(action["tool_sign"], "url")
        return [sys.executable, str(script), "--tool-sign", action["tool_sign"], "--params-json", json.dumps({parameter: action["url"]})]
    argument = "--job-url" if folder == "scraper-indeed-job-listings" else "--url"
    return [sys.executable, str(script), argument, action["url"]]


def direct_request(action: dict[str, Any], token: str) -> subprocess.CompletedProcess[str]:
    """Run discovery and page-fetch actions when atomic skill scripts are absent."""
    try:
        if action.get("type", "discover") == "discover":
            body = urllib.parse.urlencode({"engine": "google", "q": action["query"], "json": "1"}).encode("utf-8")
            request = urllib.request.Request(
                "https://scraperapi.dataify.com/request",
                data=body,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
        elif action.get("type") == "fetch":
            body = json.dumps({
                "url": action["url"], "type": "html", "js_render": "True",
                "clean_content": "true", "country": "us", "follow_redirect": "True", "isjson": "1",
            }).encode("utf-8")
            request = urllib.request.Request(
                "https://webunlocker.dataify.com/request",
                data=body,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                method="POST",
            )
        else:
            return subprocess.CompletedProcess([], 1, stdout="", stderr="Atomic scraper script is required for this action")
        with urllib.request.urlopen(request, timeout=120) as response:
            output = response.read().decode("utf-8", errors="replace")
            return subprocess.CompletedProcess([], 0, stdout=output, stderr="")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return subprocess.CompletedProcess([], 1, stdout="", stderr=detail or f"HTTP {exc.code}")
    except urllib.error.URLError as exc:
        return subprocess.CompletedProcess([], 1, stdout="", stderr=f"Request failed: {exc.reason}")


def execute_action(action: dict[str, Any], token: str) -> subprocess.CompletedProcess[str]:
    action_type = action.get("type", "discover")
    required = SEARCH_SCRIPT if action_type == "discover" else UNLOCKER_SCRIPT if action_type == "fetch" else None
    if required is not None and not required.exists():
        return direct_request(action, token)
    command = command_for(action)
    return subprocess.run(
        command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False
    )


def load_or_plan(args: argparse.Namespace) -> tuple[Path, dict[str, Any]]:
    if args.resume:
        state_path = args.resume if args.resume.name == "state.json" else args.resume / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if args.retry_failed_safe:
            for action in state.get("actions", []):
                if action.get("status") == "failed" and action.get("type", "discover") in {"discover", "fetch"}:
                    action.update(status="pending", attempts=0, error=None)
            save(state_path, state)
        return state_path, state
    if not args.company or not args.competitor:
        raise ValueError("--company and at least one --competitor are required unless --resume is used")
    clean_domain = lambda value: value.strip().lower().removeprefix("https://").removeprefix("http://").strip("/")
    domains = {args.company: clean_domain(args.company_domain)} if args.company_domain else {}
    for item in args.competitor_domain:
        if "=" not in item:
            raise ValueError("--competitor-domain must use NAME=DOMAIN")
        name, domain = item.split("=", 1)
        if name.strip() not in args.competitor:
            raise ValueError(f"competitor domain name is not present in --competitor: {name.strip()}")
        domains[name.strip()] = clean_domain(domain)
    modules = list(dict.fromkeys(args.module or ["snapshot", "product", "pricing"]))
    limit = args.max_actions if args.max_actions is not None else MODES[args.mode]
    if limit < 1:
        raise ValueError("--max-actions must be at least 1")
    planned = queries(args.company, args.competitor, modules, args.geography, args.freshness, domains)
    state = {
        "version": 1,
        "company": args.company,
        "competitors": args.competitor,
        "decision": args.decision,
        "audience": args.audience,
        "domains": domains,
        "modules": modules,
        "geography": args.geography,
        "freshness": args.freshness,
        "mode": args.mode,
        "max_actions": limit,
        "actions": planned[:max(1, min(len(planned), limit // 2))],
    }
    state_path = args.output_dir / "state.json"
    save(state_path, state)
    return state_path, state


def write_report(state_path: Path, state: dict[str, Any]) -> Path:
    completed = [action for action in state["actions"] if action["status"] == "success"]
    failed = [action for action in state["actions"] if action["status"] == "failed"]
    lines = [
        "# Competitive intelligence evidence package",
        "",
        f'- Company: {state["company"]}',
        f'- Competitors: {", ".join(state["competitors"])}',
        f'- Modules: {", ".join(state["modules"])}',
        f'- Geography: {state["geography"]}',
        f'- Freshness: {state["freshness"]}',
        f'- Collection: {len(completed)} succeeded, {len(failed)} failed, {len(state["actions"])} planned',
        "",
        "## Evidence index",
        "",
        "| Entity | Module | Capability | Source/query | Status | Raw evidence |",
        "|---|---|---|---|---|---|",
    ]
    for action in state["actions"]:
        output = action.get("output") or "—"
        target = action.get("url") or action.get("query") or "—"
        lines.append(f'| {action["entity"]} | {action["module"]} | {action.get("capability", "—")} | {target} | {action["status"]} | {output} |')
    lines.extend([
        "",
        "## Synthesis status",
        "",
        "This file is an evidence package, not a completed competitive conclusion. The agent must inspect the raw evidence, cite material claims, label inference and confidence, disclose failures, and then produce the requested comparison and recommendations.",
    ])
    report = state_path.parent / "evidence-report.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def execute(state_path: Path, state: dict[str, Any], args: argparse.Namespace) -> int:
    evidence_dir = state_path.parent / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    concurrency = max(1, min(int(args.concurrency), 8))

    def run_action(action: dict[str, Any]) -> tuple[dict[str, Any], Path, subprocess.CompletedProcess[str] | None, str | None]:
        action["attempts"] = int(action.get("attempts", 0)) + 1
        action_type = action.get("type", "discover")
        suffix = "json" if action_type in {"discover", "scrape"} else "txt"
        output_path = evidence_dir / f'{action["id"]}-{slug(action["entity"])}-{action["module"]}.{suffix}'
        try:
            result = execute_action(action, os.environ.get("DATAIFY_API_TOKEN", "").strip())
        except (OSError, ValueError) as exc:
            return action, output_path, None, str(exc)[:1000]
        return action, output_path, result, None

    succeeded_this_run = 0
    while True:
        successful_ids = {action["id"] for action in state["actions"] if action["status"] == "success"}
        candidates = [
            action for action in state["actions"]
            if action["status"] in {"pending", "failed"}
            and int(action.get("attempts", 0)) < 2
            and all(dependency in successful_ids for dependency in action.get("depends_on", []))
            and not (action["status"] == "failed" and action.get("type") == "scrape")
        ]
        if not candidates:
            break
        batch = candidates[:concurrency]
        with ThreadPoolExecutor(max_workers=len(batch)) as pool:
            results = list(pool.map(run_action, batch))
        for action, output_path, result, local_error in results:
            action_type = action.get("type", "discover")
            if local_error:
                action.update(status="failed", error=local_error)
            elif result and result.returncode == 0:
                output_path.write_text(result.stdout, encoding="utf-8")
                action.update(status="success", output=str(output_path.relative_to(state_path.parent)), error=None)
                succeeded_this_run += 1
                if action_type == "discover":
                    expand_discovered_actions(state, action, result.stdout)
            else:
                error = result and (result.stderr or result.stdout).strip() or "unknown execution error"
                action.update(status="failed", error=error[:1000])
        save(state_path, state)
        if args.checkpoint and not args.autopilot and succeeded_this_run:
            break
    write_report(state_path, state)
    evidence = normalize(state_path)
    workbook = state_path.parent / "analysis-workbook.json"
    workbook.write_text(json.dumps(build_worksheet(evidence), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report, structured_report = build_report(state_path)
    print(json.dumps({"state": str(state_path), "analysis_workbook": str(workbook), "report": str(report), "report_json": str(structured_report), "actions": state["actions"]}, ensure_ascii=False, indent=2))
    return 0 if all(action["status"] == "success" for action in state["actions"]) else 2


def main() -> int:
    args = parser().parse_args()
    try:
        state_path, state = load_or_plan(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if args.dry_run:
        report = write_report(state_path, state)
        print(json.dumps({"state": str(state_path), "report": str(report), "actions": state["actions"]}, ensure_ascii=False, indent=2))
        return 0
    if not os.environ.get("DATAIFY_API_TOKEN", "").strip():
        print("DATAIFY_API_TOKEN is not set. Configure it in the environment; never pass it on the command line.", file=sys.stderr)
        return 1
    return execute(state_path, state, args)


if __name__ == "__main__":
    raise SystemExit(main())
