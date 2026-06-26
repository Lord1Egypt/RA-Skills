#!/usr/bin/env python3
"""
A股K线图分析器 v1.0.4 - 超详细结构化报告
功能：获取K线数据、计算技术指标、生成超详细分析报告
"""

import argparse
import json
import sys
import requests
import time
from datetime import datetime, timedelta

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle
    PLOTTING_AVAILABLE = True
except ImportError as e:
    print(f"警告：部分依赖未安装: {e}")
    PLOTTING_AVAILABLE = False


class SinaFinanceAPI:
    """新浪财经API封装 - 实时价格"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://finance.sina.com.cn',
            'Connection': 'keep-alive',
        })
    
    def _get_sina_code(self, code: str) -> str:
        """转换为新浪股票代码格式"""
        code = code.strip()
        if code.startswith(('6', '688')):
            return f"sh{code}"
        elif code.startswith(('0', '3')):
            return f"sz{code}"
        elif code.startswith(('4', '8')):
            return f"bj{code}"
        else:
            return f"sz{code}"
    
    def get_realtime_price(self, code: str) -> dict:
        """获取实时价格"""
        time.sleep(0.3)
        try:
            sina_code = self._get_sina_code(code)
            url = f'https://hq.sinajs.cn/list={sina_code}'
            response = self.session.get(url, timeout=10)
            
            if response.status_code != 200:
                return None
            
            content = response.text
            if not content or '=""' in content:
                return None
            
            data_str = content.split('="')[1].split('"')[0]
            parts = data_str.split(',')
            
            if len(parts) < 33:
                return None
            
            return {
                'code': code,
                'name': parts[0],
                'open': float(parts[1]),
                'prev_close': float(parts[2]),
                'price': float(parts[3]),
                'high': float(parts[4]),
                'low': float(parts[5]),
                'volume': int(parts[8]),
                'amount': float(parts[9]),
                'change': float(parts[3]) - float(parts[2]),
                'change_pct': (float(parts[3]) - float(parts[2])) / float(parts[2]) * 100 if float(parts[2]) > 0 else 0,
                'time': f"{parts[30]} {parts[31]}",
            }
        except Exception as e:
            print(f"获取实时价格失败: {e}")
            return None


class BaostockAPI:
    """Baostock API封装 - K线数据"""
    
    def __init__(self):
        self.bs = None
        self._login()
    
    def _login(self):
        """登录Baostock"""
        try:
            import baostock as bs
            self.bs = bs
            lg = bs.login()
            if lg.error_code != '0':
                print(f"Baostock登录失败: {lg.error_msg}")
        except ImportError:
            print("Baostock未安装，请运行: pip3 install baostock")
    
    def _get_bs_code(self, code: str) -> str:
        """转换为Baostock代码格式"""
        code = code.strip()
        if code.startswith(('6', '688')):
            return f"sh.{code}"
        elif code.startswith(('0', '3')):
            return f"sz.{code}"
        else:
            return f"sz.{code}"
    
    def get_kline_data(self, code: str, period: str = "daily", days: int = 60) -> pd.DataFrame:
        """获取K线数据"""
        if not self.bs:
            print("Baostock未初始化")
            return None
        
        try:
            bs_code = self._get_bs_code(code)
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=days*2)).strftime('%Y-%m-%d')
            
            freq_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm'}
            freq = freq_map.get(period, 'd')
            
            rs = self.bs.query_history_k_data_plus(
                bs_code,
                "date,code,open,high,low,close,preclose,volume,amount,turn,pctChg",
                start_date=start_date, end_date=end_date, frequency=freq, adjustflag="3"
            )
            
            if rs.error_code != '0':
                print(f"获取K线数据失败: {rs.error_msg}")
                return None
            
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
            
            if not data_list:
                return None
            
            df = pd.DataFrame(data_list, columns=rs.fields)
            
            numeric_cols = ['open', 'high', 'low', 'close', 'preclose', 'volume', 'amount', 'turn', 'pctChg']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            df = df.tail(days).reset_index(drop=True)
            return df
            
        except Exception as e:
            print(f"获取K线数据异常: {e}")
            return None
    
    def __del__(self):
        if self.bs:
            try:
                self.bs.logout()
                print("logout success!")
            except:
                pass


class StockDataSource:
    """股票数据源统一接口"""
    
    def __init__(self):
        self.sina = SinaFinanceAPI()
        self.baostock = BaostockAPI()
    
    def get_realtime_price(self, code: str) -> dict:
        return self.sina.get_realtime_price(code)
    
    def get_kline_data(self, code: str, period: str = "daily", days: int = 60) -> pd.DataFrame:
        return self.baostock.get_kline_data(code, period, days)


def calculate_ma(df: pd.DataFrame, periods: list = [5, 10, 20, 60]) -> pd.DataFrame:
    """计算移动平均线"""
    for period in periods:
        df[f'MA{period}'] = df['close'].rolling(window=period).mean()
    return df


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """计算MACD"""
    ema_fast = df['close'].ewm(span=fast).mean()
    ema_slow = df['close'].ewm(span=slow).mean()
    df['MACD'] = ema_fast - ema_slow
    df['MACD_Signal'] = df['MACD'].ewm(span=signal).mean()
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    return df


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """计算RSI"""
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df


def calculate_bollinger(df: pd.DataFrame, period: int = 20, std: int = 2) -> pd.DataFrame:
    """计算布林带"""
    df['BOLL_MID'] = df['close'].rolling(window=period).mean()
    rolling_std = df['close'].rolling(window=period).std()
    df['BOLL_UP'] = df['BOLL_MID'] + (rolling_std * std)
    df['BOLL_DOWN'] = df['BOLL_MID'] - (rolling_std * std)
    df['BOLL_WIDTH'] = (df['BOLL_UP'] - df['BOLL_DOWN']) / df['BOLL_MID'] * 100
    return df


def calculate_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """计算波动率"""
    df['Daily_Return'] = df['close'].pct_change()
    df['Volatility_20'] = df['Daily_Return'].rolling(window=20).std() * (252 ** 0.5) * 100
    return df


def identify_patterns(df: pd.DataFrame) -> list:
    """识别K线形态"""
    patterns = []
    
    for i in range(1, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        
        body = abs(row['close'] - row['open'])
        upper_shadow = row['high'] - max(row['close'], row['open'])
        lower_shadow = min(row['close'], row['open']) - row['low']
        total_range = row['high'] - row['low']
        
        if total_range == 0:
            continue
        
        # 锤子线
        if lower_shadow > body * 2 and upper_shadow < body * 0.5 and body > 0:
            patterns.append({
                'date': row['date'],
                'pattern': '锤子线',
                'signal': '看涨',
                'price': row['close'],
                'reliability': '⭐⭐⭐',
                'explanation': '下影线长，表示下方支撑强，可能反弹'
            })
        
        # 倒锤子
        elif upper_shadow > body * 2 and lower_shadow < body * 0.5 and body > 0:
            patterns.append({
                'date': row['date'],
                'pattern': '倒锤子',
                'signal': '看跌',
                'price': row['close'],
                'reliability': '⭐⭐⭐',
                'explanation': '上影线长，表示上方压力大，可能回落'
            })
        
        # 十字星
        elif body < total_range * 0.1 and total_range > 0:
            patterns.append({
                'date': row['date'],
                'pattern': '十字星',
                'signal': '反转信号',
                'price': row['close'],
                'reliability': '⭐⭐',
                'explanation': '多空力量均衡，可能变盘'
            })
        
        # 看涨吞没
        if (prev_row['close'] < prev_row['open'] and
            row['close'] > row['open'] and
            row['open'] < prev_row['close'] and
            row['close'] > prev_row['open']):
            patterns.append({
                'date': row['date'],
                'pattern': '看涨吞没',
                'signal': '强烈看涨',
                'price': row['close'],
                'reliability': '⭐⭐⭐⭐',
                'explanation': '阳线包阴线，多头反攻，趋势反转'
            })
        
        # 看跌吞没
        elif (prev_row['close'] > prev_row['open'] and
              row['close'] < row['open'] and
              row['open'] > prev_row['close'] and
              row['close'] < prev_row['open']):
            patterns.append({
                'date': row['date'],
                'pattern': '看跌吞没',
                'signal': '强烈看跌',
                'price': row['close'],
                'reliability': '⭐⭐⭐⭐',
                'explanation': '阴线包阳线，空头反攻，趋势反转'
            })
    
    return patterns[-10:]


def generate_detailed_report(df, patterns, realtime_data, stock_code):
    """生成超详细技术分析报告 v1.0.4"""
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # 计算近期统计
    recent_5d = df.tail(5)
    recent_20d = df.tail(20)
    avg_volume_5d = recent_5d['volume'].mean()
    avg_volume_20d = recent_20d['volume'].mean()
    volume_ratio = avg_volume_5d / avg_volume_20d if avg_volume_20d > 0 else 1
    
    if realtime_data:
        current_price = realtime_data['price']
        change_pct = realtime_data['change_pct']
        change = realtime_data['change']
        stock_name = realtime_data.get('name', '')
        turnover_rate = realtime_data.get('turnover', 0)
    else:
        current_price = latest['close']
        change_pct = latest['change_pct']
        change = latest['change_pct'] / 100 * latest['preclose'] if latest['preclose'] else 0
        stock_name = ''
        turnover_rate = latest.get('turn', 0)
    
    # 计算信号
    signals = []
    signal_weights = []
    
    # MA信号
    ma_signals = []
    if 'MA5' in df.columns and not pd.isna(latest['MA5']):
        ma5_trend = "上升" if len(df) >= 5 and latest['MA5'] > df.iloc[-5]['MA5'] else "下降"
        if current_price > latest['MA5']:
            ma_signals.append(("MA5支撑", 0.5, f"股价({current_price:.2f})>MA5({latest['MA5']:.2f})，短期支撑有效"))
        else:
            ma_signals.append(("MA5压力", -0.5, f"股价({current_price:.2f})<MA5({latest['MA5']:.2f})，短期承压"))
    
    if 'MA20' in df.columns and not pd.isna(latest['MA20']):
        if current_price > latest['MA20']:
            ma_signals.append(("MA20支撑", 0.5, f"股价在中期均线上方，中期趋势向好"))
        else:
            ma_signals.append(("MA20压力", -0.5, f"股价在中期均线下方，中期趋势走弱"))
    
    if 'MA5' in df.columns and 'MA10' in df.columns and 'MA20' in df.columns:
        if latest['MA5'] > latest['MA10'] > latest['MA20']:
            signals.append(("均线多头排列", 1.5, "MA5>MA10>MA20，上升趋势确立，均线呈多头排列"))
            signal_weights.append(1.5)
        elif latest['MA5'] < latest['MA10'] < latest['MA20']:
            signals.append(("均线空头排列", -1.5, "MA5<MA10<MA20，下降趋势确立，均线呈空头排列"))
            signal_weights.append(-1.5)
        elif latest['MA5'] > latest['MA10'] and latest['MA10'] < latest['MA20']:
            signals.append(("均线金叉", 0.5, "MA5上穿MA10，短期趋势转好"))
            signal_weights.append(0.5)
        elif latest['MA5'] < latest['MA10'] and latest['MA10'] > latest['MA20']:
            signals.append(("均线死叉", -0.5, "MA5下穿MA10，短期趋势转弱"))
            signal_weights.append(-0.5)
    
    signals.extend(ma_signals)
    for s in ma_signals:
        signal_weights.append(s[1])
    
    # RSI信号
    if 'RSI' in df.columns:
        rsi = latest['RSI']
        rsi_prev = df.iloc[-2]['RSI'] if len(df) > 1 else rsi
        rsi_trend = "上升" if rsi > rsi_prev else "下降"
        
        if rsi < 20:
            signals.append(("RSI极度超卖", 1.5, f"RSI={rsi:.1f}<20，极度超卖，强烈反弹信号，趋势{rsi_trend}"))
            signal_weights.append(1.5)
        elif rsi < 30:
            signals.append(("RSI超卖", 1, f"RSI={rsi:.1f}<30，超卖区域，存在反弹机会，趋势{rsi_trend}"))
            signal_weights.append(1)
        elif rsi > 80:
            signals.append(("RSI极度超买", -1.5, f"RSI={rsi:.1f}>80，极度超买，强烈回调风险，趋势{rsi_trend}"))
            signal_weights.append(-1.5)
        elif rsi > 70:
            signals.append(("RSI超买", -1, f"RSI={rsi:.1f}>70，超买区域，注意回调风险，趋势{rsi_trend}"))
            signal_weights.append(-1)
        elif 50 < rsi <= 70:
            signals.append(("RSI强势", 0.5, f"RSI={rsi:.1f}，健康强势区，买方占优，趋势{rsi_trend}"))
            signal_weights.append(0.5)
        elif 30 <= rsi < 50:
            signals.append(("RSI弱势", -0.5, f"RSI={rsi:.1f}，偏弱区域，卖方占优，趋势{rsi_trend}"))
            signal_weights.append(-0.5)
    
    # MACD信号
    if 'MACD' in df.columns:
        macd_val = latest['MACD']
        signal_val = latest['MACD_Signal']
        hist_val = latest['MACD_Hist']
        hist_prev = df.iloc[-2]['MACD_Hist'] if len(df) > 1 else hist_val
        
        # 判断金叉/死叉
        if macd_val > signal_val:
            if df.iloc[-2]['MACD'] <= df.iloc[-2]['MACD_Signal'] if len(df) > 1 else False:
                signals.append(("MACD金叉", 1.5, f"DIF({macd_val:.3f})刚刚上穿DEA({signal_val:.3f})，金叉确立，买入信号强烈"))
                signal_weights.append(1.5)
            else:
                signals.append(("MACD金叉延续", 1, f"DIF({macd_val:.3f})>DEA({signal_val:.3f})，金叉延续，动能{'增强' if hist_val > hist_prev else '减弱'}"))
                signal_weights.append(1)
        else:
            if df.iloc[-2]['MACD'] >= df.iloc[-2]['MACD_Signal'] if len(df) > 1 else False:
                signals.append(("MACD死叉", -1.5, f"DIF({macd_val:.3f})刚刚下穿DEA({signal_val:.3f})，死叉确立，卖出信号强烈"))
                signal_weights.append(-1.5)
            else:
                signals.append(("MACD死叉延续", -1, f"DIF({macd_val:.3f})<DEA({signal_val:.3f})，死叉延续，动能{'增强' if hist_val < hist_prev else '减弱'}"))
                signal_weights.append(-1)
        
        # 柱状图判断
        if hist_val > 0 and hist_val > hist_prev:
            signals.append(("MACD红柱扩大", 0.5, "柱状图正值扩大，上涨动能增强"))
            signal_weights.append(0.5)
        elif hist_val < 0 and hist_val < hist_prev:
            signals.append(("MACD绿柱扩大", -0.5, "柱状图负值扩大，下跌动能增强"))
            signal_weights.append(-0.5)
    
    # 布林带信号
    if 'BOLL_UP' in df.columns:
        boll_width = latest.get('BOLL_WIDTH', 0)
        if current_price > latest['BOLL_UP']:
            signals.append(("突破布林上轨", -1, f"股价({current_price:.2f})突破上轨({latest['BOLL_UP']:.2f})，超买严重，可能回调，带宽{boll_width:.1f}%"))
            signal_weights.append(-1)
        elif current_price < latest['BOLL_DOWN']:
            signals.append(("跌破布林下轨", 1, f"股价({current_price:.2f})跌破下轨({latest['BOLL_DOWN']:.2f})，超卖严重，可能反弹，带宽{boll_width:.1f}%"))
            signal_weights.append(1)
        elif current_price > latest['BOLL_MID']:
            distance = (current_price - latest['BOLL_MID']) / (latest['BOLL_UP'] - latest['BOLL_MID']) * 100
            signals.append(("布林中上", 0.3, f"股价在中轨上方，偏强势，距离上轨{distance:.1f}%，带宽{boll_width:.1f}%"))
            signal_weights.append(0.3)
        else:
            distance = (latest['BOLL_MID'] - current_price) / (latest['BOLL_MID'] - latest['BOLL_DOWN']) * 100
            signals.append(("布林中下", -0.3, f"股价在中轨下方，偏弱势，距离下轨{distance:.1f}%，带宽{boll_width:.1f}%"))
            signal_weights.append(-0.3)
    
    # K线形态信号
    if patterns:
        last_pattern = patterns[-1]
        if last_pattern['signal'] in ['强烈看涨']:
            signals.append((last_pattern['pattern'], 1.5, f"{last_pattern['explanation']}，可靠性{last_pattern['reliability']}"))
            signal_weights.append(1.5)
        elif last_pattern['signal'] in ['看涨']:
            signals.append((last_pattern['pattern'], 1, f"{last_pattern['explanation']}，可靠性{last_pattern['reliability']}"))
            signal_weights.append(1)
        elif last_pattern['signal'] in ['强烈看跌']:
            signals.append((last_pattern['pattern'], -1.5, f"{last_pattern['explanation']}，可靠性{last_pattern['reliability']}"))
            signal_weights.append(-1.5)
        elif last_pattern['signal'] in ['看跌']:
            signals.append((last_pattern['pattern'], -1, f"{last_pattern['explanation']}，可靠性{last_pattern['reliability']}"))
            signal_weights.append(-1)
        elif last_pattern['signal'] in ['反转信号']:
            signals.append((last_pattern['pattern'], 0.5, f"{last_pattern['explanation']}，需结合趋势判断，可靠性{last_pattern['reliability']}"))
            signal_weights.append(0.5)
    
    # 成交量信号
    if volume_ratio > 1.5:
        signals.append(("放量", 0.5 if change_pct > 0 else -0.5, f"近5日均量/20日均量={volume_ratio:.2f}，{'放量上涨，资金流入' if change_pct > 0 else '放量下跌，资金出逃'}"))
        signal_weights.append(0.5 if change_pct > 0 else -0.5)
    elif volume_ratio < 0.7:
        signals.append(("缩量", 0.3 if change_pct < 0 else -0.3, f"近5日均量/20日均量={volume_ratio:.2f}，{'缩量下跌，抛压减轻' if change_pct < 0 else '缩量上涨，上涨乏力'}"))
        signal_weights.append(0.3 if change_pct < 0 else -0.3)
    
    total_score = sum(signal_weights)
    
    # 判断结论
    if total_score >= 4:
        conclusion = "🟢 强烈看多"
        conclusion_desc = "多项指标共振向上，买入时机较好"
        probability = "80%"
        suggestion = "强烈看多 - 可考虑加仓或买入"
    elif total_score >= 2:
        conclusion = "🟡 偏多"
        conclusion_desc = "多数指标显示积极信号，趋势向好"
        probability = "65%"
        suggestion = "偏多 - 可持有或轻仓关注"
    elif total_score >= 0.5:
        conclusion = "🟡 温和偏多"
        conclusion_desc = "部分指标向好，但力度不强"
        probability = "55%"
        suggestion = "温和偏多 - 观望或轻仓"
    elif total_score <= -4:
        conclusion = "🔴 强烈看空"
        conclusion_desc = "多项指标共振向下，卖出信号强烈"
        probability = "80%"
        suggestion = "强烈看空 - 建议减仓或清仓"
    elif total_score <= -2:
        conclusion = "🟠 偏空"
        conclusion_desc = "多数指标显示消极信号，趋势走弱"
        probability = "65%"
        suggestion = "偏空 - 谨慎操作，控制仓位"
    elif total_score <= -0.5:
        conclusion = "🟠 温和偏空"
        conclusion_desc = "部分指标走弱，需警惕"
        probability = "55%"
        suggestion = "温和偏空 - 观望为主"
    else:
        conclusion = "⚪ 中性"
        conclusion_desc = "多空力量均衡，方向不明"
        probability = "50%"
        suggestion = "中性 - 观望为主，等待方向明确"
    
    # 生成超详细报告
    report = f"""
{'='*70}
📊 {stock_code} {stock_name} 技术分析报告 (v1.0.4 超详细版)
{'='*70}
分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【一、实时行情概览】
┌─────────────────────────────────────────────────────────────────────┐
│ 最新价: {current_price:>8.2f} 元  │  涨跌幅: {change_pct:>+7.2f}%  │  涨跌额: {change:>+7.2f}元  │
│ 开盘价: {realtime_data['open'] if realtime_data else latest['open']:>8.2f} 元  │  最高价: {realtime_data['high'] if realtime_data else latest['high']:>8.2f} 元  │  最低价: {realtime_data['low'] if realtime_data else latest['low']:>8.2f} 元  │
│ 昨收价: {realtime_data['prev_close'] if realtime_data else latest['preclose']:>8.2f} 元  │  成交量: {(realtime_data['volume']/10000 if realtime_data else latest['volume']/10000):>8.2f}万手  │  成交额: {(realtime_data['amount']/10000 if realtime_data else latest['amount']/10000):>8.2f}万元  │
│ 换手率: {turnover_rate:>8.2f}%     │  量比: {volume_ratio:>8.2f}      │  更新: {realtime_data['time'] if realtime_data else 'N/A':>15}  │
└─────────────────────────────────────────────────────────────────────┘

