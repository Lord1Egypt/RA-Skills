#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dashboard.py —— 通用投标报价对比分析驾驶舱生成器（配置驱动）

    用法:
        python build_dashboard.py --config ./config.json [--out ./看板.html] [--report]

    设计要点:
        * 全部输入来自 config.json / quotes.json / history.json，不含任何门店或供应商硬编码
        * 条件模块: 明细(需 items) / 异常(需零单价) / 历史(需 history.json) —— 不满足则整节不渲染
        * 所有 ECharts option 在 Python 侧算好，JS 只负责 setOption + tab 交互，降低运行时风险
        * echarts 内联，产出为离线自包含单文件 HTML

    数据契约见 ../references/data-contract.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ECHARTS_PATH = SKILL_DIR / "assets" / "echarts.min.js"

# 色板(主/浅)：莫兰迪低饱和多彩。禁用纯粉/纯红/高饱和
PALETTE = [
    ("#3E6E9E", "#B3C5DA"),  # 钢蓝
    ("#3E8E80", "#B3D4D0"),  # 雾青
    ("#C99245", "#EDD5B5"),  # 琥珀
    ("#8B7FA8", "#CFC9DD"),  # 紫灰
    ("#2E6B66", "#C9DED9"),  # 深青
    ("#A68A5B", "#E6D9BE"),  # 驼色
    ("#7A8B5A", "#D6DECB"),  # 橄榄
    ("#5C7A99", "#C6D2DE"),  # 灰蓝
]
C_AMBER = "#B5791F"      # 成本上涨 / 历史均值线
C_GREEN = "#2E6B66"      # 成本下降
C_MEAN = "#5D4E75"       # 本项目均值线
SUBTLE_ROWS = ("小计", "合计", "TOTAL", "Subtotal", "Grand Total", "总计")


# --------------------------------------------------------------------------
# 基础工具
# --------------------------------------------------------------------------
def load_json(path):
    p = Path(path)
    if not p.is_file():
        raise SystemExit("文件不存在: %s" % p)
    return json.loads(p.read_text(encoding="utf-8"))


def money(v, cur="€"):
    if v is None:
        return "—"
    return "%s%s" % (cur, format(float(v), ",.2f"))


def kfmt(v):
    """图表标签用的紧凑金额"""
    if v is None:
        return ""
    return "€%dk" % round(float(v) / 1000)


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def rich(s):
    """esc + 把数据里的 **强调** 转成 <b>，供长文本区块渲染（避免页面上出现字面星号）。"""
    t = esc(s)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t, flags=re.S)


def dsc(s, n=42):
    """描述截断助手（与校验器无关，纯展示）"""
    s = str(s or "").replace("\n", " / ").strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def norm_desc(s):
    """描述级匹配键：首行 → 剥离中文 → 去符号 → 小写"""
    s = str(s or "").split("\n")[0]
    s = re.sub(r"[\u4e00-\u9fff]+", "", s)
    return re.sub(r"[^A-Za-z0-9]+", "", s).lower()


def round_used(r):
    """本轮采用价：used → promo → opt1 → total"""
    if not isinstance(r, dict):
        return None
    if r.get("used") not in (None, ""):
        return float(r["used"])
    for k in ("promo", "opt1", "total"):
        v = r.get(k)
        if v not in (None, "", 0):
            return float(v)
    return None


def is_subtotal(desc):
    d = str(desc or "")
    return any(k in d for k in SUBTLE_ROWS)


# --------------------------------------------------------------------------
# 模型构建
# --------------------------------------------------------------------------
def build_model(cfg, quotes, hist):
    cats = quotes.get("cats") or []
    cat_cns = [c.get("cn") or c.get("key") for c in cats]
    cat_keys = [c.get("key") for c in cats]
    ncat = len(cats)
    area = float(cfg.get("area_sqm") or 0)
    cur = cfg.get("currency", "€")
    rounds = cfg.get("rounds") or [{"key": "r1", "label": "报价"}]
    used_round = cfg.get("used_round") or rounds[-1]["key"]
    facade_key = cfg.get("facade_cat_key")
    facade_idx = cat_keys.index(facade_key) if facade_key in cat_keys else None

    colors = cfg.get("colors") or {}
    vendors = []
    for i, sv in enumerate(quotes.get("suppliers") or []):
        main, light = PALETTE[i % len(PALETTE)]
        c = sv.get("color") or colors.get(sv.get("name")) or {}
        vendors.append({
            "name": sv.get("name") or ("供应商%d" % (i + 1)),
            "main": c.get("main", main),
            "light": c.get("light", light),
            "status": sv.get("status") or "",
            "rounds": sv.get("rounds") or {},
            "complete": sv.get("complete"),   # 可显式覆盖完整性判定
            # 整包价 / 未提供分项拆分：总价有效可参与排名，但不进分项图，
            # 且其「分项求和 vs 采用价」勾稽转为口径说明（已注明），不判差错
            "noBreakdown": bool(sv.get("noBreakdown")),
        })

    # ---- 各家各轮数据规整 ----
    for v in vendors:
        v["data"] = {}
        for rd in rounds:
            rk = rd["key"]
            raw = v["rounds"].get(rk)
            if not raw:
                v["data"][rk] = None
                continue
            cvals = raw.get("cats")
            items = [it for it in (raw.get("items") or []) if not is_subtotal(it.get("desc"))]
            if not cvals and items:
                cvals = [0.0] * ncat
                for it in items:
                    ck = it.get("cat_key")
                    idx = cat_keys.index(ck) if ck in cat_keys else (
                        cat_cns.index(it.get("cat")) if it.get("cat") in cat_cns else None)
                    if idx is not None:
                        cvals[idx] += float(it.get("amount") or 0)
            cvals = [float(x or 0) for x in (cvals or [])]
            if len(cvals) != ncat:
                raise SystemExit("分项数量不符: %s / %s -> %d 项，应为 %d 项"
                                 % (v["name"], rk, len(cvals), ncat))

            # 零单价：一律逐条重算，不采信任何汇总字段
            zero_items = [it for it in items
                          if it.get("unit_price") in (None, 0, "") or it.get("zero")]
            zero_by_cat = [0] * ncat
            for it in zero_items:
                ck = it.get("cat_key")
                idx = cat_keys.index(ck) if ck in cat_keys else (
                    cat_cns.index(it.get("cat")) if it.get("cat") in cat_cns else None)
                if idx is not None:
                    zero_by_cat[idx] += 1

            v["data"][rk] = {
                "used": round_used(raw),
                "total": raw.get("total"),
                "original_total": raw.get("original_total"),
                "opt1": raw.get("opt1"),
                "opt2": raw.get("opt2"),
                "promo": raw.get("promo"),
                "cats": cvals,
                "items": items,
                "zero_count": len(zero_items),
                "zero_by_cat": zero_by_cat,
                "item_count": len(items),
                "note": raw.get("note") or "",
                "source": raw.get("source") or "",
            }

    # ---- 采用轮价格（无本轮报价则沿用上一轮补位） ----
    for v in vendors:
        cur_data = v["data"].get(used_round)
        prev_data = None
        for rd in rounds:
            if rd["key"] == used_round:
                break
            if v["data"].get(rd["key"]):
                prev_data = v["data"][rd["key"]]
        if cur_data and cur_data["used"] is not None:
            v["used"] = cur_data["used"]
            v["used_actual"] = True
        elif prev_data:
            v["used"] = prev_data["used"]
            v["used_actual"] = False
            if not v["status"]:
                v["status"] = "沿用%s·无更新" % dict(
                    (r["key"], r["label"]) for r in rounds)[
                    [r["key"] for r in rounds][
                        [r["key"] for r in rounds].index(used_round) - 1]] \
                    if [r["key"] for r in rounds].index(used_round) > 0 else "上轮"
        else:
            v["used"] = None
            v["used_actual"] = False
        v["sq"] = (v["used"] / area) if (v["used"] is not None and area) else None
        v["prev"] = prev_data

        # 涨跌
        v["delta"] = None
        if v["used"] is not None and prev_data and prev_data["used"]:
            diff = v["used"] - prev_data["used"]
            v["delta"] = {"abs": diff, "pct": diff / prev_data["used"] * 100}

        # 剔除外立面
        v["nofac"] = None
        if v["used"] is not None and facade_idx is not None:
            d = v["data"].get(used_round) or prev_data
            if d:
                v["nofac"] = v["used"] - d["cats"][facade_idx]

    # ---- 完整性判定 ----
    for v in vendors:
        d = v["data"].get(used_round) or v["prev"]
        n = d["item_count"] if d else 0
        z = d["zero_count"] if d else 0
        excluded = "不采用" in (v["status"] or "")
        if v.get("complete") is False:
            incomplete = True
        elif v.get("complete") is True:
            incomplete = False
        else:
            incomplete = excluded or (n > 0 and z / n > 0.10)
        v["excluded"] = excluded
        v["incomplete"] = incomplete
        v["zero_count"] = z
        v["item_count"] = n

    # ---- 排名（含沿用补位） ----
    valid = [v for v in vendors if v["used"] is not None and not v["excluded"]]
    ranked = sorted(valid, key=lambda x: x["used"])
    for i, v in enumerate(ranked):
        v["rank"] = i + 1
    for v in vendors:
        v.setdefault("rank", None)

    eff = [v for v in valid if not v["incomplete"]]
    for i, v in enumerate(sorted(eff, key=lambda x: x["used"])):
        v["rank_eff"] = i + 1
    for v in vendors:
        v.setdefault("rank_eff", None)

    # ---- 统计 ----
    used_vals = [v["used"] for v in valid]
    model = {
        "meta": {
            "project": cfg.get("project", "投标报价对比分析"),
            "subtitle": cfg.get("subtitle", ""),
            "version": cfg.get("version", "V1"),
            "area": area,
            "areaNote": cfg.get("area_note", ""),
            "currency": cur,
            "basis": cfg.get("basis", ""),
            "rounds": rounds,
            "usedRound": used_round,
            "facadeIdx": facade_idx,
            "facadeCn": cat_cns[facade_idx] if facade_idx is not None else None,
        },
        "cats": [{"key": c.get("key"), "cn": c.get("cn"), "en": c.get("en", "")} for c in cats],
        "vendors": vendors,
        "stats": {
            "min": min(used_vals) if used_vals else None,
            "max": max(used_vals) if used_vals else None,
            "mean": (sum(used_vals) / len(used_vals)) if used_vals else None,
            "spread": (max(used_vals) - min(used_vals)) if used_vals else None,
            "n_valid": len(valid),
            "n_eff": len(eff),
            "area": area,
        },
        "notes": quotes.get("notes") or {},
        "addenda": quotes.get("addenda") or [],
        "hist": None,
        "charts": {},
        "staticCharts": [],
    }

    # ---- 分项均值（本项目） ----
    cat_means = {}
    for rd in rounds:
        rk = rd["key"]
        arr = []
        for i in range(ncat):
            vals = [v["data"][rk]["cats"][i] for v in vendors
                    if v["data"].get(rk) and v["data"][rk]["cats"]
                    and not v.get("noBreakdown")]     # 整包价单位不进分项均值
            arr.append(round(sum(vals) / len(vals), 2) if vals else None)
        cat_means[rk] = arr
    model["catMeans"] = cat_means
    model["noBreakdown"] = [v["name"] for v in vendors if v.get("noBreakdown")]

    # ---- 历史数据（可选） ----
    if hist and hist.get("stores"):
        hcats = hist.get("cats") or cat_cns
        stores = []
        for s in hist["stores"]:
            area_s = float(s.get("area") or 0)
            total = s.get("total")
            sq = s.get("sq")
            if total and area_s:
                sq = float(total) / area_s
            stores.append({
                "name": s.get("name", ""),
                "area": area_s,
                "total": float(total) if total else None,
                "sq": float(sq) if sq else None,
                "cats": s.get("cats") or None,
                "hasCats": bool(s.get("cats")),
                "note": s.get("note", ""),
            })
        hmean = []
        for cn in hcats:
            vals = [st["cats"][cn] for st in stores
                    if st["hasCats"] and isinstance(st["cats"].get(cn), (int, float))]
            hmean.append(round(sum(vals) / len(vals), 2) if vals else None)
        model["hist"] = {"cats": hcats, "stores": stores, "catMeans": hmean}

    return model


