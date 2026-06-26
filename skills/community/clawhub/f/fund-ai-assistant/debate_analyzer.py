#!/usr/bin/env python3
"""
多智能体辩论框架 for 基金分析

基于 FinGenius 多智能体博弈架构改编
AstrBot 原项目: astrbot_plugin_fund_analyzer

Phase 1: 6个AI角色并行独立分析（6次LLM调用）
Phase 2: 多方辩手综合看涨论据（1次LLM调用）
Phase 3: 空方辩手综合看跌论据（1次LLM调用）
Phase 4: 裁判运用博弈论综合裁定（1次LLM调用）
"""

import json
import os
import re
import sys
import time

from llm import get_llm_config, call_llm as _llm_call
from dataclasses import dataclass, field
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fund_api import fetch_otc_fund_history, fetch_otc_fund_valuation
from technical import analyze_fund

# ============ MiniMax LLM 调用 ============

# ============ 6个Agent Prompts ============

SYSTEM_PROMPTS = {

    "sentiment": """## 强制规则
你必须给出一个明确的方向判断，不能填中性。当多空信号数量相等时，选择你判断概率更高的那个方向。
你是「舆情与市场情绪分析师」，专注于基金/黄金/债券的市场情绪量化分析。

## 分析框架
- 解读宏观政策（LPR/降息/美联储）对所分析资产的短期情绪影响
- 量化市场恐慌/贪婪信号
- 分析地缘政治、美元指数、人民币汇率对黄金/债券的情绪驱动

## 输出格式（必须严格遵循，方向判断只能选看涨或看跌）
【舆情分析】
情绪判断：[极度恐慌/恐慌/谨慎/乐观/贪婪]（不能选中性）
核心驱动事件：...
利多信号：🔺...（每条一行）
利空信号：🔻...（每条一行）
情绪拐点：是否接近反转...
方向判断：看涨 或 看跌（二选一，不能中性）
信心度：X/100""",

    "risk": """## 强制规则
你必须给出一个明确的方向判断，不能填中性。当多空风险对等时，选择你判断概率更高的那个方向。
你是「风险控制分析师」，专注于基金/黄金/债券的风险量化评估。

## 分析框架
- VaR（95%置信度下单日最大亏损）
- 最大回撤（历史最大跌幅）
- 年化波动率
- 宏观风险（美联储/人民币汇率/地缘冲突）

## 输出格式
【风险分析】
量化风险指标：
  VaR(95%): X%
  最大回撤: X%
  年化波动率: X%
宏观风险：...（利多/利空）
季节性风险：...
最坏情景：可能跌X%
风险等级：[低/中/高]
方向判断：看涨 或 看跌（二选一，不能中性）
信心度：X/100""",

    "technical": """## 强制规则
你必须给出一个明确的方向判断，不能填中性。当看涨看跌信号数量相等时，选择你判断概率更高的那个方向。
你是「技术分析专家」，专注于MACD/RSI/布林带/均线系统的综合研判。

## 分析框架
- MACD：DIF/DEA位置，金叉/死叉、柱状图趋势、背离
- RSI：超买超卖、多周期共振
- 布林带：价格与上下轨关系、支撑阻力位
- 均线：多头/空头排列

## 输出格式
【技术分析】
MACD信号：...
RSI信号：...
布林带信号：...
均线系统：...
关键支撑位：X元
关键阻力位：X元
看涨信号：...（每条一行）
看跌信号：...（每条一行）
趋势评分：X/100
方向判断：看涨 或 看跌（二选一，不能中性）
信心度：X/100""",

    "momentum": """## 强制规则
你必须给出一个明确的方向判断，不能填中性。当多空动量对等时，选择你判断概率更高的那个方向。
你是「动量与趋势分析师」，专注于基金/黄金的价格动量与趋势强度评估。

## 分析框架
- 短期/中期/长期动量方向（近1周/1月/3月涨跌）
- 动量加速度（趋势在加速还是减速）
- 趋势持续性评估

## 输出格式
【动量分析】
短期动量（1周）：X% → [强势/弱势/中性]
中期动量（1月）：X% → [强势/弱势/中性]
长期动量（3月）：X% → [强势/弱势/中性]
动量加速度：[加速/减速/平稳]
趋势评级：[强趋势/弱趋势/震荡]
方向判断：看涨 或 看跌（二选一，不能中性）
信心度：X/100""",

    "ratio": """## 强制规则
你必须给出一个明确的方向判断，不能填中性。当风险收益多空对等时，选择你判断概率更高的那个方向。
你是「风险收益比分析师」，专注于基金的风险收益特征量化评估。

## 分析框架
- 夏普比率：>1为优秀，>2为极佳
- 索提诺比率：只考虑下行风险，>2为优秀
- 卡玛比率：年化收益/最大回撤，>1为可接受

## 输出格式
【风险收益分析】
夏普比率：X → [说明]
索提诺比率：X → [说明]
卡玛比率：X → [说明]
综合性价比：[优秀/良好/一般/较差]
vs 无风险收益(3%)：[跑赢/跑输]
风险收益评级：[极高/高/中/低]
方向判断：看涨 或 看跌（二选一，不能中性）
信心度：X/100""",

    "macro": """## 强制规则
你必须给出一个明确的方向判断，不能填中性。当多空宏观因素对等时，选择你判断概率更高的那个方向。
你是「宏观策略分析师」，专注于全球宏观经济周期与资产配置视角的基金分析。

## 分析框架
- 美联储货币政策对黄金/债券的影响
- 人民币汇率对QDII基金/黄金ETF的影响
- 国内LPR利率对债券基金的影响

## 输出格式
【宏观策略分析】
美联储周期：[宽松/紧缩/观望]
人民币汇率：[升值压力/贬值压力/中性]
国内货币周期：[宽松/中性/紧缩]
大类资产偏好：[黄金/债券/股票]
宏观评级：[利多/利空/中性]
方向判断：看涨 或 看跌（二选一，不能中性）
信心度：X/100""",
}


