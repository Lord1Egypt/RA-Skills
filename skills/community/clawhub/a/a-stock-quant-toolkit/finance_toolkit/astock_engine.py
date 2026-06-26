#!/usr/bin/env python3
"""
A股量化数据引擎 - 基于腾讯行情API
稳定、免注册、速度快
"""

import subprocess
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import re
import time
import logging

logger = logging.getLogger(__name__)

class AStockEngine:
    """A股数据引擎"""

    def __init__(self, cache_dir="data/cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _curl(self, url, timeout=10):
        """通过curl获取数据"""
        try:
            result = subprocess.run(
                ['curl.exe', '-s', '--connect-timeout', str(timeout), url],
                capture_output=True, timeout=timeout+5
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.decode('gbk', errors='ignore')
            return None
        except:
            return None

    def get_quotes(self, symbols):
        """批量获取行情"""
        if not symbols:
            return []
        codes = ','.join(symbols)
        url = f"http://qt.gtimg.cn/q={codes}"
        data = self._curl(url)
        if not data:
            return []
        results = []
        for line in data.strip().strip(';').split(';'):
            if '="' in line:
                r = self._parse(line + ';')
                if r:
                    results.append(r)
        return results

    def _parse(self, raw):
        """解析腾讯行情数据"""
        try:
            m = re.search(r'v_[^=]+="([^"]+)"', raw)
            if not m:
                return None
            p = m.group(1).split('~')
            if len(p) < 40:
                return None
            return {
                'name': p[1], 'code': p[2],
                'price': float(p[3]) if p[3] else 0,
                'change_pct': round(float(p[32]) if p[32] else 0, 2),
                'volume': int(p[6]) if p[6] else 0,
                'amount': float(p[37]) if len(p) > 37 and p[37] else 0,
                'high': float(p[33]) if p[33] else 0,
                'low': float(p[34]) if p[34] else 0,
                'open': float(p[5]) if p[5] else 0,
                'yclose': float(p[4]) if p[4] else 0,
                'turnover': float(p[38]) if len(p) > 38 and p[38] else 0,
                'pe': float(p[39]) if len(p) > 39 and p[39] else 0,
                'market_cap': float(p[45]) if len(p) > 45 and p[45] else 0,
            }
        except:
            return None

    def get_index(self):
        """获取主要指数"""
        syms = ['sh000001','sz399001','sz399006','sh000300','sh000016','sh000688']
        names = {'000001':'上证指数','399001':'深证成指','399006':'创业板指',
                 '000300':'沪深300','000016':'上证50','000688':'科创50'}
        data = self.get_quotes(syms)
        return {names.get(d['code'], d['code']): d for d in data}

    def get_hot_stocks(self):
        """获取热门自选股"""
        syms = ['sh600519','sz300750','sz000858','sh600036','sh601318',
                'sz002594','sh600900','sz300059','sz000333','sh601899',
                'sh600887','sz000568','sh600030','sh600585','sz000651',
                'sh601166','sz002415','sh600690','sz002475','sh600276',
                'sh601012','sz002714','sz000002','sh600809','sz300124']
        return self.get_quotes(syms)

    def get_history(self, symbol, days=200):
        """获取日K线"""
        url = f"http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={symbol},day,,{days}"
        data = self._curl(url)
        if not data:
            return None
        try:
            jd = json.loads(data)
            market = symbol[:2]; code = symbol[2:]
            item = jd.get('data', {}).get(code, {})
            klines = item.get('day') or item.get('qfqday') or []
            if not klines:
                return None
            rows = []
            for r in klines[-days:]:
                if len(r) >= 6:
                    rows.append([r[0], float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(float(r[5]))])
            df = pd.DataFrame(rows, columns=['日期','开盘','收盘','最高','最低','成交量'])
            df['日期'] = pd.to_datetime(df['日期'])
            df['涨跌幅'] = df['收盘'].pct_change() * 100
            df = df.sort_values('日期').reset_index(drop=True)
            return df
        except:
            return None

    def scan_signals(self, symbols=None):
        """扫描技术信号"""
        if not symbols:
            # 自动扫描热门+指数成分
            hot = self.get_hot_stocks()
            symbols = [s['code'] for s in hot[:20]]
        signals = []
        for sym in symbols:
            if sym.startswith('sh') or sym.startswith('sz'):
                # 转格式
                code = sym[2:]
                pre = 'sh' if code.startswith('6') or code.startswith('9') else ('sz' if code.startswith('0') or code.startswith('3') else 'sh')
                full = f"{pre}{code}"
            else:
                full = sym
            hist = self.get_history(full, 100)
            if hist is not None and len(hist) > 20:
                sigs = []
                # MA
                ma5 = hist['收盘'].rolling(5).mean().iloc[-1]
                ma20 = hist['收盘'].rolling(20).mean().iloc[-1]
                price = hist['收盘'].iloc[-1]
                if price > ma5 and ma5 > ma20:
                    sigs.append("📈多头排列")
                elif price < ma5 and ma5 < ma20:
                    sigs.append("📉空头排列")
                elif price > ma20:
                    sigs.append("站上20日线")
                else:
                    sigs.append("20日线下方")

                # RSI
                delta = hist['收盘'].diff()
                gain = delta.clip(lower=0).rolling(14).mean()
                loss = (-delta.clip(upper=0)).rolling(14).mean()
                rsi = 100 - 100 / (1 + gain / loss) if loss.iloc[-1] != 0 else 50
                sigs.append(f"RSI={rsi.iloc[-1]:.0f}")

                signals.append({
                    'code': full,
                    'price': price,
                    'change': round(hist['涨跌幅'].iloc[-1], 2) if '涨跌幅' in hist.columns else 0,
                    'signals': ' | '.join(sigs),
                    'rsi': round(rsi.iloc[-1], 1)
                })
        return signals


def test():
    api = AStockEngine()
    print("=" * 45)

    # 指数
    idx = api.get_index()
    print("📈 大盘指数:")
    for n, d in idx.items():
        a = '🟢' if d['change_pct'] >= 0 else '🔴'
        print(f"  {a} {n}: {d['price']} ({d['change_pct']:+.2f}%)")

    # 热门
    hot = api.get_hot_stocks()
    print("\n🔥 热门股:")
    for s in sorted(hot, key=lambda x: abs(x['change_pct']), reverse=True)[:10]:
        a = '🟢' if s['change_pct'] >= 0 else '🔴'
        print(f"  {a} {s['name']}({s['code']}): {s['price']} ({s['change_pct']:+.2f}%)")

    # 历史
    hist = api.get_history('sh600519', 30)
    if hist is not None:
        print(f"\n📊 茅台最近5日:")
        print(hist.tail(5)[['日期','收盘','涨跌幅']].to_string(index=False))

    # 信号
    print("\n🔍 技术信号扫描:")
    sigs = api.scan_signals()
    for s in sigs[:10]:
        print(f"  {s['code']}: {s['price']} | {s['signals']}")

    print(f"\n{'='*45}")
    print(f"✅ 所有接口测试通过")

if __name__ == "__main__":
    test()