【二、趋势指标详解】

2.1 移动平均线 (MA) - Moving Average
─────────────────────────────────────────────────────────────────────
定义: 一段时间内收盘价的平均值，反映市场平均持仓成本，判断趋势方向
计算公式: MA(n) = (P1 + P2 + ... + Pn) / n

┌────────┬──────────┬──────────┬──────────┬─────────────────────────────────────┐
│  均线  │   数值   │ 股价位置 │  趋势    │              判断说明                │
├────────┼──────────┼──────────┼──────────┼─────────────────────────────────────┤"""
    
    # 添加MA详细数据
    for ma in ['MA5', 'MA10', 'MA20', 'MA60']:
        if ma in df.columns and not pd.isna(latest[ma]):
            position = "上方📈" if current_price > latest[ma] else "下方📉"
            ma_change = latest[ma] - df.iloc[-5][ma] if len(df) >= 5 and not pd.isna(df.iloc[-5][ma]) else 0
            trend = "↗️上升" if ma_change > 0 else "↘️下降" if ma_change < 0 else "➡️走平"
            trend_pct = (ma_change / latest[ma] * 100) if latest[ma] != 0 else 0
            
            if ma == 'MA5':
                desc = "短期趋势" + ("向上" if ma_change > 0 else "向下" if ma_change < 0 else "走平")
            elif ma == 'MA10':
                desc = "中短期趋势" + ("向好" if ma_change > 0 else "走弱" if ma_change < 0 else "震荡")
            elif ma == 'MA20':
                desc = "中期趋势" + ("向上" if ma_change > 0 else "向下" if ma_change < 0 else "盘整")
            else:
                desc = "长期趋势" + ("向好" if ma_change > 0 else "走弱" if ma_change < 0 else "平稳")
            
            report += f"\n│ {ma:>6} │ {latest[ma]:>8.2f} │ {position:>8} │ {trend:>8} │ {desc}({trend_pct:+.2f}%) │"
    
    report += "\n└────────┴──────────┴──────────┴──────────┴─────────────────────────────────────┘"
    
    # 均线排列详细判断
    report += "\n\n均线排列判断:\n"
    if 'MA5' in df.columns and 'MA10' in df.columns and 'MA20' in df.columns:
        ma5, ma10, ma20 = latest['MA5'], latest['MA10'], latest['MA20']
        
        if ma5 > ma10 > ma20:
            report += f"""
