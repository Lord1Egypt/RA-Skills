#!/usr/bin/env python3
"""
Quick Scan v3 — 风险警报器（非分析师）

核心原则：只报结构风险，不给方向预测

铁律：
- 禁止搜索、LLM、JSON、reasoning
- 绝不给买卖建议（不喊"别追""抄底"）
- 绝不给方向预测（不说"会跌""反弹无力"）
- 绝不给确定性结论（不说"一定""必然"）
- 只报：结构状态 + 风险等级 + 置信度
"""

from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


# ============================================================
# 风险等级（纯状态，无方向）
# ============================================================
class RiskLevel(Enum):
    SAFE = "safe"
    WARNING = "warning"
    DANGER = "danger"
    CRITICAL = "critical"


class ConfidenceLevel(Enum):
    HIGH = "high"       # 70-100
    MEDIUM = "medium"   # 40-70
    LOW = "low"         # 0-40


# ============================================================
# 1. 触发器注册表（权重 + 风险描述，无方向词汇）
# ============================================================
def _check_below_all_ma(signals: Dict, _screenshot: Dict) -> bool:
    required = ['price_vs_ma7', 'price_vs_ma25', 'price_vs_ma99']
    checks = []
    for key in required:
        t = signals.get(key, {}).get('type', '')
        if not t:
            return False
        checks.append(t)
    return all(c.startswith('below') for c in checks)


def _check_fomo_extreme(signals: Dict, screenshot_data: Dict) -> bool:
    pct = screenshot_data.get('pct_change_24h', 0) or 0
    vol_ratio = signals.get('volume_vs_ma5', 1.0)
    return (pct > 20 and vol_ratio > 2) or (pct > 15 and vol_ratio < 0.5)


def _check_price_extension(signals: Dict, screenshot_data: Dict) -> bool:
    raw = screenshot_data.get('_raw_indicators', {})
    ma7 = raw.get('ma', {}).get('ma7')
    price = screenshot_data.get('price')
    if not ma7 or not price or ma7 == 0:
        return False
    return abs(price - ma7) / ma7 > 0.15


TRIGGER_REGISTRY: Dict[str, Dict[str, Any]] = {
    "panic_selling": {
        "weight": 3,
        "tag": "panic_selling",
        "risk_desc": "放量恐慌抛售",
        "structure_impact": "流动性急剧恶化",
        "check": lambda s, d: s.get('volume_status', {}).get('type') == 'high_selling',
    },
    "death_cross": {
        "weight": 2,
        "tag": "trend_break",
        "risk_desc": "MACD死叉形成",
        "structure_impact": "短期动能转弱",
        "check": lambda s, d: s.get('macd_signal', {}).get('type') == 'bearish',
    },
    "extremely_low_volume": {
        "weight": 1,
        "tag": "liquidity_dry",
        "risk_desc": "极度缩量",
        "structure_impact": "市场参与度极低",
        "check": lambda s, d: s.get('volume_status', {}).get('type') == 'extremely_low',
    },
    "low_volume": {
        "weight": 1,
        "tag": "liquidity_weak",
        "risk_desc": "成交量萎缩",
        "structure_impact": "流动性不足",
        "check": lambda s, d: s.get('volume_status', {}).get('type') == 'low',
    },
    "below_ma7": {
        "weight": 1,
        "tag": "short_term_break",
        "risk_desc": "跌破短期均线",
        "structure_impact": "短期支撑失效",
        "check": lambda s, d: s.get('price_vs_ma7', {}).get('type') == 'below_ma7',
    },
    "below_all_ma": {
        "weight": 2,
        "tag": "full_breakdown",
        "risk_desc": "跌破全部均线",
        "structure_impact": "中短期结构破坏",
        "check": _check_below_all_ma,
    },
    "bearish_ma": {
        "weight": 1,
        "tag": "structure_bearish",
        "risk_desc": "均线空头排列",
        "structure_impact": "中期趋势向下",
        "check": lambda s, d: s.get('ma_alignment', {}).get('type') == 'bearish',
    },
    "fomo_extreme": {
        "weight": 2,
        "tag": "fomo_zone",
        "risk_desc": "价格极端偏离",
        "structure_impact": "乖离率过大，均值回归风险",
        "check": _check_fomo_extreme,
    },
    "price_extension": {
        "weight": 1,
        "tag": "volatile_extension",
        "risk_desc": "价格远离均线",
        "structure_impact": "短期波动极端化",
        "check": _check_price_extension,
    },
}


