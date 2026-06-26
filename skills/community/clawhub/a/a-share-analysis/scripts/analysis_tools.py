#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股分析工具函数库
包含：评分计算、趋势判断、数据格式化等工具函数
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json


def calculate_composite_score(data: Dict) -> float:
    """
    计算综合评分 (0-10)
    
    评分维度:
    - 技术面：±2 分
    - 情绪面：±1.5 分
    - 价格表现：±1 分
    - 基本面：±1 分（如有）
    """
    score = 5.0  # 基础分
    
    # 技术面 (±2)
    technical = data.get("technical", {})
    if technical.get("signal") == "bullish":
        score += 1.5
    elif technical.get("signal") == "bearish":
        score -= 1.5
    
    if technical.get("trend") == "bullish":
        score += 0.5
    elif technical.get("trend") == "bearish":
        score -= 0.5
    
    # 情绪面 (±1.5)
    sentiment = data.get("news_sentiment", {})
    sentiment_score = sentiment.get("avg_sentiment_score", 0.5)
    score += (sentiment_score - 0.5) * 3
    
    # 价格表现 (±1)
    change = data.get("change_percent", 0)
    if change > 5:
        score += 1.0
    elif change > 3:
        score += 0.5
    elif change < -5:
        score -= 1.0
    elif change < -3:
        score -= 0.5
    
    # 基本面 (±1)
    fundamental = data.get("fundamental", {})
    if fundamental:
        roe = fundamental.get("roe", 0)
        if roe > 20:
            score += 0.5
        elif roe < 5:
            score -= 0.5
        
        profit_growth = fundamental.get("net_profit_growth", 0)
        if profit_growth > 20:
            score += 0.5
        elif profit_growth < -10:
            score -= 0.5
    
    return max(0, min(10, score))


def get_score_label(score: float) -> str:
    """获取评分等级标签"""
    if score >= 9:
        return "强烈推荐"
    elif score >= 7:
        return "推荐"
    elif score >= 5:
        return "观望"
    elif score >= 3:
        return "谨慎"
    else:
        return "回避"


def get_score_stars(score: float) -> str:
    """获取评分星级"""
    if score >= 8:
        return "★★★"
    elif score >= 6:
        return "★★☆"
    elif score >= 4:
        return "★☆☆"
    else:
        return "☆☆☆"


def get_recommendation(data: Dict) -> Tuple[str, str, str]:
    """
    获取投资建议
    
    Returns:
        (建议，策略，仓位)
    """
    score = calculate_composite_score(data)
    
    if score >= 8:
        return "强烈推荐", "积极布局，逢低买入", "7-8 成"
    elif score >= 6:
        return "推荐", "适度参与，波段操作", "5-6 成"
    elif score >= 4:
        return "观望", "保持观望，等待信号", "3-4 成"
    elif score >= 2:
        return "谨慎", "降低仓位，注意风险", "1-2 成"
    else:
        return "回避", "建议清仓，等待企稳", "0 成"


def calculate_target_price(data: Dict) -> float:
    """计算目标价位"""
    price = data.get("price", 0)
    technical = data.get("technical", {})
    
    # 优先使用阻力位
    resistance = technical.get("resistance")
    if resistance and resistance > 0:
        return resistance
    
    # 根据评分估算
    score = calculate_composite_score(data)
    if score >= 8:
        return price * 1.15
    elif score >= 6:
        return price * 1.10
    elif score >= 4:
        return price * 1.05
    else:
        return price * 0.95


def calculate_stop_loss(data: Dict) -> float:
    """计算止损价位"""
    price = data.get("price", 0)
    technical = data.get("technical", {})
    
    # 优先使用支撑位
    support = technical.get("support")
    if support and support > 0:
        return support * 0.97
    
    # 默认止损 5%
    return price * 0.95


def format_price(price: float) -> str:
    """格式化价格显示"""
    if price >= 1000:
        return f"¥{price:,.0f}"
    elif price >= 100:
        return f"¥{price:.2f}"
    else:
        return f"¥{price:.3f}"


def format_change(change: float) -> str:
    """格式化涨跌幅"""
    if change >= 0:
        return f"+{change:.2f}%"
    else:
        return f"{change:.2f}%"


def format_volume(volume: float) -> str:
    """格式化成交量"""
    if volume >= 100000000:
        return f"{volume/100000000:.2f}亿"
    elif volume >= 1000000:
        return f"{volume/10000:.0f}万"
    else:
        return f"{volume:.0f}"


def analyze_trend(ma_data: Dict) -> str:
    """分析均线趋势"""
    if not all(ma_data.values()):
        return "数据不足"
    
    ma5 = ma_data.get(5, 0)
    ma10 = ma_data.get(10, 0)
    ma20 = ma_data.get(20, 0)
    ma60 = ma_data.get(60, 0)
    
    if ma5 > ma10 > ma20 > ma60:
        return "多头排列"
    elif ma5 < ma10 < ma20 < ma60:
        return "空头排列"
    elif ma5 > ma20 and ma10 > ma20:
        return "短期偏多"
    elif ma5 < ma20 and ma10 < ma20:
        return "短期偏空"
    else:
        return "震荡整理"


