#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Engineering & Strategic Pricing Engine (Pro v3.0.0)
=========================================================
将结构化的菜品运营数据转换为一份符合财报标准的《菜单盈利能力诊断报告》所需的所有数字。

输入（二选一）：
  A. JSON（Pro 规范）：含 period / store_info / dishes[]，详见 README 与 SKILL.md
  B. 遗留 CSV（菜名,食材成本,售价,近30天销量）—— 自动降级兼容

核心计算（全部精确到小数点后两位）：
  - CM        = Price - (raw_cost + seasoning_cost + labor_apportionment)
  - CM Mix%   = 单品总贡献毛利 / 总贡献毛利
  - Sales Mix%= 单品销售额 / 总销售额
  - PTR       = (raw_cost + labor_apportionment) / Price        # 首要成本率（不含调料）
  - 净销量     = sales_volume * (1 - return_rate)
  - BCG 分类  ：X 轴=平均 Sales Mix%(=1/N) 判受欢迎度；Y 轴=平均 CM(单位贡献毛利) 判盈利性
  - 价格弹性  ：针对 Puzzles，模拟 +5%/+10%/+15%，行业弹性系数 -1.2，计算盈亏平衡销量容忍度
  - 帕累托    ：Top 20% 菜品贡献的毛利占比 / 80% 利润集中度 / 长尾无效菜品
  - 菜单效率分：0-100 综合评分

专业定价扩展（v3 新增，可选输入）：
  - 全成本核算：store_info.operating_cost（租金/水电/人工总摊/折旧/营销/管理）按月分摊到每道菜，
    得到「完全成本 / 单份净利 / 净利率」（区分变动成本与固定运营成本）。
  - 市场定位  ：按售价分位将菜品分为引流款/主力款/利润款/形象款，并判定门店整体价格定位。
  - 竞品参考  ：每道菜可填 competitors / market_avg_price，计算价格指数、价差与市场定位诊断。
  - 利润率设定：target.gross_margin / target.net_margin 给定目标，反推「达成目标利润率所需售价」。

异常拦截：成本(合计) ≥ 售价 时立即终止并报错，绝不编造、绝不在异常数据上出报告。
用法：
  python menu_engineering.py --json-input menu.json
  python menu_engineering.py --input menu.csv --json out.json
  cat menu.json | python menu_engineering.py
