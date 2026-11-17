#!/usr/bin/env python3
"""
激进成长市场季节判断器
判断当前A股市场处于春夏秋冬哪一季，给出仓位建议

Usage:
  python3 judge_market.py

Output: JSON（stdout），进度信息输出到stderr

数据源: akshare > baostock > 东方财富API (四层降级，Tushare MCP由Agent直接调用优先)
"""

import pandas as pd
import json
import sys
import os
from datetime import datetime, timedelta
from collections import Counter

# 导入共享数据源模块
try:
    from data_source import (
        get_kline, source_label,
        SOURCE_AKSHARE, SOURCE_BAOSTOCK, SOURCE_EASTMONEY, SOURCE_FAILED
    )
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_source import (
        get_kline, source_label,
        SOURCE_AKSHARE, SOURCE_BAOSTOCK, SOURCE_EASTMONEY, SOURCE_FAILED
    )


def safe_float(val, default=None):
    try:
        return float(val) if val and val != '' else default
    except (ValueError, TypeError):
        return default


def _akshare_get_index_kline(code, start_date, end_date):
    """akshare指数专用API获取K线

    akshare的stock_zh_a_hist()不支持指数代码，需用stock_zh_index_daily()
    code格式: sh.000001 -> 000001 (沪) / sz.399006 -> 399006 (深)
    """
    try:
        import akshare as ak
        # 转换baostock代码为纯数字代码
        pure_code = code.split('.')[1]
        # 使用akshare指数日线接口
        df = ak.stock_zh_index_daily(symbol=f"sh{pure_code}" if code.startswith('sh.') else f"sz{pure_code}")
        if df is None or df.empty:
            return [], SOURCE_FAILED
        # 筛选日期范围
        df['date'] = df['date'].astype(str)
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        records = []
        for _, row in df.iterrows():
            records.append({
                'date': str(row.get('date', '')),
                'close': safe_float(row.get('close')),
                'volume': safe_float(row.get('volume')),
                'amount': safe_float(row.get('amount')),
                'pctChg': safe_float(row.get('pct_chg') if 'pct_chg' in row else row.get('change_pct')),
                'peTTM': None,  # akshare指数接口不提供PE
                'pbMRQ': None,
            })
        return records, SOURCE_AKSHARE
    except Exception:
        return [], SOURCE_FAILED


def _baostock_get_index_kline(code, start_date, end_date):
    """baostock获取指数K线（含PE/PB）"""
    try:
        import baostock as bs
        rs = bs.query_history_k_data_plus(
            code,
            "date,close,volume,amount,peTTM,pbMRQ,pctChg",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"
        )
        if rs.error_code != '0':
            return [], SOURCE_FAILED
        records = []
        while rs.next():
            row = rs.get_row_data()
            records.append({
                'date': row[0],
                'close': safe_float(row[1]),
                'volume': safe_float(row[2]),
                'amount': safe_float(row[3]),
                'peTTM': safe_float(row[4]),
                'pbMRQ': safe_float(row[5]),
                'pctChg': safe_float(row[6]),
            })
        return records, SOURCE_BAOSTOCK
    except Exception:
        return [], SOURCE_FAILED


def get_index_data(code, days=450):
    """获取指数K线数据（四层降级：akshare指数API -> baostock -> 东方财富API）

    指数代码使用baostock格式（sh.000001, sz.399006等）
    注意：akshare的stock_zh_a_hist()不支持指数代码，需用stock_zh_index_daily()
    """
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days + 60)).strftime('%Y-%m-%d')

    # 1. 尝试akshare指数专用API
    kline_list, source = _akshare_get_index_kline(code, start_date, end_date)
    if kline_list:
        df = pd.DataFrame(kline_list)
        for col in ['close', 'volume', 'amount', 'peTTM', 'pbMRQ', 'pctChg']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: safe_float(x, 0))
        return df, source_label(source)

    # 2. 降级至baostock（支持PE/PB）
    kline_list, source = _baostock_get_index_kline(code, start_date, end_date)
    if kline_list:
        df = pd.DataFrame(kline_list)
        for col in ['close', 'volume', 'amount', 'peTTM', 'pbMRQ', 'pctChg']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: safe_float(x, 0))
        return df, source_label(source)

    # 3. 所有源失败
    return pd.DataFrame(), '⚠️ 数据获取失败'