✅ 多头排列 (MA5:{ma5:.2f} > MA10:{ma10:.2f} > MA20:{ma20:.2f})
   含义: 短期均线在长期均线上方，呈多头排列
   判断: 上升趋势确立，市场处于强势状态
   操作: 持股待涨，回调至短期均线可考虑加仓
"""
        elif ma5 < ma10 < ma20:
            report += f"""
❌ 空头排列 (MA5:{ma5:.2f} < MA10:{ma10:.2f} < MA20:{ma20:.2f})
   含义: 短期均线在长期均线下方，呈空头排列
   判断: 下降趋势确立，市场处于弱势状态
   操作: 观望为主，等待趋势反转信号
"""
        elif ma5 > ma10 and ma10 < ma20:
            report += f"""
➖ 均线金叉 (MA5:{ma5:.2f} > MA10:{ma10:.2f}, MA10 < MA20:{ma20:.2f})
   含义: 短期均线上穿中期均线，中期均线仍向下
   判断: 短期趋势转好，但中期仍承压
   操作: 谨慎乐观，关注能否突破中期均线
"""
        elif ma5 < ma10 and ma10 > ma20:
            report += f"""
➖ 均线死叉 (MA5:{ma5:.2f} < MA10:{ma10:.2f}, MA10 > MA20:{ma20:.2f})
   含义: 短期均线下穿中期均线，中期均线仍向上
   判断: 短期趋势转弱，但中期仍有支撑
   操作: 警惕回调风险，关注中期均线支撑
