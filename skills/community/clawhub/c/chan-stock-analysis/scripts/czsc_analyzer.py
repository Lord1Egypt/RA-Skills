# -*- coding: utf-8 -*-
"""
基于czsc模块的缠论核心分析函数 v2
使用czsc.CZSC进行分型、笔、中枢识别
"""
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# 确保czsc路径在sys.path中（从 config.py 读取，支持环境变量 CZSC_PATH 覆盖）
import importlib.util as _ilu
_cfg_spec = _ilu.spec_from_file_location(
    "chan_config",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py"),
)
_cfg = _ilu.module_from_spec(_cfg_spec)
_cfg_spec.loader.exec_module(_cfg)
czsc_path: str = _cfg.CZSC_PATH
if czsc_path not in sys.path:
    sys.path.insert(0, czsc_path)

# 强制使用Python实现
os.environ['CZSC_USE_PYTHON'] = '1'

from czsc import CZSC, Freq, RawBar, Direction
from czsc.py.enum import Mark


def klines_to_rawbars(klines, symbol='XAUUSD', freq_str='D'):
    """将K线数据转换为czsc的RawBar列表"""
    # 映射freq字符串到Freq枚举
    freq_map = {
        'D': Freq.D, 'daily': Freq.D,
        '30': Freq.F30, '30min': Freq.F30,
        '5': Freq.F5, '5min': Freq.F5,
        '1': Freq.F1, '1min': Freq.F1,
        '60': Freq.F60, '60min': Freq.F60,
    }
    freq = freq_map.get(freq_str, Freq.D)
    
    bars = []
    for i, k in enumerate(klines):
        dt = k['datetime'] if isinstance(k['datetime'], (datetime, pd.Timestamp)) else pd.to_datetime(k['datetime'])
        bar = RawBar(
            symbol=symbol,
            id=i,
            dt=dt,
            freq=freq,
            open=float(k['open']),
            close=float(k['close']),
            high=float(k['high']),
            low=float(k['low']),
            vol=float(k.get('volume', 0)),
            amount=float(k.get('amount', 0))
        )
        bars.append(bar)
    return bars


def analyze_level(klines, level_name='日线', symbol='XAUUSD', max_bi_num=50):
    """
    使用czsc模块进行单级别缠论分析
    
    Args:
        klines: list of dict, K线数据
        level_name: str, 级别名称
        symbol: str, 标的代码
        max_bi_num: int, 最大笔数
    
    Returns:
        dict: 分析结果
    """
    if len(klines) < 10:
        return None
    
    # 映射级别名称到freq字符串
    freq_map = {
        '日线': 'D', 'daily': 'D',
        '30分钟': '30', '30min': '30',
        '5分钟': '5', '5min': '5',
        '1分钟': '1', '1min': '1',
    }
    freq_str = freq_map.get(level_name, 'D')
    
    # 转换为RawBar
    bars = klines_to_rawbars(klines, symbol, freq_str)
    
    # 创建CZSC对象
    czsc = CZSC(bars, max_bi_num=max_bi_num)
    
    # 提取分析结果
    result = {
        'name': level_name,
        'symbol': symbol,
        'count': len(bars),
        'current': bars[-1].close if bars else 0,
        'current_dt': bars[-1].dt if bars else None,
        'fx_list': [],      # 分型列表
        'bi_list': [],      # 笔列表
        'signals': [],      # 信号列表
        'trend': 'unknown', # 趋势
        'macd': None,       # MACD
        'beichi': None,     # 背驰
        'zs': None,         # 中枢
    }
    
    # 1. 提取分型 (fx_list)
    for fx in czsc.fx_list:
        power_map = {'强': 'strong', '中': 'medium', '弱': 'weak'}
        result['fx_list'].append({
            'dt': fx.dt,
            'mark': 'top' if fx.mark == Mark.G else 'bottom',
            'high': fx.high,
            'low': fx.low,
            'power': fx.power_str,
            'volume': fx.power_volume,
        })
    
    # 2. 提取笔 (bi_list)
    for bi in czsc.bi_list:
        result['bi_list'].append({
            'direction': 'up' if bi.direction == Direction.Up else 'down',
            'fx_a_dt': bi.fx_a.dt if bi.fx_a else None,
            'fx_b_dt': bi.fx_b.dt if bi.fx_b else None,
            'high': bi.high,
            'low': bi.low,
            'length': bi.length,
            'slope': bi.slope,
            'change': bi.change,
            'power': str(bi.power) if bi.power else None,
            'power_price': bi.power_price if hasattr(bi, 'power_price') else None,
        })
    
    # 3. 提取中枢 (使用ubi_fxs)
    # ubi包含当前笔的详细信息
    if hasattr(czsc, 'ubi') and czsc.ubi:
        ubi = czsc.ubi
        if 'fxs' in ubi and len(ubi['fxs']) >= 3:
            fxs = ubi['fxs']
            # 找到构成中枢的三笔
            # 中枢 = max(低点) 到 min(高点)
            lows = []
            highs = []
            for fx in fxs:
                if fx.mark == Mark.D:
                    lows.append(fx.low)
                else:
                    highs.append(fx.high)
            
            if lows and highs:
                zd = max(lows)  # 中枢低点
                zg = min(highs)  # 中枢高点
                if zg > zd:
                    result['zs'] = {
                        'zd': zd,
                        'zg': zg,
                        'begin_dt': fxs[0].dt,
                        'end_dt': fxs[-1].dt,
                    }
    
    # 4. 提取信号
    for sig in list(czsc.signals):
        result['signals'].append(str(sig))
    
    # 5. 判断趋势
    result['trend'] = judge_trend(czsc, result['zs'], result['current'])
    
    # 6. 计算MACD
    result['macd'] = calculate_macd(klines)
    
    # 7. 检测背驰
    result['beichi'] = detect_beichi(czsc)
    
    return result


