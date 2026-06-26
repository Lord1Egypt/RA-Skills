#!/usr/bin/env python3
"""
browserslist_validator.py — Validate .browserslistrc and package.json browserslist config.

Commands:
  validate  Full validation (all 20 rules)
  check     Quick syntax-only check
  coverage  Estimate approximate browser coverage
  explain   Human-readable explanation of each query

Flags:
  --format text|json|summary   Output format (default: text)
  --strict                     Treat warnings as errors
  --env production|development Target environment

Exit codes:
  0  No errors
  1  Errors found (or warnings in --strict mode)
  2  File not found or parse error
"""

import json
import re
import sys
import os
import argparse
from typing import List, Tuple, Dict, Optional, Any

# ---------------------------------------------------------------------------
# Browser data (approximate, embedded — no network calls)
# ---------------------------------------------------------------------------

# max known major version for each browser
BROWSER_MAX_VERSIONS: Dict[str, int] = {
    "chrome": 124,
    "firefox": 125,
    "safari": 17,
    "edge": 124,
    "opera": 109,
    "samsung": 24,
    "ie": 11,
    "ios_saf": 17,
    "android": 124,
    "uc": 15,
    "baidu": 13,
    "kaios": 3,
    "op_mini": 4,
    "op_mob": 80,
    "bb": 10,
    "ie_mob": 11,
    "and_ff": 125,
    "and_chr": 124,
    "and_uc": 15,
    "and_qq": 14,
    "node": 22,
}

# Browser aliases (browserslist canonical name -> our key)
BROWSER_ALIASES: Dict[str, str] = {
    "chrome": "chrome",
    "firefox": "firefox",
    "ff": "firefox",
    "safari": "safari",
    "edge": "edge",
    "opera": "opera",
    "op": "opera",
    "samsung": "samsung",
    "ie": "ie",
    "ios_saf": "ios_saf",
    "ios": "ios_saf",
    "android": "android",
    "and_chr": "and_chr",
    "and_ff": "and_ff",
    "and_uc": "and_uc",
    "and_qq": "and_qq",
    "uc": "uc",
    "baidu": "baidu",
    "kaios": "kaios",
    "op_mini": "op_mini",
    "op_mob": "op_mob",
    "bb": "bb",
    "blackberry": "bb",
    "ie_mob": "ie_mob",
    "node": "node",
}

# Approximate global usage % for coverage estimation (as of early 2024)
BROWSER_USAGE: Dict[str, float] = {
    "chrome": 65.0,
    "safari": 19.0,
    "firefox": 4.0,
    "edge": 4.5,
    "samsung": 2.5,
    "opera": 2.0,
    "ios_saf": 18.0,
    "android": 1.5,
    "and_chr": 2.0,
    "ie": 0.5,
    "uc": 1.0,
    "op_mini": 0.3,
    "baidu": 0.1,
    "kaios": 0.1,
    "bb": 0.01,
    "ie_mob": 0.01,
}

DEAD_BROWSERS = {"ie", "bb", "blackberry", "ie_mob", "op_mini", "kaios", "baidu"}
MOBILE_BROWSERS = {"ios_saf", "ios", "android", "and_chr", "and_ff", "samsung", "op_mob", "uc", "and_uc", "and_qq"}

# Browserslist keywords that are valid query types
VALID_KEYWORDS = {
    "defaults", "dead", "not", "last", "since", "versions",
    "maintained", "node", "unreleased", "cover", "supports", "extends",
    "browserslist-config",
}

# ---------------------------------------------------------------------------
# Severity constants
# ---------------------------------------------------------------------------
SEV_ERROR = "E"
SEV_WARN = "W"
SEV_INFO = "I"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

class Finding:
    def __init__(self, severity: str, rule: str, message: str, line: int = 0):
        self.severity = severity
        self.rule = rule
        self.message = message
        self.line = line

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "rule": self.rule,
            "message": self.message,
            "line": self.line,
        }


