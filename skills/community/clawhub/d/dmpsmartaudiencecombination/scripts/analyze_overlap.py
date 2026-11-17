#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""analyze_overlap.py - Overlap/渗透分析（核心决策数据）

设计原则：
- 不"填满矩阵"，只为决策问题服务
- 必建包：M ∩ 每个候选Optional标签 → 渗透率r和AND收窄量
- 按需建包：同维度OR扩量时，对1-3对兄弟标签精确算（默认不建）
- 不建包：互斥对（逻辑判定r=0）、父子对（r=100%）、跨维度对、冗余判断对
- 精确值标注"exact"，估算值标注"estimated"
- 临时包命名前缀：tmp_olp_

两种使用模式：
1. default模式（默认C）：只计算M vs Optional，不计算Tag-Tag
2. with-pairs模式：在default基础上，额外计算指定的同维度OR候选对
"""

import argparse
import json
import sys
import time
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from dmp_api_client import DmpClient, ensure_ok
from auth import add_auth_args
from rules_helper import validate_rules_http
from tag_relation import (classify_pairs, get_group_dim,
                          build_must_tag_rules, build_tag_tag_rules,
                          _get_name, is_mutex_pair, is_ancestor_pair)

CREATE_PATH = "/audience/manage/combine/create"
TASK_LIST_PATH = "/audience/manage/taskList"
TMP_PREFIX = "tmp_olp_"


def _to_int(x):
    try:
        if x is None:
            return None
        s = str(x).strip()
        return int(float(s)) if s else None
    except Exception:
        return None


def _load_list(path) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for it in (data if isinstance(data, list) else []):
        if isinstance(it, dict) and it.get("tagId") is not None:
            out.append({"tagId": int(it["tagId"]), "tagName": it.get("tagName")})
        elif not isinstance(it, dict):
            out.append({"tagId": int(it), "tagName": None})
    return out


def _poll(client, aid: int, timeout: int) -> Dict:
    """轮询单个人群任务。严格状态码：1=成功，0=失败，2/3=继续。"""
    start = time.time()
    sleep_s = 3
    while True:
        resp = client.post(TASK_LIST_PATH, {"audienceIds": [aid]})
        ensure_ok(resp)
        items = resp.get("data") or []
        last = items[0] if items else {}
        status = last.get("audienceStatus")
        if status == 1:
            return {"success": True, "amount": _to_int(last.get("audienceAmount")),
                    "audienceAmount": last.get("audienceAmount")}
        if status == 0:
            return {"success": False, "error": last.get("taskLog", "") or "人群计算失败"}
        if time.time() - start > timeout:
            return {"success": False, "error": f"轮询超时({timeout}s)，status={status}", "timeout": True}
        time.sleep(sleep_s)
        sleep_s = min(int(sleep_s * 1.5), 20)


def _create_and_poll(client, data_rules, name, track_type, id_types, timeout) -> Dict:
    errors = validate_rules_http(data_rules)
    if errors:
        return {"success": False, "error": f"规则校验失败: {';'.join(errors)}"}
    resp = client.post(CREATE_PATH, {
        "name": name, "trackType": track_type, "idTypes": id_types, "data": data_rules,
    })
    ensure_ok(resp)
    aid = (resp.get("data") or {}).get("audienceId")
    if aid is None:
        return {"success": False, "error": "未返回audienceId"}
    result = _poll(client, int(aid), timeout)
    result["audienceId"] = int(aid)
    return result


def main():
    ap = argparse.ArgumentParser()
    add_auth_args(ap)
    ap.add_argument("--audience-id-m", type=int, required=True, help="MUST基准人群ID")
    ap.add_argument("--amount-m", required=True, help="MUST基准量级|M|")
    ap.add_argument("--optional", required=True, help="Optional/候选标签列表")
    ap.add_argument("--tag-pool", default=None)
    ap.add_argument("--core-kws", default="美妆个护,护肤,彩妆")
    ap.add_argument("--or-pairs", default=None,
                    help="需要精确计算的同维度OR候选对，格式：'tagA1:tagB1,tagA2:tagB2'（按需计算，默认不指定则不算Tag-Tag）")
    ap.add_argument("--track-type", required=True, choices=["MOBILE", "PC", "OTT"])
    ap.add_argument("--id-types", required=True, nargs="+")
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    skill_dir = Path(__file__).parent.parent
    pool_path = Path(args.tag_pool) if args.tag_pool else skill_dir / "tag_pool.json"
    tag_pool = []
    if pool_path.exists():
        with open(pool_path, "r", encoding="utf-8") as f:
            tag_pool = json.load(f)
    core_kws = [kw.strip() for kw in args.core_kws.split(",") if kw.strip()]
    m_amt = _to_int(args.amount_m)
    if not m_amt or m_amt <= 0:
        raise SystemExit("amount_M必须>0")
    optionals = _load_list(args.optional)
    if not optionals:
        raise SystemExit("optional为空")

    client = DmpClient.from_config(ak=args.ak, sk=args.sk, base_url=args.base_url)
    opt_ids = [x["tagId"] for x in optionals]
    opt_names = {x["tagId"]: x.get("tagName") or _get_name(x["tagId"], tag_pool) for x in optionals}

    output = {
        "meta": {
            "mode": "default_c_plus_pairwise_on_demand",
            "must_audience_id": args.audience_id_m,
            "must_amount": m_amt,
            "precision_policy": "M∩Optional=exact; mutex=logical_0; ancestor=logical_100pct; OR-pairs=按需; cross_dim=not_calculated"
        },
        "must_vs_optional": [],    # M ∩ x，精确值
        "tag_relations": {         # Tag-Tag关系
            "mutex": [],           # 逻辑判定r=0
            "ancestor": [],        # 逻辑判定r=100%
            "same_dim_exact": [],  # 按需精确计算的同维度兄弟对
            "estimated": [],       # 估算值（降级时使用，当前默认不输出）
        },
    }

    # ────── 1. 逻辑分类所有Optional标签对 ──────
    if tag_pool:
        from tag_relation import classify_pairs
        relations = classify_pairs(opt_ids, tag_pool, core_kws)
        output["tag_relations"]["mutex"] = relations["mutex"]
        output["tag_relations"]["ancestor"] = relations["ancestor"]

    # ────── 2. 必建：M ∩ 每个Optional ──────
    print(f"📊 开始计算MUST vs Optional（{len(optionals)}个标签）...", file=sys.stderr)
    for idx, x in enumerate(optionals, 1):
        tid = int(x["tagId"])
        tname = opt_names.get(tid, str(tid))
        name = f"{TMP_PREFIX}M_{args.audience_id_m}_x_{tid}_{idx}"
        print(f"  [{idx}/{len(optionals)}] 创建 M ∩ {tname}({tid}) ...", file=sys.stderr)
        data = build_must_tag_rules(args.audience_id_m, tid)
        res = _create_and_poll(client, data, name, args.track_type, args.id_types, args.timeout)
        entry = {"tagId": tid, "tagName": tname, "precision": "exact"}
        if res.get("success"):
            amt = res.get("amount")
            entry["audienceId"] = res["audienceId"]
            entry["amount_intersection"] = res.get("audienceAmount")
            entry["amount_int"] = amt
            entry["r"] = round(amt / m_amt, 6) if amt is not None else None
            entry["s"] = round(1 - entry["r"], 6) if entry["r"] is not None else None
            entry["or_new_people_estimate"] = None  # 需要|x|独立量级才能算
            print(f"    ✅ |M∩{tname}| = {amt:,}, r = {entry['r']}", file=sys.stderr)
        else:
            entry["error"] = res.get("error")
            entry["audienceId"] = res.get("audienceId")
            print(f"    ❌ 失败: {entry['error']}", file=sys.stderr)
        output["must_vs_optional"].append(entry)

    # ────── 3. 按需：同维度OR候选对（--or-pairs指定）──────
    or_pairs_to_calc = []
    if args.or_pairs and tag_pool:
        for pair_str in args.or_pairs.split(","):
            pair_str = pair_str.strip()
            if not pair_str or ":" not in pair_str:
                continue
            parts = pair_str.split(":")
            try:
                ta, tb = int(parts[0]), int(parts[1])
            except (ValueError, IndexError):
                continue
            # 检查是不是同维度兄弟对（排除互斥/父子）
            if is_mutex_pair(ta, tb, tag_pool):
                print(f"  ⚠️ 跳过互斥对 {_get_name(ta,tag_pool)}∩{_get_name(tb,tag_pool)}", file=sys.stderr)
                continue
            from tag_hierarchy import build_parent_map
            pmap = build_parent_map(tag_pool)
            anc = is_ancestor_pair(ta, tb, pmap)
            if anc:
                print(f"  ⚠️ 跳过祖先对 {_get_name(ta,tag_pool)}∩{_get_name(tb,tag_pool)}", file=sys.stderr)
                continue
            da = get_group_dim(ta, tag_pool, core_kws)
            db = get_group_dim(tb, tag_pool, core_kws)
            if da != db:
                print(f"  ⚠️ 跳过跨维度对 {da}×{db}（同维度OR只支持同维度）", file=sys.stderr)
                continue
            or_pairs_to_calc.append((ta, tb))

    if or_pairs_to_calc:
        print(f"\n📊 开始计算同维度OR候选对（{len(or_pairs_to_calc)}对）...", file=sys.stderr)
        for idx, (ta, tb) in enumerate(or_pairs_to_calc, 1):
            na = opt_names.get(ta) or _get_name(ta, tag_pool)
            nb = opt_names.get(tb) or _get_name(tb, tag_pool)
            dim = get_group_dim(ta, tag_pool, core_kws)
            name = f"{TMP_PREFIX}pair_{ta}_{tb}_{idx}"
            print(f"  [{idx}/{len(or_pairs_to_calc)}] 创建 {na} ∩ {nb} ({dim}) ...", file=sys.stderr)
            data = build_tag_tag_rules(ta, tb)
            res = _create_and_poll(client, data, name, args.track_type, args.id_types, args.timeout)
            entry = {
                "tagId_a": ta, "tagId_b": tb,
                "tagName_a": na, "tagName_b": nb,
                "dimension": dim,
                "precision": "exact",
                "for_or_expansion": True,
            }
            if res.get("success"):
                amt = res.get("amount")
                entry["audienceId"] = res["audienceId"]
                entry["amount_intersection"] = res.get("audienceAmount")
                entry["amount_int"] = amt
                print(f"    ✅ |{na}∩{nb}| = {amt:,}", file=sys.stderr)
            else:
                entry["error"] = res.get("error")
                print(f"    ❌ 失败: {entry['error']}", file=sys.stderr)
            output["tag_relations"]["same_dim_exact"].append(entry)

    # 输出
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    n_mvo_total = len(output["must_vs_optional"])
    n_mvo_ok = len([r for r in output["must_vs_optional"] if r.get("r") is not None])
    n_mvo_fail = n_mvo_total - n_mvo_ok
    n_pairs = len(output["tag_relations"]["same_dim_exact"])
    n_pairs_ok = len([r for r in output["tag_relations"]["same_dim_exact"] if r.get("amount_int") is not None])
    n_mutex = len(output["tag_relations"]["mutex"])
    n_ancestor = len(output["tag_relations"]["ancestor"])
    print(json.dumps({
        "ok": True,
        "must_vs_optional_total": n_mvo_total,
        "must_vs_optional_ok": n_mvo_ok,
        "must_vs_optional_fail": n_mvo_fail,
        "same_dim_pairs_total": n_pairs,
        "same_dim_pairs_ok": n_pairs_ok,
        "mutex_pairs": n_mutex,
        "ancestor_pairs": n_ancestor,
        "out": args.out,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
