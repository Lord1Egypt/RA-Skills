#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_cn_pv.py / 中国官方药物警戒通报检索（轻本地端 · v3）

WHY THIS EXISTS
──────────────
ct-base §20.14 架构下，nmpa_pv 的「抓取执行器」已上移至 Coze 统一端点
（ct-search.coze.site/run · nmpa_pv source 节点）。本模块仅保留：

  - 词表扩展（drug_name_map.json 双向索引 + 事件同义词组）
  - 证据分级（_grade_hit：通报专文 > 数据报告 > 提及）
  - 本地缓存（cn_pv_cache.json，sha1 查询指纹 + 24h TTL）
  - 结果组装（与旧版 search() 返回结构一致，下游无感消费）

网络请求 / HTML 解析 / 翻页 / 正文抓取全部上 Coze，本地零 requests 依赖。
词表扩展逻辑从 cn_pv_keywords.py 导入（单一维护点）。

方法学边界（不变）：
  - CN-PV 是叙事性官方通报，非个案计数，不可做 disproportionality 分析。
  - 仅作 FAERS 量化信号的定性佐证。
  - NMPA 主站（nmpa.gov.cn）被 WAF 拦截，不在本模块覆盖内。

Reads only public data; zero confidential data or information input.
"""

import argparse
import hashlib
import json
import os
import sys
import time

# ── 导入路径 ──────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_HERE)
_ADAPTERS_DIR = os.path.join(_SKILL_ROOT, "adapters")
_SCRIPTS_DIR = _HERE

for p in (_SCRIPTS_DIR, _ADAPTERS_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)

# 词表扩展（cn_pv_keywords.py 单一维护点）
from cn_pv_keywords import (
    expand_drug_keywords,
    expand_event_keywords,
    build_nmpa_pv_query,
    query_fingerprint,
    EVENT_SYNONYMS,
)

# Coze 统一端点外发
from coze_dispatch import dispatch as coze_dispatch

# ── 常量 ──────────────────────────────────────────────────────────────────
# 栏目名（Coze 端返回的 column 字段）
COLUMNS = [
    "药物警戒快讯",
    "数据报告",
    "通知通告",
    "器械警戒快讯",
    "化妆品警戒快讯",
]

# 佐证等级（tier）
TIER_BULLETIN = "通报专文"      # 标题即点名该药物（专文通报）
TIER_DATA_REPORT = "数据报告"   # 数据报告栏目命中
TIER_MENTION = "提及"          # 其他栏目正文提及

# 缓存有效期（小时）
_CACHE_TTL_H = 24


# ── 证据分级（本地保留，Coze 不做业务判定）────────────────────────────────
def _grade_hit(title_low, col_name, drug_hits):
    """佐证等级：标题点名药物（通报专文）> 数据报告栏目 > 一般提及。"""
    if any(d and d.lower() in title_low for d in drug_hits):
        return TIER_BULLETIN
    if col_name == "数据报告" and drug_hits:
        return TIER_DATA_REPORT
    return TIER_MENTION


# ── 摘要提取 ──────────────────────────────────────────────────────────────
def _make_snippet(text, keywords, width=120):
    """取全部命中关键词中最早两处的覆盖窗口，尽量覆盖多个命中点。"""
    low = text.lower()
    positions = []
    for kw in keywords:
        if not kw:
            continue
        i = low.find(kw.lower())
        if i >= 0:
            positions.append(i)
    if not positions:
        return text[:width]
    positions = sorted(set(positions))[:2]
    start = max(0, positions[0] - width // 3)
    end = max(positions[-1] + width, start + width)
    return text[start:end]


# ── 缓存 ──────────────────────────────────────────────────────────────────
def _cache_path(out):
    """缓存文件与 out 同目录（out 为 None 时返回 None）。"""
    if not out:
        return None
    return os.path.join(os.path.dirname(os.path.abspath(out)) or ".",
                        "cn_pv_cache.json")


def _cache_load(path, key):
    """读取缓存条目；带 _cached_at 且超过 TTL 的条目视为过期（返回 None）。"""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        entry = data.get(key)
        if entry is None:
            return None
        ts = entry.get("_cached_at") if isinstance(entry, dict) else None
        if ts is not None and _CACHE_TTL_H > 0:
            if time.time() - float(ts) > _CACHE_TTL_H * 3600:
                return None
        if isinstance(entry, dict):
            entry = dict(entry)
            entry.pop("_cached_at", None)
        return entry
    except Exception:
        return None


def _cache_save(path, key, result):
    try:
        data = {}
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        entry = dict(result)
        entry["_cached_at"] = time.time()
        data[key] = entry
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    except Exception as e:
        print("[WARN] cache write failed: %s" % e)


# ── 覆盖率说明 ────────────────────────────────────────────────────────────
def _coverage_note(stats, total_columns):
    """抓取覆盖率说明：让「0 命中」与「抓取失败」在报告层可区分。"""
    parts = ["扫描 %d 条 / %d 栏目" % (stats.get("scanned", 0), total_columns)]
    if stats.get("failed_columns"):
        names = "、".join(c["column"] for c in stats["failed_columns"])
        parts.append("⚠️ %d 个栏目抓取失败（%s）——这些栏目未覆盖"
                     % (len(stats["failed_columns"]), names))
    if stats.get("empty_columns"):
        parts.append("%d 个栏目列表为空（%s）"
                     % (len(stats["empty_columns"]), "、".join(stats["empty_columns"])))
    return "；".join(parts) + "。"


# ── 主检索函数 ────────────────────────────────────────────────────────────
def search(drug_zh, drug_en=None, event=None, terms=None, max_per=10,
           out=None, since=None, until=None, use_cache=True):
    """检索 CN-PV（cdr-adr.org.cn + nmpa.gov.cn 浏览器通道）。

    轻本地端模式：词表扩展留本地，抓取外发 Coze nmpa_pv 节点。
    返回结构与旧版 search() 完全一致（hits / tier_counts / coverage_note 等）。

    Args:
        drug_zh: 药物名（中文/英文，逗号分隔别名）
        drug_en: 药物英文名（可选）
        event: 事件关键词（可选）
        terms: 额外 AND 关键词（可选）
        max_per: 每栏目最多返回篇数
        out: 输出 JSON 路径（可选）
        since: 日期窗起点（YYYY-MM-DD 或 YYYY）
        until: 日期窗终点
        use_cache: 是否使用 cn_pv_cache.json 缓存
    """
    # ① 构造查询（本地词表扩展）
    query = build_nmpa_pv_query(drug_zh, drug_en, event, terms, max_per, since, until)
    fp = query_fingerprint(query)

    # ② 缓存命中
    cpath = _cache_path(out) if use_cache else None
    if cpath:
        cached = _cache_load(cpath, fp)
        if cached is not None:
            print("[CACHE] nmpa_pv hit (%s) — reuse cached result" % fp)
            cached = dict(cached)
            cached["from_cache"] = True
            if out and cached.get("_cached_for_out") != out:
                with open(out, "w", encoding="utf-8") as f:
                    json.dump(cached, f, ensure_ascii=False, indent=2)
                print("[OK] wrote", out, "(hits=%d, from cache)" % cached["hit_count"])
            return cached

    # ③ 外发 Coze nmpa_pv 节点
    t0 = time.time()
    try:
        result = coze_dispatch("nmpa_pv", query, run=True)
    except Exception as e:
        err = "Coze nmpa_pv 调用失败: %s: %s" % (type(e).__name__, e)
        print("[ERROR] %s" % err, file=sys.stderr)
        return {
            "source": "CN-PV (cdr-adr.org.cn)",
            "note": ("定性叙事通报检索；非个案计数，不可做 disproportionality (PRR/ROR/IC) 分析。"
                     "仅作 FAERS 量化信号的定性佐证。"),
            "query": {"drug_raw": drug_zh, "drug_en": drug_en,
                      "event": event, "terms": terms},
            "expanded_keywords": {"drug": query["drug_kws"], "event": query["event_kws"], "extra": query["extra"]},
            "searched_columns": COLUMNS,
            "max_per_column": max_per,
            "since": since, "until": until,
            "stats": {"scanned": 0, "failed_columns": [], "empty_columns": COLUMNS},
            "degraded": True,
            "coverage_note": "Coze 端点不可用，本次检索未执行（非本地抓取失败）",
            "elapsed_sec": round(time.time() - t0, 2),
            "tier_counts": {TIER_BULLETIN: 0, TIER_DATA_REPORT: 0, TIER_MENTION: 0},
            "hit_count": 0,
            "hits": [],
            "error": err,
        }

    # ④ 解析 Coze 返回
    if result is None:
        err = "Coze nmpa_pv 返回 None（可能被授权闸门拦截）"
        print("[ERROR] %s" % err, file=sys.stderr)
        return {
            "source": "CN-PV (cdr-adr.org.cn)",
            "note": "定性叙事通报检索；非个案计数。",
            "query": {"drug_raw": drug_zh, "drug_en": drug_en, "event": event, "terms": terms},
            "expanded_keywords": {"drug": query["drug_kws"], "event": query["event_kws"], "extra": query["extra"]},
            "searched_columns": COLUMNS,
            "max_per_column": max_per,
            "since": since, "until": until,
            "stats": {"scanned": 0, "failed_columns": [], "empty_columns": COLUMNS},
            "degraded": True,
            "coverage_note": err,
            "elapsed_sec": round(time.time() - t0, 2),
            "tier_counts": {TIER_BULLETIN: 0, TIER_DATA_REPORT: 0, TIER_MENTION: 0},
            "hit_count": 0,
            "hits": [],
            "error": err,
        }

    if result.get("error"):
        err = result["error"]
        print("[ERROR] Coze nmpa_pv 返回错误: %s" % err, file=sys.stderr)
        return {
            "source": "CN-PV (cdr-adr.org.cn)",
            "note": "定性叙事通报检索；非个案计数。",
            "query": {"drug_raw": drug_zh, "drug_en": drug_en, "event": event, "terms": terms},
            "expanded_keywords": {"drug": query["drug_kws"], "event": query["event_kws"], "extra": query["extra"]},
            "searched_columns": COLUMNS,
            "max_per_column": max_per,
            "since": since, "until": until,
            "stats": {"scanned": 0, "failed_columns": [], "empty_columns": COLUMNS},
            "degraded": True,
            "coverage_note": "Coze 端点返回错误: %s" % err,
            "elapsed_sec": round(time.time() - t0, 2),
            "tier_counts": {TIER_BULLETIN: 0, TIER_DATA_REPORT: 0, TIER_MENTION: 0},
            "hit_count": 0,
            "hits": [],
            "error": err,
        }

    # ⑤ 本地证据分级 + 排序
    projects = result.get("projects", [])
    drug_kw = query["drug_kws"]
    hits = []
    for proj in projects:
        title = proj.get("title", "")
        col_name = proj.get("column", "")
        title_low = title.lower()
        # 计算 drug_hit（哪些 drug_kws 实际命中了标题+正文）
        text = title + "\n" + proj.get("snippet", "")
        low = text.lower()
        drug_hit = [k for k in drug_kw if k and k.lower() in low]
        tier = _grade_hit(title_low, col_name, drug_hit)
        hits.append({
            "title": title,
            "column": col_name,
            "tier": tier,
            "date": proj.get("date"),
            "url": proj.get("url", ""),
            "snippet": proj.get("snippet", "") or _make_snippet(text, drug_kw),
            "matched_keywords": sorted(set(proj.get("matched_keywords", drug_hit))),
        })

    # 排序：等级优先，同级内日期新在前
    tier_order = {TIER_BULLETIN: 0, TIER_DATA_REPORT: 1, TIER_MENTION: 2}
    hits.sort(key=lambda h: h.get("date") or "0000-00-00", reverse=True)
    hits.sort(key=lambda h: tier_order.get(h.get("tier"), 9))

    # ⑥ 组装结果
    result_out = {
        "source": "CN-PV (cdr-adr.org.cn)",
        "note": ("定性叙事通报检索；非个案计数，不可做 disproportionality (PRR/ROR/IC) 分析。"
                 "仅作 FAERS 量化信号的定性佐证。NMPA《药品不良反应信息通报》主站被 WAF 拦截，"
                 "不在本模块覆盖内（可用 nmpa_pv Coze 通道检索）。"),
        "query": {"drug_raw": drug_zh, "drug_en": drug_en,
                  "event": event, "terms": terms},
        "expanded_keywords": {"drug": query["drug_kws"], "event": query["event_kws"], "extra": query["extra"]},
        "searched_columns": COLUMNS,
        "max_per_column": max_per,
        "since": since, "until": until,
        "stats": {
            "scanned": result.get("total_count", len(projects)),
            "failed_columns": [],
            "empty_columns": [],
        },
        "degraded": False,
        "coverage_note": _coverage_note({"scanned": result.get("total_count", len(projects))}, len(COLUMNS)),
        "elapsed_sec": round(time.time() - t0, 2),
        "tier_counts": {t: sum(1 for h in hits if h.get("tier") == t)
                        for t in (TIER_BULLETIN, TIER_DATA_REPORT, TIER_MENTION)},
        "hit_count": len(hits),
        "hits": hits,
    }

    # ⑦ 写盘 + 缓存
    if out:
        with open(out, "w", encoding="utf-8") as f:
            json.dump(result_out, f, ensure_ascii=False, indent=2)
        print("[OK] wrote", out, "(hits=%d)" % len(hits))
        result_out["_cached_for_out"] = out
    if cpath:
        _cache_save(cpath, fp, result_out)
    result_out.pop("_cached_for_out", None)
    return result_out


# ── CLI ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(
        description="Search China official PV bulletins (CN-PV). Qualitative only. 轻本地端模式，抓取外发 Coze。")
    ap.add_argument("--drug", required=True,
                    help="drug name(s), Chinese preferred; comma-separated aliases OK "
                         "(e.g. 奥希替尼 or 奥希替尼,osimertinib,泰瑞沙)")
    ap.add_argument("--drug-en", help="drug English name / synonym (e.g. osimertinib); "
                                      "auto-expanded via drug_name_map.json")
    ap.add_argument("--event", help="event keyword (e.g. 肝损伤); synonym group auto-expanded")
    ap.add_argument("--terms", nargs="*", help="extra AND keywords")
    ap.add_argument("--max-per-column", type=int, default=10,
                    help="max articles returned per column (default 10)")
    ap.add_argument("--since", help="date window start, YYYY or YYYY-MM-DD")
    ap.add_argument("--until", help="date window end, YYYY or YYYY-MM-DD")
    ap.add_argument("--no-cache", action="store_true",
                    help="disable cn_pv_cache.json reuse")
    ap.add_argument("--out", help="output JSON path")
    args = ap.parse_args()

    res = search(args.drug, args.drug_en, args.event, args.terms,
                 args.max_per_column, args.out,
                 since=args.since, until=args.until,
                 use_cache=not args.no_cache)
    if res and not args.out:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
