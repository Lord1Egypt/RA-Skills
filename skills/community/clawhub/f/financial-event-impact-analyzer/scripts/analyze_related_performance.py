#!/usr/bin/env python3
"""
Analyze performance of related assets during historical events.
Calculates returns, volatility, and comparative metrics for each event period.
新增：生成变动幅度表格（从最新到最早排序），支持相关性高亮。
"""

import argparse
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple
import os


def load_indicator_data(indicator_id: str, data_dir: str = None) -> pd.DataFrame:
    """Load historical data for an indicator."""
    if data_dir:
        # 尝试多种文件格式
        for ext in ['.json', '.csv']:
            filepath = f"{data_dir}/{indicator_id}{ext}"
            if os.path.exists(filepath):
                if ext == '.json':
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    return pd.DataFrame(data['data'])
                else:
                    return pd.read_csv(filepath)
    return None


def calculate_period_performance(df: pd.DataFrame, start_date: str, end_date: str) -> Dict:
    """Calculate performance metrics for a specific period."""
    # Filter data for the period
    df['date'] = pd.to_datetime(df['date'])
    period_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if len(period_df) < 2:
        return None
    
    start_price = period_df['close'].iloc[0]
    end_price = period_df['close'].iloc[-1]
    
    # Calculate metrics
    total_return = ((end_price - start_price) / start_price) * 100
    
    # Daily returns
    daily_returns = period_df['close'].pct_change().dropna()
    volatility = daily_returns.std() * 100 if len(daily_returns) > 0 else 0
    max_drawdown = calculate_max_drawdown(period_df['close'])
    sharpe_ratio = calculate_sharpe_ratio(daily_returns)
    
    # Price statistics
    max_price = period_df['close'].max()
    min_price = period_df['close'].min()
    
    return {
        'start_date': start_date,
        'end_date': end_date,
        'start_price': round(float(start_price), 4),
        'end_price': round(float(end_price), 4),
        'total_return_pct': round(total_return, 2),
        'volatility_pct': round(volatility, 2),
        'max_drawdown_pct': round(max_drawdown, 2),
        'sharpe_ratio': round(sharpe_ratio, 2),
        'max_price': round(float(max_price), 4),
        'min_price': round(float(min_price), 4),
        'period_days': len(period_df)
    }


def calculate_max_drawdown(prices: pd.Series) -> float:
    """Calculate maximum drawdown percentage."""
    cumulative = prices / prices.iloc[0]
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    return float(drawdown.min()) * 100


