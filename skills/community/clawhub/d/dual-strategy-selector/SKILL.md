# -*- coding: utf-8 -*-
"""
双策略选股器 - 通用版
策略1: 仙人指路B + 持股20天
策略2: 老鸭头B + 持股5天

使用方法:
python dual_strategy_selector.py --data your_data.csv
python dual_strategy_selector.py --data your_data.csv --date 2026-04-30
python dual_strategy_selector.py --data your_data.csv --watch

数据接口要求:
CSV文件必须包含以下列:
- symbol: 股票代码
- name: 股票名称
- date: 日期 (YYYY-MM-DD)
- open: 开盘价
- high: 最高价
- low: 最低价
- close: 收盘价
- volume: 成交量
- turnover: 换手率 (%)
- ma5: 5日均线
- ma10: 10日均线
- ma20: 20日均线
- ma60: 60日均线
- volume_ratio: 量比
- pct_change: 涨跌幅 (%)
- is_up_limit: 是否涨停 (0/1)
"""

import pandas as pd
import numpy as np
from datetime import datetime
import argparse
import os

# ============================================================
# 策略配置
# ============================================================
STRATEGY_CONFIG = {
    '仙人指路B': {
        'name': '仙人指路B',
        'version': '1.0',
        'hold_days': 20,
        'expected_win_rate': 54.2,
        'expected_avg_profit': 3.53,
        'params': {
            'upper_shadow_pct': 2.0,  # 上影线>2%
            'body_pct_max': 2.0,      # 实体<2%
            'turnover_min': 3.0,      # 换手>3%
            'turnover_max': 7.0,      # 换手<7%
            'volume_ratio_min': 1.0,  # 量比>1
        }
    },
    '老鸭头B': {
        'name': '老鸭头B',
        'version': '1.0',
        'hold_days': 5,
        'expected_win_rate': 72.0,
        'expected_avg_profit': 0.77,
        'params': {
            'near_pct': 0.02,         # 回调至20日线±2%
            'require_10x60': True,     # 10日上穿60日
            'require_ma10_up': True,   # MA10向上
            'require_price_above_20': False,
        }
    }
}

# ============================================================
# 数据加载函数
# ============================================================

def load_data(data_path, target_date=None):
    """
    加载用户数据
    
    参数:
        data_path: CSV文件路径
        target_date: 目标日期 (可选)
    
    返回:
        DataFrame
    """
    print(f"[OK] 加载数据: {data_path}")
    
    if not os.path.exists(data_path):
        print(f"[ERROR] 文件不存在: {data_path}")
        return None
    
    df = pd.read_csv(data_path)
    
    # 检查必要列
    required_cols = ['symbol', 'name', 'date', 'open', 'high', 'low', 'close', 
                     'volume', 'turnover', 'ma5', 'ma10', 'ma20', 'ma60', 
                     'volume_ratio', 'pct_change', 'is_up_limit']
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"[ERROR] 缺少必要列: {missing_cols}")
        print("[INFO] 请确保CSV包含以下列:")
        for col in required_cols:
            print(f"  - {col}")
        return None
    
    # 转换日期
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"[OK] 数据: {len(df)}行, {df['symbol'].nunique()}只股票")
    print(f"[OK] 日期范围: {df['date'].min()} ~ {df['date'].max()}")
    
    return df

# ============================================================
# 信号检测函数
# ============================================================

