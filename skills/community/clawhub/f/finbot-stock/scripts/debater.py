#!/usr/bin/env python3
"""
棱镜 多空辩论引擎 v1.0 — 选股决策的辩论前置环节
为AI提供结构化辩论框架：多头(看涨) vs 空头(看跌) → 主持人裁决
"""

import json
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from analyzer import analyze_stock_factors, collect_market_data

# ============ 分歧转一致检测（短线生态核心信号）============
# A股短线资金从"分歧"（多空对抗激烈）到"一致"（多方胜出封板）
# 参考：私募打板策略正在"点火阶段或分歧转一致过程中通过算法介入"
#       凯文(好买基金)："2-5日事件驱动短线"取代"日内T+0式博弈"
def detect_divergence_to_consensus(factors):
    """检测分歧转一致信号
    
    分歧特征：放量+高换手+价格窄幅震荡（多空在打架）
    一致特征：放量+价格突破前高（多方赢了）
    
    如果检测到正在从分歧转向一致，这是短线的最佳介入点。
    """
    signals = []
    score = 0
    
    change_3d = factors.get("change_3d", 0)
    change_1d = factors.get("change_pct", 0)
    vol_ratio = factors.get("volume_ratio", 0)
    pullback = factors.get("pullback_from_high", 0)
    bullish_div = factors.get("bullish_divergence", False)
    
    # 信号1：缩量回调后放量上涨（分歧转一致最常见形态）
    # 昨天跌但缩量→今天涨且放量=分歧转一致
    if bullish_div and change_1d > 0:
        signals.append("分歧转一致:缩量回调后放量上涨")
        score += 3
    
    # 信号2：横盘放量突破（平台整理后启动）
    if abs(change_3d) < 3 and vol_ratio > 1.5 and change_1d > 3:
        signals.append("分歧转一致:横盘后放量突破")
        score += 3
    
    # 信号3：回调到支撑位后反弹（回踩不破MA20）
    if pullback < 8 and factors.get("above_ma20", False) and change_1d > 2:
        signals.append("分歧转一致:回调企稳后反弹")
        score += 2
    
    # 信号4：ICU多头排列+鳄鱼张嘴（趋势确认）
    if factors.get("icu_bullish", False) and factors.get("alligator_eating", False):
        signals.append("趋势确认:ICU多头+鳄鱼张嘴")
        score += 2
    
    return {
        "detected": score >= 3,
        "score": score,
        "signals": signals,
        "summary": f"分歧转一致信号{'✅' if score>=3 else '❌'} (强度{score}/10)"
    }


# ============ 风控审查（TradingAgents Risk Manager启发）============
def risk_audit(factors, bull_score, bear_score):
    """风控角色对辩论结果做二次审查
    
    TradingAgents中Risk Management Team对交易员决策做三档审查。
    我们这里做两件事：
    1. 用新因子复核辩论结果是否合理
    2. 给出仓位建议
    """
    risks = []
    flags = []
    max_position = 100  # 满仓%
    
    # 超买检查
    rsi6 = factors.get("rsi6", 50)
    bb_pos = factors.get("bb_position", 0.5)
    if rsi6 > 80:
        flags.append(f"⚠️ RSI6={rsi6}严重超买")
        max_position = min(max_position, 30)
    elif rsi6 > 70:
        flags.append(f"⚠️ RSI6={rsi6}接近超买")
        max_position = min(max_position, 50)
    
    # 布林带超界
    if bb_pos > 0.9:
        flags.append(f"⚠️ 价格在布林上轨(位置{bb_pos})")
        max_position = min(max_position, 30)
    elif bb_pos < 0.1:
        flags.append(f"✅ 价格在布林下轨(位置{bb_pos})，低吸机会")
    
    # 波动率检查
    change = abs(factors.get("change_pct", 0))
    if change > 7:
        flags.append(f"⚠️ 当日波动{change}%过大，建议轻仓")
        max_position = min(max_position, 20)
    
    # 多空对比检查——如果多头靠十几个信号堆到高分，但空头因素也很足
    diff = bull_score - bear_score
    if abs(diff) <= 2:
        flags.append("⚠️ 多空分歧大，建议等信号确认再加仓")
        max_position = min(max_position, 30)
    
    # ADX弱趋势
    adx = factors.get("adx_signal", "")
    if adx == "弱趋势":
        flags.append("⚠️ ADX弱趋势，当前无明确方向")
        max_position = min(max_position, 40)
    
    # 分歧转一致——如果检测到，反倒可以加仓
    div = detect_divergence_to_consensus(factors)
    if div["detected"]:
        flags.append(f"✅ 分歧转一致信号(强度{div['score']})")
        max_position = max(max_position, 60)  # 可以适当提高
    
    # 最终风险等级
    if max_position >= 70:
        risk_level = "低"
    elif max_position >= 40:
        risk_level = "中"
    else:
        risk_level = "高"
    
    return {
        "risk_level": risk_level,
        "max_position_pct": max_position,
        "flags": flags,
        "divergence_to_consensus": div
    }

