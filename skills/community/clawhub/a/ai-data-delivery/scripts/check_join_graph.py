#!/usr/bin/env python3
"""Check declared relation keys and query-specific fanout, without compiling joins."""
import argparse
import sys
from _contract import evidence, fields, load, quote, relation_id, relation_keys, snapshot, write

CARDS = {"1:1": ("1", "1"), "N:1": ("N", "1"), "1:N": ("1", "N"), "N:M": ("N", "N")}


def validate_relation(rel, datasets):
    if rel.get("from") not in datasets or rel.get("to") not in datasets:
        raise ValueError("unknown relationship endpoint")
    if rel.get("cardinality") not in CARDS:
        raise ValueError("cardinality must be 1:1, N:1, 1:N or N:M")
    if not isinstance(rel.get("traversable"), bool):
        raise ValueError("traversable must be boolean")
    left, right = relation_keys(rel)
    if not set(left) <= fields(datasets[rel["from"]]) or not set(right) <= fields(datasets[rel["to"]]):
        raise ValueError("relationship key not in declared fields")
    return left, right


def key_stats(conn, ds, columns):
    names = ",".join(quote(c) for c in columns)
    null = " OR ".join(quote(c) + " IS NULL" for c in columns)
    table = quote(ds["source"])
    total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    nulls = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE {null}").fetchone()[0]
    dup = conn.execute(f"SELECT COUNT(*) FROM (SELECT 1 FROM {table} WHERE NOT ({null}) GROUP BY {names} HAVING COUNT(*)>1)").fetchone()[0]
    return {"rows": total, "null_rows": nulls, "duplicate_groups": dup,
            "unique_nonnull": bool(total) and not nulls and not dup}


def analyze(model, conn=None):
    datasets = {d["name"]: d for d in model.get("datasets", [])}
    records, rel_index = [], {}
    for rel in model.get("relationships", []):
        rid = relation_id(rel)
        rec = {"id": rid, "from": rel.get("from"), "to": rel.get("to"), "status": "declared_only"}
        try:
            if rid in rel_index:
                raise ValueError("duplicate relationship id; give parallel edges explicit ids")
            rel_index[rid] = rel
            left, right = validate_relation(rel, datasets)
            rec.update(from_columns=left, to_columns=right, cardinality=rel["cardinality"])
            if conn is not None:
                rec["from_key"] = key_stats(conn, datasets[rel["from"]], left)
                rec["to_key"] = key_stats(conn, datasets[rel["to"]], right)
                required = [rec[side + "_key"] for side, card in zip(("from", "to"), CARDS[rel["cardinality"]]) if card == "1"]
                rec["status"] = "pass" if all(s["unique_nonnull"] for s in required) else "fail"
                if not required and not (rec["from_key"]["rows"] and rec["to_key"]["rows"]):
                    rec["status"] = "unknown"
        except ValueError as exc:
            rec.update(status="error", detail=str(exc))
        except Exception as exc:
            rec.update(status="error", detail=str(exc))
        records.append(rec)
    queries = []
    metrics = {m["id"]: m for m in model.get("metrics", [])}
    for query in model.get("query_plans", []):
        result = {"id": query.get("id"), "status": "declared_only", "steps": []}
        try:
            metric = metrics[query["metric"]]
            current = metric["dataset"]
            visited = {current}
            if not query.get("relationships"):
                raise ValueError("explicit query relationship path required")
            for rid in query["relationships"]:
                rel = rel_index[rid]
                if not rel["traversable"]:
                    raise ValueError("path uses non-traversable edge")
                validate_relation(rel, datasets)
                if current == rel["from"]:
                    target, card, target_key = rel["to"], CARDS[rel["cardinality"]][1], "to_key"
                elif current == rel["to"]:
                    target, card, target_key = rel["from"], CARDS[rel["cardinality"]][0], "from_key"
                else:
                    raise ValueError("disconnected query path")
                if target in visited:
                    raise ValueError("repeated dataset/alias unsupported for this query path")
                observed = next(r for r in records if r["id"] == rid)
                status = "fanout" if card != "1" else ("pass" if observed.get(target_key, {}).get("unique_nonnull") else "unknown")
                result["steps"].append({"relationship": rid, "from": current, "to": target, "status": status})
                current = target
                visited.add(current)
            states = [s["status"] for s in result["steps"]]
            result["status"] = "fail" if "fanout" in states else ("pass" if all(s == "pass" for s in states) else "unknown")
            if query.get("strategy"):
                result["strategy_note"] = "strategy is a proposal; not executed or treated as proof"
        except (KeyError, ValueError, TypeError) as exc:
            result.update(status="error", detail=str(exc))
        queries.append(result)
    states = [r["status"] for r in records + queries]
    status = "not_ready" if not states or any(s in {"fail", "error", "unknown"} for s in states) else ("pass" if conn is not None else "declared_only")
    return {"status": status, "relationships": records, "queries": queries,
            "scope": "declared edges and explicit query paths; uniqueness is not referential coverage or live lineage"}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", required=True)
    ap.add_argument("--db")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    conn = None
    try:
        db_hash = None
        if args.db:
            conn, db_hash = snapshot(args.db)
        report = analyze(load(args.model), conn)
        report["evidence"] = evidence(args.model, mode="sqlite_snapshot" if conn else "static", data_snapshot_sha256=db_hash)
    except Exception as exc:
        report = {"status": "error", "detail": str(exc), "evidence": evidence(args.model)}
    finally:
        if conn is not None:
            conn.close()
    write(args.out, report)
    print(f"join graph: {report['status']} → {args.out}")
    return 0 if report["status"] in {"pass", "declared_only"} else 1


if __name__ == "__main__":
    sys.exit(main())
