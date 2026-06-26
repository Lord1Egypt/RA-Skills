#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财报分析模块
从富途获取财务数据，进行财报分析
"""

import requests
import re

def get_financial_data(symbol):
    """
    获取股票财务数据
    """
    # 转换代码格式
    code = symbol.upper().replace('.HK', '').replace('HK', '')
    if len(code) == 4:
        code = '0' + code
    
    # 富途财务API
    url = f'https://www.futunn.com/mkt/stock/{code}/financial'
    
    # 这里需要解析网页获取财务数据
    # 暂时返回模拟数据结构
    
    return {
        'symbol': symbol,
        'revenue': None,      # 营收
        'profit': None,       # 净利润
        'eps': None,         # 每股收益
        'pe': None,          # 市盈率
        'pb': None,          # 市净率
        'roe': None,         # 净资产收益率
        'debt_ratio': None, # 资产负债率
        'gross_margin': None,# 毛利率
        'net_margin': None   # 净利率
    }

def analyze_financial_health(data):
    """
    分析财务健康状况
    """
    analysis = []
    
    # ROE分析
    if data.get('roe'):
        roe = data['roe']
        if roe > 20:
            analysis.append(f"ROE {roe}% - 优秀，股东回报率高")
        elif roe > 10:
            analysis.append(f"ROE {roe}% - 良好")
        elif roe > 5:
            analysis.append(f"ROE {roe}% - 一般")
        else:
            analysis.append(f"ROE {roe}% - 较差")
    
    # 毛利率分析
    if data.get('gross_margin'):
        gm = data['gross_margin']
        if gm > 40:
            analysis.append(f"毛利率 {gm}% - 高，具有竞争力")
        elif gm > 20:
            analysis.append(f"毛利率 {gm}% - 中等")
        else:
            analysis.append(f"毛利率 {gm}% - 较低")
    
    # 净利率分析
    if data.get('net_margin'):
        nm = data['net_margin']
        if nm > 20:
            analysis.append(f"净利率 {nm}% - 优秀")
        elif nm > 10:
            analysis.append(f"净利率 {nm}% - 良好")
        elif nm > 0:
            analysis.append(f"净利率 {nm}% - 较低")
        else:
            analysis.append(f"净利率 {nm}% - 亏损")
    
    # 资产负债率
    if data.get('debt_ratio'):
        debt = data['debt_ratio']
        if debt < 30:
            analysis.append(f"资产负债率 {debt}% - 低，财务安全")
        elif debt < 60:
            analysis.append(f"资产负债率 {debt}% - 中等")
        else:
            analysis.append(f"资产负债率 {debt}% - 高，注意风险")
    
    return analysis

def get_valuation_score(pe, pb):
    """
    估值评分
    """
    score = 50  # 基础分
    
    # 市盈率评分
    if pe:
        if pe < 0:
            pe_score = "亏损"
        elif pe < 10:
            score += 20
            pe_score = "极低"
        elif pe < 20:
            score += 10
            pe_score = "偏低"
        elif pe < 40:
            pe_score = "合理"
        elif pe < 60:
            score -= 10
            pe_score = "偏高"
        else:
            score -= 20
            pe_score = "极高"
    
    # 市净率评分
    if pb:
        if pb < 1:
            score += 15
            pb_score = "破净"
        elif pb < 2:
            score += 5
            pb_score = "偏低"
        elif pb < 5:
            pb_score = "合理"
        else:
            score -= 10
            pb_score = "偏高"
    
    # 最终评级
    if score >= 80:
        rating = "低估"
    elif score >= 60:
        rating = "合理偏低"
    elif score >= 40:
        rating = "合理"
    elif score >= 20:
        rating = "偏高"
    else:
        rating = "高估"
    
    return {
        'score': score,
        'rating': rating,
        'pe': pe,
        'pb': pb
    }

def generate_financial_report(data):
    """
    生成财报分析报告
    """
    if not data:
        return "暂无财务数据"
    
    report = []
    
    # 估值分析
    valuation = get_valuation_score(data.get('pe'), data.get('pb'))
    
    report.append("="*50)
    report.append("📊 财报分析")
    report.append("="*50)
    
    # 关键指标
    if data.get('pe'):
        report.append(f"市盈率 (P/E): {data['pe']} - {valuation['pe_score'] if 'pe_score' in dir() else ''}")
    if data.get('pb'):
        report.append(f"市净率 (P/B): {data['pb']}")
    if data.get('roe'):
        report.append(f"净资产收益率 (ROE): {data['roe']}%")
    if data.get('gross_margin'):
        report.append(f"毛利率: {data['gross_margin']}%")
    if data.get('net_margin'):
        report.append(f"净利率: {data['net_margin']}%")
    
    # 估值结论
    report.append(f"\n估值评分: {valuation['score']}/100")
    report.append(f"估值评级: {valuation['rating']}")
    
    # 财务健康分析
    health = analyze_financial_health(data)
    if health:
        report.append("\n财务健康:")
        for h in health:
            report.append(f"  • {h}")
    
    return "\n".join(report)

# ========== 测试 ==========
if __name__ == '__main__':
    # 模拟数据测试
    test_data = {
        'pe': 15.5,
        'pb': 2.3,
        'roe': 18.5,
        'gross_margin': 45.2,
        'net_margin': 12.3,
        'debt_ratio': 35
    }
    
    print(generate_financial_report(test_data))