def generate_bull_case(factors, sector_data=None):
    """生成多头论点数据包"""
    if "error" in factors:
        return {"error": factors["error"]}
    
    deviation = factors.get("deviation_ma20", 0)
    
    arguments = []
    score = 0
    
    # 技术面（基础）
    if factors.get("above_ma20"):
        arguments.append("【趋势】价格位于20日均线上方，短期趋势向上")
        score += 2
    if factors.get("above_ma60"):
        arguments.append("【趋势】价格位于60日均线上方，中期趋势向上")
        score += 2
    if deviation < 10 and deviation > 0:
        arguments.append("【位置】价格紧贴均线未远离，追涨风险低")
        score += 2
    elif deviation < -5:
        arguments.append("【机会】回调至均线下方，可能回踩确认")
        score += 1
    
    # 量能
    vol_ratio = factors.get("volume_ratio", 0)
    if vol_ratio > 1.5:
        arguments.append("【量能】成交量显著放大，资金活跃")
        score += 2
    elif vol_ratio > 1:
        arguments.append("【量能】成交温和，本轮上涨有量价配合")
        score += 1
    
    # 当日表现
    change = factors.get("change_pct", 0)
    if change > 2:
        arguments.append(f"【强度】当日涨幅{change}%，强势信号")
        score += 1
    
    # 多日趋势
    trend_3d = factors.get("trend_3d", "")
    trend_5d = factors.get("trend_5d", "")
    chg_3d = factors.get("change_3d", 0)
    chg_5d = factors.get("change_5d", 0)
    pullback = factors.get("pullback_from_high", 0)
    bullish_div = factors.get("bullish_divergence", False)
    pullback_healthy = factors.get("pullback_healthy", False)
    
    if trend_3d == "上涨":
        arguments.append(f"【多日】近3日累计上涨{chg_3d}%，趋势持续")
        score += 1
    if trend_5d == "上涨":
        arguments.append(f"【多日】近5日累计上涨{chg_5d}%，中期强势")
        score += 1
    if bullish_div:
        arguments.append("【形态】缩量回调，可能是假跌破而非真弱势")
        score += 2
    if pullback_healthy and change > 0:
        arguments.append(f"【回撤】从近期高点仅回撤{pullback}%，属健康调整")
        score += 1
    
    # ========== 新增：新因子信号 ==========
    # RSI
    rsi6 = factors.get("rsi6", 50)
    if rsi6 < 30:
        arguments.append(f"【RSI】RSI6={rsi6}超卖区，反弹概率大")
        score += 2
    elif 50 <= rsi6 < 70:
        arguments.append(f"【RSI】RSI6={rsi6}偏强区，趋势健康")
        score += 1
    
    # MACD
    if factors.get("macd_bullish", False):
        arguments.append(f"【MACD】MACD金叉(柱状{factors.get('macd_histogram',0):.2f})")
        score += 2
    
    # KDJ
    if factors.get("kdj_bullish", False):
        arguments.append("【KDJ】KDJ金叉")
        score += 1
    
    # ICU均线
    if factors.get("icu_bullish", False):
        arguments.append(f"【ICU】均线多头排列(评分{factors.get('icu_score',0)})")
        score += 2
    
    # 鳄鱼张嘴
    if factors.get("alligator_eating", False):
        arguments.append("【鳄鱼线】MA5>MA10>MA20多头排列")
        score += 2
    
    # 布林带下轨
    bb_pos = factors.get("bb_position", 0.5)
    if bb_pos < 0.15:
        arguments.append(f"【布林】接近下轨(位置{bb_pos})，支撑位附近")
        score += 1
    
    return {
        "side": "bull",
        "score": min(score, 15),  # 提高满分到15，容纳新因子
        "arguments": arguments,
        "price": factors.get("price"),
        "summary": f"多头判定{min(score,15)}/15 — 共{len(arguments)}个看多依据"
    }