def analyze_macd(macd_data: Dict) -> str:
    """分析 MACD 信号"""
    signal = macd_data.get("signal", "unknown")
    
    signals = {
        "bullish": "多头强势",
        "bearish": "空头强势",
        "golden_cross": "金叉买入",
        "dead_cross": "死叉卖出",
        "unknown": "信号不明"
    }
    
    return signals.get(signal, "未知")


def analyze_rsi(rsi: Optional[float]) -> str:
    """分析 RSI 指标"""
    if rsi is None:
        return "数据不足"
    
    if rsi >= 80:
        return "严重超买"
    elif rsi >= 70:
        return "超买"
    elif rsi >= 50:
        return "偏强"
    elif rsi >= 30:
        return "偏弱"
    else:
        return "超卖"


def get_risk_level(score: float) -> str:
    """获取风险等级"""
    if score >= 8:
        return "低风险"
    elif score >= 6:
        return "中低风险"
    elif score >= 4:
        return "中等风险"
    elif score >= 2:
        return "中高风险"
    else:
        return "高风险"


def generate_summary_text(data: Dict) -> str:
    """生成摘要文本"""
    stock_name = data.get("stock_name", "该股")
    score = calculate_composite_score(data)
    change = data.get("change_percent", 0)
    technical = data.get("technical", {})
    
    parts = []
    
    # 价格表现
    if abs(change) > 5:
        parts.append(f"今日{'大涨' if change > 0 else '大跌'}{abs(change):.1f}%")
    elif abs(change) > 2:
        parts.append(f"今日{'上涨' if change > 0 else '下跌'}{abs(change):.1f}%")
    
    # 技术面
    tech_signal = technical.get("signal", "")
    if tech_signal == "bullish":
        parts.append("技术面看多")
    elif tech_signal == "bearish":
        parts.append("技术面看空")
    
    # 趋势
    trend = technical.get("trend", "")
    if trend == "bullish":
        parts.append("趋势向上")
    elif trend == "bearish":
        parts.append("趋势向下")
    
    if not parts:
        return f"{stock_name}走势平稳，建议继续观察。"
    
    return f"{stock_name}{'，'.join(parts)}。"


def compare_stocks(stock_list: List[Dict]) -> List[Dict]:
    """
    比较多只股票，返回排序后的列表
    
    Args:
        stock_list: 股票数据列表
    
    Returns:
        按综合评分排序的股票列表
    """
    for stock in stock_list:
        stock["_score"] = calculate_composite_score(stock)
    
    return sorted(stock_list, key=lambda x: x.get("_score", 0), reverse=True)


def export_to_json(data: Dict, filepath: str) -> bool:
    """导出数据到 JSON 文件"""
    try:
        # 移除报告内容（太大）
        export_data = {k: v for k, v in data.items() if k != "report"}
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
        
        return True
    except Exception as e:
        print(f"导出失败：{e}")
        return False


def import_from_json(filepath: str) -> Optional[Dict]:
    """从 JSON 文件导入数据"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"导入失败：{e}")
        return None


def get_analysis_timestamp() -> str:
    """获取分析时间戳"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date_range(days: int = 30) -> Tuple[str, str]:
    """获取日期范围"""
    end_date = datetime.now()
    start_date = datetime.now() - timedelta(days=days)
    
    return (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )


# 导入 timedelta
from datetime import timedelta


if __name__ == "__main__":
    # 测试工具函数
    import codecs
    import sys
    if sys.platform == 'win32':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
    
    print("A 股分析工具函数库测试")
    print("=" * 50)
    
    # 测试数据
    test_data = {
        "stock_name": "贵州茅台",
        "price": 1455.02,
        "change_percent": -0.76,
        "technical": {
            "signal": "neutral",
            "trend": "neutral",
            "ma": {5: 19.21, 10: 19.24, 20: 19.05, 60: 19.06},
            "macd": {"signal": "dead_cross"},
            "rsi": 51.07
        },
        "news_sentiment": {
            "avg_sentiment_score": 0.5
        }
    }
    
    score = calculate_composite_score(test_data)
    print(f"\n综合评分：{score:.1f}")
    print(f"评分等级：{get_score_label(score)}")
    print(f"星级：{get_score_stars(score)}")
    
    rec, strategy, position = get_recommendation(test_data)
    print(f"\n投资建议：{rec}")
    print(f"操作策略：{strategy}")
    print(f"建议仓位：{position}")
    
    print(f"\n目标价：{calculate_target_price(test_data):.2f}")
    print(f"止损价：{calculate_stop_loss(test_data):.2f}")
    
    print(f"\n价格：{format_price(test_data['price'])}")
    print(f"涨跌：{format_change(test_data['change_percent'])}")
    
    ma = test_data["technical"]["ma"]
    print(f"\n均线趋势：{analyze_trend(ma)}")
    print(f"MACD: {analyze_macd(test_data['technical']['macd'])}")
    print(f"RSI: {analyze_rsi(test_data['technical']['rsi'])}")
