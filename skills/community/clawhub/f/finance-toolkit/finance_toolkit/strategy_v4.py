#!/usr/bin/env python3
"""
多指标策略引擎 v4 — 布林带/RSI/KDJ/MACD 融合
"""

import sys, os, subprocess as _bridge_sh
if 'msys64' in sys.executable:
    _bridge_sh.run(['C:/Python314/python.exe'] + sys.argv)
    sys.exit(0)

import subprocess, json, pandas as pd, numpy as np

# ==================== 数据源 ====================

class DataSource:
    """数据源（新浪+腾讯双后备）"""
    
    def _sina_kline(self, symbol, days=400):
        """新浪K线数据"""
        url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={symbol}&scale=240&ma=no&datalen={days}"
        r = subprocess.run(
            ['curl.exe','-s','-L','-e','http://finance.sina.com.cn',
             '-H','Referer: http://finance.sina.com.cn', url],
            capture_output=True, timeout=15)
        raw = r.stdout.decode('utf-8', errors='ignore')
        if not raw.strip(): return None
        data = json.loads(raw)
        return [{'date': d['day'], 'open': float(d['open']), 'high': float(d['high']),
                 'low': float(d['low']), 'close': float(d['close']), 'volume': int(d['volume'])} for d in data]

    def _tencent_kline(self, symbol, days=400):
        """腾讯K线数据（备选）"""
        code = symbol.replace('sz', '').replace('sh', '')
        url = f"https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=kline&code={symbol}&r=0"
        r = subprocess.run(['curl.exe','-s',url], capture_output=True, timeout=15)
        raw = r.stdout.decode('utf-8', errors='ignore')
        try:
            import re
            raw_clean = re.sub(r'^kline\s*=\s*', '', raw).strip()
            data = json.loads(raw_clean)
            dk = data.get('data', {}).get(symbol, {}).get('qt', {}).get(code, {}).get('qk', {})
            days_data = dk.get('days', []) if isinstance(dk, dict) else []
            if not days_data and isinstance(dk, list):
                days_data = dk
            rows = []
            for item in days_data[-days:]:
                if len(item) >= 6:
                    rows.append({'date': item[0], 'open': float(item[1]), 'close': float(item[3]),
                                 'high': float(item[2]), 'low': float(item[4]), 'volume': int(item[5])})
            return rows if rows else None
        except:
            return None

    def get_kline(self, symbol, days=400):
        """获取K线数据（新浪优先，腾讯备选）"""
        sources = [
            ("新浪", lambda: self._sina_kline(symbol, days)),
            ("腾讯", lambda: self._tencent_kline(symbol, days)),
        ]
        for name, fetcher in sources:
            try:
                rows = fetcher()
                if rows and len(rows) > 20:
                    df = pd.DataFrame(rows)
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date').reset_index(drop=True)
                    df['return'] = df['close'].pct_change()
                    return df
            except Exception as e:
                print(f"  [{name}] 获取失败: {e}")
        return None

# ==================== 指标计算 ====================

class Indicators:
    """技术指标计算工具类"""

    @staticmethod
    def MA(df, period):
        return df['close'].rolling(period).mean()

    @staticmethod
    def EMA(df, period):
        return df['close'].ewm(span=period, adjust=False).mean()

    @staticmethod
    def RSI(df, period=14):
        """RSI (相对强弱指标)"""
        delta = df['close'].diff()
        gain = delta.clip(lower=0).rolling(period).mean()
        loss = (-delta.clip(upper=0)).rolling(period).mean()
        rs = gain / loss.replace(0, np.nan)
        return 100 - 100 / (1 + rs)

    @staticmethod
    def Bollinger(df, period=20, k=2):
        """布林带"""
        mid = df['close'].rolling(period).mean()
        std = df['close'].rolling(period).std()
        return mid, mid + k * std, mid - k * std

    @staticmethod
    def MACD(df, fast=12, slow=26, signal=9):
        """MACD"""
        ema_f = df['close'].ewm(span=fast).mean()
        ema_s = df['close'].ewm(span=slow).mean()
        dif = ema_f - ema_s
        dea = dif.ewm(span=signal).mean()
        macd = (dif - dea) * 2
        return dif, dea, macd

    @staticmethod
    def KDJ(df, n=9, m1=3, m2=3):
        """KDJ指标"""
        low_n = df['low'].rolling(n).min()
        high_n = df['high'].rolling(n).max()
        rsv = (df['close'] - low_n) / (high_n - low_n).replace(0, np.nan) * 100
        k = rsv.ewm(span=m1).mean()
        d = k.ewm(span=m2).mean()
        j = 3 * k - 2 * d
        return k, d, j

    @staticmethod
    def ATR(df, period=14):
        """平均真实波幅"""
        high_low = df['high'] - df['low']
        high_close = (df['high'] - df['close'].shift(1)).abs()
        low_close = (df['low'] - df['close'].shift(1)).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    @staticmethod
    def VolumeRatio(df, period=20):
        """量比"""
        return df['volume'] / df['volume'].rolling(period).mean()

