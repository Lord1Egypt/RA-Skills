#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股专业分析报告生成器
格式固定、内容详细、界面美化
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AShareProfessionalReport:
    """A 股专业报告生成器"""

    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.path.expanduser("~/.openclaw/workspace")
        self.workspace_path = workspace_path
        self.output_dir = os.path.join(workspace_path, "a-share-reports")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, data: Dict) -> str:
        """生成专业分析报告"""
        report = []
        
        # 1. 报告头部
        report.append(self._generate_header(data))
        
        # 2. 核心摘要
        report.append(self._generate_summary(data))
        
        # 3. 实时行情
        report.append(self._generate_market_data(data))
        
        # 4. 技术分析
        if data.get("technical"):
            report.append(self._generate_technical_analysis(data))
        
        # 5. 基本面分析
        if data.get("fundamental"):
            report.append(self._generate_fundamental_analysis(data))
        
        # 6. 新闻情绪
        if data.get("news_sentiment"):
            report.append(self._generate_sentiment_analysis(data))
        
        # 7. 历史回顾
        if data.get("memory_history"):
            report.append(self._generate_history_review(data))
        
        # 8. 投资建议
        report.append(self._generate_investment_advice(data))
        
        # 9. 风险提示
        report.append(self._generate_risk_warning())
        
        # 10. 报告尾部
        report.append(self._generate_footer(data))
        
        return "\n\n".join(report)

    def _generate_header(self, data: Dict) -> str:
        """报告头部"""
        stock_name = data.get("stock_name", "未知股票")
        stock_code = data.get("stock_code", "000000")
        report_time = data.get("analysis_timestamp", datetime.now().isoformat())
        
        header = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           A 股专业分析报告                                   ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  股票名称：{stock_name:<44}║
║  股票代码：{stock_code:<44}║
║  分析时间：{report_time[:19]:<44}║
╚══════════════════════════════════════════════════════════════╝
"""
        return header

    def _generate_summary(self, data: Dict) -> str:
        """核心摘要"""
        price = data.get("price", 0)
        change = data.get("change_percent", 0)
        technical = data.get("technical", {})
        sentiment = data.get("news_sentiment", {})
        
        # 计算综合评分
        score = self._calculate_score(data)
        score_label = self._get_score_label(score)
        
        # 一句话点评
        comment = self._generate_comment(data, score)
        
        summary = f"""
┌──────────────────────────────────────────────────────────────┐
│                    ★ 核心摘要                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  当前价格：¥{price:>10.2f}   涨跌幅：{change:>+8.2f}%                      │
│                                                              │
│  技术信号：{technical.get('signal', 'N/A'):>10}   趋势：{technical.get('trend', 'N/A'):>10}                    │
│                                                              │
│  新闻情绪：{sentiment.get('overall_sentiment', 'N/A'):>10}   评分：{sentiment.get('avg_sentiment_score', 0.5):>8.3f}              │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  综合评分：{score:>5.1f} / 10  {score_label:<24}│     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  【一句话点评】                                              │
│  {comment:<58}│
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
        return summary

    def _generate_market_data(self, data: Dict) -> str:
        """实时行情"""
        market = f"""
┌──────────────────────────────────────────────────────────────┐
│                    ★ 实时行情                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   当前价：¥{data.get('price', 0):>10.2f}      涨跌额：{data.get('change', 0):>+10.2f}               │
│   开盘价：¥{data.get('open', 0):>10.2f}      昨收价：¥{data.get('pre_close', 0):>10.2f}               │
│                                                              │
│   最高价：¥{data.get('high', 0):>10.2f}      最低价：¥{data.get('low', 0):>10.2f}               │
│                                                              │
│   成交量：{data.get('volume', 'N/A'):>14}   成交额：{data.get('amount', 'N/A'):>14}           │
│                                                              │
│   更新时间：{data.get('time', 'N/A'):<44}│
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
        return market

    def _generate_technical_analysis(self, data: Dict) -> str:
        """技术分析"""
        tech = data.get("technical", {})
        ma = tech.get("ma", {})
        macd = tech.get("macd", {})
        
        tech_report = f"""
