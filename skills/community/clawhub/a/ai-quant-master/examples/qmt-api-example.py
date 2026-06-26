"""
QMT API使用示例
基于视频第2集内容整理

注意：以下代码为模板示例，实际使用时需：
1. 替换为真实的QMT API Token
2. 根据具体券商接口调整参数
3. 确保QMT客户端已登录运行
"""

# ============================================
# 1. QMT基础数据获取
# ============================================

# 参考官网示例获取K线数据
# 文档位置：QMT客户端 → 帮助 → 量化接口 → Python API

"""
官方示例模板（复制自QMT官网）：
```python
from QMTData import *

# 初始化
data = QMTData()

# 获取历史数据
history = data.get_history_data(
    symbol='000001.SZ',
    period='1d',
    start_date='2025-01-01',
    end_date='2025-12-31'
)

print(history)
```
"""

# ============================================
# 2. 因子数据加工
# ============================================

import pandas as pd
import numpy as np

def process_qmt_data(raw_data, symbols):
    """
    处理QMT原始数据，生成因子宽表
    
    Parameters:
    -----------
    raw_data : dict
        QMT获取的原始行情数据
    symbols : list
        股票代码列表
    
    Returns:
    --------
    df : pd.DataFrame
        包含因子的宽表数据
    """
    # 数据整理
    df = pd.DataFrame()
    
    for symbol in symbols:
        # 获取单只股票数据
        stock_data = raw_data.get(symbol, {})
        
        # 构建DataFrame
        temp_df = pd.DataFrame({
            'symbol': symbol,
            'trade_date': stock_data.get('trade_date'),
            'open': stock_data.get('open'),
            'high': stock_data.get('high'),
            'low': stock_data.get('low'),
            'close': stock_data.get('close'),
            'volume': stock_data.get('volume'),
        })
        
        df = pd.concat([df, temp_df], ignore_index=True)
    
    return df


# ============================================
# 3. TALib因子计算
# ============================================

import talib

def calculate_factors(df):
    """
    使用TALib计算各类因子
    
    Parameters:
    -----------
    df : pd.DataFrame
        包含OHLCV数据的DataFrame
    
    Returns:
    --------
    df : pd.DataFrame
        添加了因子的DataFrame
    """
    # MFI资金流量指标
    df['mfi'] = talib.MFI(
        df['high'].values,
        df['low'].values,
        df['close'].values,
        df['volume'].values,
        timeperiod=14
    )
    
    # RSI
    df['rsi'] = talib.RSI(df['close'].values, timeperiod=14)
    
    # MACD
    df['macd'], df['macd_signal'], df['macd_hist'] = \
        talib.MACD(df['close'].values)
    
    # 动量
    df['mom'] = talib.MOM(df['close'].values, timeperiod=10)
    
    # OBV能量潮
    df['obv'] = talib.OBV(df['close'].values, df['volume'].values)
    
    #威廉变异量 (简化计算)
    hl_diff = df['high'] - df['low']
    df['wvad'] = ((df['close'] - df['low']) - (df['high'] - df['close'])) / \
                  hl_diff.replace(0, 1) * df['volume']
    
    return df


# ============================================
# 4. 保存到QuestDB
# ============================================

"""
将处理好的因子数据保存到QuestDB

参考examples/questdb-example.py中的写入方法
"""

# ============================================
# 5. 使用示例
# ============================================

if __name__ == '__main__':
    # 示例股票列表
    symbols = ['000001.SZ', '600000.SH', '600519.SH']
    
    # 1. 获取QMT数据（需要真实API）
    # raw_data = get_qmt_data(symbols)
    
    # 2. 处理数据
    # df = process_qmt_data(raw_data, symbols)
    
    # 3. 计算因子
    # df_with_factors = calculate_factors(df)
    
    # 4. 保存到QuestDB
    # save_to_questdb(df_with_factors)
    
    print("QMT API使用示例")
    print("请根据实际券商接口调整代码")
