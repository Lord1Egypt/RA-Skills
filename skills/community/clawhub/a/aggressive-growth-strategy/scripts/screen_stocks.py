#!/usr/bin/env python3
"""
激进成长选股筛选器
基于"激进成长投研体系"七标准筛选A股小盘成长股

Usage:
  python3 screen_stocks.py --codes "sz.300308,sh.688146,sz.300769"
  python3 screen_stocks.py --industry "半导体"
  python3 screen_stocks.py --codes "sz.300308" --max-mcap 50 --min-roe 10 --min-growth 15

Output: JSON (stdout)，进度信息输出到stderr

数据源: akshare > baostock > 东方财富API (四层降级，Tushare MCP由Agent直接调用)
财务验证: 东方财富datacenter API交叉验证 (2026-07-31铁律)
"""

import pandas as pd
import argparse
import json
import sys
from datetime import datetime, timedelta

# 导入共享数据源模块
try:
    from data_source import (
        get_kline, get_spot, get_profit_data, get_growth_data,
        get_stock_industry, get_index_stocks, verify_financial_data,
        source_label, format_data_source_line,
        SOURCE_AKSHARE, SOURCE_BAOSTOCK, SOURCE_EASTMONEY, SOURCE_FAILED
    )
except ImportError:
    # 当直接运行时，添加脚本目录到path
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_source import (
        get_kline, get_spot, get_profit_data, get_growth_data,
        get_stock_industry, get_index_stocks, verify_financial_data,
        source_label, format_data_source_line,
        SOURCE_AKSHARE, SOURCE_BAOSTOCK, SOURCE_EASTMONEY, SOURCE_FAILED
    )

# ============================================================
# 科技和消费行业关键词
# ============================================================
TECH_KEYWORDS = [
    '电子', '半导体', '芯片', '集成电路', '软件', '计算机', '通信', '科技',
    '智能', '人工智能', '机器人', '新能源', '光伏', '电池', '军工', '航天',
    '航空', '信息安全', '大数据', '云计算', '物联网', '5G', '光电',
    '新材料', '自动化', '精密制造'
]
CONSUMER_KEYWORDS = [
    '消费', '食品', '饮料', '白酒', '家电', '家居', '服装', '纺织',
    '零售', '商业', '旅游', '酒店', '餐饮', '医药', '医疗', '生物',
    '制药', '中药', '保健', '化妆品', '宠物', '教育', '传媒', '游戏',
    '影视', '广告', '文娱'
]


def normalize_code(code):
    """标准化股票代码为baostock格式"""
    code = code.strip()
    if code.startswith('sh.') or code.startswith('sz.'):
        return code
    code = code.replace('sh', '').replace('sz', '').replace('.', '')
    if code.startswith('6') or code.startswith('9'):
        return f'sh.{code}'
    return f'sz.{code}'


def code_to_secucode(code):
    """baostock代码 -> 东方财富secucode (sz.300308 -> 300308.SZ)"""
    if code.startswith('sh.'):
        return f"{code[3:]}.SH"
    elif code.startswith('sz.'):
        return f"{code[3:]}.SZ"
    return code


def is_target_industry(industry):
    """判断是否属于科技或消费行业"""
    if not industry:
        return False, '未知'
    for kw in TECH_KEYWORDS:
        if kw in industry:
            return True, '科技'
    for kw in CONSUMER_KEYWORDS:
        if kw in industry:
            return True, '消费'
    return False, industry


def get_latest_quarter():
    """获取最新可用财报季度（考虑2个月延迟）"""
    now = datetime.now()
    year = now.year
    month = now.month
    if month <= 4:
        return year - 1, 3
    elif month <= 6:
        return year - 1, 4
    elif month <= 8:
        return year, 1
    elif month <= 10:
        return year, 2
    else:
        return year, 3


def estimate_market_cap(close, volume, turn):
    """通过换手率反推流通市值（亿元）"""
    try:
        close = float(close)
        volume = float(volume)
        turn = float(turn)
        if turn > 0 and volume > 0:
            float_shares = volume * 100 / turn
            market_cap = close * float_shares / 1e8
            return round(market_cap, 2)
    except (ValueError, TypeError):
        pass
    return None


def calculate_price_percentile(kline_data, lookback=250):
    """计算当前价格在历史区间的百分位（0-100）
    
    参数: kline_data - get_kline()返回的data_list
    """
    if not kline_data or len(kline_data) < 10:
        return None
    recent = kline_data[-lookback:]
    try:
        close_values = [float(d['close']) for d in recent if d['close']]
        if not close_values:
            return None
        current = close_values[-1]
        high = max(close_values)
        low = min(close_values)
        if high == low:
            return 50.0
        percentile = (current - low) / (high - low) * 100
        return round(percentile, 1)
    except (ValueError, TypeError):
        return None


