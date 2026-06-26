#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务分析模块 - 分析公司财务报表数据，评估财务健康状况和成长性
"""

from typing import Dict, List, Tuple

class FinancialAnalyzer:
    def __init__(self):
        # 行业基准值（可根据具体行业调整）
        self.benchmarks = {
            'roe': 0.15,  # 15%以上为优秀
            'deduct_roe': 0.12,  # 扣非ROE 12%以上为优秀
            'gross_margin': 0.30,  # 毛利率30%以上为优秀
            'net_margin': 0.10,  # 净利率10%以上为优秀
            'asset_liability_ratio': 0.60,  # 资产负债率60%以下为安全
            'current_ratio': 1.5,  # 流动比率1.5以上为安全
            'quick_ratio': 1.0,  # 速动比率1.0以上为安全
            'cash_to_debt_ratio': 1.0,  # 现金短债比1.0以上为安全
            'net_profit_cash_ratio': 0.8,  # 净现比0.8以上为优秀
            'peg': 1.0,  # PEG 1.0以下为合理
            'rd_ratio': 0.05,  # 研发占比5%以上为优秀
            'revenue_growth': 0.10,  # 营收增速10%以上为成长型
            'profit_growth': 0.15,  # 利润增速15%以上为优秀
        }
    
    def analyze_financial_health(self, financial_data: Dict) -> Dict:
        """
        综合分析财务健康状况
        :param financial_data: 财务数据字典
        :return: 分析结果
        """
        ratios = financial_data.get('ratios', {})
        quarterly = financial_data.get('quarterly', {})
        annual = financial_data.get('annual', {})
        rd_expense = financial_data.get('rd_expense', {})
        
        analysis = {}
        
        # 1. 管理层分析
        management = financial_data.get('management', {})
        analysis['management'] = self._analyze_management(management)
        
        # 2. 战略分析
        analysis['strategy'] = self._analyze_strategy(management)
        
        # 3. 行业地位与护城河
        analysis['moat'] = self._analyze_moat(ratios)
        
        # 4. 营收增长分析
        analysis['revenue_growth'] = self._analyze_revenue_growth(quarterly, annual)
        
        # 5. 净利润增长分析
        analysis['profit_growth'] = self._analyze_profit_growth(quarterly, annual)
        
        # 6. ROE分析
        analysis['roe_analysis'] = self._analyze_roe(ratios)
        
        # 7. 扣非ROE分析
        analysis['deduct_roe_analysis'] = self._analyze_deduct_roe(ratios)
        
        # 8. 偿债能力分析
        analysis['debt_analysis'] = self._analyze_debt_solvency(ratios)
        
        # 9. 净现比分析
        analysis['cash_flow_quality'] = self._analyze_cash_flow_quality(ratios, quarterly)
        
        # 10. 研发支出分析
        analysis['rd_analysis'] = self._analyze_rd_expense(rd_expense)
        
        # 11. PEG分析
        analysis['peg_analysis'] = self._analyze_peg(ratios)
        
        # 12. 自由现金流分析
        analysis['fcf_analysis'] = self._analyze_free_cash_flow(ratios)
        
        # 综合评分
        analysis['overall_score'] = self._calculate_overall_score(analysis)
        analysis['overall_rating'] = self._get_rating(analysis['overall_score'])
        
        return analysis
    
    def _analyze_management(self, management: Dict) -> Dict:
        """分析管理层稳定性和展望"""
        stability = management.get('stability', 'unknown')
        outlook = management.get('outlook', 'neutral')
        recent_changes = management.get('recent_changes', [])
        
        stability_rating = '优秀' if stability == 'stable' else '一般' if stability == 'minor_changes' else '较差'
        
        return {
            'stability': stability,
            'stability_rating': stability_rating,
            'outlook': outlook,
            'recent_changes': recent_changes,
            'summary': f"管理层稳定性{stability_rating}，对未来展望{outlook}"
        }
    
    def _analyze_strategy(self, management: Dict) -> Dict:
        """分析公司战略方向变化"""
        strategy = management.get('strategy', '')
        # 这里可以更复杂，暂时简单处理
        return {
            'has_change': '变化' in strategy,
            'current_strategy': strategy,
            'market_rating': '正面',  # 可根据新闻调整
            'summary': f"当前战略：{strategy}，市场评价正面"
        }
    
    def _analyze_moat(self, ratios: Dict) -> Dict:
        """分析行业地位和产品护城河"""
        gross_margin = ratios.get('gross_margin', 0)
        net_margin = ratios.get('net_margin', 0)
        
        moat_level = '强' if gross_margin > 0.4 else '中等' if gross_margin > 0.3 else '弱'
        change_trend = '稳定'  # 可对比历史数据
        
        return {
            'gross_margin': gross_margin,
            'net_margin': net_margin,
            'moat_level': moat_level,
            'change_trend': change_trend,
            'summary': f"毛利率{gross_margin:.1%}，净利率{net_margin:.1%}，护城河{moat_level}"
        }
    
    def _analyze_revenue_growth(self, quarterly: Dict, annual: Dict) -> Dict:
        """分析营收增长情况"""
        quarterly_yoy = quarterly.get('revenue', {}).get('yoy_growth', 0)
        quarterly_qoq = quarterly.get('revenue', {}).get('qoq_growth', 0)
        annual_yoy = annual.get('revenue', {}).get('yoy_growth', 0)
        
        rating = '优秀' if quarterly_yoy > 0.2 else '良好' if quarterly_yoy > 0.1 else '一般' if quarterly_yoy > 0 else '较差'
        
        return {
            'quarterly_yoy': quarterly_yoy,
            'quarterly_qoq': quarterly_qoq,
            'annual_yoy': annual_yoy,
            'analyst_forecast': '预计未来12个月增长15-20%',  # 可接入分析师预测数据
            'rating': rating,
            'summary': f"季度营收同比增长{quarterly_yoy:.1%}，环比增长{quarterly_qoq:.1%}，年度增长{annual_yoy:.1%}，增长{rating}"
        }
    
    def _analyze_profit_growth(self, quarterly: Dict, annual: Dict) -> Dict:
        """分析净利润增长情况"""
        quarterly_yoy = quarterly.get('net_profit', {}).get('yoy_growth', 0)
        quarterly_qoq = quarterly.get('net_profit', {}).get('qoq_growth', 0)
        annual_yoy = annual.get('net_profit', {}).get('yoy_growth', 0)
        
        rating = '优秀' if quarterly_yoy > 0.3 else '良好' if quarterly_yoy > 0.15 else '一般' if quarterly_yoy > 0 else '较差'
        
        return {
            'quarterly_yoy': quarterly_yoy,
            'quarterly_qoq': quarterly_qoq,
            'annual_yoy': annual_yoy,
            'analyst_forecast': '预计未来12个月利润增长20-25%',  # 可接入分析师预测数据
            'rating': rating,
            'summary': f"季度净利润同比增长{quarterly_yoy:.1%}，环比增长{quarterly_qoq:.1%}，年度增长{annual_yoy:.1%}，增长{rating}"
        }
    
    def _analyze_roe(self, ratios: Dict) -> Dict:
        """分析ROE稳定性"""
        roe = ratios.get('roe', 0)
        roe_ttm = ratios.get('roe_ttm', 0)
        
        stability = '稳定' if abs(roe - roe_ttm) < 0.03 else '波动较大'
        rating = '优秀' if roe > 0.2 else '良好' if roe > 0.15 else '一般' if roe > 0.1 else '较差'
        
        return {
            'roe': roe,
            'roe_ttm': roe_ttm,
            'stability': stability,
            'rating': rating,
            'summary': f"ROE {roe:.1%}，TTM ROE {roe_ttm:.1%}，{stability}，{rating}"
        }
    
    def _analyze_deduct_roe(self, ratios: Dict) -> Dict:
        """分析扣非ROE表现"""
        deduct_roe = ratios.get('deduct_roe', 0)
        roe = ratios.get('roe', 0)
        
        quality = '高' if deduct_roe / roe > 0.9 else '中等' if deduct_roe / roe > 0.7 else '低'
        rating = '优秀' if deduct_roe > 0.15 else '良好' if deduct_roe > 0.1 else '一般' if deduct_roe > 0.05 else '较差'
        
        return {
            'deduct_roe': deduct_roe,
            'roe_ratio': deduct_roe / roe if roe > 0 else 0,
            'profit_quality': quality,
            'rating': rating,
            'summary': f"扣非ROE {deduct_roe:.1%}，占ROE比例{deduct_roe/roe:.1%}，利润质量{quality}，{rating}"
        }
    
    def _analyze_debt_solvency(self, ratios: Dict) -> Dict:
        """分析偿债能力"""
        asset_liability_ratio = ratios.get('asset_liability_ratio', 0)
        current_ratio = ratios.get('current_ratio', 0)
        quick_ratio = ratios.get('quick_ratio', 0)
        interest_bearing_debt = ratios.get('interest_bearing_debt', 0)
        cash_to_debt_ratio = ratios.get('cash_to_debt_ratio', 0)
        
        debt_rating = '安全' if asset_liability_ratio < 0.4 else '可控' if asset_liability_ratio < 0.6 else '较高'
        short_term_rating = '安全' if cash_to_debt_ratio > 1.0 else '基本覆盖' if cash_to_debt_ratio > 0.8 else '有压力'
        
        return {
            'asset_liability_ratio': asset_liability_ratio,
            'current_ratio': current_ratio,
            'quick_ratio': quick_ratio,
            'interest_bearing_debt': interest_bearing_debt,
            'cash_to_debt_ratio': cash_to_debt_ratio,
            'debt_rating': debt_rating,
            'short_term_rating': short_term_rating,
            'summary': f"资产负债率{asset_liability_ratio:.1%}，{debt_rating}；现金短债比{cash_to_debt_ratio:.1f}，短期偿债{short_term_rating}"
        }
    
    def _analyze_cash_flow_quality(self, ratios: Dict, quarterly: Dict) -> Dict:
        """分析现金流质量（净现比）"""
        net_profit_cash_ratio = ratios.get('net_profit_cash_ratio', 0)
        operating_cash_flow = quarterly.get('operating_cash_flow', 0)
        
        quality = '优秀' if net_profit_cash_ratio > 1.0 else '良好' if net_profit_cash_ratio > 0.8 else '一般' if net_profit_cash_ratio > 0.5 else '较差'
        
        return {
            'net_profit_cash_ratio': net_profit_cash_ratio,
            'quarterly_operating_cash_flow': operating_cash_flow,
            'quality': quality,
            'summary': f"净现比{net_profit_cash_ratio:.2f}，现金流质量{quality}"
        }
    
    def _analyze_rd_expense(self, rd_expense: Dict) -> Dict:
        """分析研发支出情况"""
        annual_rd = rd_expense.get('annual', 0)
        revenue_ratio = rd_expense.get('revenue_ratio', 0)
        yoy_growth = rd_expense.get('yoy_growth', 0)
        
        rating = '高' if revenue_ratio > 0.15 else '中高' if revenue_ratio > 0.1 else '中等' if revenue_ratio > 0.05 else '低'
        
        return {
            'annual_rd': annual_rd,
            'revenue_ratio': revenue_ratio,
            'yoy_growth': yoy_growth,
            'rating': rating,
            'summary': f"年研发支出{annual_rd/1e8:.1f}亿元，占营收比例{revenue_ratio:.1%}，同比增长{yoy_growth:.1%}，研发投入{rating}"
        }
    
    def _analyze_peg(self, ratios: Dict) -> Dict:
        """分析PEG表现"""
        peg = ratios.get('peg', 0)
        
        valuation = '低估' if peg < 0.8 else '合理' if peg < 1.2 else '高估' if peg < 2.0 else '严重高估'
        
        return {
            'peg': peg,
            'valuation': valuation,
            'summary': f"PEG {peg:.2f}，估值{valuation}"
        }
    
    def _analyze_free_cash_flow(self, ratios: Dict) -> Dict:
        """分析自由现金流情况"""
        fcf_per_share = ratios.get('free_cash_flow_per_share', 0)
        
        rating = '优秀' if fcf_per_share > 2.0 else '良好' if fcf_per_share > 1.0 else '一般' if fcf_per_share > 0 else '较差'
        
        return {
            'free_cash_flow_per_share': fcf_per_share,
            'rating': rating,
            'summary': f"每股自由现金流{fcf_per_share:.2f}元，{rating}"
        }
    
    def _calculate_overall_score(self, analysis: Dict) -> float:
        """计算综合财务评分（满分100）"""
        weights = {
            'management': 0.10,
            'strategy': 0.05,
            'moat': 0.10,
            'revenue_growth': 0.12,
            'profit_growth': 0.15,
            'roe_analysis': 0.10,
            'deduct_roe_analysis': 0.08,
            'debt_analysis': 0.08,
            'cash_flow_quality': 0.07,
            'rd_analysis': 0.05,
            'peg_analysis': 0.05,
            'fcf_analysis': 0.05
        }
        
        scores = {
            'management': 90 if analysis['management']['stability_rating'] == '优秀' else 70 if analysis['management']['stability_rating'] == '一般' else 40,
            'strategy': 85,  # 默认
            'moat': 90 if analysis['moat']['moat_level'] == '强' else 70 if analysis['moat']['moat_level'] == '中等' else 50,
            'revenue_growth': 90 if analysis['revenue_growth']['rating'] == '优秀' else 75 if analysis['revenue_growth']['rating'] == '良好' else 60 if analysis['revenue_growth']['rating'] == '一般' else 30,
            'profit_growth': 90 if analysis['profit_growth']['rating'] == '优秀' else 75 if analysis['profit_growth']['rating'] == '良好' else 60 if analysis['profit_growth']['rating'] == '一般' else 30,
            'roe_analysis': 90 if analysis['roe_analysis']['rating'] == '优秀' else 75 if analysis['roe_analysis']['rating'] == '良好' else 60 if analysis['roe_analysis']['rating'] == '一般' else 30,
            'deduct_roe_analysis': 90 if analysis['deduct_roe_analysis']['rating'] == '优秀' else 75 if analysis['deduct_roe_analysis']['rating'] == '良好' else 60 if analysis['deduct_roe_analysis']['rating'] == '一般' else 30,
            'debt_analysis': 90 if analysis['debt_analysis']['debt_rating'] == '安全' and analysis['debt_analysis']['short_term_rating'] == '安全' else 70 if analysis['debt_analysis']['debt_rating'] == '可控' else 40,
            'cash_flow_quality': 90 if analysis['cash_flow_quality']['quality'] == '优秀' else 75 if analysis['cash_flow_quality']['quality'] == '良好' else 60 if analysis['cash_flow_quality']['quality'] == '一般' else 30,
            'rd_analysis': 90 if analysis['rd_analysis']['rating'] == '高' else 75 if analysis['rd_analysis']['rating'] == '中高' else 60 if analysis['rd_analysis']['rating'] == '中等' else 40,
            'peg_analysis': 90 if analysis['peg_analysis']['valuation'] == '低估' else 75 if analysis['peg_analysis']['valuation'] == '合理' else 50 if analysis['peg_analysis']['valuation'] == '高估' else 30,
            'fcf_analysis': 90 if analysis['fcf_analysis']['rating'] == '优秀' else 75 if analysis['fcf_analysis']['rating'] == '良好' else 60 if analysis['fcf_analysis']['rating'] == '一般' else 30
        }
        
        total_score = 0
        for key, weight in weights.items():
            total_score += scores.get(key, 60) * weight
        
        return round(total_score, 2)
    
    def _get_rating(self, score: float) -> str:
        """根据分数获取评级"""
        if score >= 85:
            return 'A+（优秀）'
        elif score >= 75:
            return 'A（良好）'
        elif score >= 65:
            return 'B+（中等偏上）'
        elif score >= 60:
            return 'B（中等）'
        elif score >= 50:
            return 'C+（较差）'
        else:
            return 'C（很差）'