┌──────────────────────────────────────────────────────────────┐
│                    ★ 技术分析                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  【均线系统】                                                │
│  ────────────────────────────────────────────────────────    │
│   MA5:  {ma.get('5', 'N/A')!s:>10}   MA10: {ma.get('10', 'N/A')!s:>10}                              │
│   MA20: {ma.get('20', 'N/A')!s:>10}   MA60: {ma.get('60', 'N/A')!s:>10}                              │
│                                                              │
│   均线排列：{tech.get('ma_arrangement', 'N/A'):<44}│
│                                                              │
│  【MACD 指标】                                                │
│  ────────────────────────────────────────────────────────    │
│   DIF: {macd.get('dif', 'N/A')!s:>10}   DEA: {macd.get('dea', 'N/A')!s:>10}   MACD: {macd.get('macd', 'N/A')!s:>10}      │
│   信号：{macd.get('signal', 'N/A'):<44}│
│                                                              │
│  【其他指标】                                                │
│  ────────────────────────────────────────────────────────    │
│   RSI: {tech.get('rsi', 'N/A')!s:>10}   量比：{tech.get('volume_ratio', 'N/A')!s:>10}                              │
│                                                              │
│   支撑位：¥{tech.get('support', 0):>10.2f}   阻力位：¥{tech.get('resistance', 0):>10.2f}              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
        return tech_report

    def _generate_sentiment_analysis(self, data: Dict) -> str:
        """新闻情绪分析"""
        sentiment = data.get("news_sentiment", {})
        
        sentiment_report = f"""
┌──────────────────────────────────────────────────────────────┐
│                    ★ 新闻情绪分析                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   新闻总数：{sentiment.get('news_count', 0):>10}                                        │
│                                                              │
│   看多新闻：{sentiment.get('bullish_count', 0):>10}   看空新闻：{sentiment.get('bearish_count', 0):>10}   中性：{sentiment.get('neutral_count', 0):>10}  │
│                                                              │
│   情绪评分：{sentiment.get('avg_sentiment_score', 0):>10.3f}                                      │
│   总体情绪：{sentiment.get('overall_sentiment', 'N/A'):<44}│
│                                                              │
│  【最新新闻】                                                │
│  ────────────────────────────────────────────────────────    │
"""
        
        # 添加新闻列表
        news_items = sentiment.get("news_items", [])
        if news_items:
            for i, news in enumerate(news_items[:5], 1):
                title = news.get("title", "无标题")[:50]
                label = news.get("sentiment_label", "N/A")
                score = news.get("sentiment_score", 0)
                
                if label == "BULLISH":
                    icon = "[+]"
                elif label == "BEARISH":
                    icon = "[-]"
                else:
                    icon = "[=]"
                
                sentiment_report += f"   {i}. {icon} {title:<50}│\n"
                sentiment_report += f"      情绪：{label:<8} 评分：{score:.2f}{'':>26}│\n"
        else:
            sentiment_report += "   暂无最新新闻数据\n"
        
        sentiment_report += "│                                                              │\n"
        sentiment_report += "└──────────────────────────────────────────────────────────────┘"
        
        return sentiment_report

    def _generate_history_review(self, data: Dict) -> str:
        """历史分析回顾"""
        history = data.get("memory_history", {})
        
        history_report = f"""
┌──────────────────────────────────────────────────────────────┐
│                    ★ 历史分析回顾                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   分析次数：{history.get('analysis_count', 0):>10}                                        │
│   首次分析：{history.get('first_analysis', 'N/A'):<44}│
│   最近分析：{history.get('last_analysis', 'N/A'):<44}│
│                                                              │
│   主要建议：{history.get('most_common_recommendation', 'N/A'):<44}│
│   平均情绪：{history.get('average_sentiment', 'N/A'):<44}│
│                                                              │
│  【价格历史】                                                │
│  ────────────────────────────────────────────────────────    │
"""
        
        # 添加价格历史
        price_history = history.get("price_history", [])
        if price_history:
            for item in price_history[-5:]:
                date = item.get("date", "N/A")
                price = item.get("price", 0)
                history_report += f"   {date:<12}  ¥{price:>10.2f}{'':>26}│\n"
        else:
            history_report += "   暂无历史价格数据\n"
        
        history_report += "│                                                              │\n"
        history_report += "└──────────────────────────────────────────────────────────────┘"
        
        return history_report

    def _generate_investment_advice(self, data: Dict) -> str:
        """投资建议"""
        score = self._calculate_score(data)
        tech = data.get("technical", {})
        
        # 确定建议
        if score >= 8:
            advice = "强烈推荐"
            icon = "★★★"
            strategy = "积极布局，仓位可达 7-8 成"
        elif score >= 6:
            advice = "推荐"
            icon = "★★☆"
            strategy = "适度参与，仓位控制在 5-6 成"
        elif score >= 4:
            advice = "观望"
            icon = "★☆☆"
            strategy = "保持观望，等待明确信号"
        elif score >= 2:
            advice = "谨慎"
            icon = "☆☆☆"
            strategy = "降低仓位，控制在 3 成以内"
        else:
            advice = "回避"
            icon = "☆☆☆"
            strategy = "建议清仓回避，等待企稳信号"
        
        support = tech.get("support", data.get("price", 0) * 0.95)
        resistance = tech.get("resistance", data.get("price", 0) * 1.05)
        target_price = resistance
        stop_loss = support * 0.97
        
        advice_report = f"""
┌──────────────────────────────────────────────────────────────┐
│                    ★ 投资建议                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   {icon} {advice:<8}                                              │
│                                                              │
│   操作策略：{strategy:<44}│
│                                                              │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│   关键位置：                                                 │
│   支撑位：¥{support:>10.2f}   阻力位：¥{resistance:>10.2f}                      │
│                                                              │
│   目标价位：¥{target_price:>10.2f}   止损价位：¥{stop_loss:>10.2f}                      │
│                                                              │
│  ────────────────────────────────────────────────────────    │
│                                                              │
│   买入条件参考：                                             │
│   1. 价格站稳支撑位上方                                      │
│   2. MACD 形成金叉信号                                        │
│   3. 成交量明显放大                                          │
│                                                              │
│   卖出条件参考：                                             │
│   1. 跌破支撑位                                              │
│   2. MACD 形成死叉信号                                        │
│   3. 触及阻力位后回落                                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
        return advice_report

    def _generate_risk_warning(self) -> str:
        """风险提示"""
        warning = """
