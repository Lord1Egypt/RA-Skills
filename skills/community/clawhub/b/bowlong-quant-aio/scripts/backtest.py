#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
波龙股神量化交易系统 V2.0
quant-aio 回测系统
支持A股T+1规则、涨跌停限制、印花税的完整回测框架

© 2026 SimonsTang / 上海巧未来人工智能科技有限公司 版权所有
开源协议：MIT License
源码开放，欢迎完善，共同进步
GitHub: https://github.com/simonstang/bolong-quant
"""

import os
import sys
import yaml
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import argparse

import pandas as pd
import numpy as np

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class Signal(Enum):
    """交易信号"""
    BUY = 1
    SELL = -1
    HOLD = 0


@dataclass
class Trade:
    """交易记录"""
    date: str
    ts_code: str
    direction: str       # 'buy' / 'sell'
    price: float
    volume: int
    amount: float
    commission: float
    signal: Signal
    reason: str = ""


@dataclass
class Position:
    """持仓"""
    ts_code: str
    volume: int           # 股数（A股为100的整数倍）
    avg_cost: float       # 平均成本
    current_price: float
    unrealized_pnl: float = 0

    @property
    def market_value(self) -> float:
        return self.volume * self.current_price

    def update_pnl(self):
        self.unrealized_pnl = (self.current_price - self.avg_cost) * self.volume


@dataclass
class Portfolio:
    """投资组合"""
    cash: float
    positions: Dict[str, Position] = field(default_factory=dict)
    initial_cash: float = 0
    total_trades: int = 0
    winning_trades: int = 0

    @property
    def total_value(self) -> float:
        return self.cash + sum(p.market_value for p in self.positions.values())

    @property
    def total_pnl(self) -> float:
        return self.total_value - self.initial_cash

    @property
    def return_rate(self) -> float:
        return self.total_pnl / self.initial_cash if self.initial_cash > 0 else 0

    @property
    def position_ratio(self) -> float:
        return 1 - (self.cash / self.total_value) if self.total_value > 0 else 0


@dataclass
class BacktestResult:
    """回测结果"""
    initial_cash: float
    final_value: float
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    max_drawdown_pct: float
    win_rate: float
    profit_loss_ratio: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    trades: List[Trade] = field(default_factory=list)
    equity_curve: List[Dict] = field(default_factory=list)
    daily_returns: List[float] = field(default_factory=list)


class AShareRules:
    """A股交易规则"""
    
    # 印花税（仅卖出收取）
    STAMP_DUTY_RATE = 0.001
    
    # 佣金（买卖均收取，最低5元）
    COMMISSION_RATE = 0.0003
    MIN_COMMISSION = 5.0
    
    # 最小交易单位
    LOT_SIZE = 100
    
    # 涨跌幅限制
    PRICE_LIMIT_UP = 0.10    # 普通股 10%
    PRICE_LIMIT_UP_ST = 0.05 # ST股 5%
    
    @classmethod
    def calc_commission(cls, amount: float) -> float:
        """计算佣金"""
        commission = amount * cls.COMMISSION_RATE
        return max(commission, cls.MIN_COMMISSION)
    
    @classmethod
    def calc_stamp_duty(cls, amount: float, is_sell: bool) -> float:
        """计算印花税（仅卖出时）"""
        if is_sell:
            return amount * cls.STAMP_DUTY_RATE
        return 0
    
    @classmethod
    def calc_total_cost(cls, amount: float, is_sell: bool) -> float:
        """计算总交易成本"""
        return cls.calc_commission(amount) + cls.calc_stamp_duty(amount, is_sell)
    
    @classmethod
    def align_volume(cls, volume: int) -> int:
        """对齐交易单位"""
        return (volume // cls.LOT_SIZE) * cls.LOT_SIZE
    
    @classmethod
    def is_limit_up(cls, pre_close: float, current: float) -> bool:
        """判断是否涨停"""
        return current >= pre_close * (1 + cls.PRICE_LIMIT_UP)
    
    @classmethod
    def is_limit_down(cls, pre_close: float, current: float) -> bool:
        """判断是否跌停"""
        return current <= pre_close * (1 - cls.PRICE_LIMIT_UP)


class Strategy:
    """策略基类"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.name = self.__class__.__name__
    
    def generate_signal(self, data: pd.DataFrame, position: Optional[Position], 
                        current_date: str) -> Tuple[Signal, str]:
        """
        生成交易信号
        返回: (Signal, reason)
        """
        raise NotImplementedError


