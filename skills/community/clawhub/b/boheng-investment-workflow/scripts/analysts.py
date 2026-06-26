#!/usr/bin/env python3
"""
投资研究系统 - 8位分析师模块
每位分析师独立分析并给出投资建议（使用真实财务数据）
"""
from typing import Dict, List, Tuple
from datetime import datetime
import sys
import os

try:
    from config import ANALYST_WEIGHTS, VOTE_BUY, VOTE_CAUTION, VOTE_SELL
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from config import ANALYST_WEIGHTS, VOTE_BUY, VOTE_CAUTION, VOTE_SELL

# 导入动态ROE评估器
try:
    from roe_evaluator import evaluate_roe_dynamic, get_industry_roe_benchmark
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from roe_evaluator import evaluate_roe_dynamic, get_industry_roe_benchmark
    except ImportError:
        # 降级方案：使用简单的固定阈值
        evaluate_roe_dynamic = None
        get_industry_roe_benchmark = lambda x: 10.0


class BaseAnalyst:
    """分析师基类"""
    
    def __init__(self, name: str, weight: float = 1.0):
        self.name = name
        self.weight = weight
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        """
        分析股票并给出建议
        
        Args:
            quote: 行情数据
            financial: 财务数据（来自 financial_data.py）
            
        Returns:
            (投票结果, 分析理由)
        """
        raise NotImplementedError


class MacroAnalyst(BaseAnalyst):
    """宏观经济分析师"""
    
    def __init__(self):
        super().__init__("宏观经济分析师", ANALYST_WEIGHTS.get("宏观经济分析师", 1.0))
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 获取关键数据
        change_pct = quote.get('涨跌幅', 0)
        name = quote.get('名称', '该股票')
        code = quote.get('代码', '')
        price = quote.get('现价', 0)
        
        # 确保是数值类型
        if isinstance(change_pct, str):
            change_pct = float(change_pct.replace('%', '').replace('+', ''))
        elif change_pct is None:
            change_pct = 0
        
        # 获取财务和估值数据
        fi = financial.get('财务指标', {}) if financial else {}
        ev = financial.get('估值', {}) if financial else {}
        industry_data = financial.get('行业', {}) if financial else {}
        
        # 提取关键指标
        roe = fi.get('ROE', 0)
        pe = ev.get('PE_TTM', 0)
        pb = ev.get('PB', 0)
        industry = industry_data.get('行业', '未知')
        
        # 生成个性化分析
        # 1. 市场情绪判断
        if change_pct > 3:
            sentiment = "市场情绪过热"
        elif change_pct < -3:
            sentiment = "市场情绪低迷"
        else:
            sentiment = "市场情绪平稳"
        
        # 2. 基本面评估 - 使用动态ROE评估
        if roe and roe > 0:
            # 获取财报季度（从financial数据中获取）
            quarter = financial.get('report_period', {}).get('quarter', 4) if financial else 4
            industry = financial.get('行业', {}).get('行业', '综合') if financial else '综合'
            
            # 使用动态ROE评估
            if evaluate_roe_dynamic:
                roe_result = evaluate_roe_dynamic(roe, industry, quarter)
                roe_comment = roe_result.get('reason', f"ROE {roe:.1f}%")
            else:
                # 降级方案
                industry_benchmark = get_industry_roe_benchmark(industry)
                if roe >= industry_benchmark * 1.2:
                    roe_comment = f"ROE {roe:.1f}%，高于行业平均({industry_benchmark}%)"
                elif roe >= industry_benchmark:
                    roe_comment = f"ROE {roe:.1f}%，接近行业平均({industry_benchmark}%)"
                else:
                    roe_comment = f"ROE {roe:.1f}%，低于行业平均({industry_benchmark}%)"
        else:
            roe_comment = "ROE数据异常"
        
        # 3. 估值评估
        if pe and pe > 0:
            if pe < 15:
                pe_comment = f"PE={pe:.1f}倍，估值较低"
            elif pe < 30:
                pe_comment = f"PE={pe:.1f}倍，估值合理"
            else:
                pe_comment = f"PE={pe:.1f}倍，估值偏高"
        else:
            pe_comment = "估值数据获取失败"
        
        # 4. 行业特性
        industry_comments = {
            "银行": "银行业发展受货币政策和利率环境影响较大，当前利率环境相对稳定",
            "房地产": "房地产行业受宏观调控和信贷政策影响明显，需关注政策变化",
            "医药": "医药行业具备防御性，受医保政策和人口老龄化支撑",
            "消费": "消费行业与居民收入和消费意愿密切相关，关注消费复苏进度",
            "科技": "科技行业创新驱动强，但估值波动较大",
            "新能源": "新能源行业政策支持力度大，但竞争激烈",
            "电力": "电力行业稳定但受电价政策影响",
            "钢铁": "钢铁行业受宏观经济和基建投资影响较大",
            "汽车": "汽车行业受消费政策和市场竞争影响",
        }
        industry_comment = industry_comments.get(industry, f"{industry}行业需关注其特定的市场环境和政策因素")
        
        # 5. 综合投票逻辑
        vote = VOTE_CAUTION
        score = 0
        
        # 基本面加分 - 使用动态ROE评估
        if roe and roe > 0:
            quarter = financial.get('report_period', {}).get('quarter', 4) if financial else 4
            industry = financial.get('行业', {}).get('行业', '综合') if financial else '综合'
            
            if evaluate_roe_dynamic:
                roe_result = evaluate_roe_dynamic(roe, industry, quarter)
                roe_score = roe_result.get('score', 0)
                if roe_score >= 80:
                    score += 2
                elif roe_score >= 60:
                    score += 1
            else:
                # 降级方案：使用行业基准
                industry_benchmark = get_industry_roe_benchmark(industry)
                if roe >= industry_benchmark * 1.2:
                    score += 2
                elif roe >= industry_benchmark:
                    score += 1
        
        # 估值加分
        if pe and 0 < pe < 20:
            score += 2
        elif pe and 20 <= pe < 40:
            score += 1
        elif pe and pe >= 60:
            score -= 2
        
        # 市场情绪调整
        if abs(change_pct) < 3:
            score += 1
        elif abs(change_pct) > 5:
            score -= 1
        
        if score >= 3:
            vote = VOTE_BUY
        elif score <= -1:
            vote = VOTE_SELL
        
        # 生成个性化理由
        reason = f"{sentiment}，{name}（{code}）当前价格¥{price}。{roe_comment}，{pe_comment}。{industry_comment}。综合评分{score}分，{('建议买入' if vote == VOTE_BUY else '建议观望' if vote == VOTE_CAUTION else '建议回避')}。"
        
        return vote, reason