"""
        else:
            report += f"""
➖ 均线纠缠 (MA5:{ma5:.2f}, MA10:{ma10:.2f}, MA20:{ma20:.2f})
   含义: 各均线相互缠绕，方向不明
   判断: 市场处于震荡整理阶段
   操作: 观望为主，等待方向明确
"""
    
    # MACD详细分析
    if 'MACD' in df.columns:
        macd_val = latest['MACD']
        signal_val = latest['MACD_Signal']
        hist_val = latest['MACD_Hist']
        hist_prev = df.iloc[-2]['MACD_Hist'] if len(df) > 1 else hist_val
        
        report += f"""
2.2 MACD（指数平滑异同平均线）- Moving Average Convergence Divergence
─────────────────────────────────────────────────────────────────────
定义: 通过计算两条不同周期的指数平滑移动平均线(EMA)的差值，判断趋势转折和动能
计算公式: 
  - DIF = EMA(12) - EMA(26)  [快线]
  - DEA = EMA(DIF, 9)        [慢线/信号线]
  - MACD柱 = (DIF - DEA) × 2  [柱状图]

┌────────────┬──────────┬────────────────────────────────────────────────────┐
│    指标    │   数值   │                      说明                          │
├────────────┼──────────┼────────────────────────────────────────────────────┤
│ DIF(快线)  │ {macd_val:>8.3f} │ 12日EMA - 26日EMA，反映短期趋势                   │
│ DEA(慢线)  │ {signal_val:>8.3f} │ DIF的9日EMA，反映中期趋势                         │
│ MACD柱     │ {hist_val:>8.3f} │ (DIF-DEA)×2，正值红色(多头)，负值绿色(空头)      │
│ 柱变化     │ {(hist_val-hist_prev):>+8.3f} │ 较上一周期变化，正值扩大/负值缩小                 │
└────────────┴──────────┴────────────────────────────────────────────────────┘

