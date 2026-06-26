#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
缠论技术分析脚本
"""

import yfinance as yf
import numpy as np
import sys


def get_klines(symbol, days=90):
    """获取K线数据"""
    try:
        ticker = yf.Ticker(symbol)
        
        # 判断是否为加密货币
        if '-' in symbol and symbol.split('-')[1] == 'USD':
            hist = ticker.history(period=f'{days}d', interval='1d')
        else:
            hist = ticker.history(period=f'{days}d')
        
        if hist is None or len(hist) < 30:
            return None
        
        # 转换为缠论需要的格式
        data = []
        for idx, row in hist.iterrows():
            data.append({
                'date': idx,
                'open': row['Open'],
                'high': row['High'],
                'low': row['Low'],
                'close': row['Close'],
                'volume': row['Volume']
            })
        
        return data
    except Exception as e:
        print(f"获取数据失败: {e}")
        return None


def find_fengxing(klines):
    """识别分型（顶分型/底分型）"""
    if len(klines) < 5:
        return []
    
    fengxing = []
    
    for i in range(2, len(klines) - 2):
        # 顶分型：中K线高点最高
        if (klines[i]['high'] > klines[i-1]['high'] and 
            klines[i]['high'] > klines[i-2]['high'] and
            klines[i]['high'] > klines[i+1]['high'] and 
            klines[i]['high'] > klines[i+2]['high']):
            fengxing.append({
                'type': 'top',
                'index': i,
                'price': klines[i]['high'],
                'date': klines[i]['date']
            })
        
        # 底分型：中K线低点最低
        elif (klines[i]['low'] < klines[i-1]['low'] and 
              klines[i]['low'] < klines[i-2]['low'] and
              klines[i]['low'] < klines[i+1]['low'] and 
              klines[i]['low'] < klines[i+2]['low']):
            fengxing.append({
                'type': 'bottom',
                'index': i,
                'price': klines[i]['low'],
                'date': klines[i]['date']
            })
    
    return fengxing


def merge_fengxing(fengxing):
    """合并分型（取高取低）"""
    if len(fengxing) < 2:
        return fengxing
    
    merged = [fengxing[0]]
    
    for fx in fengxing[1:]:
        last = merged[-1]
        
        # 同类型分型，合并
        if fx['type'] == last['type']:
            if fx['type'] == 'top':
                # 取更高
                if fx['price'] > last['price']:
                    merged[-1] = fx
            else:
                # 取更低
                if fx['price'] < last['price']:
                    merged[-1] = fx
        else:
            merged.append(fx)
    
    return merged


def identify_bi(klines, fengxing):
    """识别笔"""
    if len(fengxing) < 2:
        return []
    
    bis = []
    
    for i in range(len(fengxing) - 1):
        f1 = fengxing[i]
        f2 = fengxing[i + 1]
        
        # 笔：两个分型之间至少5根K线
        if f2['index'] - f1['index'] >= 5:
            direction = 'down' if f1['type'] == 'top' else 'up'
            bis.append({
                'start': f1,
                'end': f2,
                'direction': direction,
                'start_price': f1['price'],
                'end_price': f2['price'],
                'change_pct': (f2['price'] - f1['price']) / f1['price'] * 100
            })
    
    return bis


def find_zhongshu(bis):
    """识别中枢"""
    if len(bis) < 3:
        return []
    
    zhongshus = []
    
    # 中枢：至少三笔重叠区域
    for i in range(len(bis) - 2):
        b1, b2, b3 = bis[i], bis[i+1], bis[i+2]
        
        # 方向相同
        if b1['direction'] == b2['direction'] == b3['direction']:
            # 计算重叠区间
            highs = [b['start_price'] for b in [b1, b2, b3]]
            lows = [b['end_price'] for b in [b1, b2, b3]]
            
            high = min(highs)
            low = max(lows)
            
            if high > low:  # 有重叠
                zhongshus.append({
                    'range': (low, high),
                    'start': b1['start']['date'],
                    'end': b3['end']['date'],
                    'bars': b3['end']['index'] - b1['start']['index']
                })
    
    return zhongshus


def calculate_macd(klines, fast=12, slow=26, signal=9):
    """计算MACD"""
    closes = [k['close'] for k in klines]
    
    # EMA
    ema_fast = np.convolve(closes, np.ones(fast)/fast, mode='valid')
    ema_slow = np.convolve(closes, np.ones(slow)/slow, mode='valid')
    
    if len(ema_fast) < signal:
        return None
    
    # DIF
    dif = ema_fast[-len(ema_slow):] - ema_slow
    
    # DEA (signal)
    dea = np.convolve(dif, np.ones(signal)/signal, mode='valid')
    
    # MACD histogram
    macd = (dif[-len(dea):] - dea) * 2
    
    return {
        'dif': dif[-1] if len(dif) > 0 else 0,
        'dea': dea[-1] if len(dea) > 0 else 0,
        'macd': macd[-1] if len(macd) > 0 else 0,
        'trend': 'up' if macd[-1] > 0 else 'down' if len(macd) > 0 else 'unknown'
    }


def analyze(symbol):
    """缠论分析主函数"""
    print(f"\n{'='*50}")
    print(f"缠论分析: {symbol}")
    print('='*50)
    
    # 获取数据
    klines = get_klines(symbol, 90)
    if klines is None:
        print("❌ 数据获取失败")
        return
    
    print(f"📊 数据: {len(klines)}根K线")
    
    # 最新价
    latest = klines[-1]
    prev = klines[-2] if len(klines) > 1 else latest
    change = (latest['close'] - prev['close']) / prev['close'] * 100
    
    print(f"💰 最新价: {latest['close']:.2f} ({change:+.2f}%)")
    
    # 识别分型
    fx_list = find_fengxing(klines)
    fx_merged = merge_fengxing(fx_list)
    
    print(f"\n🔍 分型识别:")
    print(f"   原始分型: {len(fx_list)}个")
    print(f"   合并后: {len(fx_merged)}个")
    
    if len(fx_merged) >= 2:
        # 识别笔
        bis = identify_bi(klines, fx_merged)
        
        print(f"\n📈 笔分析:")
        print(f"   有效笔: {len(bis)}笔")
        
        if len(bis) > 0:
            # 最后两笔
            last_bi = bis[-1]
            prev_bi = bis[-2] if len(bis) > 1 else None
            
            direction = "上涨" if last_bi['direction'] == 'up' else "下跌"
            print(f"   当前笔: {direction}笔")
            print(f"   幅度: {last_bi['change_pct']:+.2f}%")
            
            if prev_bi:
                print(f"   前一笔: {'上涨' if prev_bi['direction'] == 'up' else '下跌'}笔")
                print(f"   幅度: {prev_bi['change_pct']:+.2f}%")
                
                # 背驰判断
                if abs(last_bi['change_pct']) < abs(prev_bi['change_pct']):
                    print(f"   ⚠️ 背驰迹象: 力度减弱")
            
            # 中枢
            zhongshus = find_zhongshu(bis)
            if zhongshus:
                zs = zhongshus[-1]
                print(f"\n🏛️ 中枢:")
                print(f"   区间: {zs['range'][0]:.2f} - {zs['range'][1]:.2f}")
                print(f"   跨度: {zs['bars']}根K线")
            else:
                print(f"\n🏛️ 中枢: 未形成")
        
        # MACD
        macd = calculate_macd(klines)
        if macd:
            print(f"\n📊 MACD:")
            print(f"   DIF: {macd['dif']:.2f}")
            print(f"   DEA: {macd['dea']:.2f}")
            print(f"   MACD: {macd['macd']:.2f}")
            print(f"   状态: {'多头' if macd['trend'] == 'up' else '空头'}")
        
        # 关键位置
        highs = [k['high'] for k in klines[-30:]]
        lows = [k['low'] for k in klines[-30:]]
        
        print(f"\n🎯 关键位置 (30日):")
        print(f"   最高: {max(highs):.2f}")
        print(f"   最低: {min(lows):.2f}")
        
        # 位置判断
        pos = (latest['close'] - min(lows)) / (max(highs) - min(lows)) * 100
        if pos > 80:
            zone = "高位风险区"
        elif pos < 20:
            zone = "低位机会区"
        else:
            zone = "中性区间"
        
        print(f"   当前位置: {pos:.1f}% ({zone})")
    
    print(f"\n{'='*50}")


def main():
    if len(sys.argv) < 2:
        # 默认分析几个标的
        symbols = ['BTC-USD', '0700.HK', 'AAPL']
        print("Usage: python3 analyze.py <symbol>")
        print(f"默认分析: {symbols}")
    else:
        symbols = sys.argv[1:]
    
    for symbol in symbols:
        try:
            analyze(symbol)
        except Exception as e:
            print(f"❌ {symbol} 分析失败: {e}")


if __name__ == "__main__":
    main()