class IndustryAnalyst(BaseAnalyst):
    """行业研究员"""
    
    def __init__(self):
        super().__init__("行业研究员", ANALYST_WEIGHTS.get("行业研究员", 1.5))
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 使用真实行业数据
        industry_data = financial.get('行业', {}) if financial else {}
        
        # 检查是否有有效的行业数据
        if 'error' in industry_data or not industry_data.get('行业') or industry_data.get('行业') == '未知':
            # 无行业数据时的默认判断
            name = quote.get('名称', '')
            return self._fallback_analyze(name)
        
        industry = industry_data.get('行业', '未知')
        industry_change = industry_data.get('行业涨跌幅', 0)
        industry_rank = industry_data.get('行业排名', 0)
        total_industries = industry_data.get('行业总数', 0)
        sentiment = industry_data.get('行业景气度', '中')
        
        if sentiment == '高':
            vote = VOTE_BUY
            reason = f"所属【{industry}】行业景气度高，行业涨幅{industry_change:+.2f}%，排名第{industry_rank}/{total_industries}。行业处于成长期，市场空间广阔，政策支持力度大。"
        elif sentiment == '低':
            vote = VOTE_SELL
            reason = f"所属【{industry}】行业景气度低，行业涨幅{industry_change:+.2f}%，排名靠后。行业处于调整期，建议规避或等待行业拐点。"
        else:
            vote = VOTE_CAUTION
            reason = f"所属【{industry}】行业景气度中等，行业涨幅{industry_change:+.2f}%。行业处于成熟期，增长空间有限，需关注行业竞争格局变化。"
        
        return vote, reason
    
    def _fallback_analyze(self, name: str) -> Tuple[str, str]:
        """无行业数据时的备用判断"""
        if '银行' in name:
            return VOTE_CAUTION, "所属银行业景气度中等，息差收窄但资产质量改善，需关注经济周期影响。"
        elif '核电' in name or '电力' in name:
            return VOTE_BUY, "所属电力行业景气度稳定，新能源转型带来增长机遇，政策支持力度大。"
        elif '家电' in name:
            return VOTE_CAUTION, "所属家电行业景气度中等，内需疲软但出口增长，需关注消费复苏节奏。"
        elif '永强' in name:
            return VOTE_CAUTION, "所属【家用轻工】行业景气度中等，户外休闲家具行业增长平稳，需关注海外市场需求。"
        else:
            return VOTE_CAUTION, "行业景气度需进一步分析，建议关注行业政策变化。"