# ==================== 策略 ====================

class Backtest:
    """回测引擎"""

    @staticmethod
    def evaluate(result, name="策略"):
        """统一回测评估"""
        result['sr'] = result['position'].shift(1) * result['return']
        result['sr'] = result['sr'].fillna(0)
        result['cum'] = (1 + result['sr']).cumprod()
        result['cum_bh'] = (1 + result['return']).cumprod()

        total = result['cum'].iloc[-1] - 1
        bh = result['cum_bh'].iloc[-1] - 1
        years = len(result) / 252
        annual = (1 + total) ** (1 / years) - 1 if years > 0 else 0
        excess = result['sr'] - 0.02/252
        sharpe = np.sqrt(252) * excess.mean() / excess.std() if excess.std() > 0 else 0
        cum_max = result['cum'].cummax()
        mdd = (result['cum'] / cum_max - 1).min()

        trades = result[result['signal'] != 0]
        wr = (trades['sr'] > 0).sum() / len(trades) if len(trades) > 0 else 0
        buys = int((result['signal'] == 1).sum())

        return {
            '策略': name,
            '总收益': f"{total*100:.2f}%",
            '买入持有': f"{bh*100:.2f}%",
            '年化': f"{annual*100:.2f}%",
            '夏普': round(sharpe, 2),
            '回撤': f"{mdd*100:.2f}%",
            '胜率': f"{wr*100:.0f}%",
            '交易': f"{buys}次",
            '_total': total,
            '_annual': annual,
            '_sharpe': sharpe,
            '_mdd': mdd,
            '_wr': wr,
            '_buys': buys,
        }

# ==================== 各策略实现 ====================