"""

import sys
import io
import os
import re
import json
import math
import argparse

# 强制 UTF-8，避免 Windows 控制台乱码（幂等：已为 utf-8 则跳过，防止重复包装导致 buffer 关闭）
if getattr(sys.stdout, "encoding", None) != "utf-8":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    except Exception:
        pass

CATEGORY_CN = {
    "star": "明星 Star",
    "puzzle": "问题 Puzzle",
    "cash_cow": "金牛 Cow",
    "dog": "瘦狗 Dog",
}

# 行业基准（仅供诊断提示，不参与计算）
BENCH_GM_LOW = 0.60
BENCH_GM_HIGH = 0.65
BENCH_STAR_SHARE_LOW = 0.20
BENCH_STAR_SHARE_HIGH = 0.30
BENCH_DOG_SHARE_WARN = 0.20
BENCH_PTR_TARGET = 0.35          # Puzzles 成本重构目标：PTR < 35%（通用默认值）
ELASTICITY = -1.2                # 行业平均价格弹性系数（通用默认值）

# 业态专属基准线（反映行业特征与运营差异）
FORMAT_PRESETS = {
    "快餐": {
        "label": "快餐 / 快休闲 (QSR)",
        "gm_low": 0.60, "gm_high": 0.65,
        "ptr_target": 0.38, "elasticity": -1.2,
        "rationale": "高周转、低客单价、食材+包材成本占比高，单品绝对毛利薄，靠翻台走量获利；"
                     "价格敏感但有便利性与品牌黏性，需求弹性居中偏高。",
    },
    "正餐": {
        "label": "正餐 / 商务餐饮",
        "gm_low": 0.65, "gm_high": 0.72,
        "ptr_target": 0.32, "elasticity": -0.8,
        "rationale": "客单价与体验属性强，食材+人工摊销占比相对可控，毛利率较高；"
                     "消费决策受场景/社交驱动，价格敏感度低，需求弹性较小。",
    },
    "茶饮": {
        "label": "茶饮 / 现制饮品",
        "gm_low": 0.68, "gm_high": 0.78,
        "ptr_target": 0.28, "elasticity": -1.6,
        "rationale": "原料（茶基底+小料）成本极低、毛利极高；赛道同质化与促销内卷严重，"
                     "消费者对单价高度敏感，需求价格弹性大。",
    },
}


def get_bench(format_name):
    """按业态返回基准线；未指定或未知业态回退到通用默认。"""
    if format_name in FORMAT_PRESETS:
        p = FORMAT_PRESETS[format_name]
        return {
            "format": format_name, "label": p["label"],
            "gm_low": p["gm_low"], "gm_high": p["gm_high"],
            "ptr_target": p["ptr_target"], "elasticity": p["elasticity"],
            "rationale": p["rationale"],
        }
    return {
        "format": format_name or "通用", "label": "通用 / 未指定业态",
        "gm_low": BENCH_GM_LOW, "gm_high": BENCH_GM_HIGH,
        "ptr_target": BENCH_PTR_TARGET, "elasticity": ELASTICITY,
        "rationale": "未指定业态，采用行业通用默认基准；指定业态后基准线将自动微调。",
    }


# 专业定价扩展默认值
TARGET_NET_MARGIN = 0.15          # 目标净利率（餐饮通用合理值，可在 JSON target.net_margin 覆盖）
OPERATING_COMPONENTS = ["rent", "utilities", "labor_overhead", "depreciation", "marketing", "management"]
OPERATING_LABELS = {
    "rent": "租金", "utilities": "水电燃料", "labor_overhead": "人工总摊（前厅后厨薪资）",
    "depreciation": "折旧摊销", "marketing": "营销推广", "management": "管理杂费",
}
# 菜单价格定位分层（按售价分位）
POSITION_TIERS = {
    "value": "引流款", "core": "主力款", "profit": "利润款", "image": "形象款",
}


def _extract_operating(obj):
    """从 JSON 提取门店运营成本（月）。返回 (total, breakdown_dict)。"""
    if not isinstance(obj, dict):
        return 0.0, {}
    src = obj.get("operating_cost")
    if src is None:
        si = obj.get("store_info") or {}
        src = si.get("operating_cost")
    if src is None:
        return 0.0, {}
    if isinstance(src, (int, float)):
        return float(src), {"total": float(src)}
    if isinstance(src, dict):
        bd = {}
        for k in OPERATING_COMPONENTS:
            if k in src and src[k] not in (None, ""):
                try:
                    bd[k] = float(src[k])
                except Exception:
                    pass
        total = sum(bd.values())
        if total <= 0 and "total" in src:
            try:
                total = float(src["total"])
            except Exception:
                total = 0.0
        return total, bd
    return 0.0, {}


def _extract_target(obj):
    """从 JSON 提取目标利润率。返回 {'gross_margin': x, 'net_margin': y}。"""
    if not isinstance(obj, dict):
        return {}
    t = obj.get("target") or {}
    if not isinstance(t, dict):
        return {}
    out = {}
    for k in ("gross_margin", "net_margin"):
        if k in t and t[k] not in (None, ""):
            try:
                out[k] = float(t[k])
            except Exception:
                pass
    return out


# ---------------------------------------------------------------------------
# 解析：JSON（Pro）
# ---------------------------------------------------------------------------
def parse_json(text):
    """返回 (dishes, meta, anomalies)。"""
    try:
        obj = json.loads(text)
    except Exception as e:
        return [], {}, [f"JSON 解析失败：{e}。请检查括号/引号是否完整。"]

    dishes_raw = obj.get("dishes") if isinstance(obj, dict) else obj
    if not isinstance(dishes_raw, list) or not dishes_raw:
        return [], {}, ["dishes 字段缺失或为空，请提供至少一道菜的数组。"]

    meta = {
        "period": (obj.get("period") if isinstance(obj, dict) else None) or "未指定",
        "store_info": (obj.get("store_info") if isinstance(obj, dict) else None) or {},
        "format": None,
        "operating_cost": _extract_operating(obj) if isinstance(obj, dict) else (0.0, {}),
        "operating_alloc": (
            ((obj.get("store_info") or {}).get("operating_alloc") or obj.get("operating_alloc") or "volume")
            if isinstance(obj, dict) else "volume"
        ),
        "target": _extract_target(obj) if isinstance(obj, dict) else {},
    }
    if isinstance(obj, dict):
        fmt = obj.get("format") or (obj.get("store_info") or {}).get("format")
        if isinstance(fmt, str) and fmt.strip():
            meta["format"] = fmt.strip()

    dishes, anomalies = [], []
    for i, d in enumerate(dishes_raw):
        name = d.get("name") or f"菜品{i+1}"
        raw = d.get("raw_cost")
        seasoning = d.get("seasoning_cost", 0) or 0
        labor = d.get("labor_apportionment", 0) or 0
        price = d.get("price")
        vol = d.get("sales_volume")
        ret = d.get("return_rate", 0) or 0
        is_sig = bool(d.get("is_signature", False))
        cat = d.get("category", "")

        # 校验
        if raw is None or price is None or vol is None:
            anomalies.append(f"「{name}」缺少必填字段（raw_cost / price / sales_volume），请补全。")
            continue
        try:
            raw = float(raw); seasoning = float(seasoning); labor = float(labor)
            price = float(price); vol = float(vol); ret = float(ret)
        except Exception:
            anomalies.append(f"「{name}」存在非数字字段，请检查 raw_cost/price/sales_volume/return_rate。")
            continue
        if price <= 0:
            anomalies.append(f"「{name}」售价须为正数（price={price}）。")
            continue
        if vol < 0:
            anomalies.append(f"「{name}」销量不能为负（sales_volume={vol}）。")
            continue
        if not (0 <= ret < 1):
            anomalies.append(f"「{name}」return_rate 须在 [0,1) 区间（当前 {ret}）。")
            continue
        total_cost = raw + seasoning + labor
        if total_cost >= price:
            anomalies.append(
                f"「{name}」合计成本({total_cost:.2f}) ≥ 售价({price:.2f})，"
                f"毛利为零或为负，请修正成本或售价后再分析。"
            )
            continue

        dishes.append({
            "name": name,
            "category": cat,
            "raw_cost": round(raw, 2),
            "seasoning_cost": round(seasoning, 2),
            "labor_apportionment": round(labor, 2),
            "price": round(price, 2),
            "sales_volume": int(round(vol)),
            "return_rate": round(ret, 4),
            "is_signature": is_sig,
            "net_volume": int(round(vol * (1 - ret))),
            # 专业定价扩展字段（可选，缺失为 None）
            "operating_cost_override": d.get("operating_cost"),
            "competitor_price": d.get("competitor_price"),
            "market_avg_price": d.get("market_avg_price"),
            "competitors": d.get("competitors") if isinstance(d.get("competitors"), list) else None,
        })

    if not dishes:
        anomalies.append("没有可用的合法菜品数据，请检查后重新提交。")
    return dishes, meta, anomalies


# ---------------------------------------------------------------------------
# 解析：遗留 CSV（菜名,食材成本,售价,近30天销量）
# ---------------------------------------------------------------------------
def _clean_num(s):
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None
    s = re.sub(r"[^0-9.\-]", "", s)
    if s in ("", "-", ".", "-."):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _split_row(line):
    return [c.strip() for c in re.split(r"[,;\t，、；]+", line) if c.strip() != ""]


def _looks_like_header(cells):
    kw = ["菜名", "菜品", "名称", "name", "成本", "cost", "食材", "售价", "定价",
          "price", "销量", "sales", "volume", "份", "近30", "30天"]
    low = [c.lower() for c in cells]
    return any(any(k in c for k in kw) for c in low)


def parse_csv(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() != ""]
    if not lines:
        return [], {}, ["未检测到任何菜品数据。"]
    header_map = None
    start = 0
    if _looks_like_header(_split_row(lines[0])):
        cells = [c.lower() for c in _split_row(lines[0])]
        idx = {"name": 0, "cost": 1, "price": 2, "volume": 3}
        for i, c in enumerate(cells):
            if any(k in c for k in ["菜名", "菜品", "名称", "name"]):
                idx["name"] = i
            if any(k in c for k in ["成本", "cost", "食材"]):
                idx["cost"] = i
            if any(k in c for k in ["售价", "定价", "price"]):
                idx["price"] = i
            if any(k in c for k in ["销量", "sales", "volume", "份", "30天", "30"]):
                idx["volume"] = i
        header_map = idx
        start = 1

    dishes, anomalies = [], []
    for ln in lines[start:]:
        cells = _split_row(ln)
        if not cells:
            continue
        if header_map is not None:
            name = cells[header_map["name"]] if header_map["name"] < len(cells) else f"菜品{len(dishes)+1}"
            cost = _clean_num(cells[header_map["cost"]]) if header_map["cost"] < len(cells) else None
            price = _clean_num(cells[header_map["price"]]) if header_map["price"] < len(cells) else None
            volume = _clean_num(cells[header_map["volume"]]) if header_map["volume"] < len(cells) else None
        else:
            if len(cells) < 4:
                anomalies.append(f"数据行字段不足（需 4 列）：「{ln}」")
                continue
            name, cost, price, volume = cells[0], _clean_num(cells[1]), _clean_num(cells[2]), _clean_num(cells[3])

        if cost is None or price is None or volume is None:
            anomalies.append(f"「{name}」存在无法识别的数字，请检查格式。")
            continue
        if cost <= 0 or price <= 0:
            anomalies.append(f"「{name}」成本或售价须为正数。")
            continue
        if volume < 0:
            anomalies.append(f"「{name}」销量不能为负。")
            continue
        if cost >= price:
            anomalies.append(f"「{name}」成本({cost}) ≥ 售价({price})，请修正后再分析。")
            continue
        dishes.append({
            "name": name, "category": "", "raw_cost": round(cost, 2),
            "seasoning_cost": 0.0, "labor_apportionment": 0.0,
            "price": round(price, 2), "sales_volume": int(round(volume)),
            "return_rate": 0.0, "is_signature": False, "net_volume": int(round(volume)),
        })

    if not dishes:
        anomalies.append("没有可用的合法菜品数据，请检查后重新提交。")
    return dishes, {}, anomalies


# ---------------------------------------------------------------------------
# 计算与 BCG 分类
# ---------------------------------------------------------------------------
def analyze(dishes, meta, bench):
    n = len(dishes)
    total_revenue = 0.0
    total_cm = 0.0

    for d in dishes:
        total_cost = d["raw_cost"] + d["seasoning_cost"] + d["labor_apportionment"]
        cm = d["price"] - total_cost
        revenue = d["price"] * d["net_volume"]
        total_cm_dish = cm * d["net_volume"]
        d["total_cost"] = round(total_cost, 2)
        d["cm"] = round(cm, 2)
        d["cm_pct"] = round(cm / d["price"], 4)                 # 毛利率
        d["ptr"] = round((d["raw_cost"] + d["labor_apportionment"]) / d["price"], 4)
        d["revenue"] = round(revenue, 2)
        d["total_cm"] = round(total_cm_dish, 2)
        total_revenue += revenue
        total_cm += total_cm_dish

    # ---- 专业定价扩展（一）：运营成本分摊 + 单份净利/净利率 ----
    op_total, op_breakdown = meta.get("operating_cost") or (0.0, {})
    op_alloc = meta.get("operating_alloc") or "volume"
    has_op = op_total and op_total > 0
    total_net_volume = sum(d["net_volume"] for d in dishes)
    op_for_dish = {}                      # 每道菜分摊到的「总」运营成本（非单份）
    if has_op and total_net_volume > 0:
        if op_alloc == "revenue" and total_revenue > 0:
            for d in dishes:
                op_for_dish[d["name"]] = op_total * (d["revenue"] / total_revenue)
        else:                             # 默认按销量分摊（更贴合固定开销随客流消化）
            for d in dishes:
                op_for_dish[d["name"]] = op_total * (d["net_volume"] / total_net_volume)
    for d in dishes:
        ov = d.get("operating_cost_override")
        try:
            ov = float(ov) if ov not in (None, "") else None
        except Exception:
            ov = None
        dish_op_total = ov if ov is not None else op_for_dish.get(d["name"], 0.0)
        op_per_unit = (dish_op_total / d["net_volume"]) if d["net_volume"] else 0.0
        d["operating_apportionment"] = round(op_per_unit, 2)     # 单份运营成本
        d["full_cost"] = round(d["total_cost"] + d["operating_apportionment"], 2)   # 完全成本
        d["net_profit"] = round(d["cm"] - d["operating_apportionment"], 2)          # 单份净利
        d["net_margin"] = round(d["net_profit"] / d["price"], 4) if d["price"] else 0.0
    overall_net_profit = sum(d["net_profit"] * d["net_volume"] for d in dishes)
    overall_net_margin = (overall_net_profit / total_revenue) if total_revenue else 0.0

    # 阈值
    avg_sales_mix = 1.0 / n                                      # 平均 Sales Mix% = 1/N
    avg_cm = sum(d["cm"] for d in dishes) / n                    # 平均单位 CM

    for d in dishes:
        d["sales_mix"] = round(d["revenue"] / total_revenue, 4) if total_revenue else 0.0
        d["cm_mix"] = round(d["total_cm"] / total_cm, 4) if total_cm else 0.0
        popular = d["sales_mix"] > avg_sales_mix
        profitable = d["cm"] > avg_cm
        d["is_popular"] = popular
        d["is_profitable"] = profitable
        if popular and profitable:
            d["category_key"] = "star"
        elif (not popular) and profitable:
            d["category_key"] = "cash_cow"
        elif popular and (not profitable):
            d["category_key"] = "puzzle"
        else:
            d["category_key"] = "dog"
        d["category_cn"] = CATEGORY_CN[d["category_key"]]

        # Puzzles：价格弹性与盈亏平衡分析
        if d["category_key"] == "puzzle":
            d["elasticity"] = bench["elasticity"]
            scn = []
            for dp in (0.05, 0.10, 0.15):
                new_price = d["price"] * (1 + dp)
                new_cm = new_price - d["total_cost"]
                pred_drop = -bench["elasticity"] * dp        # 预测销量降幅（比例）
                pred_vol = d["net_volume"] * (1 - pred_drop)
                new_total_cm = new_cm * pred_vol
                delta_cm = new_total_cm - d["total_cm"]
                # 盈亏平衡：提价后维持总 CM 不变的最大销量降幅
                break_even_drop = max(0.0, 1 - (d["cm"] / new_cm)) if new_cm > 0 else 0.0
                scn.append({
                    "increase_pct": round(dp * 100, 2),
                    "new_price": round(new_price, 2),
                    "new_cm": round(new_cm, 2),
                    "pred_volume_drop_pct": round(pred_drop * 100, 2),
                    "pred_volume": round(pred_vol, 1),
                    "new_total_cm": round(new_total_cm, 2),
                    "delta_cm": round(delta_cm, 2),
                    "break_even_drop_pct": round(break_even_drop * 100, 2),
                    "break_even_volume": round(d["net_volume"] * (1 - break_even_drop), 1),
                    "within_tolerance": pred_drop <= break_even_drop + 1e-9,
                })
            d["scenarios"] = scn
            # 推荐动作：在满足盈亏平衡容忍度的前提下，选取提价幅度最大者；
            # 若 +5%/+10%/+15% 均超出容忍度，则不建议提价，转成本重构。
            viable = [s for s in scn if s["within_tolerance"]]
            if viable:
                best = max(viable, key=lambda s: s["increase_pct"])
                d["recommend"] = {
                    "action": f"Price +{best['increase_pct']:.0f}%",
                    "new_price": best["new_price"],
                    "pred_volume_drop_pct": best["pred_volume_drop_pct"],
                    "delta_cm": best["delta_cm"],
                    "break_even_drop_pct": best["break_even_drop_pct"],
                    "within_tolerance": True,
                    "price_viable": True,
                }
            else:
                d["recommend"] = {
                    "action": "Cost Re-engineering（提价不可行）",
                    "new_price": d["price"],
                    "pred_volume_drop_pct": None,
                    "delta_cm": 0.0,
                    "break_even_drop_pct": scn[0]["break_even_drop_pct"],
                    "within_tolerance": False,
                    "price_viable": False,
                }

    # ---- 专业定价扩展（二）：市场定位分层 ----
    prices_sorted = sorted(d["price"] for d in dishes)

    def _pct(arr, q):
        if not arr:
            return 0.0
        if len(arr) == 1:
            return float(arr[0])
        k = (len(arr) - 1) * q
        f = math.floor(k); c = math.ceil(k)
        if f == c:
            return float(arr[int(k)])
        return arr[f] * (c - k) + arr[c] * (k - f)

    p25 = _pct(prices_sorted, 0.25)
    p75 = _pct(prices_sorted, 0.75)
    p90 = _pct(prices_sorted, 0.90)
    for d in dishes:
        p = d["price"]
        if p <= p25:
            tier = "value"
        elif p <= p75:
            tier = "core"
        elif p <= p90:
            tier = "profit"
        else:
            tier = "image"
        d["price_tier"] = tier
        d["price_tier_cn"] = POSITION_TIERS[tier]
    avg_price_cover = (total_revenue / total_net_volume) if total_net_volume else 0.0
    if avg_price_cover <= 30:
        store_pos = "大众性价比型"
    elif avg_price_cover <= 80:
        store_pos = "中端品质型"
    else:
        store_pos = "高端精品型"

    # ---- 专业定价扩展（三）：竞品价格参考 +（四）利润率目标定价 ----
    target_gm = meta.get("target", {}).get("gross_margin") or bench["gm_high"]
    target_nm = meta.get("target", {}).get("net_margin") or TARGET_NET_MARGIN
    for d in dishes:
        vc = d["total_cost"]
        # 竞品均价
        mkt = None
        comps = d.get("competitors")
        if isinstance(comps, list) and comps:
            vals = []
            for c in comps:
                if isinstance(c, dict) and c.get("price") is not None:
                    try:
                        vals.append(float(c["price"]))
                    except Exception:
                        pass
                elif isinstance(c, (int, float)):
                    vals.append(float(c))
            if vals:
                mkt = sum(vals) / len(vals)
        elif d.get("market_avg_price") is not None:
            try:
                mkt = float(d["market_avg_price"])
            except Exception:
                mkt = None
        elif d.get("competitor_price") is not None:
            try:
                mkt = float(d["competitor_price"])
            except Exception:
                mkt = None
        d["market_avg_price"] = round(mkt, 2) if mkt else None
        if mkt:
            d["price_index"] = round(d["price"] / mkt, 3)
            d["price_gap"] = round(d["price"] - mkt, 2)
            d["price_gap_pct"] = round((d["price"] - mkt) / mkt, 4)
            if d["price_index"] > 1.10:
                d["market_band"] = "偏高"
            elif d["price_index"] < 0.90:
                d["market_band"] = "偏低"
            else:
                d["market_band"] = "持平"
        else:
            d["price_index"] = None
            d["price_gap"] = None
            d["price_gap_pct"] = None
            d["market_band"] = None
        # 定价优化器：反推达成目标利润率所需售价
        price_for_gm = (vc / (1 - target_gm)) if (1 - target_gm) > 0 else d["price"]
        d["price_for_target_gm"] = round(price_for_gm, 2)
        if has_op:
            d["price_for_target_nm"] = round(d["full_cost"] / (1 - target_nm), 2) if (1 - target_nm) > 0 else d["price"]
        else:
            d["price_for_target_nm"] = None
        d["target_gm"] = target_gm
        d["target_nm"] = target_nm
        if d["cm_pct"] >= target_gm - 1e-9:
            d["pricing_action"] = "维持（毛利率已达标）"
            d["pricing_suggest_price"] = d["price"]
        else:
            sug = price_for_gm
            note = ""
            if mkt and sug > mkt * 1.15:
                note = "（建议价超市场均价15%，同步做成本重构/价值包装）"
            d["pricing_action"] = f"建议提价至 ¥{sug:.2f}{note}"
            d["pricing_suggest_price"] = round(sug, 2)
        # 瘦狗菜：低人气+低盈利，单靠提价无效，下架/重配方优先
        if d["category_key"] == "dog":
            d["pricing_action"] = "下架/重配方优先（单靠提价无效）"
            d["pricing_suggest_price"] = d["price"]

    # 诊断
    overall_gm = total_cm / total_revenue if total_revenue else 0.0
    overall_ptr = sum((d["raw_cost"] + d["labor_apportionment"]) * d["net_volume"] for d in dishes) / total_revenue if total_revenue else 0.0
    counts = {"star": 0, "cash_cow": 0, "puzzle": 0, "dog": 0}
    cm_by_cat = {"star": 0.0, "cash_cow": 0.0, "puzzle": 0.0, "dog": 0.0}
    for d in dishes:
        counts[d["category_key"]] += 1
        cm_by_cat[d["category_key"]] += d["total_cm"]

    star_share = counts["star"] / n
    dog_share = counts["dog"] / n

    # 帕累托
    ranked = sorted(dishes, key=lambda x: x["total_cm"], reverse=True)
    top20_k = max(1, math.ceil(0.2 * n))
    top20_cm = sum(d["total_cm"] for d in ranked[:top20_k])
    top20_cm_share = top20_cm / total_cm if total_cm else 0.0
    # 80% 利润集中度：达到 80% 总毛利所需最少菜品数
    cum = 0.0
    pareto80_k = n
    for i, d in enumerate(ranked, 1):
        cum += d["total_cm"]
        if total_cm and cum / total_cm >= 0.80:
            pareto80_k = i
            break
    # 长尾：按贡献毛利排序后 20% 的菜品，消耗的首要成本占比 vs 贡献毛利占比
    tail_k = max(1, math.ceil(0.2 * n))
    tail = ranked[-tail_k:]
    tail_cm = sum(d["total_cm"] for d in tail)
    prime_total = sum((d["raw_cost"] + d["labor_apportionment"]) * d["net_volume"] for d in dishes)
    tail_prime = sum((d["raw_cost"] + d["labor_apportionment"]) * d["net_volume"] for d in tail)
    tail_cm_share = tail_cm / total_cm if total_cm else 0.0
    tail_prime_share = tail_prime / prime_total if prime_total else 0.0

    # 菜单效率分 0-100
    profit_score = min(overall_gm / bench["gm_high"], 1.0) * 40
    star_score = min(star_share / BENCH_STAR_SHARE_HIGH, 1.0) * 25
    dog_penalty = min(dog_share / BENCH_DOG_SHARE_WARN, 1.0) * 25
    conc_score = min(top20_cm_share / 0.80, 1.0) * 10
    score = max(0.0, min(100.0, profit_score + star_score + conc_score - dog_penalty))
    # 净利维度加成（仅当提供了运营成本时生效）
    net_score_added = 0.0
    if has_op and target_nm > 0:
        net_score_added = min(overall_net_margin / target_nm, 1.0) * 10
        score = max(0.0, min(100.0, score + net_score_added))
    score = round(score, 1)

    # 关键发现（自动生成）
    key_findings = []
    if counts["puzzle"] > 0:
        key_findings.append(
            f"Puzzles（问题菜）共 {counts['puzzle']} 道，正在稀释整体利润率，"
            f"其贡献毛利占比仅 {cm_by_cat['puzzle']/total_cm*100:.1f}%，建议立即干预（提价测试或成本重构）。"
        )
    if dog_share > BENCH_DOG_SHARE_WARN:
        key_findings.append(
            f"Dogs（瘦狗菜）占比 {dog_share*100:.1f}% 超过 20% 预警线，占用菜单与后厨产能，建议下架或重新配方。"
        )
    if star_share < BENCH_STAR_SHARE_LOW:
        key_findings.append(
            f"Stars（明星菜）占比 {star_share*100:.1f}% 低于 20%，菜单缺乏同时走量且高毛利的‘招牌英雄’。"
        )
    if not key_findings:
        key_findings.append("菜单结构均衡，四类菜品占比健康，无紧急预警项。")

    # 菜单级提价净影响（所有 Puzzles 执行 +10%）
    menu_delta_cm = sum(d["recommend"]["delta_cm"] for d in dishes if d["category_key"] == "puzzle")
    menu_net_impact_pct = (menu_delta_cm / total_cm * 100) if total_cm else 0.0

    diag = {
        "n": n,
        "avg_sales_mix": round(avg_sales_mix, 4),
        "avg_cm": round(avg_cm, 2),
        "total_revenue": round(total_revenue, 2),
        "total_cm": round(total_cm, 2),
        "overall_gm": round(overall_gm, 4),
        "overall_ptr": round(overall_ptr, 4),
        "counts": counts,
        "cm_by_cat": {k: round(v, 2) for k, v in cm_by_cat.items()},
        "star_share": round(star_share, 4),
        "dog_share": round(dog_share, 4),
        "star_cm_share": round(cm_by_cat["star"] / total_cm, 4) if total_cm else 0.0,
        "dog_cm_share": round(cm_by_cat["dog"] / total_cm, 4) if total_cm else 0.0,
        "pareto": {
            "top20_k": top20_k,
            "top20_cm_share": round(top20_cm_share, 4),
            "pareto80_k": pareto80_k,
            "tail_k": tail_k,
            "tail_cm_share": round(tail_cm_share, 4),
            "tail_prime_share": round(tail_prime_share, 4),
            "tail_dishes": [d["name"] for d in tail],
        },
        "menu_efficiency_score": score,
        "menu_delta_cm_puzzle10": round(menu_delta_cm, 2),
        "menu_net_impact_pct_puzzle10": round(menu_net_impact_pct, 2),
        "key_findings": key_findings,
        "bench": bench,
        # ---- 专业定价扩展诊断 ----
        "operating": {
            "total": round(op_total, 2),
            "breakdown": {k: round(v, 2) for k, v in op_breakdown.items()},
            "alloc_method": op_alloc,
            "has_operating": bool(has_op),
            "net_score_added": round(net_score_added, 1),
        },
        "overall_net_profit": round(overall_net_profit, 2),
        "overall_net_margin": round(overall_net_margin, 4),
        "avg_price_per_cover": round(avg_price_cover, 2),
        "store_positioning": store_pos,
        "price_tier_counts": {t: sum(1 for d in dishes if d["price_tier"] == t) for t in POSITION_TIERS},
        "target_gm": target_gm,
        "target_nm": target_nm,
        "net_margin_ok": (sum(1 for d in dishes if d["net_margin"] >= target_nm - 1e-9) if has_op else None),
        "market_covered": any(d["market_avg_price"] for d in dishes),
    }
    return dishes, diag


# ---------------------------------------------------------------------------
# 报告输出（专业财报口径）
# ---------------------------------------------------------------------------
def pct(x, d=2):
    return f"{x*100:.{d}f}%"


def build_report(dishes, diag, meta, bench):
    L = []
    period = meta.get("period", "未指定")
    store = meta.get("store_info", {})
    store_s = ""
    if store:
        tier = store.get("city_tier", "")
        seat = store.get("seat_num", "")
        store_s = f"（城市层级：{tier}；座位数：{seat}）" if (tier or seat) else ""
    # Executive Summary
    L.append("# Menu Engineering & Strategic Pricing — 菜单盈利能力诊断报告")
    L.append("")
    L.append("## Executive Summary（执行摘要）")
    L.append("")
    L.append(f"- **分析周期**：{period}　{store_s}")
    L.append(f"- **适用业态基准**：**{bench['label']}** — 毛利率 {pct(bench['gm_low'],0)}-{pct(bench['gm_high'],0)}；"
             f"PTR 目标 < {pct(bench['ptr_target'],0)}；价格弹性系数 {bench['elasticity']}")
    L.append(f"- **菜品数量**：{diag['n']} 道")
    L.append(f"- **Overall Menu Efficiency Score**：**{diag['menu_efficiency_score']:.1f} / 100**")
    L.append(f"- **综合毛利率 (Overall GM)**：**{pct(diag['overall_gm'])}**（业态基准 {pct(bench['gm_low'],0)}-{pct(bench['gm_high'],0)}）")
    L.append(f"- **综合首要成本率 (Overall PTR)**：**{pct(diag['overall_ptr'])}**")
    L.append(f"- **总销售额**：¥{diag['total_revenue']:,.2f}　|　**总贡献毛利**：¥{diag['total_cm']:,.2f}")
    op = diag["operating"]
    if op["has_operating"]:
        L.append(f"- **门店月运营成本**：¥{op['total']:,.2f}（按{('销量' if op['alloc_method']=='volume' else '营收')}分摊）")
        L.append(f"- **整体净利**：**¥{diag['overall_net_profit']:,.2f}**　|　**整体净利率**：**{pct(diag['overall_net_margin'])}**"
                 f"（目标净利率 {pct(diag['target_nm'])}；达标菜品 {diag['net_margin_ok']}/{diag['n']}）")
    L.append(f"- **门店价格定位**：**{diag['store_positioning']}**（人均消费均价 ¥{diag['avg_price_per_cover']:.2f}）")
    L.append("")
    L.append("**Key Findings：**")
    for f in diag["key_findings"]:
        L.append(f"- {f}")
    L.append("")

    # 1. Matrix
    L.append("## 1. Menu Engineering Matrix（菜单工程矩阵）")
    L.append("")
    L.append("```")
    L.append("High Profitability (高盈利性)")
    L.append("|")
    L.append("|  Cows (金牛)        |      Stars (明星)        |")
    L.append("|  (低受欢迎·高盈利)    |   (高受欢迎·高盈利)        |")
    L.append("|--------------------|---------------------------|  High Popularity →")
    L.append("|  Dogs (瘦狗)        |      Puzzles (问题)       |")
    L.append("|  (低受欢迎·低盈利)    |   (高受欢迎·低盈利)        |")
    L.append("|")
    L.append("Low Profitability (低盈利性)")
    L.append("```")
    L.append("")
    L.append(f"> 分类阈值 — X 轴(受欢迎度)= 平均 Sales Mix% = **{pct(diag['avg_sales_mix'])}**；"
             f"Y 轴(盈利性)= 平均单位 CM = **¥{diag['avg_cm']:.2f}**")
    L.append("")
    for key in ["star", "cash_cow", "puzzle", "dog"]:
        names = [f"{d['name']}(CM¥{d['cm']:.2f}/Mix{pct(d['sales_mix'],1)})" for d in dishes if d["category_key"] == key]
        L.append(f"- **{CATEGORY_CN[key]}**（{_cat_def(key)}）：{('、'.join(names) if names else '无')}（{len(names)} 道）")
    L.append("")

    # 2. Financial Deep Dive
    L.append("## 2. Financial Deep Dive（财务深度分析）")
    L.append("")
    L.append("| 菜品 | 类别 | CM(元) | CM Mix% | Sales Mix% | PTR(%) | 分类 | 建议行动 |")
    L.append("|------|------|------:|------:|------:|------:|------|------|")
    act_map = {
        "star": "Maintain（保护份额·优化出餐速度）",
        "cash_cow": "Menu Engineering（黄金位+价值话术主推）",
        "puzzle": "Price +10% / Cost Re-engineering",
        "dog": "Delist（下架）/ Re-formulate（重新配方）",
    }
    for d in dishes:
        L.append(
            f"| {d['name']} | {d['category'] or '—'} | {d['cm']:.2f} | {pct(d['cm_mix'])} "
            f"| {pct(d['sales_mix'])} | {pct(d['ptr'])} | {d['category_cn']} | {act_map[d['category_key']]} |"
        )
    L.append("")

    # 3. Sensitivity
    puzzles = [d for d in dishes if d["category_key"] == "puzzle"]
    L.append("## 3. Sensitivity Analysis（价格弹性与敏感度分析）")
    L.append("")
    if puzzles:
        for d in puzzles:
            rec = d["recommend"]
            if rec["price_viable"]:
                L.append(f"**Scenario — 「{d['name']}」{rec['action']}（至 ¥{rec['new_price']:.2f}）**")
            else:
                L.append(f"**Scenario — 「{d['name']}」提价敏感性（结论：提价不可行，转向成本重构）**")
            L.append("")
            L.append(f"| 模拟提价 | 新售价 | 新CM | 预测销量降幅(弹性{bench['elasticity']}) | 预测新总CM | ΔCM | 盈亏平衡销量降幅 | 盈亏平衡销量 | 弹性内可行? |")
            L.append("|------:|------:|------:|------:|------:|------:|------:|------:|:--:|")
            for s in d["scenarios"]:
                L.append(
                    f"| +{s['increase_pct']:.0f}% | ¥{s['new_price']:.2f} | ¥{s['new_cm']:.2f} "
                    f"| {s['pred_volume_drop_pct']:.1f}% | ¥{s['new_total_cm']:,.2f} | ¥{s['delta_cm']:,.2f} "
                    f"| {s['break_even_drop_pct']:.1f}% | {s['break_even_volume']:.0f}份 | {'是' if s['within_tolerance'] else '否'} |"
                )
            L.append("")
            if rec["price_viable"]:
                L.append(f"- 推荐动作：**{rec['action']}**，预测销量下滑 **{rec['pred_volume_drop_pct']:.1f}%**，"
                         f"单品贡献毛利净增 **¥{rec['delta_cm']:,.2f}**。")
                tol = "在" if rec["within_tolerance"] else "超出"
                L.append(f"- 盈亏平衡校验：只要销量降幅不超过 **{rec['break_even_drop_pct']:.1f}%** 即不亏损；"
                         f"当前弹性预测降幅{tol}盈亏平衡容忍度。")
            else:
                L.append("- 推荐动作：**不提价**。三种提价幅度（+5%/+10%/+15%）的预测销量降幅均超出盈亏平衡容忍度，"
                         "提价将稀释总贡献毛利，故转向成本重构。")
            if d["ptr"] > bench["ptr_target"]:
                L.append(f"- 成本重构目标：将 PTR 由 {pct(d['ptr'])} 降至 **{pct(bench['ptr_target'])}** 以下"
                         f"（更换供应商/调整克重/替代食材）。")
            else:
                L.append(f"- 成本侧已健康（PTR {pct(d['ptr'])} ≤ {pct(bench['ptr_target'])}）；"
                         "因绝对 CM 偏低，提价不可行时优先通过‘套餐绑定/加价配料/规格升级’提升客单价，而非直接涨价。")
            L.append("")
        L.append(f"> **菜单级净影响**：若全部 Puzzles 执行推荐提价动作，总贡献毛利预计净增 "
                 f"**¥{diag['menu_delta_cm_puzzle10']:,.2f}（{diag['menu_net_impact_pct_puzzle10']:.2f}%）**，"
                 f"对 EBITDA 呈正向贡献。")
        L.append("")
    else:
        L.append("当前菜单无 Puzzles 类菜品，无需价格弹性干预。")
        L.append("")

    # 4. Pareto
    p = diag["pareto"]
    L.append("## 4. Pareto Analysis（帕累托 80/20）")
    L.append("")
    L.append(f"- **Top 20% 菜品**（{p['top20_k']} 道）贡献了 **{pct(p['top20_cm_share'])}** 的总贡献毛利。")
    L.append(f"- **利润集中度**：仅需 **{p['pareto80_k']}** 道菜（占总数 {pct(p['pareto80_k']/diag['n'])}）即可覆盖 80% 的利润。")
    if p["tail_dishes"]:
        L.append(f"- **长尾无效菜品**（按贡献毛利排序后 20%，{p['tail_k']} 道：{('、'.join(p['tail_dishes']))}）："
                 f"仅贡献 **{pct(p['tail_cm_share'])}** 的总毛利，却消耗了 **{pct(p['tail_prime_share'])}** 的首要成本，"
                 f"属于‘高消耗·低产出’单元，优先进入下架/重估清单。")
    L.append("")

    # 5. Strategic Recommendations
    L.append("## 5. Strategic Recommendations（战略执行清单）")
    L.append("")
    stars = [d["name"] for d in dishes if d["category_key"] == "star"]
    cows = [d for d in dishes if d["category_key"] == "cash_cow"]
    dogs = [d["name"] for d in dishes if d["category_key"] == "dog"]
    L.append("1. **Menu Psychology（菜单心理学）**：将 Stars 菜品（"
             + (("、".join(stars)) if stars else "—") + "）置于菜单‘金三角’区域（右上角，视线第一落点），"
             "以最大化点选率与利润捕获。")
    L.append("2. **Decoy Effect（诱饵效应）**：引入一款定价极高的‘锚点菜品’（如 ¥388 帝王蟹/豪华套餐），"
             "拉升现有 Stars 菜品的性价比感知，间接提高高毛利菜占比。")
    if cows:
        cow_s = "、".join(f"{d['name']}(PTR{pct(d['ptr'])})" for d in cows)
        L.append(f"3. **Value Selling（价值推销）**：对 Cows 金牛菜（{cow_s}）加强服务员话术主推，"
                 "强调‘价值感’而非低价；将其调整至黄金视线位，释放被埋没的利润。")
    else:
        L.append("3. **Value Selling（价值推销）**：当前无 Cows 金牛菜，可识别高毛利慢销品并培养为金牛。")
    if puzzles:
        L.append("4. **Cost Re-engineering（成本重构）**：针对 Puzzles 问题菜执行提价测试或供应链优化，"
                 f"目标将 PTR 降至 {pct(bench['ptr_target'])} 以下，将‘引流款’转化为‘利润款’。")
    if dogs:
        L.append(f"5. **Portfolio Pruning（组合裁剪）**：对 Dogs 瘦狗菜（"
                 + ("、".join(dogs)) + "）执行下架或重新配方，回收菜单位、后厨产能与顾客注意力。")
    L.append("")

    # 6. 全成本核算与净利分析
    op = diag["operating"]
    L.append("## 6. 全成本核算与净利分析（Full-Cost & Net Profit）")
    L.append("")
    if op["has_operating"]:
        L.append(f"门店月运营成本合计 **¥{op['total']:,.2f}**，按**{('销量' if op['alloc_method']=='volume' else '营收')}**"
                 f"分摊到每道菜；下表在「贡献毛利」基础上扣减单份运营成本，得到**扣费后的真实净利**。")
        if op["breakdown"]:
            bdc = "、".join(f"{OPERATING_LABELS.get(k,k)}¥{v:,.0f}" for k, v in op["breakdown"].items())
            L.append(f"> 运营成本构成：{bdc}")
        L.append("")
        L.append("| 菜品 | 变动成本VC(食材+调料+人工) | 单份运营成本 | 完全成本 | 单份净利 | 净利率 |")
        L.append("|------|------:|------:|------:|------:|------:|")
        for d in dishes:
            L.append(f"| {d['name']} | ¥{d['total_cost']:.2f} | ¥{d['operating_apportionment']:.2f} "
                     f"| ¥{d['full_cost']:.2f} | ¥{d['net_profit']:.2f} | {pct(d['net_margin'])} |")
        L.append("")
        L.append(f"> **菜单级**：整体净利 **¥{diag['overall_net_profit']:,.2f}**，整体净利率 **{pct(diag['overall_net_margin'])}**"
                 f"（目标净利率 {pct(diag['target_nm'])}）。净利率为扣减全部运营成本后的真实盈利，"
                 f"是判断‘卖得多是否真的赚得多’的关键指标。")
        L.append("")
    else:
        L.append("> 当前输入未提供**门店运营成本**，暂按「贡献毛利（扣食材+调料+人工）」口径呈现。"
                 "如需查看扣费后的**真实净利与净利率**，请在 `store_info.operating_cost` 中补充月租金/水电/人工总摊/"
                 "折旧/营销/管理，引擎将自动分摊并给出净利率与净利率达标率。")
        L.append("")

    # 7. 市场定位分析
    L.append("## 7. 市场定位分析（Price Positioning）")
    L.append("")
    L.append(f"- **门店整体定位**：**{diag['store_positioning']}**（按人均消费均价 ¥{diag['avg_price_per_cover']:.2f} 判定；业态：{bench['label']}）")
    tc = diag["price_tier_counts"]
    tier_desc = {
        "value": "低价引流、建立性价比认知（慎防亏损）",
        "core": "走量主力、承接大多数顾客",
        "profit": "高客单利润款、拉升整体盈利",
        "image": "高价形象款、锚定价值感与品牌调性",
    }
    for t in ["value", "core", "profit", "image"]:
        names = [d["name"] for d in dishes if d["price_tier"] == t]
        L.append(f"- **{POSITION_TIERS[t]}**（{tc.get(t,0)} 道）：{('、'.join(names) if names else '无')} —— {tier_desc[t]}")
    L.append("")
    L.append("> 价格分层用于校准‘菜单价格 ladder’：引流款过多会拖累盈利，形象款缺失则缺价值锚点。"
             "理想结构应为「少量引流 + 多数主力 + 若干利润 + 1-2 形象」。")
    L.append("")

    # 8. 竞品价格参考
    if diag["market_covered"]:
        L.append("## 8. 竞品价格参考（Competitor Benchmark）")
        L.append("")
        L.append("| 菜品 | 我方售价 | 市场均价 | 价格指数 | 价差% | 市场定位 | 诊断 |")
        L.append("|------|------:|------:|------:|------:|:--:|------|")
        for d in dishes:
            if not d["market_avg_price"]:
                continue
            band = d["market_band"]
            if band == "偏低" and d["cm_pct"] >= d["target_gm"] - 1e-9:
                diag_tx = "毛利率达标但定价低于市场，存在提价空间"
            elif band == "偏高" and d["cm_pct"] < d["target_gm"] - 1e-9:
                diag_tx = "溢价未被成本支撑，需降成本或强化价值感"
            elif band == "偏高":
                diag_tx = "高端定位成立（毛利率达标）"
            elif band == "持平":
                diag_tx = "与市场持平，定价合理"
            else:
                diag_tx = "低于市场，可择机回归区间"
            L.append(f"| {d['name']} | ¥{d['price']:.2f} | ¥{d['market_avg_price']:.2f} "
                     f"| {d['price_index']:.2f} | {pct(d['price_gap_pct'])} | {band} | {diag_tx} |")
        L.append("")
        L.append("> 价格指数 = 我方售价 ÷ 市场均价；>1.10 偏高、<0.90 偏低、其余持平。结合毛利率可判断是否‘贵得有理’或‘贱卖利润’。")
        L.append("")

    # 9. 利润率目标与定价建议
    L.append("## 9. 利润率目标与定价建议（Target-Margin Pricing）")
    L.append("")
    L.append(f"- **目标毛利率**：**{pct(diag['target_gm'])}**（缺省取业态基准上限；可在 `target.gross_margin` 覆盖）")
    L.append(f"- **目标净利率**：**{pct(diag['target_nm'])}**（可在 `target.net_margin` 覆盖）")
    L.append("")
    L.append("| 菜品 | 当前售价 | 当前毛利率 | 当前净利率 | 目标毛利率 | 建议售价(达目标GM) | 建议动作 |")
    L.append("|------|------:|------:|------:|------:|------:|------|")
    for d in dishes:
        cur_nm = pct(d["net_margin"]) if op["has_operating"] else "—"
        is_dog = d["category_key"] == "dog"
        if is_dog:
            sug_gm_disp = "—"
            sug_nm_disp = ""
        elif d["cm_pct"] >= d["target_gm"] - 1e-9:
            sug_gm_disp = "维持"
            sug_nm_disp = ""
        else:
            sug_gm_disp = f"¥{d['price_for_target_gm']:.2f}"
            sug_nm_disp = f" / ¥{d['price_for_target_nm']:.2f}" if d["price_for_target_nm"] else ""
        L.append(f"| {d['name']} | ¥{d['price']:.2f} | {pct(d['cm_pct'])} | {cur_nm} "
                 f"| {pct(d['target_gm'])} | {sug_gm_disp}{sug_nm_disp} | {d['pricing_action']} |")
    L.append("")
    L.append(f"> **菜单级影响**：若全部 Puzzles 按目标毛利率重新定价，总净利预计净增 "
             f"**¥{diag['menu_delta_cm_puzzle10']:,.2f}（{diag['menu_net_impact_pct_puzzle10']:.2f}%）**"
             f"（按当前销量、运营成本固定测算）。实际落地建议小步快跑、配合价值话术与 A/B 测试。")
    L.append("")

    # Disclaimer
    L.append("---")
    L.append("")
    L.append(f"> **Disclaimer**：本报告基于历史数据与静态模型（BCG / Menu Engineering / 价格弹性系数 {bench['elasticity']}），"
             "实际经营受动态市场环境影响。决策前请咨询财务总监（CMA/CFO）。")
    L.append("")
    return "\n".join(L)


def _cat_def(key):
    return {
        "star": "高受欢迎 · 高盈利",
        "cash_cow": "低受欢迎 · 高盈利",
        "puzzle": "高受欢迎 · 低盈利",
        "dog": "低受欢迎 · 低盈利",
    }[key]


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Menu Engineering & Strategic Pricing Engine (Pro)")
    ap.add_argument("--json-input", help="JSON 文件路径；留空则从 stdin 读取")
    ap.add_argument("--input", help="遗留 CSV 文件路径；留空则从 stdin 读取")
    ap.add_argument("--json", help="将结构化结果写入该 JSON 路径")
    ap.add_argument("--format", help="业态基准：快餐 / 正餐 / 茶饮（覆盖输入数据中的 format 字段）")
    args = ap.parse_args()

    text = ""
    if args.json_input:
        if not os.path.exists(args.json_input):
            sys.stderr.write(f"输入文件不存在：{args.json_input}\n")
            sys.exit(2)
        with open(args.json_input, "r", encoding="utf-8") as f:
            text = f.read()
        force_json = True
    elif args.input:
        if not os.path.exists(args.input):
            sys.stderr.write(f"输入文件不存在：{args.input}\n")
            sys.exit(2)
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
        force_json = False
    else:
        text = sys.stdin.read()
        force_json = None

    # 自动判断格式
    stripped = text.lstrip()
    is_json = force_json if force_json is not None else (stripped.startswith("{") or stripped.startswith("["))

    if is_json:
        dishes, meta, anomalies = parse_json(text)
    else:
        dishes, meta, anomalies = parse_csv(text)

    if anomalies:
        print("⚠️ 检测到异常数据，分析已终止，请先修正：\n")
        for a in anomalies:
            print(f"- {a}")
        print("\n提示：本引擎仅基于您提供的数据计算，不编造。成本(合计)须小于售价；"
              "JSON 模式必填 raw_cost / price / sales_volume。")
        if args.json:
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump({"ok": False, "anomalies": anomalies}, f, ensure_ascii=False, indent=2)
        sys.exit(0)

    # 解析业态基准（CLI > JSON format 字段 > 通用默认）
    eff_format = args.format or meta.get("format")
    bench = get_bench(eff_format)

    dishes, diag = analyze(dishes, meta, bench)
    md = build_report(dishes, diag, meta, bench)
    print(md)

    if args.json:
        payload = {
            "ok": True,
            "meta": meta,
            "dishes": dishes,
            "diagnostics": diag,
            "benchmarks": {
                "format": bench["format"], "label": bench["label"],
                "gm_low": bench["gm_low"], "gm_high": bench["gm_high"],
                "star_share_low": BENCH_STAR_SHARE_LOW, "star_share_high": BENCH_STAR_SHARE_HIGH,
                "dog_share_warn": BENCH_DOG_SHARE_WARN,
                "ptr_target": bench["ptr_target"], "elasticity": bench["elasticity"],
                "rationale": bench["rationale"],
            },
        }
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"\n[JSON 已写入: {args.json}]")


if __name__ == "__main__":
    main()
