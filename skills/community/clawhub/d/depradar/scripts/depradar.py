#!/usr/bin/env python3
"""depradar — breaking-change intelligence for your project dependencies.

Detects breaking changes in your dependencies, scans YOUR codebase for impact,
and surfaces community pain reports from GitHub Issues, Stack Overflow, Reddit,
and Hacker News.

Usage:
    python depradar.py [options] [package ...]

Options:
    --help, -h          Show this help message and exit
    --version           Print version and exit
    --diagnose          Show configuration status (API keys, sources) and exit
    --mock              Run with realistic demo data (no network calls)
    --emit=<mode>       Output: compact (default), json, md, context
    --depth=<level>     Scan depth: quick, default, deep
    --days=<N>          Look back N days (default: 30)
    --since=<YYYY-MM-DD> Only show packages released on/after this date
    --path=<dir>        Project root to scan (default: current directory)
    --no-scan           Skip codebase usage scan (faster)
    --no-community      Skip community signal search
    --refresh           Bypass cache, force fresh data
    --save              Save markdown report to ~/Documents/DepRadar/
    --save-dir=<path>   Save report to custom directory

Examples:
    python depradar.py                        # Scan all deps in current project
    python depradar.py stripe openai          # Check only these packages
    python depradar.py --quick                # Fast scan, top packages only
    python depradar.py --deep --emit=md       # Deep scan, full markdown output
    python depradar.py --mock --emit=json     # Demo mode, JSON output
    python depradar.py --diagnose             # Show API key status
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Ensure lib/ is on the import path ─────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).parent
_LIB_DIR    = _SCRIPT_DIR / "lib"
if str(_LIB_DIR) not in sys.path:
    sys.path.insert(0, str(_LIB_DIR))

from schema import (
    DepRadarReport, BreakingChange, DepInfo, GithubIssueItem,
    ImpactLocation, PackageUpdate, StackOverflowItem, SubScores,
)
from render  import render, auto_save
from env     import get_config, github_headers, load_npmrc_registry
import ui as _ui_module
from ui      import (print_banner, print_diagnose, print_status,
                     print_warn, print_error, print_ok, print_info, Spinner)
from dates   import today_utc
from score   import score_all
from ignores import load_ignores, is_ignored
from verbose_log import VerboseLog
import cache

__version__ = "2.0.0"

# ── Timeout profiles ──────────────────────────────────────────────────────────

_TIMEOUT_PROFILES: Dict[str, Dict[str, int]] = {
    "quick":   {"global": 60,  "registry": 10, "community": 15, "scan": 10, "max_pkgs": 5},
    "default": {"global": 180, "registry": 20, "community": 45, "scan": 30, "max_pkgs": 30},
    "deep":    {"global": 300, "registry": 30, "community": 90, "scan": 60, "max_pkgs": 999},
}

_DEFAULT_EMIT  = "compact"
_DEFAULT_DEPTH = "default"
_DEFAULT_DAYS  = 30


# ── Argument parsing ───────────────────────────────────────────────────────────

def _parse_args(argv: List[str]) -> Dict[str, Any]:
    args: Dict[str, Any] = {
        "help":             False,
        "diagnose":         False,
        "setup":            False,
        "mock":             False,
        "emit":             _DEFAULT_EMIT,
        "depth":            _DEFAULT_DEPTH,
        "days":             _DEFAULT_DAYS,
        "path":             ".",
        "no_scan":          False,
        "no_community":     False,
        "refresh":          False,
        "save":             False,
        "save_dir":         None,
        "version":          False,
        "verbose":          False,
        "all":              False,       # include devDependencies
        "fail_on_breaking": False,       # exit 1 if breaking changes found
        "min_score":        0,           # minimum score to show (0 = show all)
        "notify":           None,        # --notify=slack://... or file://...
        "show_ignored":     False,       # show items suppressed by .depradar-ignore
        "since":            None,        # --since=YYYY-MM-DD: only show releases after this date
        "packages":         [],
    }
    for arg in argv:
        if arg in ("--help", "-h"):          args["help"]             = True
        elif arg == "--diagnose":            args["diagnose"]         = True
        elif arg == "--setup":               args["setup"]            = True
        elif arg == "--mock":                args["mock"]             = True
        elif arg == "--no-scan":             args["no_scan"]          = True
        elif arg == "--no-community":        args["no_community"]     = True
        elif arg == "--refresh":             args["refresh"]          = True
        elif arg == "--save":                args["save"]             = True
        elif arg == "--version":             args["version"]          = True
        elif arg in ("--verbose", "-v"):     args["verbose"]          = True
        elif arg == "--all":                 args["all"]              = True
        elif arg == "--fail-on-breaking":    args["fail_on_breaking"] = True
        elif arg == "--show-ignored":        args["show_ignored"]     = True
        elif arg.startswith("--emit="):      args["emit"]             = arg.split("=", 1)[1]
        elif arg.startswith("--depth="):
            v = arg.split("=", 1)[1]
            if v in _TIMEOUT_PROFILES:
                args["depth"] = v
        elif arg.startswith("--days="):
            try:   args["days"]      = int(arg.split("=", 1)[1])
            except ValueError: pass
        elif arg.startswith("--path="):      args["path"]             = arg.split("=", 1)[1]
        elif arg.startswith("--save-dir="):  args["save_dir"]         = arg.split("=", 1)[1]
        elif arg.startswith("--min-score="):
            try:   args["min_score"] = int(arg.split("=", 1)[1])
            except ValueError: pass
        elif arg.startswith("--notify="):    args["notify"]           = arg.split("=", 1)[1]
        elif arg == "--quick":               args["depth"]            = "quick"
        elif arg == "--deep":                args["depth"]            = "deep"
        elif arg.startswith("--since="):    args["since"]            = arg.split("=", 1)[1]
        elif not arg.startswith("-"):       args["packages"].append(arg)
    return args


# ── Mock / demo data ───────────────────────────────────────────────────────────

def _make_mock_report(
    packages: Optional[List[str]] = None,
    depth: str = "default",
    days: int = 30,
    project_path: str = ".",
) -> DepRadarReport:
    """Return a rich, realistic DepRadarReport for demo/testing (no network)."""
    today = today_utc()

    stripe_bc = BreakingChange(
        symbol        = "stripe.webhooks.constructEvent",
        change_type   = "removed",
        description   = ("`stripe.webhooks.constructEvent()` has been renamed to "
                         "`stripe.webhooks.verify()`. The old method is fully removed in v8."),
        old_signature = "constructEvent(payload: string, sig: string, secret: string): Stripe.Event",
        new_signature = None,
        migration_note= "Replace all calls with `stripe.webhooks.verify(payload, sig, secret)`.",
        source        = "release_notes",
        confidence    = "high",
    )
    stripe_bc2 = BreakingChange(
        symbol        = "stripe.customers.create",
        change_type   = "signature_changed",
        description   = "`createCustomer()` now requires `email` parameter (was optional in v7).",
        old_signature = "createCustomer(params?: CustomerCreateParams): Promise<Customer>",
        new_signature = "createCustomer(params: CustomerCreateParams & { email: string }): Promise<Customer>",
        migration_note= "Ensure `email` is passed to all `createCustomer()` calls.",
        source        = "changelog",
        confidence    = "high",
    )
    stripe_pkg = PackageUpdate(
        id            = "P1",
        package       = "stripe",
        ecosystem     = "npm",
        current_version = "7.0.0",
        latest_version  = "8.0.0",
        semver_type     = "major",
        has_breaking_changes = True,
        breaking_changes = [stripe_bc, stripe_bc2],
        changelog_url  = "https://github.com/stripe/stripe-node/releases/tag/v8.0.0",
        release_date   = "2026-01-10",
        release_notes_snippet = (
            "## Breaking Changes\n- `constructEvent()` renamed to `verify()`\n"
            "- `createCustomer()` requires `email` parameter\n\n"
            "Run `stripe-node-migrate` for automated migration assistance."
        ),
        impact_locations = [
            ImpactLocation("src/payments/webhook.ts", 47,
                           "const event = stripe.webhooks.constructEvent(payload, sig, secret);",
                           "grep"),
            ImpactLocation("tests/webhook.test.ts", 23,
                           "stripe.webhooks.constructEvent(body, sig, endpointSecret)", "grep"),
        ],
        impact_confidence = "med",
        github_repo    = "stripe/stripe-node",
        subs  = SubScores(severity=100, recency=85, impact=70, community=62),
        score = 89,
    )

    openai_bc1 = BreakingChange(
        symbol        = "openai.Completion.create",
        change_type   = "removed",
        description   = "`openai.Completion.create()` removed. Use `client.completions.create()`.",
        migration_note= "Instantiate: `client = openai.OpenAI()`. Call: `client.completions.create(...)`.",
        source        = "release_notes", confidence = "high",
    )
    openai_bc2 = BreakingChange(
        symbol        = "openai.ChatCompletion.create",
        change_type   = "removed",
        description   = "`openai.ChatCompletion.create()` removed. Use `client.chat.completions.create()`.",
        migration_note= "Use `client.chat.completions.create(model=..., messages=...)`.",
        source        = "release_notes", confidence = "high",
    )
    openai_bc3 = BreakingChange(
        symbol        = "openai.error",
        change_type   = "renamed",
        description   = "Error classes moved: `openai.error.RateLimitError` → `openai.RateLimitError`.",
        old_signature = "openai.error.RateLimitError",
        new_signature = "openai.RateLimitError",
        migration_note= "Remove the `.error` intermediate module from all imports.",
        source        = "changelog", confidence = "high",
    )
    openai_pkg = PackageUpdate(
        id            = "P2",
        package       = "openai",
        ecosystem     = "pypi",
        current_version = "0.28.0",
        latest_version  = "1.35.0",
        semver_type     = "major",
        has_breaking_changes = True,
        breaking_changes = [openai_bc1, openai_bc2, openai_bc3],
        changelog_url  = "https://github.com/openai/openai-python/releases/tag/v1.0.0",
        release_date   = "2023-11-06",
        release_notes_snippet = (
            "Complete SDK rewrite. All methods now on client instance.\n"
            "Run `openai migrate` for auto-fix of most patterns."
        ),
        impact_locations = [],
        impact_confidence = "not_scanned",
        github_repo    = "openai/openai-python",
        subs  = SubScores(severity=100, recency=10, impact=50, community=80),
        score = 72,
    )

    axios_pkg = PackageUpdate(
        id="P3", package="axios", ecosystem="npm",
        current_version="1.3.0", latest_version="1.7.2", semver_type="minor",
        has_breaking_changes=False, release_date=today, score=18,
    )
    express_pkg = PackageUpdate(
        id="P4", package="express", ecosystem="npm",
        current_version="4.18.0", latest_version="4.19.2", semver_type="patch",
        has_breaking_changes=False, release_date=today,
        release_notes_snippet="Security: fixed ReDoS vulnerability in path parser.", score=15,
    )

    gh_issue = GithubIssueItem(
        id="GI1", package="stripe", version="8.0.0",
        title="Breaking change: constructEvent removed in v8",
        url="https://github.com/stripe/stripe-node/issues/1842",
        body_snippet=("`stripe.webhooks.constructEvent()` no longer available after upgrade "
                      "to stripe v8.0.0. Getting TypeError: not a function"),
        comments=23, labels=["breaking-change", "v8"], state="open",
        created_at="2026-01-11T08:15:00Z",
        subs=SubScores(severity=80, recency=85, impact=69, community=50), score=74,
    )
    gh_issue2 = GithubIssueItem(
        id="GI2", package="stripe", version="8.0.0",
        title="Migration guide for stripe v8 webhook verification",
        url="https://github.com/stripe/stripe-node/issues/1850",
        body_snippet="Community-maintained migration guide for constructEvent → verify()",
        comments=45, labels=["documentation"], state="closed",
        resolution_snippet="Use `stripe.webhooks.verify()` — full guide in MIGRATION.md",
        created_at="2026-01-12T10:00:00Z",
        subs=SubScores(severity=40, recency=85, impact=100, community=50), score=66,
    )
    so_item = StackOverflowItem(
        id="SO1", package="stripe",
        question_title="stripe webhooks constructEvent not a function after upgrade",
        question_url="https://stackoverflow.com/questions/78800042",
        answer_count=4, is_answered=True,
        accepted_answer_snippet=(
            "After upgrading to stripe v8, use `stripe.webhooks.verify()` instead "
            "of `stripe.webhooks.constructEvent()`. The signature is identical."
        ),
        tags=["stripe", "node.js", "webhooks", "breaking-change"],
        view_count=3200, so_score=28,
        created_at="2026-01-11T08:00:00Z",
        subs=SubScores(severity=40, recency=85, impact=52, community=55), score=52,
    )
    openai_so = StackOverflowItem(
        id="SO2", package="openai",
        question_title="AttributeError: module 'openai' has no attribute 'ChatCompletion'",
        question_url="https://stackoverflow.com/questions/75974873",
        answer_count=12, is_answered=True,
        accepted_answer_snippet=(
            "The openai Python library v1.0.0 was a full rewrite. "
            "Use `client = openai.OpenAI(); client.chat.completions.create(...)`"
        ),
        tags=["openai", "python", "chatgpt"],
        view_count=52000, so_score=156,
        created_at="2023-11-08T09:00:00Z",
        subs=SubScores(severity=60, recency=10, impact=100, community=95), score=68,
    )

    breaking: List[PackageUpdate] = [stripe_pkg, openai_pkg]
    minor:    List[PackageUpdate] = [axios_pkg, express_pkg]
    if packages:
        pkg_set  = {p.lower() for p in packages}
        breaking = [p for p in breaking if p.package.lower() in pkg_set]
        minor    = [p for p in minor    if p.package.lower() in pkg_set]

    return DepRadarReport(
        project_path    = str(Path(project_path).resolve()),
        dep_files_found = ["package.json", "requirements.txt"],
        packages_scanned = 6,
        packages_with_breaking_changes = breaking,
        packages_with_minor_updates    = minor,
        packages_current               = ["lodash", "dotenv", "cors"],
        packages_not_found             = [],
        github_issues = [gh_issue, gh_issue2] if (
            not packages or "stripe" in [p.lower() for p in packages]) else [],
        stackoverflow  = (
            ([so_item] if (not packages or "stripe" in [p.lower() for p in packages]) else []) +
            ([openai_so] if (not packages or "openai" in [p.lower() for p in packages]) else [])
        ),
        from_cache      = False,
        depth           = depth,
        days_window     = days,
        generated_at    = today_utc() + "T00:00:00Z",
    )


# ── Live pipeline ──────────────────────────────────────────────────────────────

def _registry_for_package(
    pkg_name: str,
    global_url: Optional[str],
    scope_map: Optional[Dict[str, str]],
    fallback: str = "",
) -> str:
    """Return the correct registry URL for a package, respecting .npmrc scope overrides."""
    if pkg_name.startswith("@") and scope_map:
        scope = "@" + pkg_name.split("/")[0].lstrip("@")
        if scope in scope_map:
            return scope_map[scope]
    return global_url or fallback


def _fetch_registry_updates(
    all_deps: Dict[str, DepInfo],
    config: Dict[str, str],
    depth: str,
    days: int,
    timeouts: Dict[str, int],
    registry_url: Optional[str] = None,
    scope_map: Optional[Dict[str, str]] = None,
    vlog: Optional[Any] = None,
) -> Tuple[List[PackageUpdate], List[PackageUpdate], List[str], Dict[str, str], Dict[str, int], List[str], Dict[str, str]]:
    """Phase 1: Parallel registry lookups.

    Returns (breaking, minor, current, errors, rate_limit_hits, rate_limited_packages, fetch_error_packages).
    """
    import npm_registry
    import pypi_registry
    import github_releases
    from changelog_parser import extract_breaking_changes, has_breaking_changes_flag

    breaking:              List[PackageUpdate] = []
    minor:                 List[PackageUpdate] = []
    current:               List[str] = []
    errors:                Dict[str, str] = {}
    rate_limit_hits:       Dict[str, int] = {}
    rate_limited_packages: List[str] = []        # packages skipped due to rate limit
    fetch_error_packages:  Dict[str, str] = {}   # transient errors (network/timeout)
    max_pkgs          = timeouts.get("max_pkgs", 999)
    reg_timeout       = timeouts["registry"]
    token             = config.get("GITHUB_TOKEN")
    _rl_lock          = threading.Lock()

    def _bump_rate_limit(source: str) -> None:
        with _rl_lock:
            rate_limit_hits[source] = rate_limit_hits.get(source, 0) + 1

    def _check_one(idx_pkg: Tuple[int, str, DepInfo]) -> Tuple[str, Optional[PackageUpdate], Optional[str]]:
        idx, pkg_name, dep_info = idx_pkg
        eco         = dep_info.ecosystem
        current_ver = dep_info.version or ""
        try:
            update: Optional[PackageUpdate] = None
            if eco == "npm":
                pkg_registry = _registry_for_package(
                    pkg_name, registry_url, scope_map, npm_registry.NPM_REGISTRY
                )
                update = npm_registry.build_package_update(
                    pkg_name, current_ver, idx,
                    registry_url=pkg_registry,
                )
                # Ecosystem fallback: CLI-specified packages may be PyPI not npm.
                # If npm returns nothing and version is synthetic "0.0.0", try PyPI.
                # (version "0.0.0" signals a CLI-guessed package not found in dep files)
                if update is None and current_ver == "0.0.0":
                    pypi_update = pypi_registry.build_package_update(pkg_name, current_ver, idx)
                    if pypi_update is not None:
                        update = pypi_update
                        _ui_module.print_info(
                            f"{pkg_name}: not found on npm — using PyPI. "
                            "Specify --ecosystem=pypi to skip npm lookup."
                        )
                elif update is not None and current_ver == "0.0.0":
                    # npm found the package but ecosystem was guessed; warn the user
                    _ui_module.print_info(
                        f"{pkg_name}: ecosystem guessed as npm (not found in dep files). "
                        "Use --ecosystem=pypi if this is a Python package."
                    )
            elif eco == "pypi":
                update = pypi_registry.build_package_update(pkg_name, current_ver, idx)
            else:
                return pkg_name, None, None   # unsupported ecosystem → skip silently

            if update is None:
                return pkg_name, None, None   # up to date

            # Transfer workspace_versions from DepInfo to PackageUpdate
            if dep_info.workspace_versions:
                update.workspace_versions = dep_info.workspace_versions

            # Enrich with GitHub release notes + changelog parsing
            if update.semver_type == "major":
                try:
                    gh_update = github_releases.fetch_package_updates(
                        pkg_name, current_ver,
                        update.github_repo or dep_info.github_repo,
                        ecosystem=eco, days=days, depth=depth, token=token,
                    )
                    if gh_update:
                        gh_update.id = f"P{idx}"
                        gh_update.workspace_versions = update.workspace_versions
                        update = gh_update
                except Exception:
                    pass

                # Parse breaking changes from whatever notes we have
                notes = update.release_notes_snippet or ""
                if notes:
                    # For multi-major jumps (e.g. 0.28→1.35), always parse —
                    # individual releases may lack conventional markers but still have breaks.
                    # For single-major bumps, require the breaking change flag first.
                    try:
                        current_major = int(update.current_version.split(".")[0])
                        latest_major  = int(update.latest_version.split(".")[0])
                        is_multi_major = latest_major > current_major
                    except (ValueError, AttributeError):
                        is_multi_major = False
                    if is_multi_major or has_breaking_changes_flag(notes):
                        bcs = extract_breaking_changes(notes, source="release_notes")
                        if bcs:
                            update.breaking_changes = bcs
                            update.has_breaking_changes = True

            elif update.semver_type in ("minor", "patch"):
                # Fix 10: Check minor/patch releases for breaking changes too
                notes = update.release_notes_snippet or ""
                if notes:
                    bcs = extract_breaking_changes(notes, source="release_notes")
                    if bcs:
                        update.breaking_changes = bcs
                        update.has_breaking_changes = True
                        update.semver_violation = True  # breaking in non-major = semver violation

            return pkg_name, update, None

        except Exception as exc:
            err_str = str(exc)
            # Detect rate limit errors (Fix 13) — track which packages were affected
            if "rate limit" in err_str.lower() or "403" in err_str or "429" in err_str:
                _bump_rate_limit("github" if "github" in err_str.lower() else "registry")
                with _rl_lock:
                    rate_limited_packages.append(pkg_name)
                return pkg_name, None, f"rate_limited: {err_str}"
            # Detect transient network errors vs definitive not-found
            lower = err_str.lower()
            is_transient = any(
                kw in lower for kw in ("timeout", "connection", "network", "dns", "socket", "ssl")
            )
            if is_transient:
                with _rl_lock:
                    fetch_error_packages[pkg_name] = err_str[:120]
            return pkg_name, None, err_str

    items = list(enumerate(all_deps.items(), 1))[:max_pkgs]
    idx_items = [(i, name, info) for i, (name, info) in items]

    if vlog:
        vlog.step("Registry lookups", f"{len(idx_items)} packages")

    with Spinner(f"Checking {len(idx_items)} packages for updates"):
        with ThreadPoolExecutor(max_workers=8) as pool:
            futs = {pool.submit(_check_one, item): item for item in idx_items}
            for fut in as_completed(futs, timeout=reg_timeout * len(idx_items) + 5):
                try:
                    pkg_name, update, err = fut.result(timeout=reg_timeout)
                except Exception as exc:
                    item = futs[fut]
                    errors[item[1]] = str(exc)
                    continue
                if err:
                    errors[pkg_name] = err
                elif update is None:
                    current.append(pkg_name)
                elif update.has_breaking_changes or update.semver_type == "major":
                    if update.semver_type == "major":
                        update.has_breaking_changes = True
                    breaking.append(update)
                else:
                    minor.append(update)

    if vlog:
        vlog.result("registry", len(breaking) + len(minor) + len(current),
                    f"{len(breaking)} breaking, {len(minor)} minor, {len(current)} current")

    # Sort breaking by recency (newest first)
    from dates import recency_score as rs
    breaking.sort(key=lambda p: rs(p.release_date or ""), reverse=True)
    return breaking, minor, current, errors, rate_limit_hits, rate_limited_packages, fetch_error_packages


def _run_codebase_scan(
    breaking: List[PackageUpdate],
    project_path: str,
    timeout: int,
    vlog: Optional[Any] = None,
) -> Tuple[List[PackageUpdate], List[str]]:
    """Phase 2: Scan YOUR codebase for impact.

    Returns (updated_breaking, skipped_files_list).
    """
    if not breaking:
        return breaking, []
    try:
        from impact_analyzer import analyze_impact
        if vlog:
            vlog.step("Codebase scan", f"{len(breaking)} packages to scan")
        with Spinner("Scanning codebase for impact"):
            updated, skipped = analyze_impact(breaking, project_path, timeout_per_package=timeout)
        if vlog:
            total_locs = sum(len(p.impact_locations) for p in updated)
            vlog.scan(
                files_scanned=0,   # analyze_impact doesn't expose this count directly
                matches=total_locs,
                skipped=len(skipped),
            )
        return updated, skipped
    except Exception as exc:
        print_warn(f"Codebase scan failed: {exc}")
        return breaking, []


def _fetch_community_signals(
    breaking: List[PackageUpdate],
    config: Dict[str, str],
    depth: str,
    days: int,
    timeout: int,
    vlog: Optional[Any] = None,
) -> Tuple[List, List, List, List, List, Dict[str, str], Dict[str, int]]:
    """Phase 3: Parallel community signal search for all breaking packages.

    Returns (github_issues, stackoverflow, reddit, hackernews, twitter, errors, rate_limit_hits).
    """
    if not breaking:
        return [], [], [], [], [], {}, {}

    from github_issues import search_issues
    from stackoverflow import search_stackoverflow
    from hackernews   import search_hackernews

    pkg_names  = [p.package for p in breaking]
    repos      = {p.package: p.github_repo for p in breaking if p.github_repo}
    ecosystems = list({p.ecosystem for p in breaking})
    ecosystem  = ecosystems[0] if len(ecosystems) == 1 else "all"

    errors:          Dict[str, str] = {}
    rate_limit_hits: Dict[str, int] = {}
    _rl_lock = threading.Lock()

    def _bump_rate_limit(source: str) -> None:
        with _rl_lock:
            rate_limit_hits[source] = rate_limit_hits.get(source, 0) + 1

    def _run_github_issues():
        try:
            return search_issues(pkg_names, repos, days=days, depth=depth,
                                 token=config.get("GITHUB_TOKEN"))
        except Exception as exc:
            err_str = str(exc)
            if "rate limit" in err_str.lower() or "403" in err_str or "429" in err_str:
                _bump_rate_limit("github_issues")
            errors["github_issues"] = err_str
            return []

    def _run_stackoverflow():
        try:
            return search_stackoverflow(pkg_names, days=days, depth=depth,
                                        api_key=config.get("STACKOVERFLOW_API_KEY"),
                                        ecosystem=ecosystem)
        except Exception as exc:
            err_str = str(exc)
            if "rate limit" in err_str.lower() or "403" in err_str or "429" in err_str:
                _bump_rate_limit("stackoverflow")
            errors["stackoverflow"] = err_str
            return []

    def _run_hackernews():
        try:
            return search_hackernews(pkg_names, days=days, depth=depth)
        except Exception as exc:
            errors["hackernews"] = str(exc)
            return []

    def _run_reddit():
        try:
            from reddit_sc import search_reddit
            sc_token = config.get("SCRAPECREATORS_API_KEY")
            if not sc_token:
                return []
            return search_reddit(pkg_names, ecosystem=ecosystem, days=days, depth=depth,
                                 token=sc_token)
        except Exception as exc:
            err_str = str(exc)
            if "rate limit" in err_str.lower() or "429" in err_str:
                _bump_rate_limit("reddit")
            errors["reddit"] = err_str
            return []

    def _run_twitter():
        try:
            from twitter_x import search_twitter
            xai_key = config.get("XAI_API_KEY")
            auth    = config.get("AUTH_TOKEN")
            ct0     = config.get("CT0")
            if not (xai_key or (auth and ct0)):
                return []
            return search_twitter(pkg_names, days=days, depth=depth,
                                  xai_api_key=xai_key, auth_token=auth, ct0=ct0)
        except Exception as exc:
            errors["twitter"] = str(exc)
            return []

    if vlog:
        vlog.step("Community signals", f"{len(pkg_names)} packages across 5 sources")

    with Spinner("Searching community signals"):
        with ThreadPoolExecutor(max_workers=5) as pool:
            futs = {
                pool.submit(_run_github_issues): "github_issues",
                pool.submit(_run_stackoverflow):  "stackoverflow",
                pool.submit(_run_hackernews):     "hackernews",
                pool.submit(_run_reddit):         "reddit",
                pool.submit(_run_twitter):        "twitter",
            }
            results: Dict[str, List] = {}
            for fut in as_completed(futs, timeout=timeout + 5):
                source = futs[fut]
                try:
                    results[source] = fut.result(timeout=timeout)
                    if vlog:
                        vlog.result(source, len(results[source]))
                except Exception as exc:
                    errors[source] = str(exc)
                    results[source] = []
                    if vlog:
                        vlog.error(source, str(exc))

    return (
        results.get("github_issues", []),
        results.get("stackoverflow",  []),
        results.get("reddit",         []),
        results.get("hackernews",     []),
        results.get("twitter",        []),
        errors,
        rate_limit_hits,
    )


# ── Notification helper ────────────────────────────────────────────────────────

def _send_notify(target: str, report: "DepRadarReport") -> None:
    """Parse --notify= target and dispatch the notification."""
    try:
        from notify import parse_notify_target, send_notification
        target_dict = parse_notify_target(target)
        if target_dict is None:
            print_warn(f"Unrecognized --notify target: {target!r}. Use slack://... or file://...")
            return
        send_notification(target_dict, report.to_dict())
        print_ok(f"Notification sent: {target}")
    except Exception as exc:
        print_warn(f"Notification failed ({target}): {exc}")


# ── Setup wizard ──────────────────────────────────────────────────────────────

def _run_setup_wizard(existing_config: Dict[str, str]) -> None:
    """Interactive first-run configuration wizard.

    Walks through each optional API key, shows current status, and writes
    to ~/.config/depradar/.env on confirmation.
    """
    import getpass

    config_dir  = Path.home() / ".config" / "depradar"
    env_file    = config_dir / ".env"
    config_dir.mkdir(parents=True, exist_ok=True)

    print("\n  /depradar — Setup Wizard")
    print("  ─────────────────────────────────────────────────────")
    print("  API keys are optional. Without them the tool still works")
    print("  using public rate limits.  Keys enable faster/deeper scans.")
    print()

    _KEY_INFO = [
        (
            "GITHUB_TOKEN",
            "GitHub Personal Access Token",
            "github.com/settings/tokens (no scopes needed)",
            "60 req/hr → 5,000 req/hr — strongly recommended",
        ),
        (
            "SCRAPECREATORS_API_KEY",
            "ScrapeCreators API Key",
            "scrapecreators.com",
            "Enables Reddit community signals (paid service)",
        ),
        (
            "XAI_API_KEY",
            "xAI API Key",
            "console.x.ai",
            "Enables X/Twitter signals via Grok (LLM-sourced, not live search)",
        ),
        (
            "STACKOVERFLOW_API_KEY",
            "Stack Overflow API Key",
            "stackapps.com/apps/oauth/register",
            "300 req/day → 10,000 req/day",
        ),
    ]

    new_values: Dict[str, str] = {}
    for key, label, url, benefit in _KEY_INFO:
        current = existing_config.get(key, "")
        status  = f"currently: {current[:8]}…" if current else "currently: not set"
        print(f"  {label}")
        print(f"    Get yours at: {url}")
        print(f"    Benefit: {benefit}")
        print(f"    ({status})")
        try:
            value = getpass.getpass(f"    Enter value (Enter to skip): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Setup cancelled.")
            return
        if value:
            new_values[key] = value
        elif current:
            new_values[key] = current  # preserve existing
        print()

    if not new_values:
        print("  No keys entered — nothing to save.")
        return

    lines = [f"# depradar API keys — generated by /depradar --setup\n"]
    for k, v in new_values.items():
        lines.append(f"{k}={v}\n")

    env_file.write_text("".join(lines), encoding="utf-8")
    print(f"  ✓ Configuration saved to: {env_file}")
    print()
    print("  Run /depradar --diagnose to verify all keys are loaded.")
    print()


# ── Main entry point ───────────────────────────────────────────────────────────

def run(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    args    = _parse_args(argv)
    config  = get_config()

    if args["help"]:
        print(__doc__)
        return 0

    if args["version"]:
        print(f"depradar {__version__}")
        return 0

    if args["diagnose"]:
        print_diagnose(config, test_calls=True)
        return 0

    if args.get("setup"):
        _run_setup_wizard(config)
        return 0

    # Set up verbose logger
    vlog = VerboseLog(enabled=args["verbose"])

    # For machine-readable emit modes, route ALL progress output to stderr so
    # stdout is pure JSON/context data that can be piped to json.load().
    _machine_emit = args["emit"] in ("json", "context")
    _ui_module.set_machine_mode(_machine_emit)
    if _machine_emit:
        print_banner(config, file=sys.stderr)
    else:
        print_banner(config)

    # ── Mock mode ────────────────────────────────────────────────────────────
    if args["mock"]:
        report   = _make_mock_report(args["packages"] or None, args["depth"],
                                     args["days"], args["path"])
        output   = render(report, emit_mode=args["emit"],
                          min_score=args["min_score"])
        print(output)
        if args["save"] or args["save_dir"]:
            saved = auto_save(report, args["save_dir"])
            if saved:
                print_ok(f"Report saved: {saved}")
        if args["notify"]:
            _send_notify(args["notify"], report)
        if args["fail_on_breaking"] and report.packages_with_breaking_changes:
            return 1
        return 0

    # ── Live mode ────────────────────────────────────────────────────────────
    try:
        from dep_parser import find_dep_files, parse_all
    except ImportError as exc:
        print_error(f"Import failed: {exc}")
        return 1

    depth    = args["depth"]
    days     = args["days"]
    emit     = args["emit"]
    timeouts = _TIMEOUT_PROFILES[depth]
    project_path = str(Path(args["path"]).resolve())

    # ── Step 1: Parse dependency files ───────────────────────────────────────
    vlog.step("Parsing dependency files", project_path)
    dep_parse_errors: List[str] = []
    depth_warnings: List[str] = []

    # Read custom npm registry from .npmrc if present
    npm_registry_url, scope_registry_map = load_npmrc_registry(project_path)
    if npm_registry_url:
        vlog.info(f"Using custom npm registry: {npm_registry_url}")
    if scope_registry_map:
        vlog.info(f"Scoped registries: {list(scope_registry_map.keys())}")

    # Load ignore list
    ignores = load_ignores(project_path)
    if ignores:
        vlog.info(f"Loaded {len(ignores)} ignore entries from .depradar-ignore")

    if args["packages"]:
        # Read dep files to get accurate current versions and ecosystems.
        # When packages are specified by name, we still consult dep files so that
        # /depradar stripe  correctly reads your package.json and knows you have v7.x.
        dep_files, _ = find_dep_files(project_path)
        _dep_lookup: Dict[str, DepInfo] = {}
        if dep_files:
            _dep_lookup, _ = parse_all(dep_files, include_dev=True)

        all_deps = {}
        for pkg in args["packages"]:
            if pkg in _dep_lookup:
                # Found in project dep files — use exact version and ecosystem
                all_deps[pkg] = _dep_lookup[pkg]
            else:
                # Not found in any dep file — ecosystem is unknown.
                # Default to npm (covers the majority of CLI use cases).
                # Will try PyPI as fallback in _check_one() if npm finds nothing.
                print_warn(
                    f"{pkg}: not found in project dep files — will try npm then PyPI. "
                    "Add --ecosystem=pypi to check PyPI first."
                )
                all_deps[pkg] = DepInfo(
                    name=pkg, version_spec="*", version="0.0.0",
                    ecosystem="npm", source_file="cli",
                )
        dep_files = []   # don't show dep file list for name-only mode
    else:
        dep_files, depth_warnings = find_dep_files(project_path)
        if not dep_files:
            print_warn("No dependency files found. Are you in a project directory?")
            print_info("Tip: use --path=/your/project or specify packages directly.")
            return 0
        all_deps, dep_parse_errors = parse_all(dep_files, include_dev=args["all"])
        if not all_deps:
            print_warn("No dependencies detected.")
            return 0
        vlog.step("Dep files parsed",
                  f"{len(all_deps)} packages, {len(dep_files)} files"
                  + (f", {len(dep_parse_errors)} errors" if dep_parse_errors else ""))
        print_status(f"Found {len(all_deps)} dependencies in: {', '.join(Path(f).name for f in dep_files)}")

        # Surface dep parse errors
        if dep_parse_errors:
            print_warn(f"{len(dep_parse_errors)} dependency file(s) had parse errors:")
            for err in dep_parse_errors[:5]:
                print_info(f"  • {err}")

        # Surface depth warnings
        for w in depth_warnings:
            print_warn(w)

    # ── Step 2: Check cache ───────────────────────────────────────────────────
    ck = cache.project_cache_key(project_path, sorted(all_deps.keys()), days, depth)
    if not args["refresh"]:
        cached, age = cache.load_with_age(ck, ttl_hours=cache.REPORT_TTL_HOURS)
        if cached:
            try:
                report = DepRadarReport.from_dict(cached)
                report.from_cache     = True
                report.cache_age_hours = age
                print_info(f"Using cached report ({age:.1f}h old). Use --refresh to update.")
                output = render(report, emit_mode=emit)
                print(output)
                return 0
            except Exception:
                pass

    # ── Step 3: Registry lookups (parallel) ─────────────────────────────────
    breaking, minor, current, reg_errors, rl_hits_reg, rl_pkgs_reg, fetch_errs_reg = _fetch_registry_updates(
        all_deps, config, depth, days, timeouts,
        registry_url=npm_registry_url,
        scope_map=scope_registry_map,
        vlog=vlog,
    )
    print_ok(f"{len(breaking)} breaking, {len(minor)} minor, {len(current)} current")

    # Warn on rate limit hits from registry lookups (console notice — footer has full list)
    for source, count in rl_hits_reg.items():
        print_warn(
            f"GitHub rate limit hit while checking {count} package(s). "
            "Add GITHUB_TOKEN to ~/.config/depradar/.env for 5000 req/hr."
        )

    # ── Step 4: Codebase scan ────────────────────────────────────────────────
    scan_skipped: List[str] = []
    if not args["no_scan"] and breaking:
        breaking, scan_skipped = _run_codebase_scan(
            breaking, project_path, timeouts["scan"], vlog=vlog
        )
        if scan_skipped:
            vlog.warn(f"{len(scan_skipped)} file(s) skipped during scan")
            print_info(f"ℹ Scan skipped {len(scan_skipped)} file(s) (run --verbose for details)")
            if vlog.enabled:
                for s in scan_skipped[:10]:
                    vlog.info(f"  skipped: {s}")

    # ── Step 5: Community signals (parallel) ────────────────────────────────
    gh_issues, so_items, reddit_items, hn_items, tw_items, comm_errors, rl_hits_comm = (
        [], [], [], [], [], {}, {}
    )
    if not args["no_community"]:
        gh_issues, so_items, reddit_items, hn_items, tw_items, comm_errors, rl_hits_comm = \
            _fetch_community_signals(breaking, config, depth, days, timeouts["community"],
                                     vlog=vlog)

    # Merge rate limit hits
    rate_limit_hits: Dict[str, int] = {}
    for src, cnt in {**rl_hits_reg, **rl_hits_comm}.items():
        rate_limit_hits[src] = rate_limit_hits.get(src, 0) + cnt

    # Warn on community rate limit hits
    if rl_hits_comm:
        for source, count in rl_hits_comm.items():
            print_warn(f"Rate limit hit on {source} ({count} request(s)). Results may be incomplete.")

    # ── Step 6: Assemble report & score ─────────────────────────────────────
    vlog.step("Scoring", f"{len(breaking)} breaking packages")

    # Apply ignore filtering
    ignored_breaking: List[PackageUpdate] = []
    ignored_minor:    List[PackageUpdate] = []
    if ignores:
        breaking_filtered: List[PackageUpdate] = []
        for pkg in breaking:
            if is_ignored(pkg.package, pkg.latest_version, ignores):
                ignored_breaking.append(pkg)
            else:
                breaking_filtered.append(pkg)
        minor_filtered: List[PackageUpdate] = []
        for pkg in minor:
            if is_ignored(pkg.package, pkg.latest_version, ignores):
                ignored_minor.append(pkg)
            else:
                minor_filtered.append(pkg)
        breaking = breaking_filtered
        minor    = minor_filtered
        if ignored_breaking or ignored_minor:
            total_ignored = len(ignored_breaking) + len(ignored_minor)
            msg = f"ℹ {total_ignored} package(s) suppressed by .depradar-ignore"
            if not args["show_ignored"]:
                msg += " (run --show-ignored to see them)"
            print_info(msg)
            if args["show_ignored"]:
                for pkg in ignored_breaking + ignored_minor:
                    print_info(f"  ignored: {pkg.package}@{pkg.latest_version}")

    # Separate definitive "not found" (404) from transient fetch errors
    not_found_pkgs = [k for k in reg_errors if k not in fetch_errs_reg]

    report = DepRadarReport(
        project_path    = project_path,
        dep_files_found = [str(f) for f in dep_files],
        packages_scanned = len(all_deps),
        packages_with_breaking_changes = breaking,
        packages_with_minor_updates    = minor,
        packages_current               = current,
        packages_not_found             = not_found_pkgs,
        github_issues    = gh_issues,
        stackoverflow    = so_items,
        reddit           = reddit_items,
        hackernews       = hn_items,
        twitter          = tw_items,
        registry_errors       = reg_errors,
        registry_fetch_errors = fetch_errs_reg,
        community_errors      = comm_errors,
        dep_parse_errors      = dep_parse_errors,
        rate_limit_hits       = rate_limit_hits,
        rate_limited_packages = rl_pkgs_reg,
        scan_skipped          = scan_skipped,
        depth            = depth,
        days_window      = days,
        generated_at     = datetime.now(timezone.utc).isoformat(),
    )
    # Mark as partial when rate limits or transient fetch errors prevented complete coverage
    report.partial_results = bool(rl_pkgs_reg or fetch_errs_reg)

    score_all(report)

    # Apply min_score filtering (after scoring — we have real scores now)
    min_score = args["min_score"]
    if min_score > 0:
        suppressed = [p for p in breaking if p.score < min_score]
        report.packages_with_breaking_changes = [p for p in breaking if p.score >= min_score]
        if suppressed:
            print_info(
                f"ℹ {len(suppressed)} low-priority item(s) below score {min_score} "
                "(use --min-score=0 to see all)"
            )

    # Apply --since DATE filtering: only show packages released on/after the given date
    since_date = args.get("since")
    if since_date:
        def _released_since(pkg: PackageUpdate) -> bool:
            rd = (pkg.release_date or "")[:10]  # "YYYY-MM-DD"
            return rd >= since_date if rd else False
        before_breaking = len(report.packages_with_breaking_changes)
        before_minor    = len(report.packages_with_minor_updates)
        report.packages_with_breaking_changes = [
            p for p in report.packages_with_breaking_changes if _released_since(p)
        ]
        report.packages_with_minor_updates = [
            p for p in report.packages_with_minor_updates if _released_since(p)
        ]
        hidden = (before_breaking - len(report.packages_with_breaking_changes)) + \
                 (before_minor    - len(report.packages_with_minor_updates))
        if hidden:
            print_info(
                f"ℹ --since {since_date}: {hidden} package(s) with older releases hidden "
                "(remove --since to see all)"
            )

    # Surface community errors if any
    if comm_errors:
        for src, err in comm_errors.items():
            vlog.error(src, err)

    # ── Step 7: Cache & render ───────────────────────────────────────────────
    cache.save(ck, report.to_dict())

    output = render(report, emit_mode=emit, min_score=min_score)
    print(output)

    if args["save"] or args["save_dir"]:
        saved = auto_save(report, args["save_dir"])
        if saved:
            print_ok(f"Report saved: {saved}")

    if args["notify"]:
        _send_notify(args["notify"], report)

    # Fix 17: Exit code for CI/CD
    if args["fail_on_breaking"] and report.packages_with_breaking_changes:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run())
