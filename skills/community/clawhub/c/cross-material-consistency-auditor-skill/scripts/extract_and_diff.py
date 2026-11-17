from __future__ import annotations

import argparse
import json
import os
import re
from hashlib import sha256
from pathlib import Path
from typing import Any


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_numbers(text: str) -> dict[str, list[str]]:
    pattern = re.compile(
        r"(?<![A-Za-z])(?:US\$|HK\$|￥|[$¥€£])?\d+(?:[.,]\d+)*(?:%|倍|万亿|亿|万|千|百万|十亿|百亿|年|月|日|小时|分钟|tokens?|Token)?",
        re.I,
    )
    return {"raw": [match.group(0).strip() for match in pattern.finditer(text)]}


def extract_headings(text: str) -> list[str]:
    return [line.strip().lstrip("#").strip() for line in text.splitlines() if re.match(r"^#{2,4}\s+", line)]


def _load_product_terms() -> list[str]:
    """Product/term watchlist is user-supplied, never hardcoded.

    Priority:
    1. Env var CONSISTENCY_PRODUCT_TERMS (comma-separated terms).
    2. product-terms.txt next to this script (one term per line, # comments allowed).
    3. Empty -> fall back to a generic CamelCase/acronym heuristic.
    """
    env_terms = os.environ.get("CONSISTENCY_PRODUCT_TERMS", "")
    if env_terms.strip():
        return [t.strip() for t in env_terms.split(",") if t.strip()]
    terms_file = Path(__file__).with_name("product-terms.txt")
    if terms_file.exists():
        lines = terms_file.read_text(encoding="utf-8").splitlines()
        return [ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("#")]
    return []


def extract_product_mentions(text: str) -> list[str]:
    terms = _load_product_terms()
    if terms:
        pattern = re.compile("|".join(re.escape(t) for t in terms), re.I)
    else:
        # Generic heuristic: CamelCase compounds (FooBar) or 2-6 letter
        # all-caps acronyms with optional hyphen suffix (ABC-X).
        pattern = re.compile(r"\b(?:[A-Z][a-z]+){2,}\b|\b[A-Z]{2,6}(?:-[A-Za-z0-9]+)?\b")
    return sorted(set(match.group(0) for match in pattern.finditer(text)))


def extract_claims(text: str, label: str) -> dict[str, Any]:
    return {
        "label": label,
        "hash": sha256(text.encode("utf-8")).hexdigest()[:16],
        "numbers": extract_numbers(text),
        "headings": extract_headings(text),
        "product_mentions": extract_product_mentions(text),
        "lines": len(text.splitlines()),
    }


def diff_claims(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    diffs: list[dict[str, Any]] = []
    if len(claims) < 2:
        return diffs
    ref = claims[0]
    for other in claims[1:]:
        pair_key = f"{ref['label']} vs {other['label']}"
        ref_numbers = set(ref["numbers"]["raw"])
        other_numbers = set(other["numbers"]["raw"])
        only_in_ref = ref_numbers - other_numbers
        only_in_other = other_numbers - ref_numbers
        if only_in_ref or only_in_other:
            diffs.append({"dimension": "numbers", "pair": pair_key, "only_in_ref": sorted(only_in_ref), "only_in_other": sorted(only_in_other)})
        ref_products = set(ref["product_mentions"])
        other_products = set(other["product_mentions"])
        product_only_in_ref = ref_products - other_products
        product_only_in_other = other_products - ref_products
        if product_only_in_ref or product_only_in_other:
            diffs.append({"dimension": "product_mentions", "pair": pair_key, "only_in_ref": sorted(product_only_in_ref), "only_in_other": sorted(product_only_in_other)})
        ref_headings = set(ref["headings"])
        other_headings = set(other["headings"])
        heading_only_in_ref = ref_headings - other_headings
        heading_only_in_other = other_headings - ref_headings
        if heading_only_in_ref or heading_only_in_other:
            diffs.append({"dimension": "headings", "pair": pair_key, "only_in_ref": sorted(heading_only_in_ref), "only_in_other": sorted(heading_only_in_other)})
    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract claims from materials for cross-material diff")
    parser.add_argument("--materials", required=True, nargs="+")
    parser.add_argument("--labels", nargs="+")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    labels = args.labels or [Path(path).stem for path in args.materials]
    claims = []
    for path, label in zip(args.materials, labels):
        text = read_text(Path(path))
        claims.append(extract_claims(text, label))
    diffs = diff_claims(claims)
    result = {"materials": claims, "numeric_diffs": diffs}
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"materials": len(claims), "diffs": len(diffs)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
