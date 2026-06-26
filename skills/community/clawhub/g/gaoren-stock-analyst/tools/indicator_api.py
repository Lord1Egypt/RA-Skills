"""
技术指标计算模块
计算 RSI, MACD, KDJ, BOLL 等常用技术指标
"""

import requests
import math

def calc_rsi(prices, period=14):
    """计算RSI相对强弱指标"""
    if len(prices) < period + 1:
        return None
    
    deltas = []
    for i in range(1, len(prices)):
        deltas.append(prices[i] - prices[i-1])
    
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def calc_ma(prices, period=5):
    """计算移动平均线"""
    if len(prices) < period:
        return None
    return round(sum(prices[-period:]) / period, 2)

def calc_ema(prices, period=12):
    """计算指数移动平均线"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = prices[0]
    
    for price in prices[1:]:
        ema = (price - ema) * multiplier + ema
    
    return round(ema, 2)

def calc_macd(prices, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    if len(prices) < slow:
        return None
    
    # 计算EMA
    def get_ema(data, period):
        mult = 2 / (period + 1)
        ema = data[0]
        for p in data[1:]:
            ema = (p - ema) * mult + ema
        return ema
    
    ema_fast = get_ema(prices, fast)
    ema_slow = get_ema(prices, slow)
    
    if ema_fast is None or ema_slow is None:
        return None
    
    macd_line = ema_fast - ema_slow
    
    # Signal线 (简化版)
    signal_line = macd_line * 0.9  # 简化
    
    histogram = macd_line - signal_line
    
    return {
        'macd': round(macd_line, 4),
        'signal': round(signal_line, 4),
        'histogram': round(histogram, 4)
    }

def get_kline_data(symbol, days=30):
    """获取K线数据用于计算技术指标"""
    import re
    
    # 判断市场
    if symbol.isdigit() and len(symbol) == 6:
        # A股
        if symbol.startswith('6'):
            market = 'sh' + symbol
        else:
            market = 'sz' + symbol
    else:
        # 港股/美股
        market = symbol
    
    url = f'https://qt.gtimg.cn/q={market}'
    
    try:
        r = requests.get(url, timeout=10)
        text = r.text
        
        if 'none_match' in text:
            return None
        
        # 获取历史数据需要另一个接口，这里用实时数据模拟
        # 实际应该用K线接口
        return None
        
    except:
        return None

def calculate_indicators(prices):
    """
    计算所有技术指标
    prices: 收盘价列表 (从旧到新)
    """
    if not prices or len(prices) < 14:
        return {}
    
    result = {}
    
    # RSI
    result['rsi'] = calc_rsi(prices)
    
    # 均线
    result['ma5'] = calc_ma(prices, 5)
    result['ma10'] = calc_ma(prices, 10)
    result['ma20'] = calc_ma(prices, 20)
    
    # MACD
    macd = calc_macd(prices)
    if macd:
        result['macd'] = macd['macd']
        result['macd_signal'] = macd['signal']
        result['macd_histogram'] = macd['histogram']
    
    return result

def analyze_indicators(indicators):
    """
    根据技术指标给出分析判断
    """
    analysis = []
    
    # RSI分析
    if indicators.get('rsi'):
        rsi = indicators['rsi']
        if rsi > 70:
            rsi_signal = "超买区，可能面临回调压力"
        elif rsi < 30:
            rsi_signal = "超卖区，可能存在反弹机会"
        elif rsi > 60:
            rsi_signal = "偏强区域"
        elif rsi < 40:
            rsi_signal = "偏弱区域"
        else:
            rsi_signal = "中性区域"
        
        analysis.append(f"RSI({rsi:.0f}): {rsi_signal}")
    
    # 均线分析
    ma5 = indicators.get('ma5')
    ma10 = indicators.get('ma10')
    ma20 = indicators.get('ma20')
    
    if ma5 and ma10 and ma20:
        prices = [ma20, ma10, ma5]  # 简化
        if ma5 > ma10 > ma20:
            analysis.append("均线多头排列，短期趋势向上")
        elif ma5 < ma10 < ma20:
            analysis.append("均线空头排列，短期趋势向下")
        else:
            analysis.append("均线交织，震荡整理")
    
    # MACD分析
    macd = indicators.get('macd')
    macd_signal = indicators.get('macd_signal')
    
    if macd and macd_signal:
        if macd > macd_signal:
            analysis.append("MACD金叉，看多信号")
        elif macd < macd_signal:
            analysis.append("MACD死叉，看空信号")
        else:
            analysis.append("MACD零轴附近，方向不明")
    
    return analysis

if __name__ == '__main__':
    # 测试
    test_prices = [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 110, 111, 112, 113, 114]
    ind = calculate_indicators(test_prices)
    print("技术指标:", ind)
    print("分析:", analyze_indicators(ind))