# --------------------------------------------------------------------------
# 条件模块判定
# --------------------------------------------------------------------------
def module_gate(cfg, model):
    mods = cfg.get("modules") or {}
    q = model["vendors"]
    has_items = any(v["data"].get(r["key"]) and v["data"][r["key"]]["items"]
                    for v in q for r in model["meta"]["rounds"])
    has_zero = any(v["zero_count"] > 0 for v in q)
    has_hist = bool(model.get("hist"))
    has_add = bool(model.get("addenda"))
    auto = {
        "overview": True, "profile": True, "totals": True, "category": True,
        "reconcile": True, "actions": True,
        "detail": has_items, "anomaly": has_zero, "history": has_hist,
        "addenda": has_add,
    }
    out, log = {}, []
    for k, v in auto.items():
        force = mods.get(k)
        if force is True:
            out[k] = True
            if not v:
                log.append("模块[%s] 被强开但数据不足，可能产生空图" % k)
        elif force is False:
            out[k] = False
            log.append("模块[%s] 已手动关闭" % k)
        else:
            out[k] = v
    model["modules"] = out
    model["moduleLog"] = log
    return out


# --------------------------------------------------------------------------
# 明细矩阵（描述级匹配）
# --------------------------------------------------------------------------
def build_item_matrix(model):
    cats = model["cats"]
    rounds = model["meta"]["rounds"]
    used_rk = model["meta"]["usedRound"]
    out = []
    for i, c in enumerate(cats):
        rows, index = [], {}
        for v in model["vendors"]:
            d = v["data"].get(used_rk)
            if not d:
                continue
            for it in d["items"]:
                ck = it.get("cat_key")
                cn = it.get("cat")
                same = (ck and ck == c["key"]) or (cn and cn == c["cn"])
                if not same:
                    continue
                k = norm_desc(it.get("desc"))
                if not k:
                    continue
                if k not in index:
                    index[k] = len(rows)
                    rows.append({"desc": it.get("desc"), "vals": {}})
                rows[index[k]]["vals"][v["name"]] = float(it.get("amount") or 0)
        out.append({"cn": c["cn"], "rows": rows})
    return out


# --------------------------------------------------------------------------
# ECharts option 构造
# --------------------------------------------------------------------------
GRID = {"left": 60, "right": 24, "top": 48, "bottom": 56, "containLabel": True}


def axis_style():
    return ({"axisLine": {"lineStyle": {"color": "#C9D2DA"}},
             "axisLabel": {"color": "#5A6672", "fontSize": 11},
             "splitLine": {"lineStyle": {"color": "#EEF2F6"}}},
            {"axisLine": {"lineStyle": {"color": "#C9D2DA"}},
             "axisLabel": {"color": "#5A6672", "fontSize": 11},
             "splitLine": {"lineStyle": {"color": "#EEF2F6", "type": "dashed"}}})


def base_opt(title):
    x, y = axis_style()
    return {"title": {"text": title, "left": 8, "top": 6,
                      "textStyle": {"fontSize": 13, "fontWeight": 700, "color": "#2C3742"}},
            "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
            "legend": {"top": 6, "right": 8, "textStyle": {"fontSize": 10, "color": "#5A6672"},
                       "itemWidth": 12, "itemHeight": 8, "type": "scroll"},
            "grid": dict(GRID), "xAxis": x, "yAxis": y, "series": []}


def mean_series(name, data, color=C_MEAN):
    """均值线序列：z 层级高于 bar，label 带白底，避免被 bar/线条遮盖或相互压字。"""
    return {"name": name, "type": "line", "symbol": "diamond", "symbolSize": 7,
            "data": data, "z": 10,
            "lineStyle": {"color": color, "type": "dashed", "width": 1.5},
            "itemStyle": {"color": color, "borderColor": "#fff", "borderWidth": 1},
            "label": {"show": True, "position": "top", "fontSize": 9,
                      "fontWeight": 700, "color": color,
                      "backgroundColor": "rgba(255,255,255,0.85)",
                      "padding": [2, 4], "borderRadius": 3,
                      "formatter": "{@[0]}"},
            "labelLayout": {"hideOverlap": True}}


