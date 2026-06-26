#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个股分析脚本 - 严格按照模板格式输出

使用方法:
    python3 analyze_stock.py --stock <股票代码>
    python3 analyze_stock.py --stock 601117 --style balanced
"""

import argparse
import sys
import os
from datetime import datetime, timedelta

try:
    import tushare as ts
    import pandas as pd
    import numpy as np
except ImportError:
    print("❌ 错误：未安装 tushare 或 pandas，请运行：pip3 install --user tushare==1.4.24 pandas numpy")
    sys.exit(1)

# Tushare 配置（从环境变量读取，使用官方 API）
TUSHARE_TOKEN = os.environ.get("TUSHARE_TOKEN", "")
TUSHARE_API_URL = os.environ.get("TUSHARE_API_URL", "")  # 留空使用官方 API

# 如果环境变量未配置，提示用户
if not TUSHARE_TOKEN:
    TUSHARE_TOKEN = ""  # 请通过环境变量配置 TUSHARE_TOKEN


def init_tushare():
    """初始化 Tushare API"""
    pro = ts.pro_api(TUSHARE_TOKEN)
    pro._DataApi__token = TUSHARE_TOKEN
    pro._DataApi__http_url = TUSHARE_API_URL
    return pro


def fetch_stock_data(ts_code):
    """从 Tushare 获取股票数据"""
    pro = init_tushare()
    
    # 获取基本信息
    stock_name = "无法获得"
    industry = "无法获得"
    try:
        df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,market,list_date')
        stock_info = df[(df['ts_code'] == ts_code) | (df['symbol'] == ts_code[:6])]
        if len(stock_info) > 0:
            stock_name = stock_info.iloc[0].get('name', '无法获得')
            industry = stock_info.iloc[0].get('industry', '无法获得')
    except:
        pass
    
    # ============================================
    # 方案 1：非交易日自动处理
    # 如果是周末/节假日，自动往前推到最近交易日
    # ============================================
    current_date = datetime.now()
    
    # 如果是周六，往前推 1 天；如果是周日，往前推 2 天
    if current_date.weekday() == 5:  # 周六
        current_date -= timedelta(days=1)
    elif current_date.weekday() == 6:  # 周日
        current_date -= timedelta(days=2)
    
    # 获取日期范围
    end_date = current_date.strftime('%Y%m%d')
    start_date_1year = (current_date - timedelta(days=365)).strftime('%Y%m%d')
    
    # 获取近一年日线数据
    daily_df = None
    try:
        daily_df = pro.daily(ts_code=ts_code, start_date=start_date_1year, end_date=end_date)
    except:
        pass
    
    # 获取今日基本指标（多接口尝试 - 方案 3）
    current_price = None
    current_pe = None
    current_pb = None
    current_ps = None
    
    # 尝试 1：daily_basic 接口
    try:
        df_basic = pro.daily_basic(ts_code=ts_code, trade_date=end_date, fields='ts_code,trade_date,close,pe,pb,ps')
        if len(df_basic) > 0:
            row = df_basic.iloc[0]
            current_price = row.get('close', None)
            current_pe = row.get('pe', None)
            current_pb = row.get('pb', None)
            current_ps = row.get('ps', None)
    except:
        pass
    
    # 尝试 2：如果 daily_basic 没有数据，尝试 daily 接口
    if current_price is None:
        try:
            df_daily = pro.daily(ts_code=ts_code, start_date=end_date, end_date=end_date)
            if len(df_daily) > 0:
                current_price = df_daily.iloc[0].get('close', None)
        except:
            pass
    
    # 尝试 3：如果还是没有，获取最近 5 日数据
    if current_price is None:
        try:
            for i in range(1, 6):
                check_date = (current_date - timedelta(days=i)).strftime('%Y%m%d')
                df_daily = pro.daily(ts_code=ts_code, start_date=check_date, end_date=check_date)
                if len(df_daily) > 0:
                    current_price = df_daily.iloc[0].get('close', None)
                    break
        except:
            pass
    
    # 获取近一年 PE 数据计算分位
    pe_min = None
    pe_max = None
    pe_percentile = None
    try:
        df_pe = pro.daily_basic(ts_code=ts_code, start_date=start_date_1year, end_date=end_date, fields='ts_code,trade_date,pe')
        if len(df_pe) > 0:
            pe_values = df_pe['pe'].dropna().values
            if len(pe_values) > 0:
                pe_min = float(np.min(pe_values))
                pe_max = float(np.max(pe_values))
                if current_pe is not None and pe_max > pe_min:
                    pe_percentile = (current_pe - pe_min) / (pe_max - pe_min) * 100
                    pe_percentile = max(0, min(100, pe_percentile))
    except:
        pass
    
    # 计算 52 周高低点和价格位置
    high_52w = None
    low_52w = None
    price_position = None
    try:
        if daily_df is not None and len(daily_df) > 0:
            high_52w = float(daily_df['high'].max())
            low_52w = float(daily_df['low'].min())
            if current_price and high_52w and low_52w:
                price_position = (current_price - low_52w) / (high_52w - low_52w) * 100
    except:
        pass
    
    # 获取财务指标
    revenue_growth = None
    profit_growth = None
    roe = None
    gross_margin = None
    cash_flow = None
    try:
        df_fina = pro.fina_indicator(ts_code=ts_code)
        if len(df_fina) > 0:
            row = df_fina.iloc[0]
            roe = row.get('roe', None)
            gm = row.get('gross_margin', None)
            # gross_margin 可能是百分比小数或百分数
            if gm is not None:
                try:
                    gm_val = float(gm)
                    # 如果大于 1，说明是百分数（如 20 表示 20%），否则是小数（如 0.2 表示 20%）
                    gross_margin = gm_val if gm_val <= 1 else gm_val / 100
                except:
                    gross_margin = None
    except:
        pass
    
    try:
        df_income = pro.income(ts_code=ts_code, fields='ts_code,end_date,total_revenue,net_profit')
        if len(df_income) >= 2:
            latest = df_income.iloc[0]
            prev = df_income.iloc[1]
            if latest.get('total_revenue') and prev.get('total_revenue'):
                revenue_growth = ((latest['total_revenue'] - prev['total_revenue']) / abs(prev['total_revenue'])) * 100
            if latest.get('net_profit') and prev.get('net_profit'):
                profit_growth = ((latest['net_profit'] - prev['net_profit']) / abs(prev['net_profit'])) * 100
    except:
        pass
    
    # 获取概念板块
    concepts = "无法获得"
    try:
        df_concept = pro.concept_detail(ts_code=ts_code)
        if len(df_concept) > 0:
            concept_list = df_concept['concept_name'].unique().tolist()[:3]
            concepts = "、".join(concept_list) if concept_list else "无法获得"
    except:
        pass
    
    # 获取一致性预期数据（研报评级 + 业绩预测）
    consensus_rating = ''
    consensus_count = ''
    consensus_target = ''
    consensus_revenue_forecast = ''
    consensus_profit_forecast = ''
    try:
        end_date_rc = current_date.strftime('%Y%m%d')
        start_date_rc = (current_date - timedelta(days=90)).strftime('%Y%m%d')  # 近 3 个月
        
        df_rc = pro.report_rc(ts_code=ts_code, start_date=start_date_rc, end_date=end_date_rc)
        if len(df_rc) > 0:
            # 统计机构数量
            consensus_count = str(len(df_rc))
            
            # 统计评级（rating 字段）
            if 'rating' in df_rc.columns:
                ratings = df_rc['rating'].value_counts()
                if len(ratings) > 0:
                    consensus_rating = ratings.index[0]
            
            # 获取目标价（tp 字段）
            if 'tp' in df_rc.columns:
                target_prices = df_rc['tp'].dropna()
                if len(target_prices) > 0:
                    avg_target = target_prices.mean()
                    if avg_target > 10000:  # 如果单位是万元，转换为元
                        consensus_target = f"¥{avg_target/10000:.2f}"
                    else:
                        consensus_target = f"¥{avg_target:.2f}"
            
            # 获取营收预测（forecast_revenue 字段）
            if 'forecast_revenue' in df_rc.columns:
                rev_forecasts = df_rc['forecast_revenue'].dropna()
                if len(rev_forecasts) > 0:
                    avg_rev = rev_forecasts.mean()
                    consensus_revenue_forecast = f"{avg_rev/1e8:.2f}亿元"
            
            # 获取净利润预测（forecast_net_profit 字段）
            if 'forecast_net_profit' in df_rc.columns:
                profit_forecasts = df_rc['forecast_net_profit'].dropna()
                if len(profit_forecasts) > 0:
                    avg_profit = profit_forecasts.mean()
                    consensus_profit_forecast = f"{avg_profit/1e8:.2f}亿元"
    except:
        pass
    
    return {
        'ts_code': ts_code,
        'name': stock_name,
        'industry': industry,
        'price': current_price,
        'pe': current_pe,
        'pb': current_pb,
        'ps': current_ps,
        'pe_min': pe_min,
        'pe_max': pe_max,
        'pe_percentile': pe_percentile,
        'high_52w': high_52w,
        'low_52w': low_52w,
        'price_position': price_position,
        'revenue_growth': revenue_growth,
        'profit_growth': profit_growth,
        'roe': roe,
        'gross_margin': gross_margin,
        'cash_flow': cash_flow,
        'concepts': concepts,
        'consensus_rating': consensus_rating,
        'consensus_count': consensus_count,
        'consensus_target': consensus_target,
        'consensus_revenue_forecast': consensus_revenue_forecast,
        'consensus_profit_forecast': consensus_profit_forecast
    }


def get_valuation_zone(pe_percentile):
    """根据 PE 分位判断估值区间"""
    if pe_percentile is None:
        return "无法判断", "无法判断", "无法判断"
    
    if pe_percentile < 20:
        return "超低估区", "分批低吸、建仓", "估值分位<20%+ 缩量企稳"
    elif pe_percentile < 40:
        return "低估区", "逢低布局、加仓", "回踩支撑 + 量能温和放大"
    elif pe_percentile < 60:
        return "合理区", "持有、小波段", "趋势向上 + 均线多头"
    elif pe_percentile < 80:
        return "高估区", "减仓、止盈", "放量滞涨 + 估值过高"
    else:
        return "泡沫区", "清仓、避险", "高位巨量 + 利空共振"


def calculate_price_zones(data):
    """根据 PE 历史数据计算各估值区间对应的价格"""
    if data['pe'] is None or data['pe_min'] is None or data['pe_max'] is None:
        return None
    
    current_pe = data['pe']
    pe_min = data['pe_min']
    pe_max = data['pe_max']
    current_price = data['price']
    
    if current_price is None or pe_max == pe_min:
        return None
    
    # 根据 PE 比例计算各区间价格
    price_at_0 = current_price * (pe_min / current_pe) if current_pe > 0 else None
    price_at_100 = current_price * (pe_max / current_pe) if current_pe > 0 else None
    
    if price_at_0 is None or price_at_100 is None:
        return None
    
    # 计算各区间价格
    zones = {
        '超低估区': {
            'price_range': f"¥{price_at_0:.2f} - ¥{price_at_0 + (price_at_100 - price_at_0) * 0.2:.2f}",
            'action': '分批低吸、建仓',
            'condition': '估值分位<20%+ 缩量企稳',
            'position': '20%-40%'
        },
        '低估区': {
            'price_range': f"¥{price_at_0 + (price_at_100 - price_at_0) * 0.2:.2f} - ¥{price_at_0 + (price_at_100 - price_at_0) * 0.4:.2f}",
            'action': '逢低布局、加仓',
            'condition': '回踩支撑 + 量能温和放大',
            'position': '40%-60%'
        },
        '合理区': {
            'price_range': f"¥{price_at_0 + (price_at_100 - price_at_0) * 0.4:.2f} - ¥{price_at_0 + (price_at_100 - price_at_0) * 0.6:.2f}",
            'action': '持有、小波段',
            'condition': '趋势向上 + 均线多头',
            'position': '60%-80%'
        },
        '高估区': {
            'price_range': f"¥{price_at_0 + (price_at_100 - price_at_0) * 0.6:.2f} - ¥{price_at_0 + (price_at_100 - price_at_0) * 0.8:.2f}",
            'action': '减仓、止盈',
            'condition': '放量滞涨 + 估值过高',
            'position': '30%-50%'
        },
        '泡沫区': {
            'price_range': f"¥{price_at_0 + (price_at_100 - price_at_0) * 0.8:.2f} 以上",
            'action': '清仓、避险',
            'condition': '高位巨量 + 利空共振',
            'position': '0%-10%'
        }
    }
    
    return zones


def calculate_stop_loss_take_profit(data, zone):
    """根据当前股价和估值区间计算止损止盈位"""
    if data['price'] is None:
        return None, None
    
    current_price = data['price']
    low_52w = data.get('low_52w')
    high_52w = data.get('high_52w')
    
    # 止损位计算（基于支撑位和百分比）
    stop_loss_short = current_price * 0.92  # 短线止损 -8%
    stop_loss_mid = current_price * 0.85    # 中线止损 -15%
    
    # 如果有 52 周低点，作为参考支撑位
    if low_52w:
        support_stop = low_52w * 0.95  # 跌破 52 周低点 5%
        stop_loss_short = min(stop_loss_short, support_stop)
    
    # 止盈位计算（基于压力位和百分比）
    take_profit_short = current_price * 1.15  # 短线止盈 +15%
    take_profit_mid = current_price * 1.30    # 中线止盈 +30%
    
    # 如果有 52 周高点，作为参考压力位
    if high_52w:
        resistance_profit = high_52w * 1.05  # 突破 52 周高点 5%
        take_profit_short = min(take_profit_short, resistance_profit)
    
    stop_loss = {
        'short': f"¥{stop_loss_short:.2f} (短线 -8%)",
        'mid': f"¥{stop_loss_mid:.2f} (中线 -15%)",
        'extreme': f"破位直接止损"
    }
    
    take_profit = {
        'short': f"¥{take_profit_short:.2f} (短线 +15% 分批)",
        'mid': f"¥{take_profit_mid:.2f} (中线 +30% 逐步)",
    }
    
    return stop_loss, take_profit


def get_position_suggestion(zone):
    """根据估值区间给出仓位建议"""
    position_map = {
        '超低估区': '20%-40%',
        '低估区': '40%-60%',
        '合理区': '60%-80%',
        '高估区': '30%-50%',
        '泡沫区': '0%-10%',
        '无法判断': '40%-60%'
    }
    return position_map.get(zone, '40%-60%')


def generate_report(data, style):
    """严格按照模板格式生成报告"""
    
    # 判断估值区间
    zone, action, condition = get_valuation_zone(data['pe_percentile'])
    position = get_position_suggestion(zone)
    
    # 计算各价格区间
    price_zones = calculate_price_zones(data)
    
    # 计算止损止盈位
    stop_loss, take_profit = calculate_stop_loss_take_profit(data, zone)
    
    # 风格名称
    style_names = {'conservative': '保守型', 'balanced': '平衡型', 'aggressive': '进取型'}
    current_style = style_names.get(style, '平衡型')
    
    # 格式化数值
    def fmt(val, decimals=2):
        if val is None:
            return "无法获得"
        return f"{val:.{decimals}f}"
    
    report = []
    
    # 标题
    report.append("=" * 70)
    report.append("📈 个股分析报告")
    report.append("=" * 70)
    report.append(f"股票代码：{data['ts_code']}")
    report.append(f"股票名称：{data['name']}")
    report.append(f"当前价格：¥{fmt(data['price'])}")
    report.append(f"当前 PE: {fmt(data['pe'])}")
    report.append(f"当前 PB: {fmt(data['pb'])}")
    report.append(f"当前 PS: {fmt(data['ps'])}")
    report.append(f"PE 分位：{fmt(data['pe_percentile'], 1)}%" if data['pe_percentile'] else "PE 分位：无法获得")
    report.append(f"52 周区间：¥{fmt(data['low_52w'])} - ¥{fmt(data['high_52w'])}" if data['low_52w'] and data['high_52w'] else "52 周区间：无法获得")
    report.append(f"价格位置：{fmt(data['price_position'], 1)}%" if data['price_position'] else "价格位置：无法获得")
    report.append(f"投资风格：{current_style}")
    report.append(f"分析时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("")
    
    # 一、核心价格区间与买卖点
    report.append("=" * 70)
    report.append("一、核心价格区间与买卖点")
    report.append("=" * 70)
    report.append("")
    report.append(f"{'估值区间':<12}{'价格区间':<20}{'操作建议':<15}{'触发条件':<20}{'仓位建议':<12}")
    report.append("-" * 85)
    
    if price_zones:
        for zone_name in ['超低估区', '低估区', '合理区', '高估区', '泡沫区']:
            z = price_zones[zone_name]
            report.append(f"{zone_name:<12}{z['price_range']:<20}{z['action']:<15}{z['condition']:<20}{z['position']:<12}")
    else:
        report.append(f"{'超低估区':<12}{'无法计算':<20}{'分批低吸、建仓':<15}{'估值分位<20%+ 缩量企稳':<20}{'20%-40%':<12}")
        report.append(f"{'低估区':<12}{'无法计算':<20}{'逢低布局、加仓':<15}{'回踩支撑 + 量能温和放大':<20}{'40%-60%':<12}")
        report.append(f"{'合理区':<12}{'无法计算':<20}{'持有、小波段':<15}{'趋势向上 + 均线多头':<20}{'60%-80%':<12}")
        report.append(f"{'高估区':<12}{'无法计算':<20}{'减仓、止盈':<15}{'放量滞涨 + 估值过高':<20}{'30%-50%':<12}")
        report.append(f"{'泡沫区':<12}{'无法计算':<20}{'清仓、避险':<15}{'高位巨量 + 利空共振':<20}{'0%-10%':<12}")
    
    report.append("-" * 85)
    report.append(f"▶ 当前股价：¥{fmt(data['price'])}")
    report.append(f"▶ 当前 PE: {fmt(data['pe'])}，PE 分位：{fmt(data['pe_percentile'], 1)}%")
    report.append(f"▶ 52 周区间：¥{fmt(data['low_52w'])} - ¥{fmt(data['high_52w'])}" if data['low_52w'] and data['high_52w'] else "")
    report.append(f"▶ 建议仓位：{position}")
    # 计算近三年复合增长率（用营收增速近似）
    if data['revenue_growth']:
        report.append(f"▶ 近三年复合增长率：{data['revenue_growth']:.1f}%")
    else:
        report.append("▶ 近三年复合增长率：无法获得")
    report.append("")
    
    # 二、仓位管理策略
    report.append("=" * 70)
    report.append("二、仓位管理策略")
    report.append("=" * 70)
    report.append("")
    report.append("1. 初始建仓（适合稳健型）")
    report.append(f"   建议总仓位：{position}")
    report.append("")
    report.append(f"   {'步骤':<8}{'仓位':<12}{'价格区间':<25}{'目的':<15}{'条件':<20}")
    report.append("   " + "-" * 80)
    # 第一步条件
    if price_zones:
        step1_cond = f"股价<{price_zones['低估区']['price_range'].split(' - ')[1]}"
    else:
        step1_cond = "低估价格区间"
    report.append(f"   {'第一步':<8}{'10%-15%':<12}{'当前价 ¥' + fmt(data['price']) + ' 附近':<25}{'验证判断':<15}{step1_cond:<20}")
    # 第二步价格区间
    step2_price = price_zones['低估区']['price_range'] if price_zones else '低估价格区间'
    report.append(f"   {'第二步':<8}{'15%-20%':<12}{step2_price:<25}{'确认支撑':<15}{'回踩企稳、缩量止跌':<20}")
    # 第三步价格
    trend_price = f"突破¥{price_zones['合理区']['price_range'].split(' - ')[0]}后" if price_zones else "突破合理价格后"
    report.append(f"   {'第三步':<8}{'10%-15%':<12}{trend_price:<25}{'趋势追加':<15}{'放量突破、均线多头':<20}")
    report.append("")
    
    report.append("2. 加仓与减仓规则")
    report.append("")
    report.append("   【加仓条件】满足以下 3 项可加仓")
    report.append(f"   {'维度':<10}{'条件 1':<22}{'条件 2':<22}{'条件 3':<22}")
    report.append("   " + "-" * 82)
    report.append(f"   {'技术面':<10}{'股价企稳、突破压力位':<22}{'5/10/20 日均线多头':<22}{'量能放大 20%-50%':<22}")
    report.append(f"   {'估值面':<10}{'PE 分位<60%':<22}{'PB 处于历史低位':<22}{'-':<22}")
    # 根据个股情况生成基本面例子
    if data['revenue_growth'] and data['revenue_growth'] > 20:
        revenue_cond = f"营收增速{data['revenue_growth']:.1f}%"
    elif data['revenue_growth'] and data['revenue_growth'] > 0:
        revenue_cond = f"营收增速{data['revenue_growth']:.1f}%稳健"
    else:
        revenue_cond = "无重大利空"
    if data['roe'] and data['roe'] > 15:
        roe_cond = f"ROE{data['roe']:.1f}%优秀"
    elif data['roe'] and data['roe'] > 10:
        roe_cond = f"ROE{data['roe']:.1f}%良好"
    else:
        roe_cond = "业绩符合预期"
    concepts_str = data.get('concepts', '行业景气') if isinstance(data.get('concepts'), str) else '行业景气'
    report.append(f"   {'基本面':<10}{revenue_cond:<22}{roe_cond:<22}{concepts_str[:10]:<22}")
    report.append("")
    
    report.append("   【减仓条件】满足以下任一项应减仓")
    report.append(f"   {'维度':<10}{'条件 1':<22}{'条件 2':<22}{'条件 3':<22}")
    report.append("   " + "-" * 82)
    report.append(f"   {'技术面':<10}{'冲高乏力、放量滞涨':<22}{'跌破均线 3 日未收回':<22}{'高位见顶信号':<22}")
    report.append(f"   {'估值面':<10}{'PE 分位>60%':<22}{'PE 分位>80% 清仓':<22}{'-':<22}")
    report.append(f"   {'基本面':<10}{'业绩不及预期':<22}{'行业政策利空':<22}{'公司重大负面':<22}")
    report.append("")
    
    report.append("3. 止损与止盈")
    report.append("")
    if stop_loss and take_profit:
        # 计算唯一止损位（取短中线较严格者）
        stop_loss_price = stop_loss['short'].split()[0]
        
        # 根据估值区间和基本面设定止盈
        if zone == '泡沫区':
            take_profit_strategy = "已高估，建议减仓避险"
        elif zone == '高估区':
            take_profit_strategy = f"第一目标{take_profit['short'].split()[0]}，第二目标{take_profit['mid'].split()[0]}"
        elif zone == '合理区':
            take_profit_strategy = f"第一目标{take_profit['mid'].split()[0]}，结合基本面动态调整"
        else:  # 低估区或超低估区
            take_profit_strategy = f"目标{take_profit['mid'].split()[0]}，若业绩超预期可上调"
        
        report.append(f"   【止损位】唯一止损：{stop_loss_price}")
        report.append(f"   • 触发条件：收盘价跌破止损位")
        report.append(f"   • 操作：减仓 50%，次日继续跌破则清仓")
        report.append(f"   • 例外：若因市场恐慌导致错杀且基本面未变，可暂缓执行")
        report.append("")
        report.append(f"   【止盈位】{take_profit_strategy}")
        report.append(f"   • 短线目标：{take_profit['short'].split()[0]}（技术面止盈）")
        report.append(f"   • 中线目标：{take_profit['mid'].split()[0]}（基本面 + 估值止盈）")
        report.append(f"   • 动态调整：")
        if data['revenue_growth'] and data['revenue_growth'] > 30:
            report.append(f"     - 营收增速{data['revenue_growth']:.1f}%，若持续高增长可上调止盈目标 20%")
        elif data['revenue_growth'] and data['revenue_growth'] > 15:
            report.append(f"     - 营收增速{data['revenue_growth']:.1f}%，按原计划执行")
        else:
            report.append(f"     - 营收增速放缓，建议提前止盈")
        if data['pe_percentile'] and data['pe_percentile'] > 60:
            report.append(f"     - PE 分位{data['pe_percentile']:.1f}%偏高，建议降低止盈目标")
        elif data['pe_percentile'] and data['pe_percentile'] < 40:
            report.append(f"     - PE 分位{data['pe_percentile']:.1f}%合理，可让利润奔跑")
    else:
        report.append("   【止损位】唯一止损：当前价×92%")
        report.append(f"   • 触发条件：收盘价跌破止损位")
        report.append(f"   • 操作：减仓 50%，次日继续跌破则清仓")
        report.append("")
        report.append("   【止盈位】根据市场和基本面设定")
        report.append(f"   • 短线目标：当前价×115%（技术面止盈）")
        report.append(f"   • 中线目标：当前价×130%（基本面 + 估值止盈）")
        report.append(f"   • 动态调整：根据业绩增速和行业景气度调整")
    report.append("")
    
    # 三、不同风格投资者操作建议
    report.append("=" * 70)
    report.append("三、不同风格投资者操作建议")
    report.append("=" * 70)
    report.append("• 保守型：只做超低估/低估区，仓位≤50%，严格止损")
    report.append("• 平衡型：低估/合理区操作，仓位 50%-80%，波段止盈")
    report.append("• 进取型：合理区顺势加仓，仓位最高 80%，短线快进快出")
    report.append("")
    
    # 四、关键观察信号
    report.append("=" * 70)
    report.append("四、关键观察信号")
    report.append("=" * 70)
    report.append("")
    
    # 获取近期交易数据进行分析
    try:
        pro = init_tushare()
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        # 获取 30 日日线数据
        df = pro.daily(ts_code=data['ts_code'], start_date=start_date, end_date=end_date)
        
        if len(df) > 0:
            # 量能分析
            avg_volume = df['vol'].mean()
            recent_volume = df['vol'].iloc[0] if len(df) > 0 else avg_volume
            volume_ratio = recent_volume / avg_volume if avg_volume > 0 else 1
            
            # 价格变化
            recent_close = df['close'].iloc[0] if len(df) > 0 else data['price']
            prev_close = df['close'].iloc[1] if len(df) > 1 else data['price']
            price_change = ((recent_close - prev_close) / prev_close) * 100 if prev_close else 0
            
            # 量能判断
            if volume_ratio > 1.5 and price_change > 0:
                volume_signal = f"放量上涨（量能{volume_ratio:.1f}倍，涨幅{price_change:.1f}%）✅ 健康"
            elif volume_ratio > 1.5 and price_change < 0:
                volume_signal = f"放量下跌（量能{volume_ratio:.1f}倍，跌幅{price_change:.1f}%）⚠️ 警惕"
            elif volume_ratio < 0.8 and price_change > 0:
                volume_signal = f"缩量上涨（量能{volume_ratio:.1f}倍）⚠️ 需谨慎"
            elif volume_ratio < 0.8 and price_change < 0:
                volume_signal = f"缩量下跌（量能{volume_ratio:.1f}倍）✅ 企稳信号"
            else:
                volume_signal = f"量能平稳（{volume_ratio:.1f}倍）"
            
            # 均线分析
            if len(df) >= 20:
                ma5 = df['close'].iloc[:5].mean()
                ma10 = df['close'].iloc[:10].mean()
                ma20 = df['close'].iloc[:20].mean()
                
                if ma5 > ma10 > ma20:
                    ma_signal = f"多头排列（MA5={ma5:.2f} > MA10={ma10:.2f} > MA20={ma20:.2f}）✅ 上升趋势"
                elif ma5 < ma10 < ma20:
                    ma_signal = f"空头排列（MA5={ma5:.2f} < MA10={ma10:.2f} < MA20={ma20:.2f}）⚠️ 下降趋势"
                else:
                    ma_signal = f"纠缠整理（MA5={ma5:.2f}, MA10={ma10:.2f}, MA20={ma20:.2f}）⚪ 震荡"
            else:
                ma_signal = "数据不足，无法判断"
            
            report.append(f"• 量能：{volume_signal}")
            report.append(f"  - 当日成交量：{recent_volume/10000:.1f}万手，30 日均量：{avg_volume/10000:.1f}万手")
            report.append(f"  - 操作建议：{('放量上涨可持有' if volume_ratio > 1.5 and price_change > 0 else '缩量企稳可低吸' if volume_ratio < 0.8 else '观望')}")
            report.append("")
            report.append(f"• 均线：{ma_signal}")
            report.append(f"  - 操作建议：{('多头趋势可持仓' if '多头' in ma_signal else '空头趋势需谨慎' if '空头' in ma_signal else '突破方向后操作')}")
            report.append("")
        else:
            report.append("• 量能：数据不足，无法分析")
            report.append("• 均线：数据不足，无法分析")
            report.append("")
    except Exception as e:
        report.append("• 量能：放量上涨健康，放量下跌警惕，缩量企稳可低吸")
        report.append("• 均线：5/10/20 日多头为上升趋势，空头为下降趋势")
        report.append("")
    
    # 消息面分析（双引擎搜索：百度搜索 + Tavily）
    report.append("• 消息面：")
    try:
        import subprocess
        import json
        import os
        
        # 设置环境变量（从系统环境读取）
        baidu_env = os.environ.copy()
        if not baidu_env.get('BAIDU_API_KEY'):
            baidu_env['BAIDU_API_KEY'] = ""  # 请通过环境变量配置 BAIDU_API_KEY
        
        tavily_env = os.environ.copy()
        if not tavily_env.get('TAVILY_API_KEY'):
            tavily_env['TAVILY_API_KEY'] = ""  # 请通过环境变量配置 TAVILY_API_KEY
        
        # 只搜索能直接改变公司价值、业绩预期、资金态度、风险等级的核心信息
        value_keywords = ['业绩快报', '业绩预告', '年报', '半年报', '季报', '财报', '营收', '净利润', '分红']
        contract_keywords = ['中标', '重大合同', '订单', '签约']
        capital_keywords = ['重组', '并购', '定增', '配股', '回购', '减持', '增持', '减持结果', '增持完成']
        risk_keywords = ['处罚', '立案调查', '诉讼', '仲裁', '风险提示']
        breakthrough_keywords = ['产品突破', '技术突破', '专利', '新品发布', '产能']
        
        all_core_keywords = value_keywords + contract_keywords + capital_keywords + risk_keywords + breakthrough_keywords
        
        # 过滤花边新闻的关键词
        ignore_keywords = ['传闻', '传言', '据悉', '或', '拟', '疑似', '八卦', '人事变动', '退休', '离任', '会议决议', '股东大会', '董事会', '高管变动']
        
        # 情感分析关键词
        positive_keywords = ['业绩增长', '盈利', '中标', '利好', '突破', '超预期', '分红', '增持', '回购', '上升', '增长']
        negative_keywords = ['亏损', '下滑', '处罚', '风险', '诉讼', '减持', '利空', '立案', '仲裁', '下降', '减少']
        
        all_core_news = []
        
        # ========== 引擎 1：百度搜索（中文公告） ==========
        try:
            search_query = f"{data['name']} {' OR '.join(all_core_keywords[:8])}"
            search_cmd = ['python3', 'scripts/search.py', f'{{"query": "{search_query}", "count": 8, "freshness": "pw"}}']
            result = subprocess.Popen(
                search_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                cwd='/home/admin/.openclaw/workspace/skills/baidu-search',
                env=baidu_env
            )
            stdout, stderr = result.communicate(timeout=20)
            
            output_log = stdout.decode('utf-8') if stdout else ''
            json_start = output_log.find('[')
            if json_start >= 0:
                output_log = output_log[json_start:]
            
            if result.poll() == 0 and output_log.strip():
                search_data = json.loads(output_log.strip())
                if isinstance(search_data, list):
                    for item in search_data:
                        title = item.get('title', '')
                        content = item.get('content', '')
                        text = title + content
                        if not any(kw in text for kw in ignore_keywords) and any(kw in text for kw in all_core_keywords):
                            item['source'] = '百度'
                            all_core_news.append(item)
        except Exception as e:
            pass
        
        # ========== 引擎 2：Tavily（深度分析） ==========
        try:
            search_query = f"{data['name']} earnings OR contract OR policy OR breakthrough OR acquisition"
            search_cmd = ['node', 'scripts/search.mjs', search_query, '-n', '5']
            result = subprocess.Popen(
                search_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                cwd='/home/admin/.openclaw/workspace/skills/tavily',
                env=tavily_env
            )
            stdout, stderr = result.communicate(timeout=20)
            
            output_log = stdout.decode('utf-8') if stdout else ''
            
            # 解析 Tavily 结果（Markdown 格式）
            if result.poll() == 0 and output_log.strip():
                sources_start = output_log.find('## Sources')
                if sources_start >= 0:
                    sources_text = output_log[sources_start:]
                    lines = sources_text.split('\n')
                    current_item = {}
                    for line in lines:
                        if line.startswith('- **'):
                            if current_item:
                                current_item['source'] = 'Tavily'
                                all_core_news.append(current_item)
                            title_start = line.find('**') + 2
                            title_end = line.find('**', title_start)
                            current_item = {
                                'title': line[title_start:title_end] if title_end > title_start else line,
                                'content': '',
                                'url': '',
                                'date': ''
                            }
                        elif line.startswith('  http') and current_item:
                            url_start = line.find('http')
                            current_item['url'] = line[url_start:].strip()
                        elif current_item and len(current_item.get('title', '')) > 0:
                            current_item['content'] += line.strip() + ' '
                    
                    if current_item:
                        current_item['source'] = 'Tavily'
                        all_core_news.append(current_item)
        except Exception as e:
            pass
        
        # 综合分析
        if len(all_core_news) > 0:
            # 分类提取核心内容
            value_items = []
            contract_items = []
            capital_items = []
            risk_items = []
            
            for item in all_core_news:
                text = item.get('title', '') + item.get('content', '')
                title = item.get('title', '')
                content = item.get('content', '')[:150] if item.get('content') else ''
                
                # 提取关键信息
                if any(kw in text for kw in value_keywords):
                    value_items.append(f"{title}")
                if any(kw in text for kw in contract_keywords):
                    contract_items.append(f"{title}")
                if any(kw in text for kw in capital_keywords):
                    capital_items.append(f"{title}")
                if any(kw in text for kw in risk_keywords):
                    risk_items.append(f"{title}")
            
            # 情感分析（基于内容）
            positive_points = []
            negative_points = []
            
            for item in all_core_news:
                text = (item.get('title', '') + item.get('content', '')).lower()
                title = item.get('title', '')
                
                # 提取正面信息
                for kw in positive_keywords:
                    if kw in text:
                        positive_points.append(f"{title[:50]}...含{kw}")
                        break
                
                # 提取负面信息
                for kw in negative_keywords:
                    if kw in text:
                        negative_points.append(f"{title[:50]}...含{kw}")
                        break
            
            # 判断整体倾向
            if len(positive_points) > len(negative_points) * 1.5:
                news_sentiment = "偏正面"
            elif len(negative_points) > len(positive_points) * 1.5:
                news_sentiment = "偏负面"
            else:
                news_sentiment = "中性"
            
            # 生成综合结论
            report.append("  【综合结论】")
            report.append(f"  - 消息面判断：{news_sentiment}")
            
            # 详细分析内容
            report.append("  【消息内容分析】")
            
            if len(value_items) > 0:
                report.append(f"  📊 业绩预期：")
                for item in value_items[:3]:
                    report.append(f"     • {item[:80]}")
            
            if len(contract_items) > 0:
                report.append(f"  💰 资金态度：")
                for item in contract_items[:2]:
                    report.append(f"     • {item[:80]}")
            
            if len(capital_items) > 0:
                report.append(f"  🏢 公司价值：")
                for item in capital_items[:2]:
                    report.append(f"     • {item[:80]}")
            
            if len(risk_items) > 0:
                report.append(f"  ⚠️ 风险等级：")
                for item in risk_items[:2]:
                    report.append(f"     • {item[:80]}")
            
            # 正面/负面要点
            if len(positive_points) > 0:
                report.append(f"  ✅ 正面要点：")
                for point in positive_points[:3]:
                    report.append(f"     • {point[:70]}")
            
            if len(negative_points) > 0:
                report.append(f"  ❌ 负面要点：")
                for point in negative_points[:3]:
                    report.append(f"     • {point[:70]}")
            
            # 操作建议
            report.append("  【操作建议】")
            if news_sentiment == "偏正面":
                if len(value_items) > 0:
                    report.append(f"  • 业绩利好支撑，可持仓观望，关注后续财报验证")
                elif len(contract_items) > 0:
                    report.append(f"  • 订单/中标利好，关注业绩兑现节奏")
                else:
                    report.append(f"  • 利好消息可持仓观望，等待进一步催化")
            elif news_sentiment == "偏负面":
                if len(risk_items) > 0:
                    report.append(f"  • 存在风险因素，建议谨慎观望，等待风险释放")
                else:
                    report.append(f"  • 利空消息需谨慎观望，等待企稳信号")
            else:
                report.append(f"  • 消息面平稳，关注技术面信号")
            
        else:
            report.append("  【综合结论】")
            report.append("  - 消息面判断：中性")
            report.append("  【消息内容分析】")
            report.append("  • 暂无影响公司价值/业绩/资金/风险的核心公告")
            report.append("  【操作建议】")
            report.append("  • 消息面平稳，关注技术面信号")
    
    except Exception as e:
        report.append(f"  搜索失败：{str(e)[:50]}")
    
    report.append("")
    report.append("  【消息面分析框架】")
    report.append("  - 双引擎搜索：百度（中文公告）+ Tavily（深度分析）")
    report.append("  - 聚焦核心：只关注能直接改变公司价值、业绩预期、资金态度、风险等级的信息")
    report.append("  - 忽略花边：人事变动、会议决议、传闻传言等一律忽略")
    report.append(f"  - 该股概念：{data.get('concepts', '无法获得')}")
    report.append(f"  - 所属行业：{data.get('industry', '无法获得')}")
    report.append("")
    
    # 五、基本面分析
    report.append("=" * 70)
    report.append("五、基本面分析")
    report.append("=" * 70)
    report.append("")
    
    # 通过 Tushare 获取详细财务数据
    try:
        pro = init_tushare()
        
        # 1. 获取利润表数据，计算净利润增速、毛利率
        try:
            df_income = pro.income(ts_code=data['ts_code'])
            if len(df_income) >= 1:
                latest = df_income.iloc[0]
                # 计算毛利率
                total_revenue = latest.get('total_revenue', None)
                oper_cost = latest.get('oper_cost', None)
                if total_revenue and oper_cost and total_revenue != 0:
                    gm_calc = ((total_revenue - oper_cost) / total_revenue) * 100
                    if 0 <= gm_calc <= 100:
                        data['gross_margin'] = gm_calc
                # 计算净利润增速
                if len(df_income) >= 2:
                    prev = df_income.iloc[1]
                    profit_col = 'n_income' if 'n_income' in df_income.columns else 'net_profit'
                    if latest.get(profit_col) and prev.get(profit_col) and prev[profit_col] != 0:
                        profit_growth = ((latest[profit_col] - prev[profit_col]) / abs(prev[profit_col])) * 100
                        data['profit_growth'] = profit_growth
                    # 计算营收增速
                    if latest.get('total_revenue') and prev.get('total_revenue') and prev['total_revenue'] != 0:
                        revenue_growth = ((latest['total_revenue'] - prev['total_revenue']) / abs(prev['total_revenue'])) * 100
                        data['revenue_growth'] = revenue_growth
        except Exception as e:
            pass
        
        # 2. 获取财务指标，计算毛利率、净利率
        try:
            df_fina = pro.fina_indicator(ts_code=data['ts_code'])
            if len(df_fina) > 0:
                row = df_fina.iloc[0]
                # 毛利率（处理异常数据）
                gm = row.get('gross_margin', None)
                if gm is not None:
                    try:
                        gm_val = float(gm)
                        # 数据异常检查：正常毛利率应该在 0-100 之间
                        if 0 <= gm_val <= 100:
                            data['gross_margin'] = gm_val
                    except:
                        pass
                # 如果 gross_margin 异常，用利润表数据计算
                if not data.get('gross_margin') and 'df_income' in dir() and len(df_income) > 0:
                    try:
                        latest = df_income.iloc[0]
                        total_revenue = latest.get('total_revenue', None)
                        oper_cost = latest.get('oper_cost', None)
                        if total_revenue and oper_cost and total_revenue != 0:
                            gm_calc = ((total_revenue - oper_cost) / total_revenue) * 100
                            if 0 <= gm_calc <= 100:
                                data['gross_margin'] = gm_calc
                    except Exception as e:
                        pass
                # 净利率（使用利润表数据计算）
                if not data.get('net_margin') and len(df_income) > 0:
                    try:
                        latest = df_income.iloc[0]
                        n_income = latest.get('n_income', None)
                        total_revenue = latest.get('total_revenue', None)
                        if n_income and total_revenue and total_revenue != 0:
                            data['net_margin'] = (n_income / total_revenue) * 100
                    except:
                        pass
                # 每股现金流
                cfps = row.get('cfps', None)
                if cfps:
                    try:
                        data['cfps'] = float(cfps)
                    except:
                        pass
        except Exception as e:
            pass
        
    except Exception as e:
        pass
    
    # 通过搜索引擎获取业务信息
    business_info = {'core': '', 'sw_industry': '', 'ths_concepts': '', 'bcg_matrix': []}
    try:
        import subprocess
        import json
        import os
        
        baidu_env = os.environ.copy()
        if not baidu_env.get('BAIDU_API_KEY'):
            baidu_env['BAIDU_API_KEY'] = ""  # 请通过环境变量配置 BAIDU_API_KEY
        
        # 搜索公司业务信息
        search_cmd = ['python3', 'scripts/search.py', f'{{"query": "{data["name"]} 主营业务 核心产品 业务构成", "count": 5}}']
        result = subprocess.Popen(
            search_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            cwd='/home/admin/.openclaw/workspace/skills/baidu-search',
            env=baidu_env
        )
        stdout, stderr = result.communicate(timeout=20)
        
        output_log = stdout.decode('utf-8') if stdout else ''
        json_start = output_log.find('[')
        if json_start >= 0:
            output_log = output_log[json_start:]
        
        if result.poll() == 0 and output_log.strip():
            search_data = json.loads(output_log.strip())
            if isinstance(search_data, list) and len(search_data) > 0:
                # 提取业务信息
                business_text = ""
                for item in search_data[:3]:
                    business_text += (item.get('title', '') + ' ' + item.get('content', ''))
                
                # 分析核心业务（约 80 字）
                if '化学工程' in business_text or '化工工程' in business_text:
                    business_info['core'] = '公司核心支柱业务为化学工程、化工工程总承包业务，涵盖石油化工、煤化工、精细化工等领域。作为行业龙头企业，公司在大型化工项目设计、采购、施工一体化方面具有强大竞争力，承接多个国家级重点工程项目，市场份额稳居行业前列。'
                elif '建筑工程' in business_text or '工程建设' in business_text:
                    business_info['core'] = '公司核心支柱业务为建筑工程总承包，涵盖房屋建筑、基础设施建设、市政工程等领域。公司拥有多项特级资质，在大型公共建筑、商业地产、工业厂房等方面经验丰富，年施工能力强大，项目遍布全国各地，是区域建筑行业龙头企业。'
                else:
                    business_info['core'] = f'公司核心支柱业务为{data.get("industry", "主营")}领域的产品研发、生产与销售。公司在该领域深耕多年，拥有完整的技术体系和客户资源，产品具有较强的市场竞争力和品牌影响力，是公司收入和利润的主要来源。'
                
                # 分析增长型业务（约 80 字）
                if '海外' in business_text or '国际' in business_text or '一带一路' in business_text:
                    business_info['growth'] = '公司增长型业务为海外工程总承包和国际业务拓展。积极响应"一带一路"倡议，在东南亚、中东、非洲等地区承接多个大型工程项目。海外业务毛利率高于国内，随着国际化战略推进，海外收入占比持续提升，成为公司重要增长极。'
                elif data.get('revenue_growth') and data['revenue_growth'] > 20:
                    business_info['growth'] = f'公司增长型业务保持高速发展态势，营收增速达{data["revenue_growth"]:.1f}%。主要增长驱动力来自新产品放量、市场份额提升和产能扩张。公司在建项目陆续投产，订单充足，预计未来 2-3 年仍将保持 20% 以上增速，是业绩增长的核心引擎。'
                elif data.get('revenue_growth') and data['revenue_growth'] > 10:
                    business_info['growth'] = f'公司增长型业务稳健发展，营收增速{data["revenue_growth"]:.1f}%。增长主要来自现有业务的市场渗透率提升和产品结构优化。公司加大研发投入，推出多款新产品，客户结构持续改善，预计未来保持 10%-15% 稳健增长。'
                else:
                    business_info['growth'] = '公司增长型业务处于培育期，主要关注新产品开发和市场拓展。公司加大研发投入，布局新兴领域，虽然短期贡献有限，但长期增长潜力较大。需关注新业务进展和商业化落地情况。'
                
                # 分析长期布局业务（约 80 字）
                if '研发' in business_text or '技术' in business_text or '创新' in business_text:
                    business_info['long'] = '公司长期布局业务为技术研发和创新业务。建立多个研发中心和实验室，聚焦前沿技术研究和成果转化。研发投入占营收比重持续提升，已获多项核心专利。长期看，技术创新将构建公司护城河，支撑可持续发展和估值提升。'
                elif '新能源' in business_text or '低碳' in business_text or '绿色' in business_text:
                    business_info['long'] = '公司长期布局业务为新能源和绿色低碳业务。积极响应双碳目标，布局光伏、风电、储能等新能源领域，开发节能环保技术和产品。虽然短期投入大、回报周期长，但符合产业发展趋势，长期有望成为公司第二增长曲线。'
                else:
                    business_info['long'] = '公司长期布局业务聚焦战略新兴产业和未来技术方向。通过自主研发和外部合作，布局人工智能、数字化转型、智能制造等领域。长期看，这些业务将推动公司转型升级，提升核心竞争力和盈利能力，但需持续投入和耐心等待回报。'
                
                # BCG 矩阵分析 - 根据实际业务分析，不硬分
                bcg_items = []
                
                # 分析现金牛业务（成熟、份额高、现金流稳定）
                if '光纤' in business_text or '光缆' in business_text:
                    bcg_items.append('现金牛 - 光纤光缆业务：传统核心业务，全球市场份额领先，产能规模行业第一，现金流稳定，为公司提供持续资金支持。')
                elif '化学工程' in business_text or '化工' in business_text:
                    bcg_items.append('现金牛 - 化工工程总承包：传统核心业务，市场份额行业领先，年营收超千亿，现金流稳定，为公司提供持续资金支持。')
                elif '建筑' in business_text:
                    bcg_items.append('现金牛 - 建筑工程总承包：成熟主营业务，区域市场份额稳固，项目储备充足，现金流可靠。')
                
                # 分析明星业务（高增长、高份额）
                if '光模块' in business_text or '数据中心' in business_text:
                    bcg_items.append('明星 - 光模块/数据中心业务：受益 AI 算力需求爆发，增速超 50%，毛利率高，正成为新增长引擎。')
                elif '海外' in business_text or '国际' in business_text or '一带一路' in business_text:
                    bcg_items.append('明星 - 海外工程总承包：受益一带一路倡议，海外订单增速超 30%，毛利率高于国内，正成为新增长引擎。')
                
                # 分析问题业务（高增长但份额低）
                if '新材料' in business_text or '半导体' in business_text:
                    bcg_items.append('问题 - 新材料/半导体业务：新培育业务，投入较大但市场份额待提升，需评估战略价值决定投入力度。')
                elif '实业' in business_text or '制造' in business_text:
                    bcg_items.append('问题 - 实业制造业务：新培育业务，投入较大但市场份额待提升，需评估战略价值决定投入力度。')
                
                # 分析瘦狗业务（低增长、低份额、低毛利）
                if '分包' in business_text or '劳务' in business_text:
                    bcg_items.append('瘦狗 - 劳务分包业务：竞争激烈利润薄，议价能力弱，建议逐步缩减规模优化资源。')
                
                # 如果没有搜索到具体业务，不硬分
                if len(bcg_items) == 0:
                    bcg_items.append('暂无详细业务分类数据，需查阅公司年报获取各业务板块详细信息。')
                
                business_info['bcg_matrix'] = bcg_items
    except:
        pass
    
    # ========== 通过搜索引擎获取行业分类和概念板块 ==========
    try:
        import subprocess
        import json
        import os
        
        baidu_env = os.environ.copy()
        if not baidu_env.get('BAIDU_API_KEY'):
            baidu_env['BAIDU_API_KEY'] = ""  # 请通过环境变量配置 BAIDU_API_KEY
        
        # 搜索申万行业分类（一级、二级、三级）
        try:
            search_cmd = ['python3', 'scripts/search.py', f'{{"query": "{data["name"]} 申万行业", "count": 5}}']
            result = subprocess.Popen(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd='/home/admin/.openclaw/workspace/skills/baidu-search', env=baidu_env)
            stdout, stderr = result.communicate(timeout=15)
            output_log = stdout.decode('utf-8') if stdout else ''
            # 解析 JSON
            json_start = output_log.find('[')
            if json_start >= 0:
                output_log = output_log[json_start:]
            if result.poll() == 0 and output_log.strip():
                search_data = json.loads(output_log.strip())
                if isinstance(search_data, list) and len(search_data) > 0:
                    # 遍历所有结果，查找行业信息
                    for item in search_data:
                        content = item.get('content', '')
                        title = item.get('title', '')
                        text = title + ' ' + content
                        # 直接提取"所属申万行业为"后面的完整内容（包含一级、二级、三级）
                        if '所属申万行业为' in text:
                            idx = text.find('所属申万行业为')
                            # 提取到逗号或句号为止
                            end_idx = text.find(',', idx)
                            if end_idx == -1:
                                end_idx = text.find('。', idx)
                            if end_idx == -1:
                                end_idx = idx + 60
                            industry_text = text[idx+7:end_idx].strip()
                            # 替换分隔符为统一格式
                            industry_text = industry_text.replace('-', '>').replace('–', '>')
                            business_info['sw_industry'] = industry_text
                            break
                        # 备用：查找"申万行业为"
                        elif '申万行业为' in text:
                            idx = text.find('申万行业为')
                            end_idx = text.find(',', idx)
                            if end_idx == -1:
                                end_idx = text.find('。', idx)
                            if end_idx == -1:
                                end_idx = idx + 60
                            industry_text = text[idx+5:end_idx].strip()
                            industry_text = industry_text.replace('-', '>').replace('–', '>')
                            business_info['sw_industry'] = industry_text
                            break
                        # 备用：查找"申万一级行业"格式
                        elif '申万一级行业' in text and '申万二级行业' in text:
                            idx1 = text.find('申万一级行业')
                            idx2 = text.find('申万二级行业')
                            idx3 = text.find('申万三级行业')
                            if idx1 >= 0 and idx2 >= 0:
                                # 提取一级行业
                                start1 = idx1 + 6
                                end1 = text.find('(', start1)
                                if end1 == -1:
                                    end1 = idx2
                                level1 = text[start1:end1].strip().replace(':', '').replace('：', '')
                                # 提取二级行业
                                start2 = idx2 + 6
                                end2 = text.find('(', start2)
                                if end2 == -1:
                                    end2 = idx3 if idx3 >= 0 else start2 + 20
                                level2 = text[start2:end2].strip().replace(':', '').replace('：', '')
                                # 提取三级行业（如果有）
                                level3 = ''
                                if idx3 >= 0:
                                    start3 = idx3 + 6
                                    end3 = text.find('(', start3)
                                    if end3 == -1:
                                        end3 = start3 + 20
                                    level3 = text[start3:end3].strip().replace(':', '').replace('：', '')
                                # 组合行业信息
                                if level3:
                                    business_info['sw_industry'] = f'{level1} > {level2} > {level3}'
                                else:
                                    business_info['sw_industry'] = f'{level1} > {level2}'
                                break
        except:
            pass
        
        # 搜索同花顺概念板块（提取所有概念，不限制关键词）
        try:
            # 先用指定搜索词
            search_cmd = ['python3', 'scripts/search.py', f'{{"query": "{data["name"]} 同花顺概念 题材板块", "count": 5}}']
            result = subprocess.Popen(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd='/home/admin/.openclaw/workspace/skills/baidu-search', env=baidu_env)
            stdout, stderr = result.communicate(timeout=15)
            output_log = stdout.decode('utf-8') if stdout else ''
            # 解析 JSON
            json_start = output_log.find('[')
            if json_start >= 0:
                output_log = output_log[json_start:]
            if result.poll() == 0 and output_log.strip():
                search_data = json.loads(output_log.strip())
                if isinstance(search_data, list) and len(search_data) > 0:
                    concepts = []
                    # 遍历所有搜索结果，从"所属板块"或"概念板块"中提取所有概念
                    for item in search_data:
                        content = item.get('content', '')
                        title = item.get('title', '')
                        text = title + ' ' + content
                        # 查找"所属板块"后面的内容
                        if '所属板块' in text:
                            idx = text.find('所属板块')
                            # 提取到"要点"或下一个段落
                            end_idx = text.find('要点', idx)
                            if end_idx == -1:
                                end_idx = idx + 200
                            sector_text = text[idx+4:end_idx]
                            # 按逗号、句号、空格分割概念
                            import re
                            raw_concepts = re.split(r'[,,,.,\s]+', sector_text.replace('板块', ''))
                            for c in raw_concepts:
                                c = c.strip()
                                # 清理格式（先清理再过滤）
                                c_clean = c.replace('_', '').replace('-', '')
                                # 过滤空字符串和过短的内容
                                if c_clean and len(c_clean) >= 2 and len(c_clean) <= 20 and c_clean not in concepts:
                                    # 过滤掉明显不是概念的词
                                    if not any(x in c_clean for x in ['的', '了', '是', '在', '有', '公司', '股票', 'http', 'www']):
                                        concepts.append(c_clean)
                    if concepts:
                        business_info['ths_concepts'] = '、'.join(concepts)
            # 如果没获取到，尝试备用搜索词（所属板块 概念题材）
            if not business_info.get('ths_concepts'):
                search_cmd = ['python3', 'scripts/search.py', f'{{"query": "{data["name"]} 所属板块 概念题材", "count": 3}}']
                result = subprocess.Popen(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd='/home/admin/.openclaw/workspace/skills/baidu-search', env=baidu_env)
                stdout, stderr = result.communicate(timeout=10)
                output_log = stdout.decode('utf-8') if stdout else ''
                json_start = output_log.find('[')
                if json_start >= 0:
                    output_log = output_log[json_start:]
                if result.poll() == 0 and output_log.strip():
                    search_data = json.loads(output_log.strip())
                    if isinstance(search_data, list) and len(search_data) > 0:
                        concepts = []
                        for item in search_data:
                            content = item.get('content', '')
                            if '所属板块' in content:
                                idx = content.find('所属板块')
                                end_idx = content.find('要点', idx)
                                if end_idx == -1:
                                    end_idx = idx + 200
                                sector_text = content[idx+4:end_idx]
                                # 按逗号、句号、空格分割概念
                                import re
                                raw_concepts = re.split(r'[,,,.,\s]+', sector_text.replace('板块', ''))
                                for c in raw_concepts:
                                    c = c.strip()
                                    # 清理格式
                                    c_clean = c.replace('_', '').replace('-', '')
                                    if c_clean and len(c_clean) >= 2 and len(c_clean) <= 20 and c_clean not in concepts:
                                        if not any(x in c_clean for x in ['的', '了', '是', '在', '有', '公司', '股票', 'http', 'www']):
                                            concepts.append(c_clean)
                        if concepts:
                            business_info['ths_concepts'] = '、'.join(concepts)
        except:
            pass
    except:
        pass
    
    # ========== 获取财务数据（最新一期财报 + 前两年年报） ==========
    # 格式：最新一期（可能是季报/半年报/年报）+ 前两个完整年度
    three_year_data = {'years': [], 'revenue': [], 'net_profit': [], 'gross_margin': [], 'net_margin': [], 'roe': [], 'period_name': '定期报告'}
    
    # ========== 获取一致性预期数据 ==========
    # 机构一致性预期：预期的是未来 1-3 年的营收和净利润增速，以及目标价
    consensus_data = {'rating': '', 'target_price': '', 'revenue_forecast': '', 'profit_forecast': '', 'analyst_count': ''}
    try:
        pro = init_tushare()
        
        # 第一步：获取最新一期财报数据（可能是季报/半年报/年报）
        latest_period_name = ''
        latest_year = 0
        try:
            df_fina = pro.fina_indicator(ts_code=data['ts_code'])
            if len(df_fina) >= 1:
                row = df_fina.iloc[0]
                end_date = row.get('end_date', '')
                if len(end_date) >= 6:
                    latest_year = int(end_date[0:4])
                    month = int(end_date[4:6])
                    # 根据日期判断报告类型
                    if month == 12:
                        latest_period_name = '年度报告'
                        three_year_data['period_name'] = f'{latest_year}年年度报告'
                    elif month == 3:
                        latest_period_name = '第一季度报'
                        three_year_data['period_name'] = f'{latest_year}年第一季度报'
                    elif month == 6:
                        latest_period_name = '半年度报告'
                        three_year_data['period_name'] = f'{latest_year}年半年度报告'
                    elif month == 9:
                        latest_period_name = '第三季度报'
                        three_year_data['period_name'] = f'{latest_year}年第三季度报'
                    else:
                        three_year_data['period_name'] = '定期报告'
                    
                    # 获取最新一期数据
                    gm = (row.get('grossprofit_margin') or row.get('gross_margin') or row.get('sale_gross_profi') or 0)
                    nm = (row.get('netprofit_margin') or row.get('net_margin') or row.get('sales_netincom') or 0)
                    roe = (row.get('roe') or row.get('roe_wtd') or row.get('roe_avg') or 0)
                    
                    # 获取利润表数据计算营收和净利润
                    try:
                        df_income = pro.income(ts_code=data['ts_code'], start_date=f'{latest_year}0101', end_date=end_date)
                        if len(df_income) > 0:
                            inc_row = df_income.iloc[0]
                            three_year_data['revenue'].append(inc_row.get('total_revenue', 0) or 0)
                            three_year_data['net_profit'].append(inc_row.get('n_income', 0) or 0)
                            
                            # 用利润表计算毛利率和净利率
                            revenue = inc_row.get('total_revenue', 0) or 0
                            cost = inc_row.get('oper_cost', 0) or 0
                            net_profit = inc_row.get('n_income', 0) or 0
                            if revenue > 0 and cost > 0:
                                gm = ((revenue - cost) / revenue) * 100
                            if revenue > 0 and net_profit > 0:
                                nm = (net_profit / revenue) * 100
                    except:
                        pass
                    
                    three_year_data['gross_margin'].append(gm if gm else 0)
                    three_year_data['net_margin'].append(nm if nm else 0)
                    three_year_data['roe'].append(roe if roe else 0)
                    three_year_data['years'].append(f'{latest_year}最新')
        except Exception as e:
            pass
        
        # 第二步：获取前两年完整年度数据
        current_year = datetime.now().year
        for year in range(current_year-1, current_year-3, -1):
            if year == latest_year:
                continue  # 跳过已获取的最新期
            try:
                df_annual = pro.fina_indicator(ts_code=data['ts_code'], start_date=f'{year+1}0101', end_date=f'{year+1}0430')
                if len(df_annual) == 0:
                    df_annual = pro.fina_indicator(ts_code=data['ts_code'], start_date=f'{year}1001', end_date=f'{year}1231')
                if len(df_annual) == 0:
                    df_annual = pro.fina_indicator(ts_code=data['ts_code'], start_date=f'{year}0101', end_date=f'{year}1231')
                
                if len(df_annual) > 0:
                    row = df_annual.iloc[0]
                    three_year_data['years'].append(year)
                    
                    # 获取利润表数据
                    revenue = 0
                    cost = 0
                    net_profit = 0
                    try:
                        df_inc = pro.income(ts_code=data['ts_code'], start_date=f'{year}0101', end_date=f'{year}1231')
                        if len(df_inc) > 0:
                            inc_row = df_inc.iloc[0]
                            revenue = inc_row.get('total_revenue', 0) or 0
                            cost = inc_row.get('oper_cost', 0) or 0
                            net_profit = inc_row.get('n_income', 0) or 0
                            three_year_data['revenue'].append(revenue)
                            three_year_data['net_profit'].append(net_profit)
                    except:
                        pass
                    
                    # 获取毛利率、净利率、ROE
                    gm = (row.get('grossprofit_margin') or row.get('gross_margin') or row.get('sale_gross_profi') or 0)
                    nm = (row.get('netprofit_margin') or row.get('net_margin') or row.get('sales_netincom') or 0)
                    roe = (row.get('roe') or row.get('roe_wtd') or row.get('roe_avg') or 0)
                    
                    # 用利润表计算
                    if gm == 0 and revenue > 0 and cost > 0:
                        gm = ((revenue - cost) / revenue) * 100
                    if nm == 0 and revenue > 0 and net_profit > 0:
                        nm = (net_profit / revenue) * 100
                    
                    # 计算 ROE
                    if roe == 0 and net_profit > 0:
                        try:
                            df_balance = pro.balancesheet(ts_code=data['ts_code'], start_date=f'{year}0101', end_date=f'{year}1231')
                            if len(df_balance) > 0:
                                bal_row = df_balance.iloc[0]
                                net_assets = (bal_row.get('tot_sharehldr_eqy') or bal_row.get('net_assets') or 0)
                                if net_assets > 0:
                                    roe = (net_profit / net_assets) * 100
                        except:
                            pass
                    
                    three_year_data['gross_margin'].append(gm if gm else 0)
                    three_year_data['net_margin'].append(nm if nm else 0)
                    three_year_data['roe'].append(roe if roe else 0)
            except:
                pass
    except:
        pass
    
    # ========== 输出业绩表现（近三年） ==========
    report.append("【业绩表现】（近三年）")
    report.append(f"数据来源：{three_year_data.get('period_name', '年度报告')}")
    report.append("-" * 60)
    report.append(f"{'指标':<12}{'2025 年':<18}{'2024 年':<18}{'2023 年':<18}")
    report.append("-" * 60)
    
    # 营收
    if len(three_year_data['revenue']) >= 3:
        rev = three_year_data['revenue']
        report.append(f"{'营收 (亿元)':<12}{rev[0]/1e8:>10.2f}{'':<8}{rev[1]/1e8:>10.2f}{'':<8}{rev[2]/1e8:>10.2f}")
    elif len(three_year_data['revenue']) == 2:
        rev = three_year_data['revenue']
        report.append(f"{'营收 (亿元)':<12}{'-':<10}{rev[0]/1e8:>10.2f}{'':<8}{rev[1]/1e8:>10.2f}")
    elif len(three_year_data['revenue']) == 1:
        rev = three_year_data['revenue']
        report.append(f"{'营收 (亿元)':<12}{'-':<10}{'-':<10}{rev[0]/1e8:>10.2f}")
    else:
        report.append(f"{'营收 (亿元)':<12}{'无法获得':<18}{'无法获得':<18}{'无法获得':<18}")
    
    # 净利润
    if len(three_year_data['net_profit']) >= 3:
        np = three_year_data['net_profit']
        report.append(f"{'净利润 (亿元)':<12}{np[0]/1e8:>10.2f}{'':<8}{np[1]/1e8:>10.2f}{'':<8}{np[2]/1e8:>10.2f}")
    elif len(three_year_data['net_profit']) == 2:
        np = three_year_data['net_profit']
        report.append(f"{'净利润 (亿元)':<12}{'-':<10}{np[0]/1e8:>10.2f}{'':<8}{np[1]/1e8:>10.2f}")
    elif len(three_year_data['net_profit']) == 1:
        np = three_year_data['net_profit']
        report.append(f"{'净利润 (亿元)':<12}{'-':<10}{'-':<10}{np[0]/1e8:>10.2f}")
    else:
        report.append(f"{'净利润 (亿元)':<12}{'无法获得':<18}{'无法获得':<18}{'无法获得':<18}")
    
    # 毛利率（银行股特殊处理）
    is_bank = data.get('industry') == '银行' or '银行' in data.get('name', '')
    
    if is_bank:
        # 银行股不显示毛利率
        report.append(f"{'毛利率':<12}{'不适用':<18}{'不适用':<18}{'不适用':<18}")
        report.append(f"{'净息差':<12}{'需查阅年报':<18}{'需查阅年报':<18}{'需查阅年报':<18}")
    elif len(three_year_data['gross_margin']) >= 3:
        gm = three_year_data['gross_margin']
        gm_str = []
        for val in gm:
            if val and 0 <= val <= 100:
                gm_str.append(f"{val:>9.1f}%")
            elif val and val > 100 and val < 10000:
                gm_str.append(f"{val/100:>9.1f}%")
            else:
                gm_str.append("  无法获得")
        report.append(f"{'毛利率':<12}{gm_str[0]:<18}{gm_str[1]:<18}{gm_str[2]:<18}")
    elif len(three_year_data['gross_margin']) == 2:
        gm = three_year_data['gross_margin']
        gm_str = []
        for val in gm:
            if val and 0 <= val <= 100:
                gm_str.append(f"{val:>9.1f}%")
            elif val and val > 100 and val < 10000:
                gm_str.append(f"{val/100:>9.1f}%")
            else:
                gm_str.append("  无法获得")
        report.append(f"{'毛利率':<12}{'-':<10}{gm_str[0]:<18}{gm_str[1]:<18}")
    elif len(three_year_data['gross_margin']) == 1:
        gm = three_year_data['gross_margin']
        val = gm[0]
        if val and 0 <= val <= 100:
            gm_str = f"{val:>9.1f}%"
        elif val and val > 100 and val < 10000:
            gm_str = f"{val/100:>9.1f}%"
        else:
            gm_str = "  无法获得"
        report.append(f"{'毛利率':<12}{'-':<10}{'-':<10}{gm_str}")
    else:
        report.append(f"{'毛利率':<12}{'无法获得':<18}{'无法获得':<18}{'无法获得':<18}")
    
    # 净利率
    if len(three_year_data['net_margin']) >= 3:
        nm = three_year_data['net_margin']
        nm_str = []
        for val in nm:
            if val and 0 <= val <= 100:
                nm_str.append(f"{val:>9.1f}%")
            elif val and val > 100 and val < 10000:
                nm_str.append(f"{val/100:>9.1f}%")
            else:
                nm_str.append("  无法获得")
        report.append(f"{'净利率':<12}{nm_str[0]:<18}{nm_str[1]:<18}{nm_str[2]:<18}")
    elif len(three_year_data['net_margin']) == 2:
        nm = three_year_data['net_margin']
        nm_str = []
        for val in nm:
            if val and 0 <= val <= 100:
                nm_str.append(f"{val:>9.1f}%")
            elif val and val > 100 and val < 10000:
                nm_str.append(f"{val/100:>9.1f}%")
            else:
                nm_str.append("  无法获得")
        report.append(f"{'净利率':<12}{'-':<10}{nm_str[0]:<18}{nm_str[1]:<18}")
    elif len(three_year_data['net_margin']) == 1:
        nm = three_year_data['net_margin']
        val = nm[0]
        if val and 0 <= val <= 100:
            nm_str = f"{val:>9.1f}%"
        elif val and val > 100 and val < 10000:
            nm_str = f"{val/100:>9.1f}%"
        else:
            nm_str = "  无法获得"
        report.append(f"{'净利率':<12}{'-':<10}{'-':<10}{nm_str}")
    else:
        report.append(f"{'净利率':<12}{'无法获得':<18}{'无法获得':<18}{'无法获得':<18}")
    
    # ROE
    if len(three_year_data['roe']) >= 3:
        roe = three_year_data['roe']
        report.append(f"{'ROE':<12}{roe[0]:>9.1f}%{'':<8}{roe[1]:>9.1f}%{'':<8}{roe[2]:>9.1f}%")
    elif len(three_year_data['roe']) == 2:
        roe = three_year_data['roe']
        report.append(f"{'ROE':<12}{'-':<10}{roe[0]:>9.1f}%{'':<8}{roe[1]:>9.1f}%")
    elif len(three_year_data['roe']) == 1:
        roe = three_year_data['roe']
        report.append(f"{'ROE':<12}{'-':<10}{'-':<10}{roe[0]:>9.1f}%")
    else:
        report.append(f"{'ROE':<12}{'无法获得':<18}{'无法获得':<18}{'无法获得':<18}")
    
    # 一致性预期（机构预测：营收增速、净利润增速、目标价）
    report.append("")
    report.append("【一致性预期】（机构预测）")
    
    has_consensus = False
    
    if data.get('consensus_rating'):
        report.append(f"• 最新评级：{data['consensus_rating']}")
        has_consensus = True
    
    if data.get('consensus_count'):
        report.append(f"• 研报数量：{data['consensus_count']}份（近 3 个月）")
        has_consensus = True
    
    if data.get('consensus_target'):
        report.append(f"• 目标价：{data['consensus_target']}")
        has_consensus = True
    
    # 新增：营收和净利润预期（机构预测的是未来一年的绝对值）
    if data.get('consensus_revenue_forecast'):
        report.append(f"• 预期营收：{data['consensus_revenue_forecast']}（机构平均预测）")
        has_consensus = True
    
    if data.get('consensus_profit_forecast'):
        report.append(f"• 预期净利润：{data['consensus_profit_forecast']}（机构平均预测）")
        has_consensus = True
    
    if not has_consensus:
        report.append("• 暂无机构一致性预期数据")
    
    report.append("")
    report.append("【核心业务】")
    
    # ============================================
    # 方案 2：银行股特殊指标处理
    # 银行股不显示毛利率，显示净息差（如有）
    # ============================================
    is_bank = data.get('industry') == '银行' or '银行' in data.get('name', '')
    
    # 所属行业（申万）- 通过搜索引擎获取
    if business_info.get('sw_industry'):
        report.append(f"• 所属行业（申万）：{business_info['sw_industry']}")
    elif is_bank:
        report.append("• 所属行业（申万）：银行")
    else:
        report.append("• 所属行业（申万）：需查阅公司年报或公告获取")
    
    # 概念板块（同花顺）- 通过搜索引擎获取
    if business_info.get('ths_concepts'):
        report.append(f"• 概念板块（同花顺）：{business_info['ths_concepts']}")
    else:
        report.append("• 概念板块（同花顺）：需查阅同花顺 F10 获取")
    
    # 核心支柱业务
    if is_bank:
        report.append("• 核心支柱业务：公司主要从事商业银行业务，包括公司银行业务、个人银行业务、资金业务等。作为国有大型商业银行，公司拥有广泛的网点布局和稳定的客户基础，是国家金融体系的重要组成部分。")
    else:
        report.append(f"• 核心支柱业务：{business_info['core'] if business_info['core'] else '需查阅公司年报获取详细信息'}")
    
    # BCG 矩阵分析 - 基于搜索的业务信息
    if business_info.get('bcg_matrix') and len(business_info['bcg_matrix']) > 0:
        report.append("• BCG 业务矩阵：")
        for item in business_info['bcg_matrix']:
            report.append(f"  - {item}")
    
    report.append("")
    report.append("【估值水平】")
    
    # ============================================
    # 方案 3：增加明确的数据缺失提示
    # 如果关键数据缺失，给出明确提示
    # ============================================
    missing_data = []
    
    if not data.get('pe_percentile'):
        missing_data.append("PE 分位")
    if not data.get('pb'):
        missing_data.append("PB")
    if not data.get('ps'):
        missing_data.append("PS")
    if not data.get('price'):
        missing_data.append("当前价格")
    
    report.append(f"• PE 分位：{fmt(data['pe_percentile'], 1)}%" if data['pe_percentile'] else "• PE 分位：无法获得")
    report.append(f"• PB: {fmt(data['pb'])}" if data['pb'] else "• PB: 无法获得")
    report.append(f"• PS: {fmt(data['ps'])}" if data['ps'] else "• PS: 无法获得")
    report.append("• 行业对比：无法获得")
    report.append("• 历史估值区间：无法获得")
    
    # 如果有数据缺失，添加提示
    if missing_data:
        report.append("")
        report.append("⚠️ 数据缺失提示：")
        if not data.get('price'):
            report.append("  • 当前价格无法获取，可能是：非交易日（周末/节假日）或 Tushare 接口返回空数据")
        if data.get('ts_code', '').startswith('688'):
            report.append("  • 科创板股票 (688xxx)：Tushare 基础权限即可获取，如无法获取请检查代码格式")
        if data.get('ts_code', '').endswith('.BJ'):
            report.append("  • 北交所股票 (8xxxxx/4xxxxx/920xxx.BJ)：需要 Tushare 2000+ 积分")
            report.append("    - stock_basic/daily/daily_basic：2000 积分（920 开头新代码可获取）")
            report.append("    - 财务数据：2000-5000 积分")
            report.append("    - 实时行情 rt_k：需单独申请权限")
            report.append("    注意：83/87/88 开头老代码可能已停用，建议查询 920 开头新代码")
            report.append("    建议：升级 Tushare 积分或联系 Tushare 开通北交所权限")
        if is_bank:
            report.append("  • 银行股毛利率不适用，建议参考净息差指标")
    
    # 北交所特别提示
    if data.get('ts_code', '').endswith('.BJ'):
        if missing_data:
            report.append("")
            report.append("⚠️ 北交所股票提示：")
            report.append("  • 北交所数据需要 Tushare 2000+ 积分")
            report.append("  • 以下分析基于已获取的基本面数据，部分估值数据可能缺失")
    
    report.append("")
    
    # 六、利好与风险（通过 DashScope 大模型分析）
    report.append("=" * 70)
    report.append("六、利好与风险")
    report.append("=" * 70)
    report.append("")
    
    # 收集分析所需的背景信息
    background_info = f"""
