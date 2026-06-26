#!/usr/bin/env python3
"""
ETF模拟交易回测系统
支持A股ETF日内交易策略的模拟交易与回测分析
"""

import json
import time
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple

# ==================== 配置 ====================
CONFIG = {
    "product_code": "560710",  # 船舶ETF
    "product_name": "富国中证智选船舶产业ETF",
    "initial_capital": 1_000_000,  # 初始资金100万
    "fee_buy": 0.00025,  # 买入手续费0.025%
    "fee_sell": 0.00025,  # 卖出手续费0.025%
    "stamp_duty": 0.001,  # 印花税0.1%
    "stop_loss": -0.05,  # 止损线-5%
    "take_profit": 0.08,  # 止盈线+8%
    "max_position": 1.0,  # 最大仓位100%
}

# ==================== 数据获取 ====================
def get_realtime_data(code: str) -> Optional[Dict]:
    """获取实时行情数据"""
    try:
        url = f"http://push2.eastmoney.com/api/qt/stock/get"
        params = {
            "ut": "fa5fd1943c7b386f172d6893dbfba10b",
            "invt": "2",
            "fltt": "2",
            "fields": "f43,f44,f45,f46,f47,f48,f49,f50,f51,f52,f55,f57,f58,f59,f60,f116,f117,f162,f167,f168,f169,f170,f171,f173,f177",
            "secid": f"1.{code}" if code.startswith('6') else f"0.{code}"
        }
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()
        if data.get('data'):
            return data['data']
    except Exception as e:
        print(f"获取数据失败: {e}")
    return None

def get_history_data(code: str, days: int = 60) -> List[Dict]:
    """获取历史K线数据（用于回测）"""
    try:
        url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            "secid": f"1.{code}" if code.startswith('6') else f"0.{code}",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87,f88,f89,f90,f91,f92,f93,f94,f95,f96,f97,f98,f99,f100,f101,f102,f103,f104,f105,f106,f107,f108,f109,f110,f111,f112,f113,f114,f115,f116,f117,f118,f119,f120,f121,f122,f123,f124,f125,f126,f127,f128,f129,f130,f131,f132,f133,f134,f135,f136,f137,f138,f139,f140,f141,f142,f143,f144,f145,f146,f147,f148,f149,f150,f151,f152,f153,f154,f155,f156,f157,f158,f159,f160,f161,f162,f163,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f193,f194,f195,f196,f197,f198,f199,f200,f201,f202,f203,f204,f205,f206,f207,f208,f209,f210,f211,f212,f213,f214,f215,f216,f217,f218,f219,f220,f221,f222,f223,f224,f225,f226,f227,f228,f229,f230,f231,f232,f233,f234,f235,f236,f237,f238,f239,f240,f241,f242,f243,f244,f245,f246,f247,f248,f249,f250,f251,f252",
            "klt": "101",  # 日K
            "fqt": "1",    # 前复权
            "end": "20500101",
            "lmt": days
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get('data') and data['data'].get('klines'):
            klines = data['data']['klines']
            result = []
            for line in klines:
                parts = line.split(',')
                result.append({
                    'date': parts[0],
                    'open': float(parts[1]),
                    'close': float(parts[2]),
                    'high': float(parts[3]),
                    'low': float(parts[4]),
                    'volume': float(parts[5]),
                })
            return result
    except Exception as e:
        print(f"获取历史数据失败: {e}")
    return []

# ==================== 技术指标 ====================
def calculate_ma(prices: List[float], period: int) -> List[float]:
    """计算移动平均线"""
    result = []
    for i in range(len(prices)):
        if i < period - 1:
            result.append(None)
        else:
            result.append(sum(prices[i-period+1:i+1]) / period)
    return result

def calculate_boll(prices: List[float], period: int = 20, std_dev: float = 2.0) -> Tuple[List[float], List[float], List[float]]:
    """计算布林带"""
    ma = calculate_ma(prices, period)
    upper = []
    lower = []
    
    for i in range(len(prices)):
        if i < period - 1:
            upper.append(None)
            lower.append(None)
        else:
            segment = prices[i-period+1:i+1]
            std = (sum((x - ma[i])**2 for x in segment) / period) ** 0.5
            upper.append(ma[i] + std_dev * std)
            lower.append(ma[i] - std_dev * std)
    
    return ma, upper, lower