MACD信号判断:
"""
        if macd_val > signal_val:
            if df.iloc[-2]['MACD'] <= df.iloc[-2]['MACD_Signal'] if len(df) > 1 else False:
                report += f"""
✅ 金叉信号 (DIF:{macd_val:.3f} 刚刚上穿 DEA:{signal_val:.3f})
   含义: 快线自下而上穿越慢线，短期动能转强
   可靠性: ⭐⭐⭐⭐ 较强买入信号
   判断: 趋势由弱转强，可考虑建仓或加仓
   注意: 需结合成交量和其他指标确认
"""
            else:
                hist_change = "扩大" if hist_val > hist_prev else "缩小"
                report += f"""
✅ 金叉延续 (DIF:{macd_val:.3f} > DEA:{signal_val:.3f})
   含义: 快线持续在慢线上方，多头趋势延续
   动能: 柱状图{hist_change}({'增强' if hist_val > hist_prev else '减弱'})
   判断: 上升趋势持续，{'动能增强，可继续持有' if hist_val > hist_prev else '动能减弱，注意回调风险'}
   操作: {'持股待涨' if hist_val > hist_prev else '适当减仓锁定利润'}
"""
        else:
            if df.iloc[-2]['MACD'] >= df.iloc[-2]['MACD_Signal'] if len(df) > 1 else False:
                report += f"""
❌ 死叉信号 (DIF:{macd_val:.3f} 刚刚下穿 DEA:{signal_val:.3f})
   含义: 快线自上而下穿越慢线，短期动能转弱
   可靠性: ⭐⭐⭐⭐ 较强卖出信号
   判断: 趋势由强转弱，应考虑减仓或清仓
   注意: 需结合成交量和其他指标确认
"""
            else:
                hist_change = "扩大" if hist_val < hist_prev else "缩小"
                report += f"""
❌ 死叉延续 (DIF:{macd_val:.3f} < DEA:{signal_val:.3f})
   含义: 快线持续在慢线下方，空头趋势延续
   动能: 柱状图{hist_change}({'增强' if hist_val < hist_prev else '减弱'})
   判断: 下降趋势持续，{'动能增强，继续观望' if hist_val < hist_prev else '动能减弱，可能企稳'}
   操作: {'空仓观望' if hist_val < hist_prev else '关注企稳信号'}
