"""
因子计算示例
基于视频第2、3集内容整理

包含：
1. 基础量价因子计算
2. IC/IR/T值计算
3. 多因子组合
"""

import pandas as pd
import numpy as np
import talib


# ============================================
# 1. 因子计算
# ============================================

def calculate_all_factors(df):
    """
    计算所有量价因子
    
    Parameters:
    -----------
    df : pd.DataFrame
        包含OHLCV数据的DataFrame
    
    Returns:
    --------
    df : pd.DataFrame
        添加了所有因子的DataFrame
    """
    # 确保数据格式正确
    high = df['high'].values.astype(float)
    low = df['low'].values.astype(float)
    close = df['close'].values.astype(float)
    volume = df['volume'].values.astype(float)
    
    # ===== 量价类因子 =====
    
    # OBV能量潮
    df['obv'] = talib.OBV(close, volume)
    
    # MFI资金流量指标
    df['mfi'] = talib.MFI(high, low, close, volume, timeperiod=14)
    
    # EMV波动指标（简化版）
    mid = (high + low) / 2
    vol = volume / 1000000  # 转换单位
    emv = (mid - np.roll(mid, 1)) / vol
    emv[0] = 0
    df['emv'] = pd.Series(emv).rolling(14).mean().values
    
    # ===== 趋势类因子 =====
    
    # RSI
    df['rsi'] = talib.RSI(close, timeperiod=14)
    
    # MACD
    df['macd'], df['macd_signal'], df['macd_hist'] = \
        talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    
    # 动量
    df['mom'] = talib.MOM(close, timeperiod=10)
    
    # ===== 反转类因子 =====
    
    # KDJ
    df['k'], df['d'] = talib.STOCH(
        high, low, close,
        fastk_period=9,
        slowk_period=3,
        slowk_matype=0,
        slowd_period=3,
        slowd_matype=0
    )
    df['j'] = 3 * df['k'] - 2 * df['d']
    
    # ===== 情绪类因子 =====
    
    # VPT量价趋势
    vpt = (close - np.roll(close, 1)) / np.roll(close, 1) * volume
    vpt[0] = 0
    df['vpt'] = pd.Series(vpt).cumsum().values
    
    # 威廉变异量
    hl_diff = high - low
    df['wvad'] = ((close - low) - (high - close)) / \
                  np.where(hl_diff == 0, 1, hl_diff) * volume
    
    return df


# ============================================
# 2. IC/IR/T值计算
# ============================================

def calculate_ic(factor_values, future_returns):
    """
    计算IC值（Spearman相关系数）
    
    Parameters:
    -----------
    factor_values : pd.Series
        因子值
    future_returns : pd.Series
        未来收益
    
    Returns:
    --------
    ic : float
        IC值
    """
    return factor_values.rank().corr(future_returns.rank())


def calculate_ic_series(factor_df, factor_name, return_col='ret'):
    """
    计算一段时间的IC序列
    
    Parameters:
    -----------
    factor_df : pd.DataFrame
        包含因子值和收益的DataFrame
    factor_name : str
        因子名称
    return_col : str
        收益列名
    
    Returns:
    --------
    ic_series : pd.Series
        IC时间序列
    """
    ic_list = []
    dates = factor_df['trade_date'].unique()
    
    for date in dates:
        date_data = factor_df[factor_df['trade_date'] == date]
        if len(date_data) > 2:
            ic = calculate_ic(
                date_data[factor_name],
                date_data[return_col]
            )
            ic_list.append({'date': date, 'ic': ic})
    
    return pd.DataFrame(ic_list).set_index('date')['ic']


def calculate_ir(ic_series):
    """
    计算IR（信息比率）
    
    Parameters:
    -----------
    ic_series : pd.Series
        IC时间序列
    
    Returns:
    --------
    ir : float
        IR值
    """
    return ic_series.mean() / ic_series.std()


def calculate_t_value(ic_series):
    """
    计算T值和P值
    
    Parameters:
    -----------
    ic_series : pd.Series
        IC时间序列
    
    Returns:
    --------
    t_stat : float
        T统计量
    p_value : float
        P值
    """
    n = len(ic_series)
    se = ic_series.std() / np.sqrt(n)
    t_stat = ic_series.mean() / se
    # 双尾检验
    from scipy import stats
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 1))
    return t_stat, p_value


# ============================================
# 3. 多因子组合
# ============================================

def combine_factors_ic_weight(factor_ics):
    """
    基于IC值分配因子权重
    
    Parameters:
    -----------
    factor_ics : dict
        各因子IC均值字典
    
    Returns:
    --------
    weights : dict
        各因子权重
    """
    total = sum(abs(ic) for ic in factor_ics.values())
    if total == 0:
        return {k: 0 for k in factor_ics}
    return {k: abs(v) / total for k, v in factor_ics.items()}


def calculate_composite_score(factor_df, weights):
    """
    计算综合因子得分
    
    Parameters:
    -----------
    factor_df : pd.DataFrame
        包含各因子值的DataFrame
    weights : dict
        各因子权重
    
    Returns:
    --------
    composite : pd.Series
        综合得分
    """
    composite = pd.Series(0, index=factor_df.index)
    
    for factor, weight in weights.items():
        if factor in factor_df.columns:
            # 因子值排名（归一化）
            ranked = factor_df[factor].rank(pct=True)
            composite += ranked * weight
    
    return composite


# ============================================
# 4. 示例使用
# ============================================

if __name__ == '__main__':
    # 模拟数据
    dates = pd.date_range('2025-01-01', '2025-12-31', freq='B')
    n = len(dates)
    
    df = pd.DataFrame({
        'trade_date': np.repeat(dates, 10),
        'symbol': np.tile([f'{i:06d}.SZ' for i in range(1, 11)], n),
        'open': np.random.uniform(10, 50, n * 10),
        'high': np.random.uniform(10, 55, n * 10),
        'low': np.random.uniform(5, 45, n * 10),
        'close': np.random.uniform(10, 50, n * 10),
        'volume': np.random.uniform(1000000, 10000000, n * 10),
    })
    
    # 计算因子
    df = calculate_all_factors(df)
    
    # 计算IC
    # ic_series = calculate_ic_series(df, 'mfi')
    # ir = calculate_ir(ic_series)
    # t_stat, p_value = calculate_t_value(ic_series)
    
    print("因子计算完成")
    print(df.head())
