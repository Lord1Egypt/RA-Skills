#!/usr/bin/env python3
"""
中国宏观景气分析 — 打分计算引擎

输入: JSON 格式的指标数据
输出: 各维度得分、宏观景气度、周期阶段、资产配置建议

用法:
  python3 compute_macro_score.py --input data.json [--output result.json]

输入 JSON 格式:
{
  "date": "2026-05-27",
  "indicators": {
    "hsi": {"value": 19200, "percentile": 72.5},
    "crb_spot": {"value": 540, "percentile": 65.0},
    ...
  }
}

如果提供了历史序列，脚本可自行计算百分位。否则接受预计算的百分位。
"""

import json
import sys
import argparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

# ── 指标体系定义 ──────────────────────────────────────────────

@dataclass
class Indicator:
    """单个指标定义"""
    key: str
    name: str
    dimension: str  # growth / inflation / fx / rate / credit
    direction: str  # positive 或 negative
    is_core: bool = True  # 核心指标 vs 补充指标

# 五维度全部指标
INDICATORS: List[Indicator] = [
    # ═══ 增长 ═══
    Indicator("hsi", "恒生指数收盘价", "growth", "positive", True),
    Indicator("crb_spot", "CRB现货指数:综合", "growth", "positive", True),
    Indicator("nanhua_copper", "南华沪铜指数收盘价", "growth", "positive", True),
    Indicator("nanhua_industrial", "南华工业品指数", "growth", "positive", False),
    Indicator("pmi_manufacturing", "制造业PMI", "growth", "positive", False),
    Indicator("agg_financing_yoy", "社融存量:同比", "growth", "positive", False),

    # ═══ 通胀 ═══
    Indicator("brent_crude", "布伦特原油期货结算价", "inflation", "positive", True),
    Indicator("pork_price", "猪肉平均价:全国", "inflation", "positive", True),
    Indicator("rebar_futures", "螺纹钢期货结算价", "inflation", "positive", True),
    Indicator("nanhua_agri", "南华农产品指数", "inflation", "positive", False),
    Indicator("cpi_yoy", "CPI:当月同比", "inflation", "positive", False),
    Indicator("ppi_yoy", "PPI:全部工业品:当月同比", "inflation", "positive", False),

    # ═══ 汇率 ═══
    Indicator("usdcny_fixing", "美元兑人民币中间价", "fx", "negative", True),
    Indicator("cfets_index", "CFETS人民币汇率指数", "fx", "positive", False),
    Indicator("dxy", "美元指数(DXY)", "fx", "negative", False),
    Indicator("fx_reserves", "中国外汇储备", "fx", "positive", False),
    Indicator("cn_us_spread", "中美10年期国债利差", "fx", "positive", False),

    # ═══ 利率 ═══
    Indicator("cb_tsry_index", "中债-国债总指数", "rate", "negative", True),
    Indicator("cn_10y_yield", "中国10年期国债收益率", "rate", "positive", False),
    Indicator("shibor_on", "SHIBOR隔夜", "rate", "positive", False),
    Indicator("reverse_repo_7d", "7天逆回购操作利率", "rate", "positive", False),
    Indicator("lpr_1y", "LPR 1年期", "rate", "positive", False),

    # ═══ 信用 ═══
    Indicator("cb_tsry_3_5y", "中债国债总指数(3-5年)", "credit", "negative", True),
    Indicator("cb_corp_3_5y", "中债企业债总指数(3-5年)", "credit", "negative", True),
    Indicator("credit_spread_aaa", "信用利差(AAA企业债-国债 3-5年)", "credit", "negative", False),
    Indicator("agg_financing_flow", "社会融资规模:当月值", "credit", "positive", False),
    Indicator("m2_yoy", "M2:同比", "credit", "positive", False),
    Indicator("npl_ratio", "商业银行不良贷款率", "credit", "negative", False),
]

# ── 百分位计算 ──────────────────────────────────────────────