def screen_single_stock(code, args):
    """对单只股票执行七标准筛选
    
    返回: result dict (包含pass/score/criteria/fail_reason/data_sources)
    """
    result = {
        'code': code,
        'pass': True,
        'score': 0,
        'criteria': {},
        'fail_reason': None,
        'data_sources': {}  # 记录每项数据的数据来源
    }

    # === 标准1: 赛道 ===
    industry, ind_source = get_stock_industry(code)
    result['data_sources']['industry'] = source_label(ind_source)
    if industry and industry != '未知':
        is_target, sector = is_target_industry(industry)
        result['criteria']['industry'] = industry
        result['criteria']['sector'] = sector
        if is_target:
            result['score'] += 10
        else:
            result['pass'] = False
            result['fail_reason'] = f'行业({industry})不在科技/消费范围'
            return result
    else:
        result['criteria']['industry'] = '未分类'
        result['criteria']['sector'] = '未知'

    # === 获取K线数据 (通过data_source模块降级获取) ===
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=400)).strftime('%Y-%m-%d')
    kline_data, kline_source = get_kline(code, start_date, end_date, adjust='qfq')
    result['data_sources']['kline'] = source_label(kline_source)

    if not kline_data:
        result['pass'] = False
        result['fail_reason'] = '⚠️ K线数据获取失败（所有数据源均不可用）'
        return result

    latest = kline_data[-1]
    try:
        close = float(latest.get('close', 0))
        volume = float(latest.get('volume', 0))
        turn = float(latest.get('turn', 0)) if latest.get('turn') else 0
        # baostock K线中可能包含peTTM/pbMRQ
        pe = float(latest.get('peTTM', 0)) if latest.get('peTTM') else None
        pb = float(latest.get('pbMRQ', 0)) if latest.get('pbMRQ') else None
    except (ValueError, TypeError):
        result['pass'] = False
        result['fail_reason'] = 'K线数据解析失败'
        return result

    is_st = str(latest.get('isST', 0))

    result['criteria']['close'] = close
    result['criteria']['pe'] = pe
    result['criteria']['pb'] = pb
    result['criteria']['turn'] = turn

    # 如果K线数据中没有PE/PB，尝试从实时行情获取
    if pe is None or pe == 0:
        spot_data, spot_source = get_spot(code)
        if spot_data:
            pe = float(spot_data.get('pe', 0)) if spot_data.get('pe') else None
            pb = float(spot_data.get('pb', 0)) if spot_data.get('pb') else None
            result['criteria']['pe'] = pe
            result['criteria']['pb'] = pb
            result['data_sources']['spot'] = source_label(spot_source)

    # === 标准7（排除项）: ST检查 ===
    if is_st == '1':
        result['pass'] = False
        result['fail_reason'] = 'ST股，排除'
        return result

    # === 标准7: 价格检查 ===
    if close < 2:
        result['pass'] = False
        result['fail_reason'] = f'股价{close:.2f}元低于2元，有退市风险'
        return result

    # === 标准2: 市值 ===
    market_cap = estimate_market_cap(close, volume, turn)
    result['criteria']['market_cap'] = market_cap
    if market_cap is not None:
        if market_cap <= args.max_mcap:
            result['score'] += 20
            if market_cap < 30:
                result['score'] += 10
        else:
            result['pass'] = False
            result['fail_reason'] = f'流通市值{market_cap:.1f}亿超过{args.max_mcap}亿上限'
            return result

    # === 标准5: 位置 ===
    percentile = calculate_price_percentile(kline_data)
    result['criteria']['price_percentile'] = percentile
    if percentile is not None:
        if percentile <= 50:
            result['score'] += 20
            if percentile < 30:
                result['score'] += 10
        else:
            result['pass'] = False
            result['fail_reason'] = f'价格位置{percentile:.0f}%偏高，非左侧布局'
            return result

    # === 标准3: ROE (通过data_source模块降级获取) ===
    year, quarter = get_latest_quarter()
    profit_data, profit_source = get_profit_data(code, year, quarter)
    result['data_sources']['profit'] = source_label(profit_source)

    if profit_data:
        roe_val = profit_data.get('roeAvg', 0)
        try:
            roe = float(roe_val) * 100 if abs(float(roe_val)) < 1 else float(roe_val)
        except (ValueError, TypeError):
            roe = 0
        result['criteria']['roe'] = round(roe, 2)
        result['criteria']['report_period'] = f'{year}Q{quarter}'

        if roe >= args.min_roe:
            result['score'] += 15
            if roe > 15:
                result['score'] += 5
        else:
            result['pass'] = False
            result['fail_reason'] = f'ROE {roe:.1f}%低于{args.min_roe}%'
            return result
    else:
        result['criteria']['roe'] = None
        result['criteria']['report_period'] = f'{year}Q{quarter}'
        result['data_sources']['profit'] = '⚠️ 财务数据获取失败'

    # === 标准4: 成长性 (通过data_source模块降级获取) ===
    growth_data, growth_source = get_growth_data(code, year, quarter)
    result['data_sources']['growth'] = source_label(growth_source)

    if growth_data:
        yoy_ni = float(growth_data.get('YOYNI', 0)) if growth_data.get('YOYNI') else 0
        result['criteria']['yoy_ni'] = round(yoy_ni, 2)

        if yoy_ni >= args.min_growth:
            result['score'] += 15
            if yoy_ni > 30:
                result['score'] += 5
        else:
            result['pass'] = False
            result['fail_reason'] = f'净利润同比增长{yoy_ni:.1f}%低于{args.min_growth}%'
            return result
    else:
        result['criteria']['yoy_ni'] = None
        result['data_sources']['growth'] = '⚠️ 成长数据获取失败'

    # === 财务数据交叉验证 (2026-07-31 铁律要求) ===
    secucode = code_to_secucode(code)
    verified = verify_financial_data(secucode)
    if verified:
        result['data_sources']['financial_verification'] = '东方财富datacenter ✓'
        result['criteria']['verified_netprofit'] = verified.get('parent_netprofit')
        result['criteria']['verified_revenue'] = verified.get('total_operate_income')
        result['criteria']['verified_yoy_netprofit'] = verified.get('yoy_netprofit')
        result['criteria']['verified_report_date'] = verified.get('report_date')
    else:
        result['data_sources']['financial_verification'] = '⚠️ 财务数据未验证（datacenter API不可用）'

    # === 标准6: 指数路径 ===
    in_index = False
    for idx_code, idx_name in [('sz50', '上证50'), ('hs300', '沪深300')]:
        idx_stocks, idx_source = get_index_stocks(idx_code)
        if idx_stocks and code in idx_stocks:
            in_index = True
            result['criteria']['in_index'] = idx_name
            result['data_sources']['index'] = source_label(idx_source)
            break
    if not in_index:
        result['criteria']['in_index'] = '否'
        result['score'] += 5
        result['data_sources']['index'] = 'baostock'  # 默认来源

    # === 估值加分 ===
    if pe and 0 < pe < 30:
        result['score'] += 10

    return result