def detect_signals(df):
    """检测双策略信号"""
    df = df.sort_values(['symbol', 'date'])
    
    # 预计算shift
    df['ma5_prev'] = df.groupby('symbol')['ma5'].shift(1)
    df['ma10_prev'] = df.groupby('symbol')['ma10'].shift(1)
    df['ma20_prev'] = df.groupby('symbol')['ma20'].shift(1)
    df['ma60_prev'] = df.groupby('symbol')['ma60'].shift(1)
    df['close_prev'] = df.groupby('symbol')['close'].shift(1)
    
    # === 仙人指路B ===
    df['body'] = abs(df['close'] - df['open'])
    df['body_pct'] = df['body'] / df['close_prev'] * 100
    df['upper_shadow'] = df['high'] - df[['open', 'close']].max(axis=1)
    df['upper_shadow_pct'] = df['upper_shadow'] / df['close_prev'] * 100
    
    params_xr = STRATEGY_CONFIG['仙人指路B']['params']
    df['signal_xrB'] = (
        (df['upper_shadow_pct'] > params_xr['upper_shadow_pct']) &
        (df['body_pct'] < params_xr['body_pct_max']) &
        (df['turnover'] >= params_xr['turnover_min']) &
        (df['turnover'] <= params_xr['turnover_max']) &
        (df['volume_ratio'] > params_xr['volume_ratio_min'])
    ).astype(int)
    
    # === 老鸭头B ===
    df['s_5x10'] = ((df['ma5_prev'] < df['ma10_prev']) & (df['ma5'] >= df['ma10'])).astype(int)
    df['ma20_slope'] = df.groupby('symbol')['ma20'].transform(lambda x: x.diff().rolling(5).mean())
    df['s_20_up'] = (df['ma20_slope'] > 0).astype(int)
    df['price_near_20'] = (abs(df['close'] - df['ma20']) / df['ma20'] < STRATEGY_CONFIG['老鸭头B']['params']['near_pct']).astype(int)
    df['signal_lyB_base'] = (df['s_5x10'] & df['s_20_up'] & df['price_near_20']).astype(int)
    
    # 加成条件
    df['s_10x60'] = ((df['ma10_prev'] < df['ma60_prev']) & (df['ma10'] >= df['ma60'])).astype(int)
    df['s_ma10_up'] = (df['ma10'] > df['ma10_prev']).astype(int)
    df['s_price_above_20'] = (df['close'] > df['ma20']).astype(int)
    
    # 老鸭头B完整信号
    ly_params = STRATEGY_CONFIG['老鸭头B']['params']
    conditions = [df['signal_lyB_base'] == 1]
    if ly_params['require_10x60']:
        conditions.append(df['s_10x60'] == 1)
    if ly_params['require_ma10_up']:
        conditions.append(df['s_ma10_up'] == 1)
    if ly_params['require_price_above_20']:
        conditions.append(df['s_price_above_20'] == 1)
    
    df['signal_lyB'] = np.where(pd.concat(conditions, axis=1).all(axis=1), 1, 0)
    
    # 清理临时列
    drop_cols = ['ma5_prev', 'ma10_prev', 'ma20_prev', 'ma60_prev', 'close_prev',
                 'body', 'body_pct', 'upper_shadow', 'upper_shadow_pct',
                 's_5x10', 'ma20_slope', 's_20_up', 'price_near_20']
    df = df.drop(columns=drop_cols)
    
    return df

# ============================================================
# 选股函数
# ============================================================