class FundamentalAnalyst(BaseAnalyst):
    """基本面分析师"""
    
    def __init__(self):
        super().__init__("基本面分析师", ANALYST_WEIGHTS.get("基本面分析师", 1.5))
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 使用真实财务数据
        fi = financial.get('财务指标', {}) if financial else {}
        
        if 'error' in fi:
            return self._fallback_analyze(quote.get('名称', ''))
        
        # 提取关键指标
        roe = fi.get('ROE', 0)
        gross_margin = fi.get('毛利率', 0)
        net_margin = fi.get('净利率', 0)
        revenue_growth = fi.get('营收增速', 0)
        profit_growth = fi.get('利润增速', 0)
        debt_ratio = fi.get('资产负债率', 0)
        current_ratio = fi.get('流动比率', 0)
        ocf_ratio = fi.get('经营现金流/营收', 0)
        
        # 获取行业和财报季度信息
        industry_data = financial.get('行业', {}) if financial else {}
        industry = industry_data.get('行业', '综合') if industry_data else '综合'
        report_period = financial.get('report_period', {}) if financial else {}
        quarter = report_period.get('quarter', 4) if report_period else 4
        
        # 计算基本面评分 - 传入行业和季度用于动态ROE评估
        score = self._calculate_score(
            roe, gross_margin, revenue_growth, profit_growth, 
            debt_ratio, current_ratio, ocf_ratio,
            industry=industry, quarter=quarter
        )
        
        if score >= 70:
            vote = VOTE_BUY
            reason = f"基本面优秀：ROE {roe:.1f}%，毛利率{gross_margin:.1f}%，净利率{net_margin:.1f}%。营收增速{revenue_growth:.1f}%，利润增速{profit_growth:.1f}%。资产负债率{debt_ratio:.1f}%，流动比率{current_ratio:.2f}。经营现金流/营收{ocf_ratio:.1f}%，现金流健康。护城河稳固，具备长期投资价值。"
        elif score >= 50:
            vote = VOTE_CAUTION
            reason = f"基本面一般：ROE {roe:.1f}%，毛利率{gross_margin:.1f}%。营收增速{revenue_growth:.1f}%，利润增速{profit_growth:.1f}%。资产负债率{debt_ratio:.1f}%。需关注业绩增长持续性，建议等待业绩拐点确认。"
        else:
            vote = VOTE_SELL
            reason = f"基本面较差：ROE {roe:.1f}%偏低，毛利率{gross_margin:.1f}%下滑。营收增速{revenue_growth:.1f}%，利润增速{profit_growth:.1f}%。资产负债率{debt_ratio:.1f}%偏高。盈利能力下滑，现金流承压，建议规避。"
        
        return vote, reason
    
    def _calculate_score(self, roe, gross_margin, revenue_growth, profit_growth, 
                         debt_ratio, current_ratio, ocf_ratio, industry="综合", quarter=4) -> float:
        """
        计算基本面评分 - 使用动态ROE评估
        
        Args:
            industry: 行业名称
            quarter: 财报季度 (1/2/3/4)
        """
        score = 0
        
        # ROE评分（权重30%）- 使用动态评估
        if evaluate_roe_dynamic and roe and roe > 0:
            roe_result = evaluate_roe_dynamic(roe, industry, quarter)
            roe_score = roe_result.get('score', 0)
            score += roe_score * 0.3  # 30%权重对应30分
        else:
            # 降级方案：使用行业基准
            industry_benchmark = get_industry_roe_benchmark(industry)
            if roe >= industry_benchmark * 1.3:
                score += 30
            elif roe >= industry_benchmark:
                score += 20
            elif roe >= industry_benchmark * 0.7:
                score += 10
        
        # 毛利率评分（权重20%）
        if gross_margin >= 40:
            score += 20
        elif gross_margin >= 25:
            score += 15
        elif gross_margin >= 15:
            score += 10
        
        # 增长评分（权重20%）
        avg_growth = (revenue_growth + profit_growth) / 2
        if avg_growth >= 20:
            score += 20
        elif avg_growth >= 10:
            score += 15
        elif avg_growth >= 0:
            score += 10
        
        # 偿债能力评分（权重15%）
        if debt_ratio < 40 and current_ratio >= 1.5:
            score += 15
        elif debt_ratio < 60 and current_ratio >= 1:
            score += 10
        elif debt_ratio < 75:
            score += 5
        
        # 现金流评分（权重15%）
        if ocf_ratio >= 20:
            score += 15
        elif ocf_ratio >= 10:
            score += 10
        elif ocf_ratio >= 0:
            score += 5
        
        return score
    
    def _fallback_analyze(self, name: str) -> Tuple[str, str]:
        """无财务数据时的备用判断"""
        return VOTE_CAUTION, "财务数据获取失败，无法进行基本面分析，建议谨慎观望。"


