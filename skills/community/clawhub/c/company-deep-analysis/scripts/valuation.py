#!/usr/bin/env python3
"""
公司估值模块 —— 10 个相对估值变体 + 行业判定 + 自动数据适配。

数据流：
  1. 读 系统临时目录/{code}_data.json（collect_data.py 采集；macOS/Linux = /tmp/，Windows = %TEMP%）
  2. ensure_ebitda(data) —— 自动从三表拆解 EBITDA（A股；港股无 OCF 自动跳过）
  3. estimate_value(data) —— 按行业判定走对应变体
  4. 输出 JSON：方法名 / 估值区间 / 关键假设 / 数据完整度

设计原则：
  - 纯 stdlib（无第三方依赖）
  - 每个函数 1 个返回 dict，方便上层组装
  - 数据缺失时返回 {"error": "..."}，不硬算
  - 报告层只取"估值区间"和"关键假设"，公式不进报告

权威背书：
  - PE/PB/PS 传统倍数法：Damodaran《Investment Valuation》Ch.11-12
  - EV/EBITDA：McKinsey《Valuation》Ch.22（资本密集行业）
  - 周期中点 PE：Damodaran Ch.10 "Roller-Coaster Valuation"
  - 行业方法选择：见 §7 行业判定框架
"""

import json
import os
import sys
import statistics
import tempfile
from typing import Optional

try:
    from westock_data import _safe_float as _f
except ImportError:
    def _f(v):  # 降级版：百分号不支持（westock_data 不可用时的 fallback）
        if v is None or v == "" or v == "--":
            return None
        try:
            if isinstance(v, str):
                v = v.replace(",", "").replace("元", "").strip()
            return float(v)
        except (ValueError, TypeError):
            return None


# ── 数据源适配：自动从三表拆 EBITDA（A股新浪 / 港股跳过） ──
def ensure_ebitda(data):
    """
    优先用 data["ebitda"]（gildata MCP 接入时会预填）；
    否则调 westock_data.calc_ebitda() 拆解；
    再否则返回 None，估值跳过 EV/EBITDA 变体。
    """
    if data.get("ebitda") and isinstance(data["ebitda"], dict) and data["ebitda"].get("EBITDA"):
        return data["ebitda"]

    try:
        # 懒加载：避免 collect_data 没安装时 import 报错
        from westock_data import calc_ebitda
        return calc_ebitda(data)
    except (ImportError, Exception) as e:
        return {"EBITDA": None, "error": f"EBITDA 拆解失败: {e}"}


# ══════════════════════════════════════════════════════════════
# 一、PE 估值（3 个变体）
# ══════════════════════════════════════════════════════════════

def val_pe_ttm(data, peer_pe_median=None):
    """
    PE-TTM 估值：当前市值 / 滚动 12 月净利润
    适用：盈利稳定的成熟公司（消费/医药/公用）
    """
    eps_ttm = _f(data.get("eps_ttm"))
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))

    if not (eps_ttm and price and shares and eps_ttm > 0):
        return {"error": "EPS/股价/股本缺失或 EPS 非正"}

    market_cap = price * shares
    pe_ttm = price / eps_ttm

    # 用可比公司 PE 中位数算"合理估值"
    if peer_pe_median and peer_pe_median > 0:
        reasonable_market_cap = eps_ttm * peer_pe_median * shares
        reasonable_price = reasonable_market_cap / shares
        upside = (reasonable_price - price) / price
    else:
        # 退化：用自身 PE 作为基准（合理市值 = 当前市值）
        reasonable_market_cap = market_cap
        reasonable_price = price
        upside = 0.0
        peer_pe_median = pe_ttm

    return {
        "方法": "PE-TTM",
        "EPS-TTM": round(eps_ttm, 2),
        "PE-TTM": round(pe_ttm, 2),
        "可比公司 PE 中位数": round(peer_pe_median, 2),
        "合理股价": round(reasonable_price, 2),
        "合理市值(亿)": round(reasonable_market_cap / 1e8, 2) if peer_pe_median else None,
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "eps_ttm / quote / peers"
    }


