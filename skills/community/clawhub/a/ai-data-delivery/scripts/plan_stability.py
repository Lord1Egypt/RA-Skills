#!/usr/bin/env python3
"""plan_stability.py — 验收段：查询计划稳定性抽查（ai-data-delivery v0.0.4）

引擎不变式 1：同一语义输入产出稳定唯一的查询计划。
同义词命中顺序、字典序、并发都不得影响计划。验收门槛：同句连跑 N 次 SQL 哈希一致。

用法：
  python plan_stability.py --endpoint http://localhost:7100 --question "上月各企业报警数排名" [--times 10]
  python plan_stability.py --endpoint http://localhost:7100 --cases cases.json [--times 10] [--limit 20]

判定依据：响应中的 sql 字段（无 sql 字段则退化比对 value/rows 指纹）。
退出码：0 = 全部稳定；1 = 发现漂移；2 = 用法错误。

安全声明：网络访问仅限 --endpoint 指定地址，默认仅本机/内网（端点守卫，远程需 --allow-remote）；无任何其他出站请求。
"""
import argparse
import hashlib
import json
import sys

import yaml

from _contract import guard_endpoint
from _network import safe_json, response_error


def ask(endpoint, q, timeout=30, allow_remote=False):
    try:
        return safe_json(endpoint.rstrip("/") + "/api/ask", {"question": q}, timeout=timeout, allow_remote=allow_remote)
    except Exception as e:
        return {"error": str(e)}


def fingerprint(resp):
    error = response_error(resp, require_result=True, allow_sql=True)
    if error:
        return "ERROR:" + error
    plan = resp.get("sql")
    if isinstance(plan, str) and plan.strip():
        return "SQL:" + str(plan).strip()
    return "DATA:" + json.dumps([resp.get("value"), resp.get("rows"), resp.get("rejected")],
                                ensure_ascii=False, sort_keys=True)


def check_one(endpoint, question, times, allow_remote=False):
    fps = []
    for _ in range(times):
        fps.append(fingerprint(ask(endpoint, question, allow_remote=allow_remote)))
    uniq = sorted(set(fps))
    errored = all(u.startswith("ERROR:") for u in uniq)  # 全失败≠稳定，属服务不可用
    return len(uniq) == 1 and not errored, uniq, errored


def main():
    ap = argparse.ArgumentParser(description="查询计划稳定性抽查")
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--question", default=None)
    ap.add_argument("--cases", default=None)
    ap.add_argument("--times", type=int, default=10)
    ap.add_argument("--limit", type=int, default=20, help="--cases 模式下抽查前 N 条")
    ap.add_argument("--allow-remote", action="store_true",
                    help="允许非本机/内网端点（默认拒绝，防误发业务内容到公网）")
    args = ap.parse_args()
    try:
        guard_endpoint(args.endpoint, args.allow_remote)
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    questions = []
    if args.question:
        questions = [args.question]
    elif args.cases:
        with open(args.cases, encoding="utf-8") as f:
            data = yaml.safe_load(f) if args.cases.endswith((".yaml", ".yml")) else json.load(f)
        if isinstance(data, dict):
            data = data.get("cases", data.get("gold_results", []))
        questions = [c["question"] for c in data[: args.limit] if c.get("question")]
    if not questions:
        print("错误：需要 --question 或 --cases", file=sys.stderr)
        return 2

    drift = 0
    for q in questions:
        stable, uniq, errored = check_one(args.endpoint, q, args.times, allow_remote=args.allow_remote)
        mark = "异常" if errored else ("稳定" if stable else "漂移")
        print(f"[{mark}] {q[:40]}（{args.times} 次，{len(uniq)} 种指纹）")
        if not stable:
            drift += 1
            for u in uniq[:3]:
                print(f"    {hashlib.md5(u.encode()).hexdigest()[:8]}  {u[:100]}")
    print(f"\n抽查 {len(questions)} 句 × {args.times} 次：漂移/异常 {drift} 句")
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main())