def build_charts(model):
    ch = {}
    static_ids = []
    meta = model["meta"]
    cats_cn = [c["cn"] for c in model["cats"]]
    vendors = model["vendors"]
    rounds = meta["rounds"]
    used_rk = meta["usedRound"]
    hist = model.get("hist")
    area = meta["area"]

    # ===== 三、总价 / 单方 / 剔除后 =====
    names = [v["name"] for v in vendors]
    for cid, title, keyfn in (
            ("cTotal", "各家报价对比（%s）" % dict((r["key"], r["label"]) for r in rounds)[used_rk],
             lambda v: round(v["used"], 2) if v["used"] is not None else None),
            ("cSq", "单方造价对比（%s/㎡）" % meta["currency"],
             lambda v: round(v["sq"], 2) if v["sq"] is not None else None),
            ("cNoFac", "剔除%s后对比" % (meta["facadeCn"] or "指定分项"),
             lambda v: round(v["nofac"], 2) if v["nofac"] is not None else None)):
        if cid == "cNoFac" and meta["facadeIdx"] is None:
            continue
        o = base_opt(title)
        o["xAxis"]["data"] = names
        o["yAxis"]["type"] = "value"
        o["xAxis"]["type"] = "category"
        o["series"] = [{"name": "报价", "type": "bar", "barMaxWidth": 42,
                        "data": [{"value": keyfn(v),
                                  "itemStyle": {"color": v["main"] if v["used_actual"] else v["light"]}}
                                 for v in vendors],
                        "label": {"show": True, "position": "top", "fontSize": 10,
                                  "color": "#5A6672",
                                  "formatter": "{c}"}}]
        ch[cid] = o
        static_ids.append(cid)

    # ===== 四、分部分项（各轮 × 金额/单方） =====
    for rd in rounds:
        rk = rd["key"]
        for suffix, unit_mode, unit_name in (("", False, meta["currency"]),
                                             ("Unit", True, "%s/㎡" % meta["currency"])):
            cid = "cCat%s%s" % (rk.upper(), suffix)
            o = base_opt("%s · 分部分项对比（%s）" % (rd["label"], unit_name))
            o["xAxis"]["type"] = "category"
            o["xAxis"]["data"] = cats_cn
            o["xAxis"]["axisLabel"] = {"color": "#5A6672", "fontSize": 10, "interval": 0,
                                       "rotate": 18}
            o["yAxis"]["type"] = "value"
            series = []
            for v in vendors:
                if v.get("noBreakdown"):
                    continue          # 整包价单位无分项，画 0 柱会被误读为「该项报价 0」
                d = v["data"].get(rk) or (v["prev"] if rk == used_rk else None)
                if not d:
                    continue
                vals = [round(x / area, 2) if unit_mode else round(x, 2) for x in d["cats"]]
                series.append({"name": v["name"] + ("" if v["data"].get(rk) else "（沿用）"),
                               "type": "bar", "barMaxWidth": 14,
                               "itemStyle": {"color": v["main"] if v["data"].get(rk) else v["light"]},
                               "data": vals})
            means = model["catMeans"].get(rk) or []
            mv = [round(x / area, 2) if (unit_mode and x is not None) else x for x in means]
            if any(x is not None for x in mv):
                series.append(mean_series("本项目均值", mv, C_MEAN))
            if hist and any(x is not None for x in hist["catMeans"]):
                hm = hist["catMeans"]
                hv = [round(x / area, 2) if (unit_mode and x is not None) else x for x in hm]
                series.append(mean_series("历史均值", hv, C_AMBER))
            o["series"] = series
            ch[cid] = o
            static_ids.append(cid)

    # ===== 七、历史对比（各家 vs 历史门店） =====
    if hist:
        hstores = [s for s in hist["stores"] if s["hasCats"]]
        for vi, v in enumerate(vendors):
            if not hstores:
                break                 # 历史门店均无分项拆分 → 7.1 不渲染，只做单方对比
            if v.get("noBreakdown"):
                continue              # 整包价单位无分项，不画「vs 历史门店（分部分项）」
            d = v["data"].get(used_rk) or v["prev"]
            if not d:
                continue
            cid = "cHist%d" % vi          # 用序号而非名称，避免名称归一化后 ID 碰撞
            o = base_opt("%s vs 历史门店（分部分项）" % v["name"])
            o["xAxis"]["type"] = "category"
            o["xAxis"]["data"] = cats_cn
            o["xAxis"]["axisLabel"] = {"color": "#5A6672", "fontSize": 10, "interval": 0,
                                       "rotate": 18}
            o["yAxis"]["type"] = "value"
            series = [{"name": v["name"], "type": "bar", "barMaxWidth": 14,
                       "itemStyle": {"color": v["main"]},
                       "data": [round(x, 2) for x in d["cats"]]}]
            for j, s in enumerate(hstores):
                series.append({"name": s["name"], "type": "bar", "barMaxWidth": 14,
                               "itemStyle": {"color": ["#5E8B7C", "#7A9F94", "#A2B5B0",
                                                       "#8FA3B8", "#B0A48C"][j % 5]},
                               "data": [round(float(s["cats"].get(cn) or 0), 2)
                                        for cn in cats_cn]})
            if any(x is not None for x in hist["catMeans"]):
                series.append(mean_series("历史均值", hist["catMeans"], C_AMBER))
            o["series"] = series
            ch[cid] = o
            static_ids.append(cid)

        # 单方对比（本项目各单位 + 历史门店，同一 €/㎡ 口径）
        o = base_opt("全门店单方造价对比（%s/㎡）" % meta["currency"])
        n_v = len(vendors)
        names_sq = [v["name"] for v in vendors if v["sq"] is not None]
        vals_sq = [round(v["sq"], 2) for v in vendors if v["sq"] is not None]
        hvals_sq = []
        for s in hist["stores"]:
            if s["sq"] is not None:
                names_sq.append(s["name"])
                vals_sq.append(round(s["sq"], 2))
                hvals_sq.append(round(s["sq"], 2))
        o["xAxis"]["type"] = "category"
        o["xAxis"]["data"] = names_sq
        o["xAxis"]["axisLabel"] = {"color": "#5A6672", "fontSize": 10, "interval": 0,
                                   "rotate": 18}
        o["yAxis"]["type"] = "value"
        # 本项目与历史门店用两段不同色，避免读成一类
        o["series"] = [
            {"name": "本项目各单位", "type": "bar", "barMaxWidth": 34, "z": 2,
             "data": vals_sq[:n_v] + [None] * (len(vals_sq) - n_v),
             "itemStyle": {"color": "#3E6E9E"},
             "label": {"show": True, "position": "top", "fontSize": 10,
                       "color": "#2C3742", "fontWeight": 700},
             "labelLayout": {"hideOverlap": True}},
            # 历史门店只作参考柱，不显示顶部数值（数量多会堆叠压字），精确值进 tooltip
            {"name": "历史门店", "type": "bar", "barMaxWidth": 34, "z": 2,
             "data": [None] * n_v + vals_sq[n_v:],
             "itemStyle": {"color": "#A8BCCF"},
             "label": {"show": False}},
        ]
        # 过往项目均值线（历史门店单方均值，橙虚线菱形）
        if hvals_sq:
            hmean_sq = round(sum(hvals_sq) / len(hvals_sq), 2)
            o["series"].append({
                "name": "过往项目单方均值", "type": "line", "symbol": "none",
                "data": [hmean_sq] * len(names_sq),
                "z": 10, "silent": True,
                "lineStyle": {"color": C_AMBER, "type": "dashed", "width": 1.6},
                "itemStyle": {"color": C_AMBER},
                # 均值线标签：白底+ padding，确保压在线/柱之上清晰可读；
                # 用 markLine.label 单标签，去掉冗余的 endLabel，避免多标签重叠
                "markLine": {"silent": True, "symbol": "none", "z": 10,
                             "lineStyle": {"color": C_AMBER, "type": "dashed", "width": 1.6},
                             "label": {"show": True, "position": "insideEndTop",
                                       "formatter": "过往项目单方均值 %s%s/㎡"
                                                    % (meta["currency"], hmean_sq),
                                       "color": C_AMBER, "fontSize": 10, "fontWeight": 700,
                                       "backgroundColor": "rgba(255,255,255,0.85)",
                                       "padding": [3, 6], "borderRadius": 3, "z": 11},
                             "data": [{"yAxis": hmean_sq}]},
            })
        ch["cHistSq"] = o
        static_ids.append("cHistSq")

    # ===== 六、异常核查图 =====
    if model["modules"].get("anomaly"):
        anom = [v for v in vendors if v["zero_count"] > 0]
        if anom:
            o = base_opt("异常条目分布（各供应商）")
            o["xAxis"]["type"] = "category"
            o["xAxis"]["data"] = cats_cn
            o["xAxis"]["axisLabel"] = {"color": "#5A6672", "fontSize": 10, "interval": 0,
                                       "rotate": 18}
            o["yAxis"]["type"] = "value"
            o["series"] = [{"name": v["name"], "type": "bar", "barMaxWidth": 14,
                            "itemStyle": {"color": v["main"]},
                            "data": (v["data"].get(used_rk) or v["prev"] or {}).get("zero_by_cat") or []}
                           for v in anom]
            ch["cAnomCat"] = o
            static_ids.append("cAnomCat")

            o2 = {"title": {"text": "报价完整性构成", "left": 8, "top": 6,
                            "textStyle": {"fontSize": 13, "fontWeight": 700, "color": "#2C3742"}},
                  "tooltip": {"trigger": "item"},
                  "legend": {"bottom": 4, "textStyle": {"fontSize": 10, "color": "#5A6672"}},
                  "series": []}
            for v in anom:
                d = v["data"].get(used_rk) or v["prev"] or {}
                ok = (d.get("item_count") or 0) - (d.get("zero_count") or 0)
                o2["series"].append({
                    "name": v["name"], "type": "pie", "radius": ["38%", "62%"],
                    "center": ["50%", "54%"],
                    "data": [{"name": "有单价", "value": ok, "itemStyle": {"color": v["main"]}},
                             {"name": "零单价/缺项", "value": d.get("zero_count") or 0,
                              "itemStyle": {"color": v["light"]}}],
                    "label": {"fontSize": 10, "color": "#5A6672"}})
            ch["cAnomPie"] = o2
            static_ids.append("cAnomPie")

    model["charts"] = ch
    model["staticCharts"] = static_ids
    return model