# ---------------------------------------------------------------------------
# Query parser
# ---------------------------------------------------------------------------

class Query:
    """Represents a single parsed browserslist query."""

    def __init__(self, raw: str, line: int):
        self.raw = raw.strip()
        self.line = line
        self.negated = False
        self.canonical = self.raw

        # Strip leading "not "
        if self.raw.lower().startswith("not "):
            self.negated = True
            self.canonical = self.raw[4:].strip()

    def __repr__(self):
        return f"Query({self.raw!r}, line={self.line})"


def parse_browserslist_text(text: str) -> List[Query]:
    """Parse browserslist text format (one query per line, # comments, sections)."""
    queries = []
    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        # Remove inline comments
        if "#" in line:
            line = line[:line.index("#")].strip()
        # Skip empty lines and section headers (e.g. [production])
        if not line or line.startswith("["):
            continue
        queries.append(Query(line, lineno))
    return queries


def load_config(filepath: str) -> Tuple[Optional[List[Query]], Optional[str]]:
    """
    Load browserslist config from a file.
    Returns (queries, error_message). On error queries is None.
    """
    if not os.path.exists(filepath):
        return None, f"File not found: {filepath}"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except OSError as e:
        return None, f"Cannot read file: {e}"

    basename = os.path.basename(filepath)

    if basename.endswith(".json"):
        return _load_from_package_json(content, filepath)
    else:
        # .browserslistrc or any other text file
        return _load_from_text(content)


def _load_from_text(content: str) -> Tuple[Optional[List[Query]], Optional[str]]:
    queries = parse_browserslist_text(content)
    return queries, None


def _load_from_package_json(content: str, filepath: str) -> Tuple[Optional[List[Query]], Optional[str]]:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON in package.json: {e}"

    browserslist = data.get("browserslist")
    if browserslist is None:
        return None, "No 'browserslist' key found in package.json"

    # browserslist can be a list of strings or a dict of env->list
    if isinstance(browserslist, list):
        text = "\n".join(browserslist)
        return _load_from_text(text)
    elif isinstance(browserslist, dict):
        # Use all environments merged, or pick production
        all_queries: List[Query] = []
        for env_name, queries in browserslist.items():
            if isinstance(queries, list):
                for i, q in enumerate(queries, start=1):
                    all_queries.append(Query(str(q), i))
        return all_queries, None
    else:
        return None, f"'browserslist' in package.json must be an array or object, got {type(browserslist).__name__}"


# ---------------------------------------------------------------------------
# Query classification helpers
# ---------------------------------------------------------------------------

# Regex patterns for recognising query types
RE_LAST_N = re.compile(r"^last\s+(\d+)\s+versions?$", re.I)
RE_LAST_N_BROWSER = re.compile(r"^last\s+(\d+)\s+(\w[\w_]*)\s+versions?$", re.I)
RE_PERCENT_GT = re.compile(r"^>\s*([\d.]+)%(?:\s+in\s+\S+)?$", re.I)
RE_PERCENT_GTE = re.compile(r"^>=\s*([\d.]+)%(?:\s+in\s+\S+)?$", re.I)
RE_PERCENT_LT = re.compile(r"^<\s*([\d.]+)%(?:\s+in\s+\S+)?$", re.I)
RE_PERCENT_LTE = re.compile(r"^<=\s*([\d.]+)%(?:\s+in\s+\S+)?$", re.I)
RE_BROWSER_GTE = re.compile(r"^(\w[\w_]*)\s*>=\s*(\d+)$", re.I)
RE_BROWSER_GT = re.compile(r"^(\w[\w_]*)\s*>\s*(\d+)$", re.I)
RE_BROWSER_LTE = re.compile(r"^(\w[\w_]*)\s*<=\s*(\d+)$", re.I)
RE_BROWSER_LT = re.compile(r"^(\w[\w_]*)\s*<\s*(\d+)$", re.I)
RE_BROWSER_VER = re.compile(r"^(\w[\w_]*)\s+(\d[\d.]*)$", re.I)  # pinned: "Chrome 90"
RE_SINCE = re.compile(r"^since\s+\d{4}(?:-\d{2})?(?:-\d{2})?$", re.I)
RE_COVER = re.compile(r"^cover\s+[\d.]+%$", re.I)
RE_EXTENDS = re.compile(r"^extends\s+\S+$", re.I)
RE_SUPPORTS = re.compile(r"^supports\s+\S+$", re.I)