class TechnicalAnalyst(BaseAnalyst):
    """技术分析师"""
    
    def __init__(self):
        super().__init__("技术分析师", ANALYST_WEIGHTS.get("技术分析师", 1.0))
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 使用真实技术指标数据
        tech = financial.get('技术指标', {}) if financial else {}
        
        if 'error' in tech:
            return self._fallback_analyze(quote)
        
        # 确保价格是数值
        def safe_float(val):
            if isinstance(val, str):
                try:
                    return float(val.replace('¥', '').replace(',', ''))
                except:
                    return 0
            return float(val) if val is not None else 0
        
        price = safe_float(tech.get('收盘价', quote.get('现价', 0)))
        ma5 = tech.get('MA5', 0)
        ma10 = tech.get('MA10', 0)
        ma20 = tech.get('MA20', 0)
        macd = tech.get('MACD', 0)
        rsi = tech.get('RSI', 50)
        ma_cross = tech.get('MA金叉', False)
        macd_cross = tech.get('MACD金叉', False)
        rsi_overbuy = tech.get('RSI超买', False)
        rsi_oversell = tech.get('RSI超卖', False)
        
        # 技术信号判断
        signals = []
        
        if ma_cross:
            signals.append("MA金叉")
        if macd_cross:
            signals.append("MACD金叉")
        if rsi_oversell:
            signals.append("RSI超卖")
        if rsi_overbuy:
            signals.append("RSI超买")
        
        # 趋势判断
        if price > ma5 and price > ma20:
            trend = "上升趋势"
        elif price < ma5 and price < ma20:
            trend = "下降趋势"
        else:
            trend = "震荡整理"
        
        # 综合判断
        positive_signals = ma_cross or macd_cross or rsi_oversell
        negative_signals = rsi_overbuy
        
        if positive_signals and not negative_signals:
            vote = VOTE_BUY
            reason = f"技术面偏强：{trend}，当前价格¥{price:.2f}。MA5={ma5:.2f}，MA20={ma20:.2f}。RSI={rsi:.1f}。出现买入信号：{', '.join(signals) if signals else '趋势向上'}。建议顺势参与。"
        elif negative_signals:
            vote = VOTE_CAUTION
            reason = f"技术面偏弱：{trend}，当前价格¥{price:.2f}。RSI={rsi:.1f}超买。出现卖出信号：{', '.join(signals)}。建议等待回调。"
        else:
            vote = VOTE_CAUTION
            reason = f"技术面中性：{trend}，当前价格¥{price:.2f}。MA5={ma5:.2f}，MA20={ma20:.2f}。RSI={rsi:.1f}。方向不明，建议等待突破信号。"
        
        return vote, reason
    
    def _fallback_analyze(self, quote: Dict) -> Tuple[str, str]:
        """无技术数据时的备用判断"""
        change_pct = quote.get('涨跌幅', 0)
        if isinstance(change_pct, str):
            try:
                change_pct = float(change_pct.replace('%', '').replace('+', ''))
            except:
                change_pct = 0
        
        price = quote.get('现价', 0)
        if isinstance(price, str):
            try:
                price = float(price.replace('¥', '').replace(',', ''))
            except:
                price = 0
        
        if change_pct > 5:
            return VOTE_CAUTION, f"短期涨幅过大（+{change_pct}%），技术指标可能超买，存在回调压力。"
        elif change_pct > 2:
            return VOTE_BUY, f"股价走势强劲（+{change_pct}%），短期趋势向上，可适当参与。"
        elif change_pct < -3:
            return VOTE_CAUTION, f"股价下跌（{change_pct}%），技术形态走弱，建议观望。"
        else:
            return VOTE_CAUTION, f"股价震荡整理，当前¥{price:.2f}，方向不明。"


