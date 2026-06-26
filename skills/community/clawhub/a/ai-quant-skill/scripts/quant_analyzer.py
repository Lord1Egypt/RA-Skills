# -*- coding: utf-8 -*-
"""
WorkBuddy AI Quant Skill - Technical Analyzer
提供核心技术指标分析，包括MACD/KDJ/SAR/均线/OBV/PVT/BOLL/CCI/RSI
并根据指标特征提供突破、量能、风险、交易信号等分析。

数据源: 东方财富/腾讯 (通过akshare)
"""

import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
import warnings
import sys

warnings.filterwarnings('ignore')

class OpenClawQuantAnalyzer:
    """WorkBuddy 量化技术分析器"""

    def __init__(self):
        self.disclaimer = (
            "\n【免责声明】\n"
            "本报告仅供参考，不构成任何投资建议。投资者不应以该等信息取代其独立判断或仅根据该等信息做出决策。\n"
            "股市有风险，入市需谨慎。技术指标存在滞后性，请结合基本面、政策面等多维度综合判断。"
        )

    def get_data(self, symbol, days=120):
        """获取行情数据"""
        try:
            # 格式化代码
            if len(symbol) == 6:
                if symbol.startswith('6'):
                    market = 'sh'
                else:
                    market = 'sz'
            else:
                return None

            end_date = datetime.now()
            start_date = end_date - timedelta(days=days * 1.5) # 多取一点保证交易日充足

            # 使用 akshare 获取历史行情 (腾讯接口通常更稳定)
            try:
                df = ak.stock_zh_a_hist(
                    symbol=symbol,
                    period="daily",
                    start_date=start_date.strftime("%Y%m%d"),
                    end_date=end_date.strftime("%Y%m%d"),
                    adjust="qfq"
                )
            except:
                # 备用方案
                df = ak.stock_zh_a_daily(
                    symbol=f"{market}{symbol}",
                    start_date=start_date.date(),
                    end_date=end_date.date()
                )

            if df is None or len(df) < 30:
                return None

            # 标准化列名
            mapping = {
                '日期': 'date', '开盘': 'open', '最高': 'high', '最低': 'low',
                '收盘': 'close', '成交量': 'volume', '成交额': 'amount',
                '涨跌幅': 'pct_chg'
            }
            df = df.rename(columns=mapping)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            
            return df
        except Exception as e:
            print(f"数据获取失败: {e}")
            return None

    def calculate_indicators(self, df):
        """计算核心 9 大指标"""
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']

        # 1. 均线 (MA)
        df['MA5'] = close.rolling(5).mean()
        df['MA10'] = close.rolling(10).mean()
        df['MA20'] = close.rolling(20).mean()
        df['MA60'] = close.rolling(60).mean()

        # 2. MACD
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        df['DIF'] = ema12 - ema26
        df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
        df['MACD'] = (df['DIF'] - df['DEA']) * 2

        # 3. KDJ
        low9 = low.rolling(9).min()
        high9 = high.rolling(9).max()
        rsv = (close - low9) / (high9 - low9) * 100
        df['K'] = rsv.ewm(span=3, adjust=False).mean()
        df['D'] = df['K'].ewm(span=3, adjust=False).mean()
        df['J'] = 3 * df['K'] - 2 * df['D']

        # 4. RSI (14日)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))

        # 5. BOLL (布林带)
        df['BOLL_Mid'] = close.rolling(20).mean()
        df['BOLL_Std'] = close.rolling(20).std()
        df['BOLL_Upper'] = df['BOLL_Mid'] + 2 * df['BOLL_Std']
        df['BOLL_Lower'] = df['BOLL_Mid'] - 2 * df['BOLL_Std']

        # 6. CCI (20日)
        tp = (high + low + close) / 3
        ma_tp = tp.rolling(20).mean()
        md = tp.rolling(20).apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
        df['CCI'] = (tp - ma_tp) / (0.015 * md)

        # 7. OBV (能量潮)
        df['OBV'] = (np.sign(close.diff()).fillna(0) * volume).cumsum()

        # 8. PVT (价量趋势)
        df['PVT'] = (close.pct_change().fillna(0) * volume).cumsum()

        # 9. SAR (抛物线转向) - 简易实现
        df['SAR'] = self._calculate_sar(df)

        return df

    def _calculate_sar(self, df):
        """
        抛物线指标 (SAR) 简易算法
        """
        high = df['high'].values
        low = df['low'].values
        sar = np.zeros(len(df))
        
        # 初始状态
        bull = True # 初始看涨
        af = 0.02
        ep = high[0]
        sar[0] = low[0]
        
        for i in range(1, len(df)):
            sar[i] = sar[i-1] + af * (ep - sar[i-1])
            
            if bull:
                if low[i] < sar[i]:
                    bull = False
                    sar[i] = ep
                    ep = low[i]
                    af = 0.02
                else:
                    if high[i] > ep:
                        ep = high[i]
                        af = min(af + 0.02, 0.2)
                    sar[i] = min(sar[i], low[i-1], low[max(0, i-2)])
            else:
                if high[i] > sar[i]:
                    bull = True
                    sar[i] = ep
                    ep = high[i]
                    af = 0.02
                else:
                    if low[i] < ep:
                        ep = low[i]
                        af = min(af + 0.02, 0.2)
                    sar[i] = max(sar[i], high[i-1], high[max(0, i-2)])
                    
        return sar

    def analyze_status(self, df):
        """分析当前状态：突破、量能、风险、交易信号"""
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 1. 突破分析 (Breakout)
        breakout = []
        if latest['close'] > latest['BOLL_Upper']:
            breakout.append("向上突破布林带上轨 (强势拉升)")
        elif latest['close'] < latest['BOLL_Lower']:
            breakout.append("向下触及布林带下轨 (超跌)")
            
        if latest['close'] > latest['MA60'] and prev['close'] <= prev['MA60']:
            breakout.append("放量突破60日生命线 (中期走强)")
            
        if latest['CCI'] > 100 and prev['CCI'] <= 100:
            breakout.append("CCI进入强势区间 (进入暴走模式)")
            
        # 2. 量能分析 (Momentum/Volume)
        volume_status = []
        vol_ma5 = df['volume'].tail(5).mean()
        if latest['volume'] > vol_ma5 * 1.5:
            volume_status.append("放量 (成交量超均值50%)")
        elif latest['volume'] < vol_ma5 * 0.5:
            volume_status.append("缩量 (交投清淡)")
            
        obv_trend = "上升" if latest['OBV'] > df['OBV'].iloc[-5] else "下降"
        pvt_trend = "上升" if latest['PVT'] > df['PVT'].iloc[-5] else "下降"
        volume_status.append(f"OBV{obv_trend}，PVT{pvt_trend}，资金流向{'积极' if obv_trend == '上升' else '消极'}")

        # 3. 风险评估 (Risk)
        risk = []
        rsi = latest['RSI']
        if rsi > 75:
            risk.append("高位超买 (RSI>75)，防范回调")
        elif rsi < 25:
            risk.append("低位超卖 (RSI<25)，随时反弹")
            
        volatility = df['close'].pct_change().std() * np.sqrt(252) * 100
        risk_level = "高" if volatility > 45 else ("中" if volatility > 25 else "低")
        risk.append(f"当前年化波动率约为 {volatility:.1f}%，风险等级: {risk_level}")

        # 4. 交易信号 (Signals)
        signals = []
        # MACD
        if latest['DIF'] > latest['DEA'] and prev['DIF'] <= prev['DEA']:
            signals.append("MACD金叉 (买入信号)")
        elif latest['DIF'] < latest['DEA'] and prev['DIF'] >= prev['DEA']:
            signals.append("MACD死叉 (卖出信号)")
            
        # KDJ
        if latest['K'] > latest['D'] and prev['K'] <= prev['D']:
            signals.append("KDJ金叉 (短线买入)")
            
        # SAR
        if latest['close'] > latest['SAR'] and prev['close'] <= prev['SAR']:
            signals.append("SAR反转向上 (止损转向持股)")
        elif latest['close'] < latest['SAR'] and prev['close'] >= prev['SAR']:
            signals.append("SAR反转向下 (离场信号)")

        return {
            'breakout': breakout,
            'volume': volume_status,
            'risk': risk,
            'signals': signals
        }

    def run_analysis(self, symbol):
        """执行全流程分析并汇总返回报告内容"""
        df = self.get_data(symbol)
        if df is None:
            return f"无法获取股票 {symbol} 的数据，请检查代码是否正确。"
        
        df = self.calculate_indicators(df)
        status = self.analyze_status(df)
        latest = df.iloc[-1]
        
        report = []
        report.append(f"📊 WorkBuddy 量化分析报告 - {symbol}")
        report.append(f"日期: {latest['date'].strftime('%Y-%m-%d')}  收盘价: {latest['close']:.2f}")
        report.append("-" * 40)
        
        report.append("【突破特征】")
        if status['breakout']:
            for s in status['breakout']: report.append(f"  • {s}")
        else:
            report.append("  • 无显著技术突破")
            
        report.append("\n【量能分析】")
        for s in status['volume']: report.append(f"  • {s}")
            
        report.append("\n【风险评估】")
        for s in status['risk']: report.append(f"  • {s}")
            
        report.append("\n【交易信号】")
        if status['signals']:
            for s in status['signals']: report.append(f"  • {s}")
        else:
            report.append("  • 信号中性，建议观望")
            
        report.append("\n【核心指标一览】")
        report.append(f"  • 均线系统: MA5={latest['MA5']:.2f}, MA20={latest['MA20']:.2f}, MA60={latest['MA60']:.2f}")
        report.append(f"  • MACD: DIF={latest['DIF']:.3f}, DEA={latest['DEA']:.3f}, HIST={latest['MACD']:.3f}")
        report.append(f"  • KDJ: K={latest['K']:.1f}, D={latest['D']:.1f}, J={latest['J']:.1f}")
        report.append(f"  • 强弱/超买卖: RSI={latest['RSI']:.1f}, CCI={latest['CCI']:.1f}")
        report.append(f"  • 布林带: 中轨={latest['BOLL_Mid']:.2f}, 上轨={latest['BOLL_Upper']:.2f}, 下轨={latest['BOLL_Lower']:.2f}")
        report.append(f"  • 量价指标: OBV={latest['OBV']:.0f}, PVT={latest['PVT']:.0f}")
        report.append(f"  • 趋势转向: SAR={latest['SAR']:.2f} ({'看多' if latest['close']>latest['SAR'] else '看空'})")
        
        report.append(self.disclaimer)
        return "\n".join(report)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='WorkBuddy Quant Analyzer')
    parser.add_argument('symbol', type=str, help='Stock symbol (e.g. 600519)')
    args = parser.parse_args()
    
    analyzer = OpenClawQuantAnalyzer()
    print(analyzer.run_analysis(args.symbol))

