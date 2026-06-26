"""
技术面分析
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from .base import BaseAnalyzer

try:
    import efinance as ef
except ImportError:
    ef = None


class TechnicalAnalyzer(BaseAnalyzer):
    """技术面分析器"""

    @property
    def name(self) -> str:
        return "技术面分析"

    @property
    def dimensions(self) -> list:
        return ['trend', 'moving_average', 'support_resistance', 'indicators', 'fund_flow']

    def calculate_ma(self, df: pd.DataFrame, periods: list = [5, 10, 20, 60]) -> Dict:
        """计算均线"""
        ma_result = {}
        close_prices = df['收盘']
        
        for period in periods:
            ma = close_prices.rolling(window=period).mean()
            ma_result[f'MA{period}'] = ma.iloc[-1]
            ma_result[f'MA{period}_prev'] = ma.iloc[-2]
        
        # 判断均线多头排列
        ma5 = ma_result['MA5']
        ma10 = ma_result['MA10']
        ma20 = ma_result['MA20']
        ma60 = ma_result['MA60']
        
        # 当前价格位置
        current_price = close_prices.iloc[-1]
        ma_result['current_price'] = current_price
        
        # 判断排列关系
        if ma5 > ma10 > ma20 > ma60:
            ma_result['arrangement'] = '多头排列'
            ma_result['trend_strength'] = '强势多头'
        elif ma5 < ma10 < ma20 < ma60:
            ma_result['arrangement'] = '空头排列'
            ma_result['trend_strength'] = '弱势空头'
        elif ma5 > ma10 > ma20 and current_price > ma60:
            ma_result['arrangement'] = '偏多排列'
            ma_result['trend_strength'] = '中期转强'
        else:
            ma_result['arrangement'] = '交叉震荡'
            ma_result['trend_strength'] = '方向不明'
        
        return ma_result

    def calculate_kdj(self, df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> Dict:
        """计算KDJ指标"""
        low_list = df['最低'].rolling(n).min()
        high_list = df['最高'].rolling(n).max()
        rsv = (df['收盘'] - low_list) / (high_list - low_list) * 100
        
        k = rsv.ewm(alpha=1/m1, adjust=False).mean()
        d = k.ewm(alpha=1/m2, adjust=False).mean()
        j = 3 * k - 2 * d
        
        return {
            'K': k.iloc[-1],
            'D': d.iloc[-1],
            'J': j.iloc[-1],
            'K_prev': k.iloc[-2],
            'D_prev': d.iloc[-2],
            'J_prev': j.iloc[-2]
        }

    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> Dict:
        """计算RSI指标"""
        delta = df['收盘'].diff()
        gain = delta.where(delta > 0, 0)
        loss = (-delta).where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return {
            f'RSI{period}': rsi.iloc[-1],
            f'RSI{period}_prev': rsi.iloc[-2]
        }

    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """计算MACD指标"""
        close = df['收盘']
        exp1 = close.ewm(span=fast, adjust=False).mean()
        exp2 = close.ewm(span=slow, adjust=False).mean()
        dif = exp1 - exp2
        dea = dif.ewm(span=signal, adjust=False).mean()
        macd = (dif - dea) * 2
        
        return {
            'DIF': dif.iloc[-1],
            'DEA': dea.iloc[-1],
            'MACD': macd.iloc[-1],
            'DIF_prev': dif.iloc[-2],
            'DEA_prev': dea.iloc[-2],
            'MACD_prev': macd.iloc[-2]
        }

    def find_support_resistance(self, df: pd.DataFrame, lookback: int = 60) -> Dict:
        """找出支撑位和压力位"""
        recent = df.tail(lookback)
        high_max = recent['最高'].max()
        low_min = recent['最低'].min()
        current_price = recent['收盘'].iloc[-1]
        
        # 找近期关键价格平台
        highs = recent.nlargest(5, '最高')['最高'].mean()
        lows = recent.nsmallest(5, '最低')['最低'].mean()
        
        # 计算均线作为支撑压力
        ma20 = recent['收盘'].rolling(20).mean().iloc[-1]
        ma60 = recent['收盘'].rolling(60).mean().iloc[-1]
        
        # 确定支撑和压力
        supports = []
        resistances = []
        
        if current_price > ma20:
            supports.append(round(ma20, 2))
        else:
            resistances.append(round(ma20, 2))
            
        if current_price > ma60:
            supports.append(round(ma60, 2))
        else:
            resistances.append(round(ma60, 2))
        
        supports.append(round(lows, 2))
        resistances.append(round(highs, 2))
        
        supports = sorted(list(set(supports)))
        resistances = sorted(list(set(resistances)))
        
        return {
            'support_levels': supports,
            'resistance_levels': resistances,
            'recent_low': round(low_min, 2),
            'recent_high': round(high_max, 2),
            'ma20_level': round(ma20, 2),
            'ma60_level': round(ma60, 2)
        }

    def analyze_trend(self, df: pd.DataFrame, ma_result: Dict) -> Dict:
        """分析整体趋势"""
        current_price = ma_result['current_price']
        ma5 = ma_result['MA5']
        ma10 = ma_result['MA10']
        ma20 = ma_result['MA20']
        ma60 = ma_result['MA60']
        
        # 计算近期涨跌幅
        if len(df) >= 20:
            change_5 = (current_price - df['收盘'].iloc[-5]) / df['收盘'].iloc[-5] * 100
            change_20 = (current_price - df['收盘'].iloc[-20]) / df['收盘'].iloc[-20] * 100
            change_60 = (current_price - df['收盘'].iloc[-60]) / df['收盘'].iloc[-60] * 100 if len(df) >= 60 else None
        else:
            change_5 = change_20 = change_60 = None
        
        # 判断趋势方向
        if current_price > ma5 > ma10 > ma20 > ma60:
            direction = '明确上升'
            strength = '强势'
            rating = '积极'
        elif current_price < ma5 < ma10 < ma20 < ma60:
            direction = '明确下降'
            strength = '弱势'
            rating = '消极'
        elif current_price > ma60 and ma5 > ma20:
            direction = '中期上升'
            strength = '中等偏强'
            rating = '偏多'
        elif current_price < ma60 and ma5 < ma20:
            direction = '中期下降'
            strength = '中等偏弱'
            rating = '偏空'
        else:
            direction = '震荡整理'
            strength = '方向不明'
            rating = '中性'
        
        return {
            'direction': direction,
            'strength': strength,
            'rating': rating,
            'change_5d': round(change_5, 2) if change_5 is not None else None,
            'change_20d': round(change_20, 2) if change_20 is not None else None,
            'change_60d': round(change_60, 2) if change_60 is not None else None
        }

    def analyze_indicators(self, kdj: Dict, rsi: Dict, macd: Dict) -> Dict:
        """综合分析技术指标"""
        signals = {
            'kdj_signal': '中性',
            'rsi_signal': '中性',
            'macd_signal': '中性',
            'overall': '中性'
        }
        
        # KDJ分析
        k = kdj['K']
        d = kdj['D']
        j = kdj['J']
        k_prev = kdj['K_prev']
        d_prev = kdj['D_prev']
        
        if k < 20 and j < 0:
            signals['kdj_signal'] = '超卖'
        elif k > 80 and j > 100:
            signals['kdj_signal'] = '超买'
        elif k > d and k_prev < d_prev:
            signals['kdj_signal'] = '金叉'
        elif k < d and k_prev > d_prev:
            signals['kdj_signal'] = '死叉'
        else:
            signals['kdj_signal'] = '中性'
        
        # RSI分析
        rsi14 = rsi['RSI14']
        if rsi14 < 30:
            signals['rsi_signal'] = '超卖'
        elif rsi14 > 70:
            signals['rsi_signal'] = '超买'
        elif rsi14 < 50:
            signals['rsi_signal'] = '偏弱'
        else:
            signals['rsi_signal'] = '偏强'
        
        # MACD分析
        dif = macd['DIF']
        dea = macd['DEA']
        macd_bar = macd['MACD']
        dif_prev = macd['DIF_prev']
        dea_prev = macd['DEA_prev']
        
        if dif > dea and dif_prev <= dea_prev:
            signals['macd_signal'] = '金叉'
        elif dif < dea and dif_prev >= dea_prev:
            signals['macd_signal'] = '死叉'
        elif dif > dea and macd_bar > 0:
            signals['macd_signal'] = '多头排列'
        elif dif < dea and macd_bar < 0:
            signals['macd_signal'] = '空头排列'
        else:
            signals['macd_signal'] = '中性'
        
        # 综合评分
        bull_count = 0
        bull_signals = ['超卖', '金叉', '偏强', '多头排列']
        bear_signals = ['超买', '死叉', '偏弱', '空头排列']
        
        if signals['kdj_signal'] in bull_signals:
            bull_count += 1
        if signals['rsi_signal'] in bull_signals:
            bull_count += 1
        if signals['macd_signal'] in bull_signals:
            bull_count += 1
        
        if bull_count >= 2:
            signals['overall'] = '多头信号'
        elif bull_count == 0:
            signals['overall'] = '空头信号'
        else:
            signals['overall'] = '信号混杂'
        
        return signals

    def calculate_score(self, trend: Dict, ma: Dict, indicators: Dict, sr: Dict) -> int:
        """计算技术面得分"""
        score = 50  # 基础分
        
        # 趋势加分
        trend_bonus = {
            '明确上升': 15,
            '中期上升': 10,
            '震荡整理': 0,
            '中期下降': -10,
            '明确下降': -15
        }
        score += trend_bonus.get(trend['direction'], 0)
        
        # 均线排列加分
        ma_bonus = {
            '多头排列': 10,
            '偏多排列': 5,
            '交叉震荡': 0,
            '空头排列': -10,
        }
        score += ma_bonus.get(ma['arrangement'], 0)
        
        # 指标加分
        indicator_bonus = {
            '多头信号': 10,
            '信号混杂': 0,
            '空头信号': -10
        }
        score += indicator_bonus.get(indicators['overall'], 0)
        
        # KDJ金叉/死叉额外加减
        if indicators['kdj_signal'] == '金叉':
            score += 5
        elif indicators['kdj_signal'] == '死叉':
            score -= 5
        
        # MACD金叉/死叉额外加减
        if indicators['macd_signal'] == '金叉':
            score += 5
        elif indicators['macd_signal'] == '死叉':
            score -= 5
        
        # 当前价格位置（在均线上方加分）
        current_price = ma['current_price']
        if current_price > ma['MA5']:
            score += 2
        if current_price > ma['MA20']:
            score += 3
        if current_price > ma['MA60']:
            score += 5
        
        # 限制分数范围
        return max(0, min(100, score))

    def analyze(self, symbol: str) -> Dict[str, Any]:
        """执行技术面分析"""
        self.log(f"开始技术面分析: {symbol}")

        result = {
            'symbol': symbol,
            'score': 0,
            'details': {},
            'ratings': {}
        }

        # 获取历史K线数据
        try:
            self.log("获取历史K线数据...")
            df = None
            
            # 先尝试 efinance
            if ef is not None:
                try:
                    df = ef.stock.get_quote_history(symbol)
                    if df is not None and not df.empty:
                        self.log(f"  ✓ efinance 获取 {len(df)} 条K线数据")
                except Exception as e:
                    self.log(f"  ✗ efinance 获取失败: {e}")
                    df = None
            
            # 如果efinance失败，尝试akshare
            if df is None or df.empty:
                try:
                    import akshare as ak
                    # akshare 需要处理市场前缀
                    if symbol.startswith('6'):
                        ak_symbol = f'sh{symbol}'
                    elif symbol.startswith('0') or symbol.startswith('3'):
                        ak_symbol = f'sz{symbol}'
                    else:
                        ak_symbol = symbol
                    
                    df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date="20200101", end_date="20500101", adjust="qfq")
                    # 重命名列以匹配efinance格式
                    df = df.rename(columns={
                        '日期': '日期',
                        '开盘': '开盘',
                        '最高': '最高',
                        '最低': '最低',
                        '收盘': '收盘',
                        '成交量': '成交量',
                    })
                    if df is not None and not df.empty:
                        self.log(f"  ✓ akshare 获取 {len(df)} 条K线数据")
                except Exception as e:
                    self.log(f"  ✗ akshare 获取失败: {e}")
                    df = None
            
            if df is None or df.empty:
                raise ValueError("所有数据源获取K线数据均失败")
            
            # 确保数据按日期排序
            df = df.sort_values('日期').reset_index(drop=True)
            
            # 计算均线
            self.log("计算均线系统...")
            ma_result = self.calculate_ma(df, [5, 10, 20, 60])
            result['details']['moving_average'] = ma_result
            
            # 趋势分析
            self.log("趋势分析...")
            trend_result = self.analyze_trend(df, ma_result)
            result['details']['trend'] = trend_result
            
            # 计算技术指标
            self.log("计算KDJ指标...")
            kdj_result = self.calculate_kdj(df)
            result['details']['kdj'] = kdj_result
            
            self.log("计算RSI指标...")
            rsi_result = self.calculate_rsi(df, 14)
            result['details']['rsi'] = rsi_result
            
            self.log("计算MACD指标...")
            macd_result = self.calculate_macd(df)
            result['details']['macd'] = macd_result
            
            # 支撑压力位
            self.log("识别支撑位和压力位...")
            sr_result = self.find_support_resistance(df, 60)
            result['details']['support_resistance'] = sr_result
            
            # 综合指标分析
            self.log("综合指标分析...")
            indicator_result = self.analyze_indicators(kdj_result, rsi_result, macd_result)
            result['details']['indicators'] = indicator_result
            
            # 计算最终得分
            self.log("计算技术面综合得分...")
            final_score = self.calculate_score(trend_result, ma_result, indicator_result, sr_result)
            result['score'] = final_score
            
            # 资金流向（占位，后续可扩展）
            result['details']['fund_flow'] = {
                'main_inflow': None,
                'main_outflow': None,
                'net_flow': None,
                'rating': '暂无数据'
            }
            
            self.log(f"技术面分析完成，得分: {final_score}/100")
            
        except Exception as e:
            self.log(f"技术面分析出错: {e}")
            result['errors'] = [str(e)]
            result['score'] = 0
            
        return result