# ============================================================
# 2. 置信度引擎
# ============================================================
class ConfidenceEngine:
    BASE_SCORE = 100

    DEDUCTIONS = {
        "missing_ma": 15, "missing_macd": 15,
        "missing_volume": 15, "missing_price_extremes": 10,
        "blurry_screenshot": 20,
        "no_timestamp": 10, "no_timeframe": 10,
        "meme_extra_volatility": 10,
        "altcoin_low_liquidity": 5,
    }

    @classmethod
    def calculate(cls, screenshot_data: Dict,
                  indicators: Dict, category: str) -> Dict:
        score = cls.BASE_SCORE
        deductions = []

        required_map = {
            'ma': 'missing_ma', 'macd': 'missing_macd',
            'volume': 'missing_volume', 'price_extremes': 'missing_price_extremes',
        }
        for key, ded_key in required_map.items():
            if not indicators or key not in indicators:
                score -= cls.DEDUCTIONS.get(ded_key, 10)
                deductions.append(f"缺失{key}")

        if screenshot_data.get('clarity') == 'blurry':
            score -= cls.DEDUCTIONS['blurry_screenshot']
            deductions.append("截图模糊")

        missing = screenshot_data.get('missing_elements', [])
        if missing:
            score -= 5
            deductions.append(f"截图缺失: {missing}")

        if not screenshot_data.get('time'):
            score -= cls.DEDUCTIONS['no_timestamp']
            deductions.append("无时间戳")

        validation = cls._validate_indicators(indicators)
        if not validation['valid']:
            for issue in validation['issues']:
                deductions.append(issue)
                score -= 10

        if category == 'meme':
            score -= cls.DEDUCTIONS['meme_extra_volatility']
            deductions.append("Meme币高波动（天然置信度折扣）")
        elif category == 'altcoin':
            score -= cls.DEDUCTIONS['altcoin_low_liquidity']
            deductions.append("山寨币流动性差（天然置信度折扣）")

        level = (ConfidenceLevel.HIGH if score >= 70
                 else ConfidenceLevel.MEDIUM if score >= 40
                 else ConfidenceLevel.LOW)

        return {
            "score": max(0, score),
            "level": level.value,
            "max_score": cls.BASE_SCORE,
            "deductions": deductions or ["指标完整，数据自洽"],
            "note": "基于截图质量与指标完整性，非预测准确率",
        }

    @staticmethod
    def _validate_indicators(indicators: Dict) -> Dict:
        issues = []

        price = indicators.get('current_price')
        ma7 = indicators.get('ma', {}).get('ma7')
        if price and ma7 and ma7 != 0:
            dev = abs(price - ma7) / ma7
            if dev > 0.5:
                issues.append(
                    f"MA7({ma7})与价格({price})偏离{dev:.0%}，疑似OCR错误"
                )

        macd = indicators.get('macd') or {}
        dif, dea, hist = macd.get('dif'), macd.get('dea'), macd.get('macd')
        if dif is not None and dea is not None and hist is not None:
            if abs((dif - dea) - hist) > abs(hist) * 0.5 + 0.001:
                issues.append("MACD柱与DIF/DEA计算不匹配")

        vol = indicators.get('volume', {})
        cur, ma5 = vol.get('current_bar'), vol.get('current_bar_ma5')
        if cur and ma5 and ma5 > 0:
            ratio = cur / ma5
            if ratio > 100 or ratio < 0.01:
                issues.append(f"成交量({cur})与MA5({ma5})数量级异常")

        return {"valid": len(issues) == 0, "issues": issues}


# ============================================================
# 3. 风险状态判定
# ============================================================
def determine_risk_state(signals: Dict, screenshot_data: Dict) -> Dict:
    triggered = []
    total_weight = 0
    for name, cfg in TRIGGER_REGISTRY.items():
        if cfg['check'](signals, screenshot_data):
            triggered.append({
                "trigger": name,
                "tag": cfg['tag'],
                "weight": cfg['weight'],
                "risk_desc": cfg['risk_desc'],
                "structure_impact": cfg['structure_impact'],
            })
            total_weight += cfg['weight']

    if total_weight >= 6:
        level = RiskLevel.CRITICAL
    elif total_weight >= 4:
        level = RiskLevel.DANGER
    elif total_weight >= 2:
        level = RiskLevel.WARNING
    else:
        level = RiskLevel.SAFE

    return {
        "risk_level": level.value,
        "total_weight": total_weight,
        "triggered_by": [t['tag'] for t in triggered],
        "triggered_detail": triggered,
        "threshold_note": "基于技术结构，非方向预测",
    }