def main():
    parser = argparse.ArgumentParser(description='激进成长选股筛选器')
    parser.add_argument('--codes', type=str, help='股票代码列表（逗号分隔）')
    parser.add_argument('--industry', type=str, help='行业关键词')
    parser.add_argument('--max-mcap', type=float, default=50, help='最大流通市值（亿元，默认50）')
    parser.add_argument('--min-roe', type=float, default=8, help='最低ROE%%（默认8）')
    parser.add_argument('--min-growth', type=float, default=10, help='最低净利润同比增长%%（默认10）')
    args = parser.parse_args()

    if not args.codes and not args.industry:
        print('错误：请提供 --codes 或 --industry 参数', file=sys.stderr)
        sys.exit(1)

    # baostock login (data_source模块中baostock层需要已登录)
    import baostock as bs
    _stdout = sys.stdout
    sys.stdout = sys.stderr
    lg = bs.login()
    sys.stdout = _stdout
    if lg.error_code != '0':
        print(json.dumps({'error': f'baostock登录失败: {lg.error_msg}'}, ensure_ascii=False))
        sys.exit(1)

    try:
        # 获取行业分类 (baostock)
        industry_rs = bs.query_stock_industry()
        industry_df = industry_rs.get_data()

        # 确定股票列表
        if args.codes:
            stock_codes = [normalize_code(c) for c in args.codes.split(',')]
        else:
            # 通过行业关键词筛选
            if industry_df is not None and len(industry_df) > 0:
                mask = industry_df['industry'].str.contains(args.industry, na=False)
                stock_codes = industry_df[mask]['code'].tolist()
                print(f"行业'{args.industry}'匹配到 {len(stock_codes)} 只股票", file=sys.stderr)
            else:
                # industry_df为空时，用data_source模块获取全部股票列表
                from data_source import get_stock_list
                all_stocks, list_source = get_stock_list()
                stock_codes = [s['code'] for s in all_stocks if args.industry in s.get('code_name', '')]
                print(f"行业'{args.industry}'通过{source_label(list_source)}匹配到 {len(stock_codes)} 只股票", file=sys.stderr)

        # 逐只筛选
        results = []
        for i, code in enumerate(stock_codes):
            print(f"[{i+1}/{len(stock_codes)}] 筛选 {code}...", file=sys.stderr)
            try:
                result = screen_single_stock(code, args)
            except Exception as e:
                result = {
                    'code': code,
                    'pass': False,
                    'score': 0,
                    'criteria': {},
                    'fail_reason': f'筛选异常: {str(e)}',
                    'data_sources': {}
                }
            results.append(result)

        # 排序：通过的在前，按分数降序
        results.sort(key=lambda x: (x['pass'], x['score']), reverse=True)

        # 输出JSON
        output = {
            'screen_date': datetime.now().strftime('%Y-%m-%d'),
            'screen_params': {
                'max_mcap': args.max_mcap,
                'min_roe': args.min_roe,
                'min_growth': args.min_growth
            },
            'total_screened': len(results),
            'passed': len([r for r in results if r['pass']]),
            'failed': len([r for r in results if not r['pass']]),
            'results': results,
            'data_source_note': '数据源降级链: akshare > baostock > 东方财富API. Tushare MCP由Agent直接调用优先于以上所有源。财务数据经东方财富datacenter API交叉验证。'
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    finally:
        _stdout = sys.stdout
        sys.stdout = sys.stderr
        bs.logout()
        sys.stdout = _stdout


if __name__ == '__main__':
    main()