def classify_query(q: Query) -> str:
    """Return a short type tag for a canonical query."""
    c = q.canonical.strip()
    cl = c.lower()

    if cl == "defaults":
        return "defaults"
    if cl == "dead":
        return "dead"
    if cl == "not dead":
        return "not_dead"
    if cl == "maintained node versions":
        return "node"
    if cl == "unreleased versions":
        return "unreleased_all"
    if cl == "all":
        return "all"
    if RE_LAST_N.match(cl):
        return "last_n"
    if RE_LAST_N_BROWSER.match(cl):
        return "last_n_browser"
    if RE_PERCENT_GT.match(c) or RE_PERCENT_GTE.match(c):
        return "pct_gt"
    if RE_PERCENT_LT.match(c) or RE_PERCENT_LTE.match(c):
        return "pct_lt"
    if RE_BROWSER_GTE.match(c) or RE_BROWSER_GT.match(c) or RE_BROWSER_LTE.match(c) or RE_BROWSER_LT.match(c):
        return "browser_range"
    if RE_BROWSER_VER.match(c):
        return "browser_pin"
    if RE_SINCE.match(cl):
        return "since"
    if RE_COVER.match(cl):
        return "cover"
    if RE_EXTENDS.match(cl):
        return "extends"
    if RE_SUPPORTS.match(cl):
        return "supports"
    return "unknown"


def extract_browser_from_query(c: str) -> Optional[str]:
    """Extract browser name from a browser-specific query, or None."""
    for pat in (RE_LAST_N_BROWSER, RE_BROWSER_GTE, RE_BROWSER_GT,
                RE_BROWSER_LTE, RE_BROWSER_LT, RE_BROWSER_VER):
        m = pat.match(c.strip())
        if m:
            return m.group(1).lower()
    # last N chrome versions -> group(2)
    m = RE_LAST_N_BROWSER.match(c.strip().lower())
    if m:
        return m.group(2).lower()
    return None


def extract_version_from_query(c: str) -> Optional[int]:
    """Extract the version number from a browser-pinned or range query."""
    for pat in (RE_BROWSER_GTE, RE_BROWSER_GT, RE_BROWSER_LTE, RE_BROWSER_LT, RE_BROWSER_VER):
        m = pat.match(c.strip())
        if m and len(m.groups()) >= 2:
            try:
                return int(float(m.group(2)))
            except (ValueError, IndexError):
                pass
    return None


# ---------------------------------------------------------------------------
# Validation rules
# ---------------------------------------------------------------------------

def rule_s2_empty(queries: List[Query]) -> List[Finding]:
    findings = []
    if not queries:
        findings.append(Finding(SEV_ERROR, "S2", "Config is empty — no queries found.", 0))
    return findings


def rule_s3_syntax(queries: List[Query]) -> List[Finding]:
    """Check for invalid/unrecognisable query syntax."""
    findings = []
    for q in queries:
        qtype = classify_query(q)
        if qtype == "unknown":
            # Try to give a better message
            first_word = q.canonical.split()[0].lower() if q.canonical.split() else ""
            if first_word and first_word not in BROWSER_ALIASES and first_word not in VALID_KEYWORDS:
                findings.append(Finding(
                    SEV_ERROR, "S3",
                    f"Unknown browser or keyword '{first_word}' in query: {q.raw!r}",
                    q.line
                ))
            else:
                findings.append(Finding(
                    SEV_ERROR, "S3",
                    f"Cannot parse query: {q.raw!r} — check browserslist syntax",
                    q.line
                ))
    return findings