def calc_percentile(value: float, history: List[float]) -> float:
    """
    计算 value 在 history 序列中的升序百分位排名 (0-100)
    """
    if not history:
        return 50.0  # 无数据默认中位
    sorted_hist = sorted(history)
    n = len(sorted_hist)
    # 计算严格排名: 小于 value 的数量
    below = sum(1 for v in sorted_hist if v < value)
    percentile = (below / n) * 100
    return round(percentile, 2)


def apply_direction(percentile: float, direction: str) -> float:
    """根据指标方向映射得分，结果裁剪至 0-100"""
    if direction == "positive":
        score = percentile
    else:  # negative
        score = 100.0 - percentile
    return round(max(0.0, min(100.0, score)), 2)


# ── 维度聚合 ──────────────────────────────────────────────

@dataclass
class DimensionScore:
    name: str
    score: float
    confidence: str  # high / medium / low
    details: List[dict] = field(default_factory=list)

def compute_dimension(
    dim_name: str,
    indicator_data: Dict[str, dict],
    indicators: List[Indicator],
    history_map: Optional[Dict[str, List[float]]] = None,
) -> DimensionScore:
    """
    计算单个维度得分

    indicator_data: {key: {"value": float, "percentile": float (optional)}}
    history_map: {key: [历史序列]} 用于自行计算百分位
    """
    dim_indicators = [i for i in indicators if i.dimension == dim_name]
    scores = []
    details = []

    core_available = 0
    core_total = sum(1 for i in dim_indicators if i.is_core)

    for ind in dim_indicators:
        data = indicator_data.get(ind.key)
        if data is None or data.get("value") is None:
            details.append({
                "key": ind.key,
                "name": ind.name,
                "value": None,
                "percentile": None,
                "score": None,
                "available": False,
                "is_core": ind.is_core,
            })
            continue

        value = data["value"]

        # 百分位：优先用预计算的，否则自己算
        if "percentile" in data and data["percentile"] is not None:
            percentile = data["percentile"]
        elif history_map and ind.key in history_map:
            percentile = calc_percentile(value, history_map[ind.key])
        else:
            details.append({
                "key": ind.key,
                "name": ind.name,
                "value": value,
                "percentile": None,
                "score": None,
                "available": False,
                "is_core": ind.is_core,
            })
            continue

        score = apply_direction(percentile, ind.direction)
        scores.append(score)
        if ind.is_core:
            core_available += 1

        details.append({
            "key": ind.key,
            "name": ind.name,
            "value": value,
            "percentile": round(percentile, 2),
            "score": round(score, 2),
            "direction": ind.direction,
            "available": True,
            "is_core": ind.is_core,
        })

    # 维度得分
    if scores:
        dim_score = round(sum(scores) / len(scores), 2)
    else:
        dim_score = 50.0  # 完全无数据默认中性

    # 置信度
    supp_total = sum(1 for i in dim_indicators if not i.is_core)
    if core_available == core_total and (supp_total == 0 or len(scores) >= core_total + 1):
        confidence = "高"
    elif core_available == core_total:
        confidence = "中"
    else:
        confidence = "低"

    return DimensionScore(
        name=dim_name,
        score=dim_score,
        confidence=confidence,
        details=details,
    )


# ── 周期判断 ──────────────────────────────────────────────

def classify_cycle(growth_score: float, inflation_score: float) -> Tuple[str, str]:
    """
    根据增长和通胀得分判断美林时钟阶段
    返回: (阶段中文名, 阶段英文名)
    """
    g = growth_score
    i = inflation_score

    if g >= 50 and i < 50:
        return "复苏", "Recovery"
    elif g >= 50 and i >= 50:
        return "过热", "Overheat"
    elif g < 50 and i >= 50:
        return "滞胀", "Stagflation"
    else:
        return "衰退", "Recession"


def transition_check(growth_score: float, inflation_score: float) -> Optional[str]:
    """检查是否处于过渡区 (45-55分)"""
    g_near = 45 <= growth_score <= 55
    i_near = 45 <= inflation_score <= 55
    if g_near or i_near:
        return "处于周期过渡区，建议结合趋势方向综合判断"
    return None


# ── 资产配置 ──────────────────────────────────────────────