def judge_trend(czsc, zs, current_price):
    """判断趋势"""
    if len(czsc.bi_list) < 3:
        return 'unknown'
    
    last_bi = czsc.bi_list[-1]
    
    # 有中枢的情况
    if zs:
        if current_price > zs['zg']:
            return 'up'  # 价格在中枢上方
        elif current_price < zs['zd']:
            return 'down'  # 价格在中枢下方
        else:
            return 'consolidation'  # 价格在中枢内
    
    # 没有中枢，根据笔的方向判断
    return 'up' if last_bi.direction == Direction.Up else 'down'


def calculate_macd(klines, fast=12, slow=26, signal=9):
    """计算MACD指标"""
    if len(klines) < slow + signal:
        return None
    
    closes = [k['close'] for k in klines]
    
    def ema(data, period):
        result = [sum(data[:period]) / period]
        multiplier = 2 / (period + 1)
        for i in range(period, len(data)):
            result.append((data[i] - result[-1]) * multiplier + result[-1])
        return result
    
    ema_fast = ema(closes, fast)
    ema_slow = ema(closes, slow)
    
    min_len = min(len(ema_fast), len(ema_slow))
    dif = [ema_fast[i] - ema_slow[i] for i in range(min_len)]
    
    dea = ema(dif, signal)
    
    min_len2 = min(len(dif), len(dea))
    macd_hist = [(dif[i] - dea[i]) * 2 for i in range(min_len2)]
    
    return {
        'dif': dif[-1] if dif else 0,
        'dea': dea[-1] if dea else 0,
        'macd': macd_hist[-1] if macd_hist else 0,
        'trend': 'up' if (macd_hist[-1] > 0 if macd_hist else False) else 'down'
    }


def detect_beichi(czsc):
    """检测背驰 - 比较同向相邻两笔的力度"""
    if len(czsc.bi_list) < 4:
        return None
    
    # 获取最后两笔
    last_bi = czsc.bi_list[-1]
    
    # 找前一笔同向笔
    prev_bi = None
    for bi in reversed(czsc.bi_list[:-1]):
        if bi.direction == last_bi.direction:
            prev_bi = bi
            break
    
    if prev_bi is None:
        return None
    
    # 比较力度 (使用change作为力度指标)
    enter_change = abs(prev_bi.change) if prev_bi.change else 0
    leave_change = abs(last_bi.change) if last_bi.change else 0
    
    if enter_change == 0:
        return None
    
    # 离开段力度 < 进入段力度 → 背驰
    if leave_change < enter_change:
        ratio = leave_change / enter_change
        bc_type = 'bottom' if last_bi.direction == Direction.Up else 'top'
        strength = 'strong' if ratio < 0.5 else 'weak'
        
        return {
            'type': bc_type,
            'strength': strength,
            'enter_change': enter_change,
            'leave_change': leave_change,
            'ratio': ratio,
            'enter_dt': prev_bi.fx_a.dt if prev_bi.fx_a else None,
            'leave_dt': last_bi.fx_a.dt if last_bi.fx_a else None,
        }
    
    return None


# ============ 测试代码 ============
if __name__ == '__main__':
    # 读取测试数据
    df = pd.read_csv(r'D:/QClawData/workspace/XAUUSD_daily.csv')
    df = df.rename(columns={'date': 'datetime'})
    
    # 转换为klines格式
    klines = df.to_dict('records')
    
    print(f"测试数据: {len(klines)}条")
    print(f"时间范围: {klines[0]['datetime']} ~ {klines[-1]['datetime']}")
    print(f"最新价: {klines[-1]['close']}")
    
    # 进行日线分析
    print("\n" + "="*60)
    print("日线级别分析")
    print("="*60)
    
    result = analyze_level(klines[-200:], '日线', 'XAUUSD')
    
    if result:
        print(f"\n标的: {result['symbol']}")
        print(f"数据量: {result['count']}")
        print(f"当前价: {result['current']:.2f}")
        print(f"趋势: {result['trend']}")
        print(f"分型数: {len(result['fx_list'])}")
        print(f"笔数: {len(result['bi_list'])}")
        
        if result['zs']:
            print(f"\n中枢:")
            zs = result['zs']
            print(f"  区间: {zs['zd']:.2f} - {zs['zg']:.2f}")
            print(f"  跨度: {zs['zg']-zs['zd']:.2f}")
        
        if result['beichi']:
            bc = result['beichi']
            print(f"\n背驰:")
            print(f"  类型: {bc['type']} {'底背驰' if bc['type']=='bottom' else '顶背驰'}")
            print(f"  强度: {bc['strength']} {'强' if bc['strength']=='strong' else '弱'}")
            print(f"  比率: {bc['ratio']:.2%}")
        
        if result['macd']:
            m = result['macd']
            print(f"\nMACD:")
            print(f"  DIF: {m['dif']:.2f}")
            print(f"  DEA: {m['dea']:.2f}")
            print(f"  柱: {m['macd']:.2f}")
            print(f"  状态: {'多头' if m['trend']=='up' else '空头'}")
        
        # 最近5笔
        if result['bi_list']:
            print(f"\n最近5笔:")
            for bi in result['bi_list'][-5:]:
                d = '↑' if bi['direction']=='up' else '↓'
                print(f"  {d} {bi['fx_a_dt']} → {bi['fx_b_dt']} (变化:{bi['change']:.1f}%)")