def generate_bear_case(factors, sector_data=None):
    """生成空头论点数据包"""
    if "error" in factors:
        return {"error": factors["error"]}
    
    deviation = factors.get("deviation_ma20", 0)
    
    arguments = []
    score = 0
    
    # 技术面（基础）
    if not factors.get("above_ma20"):
        arguments.append("【趋势】价格在20日均线下方，短期趋势偏弱")
        score += 2
    if deviation > 15:
        arguments.append(f"【位置】偏离20日线{deviation}%，追高风险较大")
        score += 2
    elif deviation > 5 and deviation <= 15:
        arguments.append(f"【位置】偏离均线{deviation}%，有一定追高风险")
        score += 1
    
    # 量能
    vol_ratio = factors.get("volume_ratio", 0)
    if vol_ratio < 0.5:
        arguments.append("【量能】成交量萎缩至日均一半以下，上攻乏力")
        score += 2
    elif vol_ratio < 0.8:
        arguments.append("【量能】量能不足，缺乏上涨动力")
        score += 1
    
    # 当日表现
    change = factors.get("change_pct", 0)
    if change < -2:
        arguments.append(f"【强度】当日跌幅{change}%，弱势")
        score += 1
    
    # ========== 新增：新因子空头信号 ==========
    # RSI超买
    rsi6 = factors.get("rsi6", 50)
    if rsi6 > 80:
        arguments.append(f"【RSI】RSI6={rsi6}严重超买，回调风险大")
        score += 2
    elif rsi6 > 70:
        arguments.append(f"【RSI】RSI6={rsi6}接近超买")
        score += 1
    
    # MACD死叉
    if not factors.get("macd_bullish", True):
        arguments.append(f"【MACD】MACD死叉(柱状{factors.get('macd_histogram',0):.2f})")
        score += 2
    
    # 布林带上轨
    bb_pos = factors.get("bb_position", 0.5)
    if bb_pos > 0.9:
        arguments.append(f"【布林】逼近上轨(位置{bb_pos})，可能回调")
        score += 2
    elif bb_pos > 0.8:
        arguments.append(f"【布林】接近上轨(位置{bb_pos})，注意压力")
        score += 1
    
    # OBV能量潮
    obv = factors.get("obv_trend", "")
    if obv == "流出":
        arguments.append("【OBV】能量潮显示资金流出")
        score += 1
    
    # 波动率
    if abs(factors.get("change_pct", 0)) > 5:
        arguments.append("【波动率】日内波动超5%，高波动市场增大不确定性")
        score += 1
    
    # 通用风险
    arguments.append("【风险】短线操作需设置明确止损位")
    score += 1
    
    return {
        "side": "bear",
        "score": min(score, 15),  # 提高满分到15
        "arguments": arguments,
        "price": factors.get("price"),
        "summary": f"空头判定{min(score,15)}/15 — 共{len(arguments)}个看空依据"
    }

