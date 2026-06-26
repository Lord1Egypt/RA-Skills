#!/usr/bin/env python3
"""
关键发现模块

自动生成：
- 亮点（增长显著、超预算、表现好的方面）
- 关注点（下滑、未达标、亏损等需要关注的方面）
"""

from collections import defaultdict


def generate_key_findings(actual, actual_yoy, budget, volume, volume_yoy, customer_data, warehouse_data, loss_customers, period='2026-Q1'):
    """生成关键发现
    
    返回：
    - highlights: 亮点列表
    - concerns: 关注点列表
    """
    highlights = []
    concerns = []
    
    # 计算汇总数据
    current_revenue = sum(actual['current'].get(f'{k}_revenue', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    current_profit = sum(actual['current'].get(f'{k}_profit', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    cumulative_revenue = sum(actual['cumulative'].get(f'{k}_revenue', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    cumulative_profit = sum(actual['cumulative'].get(f'{k}_profit', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    
    # 同比汇总
    current_revenue_yoy = sum(actual_yoy['current'].get(f'{k}_revenue', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    current_profit_yoy = sum(actual_yoy['current'].get(f'{k}_profit', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    cumulative_revenue_yoy = sum(actual_yoy['cumulative'].get(f'{k}_revenue', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    cumulative_profit_yoy = sum(actual_yoy['cumulative'].get(f'{k}_profit', 0) for k in ['b', 'c', 'd', 'ecom', 'other'])
    
    # 计算增长率
    def yoy_growth(current, last_year):
        if not last_year or last_year == 0:
            return 0
        return ((current - last_year) / last_year) * 100
    
    def achievement(act, bud):
        if not bud or bud == 0:
            return 100
        return (act / bud) * 100
    
    revenue_yoy = yoy_growth(cumulative_revenue, cumulative_revenue_yoy)
    profit_yoy = yoy_growth(cumulative_profit, cumulative_profit_yoy)
    # 预算数据单位是元，actual 数据单位也是元，直接计算
    revenue_ach = achievement(cumulative_revenue, budget.get('revenue_cumulative', 1))
    profit_ach = achievement(cumulative_profit, budget.get('gross_profit_cumulative', 1))
    
    # ========== 亮点分析 ==========
    
    # 1. 收入增长
    if revenue_yoy > 20:
        highlights.append(f"收入增长强劲，累计收入{cumulative_revenue:,.0f}万元，同比增长{revenue_yoy:.1f}%")
    elif revenue_yoy > 10:
        highlights.append(f"收入稳步增长，累计收入{cumulative_revenue:,.0f}万元，同比增长{revenue_yoy:.1f}%")
    elif revenue_yoy > 0:
        highlights.append(f"收入小幅增长，累计收入{cumulative_revenue:,.0f}万元，同比增长{revenue_yoy:.1f}%")
    
    # 2. 毛利增长
    if profit_yoy > 20:
        highlights.append(f"毛利增长显著，累计毛利{cumulative_profit/10000:.1f}万元，同比增长{profit_yoy:.1f}%")
    elif profit_yoy > 10:
        highlights.append(f"毛利表现良好，累计毛利{cumulative_profit/10000:.1f}万元，同比增长{profit_yoy:.1f}%")
    
    # 3. 预算达成
    if revenue_ach >= 120:
        highlights.append(f"收入超额完成预算，达成率{revenue_ach:.1f}%，超预算{revenue_ach-100:.1f}%")
    elif revenue_ach >= 100:
        highlights.append(f"收入达成预算目标，达成率{revenue_ach:.1f}%")
    
    if profit_ach >= 120:
        highlights.append(f"毛利超额完成预算，达成率{profit_ach:.1f}%，超预算{profit_ach-100:.1f}%")
    elif profit_ach >= 100:
        highlights.append(f"毛利达成预算目标，达成率{profit_ach:.1f}%")
    
    # 4. 箱量增长
    if volume['cumulative']['b_volume'] > 0 and volume_yoy['cumulative']['b_volume'] > 0:
        b_vol_yoy = yoy_growth(volume['cumulative']['b_volume'], volume_yoy['cumulative']['b_volume'])
        if b_vol_yoy > 30:
            highlights.append(f"B 段箱量增长迅猛，累计{volume['cumulative']['b_volume']:.0f}TEU，同比增长{b_vol_yoy:.1f}%")
        elif b_vol_yoy > 10:
            highlights.append(f"B 段箱量稳步增长，累计{volume['cumulative']['b_volume']:.0f}TEU，同比增长{b_vol_yoy:.1f}%")
    
    if volume['cumulative']['c_volume'] > 0 and volume_yoy['cumulative']['c_volume'] > 0:
        c_vol_yoy = yoy_growth(volume['cumulative']['c_volume'], volume_yoy['cumulative']['c_volume'])
        if c_vol_yoy > 30:
            highlights.append(f"C 段箱量增长迅猛，累计{volume['cumulative']['c_volume']:.0f}TEU，同比增长{c_vol_yoy:.1f}%")
        elif c_vol_yoy > 10:
            highlights.append(f"C 段箱量稳步增长，累计{volume['cumulative']['c_volume']:.0f}TEU，同比增长{c_vol_yoy:.1f}%")
    
    if volume['cumulative']['d_volume'] > 0 and volume_yoy['cumulative']['d_volume'] > 0:
        d_vol_yoy = yoy_growth(volume['cumulative']['d_volume'], volume_yoy['cumulative']['d_volume'])
        if d_vol_yoy > 50:
            highlights.append(f"D 段箱量爆发式增长，累计{volume['cumulative']['d_volume']:.0f}TEU，同比增长{d_vol_yoy:.1f}%")
        elif d_vol_yoy > 20:
            highlights.append(f"D 段箱量增长强劲，累计{volume['cumulative']['d_volume']:.0f}TEU，同比增长{d_vol_yoy:.1f}%")
    
    # 5. 客户开发
    if len(customer_data['cumulative']['d_customers']) > 20:
        highlights.append(f"D 段客户开发成效显著，累计新增{len(customer_data['cumulative']['d_customers'])}家客户")
    
    # 6. 美国仓库占比
    us_inbound = warehouse_data['us_warehouse']['self_run']['inbound_containers'] + warehouse_data['us_warehouse']['third_party']['inbound_containers']
    total_inbound = sum(d['inbound_containers'] for d in warehouse_data['by_country'].values())
    if total_inbound > 0 and us_inbound / total_inbound > 0.9:
        highlights.append(f"美国市场占主导地位，入库柜量占比{us_inbound/total_inbound*100:.1f}%")
    
    # ========== 关注点分析 ==========
    
    # 1. 收入下滑
    if revenue_yoy < -20:
        concerns.append(f"收入下滑明显，累计收入{cumulative_revenue:,.0f}万元，同比下降{abs(revenue_yoy):.1f}%")
    elif revenue_yoy < -10:
        concerns.append(f"收入有所下滑，累计收入{cumulative_revenue:,.0f}万元，同比下降{abs(revenue_yoy):.1f}%")
    elif revenue_yoy < 0:
        concerns.append(f"收入小幅下滑，累计收入{cumulative_revenue:,.0f}万元，同比下降{abs(revenue_yoy):.1f}%")
    
    # 2. 毛利下滑
    if profit_yoy < -20:
        concerns.append(f"毛利下滑明显，累计毛利{cumulative_profit/10000:.1f}万元，同比下降{abs(profit_yoy):.1f}%")
    elif profit_yoy < -10:
        concerns.append(f"毛利有所下滑，累计毛利{cumulative_profit/10000:.1f}万元，同比下降{abs(profit_yoy):.1f}%")
    elif profit_yoy < 0:
        concerns.append(f"毛利小幅下滑，累计毛利{cumulative_profit/10000:.1f}万元，同比下降{abs(profit_yoy):.1f}%")
    
    # 3. 预算未达成
    if revenue_ach < 80:
        concerns.append(f"收入未达预算目标，达成率{revenue_ach:.1f}%，低于预算{100-revenue_ach:.1f}%")
    elif revenue_ach < 95:
        concerns.append(f"收入接近预算目标，达成率{revenue_ach:.1f}%")
    
    if profit_ach < 80:
        concerns.append(f"毛利未达预算目标，达成率{profit_ach:.1f}%，低于预算{100-profit_ach:.1f}%")
    elif profit_ach < 95:
        concerns.append(f"毛利接近预算目标，达成率{profit_ach:.1f}%")
    
    # 4. 箱量下滑
    if volume['cumulative']['b_volume'] > 0 and volume_yoy['cumulative']['b_volume'] > 0:
        b_vol_yoy = yoy_growth(volume['cumulative']['b_volume'], volume_yoy['cumulative']['b_volume'])
        if b_vol_yoy < -30:
            concerns.append(f"B 段箱量下滑明显，累计{volume['cumulative']['b_volume']:.0f}TEU，同比下降{abs(b_vol_yoy):.1f}%")
        elif b_vol_yoy < -10:
            concerns.append(f"B 段箱量有所下滑，累计{volume['cumulative']['b_volume']:.0f}TEU，同比下降{abs(b_vol_yoy):.1f}%")
    
    if volume['cumulative']['c_volume'] > 0 and volume_yoy['cumulative']['c_volume'] > 0:
        c_vol_yoy = yoy_growth(volume['cumulative']['c_volume'], volume_yoy['cumulative']['c_volume'])
        if c_vol_yoy < -30:
            concerns.append(f"C 段箱量下滑明显，累计{volume['cumulative']['c_volume']:.0f}TEU，同比下降{abs(c_vol_yoy):.1f}%")
    
    # 5. 亏损客户
    if len(loss_customers) > 5:
        total_loss = sum(prof for _, prof in loss_customers)
        concerns.append(f"亏损客户较多，共{len(loss_customers)}家，合计亏损{abs(total_loss)/10000:.1f}万元")
    
    if loss_customers:
        worst_customer = loss_customers[0]
        if abs(worst_customer[1]) > 50000:  # 亏损超过 5 万
            concerns.append(f"最大亏损客户为{worst_customer[0]}，亏损{abs(worst_customer[1])/10000:.1f}万元")
    
    # 6. 客户开发不足
    if len(customer_data['cumulative']['total']) < 10:
        concerns.append(f"客户开发进度较慢，累计仅新增{len(customer_data['cumulative']['total'])}家客户")
    
    # 如果没有发现，给默认文案
    if not highlights:
        highlights.append("整体经营平稳，无显著亮点")
    
    if not concerns:
        concerns.append("无明显风险点，需继续保持")
    
    return highlights, concerns