# --------------------------------------------------------------------------
# 勾稽与行动清单
# --------------------------------------------------------------------------
def build_checks(model):
    checks = []
    meta = model["meta"]
    for v in model["vendors"]:
        d = v["data"].get(meta["usedRound"])
        if not d:
            continue
        # 整包价单位：原文未提供分项拆分，不判「勾稽差异」，改判口径说明（已注明）
        if v.get("noBreakdown"):
            checks.append({"name": "%s · 分项求和 vs 采用价" % v["name"],
                           "ok": True, "warn": True,
                           "detail": "原文未提供分项拆分（整包价），分项和为 0、采用价 %s，"
                                     "二者不可勾稽，属口径说明而非差错；该单位不进入分项对比图"
                                     % money(d["used"], meta["currency"])})
            continue
        s = sum(d["cats"])
        if d["used"] is not None:
            diff = s - d["used"]
            checks.append({"name": "%s · 分项求和 vs 采用价" % v["name"],
                           "ok": abs(diff) <= 0.05,
                           "detail": "分项和 %s，采用价 %s，差 %s"
                                     % (money(s, meta["currency"]), money(d["used"], meta["currency"]),
                                        money(round(diff, 2), meta["currency"]))})
        if d["items"]:
            for i, c in enumerate(model["cats"]):
                sub = sum(float(it.get("amount") or 0) for it in d["items"]
                          if (it.get("cat_key") == c["key"] or it.get("cat") == c["cn"]))
                diff = sub - d["cats"][i]
                if abs(diff) > 0.05:
                    checks.append({"name": "%s · %s 明细求和 vs 分项小计" % (v["name"], c["cn"]),
                                   "ok": False,
                                   "detail": "明细和 %s，分项 %s，差 %s"
                                             % (money(sub, meta["currency"]),
                                                money(d["cats"][i], meta["currency"]),
                                                money(round(diff, 2), meta["currency"]))})
        if d.get("original_total") and d["used"] is not None and abs(d["original_total"] - d["used"]) > 0.05:
            checks.append({"name": "%s · 采用价 vs 原文总价" % v["name"],
                           "ok": True, "warn": True,
                           "detail": "原文 %s，采用 %s，差 %s（优惠/方案口径，属已知差异，非差错）"
                                     % (money(d["original_total"], meta["currency"]),
                                        money(d["used"], meta["currency"]),
                                        money(round(d["used"] - d["original_total"], 2), meta["currency"]))})
    return checks


def build_actions(model):
    acts = []
    meta = model["meta"]
    cur = meta["currency"]
    for v in model["vendors"]:
        if v["excluded"]:
            acts.append({"p": "P0", "text": "确认报价有效性：文件多数分项为 0，判定未填完，需重新提交完整报价",
                         "who": v["name"], "basis": "完整性判定"})
        elif v["incomplete"]:
            acts.append({"p": "P0", "text": "发出澄清函，要求补齐 %d 条零单价/缺项条目并书面确认是否已含在其它条目中"
                         % v["zero_count"], "who": v["name"],
                         "basis": "零单价 %d / 共 %d 条" % (v["zero_count"], v["item_count"])})
        if not v["used_actual"]:
            acts.append({"p": "P1", "text": "催促提交本轮报价（当前沿用上轮价参与排名）",
                         "who": v["name"], "basis": "无本轮报价"})
    eff = [v for v in model["vendors"] if not v["incomplete"] and v["used"] is not None]
    if eff:
        best = sorted(eff, key=lambda x: x["used"])[0]
        acts.append({"p": "P1", "text": "以 %s 作为有效可比最低价推进定标（%s，单方 %s）"
                     % (best["name"], money(best["used"], cur),
                        money(best["sq"], cur) if best["sq"] else "—"),
                     "who": "决策", "basis": "有效可比排名"})
    for ad in (model.get("addenda") or []):
        who = ad.get("vendor", "")
        n = len(ad.get("items", []))
        acts.append({"p": "P0",
                     "text": "就 %d 项清单外增项（原文不含税 %s / 含税 %s）发出书面澄清："
                             "确认哪些属其自身法定合规义务、哪些应由业主另计，并要求逐项拆分报价"
                             % (n, money(ad.get("subtotal_printed"), cur),
                                money(ad.get("total"), cur)),
                     "who": who, "basis": ad.get("source", "邮件补充报价")})
        acts.append({"p": "P0",
                     "text": "对齐四家单位合规口径：要求全部投标方书面声明是否已含电气合法化+OCA、"
                             "安全协调员、安全计划、开设工作中心申报、分包台账、REA 登记",
                     "who": "全部 4 家", "basis": "避免范围不一致导致总价不可比"})
        if ad.get("sum_unit_col") is not None and abs(
                (ad.get("subtotal_printed") or 0) - ad["sum_unit_col"]) > 0.05:
            acts.append({"p": "P1",
                         "text": "核对增项清单内部勾稽：原文小计 %s 与逐项相加 %s 差 %s，需其书面更正"
                                 % (money(ad.get("subtotal_printed"), cur),
                                    money(ad["sum_unit_col"], cur),
                                    money(round((ad.get("subtotal_printed") or 0)
                                                - ad["sum_unit_col"], 2), cur)),
                         "who": who, "basis": "增项表内部金额不一致"})
    for v in model["vendors"]:
        if v.get("noBreakdown"):
            acts.append({"p": "P1",
                         "text": "总价有效但未提供分项拆分，分项级不可比；"
                                 "建议要求按 BOQ 口径补充逐条拆分以便同口径核价",
                         "who": v["name"], "basis": "整包价 / 无分项拆分"})
    return acts


