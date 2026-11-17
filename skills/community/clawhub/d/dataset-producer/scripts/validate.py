#!/usr/bin/env python3
"""
validate.py — Standalone validation suite for raw dataset rows.

Runs schema conformance, dedup, PII scan, contamination check, length stats,
and language ID on raw JSONL/CSV/TSV data BEFORE sharding. Use this before
running produce_dataset.py — fixing schema issues after sharding is painful.

USAGE
-----
    python validate.py \
        --input raw.jsonl \
        --features features.json \
        --check schema,dedup,pii,length

Run all checks (default):

    python validate.py --input raw.jsonl --features features.json

Available checks:
  schema        — every row matches the declared Features (required)
  dedup         — exact-dedup on a canonical JSON hash; reports duplicate rate
  pii           — regex scan for emails, phone numbers, SSNs, credit cards
  length        — min/p25/median/p75/max length for text fields
  language      — fastText LID if available; flags low-confidence rows
  contamination — scan for known benchmark prompts (MMLU, GSM8K, HumanEval)
  classlabel    — for ClassLabel fields, check that values are in range

Use --pii-contextual to also include patterns that are PII only in context
(IPv4 addresses, ISO dates, US ZIP codes). These are NOT included by default
because they have a high false-positive rate in normal text.

OUTPUT
------
Prints a summary report to stdout. Exits with code 0 if all critical checks
pass, 1 otherwise.

PII and contamination findings are flagged for review but do not auto-fail
the validation — the user decides whether to redact / drop / keep. Use
--strict to make any high-risk PII or contamination finding non-zero-exit.
"""

import argparse
import hashlib
import json
import re
import sys
import statistics
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import Counter

# Reuse the feature loader and CSV coercion from produce_dataset.py
sys.path.insert(0, str(Path(__file__).parent))
try:
    from produce_dataset import load_rows, load_features
except ImportError as e:
    print(f"ERROR: cannot import from produce_dataset.py: {e}", file=sys.stderr)
    sys.exit(1)

try:
    from datasets import Features, Value, Sequence, ClassLabel
except ImportError:
    print("ERROR: install datasets:  pip install datasets pyarrow", file=sys.stderr)
    sys.exit(1)


# ─── PII patterns ───────────────────────────────────────────────────────────
#
# Two tiers:
#   - Default (always-on): patterns that are unambiguously PII in any
#     context — email addresses, US phone numbers, US SSNs, credit-card
#     numbers.
#   - Contextual (opt-in via --pii-contextual): patterns that are PII only
#     in specific contexts — IPv4 addresses, ISO dates, US ZIP codes. These
#     have a high false-positive rate in normal text (dates are everywhere,
#     ZIP codes appear in addresses, IPs are common in logs), so they're
#     off by default.

DEFAULT_PII_PATTERNS = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "us_phone": re.compile(r"\b(\+?1[-.\s]?)?(\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b"),
    "us_ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
}

CONTEXTUAL_PII_PATTERNS = {
    "us_zip": re.compile(r"\b\d{5}(?:-\d{4})?\b"),
    "ipv4":   re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "iso_date": re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
}

# Patterns that ALWAYS warrant review (the others are contextual)
HIGH_RISK_PII = {"us_ssn", "credit_card"}


# ─── Contamination fingerprints ────────────────────────────────────────────
#
# A handful of distinctive prompts from common benchmarks. Real contamination
# scanning uses full prompt sets; these are tripwires. If any tripwire fires,
# you should consider running a more thorough contamination scan.

CONTAMINATION_TRIGGERS = {
    "gsm8k": [
        "Janet's ducks lay 16 eggs per day",                     # GSM8K q1
        "A robe takes 2 bolts of blue fiber and half that much white fiber",  # q2
    ],
    "mmlu": [
        "Which of the following is a primary lesion",            # MMLU anatomy
        "In a chemical reaction, which is true of a catalyst",  # MMLU chemistry
    ],
    "humaneval": [
        "def has_close_elements",                                # HumanEval 0
        "def truncate_number",                                   # HumanEval 1
    ],
}


# ─── Schema validation ──────────────────────────────────────────────────────