class RiskAnalyst(BaseAnalyst):
    """风险控制师"""
    
    def __init__(self):
        super().__init__("风险控制师", ANALYST_WEIGHTS.get("风险控制师", 1.2))
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 综合风险评估
        risks = []
        risk_level = "低"
        
        # 波动风险
        change_pct = quote.get('涨跌幅', 0)
        if isinstance(change_pct, str):
            try:
                change_pct = float(change_pct.replace('%', '').replace('+', ''))
            except:
                change_pct = 0
        
        if abs(change_pct) > 5:
            risks.append("波动风险较高")
            risk_level = "中"
        
        # 财务风险
        fi = financial.get('财务指标', {}) if financial else {}
        if 'error' not in fi:
            debt_ratio = fi.get('资产负债率', 0)
            if debt_ratio > 70:
                risks.append("财务杠杆风险")
                risk_level = "高"
            
            ocf_ratio = fi.get('经营现金流/营收', 0)
            if ocf_ratio < 0:
                risks.append("现金流风险")
                risk_level = "高"
        
        # 估值风险
        ev = financial.get('估值分位', {}) if financial else {}
        if 'error' not in ev:
            pe_percentile = ev.get('PE分位', 50)
            if pe_percentile > 80:
                risks.append("估值偏高风险")
                risk_level = "高"
        
        # 系统性风险
        risks.append("市场系统性风险")
        
        # 给出建议
        if risk_level == "高":
            vote = VOTE_SELL
            reason = f"风险等级：高。主要风险：{', '.join(risks)}。建议仓位控制在10%以内，设置8%止损线。谨慎参与。"
        elif risk_level == "中":
            vote = VOTE_CAUTION
            reason = f"风险等级：中。主要风险：{', '.join(risks)}。建议仓位控制在20%以内，设置10%止损线。"
        else:
            vote = VOTE_BUY
            reason = f"风险等级：低。主要风险：{', '.join(risks)}。建议仓位可放宽至30%，设置12%止损线。"
        
        return vote, reason


class QuantAnalyst(BaseAnalyst):
    """量化分析师"""
    
    def __init__(self):
        super().__init__("量化分析师", ANALYST_WEIGHTS.get("量化分析师", 1.0))
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 量化因子分析
        momentum_score = 50
        value_score = 50
        quality_score = 50
        
        # 动量因子
        change_pct = quote.get('涨跌幅', 0)
        if isinstance(change_pct, str):
            try:
                change_pct = float(change_pct.replace('%', '').replace('+', ''))
            except:
                change_pct = 0
        momentum_score = 50 + change_pct * 5
        
        # 价值因子
        ev = financial.get('估值分位', {}) if financial else {}
        if 'error' not in ev:
            pe_percentile = ev.get('PE分位', 50)
            value_score = 100 - pe_percentile  # PE分位越低越好
        
        # 质量因子
        fi = financial.get('财务指标', {}) if financial else {}
        if 'error' not in fi:
            roe = fi.get('ROE', 0)
            gross_margin = fi.get('毛利率', 0)
            quality_score = min(100, roe * 3 + gross_margin)
        
        # 综合得分
        total_score = momentum_score * 0.3 + value_score * 0.3 + quality_score * 0.4
        
        if total_score >= 65:
            vote = VOTE_BUY
            reason = f"量化综合得分：{total_score:.1f}分。动量因子{momentum_score:.1f}，价值因子{value_score:.1f}，质量因子{quality_score:.1f}。多因子模型显示正向信号，建议参与。"
        elif total_score >= 50:
            vote = VOTE_CAUTION
            reason = f"量化综合得分：{total_score:.1f}分。动量因子{momentum_score:.1f}，价值因子{value_score:.1f}，质量因子{quality_score:.1f}。因子信号中性，建议观望。"
        else:
            vote = VOTE_SELL
            reason = f"量化综合得分：{total_score:.1f}分。动量因子{momentum_score:.1f}，价值因子{value_score:.1f}，质量因子{quality_score:.1f}。因子信号偏负面，建议规避。"
        
        return vote, reason


