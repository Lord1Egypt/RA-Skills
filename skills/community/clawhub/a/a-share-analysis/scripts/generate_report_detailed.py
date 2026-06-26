#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股专业详细分析报告生成器（增强版）
生成内容详细、专业、可商用的分析报告
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AShareDetailedReport:
    """A 股详细报告生成器（增强版）"""

    def __init__(self, workspace_path: str = None):
        if workspace_path is None:
            workspace_path = os.path.expanduser("~/.openclaw/workspace")
        self.workspace_path = workspace_path
        self.output_dir = os.path.join(workspace_path, "a-share-reports")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_report(self, data: Dict) -> str:
        """生成详细专业报告"""
        report = []
        
        # 1. 专业封面
        report.append(self._create_cover(data))
        
        # 2. 重要声明
        report.append(self._create_disclaimer())
        
        # 3. 投资评级
        report.append(self._create_rating(data))
        
        # 4. 核心摘要（详细）
        report.append(self._create_executive_summary(data))
        
        # 5. 实时行情（详细）
        report.append(self._create_market_data_detailed(data))
        
        # 6. 技术分析（超详细）
        if data.get('technical'):
            report.append(self._create_technical_analysis_super_detailed(data))
        
        # 7. 新闻情绪
        if data.get('news_sentiment'):
            report.append(self._create_sentiment_analysis(data))
        
        # 8. 历史回顾
        if data.get('memory_history') and data['memory_history'].get('analysis_count', 0) > 0:
            report.append(self._create_history_review_detailed(data))
        
        # 9. 投资建议（详细）
        report.append(self._create_investment_advice_detailed(data))
        
        # 10. 情景分析
        report.append(self._create_scenario_analysis(data))
        
        # 11. 风险提示（详细）
        report.append(self._create_risk_warning_detailed(data))
        
        # 12. 报告附录
        report.append(self._create_appendix(data))
        
        return "\n\n".join(report)

    def _create_cover(self, data: Dict) -> str:
        """创建专业封面"""
        stock_name = data.get('stock_name', '未知股票')
        stock_code = data.get('stock_code', '000000')
        report_date = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        
        return f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                          A 股深度研究报告                                 ║