BULL_DEBATER_PROMPT = """你是「多方辩手」，需要综合以下6位分析师的看涨论据，用最有力的逻辑说服裁判支持看涨。

请整理所有分析师的看涨信号，合并重复论点，排出优先级，给出最有力的3个看涨理由。只引用看涨论据，不要提及空方观点。"""

BEAR_DEBATER_PROMPT = """你是「空方辩手」，需要综合以下6位分析师的看跌论据，用最有力的逻辑说服裁判支持看跌。

请整理所有分析师的看跌信号，合并重复论点，排出优先级，给出最有力的3个看跌理由。只引用看跌论据，不要提及多方观点。"""

JUDGE_PROMPT = """你是「裁判」，运用博弈论对多空双方进行最终裁定。

## 博弈论框架
- 评估多空双方论据的信息量（是否是新信息？还是已经被市场定价？）
- 评估多空论据的可信度（历史规律 vs 偶发事件）
- 纳什均衡分析：当前价格是否已经充分反映了多空双方的信息？
- 信息不对称分析：哪方掌握的信息更有价值？

## 输出格式
【裁判最终裁定】
多方最强论据：...
空方最强论据：...
博弈论分析：...
综合裁定：[强烈看涨/看涨/中性/看跌/强烈看跌]
多方胜率：X%
空方胜率：X%
最终操作建议：[强烈买入/买入/持有/观望/减持]
止盈参考位：X元（+X%）
止损参考位：X元（-X%）"""


# ============ 数据收集 ============

def collect_agent_data(fund_code: str, days: int = 60) -> Optional[dict]:
    """收集各Agent需要的分析数据"""
    valuation = fetch_otc_fund_valuation(fund_code)
    # 尝试60天，不够则用更少（基金历史可能不足），网络抖动时多重试
    history = None
    for d in [60, 45, 30]:
        try:
            h = fetch_otc_fund_history(fund_code, days=d)
            if h and len(h) >= 10:
                history = h
                break
        except Exception:
            continue

    if not valuation or not history:
        return None

    result = analyze_fund(fund_code, history)
    prices = result.get("prices", [])

    nav = valuation.get("nav", 0)
    change = valuation.get("change", 0)
    name = valuation.get("name", fund_code)

    def period_ret(d: int) -> Optional[float]:
        if len(prices) <= d or d >= len(prices):
            return None
        try:
            return round((prices[0] - prices[d]) / prices[d] * 100, 2)
        except (IndexError, ZeroDivisionError):
            return None

    return {
        "fund_name": name,
        "fund_code": fund_code,
        "nav": nav,
        "latest_change": change,
        "rsi14": result.get("rsi14"),
        "macd_dif": result.get("macd_dif"),
        "macd_dea": result.get("macd_dea"),
        "macd_hist": result.get("macd_hist"),
        "boll_upper": result.get("boll_upper"),
        "boll_middle": result.get("boll_middle"),
        "boll_lower": result.get("boll_lower"),
        "ma5": result.get("ma5"),
        "ma10": result.get("ma10"),
        "ma20": result.get("ma20"),
        "trend": result.get("trend"),
        "volatility": result.get("volatility"),
        "max_drawdown": result.get("max_drawdown"),
        "sharpe_ratio": result.get("sharpe_ratio"),
        "var_95": result.get("var_95"),
        "sortino_ratio": result.get("sortino_ratio"),
        "calmar_ratio": result.get("calmar_ratio"),
        "return_1w": period_ret(5),
        "return_1m": period_ret(22),
        "return_3m": period_ret(66),
        "return_6m": period_ret(126),
        "return_1y": period_ret(252),
        "prices": prices,
    }


