#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可转债新债分析模块
提供转债基本面分析、行业对比等功能
"""

import json
from datetime import datetime

# 模拟转债数据
MOCK_CB_DATA = {
    "123205": {
        "code": "123205",
        "name": "赛龙转债",
        "amount": 7.5,
        "balance": 7.5,
        "convert_price": 15.23,
        "stock_code": "300123",
        "stock_name": "赛龙科技",
        "stock_pe": 25.3,
        "stock_pb": 3.2,
        "industry": "汽车零部件",
        "rating": "AA-",
        "issue_date": "2026-03-07",
        "list_date": "2026-03-28",
        "maturity": 6,  # 年
        "coupon_rate": [0.3, 0.5, 1.0, 1.5, 2.0, 2.5],  # 每年利率
        "redemption_price": 108,  # 强赎价格
    },
    "123206": {
        "code": "123206",
        "name": "恒泰转债",
        "amount": 10.0,
        "balance": 10.0,
        "convert_price": 8.56,
        "stock_code": "600456",
        "stock_name": "恒泰股份",
        "stock_pe": 18.5,
        "stock_pb": 1.8,
        "industry": "化工",
        "rating": "AA",
        "issue_date": "2026-03-07",
        "list_date": "2026-03-28",
        "maturity": 6,
        "coupon_rate": [0.4, 0.6, 1.0, 1.5, 2.0, 2.5],
        "redemption_price": 107,
    },
}

# 行业平均数据
INDUSTRY_AVERAGE = {
    "汽车零部件": {"pe": 28.5, "cb_premium": 35},
    "化工": {"pe": 15.2, "cb_premium": 25},
    "医药生物": {"pe": 35.0, "cb_premium": 40},
    "电子": {"pe": 32.0, "cb_premium": 38},
    "机械设备": {"pe": 22.0, "cb_premium": 30},
    "食品饮料": {"pe": 30.0, "cb_premium": 32},
}


def analyze_cb(cb_code):
    """
    分析可转债
    
    Args:
        cb_code: 转债代码
        
    Returns:
        dict: 分析结果
    """
    if cb_code not in MOCK_CB_DATA:
        return get_default_analysis(cb_code)
    
    cb = MOCK_CB_DATA[cb_code]
    industry = cb['industry']
    
    # 获取行业对比
    industry_pe = INDUSTRY_AVERAGE.get(industry, {}).get('pe', 25)
    
    # 判断 PE 水平
    if cb['stock_pe'] < industry_pe * 0.8:
        pe_level = "行业较低"
    elif cb['stock_pe'] > industry_pe * 1.2:
        pe_level = "行业较高"
    else:
        pe_level = "行业中等"
    
    # 规模判断
    if cb['amount'] < 5:
        size_desc = "超小盘，易被炒作"
    elif cb['amount'] < 10:
        size_desc = "小规模，较易炒作"
    elif cb['amount'] < 30:
        size_desc = "中等规模"
    else:
        size_desc = "大规模，波动较小"
    
    # 评级判断
    rating_score = {
        'AAA': 5,
        'AA+': 4,
        'AA': 3,
        'AA-': 2,
        'A+': 1,
    }
    rating_val = rating_score.get(cb['rating'], 2)
    
    # 综合建议
    if rating_val >= 3 and cb['amount'] < 10 and cb['stock_pe'] < industry_pe:
        recommendation = "⭐⭐⭐ 积极申购（评级高 + 规模小 + 估值低）"
    elif rating_val >= 2 and cb['amount'] < 15:
        recommendation = "⭐⭐ 建议申购（资质尚可）"
    elif rating_val >= 2:
        recommendation = "⭐ 谨慎申购（规模偏大）"
    else:
        recommendation = "⚠️ 不建议申购（评级偏低）"
    
    return {
        'code': cb['code'],
        'name': cb['name'],
        'amount': cb['amount'],
        'balance': cb['balance'],
        'convert_price': cb['convert_price'],
        'stock_pe': cb['stock_pe'],
        'stock_pe_level': pe_level,
        'stock_pb': cb['stock_pb'],
        'industry': cb['industry'],
        'rating': cb['rating'],
        'size_desc': size_desc,
        'recommendation': recommendation,
    }


def get_default_analysis(cb_code):
    """返回默认分析结果（用于未知转债）"""
    return {
        'code': cb_code,
        'name': '未知转债',
        'amount': 0,
        'balance': 0,
        'convert_price': 0,
        'stock_pe': 0,
        'stock_pe_level': '未知',
        'stock_pb': 0,
        'industry': '未知',
        'rating': 'N/A',
        'size_desc': '未知',
        'recommendation': '⚠️ 数据不足，请查询官方公告',
    }


def compare_industry(cb_code):
    """
    行业对比分析
    
    Args:
        cb_code: 转债代码
        
    Returns:
        dict: 对比结果
    """
    if cb_code not in MOCK_CB_DATA:
        return None
    
    cb = MOCK_CB_DATA[cb_code]
    industry = cb['industry']
    
    industry_data = INDUSTRY_AVERAGE.get(industry, {})
    
    if not industry_data:
        return {
            'industry': industry,
            'message': '该行业暂无对比数据',
        }
    
    return {
        'industry': industry,
        'stock_pe': cb['stock_pe'],
        'industry_avg_pe': industry_data['pe'],
        'pe_diff': cb['stock_pe'] - industry_data['pe'],
        'industry_cb_premium': industry_data['cb_premium'],
        'conclusion': f"正股 PE{'低于' if cb['stock_pe'] < industry_data['pe'] else '高于'}行业平均",
    }


def calculate_cb_value(cb_code):
    """
    计算转债内在价值
    
    Args:
        cb_code: 转债代码
        
    Returns:
        dict: 估值结果
    """
    if cb_code not in MOCK_CB_DATA:
        return None
    
    cb = MOCK_CB_DATA[cb_code]
    
    # 简化估值模型
    # 纯债价值 = 未来现金流折现
    bond_value = sum(
        cb['coupon_rate'][i] / (1.03 ** (i + 1))
        for i in range(len(cb['coupon_rate']))
    ) + 100 / (1.03 ** 6)
    
    # 转股价值 = 正股价格 / 转股价 * 100
    # 这里简化处理
    conversion_value = 100  # 假设平价
    
    # 转债价值 = max(纯债价值，转股价值) + 期权价值
    option_value = cb['amount'] * 0.5  # 规模越小，期权价值越高
    if cb['amount'] < 5:
        option_value = 15
    elif cb['amount'] < 10:
        option_value = 10
    elif cb['amount'] < 20:
        option_value = 5
    
    total_value = max(bond_value, conversion_value) + option_value
    
    return {
        'bond_value': round(bond_value, 2),
        'conversion_value': round(conversion_value, 2),
        'option_value': round(option_value, 2),
        'total_value': round(total_value, 2),
        'rating': cb['rating'],
    }


if __name__ == "__main__":
    # 测试
    print("赛龙转债分析:")
    result = analyze_cb("123205")
    print(f"  发行规模：{result['amount']}亿 - {result['size_desc']}")
    print(f"  评级：{result['rating']}")
    print(f"  正股 PE: {result['stock_pe']}倍 ({result['stock_pe_level']})")
    print(f"  建议：{result['recommendation']}")
    
    print("\n行业对比:")
    comp = compare_industry("123205")
    print(f"  行业：{comp['industry']}")
    print(f"  正股 PE: {comp['stock_pe']} vs 行业平均 {comp['industry_avg_pe']}")