"""
    
    # RSI详细分析
    if 'RSI' in df.columns:
        rsi = latest['RSI']
        rsi_prev = df.iloc[-2]['RSI'] if len(df) > 1 else rsi
        rsi_change = rsi - rsi_prev
        
        report += f"""
【三、强弱指标详解】

3.1 RSI（相对强弱指标）- Relative Strength Index
─────────────────────────────────────────────────────────────────────
定义: 通过比较一段时间内股价上涨和下跌的幅度，衡量买卖双方力量对比
计算公式: RSI = 100 - (100 / (1 + RS))，其中 RS = 平均涨幅 / 平均跌幅
参数: 周期14日（常用），也可使用6日或12日

┌──────────┬──────────┬──────────┬────────────────────────────────────────────┐
│ RSI数值  │   状态   │  变化    │                  判断说明                   │
├──────────┼──────────┼──────────┼────────────────────────────────────────────┤
│ {rsi:>8.1f} │"""
        
        if rsi > 80:
            status = "极度超买"
            emoji = "⚠️⚠️"
        elif rsi > 70:
            status = "超买"
            emoji = "⚠️"
        elif rsi > 50:
            status = "强势"
            emoji = "📈"
        elif rsi > 30:
            status = "弱势"
            emoji = "📉"
        elif rsi > 20:
            status = "超卖"
            emoji = "💡"
        else:
            status = "极度超卖"
            emoji = "💡💡"
        
        trend = "↗️上升" if rsi_change > 0 else "↘️下降" if rsi_change < 0 else "➡️持平"
        
        report += f" {status:>8} {emoji} │ {trend:>8} │"
        
        if rsi > 80:
            report += " 买方力量极强，严重超买，随时可能大幅回调    │"
        elif rsi > 70:
            report += " 买方力量较强，超买区域，注意回调风险        │"
        elif rsi > 50:
            report += " 买方占优，健康强势区，可继续持有            │"
        elif rsi > 30:
            report += " 卖方占优，偏弱区域，观望或减仓              │"
        elif rsi > 20:
            report += " 卖方力量较强，超卖区域，存在反弹机会        │"
        else:
            report += " 卖方力量极强，严重超卖，随时可能大幅反弹    │"
        
        report += f"""
└──────────┴──────────┴──────────┴────────────────────────────────────────────┘

RSI区域划分与操作建议:
┌─────────────┬──────────┬─────────────────────┬─────────────────────────────┐
│    区域     │ RSI范围  │       含义          │           操作建议          │
├─────────────┼──────────┼─────────────────────┼─────────────────────────────┤
│ 极度超买区  │  > 80    │ 买方过度，严重超买  │ 减仓/观望，防范回调风险     │
│ 超买区      │ 70-80    │ 买方较强，可能回调  │ 适当减仓，锁定利润          │
│ 强势区      │ 50-70    │ 买方占优，趋势向好  │ 持有或逢低买入              │
│ 弱势区      │ 30-50    │ 卖方占优，趋势走弱  │ 观望或减仓                  │
│ 超卖区      │ 20-30    │ 卖方较强，可能反弹  │ 关注抄底机会                │
│ 极度超卖区  │  < 20    │ 卖方过度，严重超卖  │ 可考虑分批建仓              │
└─────────────┴──────────┴─────────────────────┴─────────────────────────────┘

当前RSI分析:
   RSI={rsi:.1f} 处于"""
        
        if rsi > 80:
            report += "极度超买区，强烈建议减仓"
        elif rsi > 70:
            report += "超买区，建议适当减仓"
        elif rsi > 50:
            report += "强势区，可继续持有"
        elif rsi > 30:
            report += "弱势区，建议观望"
        elif rsi > 20:
            report += "超卖区，可关注反弹"
        else:
            report += "极度超卖区，可考虑分批建仓"
        
        report += f"\n   较昨日变化: {rsi_change:+.1f} ({'增强' if rsi_change > 0 else '减弱' if rsi_change < 0 else '持平'})\n"
    
    # 布林带详细分析
    if 'BOLL_UP' in df.columns:
        boll_up = latest['BOLL_UP']
        boll_mid = latest['BOLL_MID']
        boll_down = latest['BOLL_DOWN']
        boll_width = latest.get('BOLL_WIDTH', (boll_up - boll_down) / boll_mid * 100)
        
        # 计算位置百分比
        if boll_up != boll_down:
            position_pct = (current_price - boll_down) / (boll_up - boll_down) * 100
        else:
            position_pct = 50
        
        report += f"""
【四、布林带详解】

4.1 BOLL（布林带）- Bollinger Bands
─────────────────────────────────────────────────────────────────────
定义: 由三条轨道线组成的通道，反映股价波动范围和相对高低位置
计算公式:
  - 中轨 = MA20 (20日移动平均线)
  - 上轨 = 中轨 + 2 × 标准差 (压力位)
  - 下轨 = 中轨 - 2 × 标准差 (支撑位)
  - 带宽 = (上轨 - 下轨) / 中轨 × 100% (波动率)

┌────────────┬──────────┬─────────────────────────────────────────────────────┐
│    轨道    │   数值   │                      说明                           │
├────────────┼──────────┼─────────────────────────────────────────────────────┤
│ 上轨(压力) │ {boll_up:>8.2f} │ 中轨+2倍标准差，股价触及可能回落                    │
│ 中轨(均线) │ {boll_mid:>8.2f} │ 20日均线，股价在此上方偏强，下方偏弱               │
│ 下轨(支撑) │ {boll_down:>8.2f} │ 中轨-2倍标准差，股价触及可能反弹                    │
│ 当前位置   │ {position_pct:>7.1f}%   │ 在布林带中的相对位置(0%=下轨, 100%=上轨)           │
│ 带宽       │ {boll_width:>7.1f}%   │ 波动率指标，>15%为高波动，<10%为低波动             │
└────────────┴──────────┴─────────────────────────────────────────────────────┘

布林带位置判断:
"""
        
        if current_price > boll_up:
            report += f"""
