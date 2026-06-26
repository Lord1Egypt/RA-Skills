#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TuShare 数据增强模块 - 个股推荐版
用于金融日报推送技能，提供个股行情和分析建议
"""

import tushare as ts
import pandas as pd
import json
import sys
import os
from datetime import datetime, timedelta

# ==================== 配置 ====================
TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN') or 'c69074d39ca1d31eba5f517273ab14c9cc382a176b25993a2450f221'
pro = ts.pro_api(TUSHARE_TOKEN)

# ==================== 推荐股票池（科技方向） ====================
RECOMMENDED_STOCKS = [
    {'ts_code': '002533.SZ', 'name': '金杯电工', 'sector': '电网设备', 'reason': '电网投资加码'},
    {'ts_code': '688981.SH', 'name': '中芯国际', 'sector': '半导体', 'reason': '国产替代加速'},
    {'ts_code': '000977.SZ', 'name': '浪潮信息', 'sector': 'AI 算力', 'reason': '算力网建设'},
    {'ts_code': '600519.SH', 'name': '贵州茅台', 'sector': '白酒', 'reason': '估值合理'},
    {'ts_code': '002230.SZ', 'name': '科大讯飞', 'sector': 'AI 应用', 'reason': '大模型商业化'},
    {'ts_code': '300750.SZ', 'name': '宁德时代', 'sector': '新能源', 'reason': '技术领先'},
    {'ts_code': '600000.SH', 'name': '浦发银行', 'sector': '银行', 'reason': '低估值'},
    {'ts_code': '000858.SZ', 'name': '五粮液', 'sector': '白酒', 'reason': '稳健增长'},
]

# ==================== 数据获取函数 ====================

def get_stock_daily(ts_code, days=20):
    """
    获取个股日线数据
    
    Args:
        ts_code: 股票代码
        days: 获取天数
    
    Returns:
        DataFrame: 日线数据
    """
    try:
        today = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days+5)).strftime('%Y%m%d')
        
        df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=today)
        
        if df.empty:
            return None
        
        return df.head(days)
    
    except Exception as e:
        print(f"获取 {ts_code} 数据失败：{e}", file=sys.stderr)
        return None


def analyze_stock(ts_code, name, sector, reason):
    """
    分析个股数据
    
    Returns:
        dict: 分析结果
    """
    df = get_stock_daily(ts_code)
    
    if df is None or df.empty:
        return {
            'ts_code': ts_code,
            'name': name,
            'sector': sector,
            'reason': reason,
            'error': '数据获取失败'
        }
    
    latest = df.iloc[0]
    
    # 计算统计指标
    analysis = {
        'ts_code': ts_code,
        'name': name,
        'sector': sector,
        'reason': reason,
        
        # 最新行情
        'close': round(latest['close'], 2),
        'change': round(latest['change'], 2),
        'pct_chg': round(latest['pct_chg'], 2),
        'vol': int(latest['vol']),
        'amount': round(latest['amount'] / 10000, 2),  # 万元
        
        # 统计
        'high_n': round(df['high'].max(), 2),
        'low_n': round(df['low'].min(), 2),
        'avg_vol': int(df['vol'].mean()),
        
        # 累计涨跌
        'total_change': round(((latest['close'] / df.iloc[-1]['close']) - 1) * 100, 2) if len(df) > 1 else 0,
    }
    
    # 技术面分析
    if analysis['total_change'] > 15:
        analysis['tech_comment'] = '短期涨幅较大，注意回调风险'
        analysis['risk_level'] = '高'
    elif analysis['total_change'] > 5:
        analysis['tech_comment'] = '处于上升通道，趋势良好'
        analysis['risk_level'] = '中'
    elif analysis['total_change'] > -5:
        analysis['tech_comment'] = '震荡整理，等待方向选择'
        analysis['risk_level'] = '中'
    elif analysis['total_change'] > -15:
        analysis['tech_comment'] = '短期超跌，关注反弹机会'
        analysis['risk_level'] = '中'
    else:
        analysis['tech_comment'] = '跌幅较大，注意风险'
        analysis['risk_level'] = '高'
    
    # 今日表现分析
    if latest['pct_chg'] > 3:
        analysis['today_comment'] = '今日大涨，表现强势'
    elif latest['pct_chg'] > 0:
        analysis['today_comment'] = '今日收涨，表现平稳'
    elif latest['pct_chg'] > -3:
        analysis['today_comment'] = '今日小幅回调'
    else:
        analysis['today_comment'] = '今日大跌，注意风险'
    
    return analysis


def get_recommendations():
    """
    获取推荐股票分析
    
    Returns:
        list: 推荐股票分析列表
    """
    results = []
    
    for stock in RECOMMENDED_STOCKS:
        analysis = analyze_stock(
            stock['ts_code'],
            stock['name'],
            stock['sector'],
            stock['reason']
        )
        results.append(analysis)
    
    return results


def get_macro_data():
    """
    获取宏观经济数据
    """
    results = {}
    today = datetime.now().strftime('%Y%m%d')
    
    try:
        # LPR 利率
        lpr = pro.shibor_lpr(start_date='20260301', end_date=today)
        if not lpr.empty:
            latest = lpr.iloc[-1]
            results['lpr'] = {
                '1y': float(latest.get('1y', 0)) if latest.get('1y') else None,
                '5y': float(latest.get('5y', 0)) if latest.get('5y') else None,
            }
        
        # SHIBOR 利率
        shibor = pro.shibor(start_date=today, end_date=today)
        if not shibor.empty:
            latest = shibor.iloc[0]
            results['shibor'] = {
                'on': round(float(latest.get('on', 0)), 4),
                '1w': round(float(latest.get('1w', 0)), 4),
                '3m': round(float(latest.get('3m', 0)), 4),
            }
    except Exception as e:
        print(f"获取宏观数据失败：{e}", file=sys.stderr)
    
    return results


# ==================== 输出格式化 ====================

def format_recommendations():
    """
    生成推荐股票格式化输出
    """
    output = []
    
    output.append("=" * 80)
    output.append("🎯 个股推荐（基于 TuShare 日线数据）")
    output.append("=" * 80)
    output.append("")
    
    recommendations = get_recommendations()
    
    for stock in recommendations:
        if stock.get('error'):
            continue
        
        output.append(f"**{stock['name']} ({stock['ts_code']})**")
        output.append(f"-  sector：{stock['sector']}")
        output.append(f"-  推荐逻辑：{stock['reason']}")
        output.append(f"-  收盘价：{stock['close']:.2f}元 ({stock['pct_chg']:+.2f}%)")
        output.append(f"-  成交量：{stock['vol']:,}手")
        output.append(f"-  20 日统计：高{stock['high_n']:.2f} / 低{stock['low_n']:.2f}")
        output.append(f"-  20 日累计涨跌：{stock['total_change']:+.2f}%")
        output.append(f"-  技术面：{stock['tech_comment']}")
        output.append(f"-  风险等级：⭐{'⭐' * (3 if stock['risk_level'] == '中' else 4 if stock['risk_level'] == '高' else 2)} {stock['risk_level']}风险")
        output.append("")
    
    return "\n".join(output)


def format_as_json():
    """
    生成 JSON 格式
    """
    return json.dumps({
        'timestamp': datetime.now().isoformat(),
        'macro': get_macro_data(),
        'recommendations': get_recommendations(),
    }, ensure_ascii=False, indent=2)


# ==================== 主函数 ====================

def main():
    """主函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--json':
            print(format_as_json())
        elif sys.argv[1] == '--macro':
            print(json.dumps(get_macro_data(), ensure_ascii=False, indent=2))
        elif sys.argv[1] == '--recommend':
            print(format_recommendations())
        else:
            print("未知参数，可用：--json, --macro, --recommend")
    else:
        # 默认输出推荐股票
        print(format_recommendations())


if __name__ == "__main__":
    main()