def format_agent_data(data: dict) -> str:
    """将数据格式化为各Agent可读的文本"""
    if not data:
        return "数据获取失败"

    return f"""基金：{data['fund_name']}（{data['fund_code']}）
当前净值：{data['nav']}（{'+' if data['latest_change'] >= 0 else ''}{data['latest_change']}%）

【技术指标】
RSI(14): {data['rsi14']}
MACD：DIF={data['macd_dif']} DEA={data['macd_dea']} 柱状图={data['macd_hist']}
布林带：上轨={data['boll_upper']} 中轨={data['boll_middle']} 下轨={data['boll_lower']}
MA5={data['ma5']} MA10={data['ma10']} MA20={data['ma20']}
趋势：{data['trend']}

【收益指标】
近1周：{data['return_1w']}%
近1月：{data['return_1m']}%
近3月：{data['return_3m']}%
近6月：{data['return_6m']}%
近1年：{data['return_1y']}%

【风险指标】
VaR(95%): {data['var_95']}%
最大回撤: {data['max_drawdown']}%
年化波动率: {data['volatility']}%
夏普比率: {data['sharpe_ratio']}
索提诺比率: {data['sortino_ratio']}
卡玛比率: {data['calmar_ratio']}"""


# ============ 结果结构 ============

@dataclass
class AgentResult:
    agent_id: str
    agent_name: str
    agent_emoji: str
    analysis: str
    direction: str = "中性"
    confidence: float = 50.0


@dataclass
class DebateResult:
    fund_code: str
    fund_name: str
    nav: float
    agent_reports: list = field(default_factory=list)
    bull_argument: str = ""
    bear_argument: str = ""
    judge_verdict: str = ""
    final_direction: str = "中性"
    confidence: float = 50.0
    bull_win_rate: float = 50.0
    bear_win_rate: float = 50.0
    total_time: float = 0.0


def parse_direction(text: str) -> tuple:
    """
    从分析文本中提取方向和信心度
    策略：数信号条数，而非简单关键字匹配
    """
    import re as re_module

    # 数看涨/看跌信号条数
    bullish_count = len(re_module.findall(r'看涨信号[：:]\s*\S', text))
    bearish_count = len(re_module.findall(r'看跌信号[：:]\s*\S', text))

    # 信号强度指示符
    strong_bull = text.count('🔺') + text.count('强烈看涨') * 2
    strong_bear = text.count('🔻') + text.count('强烈看跌') * 2
    bullish_count += strong_bull
    bearish_count += strong_bear

    # 显式方向词（权重更高）
    explicit_bull = text.count('方向判断：看涨') + text.count('方向判断：强烈看涨')
    explicit_bear = text.count('方向判断：看跌') + text.count('方向判断：强烈看跌')

    net = bullish_count + explicit_bull - bearish_count - explicit_bear

    if net >= 3:
        direction = "看涨"
    elif net <= -3:
        direction = "看跌"
    elif net > 0:
        direction = "中性偏多"
    elif net < 0:
        direction = "中性偏空"
    else:
        direction = "中性"

    # 信心度：基线50 + 信号倾向调整
    m = re_module.search(r'信心[度：:]\s*([0-9]+)', text)
    confidence = float(m.group(1)) if m else (50 + net * 5)
    confidence = max(30, min(95, confidence))  # 限制在30-95范围
    return direction, confidence


# ============ 主流程 ============