def calculate_sharpe_ratio(daily_returns: pd.Series, risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio (annualized)."""
    if len(daily_returns) == 0 or daily_returns.std() == 0:
        return 0.0
    excess_return = daily_returns.mean() * 252 - risk_free_rate
    return float(excess_return / (daily_returns.std() * np.sqrt(252)))


def analyze_single_event(event: Dict, related_indicators: List[str], 
                          data_cache: Dict, primary_indicator: str) -> Dict:
    """Analyze performance of all related indicators during a single event."""
    results = {
        'event': event,
        'related_performance': {},
        'primary_performance': {}
    }
    
    # 计算主指标表现
    if primary_indicator in data_cache:
        primary_perf = calculate_period_performance(
            data_cache[primary_indicator], 
            event['start_date'], 
            event['end_date']
        )
        if primary_perf:
            results['primary_performance'] = primary_perf
    
    # 计算各相关指标表现
    for indicator_id in related_indicators:
        if indicator_id not in data_cache:
            continue
        
        df = data_cache[indicator_id]
        performance = calculate_period_performance(df, event['start_date'], event['end_date'])
        
        if performance:
            results['related_performance'][indicator_id] = performance
    
    return results


def analyze_all_events(events: List[Dict], related_indicators: List[str], 
                       data_cache: Dict, primary_indicator: str) -> List[Dict]:
    """Analyze performance across all historical events."""
    results = []
    
    # 按时间从最新到最早排序事件
    sorted_events = sorted(events, key=lambda x: x['start_date'], reverse=True)
    
    for event in sorted_events:
        result = analyze_single_event(event, related_indicators, data_cache, primary_indicator)
        results.append(result)
    
    return results


def create_change_table(event_results: List[Dict], primary_indicator: str) -> Dict:
    """
    创建变动幅度表格数据（从最新到最早排序）
    
    Returns:
        包含表格数据和相关性分析的字典
    """
    if not event_results:
        return {'table_data': [], 'high_correlation': []}
    
    table_rows = []
    high_correlation_pairs = []
    
    for i, result in enumerate(event_results):
        event = result['event']
        primary_perf = result.get('primary_performance', {})
        related_perf = result.get('related_performance', {})
        
        row = {
            'event_num': i + 1,
            'time_range': f"{event['start_date']} ~ {event['end_date']}",
            'start_date': event['start_date'],
            'end_date': event['end_date'],
            'primary_change_pct': primary_perf.get('total_return_pct', 'N/A'),
            'related_changes': {}
        }
        
        # 收集各相关指标变动
        for indicator, perf in related_perf.items():
            change_pct = perf.get('total_return_pct', 'N/A')
            row['related_changes'][indicator] = change_pct
            
            # 判断相关性（同向变动为高相关）
            if primary_perf.get('total_return_pct') is not None and change_pct != 'N/A':
                primary_change = primary_perf['total_return_pct']
                related_change = change_pct
                
                # 同向变动判断（都上涨或都下跌）
                is_same_direction = (primary_change > 0 and related_change > 0) or \
                                   (primary_change < 0 and related_change < 0)
                
                if is_same_direction:
                    high_correlation_pairs.append({
                        'event_num': i + 1,
                        'indicator': indicator,
                        'primary_change': primary_change,
                        'related_change': related_change,
                        'same_direction': True
                    })
        
        table_rows.append(row)
    
    return {
        'table_data': table_rows,
        'high_correlation': high_correlation_pairs,
        'total_events': len(event_results)
    }


def calculate_aggregate_stats(event_results: List[Dict]) -> Dict:
    """Calculate aggregate statistics by indicator."""
    if not event_results:
        return {}
    
    # 收集所有指标
    all_indicators = set()
    for result in event_results:
        all_indicators.update(result['related_performance'].keys())
    
    agg_stats = {}
    
    for indicator in all_indicators:
        returns = []
        volatilities = []
        sharpes = []
        positive_count = 0
        negative_count = 0
        
        for result in event_results:
            perf = result['related_performance'].get(indicator)
            if perf:
                returns.append(perf['total_return_pct'])
                volatilities.append(perf['volatility_pct'])
                sharpes.append(perf['sharpe_ratio'])
                if perf['total_return_pct'] > 0:
                    positive_count += 1
                elif perf['total_return_pct'] < 0:
                    negative_count += 1
        
        if returns:
            agg_stats[indicator] = {
                'avg_return_pct': round(np.mean(returns), 2),
                'std_return_pct': round(np.std(returns), 2),
                'min_return_pct': round(np.min(returns), 2),
                'max_return_pct': round(np.max(returns), 2),
                'avg_volatility_pct': round(np.mean(volatilities), 2),
                'avg_sharpe': round(np.mean(sharpes), 2),
                'positive_events': positive_count,
                'negative_events': negative_count,
                'total_events': len(returns),
                'win_rate_pct': round(positive_count / len(returns) * 100, 1)
            }
    
    return agg_stats


def create_summary_table(event_results: List[Dict]) -> pd.DataFrame:
    """Create summary table of all event performances."""
    rows = []
    
    for result in event_results:
        event = result['event']
        event_num = event_results.index(result) + 1
        
        for indicator_id, perf in result['related_performance'].items():
            rows.append({
                'Event': f"Event {event_num}",
                'Start': event['start_date'],
                'End': event['end_date'],
                'Indicator': indicator_id,
                'Return (%)': perf['total_return_pct'],
                'Volatility (%)': perf['volatility_pct'],
                'Max Drawdown (%)': perf['max_drawdown_pct'],
                'Sharpe': perf['sharpe_ratio']
            })
    
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(
        description='分析历史事件期间相关资产表现'
    )
    parser.add_argument('--events', required=True, 
                        help='事件JSON文件 (来自 find_similar_events)')
    parser.add_argument('--related', required=True, 
                        help='相关资产JSON文件 (来自 infer_related_assets)')
    parser.add_argument('--primary-indicator', required=True,
                        help='表征指标ID')
    parser.add_argument('--data-dir', required=True, 
                        help='指标数据文件目录')
    parser.add_argument('--output', '-o', help='输出文件 (JSON)')
    parser.add_argument('--json', action='store_true', help='输出为JSON')
    
    args = parser.parse_args()
    
    # 加载事件数据
    with open(args.events, 'r') as f:
        events_data = json.load(f)
    events = events_data.get('similar_events', [])
    
    # 加载相关资产
    with open(args.related, 'r') as f:
        related_data = json.load(f)
    
    # 收集所有相关指标ID
    all_indicators = set()
    for category in ['benefited', 'harmed', 'neutral_uncertain']:
        for asset in related_data.get(category, []):
            if 'indicator' in asset:
                all_indicators.add(asset['indicator'])
    
    primary_indicator = args.primary_indicator
    all_indicators.add(primary_indicator)
    all_indicators = sorted(list(all_indicators))
    
    print(f"\n分析 {len(events)} 个历史事件，涉及 {len(all_indicators)} 个指标...")
    
    # 加载所有指标数据
    data_cache = {}
    for indicator_id in all_indicators:
        try:
            df = load_indicator_data(indicator_id, args.data_dir)
            if df is not None:
                data_cache[indicator_id] = df
                print(f"  已加载 {indicator_id}: {len(df)} 条记录")
            else:
                print(f"  未找到 {indicator_id} 数据文件")
        except Exception as e:
            print(f"  加载 {indicator_id} 失败: {e}")
    
    # 获取相关指标列表（不含主指标）
    related_indicators = [ind for ind in all_indicators if ind != primary_indicator]
    
    # 分析所有事件
    event_results = analyze_all_events(
        events, related_indicators, data_cache, primary_indicator
    )
    
    # 创建变动幅度表格
    change_table = create_change_table(event_results, primary_indicator)
    
    # 计算汇总统计
    aggregate_stats = calculate_aggregate_stats(event_results)
    
    # 创建详细表格
    summary_df = create_summary_table(event_results)
    
    # 输出
    result = {
        'primary_indicator': primary_indicator,
        'events_count': len(events),
        'related_indicators': related_indicators,
        'event_results': event_results,
        'change_table': change_table,  # 新增：变动幅度表格数据
        'aggregate_stats': aggregate_stats,
        'summary_table': summary_df.to_dict('records') if not summary_df.empty else []
    }
    
    # 打印变动幅度表格
    print(f"\n=== 变动幅度表格（从最新到最早） ===")
    print(f"\n| 事件 | 时间区间 | {primary_indicator} |", end='')
    for ind in related_indicators[:5]:  # 只显示前5个相关指标
        print(f" {ind} |", end='')
    print()
    print('|------|---------|------|', end='')
    for _ in range(min(5, len(related_indicators))):
        print('------|', end='')
    print()
    
    for row in change_table['table_data']:
        primary_change = row['primary_change_pct']
        if primary_change != 'N/A':
            primary_str = f"{'🔴' if primary_change > 0 else '🟢'} {primary_change:.1f}%"
        else:
            primary_str = 'N/A'
        
        print(f"| 事件{row['event_num']} | {row['time_range']} | {primary_str} |", end='')
        
        for ind in related_indicators[:5]:
            change = row['related_changes'].get(ind, 'N/A')
            if change != 'N/A':
                # 判断是否高相关（同向变动）
                is_high_corr = any(
                    p['event_num'] == row['event_num'] and p['indicator'] == ind
                    for p in change_table['high_correlation']
                )
                emoji = '🔴' if change > 0 else '🟢'
                if is_high_corr:
                    print(f" **{emoji}{change:.1f}%** |", end='')
                else:
                    print(f" {emoji}{change:.1f}% |", end='')
            else:
                print(' N/A |', end='')
        print()
    
    # 打印汇总统计
    print(f"\n=== 汇总统计 ===")
    for indicator, stats in aggregate_stats.items():
        win_rate = stats['win_rate_pct']
        avg_return = stats['avg_return_pct']
        print(f"\n{indicator}:")
        print(f"  平均收益: {'🔴' if avg_return > 0 else '🟢'} {avg_return:.2f}%")
        print(f"  收益波动: ±{stats['std_return_pct']:.2f}%")
        print(f"  胜率: {win_rate:.1f}% ({stats['positive_events']}/{stats['total_events']})")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n已保存至: {args.output}")
    
    return result


if __name__ == '__main__':
    main()