def calculate_ma(df, periods=[20, 60, 250]):
    """计算均线"""
    result = {}
    df['close'] = df['close'].astype(float)
    for p in periods:
        if len(df) >= p:
            result[f'ma{p}'] = round(df['close'].tail(p).mean(), 2)
        else:
            result[f'ma{p}'] = None
    return result


def calculate_percentile(df, column='close', lookback=250):
    """计算当前值在历史区间的百分位"""
    if len(df) < 10:
        return None
    df = df.tail(lookback)
    values = df[column].astype(float)
    current = float(values.iloc[-1])
    high = values.max()
    low = values.min()
    if high == low:
        return 50.0
    return round((current - low) / (high - low) * 100, 1)


def calculate_volume_trend(df, short=5, long=60):
    """计算成交量趋势：近5日均量 vs 近60日均量"""
    if len(df) < long:
        long = min(long, len(df) - 1)
    if len(df) < short + 1:
        return None
    df['amount'] = df['amount'].astype(float)
    short_avg = df['amount'].tail(short).mean()
    long_avg = df['amount'].tail(long).mean()
    if long_avg == 0:
        return None
    return round(short_avg / long_avg, 2)


def determine_season(ma_data, price_percentile, vol_trend, pe_percentile):
    """根据量化指标判断市场季节"""

    ma20 = ma_data.get('ma20')
    ma60 = ma_data.get('ma60')
    ma250 = ma_data.get('ma250')

    # 均线排列判断
    ma_bullish = False
    ma_bearish = False
    ma_flat = False

    if ma20 and ma60:
        if ma20 > ma60:
            ma_bullish = True
        elif ma20 < ma60:
            ma_bearish = True
        else:
            ma_flat = True

    if ma250 and ma20 and ma60:
        if ma20 > ma60 > ma250:
            ma_bullish = True  # 完整多头排列
        elif ma20 < ma60 < ma250:
            ma_bearish = True  # 完整空头排列

    # 季节判断
    if ma_bearish and (price_percentile is None or price_percentile < 30):
        vol_shrinking = vol_trend is not None and vol_trend < 0.7
        if vol_shrinking:
            return '冬歇', '空头排列+缩量+低位，系统性风险中'
        else:
            return '冬歇', '空头排列+低位，可能接近底部但风险未消'

    if ma_bearish and price_percentile and price_percentile > 30:
        return '冬歇', '空头排列+中高位，趋势下行中'

    if ma_flat or (ma20 and ma60 and abs(ma20 - ma60) / ma60 < 0.02):
        # 均线缠绕
        if price_percentile and price_percentile < 40:
            vol_warming = vol_trend is not None and vol_trend > 1.0
            if vol_warming:
                return '春耕', '均线走平+低位+温和放量，底部启动信号'
            else:
                return '春耕', '均线走平+低位，等待放量确认'
        else:
            return '春耕', '均线缠绕，方向待确认'

    if ma_bullish:
        if price_percentile and price_percentile > 70:
            vol_surge = vol_trend is not None and vol_trend > 1.5
            if vol_surge:
                return '秋收', '多头排列+高位+天量，主升浪/赶顶阶段'
            else:
                return '秋收', '多头排列+高位，需警惕滞涨'
        elif price_percentile and price_percentile > 40:
            return '夏耘', '多头排列+中位，趋势确认期'
        else:
            return '春耕', '多头排列但位置偏低，仍在布局期'

    return '春耕', '默认春耕，需结合宏观判断'


