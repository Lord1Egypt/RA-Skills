#!/usr/bin/env python3
"""lead_sheet.py - normalize, dedupe, ICP-score and tier a US B2B account list.

Input  : accounts.csv (or .jsonl) with columns
         company,domain,employees,industry,state,country,notes
         source_url, researched_on  (optional but recommended)
ICP    : icp.json - criteria with weights, plus disqualifiers and tier cutoffs
Output : scored CSV (stdout summary in text, or --json)

Example:
    python3 lead_sheet.py --accounts accounts.csv --icp icp.json --out scored.csv

Stdlib only. No network access, no scraping, no contact enrichment.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from datetime import date

FREEMAIL = {
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
    "icloud.com", "live.com", "msn.com", "proton.me", "protonmail.com",
    "gmx.com", "mail.com", "yandex.com",
}

COUNTRY_DEFAULT = "US"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def norm_domain(domain: str) -> str:
    d = (domain or "").strip().lower()
    d = re.sub(r"^https?://", "", d)
    d = d.split("/")[0].split("?")[0].split(":")[0]
    if d.startswith("www."):
        d = d[4:]
    parts = d.split(".")
    if len(parts) > 2 and ".".join(parts[-2:]) not in {"co.uk", "com.au", "co.nz", "com.br"}:
        d = ".".join(parts[-2:])
    return d


def norm_company(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def parse_employees(raw: str):
    if raw is None:
        return None
    text = str(raw).strip().lower().replace(",", "")
    if not text:
        return None
    mult = 1
    if text.endswith("+"):
        mult = 1000
        text = text[:-1]
    elif text.endswith("k"):
        mult = 1000
        text = text[:-1]
    elif text.endswith("m"):
        mult = 1_000_000
        text = text[:-1]
    try:
        return int(float(text) * mult)
    except ValueError:
        return None


def load_accounts(path: str) -> list:
    rows = []
    if path.lower().endswith(".jsonl"):
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        return rows

    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            raise SystemExit("accounts file has no header row.")
        fields = {f.strip().lower(): f for f in reader.fieldnames}
        for row in reader:
            record = {k.lower(): (v or "").strip() for k, v in zip(fields.values(), row.values())}
            records = [record]
            if ";" in record.get("domain", ""):
                records = []
                for chunk in record["domain"].split(";"):
                    piece = dict(record)
                    piece["domain"] = chunk.strip()
                    records.append(piece)
            rows.extend(records)
    return rows


def range_score(value, spec: dict) -> tuple:
    """Return (score_fraction, label)."""
    if value is None:
        return 0.0, "unknown"
    lo = spec.get("min")
    hi = spec.get("max")
    if lo is not None and value < lo:
        return 0.0, f"under {lo}"
    if hi is not None and value > hi:
        return 0.0, f"over {hi}"
    if spec.get("ideal_min") is not None and value < spec["ideal_min"]:
        return 0.5, "below ideal band"
    if spec.get("ideal_max") is not None and value > spec["ideal_max"]:
        return 0.5, "above ideal band"
    return 1.0, "in range"


def list_match(value: str, allowed: list) -> tuple:
    if not allowed:
        return 1.0, "no filter"
    v = (value or "").strip().lower()
    if not v:
        return 0.0, "missing"
    for item in allowed:
        if item.lower() == v or item.lower() in v or v in item.lower():
            return 1.0, f"match: {item}"
    return 0.0, f"not in list ({v})"


# --------------------------------------------------------------------------- #
# scoring
# --------------------------------------------------------------------------- #
def score_account(account: dict, icp: dict) -> dict:
    weights = icp.get("weights", {})
    checks = []
    earned = 0.0
    total = 0.0

    for key, spec in weights.items():
        weight = float(spec.get("weight", 0))
        total += weight
        if key == "employees":
            frac, label = range_score(parse_employees(account.get("employees")), spec)
        elif key in ("industry", "state", "country", "region"):
            frac, label = list_match(account.get(key, ""), spec.get("include", []))
        else:
            frac, label = range_score(parse_employees(account.get(key)), spec)
        earned += weight * frac
        checks.append({"criterion": key, "score": round(frac, 2), "weight": weight, "note": label})

    score = round((earned / total * 100) if total else 0.0, 1)

    disqualifiers = []
    for rule in icp.get("disqualifiers", []):
        field = rule.get("field", "")
        op = rule.get("op", "equals")
        want = str(rule.get("value", "")).lower()
        have = str(account.get(field, "")).strip().lower()
        hit = False
        if op == "equals":
            hit = have == want
        elif op == "not_equals":
            hit = have != want
        elif op == "contains":
            hit = want in have
        elif op == "not_contains":
            hit = want not in have
        elif op == "max":
            val = parse_employees(account.get(field))
            limit = parse_employees(rule.get("value"))
            hit = val is not None and limit is not None and val <= limit
        elif op == "min":
            val = parse_employees(account.get(field))
            limit = parse_employees(rule.get("value"))
            hit = val is not None and limit is not None and val >= limit
        if hit:
            disqualifiers.append(f"{field} {op} {rule.get('value')}")

    tier = "C"
    for name, cutoff in sorted(icp.get("tiers", {"A": 75, "B": 50}).items(), key=lambda kv: -kv[1]):
        if score >= cutoff:
            tier = name
            break

    if disqualifiers:
        tier = "X"
    if not account.get("domain"):
        tier = "X"

    return {
        "score": score,
        "tier": tier,
        "checks": checks,
        "disqualifiers": disqualifiers,
    }


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description="Dedupe, ICP-score and tier a B2B account list.")
    ap.add_argument("--accounts", required=True, help="accounts.csv or accounts.jsonl")
    ap.add_argument("--icp", required=True, help="icp.json")
    ap.add_argument("--out", help="Write scored CSV here")
    ap.add_argument("--json", action="store_true", help="Print the scored list as JSON")
    args = ap.parse_args()

    if not os.path.exists(args.accounts):
        print(f"error: accounts file not found: {args.accounts}", file=sys.stderr)
        return 2
    if not os.path.exists(args.icp):
        print(f"error: icp file not found: {args.icp}", file=sys.stderr)
        return 2

    with open(args.icp, "r", encoding="utf-8") as fh:
        icp = json.load(fh)

    raw_accounts = load_accounts(args.accounts)
    seen_domain = {}
    seen_name = {}
    scored = []
    dupes = []

    for account in raw_accounts:
        account.setdefault("country", COUNTRY_DEFAULT)
        domain = norm_domain(account.get("domain", ""))
        company = account.get("company", "")
        key_domain = domain
        key_name = norm_company(company)
        if key_domain and key_domain in seen_domain:
            dupes.append({"company": company, "domain": key_domain, "reason": "duplicate domain"})
            continue
        if key_name and key_name in seen_name:
            dupes.append({"company": company, "domain": key_domain, "reason": "duplicate company name"})
            continue
        if key_domain:
            seen_domain[key_domain] = company
        if key_name:
            seen_name[key_name] = company

        result = score_account(account, icp)
        record = dict(account)
        record["domain"] = domain
        record["score"] = result["score"]
        record["tier"] = result["tier"]
        record["reasons"] = "; ".join(
            f"{c['criterion']}: {c['note']}" for c in result["checks"] if c["score"] > 0
        )
        record["disqualifiers"] = "; ".join(result["disqualifiers"])
        record["researched_on"] = record.get("researched_on") or date.today().isoformat()
        scored.append((record, result))

    scored.sort(key=lambda pair: (-pair[1]["score"], pair[0].get("company", "")))

    counts = {"A": 0, "B": 0, "C": 0, "X": 0}
    for _record, result in scored:
        counts[result["tier"]] = counts.get(result["tier"], 0) + 1

    if args.out:
        fields = [
            "company", "domain", "tier", "score", "employees", "industry", "state",
            "country", "source_url", "researched_on", "reasons", "disqualifiers", "notes",
        ]
        with open(args.out, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for record, _result in scored:
                writer.writerow({k: record.get(k, "") for k in fields})
        print(f"written: {args.out}")

    if args.json:
        print(json.dumps(
            {
                "accounts": [r for r, _ in scored],
                "tiers": counts,
                "duplicates_removed": dupes,
                "scored_at": date.today().isoformat(),
            },
            indent=2,
        ))
    else:
        print(f"accounts scored : {len(scored)}")
        print(f"duplicates      : {len(dupes)} removed")
        print(f"tier A          : {counts.get('A', 0)}")
        print(f"tier B          : {counts.get('B', 0)}")
        print(f"tier C          : {counts.get('C', 0)}")
        print(f"tier X (excluded): {counts.get('X', 0)}")
        print("\nTop accounts:")
        for record, _result in scored[:10]:
            print(f"  {record.get('tier')}  {record.get('score'):>5}  {record.get('company','')} [{record.get('domain','')}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
