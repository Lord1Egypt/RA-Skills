#!/usr/bin/env python3
"""
投资研究系统 - Graham 价值投资评分模块 v1.0
基于格雷厄姆价值投资理念进行股票评估
"""
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class GrahamScore:
    """Graham 评分结果"""
    total_score: float        # 总分 (0-1)
    safety_margin: float      # 安全边际得分
    profitability: float      # 盈利能力得分
    stability: float          # 稳定性得分
    dividend: float           # 股息得分
    recommendation: str       # 建议
    reasons: list             # 理由


class GrahamEvaluator:
    """Graham 价值投资评估器"""
    
    # Graham 价值投资标准
    STANDARDS = {
        # 盈利指标
        'roe_min': 10.0,         # ROE 最低要求
        'roe_good': 15.0,        # ROE 优秀
        'gross_margin_min': 20.0, # 毛利率最低要求
        'gross_margin_good': 40.0, # 毛利率优秀
        
        # 估值指标
        'pe_max': 15.0,          # PE 最高要求
        'pe_good': 10.0,         # PE 优秀
        'pb_max': 1.5,           # PB 最高要求
        'pb_good': 1.0,          # PB 优秀
        
        # 股息
        'dividend_min': 2.0,     # 股息率最低要求
        'dividend_good': 4.0,    # 股息率优秀
        
        # 财务健康
        'debt_max': 50.0,        # 资产负债率最高
        'current_ratio_min': 1.5, # 流动比率最低
    }
    
    def __init__(self, user_profile=None):
        """初始化评估器，可选传入用户画像"""
        self.user_profile = user_profile
    
    def evaluate(self, financial_data: Dict, quote: Dict = None) -> GrahamScore:
        """
        评估股票是否满足 Graham 价值投资标准
        
        Args:
            financial_data: 财务指标字典
            quote: 行情数据字典（可选）
        
        Returns:
            GrahamScore: 评分结果
        """
        fi = financial_data.get('财务指标', {})
        valuation = financial_data.get('估值', {})
        
        # 提取关键指标
        roe = float(fi.get('ROE', 0) or 0)
        gross_margin = float(fi.get('毛利率', 0) or 0)
        net_margin = float(fi.get('净利率', 0) or 0)
        revenue_growth = float(fi.get('营收增速', 0) or 0)
        profit_growth = float(fi.get('利润增速', 0) or 0)
        debt_ratio = float(fi.get('资产负债率', 0) or 0)
        current_ratio = float(fi.get('流动比率', 0) or 0)
        
        pe = float(valuation.get('PE_TTM', 0) or 0)
        pb = float(valuation.get('PB', 0) or 0)
        dividend_yield = float(valuation.get('股息率', 0) or 0)
        
        # 1. 安全边际评分 (40%)
        safety_score = self._calc_safety_score(pe, pb, roe, current_ratio)
        
        # 2. 盈利能力评分 (30%)
        profitability_score = self._calc_profitability_score(roe, gross_margin, net_margin)
        
        # 3. 稳定性评分 (15%)
        stability_score = self._calc_stability_score(debt_ratio, current_ratio, revenue_growth)
        
        # 4. 股息评分 (15%)
        dividend_score = self._calc_dividend_score(dividend_yield)
        
        # 计算总分
        total_score = (
            safety_score * 0.40 +
            profitability_score * 0.30 +
            stability_score * 0.15 +
            dividend_score * 0.15
        )
        
        # 生成建议
        recommendation, reasons = self._generate_recommendation(
            total_score, safety_score, profitability_score, dividend_score,
            roe, pe, pb, dividend_yield, current_ratio
        )
        
        return GrahamScore(
            total_score=round(total_score, 2),
            safety_margin=round(safety_score, 2),
            profitability=round(profitability_score, 2),
            stability=round(stability_score, 2),
            dividend=round(dividend_score, 2),
            recommendation=recommendation,
            reasons=reasons
        )
    
    def _calc_safety_score(self, pe: float, pb: float, roe: float, current_ratio: float) -> float:
        """计算安全边际得分"""
        score = 0
        
        # PE 评分
        if pe > 0:
            if pe <= self.STANDARDS['pe_good']:
                score += 0.4
            elif pe <= self.STANDARDS['pe_max']:
                score += 0.2
            else:
                score += max(0, 0.2 - (pe - self.STANDARDS['pe_max']) * 0.02)
        
        # PB 评分
        if pb > 0:
            if pb <= self.STANDARDS['pb_good']:
                score += 0.3
            elif pb <= self.STANDARDS['pb_max']:
                score += 0.15
            else:
                score += max(0, 0.15 - (pb - self.STANDARDS['pb_max']) * 0.05)
        
        # 流动比率评分
        if current_ratio >= self.STANDARDS['current_ratio_min']:
            score += 0.3
        elif current_ratio >= 1.0:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calc_profitability_score(self, roe: float, gross_margin: float, net_margin: float) -> float:
        """计算盈利能力得分"""
        score = 0
        
        # ROE 评分
        if roe >= self.STANDARDS['roe_good']:
            score += 0.4
        elif roe >= self.STANDARDS['roe_min']:
            score += 0.2
        elif roe > 0:
            score += 0.1
        
        # 毛利率评分
        if gross_margin >= self.STANDARDS['gross_margin_good']:
            score += 0.35
        elif gross_margin >= self.STANDARDS['gross_margin_min']:
            score += 0.2
        
        # 净利率评分
        if net_margin >= 15:
            score += 0.25
        elif net_margin >= 10:
            score += 0.15
        elif net_margin > 0:
            score += 0.1
        
        return min(score, 1.0)
    
    def _calc_stability_score(self, debt_ratio: float, current_ratio: float, 
                               revenue_growth: float) -> float:
        """计算稳定性得分"""
        score = 0
        
        # 资产负债率评分
        if debt_ratio <= 30:
            score += 0.35
        elif debt_ratio <= self.STANDARDS['debt_max']:
            score += 0.2
        else:
            score += max(0, 0.2 - (debt_ratio - self.STANDARDS['debt_max']) * 0.01)
        
        # 流动比率评分
        if current_ratio >= 2.0:
            score += 0.35
        elif current_ratio >= 1.5:
            score += 0.25
        elif current_ratio >= 1.0:
            score += 0.15
        
        # 营收增长稳定性
        if revenue_growth > 0:
            score += 0.3
        elif revenue_growth > -5:
            score += 0.15
        
        return min(score, 1.0)
    
    def _calc_dividend_score(self, dividend_yield: float) -> float:
        """计算股息得分"""
        if dividend_yield >= self.STANDARDS['dividend_good']:
            return 1.0
        elif dividend_yield >= self.STANDARDS['dividend_min']:
            return 0.6
        elif dividend_yield > 0:
            return 0.3
        return 0.0
    
    def _generate_recommendation(self, total: float, safety: float, 
                                  profit: float, div: float,
                                  roe: float, pe: float, pb: float,
                                  dividend: float, current_ratio: float) -> Tuple[str, list]:
        """生成投资建议"""
        reasons = []
        
        # 分析各项
        if pe > 0 and pe < self.STANDARDS['pe_max']:
            reasons.append(f"PE={pe:.1f}倍，符合 Graham 标准（<{self.STANDARDS['pe_max']}倍）")
        if pb > 0 and pb < self.STANDARDS['pb_max']:
            reasons.append(f"PB={pb:.2f}倍，具备安全边际")
        if roe >= self.STANDARDS['roe_min']:
            reasons.append(f"ROE={roe:.1f}% > {self.STANDARDS['roe_min']}%，盈利能力强")
        if dividend >= self.STANDARDS['dividend_min']:
            reasons.append(f"股息率={dividend:.2f}% > {self.STANDARDS['dividend_min']}%，提供现金流")
        if current_ratio >= self.STANDARDS['current_ratio_min']:
            reasons.append(f"流动比率={current_ratio:.2f}，财务健康")
        
        if roe < self.STANDARDS['roe_min']:
            reasons.append(f"⚠️ ROE={roe:.1f}% 偏低")
        if pe > self.STANDARDS['pe_max']:
            reasons.append(f"⚠️ PE={pe:.1f}倍偏高")
        if dividend < self.STANDARDS['dividend_min']:
            reasons.append(f"⚠️ 股息率较低")
        
        # 生成建议
        if total >= 0.75:
            recommendation = "✅ 强烈建议"
            if self.user_profile and self.user_profile.investment_style == "价值投资":
                recommendation = "✅ 符合 Graham 价值投资标准"
        elif total >= 0.50:
            recommendation = "⚠️ 谨慎观望"
        else:
            recommendation = "❌ 不建议"
        
        return recommendation, reasons


def evaluate_with_graham(code: str, financial_data: Dict, quote: Dict = None, 
                         user_profile=None) -> GrahamScore:
    """便捷函数：Graham 价值评估"""
    evaluator = GrahamEvaluator(user_profile)
    return evaluator.evaluate(financial_data, quote)


if __name__ == "__main__":
    # 测试
    test_financial = {
        '财务指标': {
            'ROE': 10.87,
            '毛利率': 18.88,
            '净利率': 8.33,
            '营收增速': -0.24,
            '利润增速': 10.0,
            '资产负债率': 45.64,
            '流动比率': 1.52
        },
        '估值': {
            'PE_TTM': 32.73,
            'PB': 1.77,
            '股息率': 0.96
        }
    }
    
    score = evaluate_with_graham('002489', test_financial)
    print(f"Graham 评分: {score.total_score}")
    print(f"建议: {score.recommendation}")
    print(f"理由: {score.reasons}")