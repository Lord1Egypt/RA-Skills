#!/usr/bin/env python3
"""
provenance_verify.py — guard that every hard number in a China-target
banker markdown deliverable has a matching row in the companion
data-provenance.md tracking table.

Context: Rule 5 of the cn-client-investigation skill says every hard
number (revenue, valuation, margin, market cap, etc.) must be backed by
at least one cited source. This script is the automated gate.

Usage:
    python3 provenance_verify.py <analysis.md> <data-provenance.md>
    # exit 0 → clean (every hard number cross-references a provenance row)
    # exit 1 → one or more hard numbers are missing a provenance row

Assumptions:
    - <analysis.md>       is the primary banker markdown draft
    - <data-provenance.md> is a markdown file containing a table whose
      rows list one hard number each; the script scans every non-header
      row and collects the numeric tokens in any cell

"Hard number" here means a number immediately followed by a banker unit:
    亿 万 % RMB USD 元 CNY HKD  (also the English shorthand M / B and 亿元)

The comparison is deliberately coarse: if a hard-number token appears
verbatim in any row of the provenance table, it is considered covered.
Rows in the provenance table that are themselves the column-header line
(first row with "----" below it) are skipped.

This script is intended to be part of the Phase 5 QA pass in the
cn-client-investigation skill, and it can also be wired into CI if the
deliverable is checked into a repo.
"""
from __future__ import annotations
import pathlib
import re
import sys
from typing import Iterable

from _shared import find_precision_drift


# --- Regex: the hard-number pattern we flag ---
# A digit run (with optional decimal) followed (possibly after one space)
# by one of the banker units below.
# NOTE: `HARD_NUMBER` + `normalize_variants` + `extract_provenance_corpus`
# are also imported by slide_data_audit.py to keep matching semantics
# consistent between analysis.md and .pptx slide gates. Changing the
# regex here propagates to both scanners by design.
UNITS = r"(?:亿元|亿|万|%|元|RMB|USD|CNY|HKD|M|B)"
# Allow any digit run (no 3-cap) so "1500亿元" captures as 1500, not 500.
# Thousands separators are still handled by the optional `(?:,\d{3})*` group.
NUM_CORE = r"\d+(?:,\d{3})*(?:\.\d+)?"
HARD_NUMBER = re.compile(rf"({NUM_CORE})\s*({UNITS})")


# Lines containing these tags are explicitly non-MCP-sourced estimates
# (peer comparisons, rough sector consensus, "not yet verified") — the
# banker-memo skill mandates the `[EST, per sector consensus]` tag on
# every such value. Skipping them from provenance-coverage checks is
# semantically correct: they were never intended to be MCP-sourced.
EST_TAGS = ("[EST", "[未核实]", "[估算]", "per sector consensus", "estimate]")


def _is_estimate_line(line: str) -> bool:
    return any(tag in line for tag in EST_TAGS)


