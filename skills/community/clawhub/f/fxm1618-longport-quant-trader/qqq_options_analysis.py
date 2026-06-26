#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQQ 期权操作建议分析
基于长桥 API 实时数据
"""

from longport.openapi import QuoteContext, Config
from datetime import datetime, timedelta
from decimal import Decimal

config = Config.from_env()
qctx = QuoteContext(config)

def analyze_qqq_options():
    """分析 QQQ 期权操作建议"""
    
    print('=' * 80)
    print('📊 QQQ 期权操作建议')
    print('=' * 80)
    print(f'分析时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}（美东时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}）')
    print(f'数据源：长桥 OpenAPI 实时行情')
    print()
    
    # 获取 QQQ 实时行情
    quotes = qctx.quote(['QQQ.US'])
    qqq = quotes[0]
    
    # 基础数据
    current_price = float(qqq.last_done)
    open_price = float(qqq.open)
    high_price = float(qqq.high)
    low_price = float(qqq.low)
    prev_close = float(qqq.prev_close)
    volume = int(qqq.volume)
    
    change = current_price - prev_close
    change_pct = change / prev_close * 100
    
    print('💹 QQQ 基础数据:')
    print(f'  最新价：${current_price:.2f}')
    print(f'  开盘价：${open_price:.2f}')
    print(f'  最高价：${high_price:.2f}')
    print(f'  最低价：${low_price:.2f}')
    print(f'  昨收价：${prev_close:.2f}')
    print(f'  成交量：{volume:,}股')
    print(f'  涨跌额：${change:+.2f} ({change_pct:+.2f}%)')
    print()
    
    # 技术形态分析
    print('📈 技术形态分析:')
    
    # 1. 日内走势
    if current_price > open_price:
        intraday_trend = '强势'
        intraday_score = 1
    else:
        intraday_trend = '弱势'
        intraday_score = -1
    print(f'  日内走势：{intraday_trend}（现价${current_price:.2f} vs 开盘${open_price:.2f}）')
    
    # 2. 位置判断
    mid_price = (high_price + low_price) / 2
    price_position = (current_price - low_price) / (high_price - low_price) * 100
    if price_position > 80:
        position_desc = '接近日内高点'
        position_score = 1
    elif price_position < 20:
        position_desc = '接近日内低点'
        position_score = -1
    elif price_position > 50:
        position_desc = '中上部'
        position_score = 0.5
    else:
        position_desc = '中下部'
        position_score = -0.5
    print(f'  价格位置：{position_desc}（{price_position:.1f}%分位）')
    
    # 3. 波动率
    intraday_volatility = (high_price - low_price) / prev_close * 100
    if intraday_volatility > 2:
        vol_desc = '高波动'
        vol_recommendation = '适合期权买方（买 Call/Put）'
    elif intraday_volatility > 1:
        vol_desc = '中等波动'
        vol_recommendation = '可考虑价差策略'
    else:
        vol_desc = '低波动'
        vol_recommendation = '适合期权卖方（卖 Call/Put）'
    print(f'  日内波动：{intraday_volatility:.2f}% - {vol_desc}')
    print(f'  波动建议：{vol_recommendation}')
    
    # 4. 成交量
    avg_volume = 50000000  # QQQ 日均成交量约 5000 万股
    volume_ratio = volume / avg_volume
    if volume_ratio > 1.5:
        volume_desc = '放量'
        volume_score = 1
    elif volume_ratio < 0.5:
        volume_desc = '缩量'
        volume_score = -1
    else:
        volume_desc = '正常'
        volume_score = 0
    print(f'  成交量：{volume_ratio:.2f}倍日均 - {volume_desc}')
    
    # 综合评分
    total_score = intraday_score + position_score + volume_score
    print()
    print(f'🎯 综合评分：{total_score:+.1f}/3')
    
    # 期权操作建议
    print()
    print('=' * 80)
    print('🎓 期权操作建议')
    print('=' * 80)
    
    # 判断趋势
    if total_score >= 1.5:
        trend = '看涨'
        main_strategy = '买入 Call 或牛市价差'
    elif total_score <= -1.5:
        trend = '看跌'
        main_strategy = '买入 Put 或熊市价差'
    else:
        trend = '震荡'
        main_strategy = '卖出跨式或铁鹰价差'
    
    print(f'📊 短期趋势：{trend}')
    print(f'💡 主要策略：{main_strategy}')
    print()
    
    # 具体操作建议
    print('📋 具体操作建议:')
    print()
    
    if trend == '看涨':
        strike_above = round(current_price * 1.01 / 5) * 5  # 上方 1% 行权价
        strike_far = round(current_price * 1.03 / 5) * 5    # 上方 3% 行权价
        
        print('  ✅ 激进策略（高风险高收益）:')
        print(f'    买入 1-2 张 QQQ Call，行权价${strike_above}，到期日：本周五')
        print(f'    目标：QQQ 突破${high_price:.2f}后加速上涨')
        print(f'    止损：QQQ 跌破${low_price:.2f}')
        print()
        print('  ✅ 保守策略（中等风险）:')
        print(f'    牛市价差：买入${strike_above} Call + 卖出${strike_far} Call')
        print(f'    最大收益：${strike_far - strike_above:.2f} × 100')
        print(f'    最大亏损：权利金净支出')
        print()
        
    elif trend == '看跌':
        strike_below = round(current_price * 0.99 / 5) * 5  # 下方 1% 行权价
        strike_far = round(current_price * 0.97 / 5) * 5    # 下方 3% 行权价
        
        print('  ✅ 激进策略（高风险高收益）:')
        print(f'    买入 1-2 张 QQQ Put，行权价${strike_below}，到期日：本周五')
        print(f'    目标：QQQ 跌破${low_price:.2f}后加速下跌')
        print(f'    止损：QQQ 突破${high_price:.2f}')
        print()
        print('  ✅ 保守策略（中等风险）:')
        print(f'    熊市价差：买入${strike_below} Put + 卖出${strike_far} Put')
        print(f'    最大收益：${strike_below - strike_far:.2f} × 100')
        print(f'    最大亏损：权利金净支出')
        print()
        
    else:  # 震荡
        strike_call = round(current_price * 1.02 / 5) * 5   # 上方 2%
        strike_put = round(current_price * 0.98 / 5) * 5    # 下方 2%
        
        print('  ✅ 震荡策略（收取时间价值）:')
        print(f'    卖出跨式：卖出${strike_call} Call + 卖出${strike_put} Put')
        print(f'    到期日：本周五')
        print(f'    最大收益：权利金总收入')
        print(f'    风险：QQQ 大幅突破任一方向')
        print()
        print('  ✅ 保守策略（铁鹰价差）:')
        print(f'    卖出${strike_put} Put + 买入${strike_put - 5} Put（保护）')
        print(f'    卖出${strike_call} Call + 买入${strike_call + 5} Call（保护）')
        print(f'    最大收益：权利金净收入')
        print(f'    最大亏损：有限（行权价间距 - 权利金）')
        print()
    
    # 风险提示
    print('=' * 80)
    print('⚠️ 风险提示:')
    print('  1. 期权交易风险高，可能损失全部权利金')
    print('  2. 建议单笔交易不超过账户资金的 5%')
    print('  3. 设置止损，严格执行')
    print('  4. 关注今晚美股开盘后走势')
    print('  5. 注意本周期权到期日（周五）')
    print()
    
    # 关键价位
    print('=' * 80)
    print('📊 关键价位:')
    print(f'  阻力位：${high_price:.2f}（日内高点）')
    print(f'  支撑位：${low_price:.2f}（日内低点）')
    print(f'  中轴：  ${mid_price:.2f}')
    print(f'  突破${high_price:.2f}：看涨信号增强')
    print(f'  跌破${low_price:.2f}：看跌信号增强')
    print()
    print('=' * 80)

if __name__ == '__main__':
    analyze_qqq_options()