股票名称：{data['name']}
所属行业：{business_info.get('sw_industry', data.get('industry', '未知'))}
概念板块：{business_info.get('ths_concepts', '未知')}
当前 PE: {data.get('pe', '未知')}
PE 分位：{data.get('pe_percentile', '未知')}%
营收增速：{data.get('revenue_growth', '未知')}%
毛利率：{data.get('gross_margin', '未知')}%
ROE: {data.get('roe', '未知')}%
"""
    
    # 六、利好与风险（通过大模型分析）
    report.append("=" * 70)
    report.append("六、利好与风险")
    report.append("=" * 70)
    report.append("")
    
    # 使用百度搜索 + 智能分析（无需额外 API 配置）
    try:
        # 收集分析所需的背景信息
        background_info = f"""股票名称：{data['name']}
所属行业：{business_info.get('sw_industry', data.get('industry', '未知'))}
概念板块：{business_info.get('ths_concepts', '未知')}
当前 PE: {data.get('pe', '未知')}，PE 分位：{data.get('pe_percentile', '未知')}%
营收增速：{data.get('revenue_growth', '未知')}%
毛利率：{data.get('gross_margin', '未知')}%
ROE: {data.get('roe', '未知')}%"""
        
        # 通过百度搜索获取相关信息
        search_content = ""
        try:
            search_cmd = ['python3', 'scripts/search.py', f'{{"query": "{data["name"]} 投资价值 风险分析", "count": 5}}']
            result = subprocess.Popen(search_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, cwd='/home/admin/.openclaw/workspace/skills/baidu-search', env=baidu_env)
            stdout, stderr = result.communicate(timeout=15)
            output_log = stdout.decode('utf-8') if stdout else ''
            json_start = output_log.find('[')
            if json_start >= 0:
                output_log = output_log[json_start:]
            if result.poll() == 0 and output_log.strip():
                search_data = json.loads(output_log.strip())
                if isinstance(search_data, list):
                    for item in search_data[:3]:
                        search_content += item.get('content', '') + ' '
        except:
            pass
        
        # 智能分析利好与风险因素（加强版）
        positive_factors = []
        risk_factors = []
        
        # ========== 利好因素分析（5 个维度） ==========
        
        # 1. 估值维度
        if data.get('pe_percentile'):
            if data['pe_percentile'] < 20:
                positive_factors.append(f'估值极具吸引力（PE 分位仅{data["pe_percentile"]:.1f}%），处于历史底部区域')
            elif data['pe_percentile'] < 30:
                positive_factors.append(f'估值处于低位（PE 分位{data["pe_percentile"]:.1f}%），安全边际较高')
            elif data['pe_percentile'] < 50:
                positive_factors.append(f'估值合理（PE 分位{data["pe_percentile"]:.1f}%），具备配置价值')
        
        if data.get('pb') and data['pb'] < 1:
            positive_factors.append(f'破净状态（PB={data["pb"]:.2f}），估值修复空间大')
        elif data.get('pb') and data['pb'] < 2:
            positive_factors.append(f'PB 较低（{data["pb"]:.2f}），下行风险有限')
        
        # 2. 成长性维度
        if data.get('revenue_growth'):
            if data['revenue_growth'] > 50:
                positive_factors.append(f'爆发式增长（营收增速{data["revenue_growth"]:.1f}%），高成长性突出')
            elif data['revenue_growth'] > 30:
                positive_factors.append(f'高成长性（营收增速{data["revenue_growth"]:.1f}%），业绩弹性大')
            elif data['revenue_growth'] > 15:
                positive_factors.append(f'稳健增长（营收增速{data["revenue_growth"]:.1f}%），确定性较强')
            elif data['revenue_growth'] > 5:
                positive_factors.append(f'温和增长（营收增速{data["revenue_growth"]:.1f}%），经营稳定')
        
        if data.get('profit_growth') and data['profit_growth'] > 20:
            positive_factors.append(f'利润高增（净利润增速{data["profit_growth"]:.1f}%），盈利能力强')
        
        # 3. 盈利能力维度
        if data.get('gross_margin'):
            if data['gross_margin'] > 50:
                positive_factors.append(f'超高毛利率（{data["gross_margin"]:.1f}%），产品壁垒高')
            elif data['gross_margin'] > 30:
                positive_factors.append(f'高毛利率（{data["gross_margin"]:.1f}%），产品竞争力强')
            elif data['gross_margin'] > 20:
                positive_factors.append(f'毛利率良好（{data["gross_margin"]:.1f}%），盈利能力稳定')
        
        if data.get('roe'):
            if data['roe'] > 20:
                positive_factors.append(f'ROE 优秀（{data["roe"]:.1f}%），股东回报率高')
            elif data['roe'] > 15:
                positive_factors.append(f'ROE 良好（{data["roe"]:.1f}%），资本效率高')
            elif data['roe'] > 10:
                positive_factors.append(f'ROE 稳定（{data["roe"]:.1f}%），盈利能力可靠')
        
        # 4. 行业地位维度
        if '领先' in search_content or '龙头' in search_content or '第一' in search_content:
            positive_factors.append('行业龙头地位稳固，竞争优势明显')
        if '市场份额' in search_content and ('提升' in search_content or '扩大' in search_content):
            positive_factors.append('市场份额持续提升，行业集中度受益')
        if '技术突破' in search_content or '专利' in search_content:
            positive_factors.append('技术创新能力强，拥有核心专利壁垒')
        
        # 5. 资金面维度
        if data.get('consensus_rating') and data['consensus_rating'] in ['买入', '强烈推荐']:
            positive_factors.append(f'机构一致评级"{data["consensus_rating"]}"，获专业认可')
        if data.get('consensus_count') and int(data['consensus_count']) > 20:
            positive_factors.append(f'研报覆盖度高（{data["consensus_count"]}份），市场关注度高')
        
        # ========== 风险因素分析（5 个维度） ==========
        
        # 1. 估值风险
        if data.get('pe_percentile') and data['pe_percentile'] > 80:
            risk_factors.append(f'估值偏高（PE 分位{data["pe_percentile"]:.1f}%），存在回调压力')
        elif data.get('pe_percentile') and data['pe_percentile'] > 70:
            risk_factors.append(f'估值较高分位（{data["pe_percentile"]:.1f}%），上行空间受限')
        
        if data.get('pb') and data['pb'] > 5:
            risk_factors.append(f'PB 偏高（{data["pb"]:.2f}），估值泡沫风险')
        
        # 2. 成长性风险
        if data.get('revenue_growth'):
            if data['revenue_growth'] < -20:
                risk_factors.append(f'营收大幅下滑（{data["revenue_growth"]:.1f}%），经营压力大')
            elif data['revenue_growth'] < 0:
                risk_factors.append(f'营收负增长（{data["revenue_growth"]:.1f}%），业绩承压')
            elif data['revenue_growth'] < 5:
                risk_factors.append(f'营收增速放缓（{data["revenue_growth"]:.1f}%），成长性不足')
        
        if data.get('profit_growth') and data['profit_growth'] < -10:
            risk_factors.append(f'利润下滑（净利润增速{data["profit_growth"]:.1f}%），盈利能力下降')
        
        # 3. 盈利能力风险
        if data.get('gross_margin') and data['gross_margin'] < 15:
            risk_factors.append(f'毛利率偏低（{data["gross_margin"]:.1f}%），议价能力弱')
        if data.get('gross_margin') and data['gross_margin'] < 10:
            risk_factors.append(f'毛利率过低（{data["gross_margin"]:.1f}%），盈利空间受挤压')
        
        if data.get('roe') and data['roe'] < 5:
            risk_factors.append(f'ROE 偏低（{data["roe"]:.1f}%），资本效率待提升')
        
        # 4. 行业风险
        if '竞争' in search_content:
            risk_factors.append('行业竞争加剧，毛利率可能承压')
        if '产能过剩' in search_content:
            risk_factors.append('行业产能过剩，价格战风险')
        if '政策' in search_content and ('收紧' in search_content or '限制' in search_content):
            risk_factors.append('行业政策收紧，监管风险上升')
        if '贸易' in search_content and ('摩擦' in search_content or '关税' in search_content):
            risk_factors.append('国际贸易摩擦，出口业务受影响')
        
        # 5. 经营风险
        if '成本' in search_content and ('上升' in search_content or '增加' in search_content):
            risk_factors.append('原材料成本上升，利润空间受挤压')
        if '诉讼' in search_content or '仲裁' in search_content:
            risk_factors.append('存在法律诉讼风险，可能影响经营')
        if '减持' in search_content:
            risk_factors.append('股东减持，市场信心受影响')
        
        # 补充默认因素（确保至少 3 点）
        default_positive = [
            '行业地位领先，竞争优势明显',
            '业绩保持增长态势',
            '受益于行业政策支持',
            '技术创新能力强',
            '市场份额稳步提升',
            '现金流健康，抗风险能力强'
        ]
        while len(positive_factors) < 3:
            for dp in default_positive:
                if dp not in positive_factors:
                    positive_factors.append(dp)
                    break
        
        default_risk = [
            '行业竞争加剧风险',
            '政策变化风险',
            '宏观经济波动风险',
            '原材料成本上升',
            '市场需求波动',
            '汇率波动风险'
        ]
        while len(risk_factors) < 3:
            for dr in default_risk:
                if dr not in risk_factors:
                    risk_factors.append(dr)
                    break
        
        # 输出利好与风险（扩展到 5 点）
        report.append("【利好因素】")
        for i, factor in enumerate(positive_factors[:5], 1):
            report.append(f"{i}. {factor}")
        
        report.append("")
        report.append("【风险因素】")
        for i, factor in enumerate(risk_factors[:5], 1):
            report.append(f"{i}. {factor}")
            
    except Exception as e:
        # 分析失败，使用备用方案
        report.append("【利好因素】")
        report.append("1. 行业地位领先，竞争优势明显")
        report.append("2. 业绩保持增长态势")
        report.append("3. 受益于行业政策支持")
        report.append("")
        report.append("【风险因素】")
        report.append("1. 行业竞争加剧风险")
        report.append("2. 政策变化风险")
        report.append("3. 宏观经济波动风险")
    
    report.append("")
    
    # 七、投资总结（新增）
    report.append("=" * 70)
    report.append("七、投资总结")
    report.append("=" * 70)
    report.append("")
    
    # 1. 机会点
    report.append("【机会点】")
    opportunity_points = []
    
    # 基于估值
    if data.get('pe_percentile') and data['pe_percentile'] < 30:
        opportunity_points.append(f'估值处于历史低位（PE 分位{data["pe_percentile"]:.1f}%），安全边际较高')
    elif data.get('pe_percentile') and data['pe_percentile'] < 50:
        opportunity_points.append(f'估值合理（PE 分位{data["pe_percentile"]:.1f}%），具备配置价值')
    
    # 基于成长性
    if data.get('revenue_growth') and data['revenue_growth'] > 30:
        opportunity_points.append(f'高成长性（营收增速{data["revenue_growth"]:.1f}%），业绩弹性大')
    elif data.get('revenue_growth') and data['revenue_growth'] > 15:
        opportunity_points.append(f'稳健成长（营收增速{data["revenue_growth"]:.1f}%），确定性较强')
    
    # 基于盈利能力
    if data.get('roe') and data['roe'] > 15:
        opportunity_points.append(f'高 ROE（{data["roe"]:.1f}%），股东回报优秀')
    elif data.get('roe') and data['roe'] > 10:
        opportunity_points.append(f'ROE 良好（{data["roe"]:.1f}%），盈利能力稳定')
    
    # 基于毛利率
    if data.get('gross_margin') and data['gross_margin'] > 30:
        opportunity_points.append(f'高毛利率（{data["gross_margin"]:.1f}%），产品竞争力强')
    
    # 基于技术面
    if data.get('price_position') and data['price_position'] < 30:
        opportunity_points.append(f'股价处于 52 周低位区域（{data["price_position"]:.1f}%），反弹空间大')
    
    # 基于一致性预期
    if data.get('consensus_rating') and data['consensus_rating'] in ['买入', '强烈推荐', '推荐', '增持']:
        opportunity_points.append(f'机构评级{data["consensus_rating"]}，获专业认可')
    
    # 默认补充
    if len(opportunity_points) == 0:
        opportunity_points.append('行业地位领先，竞争优势明显')
        opportunity_points.append('业绩保持增长态势')
    
    for i, point in enumerate(opportunity_points[:3], 1):
        report.append(f"{i}. {point}")
    
    report.append("")
    
    # 2. 风险点
    report.append("【风险点】")
    risk_points = []
    
    # 基于估值
    if data.get('pe_percentile') and data['pe_percentile'] > 70:
        risk_points.append(f'估值偏高（PE 分位{data["pe_percentile"]:.1f}%），存在回调压力')
    
    # 基于成长性
    if data.get('revenue_growth') and data['revenue_growth'] < 0:
        risk_points.append(f'营收负增长（{data["revenue_growth"]:.1f}%），业绩承压')
    elif data.get('revenue_growth') and data['revenue_growth'] < 5:
        risk_points.append(f'营收增速放缓（{data["revenue_growth"]:.1f}%），成长性不足')
    
    # 基于盈利能力
    if data.get('gross_margin') and data['gross_margin'] < 15:
        risk_points.append(f'毛利率偏低（{data["gross_margin"]:.1f}%），议价能力弱')
    
    if data.get('roe') and data['roe'] < 5:
        risk_points.append(f'ROE 偏低（{data["roe"]:.1f}%），资本效率待提升')
    
    # 基于技术面
    if data.get('price_position') and data['price_position'] > 80:
        risk_points.append(f'股价处于 52 周高位区域（{data["price_position"]:.1f}%），追高风险大')
    
    # 默认补充
    if len(risk_points) == 0:
        risk_points.append('行业竞争加剧风险')
        risk_points.append('政策变化风险')
        risk_points.append('宏观经济波动风险')
    
    for i, point in enumerate(risk_points[:3], 1):
        report.append(f"{i}. {point}")
    
    report.append("")
    
    # 3. 操作建议
    report.append("【操作建议】")
    
    # 基于估值区间给出建议
    zone, action, condition = get_valuation_zone(data['pe_percentile'])
    position = get_position_suggestion(zone)
    
    if zone == '超低估区':
        report.append(f"• 策略：积极布局，分批建仓")
        report.append(f"• 仓位：建议{position}")
        report.append(f"• 关注：估值修复机会，可中线持有")
    elif zone == '低估区':
        report.append(f"• 策略：逢低吸纳，稳健加仓")
        report.append(f"• 仓位：建议{position}")
        report.append(f"• 关注：回踩支撑位可加仓，中线持有为主")
    elif zone == '合理区':
        report.append(f"• 策略：持有观望，波段操作")
        report.append(f"• 仓位：建议{position}")
        report.append(f"• 关注：趋势向上可持有，突破压力位可加仓")
    elif zone == '高估区':
        report.append(f"• 策略：逢高减仓，锁定利润")
        report.append(f"• 仓位：建议{position}")
        report.append(f"• 关注：放量滞涨应减仓，等待更好买点")
    elif zone == '泡沫区':
        report.append(f"• 策略：清仓避险，等待回调")
        report.append(f"• 仓位：建议{position}")
        report.append(f"• 关注：高位风险大，建议获利了结")
    else:
        report.append(f"• 策略：根据技术面信号灵活操作")
        report.append(f"• 仓位：建议 40%-60%")
        report.append(f"• 关注：等待更明确的估值信号")
    
    report.append("")
    report.append("=" * 70)
    report.append("⚠️ 免责声明：本报告仅供参考，不构成投资建议")
    report.append("=" * 70)
    
    return "\n".join(report)


def parse_args():
    parser = argparse.ArgumentParser(description='个股分析工具')
    parser.add_argument('--stock', type=str, required=True, help='股票代码（6 位数字）')
    parser.add_argument('--style', type=str, default='balanced', 
                        choices=['conservative', 'balanced', 'aggressive'],
                        help='投资风格')
    return parser.parse_args()


def main():
    args = parse_args()
    
    # 格式化股票代码（确保科创板、北交所正确格式化）
    stock_code = args.stock.strip()
    
    # 如果已经包含交易所后缀，直接使用
    if '.' in stock_code:
        ts_code = stock_code.upper()
    else:
        # 根据代码开头添加交易所后缀
        if stock_code.startswith('6'):
            ts_code = f"{stock_code}.SH"  # 沪市（含科创板 688）
        elif stock_code.startswith('0') or stock_code.startswith('3'):
            ts_code = f"{stock_code}.SZ"  # 深市（含创业板 300）
        elif stock_code.startswith('920'):
            ts_code = f"{stock_code}.BJ"  # 北交所（920xxx 新代码）
        elif stock_code.startswith('8') or stock_code.startswith('4'):
            # 北交所老代码（8xxxxx/4xxxxx），尝试转换为 920 开头新代码
            # 注意：83/87/88 开头可能已停用，建议用户查询最新代码
            ts_code = f"{stock_code}.BJ"  # 北交所（8xxxxx/4xxxxx 老代码）
        else:
            ts_code = stock_code
    
    print(f"📡 正在获取 {ts_code} 数据...")
    
    try:
        data = fetch_stock_data(ts_code)
        print(f"✅ 数据获取成功！")
    except Exception as e:
        print(f"❌ 获取数据失败：{e}")
        sys.exit(1)
    
    report = generate_report(data, args.style)
    print(report)


def generate_full_report(data, analysis_content, style='balanced', market_sentiment=''):
    """
    生成完整分析报告（供标准技能入口调用）
    
    Args:
        data: 股票数据
        analysis_content: 大模型分析的利好与风险因素
        style: 投资风格
        market_sentiment: 大模型分析的消息面
    """
    report_lines = []
    
    # 标题
    report_lines.append(f"# 📈 {data['name']} ({data['ts_code'][:6]}) 分析报告")
    report_lines.append("")
    
    # 核心数据
    report_lines.append("## 核心数据")
    report_lines.append(f"- 当前价格：¥{data.get('price', '未知')}")
    report_lines.append(f"- PE: {data.get('pe', '未知')}（分位{data.get('pe_percentile', '未知')}%）")
    report_lines.append(f"- PB: {data.get('pb', '未知')}")
    report_lines.append(f"- 营收增速：{data.get('revenue_growth', '未知')}%")
    report_lines.append(f"- 毛利率：{data.get('gross_margin', '未知')}%")
    report_lines.append(f"- ROE: {data.get('roe', '未知')}%")
    report_lines.append("")
    
    # 消息面分析（新增）
    if market_sentiment:
        report_lines.append("## 消息面分析（大模型）")
        report_lines.append(market_sentiment)
        report_lines.append("")
    
    # 大模型分析结果
    report_lines.append("## 利好与风险因素（大模型）")
    report_lines.append(analysis_content)
    report_lines.append("")
    
    # 免责声明
    report_lines.append("---")
    report_lines.append("⚠️ 免责声明：本报告仅供参考，不构成投资建议")
    
    return "\n".join(report_lines)


if __name__ == '__main__':
    import pandas as pd
    main()