# --------------------------------------------------------------------------
# HTML 渲染
# --------------------------------------------------------------------------
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
background:#F4F7FA;color:#2C3742;line-height:1.6;padding:28px 18px 60px}
.wrap{max-width:1360px;margin:0 auto}
header{background:linear-gradient(135deg,#3E6E9E 0%,#3E8E80 100%);color:#fff;
border-radius:14px;padding:26px 30px;margin-bottom:22px;box-shadow:0 4px 18px rgba(62,110,158,.18)}
header h1{font-size:24px;font-weight:700;letter-spacing:.5px}
header .sub{opacity:.9;font-size:13px;margin-top:6px}
header .tags{margin-top:12px;display:flex;gap:8px;flex-wrap:wrap}
.tag{background:rgba(255,255,255,.18);border-radius:20px;padding:3px 12px;font-size:12px}
.sec{background:#fff;border-radius:12px;padding:22px 24px;margin-bottom:20px;
box-shadow:0 2px 10px rgba(44,55,66,.06)}
.sec h2{font-size:17px;font-weight:700;color:#2C3742;margin-bottom:4px;
padding-left:11px;border-left:4px solid #3E6E9E}
.sec .desc{font-size:12.5px;color:#6B7785;margin:6px 0 16px;padding-left:15px}
.subttl{font-size:13px;font-weight:700;color:#3E6E9E;margin:18px 0 9px}
.note{background:#F7F9FB;border-left:3px solid #C9D2DA;border-radius:6px;
padding:10px 14px;font-size:12px;color:#5A6672;margin-top:12px;line-height:1.75}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th{background:#EEF3F7;color:#3D4A57;font-weight:700;text-align:right;padding:9px 10px;
border-bottom:2px solid #D6DEE6;white-space:nowrap}
th:first-child{text-align:left}
td{padding:8px 10px;border-bottom:1px solid #EDF1F5;text-align:right;white-space:nowrap}
td:first-child{text-align:left;font-weight:600}
tbody tr:hover{background:#F8FAFC}
/* 长文本表格：列宽受控 + 强制换行，避免 nowrap 把整表撑出卡片（附录 A 等） */
.tblscroll{overflow-x:auto;margin-bottom:4px}
table.fixed{table-layout:fixed}
table.fixed th,table.fixed td{white-space:normal;word-break:break-word;overflow-wrap:anywhere}
table.fixed td.lft,table.fixed th.lft{text-align:left}
td.lft,th.lft{text-align:left}
td.wrapcell{white-space:normal;text-align:left;word-break:break-word;overflow-wrap:anywhere}
.mono{font-variant-numeric:tabular-nums}
.best{color:#2E6B66;font-weight:700}
.badge{display:inline-block;border-radius:11px;padding:1px 9px;font-size:11px;font-weight:700}
.b1{background:#3E6E9E;color:#fff}
.b2{background:#8B7FA8;color:#fff}
.b3{background:#C99245;color:#fff}
.bn{background:#E7EBEF;color:#6B7785}
.bw{background:#F7EEDC;color:#8A6218}
/* 指标速览带 */
.mstrip{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:18px}
@media(max-width:1080px){.mstrip{grid-template-columns:repeat(2,1fr)}}
.mitem{background:#FAFCFD;border:1px solid #E8EEF3;border-radius:10px;padding:13px 15px;
border-left:4px solid #3E6E9E}
.mitem .lbl{font-size:11.5px;color:#7A8794;margin-bottom:5px}
.mitem .val{font-size:20px;font-weight:700;color:#2C3742;line-height:1.25}
.mitem .sub{font-size:11px;color:#8A96A3;margin-top:3px}
.m2{border-left-color:#3E8E80}.m3{border-left-color:#C99245}
.m4{border-left-color:#B5791F}.m5{border-left-color:#8B7FA8}
/* 报价标尺 */
.pscale{border:1px solid #E8EEF3;border-radius:10px;padding:14px 16px;margin-bottom:6px}
.psrow{display:grid;grid-template-columns:132px 1fr 176px;gap:12px;align-items:center;
padding:9px 0;border-bottom:1px dashed #EDF1F5}
.psrow:last-child{border-bottom:none}
.psname{font-size:12.5px;font-weight:700}
.pstrack{background:#F1F5F8;border-radius:5px;height:26px;position:relative;overflow:hidden}
.psfill{height:11px;border-radius:4px;margin:3px 0;min-width:2px}
.psval{font-size:12.5px;text-align:right}
.psval .t{font-weight:700}
.dchip{display:inline-block;border-radius:10px;padding:1px 8px;font-size:11px;font-weight:700}
.dchip.up{background:#F7EEDC;color:#8A6218}
.dchip.dn{background:#DCE9E5;color:#2E6B66}
.dchip.na{background:#E7EBEF;color:#8A96A3}
.pslegend{display:flex;gap:16px;flex-wrap:wrap;font-size:11.5px;color:#7A8794;margin-top:10px}
.lgsw{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:5px;
vertical-align:-1px}
/* 卡片网格 */
.vgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
@media(max-width:1080px){.vgrid{grid-template-columns:repeat(2,1fr)}}
.vcard{border:1px solid #E8EEF3;border-radius:11px;padding:15px 16px;background:#fff;
transition:box-shadow .18s}
.vcard:hover{box-shadow:0 4px 14px rgba(44,55,66,.09)}
.vcard .vbarwr{background:#EFF3F7;border-radius:4px;height:7px;margin-bottom:11px;overflow:hidden}
.vcard .vbar{height:7px;border-radius:4px}
.vcard .vn{font-size:14px;font-weight:700;margin-bottom:8px}
.vcard .vp{font-size:21px;font-weight:700;line-height:1.2}
.vcard .vs{font-size:11.5px;color:#8A96A3;margin-top:3px}
.vcard .vr{margin-top:9px}
/* tabs */
.tabs{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:12px}
.tab{border:1px solid #D6DEE6;background:#fff;border-radius:16px;padding:4px 13px;
font-size:12px;color:#5A6672;cursor:pointer}
.tab.on{background:#3E6E9E;color:#fff;border-color:#3E6E9E;font-weight:700}
.chart{width:100%;height:420px}
.chart.sm{height:340px}
.twinrow{display:grid;grid-template-columns:1fr 1fr;gap:16px}
@media(max-width:1080px){.twinrow{grid-template-columns:1fr}}
.ok{color:#2E6B66;font-weight:700}
.no{color:#B5791F;font-weight:700}
.act{display:grid;grid-template-columns:52px 1fr 150px 190px;gap:10px;padding:9px 10px;
border-bottom:1px solid #EDF1F5;font-size:12.5px;align-items:start}
.act:last-child{border-bottom:none}
.p0{background:#F7EEDC;color:#8A6218;border-radius:5px;text-align:center;font-weight:700;font-size:11.5px;padding:2px 0}
.p1{background:#E4EDF5;color:#2F5B85;border-radius:5px;text-align:center;font-weight:700;font-size:11.5px;padding:2px 0}
.p2{background:#E7EBEF;color:#6B7785;border-radius:5px;text-align:center;font-weight:700;font-size:11.5px;padding:2px 0}
.who{font-weight:700;color:#3E6E9E}
.basis{font-size:11.5px;color:#8A96A3}
footer{text-align:center;color:#98A3AF;font-size:11.5px;padding:18px}
"""

JS = r"""
/* ==== 通用看板渲染器 ==== */
(function () {
  function mk(id) {
    var el = document.getElementById(id);
    var c = (window.echarts && echarts.getInstanceByDom(el)) || echarts.init(el);
    return c;
  }
  window.addEventListener('resize', function () {
    Object.keys(DATA.charts).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) { var c = echarts.getInstanceByDom(el); if (c) { c.resize(); } }
    });
  });

  // 静态图
  (DATA.staticCharts || []).forEach(function (id) {
    var el = document.getElementById(id);
    if (el) { mk(id).setOption(DATA.charts[id]); }
  });

  // 明细 tab
  var detailIds = DATA.detailCharts || [];
  function renderDetail(i) {
    var spec = detailIds[i];
    if (!spec) { return; }
    var el = document.getElementById('cItem');
    if (!el) { return; }
    var c = echarts.getInstanceByDom(el) || echarts.init(el);
    c.setOption(DATA.charts[spec.id], true);
  }
  var tabs = document.querySelectorAll('.tab');
  for (var i = 0; i < tabs.length; i++) {
    (function (t) {
      var key = parseInt(t.getAttribute('data-k'), 10);
      t.onclick = function () {
        for (var j = 0; j < tabs.length; j++) { tabs[j].className = 'tab'; }
        t.className = 'tab on';
        renderDetail(key);
      };
      if (t.className.indexOf('on') >= 0) { t.onclick(); }
    })(tabs[i]);
  }
})();
"""


def render_html(model, cfg):
    meta = model["meta"]
    cur = meta["currency"]
    vendors = model["vendors"]
    mods = model["modules"]
    hist = model.get("hist")
    used_rk = meta["usedRound"]
    round_label = dict((r["key"], r["label"]) for r in meta["rounds"])
    st = model["stats"]
    H = []

    # ---------------- header ----------------
    H.append('<div class="wrap"><header>')
    H.append("<h1>%s</h1>" % esc(meta["project"]))
    if meta["subtitle"]:
        H.append('<div class="sub">%s</div>' % esc(meta["subtitle"]))
    H.append('<div class="tags">')
    H.append('<span class="tag">%s</span>' % esc(meta["version"]))
    H.append('<span class="tag">面积 %s ㎡%s</span>' % (
        format(meta["area"], "g"), "（%s）" % esc(meta["areaNote"]) if meta["areaNote"] else ""))
    H.append('<span class="tag">%s</span>' % esc(meta["basis"] or "口径待确认"))
    H.append('<span class="tag">%d 家单位 · %d 个分项</span>' % (len(vendors), len(model["cats"])))
    H.append('<span class="tag">采用口径：%s</span>' % esc(round_label.get(used_rk, "")))
    H.append("</div></header>")

    # ---------------- 一、总览表 ----------------
    if mods.get("overview"):
        H.append('<div class="sec"><h2>一、各单位报价总览</h2>')
        H.append('<div class="desc">采用口径：%s；排名按采用价升序。无本轮报价的单位沿用上轮价参与排名并标注。</div>'
                 % esc(round_label.get(used_rk, "")))
        H.append('<div class="tblscroll">')
        H.append('<table><thead><tr><th>单位</th>')
        for rd in meta["rounds"]:
            H.append("<th>%s</th>" % esc(rd["label"]))
        H.append("<th>采用价</th><th>单方（%s/㎡）</th><th>较上轮</th><th>排名</th></tr></thead><tbody>"
                 % esc(cur))
        for v in vendors:
            H.append('<tr><td><span class="badge bn" style="background:%s;color:#fff">%s</span> %s</td>'
                     % (v["main"], esc(v["name"][:1]), esc(v["name"])))
            for rd in meta["rounds"]:
                d = v["data"].get(rd["key"])
                cell = money(d["used"], cur) if (d and d["used"] is not None) else "—"
                extra = ""
                if d and d.get("promo"):
                    extra = '<div class="basis">优惠 %s</div>' % money(d["promo"], cur)
                H.append('<td class="mono">%s%s</td>' % (cell, extra))
            used_cls = "best" if v.get("rank") == 1 else ""
            H.append('<td class="mono %s"><b>%s</b>%s</td>' % (
                used_cls, money(v["used"], cur),
                "" if v["used_actual"] else '<div class="basis">沿用上轮</div>'))
            H.append('<td class="mono">%s</td>' % money(v["sq"], cur))
            if v["delta"]:
                up = v["delta"]["abs"] > 0
                H.append('<td><span class="dchip %s">%s%.2f%%</span></td>'
                         % ("up" if up else "dn", "▲" if up else "▼", abs(v["delta"]["pct"])))
            else:
                H.append('<td class="basis">—</td>')
            if v["excluded"]:
                H.append('<td><span class="badge bw">不采用</span></td>')
            elif v["incomplete"]:
                H.append('<td><span class="badge bw">名义·不完整</span><div class="basis">有效可比第 %s</div></td>'
                         % (v["rank_eff"] if v["rank_eff"] else "—"))
            else:
                H.append('<td><span class="badge %s">第 %d</span></td>'
                         % ("b1" if v["rank"] == 1 else ("b2" if v["rank"] == 2 else "b3"),
                            v["rank"] or 0))
            H.append("</tr>")
        H.append("</tbody></table></div>")
        notes = model.get("notes") or {}
        if notes:
            H.append('<div class="note">')
            for k, val in notes.items():
                H.append("%s：%s<br>" % (esc(k), rich(val)))
            H.append("</div>")
        H.append("</div>")

    # ---------------- 二、报价概况 ----------------
    if mods.get("profile"):
        H.append('<div class="sec"><h2>二、各单位报价概况</h2>')
        H.append('<div class="desc">指标速览 + 报价标尺（0 起点同坐标）+ 卡片网格三种互补视角。</div>')
        # 2.1 指标带
        H.append('<div class="subttl">2.1 指标速览</div><div class="mstrip">')
        eff = [v for v in vendors if not v["incomplete"] and v["used"] is not None]
        best = sorted(eff, key=lambda x: x["used"])[0] if eff else None
        H.append('<div class="mitem"><div class="lbl">有效可比最低报价</div>'
                 '<div class="val">%s</div><div class="sub">%s · 单方 %s · 第 1</div></div>'
                 % (money(best["used"], cur) if best else "—",
                    esc(best["name"]) if best else "—",
                    money(best["sq"], cur) if best and best["sq"] else "—"))
        H.append('<div class="mitem m2"><div class="lbl">有效可比价差</div>'
                 '<div class="val">%s</div><div class="sub">区间 %s ~ %s</div></div>'
                 % (money(st["spread"], cur) if st["spread"] is not None else "—",
                    money(st["min"], cur), money(st["max"], cur)))
        H.append('<div class="mitem m3"><div class="lbl">各单位采用价均值</div>'
                 '<div class="val">%s</div><div class="sub">单方 %s</div></div>'
                 % (money(st["mean"], cur) if st["mean"] is not None else "—",
                    money(st["mean"] / meta["area"], cur) if st["mean"] else "—"))
        # ⬜ 历史格：仅在有历史数据时出现
        if hist:
            sqs = [s["sq"] for s in hist["stores"] if s["sq"] is not None]
            if sqs:
                H.append('<div class="mitem m4"><div class="lbl">历史门店单方均值</div>'
                         '<div class="val">%s/㎡</div>'
                         '<div class="sub">%d 家历史门店 · 仅单方可比，不折算总额</div></div>'
                         % (money(sum(sqs) / len(sqs), cur), len(sqs)))
        pend = [v for v in vendors if not v["used_actual"]]
        H.append('<div class="mitem m5"><div class="lbl">待跟进</div>'
                 '<div class="val">%d 项</div><div class="sub">%s</div></div>'
                 % (len(pend) + sum(1 for v in vendors if v["incomplete"]),
                    esc("；".join([v["name"] + " 待更新" for v in pend]) or "无")))
        H.append("</div>")

        # 2.2 报价标尺
        H.append('<div class="subttl">2.2 报价标尺（上轮 / 本轮 同坐标）</div>')
        H.append('<div class="pscale" id="s2Scale">')
        maxv = max([v["used"] or 0 for v in vendors] +
                   [(v["prev"]["used"] or 0) if v["prev"] else 0] + [1])
        for v in vendors:
            pv = v["prev"]["used"] if v["prev"] else None
            cv = v["used"]
            H.append('<div class="psrow"><div class="psname">%s</div><div>' % esc(v["name"]))
            if pv is not None:
                H.append('<div class="psfill" style="width:%.2f%%;background:%s"></div>'
                         % (pv / maxv * 100, v["light"]))
            if cv is not None:
                H.append('<div class="psfill" style="width:%.2f%%;background:%s"></div>'
                         % (cv / maxv * 100, v["main"] if v["used_actual"] else v["light"]))
            H.append("</div><div class='psval'>")
            if cv is not None:
                H.append("<span class='t'>%s</span>" % money(cv, cur))
                if v["delta"]:
                    up = v["delta"]["abs"] > 0
                    H.append(" <span class='dchip %s'>%s%.2f%%</span>"
                             % ("up" if up else "dn", "▲" if up else "▼", abs(v["delta"]["pct"])))
                elif not v["used_actual"]:
                    H.append(" <span class='dchip na'>沿用上轮</span>")
            H.append("</div></div>")
        H.append("</div>")
        H.append('<div class="pslegend">')
        H.append('<span><span class="lgsw" style="background:#B3C5DA"></span>上轮（浅色）</span>')
        H.append('<span><span class="lgsw" style="background:#3E6E9E"></span>本轮（深色）</span>')
        H.append('<span>标尺 0 起点同坐标，仅做各单位之间相对量级比较</span>')
        H.append("</div>")
        # 无历史数据时，note 不提"历史"二字，避免与"不体现历史对比"自相矛盾
        if hist:
            H.append('<div class="note" id="s2note">标尺不做历史金额折算对照：历史门店与本项目城市、面积、'
                     '范围均不同，总额均值不具备可比性。横向可比口径见第四节（各分项单方）。</div>')
        else:
            H.append('<div class="note" id="s2note">本次未提供历史门店数据，看板不体现历史对比。'
                     '标尺 0 起点同坐标，仅用于各单位之间的相对量级比较；横向可比口径见第四节（各分项单方）。</div>')

        # 2.3 卡片网格
        H.append('<div class="subttl">2.3 各单位卡片（顶部色条为相对价位）</div>')
        gmax = max([v["used"] or 0 for v in vendors] + [1])
        H.append('<div class="vgrid" id="vgridUsed">')
        for v in vendors:
            H.append('<div class="vcard"><div class="vbarwr"><div class="vbar" '
                     'style="width:%.2f%%;background:%s"></div></div>'
                     % ((v["used"] or 0) / gmax * 100, v["main"]))
            H.append('<div class="vn" style="color:%s">%s</div>' % (v["main"], esc(v["name"])))
            H.append('<div class="vp mono">%s</div>' % money(v["used"], cur))
            H.append('<div class="vs">单方 %s · 共 %d 条</div>'
                     % (money(v["sq"], cur), v["item_count"] or 0))
            H.append('<div class="vr">')
            if v["excluded"]:
                H.append('<span class="badge bw">不采用</span>')
            elif v["incomplete"]:
                H.append('<span class="badge bw">名义·不完整</span>')
            else:
                H.append('<span class="badge %s">第 %d</span>'
                         % ("b1" if v["rank"] == 1 else "b3", v["rank"] or 0))
            if not v["used_actual"]:
                H.append(' <span class="badge bn">沿用上轮</span>')
            H.append("</div></div>")
        H.append("</div>")

        # 2.4 剔除外立面
        if meta["facadeIdx"] is not None:
            H.append('<div class="subttl">2.4 剔除%s后对比</div>' % esc(meta["facadeCn"]))
            nfmax = max([v["nofac"] or 0 for v in vendors] + [1])
            H.append('<div class="vgrid" id="vgridNoFac">')
            for v in vendors:
                H.append('<div class="vcard"><div class="vbarwr"><div class="vbar" '
                         'style="width:%.2f%%;background:%s"></div></div>'
                         % ((v["nofac"] or 0) / nfmax * 100, v["main"]))
                H.append('<div class="vn" style="color:%s">%s</div>' % (v["main"], esc(v["name"])))
                H.append('<div class="vp mono">%s</div>' % money(v["nofac"], cur))
                H.append('<div class="vs">单方 %s</div>'
                         % money(v["nofac"] / meta["area"] if v["nofac"] else None, cur))
                H.append("</div>")
            H.append("</div>")
        H.append("</div>")

    # ---------------- 三、柱状图 ----------------
    if mods.get("totals"):
        H.append('<div class="sec"><h2>三、%s</h2>'
                 % ("总价 / 单方 / 剔除后对比" if meta["facadeIdx"] is not None
                    else "总价 / 单方对比（本项目无剔除项）"))
        H.append('<div class="desc">同色系：浅色=上轮，深色=本轮。</div>')
        H.append('<div class="twinrow"><div id="cTotal" class="chart"></div>'
                 '<div id="cSq" class="chart"></div></div>')
        if meta["facadeIdx"] is not None and "cNoFac" in model["charts"]:
            H.append('<div id="cNoFac" class="chart" style="margin-top:14px"></div>')
        H.append("</div>")

    # ---------------- 四、分部分项 ----------------
    if mods.get("category"):
        H.append('<div class="sec"><h2>四、分部分项报价横向对比</h2>')
        H.append('<div class="desc">各轮 × 金额/单方。%s%s</div>'
                 % ("叠加历史门店分项均值线。" if (hist and any(
                        x is not None for x in (hist.get("catMeans") or []))) else "",
                    ("<b>%s</b> 未提供分项拆分（整包价），不进本图，"
                     "其柱缺失仅代表未拆分、不代表该项为 0；比较请以总价/单方为准。"
                     % "、".join(model.get("noBreakdown") or []))
                    if model.get("noBreakdown") else ""))
        for rd in meta["rounds"]:
            H.append('<div class="subttl">%s</div><div class="twinrow">' % esc(rd["label"]))
            for cid in ("cCat%s" % rd["key"].upper(), "cCat%sUnit" % rd["key"].upper()):
                if cid in model["charts"]:
                    H.append('<div id="%s" class="chart"></div>' % cid)
            H.append("</div>")
        H.append("</div>")

    # ---------------- 五、明细 ----------------
    if mods.get("detail"):
        matrix = model.get("_matrix") or []
        if any(m["rows"] for m in matrix):
            H.append('<div class="sec"><h2>五、分项明细逐条对比</h2>')
            H.append('<div class="desc">按分项切换；描述级匹配（首行归一化后出现顺序配对）。</div>')
            H.append('<div class="tabs" id="catTabs">')
            for i, m in enumerate(matrix):
                if m["rows"]:
                    H.append('<span class="tab%s" data-k="%d">%s</span>'
                             % (" on" if i == 0 else "", i, esc(m["cn"])))
            H.append("</div>")
            H.append('<div id="cItem" class="chart" style="height:620px"></div>')
            H.append("</div>")

    # ---------------- 六、异常核查 ----------------
    if mods.get("anomaly"):
        anom = [v for v in vendors if v["zero_count"] > 0]
        if anom:
            H.append('<div class="sec"><h2>六、异常报价专项核查</h2>')
            H.append('<div class="desc">零单价/缺项条目逐条重算（不采信任何汇总字段），已剔除小计行。</div>')
            H.append('<div class="mstrip">')
            for v in anom:
                d = v["data"].get(used_rk) or v["prev"] or {}
                H.append('<div class="mitem m5"><div class="lbl">%s</div>'
                         '<div class="val">%d 条</div>'
                         '<div class="sub">零单价 / 共 %d 条 · 占比 %.1f%%</div></div>'
                         % (esc(v["name"]), v["zero_count"], v["item_count"],
                            v["zero_count"] / v["item_count"] * 100 if v["item_count"] else 0))
            H.append("</div>")
            if "cAnomCat" in model["charts"]:
                H.append('<div class="twinrow"><div id="cAnomCat" class="chart sm"></div>')
                if "cAnomPie" in model["charts"]:
                    H.append('<div id="cAnomPie" class="chart sm"></div>')
                H.append("</div>")
            H.append('<div class="note">判定规则：否定式（not included / excluding）→ 明确不含；'
                     '肯定式（included in ...）→ 已含·正常；词形 including/includes 为材料工艺描述，'
                     '非价格包含声明；三列均无标识 → 疑问项，需书面澄清。</div>')
            H.append("</div>")

    # ---------------- 七、历史对比（条件模块） ----------------
    if mods.get("history") and hist:
        H.append('<div class="sec"><h2>七、历史报价对比</h2>')
        H.append('<div class="desc">仅做<b>分项级</b>与<b>单方级</b>对比。'
                 '不同城市/面积的历史门店<b>总额</b>均值不可比，不做折算对照。</div>')
        has_hsub = any(("cHist%d" % vi) in model["charts"] for vi in range(len(vendors)))
        if has_hsub:
            H.append('<div class="subttl">7.1 各单位 vs 历史门店（分部分项）</div>')
            for vi, v in enumerate(vendors):
                cid = "cHist%d" % vi
                if cid in model["charts"]:
                    H.append('<div id="%s" class="chart"></div>' % cid)
        else:
            H.append('<div class="note">历史门店与本次报价单位均未提供可对齐的分项拆分，'
                     '7.1 分部分项对比不渲染；本节只做<b>单方造价</b>口径对比。</div>')
        H.append('<div class="subttl">7.2 全门店单方造价对比</div>')
        H.append('<div id="cHistSq" class="chart"></div>')
        H.append('<div class="note">深色柱＝本项目各单位，浅色柱＝历史门店；'
                 '<span style="color:%s;font-weight:700">橙色虚线</span>＝过往门店单方均值'
                 '（由各家 total ÷ area 自动计算，无现成单方值时才直取原文）。<br>'
                 '历史门店口径须与本项目一致（%s）；'
                 '口径不一致的已排除，不参与均值计算。</div>'
                 % (C_AMBER, esc(meta["basis"] or "口径待确认")))
        H.append("</div>")

    # ---------------- 八、勾稽 ----------------
    if mods.get("reconcile"):
        H.append('<div class="sec"><h2>八、勾稽校验</h2>')
        checks = model.get("_checks") or []
        H.append('<div class="desc">共 %d 项；合格 %d，差异 %d。</div>'
                 % (len(checks), sum(1 for c in checks if c["ok"] and not c.get("warn")),
                    sum(1 for c in checks if not c["ok"] or c.get("warn"))))
        H.append('<div class="tblscroll">')
        H.append('<table class="fixed"><colgroup><col style="width:30%"><col style="width:13%">'
                 '<col style="width:57%"></colgroup>'
                 '<thead><tr><th class="lft">校验项</th><th>结果</th><th class="lft">说明</th>'
                 '</tr></thead><tbody>')
        for c in checks:
            mark = '<span class="ok">✓ 通过</span>' if (c["ok"] and not c.get("warn")) else (
                '<span class="no">! 已注明</span>' if c.get("warn") else '<span class="no">✗ 差异</span>')
            H.append('<tr><td class="lft">%s</td><td>%s</td><td class="lft">%s</td></tr>'
                     % (esc(c["name"]), mark, rich(c["detail"])))
        H.append("</tbody></table></div></div>")

    # ---------------- 九、行动清单 ----------------
    if mods.get("actions"):
        acts = model.get("_actions") or []
        H.append('<div class="sec"><h2>九、行动清单</h2>')
        H.append('<div class="desc">按优先级排列，每条含依据。</div>')
        H.append('<div style="border:1px solid #E8EEF3;border-radius:10px;overflow:hidden">')
        H.append('<div class="act" style="background:#EEF3F7;font-weight:700">'
                 '<div>优先级</div><div>动作</div><div>对象</div><div>依据</div></div>')
        for a in acts:
            H.append('<div class="act"><div class="%s">%s</div><div>%s</div>'
                     '<div class="who">%s</div><div class="basis">%s</div></div>'
                     % (a["p"].lower(), a["p"], esc(a["text"]), esc(a["who"]), esc(a["basis"])))
        H.append("</div></div>")

    # ---------------- 附录 A、清单外增项（邮件补充报价） ----------------
    if mods.get("addenda") and model.get("addenda"):
        for ad in model["addenda"]:
            acur = ad.get("currency") or cur
            vname = ad.get("vendor", "")
            v = next((x for x in vendors if x["name"] == vname), None)
            sub = ad.get("subtotal_printed")
            H.append('<div class="sec"><h2>附录 A · 清单外增项必要性核查</h2>')
            H.append('<div class="desc"><b>%s</b> 另以邮件提交《%s》：该批工作<b>不在</b>其 BOQ 报价内，'
                     '属 MM（商场）要求但其未纳入清单的项目。以下逐项核查<b>必要性</b>'
                     '（是否法定强制）与<b>金额弹性</b>，并给出处理建议。</div>'
                     % (esc(vname), esc(ad.get("title", ""))))

            H.append('<div class="subttl">A.1 指标速览</div><div class="mstrip">')
            H.append('<div class="mitem"><div class="lbl">原文不含税小计</div>'
                     '<div class="val">%s</div><div class="sub">原文写定 SUBTOTAL</div></div>'
                     % money(sub, acur))
            H.append('<div class="mitem"><div class="lbl">I.V.A.</div>'
                     '<div class="val">%s</div><div class="sub">税率 %s%%</div></div>'
                     % (money(ad.get("vat"), acur),
                        round(float(ad.get("vat_rate") or 0) * 100, 1)))
            H.append('<div class="mitem"><div class="lbl">原文含税合计</div>'
                     '<div class="val">%s</div><div class="sub">TOTAL（含税，另计）</div></div>'
                     % money(ad.get("total"), acur))
            if v and v.get("used"):
                H.append('<div class="mitem"><div class="lbl">占其 BOQ 报价</div>'
                         '<div class="val">%.1f%%</div><div class="sub">不含税小计 ÷ %s</div></div>'
                         % (sub / v["used"] * 100, money(v["used"], acur)))
            H.append('<div class="mitem"><div class="lbl">法定强制项</div>'
                     '<div class="val">%d / %d</div>'
                     '<div class="sub">其余为行政代办性费用</div></div>'
                     % (sum(1 for i in ad.get("items", []) if "法定" in (i.get("mandatory") or "")),
                        len(ad.get("items", []))))
            H.append("</div>")

            H.append('<div class="subttl">A.2 逐项核查（原文金额，未做估算）</div>')
            H.append('<div class="tblscroll">')
            # table-layout:fixed + colgroup：长文本列受控换行，绝不撑破卡片
            H.append('<table class="fixed"><colgroup>'
                     '<col style="width:5%"><col style="width:22%"><col style="width:10%">'
                     '<col style="width:9%"><col style="width:28%"><col style="width:26%">'
                     '</colgroup><thead><tr><th>序号</th><th class="lft">项目（原文 / 中文）</th>'
                     '<th>原文金额</th><th>强制属性</th>'
                     '<th class="lft">法规依据</th>'
                     '<th class="lft">必要性判定 / 金额弹性</th>'
                     '</tr></thead><tbody>')
            for it in ad.get("items", []):
                dsc = rich(it.get("desc", ""))
                if it.get("sub"):
                    dsc += '<div class="basis">+ %s</div>' % rich(it["sub"])
                H.append('<tr><td class="mono">%s</td>'
                         '<td class="lft">%s<div class="basis">%s</div></td>'
                         '<td class="mono">%s</td>'
                         '<td><span class="badge bn">%s</span></td>'
                         '<td class="lft basis">%s</td>'
                         '<td class="lft">%s<div class="basis">金额弹性：%s</div></td></tr>'
                         % (esc(it.get("no")), dsc, rich(it.get("desc_cn", "")),
                            money(it.get("amount"), acur), esc(it.get("mandatory", "")),
                            rich(it.get("basis", "")), rich(it.get("verdict", "")),
                            esc(it.get("flex", ""))))
            H.append('<tr><td colspan="2" class="lft"><b>原文 SUBTOTAL</b></td>'
                     '<td class="mono"><b>%s</b></td><td colspan="3" class="lft">'
                     '<span class="basis">逐项单价相加为 %s，与原文小计差 %s</span></td></tr>'
                     % (money(sub, acur), money(ad.get("sum_unit_col"), acur),
                        money(round((sub or 0) - (ad.get("sum_unit_col") or 0), 2), acur)))
            H.append("</tbody></table></div>")

            if ad.get("reconcile_note"):
                H.append('<div class="note"><b>金额勾稽说明：</b>%s</div>' % rich(ad["reconcile_note"]))
            H.append('<div class="subttl">A.3 结论与处理建议</div>')
            H.append('<div class="note"><b>必要性：</b>%s<br><br><b>对报价的影响：</b>%s</div>'
                     % (rich(ad.get("conclusion", "")), rich(ad.get("impact", ""))))
            H.append('<div class="note basis">数据来源：%s</div>' % rich(ad.get("source", "")))
            H.append("</div>")

    H.append('<footer>%s · 数据均取自报价原文，未做估算或补全</footer></div>' % esc(meta["project"]))
    return "".join(H)


# --------------------------------------------------------------------------
# 明细图表（每个 tab 一张）
# --------------------------------------------------------------------------
def build_detail_charts(model):
    matrix = model.get("_matrix") or []
    detail = []
    for i, m in enumerate(matrix):
        if not m["rows"]:
            continue
        cid = "cItem%d" % i
        descs = [dsc(r["desc"], 46) for r in m["rows"]]
        o = {"title": {"text": "%s · 逐条对比" % m["cn"], "left": 8, "top": 6,
                       "textStyle": {"fontSize": 13, "fontWeight": 700, "color": "#2C3742"}},
             "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
             "legend": {"top": 6, "right": 8, "textStyle": {"fontSize": 10, "color": "#5A6672"}},
             "grid": {"left": 8, "right": 30, "top": 46, "bottom": 30, "containLabel": True},
             "xAxis": {"type": "value",
                       "axisLabel": {"color": "#5A6672", "fontSize": 10},
                       "splitLine": {"lineStyle": {"color": "#EEF2F6"}}},
             "yAxis": {"type": "category", "data": descs, "inverse": True,
                       "axisLabel": {"color": "#5A6672", "fontSize": 10}},
             "series": []}
        series = []
        for v in model["vendors"]:
            vals = [r["vals"].get(v["name"]) for r in m["rows"]]
            if any(x is not None for x in vals):
                series.append({"name": v["name"], "type": "bar", "barMaxWidth": 11,
                               "itemStyle": {"color": v["main"]}, "data": vals})
        o["series"] = series
        model["charts"][cid] = o
        detail.append({"id": cid, "idx": i})
    model["detailCharts"] = detail
    return model


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--score-panel", default=None,
                    help="可选：gen_score_panel.py 产出的评分片段 HTML，装配进看板")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    cfg = load_json(a.config)
    base = Path(a.config).resolve().parent
    quotes = load_json(base / cfg["quotes"])
    hist = None
    if cfg.get("history"):
        hist = load_json(base / cfg["history"])

    model = build_model(cfg, quotes, hist)
    mods = module_gate(cfg, model)
    model["_matrix"] = build_item_matrix(model) if mods.get("detail") else []
    model["_checks"] = build_checks(model)
    model["_actions"] = build_actions(model)
    build_charts(model)
    build_detail_charts(model)

    body = render_html(model, cfg)
    echarts = ECHARTS_PATH.read_text(encoding="utf-8")

    # ── 可选评分节：由 gen_score_panel.py 产出片段，经 --score-panel 传入 ──────
    # ⚠️ 必须在这里装配，不要事后去 HTML 里找 "<style>"/"</body>" 字符串注入：
    #    内联的压缩版 ECharts 源码里含有 "<style>"、</body>" 一类字面量，
    #    事后注入极易把 DOM 塞进 JS 字符串 → 页面看不到，且不报任何错。
    panel_dom, panel_css, panel_js = "", "", ""
    if a.score_panel:
        sp = Path(a.score_panel)
        if not sp.is_absolute():
            sp = base / sp
        _raw = sp.read_text(encoding="utf-8")
        panel_css = "".join(re.findall(r"<style[^>]*>.*?</style>", _raw, re.S))
        panel_js = "".join(re.findall(r"<script[^>]*>.*?</script>", _raw, re.S))
        panel_dom = _raw
        for _blk in (panel_css, panel_js):
            panel_dom = panel_dom.replace(_blk, "")
        panel_dom = panel_dom.strip()
        assert "scorePanel" in panel_dom or "scoreRulesBox" in panel_dom, (
            "--score-panel 片段里找不到评分面板 DOM（期望含 id=scorePanel/scoreRulesBox）：%s" % sp)

    data_js = "var DATA=" + json.dumps(
        {k: model[k] for k in ("meta", "cats", "vendors", "stats", "catMeans",
                               "hist", "charts", "staticCharts", "detailCharts",
                               "modules")}, ensure_ascii=False) + ";"

    html = (
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>%s</title><style>%s</style>%s</head><body>%s"
        "<script>%s</script><script>%s</script><script>%s</script>%s"
        "</body></html>"
        % (esc(model["meta"]["project"]), CSS, panel_css, body, echarts, data_js, JS,
           panel_dom + panel_js)
    )

    out = Path(a.out or cfg.get("out") or "报价分析看板.html")
    if not out.is_absolute():
        out = base / out          # 与 quotes/history 同口径：相对路径按 config 所在目录解析
    # newline="\n"：禁用 Windows 文本模式的 \n -> \r\n 转换，
    # 否则落盘字节数会比下面打印的多（每个换行 +1 字节），容易被误读成"文件不是这次生成的"
    out.write_text(html, encoding="utf-8", newline="\n")
    print("OK -> %s (%s bytes)" % (out, format(len(html.encode('utf-8')), ",")))
    print("模块: " + ", ".join("%s=%s" % (k, "ON" if v else "off") for k, v in sorted(mods.items())))
    for w in model.get("moduleLog") or []:
        print("  ⚠ " + w)
    if a.report:
        print("图表: " + ", ".join(model["staticCharts"]))
        print("明细 tab: %d 个" % len(model.get("detailCharts") or []))
        print("勾稽: %d 项" % len(model["_checks"]))
        print("行动: %d 条" % len(model["_actions"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