║                     A-SHARE IN-DEPTH RESEARCH REPORT                     ║
║                                                                          ║
║  ════════════════════════════════════════════════════════════════════   ║
║                                                                          ║
║  股票名称：{stock_name:<54}║
║  股票代码：{stock_code:<54}║
║  报告类型：深度研究报告                                                ║
║  报告日期：{report_date}                                         ║
║                                                                          ║
║  ════════════════════════════════════════════════════════════════════   ║
║                                                                          ║
║  编制机构：A 股专业分析系统                                               ║
║  系统版本：v2.6 专业增强版                                                ║
║  分 析 师：AI 分析师                                                      ║
║  报告编号：ASHARE-{stock_code}-{datetime.now().strftime("%Y%m%d")}                          ║
║                                                                          ║
║  保密等级：内部资料·注意保密                                           ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

    def _create_disclaimer(self) -> str:
        """创建重要声明"""
        return """
┌──────────────────────────────────────────────────────────────────────────┐
│                           重 要 声 明                                    │
│                         IMPORTANT DISCLAIMER                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. 报告性质声明                                                         │
│     本报告由 AI 分析系统自动生成，基于公开数据进行技术分析，仅供参考。      │
│                                                                          │
│  2. 投资建议声明                                                         │
│     本报告不构成任何投资建议或推荐，投资者应独立判断，自主决策。          │
│                                                                          │
│  3. 数据准确性声明                                                       │
│     报告数据来源于公开渠道，可能存在延迟或误差，以交易所数据为准。        │
│                                                                          │
│  4. 风险提示                                                             │
│     股市有风险，投资需谨慎。过往表现不代表未来收益。                      │
│                                                                          │
│  5. 使用限制                                                             │
│     本报告仅供个人参考，未经书面许可，不得用于商业用途或公开传播。        │
│                                                                          │
│  6. 责任免除                                                             │
│     因使用本报告导致的任何损失，编制方不承担法律责任。                    │
│                                                                          │
│  阅读本报告即表示您已充分理解并接受上述声明的全部内容。                  │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_rating(self, data: Dict) -> str:
        """创建投资评级"""
        # 确保数据存在
        if 'price' not in data or data['price'] is None:
            data['price'] = 0
        if 'change_percent' not in data or data['change_percent'] is None:
            data['change_percent'] = 0
        if 'technical' not in data or data['technical'] is None:
            data['technical'] = {}
        if 'news_sentiment' not in data or data['news_sentiment'] is None:
            data['news_sentiment'] = {}
        if 'memory_history' not in data or data['memory_history'] is None:
            data['memory_history'] = {}
        
        score = self._calculate_score(data)
        rating = self._get_rating_label(score)
        rating_en = self._get_rating_label_en(score)
        target_price = self._calculate_target_price(data)
        stop_loss = self._calculate_stop_loss(data)
        current_price = data.get('price', 0)
        upside = ((target_price - current_price) / current_price * 100) if current_price and current_price > 0 else 0
        downside = ((stop_loss - current_price) / current_price * 100) if current_price and current_price > 0 else 0
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                           投 资 评 级                                    │
│                         INVESTMENT RATING                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌────────────────────────────────────────────────────────────────┐    │
│   │                                                                │    │
│   │     综合评分：{score:.1f} / 10.0                                          │    │
│   │     投资评级：{rating} ({rating_en})                               │    │
│   │                                                                │    │
│   └────────────────────────────────────────────────────────────────┘    │
│                                                                          │
│   当前价格：¥{current_price:>10.2f}                                       │
│   目标价格：¥{target_price:>10.2f}     (潜在空间：{upside:+.1f}%)                     │
│   止损价格：¥{stop_loss:>10.2f}     (风险空间：{downside:.1f}%)        │
│                                                                          │
│   评级说明：                                                             │
│   ┌────────────┬────────────────────────────────────────────────────┐   │
│   │ 强烈推荐   │ 预计涨幅>20%，技术面与基本面共振向好                │   │
│   ├────────────┼────────────────────────────────────────────────────┤   │
│   │ 推荐       │ 预计涨幅 10-20%，整体表现良好                       │   │
│   ├────────────┼────────────────────────────────────────────────────┤   │
│   │ 中性       │ 预计涨幅 -10% 至 10%，震荡整理                        │   │
│   ├────────────┼────────────────────────────────────────────────────┤   │
│   │ 谨慎       │ 预计跌幅 10-20%，风险较高                           │   │
│   ├────────────┼────────────────────────────────────────────────────┤   │
│   │ 回避       │ 预计跌幅>20%，多项指标走弱                          │   │
│   └────────────┴────────────────────────────────────────────────────┘   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_executive_summary(self, data: Dict) -> str:
        """创建详细核心摘要"""
        stock_name = data.get('stock_name', '未知股票')
        stock_code = data.get('stock_code', '000000')
        price = data.get('price', 0)
        change = data.get('change_percent', 0)
        volume = data.get('volume', 'N/A')
        amount = data.get('amount', 'N/A')
        
        technical = data.get('technical', {})
        ma_arrangement = technical.get('ma_arrangement', 'N/A')
        macd_signal = technical.get('macd', {}).get('signal', 'N/A')
        rsi = technical.get('rsi', 'N/A')
        trend = technical.get('trend', 'N/A')
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                           核 心 摘 要                                    │
│                        EXECUTIVE SUMMARY                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、基本信息                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  股票名称：{stock_name} ({stock_code})                                              │
│  当前价格：¥{price:.2f}   涨跌幅：{change:+.2f}%                                     │
│  成交金额：{amount}   成交量：{volume}                                           │
│  分析时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                               │
│                                                                          │
│  二、技术面要点                                                          │
│  ────────────────────────────────────────────────────────────────────    │
│  均线排列：{ma_arrangement:<70}│
│  MACD 信号：{macd_signal:<70}│
│  趋势方向：{trend:<70}│
│  RSI 指标：{str(rsi):<70}│
│                                                                          │
│  三、核心观点                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  {self._generate_core_view(data):<70}│
│                                                                          │
│  四、操作建议                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  {self._generate_operation_advice(data):<70}│
│                                                                          │
│  五、关键位置                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  支撑位：¥{technical.get('support', 'N/A'):<10}    阻力位：¥{technical.get('resistance', 'N/A'):<10}                     │
│  目标价：¥{self._calculate_target_price(data):<10}    止损价：¥{self._calculate_stop_loss(data):<10}                     │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_market_data_detailed(self, data: Dict) -> str:
        """创建详细行情数据"""
        price = data.get('price', 0)
        high = data.get('high', price)
        low = data.get('low', price)
        amplitude = ((high - low) / low * 100) if low else 0
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                           行 情 数 据                                    │
│                         MARKET DATA                                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、实时行情                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  ┌────────────┬────────────┬────────────┬────────────┬────────────┐     │
│  │   项目     │    数值    │   项目     │    数值    │   项目     │     │
│  ├────────────┼────────────┼────────────┼────────────┼────────────┤     │
│  │  当前价格  │¥{price:>10.2f}│  涨跌额    │{data.get('change', 0):>+10.2f}│  涨跌幅    │     │
│  │  开盘价格  │¥{data.get('open', 0):>10.2f}│  最高价格  │¥{high:>10.2f}│  最低价格  │     │
│  │  昨收价格  │¥{data.get('pre_close', 0):>10.2f}│  成交数量  │{str(data.get('volume', 'N/A')):>10}│  成交金额  │     │
│  └────────────┴────────────┴────────────┴────────────┴────────────┘     │
│                                                                          │
│  二、价格统计                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  日内振幅：{amplitude:>10.2f}%                                           │
│  量比：{data.get('technical', {}).get('volume_ratio', 'N/A'):>10}                                                         │
│  更新时间：{str(data.get('time', 'N/A'))[:16]:>10}                                                 │
│                                                                          │
│  三、盘面解读                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  {self._interpret_market_data(data):<70}│
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_technical_analysis_super_detailed(self, data: Dict) -> str:
        """创建超详细技术分析"""
        tech = data.get('technical', {})
        ma = tech.get('ma', {})
        macd = tech.get('macd', {})
        price = data.get('price', 0)
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                     技 术 分 析（超详细）                                 │
│                      TECHNICAL ANALYSIS                                  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、均线系统分析                                                        │
│  ────────────────────────────────────────────────────────────────────    │
│  ┌────────────┬────────────┬────────────┬────────────────────────────┐  │
│  │   均线     │    数值    │   位置     │           说明             │  │
│  ├────────────┼────────────┼────────────┼────────────────────────────┤  │
│  │   MA5      │{str(ma.get(5, 'N/A')):>10}│{self._get_ma_position(price, ma.get(5)):>10}│ 短期趋势线（5 日均线）       │  │
│  │   MA10     │{str(ma.get(10, 'N/A')):>10}│{self._get_ma_position(price, ma.get(10)):>10}│ 半月趋势线（10 日均线）      │  │
│  │   MA20     │{str(ma.get(20, 'N/A')):>10}│{self._get_ma_position(price, ma.get(20)):>10}│ 月线（生命线，20 日均线）    │  │
│  │   MA60     │{str(ma.get(60, 'N/A')):>10}│{self._get_ma_position(price, ma.get(60)):>10}│ 季线（决策线，60 日均线）    │  │
│  └────────────┴────────────┴────────────┴────────────────────────────┘  │
│                                                                          │
│  均线排列：{tech.get('ma_arrangement', 'N/A'):<70}│
│  均线解读：{self._interpret_ma_arrangement(tech.get('ma_arrangement', '')):<70}│
│                                                                          │
│  二、MACD 指标分析                                                       │
│  ────────────────────────────────────────────────────────────────────    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  DIF（快线/差离值）：{str(macd.get('dif', 'N/A')):>10}                                   │  │
│  │  DEA（慢线/信号线）：{str(macd.get('dea', 'N/A')):>10}                                   │  │
│  │  MACD 柱（红绿柱）：{str(macd.get('macd', 'N/A')):>10}                                     │  │
│  │  信号状态：{macd.get('signal', 'N/A'):>10}                                              │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│  MACD 解读：{self._interpret_macd(macd):<70}│
│                                                                          │
│  三、RSI 指标分析                                                        │
│  ────────────────────────────────────────────────────────────────────    │
│  RSI 数值：{tech.get('rsi', 'N/A'):>10}                                                  │
│  RSI 状态：{self._get_rsi_status(tech.get('rsi')):<70}│
│  RSI 解读：{self._interpret_rsi(tech.get('rsi')):<70}│
│                                                                          │
│  四、成交量分析                                                          │
│  ────────────────────────────────────────────────────────────────────    │
│  量比：{tech.get('volume_ratio', 'N/A'):>10}                                                             │
│  量比解读：{self._interpret_volume_ratio(tech.get('volume_ratio')):<70}│
│                                                                          │
│  五、支撑阻力分析                                                        │
│  ────────────────────────────────────────────────────────────────────    │
│  第一支撑位：¥{tech.get('support', 'N/A'):<10}    第二支撑位：¥{tech.get('support', 0) * 0.95 if tech.get('support') else 'N/A':<10}       │
│  第一阻力位：¥{tech.get('resistance', 'N/A'):<10}    第二阻力位：¥{tech.get('resistance', 0) * 1.05 if tech.get('resistance') else 'N/A':<10}       │
│                                                                          │
│  支撑位解读：{self._interpret_support_resistance(tech):<70}│
│                                                                          │
│  六、综合技术评级                                                        │
│  ────────────────────────────────────────────────────────────────────    │
│  技术评分：{self._calculate_technical_score(tech):>10}/100                                                 │
│  技术评级：{self._get_technical_rating(tech):<70}│
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_sentiment_analysis(self, data: Dict) -> str:
        """创建新闻情绪分析"""
        sentiment = data.get('news_sentiment', {})
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                         新 闻 情 绪 分 析                                 │
│                       SENTIMENT ANALYSIS                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、情绪概览                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  新闻总数：{sentiment.get('news_count', 0):>10}                                                │
│  情绪评分：{sentiment.get('avg_sentiment_score', 0):>10.3f}（0-1，越高越积极）                           │
│  总体情绪：{sentiment.get('overall_sentiment', 'UNKNOWN'):>10}                                                │
│                                                                          │
│  二、情绪分布                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  看多新闻：{sentiment.get('bullish_count', 0):>10}  占比：{sentiment.get('bullish_count', 0) / max(sentiment.get('news_count', 1), 1) * 100:>5.1f}%                  │
│  看空新闻：{sentiment.get('bearish_count', 0):>10}  占比：{sentiment.get('bearish_count', 0) / max(sentiment.get('news_count', 1), 1) * 100:>5.1f}%                  │
│  中性新闻：{sentiment.get('neutral_count', 0):>10}  占比：{sentiment.get('neutral_count', 0) / max(sentiment.get('news_count', 1), 1) * 100:>5.1f}%                  │
│                                                                          │
│  三、情绪解读                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  {self._interpret_sentiment(sentiment):<70}│
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_history_review_detailed(self, data: Dict) -> str:
        """创建详细历史回顾"""
        history = data.get('memory_history', {})
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                         历 史 分 析 回 顾                                 │
│                      HISTORY REVIEW                                      │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、分析统计                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  分析次数：{history.get('analysis_count', 0):>10}                                                │
│  首次分析：{history.get('first_analysis', 'N/A'):>10}                                                │
│  最近分析：{history.get('last_analysis', 'N/A'):>10}                                                │
│                                                                          │
│  二、历史观点                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  主要建议：{history.get('most_common_recommendation', 'N/A'):>10}                                                │
│  平均情绪：{history.get('average_sentiment', 'N/A'):>10}                                                │
│                                                                          │
│  三、价格历史                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  {self._generate_price_history_table(history):<70}│
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_investment_advice_detailed(self, data: Dict) -> str:
        """创建详细投资建议"""
        # 确保数据存在
        price = data.get('price', 0) or 0
        tech = data.get('technical', {}) or {}
        
        score = self._calculate_score(data)
        rating = self._get_rating_label(score)
        
        support = tech.get('support') or (price * 0.9)
        resistance = tech.get('resistance') or (price * 1.1)
        target_price = self._calculate_target_price(data)
        stop_loss = self._calculate_stop_loss(data)
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                           投 资 建 议                                    │
│                      INVESTMENT ADVICE                                   │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、综合建议                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                   │  │
│  │     投资评级：{rating:<10}   综合评分：{score:.1f}/10                            │  │
│  │                                                                   │  │
│  │     建议操作：{self._get_operation_suggestion(score):<48}│  │
│  │                                                                   │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  二、仓位建议                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  建议仓位：{self._get_position_suggestion(score):<70}│
│  加仓条件：价格站稳{support:.2f}上方且 MACD 金叉                               │
│  减仓条件：触及{resistance:.2f}阻力位或 RSI>80                                   │
│                                                                          │
│  三、价格目标                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  ┌────────────┬────────────┬────────────┬────────────────────────────┐  │
│  │   类型     │    价格    │   空间     │           说明             │  │
│  ├────────────┼────────────┼────────────┼────────────────────────────┤  │
│  │  短期目标  │¥{target_price:>10.2f}│{((target_price - price) / price * 100):>+10.1f}%│ 1-2 周                        │  │
│  │  中期目标  │¥{(target_price * 1.1):>10.2f}│{((target_price * 1.1 - price) / price * 100):>+10.1f}%│ 1-3 个月                      │  │
│  │  止损价位  │¥{stop_loss:>10.2f}│{((stop_loss - price) / price * 100):>+10.1f}%│ 风险控制                      │  │
│  └────────────┴────────────┴────────────┴────────────────────────────┘  │
│                                                                          │
│  四、操作策略                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  {self._get_detailed_strategy(score, tech):<70}│
│                                                                          │
│  五、关注要点                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  1. 关注{support:.2f}支撑位的有效性                                            │
│  2. 关注{resistance:.2f}阻力位的突破情况                                         │
│  3. 关注 MACD 指标是否持续金叉                                             │
│  4. 关注 RSI 是否出现超买信号                                              │
│  5. 关注成交量变化配合情况                                               │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_scenario_analysis(self, data: Dict) -> str:
        """创建情景分析"""
        price = data.get('price', 0) or 0
        tech = data.get('technical', {}) or {}
        support = tech.get('support') or (price * 0.9)
        resistance = tech.get('resistance') or (price * 1.1)
        
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                           情 景 分 析                                    │
│                       SCENARIO ANALYSIS                                  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、乐观情景（概率 30%）                                                 │
│  ────────────────────────────────────────────────────────────────────    │
│  触发条件：突破{resistance:.2f}阻力位，成交量放大 50% 以上                        │
│  目标价格：¥{resistance * 1.15:.2f}                                                           │
│  操作建议：加仓至 7-8 成，设置移动止损                                       │
│                                                                          │
│  二、基准情景（概率 50%）                                                 │
│  ────────────────────────────────────────────────────────────────────    │
│  触发条件：在{support:.2f}-{resistance:.2f}区间震荡                                  │
│  目标价格：¥{(support + resistance) / 2:.2f}                                                           │
│  操作建议：保持 5-6 成仓位，高抛低吸                                        │
│                                                                          │
│  三、悲观情景（概率 20%）                                                 │
│  ────────────────────────────────────────────────────────────────────    │
│  触发条件：跌破{support:.2f}支撑位，MACD 死叉                                       │
│  目标价格：¥{support * 0.85:.2f}                                                           │
│  操作建议：减仓至 3 成以下，严格止损                                       │
│                                                                          │
│  四、风险收益比                                                          │
│  ────────────────────────────────────────────────────────────────────    │
│  预期收益：{((resistance - price) / price * 100):.1f}%（乐观情景）                                                │
│  预期损失：{((price - support * 0.85) / price * 100):.1f}%（悲观情景）                                                │
│  风险收益比：{((resistance - price) / (price - support * 0.85)):.2f}:1                                                   │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_risk_warning_detailed(self, data: Dict) -> str:
        """创建详细风险提示"""
        return """
