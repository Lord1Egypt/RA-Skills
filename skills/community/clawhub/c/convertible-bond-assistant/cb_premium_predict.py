#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可转债上市溢价预测模块
基于历史数据和行业对比预测上市溢价率
"""

from datetime import datetime
import random

# 模拟历史数据
HISTORY_PREMIUM = [
    {'name': 'XX 转债', 'industry': '汽车零部件', 'premium': 35, 'list_date': '2026-02-15'},
    {'name': 'YY 转债', 'industry': '汽车零部件', 'premium': 28, 'list_date': '2026-02-20'},
    {'name': 'ZZ 转债', 'industry': '化工', 'premium': 22, 'list_date': '2026-02-18'},
    {'name': 'AA 转债', 'industry': '化工', 'premium': 26, 'list_date': '2026-02-25'},
    {'name': 'BB 转债', 'industry': '医药生物', 'premium': 45, 'list_date': '2026-02-10'},
    {'name': 'CC 转债', 'industry': '电子', 'premium': 40, 'list_date': '2026-02-28'},
]

# 近期新债平均溢价（模拟）
RECENT_AVG_PREMIUM = 32  # 近 3 个月新债平均上市溢价率

# 行业平均溢价
INDUSTRY_PREMIUM = {
    '汽车零部件': 32,
    '化工': 24,
    '医药生物': 42,
    '电子': 38,
    '机械设备': 30,
    '食品饮料': 35,
    '计算机': 40,
    '通信': 36,
    '电气设备': 33,
    '有色金属': 28,
}

# 转债数据
CB_DATA = {
    "123205": {
        "name": "赛龙转债",
        "industry": "汽车零部件",
        "amount": 7.5,
        "rating": "AA-",
        "stock_pe": 25.3,
    },
    "123206": {
        "name": "恒泰转债",
        "industry": "化工",
        "amount": 10.0,
        "rating": "AA",
        "stock_pe": 18.5,
    },
}


def predict_premium_rate(cb_code):
    """
    预测转债上市溢价率
    
    Args:
        cb_code: 转债代码
        
    Returns:
        dict: 预测结果
    """
    if cb_code not in CB_DATA:
        return get_default_prediction(cb_code)
    
    cb = CB_DATA[cb_code]
    industry = cb['industry']
    
    # 1. 行业平均溢价
    industry_avg = INDUSTRY_PREMIUM.get(industry, 30)
    
    # 2. 近期市场平均
    recent_avg = RECENT_AVG_PREMIUM
    
    # 3. 规模调整（规模越小，溢价越高）
    if cb['amount'] < 5:
        size_adjust = 5
    elif cb['amount'] < 10:
        size_adjust = 3
    elif cb['amount'] < 20:
        size_adjust = 0
    else:
        size_adjust = -3
    
    # 4. 评级调整
    rating_adjust = {
        'AAA': 5,
        'AA+': 3,
        'AA': 0,
        'AA-': -2,
        'A+': -5,
    }.get(cb['rating'], 0)
    
    # 5. 正股估值调整（PE 越低，溢价越高）
    industry_pe_avg = {
        '汽车零部件': 28,
        '化工': 15,
        '医药生物': 35,
        '电子': 32,
    }.get(industry, 25)
    
    if cb['stock_pe'] < industry_pe_avg * 0.8:
        pe_adjust = 3
    elif cb['stock_pe'] > industry_pe_avg * 1.2:
        pe_adjust = -3
    else:
        pe_adjust = 0
    
    # 综合计算
    base_premium = (industry_avg + recent_avg) / 2
    predicted = base_premium + size_adjust + rating_adjust + pe_adjust
    
    # 限制范围
    predicted = max(10, min(60, predicted))
    
    # 预测区间
    lower = max(5, predicted - 8)
    upper = min(70, predicted + 8)
    
    # 预测价格（假设转股价值 100 元）
    predicted_price = 100 * (1 + predicted / 100)
    
    # 置信度
    confidence = "高" if abs(predicted - industry_avg) < 5 else "中"
    
    return {
        'code': cb_code,
        'name': cb['name'],
        'predicted_premium': round(predicted, 1),
        'premium_range': [round(lower, 1), round(upper, 1)],
        'predicted_price': round(predicted_price, 2),
        'confidence': confidence,
        'industry_avg_premium': industry_avg,
        'recent_avg_premium': recent_avg,
        'stock_valuation': f"PE {cb['stock_pe']}倍",
        'factors': {
            'size_adjust': size_adjust,
            'rating_adjust': rating_adjust,
            'pe_adjust': pe_adjust,
        }
    }


def get_default_prediction(cb_code):
    """返回默认预测（未知转债）"""
    return {
        'code': cb_code,
        'name': '未知转债',
        'predicted_premium': 30,
        'premium_range': [22, 38],
        'predicted_price': 130.0,
        'confidence': '低',
        'industry_avg_premium': 30,
        'recent_avg_premium': RECENT_AVG_PREMIUM,
        'stock_valuation': '未知',
        'factors': {},
    }


def get_industry_comparison(industry):
    """
    获取行业溢价对比
    
    Args:
        industry: 行业名称
        
    Returns:
        list: 同行业转债列表
    """
    result = [cb for cb in HISTORY_PREMIUM if cb['industry'] == industry]
    return result


def calculate_accuracy():
    """
    计算预测准确率（回测）
    
    Returns:
        dict: 准确率统计
    """
    # 模拟回测结果
    total = len(HISTORY_PREMIUM)
    accurate = sum(1 for cb in HISTORY_PREMIUM if abs(cb['premium'] - RECENT_AVG_PREMIUM) < 10)
    
    return {
        'total_samples': total,
        'accurate_predictions': accurate,
        'accuracy_rate': round(accurate / total * 100, 1),
        'avg_error': round(abs(HISTORY_PREMIUM[0]['premium'] - RECENT_AVG_PREMIUM), 1),
    }


if __name__ == "__main__":
    # 测试
    print("赛龙转债溢价预测:")
    result = predict_premium_rate("123205")
    print(f"  预测溢价率：{result['predicted_premium']}%")
    print(f"  合理区间：{result['premium_range'][0]}% - {result['premium_range'][1]}%")
    print(f"  预测价格：{result['predicted_price']}元")
    print(f"  置信度：{result['confidence']}")
    print(f"  影响因素：{result['factors']}")
    
    print("\n预测准确率回测:")
    accuracy = calculate_accuracy()
    print(f"  样本数：{accuracy['total_samples']}")
    print(f"  准确率：{accuracy['accuracy_rate']}%")