class SentimentAnalyst(BaseAnalyst):
    """情绪分析师"""
    
    def __init__(self):
        super().__init__("情绪分析师", ANALYST_WEIGHTS.get("情绪分析师", 0.8))
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 1. 首先分析资金流向情绪
        flow = financial.get('资金流向', {}) if financial else {}
        
        if 'error' in flow:
            # 无资金数据时，使用新闻数据分析
            return self._news_only_analyze(quote, news_data)
        
        main_flow = flow.get('主力净流入', 0) or 0
        five_day_flow = flow.get('5日主力净流入', 0) or 0
        
        # 2. 分析新闻情绪
        news_sentiment = ""
        news_info = ""
        if news_data and len(news_data) > 0:
            positive = sum(1 for n in news_data if n.get('sentiment') == 'positive')
            negative = sum(1 for n in news_data if n.get('sentiment') == 'negative')
            neutral = sum(1 for n in news_data if n.get('sentiment') == 'neutral')
            total = len(news_data)
            
            if positive > negative and positive >= total * 0.4:
                news_sentiment = "偏正面"
            elif negative > positive and negative >= total * 0.4:
                news_sentiment = "偏负面"
            elif neutral >= total * 0.6:
                news_sentiment = "中性"
            else:
                news_sentiment = "分化"
            
            # 获取最新新闻
            latest = news_data[0].get('title', '')[:35] if news_data else ''
            news_info = f"。新闻情绪{news_sentiment}（最新：「{latest}...」）"
        
        # 3. 综合判断
        if main_flow > 0 and five_day_flow > 0:
            sentiment = "乐观"
            vote = VOTE_BUY
            reason = f"市场情绪：{sentiment}。主力资金今日净流入{main_flow/10000:.1f}万，5日累计净流入{five_day_flow/10000:.1f}万。资金流入积极{news_info}可适当参与。"
        elif main_flow < 0 and five_day_flow < 0:
            sentiment = "恐惧"
            vote = VOTE_CAUTION
            reason = f"市场情绪：{sentiment}。主力资金今日净流出{abs(main_flow)/10000:.1f}万，5日累计净流出{abs(five_day_flow)/10000:.1f}万。恐慌情绪蔓延{news_info}建议分批建仓。"
        else:
            sentiment = "中性"
            vote = VOTE_CAUTION
            reason = f"市场情绪：{sentiment}。主力资金今日净流入{main_flow/10000:.1f}万。观望情绪浓厚{news_info}建议等待方向明确。"
        
        return vote, reason
    
    def _news_only_analyze(self, quote: Dict, news_data: List[Dict] = None) -> Tuple[str, str]:
        """无资金数据时，仅根据新闻分析"""
        if not news_data or len(news_data) == 0:
            return self._fallback_analyze(quote)
        
        positive = sum(1 for n in news_data if n.get('sentiment') == 'positive')
        negative = sum(1 for n in news_data if n.get('sentiment') == 'negative')
        total = len(news_data)
        
        latest = news_data[0].get('title', '')[:40] if news_data else ''
        
        if positive > negative and positive >= total * 0.4:
            return VOTE_BUY, f"市场情绪：乐观（基于新闻分析）。正面{positive}条，负面{negative}条。最新：「{latest}...」新闻面偏多，可适当关注。"
        elif negative > positive and negative >= total * 0.4:
            return VOTE_CAUTION, f"市场情绪：谨慎（基于新闻分析）。正面{positive}条，负面{negative}条。最新：「{latest}...」新闻面偏空，建议观望。"
        else:
            return VOTE_CAUTION, f"市场情绪：中性（基于新闻分析）。正面{positive}条，负面{negative}条。最新：「{latest}...」新闻面无明显方向，建议等待。"
    
    def _fallback_analyze(self, quote: Dict) -> Tuple[str, str]:
        """无资金数据时的备用判断"""
        change_pct = quote.get('涨跌幅', 0)
        if isinstance(change_pct, str):
            try:
                change_pct = float(change_pct.replace('%', '').replace('+', ''))
            except:
                change_pct = 0
        
        if change_pct > 5:
            return VOTE_SELL, f"市场情绪：极度贪婪。短期涨幅过大，投资者情绪亢奋，需警惕获利回吐。"
        elif change_pct > 2:
            return VOTE_BUY, f"市场情绪：乐观。股价上涨，市场信心增强。"
        elif change_pct < -3:
            return VOTE_CAUTION, f"市场情绪：恐惧。恐慌情绪蔓延，可能存在逆向机会。"
        else:
            return VOTE_CAUTION, f"市场情绪：中性。观望情绪浓厚。"