class Strategies:
    """策略库"""

    @staticmethod
    def MA_Cross(df, fast=5, slow=20, stop_loss=None):
        """MA双均线金叉/死叉"""
        d = df.copy()
        d['ma_f'] = d['close'].rolling(fast).mean()
        d['ma_s'] = d['close'].rolling(slow).mean()
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(len(d)):
            if not pos and d['ma_f'].iloc[i] > d['ma_s'].iloc[i]:
                pos = True; entry = d['close'].iloc[i]
                d.loc[d.index[i], 'signal'] = 1
            elif pos:
                sell = d['ma_f'].iloc[i] < d['ma_s'].iloc[i]
                if stop_loss and not sell:
                    if (d['close'].iloc[i] - entry) / entry < -stop_loss:
                        sell = True
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

    @staticmethod
    def Bollinger_Reversal(df, period=20, k=2, stop_loss=None):
        """布林带反转策略：触下轨买，回中轨卖"""
        d = df.copy()
        d['mid'], d['upper'], d['lower'] = Indicators.Bollinger(d, period, k)
        d['bw'] = (d['upper'] - d['lower']) / d['mid'] * 100  # 带宽
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(len(d)):
            if not pos:
                if d['low'].iloc[i] <= d['lower'].iloc[i] and d['bw'].iloc[i] > 3:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
            else:
                sell = d['close'].iloc[i] >= d['mid'].iloc[i]
                if stop_loss and not sell:
                    if (d['close'].iloc[i] - entry) / entry < -stop_loss:
                        sell = True
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

    @staticmethod
    def KDJ_OverTrade(df, n=9, stop_loss=None):
        """KDJ超买超卖策略：K<20且J<0买入，K>80且J>100卖出"""
        d = df.copy()
        k, d_kdj, j = Indicators.KDJ(d, n)
        d['k'] = k; d['d'] = d_kdj; d['j'] = j
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(len(d)):
            if not pos:
                if d['k'].iloc[i] < 20 and d['j'].iloc[i] < 0 and d['k'].iloc[i] > 0:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
            else:
                sell = d['k'].iloc[i] > 80 or d['j'].iloc[i] > 100
                if stop_loss and not sell:
                    if (d['close'].iloc[i] - entry) / entry < -stop_loss:
                        sell = True
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

    @staticmethod
    def RSI_MeanReversion(df, period=14, oversold=30, overbought=70, stop_loss=None):
        """RSI均值回归：超卖买，超买卖"""
        d = df.copy()
        d['rsi'] = Indicators.RSI(d, period)
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(len(d)):
            if not pos:
                if d['rsi'].iloc[i] < oversold:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
            else:
                sell = d['rsi'].iloc[i] > overbought or d['rsi'].iloc[i] > 50
                if stop_loss and not sell:
                    if (d['close'].iloc[i] - entry) / entry < -stop_loss:
                        sell = True
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

    @staticmethod
    def MACD_Cross(df, stop_loss=None):
        """MACD金叉死叉策略"""
        d = df.copy()
        d['dif'], d['dea'], d['macd'] = Indicators.MACD(d)
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(1, len(d)):
            if not pos:
                if d['macd'].iloc[i-1] < 0 and d['macd'].iloc[i] > 0:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
                elif d['dif'].iloc[i-1] < d['dea'].iloc[i-1] and d['dif'].iloc[i] > d['dea'].iloc[i]:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
            else:
                sell = d['macd'].iloc[i-1] > 0 and d['macd'].iloc[i] < 0
                if not sell and d['dif'].iloc[i-1] > d['dea'].iloc[i-1] and d['dif'].iloc[i] < d['dea'].iloc[i]:
                    sell = True
                if stop_loss and not sell:
                    if (d['close'].iloc[i] - entry) / entry < -stop_loss:
                        sell = True
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

    @staticmethod
    def Fusion_MA_Bollinger(df, fast=14, slow=18, bb_period=20, stop_loss=0.05):
        """融合策略：MA金叉 + 布林下轨确认"""
        d = df.copy()
        d['ma_f'] = d['close'].rolling(fast).mean()
        d['ma_s'] = d['close'].rolling(slow).mean()
        d['mid'], d['upper'], d['lower'] = Indicators.Bollinger(d, bb_period, 2)
        d['rsi'] = Indicators.RSI(d, 14)
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(len(d)):
            if not pos:
                # 买入条件：MA金叉 + RSI不超买 + 接近布林下轨
                buy_ma = d['ma_f'].iloc[i] > d['ma_s'].iloc[i]
                buy_rsi = d['rsi'].iloc[i] < 70
                buy_bb = d['close'].iloc[i] <= d['mid'].iloc[i] * 1.02  # 不偏离中轨太远
                if buy_ma and buy_rsi and buy_bb:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
            else:
                sell = d['ma_f'].iloc[i] < d['ma_s'].iloc[i]
                if stop_loss and not sell:
                    if (d['close'].iloc[i] - entry) / entry < -stop_loss:
                        sell = True
                if d['rsi'].iloc[i] > 80:
                    sell = True  # RSI 超买强制卖出
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

    @staticmethod
    def Fusion_Bollinger_KDJ(df, bb_period=20, kdj_n=9, stop_loss=0.05):
        """融合策略：布林带触底 + KDJ共振"""
        d = df.copy()
        d['mid'], d['upper'], d['lower'] = Indicators.Bollinger(d, bb_period, 2)
        k, d_kdj, j = Indicators.KDJ(d, kdj_n)
        d['k'] = k; d['kdj_j'] = j
        d['rsi'] = Indicators.RSI(d, 14)
        d['atr'] = Indicators.ATR(d, 14)
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(len(d)):
            if not pos:
                touch_lower = d['low'].iloc[i] <= d['lower'].iloc[i]
                kdj_oversold = d['k'].iloc[i] < 25
                rsi_ok = d['rsi'].iloc[i] < 40
                if touch_lower and kdj_oversold and rsi_ok:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
            else:
                sell = d['close'].iloc[i] >= d['mid'].iloc[i]
                if not sell and d['kdj_j'].iloc[i] > 100:
                    sell = True
                if stop_loss:
                    if (d['close'].iloc[i] - entry) / entry < -stop_loss:
                        sell = True
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

    @staticmethod
    def Fusion_Triple_Confirmation(df, fast=14, slow=18):
        """三确认策略：MA金叉 + RSI多头 + 布林带中轨上方"""
        d = df.copy()
        d['ma_f'] = d['close'].rolling(fast).mean()
        d['ma_s'] = d['close'].rolling(slow).mean()
        d['mid'], _, _ = Indicators.Bollinger(d, 20, 2)
        d['rsi'] = Indicators.RSI(d, 14)
        d['macd_dif'], d['macd_dea'], _ = Indicators.MACD(d)
        d['signal'] = 0; d['position'] = 0
        pos = False; entry = 0
        for i in range(len(d)):
            if not pos:
                buy_ma = d['ma_f'].iloc[i] > d['ma_s'].iloc[i]
                buy_rsi = d['rsi'].iloc[i] > 50
                buy_bb = d['close'].iloc[i] > d['mid'].iloc[i]
                buy_macd = d['macd_dif'].iloc[i] > d['macd_dea'].iloc[i]
                if buy_ma and buy_rsi and buy_bb and buy_macd:
                    pos = True; entry = d['close'].iloc[i]
                    d.loc[d.index[i], 'signal'] = 1
            else:
                sell = d['ma_f'].iloc[i] < d['ma_s'].iloc[i]
                if sell or d['rsi'].iloc[i] > 85 or d['close'].iloc[i] < d['mid'].iloc[i]:
                    sell = True
                if (d['close'].iloc[i] - entry) / entry < -0.05:
                    sell = True  # 止损5%
                if sell:
                    pos = False; d.loc[d.index[i], 'signal'] = -1
            d.loc[d.index[i], 'position'] = 1 if pos else 0
        return d

