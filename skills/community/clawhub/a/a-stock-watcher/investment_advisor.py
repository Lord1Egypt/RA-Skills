#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能投顾模块

功能：
- 风险评估问卷
- 投资组合优化
- 止损止盈计算器
- 估值模型

⚠️ 重要声明：本模块所有功能仅供参考，不构成投资建议
"""

import math
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# ============== 风险评估 ==============
RISK_QUESTIONS = [
    {
        "question": "您的投资经验是？",
        "options": [
            {"text": "完全没有经验", "score": 1},
            {"text": "少量经验（<1 年）", "score": 2},
            {"text": "有一定经验（1-3 年）", "score": 3},
            {"text": "经验丰富（3-5 年）", "score": 4},
            {"text": "非常专业（>5 年）", "score": 5}
        ]
    },
    {
        "question": "您的投资目标是？",
        "options": [
            {"text": "保本为主，接受低收益", "score": 1},
            {"text": "稳健增值，接受小幅波动", "score": 2},
            {"text": "平衡收益和风险", "score": 3},
            {"text": "追求较高收益，接受较大波动", "score": 4},
            {"text": "追求最大收益，不怕高风险", "score": 5}
        ]
    },
    {
        "question": "如果投资下跌 20%，您会？",
        "options": [
            {"text": "立即卖出止损", "score": 1},
            {"text": "卖出部分，降低风险", "score": 2},
            {"text": "持有观望", "score": 3},
            {"text": "适当加仓", "score": 4},
            {"text": "大量加仓，摊低成本", "score": 5}
        ]
    },
    {
        "question": "您的投资期限是？",
        "options": [
            {"text": "短期（<3 个月）", "score": 1},
            {"text": "中短期（3-12 个月）", "score": 2},
            {"text": "中期（1-3 年）", "score": 3},
            {"text": "中长期（3-5 年）", "score": 4},
            {"text": "长期（>5 年）", "score": 5}
        ]
    },
    {
        "question": "您可接受的最大回撤是？",
        "options": [
            {"text": "<5%", "score": 1},
            {"text": "5%-10%", "score": 2},
            {"text": "10%-20%", "score": 3},
            {"text": "20%-30%", "score": 4},
            {"text": ">30%", "score": 5}
        ]
    }
]

RISK_PROFILES = {
    (1, 10): {
        "level": "保守型",
        "description": "风险承受能力较低，建议以保本为主",
        "allocation": {
            "债券": 70,
            "货币基金": 20,
            "股票": 5,
            "另类投资": 5
        },
        "advice": "建议以固定收益类产品为主，股票投资不超过 10%"
    },
    (11, 15): {
        "level": "稳健型",
        "description": "风险承受能力中等偏低，追求稳健增值",
        "allocation": {
            "债券": 50,
            "货币基金": 10,
            "股票": 30,
            "另类投资": 10
        },
        "advice": "建议股债配比 3:7，注重资产配置平衡"
    },
    (16, 20): {
        "level": "平衡型",
        "description": "风险承受能力中等，平衡收益和风险",
        "allocation": {
            "债券": 40,
            "货币基金": 5,
            "股票": 50,
            "另类投资": 5
        },
        "advice": "建议股债配比 5:5，可适当配置行业龙头"
    },
    (21, 24): {
        "level": "积极型",
        "description": "风险承受能力较高，追求较高收益",
        "allocation": {
            "债券": 20,
            "货币基金": 5,
            "股票": 70,
            "另类投资": 5
        },
        "advice": "建议股债配比 7:3，可关注成长股和 sector 轮动"
    },
    (25, 30): {
        "level": "激进型",
        "description": "风险承受能力很高，追求最大收益",
        "allocation": {
            "债券": 10,
            "货币基金": 0,
            "股票": 85,
            "另类投资": 5
        },
        "advice": "建议高仓位股票，可配置部分高风险标的"
    }
}


def assess_risk_profile(answers: List[int]) -> Dict:
    """
    评估风险画像
    
    Args:
        answers: 用户答案列表（每题的得分）
    
    Returns:
        风险画像字典
    """
    total_score = sum(answers)
    
    # 找到对应的风险等级
    profile = None
    for (min_score, max_score), p in RISK_PROFILES.items():
        if min_score <= total_score <= max_score:
            profile = p
            break
    
    if not profile:
        profile = RISK_PROFILES[(11, 15)]  # 默认稳健型
    
    return {
        "total_score": total_score,
        "max_score": len(RISK_QUESTIONS) * 5,
        "level": profile["level"],
        "description": profile["description"],
        "allocation": profile["allocation"],
        "advice": profile["advice"],
        "assessment_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def format_risk_assessment(assessment: Dict) -> str:
    """
    格式化风险评估报告
    
    Args:
        assessment: 评估结果
    
    Returns:
        格式化的报告
    """
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 投资风险画像评估
━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 风险评估得分：{assessment['total_score']}/{assessment['max_score']}

🎯 风险等级：{assessment['level']}
{assessment['description']}

📋 建议资产配置:
"""
    
    for asset, ratio in assessment['allocation'].items():
        bar = '█' * (ratio // 5)
        report += f"  {asset}: {ratio}% {bar}\n"
    
    report += f"""
💡 投资建议:
{assessment['advice']}

⏰ 评估时间：{assessment['assessment_time']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示：本评估仅供参考，不构成投资建议
市场有风险，投资需谨慎
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report


# ============== 止损止盈计算器 ==============
def calculate_stop_loss_stop_profit(
    entry_price: float,
    current_price: float,
    volatility: float = 2.0,
    risk_reward_ratio: float = 2.0,
    position_size: float = 10000
) -> Dict:
    """
    计算止损止盈位
    
    Args:
        entry_price: 入场价格
        current_price: 当前价格
        volatility: 波动率 (%), 默认 2%
        risk_reward_ratio: 风险收益比，默认 2:1
        position_size: 仓位金额
    
    Returns:
        计算结果字典
    """
    # 基于波动率计算止损位
    stop_loss_pct = volatility * 1.5  # 1.5 倍波动率作为止损
    stop_loss_price = entry_price * (1 - stop_loss_pct / 100)
    
    # 基于风险收益比计算止盈位
    stop_profit_pct = stop_loss_pct * risk_reward_ratio
    stop_profit_price = entry_price * (1 + stop_profit_pct / 100)
    
    # 计算盈亏金额
    if current_price > entry_price:
        current_profit = (current_price - entry_price) * (position_size / entry_price)
        is_profit = True
    else:
        current_profit = (entry_price - current_price) * (position_size / entry_price)
        is_profit = False
    
    # 止损金额
    stop_loss_amount = (entry_price - stop_loss_price) * (position_size / entry_price)
    # 止盈金额
    stop_profit_amount = (stop_profit_price - entry_price) * (position_size / entry_price)
    
    # 当前位置建议
    if current_price <= stop_loss_price:
        action = "⚠️ 已触及止损位，建议考虑止损"
    elif current_price >= stop_profit_price:
        action = "✅ 已触及止盈位，建议考虑止盈"
    elif current_price > entry_price * 1.05:
        action = "📈 盈利中，建议提高止损位保护利润"
    elif current_price < entry_price * 0.95:
        action = "📉 亏损中，建议严格执行止损纪律"
    else:
        action = "➖ 正常波动，继续持有观察"
    
    return {
        "entry_price": entry_price,
        "current_price": current_price,
        "stop_loss_price": stop_loss_price,
        "stop_loss_pct": stop_loss_pct,
        "stop_profit_price": stop_profit_price,
        "stop_profit_pct": stop_profit_pct,
        "stop_loss_amount": stop_loss_amount,
        "stop_profit_amount": stop_profit_amount,
        "current_profit": current_profit,
        "is_profit": is_profit,
        "risk_reward_ratio": risk_reward_ratio,
        "action": action
    }


def format_stop_loss_report(calculation: Dict) -> str:
    """
    格式化止损止盈报告
    
    Args:
        calculation: 计算结果
    
    Returns:
        格式化的报告
    """
    profit_emoji = "📈" if calculation["is_profit"] else "📉"
    profit_sign = "+" if calculation["is_profit"] else ""
    
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 止损止盈计算
━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 持仓信息:
  入场价：¥{calculation['entry_price']:.2f}
  当前价：¥{calculation['current_price']:.2f}
  当前盈亏：{profit_emoji} ¥{profit_sign}{calculation['current_profit']:.2f}

🛑 止损位:
  价格：¥{calculation['stop_loss_price']:.2f}
  幅度：-{calculation['stop_loss_pct']:.1f}%
  金额：-¥{calculation['stop_loss_amount']:.2f}

🎯 止盈位:
  价格：¥{calculation['stop_profit_price']:.2f}
  幅度：+{calculation['stop_profit_pct']:.1f}%
  金额：+¥{calculation['stop_profit_amount']:.2f}

📐 风险收益比：1:{calculation['risk_reward_ratio']}

💡 操作建议:
{calculation['action']}

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示：以上计算仅供参考，不构成投资建议
请根据个人风险承受能力调整参数
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report


# ============== 估值模型 ==============
def pe_relative_valuation(
    stock_pe: float,
    industry_pe: float,
    market_pe: float,
    growth_rate: float = 0
) -> Dict:
    """
    PE 相对估值法
    
    Args:
        stock_pe: 个股 PE
        industry_pe: 行业平均 PE
        market_pe: 市场平均 PE
        growth_rate: 预期增长率 (%)
    
    Returns:
        估值结果
    """
    # 与行业对比
    vs_industry = (stock_pe - industry_pe) / industry_pe * 100
    
    # 与市场对比
    vs_market = (stock_pe - market_pe) / market_pe * 100
    
    # PEG 估值（考虑增长）
    peg = stock_pe / growth_rate if growth_rate > 0 else None
    
    # 估值判断
    if vs_industry < -20:
        valuation_vs_industry = "低估"
    elif vs_industry > 20:
        valuation_vs_industry = "高估"
    else:
        valuation_vs_industry = "合理"
    
    if peg and peg < 1:
        peg_assessment = "低估（PEG<1）"
    elif peg and peg > 2:
        peg_assessment = "高估（PEG>2）"
    elif peg:
        peg_assessment = "合理"
    else:
        peg_assessment = "N/A"
    
    return {
        "stock_pe": stock_pe,
        "industry_pe": industry_pe,
        "market_pe": market_pe,
        "vs_industry": vs_industry,
        "vs_market": vs_market,
        "growth_rate": growth_rate,
        "peg": peg,
        "valuation_vs_industry": valuation_vs_industry,
        "peg_assessment": peg_assessment
    }


def format_valuation_report(valuation: Dict, stock_name: str = "") -> str:
    """
    格式化估值报告
    
    Args:
        valuation: 估值结果
        stock_name: 股票名称
    
    Returns:
        格式化的报告
    """
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PE 相对估值分析 {stock_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 市盈率对比:
  个股 PE: {valuation['stock_pe']:.2f}
  行业 PE: {valuation['industry_pe']:.2f}
  市场 PE: {valuation['market_pe']:.2f}

📊 相对估值:
  vs 行业：{valuation['vs_industry']:+.1f}% ({valuation['valuation_vs_industry']})
  vs 市场：{valuation['vs_market']:+.1f}%

📈 成长性估值 (PEG):
  预期增长率：{valuation['growth_rate']:.1f}%
  PEG: {valuation['peg']:.2f}
  评估：{valuation['peg_assessment']}

💡 估值结论:
"""
    
    if valuation['valuation_vs_industry'] == "低估" and (valuation['peg'] and valuation['peg'] < 1.5):
        conclusion = "✅ 相对行业和成长性均显示低估，值得关注"
    elif valuation['valuation_vs_industry'] == "高估" and (valuation['peg'] and valuation['peg'] > 1.5):
        conclusion = "⚠️ 估值偏高，建议谨慎"
    else:
        conclusion = "➖ 估值处于合理区间"
    
    report += f"{conclusion}\n"
    
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示：估值模型仅供参考，不构成投资建议
实际投资需综合考虑多方面因素
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report


# ============== 投资组合优化 ==============
def calculate_portfolio_optimization(
    assets: List[Dict],
    risk_free_rate: float = 0.03
) -> Dict:
    """
    简化的投资组合优化（基于现代投资组合理论）
    
    Args:
        assets: 资产列表，每项包含 {name, expected_return, volatility, correlation}
        risk_free_rate: 无风险利率
    
    Returns:
        优化结果
    """
    n = len(assets)
    
    # 简化计算：等权重组合作为基准
    equal_weight = 1.0 / n
    
    # 计算等权重组合的预期收益和风险
    portfolio_return = sum(a['expected_return'] * equal_weight for a in assets)
    
    # 简化风险计算（忽略相关性）
    portfolio_volatility = math.sqrt(
        sum((a['volatility'] * equal_weight) ** 2 for a in assets)
    )
    
    # 夏普比率
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility if portfolio_volatility > 0 else 0
    
    # 简化的最优配置（高风险高收益资产降低权重）
    optimal_weights = []
    total_inverse_vol = sum(1/a['volatility'] for a in assets if a['volatility'] > 0)
    
    for a in assets:
        if a['volatility'] > 0:
            weight = (1/a['volatility']) / total_inverse_vol
        else:
            weight = equal_weight
        optimal_weights.append({
            'name': a['name'],
            'weight': weight * 100
        })
    
    # 排序
    optimal_weights.sort(key=lambda x: x['weight'], reverse=True)
    
    return {
        "assets": [a['name'] for a in assets],
        "equal_weight_portfolio": {
            "return": portfolio_return * 100,
            "volatility": portfolio_volatility * 100,
            "sharpe_ratio": sharpe_ratio
        },
        "optimal_allocation": optimal_weights,
        "risk_free_rate": risk_free_rate * 100
    }


def format_portfolio_optimization(optimization: Dict) -> str:
    """
    格式化投资组合优化报告
    
    Args:
        optimization: 优化结果
    
    Returns:
        格式化的报告
    """
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 投资组合优化建议
━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 等权重组合表现:
  预期年化收益：{optimization['equal_weight_portfolio']['return']:.1f}%
  预期波动率：{optimization['equal_weight_portfolio']['volatility']:.1f}%
  夏普比率：{optimization['equal_weight_portfolio']['sharpe_ratio']:.2f}

💡 优化配置建议 (风险平价):
"""
    
    for i, asset in enumerate(optimization['optimal_allocation'], 1):
        bar = '█' * int(asset['weight'] / 5)
        report += f"  {i}. {asset['name']}: {asset['weight']:.1f}% {bar}\n"
    
    report += f"""
📐 无风险利率假设：{optimization['risk_free_rate']:.1f}%

💡 配置思路:
  • 低波动资产获得更高权重（风险平价）
  • 分散配置降低整体风险
  • 定期再平衡维持目标配置

━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 风险提示：模型基于历史数据，不保证未来表现
实际投资需考虑个人情况和市场变化
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report


# ============== 测试 ==============
if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    print("=" * 60)
    print("智能投顾模块测试")
    print("=" * 60)
    
    # 测试风险评估
    print("\n[测试] 风险评估")
    test_answers = [3, 3, 3, 3, 3]  # 平衡型答案
    assessment = assess_risk_profile(test_answers)
    print(format_risk_assessment(assessment))
    
    # 测试止损止盈
    print("\n[测试] 止损止盈计算")
    calc = calculate_stop_loss_stop_profit(
        entry_price=10.0,
        current_price=10.5,
        volatility=2.5,
        position_size=10000
    )
    print(format_stop_loss_report(calc))
    
    # 测试估值
    print("\n[测试] PE 相对估值")
    valuation = pe_relative_valuation(
        stock_pe=15.0,
        industry_pe=20.0,
        market_pe=18.0,
        growth_rate=15.0
    )
    print(format_valuation_report(valuation, "测试股票"))
    
    # 测试投资组合优化
    print("\n[测试] 投资组合优化")
    assets = [
        {"name": "股票 A", "expected_return": 0.12, "volatility": 0.25},
        {"name": "股票 B", "expected_return": 0.10, "volatility": 0.20},
        {"name": "债券", "expected_return": 0.05, "volatility": 0.05},
        {"name": "黄金", "expected_return": 0.06, "volatility": 0.15}
    ]
    optimization = calculate_portfolio_optimization(assets)
    print(format_portfolio_optimization(optimization))
