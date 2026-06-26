#!/usr/bin/env python3
"""
Stock Monitor Pro - AI 深度分析引擎（付费版）
调用 Kimi/DeepSeek API 生成专业投资分析
"""

import requests
import json
import os
from typing import Dict, List, Optional
from datetime import datetime

class AIAnalyser:
    """AI 深度分析器 - 付费版核心功能"""
    
    def __init__(self, api_key: str = None, model: str = "kimi"):
        self.api_key = api_key or os.environ.get("KIMI_API_KEY")
        self.model = model
        self.base_url = {
            "kimi": "https://api.moonshot.cn/v1/chat/completions",
            "deepseek": "https://api.deepseek.com/v1/chat/completions"
        }
    
    def analyze_stock(self, stock: Dict, price_data: Dict, alerts: List, news: List = None) -> str:
        """
        AI 深度分析单只股票
        
        Args:
            stock: 股票信息 {code, name, cost, shares, ...}
            price_data: 价格数据 {price, change_pct, volume, ...}
            alerts: 触发的预警列表
            news: 相关新闻列表
        
        Returns:
            AI 生成的分析报告
        """
        # 构建分析提示词
        prompt = self._build_analysis_prompt(stock, price_data, alerts, news)
        
        # 调用 AI API
        try:
            response = self._call_ai_api(prompt)
            return response
        except Exception as e:
            return f"⚠️ AI 分析暂时不可用: {str(e)}"
    
    def _build_analysis_prompt(self, stock: Dict, price_data: Dict, alerts: List, news: List = None) -> str:
        """构建分析提示词"""
        code = stock.get('code', '')
        name = stock.get('name', '')
        cost = stock.get('cost', 0)
        shares = stock.get('shares', 0)
        
        price = price_data.get('price', 0)
        change_pct = price_data.get('change_pct', 0)
        volume = price_data.get('volume', 0)
        
        # 计算盈亏
        pnl_pct = ((price - cost) / cost * 100) if cost > 0 else 0
        pnl_amount = (price - cost) * shares
        
        prompt = f"""你是一位专业的A股投资顾问。请分析以下股票情况并给出建议：

## 股票信息
- 代码: {code}
- 名称: {name}
- 持仓成本: ¥{cost:.2f}
- 持仓数量: {shares} 股
- 当前价格: ¥{price:.2f}
- 今日涨跌: {change_pct:+.2f}%
- 成交量: {volume}

## 盈亏情况
- 盈亏比例: {pnl_pct:+.2f}%
- 盈亏金额: ¥{pnl_amount:,.2f}

## 触发预警
{self._format_alerts(alerts)}

## 相关新闻
{self._format_news(news)}

## 分析要求
请从以下维度进行分析（200字以内）：
1. **技术面**: 价格走势、支撑压力位
2. **消息面**: 新闻影响、市场情绪
3. **操作建议**: 买入/持有/卖出建议，具体价位

请用简洁专业的语言，避免废话。"""

        return prompt
    
    def _format_alerts(self, alerts: List) -> str:
        """格式化预警信息"""
        if not alerts:
            return "无预警触发"
        
        lines = []
        for alert in alerts:
            lines.append(f"- {alert.get('type', '未知')}: {alert.get('message', '')}")
        return "\n".join(lines)
    
    def _format_news(self, news: List) -> str:
        """格式化新闻信息"""
        if not news:
            return "暂无相关新闻"
        
        lines = []
        for n in news[:3]:  # 最多 3 条
            lines.append(f"- {n.get('title', '无标题')}")
        return "\n".join(lines)
    
    def _call_ai_api(self, prompt: str) -> str:
        """调用 AI API"""
        if not self.api_key:
            return "⚠️ 未配置 API Key，请设置 KIMI_API_KEY 环境变量"
        
        url = self.base_url.get(self.model, self.base_url["kimi"])
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "moonshot-v1-8k" if self.model == "kimi" else "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一位专业的A股投资顾问，擅长技术分析和基本面分析。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def generate_trading_signal(self, stock: Dict, price_data: Dict, indicators: Dict) -> Dict:
        """
        生成交易信号
        
        Returns:
            {
                "signal": "buy" | "sell" | "hold",
                "confidence": 0.0-1.0,
                "reason": "原因说明",
                "target_price": 目标价,
                "stop_loss": 止损价
            }
        """
        # 基于技术指标生成信号
        signal = "hold"
        confidence = 0.5
        reasons = []
        
        # RSI 分析
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            signal = "buy"
            confidence += 0.2
            reasons.append("RSI 超卖")
        elif rsi > 70:
            signal = "sell"
            confidence += 0.2
            reasons.append("RSI 超买")
        
        # 均线分析
        ma5 = indicators.get('ma5', 0)
        ma10 = indicators.get('ma10', 0)
        if ma5 > ma10:
            confidence += 0.1
            reasons.append("均线多头")
        elif ma5 < ma10:
            confidence -= 0.1
            reasons.append("均线空头")
        
        # 成交量分析
        volume_ratio = indicators.get('volume_ratio', 1)
        if volume_ratio > 2:
            confidence += 0.1
            reasons.append("放量异动")
        
        # 价格相对成本
        price = price_data.get('price', 0)
        cost = stock.get('cost', 0)
        pnl_pct = ((price - cost) / cost * 100) if cost > 0 else 0
        
        if pnl_pct < -15:
            signal = "hold"  # 深套不建议割肉
            reasons.append("深度亏损，建议等待反弹")
        elif pnl_pct > 20:
            signal = "sell"
            confidence += 0.2
            reasons.append("盈利较多，可考虑减仓")
        
        return {
            "signal": signal,
            "confidence": min(confidence, 1.0),
            "reason": "；".join(reasons) if reasons else "无明显信号",
            "target_price": price * 1.1 if signal == "buy" else price * 0.95,
            "stop_loss": cost * 0.9 if cost > 0 else price * 0.9
        }


# ========== 免费版 vs 付费版 ==========

class FreeAnalyser:
    """免费版分析器 - 简单规则"""
    
    def analyze_stock(self, stock: Dict, price_data: Dict, alerts: List, news: List = None) -> str:
        """简单分析"""
        price = price_data.get('price', 0)
        change_pct = price_data.get('change_pct', 0)
        
        if change_pct > 3:
            return "📈 短期涨幅较大，注意风险。"
        elif change_pct < -3:
            return "📉 短期跌幅较大，关注反弹机会。"
        else:
            return "⏳ 走势平稳，继续观察。"


# ========== 使用示例 ==========

if __name__ == '__main__':
    # 付费版使用
    ai_analyser = AIAnalyser(model="kimi")
    
    # 测试数据
    stock = {
        "code": "002459",
        "name": "晶澳科技",
        "cost": 16.275,
        "shares": 16900
    }
    
    price_data = {
        "price": 13.20,
        "change_pct": -2.5,
        "volume": 150000
    }
    
    alerts = [
        {"type": "亏损预警", "message": "亏损 18.9%"}
    ]
    
    # 分析
    print("=== AI 深度分析（付费版）===")
    analysis = ai_analyser.analyze_stock(stock, price_data, alerts)
    print(analysis)
    
    # 交易信号
    print("\n=== 交易信号 ===")
    indicators = {"rsi": 35, "ma5": 13.5, "ma10": 13.8, "volume_ratio": 1.5}
    signal = ai_analyser.generate_trading_signal(stock, price_data, indicators)
    print(json.dumps(signal, ensure_ascii=False, indent=2))
