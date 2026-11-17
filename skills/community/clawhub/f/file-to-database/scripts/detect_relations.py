#!/usr/bin/env python3
"""detect_relations.py — Detect primary-key and foreign-key candidates across file profiles.

Usage:
  python3 detect_relations.py --profiles <profiles.json> [--json] [--out FILE]

Input: the JSON produced by infer_schema.py
Output: PK candidates per table + FK candidates with confidence and evidence.

Heuristics (mirrors references/methodology.md "Foreign-Key Adjudication"):
  >= 0.8  name match (user_id -> users.id) AND 100% value containment -> adopt
  0.5-0.8 value containment but name mismatch -> ask user
  < 0.5   name-only similarity -> ignore (reported)

Value containment is checked when source value sets are available; otherwise
name matching alone caps confidence at 0.5.
"""
import argparse
import json
import re


def table_name(fname):
    base = re.sub(r"\.[^.]+$", "", fname.split("/")[-1])
    base = re.sub(r"[^a-z0-9]+", "_", base.lower()).strip("_")
    if not base.endswith("s"):
        base += "s"
    return base


def singular(name):
    if name.endswith("ies"):
        return name[:-3] + "y"
    if name.endswith("ses"):
        return name[:-2]
    if name.endswith("s") and not name.endswith("ss"):
        return name[:-1]
    return name


def name_matches(col, tables):
    """Return (table, refcol, strength) if col looks like a reference."""
    m = re.match(r"^(.*?)_?id$", col)
    if not m:
        return None
    base = m.group(1)
    if not base:
        return None
    for t in tables:
        if base == singular(t):
            return (t, "id", 1.0)
        if base == t:
            return (t, "id", 0.9)
    return None


def containment(refset, fkset):
    """|fk ∩ ref| / |fk| ; None when either set unavailable."""
    if refset is None or fkset is None or not fkset:
        return None
    return len(fkset & refset) / len(fkset)


def main():
    ap = argparse.ArgumentParser(description="PK/FK candidate detection from profiles")
    ap.add_argument("--profiles", required=True, help="profiles.json from infer_schema.py")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    args = ap.parse_args()

    with open(args.profiles, "r", encoding="utf-8") as f:
        data = json.load(f)

    profiles = data["profiles"] if isinstance(data, dict) else data
    tables = {}
    for p in profiles:
        if "error" in p or not p.get("columns"):
            continue
        t = table_name(p["file"])
        tables[t] = {"profile": p, "pk": [], "value_sets": {}}
        for col in p["columns"]:
            if col.get("primary_key_candidate"):
                tables[t]["pk"].append(col["name"])

    # FK candidates
    fk_candidates = []
    for t, info in tables.items():
        for col in info["profile"]["columns"]:
            nm = name_matches(col["name"], tables)
            if not nm:
                continue
            ref_t, ref_c, strength = nm
            if ref_t == t:
                continue
            conf = 0.5 * strength  # name-only baseline
            evidence = {"name_match": f"{col['name']} -> {ref_t}.{ref_c}"}
            # value containment if both sides look unique-ish and samples exist
            ref_cols = tables[ref_t]["profile"]["columns"]
            ref_col = next((c for c in ref_cols if c["name"] == ref_c), None)
            if ref_col is not None:
                ref_set, fk_set = set(ref_col.get("samples", [])), set(col.get("samples", []))
                cont = containment(ref_set, fk_set)
                if cont is not None and fk_set:
                    evidence["sample_containment"] = round(cont, 3)
                    if cont >= 0.99:
                        conf = 0.5 + 0.3 * strength  # up to 0.8+
                    elif cont >= 0.9:
                        conf = 0.55
                    else:
                        conf = 0.3
                        evidence["note"] = "sample values not contained; likely different entity or dirty refs"
            fk_candidates.append({
                "table": t, "column": col["name"], "references": f"{ref_t}.{ref_c}",
                "confidence": round(conf, 2), "evidence": evidence,
                "verdict": "adopt" if conf >= 0.8 else ("ask_user" if conf >= 0.5 else "ignore"),
            })

    out = {
        "tables": {t: {"primary_key_candidates": i["pk"]} for t, i in tables.items()},
        "foreign_keys": fk_candidates,
        "counts": {
            "tables": len(tables),
            "fk_adopt": sum(1 for f in fk_candidates if f["verdict"] == "adopt"),
            "fk_ask": sum(1 for f in fk_candidates if f["verdict"] == "ask_user"),
            "fk_ignore": sum(1 for f in fk_candidates if f["verdict"] == "ignore"),
        },
    }
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"relations written to {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