def extract_hard_numbers(text: str) -> list[tuple[int, str, str, str]]:
    """
    Return [(line_no, number, unit, line_snippet), ...] for every hard
    number found in `text`. Skips lines tagged as `[EST]` / estimate —
    those are not required to have provenance entries.
    """
    hits: list[tuple[int, str, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if _is_estimate_line(line):
            continue
        for m in HARD_NUMBER.finditer(line):
            hits.append((lineno, m.group(1), m.group(2), line.strip()[:120]))
    return hits


def extract_provenance_corpus(prov_text: str) -> str:
    """
    Flatten the provenance markdown to a single string the script can
    substring-search. We don't try to parse the markdown table, because
    provenance tables come in varying shapes — a raw flatten is enough
    for the coarse existence check this gate performs.
    """
    # Strip markdown table separators and pipes so "15.2 亿RMB" matches
    # against "| 15.2 | 亿RMB |" style cells.
    cleaned = prov_text.replace("|", " ").replace("---", " ")
    # Collapse runs of whitespace.
    return re.sub(r"\s+", " ", cleaned)


def normalize_variants(num: str, unit: str) -> tuple[list[str], list[str]]:
    """
    Return (unit_attached_variants, bare_number_variants).

    Unit-attached variants are the strong signal and always checked.
    Bare-number variants are a fallback only used when the unit token also
    appears somewhere in the provenance corpus — they're noisier so the
    verifier applies them last.

    Covers:
      - exact "15.2 亿RMB"
      - without space "15.2亿RMB"
      - common comma-thousands variation (strip commas)
      - cross-unit equivalences (亿元 ↔ 万元 ↔ 元 ↔ 亿 ↔ 万) so a markdown
        claim of "1476.94 亿元" matches a provenance row citing
        "14,769,400 万元" (banker reports routinely mix 万元/亿元 scales
        between analysis text and underlying Tushare / CNINFO tables).
    """
    unit_attached: set[str] = set()
    bare: set[str] = set()

    base = num
    no_commas = num.replace(",", "")
    for n in {base, no_commas}:
        unit_attached.add(f"{n}{unit}")
        unit_attached.add(f"{n} {unit}")
        bare.add(n)

    # Unit equivalences — convert numeric value into companion-unit form and
    # add those as search candidates. Only kicks in for units that have a
    # well-defined scalar multiple.
    try:
        value = float(no_commas)
    except ValueError:
        return list(unit_attached), list(bare)

    equivalents: list[tuple[float, str]] = []
    if unit == "亿元":
        # 1亿元 = 10000 万元 = 1e8 元
        equivalents = [(value * 10000, "万元"), (value * 1e8, "元")]
    elif unit == "万元":
        # 1万元 = 0.0001 亿元 = 10000 元
        equivalents = [(value / 10000, "亿元"), (value * 10000, "元")]
    elif unit == "元":
        equivalents = [(value / 1e8, "亿元"), (value / 10000, "万元")]
    elif unit == "亿":
        equivalents = [(value * 10000, "万"), (value * 1e8, "")]
    elif unit == "万":
        equivalents = [(value / 10000, "亿"), (value * 10000, "")]

    for v, u in equivalents:
        if v <= 0:
            continue
        is_whole = v == int(v)
        # Integer form + comma-thousands form + decimal form. Banker
        # provenance tables encode the same number in several textual
        # variants, so we emit all of them.
        whole_int = int(v) if is_whole else None
        if is_whole:
            unit_attached.add(f"{whole_int}{u}")
            unit_attached.add(f"{whole_int} {u}")
            try:
                unit_attached.add(f"{whole_int:,}{u}")
                unit_attached.add(f"{whole_int:,} {u}")
            except (OverflowError, ValueError):
                pass
        else:
            unit_attached.add(f"{v:g}{u}")
            unit_attached.add(f"{v:g} {u}")
            unit_attached.add(f"{v:.2f}{u}")
            unit_attached.add(f"{v:.2f} {u}")
    return list(unit_attached), list(bare)


def verify(
    analysis_text: str,
    provenance_text: str,
) -> tuple[int, list[str]]:
    """Return (missing_count, messages)."""
    hits = extract_hard_numbers(analysis_text)
    if not hits:
        return 0, ["OK: no hard numbers found in analysis.md — nothing to verify"]

    corpus = extract_provenance_corpus(provenance_text)

    missing: list[str] = []
    covered_count = 0

    for lineno, num, unit, snippet in hits:
        unit_variants, bare_variants = normalize_variants(num, unit)
        unit_ok = unit in corpus
        # Primary check: any unit-attached variant present anywhere in corpus.
        num_ok = any(v in corpus for v in unit_variants)
        if num_ok:
            covered_count += 1
            continue
        # Fallback: bare number appears AND matching unit token also appears
        # (not necessarily adjacent) — soft match, useful when the provenance
        # table encodes number and unit in separate table cells.
        if unit_ok and any(v in corpus for v in bare_variants):
            covered_count += 1
            continue
        missing.append(
            f"L{lineno:>4}: hard number '{num}{unit}' missing from data-provenance.md"
            f"\n       context: {snippet!r}"
        )

    total = len(hits)
    summary = [
        f"scan: {total} hard numbers in analysis.md; "
        f"{covered_count} covered, {len(missing)} missing."
    ]
    return len(missing), summary + missing


# -----------------------------------------------------------------------------
# Strict-mode additions (US-001 data-text-accuracy-20260419):
#
# Goal: catch the 海天味业 / 五粮液 failure mode where analysis.md claims a
# number with an estimate marker (`~22.9%`, `约 1.34 元`, `估算 XXX`) yet the
# companion data-provenance.md row attributes the value to a Tier-1 source
# (Tushare / 巨潮 / 交易所 / East Money) — i.e. estimate-as-T1 smuggling.
#
# In strict mode, every hard number that sits within an estimate-marker
# window MUST have its provenance row status/source cell contain one of
# the derivation markers (`估算`, `推算`, `derived`, `computed`, `analyst
# estimate`, `ESTIMATED`, `DERIVED`). Otherwise the scanner fails with a
# line-level report.
#
# Strict mode also reports (as a WARN, not FAIL) when the same metric
# appears at multiple precisions in the analysis markdown, because
# precision drift is a correctness smell on its own (e.g. "22.9%" and
# "22.92%" in different paragraphs for the same ROE figure).

# Tokens that immediately flag a hard number as an agent estimate /
# derivation rather than a verbatim source value. Case-sensitive for
# ASCII tokens; Chinese are always case-literal anyway.
ESTIMATE_MARKERS = (
    "~",
    "约",
    "大约",
    "估算",
    "粗估",
    "推算",
    "approximately",
    "approx.",
    "est.",
    "≈",
)

# Tokens that, if present in the provenance row that contains a matching
# hard number, certify the value is INTENTIONALLY labelled as an agent-
# derived value (so strict mode does NOT fail on it).
DERIVATION_MARKERS = (
    "估算",
    "推算",
    "derived",
    "Derived",
    "DERIVED",
    "computed",
    "Computed",
    "analyst estimate",
    "Analyst estimate",
    "ESTIMATED",
    "[ESTIMATED]",
    "[DERIVED]",
)


def find_estimate_hits(analysis_text: str) -> list[tuple[int, str, str, str]]:
    """Return [(lineno, number, unit, snippet), ...] for hard numbers that
    sit within ~8 chars of an estimate marker on the same line."""
    hits: list[tuple[int, str, str, str]] = []
    for lineno, line in enumerate(analysis_text.splitlines(), 1):
        for m in HARD_NUMBER.finditer(line):
            win_start = max(0, m.start() - 8)
            win_end = min(len(line), m.end() + 8)
            window = line[win_start:win_end]
            if any(tok in window for tok in ESTIMATE_MARKERS):
                hits.append(
                    (lineno, m.group(1), m.group(2), line.strip()[:120])
                )
    return hits


def find_provenance_line_for(
    provenance_text: str, num: str, unit: str
) -> str | None:
    """Find the provenance row that best matches ``num+unit``.

    Preference order (stronger match wins; within a tier, a row marked
    with a DERIVATION_MARKERS keyword wins over an unmarked row so the
    strict-mode estimate check doesn't false-FAIL on author-tagged rows):

    1. ``{num}{unit}`` appears as a contiguous substring (e.g. ``1.34元``)
    2. ``{num} {unit}`` with a space between (e.g. ``1.34 元``)
    3. Bare-number + unit both appear somewhere in the row, but the
       number token isn't adjacent to the unit — soft match only used
       when stronger matches are absent.

    Returns ``None`` when no row matches any tier.
    """
    needle = f"{num}{unit}"
    needle_spaced = f"{num} {unit}"
    bare_num = num.replace(",", "")
    lines = provenance_text.splitlines()

    def _best_of(candidates: list[str]) -> str | None:
        """Prefer a row explicitly labelled as derived/estimated."""
        if not candidates:
            return None
        for raw in candidates:
            if any(tok in raw for tok in DERIVATION_MARKERS):
                return raw
        return candidates[0]

    tier1 = [raw for raw in lines if needle in raw]
    if tier1:
        return _best_of(tier1)
    tier2 = [raw for raw in lines if needle_spaced in raw]
    if tier2:
        return _best_of(tier2)
    tier3 = [raw for raw in lines if bare_num in raw and unit in raw]
    if tier3:
        return _best_of(tier3)
    return None


def precision_scan(analysis_text: str) -> list[str]:
    """Thin wrapper: delegate to _shared.find_precision_drift using this
    script's HARD_NUMBER regex (which covers the banker-unit set)."""
    return find_precision_drift(analysis_text, HARD_NUMBER)


def strict_verify(
    analysis_text: str, provenance_text: str
) -> tuple[int, list[str], list[str]]:
    """Return (strict_violation_count, violation_messages, precision_warnings)."""
    est_hits = find_estimate_hits(analysis_text)
    violations: list[str] = []
    for lineno, num, unit, snippet in est_hits:
        prov_line = find_provenance_line_for(provenance_text, num, unit)
        if prov_line is None:
            continue
        has_derivation = any(tok in prov_line for tok in DERIVATION_MARKERS)
        if not has_derivation:
            violations.append(
                f"L{lineno:>4}: hard number '{num}{unit}' has estimate marker in "
                f"analysis but provenance row does NOT label it as estimated/derived"
                f"\n       analysis:    {snippet!r}"
                f"\n       provenance:  {prov_line.strip()[:140]!r}"
                f"\n       fix: mark the provenance row source with "
                f"[ESTIMATED] / [DERIVED] / 估算 / 推算, or resolve the "
                f"analysis value to the exact source-returned value."
            )
    precision_warnings = precision_scan(analysis_text)
    return len(violations), violations, precision_warnings


def main(argv: list[str]) -> int:
    strict = False
    args = list(argv[1:])
    if "--strict" in args:
        strict = True
        args.remove("--strict")
    if len(args) != 2:
        print(
            "usage: provenance_verify.py [--strict] <analysis.md> <data-provenance.md>",
            file=sys.stderr,
        )
        return 2
    analysis_p = pathlib.Path(args[0])
    prov_p = pathlib.Path(args[1])
    for p in (analysis_p, prov_p):
        if not p.exists():
            print(f"file not found: {p}", file=sys.stderr)
            return 2
    analysis_text = analysis_p.read_text(encoding="utf-8", errors="replace")
    prov_text = prov_p.read_text(encoding="utf-8", errors="replace")

    missing, messages = verify(analysis_text, prov_text)
    header = messages[0]
    details = messages[1:]
    base_fail = missing > 0

    strict_fail = False
    if strict:
        s_count, s_msgs, s_warns = strict_verify(analysis_text, prov_text)
        if s_count > 0:
            strict_fail = True
            print(
                f"FAIL (--strict): {s_count} estimate-marker hard number(s) "
                f"missing derivation label in provenance.",
                file=sys.stderr,
            )
            for m in s_msgs:
                print(m, file=sys.stderr)
        if s_warns:
            print(
                f"WARN (--strict precision): {len(s_warns)} precision-drift "
                f"group(s) detected (non-blocking):",
                file=sys.stderr,
            )
            for w in s_warns:
                print(f"  - {w}", file=sys.stderr)

    if base_fail:
        print(f"FAIL: {header}", file=sys.stderr)
        for m in details:
            print(m, file=sys.stderr)
        return 1
    if strict_fail:
        return 1

    print(f"OK: {header}")
    if strict:
        print("OK: --strict estimate-label check clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