┌──────────────────────────────────────────────────────────────────────────┐
│                           风 险 提 示                                    │
│                         RISK WARNING                                     │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、市场风险                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  □ 大盘系统性风险          风险等级：中高                                │
│  □ 行业政策变化风险          风险等级：中                                │
│  □ 市场流动性风险          风险等级：低                                │
│                                                                          │
│  二、个股风险                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  □ 业绩不及预期风险          风险等级：待评估                            │
│  □ 股东减持风险              风险等级：待评估                            │
│  □ 股权质押风险              风险等级：待评估                            │
│                                                                          │
│  三、技术风险                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  □ 技术指标失效风险          风险等级：中                                │
│  □ 数据延迟风险              风险等级：低                                │
│  □ 模型误差风险              风险等级：中                                │
│                                                                          │
│  四、操作风险                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  □ 仓位过重风险              风险等级：可控                              │
│  □ 止损不及时风险            风险等级：可控                              │
│  □ 追涨杀跌风险              风险等级：可控                              │
│                                                                          │
│  五、风险应对措施                                                        │
│  ────────────────────────────────────────────────────────────────────    │
│  1. 严格控制仓位，单只股票不超过总仓位的 20%                              │
│  2. 设置止损位，亏损达到 5% 坚决止损                                       │
│  3. 分散投资，不集中持有单一行业股票                                     │
│  4. 定期复盘，及时调整投资策略                                         │
│  5. 关注公告，及时获取公司信息                                         │
│                                                                          │
│  六、风险评级                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  综合风险等级：中等风险（R3）                                            │
│  适合投资者：稳健型及以上                                                │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    def _create_appendix(self, data: Dict) -> str:
        """创建报告附录"""
        return f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                           报 告 附 录                                    │
