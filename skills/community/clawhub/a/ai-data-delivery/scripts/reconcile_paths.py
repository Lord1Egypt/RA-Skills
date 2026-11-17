#!/usr/bin/env python3
"""reconcile_paths.py — 闭环段：指标路径 vs 宽表路径双路对账（ai-data-delivery v0.0.5）

RULE-METRIC-01：同一问题两条路径结果必须一致，不一致即存在双口径（两个正确答案 = 零信任）。

两种用法：
  # 模式 A · 主动对账（推荐）：从 semantic.yaml 编译结构化指标的 SQL，直连物理库算"指标口径值"，
  #   再打活引擎拿"问数路径值"，逐指标比对
  python reconcile_paths.py --model semantic.yaml --db physical.db --endpoint http://localhost:7100 \
      [--metric inspect_count ...] [--out reconcile.json]

  # 模式 B · 离线比对两份结果（json: {id: {"value": n} 或 {"rows": [[...]]}}）
  python reconcile_paths.py --metric-path a.json --wide-path b.json

口径编译规则（与引擎不变式一致）：expr/分子分母 + extra_where + 数据集 source 表；
dataset./表名前缀自动剥离；仅对 single-dataset 的 count/sum/avg/ratio 编译，其余跳过并声明。

安全声明：网络访问仅限 --endpoint 指定地址，默认仅本机/内网（端点守卫，远程需 --allow-remote）；无任何其他出站请求。
"""
import os
import argparse
import json
import sys

import yaml
from _contract import guard_endpoint, readonly, load
from _sql import compile_single
from _network import safe_json, response_error


def compile_metric_sql(mt, ds, names):
    """结构化指标 → 可执行 SQL（expr/分子分母 + filters + extra_where 全量口径）。
    返回 (sql, 不可编译原因)。"""
    return compile_single(mt, ds, names)


def classify_diff(expected, actual, mt, tol=1e-4):
    """不一致分类：量纲差异（×100 百分比）/ 数值不一致。"""
    try:
        e, a = float(expected), float(actual)
    except (TypeError, ValueError):
        return "不一致"
    if abs(e - a) <= tol or (e and abs(a / e - 100) <= 0.01) or (a and abs(e / a - 100) <= 0.01):
        if abs(e - a) > tol:
            return "量纲差异"  # 候选解释，需要确认单位转换后重新对账
    return "不一致"


def ask(endpoint, q, timeout=30, allow_remote=False):
    try:
        return safe_json(endpoint.rstrip("/") + "/api/ask", {"question": q}, timeout=timeout, allow_remote=allow_remote)
    except Exception as e:
        return {"error": str(e)}


def norm(x):
    try:
        return round(float(x), 4)
    except (TypeError, ValueError):
        return x