def val_pe_forward(data, peer_pe_median=None, eps_growth_assumption=0.10):
    """
    PE-Forward 估值：用一致预期 EPS（ths_forecast）
    适用：盈利可见的高增长（券商/部分科技）
    """
    eps_forward = _f(data.get("eps_forward"))  # 一致预期次年 EPS
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))

    if not (eps_forward and price and shares and eps_forward > 0):
        return {"error": "Forward EPS/股价/股本缺失"}

    market_cap = price * shares
    pe_forward = price / eps_forward

    if peer_pe_median and peer_pe_median > 0:
        reasonable_price = eps_forward * peer_pe_median
        upside = (reasonable_price - price) / price
    else:
        reasonable_price = price
        upside = 0.0
        peer_pe_median = pe_forward

    return {
        "方法": "PE-Forward",
        "EPS-Forward": round(eps_forward, 2),
        "PE-Forward": round(pe_forward, 2),
        "可比公司 PE 中位数": round(peer_pe_median, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "ths_forecast / quote / peers"
    }


def val_pe_cycle(data, peer_pe_cycle_median=None, lookback_years=7):
    """
    周期中点 PE：用 5-10 年平均 PE 估值
    适用：周期制造（钢/化/煤/航运）—— 顶部 PE 反而最低，不能用 TTM

    ⚠️ 关键：必须用 lookback_years 年的 EPS 均值 × 当前 PE 中位数，
    不能用当前 EPS × 历史 PE 中位数（这是周期股估值的常见错误）
    """
    eps_history = data.get("eps_history", [])  # 历史 EPS 数组（最新到最旧）
    price = _f(data.get("price"))

    if not (price and len(eps_history) >= lookback_years):
        return {"error": f"需要至少 {lookback_years} 年历史 EPS"}

    # 取最近 lookback_years 年
    eps_recent = [_f(e) for e in eps_history[:lookback_years] if _f(e)]
    if not eps_recent:
        return {"error": "历史 EPS 数据无效"}

    # 关键：用历史 EPS 中位数（不是平均数，规避极值）
    eps_cycle_median = statistics.median(eps_recent)

    if peer_pe_cycle_median and peer_pe_cycle_median > 0:
        reasonable_price = eps_cycle_median * peer_pe_cycle_median
    else:
        # 退化：用行业默认周期 PE（消费品 15-20x、周期股 8-12x）
        peer_pe_cycle_median = 10.0
        reasonable_price = eps_cycle_median * peer_pe_cycle_median

    shares = _f(data.get("total_shares"))
    upside = (reasonable_price - price) / price

    return {
        "方法": f"周期中点 PE（{lookback_years}年）",
        "EPS-中位数": round(eps_cycle_median, 2),
        "周期 PE 中位数": round(peer_pe_cycle_median, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "历史 EPS 区间": [round(e, 2) for e in eps_recent],
        "数据来源": f"历史 EPS × {lookback_years} 年 / 同行业周期 PE"
    }


# ══════════════════════════════════════════════════════════════
# 二、PB 估值（2 个变体）
# ══════════════════════════════════════════════════════════════

def val_pb_mrq(data, peer_pb_median=None):
    """
    PB-MRQ 估值：当前市值 / 最新季报归母净资产
    适用：银行、地产、重资产
    """
    bvps = _f(data.get("bvps"))  # 每股净资产
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))

    if not (bvps and price and shares and bvps > 0):
        return {"error": "BVPS/股价/股本缺失"}

    market_cap = price * shares
    pb = price / bvps

    if peer_pb_median and peer_pb_median > 0:
        reasonable_price = bvps * peer_pb_median
        upside = (reasonable_price - price) / price
    else:
        reasonable_price = price
        upside = 0.0
        peer_pb_median = pb

    return {
        "方法": "PB-MRQ",
        "BVPS": round(bvps, 2),
        "PB": round(pb, 2),
        "可比公司 PB 中位数": round(peer_pb_median, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "finance.bvps / quote / peers"
    }


def val_pb_forward(data, peer_pb_median=None, roe_assumption=0.10):
    """
    PB-Forward 估值：用预测 ROE 推合理 PB
    公式：合理 PB = (ROE - g) / (COE - g)  （Gordon 增长模型推导）
    适用：银行、券商
    """
    bvps = _f(data.get("bvps"))
    price = _f(data.get("price"))

    coe = 0.10  # 股权成本（默认 10%）
    g = 0.03    # 永续增长（默认 3%）

    if not (bvps and price and bvps > 0):
        return {"error": "BVPS/股价缺失"}

    pb = price / bvps
    reasonable_pb = (roe_assumption - g) / (coe - g)
    reasonable_price = bvps * reasonable_pb
    upside = (reasonable_price - price) / price

    return {
        "方法": "PB-Forward（Gordon 推导）",
        "BVPS": round(bvps, 2),
        "当前 PB": round(pb, 2),
        "假设 ROE": f"{roe_assumption*100:.1f}%",
        "合理 PB": round(reasonable_pb, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "ROE 假设 / COE 10% / g 3%"
    }


# ══════════════════════════════════════════════════════════════
# 三、PS 估值（2 个变体）
# ══════════════════════════════════════════════════════════════

def val_ps_ttm(data, peer_ps_median=None):
    """
    PS-TTM 估值：当前市值 / 滚动 12 月营收
    适用：高成长未盈利（早期互联网、生物）
    """
    sps_ttm = _f(data.get("sps_ttm"))  # 每股营收
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))

    if not (sps_ttm and price and shares and sps_ttm > 0):
        return {"error": "SPS/股价/股本缺失"}

    ps = price / sps_ttm

    if peer_ps_median and peer_ps_median > 0:
        reasonable_price = sps_ttm * peer_ps_median
        upside = (reasonable_price - price) / price
    else:
        reasonable_price = price
        upside = 0.0
        peer_ps_median = ps

    return {
        "方法": "PS-TTM",
        "SPS-TTM": round(sps_ttm, 2),
        "PS-TTM": round(ps, 2),
        "可比公司 PS 中位数": round(peer_ps_median, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "sps_ttm / quote / peers"
    }


def val_ps_forward(data, peer_ps_median=None):
    """
    PS-Forward 估值：用一致预期营收
    适用：高成长可见（已盈利路径清晰）
    """
    sps_forward = _f(data.get("sps_forward"))
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))

    if not (sps_forward and price and shares and sps_forward > 0):
        return {"error": "Forward SPS/股价/股本缺失"}

    ps = price / sps_forward

    if peer_ps_median and peer_ps_median > 0:
        reasonable_price = sps_forward * peer_ps_median
        upside = (reasonable_price - price) / price
    else:
        reasonable_price = price
        upside = 0.0

    return {
        "方法": "PS-Forward",
        "SPS-Forward": round(sps_forward, 2),
        "PS-Forward": round(ps, 2),
        "可比公司 PS 中位数": round(peer_ps_median, 2) if peer_ps_median else None,
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "ths_forecast / quote / peers"
    }


