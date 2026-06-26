#!/usr/bin/env python3
"""
动态ROE评估器
根据财报期间、行业平均、历史趋势动态评估ROE

版本: 1.0.0
"""

from typing import Dict, Optional, Tuple
from datetime import datetime


# 行业ROE基准线（基于A股历史数据统计）
INDUSTRY_ROE_BENCHMARKS = {
    # 高ROE行业
    "食品饮料": 18.0,
    "医药生物": 15.0,
    "电子": 14.0,
    "计算机": 13.0,
    "电力设备": 13.0,
    "新能源": 14.0,
    # 中等ROE行业
    "家用电器": 12.0,
    "汽车": 11.0,
    "机械设备": 10.0,
    "化工": 10.0,
    "建筑材料": 9.0,
    "交通运输": 9.0,
    "传媒": 9.0,
    # 低ROE行业
    "银行": 10.0,
    "房地产": 6.0,
    "商业贸易": 7.0,
    "农林牧渔": 7.0,
    "纺织服装": 8.0,
    "轻工制造": 8.0,
    "综合": 8.0,
    "环保": 8.0,
    "电气机械": 11.0,  # C38
    "仪器仪表": 10.0,
    "通用设备": 9.0,
    "专用设备": 10.0,
    "通信": 8.0,
    "有色金属": 9.0,
    "钢铁": 7.0,
    "建筑装饰": 8.0,
    "非银金融": 9.0,
    "休闲服务": 10.0,
    "国防军工": 8.0,
    "采掘": 6.0,
    "公用事业": 8.0,
    "农业": 6.0,
    "林业": 5.0,
    "渔业": 5.0,
    "牧业": 6.0,
    "煤炭": 8.0,
    "石油石化": 8.0,
}

# 财报期间调整系数
# 用户的建议：Q1=25%, Q2=50%, Q3=75%, Q4=100%
# 这个设计让早期财报的评估阈值更低，更容易通过
# 逻辑：Q1数据少，不应该用full standard来卡
REPORT_PERIOD_FACTORS = {
    1: 0.25,   # Q1: 仅25%年度数据，阈值放宽
    2: 0.50,   # Q2: 50%年度数据
    3: 0.75,   # Q3: 75%年度数据
    4: 1.0,    # Q4: 100%年度数据（年报标准）
}


def get_industry_roe_benchmark(industry: str) -> float:
    """
    获取行业ROE基准线
    
    Args:
        industry: 行业名称
        
    Returns:
        行业ROE基准线（百分比）
    """
    # 精确匹配
    if industry in INDUSTRY_ROE_BENCHMARKS:
        return INDUSTRY_ROE_BENCHMARKS[industry]
    
    # 模糊匹配
    industry_keywords = {
        "食品": 18.0,
        "饮料": 18.0,
        "医药": 15.0,
        "医疗": 15.0,
        "电子": 14.0,
        "计算机": 13.0,
        "软件": 13.0,
        "新能源": 14.0,
        "电力": 13.0,
        "光伏": 14.0,
        "锂电": 14.0,
        "家电": 12.0,
        "汽车": 11.0,
        "机械": 10.0,
        "化工": 10.0,
        "银行": 10.0,
        "房地产": 6.0,
        "环保": 8.0,
        "电气": 11.0,
        "通信": 8.0,
        "传媒": 9.0,
        "建筑": 8.0,
        "钢铁": 7.0,
        "煤炭": 8.0,
        "有色": 9.0,
        "农业": 6.0,
        "纺服": 8.0,
        "轻工": 8.0,
        "零售": 7.0,
        "商贸": 7.0,
    }
    
    for keyword, benchmark in industry_keywords.items():
        if keyword in industry:
            return benchmark
    
    # 默认基准
    return 10.0


