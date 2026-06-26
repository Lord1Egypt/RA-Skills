#!/usr/bin/env python3
"""分析美联储缩表周期内各类资产的历史表现"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
import sys

def load_indicator_data(filepath):
    """加载指标数据"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['data'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)
    
    return df

def calculate_performance(df, start_date, end_date):
    """计算指定期间的涨跌幅"""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # 获取期间数据
    period_data = df.loc[start:end]
    
    if len(period_data) < 2:
        return None
    
    start_price = period_data.iloc[0]['close']
    end_price = period_data.iloc[-1]['close']
    
    pct_change = (end_price - start_price) / start_price * 100
    
    # 计算期间最大涨跌幅
    max_price = period_data['close'].max()
    min_price = period_data['close'].min()
    
    max_drawdown = (min_price - max_price) / max_price * 100
    max_gain = (max_price - start_price) / start_price * 100
    
    return {
        'pct_change': pct_change,
        'max_gain': max_gain,
        'max_drawdown': max_drawdown,
        'start_price': start_price,
        'end_price': end_price,
        'data_points': len(period_data)
    }

def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / '.openclaw/workspace/memory/reports/fed_qt_20260328'
    data_dir = output_dir / 'data'
    
    # 加载事件定义
    with open(output_dir / 'events.json', 'r') as f:
        events = json.load(f)
    
    # 指标列表
    indicators = ['sp500', 'nasdaq', 'usd_index', 'xlf', 'tlt', 'xlk', 'xle', 'us_10y_treasury']
    
    results = {
        'events': [],
        'performance': {}
    }
    
    # 分析每个缩表周期
    for event in events['historical_events']:
        event_result = {
            'event_id': event['event_id'],
            'name': event['name'],
            'start_date': event['start_date'],
            'end_date': event['end_date'],
            'description': event['description'],
            'assets': {}
        }
        
        for indicator in indicators:
            filepath = data_dir / f'{indicator}.json'
            if filepath.exists():
                df = load_indicator_data(filepath)
                perf = calculate_performance(df, event['start_date'], event['end_date'])
                if perf:
                    event_result['assets'][indicator] = perf
        
        results['events'].append(event_result)
    
    # 计算汇总统计
    summary = {}
    for indicator in indicators:
        changes = []
        for event in results['events']:
            if indicator in event['assets']:
                changes.append(event['assets'][indicator]['pct_change'])
        
        if changes:
            summary[indicator] = {
                'avg_change': np.mean(changes),
                'min_change': np.min(changes),
                'max_change': np.max(changes),
                'win_rate': sum(1 for c in changes if c > 0) / len(changes) * 100,
                'event_count': len(changes)
            }
    
    results['summary'] = summary
    
    # 保存结果
    with open(output_dir / 'performance.json', 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"分析完成，结果保存到: {output_dir / 'performance.json'}")
    
    # 打印汇总
    print("\n📊 美联储缩表周期资产表现汇总:")
    print("=" * 60)
    
    indicator_names = {
        'sp500': '标普500',
        'nasdaq': '纳斯达克',
        'usd_index': '美元指数',
        'xlf': '金融ETF',
        'tlt': '长债ETF',
        'xlk': '科技ETF',
        'xle': '能源ETF',
        'us_10y_treasury': '10年美债收益率'
    }
    
    for event in results['events']:
        print(f"\n【{event['name']}】 ({event['start_date']} ~ {event['end_date']})")
        for indicator, perf in event['assets'].items():
            name = indicator_names.get(indicator, indicator)
            change = perf['pct_change']
            color = '🔴' if change > 0 else '🟢'
            print(f"  {name}: {color} {change:+.2f}%")
    
    print("\n📈 平均表现统计:")
    for indicator, stats in summary.items():
        name = indicator_names.get(indicator, indicator)
        avg = stats['avg_change']
        win_rate = stats['win_rate']
        color = '🔴' if avg > 0 else '🟢'
        print(f"  {name}: 平均{color} {avg:+.2f}%, 胜率 {win_rate:.0f}%")
    
    return results

if __name__ == '__main__':
    main()