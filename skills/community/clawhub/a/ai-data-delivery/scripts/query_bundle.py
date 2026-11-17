#!/usr/bin/env python3
"""Read a metric and its contributing input rows from one SQLite snapshot.

The detail rows are the metric's filtered input, not necessarily rows counted by
COUNT(column)/COUNT(DISTINCT column) or the numerator of a ratio. This local tool
does not authenticate callers, infer question filters or prove tenant isolation.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sqlite3

import yaml
from _contract import keys, now, object_digest, quote, snapshot
from _sql import compile_scope, compile_single, metric_dependencies


class BundleError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def _failure(code, message, evidence=None):
    return {"status": "error", "error": {"code": code, "message": str(message)},
            "evidence": evidence or {}}


def _json_cell(value):
    if value is None or isinstance(value, (str, int)):
        return value
    if isinstance(value, float) and math.isfinite(value):
        return value
    raise BundleError("unsupported_value", "结果含 BLOB 或非有限数值，不能作为 JSON 明细交付")


def run_bundle(model, conn, metric_id, columns, limit=50, offset=0, *, expected_model_sha256=None):
    """Return computed_only/error; errors never contain partial result values.

    expected_model_sha256, when supplied, is _contract.object_digest(model).
    The caller's existing transaction is retained; otherwise this function opens
    and rolls back its own read transaction. All statements use the same snapshot.
    Evidence hashes canonical JSON and the SQLite iterdump snapshot respectively.
    """
    evidence, own_transaction, old_query_only = {}, False, None
    try:
        if not isinstance(model, dict):
            raise BundleError("invalid_model", "模型必须是对象")
        model_hash = object_digest(model)
        evidence = {"created_at": now(), "mode": "offline", "model_sha256": model_hash,
                    "model_hash_kind": "canonical_json", "semantic_model_sha256": model_hash}
        if expected_model_sha256 is not None and expected_model_sha256 != model_hash:
            raise BundleError("model_mismatch", "模型摘要与请求预期不一致；未执行查询")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 500:
            raise BundleError("invalid_page", "limit 必须为 1–500 的整数")
        if isinstance(offset, bool) or not isinstance(offset, int) or not 0 <= offset <= 1000000:
            raise BundleError("invalid_page", "offset 必须为 0–1000000 的整数")
        metrics = [m for m in model.get("metrics", []) if m.get("id") == metric_id]
        if len(metrics) != 1:
            raise BundleError("unknown_metric", "指标不存在或 ID 重复")
        metric = metrics[0]
        datasets = [d for d in model.get("datasets", []) if d.get("name") == metric.get("dataset")]
        if len(datasets) != 1:
            raise BundleError("unknown_dataset", "指标数据集不存在或名称重复")
        ds = datasets[0]
        declared = {f["name"] for f in ds.get("fields", [])}
        if not isinstance(columns, (list, tuple)) or not columns or any(not isinstance(c, str) for c in columns):
            raise BundleError("invalid_columns", "必须显式提供非空明细字段列表")
        if len(set(columns)) != len(columns) or not set(columns) <= declared:
            raise BundleError("invalid_columns", "明细字段重复或不在数据集声明内")
        pk = keys(ds.get("primary_key"))
        if not pk or len(set(pk)) != len(pk) or not set(pk) <= declared:
            raise BundleError("unstable_identity", "稳定分页需要已声明的唯一主键字段")
        sql, error = compile_single(metric, ds)
        if error: raise BundleError("unsupported_metric", error)
        where, error = compile_scope(metric, ds)
        if error: raise BundleError("unsupported_scope", error)
        required = set(columns) | set(pk) | set(metric_dependencies(metric, ds)["fields"])
        if not isinstance(conn, sqlite3.Connection):
            raise BundleError("missing_snapshot", "需要可读取的 SQLite 快照连接")
        old_query_only = conn.execute("PRAGMA query_only").fetchone()[0]
        conn.execute("PRAGMA query_only=ON")
        own_transaction = not conn.in_transaction
        if own_transaction: conn.execute("BEGIN")
        table = quote(ds["source"])
        physical = {c[0] for c in conn.execute(f"SELECT * FROM {table} LIMIT 0").description}
        if not required <= physical:
            raise BundleError("source_schema_mismatch", "当前快照缺少引用字段：" + ", ".join(sorted(required - physical)))
        nulls = " OR ".join(f"{quote(c)} IS NULL" for c in pk)
        identity = ", ".join(quote(c) for c in pk)
        if conn.execute(f"SELECT 1 FROM {table} WHERE {nulls} LIMIT 1").fetchone():
            raise BundleError("unstable_identity", "声明主键存在 NULL，不能稳定分页")
        if conn.execute(f"SELECT 1 FROM {table} GROUP BY {identity} HAVING COUNT(*) > 1 LIMIT 1").fetchone():
            raise BundleError("unstable_identity", "声明主键存在重复，不能稳定分页")
        rows = conn.execute(sql).fetchmany(2)
        if len(rows) != 1 or len(rows[0]) != 1:
            raise BundleError("non_scalar_metric", "指标未返回唯一标量")
        value = _json_cell(rows[0][0])
        if value == "ZERO_DENOMINATOR":
            raise BundleError("zero_denominator", "分母为零，当前口径要求报错")
        suffix = " WHERE " + where if where else ""
        count = conn.execute(f"SELECT COUNT(*) FROM {table}{suffix}").fetchone()[0]
        detail_sql = f"SELECT {', '.join(quote(c) for c in columns)} FROM {table}{suffix} ORDER BY {identity} LIMIT ? OFFSET ?"
        details = [[_json_cell(cell) for cell in row] for row in conn.execute(detail_sql, (limit, offset)).fetchall()]
        fingerprint = hashlib.sha256()
        for statement in conn.iterdump():
            fingerprint.update(statement.encode("utf-8")); fingerprint.update(b"\n")
        evidence["data_snapshot_sha256"] = fingerprint.hexdigest()
        has_more = offset + len(details) < count
        return {"status": "computed_only", "metric": metric_id, "dataset": ds["name"],
                "metric_name": metric.get("name", metric_id), "metric_unit": metric.get("unit", ""),
                "metric_value": value, "matched_row_count": count,
                "detail_columns": list(columns), "detail_rows": details,
                "queries": {"metric_sql": sql, "detail_sql": detail_sql, "detail_parameters": [limit, offset]},
                "pagination": {"limit": limit, "offset": offset, "returned_rows": len(details),
                               "has_more": has_more, "next_offset": offset + len(details) if has_more else None,
                               "truncated": len(details) < count, "order_by": pk},
                "scope": {"filters": metric.get("filters", []), "extra_where": metric.get("extra_where"),
                          "detail_meaning": "指标过滤后的输入记录；不等于非空计数、去重计数或比率分子的条数",
                          "boundary": "没有从自然语言追加条件；本地过滤不是身份鉴权或租户隔离证明"},
                "evidence": evidence}
    except BundleError as exc:
        return _failure(exc.code, exc, evidence)
    except (sqlite3.Error, ValueError, TypeError, KeyError, AttributeError, OverflowError) as exc:
        return _failure("execution_error", exc, evidence)
    finally:
        if own_transaction:
            conn.rollback()
        if old_query_only is not None:
            conn.execute("PRAGMA query_only=" + str(int(old_query_only)))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--metric", required=True)
    parser.add_argument("--columns", required=True, help="显式明细字段，以逗号分隔")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--expected-model", help="当前模型文件的 SHA256；失配不打开数据快照")
    parser.add_argument("--out", help="JSON 结果；省略时输出到标准输出")
    args = parser.parse_args(argv)
    try:
        raw = Path(args.model).read_bytes()
        file_hash = hashlib.sha256(raw).hexdigest()
        if args.expected_model and args.expected_model != file_hash:
            raise BundleError("model_mismatch", "模型文件摘要与请求预期不一致")
        model = yaml.safe_load(raw.decode("utf-8-sig"))
        if not Path(args.db).is_file():
            raise BundleError("missing_snapshot", "SQLite 快照不存在；不会创建空数据库")
        conn, snapshot_hash = snapshot(args.db)
        try:
            result = run_bundle(model, conn, args.metric, [c.strip() for c in args.columns.split(",")], args.limit, args.offset)
        finally:
            conn.close()
        result["evidence"].update(model_sha256=file_hash, model_hash_kind="file",
                                  data_snapshot_sha256=snapshot_hash)
    except BundleError as exc:
        result = _failure(exc.code, exc)
    except (OSError, sqlite3.Error, ValueError, TypeError, yaml.YAMLError) as exc:
        result = _failure("input_error", exc)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result["status"] == "computed_only" else 2


if __name__ == "__main__":
    raise SystemExit(main())