# ==================== 比较引擎 ====================

class StrategyComparer:
    """策略对比"""

    @staticmethod
    def run_all(df, name):
        """跑所有策略并对比"""
        print(f"\n{'='*65}")
        print(f"🏦 {name}")
        print(f"{'='*65}")
        print(f"  数据: {df['date'].iloc[0].strftime('%Y-%m-%d')} → {df['date'].iloc[-1].strftime('%Y-%m-%d')} ({len(df)}天)")
        print(f"  最新: {df['close'].iloc[-1]:.2f}")
        print(f"  区间: {df['close'].iloc[-1] / df['close'].iloc[0] - 1:.2%}")

        bt = Backtest()

        strategies = [
            ("🔴 MA金叉/死叉 MA5/20", Strategies.MA_Cross(df, 5, 20)),
            ("🔵 MA金叉/死叉 MA14/18", Strategies.MA_Cross(df, 14, 18)),
            ("📊 布林带反转 20/2", Strategies.Bollinger_Reversal(df, 20, 2)),
            ("📊 布林带反转 20/2.5", Strategies.Bollinger_Reversal(df, 20, 2.5)),
            ("📈 KDJ超买超卖 9", Strategies.KDJ_OverTrade(df, 9)),
            ("📉 RSI均值回归 14/30/70", Strategies.RSI_MeanReversion(df, 14, 30, 70)),
            ("💡 MACD金叉死叉", Strategies.MACD_Cross(df)),
            ("🧩 融合: MA14/18+布林中轨+RSI", Strategies.Fusion_MA_Bollinger(df, 14, 18, 20, 0.05)),
            ("🧩 融合: 布林触底+KDJ共振", Strategies.Fusion_Bollinger_KDJ(df, 20, 9, 0.05)),
            ("🧩 融合: 三确认(MA+RSI+BB+MACD)", Strategies.Fusion_Triple_Confirmation(df, 14, 18)),
        ]

        results = []
        for sname, result in strategies:
            m = bt.evaluate(result, sname)
            results.append(m)
            print(f"\n  {sname}")
            print(f"    收益 {m['总收益']:>8} | 年化 {m['年化']:>8} | 夏普 {m['夏普']:>5} | 回撤 {m['回撤']:>6} | 胜率 {m['胜率']:>4} | {m['交易']}")

        print(f"\n{'='*65}")
        print(f"🏆 排名（按夏普比率）:")
        results.sort(key=lambda x: x['_sharpe'], reverse=True)
        for i, m in enumerate(results[:5], 1):
            print(f"  {i}. {m['策略']} — 夏普 {m['夏普']} | 年化 {m['年化']} | 回撤 {m['回撤']}")

        print(f"\n🏆 排名（按总收益率）:")
        results.sort(key=lambda x: x['_total'], reverse=True)
        for i, m in enumerate(results[:5], 1):
            print(f"  {i}. {m['策略']} — 收益 {m['总收益']} | 年化 {m['年化']} | 夏普 {m['夏普']}")

