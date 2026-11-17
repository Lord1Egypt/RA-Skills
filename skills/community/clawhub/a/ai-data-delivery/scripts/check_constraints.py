#!/usr/bin/env python3
"""Full-snapshot SQLite constraints, with explicit NULL and evidence states."""
import argparse
import sys
from _contract import evidence, fields, keys, load, quote, snapshot, write

KINDS = {"unique", "not_null", "allowed_values", "range", "date_order", "referential"}


def check_rule(conn, model, rule):
    rec = {"id": rule.get("id"), "kind": rule.get("kind"), "status": "unknown"}
    try:
        datasets = {d["name"]: d for d in model.get("datasets", [])}
        ds = datasets[rule["dataset"]]
        kind = rule["kind"]
        columns = keys(rule.get("columns", rule.get("field")))
        if kind not in KINDS:
            raise ValueError("unsupported constraint kind")
        if not columns or not set(columns) <= fields(ds):
            raise ValueError("missing/unknown columns")
        if kind in {"range", "allowed_values"} and len(columns) != 1:
            raise ValueError("range/allowed_values require exactly one column")
        policy = rule.get("null_policy")
        if policy not in {"forbid", "ignore", "unknown"}:
            raise ValueError("null_policy must be forbid/ignore/unknown")
        table = quote(ds["source"])
        cols = ["a." + quote(c) for c in columns]
        null = " OR ".join(c + " IS NULL" for c in cols)
        nonnull = " AND ".join(c + " IS NOT NULL" for c in cols)
        total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        nulls = conn.execute(f"SELECT COUNT(*) FROM {table} a WHERE {null}").fetchone()[0]
        params = []
        if kind == "unique":
            sql = (f"SELECT COALESCE(SUM(n - 1), 0) FROM (SELECT COUNT(*) n FROM {table} a "
                   f"WHERE {nonnull} GROUP BY {','.join(cols)} HAVING COUNT(*) > 1)")
        elif kind == "not_null":
            if policy != "forbid":
                raise ValueError("not_null requires null_policy=forbid")
            sql = "SELECT 0"  # nulls counted below, once
        else:
            if kind == "allowed_values":
                values = rule.get("values")
                if not isinstance(values, list) or not values or None in values:
                    raise ValueError("values must be a nonempty list without NULL")
                condition = f"{cols[0]} NOT IN ({','.join('?' for _ in values)})"
                params = values
            elif kind == "range":
                bounds = [("min", "<"), ("max", ">")]
                comparisons = [f"typeof({cols[0]}) NOT IN ('integer','real')"]
                for key, op in bounds:
                    if key in rule:
                        if not isinstance(rule[key], (int, float)) or isinstance(rule[key], bool):
                            raise ValueError("range bounds must be numbers")
                        comparisons.append(f"{cols[0]} {op} ?")
                        params.append(rule[key])
                if not params or ("min" in rule and "max" in rule and rule["min"] > rule["max"]):
                    raise ValueError("missing or inverted range bounds")
                condition = " OR ".join(comparisons)
            elif kind == "date_order":
                if len(cols) != 2:
                    raise ValueError("date_order needs [earlier, later]")
                condition = (f"julianday({cols[0]}) IS NULL OR julianday({cols[1]}) IS NULL "
                             f"OR julianday({cols[0]}) > julianday({cols[1]})")
            else:
                ref = rule["references"]
                target = datasets[ref["dataset"]]
                target_cols = keys(ref["columns"])
                if len(target_cols) != len(cols) or not set(target_cols) <= fields(target):
                    raise ValueError("invalid referenced columns")
                eq = " AND ".join(f"b.{quote(b)} = {a}" for a, b in zip(cols, target_cols))
                condition = f"NOT EXISTS (SELECT 1 FROM {quote(target['source'])} b WHERE {eq})"
            sql = f"SELECT COUNT(*) FROM {table} a WHERE ({nonnull}) AND ({condition})"
        count = conn.execute(sql, params).fetchone()[0]
        violations = count + (nulls if policy == "forbid" else 0)
        state = "fail" if violations else ("unknown" if not total or (nulls and policy == "unknown") else "pass")
        rec.update(status=state, checked_rows=total, null_rows=nulls,
                   violation_count=violations, null_policy=policy, scan="full_snapshot",
                   detail="empty dataset" if not total else None)
    except (ValueError, KeyError, TypeError) as exc:
        rec.update(status="unknown", detail=str(exc))
    except Exception as exc:
        rec.update(status="error", detail=str(exc))
    return rec


def check_all(model, conn):
    rules = model.get("constraints", [])
    records = [check_rule(conn, model, rule) for rule in rules]
    ids = [r.get("id") for r in records]
    if any(not cid for cid in ids) or len(set(ids)) != len(ids):
        records.append({"id": "constraint-identities", "status": "error", "detail": "missing/duplicate constraint id"})
    return {"status": "pass" if records and all(r["status"] == "pass" for r in records) else "not_ready",
            "records": records, "scope": "declared constraints only; full SQLite snapshot; no row samples"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True)
    ap.add_argument("--db", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    try:
        conn, db_hash = snapshot(args.db)
        try:
            report = check_all(load(args.model), conn)
        finally:
            conn.close()
        report["evidence"] = evidence(args.model, mode="sqlite_snapshot", data_snapshot_sha256=db_hash)
    except Exception as exc:
        report = {"status": "error", "detail": str(exc), "evidence": evidence(args.model)}
    write(args.out, report)
    print(f"constraints: {report['status']} → {args.out}")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