def analyze_index(code, name):
    """分析单个指数"""
    df, data_src = get_index_data(code)

    if df.empty:
        return {
            'name': name,
            'code': code,
            'error': '⚠️ 数据获取失败（所有数据源均不可用）',
            'data_source': '⚠️ 数据获取失败'
        }

    latest = df.iloc[-1]
    close = safe_float(latest.get('close'), 0)
    pe = safe_float(latest.get('peTTM'))
    pb = safe_float(latest.get('pbMRQ'))

    ma_data = calculate_ma(df)
    price_percentile = calculate_percentile(df)
    pe_percentile = calculate_percentile(df, 'peTTM') if pe else None
    vol_trend = calculate_volume_trend(df)

    season, reason = determine_season(ma_data, price_percentile, vol_trend, pe_percentile)

    return {
        'name': name,
        'code': code,
        'close': close,
        'pe': pe,
        'pb': pb,
        'ma20': ma_data.get('ma20'),
        'ma60': ma_data.get('ma60'),
        'ma250': ma_data.get('ma250'),
        'price_percentile': price_percentile,
        'pe_percentile': pe_percentile,
        'volume_trend': vol_trend,
        'season': season,
        'season_reason': reason,
        'data_source': data_src
    }


def get_position_advice(season):
    """根据季节给出仓位建议"""
    advice = {
        '春耕': {
            'total_position': '30-50%',
            'single_max': '10%',
            'strategy': '逐步布局优质标的，分批试探。春耕期是左侧布局的最佳窗口，但需要耐心等待趋势确认。'
        },
        '夏耘': {
            'total_position': '50-70%',
            'single_max': '15%',
            'strategy': '持有为主，趋势确认后加仓。夏耘期可以适当提高仓位，但不可满仓，保留弹药应对波动。'
        },
        '秋收': {
            'total_position': '70%->递减',
            'single_max': '20%',
            'strategy': '倒金字塔止盈，越涨越卖。秋收期是兑现利润的阶段，不可贪心。翻倍后先卖一半收回本金。'
        },
        '冬歇': {
            'total_position': '0-10%',
            'single_max': '-',
            'strategy': '空仓或逆回购，保本即胜利。冬歇期绝不为了10%的收益去冒40%的亏损风险。活久比赚猛重要。'
        }
    }
    return advice.get(season, advice['春耕'])


def main():
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
        # 分析主要指数
        indices = [
            ('sh.000001', '上证指数'),
            ('sh.000300', '沪深300'),
            ('sz.399006', '创业板指'),
        ]

        index_results = []
        seasons = []
        data_sources = []

        for code, name in indices:
            print(f"分析 {name}...", file=sys.stderr)
            result = analyze_index(code, name)
            index_results.append(result)
            if 'season' in result:
                seasons.append(result['season'])
            if 'data_source' in result:
                data_sources.append(result['data_source'])

        # 综合季节判断（取多数票）
        if seasons:
            season_count = Counter(seasons)
            overall_season = season_count.most_common(1)[0][0]
        else:
            overall_season = '春耕'

        position_advice = get_position_advice(overall_season)

        # 时间节点提醒
        now = datetime.now()
        month = now.month
        time_warnings = []
        if month == 7:
            time_warnings.append('7月业绩预告期，小心业绩雷')
        elif month == 8:
            time_warnings.append('8月中报密集期，越往后出来的越丑')
        elif month in [1, 4]:
            time_warnings.append(f'{month}月年报/一季报窗口，注意业绩风险')

        # 数据源汇总
        unique_sources = list(set(data_sources))

        output = {
            'judge_date': now.strftime('%Y-%m-%d'),
            'indices': index_results,
            'overall_season': overall_season,
            'position_advice': position_advice,
            'time_warnings': time_warnings,
            'note': '季节判断基于量化指标（均线+位置+量能），冬季判断需综合宏观信号（金融危机、政策转向、流动性收紧等）。Agent需补充定性分析。',
            'data_sources': unique_sources,
            'data_source_fallback': 'akshare > baostock > 东方财富API (Tushare MCP由Agent直接调用优先)'
        }

        print(json.dumps(output, ensure_ascii=False, indent=2))

    finally:
        _stdout = sys.stdout
        sys.stdout = sys.stderr
        bs.logout()
        sys.stdout = _stdout


if __name__ == '__main__':
    main()