┌──────────────────────────────────────────────────────────────┐
│                    ⚠ 风险提示                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   1. 市场风险：股市有风险，投资需谨慎                         │
│   2. 数据延迟：实时行情可能存在 1-2 秒延迟                      │
│   3. 分析局限：技术分析不是 100% 准确，需结合多方面因素          │
│   4. 信息时效：新闻情绪分析基于公开信息，可能存在滞后         │
│   5. 个人情况：请根据自身风险承受能力做出决策                 │
│   6. 不构成建议：本报告仅供参考，不构成投资建议               │
│                                                              │
│   ═══════════════════════════════════════════════════════    │
│   重要声明：投资有风险，入市需谨慎。过往表现不代表未来收益。 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
        return warning

    def _generate_footer(self, data: Dict) -> str:
        """报告尾部"""
        footer = f"""
┌──────────────────────────────────────────────────────────────┐
│                    ★ 数据源说明                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   • 实时行情：新浪财经 API                                    │
│   • 技术指标：东方财富网 (免费)                               │
│   • 新闻情绪：Firecrawl 网页抓取                              │
│   • 历史记忆：Elite Long-term Memory                          │
│                                                              │
│   报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<40}│
│                                                              │
│   ═══════════════════════════════════════════════════════    │
│              感谢使用 A 股专业分析系统                         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
"""
        return footer

    def _calculate_score(self, data: Dict) -> float:
        """计算综合评分 (0-10)"""
        score = 5.0
        
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
        if change > 3:
            score += 0.5
        elif change < -3:
            score -= 0.5
        
        return max(0, min(10, score))

    def _get_score_label(self, score: float) -> str:
        """获取评分标签"""
        if score >= 8:
            return "强烈推荐"
        elif score >= 6:
            return "推荐"
        elif score >= 4:
            return "观望"
        elif score >= 2:
            return "谨慎"
        else:
            return "回避"

    def _generate_comment(self, data: Dict, score: float) -> str:
        """生成一句话点评"""
        stock_name = data.get("stock_name", "该股")
        
        if score >= 8:
            return f"{stock_name} 各项指标优秀，建议重点关注，逢低布局。"
        elif score >= 6:
            return f"{stock_name} 整体表现良好，可适度参与，注意仓位控制。"
        elif score >= 4:
            return f"{stock_name} 走势震荡，建议观望为主，等待明确信号。"
        elif score >= 2:
            return f"{stock_name} 风险较高，谨慎参与，设置好止损位。"
        else:
            return f"{stock_name} 多项指标走弱，建议回避，等待企稳信号。"

    def save_report(self, report: str, stock_code: str, stock_name: str) -> str:
        """保存报告（按股票代码分类存储）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 创建股票代码二级目录
        stock_dir = os.path.join(self.output_dir, stock_code)
        os.makedirs(stock_dir, exist_ok=True)
        
        # 保存报告到股票代码目录
        filename = f"{stock_code}_{stock_name}_{timestamp}_PRO.md"
        filepath = os.path.join(stock_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)
        
        logger.info(f"报告已保存：{filepath}")
        return filepath