# ============================================================
# 4. 冷启动模板
# ============================================================
COLD_START_TEMPLATES = {
    "meme":       "📡 正在补充：社交热度、鲸鱼地址、交易所异动...",
    "mainstream": "📡 正在补充：ETF资金流、链上流向、宏观数据...",
    "altcoin":    "📡 正在补充：解锁计划、流动性数据、概念热度...",
    "stable":     "📡 正在补充：锚定状态、储备审计、脱钩风险...",
    "commodity":  "📡 正在补充：美元指数、COMEX持仓、实物供需...",
    "equity":     "📡 正在补充：股市基本面、财报数据、监管动态...",
}


# ============================================================
# 5. Signal Reconciliation（S>A>B>C）
# ============================================================
class SignalReconciliation:
    LAYER_WEIGHTS = {
        "macro_flow":  {"weight": "S", "desc": "宏观资金流（ETF/机构）"},
        "onchain":     {"weight": "A", "desc": "链上行为（交易所流向）"},
        "sentiment":   {"weight": "A", "desc": "情绪周期（FGI/社交）"},
        "tokenomics":  {"weight": "B", "desc": "代币经济（解锁/FDV）"},
        "technical":   {"weight": "C", "desc": "技术结构（MA/MACD/量）"},
    }

    @classmethod
    def reconcile(cls, quick_state: Dict, deep_data: Dict) -> Dict:
        overlays = []

        # 宏观覆盖
        if quick_state['risk_level'] in ('danger', 'critical'):
            etf_flow = deep_data.get('etf_netflow', 0)
            if etf_flow and etf_flow > 100_000_000:
                overlays.append({
                    "layer": "macro_flow",
                    "weight": "S",
                    "quick_signal": quick_state['risk_level'],
                    "deep_evidence": f"ETF净流入${etf_flow/1e8:.1f}亿",
                    "reconciliation": "宏观资金流覆盖技术结构",
                    "user_message": "技术结构偏弱，但宏观资金持续流入，结构风险可能被稀释",
                })

        # 链上覆盖
        exchange_flow = deep_data.get('exchange_netflow', 0)
        if exchange_flow and exchange_flow < -1000:
            overlays.append({
                "layer": "onchain",
                "weight": "A",
                "quick_evidence": "缩量",
                "deep_evidence": f"交易所净流出{-exchange_flow}BTC，大户提走",
                "reconciliation": "链上行为覆盖成交量信号",
                "user_message": "缩量伴随交易所净流出，可能是筹码锁定而非流动性枯竭",
            })

        # 情绪覆盖
        fgi = deep_data.get('fear_greed_index', {})
        fgi_val = fgi.get('value', 50) if isinstance(fgi, dict) else 50
        if fgi_val < 20 and 'fomo_zone' in quick_state.get('triggered_by', []):
            overlays.append({
                "layer": "sentiment",
                "weight": "A",
                "quick_evidence": "价格极端偏离",
                "deep_evidence": f"FGI仅{fgi_val}，市场极度恐惧",
                "reconciliation": "情绪周期覆盖价格偏离信号",
                "user_message": "价格偏离但情绪极度恐惧，可能是恐慌底而非FOMO顶",
            })

        if not overlays:
            return {
                "status": "confirmed",
                "note": "多层信号一致，结构风险未被覆盖",
                "overlays": [],
            }

        overlays.sort(key=lambda x: {'S': 0, 'A': 1, 'B': 2, 'C': 3}[x['weight']])
        return {
            "status": "context_adjusted",
            "note": f"{len(overlays)}层更高权重信息覆盖技术结构信号",
            "overlays": overlays,
            "dominant_layer": overlays[0]['layer'],
        }