# ==================== 当前行情分析 ====================

class RealTimeAnalyst:
    """实时行情分析"""

    def __init__(self):
        self.ds = DataSource()

    def get_quotes(self, symbols):
        """腾讯实时行情"""
        if isinstance(symbols, str): symbols = [symbols]
        import re
        url = f"http://qt.gtimg.cn/q={','.join(symbols)}"
        r = subprocess.run(['curl.exe','-s',url], capture_output=True, timeout=10)
        raw = r.stdout.decode('gbk', errors='ignore')
        results = {}
        for line in raw.strip().strip(';').split(';'):
            m = re.search(r'"([^"]+)"', line)
            if not m: continue
            p = m.group(1).split('~')
            if len(p) < 46: continue
            results[p[1]] = {
                'name': p[1], 'code': p[2],
                'price': float(p[3]) if p[3] else 0,
                'change_pct': round(float(p[32]) if p[32] else 0, 2),
                'high': float(p[33]) if p[33] else 0,
                'low': float(p[34]) if p[34] else 0,
                'open': float(p[5]) if p[5] else 0,
                'yclose': float(p[4]) if p[4] else 0,
                'volume': int(p[6]) if p[6] else 0,
                'turnover': float(p[38]) if len(p)>38 and p[38] else 0,
                'market_cap': float(p[45]) if len(p)>45 and p[45] else 0,
            }
        return results

    def live_analysis(self, code, days=60):
        """实时多指标分析"""
        sym = f"sz{code}" if not code.startswith(('sh','sz')) else code
        df = self.ds.get_kline(sym, days)
        if df is None or len(df) < 20:
            return {"error": "数据不足"}

        d = df.copy()
        price = d['close'].iloc[-1]

        # 计算全部指标
        ma14 = Indicators.MA(d, 14).iloc[-1]
        ma18 = Indicators.MA(d, 18).iloc[-1]
        ma20 = Indicators.MA(d, 20).iloc[-1]
        ma60 = Indicators.MA(d, 60).iloc[-1] if len(d) >= 60 else price
        rsi = Indicators.RSI(d, 14).iloc[-1]
        k, d_kdj, j = Indicators.KDJ(d, 9)
        mid, upper, lower = Indicators.Bollinger(d, 20, 2)
        dif, dea, macd_val = Indicators.MACD(d)
        atr = Indicators.ATR(d, 14).iloc[-1]

        # 信号
        signals = []

        # MA信号
        if ma14 > ma18:
            signals.append("🟢 MA金叉")
        else:
            signals.append("🔴 MA死叉")

        # RSI
        if rsi < 30:
            signals.append("⚠️ RSI超卖")
        elif rsi > 70:
            signals.append("⚠️ RSI超买")
        else:
            signals.append(f"RSI中性({rsi:.0f})")

        # 布林带
        bb_pos = (price - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]) * 100
        if price <= lower.iloc[-1]:
            signals.append("📊 触下轨")
        elif price >= upper.iloc[-1]:
            signals.append("📊 触上轨")
        else:
            signals.append(f"布林{bb_pos:.0f}%位置")

        # KDJ
        if k.iloc[-1] < 20 and j.iloc[-1] < 0:
            signals.append("📈 KDJ超卖")
        elif k.iloc[-1] > 80 and j.iloc[-1] > 100:
            signals.append("📉 KDJ超买")

        # MACD
        if dif.iloc[-1] > dea.iloc[-1] and macd_val.iloc[-1] > 0:
            signals.append("💡 MACD多头")
        elif dif.iloc[-1] < dea.iloc[-1]:
            signals.append("💡 MACD空头")

        # 支撑压力
        support = round(lower.iloc[-1], 2)
        resistance = round(upper.iloc[-1], 2)

        return {
            'price': price,
            'signals': ' | '.join(signals),
            'ma14': round(ma14, 2), 'ma18': round(ma18, 2),
            'ma20': round(ma20, 2), 'ma60': round(ma60, 2),
            'rsi': round(rsi, 1),
            'k': round(k.iloc[-1], 1), 'd': round(d_kdj.iloc[-1], 1), 'j': round(j.iloc[-1], 1),
            'bb_pos': round(bb_pos, 0),
            'macd': '多头✔️' if dif.iloc[-1] > dea.iloc[-1] else '空头❌',
            'atr': round(atr, 3),
            'support': support,
            'resistance': resistance,
            'bb_lower': round(lower.iloc[-1], 2),
            'bb_upper': round(upper.iloc[-1], 2),
        }

