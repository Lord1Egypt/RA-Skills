#!/usr/bin/env python3
"""capture_case.py — 闭环段：bad case 一键取证（ai-data-delivery v0.0.4）

对活引擎复现 bad case，一次拿齐三件套再下结论：
  POST /api/ask       → 答案/SQL/推理链/拒绝判定
  GET  /api/search?q= → 检索打分（看命中了谁、被谁吸走）
  GET  /api/model     → 运行时模型版本与计数（防对着旧模型归因）

用法：
  python capture_case.py --endpoint http://localhost:7100 \
      --question "上个月华东的重大隐患有多少条" [--id bc-001] [--note "用户投诉数值偏小"] \
      --out badcases/

输出 badcases/<id>.yaml：bad case 登记卡（证据已填，symptom/layer/fix 留待归因）。

安全声明：网络访问仅限 --endpoint 指定地址，默认仅本机/内网（端点守卫，远程需 --allow-remote）；无任何其他出站请求。
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.parse

import yaml

from _contract import guard_endpoint
from _network import safe_json


def call(method, url, payload=None, timeout=30, allow_remote=False):
    try:
        if method not in {"GET", "POST"}:
            raise ValueError("取证调用仅支持 GET/POST")
        return safe_json(url, payload=payload, timeout=timeout, allow_remote=allow_remote), None
    except Exception as e:
        return None, str(e)


def norm_search(search, err=None):
    """检索响应归一为 dict{hits: [...]}——不同引擎实现可能是 list 或 dict，统一后才能下游复用。"""
    if isinstance(search, list):
        return {"hits": search}
    if isinstance(search, dict):
        if isinstance(search.get("hits"), list):
            return search
        return {"hits": [search]} if search else {"hits": []}
    return {"hits": [], "error": err or "检索响应为空或不可解析"}


def main():
    ap = argparse.ArgumentParser(description="bad case 一键取证")
    ap.add_argument("--endpoint", required=True)
    ap.add_argument("--question", required=True)
    ap.add_argument("--id", default=None)
    ap.add_argument("--note", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--allow-remote", action="store_true",
                    help="允许非本机/内网端点（默认拒绝，防误发业务内容到公网）")
    args = ap.parse_args()
    try:
        guard_endpoint(args.endpoint, args.allow_remote)
    except ValueError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    base = args.endpoint.rstrip("/")
    case_id = args.id or "bc-" + datetime.date.today().strftime("%Y%m%d") + "-001"

    ask, e1 = call("POST", base + "/api/ask", {"question": args.question}, allow_remote=args.allow_remote)
    search, e2 = call("GET", base + "/api/search?q=" + urllib.parse.quote(args.question), allow_remote=args.allow_remote)
    prog, e3 = call("GET", base + "/api/metrics/progress", allow_remote=args.allow_remote)
    if prog is None:
        prog, e3b = call("GET", base + "/api/model", allow_remote=args.allow_remote)
        if prog:
            prog = {"modelVersion": prog.get("version"), "total": len(prog.get("metrics", []))}
    if e1:
        print(f"错误：/api/ask 不可达：{e1}", file=sys.stderr)
        return 2
    if not isinstance(ask, dict):
        print("错误：/api/ask 必须返回 JSON 对象", file=sys.stderr)
        return 2

    hits_norm = norm_search(search, e2)
    card = {
        "id": case_id,
        "captured_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "question": args.question,
        "note": args.note,
        "evidence": {
            "model_snapshot": prog or {"error": e3},
            "retrieval": hits_norm,
            "answer": {k: ask.get(k) for k in
                       ("value", "rows", "rejected", "refused", "error", "status", "success", "reason", "sql", "reasoning")
                       if k in ask},
        },
        # 以下由归因填写（模板与 diagnosis-playbook 对齐）
        "symptom": None, "layer": None, "fix": None, "verify": None,
        "expect": {"type": None, "value": None, "rows": None},
        "regression_before": None, "regression_after": None,
    }
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, f"{case_id}.yaml")
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(card, f, allow_unicode=True, sort_keys=False, width=120)
    ans = card["evidence"]["answer"]
    print(f"取证完成 → {path}")
    print(f"  模型版本: {(prog or {}).get('modelVersion')}  指标数: {(prog or {}).get('total')}")
    print(f"  检索命中: {[h.get('name') for h in hits_norm['hits']][:3]}")
    print(f"  应答: rejected={ans.get('rejected')} value={ans.get('value')} "
          f"rows={len(ans.get('rows') or [])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