⚠️ 突破上轨 (股价:{current_price:.2f} > 上轨:{boll_up:.2f})
   含义: 股价突破布林带上轨，进入超买区域
   判断: 短期涨幅过大，可能面临回调压力
   操作: 考虑适当减仓，锁定利润
   注意: 强势行情中可能沿上轨运行，需结合成交量判断
"""
        elif current_price < boll_down:
            report += f"""
💡 跌破下轨 (股价:{current_price:.2f} < 下轨:{boll_down:.2f})
   含义: 股价跌破布林带下轨，进入超卖区域
   判断: 短期跌幅过大，可能存在反弹机会
   操作: 关注抄底机会，可分批建仓
   注意: 弱势行情中可能沿下轨运行，需等待企稳信号
"""
        elif current_price > boll_mid:
            distance_to_up = (boll_up - current_price) / (boll_up - boll_mid) * 100
            report += f"""
📈 中上区域 (中轨:{boll_mid:.2f} < 股价:{current_price:.2f} < 上轨:{boll_up:.2f})
   含义: 股价在中轨上方，处于强势区域
   位置: 距离上轨{distance_to_up:.1f}%，距离下轨{100-distance_to_up:.1f}%
   判断: 多头占优，趋势向好
   操作: 持股待涨，回调至中轨可考虑加仓
"""
        else:
            distance_to_down = (current_price - boll_down) / (boll_mid - boll_down) * 100
            report += f"""
📉 中下区域 (下轨:{boll_down:.2f} < 股价:{current_price:.2f} < 中轨:{boll_mid:.2f})
   含义: 股价在中轨下方，处于弱势区域
   位置: 距离上轨{100-distance_to_down:.1f}%，距离下轨{distance_to_down:.1f}%
   判断: 空头占优，趋势走弱
   操作: 观望为主，等待突破中轨或跌至下轨
"""
        
        # 带宽分析
        report += f"""
带宽分析 (当前带宽: {boll_width:.1f}%):
"""
        if boll_width > 15:
            report += f"""
🔴 高波动状态 (带宽 > 15%)
   含义: 市场波动剧烈，多空分歧大
   判断: 可能处于趋势末端或变盘前夕
   操作: 控制仓位，严格止损
"""
        elif boll_width < 10:
            report += f"""
🟡 低波动状态 (带宽 < 10%)
   含义: 市场波动收窄，多空力量均衡
   判断: 震荡整理，即将选择方向
   操作: 观望为主，等待突破信号
"""
        else:
            report += f"""
🟢 正常波动状态 (带宽 10%-15%)
   含义: 市场波动正常，趋势稳定
   判断: 当前趋势延续概率较大
   操作: 按趋势操作
"""
    
    # K线形态详细分析
    report += """
【五、K线形态详解】

5.1 近期形态识别
─────────────────────────────────────────────────────────────────────
定义: 通过单根或多根K线的组合形态，判断市场情绪和可能的转折点

┌────────────┬────────────┬──────────┬──────────┬──────────────────────────────┐
│    日期    │    形态    │   信号   │  可靠性  │           形态说明           │
├────────────┼────────────┼──────────┼──────────┼──────────────────────────────┤"""
    
    if patterns:
        for p in patterns[-5:]:
            report += f"\n│ {p['date']} │ {p['pattern']:>10} │ {p['signal']:>8} │ {p['reliability']:>8} │ {p['explanation'][:28]:<28} │"
    else:
        report += "\n│     -      │     无     │    -     │    -     │      近期未识别到明显形态      │"
    
    report += """
└────────────┴────────────┴──────────┴──────────┴──────────────────────────────┘

形态说明:
  - 锤子线: 下影线长，实体小，底部反转信号
  - 倒锤子: 上影线长，实体小，顶部反转信号
  - 十字星: 开盘价≈收盘价，多空均衡，变盘信号
  - 看涨吞没: 阳线包阴线，多头反攻，强烈看涨
  - 看跌吞没: 阴线包阳线，空头反攻，强烈看跌
"""
    
    # 成交量分析
    report += f"""
【六、成交量分析】

6.1 量能分析
─────────────────────────────────────────────────────────────────────
定义: 成交量反映市场参与度和资金流向，是价格变动的确认指标

┌─────────────────┬──────────────┬─────────────────────────────────────────────┐
│     指标        │     数值     │                   判断说明                  │
├─────────────────┼──────────────┼─────────────────────────────────────────────┤
│ 近5日平均成交量 │ {(avg_volume_5d/10000):>10.2f}万手 │ 短期平均成交水平                            │
│ 近20日平均成交量│ {(avg_volume_20d/10000):>10.2f}万手 │ 中期平均成交水平                            │
│ 量比            │ {volume_ratio:>10.2f}      │ 近5日/近20日，>1.5放量，<0.7缩量           │
│ 换手率          │ {turnover_rate:>10.2f}%      │ 今日成交股数/总股本，反映活跃度             │
└─────────────────┴──────────────┴─────────────────────────────────────────────┘

量能判断:
"""
    
    if volume_ratio > 1.5:
        if change_pct > 0:
            report += f"""
✅ 放量上涨 (量比: {volume_ratio:.2f})
   含义: 成交量较近期平均水平放大{((volume_ratio-1)*100):.0f}%，且股价上涨
   判断: 资金主动买入，上涨有量能支撑，可信度较高
   可靠性: ⭐⭐⭐⭐⭐
   操作: 积极看多，可考虑追涨
"""
        else:
            report += f"""
❌ 放量下跌 (量比: {volume_ratio:.2f})
   含义: 成交量较近期平均水平放大{((volume_ratio-1)*100):.0f}%，且股价下跌
   判断: 资金出逃，下跌有量能配合，调整可能持续
   可靠性: ⭐⭐⭐⭐
   操作: 谨慎看空，考虑减仓
"""
    elif volume_ratio < 0.7:
        if change_pct > 0:
            report += f"""