class ValuationAnalyst(BaseAnalyst):
    """估值分析师"""
    
    def __init__(self):
        super().__init__("估值分析师", ANALYST_WEIGHTS.get("估值分析师", 1.2))
    
    def calculate_target_prices(self, quote: Dict, financial: Dict = None) -> Dict:
        """
        计算目标价（方案B扩展）
        
        Returns:
            dict: {'pessimistic', 'neutral', 'optimistic', 'safety_margin', 'method'}
        """
        # 获取当前价格
        price = quote.get('现价', 0)
        if isinstance(price, str):
            try:
                price = float(price.replace('¥', '').replace(',', ''))
            except:
                price = 0
        
        if price <= 0:
            return None
        
        # 获取财务数据
        fi = financial.get('财务指标', {}) if financial else {}
        ev = financial.get('估值分位', {}) if financial else {}
        
        # 方法1：PE分位法
        pe_percentile = ev.get('PE分位', 50) if ev else 50
        pe_target = price * (pe_percentile / 50)  # 基于分位调整
        
        # 方法2：简化DCF法（基于ROE）
        roe = fi.get('ROE', 0) if fi else 0
        growth_rate = fi.get('利润增速', 5) / 100 if fi else 0.05
        if roe > 0 and growth_rate > 0:
            # 简化Gordon模型：价值 = ROE * (1+g) / (r-g)
            # 假设折现率r=10%，永续增长率g=3%
            dcf_value = (roe / 100) * (1 + growth_rate) / (0.10 - 0.03)
            dcf_target = price * dcf_value * 10  # 调整为相对价格
            # 限制波动范围
            dcf_target = max(price * 0.5, min(price * 2.0, dcf_target))
        else:
            dcf_target = price
        
        # 方法3：PEG法
        pe_current = ev.get('PE当前', 0) if ev else 0
        if pe_current > 0 and growth_rate > 0:
            peg = pe_current / (growth_rate * 100)  # 转为百分比
            # PEG=1为合理，<1为低估，>1为高估
            peg_target = price / peg if peg > 0 else price
            peg_target = max(price * 0.5, min(price * 2.0, peg_target))
        else:
            peg_target = price
        
        # 综合目标价（三种方法平均）
        neutral_target = (pe_target + dcf_target + peg_target) / 3
        
        # 计算三个目标价
        pessimistic = round(neutral_target * 0.7, 2)   # -30%
        optimistic = round(neutral_target * 1.3, 2)    # +30%
        neutral = round(neutral_target, 2)
        
        # 安全边际
        safety_margin = round((price - neutral) / neutral * 100, 2)
        
        return {
            'pessimistic': pessimistic,
            'neutral': neutral,
            'optimistic': optimistic,
            'safety_margin': safety_margin,
            'method': 'PE分位 + DCF + PEG 综合'
        }
    
    def analyze(self, quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> Tuple[str, str]:
        # 使用真实估值数据
        ev = financial.get('估值分位', {}) if financial else {}
        valuation = financial.get('估值', {}) if financial else {}
        
        if not ev or 'error' in ev:
            return self._fallback_analyze(quote, valuation)
        
        pe_current = ev.get('PE当前', 0)
        pe_percentile = ev.get('PE分位', 50)
        pb_current = ev.get('PB当前', 0)
        pb_percentile = ev.get('PB分位', 50)
        rating = ev.get('估值评级', '合理')
        
        # 股息率
        dv_ratio = valuation.get('股息率', 0) if 'error' not in valuation else 0
        
        # 计算目标价
        target_info = self.calculate_target_prices(quote, financial)
        
        if pe_percentile <= 30:
            vote = VOTE_BUY
            reason = f"估值水平：{pe_percentile}%分位，属于【{rating}】。PE {pe_current}倍，PB {pb_current}倍。股息率{dv_ratio:.1f}%。估值具备安全边际，适合长期持有。"
        elif pe_percentile <= 60:
            vote = VOTE_CAUTION
            reason = f"估值水平：{pe_percentile}%分位，属于【{rating}】。PE {pe_current}倍，PB {pb_current}倍。股息率{dv_ratio:.1f}%。估值合理但无显著优势，需关注业绩增长。"
        else:
            vote = VOTE_SELL
            reason = f"估值水平：{pe_percentile}%分位，属于【{rating}】。PE {pe_current}倍，PB {pb_current}倍。估值偏高，风险大于机会，建议等待估值回归。"
        
        # 添加目标价信息到理由中
        if target_info:
            target_line = f"\n\n🎯 目标价指导：悲观¥{target_info['pessimistic']}（-30%）| 中性¥{target_info['neutral']}（合理）| 乐观¥{target_info['optimistic']}（+30%）\n📊 当前安全边际：{target_info['safety_margin']}%{'（价格低于目标价，可买入）' if target_info['safety_margin'] > 0 else '（价格高于目标价，建议持有）'}"
            reason += target_line
        
        return vote, reason
    
    def _fallback_analyze(self, quote: Dict, valuation: Dict) -> Tuple[str, str]:
        """无估值分位数据时的备用判断"""
        if 'error' not in valuation:
            pe = valuation.get('PE_TTM', 0)
            pb = valuation.get('PB', 0)
            dv = valuation.get('股息率', 0)
            
            if pe < 15 and pb < 1.5:
                return VOTE_BUY, f"PE {pe}倍，PB {pb}倍，股息率{dv:.1f}%。估值偏低，具备安全边际。"
            elif pe < 30:
                return VOTE_CAUTION, f"PE {pe}倍，PB {pb}倍。估值合理，需关注业绩增长。"
            else:
                return VOTE_SELL, f"PE {pe}倍，估值偏高，建议谨慎。"
        
        return VOTE_CAUTION, "估值数据获取失败，无法进行估值分析。"


# 分析师注册表
ANALYSTS = [
    MacroAnalyst(),
    IndustryAnalyst(),
    FundamentalAnalyst(),
    TechnicalAnalyst(),
    RiskAnalyst(),
    QuantAnalyst(),
    SentimentAnalyst(),
    ValuationAnalyst(),
]


def run_all_analysts(quote: Dict, financial: Dict = None, news_data: List[Dict] = None) -> List[Dict]:
    """
    运行所有分析师并返回结果
    
    Args:
        quote: 股票行情数据
        financial: 财务数据（来自 financial_data.py）
        news_data: 新闻数据（传给情绪分析师）
        
    Returns:
        分析结果列表
    """
    results = []
    
    for analyst in ANALYSTS:
        # 所有分析师都需要接收news_data参数
        vote, reason = analyst.analyze(quote, financial, news_data)
        results.append({
            'name': analyst.name,
            'weight': analyst.weight,
            'vote': vote,
            'reason': reason
        })
    
    return results


def calculate_weighted_vote(results: List[Dict]) -> Tuple[str, float]:
    """
    计算加权投票结果
    
    Returns:
        (最终建议, 加权得分)
    """
    scores = {
        VOTE_BUY: 0.0,
        VOTE_CAUTION: 0.0,
        VOTE_SELL: 0.0
    }
    
    total_weight = 0.0
    
    for r in results:
        scores[r['vote']] += r['weight']
        total_weight += r['weight']
    
    # 归一化
    for k in scores:
        scores[k] = scores[k] / total_weight if total_weight > 0 else 0
    
    # 选择得分最高的
    final_vote = max(scores, key=scores.get)
    
    return final_vote, scores[final_vote]


if __name__ == "__main__":
    # 测试
    test_quote = {
        '代码': '600919',
        '名称': '江苏银行',
        '现价': 11.40,
        '涨跌幅': 0.35
    }
    
    test_financial = {
        '财务指标': {
            'ROE': 12.5,
            '毛利率': 45,
            '净利率': 28,
            '营收增速': 8,
            '利润增速': 12,
            '资产负债率': 92,
            '流动比率': 0.8,
            '经营现金流/营收': 25
        },
        '估值分位': {
            'PE当前': 5.8,
            'PE分位': 25,
            'PB当前': 0.65,
            '估值评级': '偏低'
        }
    }
    
    results = run_all_analysts(test_quote, test_financial)
    
    print("=" * 60)
    print("8位分析师投票结果")
    print("=" * 60)
    
    for r in results:
        print(f"{r['name']} → {r['vote']} (权重 {r['weight']}x)")
        print(f"   理由：{r['reason']}")
        print()
    
    final_vote, score = calculate_weighted_vote(results)
    print(f"最终建议：{final_vote} (得分：{score:.2%})")