def asset_allocation(cycle_en: str) -> dict:
    """根据周期阶段给出大类资产配置建议"""
    configs = {
        "Recovery": {
            "phase": "复苏",
            "phase_en": "Recovery",
            "rank": "股票 > 信用债 > 商品 > 现金 > 利率债",
            "allocation": {"股票": 55, "债券": 25, "商品": 10, "现金/货基": 10},
            "stock_style": "小盘成长",
            "stock_sectors": ["科技", "可选消费", "金融", "券商"],
            "stock_avoid": ["公用事业"],
            "bond_duration": "中等 (3-5年)",
            "bond_type": "信用债 > 利率债",
            "narrative": "经济回暖，企业盈利改善，通胀温和，是股票最佳配置期。建议超配权益，适度配置信用债获取票息。",
        },
        "Overheat": {
            "phase": "过热",
            "phase_en": "Overheat",
            "rank": "商品 > 股票 > 现金 > 债券",
            "allocation": {"股票": 30, "债券": 10, "商品": 40, "现金/货基": 20},
            "stock_style": "大盘价值",
            "stock_sectors": ["能源", "材料", "工业", "银行"],
            "stock_avoid": ["利率敏感型（地产、REITs）"],
            "bond_duration": "短 (<2年)",
            "bond_type": "短久期利率债、货币基金",
            "narrative": "经济高速增长，通胀压力上升，央行可能收紧货币。商品受益于需求旺盛，股票选价值防御，债券回避长久期。",
        },
        "Stagflation": {
            "phase": "滞胀",
            "phase_en": "Stagflation",
            "rank": "现金/货基 > 商品 > 短久期债 > 股票/长债",
            "allocation": {"股票": 10, "债券": 15, "商品": 25, "现金/货基": 50},
            "stock_style": "防御价值",
            "stock_sectors": ["必选消费", "医药", "公用事业", "高股息"],
            "stock_avoid": ["周期股", "科技成长"],
            "bond_duration": "短 (<2年)",
            "bond_type": "短债、货币基金，回避长债",
            "narrative": "经济下行但通胀高企，企业盈利恶化，政策两难。现金为王，商品对冲通胀，股票仅保留防御板块。",
        },
        "Recession": {
            "phase": "衰退",
            "phase_en": "Recession",
            "rank": "利率债 > 现金 > 高等级信用债 > 股票 > 商品",
            "allocation": {"股票": 10, "债券": 55, "商品": 5, "现金/货基": 30},
            "stock_style": "高股息防御",
            "stock_sectors": ["公用事业", "必选消费", "高股息红利"],
            "stock_avoid": ["金融", "地产", "周期"],
            "bond_duration": "长 (>7年)",
            "bond_type": "长久期利率债为主，高等级信用债",
            "narrative": "经济萎缩，通胀回落，央行宽松降息。债券是最佳资产，长久期利率债弹性最大。股票仅保留高股息防御仓位。",
        },
    }
    return configs.get(cycle_en, configs["Recession"])


# ── 主逻辑 ──────────────────────────────────────────────

def run_analysis(
    indicator_data: Dict[str, dict],
    history_map: Optional[Dict[str, List[float]]] = None,
    analysis_date: str = "",
) -> dict:
    """执行完整宏观景气分析"""

    # 计算五个维度得分
    dimensions = {}
    dim_names = ["growth", "inflation", "fx", "rate", "credit"]
    dim_labels = {"growth": "增长", "inflation": "通胀", "fx": "汇率", "rate": "利率", "credit": "信用"}

    for dim in dim_names:
        dim_score = compute_dimension(dim, indicator_data, INDICATORS, history_map)
        dimensions[dim] = dim_score

    # 宏观景气度 = 增长*0.2 + (100-通胀)*0.2 + (100-利率)*0.2 + 汇率*0.2 + 信用*0.2
    # 通胀和利率取反向：低通胀/低利率对经济友好，应提升景气度
    macro_climate = round(
        dimensions["growth"].score * 0.2
        + (100 - dimensions["inflation"].score) * 0.2
        + (100 - dimensions["rate"].score) * 0.2
        + dimensions["fx"].score * 0.2
        + dimensions["credit"].score * 0.2,
        2,
    )

    # 周期判断
    growth_score = dimensions["growth"].score
    inflation_score = dimensions["inflation"].score
    cycle_cn, cycle_en = classify_cycle(growth_score, inflation_score)
    transition = transition_check(growth_score, inflation_score)

    # 资产配置
    allocation = asset_allocation(cycle_en)

    # 汇总结果
    result = {
        "date": analysis_date,
        "macro_climate_score": macro_climate,
        "cycle": {"cn": cycle_cn, "en": cycle_en},
        "transition_warning": transition,
        "dimensions": {},
        "asset_allocation": allocation,
    }

    for dim in dim_names:
        ds = dimensions[dim]
        result["dimensions"][dim_labels[dim]] = {
            "score": ds.score,
            "confidence": ds.confidence,
            "indicators": ds.details,
        }

    return result