def validate_schema(rows: List[Dict[str, Any]], features: Features) -> Tuple[bool, List[str]]:
    """Check that every row matches the Features. Returns (ok, errors)."""
    errors: List[str] = []
    ok = True

    feature_names = set(features.keys())
    for i, row in enumerate(rows):
        row_keys = set(row.keys())
        # Missing fields
        missing = feature_names - row_keys
        if missing:
            errors.append(f"Row {i}: missing fields: {sorted(missing)}")
            ok = False
            if len(errors) > 50:
                errors.append("... (too many errors, truncating)")
                break
            continue
        # Extra fields (warn, don't fail)
        extra = row_keys - feature_names
        if extra:
            errors.append(f"Row {i}: extra fields (will be dropped): {sorted(extra)}")
        # Type-check (lightweight — heavy lifting is done by datasets on convert)
        for name, feat in features.items():
            val = row.get(name)
            if val is None:
                # Allow None for nullable fields (all HF Value types are
                # nullable by default)
                continue
            if isinstance(feat, Value):
                # NOTE: bool is a subclass of int in Python — check bool FIRST
                # so a `True` value doesn't silently pass the int type check.
                if feat.dtype == "string" and not isinstance(val, str):
                    errors.append(f"Row {i}.{name}: expected string, got {type(val).__name__}")
                    ok = False
                elif feat.dtype in ("int32", "int64", "uint32", "uint64") and (
                        not isinstance(val, int) or isinstance(val, bool)):
                    errors.append(f"Row {i}.{name}: expected int, got {type(val).__name__}")
                    ok = False
                elif feat.dtype in ("float32", "float64") and not isinstance(val, (int, float)):
                    errors.append(f"Row {i}.{name}: expected float, got {type(val).__name__}")
                    ok = False
                elif feat.dtype == "bool" and not isinstance(val, bool):
                    errors.append(f"Row {i}.{name}: expected bool, got {type(val).__name__}")
                    ok = False
            elif isinstance(feat, ClassLabel):
                if isinstance(val, int) and not (0 <= val < len(feat.names)):
                    errors.append(f"Row {i}.{name}: ClassLabel value {val} out of range [0, {len(feat.names)})")
                    ok = False
                elif isinstance(val, str) and val not in feat.names:
                    errors.append(f"Row {i}.{name}: ClassLabel string {val!r} not in names {feat.names}")
                    ok = False
            elif isinstance(feat, Sequence):
                if not isinstance(val, list):
                    errors.append(f"Row {i}.{name}: expected list, got {type(val).__name__}")
                    ok = False
        if len(errors) > 50:
            errors.append("... (too many errors, truncating)")
            break
    return ok, errors


# ─── Dedup ──────────────────────────────────────────────────────────────────