⚠️ 缩量上涨 (量比: {volume_ratio:.2f})
   含义: 成交量较近期平均水平缩小{((1-volume_ratio)*100):.0f}%，但股价上涨
   判断: 上涨缺乏量能支撑，可能是假突破或诱多
   可靠性: ⭐⭐
   操作: 警惕回调，不宜追高
"""
        else:
            report += f"""
🟡 缩量下跌 (量比: {volume_ratio:.2f})
   含义: 成交量较近期平均水平缩小{((1-volume_ratio)*100):.0f}%，且股价下跌
   判断: 抛压减轻，可能是洗盘或企稳信号
   可靠性: ⭐⭐⭐
   操作: 关注企稳信号，不宜盲目割肉
"""
    else:
        report += f"""
➖ 正常量能 (量比: {volume_ratio:.2f})
   含义: 成交量处于近期正常水平
   判断: 市场参与度正常，趋势延续概率较大
   可靠性: ⭐⭐⭐
   操作: 按技术指标操作
"""
    
    # 信号汇总
    report += """
【七、信号汇总与评分】

7.1 多空信号明细
─────────────────────────────────────────────────────────────────────
"""
    
    bullish_signals = [s for s in signals if s[1] > 0]
    bearish_signals = [s for s in signals if s[1] < 0]
    neutral_signals = [s for s in signals if s[1] == 0]
    
    if bullish_signals:
        report += "\n📈 看多信号:\n"
        for sig in bullish_signals:
            report += f"   ✅ {sig[0]:<15} (+{sig[1]:.1f}分) - {sig[2]}\n"
    
    if bearish_signals:
        report += "\n📉 看空信号:\n"
        for sig in bearish_signals:
            report += f"   ❌ {sig[0]:<15} ({sig[1]:.1f}分) - {sig[2]}\n"
    
    if neutral_signals:
        report += "\n➖ 中性信号:\n"
        for sig in neutral_signals:
            report += f"   ➖ {sig[0]:<15} ({sig[1]:.1f}分) - {sig[2]}\n"
    
    # 综合判断
    report += f"""
7.2 综合评分
─────────────────────────────────────────────────────────────────────
   看多信号: {len(bullish_signals)}个，总权重 +{sum(s[1] for s in bullish_signals):.1f}分
   看空信号: {len(bearish_signals)}个，总权重 {sum(s[1] for s in bearish_signals):.1f}分
   ─────────────────────────────
   技术评分: {total_score:+.1f}分 (评分范围: -5到+5)
   
   评分说明:
   - +4分以上: 强烈看多，多项指标共振向上
   - +2到+4分: 偏多，多数指标显示积极信号
   - 0到+2分: 温和偏多，部分指标向好
   - 0分左右: 中性，多空力量均衡
   - -2到0分: 温和偏空，部分指标走弱
   - -4到-2分: 偏空，多数指标显示消极信号
   - -4分以下: 强烈看空，多项指标共振向下

【八、综合判断与操作建议】

8.1 结论
─────────────────────────────────────────────────────────────────────
   综合判断: {conclusion}
   判断说明: {conclusion_desc}
   明日预测: {conclusion.replace('🟢', '').replace('🟡', '').replace('🟠', '').replace('🔴', '').replace('⚪', '').strip()}概率 {probability}

8.2 操作建议
─────────────────────────────────────────────────────────────────────
   {suggestion}

8.3 风险提示
─────────────────────────────────────────────────────────────────────
   ⚠️ 以上分析仅基于技术指标，不构成投资建议
   ⚠️ 技术分析有滞后性，不能预测突发事件
   ⚠️ 股市有风险，投资需谨慎
   ⚠️ 建议结合基本面分析和市场环境综合判断
   ⚠️ 设置止损位，控制单笔亏损在可承受范围内

{'='*70}
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='A股K线分析工具 v1.0.4 - 超详细结构化报告')
    parser.add_argument('--code', required=True, help='股票代码 (如: 600409)')
    parser.add_argument('--period', default='daily', choices=['daily', 'weekly', 'monthly'])
    parser.add_argument('--days', type=int, default=60, help='获取天数')
    parser.add_argument('--realtime', action='store_true', help='获取实时价格')
    parser.add_argument('--report', action='store_true', help='输出分析报告')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')
    
    args = parser.parse_args()
    
    api = StockDataSource()
    
    # 获取实时价格
    realtime_data = None
    if args.realtime or args.report:
        print(f"正在获取 {args.code} 实时价格...")
        realtime_data = api.get_realtime_price(args.code)
        if realtime_data:
            print(f"✓ 实时价格: {realtime_data['price']:.2f} ({realtime_data['change_pct']:+.2f}%)")
        else:
            print("✗ 获取实时价格失败")
    
    # 获取K线数据
    print(f"正在获取 {args.code} K线数据...")
    df = api.get_kline_data(args.code, args.period, args.days)
    
    if df is None or df.empty:
        print("✗ 获取K线数据失败")
        sys.exit(1)
    
    print(f"✓ 成功获取 {len(df)} 条K线数据")
    
    # 计算技术指标
    df = calculate_ma(df)
    df = calculate_macd(df)
    df = calculate_rsi(df)
    df = calculate_bollinger(df)
    df = calculate_volatility(df)
    
    # 识别形态
    patterns = identify_patterns(df)
    
    # 输出报告
    if args.report:
        print(generate_detailed_report(df, patterns, realtime_data, args.code))
    
    if args.json:
        result = {
            'code': args.code,
            'realtime': realtime_data,
            'data': df.to_dict('records'),
            'patterns': patterns,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    
    if not args.report and not args.json:
        latest = df.iloc[-1]
        print(f"\n股票: {args.code} {realtime_data.get('name', '') if realtime_data else ''}")
        print(f"最新价: {latest['close']:.2f}")
        if 'RSI' in df.columns:
            print(f"RSI: {latest['RSI']:.2f}")
        if 'MACD' in df.columns:
            print(f"MACD: {latest['MACD']:.3f}")


if __name__ == '__main__':
    main()
