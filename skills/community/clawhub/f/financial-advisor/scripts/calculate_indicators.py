#!/usr/bin/env python3
"""
技术指标计算脚本
- 计算常用技术指标（MA、MACD、RSI、BOLL、KDJ等）
- 输入：历史K线数据（CSV/JSON）
- 输出：技术指标数据（CSV/JSON）
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"错误：缺少必要的Python库: {e}")
    print("请运行: pip install pandas numpy")
    sys.exit(1)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def calculate_ma(df, periods=[5, 10, 20, 30, 60, 120, 250]):
    """计算移动平均线"""
    for period in periods:
        if len(df) >= period:
            df[f'MA{period}'] = df['Close'].rolling(window=period).mean()
    return df


def calculate_bias(df, periods=[5, 10, 20]):
    """计算乖离率（防追高核心指标）"""
    for period in periods:
        if len(df) >= period:
            ma_col = f'MA{period}'
            if ma_col in df.columns:
                df[f'BIAS{period}'] = ((df['Close'] - df[ma_col]) / df[ma_col]) * 100
    return df


def calculate_macd(df, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    df['MACD_DIF'] = ema_fast - ema_slow
    df['MACD_DEA'] = df['MACD_DIF'].ewm(span=signal, adjust=False).mean()
    df['MACD_HIST'] = (df['MACD_DIF'] - df['MACD_DEA']) * 2
    return df


def calculate_rsi(df, period=14):
    """计算RSI指标"""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def calculate_bollinger(df, period=20, std_dev=2):
    """计算布林带"""
    df['BOLL_MID'] = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    df['BOLL_UPPER'] = df['BOLL_MID'] + (std_dev * std)
    df['BOLL_LOWER'] = df['BOLL_MID'] - (std_dev * std)
    df['BOLL_WIDTH'] = ((df['BOLL_UPPER'] - df['BOLL_LOWER']) / df['BOLL_MID']) * 100
    return df


def calculate_kdj(df, n=9, m1=3, m2=3):
    """计算KDJ指标"""
    low_list = df['Low'].rolling(window=n, min_periods=1).min()
    high_list = df['High'].rolling(window=n, min_periods=1).max()
    
    rsv = (df['Close'] - low_list) / (high_list - low_list) * 100
    df['KDJ_K'] = rsv.ewm(com=m1-1, adjust=False).mean()
    df['KDJ_D'] = df['KDJ_K'].ewm(com=m2-1, adjust=False).mean()
    df['KDJ_J'] = 3 * df['KDJ_K'] - 2 * df['KDJ_D']
    return df


def calculate_atr(df, period=14):
    """计算ATR（平均真实波幅）"""
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df['ATR'] = true_range.rolling(window=period).mean()
    return df


def calculate_obv(df):
    """计算OBV（能量潮）"""
    obv = [0]
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    df['OBV'] = obv
    return df


def calculate_all_indicators(df):
    """计算所有技术指标"""
    logger.info("开始计算技术指标...")
    
    df = calculate_ma(df)
    df = calculate_bias(df)  # 新增：乖离率计算
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_bollinger(df)
    df = calculate_kdj(df)
    df = calculate_atr(df)
    df = calculate_obv(df)
    
    # 添加元数据
    df['计算时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['数据来源'] = '技术指标计算'
    
    logger.info(f"技术指标计算完成，共 {len(df)} 条数据")
    return df


def main():
    parser = argparse.ArgumentParser(description='技术指标计算工具')
    parser.add_argument('--input', required=True, help='输入文件路径（CSV或JSON）')
    parser.add_argument('--output', required=True, help='输出文件路径（CSV或JSON）')
    parser.add_argument('--indicator', default='all',
                       help='指标类型：all, ma, bias, macd, rsi, boll, kdj, atr, obv')
    args = parser.parse_args()
    
    # 读取数据
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"输入文件不存在: {input_path}")
        sys.exit(1)
    
    if input_path.suffix == '.csv':
        df = pd.read_csv(input_path)
    elif input_path.suffix == '.json':
        df = pd.read_json(input_path)
    else:
        logger.error("不支持的文件格式，仅支持 CSV 和 JSON")
        sys.exit(1)
    
    # 列名映射（兼容中文和英文）
    column_mapping = {
        '日期': 'Date', '开盘': 'Open', '收盘': 'Close', '最高': 'High', 
        '最低': 'Low', '成交量': 'Volume'
    }
    df.rename(columns=column_mapping, inplace=True)
    
    # 确保必要的列存在
    required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.error(f"缺少必要的列: {missing_cols}")
        logger.error(f"当前列: {list(df.columns)}")
        sys.exit(1)
    
    # 计算指标
    if args.indicator == 'all':
        df = calculate_all_indicators(df)
    elif args.indicator == 'ma':
        df = calculate_ma(df)
        df = calculate_bias(df)  # MA之后自动计算乖离率
    elif args.indicator == 'bias':
        df = calculate_ma(df)  # 乖离率依赖MA
        df = calculate_bias(df)
    elif args.indicator == 'macd':
        df = calculate_macd(df)
    elif args.indicator == 'rsi':
        df = calculate_rsi(df)
    elif args.indicator == 'boll':
        df = calculate_bollinger(df)
    elif args.indicator == 'kdj':
        df = calculate_kdj(df)
    elif args.indicator == 'atr':
        df = calculate_atr(df)
    elif args.indicator == 'obv':
        df = calculate_obv(df)
    
    # 保存结果
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if output_path.suffix == '.csv':
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        logger.info(f"CSV文件已保存: {output_path}")
    elif output_path.suffix == '.json':
        df.to_json(output_path, orient='records', force_ascii=False, indent=2)
        logger.info(f"JSON文件已保存: {output_path}")
    
    # 输出统计信息
    logger.info(f"\n技术指标统计:")
    logger.info(f"- 数据行数: {len(df)}")
    logger.info(f"- 指标列数: {len(df.columns) - len(required_cols)}")
    logger.info(f"- 最新收盘价: {df['Close'].iloc[-1]:.2f}")
    if 'BIAS5' in df.columns:
        bias5 = df['BIAS5'].iloc[-1]
        logger.info(f"- 乖离率(MA5): {bias5:.2f}% {'⚠️追高警告' if bias5 > 5 else '✓正常'}")
    if 'RSI' in df.columns:
        logger.info(f"- 最新RSI: {df['RSI'].iloc[-1]:.2f}")
    if 'MACD_DIF' in df.columns:
        logger.info(f"- 最新MACD DIF: {df['MACD_DIF'].iloc[-1]:.4f}")


if __name__ == '__main__':
    main()