def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[List[float], List[float], List[float]]:
    """计算MACD"""
    # EMA
    ema_fast = [prices[0]]
    ema_slow = [prices[0]]
    for p in prices[1:]:
        ema_fast.append(ema_fast[-1] * (fast-2)/(fast-1) + p * 2/(fast-1))
        ema_slow.append(ema_slow[-1] * (slow-2)/(slow-1) + p * 2/(slow-1))
    
    # DIF
    dif = [ema_fast[i] - ema_slow[i] for i in range(len(prices))]
    
    # DEA (signal line)
    dea = [dif[0]]
    for d in dif[1:]:
        dea.append(dea[-1] * (signal-1)/(signal+1) + d * 2/(signal+1))
    
    # MACD histogram
    hist = [dif[i] - dea[i] for i in range(len(prices))]
    
    return dif, dea, hist

def calculate_kdj(highs: List[float], lows: List[float], closes: List[float], period: int = 9) -> Tuple[List[float], List[float], List[float]]:
    """计算KDJ指标"""
    rsv = []
    for i in range(len(closes)):
        if i < period - 1:
            rsv.append(50.0)
        else:
            high_max = max(highs[i-period+1:i+1])
            low_min = min(lows[i-period+1:i+1])
            if high_max == low_min:
                rsv.append(50.0)
            else:
                rsv.append((closes[i] - low_min) / (high_max - low_min) * 100)
    
    k = [50.0]
    d = [50.0]
    j = [50.0]
    
    for i in range(1, len(rsv)):
        k.append(k[-1] * 2/3 + rsv[i] * 1/3)
        d.append(d[-1] * 2/3 + k[i] * 1/3)
        j.append(3 * k[i] - 2 * d[i])
    
    return k, d, j

# ==================== 信号判断 ====================
def generate_signals(data: List[Dict]) -> List[Dict]:
    """生成交易信号"""
    if len(data) < 30:
        return []
    
    closes = [d['close'] for d in data]
    highs = [d['high'] for d in data]
    lows = [d['low'] for d in data]
    volumes = [d['volume'] for d in data]
    
    ma20, upper, lower = calculate_boll(closes)
    dif, dea, hist = calculate_macd(closes)
    k, d, j = calculate_kdj(highs, lows, closes)
    
    signals = []
    for i in range(30, len(data)):
        date = data[i]['date']
        close = closes[i]
        vol = volumes[i]
        vol_yes = volumes[i-1] if i > 0 else vol
        vol_ratio = vol / vol_yes if vol_yes > 0 else 1.0
        
        signal = {'date': date, 'action': 'hold', 'reason': '', 'strength': 0}
        
        # 买入信号
        if j[i] < 20 and close <= lower[i] * 1.02:  # BOLL下轨+KDJ超卖
            signal['action'] = 'buy'
            signal['reason'] = 'BOLL下轨+KDJ超卖'
            signal['strength'] = 3
        elif close > ma20[i] and vol_ratio > 1.5 and dif[i] > dea[i]:  # 突破中轨+放量
            signal['action'] = 'buy'
            signal['reason'] = '突破中轨+放量'
            signal['strength'] = 3
        elif i > 0 and closes[i] < closes[i-1] and hist[i] > hist[i-1]:  # MACD底背离
            signal['action'] = 'buy'
            signal['reason'] = 'MACD底背离'
            signal['strength'] = 2
        
        # 卖出信号
        if j[i] > 80 and close >= upper[i] * 0.98:  # BOLL上轨+KDJ超买
            signal['action'] = 'sell'
            signal['reason'] = 'BOLL上轨+KDJ超买'
            signal['strength'] = 3
        elif dif[i] < dea[i] and j[i] > 70:  # 死叉
            signal['action'] = 'sell'
            signal['reason'] = 'MACD死叉+KDJ超买'
            signal['strength'] = 2
        
        signal['price'] = close
        signal['j'] = j[i]
        signal['boll_position'] = '下轨' if close < lower[i] else ('上轨' if close > upper[i] else '中轨')
        signal['volume_ratio'] = vol_ratio
        
        signals.append(signal)
    
    return signals