def arbitrate(bull, bear, factors=None):
    """主持人裁决 + 风控审查（TradingAgents Risk Manager）"""
    bull_score = bull.get("score", 0)
    bear_score = bear.get("score", 0)
    diff = bull_score - bear_score
    
    if diff >= 4:  # 阈值从3提高到4（因子多了满分变15了）
        verdict = "多头明显占优"
        action = "推进到红队测试"
    elif diff <= -4:
        verdict = "空头明显占优"
        action = "放弃该标的"
    else:
        verdict = "分歧较大"
        action = "降低仓位、缩小止损"
    
    result = {
        "bull_score": bull_score,
        "bear_score": bear_score,
        "diff": diff,
        "verdict": verdict,
        "action": action,
        "bull_arguments": bull.get("arguments", []),
        "bear_arguments": bear.get("arguments", []),
        "bull_summary": bull.get("summary"),
        "bear_summary": bear.get("summary"),
    }
    
    # 如果传入了factors数据，追加风控审查
    if factors:
        risk_result = risk_audit(factors, bull_score, bear_score)
        result["risk_audit"] = risk_result
        
        # 如果风控等级高，覆盖action
        if risk_result["risk_level"] == "高":
            result["action"] = "风控否决:风险等级高，建议等待"
            result["verdict"] += "(风控否决)"
        elif risk_result["risk_level"] == "中" and verdict == "多头明显占优":
            result["action"] = f"轻仓试仓(建议仓位<={risk_result['max_position_pct']}%)"
        
        # 分歧转一致信号作为独立输出
        if risk_result["divergence_to_consensus"]["detected"]:
            result["divergence_to_consensus"] = risk_result["divergence_to_consensus"]
    
    return result

def debate_stock(code):
    """对单只股票执行完整的辩论流程（v2.0）
    
    TradingAgents启发：五层流程
    1. Analyst Team → 采集数据
    2. Researcher Team → 多空辩论
    3. Risk Management → 风控审查
    4. Trader → 交易建议
    5. Fund Manager → 输出报告
    """
    factors = analyze_stock_factors(code)
    if "error" in factors:
        return {"error": factors["error"]}
    
    bull = generate_bull_case(factors)
    bear = generate_bear_case(factors)
    result = arbitrate(bull, bear, factors=factors)
    
    # 附带完整因子数据
    result["factors"] = {
        "price": factors.get("price"),
        "change_pct": factors.get("change_pct"),
        "ma20": factors.get("ma20"),
        "ma5": factors.get("ma5"),
        "ma10": factors.get("ma10"),
        "ma60": factors.get("ma60"),
        "deviation_ma20": factors.get("deviation_ma20"),
        "amount_yi": factors.get("amount_yi"),
        "volume_ratio": factors.get("volume_ratio"),
        # 新因子
        "rsi6": factors.get("rsi6"),
        "rsi14": factors.get("rsi14"),
        "macd_histogram": factors.get("macd_histogram"),
        "macd_bullish": factors.get("macd_bullish"),
        "kdj_bullish": factors.get("kdj_bullish"),
        "bb_position": factors.get("bb_position"),
        "icu_bullish": factors.get("icu_bullish"),
        "alligator_eating": factors.get("alligator_eating"),
        "adx_signal": factors.get("adx_signal"),
        "obv_trend": factors.get("obv_trend"),
        # 多日趋势
        "change_3d": factors.get("change_3d"),
        "trend_3d": factors.get("trend_3d"),
        "pullback_from_high": factors.get("pullback_from_high"),
        "bullish_divergence": factors.get("bullish_divergence", False),
    }
    
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = debate_stock(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法: python3 debater.py <股票代码>")