def run_debate(fund_code: str) -> DebateResult:
    """执行完整的多智能体辩论分析"""
    model, api_key = get_llm_config()
    if not model or not api_key:
        print("=" * 50)
        print("【错误】LLM_MODEL 或 LLM_API_KEY 未配置")
        print("请配置环境变量后重试：")
        print("  export LLM_MODEL=your_model_name")
        print("  export LLM_API_KEY=your_api_key")
        print("=" * 50)
        sys.exit(1)

    print("开始采集数据...")
    data = collect_agent_data(fund_code, days=252)
    if not data:
        return DebateResult(fund_code=fund_code, fund_name="数据获取失败", nav=0)

    result = DebateResult(
        fund_code=fund_code,
        fund_name=data["fund_name"],
        nav=data["nav"],
    )

    agent_data_text = format_agent_data(data)
    start_time = time.time()

    agent_names = {
        "sentiment": "舆情分析师",
        "risk": "风控分析师",
        "technical": "技术分析师",
        "momentum": "动量分析师",
        "ratio": "风险收益分析师",
        "macro": "宏观策略分析师",
    }
    agent_emojis = {
        "sentiment": "📰",
        "risk": "🛡️",
        "technical": "📊",
        "momentum": "⚡",
        "ratio": "📈",
        "macro": "🌍",
    }

    print("Phase 1: 6位分析师独立分析...")
    bull_signals = []
    bear_signals = []

    for agent_id, prompt in SYSTEM_PROMPTS.items():
        print(f"  -> {agent_names[agent_id]}...", end=" ", flush=True)
        t0 = time.time()
        analysis = _llm_call(model, f"{prompt}\n\n{agent_data_text}", api_key)
        elapsed = time.time() - t0
        direction, confidence = parse_direction(analysis)

        report = AgentResult(
            agent_id=agent_id,
            agent_name=agent_names[agent_id],
            agent_emoji=agent_emojis[agent_id],
            analysis=analysis,
            direction=direction,
            confidence=confidence,
        )
        result.agent_reports.append(report)

        if direction in ("看涨", "强烈看涨"):
            bull_signals.append(f"【{agent_names[agent_id]}】{analysis[:300]}")
        elif direction in ("看跌", "强烈看跌"):
            bear_signals.append(f"【{agent_names[agent_id]}】{analysis[:300]}")

        print(f"{direction} ({confidence:.0f}%) {elapsed:.1f}秒")

    # Phase 2
    print("Phase 2: 多方辩手整合...")
    bull_text = "\n\n".join(bull_signals) if bull_signals else "无明确看涨信号"
    result.bull_argument = _llm_call(model, f"{BULL_DEBATER_PROMPT}\n\n{bull_text}", api_key)
    result.bull_win_rate = parse_direction(result.bull_argument)[1]

    # Phase 3
    print("Phase 3: 空方辩手整合...")
    bear_text = "\n\n".join(bear_signals) if bear_signals else "无明确看跌信号"
    result.bear_argument = _llm_call(model, f"{BEAR_DEBATER_PROMPT}\n\n{bear_text}", api_key)
    result.bear_win_rate = parse_direction(result.bear_argument)[1]

    # Phase 4
    print("Phase 4: 裁判裁定...")
    judge_input = (
        f"多方辩手论据：\n{result.bull_argument}\n\n"
        f"空方辩手论据：\n{result.bear_argument}\n\n"
        f"标的：{data['fund_name']}（{fund_code}）\n当前价格：{data['nav']}"
    )
    result.judge_verdict = _llm_call(model, f"{JUDGE_PROMPT}\n\n{judge_input}", api_key)
    result.final_direction, result.confidence = parse_direction(result.judge_verdict)

    result.total_time = time.time() - start_time
    print(f"辩论完成，耗时{result.total_time:.1f}秒")
    return result


def format_debate_report(result: DebateResult) -> str:
    """格式化辩论报告"""
    lines = []
    lines.append(f"=== 多智能体辩论分析 === {result.fund_name}（{result.fund_code}）")
    lines.append(f"当前价格：{result.nav}")

    lines.append("")
    lines.append("【Phase 1】六位分析师独立判断")
    for r in result.agent_reports:
        emoji = "+" if r.direction in ("看涨", "强烈看涨") else ("-" if r.direction in ("看跌", "强烈看跌") else "=")
        lines.append(f"  [{emoji}] {r.agent_emoji}{r.agent_name}：{r.direction}（{r.confidence:.0f}%）")

    bull_count = sum(1 for r in result.agent_reports if r.direction in ("看涨", "强烈看涨"))
    bear_count = sum(1 for r in result.agent_reports if r.direction in ("看跌", "强烈看跌"))
    lines.append(f"  投票：+{bull_count} vs -{bear_count}")

    lines.append("")
    lines.append("【Phase 2】多方辩手论据")
    lines.append(result.bull_argument[:600] if result.bull_argument else "（无）")

    lines.append("")
    lines.append("【Phase 3】空方辩手论据")
    lines.append(result.bear_argument[:600] if result.bear_argument else "（无）")

    lines.append("")
    lines.append("【Phase 4】裁判最终裁定")
    lines.append(result.judge_verdict)

    emoji = "+" if result.final_direction in ("看涨", "强烈看涨") else ("-" if result.final_direction in ("看跌", "强烈看跌") else "=")
    lines.append(f"\n最终裁定：[{emoji}] {result.final_direction}（{result.confidence:.0f}%）")
    lines.append("耗时：{:.0f}秒".format(result.total_time))

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 debate_analyzer.py <基金代码>")
        print("示例: python3 debate_analyzer.py 000001")
        sys.exit(1)

    # 检查 LLM 配置
    model, api_key = get_llm_config()
    if not model or not api_key:
        print("=" * 50)
        print("【错误】LLM 模型未配置")
        print("请配置以下环境变量：")
        print("  export LLM_MODEL=your_model_name")
        print("  export LLM_API_KEY=your_api_key")
        print("=" * 50)
        sys.exit(1)

    fund_code = sys.argv[1].strip()
    result = run_debate(fund_code)
    print("\n" + format_debate_report(result))