# ==================== 模拟交易 ====================
class SimulatedTrader:
    def __init__(self, config: Dict):
        self.config = config
        self.cash = config['initial_capital']
        self.position = 0
        self.position_price = 0
        self.trades = []
        self.holding_days = 0
    
    def buy(self, date: str, price: float, signal: Dict) -> bool:
        """买入"""
        # 计算可买数量（整手）
        max_shares = int(self.cash / price / 100) * 100
        if max_shares < 100:
            return False
        
        fee = price * max_shares * self.config['fee_buy']
        total_cost = price * max_shares + fee
        
        if total_cost > self.cash:
            max_shares = int((self.cash / (1 + self.config['fee_buy'])) / price / 100) * 100
            if max_shares < 100:
                return False
            fee = price * max_shares * self.config['fee_buy']
            total_cost = price * max_shares + fee
        
        self.cash -= total_cost
        self.position = max_shares
        self.position_price = price
        self.holding_days = 0
        
        self.trades.append({
            'date': date,
            'action': 'buy',
            'price': price,
            'shares': max_shares,
            'fee': fee,
            'reason': signal.get('reason', ''),
            'signal_strength': signal.get('strength', 0)
        })
        return True
    
    def sell(self, date: str, price: float, reason: str = '') -> bool:
        """卖出"""
        if self.position == 0:
            return False
        
        fee = price * self.position * self.config['fee_sell']
        stamp = price * self.position * self.config['stamp_duty']
        net_proceeds = price * self.position - fee - stamp
        
        pnl = net_proceeds - (self.position_price * self.position)
        pnl_percent = pnl / (self.position_price * self.position) * 100
        
        self.trades.append({
            'date': date,
            'action': 'sell',
            'price': price,
            'shares': self.position,
            'fee': fee,
            'stamp_duty': stamp,
            'reason': reason,
            'pnl': pnl,
            'pnl_percent': pnl_percent,
            'holding_days': self.holding_days
        })
        
        self.cash += net_proceeds
        self.position = 0
        self.position_price = 0
        return True
    
    def check_stop(self, current_price: float) -> Optional[str]:
        """检查是否触发止损止盈"""
        if self.position == 0:
            return None
        
        pnl_percent = (current_price - self.position_price) / self.position_price * 100
        
        if pnl_percent <= self.config['stop_loss'] * 100:
            return '止损'
        if pnl_percent >= self.config['take_profit'] * 100:
            return '止盈'
        return None
    
    def get_portfolio_value(self, current_price: float) -> float:
        """获取当前组合市值"""
        return self.cash + self.position * current_price

# ==================== 风险指标计算 ====================
def calculate_metrics(trades: List[Dict], initial_capital: float) -> Dict:
    """计算风险指标"""
    if not trades:
        return {}
    
    # 提取卖出交易（平仓记录）
    closed_trades = [t for t in trades if t['action'] == 'sell']
    
    if not closed_trades:
        return {'total_trades': 0}
    
    # 基本统计
    wins = [t for t in closed_trades if t.get('pnl', 0) > 0]
    losses = [t for t in closed_trades if t.get('pnl', 0) <= 0]
    
    win_count = len(wins)
    loss_count = len(losses)
    total_trades = win_count + loss_count
    
    win_rate = win_count / total_trades * 100 if total_trades > 0 else 0
    
    total_pnl = sum(t.get('pnl', 0) for t in closed_trades)
    avg_win = sum(t.get('pnl', 0) for t in wins) / win_count if win_count > 0 else 0
    avg_loss = sum(t.get('pnl', 0) for t in losses) / loss_count if loss_count > 0 else 0
    
    profit_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
    
    # 最大回撤计算
    daily_values = []
    cumulative = 0
    for t in closed_trades:
        cumulative += t.get('pnl', 0)
        daily_values.append(initial_capital + cumulative)
    
    max_value = daily_values[0]
    max_drawdown = 0
    for v in daily_values:
        if v > max_value:
            max_value = v
        dd = (max_value - v) / max_value * 100
        if dd > max_drawdown:
            max_drawdown = dd
    
    # 年化收益率
    if closed_trades:
        first_date = closed_trades[0]['date']
        last_date = closed_trades[-1]['date']
        try:
            start = datetime.strptime(first_date, '%Y-%m-%d')
            end = datetime.strptime(last_date, '%Y-%m-%d')
            days = (end - start).days
            if days > 0:
                total_return = total_pnl / initial_capital
                annual_return = (1 + total_return) ** (365 / days) - 1
            else:
                annual_return = 0
        except:
            annual_return = 0
    else:
        annual_return = 0
    
    return {
        'total_trades': total_trades,
        'win_count': win_count,
        'loss_count': loss_count,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_loss_ratio': profit_loss_ratio,
        'max_drawdown': max_drawdown,
        'annual_return': annual_return * 100,
        'final_capital': initial_capital + total_pnl,
    }