class MomentumStrategy(Strategy):
    """动量策略 - 均线金叉买入，死叉卖出"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.ma_short = config.get('ma_short', 5)
        self.ma_long = config.get('ma_long', 20)
    
    def generate_signal(self, data: pd.DataFrame, position: Optional[Position],
                        current_date: str) -> Tuple[Signal, str]:
        if len(data) < self.ma_long + 1:
            return Signal.HOLD, "数据不足"
        
        df = data.tail(self.ma_long + 1).copy()
        df['ma_short'] = df['close'].rolling(self.ma_short).mean()
        df['ma_long'] = df['close'].rolling(self.ma_long).mean()
        df = df.dropna()
        
        if len(df) < 2:
            return Signal.HOLD, "均线数据不足"
        
        prev_short = df['ma_short'].iloc[-2]
        curr_short = df['ma_short'].iloc[-1]
        prev_long = df['ma_long'].iloc[-2]
        curr_long = df['ma_long'].iloc[-1]
        
        # 金叉买入
        if prev_short <= prev_long and curr_short > curr_long:
            return Signal.BUY, f"MA{self.ma_short}上穿MA{self.ma_long}"
        
        # 死叉卖出
        if prev_short >= prev_long and curr_short < curr_long:
            return Signal.SELL, f"MA{self.ma_short}下穿MA{self.ma_long}"
        
        return Signal.HOLD, "无信号"


class RSIStrategy(Strategy):
    """RSI均值回归策略 - RSI<30超卖买入，RSI>70超买卖出"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.rsi_period = config.get('rsi_period', 14)
        self.oversold = config.get('oversold', 30)
        self.overbought = config.get('overbought', 70)
    
    def generate_signal(self, data: pd.DataFrame, position: Optional[Position],
                        current_date: str) -> Tuple[Signal, str]:
        if len(data) < self.rsi_period + 1:
            return Signal.HOLD, "数据不足"
        
        df = data.tail(self.rsi_period + 1).copy()
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.rsi_period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi = rsi.dropna()
        
        if len(rsi) < 1:
            return Signal.HOLD, "RSI数据不足"
        
        current_rsi = rsi.iloc[-1]
        
        if current_rsi < self.oversold:
            return Signal.BUY, f"RSI={current_rsi:.1f}低于{self.oversold}超卖区间"
        
        if current_rsi > self.overbought:
            return Signal.SELL, f"RSI={current_rsi:.1f}高于{self.overbought}超买区间"
        
        return Signal.HOLD, f"RSI={current_rsi:.1f}处于正常区间"