def canonical_hash(row: Dict[str, Any]) -> str:
    """Stable hash of a row, ignoring key order."""
    return hashlib.sha256(
        json.dumps(row, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()


def check_dedup(rows: List[Dict[str, Any]]) -> Tuple[int, int, List[str]]:
    """Returns (n_unique, n_dupes, sample_dupe_keys)."""
    seen: Set[str] = set()
    dupes = 0
    sample_dupe_keys: List[str] = []
    for row in rows:
        h = canonical_hash(row)
        if h in seen:
            dupes += 1
            if len(sample_dupe_keys) < 5:
                sample_dupe_keys.append(h[:16])
        else:
            seen.add(h)
    return len(seen), dupes, sample_dupe_keys


# ─── PII ────────────────────────────────────────────────────────────────────

def _luhn_ok(digits: str) -> bool:
    """Luhn checksum validation for a digit string (spaces/hyphens stripped)."""
    digits = digits.replace(" ", "").replace("-", "")
    if not digits.isdigit() or len(digits) < 13:
        return False
    total = 0
    parity = len(digits) % 2
    for i, ch in enumerate(digits):
        d = int(ch)
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


def scan_pii(rows: List[Dict[str, Any]],
             include_contextual: bool = False) -> Dict[str, List[Tuple[int, str, str]]]:
    """Scan all string fields for PII patterns. Returns findings dict.

    Reports ALL PII types found in a field (the previous implementation broke
    after the first match, missing e.g. SSNs in a field that also had an email).

    Credit-card matches are Luhn-validated before being reported: a bare run
    of 13-16 digits is usually an order ID / serial number, and the Luhn
    checksum separates real card numbers from coincidental digit runs.
    """
    patterns = dict(DEFAULT_PII_PATTERNS)
    if include_contextual:
        patterns.update(CONTEXTUAL_PII_PATTERNS)
    findings: Dict[str, List[Tuple[int, str, str]]] = {k: [] for k in patterns}
    for i, row in enumerate(rows):
        for field, val in row.items():
            if not isinstance(val, str):
                continue
            for pii_type, pattern in patterns.items():
                for m in pattern.finditer(val):
                    if pii_type == "credit_card" and not _luhn_ok(m.group()):
                        continue  # digit run fails Luhn — likely an ID, not a card
                    findings[pii_type].append((i, field, m.group()))
                    break  # one match per type per field is enough; other PII
                           # types in the same field are still scanned below
    return findings


# ─── Length stats ───────────────────────────────────────────────────────────

def _percentile(sorted_values: List[int], p: float) -> int:
    """Compute the p-th percentile (0 ≤ p ≤ 100) of a sorted list using
    linear interpolation between adjacent values. Matches numpy.percentile
    with `method='linear'` (the default).
    """
    if not sorted_values:
        return 0
    if len(sorted_values) == 1:
        return sorted_values[0]
    n = len(sorted_values)
    # Index position (0-indexed) — same formula numpy uses
    pos = (p / 100.0) * (n - 1)
    lower = int(pos)
    upper = min(lower + 1, n - 1)
    frac = pos - lower
    return int(round(sorted_values[lower] * (1 - frac) + sorted_values[upper] * frac))


def length_stats(rows: List[Dict[str, Any]], features: Features) -> Dict[str, Dict[str, Any]]:
    """For each text field, compute min/p25/median/p75/max length.

    Uses linear interpolation for percentiles (matches numpy.percentile default).
    """
    result: Dict[str, Dict[str, Any]] = {}
    for name, feat in features.items():
        if not isinstance(feat, Value) or feat.dtype != "string":
            continue
        lengths = []
        for row in rows:
            v = row.get(name)
            if isinstance(v, str):
                lengths.append(len(v))
        if not lengths:
            continue
        lengths.sort()
        n = len(lengths)
        result[name] = {
            "count": n,
            "min": lengths[0],
            "p25": _percentile(lengths, 25),
            "median": _percentile(lengths, 50),
            "p75": _percentile(lengths, 75),
            "max": lengths[-1],
            "empty_count": sum(1 for x in lengths if x == 0),
        }
    return result


# ─── Language ID (optional, requires fasttext) ─────────────────────────────

def check_language(rows: List[Dict[str, Any]], features: Features) -> Optional[Dict[str, Any]]:
    """Run fastText LID on text fields if available. Returns None if unavailable."""
    try:
        import fasttext
        model_path = Path("/tmp/lid.176.bin")
        if not model_path.exists():
            # Don't auto-download (50MB); just skip
            return None
        model = fasttext.load_model(str(model_path))
    except Exception:
        return None

    # Pick the largest text field for LID
    text_fields = [name for name, feat in features.items()
                   if isinstance(feat, Value) and feat.dtype == "string"]
    if not text_fields:
        return None

    lang_counts: Counter = Counter()
    low_conf_count = 0
    for row in rows:
        # Concatenate text fields for a representative sample
        text = " ".join(str(row.get(f, "")) for f in text_fields)[:500]
        if not text.strip():
            continue
        pred = model.predict(text, k=1)
        lang = pred[0][0].replace("__label__", "")
        score = pred[1][0]
        lang_counts[lang] += 1
        if score < 0.7:
            low_conf_count += 1

    return {
        "top_languages": lang_counts.most_common(10),
        "low_confidence_count": low_conf_count,
        "total_scanned": sum(lang_counts.values()),
    }


# ─── Contamination check ────────────────────────────────────────────────────

def check_contamination(rows: List[Dict[str, Any]]) -> Dict[str, List[int]]:
    """Scan text fields for known benchmark prompts. Returns {bench: [row_indices]}."""
    findings: Dict[str, List[int]] = {bench: [] for bench in CONTAMINATION_TRIGGERS}
    for i, row in enumerate(rows):
        text_blob = " ".join(str(v) for v in row.values() if isinstance(v, str)).lower()
        for bench, triggers in CONTAMINATION_TRIGGERS.items():
            for trigger in triggers:
                if trigger.lower() in text_blob:
                    findings[bench].append(i)
                    break  # one trigger per benchmark per row is enough
    return findings


# ─── ClassLabel balance ────────────────────────────────────────────────────

def classlabel_balance(rows: List[Dict[str, Any]], features: Features) -> Dict[str, Dict[str, Any]]:
    """For ClassLabel fields, compute the value distribution."""
    result: Dict[str, Dict[str, Any]] = {}
    for name, feat in features.items():
        if not isinstance(feat, ClassLabel):
            continue
        counts: Counter = Counter()
        for row in rows:
            v = row.get(name)
            if isinstance(v, int):
                try:
                    counts[feat.int2str(v)] += 1
                except Exception:
                    counts[f"<int:{v}>"] += 1
            elif isinstance(v, str):
                counts[v] += 1
        if not counts:
            continue
        most = counts.most_common(1)[0][1]
        least = counts.most_common()[-1][1]
        result[name] = {
            "distribution": dict(counts),
            "imbalance_ratio": (most / least) if least > 0 else float("inf"),
        }
    return result


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Validate raw dataset rows.")
    parser.add_argument("--input", required=True, help="Input .jsonl / .json / .csv / .tsv")
    parser.add_argument("--features", required=True, help="features.json path")
    parser.add_argument("--check", default="schema,dedup,pii,length,classlabel,contamination,language",
                        help="Comma-separated list of checks to run")
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on any PII/contamination finding (default: warn only)")
    parser.add_argument("--pii-contextual", action="store_true",
                        help="Include contextual PII patterns (us_zip, ipv4, iso_date) — "
                             "high false-positive rate, off by default")
    args = parser.parse_args()

    checks = [c.strip() for c in args.check.split(",") if c.strip()]

    print(f"Loading features from: {args.features}")
    features = load_features(args.features)

    print(f"Loading rows from: {args.input}")
    # Pass features so CSV/TSV string cells are coerced to declared dtypes
    # (without this, every numeric column in a CSV fails the schema check)
    rows = load_rows(args.input, features=features)
    print(f"  Loaded {len(rows)} rows")
    print()

    critical_failure = False
    warnings: List[str] = []

    # === SCHEMA ===
    if "schema" in checks:
        print("=" * 60)
        print("CHECK: schema conformance")
        print("=" * 60)
        ok, errors = validate_schema(rows, features)
        if ok:
            print(f"  ✓ All {len(rows)} rows conform to the schema")
        else:
            critical_failure = True
            print(f"  ✗ Schema violations found ({len(errors)} errors):")
            for err in errors[:20]:
                print(f"    - {err}")
        print()

    # === DEDUP ===
    if "dedup" in checks:
        print("=" * 60)
        print("CHECK: deduplication")
        print("=" * 60)
        n_unique, n_dupes, samples = check_dedup(rows)
        rate = (n_dupes / len(rows) * 100) if rows else 0
        print(f"  Unique rows: {n_unique:,}")
        print(f"  Duplicate rows: {n_dupes:,} ({rate:.2f}%)")
        if samples:
            print(f"  Sample dupe hashes: {samples}")
        if rate > 5:
            warnings.append(f"High duplicate rate: {rate:.1f}% — consider dedup before publishing")
        print()

    # === PII ===
    if "pii" in checks:
        print("=" * 60)
        print("CHECK: PII scan" + (" (including contextual)" if args.pii_contextual else ""))
        print("=" * 60)
        findings = scan_pii(rows, include_contextual=args.pii_contextual)
        has_high_risk = False
        for pii_type, hits in findings.items():
            if not hits:
                continue
            risk = "HIGH" if pii_type in HIGH_RISK_PII else "medium"
            if risk == "HIGH":
                has_high_risk = True
            print(f"  {pii_type} ({risk} risk): {len(hits)} hits")
            for row_idx, field, match in hits[:3]:
                print(f"    row {row_idx}.{field}: {match!r}")
            if len(hits) > 3:
                print(f"    ... and {len(hits) - 3} more")
        if not any(findings.values()):
            print("  ✓ No PII patterns detected")
        if has_high_risk:
            msg = "High-risk PII detected (SSN/credit-card) — review and redact before publishing"
            warnings.append(msg)
            if args.strict:
                critical_failure = True
        print()

    # === LENGTH ===
    if "length" in checks:
        print("=" * 60)
        print("CHECK: length distribution")
        print("=" * 60)
        lens = length_stats(rows, features)
        if not lens:
            print("  (no string fields to analyze)")
        for field, stats in lens.items():
            print(f"  {field}:")
            print(f"    count: {stats['count']:,}  empty: {stats['empty_count']}")
            print(f"    min: {stats['min']}  p25: {stats['p25']}  median: {stats['median']}  "
                  f"p75: {stats['p75']}  max: {stats['max']}")
            if stats["empty_count"] > 0:
                rate = stats["empty_count"] / stats["count"] * 100
                if rate > 1:
                    warnings.append(f"{field}: {rate:.1f}% empty strings")
            if stats["max"] > 100_000:
                warnings.append(f"{field}: max length {stats['max']} — extremely long row, check for noise")
        print()

    # === LANGUAGE ===
    if "language" in checks:
        print("=" * 60)
        print("CHECK: language ID")
        print("=" * 60)
        lang_stats = check_language(rows, features)
        if lang_stats is None:
            print("  (skipped — fasttext or lid.176.bin not available; install with:")
            print("    pip install fasttext && curl -L https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -o /tmp/lid.176.bin)")
        else:
            print(f"  Scanned {lang_stats['total_scanned']:,} rows")
            print(f"  Low-confidence (<0.7): {lang_stats['low_confidence_count']:,}")
            print("  Top languages:")
            for lang, count in lang_stats["top_languages"]:
                print(f"    {lang}: {count:,}")
        print()

    # === CLASSLABEL ===
    if "classlabel" in checks:
        print("=" * 60)
        print("CHECK: ClassLabel balance")
        print("=" * 60)
        balance = classlabel_balance(rows, features)
        if not balance:
            print("  (no ClassLabel fields to analyze)")
        for field, stats in balance.items():
            print(f"  {field}:")
            print(f"    distribution: {stats['distribution']}")
            print(f"    imbalance ratio (max/min): {stats['imbalance_ratio']:.2f}")
            if stats["imbalance_ratio"] > 10:
                warnings.append(f"{field}: severe class imbalance (ratio {stats['imbalance_ratio']:.1f})")
        print()

    # === CONTAMINATION ===
    if "contamination" in checks:
        print("=" * 60)
        print("CHECK: contamination with known benchmarks")
        print("=" * 60)
        contam = check_contamination(rows)
        any_contam = False
        for bench, indices in contam.items():
            if indices:
                any_contam = True
                print(f"  {bench}: {len(indices)} rows match known prompts (rows: {indices[:5]}{'...' if len(indices) > 5 else ''})")
        if not any_contam:
            print("  ✓ No contamination with the tripwire set (note: this is a small sample; full scan needs the full benchmark set)")
        else:
            warnings.append("Contamination detected — add in_<bench>_train boolean columns or drop the contaminated rows")
            if args.strict:
                critical_failure = True
        print()

    # === SUMMARY ===
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    if warnings:
        print(f"  ⚠ {len(warnings)} warning(s):")
        for w in warnings:
            print(f"    - {w}")
    else:
        print("  ✓ No warnings")
    if critical_failure:
        print("\n  ✗ Critical failure — fix before proceeding to produce_dataset.py")
        sys.exit(1)
    else:
        print("\n  ✓ Validation passed — ready for produce_dataset.py")
        sys.exit(0)


if __name__ == "__main__":
    main()