def evaluate_roe_dynamic(
    roe: float,
    industry: str = "综合",
    quarter: int = 4,
    historical_roe: list = None
) -> Dict:
    """
    动态评估ROE
    
    Args:
        roe: 当前ROE（百分比）
        industry: 行业名称
        quarter: 财报季度 (1/2/3/4)
        historical_roe: 历史ROE列表，按时间倒序 [2025Q4, 2024Q4, ...]
        
    Returns:
        评估结果字典:
        - level: 评级 (优秀/良好/一般/较差)
        - score: 得分 (0-100)
        - vs_industry: 相对行业平均 (百分比)
        - vs_historica: 相对历史平均 (百分比)
        - reason: 评估理由
    """
    if roe is None or roe <= 0:
        return {
            "level": "异常",
            "score": 0,
            "vs_industry": 0,
            "vs_historical": 0,
            "reason": "ROE数据异常",
            "threshold": 0,
            "adjusted_threshold": 0
        }
    
    # 1. 获取行业基准并调整
    industry_benchmark = get_industry_roe_benchmark(industry)
    period_factor = REPORT_PERIOD_FACTORS.get(quarter, 1.0)
    adjusted_threshold = industry_benchmark * period_factor
    
    # 生成季度对比表
    quarter_comparison = []
    for q in [1, 2, 3, 4]:
        q_factor = REPORT_PERIOD_FACTORS.get(q, 1.0)
        q_threshold = industry_benchmark * q_factor
        q_roe = roe if q == quarter else None
        q_diff = (q_roe - q_threshold) if q_roe else None
        quarter_comparison.append({
            "quarter": q,
            "factor": q_factor,
            "industry_avg": industry_benchmark,
            "threshold": q_threshold,
            "company_roe": q_roe,
            "diff": q_diff
        })
    
    # 2. 计算相对行业平均
    vs_industry = ((roe - industry_benchmark) / industry_benchmark) * 100
    
    # 3. 计算相对历史平均
    vs_historical = 0
    if historical_roe and len(historical_roe) > 0:
        valid_historical = [r for r in historical_roe if r and r > 0]
        if valid_historical:
            hist_avg = sum(valid_historical) / len(valid_historical)
            vs_historical = ((roe - hist_avg) / hist_avg) * 100 if hist_avg > 0 else 0
    
    # 4. 计算得分 (0-100)
    score = 0
    
    # 基础分：相对于行业基准
    if roe >= adjusted_threshold * 1.5:
        # 大幅高于行业
        base_score = 80 + min(20, (roe - adjusted_threshold * 1.5) / adjusted_threshold * 20)
    elif roe >= adjusted_threshold:
        # 高于行业基准
        base_score = 60 + (roe - adjusted_threshold) / adjusted_threshold * 20
    elif roe >= adjusted_threshold * 0.7:
        # 低于行业基准但可接受
        base_score = 40 + (roe - adjusted_threshold * 0.7) / (adjusted_threshold * 0.3) * 20
    else:
        # 显著低于行业
        base_score = max(0, roe / (adjusted_threshold * 0.7) * 40)
    
    # 趋势加分：相对历史提升
    if vs_historical > 10:
        trend_bonus = 10
    elif vs_historical > 0:
        trend_bonus = 5
    elif vs_historical > -10:
        trend_bonus = 0
    else:
        trend_bonus = -5
    
    score = min(100, max(0, base_score + trend_bonus))
    
    # 5. 确定评级
    if score >= 80:
        level = "优秀"
    elif score >= 60:
        level = "良好"
    elif score >= 40:
        level = "一般"
    else:
        level = "较差"
    
    # 6. 生成理由
    quarter_names = {1: "一季报", 2: "半年报", 3: "三季报", 4: "年报"}
    quarter_name = quarter_names.get(quarter, "年报")
    
    # vs 行业
    if vs_industry > 20:
        industry_comment = f"大幅高于行业平均({industry_benchmark}%)"
    elif vs_industry > 0:
        industry_comment = f"高于行业平均({industry_benchmark}%)"
    elif vs_industry > -20:
        industry_comment = f"低于行业平均({industry_benchmark}%)"
    else:
        industry_comment = f"显著低于行业平均({industry_benchmark}%)"
    
    # vs 历史
    if historical_roe and len(historical_roe) > 0:
        if vs_historical > 10:
            historical_comment = f"，同比提升{vs_historical:.1f}%"
        elif vs_historical > 0:
            historical_comment = f"，同比小幅提升{vs_historical:.1f}%"
        elif vs_historical > -10:
            historical_comment = f"，同比下降{abs(vs_historical):.1f}%"
        else:
            historical_comment = f"，同比大幅下降{abs(vs_historical):.1f}%"
    else:
        historical_comment = ""
    
    reason = f"ROE {roe:.2f}%（{quarter_name}）{industry_comment}{historical_comment}。动态阈值{adjusted_threshold:.1f}%，综合得分{score:.0f}分，评级'{level}'。"
    
    return {
        "level": level,
        "score": score,
        "vs_industry": vs_industry,
        "vs_historical": vs_historical,
        "reason": reason,
        "threshold": industry_benchmark,
        "adjusted_threshold": adjusted_threshold,
        "quarter": quarter,
        "industry": industry,
        "quarter_comparison": quarter_comparison
    }


def roe_to_score(roe: float, industry: str = "综合", quarter: int = 4) -> float:
    """
    简化版：将ROE转换为评分（供分析师使用）
    
    Args:
        roe: ROE百分比
        industry: 行业
        quarter: 财报季度
        
    Returns:
        评分 (0-100)
    """
    result = evaluate_roe_dynamic(roe, industry, quarter)
    return result["score"]


# 测试
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        # (ROE, 行业, 季度, 历史ROE列表, 预期评级)
        (20.0, "食品饮料", 4, [18, 17, 16], "优秀"),
        (12.0, "银行", 4, [11, 10, 9], "良好"),
        (5.0, "电气机械", 1, [8, 7, 6], "较差"),  # Q1需年化，降低预期
        (6.0, "房地产", 4, [5, 4, 3], "一般"),
    ]
    
    print("=" * 70)
    print("动态ROE评估测试")
    print("=" * 70)
    
    for roe, industry, quarter, hist, expected in test_cases:
        result = evaluate_roe_dynamic(roe, industry, quarter, hist)
        status = "✓" if result["level"] == expected else "✗"
        print(f"\n{status} 测试: ROE={roe}%, 行业={industry}, 季度={quarter}")
        print(f"   结果: {result['level']} (得分: {result['score']})")
        print(f"   vs行业: {result['vs_industry']:+.1f}%")
        print(f"   vs历史: {result['vs_historical']:+.1f}%")
        print(f"   动态阈值: {result['adjusted_threshold']:.1f}%")
        print(f"   理由: {result['reason']}")