class MACDStrategy(Strategy):
    """MACD策略 - MACD金叉买入，死叉卖出"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.fast = config.get('fast', 12)
        self.slow = config.get('slow', 26)
        self.signal = config.get('signal', 9)
    
    def generate_signal(self, data: pd.DataFrame, position: Optional[Position],
                        current_date: str) -> Tuple[Signal, str]:
        if len(data) < self.slow + self.signal + 1:
            return Signal.HOLD, "数据不足"
        
        df = data.copy()
        df['ema_fast'] = df['close'].ewm(span=self.fast, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=self.slow, adjust=False).mean()
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['signal_line'] = df['macd'].ewm(span=self.signal, adjust=False).mean()
        df['histogram'] = df['macd'] - df['signal_line']
        df = df.dropna()
        
        if len(df) < 2:
            return Signal.HOLD, "MACD数据不足"
        
        prev_hist = df['histogram'].iloc[-2]
        curr_hist = df['histogram'].iloc[-1]
        
        if prev_hist <= 0 and curr_hist > 0:
            return Signal.BUY, "MACD金叉"
        
        if prev_hist >= 0 and curr_hist < 0:
            return Signal.SELL, "MACD死叉"
        
        return Signal.HOLD, "无信号"


class Backtester:
    """回测引擎"""
    
    STRATEGIES = {
        'momentum': MomentumStrategy,
        'rsi': RSIStrategy,
        'macd': MACDStrategy,
    }
    
    def __init__(self, config_path: str = 'config/config.yaml'):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.backtest_config = self.config['backtest']
        self.rules = AShareRules()
        
        # 初始资金
        self.initial_cash = self.backtest_config['initial_cash']
        
        # 佣金和滑点
        self.commission_rate = self.backtest_config['commission']
        self.stamp_duty = self.backtest_config['stamp_duty']
        self.slippage = self.backtest_config['slippage']
        
        # 启用规则
        self.t_plus_1 = self.backtest_config['rules']['t_plus_1']
        self.price_limit = self.backtest_config['rules']['price_limit']
        
        # 输出目录
        self.output_dir = Path(self.backtest_config['output_dir'])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 统计
        self.trades: List[Trade] = []
        self.equity_curve: List[Dict] = []
        self.daily_returns: List[float] = []
        
        # 持仓快照（用于T+1限制）
        self.buy_cooldown: Dict[str, str] = {}  # ts_code -> 买入日期
    
    def _apply_slippage(self, price: float, is_buy: bool) -> float:
        """应用滑点"""
        if is_buy:
            return price * (1 + self.slippage)
        return price * (1 - self.slippage)
    
    def _apply_price_limit(self, pre_close: float, price: float, 
                           is_buy: bool) -> Tuple[bool, float]:
        """应用涨跌停限制，返回(是否受限, 实际价格)"""
        if not self.price_limit:
            return False, price
        
        if self.rules.is_limit_up(pre_close, price) and is_buy:
            return True, pre_close * 1.10  # 涨停价买入（实际不成交）
        
        if self.rules.is_limit_down(pre_close, price) and not is_buy:
            return True, pre_close * 0.90  # 跌停价卖出
        
        return False, price
    
    def run(self, data: pd.DataFrame, strategy_name: str = 'momentum',
            strategy_config: Optional[Dict] = None) -> BacktestResult:
        """执行回测"""
        
        if data.empty:
            raise ValueError("数据为空")
        
        logger.info(f"🚀 开始回测 - 策略: {strategy_name}")
        logger.info(f"📊 数据范围: {data['trade_date'].min()} ~ {data['trade_date'].max()}")
        logger.info(f"💰 初始资金: {self.initial_cash:,.2f}")
        
        # 初始化策略
        strategy_class = self.STRATEGIES.get(strategy_name.lower(), MomentumStrategy)
        strategy = strategy_class(strategy_config or {})
        
        # 初始化组合
        portfolio = Portfolio(cash=self.initial_cash, initial_cash=self.initial_cash)
        
        # 获取交易日期列表
        dates = sorted(data['trade_date'].unique())
        stocks = data['ts_code'].unique()
        
        logger.info(f"📅 交易日: {len(dates)}天 | 股票数: {len(stocks)}")
        
        # 日志进度
        total_dates = len(dates)
        
        for i, current_date in enumerate(dates):
            date_data = data[data['trade_date'] == current_date]
            
            daily_pnl = 0
            daily_value = portfolio.cash
            
            # 更新持仓价格并计算当日盈亏
            for ts_code, pos in list(portfolio.positions.items()):
                stock_day = date_data[date_data['ts_code'] == ts_code]
                if not stock_day.empty:
                    pos.current_price = stock_day.iloc[0]['close']
                    pos.update_pnl()
                    daily_pnl += pos.unrealized_pnl
                    daily_value += pos.market_value
            
            # 每日调仓检查（以成交量最大的股票为代表）
            if not date_data.empty:
                top_stock = date_data.nlargest(1, 'vol')
                if not top_stock.empty:
                    ts_code = top_stock.iloc[0]['ts_code']
                    stock_data = data[data['ts_code'] == ts_code].sort_values('trade_date')
                    stock_up_to_date = stock_data[stock_data['trade_date'] <= current_date]
                    
                    if len(stock_up_to_date) > 1:
                        # 获取前一日收盘价（用于涨跌停判断）
                        pre_close = stock_up_to_date.iloc[-2]['close']
                        current_price = stock_up_to_date.iloc[-1]['close']
                        
                        signal, reason = strategy.generate_signal(
                            stock_up_to_date, 
                            portfolio.positions.get(ts_code),
                            current_date
                        )
                        
                        position = portfolio.positions.get(ts_code)
                        
                        # === 买入逻辑 ===
                        if signal == Signal.BUY and position is None:
                            # 检查T+1限制
                            can_buy = True
                            if self.t_plus_1 and ts_code in self.buy_cooldown:
                                if self.buy_cooldown[ts_code] == current_date:
                                    can_buy = False
                            
                            # 检查涨跌停
                            limited, limit_price = self._apply_price_limit(
                                pre_close, current_price, is_buy=True
                            )
                            
                            if can_buy and not limited:
                                # 计算可买入数量
                                available_cash = portfolio.cash * 0.95  # 预留5%
                                exec_price = self._apply_slippage(limit_price, is_buy=True)
                                max_volume = int(available_cash / exec_price / 100) * 100
                                
                                if max_volume >= 100:
                                    amount = max_volume * exec_price
                                    commission = self.rules.calc_commission(amount)
                                    
                                    portfolio.cash -= (amount + commission)
                                    portfolio.positions[ts_code] = Position(
                                        ts_code=ts_code,
                                        volume=max_volume,
                                        avg_cost=exec_price,
                                        current_price=exec_price
                                    )
                                    self.buy_cooldown[ts_code] = current_date
                                    
                                    trade = Trade(
                                        date=current_date,
                                        ts_code=ts_code,
                                        direction='buy',
                                        price=exec_price,
                                        volume=max_volume,
                                        amount=amount,
                                        commission=commission,
                                        signal=signal,
                                        reason=reason
                                    )
                                    self.trades.append(trade)
                                    portfolio.total_trades += 1
                                    logger.debug(f"[{current_date}] 买入 {ts_code} @ {exec_price:.2f} x {max_volume}")
                        
                        # === 卖出逻辑 ===
                        elif signal == Signal.SELL and position is not None:
                            # 检查涨跌停
                            limited, limit_price = self._apply_price_limit(
                                pre_close, current_price, is_buy=False
                            )
                            
                            if not limited:
                                exec_price = self._apply_slippage(limit_price, is_buy=False)
                                amount = position.volume * exec_price
                                commission = self.rules.calc_commission(amount)
                                stamp = self.rules.calc_stamp_duty(amount, is_sell=True)
                                
                                total_cost = amount - commission - stamp
                                
                                # 记录盈亏
                                realized_pnl = total_cost - (position.volume * position.avg_cost)
                                if realized_pnl > 0:
                                    portfolio.winning_trades += 1
                                else:
                                    portfolio.winning_trades += 0  # 亏损不计入胜率分子
                                
                                portfolio.cash += total_cost
                                del portfolio.positions[ts_code]
                                
                                trade = Trade(
                                    date=current_date,
                                    ts_code=ts_code,
                                    direction='sell',
                                    price=exec_price,
                                    volume=position.volume,
                                    amount=amount,
                                    commission=commission + stamp,
                                    signal=signal,
                                    reason=reason
                                )
                                self.trades.append(trade)
                                portfolio.total_trades += 1
                                logger.debug(f"[{current_date}] 卖出 {ts_code} @ {exec_price:.2f}")
            
            # 记录每日权益曲线
            self.equity_curve.append({
                'date': current_date,
                'total_value': portfolio.total_value,
                'cash': portfolio.cash,
                'position_value': portfolio.total_value - portfolio.cash,
                'return': portfolio.return_rate
            })
            
            # 计算日收益率
            if len(self.equity_curve) > 1:
                prev_value = self.equity_curve[-2]['total_value']
                curr_value = portfolio.total_value
                daily_return = (curr_value - prev_value) / prev_value if prev_value > 0 else 0
                self.daily_returns.append(daily_return)
            
            # 进度日志
            if (i + 1) % 100 == 0:
                logger.info(f"⏳ [{current_date}] {i+1}/{total_dates}天 | 净值: {portfolio.total_value:,.2f}")
        
        # === 计算绩效指标 ===
        logger.info("📊 计算绩效指标...")
        
        result = self._calculate_metrics(portfolio)
        
        logger.info(f"✅ 回测完成!")
        logger.info(f"   最终净值: {result.final_value:,.2f}")
        logger.info(f"   总收益率: {result.total_return:.2%}")
        logger.info(f"   夏普比率: {result.sharpe_ratio:.2f}")
        logger.info(f"   最大回撤: {result.max_drawdown_pct:.2%}")
        logger.info(f"   胜率: {result.win_rate:.2%}")
        
        return result
    
    def _calculate_metrics(self, portfolio: Portfolio) -> BacktestResult:
        """计算绩效指标"""
        
        final_value = portfolio.total_value
        total_return = portfolio.return_rate
        
        # 年化收益率
        n_days = len(self.equity_curve)
        n_years = n_days / 252
        annual_return = (final_value / self.initial_cash) ** (1 / n_years) - 1 if n_years > 0 else 0
        
        # 夏普比率
        if self.daily_returns and len(self.daily_returns) > 1:
            daily_returns_arr = np.array(self.daily_returns)
            excess_returns = daily_returns_arr - 0.03 / 252  # 无风险利率年化3%
            sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252) if np.std(excess_returns) > 0 else 0
        else:
            sharpe_ratio = 0
        
        # 最大回撤
        equity_values = [e['total_value'] for e in self.equity_curve]
        peak = equity_values[0]
        max_drawdown = 0
        max_drawdown_pct = 0
        
        for value in equity_values:
            if value > peak:
                peak = value
            drawdown = peak - value
            drawdown_pct = drawdown / peak if peak > 0 else 0
            if drawdown > max_drawdown:
                max_drawdown = drawdown
                max_drawdown_pct = drawdown_pct
        
        # 交易统计
        total_trades = portfolio.total_trades
        winning_trades = portfolio.winning_trades
        losing_trades = total_trades - winning_trades
        
        # 盈亏统计
        buy_records = {}
        sell_trades = [t for t in self.trades if t.direction == 'sell']
        
        total_wins = 0
        total_losses = 0
        
        for sell_trade in sell_trades:
            if sell_trade.ts_code in buy_records:
                buy_price = buy_records[sell_trade.ts_code]['price']
                sell_price = sell_trade.price
                pnl_per_share = sell_price - buy_price
                if pnl_per_share > 0:
                    total_wins += pnl_per_share * sell_trade.volume
                else:
                    total_losses += abs(pnl_per_share) * sell_trade.volume
        
        avg_win = total_wins / winning_trades if winning_trades > 0 else 0
        avg_loss = total_losses / losing_trades if losing_trades > 0 else 0
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        profit_loss_ratio = (avg_win / abs(avg_loss)) if losing_trades > 0 and winning_trades > 0 and avg_loss != 0 else 0
        
        return BacktestResult(
            initial_cash=self.initial_cash,
            final_value=final_value,
            total_return=total_return,
            annual_return=annual_return,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            max_drawdown_pct=max_drawdown_pct,
            win_rate=win_rate,
            profit_loss_ratio=profit_loss_ratio,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            avg_win=avg_win,
            avg_loss=avg_loss,
            trades=self.trades,
            equity_curve=self.equity_curve,
            daily_returns=self.daily_returns
        )
    
    def save_report(self, result: BacktestResult, strategy_name: str, 
                    output_format: str = 'md'):
        """保存回测报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if output_format == 'json':
            # JSON格式
            output_file = self.output_dir / f"backtest_{strategy_name}_{timestamp}.json"
            data = {
                'strategy': strategy_name,
                'timestamp': timestamp,
                'metrics': {
                    'initial_cash': result.initial_cash,
                    'final_value': result.final_value,
                    'total_return': result.total_return,
                    'annual_return': result.annual_return,
                    'sharpe_ratio': result.sharpe_ratio,
                    'max_drawdown': result.max_drawdown,
                    'max_drawdown_pct': result.max_drawdown_pct,
                    'win_rate': result.win_rate,
                    'profit_loss_ratio': result.profit_loss_ratio,
                    'total_trades': result.total_trades,
                    'winning_trades': result.winning_trades,
                    'losing_trades': result.losing_trades,
                    'avg_win': result.avg_win,
                    'avg_loss': result.avg_loss,
                },
                'trades': [
                    {
                        'date': t.date,
                        'ts_code': t.ts_code,
                        'direction': t.direction,
                        'price': t.price,
                        'volume': t.volume,
                        'amount': t.amount,
                        'commission': t.commission,
                        'signal': t.signal.name,
                        'reason': t.reason
                    }
                    for t in result.trades
                ]
            }
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        
        else:
            # Markdown格式
            output_file = self.output_dir / f"backtest_report_{strategy_name}_{timestamp}.md"
            
            report = f"""# 📊 回测报告 · {strategy_name}策略

**生成时间**: {timestamp}
**回测日期**: {self.equity_curve[0]['date']} ~ {self.equity_curve[-1]['date']}

---

## 💰 收益概览

| 指标 | 数值 |
|------|------|
| 初始资金 | {result.initial_cash:,.2f} 元 |
| 最终净值 | {result.final_value:,.2f} 元 |
| 总收益率 | {result.total_return:+.2%} |
| 年化收益 | {result.annual_return:+.2%} |
| 夏普比率 | {result.sharpe_ratio:.2f} |
| 最大回撤 | {result.max_drawdown:,.2f} 元 ({result.max_drawdown_pct:.2%}) |

---

## 📈 交易统计

| 指标 | 数值 |
|------|------|
| 总交易次数 | {result.total_trades} |
| 盈利次数 | {result.winning_trades} |
| 亏损次数 | {result.losing_trades} |
| 胜率 | {result.win_rate:.2%} |
| 盈亏比 | {result.profit_loss_ratio:.2f} |
| 平均盈利 | {result.avg_win:+,.2f} 元/笔 |
| 平均亏损 | {result.avg_loss:+,.2f} 元/笔 |

---

## 📋 交易记录

| 日期 | 股票 | 方向 | 价格 | 数量 | 金额 | 手续费 | 信号 | 理由 |
|------|------|------|------|------|------|--------|------|------|
"""
            for t in result.trades:
                report += f"| {t.date} | {t.ts_code} | {t.direction} | {t.price:.2f} | {t.volume} | {t.amount:,.2f} | {t.commission:.2f} | {t.signal.name} | {t.reason} |\n"
            
            report += f"""
---

## 📉 权益曲线

```
日期            净值        收益率
"""
            for e in self.equity_curve[::max(1, len(self.equity_curve)//20)]:
                report += f"{e['date']}    {e['total_value']:>12,.2f}    {e['return']:+.2%}\n"
            
            report += f"""
---

## ⚠️ 风险提示

本回测结果仅供参考，不构成投资建议。
历史业绩不代表未来表现。
请结合自身风险承受能力谨慎决策。

---
*quant-aio 回测系统 v1.0*
"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
        
        logger.info(f"💾 报告已保存: {output_file}")
        return output_file


def main():
    parser = argparse.ArgumentParser(description='quant-aio 回测系统')
    parser.add_argument('--strategy', default='momentum', 
                        choices=['momentum', 'rsi', 'macd'],
                        help='策略: momentum/rsi/macd')
    parser.add_argument('--start', default='2020-01-01', help='回测开始日期')
    parser.add_argument('--end', default='2026-03-27', help='回测结束日期')
    parser.add_argument('--cash', type=float, default=1000000, help='初始资金')
    parser.add_argument('--config', default='config/config.yaml', help='配置文件路径')
    parser.add_argument('--output', choices=['md', 'json'], default='md', help='输出格式')
    parser.add_argument('--symbol', default='000001.SZ', help='回测股票代码')
    
    args = parser.parse_args()
    
    # 加载配置
    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 模拟数据（实际应从数据源读取）
    # 这里用随机数据演示，实际使用中替换为真实数据
    logger.info(f"⚠️ 使用模拟数据演示，请替换为真实数据")
    
    np.random.seed(42)
    dates = pd.date_range(args.start, args.end, freq='B')  # 工作日
    
    mock_data = []
    base_price = 10.0
    for date in dates:
        base_price *= (1 + np.random.normal(0.001, 0.02))
        for ts_code in [args.symbol]:
            mock_data.append({
                'trade_date': date.strftime('%Y%m%d'),
                'ts_code': ts_code,
                'open': base_price * np.random.uniform(0.99, 1.01),
                'high': base_price * np.random.uniform(1.00, 1.03),
                'low': base_price * np.random.uniform(0.97, 1.00),
                'close': base_price,
                'vol': int(np.random.uniform(1e6, 1e8)),
            })
    
    df = pd.DataFrame(mock_data)
    logger.info(f"📊 加载 {len(df)} 条数据")
    
    # 修改初始资金
    config['backtest']['initial_cash'] = args.cash
    
    # 运行回测
    engine = Backtester(args.config)
    result = engine.run(df, strategy_name=args.strategy)
    
    # 保存报告
    output_file = engine.save_report(result, args.strategy, output_format=args.output)
    
    print(f"\n🎉 回测完成！报告: {output_file}")
    print(f"\n{'='*50}")
    print(f"  总收益率: {result.total_return:+.2%}")
    print(f"  年化收益: {result.annual_return:+.2%}")
    print(f"  夏普比率: {result.sharpe_ratio:.2f}")
    print(f"  最大回撤: {result.max_drawdown_pct:.2%}")
    print(f"  胜率: {result.win_rate:.2%}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