# ==================== 主控制 ====================

if __name__ == "__main__":
    ds = DataSource()
    comparer = StrategyComparer()
    analyst = RealTimeAnalyst()

    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'

    if mode == 'backtest' or mode == 'all':
        print("=" * 65)
        print("🏆 多指标策略对比 — v4")
        print("=" * 65)

        for sym, name in [('sz000009', '中国宝安'), ('sz002332', '仙琚制药')]:
            df = ds.get_kline(sym, 400)
            if df is not None and len(df) > 60:
                comparer.run_all(df, name)
            else:
                print(f"\n❌ {name}: 数据不足")

    if mode == 'live' or mode == 'all':
        print(f"\n{'='*65}")
        print(f"📊 实时多指标分析")
        print(f"{'='*65}")

        for code in ['000009', '002332']:
            ta = analyst.live_analysis(code)
            if 'error' in ta:
                print(f"\n  ❌ {code}: {ta['error']}")
                continue
            print(f"\n  🏦 {code}")
            print(f"  价格: {ta['price']}")
            print(f"  MA14: {ta['ma14']} | MA18: {ta['ma18']} | MA20: {ta['ma20']} | MA60: {ta['ma60']}")
            print(f"  KDJ: K={ta['k']} D={ta['d']} J={ta['j']}")
            print(f"  RSI: {ta['rsi']} | MACD: {ta['macd']}")
            print(f"  布林: {ta['bb_lower']} - {ta['price']} - {ta['bb_upper']} (位置{ta['bb_pos']:.0f}%)")
            print(f"  支撑: {ta['support']} | 压力: {ta['resistance']}")
            print(f"  📡 {ta['signals']}")

    if mode == 'live' or mode == 'all':
        # 实时买入建议
        print(f"\n{'='*65}")
        print(f"🎯 综合买入建议")
        print(f"{'='*65}")

        for code, name in [('000009', '中国宝安'), ('002332', '仙琚制药')]:
            ta = analyst.live_analysis(code)
            if 'error' in ta: continue

            score = 0
            reasons = []

            # MA 趋势 +10
            if ta['ma14'] > ta['ma18']: score += 10; reasons.append("MA金叉")
            else: reasons.append("MA死叉")

            # RSI不超买 +10
            if ta['rsi'] < 70: score += 10; reasons.append("RSI正常")
            else: reasons.append("RSI超买⚠️")

            # RSI超卖 +15 (抄底信号)
            if ta['rsi'] < 30: score += 15; reasons.append("RSI超卖⚡")

            # 布林位置
            if ta['bb_pos'] < 20: score += 15; reasons.append("布林低位⚡")
            elif ta['bb_pos'] < 40: score += 10; reasons.append("布林中低位")
            elif ta['bb_pos'] > 80: score -= 10; reasons.append("布林高位⚠️")

            # KDJ
            if ta['k'] < 20: score += 10; reasons.append("KDJ超卖")
            elif ta['k'] > 80: score -= 5; reasons.append("KDJ超买")

            # MACD
            if '多头' in ta['macd']: score += 10; reasons.append("MACD多头")
            else: reasons.append("MACD空头")

            # 信号
            if score >= 45:
                rec = "✅ **强烈买入信号**"
            elif score >= 30:
                rec = "🟢 **可考虑买入**"
            elif score >= 15:
                rec = "⚪ **观望**"
            else:
                rec = "🔴 **回避**"

            print(f"\n  🏦 {name}")
            print(f"  评分: {score}/60 | {rec}")
            print(f"  理由: {' · '.join(reasons)}")

    print(f"\n{'='*65}")
    print("✅ 分析完成")