# ==================== 主函数 ====================
def run_realtime_trade():
    """执行实时交易"""
    code = CONFIG['product_code']
    data = get_realtime_data(code)
    
    if not data:
        print("无法获取实时数据")
        return
    
    close = float(data.get('f43', 0))  # 最新价
    print(f"当前价格: {close}")
    
    # 获取历史数据计算指标
    history = get_history_data(code, 60)
    if not history:
        print("无法获取历史数据")
        return
    
    # 生成信号
    signals = generate_signals(history)
    if signals:
        latest = signals[-1]
        print(f"最新信号: {latest['action']} - {latest['reason']}")
        print(f"信号强度: {'⭐' * latest['strength']}")

def run_backtest():
    """执行回测"""
    code = CONFIG['product_code']
    data = get_history_data(code, 250)  # 获取一年数据
    
    if not data:
        print("无法获取历史数据")
        return
    
    signals = generate_signals(data)
    trader = SimulatedTrader(CONFIG)
    
    for sig in signals:
        date = sig['date']
        price = sig['price']
        
        # 持仓天数+1
        if trader.position > 0:
            trader.holding_days += 1
        
        # 检查止损止盈
        if trader.position > 0:
            stop_reason = trader.check_stop(price)
            if stop_reason:
                trader.sell(date, price, stop_reason)
                print(f"{date}: 卖出 {stop_reason}, 价格: {price}")
                continue
        
        # 买入信号
        if sig['action'] == 'buy' and trader.position == 0:
            if trader.buy(date, price, sig):
                print(f"{date}: 买入, 价格: {price}, 原因: {sig['reason']}")
        
        # 卖出信号
        elif sig['action'] == 'sell' and trader.position > 0:
            if trader.sell(date, price, sig['reason']):
                print(f"{date}: 卖出, 价格: {price}, 原因: {sig['reason']}")
    
    # 最后一天如果还持仓，强制平仓
    if trader.position > 0:
        last_price = data[-1]['close']
        trader.sell(data[-1]['date'], last_price, '回测结束清仓')
    
    # 计算指标
    metrics = calculate_metrics(trader.trades, CONFIG['initial_capital'])
    
    print("\n" + "="*50)
    print("回测报告")
    print("="*50)
    print(f"总交易次数: {metrics.get('total_trades', 0)}")
    print(f"盈利次数: {metrics.get('win_count', 0)}")
    print(f"亏损次数: {metrics.get('loss_count', 0)}")
    print(f"胜率: {metrics.get('win_rate', 0):.2f}%")
    print(f"总盈亏: {metrics.get('total_pnl', 0):.2f}元")
    print(f"平均盈利: {metrics.get('avg_win', 0):.2f}元")
    print(f"平均亏损: {metrics.get('avg_loss', 0):.2f}元")
    print(f"盈亏比: {metrics.get('profit_loss_ratio', 0):.2f}")
    print(f"最大回撤: {metrics.get('max_drawdown', 0):.2f}%")
    print(f"年化收益率: {metrics.get('annual_return', 0):.2f}%")
    print(f"期末资金: {metrics.get('final_capital', 0):.2f}元")
    print("="*50)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'backtest':
        run_backtest()
    else:
        run_realtime_trade()