def format_output(result: dict) -> str:
    """格式化输出人类可读的分析结果"""
    lines = []
    lines.append("=" * 70)
    lines.append(f"  中国宏观景气分析报告")
    lines.append(f"  日期: {result['date']}")
    lines.append(f"  ─────────────────────────────────────────")
    lines.append(f"  宏观景气度: {result['macro_climate_score']:.1f} / 100")
    lines.append(f"  经济周期阶段: {result['cycle']['cn']} ({result['cycle']['en']})")
    if result["transition_warning"]:
        lines.append(f"  ⚠ {result['transition_warning']}")
    lines.append("=" * 70)

    dim_order = ["增长", "通胀", "汇率", "利率", "信用"]
    for dim_name in dim_order:
        d = result["dimensions"][dim_name]
        conf_icon = {"高": "🟢", "中": "🟡", "低": "🔴"}.get(d["confidence"], "⚪")
        lines.append(f"\n{'─' * 50}")
        lines.append(f"  [{dim_name}] 得分: {d['score']:.1f}  置信度: {conf_icon} {d['confidence']}")
        lines.append(f"{'─' * 50}")
        for ind in d["indicators"]:
            if ind["available"]:
                tag = "★" if ind["is_core"] else " +"
                dir_arrow = {"positive": "↑", "negative": "↓"}.get(ind.get("direction", ""), "")
                lines.append(
                    f"  {tag} {ind['name']:30s}  当前值: {ind['value']:>12}  "
                    f"百分位: {ind['percentile']:>6.1f}  → 得分: {ind['score']:>6.1f}  {dir_arrow}"
                )
            else:
                tag = "✗" if ind["is_core"] else " -"
                lines.append(f"  {tag} {ind['name']:30s}  [数据缺失]")

    lines.append(f"\n{'=' * 70}")
    lines.append(f"  大类资产配置建议 — {result['cycle']['cn']}阶段")
    lines.append(f"{'=' * 70}")
    alloc = result["asset_allocation"]
    lines.append(f"  配置排序: {alloc['rank']}")
    lines.append(f"  配置比例: 股票 {alloc['allocation']['股票']}% | 债券 {alloc['allocation']['债券']}% | "
                 f"商品 {alloc['allocation']['商品']}% | 现金 {alloc['allocation']['现金/货基']}%")
    lines.append(f"  股票风格: {alloc['stock_style']}")
    lines.append(f"  推荐板块: {', '.join(alloc['stock_sectors'])}")
    lines.append(f"  回避板块: {', '.join(alloc['stock_avoid'])}")
    lines.append(f"  债券久期: {alloc['bond_duration']}")
    lines.append(f"  债券品种: {alloc['bond_type']}")
    lines.append(f"\n  💡 {alloc['narrative']}")
    lines.append(f"{'=' * 70}")

    return "\n".join(lines)


# ── CLI ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="中国宏观景气分析打分引擎")
    parser.add_argument("--input", "-i", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", "-o", help="输出 JSON 文件路径 (可选)")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    date = data.get("date", "")
    indicator_data = data.get("indicators", {})
    history_map = data.get("history", None)

    result = run_analysis(indicator_data, history_map, date)

    if args.format == "json":
        output_str = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output_str = format_output(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"结果已写入: {args.output}", file=sys.stderr)

    print(output_str)


if __name__ == "__main__":
    main()