# ============================================================
# 6. Quick Scan v3 最终输出（风险警报器范式）
# ============================================================
def quick_scan_v3(symbol: str, category: str,
                  screenshot_data: Dict, indicators: Dict) -> str:
    from crypto_advisor import compute_indicator_signals

    signals = compute_indicator_signals(indicators)
    confidence = ConfidenceEngine.calculate(screenshot_data, indicators, category)
    risk_state = determine_risk_state(signals, screenshot_data)

    lines = [
        f"⚠️ {symbol} 快扫（{screenshot_data.get('timeframe', '4h')}）",
        f"置信度：{confidence['level'].upper()}（{confidence['score']}/100）",
        "",
    ]

    # 置信度扣分说明
    if confidence['level'] != 'high':
        lines.append("置信度说明：")
        for reason in confidence['deductions']:
            lines.append(f"• {reason}")
        lines.append("")

    # 结构状态
    lines.append("结构状态：")
    ma_type = signals.get('ma_alignment', {}).get('type', 'unknown')
    if ma_type == 'bearish':
        lines.append("• 均线空头排列（短期<中期<长期）")
    elif ma_type in ('bullish', 'bullish_fading'):
        lines.append("• 均线多头排列（短期>中期>长期）")
    else:
        lines.append("• 均线纠缠，方向不明")

    macd = signals.get('macd_signal', {})
    macd_type = macd.get('type')
    if macd_type == 'bearish':
        lines.append("• MACD死叉，短期动能转弱")
    elif macd_type == 'bullish':
        lines.append("• MACD金叉，动能转强")
    elif macd_type == 'weak_bullish':
        lines.append("• MACD弱势金叉，动能不足")
    elif macd_type == 'neutral_bullish':
        lines.append("• MACD收口，动能衰减")
    else:
        lines.append("• MACD方向不明")

    vol = signals.get('volume_status', {})
    vol_type = vol.get('type')
    vol_ratio = signals.get('volume_vs_ma5', 1.0)
    if vol_type == 'extremely_low':
        lines.append(f"• 极度缩量（{vol_ratio:.0%}），市场参与度极低")
    elif vol_type == 'low':
        lines.append(f"• 成交量萎缩（{vol_ratio:.0%}），流动性不足")
    elif vol_type == 'high_selling':
        lines.append("• 放量下跌，筹码出逃")
    elif vol_type == 'high_buying':
        lines.append("• 放量上涨，交投活跃")
    else:
        lines.append(f"• 成交量正常（{vol_ratio:.0%}）")
    lines.append("")

    # 风险等级
    emoji = {'safe': '✅', 'warning': '⚠️', 'danger': '🚨', 'critical': '🔴'}.get(
        risk_state['risk_level'], '⚪'
    )
    lines.append(
        f"{emoji} 风险等级：{risk_state['risk_level'].upper()}"
    )
    lines.append(
        f"触发信号：{', '.join(risk_state['triggered_by']) if risk_state['triggered_by'] else '无显著结构风险'}"
    )
    lines.append("")

    # 结构影响说明
    if risk_state['triggered_detail']:
        lines.append("结构影响：")
        for t in risk_state['triggered_detail']:
            lines.append(f"• {t['structure_impact']}")
        lines.append("")

    lines.append("ℹ️ 以上仅基于截图技术结构，不涉及宏观/资金/情绪判断")
    lines.append("")

    lines.append(COLD_START_TEMPLATES.get(category, "📡 正在补充详细数据..."))
    lines.append("")
    lines.append("详细分析生成中...")

    return "\n".join(lines)


# ============================================================
# 禁止方向词汇清单（测试用）
# ============================================================
FORBIDDEN_DIRECTION_WORDS = [
    '别追', '抄底', '会跌', '反弹无力', '反弹强劲',
    '买入', '卖出', '做多', '做空', '满仓', '清仓',
    '一定', '必然', '肯定', '绝对', '必定',
]


# ============================================================
# 兼容旧接口
# ============================================================
def quick_scan_v2(symbol: str, category: str,
                  screenshot_data: Dict, indicators: Dict) -> str:
    """v2 兼容入口，内部调用 v3"""
    return quick_scan_v3(symbol, category, screenshot_data, indicators)


def quick_scan(symbol: str, screenshot_data: Dict,
               indicators: Dict = None) -> str:
    if indicators is None:
        indicators = {}
    category = screenshot_data.get('asset_type', 'altcoin')
    return quick_scan_v3(symbol, category, screenshot_data, indicators)