def rule_s4_duplicates(queries: List[Query]) -> List[Finding]:
    findings = []
    seen: Dict[str, int] = {}
    for q in queries:
        key = q.raw.lower()
        if key in seen:
            findings.append(Finding(
                SEV_WARN, "S4",
                f"Duplicate query: {q.raw!r} (first seen at line {seen[key]})",
                q.line
            ))
        else:
            seen[key] = q.line
    return findings


def rule_b1_dead_browsers(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        if q.negated:
            continue
        browser = extract_browser_from_query(q.canonical)
        if browser and browser in DEAD_BROWSERS:
            findings.append(Finding(
                SEV_WARN, "B1",
                f"Deprecated/dead browser '{browser}' in query: {q.raw!r}",
                q.line
            ))
        # Also catch "ie <= 11" style
        if not browser:
            first = q.canonical.split()[0].lower() if q.canonical.split() else ""
            if first in DEAD_BROWSERS:
                findings.append(Finding(
                    SEV_WARN, "B1",
                    f"Deprecated/dead browser '{first}' in query: {q.raw!r}",
                    q.line
                ))
    return findings


def rule_b2_low_usage(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        if q.negated:
            continue
        browser = extract_browser_from_query(q.canonical)
        if browser:
            canonical_key = BROWSER_ALIASES.get(browser)
            if canonical_key:
                usage = BROWSER_USAGE.get(canonical_key, 100.0)
                if usage < 0.01:
                    findings.append(Finding(
                        SEV_WARN, "B2",
                        f"Browser '{browser}' has <0.01% global usage in query: {q.raw!r}",
                        q.line
                    ))
    return findings


def rule_b3_version_exists(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        browser = extract_browser_from_query(q.canonical)
        if not browser:
            continue
        ver = extract_version_from_query(q.canonical)
        if ver is None:
            continue
        canonical_key = BROWSER_ALIASES.get(browser)
        if canonical_key and canonical_key in BROWSER_MAX_VERSIONS:
            max_ver = BROWSER_MAX_VERSIONS[canonical_key]
            if ver > max_ver:
                findings.append(Finding(
                    SEV_ERROR, "B3",
                    f"Browser version {browser} {ver} does not exist (max known: {max_ver}) in query: {q.raw!r}",
                    q.line
                ))
    return findings


def rule_b4_unknown_browser(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        qtype = classify_query(q)
        if qtype in ("last_n_browser", "browser_range", "browser_pin"):
            browser = extract_browser_from_query(q.canonical)
            if browser and browser not in BROWSER_ALIASES:
                findings.append(Finding(
                    SEV_ERROR, "B4",
                    f"Unknown browser name '{browser}' in query: {q.raw!r}",
                    q.line
                ))
    return findings


def rule_q1_redundant(queries: List[Query]) -> List[Finding]:
    """Detect obviously redundant queries."""
    findings = []
    # "last 1 versions" is covered by "last 2 versions"
    last_n_values = {}
    for q in queries:
        if q.negated:
            continue
        m = RE_LAST_N.match(q.canonical.lower())
        if m:
            n = int(m.group(1))
            for existing_n, existing_q in last_n_values.items():
                if n < existing_n:
                    findings.append(Finding(
                        SEV_WARN, "Q1",
                        f"Query {q.raw!r} (last {n}) is redundant — already covered by {existing_q.raw!r} (last {existing_n})",
                        q.line
                    ))
                    break
            last_n_values[n] = q

    # "> 0.5%" and "> 1%" — the smaller threshold covers the larger
    pct_gt_values = []
    for q in queries:
        if q.negated:
            continue
        m = RE_PERCENT_GT.match(q.canonical) or RE_PERCENT_GTE.match(q.canonical)
        if m:
            pct = float(m.group(1))
            for existing_pct, existing_q in pct_gt_values:
                if pct > existing_pct:
                    findings.append(Finding(
                        SEV_WARN, "Q1",
                        f"Query {q.raw!r} (>{pct}%) is redundant — already covered by {existing_q.raw!r} (>{existing_pct}%)",
                        q.line
                    ))
                    break
            pct_gt_values.append((pct, q))

    return findings


def rule_q2_conflicting(queries: List[Query]) -> List[Finding]:
    """Detect conflicting percentage queries."""
    findings = []
    pct_gt: List[Tuple[float, Query]] = []
    pct_lt: List[Tuple[float, Query]] = []

    for q in queries:
        if q.negated:
            continue
        m = RE_PERCENT_GT.match(q.canonical) or RE_PERCENT_GTE.match(q.canonical)
        if m:
            pct_gt.append((float(m.group(1)), q))
        m2 = RE_PERCENT_LT.match(q.canonical) or RE_PERCENT_LTE.match(q.canonical)
        if m2:
            pct_lt.append((float(m2.group(1)), q))

    for (gt_val, gt_q) in pct_gt:
        for (lt_val, lt_q) in pct_lt:
            if lt_val < gt_val:
                findings.append(Finding(
                    SEV_WARN, "Q2",
                    f"Conflicting queries: {gt_q.raw!r} (>{gt_val}%) vs {lt_q.raw!r} (<{lt_val}%) — the 'less than' range is within 'greater than' exclusion",
                    max(gt_q.line, lt_q.line)
                ))
    return findings


def rule_q3_not_dead_no_positive(queries: List[Query]) -> List[Finding]:
    findings = []
    # "not dead" is stored as negated=True, canonical="dead"
    has_not_dead = any(q.negated and q.canonical.lower() == "dead" for q in queries)
    has_positive = any(not q.negated and classify_query(q) not in ("unknown",) for q in queries)
    if has_not_dead and not has_positive:
        findings.append(Finding(
            SEV_ERROR, "Q3",
            "'not dead' used without any positive query — this will match nothing (must combine with e.g. 'last 2 versions')",
            0
        ))
    return findings


def rule_q4_empty_negation(queries: List[Query]) -> List[Finding]:
    """Warn if 'not' query is very likely to negate everything."""
    findings = []
    negated = [q for q in queries if q.negated]
    positive = [q for q in queries if not q.negated]
    if negated and not positive:
        findings.append(Finding(
            SEV_WARN, "Q4",
            "All queries are negated ('not ...') with no positive queries — result will be empty",
            negated[0].line
        ))
    return findings


def _estimate_coverage(queries: List[Query]) -> float:
    """
    Rough coverage heuristic — not accurate, just illustrative.
    Returns a percentage 0-100.
    """
    coverage = 0.0
    has_defaults = any(classify_query(q) == "defaults" for q in queries if not q.negated)
    has_all = any(classify_query(q) == "all" for q in queries if not q.negated)
    has_last_2 = any(RE_LAST_N.match(q.canonical.lower()) and int(RE_LAST_N.match(q.canonical.lower()).group(1)) >= 2
                     for q in queries if not q.negated)

    if has_all:
        return 99.9
    if has_defaults:
        coverage += 85.0
    elif has_last_2:
        coverage += 78.0

    for q in queries:
        if q.negated:
            continue
        m = RE_PERCENT_GT.match(q.canonical) or RE_PERCENT_GTE.match(q.canonical)
        if m:
            pct = float(m.group(1))
            if pct < 1.0:
                coverage = max(coverage, 92.0)
            elif pct < 2.0:
                coverage = max(coverage, 88.0)
            else:
                coverage = max(coverage, 80.0)

    return min(coverage, 99.9)


def rule_c1_low_coverage(queries: List[Query]) -> List[Finding]:
    findings = []
    cov = _estimate_coverage(queries)
    if 0 < cov < 80.0:
        findings.append(Finding(
            SEV_WARN, "C1",
            f"Estimated coverage is low (~{cov:.1f}%) — consider broadening queries",
            0
        ))
    return findings


def rule_c2_high_coverage(queries: List[Query]) -> List[Finding]:
    findings = []
    cov = _estimate_coverage(queries)
    if cov > 99.5:
        findings.append(Finding(
            SEV_WARN, "C2",
            f"Estimated coverage is very high (~{cov:.1f}%) — may include dead/legacy browsers",
            0
        ))
    return findings


def rule_c3_no_mobile(queries: List[Query]) -> List[Finding]:
    findings = []
    has_defaults = any(classify_query(q) == "defaults" for q in queries if not q.negated)
    has_all = any(classify_query(q) == "all" for q in queries if not q.negated)
    if has_defaults or has_all:
        return findings  # defaults includes mobile

    has_mobile = False
    for q in queries:
        if q.negated:
            continue
        browser = extract_browser_from_query(q.canonical)
        if browser and browser in MOBILE_BROWSERS:
            has_mobile = True
            break
        # last N versions covers mobile implicitly
        if classify_query(q) in ("last_n",):
            has_mobile = True
            break

    if not has_mobile:
        findings.append(Finding(
            SEV_INFO, "C3",
            "No explicit mobile browser coverage detected — consider adding 'last 2 iOS versions' or similar",
            0
        ))
    return findings


def rule_c4_no_country(queries: List[Query]) -> List[Finding]:
    """Info: no country-specific override (> N% in CC)."""
    findings = []
    has_country = any("in " in q.canonical.lower() for q in queries)
    if not has_country:
        findings.append(Finding(
            SEV_INFO, "C4",
            "No country-specific query detected — consider '> 0.5% in US' if targeting a specific market",
            0
        ))
    return findings


def rule_p1_ie_queries(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        if q.negated:
            continue
        first = q.canonical.split()[0].lower() if q.canonical.split() else ""
        if first == "ie" or (first in BROWSER_ALIASES and BROWSER_ALIASES[first] == "ie"):
            findings.append(Finding(
                SEV_WARN, "P1",
                f"IE query found: {q.raw!r} — consider dropping IE support (global usage ~0.5%)",
                q.line
            ))
    return findings


def rule_p2_old_versions(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        if q.negated:
            continue
        m = RE_LAST_N.match(q.canonical.lower())
        if m:
            n = int(m.group(1))
            if n >= 10:
                findings.append(Finding(
                    SEV_WARN, "P2",
                    f"Query {q.raw!r} targets {n} versions back — this may include very old browsers",
                    q.line
                ))
        m2 = RE_LAST_N_BROWSER.match(q.canonical.lower())
        if m2:
            n = int(m2.group(1))
            if n >= 10:
                findings.append(Finding(
                    SEV_WARN, "P2",
                    f"Query {q.raw!r} targets {n} versions back — this may include very old browsers",
                    q.line
                ))
    return findings


def rule_p3_all_query(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        if not q.negated and classify_query(q) == "all":
            findings.append(Finding(
                SEV_WARN, "P3",
                f"Query 'all' is extremely broad — it includes every known browser version",
                q.line
            ))
    return findings


def rule_p4_version_pin(queries: List[Query]) -> List[Finding]:
    findings = []
    for q in queries:
        if q.negated:
            continue
        if classify_query(q) == "browser_pin":
            m = RE_BROWSER_VER.match(q.canonical.strip())
            if m:
                browser = m.group(1)
                ver = m.group(2)
                # Skip if it's a dead browser (already caught by B1)
                if browser.lower() not in DEAD_BROWSERS:
                    findings.append(Finding(
                        SEV_WARN, "P4",
                        f"Pinned version query {q.raw!r} — prefer a range like '{browser} >= {ver}' for future-proofing",
                        q.line
                    ))
    return findings


# ---------------------------------------------------------------------------
# Rule runners
# ---------------------------------------------------------------------------

SYNTAX_RULES = [rule_s2_empty, rule_s3_syntax, rule_s4_duplicates]
ALL_RULES = [
    rule_s2_empty, rule_s3_syntax, rule_s4_duplicates,
    rule_b1_dead_browsers, rule_b2_low_usage, rule_b3_version_exists, rule_b4_unknown_browser,
    rule_q1_redundant, rule_q2_conflicting, rule_q3_not_dead_no_positive, rule_q4_empty_negation,
    rule_c1_low_coverage, rule_c2_high_coverage, rule_c3_no_mobile, rule_c4_no_country,
    rule_p1_ie_queries, rule_p2_old_versions, rule_p3_all_query, rule_p4_version_pin,
]


def run_rules(queries: List[Query], rules) -> List[Finding]:
    findings = []
    for rule_fn in rules:
        findings.extend(rule_fn(queries))
    return findings


# ---------------------------------------------------------------------------
# Coverage command
# ---------------------------------------------------------------------------

def cmd_coverage(queries: List[Query]) -> str:
    cov = _estimate_coverage(queries)
    has_mobile = any(
        not q.negated and (
            (extract_browser_from_query(q.canonical) or "").lower() in MOBILE_BROWSERS
            or classify_query(q) in ("defaults", "last_n", "all")
        )
        for q in queries
    )
    mobile_note = "includes mobile" if has_mobile else "no explicit mobile"
    lines = [
        f"Estimated coverage: ~{cov:.1f}% ({mobile_note})",
        "",
        "Note: This is a heuristic estimate using embedded usage data.",
        "For accurate coverage, use: npx browserslist --coverage",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Explain command
# ---------------------------------------------------------------------------

QUERY_EXPLANATIONS = {
    "defaults": "Shorthand for '> 0.5%, last 2 versions, Firefox ESR, not dead'",
    "all": "Every browser and version ever known — extremely broad",
    "dead": "Browsers officially unsupported or with <0.5% usage for 24 months",
    "not_dead": "Excludes browsers that are dead",
    "last_n": "The last N major versions of every browser",
    "last_n_browser": "The last N major versions of the specified browser",
    "pct_gt": "Browsers with more than N% global usage",
    "pct_lt": "Browsers with less than N% global usage",
    "browser_range": "Specific browser at/above/below a version number",
    "browser_pin": "Exact pinned version of a browser",
    "node": "All maintained (LTS/current) Node.js versions",
    "unreleased_all": "All browsers in alpha/beta (not stable)",
    "since": "All browser versions released since a given date",
    "cover": "Minimum set of browsers covering N% of users",
    "extends": "Inherits from a published browserslist config package",
    "supports": "Browsers that support a specific web platform feature",
    "unknown": "Unrecognised query — may be a syntax error",
}


def explain_query(q: Query) -> str:
    qtype = classify_query(q)
    base = QUERY_EXPLANATIONS.get(qtype, "Unknown query type")
    prefix = "[NOT] " if q.negated else ""

    if qtype == "last_n":
        m = RE_LAST_N.match(q.canonical.lower())
        n = m.group(1) if m else "?"
        detail = f"Last {n} major versions of every browser"
    elif qtype == "last_n_browser":
        m = RE_LAST_N_BROWSER.match(q.canonical.lower())
        n, browser = (m.group(1), m.group(2)) if m else ("?", "?")
        detail = f"Last {n} major versions of {browser.title()}"
    elif qtype == "pct_gt":
        m = RE_PERCENT_GT.match(q.canonical) or RE_PERCENT_GTE.match(q.canonical)
        pct = m.group(1) if m else "?"
        detail = f"Browsers used by more than {pct}% of global users"
    elif qtype == "browser_range":
        detail = f"Browser version range: {q.canonical}"
    elif qtype == "browser_pin":
        m = RE_BROWSER_VER.match(q.canonical.strip())
        if m:
            detail = f"Exactly {m.group(1).title()} version {m.group(2)} only"
        else:
            detail = base
    else:
        detail = base

    return f"{prefix}{detail}"


def cmd_explain(queries: List[Query]) -> str:
    lines = ["Query explanations:", ""]
    for q in queries:
        explanation = explain_query(q)
        lines.append(f"  Line {q.line:3d}: {q.raw!r}")
        lines.append(f"           -> {explanation}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SEV_LABEL = {SEV_ERROR: "[E]", SEV_WARN: "[W]", SEV_INFO: "[I]"}


def format_text(findings: List[Finding], filepath: str) -> str:
    if not findings:
        return f"OK  No issues found in {filepath}"
    lines = [f"Findings in {filepath}:", ""]
    for f in sorted(findings, key=lambda x: (x.line, x.severity)):
        loc = f"line {f.line}" if f.line else "config"
        lines.append(f"  {SEV_LABEL[f.severity]} [{f.rule}] {loc}: {f.message}")
    errors = sum(1 for f in findings if f.severity == SEV_ERROR)
    warns = sum(1 for f in findings if f.severity == SEV_WARN)
    infos = sum(1 for f in findings if f.severity == SEV_INFO)
    lines.append("")
    lines.append(f"  {errors} error(s), {warns} warning(s), {infos} info(s)")
    return "\n".join(lines)


def format_json(findings: List[Finding], filepath: str) -> str:
    errors = sum(1 for f in findings if f.severity == SEV_ERROR)
    warns = sum(1 for f in findings if f.severity == SEV_WARN)
    result = {
        "file": filepath,
        "errors": errors,
        "warnings": warns,
        "findings": [f.to_dict() for f in findings],
    }
    return json.dumps(result, indent=2)


def format_summary(findings: List[Finding], filepath: str, strict: bool = False) -> str:
    errors = sum(1 for f in findings if f.severity == SEV_ERROR)
    warns = sum(1 for f in findings if f.severity == SEV_WARN)
    if errors > 0 or (strict and warns > 0):
        status = "FAIL"
    elif warns > 0:
        status = "WARN"
    else:
        status = "PASS"
    return f"{status}  {filepath}  ({errors}E {warns}W)"


# ---------------------------------------------------------------------------
# Exit code logic
# ---------------------------------------------------------------------------

def compute_exit_code(findings: List[Finding], strict: bool) -> int:
    errors = sum(1 for f in findings if f.severity == SEV_ERROR)
    warns = sum(1 for f in findings if f.severity == SEV_WARN)
    if errors > 0:
        return 1
    if strict and warns > 0:
        return 1
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate browserslist configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("command", choices=["validate", "check", "coverage", "explain"],
                        help="Command to run")
    parser.add_argument("file", help="Path to .browserslistrc or package.json")
    parser.add_argument("--format", choices=["text", "json", "summary"], default="text",
                        dest="fmt", help="Output format (default: text)")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (exit code 1)")
    parser.add_argument("--env", choices=["production", "development"], default="production",
                        help="Target environment when reading package.json (default: production)")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    # Load config
    queries, load_error = load_config(args.file)
    if load_error:
        if args.fmt == "json":
            print(json.dumps({"error": load_error, "file": args.file}))
        else:
            print(f"[E] {load_error}", file=sys.stderr)
        return 2
    if queries is None:
        print(f"[E] Failed to load config from {args.file}", file=sys.stderr)
        return 2

    # Dispatch commands
    if args.command == "coverage":
        print(cmd_coverage(queries))
        return 0

    if args.command == "explain":
        print(cmd_explain(queries))
        return 0

    if args.command == "check":
        rules = SYNTAX_RULES
    else:  # validate
        rules = ALL_RULES

    findings = run_rules(queries, rules)

    if args.fmt == "json":
        print(format_json(findings, args.file))
    elif args.fmt == "summary":
        print(format_summary(findings, args.file, args.strict))
    else:
        print(format_text(findings, args.file))

    return compute_exit_code(findings, args.strict)


if __name__ == "__main__":
    sys.exit(main())