│                           APPENDIX                                       │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  一、数据来源                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  1. 实时行情：新浪财经 API                                               │
│  2. 技术指标：东方财富网 API                                             │
│  3. 新闻情绪：Firecrawl 网页抓取（可选）                                  │
│  4. 历史记忆：Elite Long-term Memory                                     │
│                                                                          │
│  二、分析方法                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  1. 技术分析：均线、MACD、RSI 等指标分析                                   │
│  2. 情绪分析：新闻文本 AI 情感分析                                         │
│  3. 综合评分：多维度加权评分模型                                         │
│                                                                          │
│  三、指标说明                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  MA：移动平均线，反映价格趋势                                           │
│  MACD：指数平滑异同移动平均线，反映趋势强弱                              │
│  RSI：相对强弱指标，反映超买超卖状态                                     │
│                                                                          │
│  四、报告生成信息                                                        │
│  ────────────────────────────────────────────────────────────────────    │
│  报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}                               │
│  报告生成系统：A 股专业分析系统 v2.6                                        │
│  数据截止时间：{str(data.get('time', 'N/A'))[:16]:>20}                               │
│                                                                          │
│  五、报告编号                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  ASHARE-{data.get('stock_code', '000000')}-{datetime.now().strftime("%Y%m%d")}                                                        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
"""

    # ========== 辅助方法 ==========

    def _calculate_score(self, data: Dict) -> float:
        """计算综合评分"""
        score = 5.0
        technical = data.get('technical', {})
        
        if technical.get('signal') == 'bullish':
            score += 1.5
        elif technical.get('signal') == 'bearish':
            score -= 1.5
        
        if technical.get('trend') == 'bullish':
            score += 0.5
        elif technical.get('trend') == 'bearish':
            score -= 0.5
        
        sentiment = data.get('news_sentiment', {})
        sentiment_score = sentiment.get('avg_sentiment_score', 0.5)
        score += (sentiment_score - 0.5) * 3
        
        change = data.get('change_percent', 0)
        if change > 3:
            score += 0.5
        elif change < -3:
            score -= 0.5
        
        return max(0, min(10, score))

    def _get_rating_label(self, score: float) -> str:
        """获取评级标签"""
        if score >= 8:
            return "强烈推荐"
        elif score >= 6:
            return "推荐"
        elif score >= 4:
            return "中性"
        elif score >= 2:
            return "谨慎"
        else:
            return "回避"

    def _get_rating_label_en(self, score: float) -> str:
        """获取英文评级"""
        if score >= 8:
            return "STRONG BUY"
        elif score >= 6:
            return "BUY"
        elif score >= 4:
            return "HOLD"
        elif score >= 2:
            return "CAUTION"
        else:
            return "AVOID"

    def _calculate_target_price(self, data: Dict) -> float:
        """计算目标价"""
        price = data.get('price', 0)
        tech = data.get('technical', {})
        resistance = tech.get('resistance', price * 1.1)
        return resistance

    def _calculate_stop_loss(self, data: Dict) -> float:
        """计算止损价"""
        price = data.get('price', 0)
        tech = data.get('technical', {})
        support = tech.get('support', price * 0.9)
        return support * 0.97

    def _get_ma_position(self, price: float, ma) -> str:
        """获取均线位置"""
        if ma == 'N/A' or ma == 0:
            return "N/A"
        return "上方" if price > ma else "下方"

    def _interpret_ma_arrangement(self, arrangement: str) -> str:
        """解读均线排列"""
        interpretations = {
            '多头排列': '均线呈多头排列，上涨趋势明确，建议持股待涨',
            '空头排列': '均线呈空头排列，下跌趋势明确，建议谨慎观望',
            '震荡整理': '均线纠缠，方向不明，建议等待突破信号',
        }
        return interpretations.get(arrangement, '数据不足，无法判断')

    def _interpret_macd(self, macd: Dict) -> str:
        """解读 MACD"""
        signal = macd.get('signal', '')
        interpretations = {
            'bullish': 'MACD 金叉，多头强势，建议关注',
            'bearish': 'MACD 死叉，空头强势，建议谨慎',
            'golden_cross': 'MACD 金叉买入信号，可考虑介入',
            'dead_cross': 'MACD 死叉卖出信号，建议减仓',
        }
        return interpretations.get(signal, '信号不明，建议观望')

    def _get_rsi_status(self, rsi) -> str:
        """获取 RSI 状态"""
        if rsi == 'N/A':
            return "N/A"
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

    def _interpret_rsi(self, rsi) -> str:
        """解读 RSI"""
        if rsi == 'N/A':
            return "数据不足"
        if rsi >= 80:
            return "RSI 严重超买，警惕回调风险，建议减仓"
        elif rsi >= 70:
            return "RSI 超买，短期可能回调，建议谨慎"
        elif rsi >= 50:
            return "RSI 偏强，上涨动能充足，可继续持有"
        elif rsi >= 30:
            return "RSI 偏弱，下跌动能释放，建议观望"
        else:
            return "RSI 超卖，可能反弹，可关注"

    def _interpret_volume_ratio(self, volume_ratio) -> str:
        """解读量比"""
        if volume_ratio == 'N/A':
            return "数据不足"
        if volume_ratio > 2:
            return "成交量明显放大，资金活跃，关注持续性"
        elif volume_ratio > 1:
            return "成交量温和放大，资金流入，健康状态"
        elif volume_ratio > 0.5:
            return "成交量正常，市场平稳"
        else:
            return "成交量萎缩，市场清淡，观望为主"

    def _interpret_support_resistance(self, tech: Dict) -> str:
        """解读支撑阻力"""
        support = tech.get('support', 0)
        resistance = tech.get('resistance', 0)
        price = tech.get('current_price', 0)
        
        if price > resistance * 0.95:
            return "价格接近阻力位，关注突破情况，突破可加仓"
        elif price < support * 1.05:
            return "价格接近支撑位，关注支撑有效性，破位需止损"
        else:
            return "价格在支撑阻力之间，可区间操作"

    def _calculate_technical_score(self, tech: Dict) -> int:
        """计算技术评分"""
        score = 50
        
        if tech.get('signal') == 'bullish':
            score += 20
        elif tech.get('signal') == 'bearish':
            score -= 20
        
        if tech.get('trend') == 'bullish':
            score += 15
        elif tech.get('trend') == 'bearish':
            score -= 15
        
        rsi = tech.get('rsi', 50)
        if 40 <= rsi <= 60:
            score += 10
        elif rsi > 70 or rsi < 30:
            score -= 10
        
        return max(0, min(100, score))

    def _get_technical_rating(self, tech: Dict) -> str:
        """获取技术评级"""
        score = self._calculate_technical_score(tech)
        if score >= 80:
            return "强势（建议积极操作）"
        elif score >= 60:
            return "偏强（建议适度参与）"
        elif score >= 40:
            return "中性（建议观望）"
        elif score >= 20:
            return "偏弱（建议谨慎）"
        else:
            return "弱势（建议回避）"

    def _interpret_sentiment(self, sentiment: Dict) -> str:
        """解读情绪"""
        score = sentiment.get('avg_sentiment_score', 0.5)
        if score >= 0.7:
            return "情绪积极，新闻面利好，可增强持股信心"
        elif score >= 0.5:
            return "情绪中性，新闻面平淡，以技术面为主"
        else:
            return "情绪消极，新闻面利空，建议谨慎"

    def _generate_core_view(self, data: Dict) -> str:
        """生成核心观点"""
        score = self._calculate_score(data)
        if score >= 7:
            return "技术面与情绪面共振向好，建议积极关注，逢低布局"
        elif score >= 5:
            return "整体表现平稳，建议适度参与，注意仓位控制"
        else:
            return "多项指标走弱，建议谨慎观望，等待企稳信号"

    def _generate_operation_advice(self, data: Dict) -> str:
        """生成操作建议"""
        score = self._calculate_score(data)
        if score >= 8:
            return "建议买入，仓位 7-8 成，目标价见阻力位"
        elif score >= 6:
            return "建议增持，仓位 5-6 成，波段操作"
        elif score >= 4:
            return "建议观望，仓位 3-4 成，等待信号"
        else:
            return "建议减仓，仓位 1-2 成，控制风险"

    def _get_operation_suggestion(self, score: float) -> str:
        """获取操作建议"""
        if score >= 8:
            return "积极买入，逢低布局"
        elif score >= 6:
            return "适度增持，波段操作"
        elif score >= 4:
            return "保持观望，等待信号"
        elif score >= 2:
            return "谨慎减持，控制仓位"
        else:
            return "建议回避，等待企稳"

    def _get_position_suggestion(self, score: float) -> str:
        """获取仓位建议"""
        if score >= 8:
            return "建议仓位 7-8 成，可积极操作"
        elif score >= 6:
            return "建议仓位 5-6 成，适度参与"
        elif score >= 4:
            return "建议仓位 3-4 成，保持灵活"
        elif score >= 2:
            return "建议仓位 1-2 成，控制风险"
        else:
            return "建议仓位 0-1 成，观望为主"

    def _get_detailed_strategy(self, score: float, tech: Dict) -> str:
        """获取详细策略"""
        support = tech.get('support', 0)
        resistance = tech.get('resistance', 0)
        
        if score >= 7:
            return f"突破{resistance:.2f}加仓，回调{support:.2f}不破持有，止损设{support * 0.97:.2f}"
        elif score >= 5:
            return f"{support:.2f}-{resistance:.2f}区间操作，突破跟进，破位止损"
        else:
            return f"反弹{resistance:.2f}减仓，跌破{support:.2f}止损，观望为主"

    def _interpret_market_data(self, data: Dict) -> str:
        """解读行情数据"""
        change = data.get('change_percent', 0)
        volume_ratio = data.get('technical', {}).get('volume_ratio', 1)
        
        if change > 3 and volume_ratio > 1.5:
            return "放量上涨，资金积极入场，上涨动能充足"
        elif change > 3:
            return "缩量上涨，上涨动能待确认，关注成交量"
        elif change < -3 and volume_ratio > 1.5:
            return "放量下跌，资金出逃明显，注意风险"
        elif change < -3:
            return "缩量下跌，下跌动能有限，关注支撑"
        else:
            return "震荡整理，方向不明，等待突破信号"

    def _generate_price_history_table(self, history: Dict) -> str:
        """生成价格历史表格"""
        price_history = history.get('price_history', [])
        if not price_history:
            return "暂无历史价格数据"
        
        lines = []
        for item in price_history[-5:]:
            date = item.get('date', 'N/A')
            price = item.get('price', 0)
            lines.append(f"  {date:<12}  ¥{price:>10.2f}")
        
        return "\n".join(lines) if lines else "暂无数据"

    def save_report(self, report: str, stock_code: str, stock_name: str) -> str:
        """保存报告到文件（按股票代码分类存储）"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 创建股票代码二级目录
        stock_dir = os.path.join(self.output_dir, stock_code)
        os.makedirs(stock_dir, exist_ok=True)
        
        # 保存报告到股票代码目录
        filename = f"{stock_code}_{stock_name}_{timestamp}_DETAILED.md"
        filepath = os.path.join(stock_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"详细报告已保存：{filepath}")
        return filepath


if __name__ == "__main__":
    # 测试
    test_data = {
        "stock_code": "600619",
        "stock_name": "海立股份",
        "price": 18.99,
        "change": 0.24,
        "change_percent": 1.28,
        "open": 18.67,
        "high": 18.99,
        "low": 18.43,
        "pre_close": 18.75,
        "volume": "2174.12 万手",
        "amount": "4.08 亿元",
        "time": "2026-03-01 12:06:41",
        "technical": {
            "signal": "bullish",
            "trend": "neutral",
            "ma": {5: 18.68, 10: 18.53, 20: 18.85, 60: 20.25},
            "ma_arrangement": "震荡整理",
            "macd": {"dif": -0.4622, "dea": -0.5699, "macd": 0.2155, "signal": "golden_cross"},
            "rsi": 53.23,
            "volume_ratio": 1.24,
            "support": 18.02,
            "resistance": 18.99
        },
        "news_sentiment": {
            "avg_sentiment_score": 0.5,
            "overall_sentiment": "UNKNOWN"
        }
    }
    
    generator = AShareDetailedReport()
    report = generator.generate_report(test_data)
    filepath = generator.save_report(report, "600619", "海立股份")
    print(f"报告已保存：{filepath}")