def select_stocks(df, target_date=None, top_n=20):
    """选股主函数"""
    
    if target_date:
        target_dt = pd.to_datetime(target_date)
    else:
        target_dt = df['date'].max()
    
    print(f"[OK] 目标日期: {target_dt.strftime('%Y-%m-%d')}")
    
    # 检测信号
    df = detect_signals(df)
    
    # 只取目标日期
    today_df = df[df['date'] == target_dt].copy()
    
    if len(today_df) == 0:
        print(f"[WARN] 目标日期无数据")
        return None
    
    # === 策略1: 仙人指路B ===
    xr_signals = today_df[today_df['signal_xrB'] == 1].copy()
    
    # === 策略2: 老鸭头B ===
    ly_signals = today_df[today_df['signal_lyB'] == 1].copy()
    
    # 输出结果
    print("\n" + "="*80)
    print(f"双策略选股结果 - {target_dt.strftime('%Y-%m-%d')}")
    print("="*80)
    
    # 策略1输出
    print(f"\n【策略1: 仙人指路B】")
    print(f"预期胜率: {STRATEGY_CONFIG['仙人指路B']['expected_win_rate']}%")
    print(f"预期均益: +{STRATEGY_CONFIG['仙人指路B']['expected_avg_profit']}%")
    print(f"持股周期: {STRATEGY_CONFIG['仙人指路B']['hold_days']}天")
    print(f"信号股票: {len(xr_signals)}只")
    
    if len(xr_signals) > 0:
        xr_signals = xr_signals.sort_values('volume_ratio', ascending=False)
        top_xr = xr_signals.head(top_n)
        
        print(f"\n--- TOP {len(top_xr)} ---")
        for i, (_, row) in enumerate(top_xr.iterrows(), 1):
            print(f"\n{i:2d}. {row['symbol']} {row['name']}")
            print(f"    价格: {row['close']:.2f} | 涨幅: {row['pct_change']:+.2f}%")
            print(f"    换手: {row['turnover']:.2f}% | 量比: {row['volume_ratio']:.2f}")
            print(f"    上影线: {(row['high'] - max(row['open'], row['close'])) / row['close'] * 100:.2f}%")
            print(f"    实体: {abs(row['close'] - row['open']) / row['open'] * 100:.2f}%")
    
    # 策略2输出
    print(f"\n【策略2: 老鸭头B】")
    print(f"预期胜率: {STRATEGY_CONFIG['老鸭头B']['expected_win_rate']}%")
    print(f"预期均益: +{STRATEGY_CONFIG['老鸭头B']['expected_avg_profit']}%")
    print(f"持股周期: {STRATEGY_CONFIG['老鸭头B']['hold_days']}天")
    print(f"信号股票: {len(ly_signals)}只")
    
    if len(ly_signals) > 0:
        ly_signals['score'] = (
            ly_signals['s_10x60'] * 30 +
            ly_signals['s_ma10_up'] * 20 +
            ly_signals['turnover'] * 5
        )
        ly_signals = ly_signals.sort_values('score', ascending=False)
        top_ly = ly_signals.head(top_n)
        
        print(f"\n--- TOP {len(top_ly)} ---")
        for i, (_, row) in enumerate(top_ly.iterrows(), 1):
            print(f"\n{i:2d}. {row['symbol']} {row['name']}")
            print(f"    价格: {row['close']:.2f} | 涨幅: {row['pct_change']:+.2f}%")
            print(f"    换手: {row['turnover']:.2f}% | 量比: {row['volume_ratio']:.2f}")
            print(f"    MA5: {row['ma5']:.2f} | MA10: {row['ma10']:.2f} | MA20: {row['ma20']:.2f} | MA60: {row['ma60']:.2f}")
            print(f"    信号: 10日上穿60日{'Y' if row['s_10x60'] else 'N'} | MA10向上{'Y' if row['s_ma10_up'] else 'N'}")
            print(f"    评分: {row['score']:.0f}")
    
    # 保存结果
    if len(xr_signals) > 0 or len(ly_signals) > 0:
        output_file = f"selection_{target_dt.strftime('%Y%m%d')}.csv"
        
        # 合并保存
        xr_save = xr_signals[['symbol', 'name', 'date', 'close', 'pct_change', 'turnover', 'volume_ratio']].copy()
        xr_save['strategy'] = '仙人指路B'
        
        ly_save = ly_signals[['symbol', 'name', 'date', 'close', 'pct_change', 'turnover', 'volume_ratio']].copy()
        ly_save['strategy'] = '老鸭头B'
        
        combined = pd.concat([xr_save, ly_save], ignore_index=True)
        combined.to_csv(output_file, index=False)
        print(f"\n[OK] 结果保存: {output_file}")
    
    return xr_signals, ly_signals

# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(description='双策略选股器 - 通用版')
    parser.add_argument('--data', type=str, required=True, help='数据文件路径 (CSV)')
    parser.add_argument('--date', type=str, help='指定日期 (YYYY-MM-DD)')
    parser.add_argument('--top', type=int, default=20, help='显示前N只 (默认20)')
    
    args = parser.parse_args()
    
    # 加载数据
    df = load_data(args.data, args.date)
    if df is None:
        return
    
    # 选股
    select_stocks(df, args.date, args.top)

if __name__ == '__main__':
    main()