# ══════════════════════════════════════════════════════════════
# 四、EV/EBITDA 估值（2 个变体）
# ══════════════════════════════════════════════════════════════

def val_ev_ebitda_ttm(data, peer_ev_ebitda_median=None, ebitda_obj=None):
    """
    EV/EBITDA-TTM 估值：EV / 滚动 12 月 EBITDA
    适用：资本密集（半导体、资源、航空、跨国比较）

    ⚠️ 关键：EBITDA 必须是"扣非"或"主营 EBITDA"，不要包含投资收益
    """
    ebitda_info = ebitda_obj or ensure_ebitda(data)
    ebitda = _f(ebitda_info.get("EBITDA")) if ebitda_info else None
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))
    net_debt = _f(data.get("net_debt")) or 0  # 净负债（短借+长借-货币）

    if not (ebitda and price and shares and ebitda > 0):
        return {"error": f"EBITDA/股价/股本缺失: EBITDA={ebitda}"}

    market_cap = price * shares
    ev = market_cap + net_debt
    ev_ebitda = ev / ebitda

    if peer_ev_ebitda_median and peer_ev_ebitda_median > 0:
        reasonable_ev = ebitda * peer_ev_ebitda_median
        reasonable_market_cap = reasonable_ev - net_debt
        reasonable_price = reasonable_market_cap / shares
        upside = (reasonable_price - price) / price
    else:
        reasonable_price = price
        upside = 0.0
        peer_ev_ebitda_median = ev_ebitda

    return {
        "方法": "EV/EBITDA-TTM",
        "EBITDA(亿)": round(ebitda / 1e8, 2),
        "EV(亿)": round(ev / 1e8, 2),
        "EV/EBITDA": round(ev_ebitda, 2),
        "可比公司 EV/EBITDA 中位数": round(peer_ev_ebitda_median, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "calc_ebitda(lrb+llb) / quote / peers",
        "EBITDA 拆解": ebitda_info
    }


def val_ev_ebitda_forward(data, peer_ev_ebitda_median=None, ebitda_growth=0.10):
    """
    EV/EBITDA-Forward：用预测 EBITDA
    """
    ebitda_info = ensure_ebitda(data)
    ebitda_ttm = _f(ebitda_info.get("EBITDA")) if ebitda_info else None
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))
    net_debt = _f(data.get("net_debt")) or 0

    if not (ebitda_ttm and price and shares and ebitda_ttm > 0):
        return {"error": "EBITDA/股价/股本缺失"}

    ebitda_forward = ebitda_ttm * (1 + ebitda_growth)
    market_cap = price * shares
    ev = market_cap + net_debt
    ev_ebitda = ev / ebitda_forward

    if peer_ev_ebitda_median and peer_ev_ebitda_median > 0:
        reasonable_ev = ebitda_forward * peer_ev_ebitda_median
        reasonable_market_cap = reasonable_ev - net_debt
        reasonable_price = reasonable_market_cap / shares
        upside = (reasonable_price - price) / price
    else:
        reasonable_price = price
        upside = 0.0
        peer_ev_ebitda_median = ev_ebitda

    return {
        "方法": "EV/EBITDA-Forward",
        "EBITDA-Forward(亿)": round(ebitda_forward / 1e8, 2),
        "EBITDA 增长率假设": f"{ebitda_growth*100:.1f}%",
        "EV/EBITDA-Forward": round(ev_ebitda, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "TTM EBITDA × 增长假设 / peers"
    }


# ══════════════════════════════════════════════════════════════
# 五、EV/Revenue 估值（1 个变体）
# ══════════════════════════════════════════════════════════════

def val_ev_revenue_ttm(data, peer_ev_revenue_median=None):
    """
    EV/Revenue-TTM：EV / 滚动 12 月营收
    适用：互联网平台、SaaS、轻资产高增长
    """
    revenue_ttm = _f(data.get("revenue_ttm"))
    price = _f(data.get("price"))
    shares = _f(data.get("total_shares"))
    net_debt = _f(data.get("net_debt")) or 0

    if not (revenue_ttm and price and shares and revenue_ttm > 0):
        return {"error": "营收/股价/股本缺失"}

    market_cap = price * shares
    ev = market_cap + net_debt
    ev_revenue = ev / revenue_ttm

    if peer_ev_revenue_median and peer_ev_revenue_median > 0:
        reasonable_ev = revenue_ttm * peer_ev_revenue_median
        reasonable_market_cap = reasonable_ev - net_debt
        reasonable_price = reasonable_market_cap / shares
        upside = (reasonable_price - price) / price
    else:
        reasonable_price = price
        upside = 0.0
        peer_ev_revenue_median = ev_revenue

    return {
        "方法": "EV/Revenue-TTM",
        "营收-TTM(亿)": round(revenue_ttm / 1e8, 2),
        "EV(亿)": round(ev / 1e8, 2),
        "EV/Revenue": round(ev_revenue, 2),
        "可比公司 EV/Revenue 中位数": round(peer_ev_revenue_median, 2),
        "合理股价": round(reasonable_price, 2),
        "上行空间": f"{upside*100:+.1f}%",
        "数据来源": "revenue_ttm / quote / peers"
    }


# ══════════════════════════════════════════════════════════════
# 六、Rule of 40（SaaS 专用变体）
# ══════════════════════════════════════════════════════════════

def val_rule_of_40(data, peer_ev_revenue_median=None):
    """
    Rule of 40 = 营收增速 + EBITDA 利润率 ≥ 40%
    适用：SaaS、互联网平台

    如果满足 Rule of 40，给 EV/Revenue 加溢价
    """
    revenue_growth = _f(data.get("revenue_growth"))  # 营收 YoY
    ebitda_info = ensure_ebitda(data)
    ebitda = _f(ebitda_info.get("EBITDA")) if ebitda_info else None
    revenue_ttm = _f(data.get("revenue_ttm"))

    if not (revenue_growth is not None and ebitda is not None and revenue_ttm):
        return {"error": "营收增速/EBITDA/营收缺失"}

    ebitda_margin = ebitda / revenue_ttm if revenue_ttm else 0
    rule_score = revenue_growth + ebitda_margin

    # 满足 Rule of 40 → EV/Revenue 溢价 1.5x
    premium = 1.5 if rule_score >= 0.40 else 1.0
    method_note = "✓ 满足 Rule of 40" if rule_score >= 0.40 else "✗ 未满足 Rule of 40"

    ev_rev_result = val_ev_revenue_ttm(data, peer_ev_revenue_median)
    if "合理股价" in ev_rev_result:
        ev_rev_result["合理股价"] = round(ev_rev_result["合理股价"] * premium, 2)
        ev_rev_result["Rule of 40 溢价"] = f"×{premium}"
        ev_rev_result["Rule 评分"] = f"{rule_score*100:.1f}%"
        ev_rev_result["方法"] = "EV/Revenue + Rule of 40"

    ev_rev_result["数据来源"] = f"营收增速 {revenue_growth*100:.1f}% + EBITDA 率 {ebitda_margin*100:.1f}% = {method_note}"

    return ev_rev_result


# ══════════════════════════════════════════════════════════════
# 七、行业判定框架 + 顶层 estimate_value
# ══════════════════════════════════════════════════════════════

def _ebitda_available(data):
    """EBITDA 是否可得（用于优雅跳过 EV/EBITDA 变体）。"""
    eb = data.get("ebitda")
    return isinstance(eb, dict) and bool(eb.get("EBITDA"))


def _classify_industry(data):
    """
    行业判定（按行业属性选择估值变体）：
      1. 现金流稳不稳？
      2. 资产重 vs 轻？
      3. 行业特殊触发？
      4. 是否盈利用 Forward？

    返回：(industry_class, recommended_methods_dict)
    """
    industry_swhy = data.get("industry_swhy", "")  # 申万一级
    code = data.get("code", "")

    # 周期制造
    cycle_industries = ["钢铁", "化工", "煤炭", "石油石化", "有色金属", "建材", "航运"]
    for kw in cycle_industries:
        if kw in industry_swhy:
            return "周期制造", {"primary": "val_pe_cycle", "secondary": ["val_pb_mrq", "val_ev_ebitda_ttm"]}

    # 银行/券商
    if any(kw in industry_swhy for kw in ["银行", "非银金融", "证券"]):
        return "金融", {"primary": "val_pb_mrq", "secondary": ["val_pb_forward", "val_pe_ttm"]}

    # 地产
    if "房地产" in industry_swhy or "地产" in industry_swhy:
        return "地产", {"primary": "val_pb_mrq", "secondary": ["val_ev_ebitda_ttm"]}

    # 公用事业
    if any(kw in industry_swhy for kw in ["公用事业", "电力", "水务", "燃气"]):
        return "公用事业", {"primary": "val_pe_ttm", "secondary": ["val_pb_mrq"]}

    # 资源/矿业
    if any(kw in industry_swhy for kw in ["矿业", "采掘", "有色金属"]):
        return "资源", {"primary": "val_ev_ebitda_ttm", "secondary": ["val_pb_mrq"]}

    # 半导体/航空（资本密集）
    if any(kw in industry_swhy for kw in ["半导体", "航空", "航运"]):
        return "资本密集", {"primary": "val_ev_ebitda_ttm", "secondary": ["val_pe_ttm"]}

    # SaaS / 互联网
    if any(kw in industry_swhy for kw in ["计算机", "传媒", "互联网", "软件"]):
        return "互联网/SaaS", {"primary": "val_rule_of_40", "secondary": ["val_ev_revenue_ttm", "val_ps_ttm"]}

    # 创新药
    if "医药生物" in industry_swhy and "亏损" in str(data.get("profit_status", "")):
        return "创新药", {"primary": "val_ps_ttm", "secondary": ["val_ev_revenue_ttm"]}

    # 消费/医药成熟
    if any(kw in industry_swhy for kw in ["食品饮料", "家用电器", "纺织服饰", "美容护理"]):
        return "品牌消费", {"primary": "val_pe_ttm", "secondary": ["val_pe_forward", "val_ev_ebitda_ttm"]}

    # 兜底：通用
    return "通用", {"primary": "val_pe_ttm", "secondary": ["val_pb_mrq", "val_ev_ebitda_ttm"]}


def estimate_value(data, peer_multiples=None):
    """
    顶层入口：读 data.json → 判定行业 → 调对应方法 → 输出估值区间

    输入：data（从 {系统临时目录}/{code}_data.json 加载）
    输出：{
        "行业分类": "周期制造",
        "首选方法": "周期中点 PE",
        "首选估值": {...},
        "交叉验证": [{...}, {...}],
        "综合中枢": float,
        "上行空间": str,
        "数据完整度": float  # 0-1
    }
    """
    peer_multiples = peer_multiples or {}
    industry_class, methods = _classify_industry(data)

    # 按方法签名筛选 peer_multiples（避免 PE 收到 PB 参数）
    def _filter_kwargs(fn, kwargs):
        import inspect
        try:
            valid = [p for p in inspect.signature(fn).parameters if p != "data"]
        except (ValueError, TypeError):
            return {}
        return {k: v for k, v in kwargs.items() if k in valid}

    # 调首选方法
    primary_name = methods["primary"]
    primary_fn = globals().get(primary_name)
    if primary_fn:
        primary_result = primary_fn(data, **_filter_kwargs(primary_fn, peer_multiples))
    else:
        primary_result = {"error": f"方法 {primary_name} 未找到"}

    # 调交叉验证方法
    # 港股无一致预期数据源时跳过 val_pe_forward（不计入"成功/失败"也不参与中枢）
    cross_results = []
    skipped = []  # 跳过的方法名（用于数据完整度分母调整）
    for sec_name in methods.get("secondary", []):
        sec_fn = globals().get(sec_name)
        if not sec_fn:
            continue
        # 港股 / 未采 ths_forecast → 跳过 val_pe_forward
        if sec_name == "val_pe_forward" and not _f(data.get("eps_forward")):
            cross_results.append({"方法": "PE-Forward", "跳过": "无一致预期数据（港股 / 未采 ths_forecast）"})
            skipped.append(sec_name)
            continue
        # 港股无现金流量表 → EBITDA 不可得 → 跳过 EV/EBITDA 变体
        if sec_name in ("val_ev_ebitda_ttm", "val_ev_ebitda_forward") and not _ebitda_available(data):
            label = "EV/EBITDA-TTM" if sec_name == "val_ev_ebitda_ttm" else "EV/EBITDA-Forward"
            cross_results.append({"方法": label, "跳过": "无 EBITDA 数据（港股无现金流量表 / OCF 缺失）"})
            skipped.append(sec_name)
            continue
        cross_results.append(sec_fn(data, **_filter_kwargs(sec_fn, peer_multiples)))

    # 计算综合中枢（取所有成功方法的"合理股价"中位数；跳过的不参与）
    all_prices = []
    if "合理股价" in primary_result:
        all_prices.append(primary_result["合理股价"])
    for cr in cross_results:
        if "合理股价" in cr and not cr.get("跳过"):
            all_prices.append(cr["合理股价"])

    center_price = statistics.median(all_prices) if all_prices else None
    current_price = _f(data.get("price"))
    upside = (center_price - current_price) / current_price if (center_price and current_price) else None

    # 数据完整度 = 成功方法数 / 实际执行的方法数（跳过的从分母中扣除）
    total_methods = 1 + len(methods.get("secondary", [])) - len(skipped)
    success_methods = sum(1 for r in [primary_result] + cross_results
                          if "error" not in r and not r.get("跳过"))
    data_completeness = success_methods / total_methods if total_methods else 0

    return {
        "行业分类": industry_class,
        "首选方法": primary_name.replace("val_", "").replace("_", " ").upper(),
        "首选估值": primary_result,
        "交叉验证": cross_results,
        "综合中枢(元)": round(center_price, 2) if center_price else None,
        "当前股价": current_price,
        "上行空间": f"{upside*100:+.1f}%" if upside is not None else "N/A",
        "数据完整度": f"{data_completeness*100:.0f}%",
        "提示": "数据完整度 < 60% 时建议补充行业数据" if data_completeness < 0.6 else None
    }


# ══════════════════════════════════════════════════════════════
# 八、主入口（CLI）
# ══════════════════════════════════════════════════════════════

def _load_data(code):
    """读 {系统临时目录}/{code}_data.json（macOS/Linux = /tmp/，Windows = %TEMP%）"""
    # 跨平台：macOS/Linux 走 /tmp/（保持向后兼容），Windows 走 %TEMP%
    if sys.platform == "win32":
        tmp = tempfile.gettempdir()
    else:
        tmp = "/tmp"
    paths = [
        os.path.join(tmp, f"{code}_data.json"),
        os.path.join(tmp, f"{code.lower()}_data.json"),
        os.path.join(tmp, f"{code.upper()}_data.json"),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    return None


def main():
    if len(sys.argv) < 2:
        print("用法: python3 valuation.py <股票代码> [可比公司倍数JSON文件]")
        print("示例: python3 valuation.py 600519")
        print("      python3 valuation.py 600519 peers.json  # peers.json: {\"peer_pe_median\": 18.5}")
        sys.exit(1)

    code = sys.argv[1]
    peer_multiples = {}

    if len(sys.argv) > 2 and os.path.exists(sys.argv[2]):
        with open(sys.argv[2], "r", encoding="utf-8") as f:
            peer_multiples = json.load(f)

    data = _load_data(code)
    if not data:
        # 错误提示也用跨平台路径
        if sys.platform == "win32":
            _errdir = tempfile.gettempdir()
        else:
            _errdir = "/tmp"
        print(f"❌ {os.path.join(_errdir, f'{code}_data.json')} 不存在，请先跑 collect_data.py")
        sys.exit(1)

    result = estimate_value(data, peer_multiples)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