def run_active(args):
    m = load(args.model)
    ds_index = {d["name"]: d for d in m.get("datasets", [])}
    names = set(ds_index) | {d.get("source") for d in m.get("datasets", [])}
    conn = readonly(args.db)

    only = set(args.metric or [])
    rows, n_mismatch, n_scale = [], 0, 0
    for mt in m.get("metrics", []):
        if not mt.get("structured"):
            continue
        if only and mt["id"] not in only:
            continue
        sql, why = compile_metric_sql(mt, ds_index.get(mt.get("dataset")), names)
        rec = {"metric": mt["id"], "name": mt.get("name")}
        if not sql:
            rec["status"] = "skip"; rec["why"] = why
            n_mismatch += 1
        else:
            try:
                expected = conn.execute(sql).fetchone()[0]
                if expected is None:
                    raise ValueError("NULL 结果未定义，不能标记为验证通过")
                rec["metric_path"] = norm(expected)
                rec["compiled_sql"] = sql
                if args.endpoint:
                    resp = ask(args.endpoint, f"查一下{mt.get('name')}", allow_remote=getattr(args, "allow_remote", False))
                    failure = response_error(resp, require_result=True)
                    if failure:
                        raise ValueError(failure)
                    actual = resp.get("value")
                    if actual is None and resp.get("rows"):
                        if len(resp["rows"]) != 1 or not isinstance(resp["rows"][0], list) or len(resp["rows"][0]) != 1:
                            raise ValueError("标量指标核对要求唯一一行一列，不能截取部分结果")
                        actual = resp["rows"][0][0]
                    rec["query_path"] = norm(actual) if actual is not None else None
                    ok = actual is not None and norm(actual) == norm(expected)
                    if not ok and actual is not None and \
                            classify_diff(expected, actual, mt) == "量纲差异":
                        rec["status"] = "量纲差异"
                        n_scale += 1
                        n_mismatch += 1
                        rec["why"] = (f"指标路径={norm(expected)} 问数路径={norm(actual)}"
                                      f"（疑似 ×100 量纲差异，尚未确认；请核对模型单位 "
                                      f"{mt.get('unit') or '?'}）")
                    else:
                        rec["status"] = "一致" if ok else "不一致"
                        if not ok:
                            n_mismatch += 1
                            rec["why"] = f"指标路径={norm(expected)} 问数路径={norm(actual)}"
                            if resp.get("rejected"):
                                rec["why"] += "（引擎拒答/追问）"
                            if resp.get("error"):
                                rec["why"] += f"（请求失败：{resp['error']}）"
                else:
                    rec["status"] = "computed_only"
            except Exception as e:
                rec["status"] = "error"; rec["why"] = str(e)
                n_mismatch += 1
        rows.append(rec)

    conn.close()
    for r in rows:
        print(f"[{r['status']:>10s}] {r['metric']:24s} {r.get('metric_path', '')} "
              f"{('vs ' + str(r.get('query_path', ''))) if 'query_path' in r else ''} {r.get('why', '')}")
    print(f"\n对账完成：{len(rows)} 个结构化指标，不一致 {n_mismatch} 个，量纲差异 {n_scale} 个")
    if n_scale:
        print("提示：量纲差异计入不一致，需明确单位转换并重新对账。")
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False, indent=1)
    return 1 if n_mismatch or not rows else 0


def run_offline(args):
    a = json.load(open(args.metric_path, encoding="utf-8"))
    b = json.load(open(args.wide_path, encoding="utf-8"))

    def pick(d, k):
        v = d.get(k)
        if isinstance(v, dict):
            if response_error(v, require_result=True):
                return None
            return v.get("value", v.get("rows"))
        return v  # 兼容扁平 {id: 数值} 写法

    mismatch = 0
    for k in sorted(set(a) | set(b)):
        va, vb = pick(a, k), pick(b, k)
        ok = va is not None and vb is not None and norm(va) == norm(vb)
        mismatch += 0 if ok else 1
        print(f"[{'一致' if ok else '不一致'}] {k}: 指标路径={va} 宽表路径={vb}")
    print(f"\n离线对账：不一致 {mismatch} 条")
    return 1 if mismatch or not (set(a) | set(b)) else 0


def main():
    ap = argparse.ArgumentParser(description="双路径口径对账")
    ap.add_argument("--model", help="semantic.yaml（模式 A）")
    ap.add_argument("--db", help="物理库（模式 A）")
    ap.add_argument("--endpoint", help="活引擎（模式 A 可选；不给则只编译计算指标路径）")
    ap.add_argument("--metric", action="append", default=[])
    ap.add_argument("--out", default=None)
    ap.add_argument("--metric-path", dest="metric_path", help="指标路径结果 json（模式 B）")
    ap.add_argument("--wide-path", dest="wide_path", help="宽表路径结果 json（模式 B）")
    ap.add_argument("--allow-remote", action="store_true",
                    help="允许非本机/内网端点（默认拒绝，防误发业务内容到公网）")
    args = ap.parse_args()
    if args.endpoint:
        try:
            guard_endpoint(args.endpoint, args.allow_remote)
        except ValueError as exc:
            print(f"错误：{exc}", file=sys.stderr)
            return 2

    if args.model and args.db:
        return run_active(args)
    if args.metric_path and args.wide_path:
        return run_offline(args)
    print("错误：模式 A 需 --model + --db（可再加 --endpoint）；模式 B 需 --metric-path + --wide-path",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
