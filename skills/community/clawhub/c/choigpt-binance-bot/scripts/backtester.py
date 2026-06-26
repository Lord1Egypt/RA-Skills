"""
백테스트 엔진
ChoiGPT 방법론 전략을 과거 데이터로 검증
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Optional
import logging

from src.strategy import ChoiGPTStrategy
from src.indicators import calculate_atr
from config.config import *

logger = logging.getLogger(__name__)


class Trade:
    """개별 거래 기록"""
    def __init__(self, direction, entry_price, stop_loss, take_profit,
                 entry_time, quantity, leverage, confidence, reasons):
        self.direction = direction
        self.entry_price = entry_price
        self.stop_loss = stop_loss
        self.initial_stop_loss = stop_loss
        self.take_profit = take_profit
        self.entry_time = entry_time
        self.exit_time = None
        self.exit_price = None
        self.quantity = quantity
        self.leverage = leverage
        self.confidence = confidence
        self.reasons = reasons
        self.pnl = 0.0
        self.pnl_pct = 0.0
        self.status = "OPEN"  # OPEN, WIN, LOSS, CLOSED
        self.bars_held = 0
        self.max_favorable = 0.0  # 최대 유리한 방향으로의 움직임
        self.max_adverse = 0.0    # 최대 불리한 방향으로의 움직임

    @property
    def risk_reward(self):
        if self.direction == "LONG":
            risk = self.entry_price - self.stop_loss
            reward = self.take_profit - self.entry_price
        else:
            risk = self.stop_loss - self.entry_price
            reward = self.entry_price - self.take_profit
        return reward / risk if risk > 0 else 0


class BacktestResult:
    """백테스트 결과"""
    def __init__(self):
        self.trades: List[Trade] = []
        self.equity_curve: pd.Series = None
        self.metrics: dict = {}

    def calculate_metrics(self, initial_capital: float):
        if not self.trades:
            return

        closed_trades = [t for t in self.trades if t.status != "OPEN"]
        wins = [t for t in closed_trades if t.pnl > 0]
        losses = [t for t in closed_trades if t.pnl <= 0]

        total_trades = len(closed_trades)
        win_rate = len(wins) / total_trades if total_trades > 0 else 0

        total_pnl = sum(t.pnl for t in closed_trades)
        avg_win = np.mean([t.pnl for t in wins]) if wins else 0
        avg_loss = abs(np.mean([t.pnl for t in losses])) if losses else 0
        profit_factor = (sum(t.pnl for t in wins) /
                        abs(sum(t.pnl for t in losses))) if losses else float('inf')

        # 최대 낙폭 (MDD)
        eq = self.equity_curve
        rolling_max = eq.cummax()
        drawdown = (eq - rolling_max) / rolling_max * 100
        max_drawdown = drawdown.min()

        # 샤프 비율 (연간화)
        daily_returns = eq.pct_change().dropna()
        sharpe = (daily_returns.mean() / daily_returns.std() * np.sqrt(252)
                  if daily_returns.std() > 0 else 0)

        # 칼마 비율
        total_return_pct = (eq.iloc[-1] - initial_capital) / initial_capital * 100
        calmar = total_return_pct / abs(max_drawdown) if max_drawdown != 0 else 0

        # 연속 승/패
        win_streak = loss_streak = 0
        current_streak = 0
        last_result = None
        for t in closed_trades:
            result = t.pnl > 0
            if result == last_result:
                current_streak += 1
            else:
                current_streak = 1
                last_result = result
            if result:
                win_streak = max(win_streak, current_streak)
            else:
                loss_streak = max(loss_streak, current_streak)

        avg_bars = np.mean([t.bars_held for t in closed_trades]) if closed_trades else 0

        self.metrics = {
            '총 거래 수': total_trades,
            '승률': f"{win_rate:.1%}",
            '승률_raw': win_rate,
            '수익 거래': len(wins),
            '손실 거래': len(losses),
            '총 손익 (USDT)': f"{total_pnl:.2f}",
            '총 수익률': f"{total_return_pct:.2f}%",
            '최종 잔고': f"{eq.iloc[-1]:.2f}",
            '평균 수익 (USDT)': f"{avg_win:.2f}",
            '평균 손실 (USDT)': f"{avg_loss:.2f}",
            '손익비': f"{avg_win/avg_loss:.2f}" if avg_loss > 0 else "N/A",
            '프로핏 팩터': f"{profit_factor:.2f}",
            '최대 낙폭 (MDD)': f"{max_drawdown:.2f}%",
            '샤프 비율': f"{sharpe:.2f}",
            '칼마 비율': f"{calmar:.2f}",
            '최장 연승': win_streak,
            '최장 연패': loss_streak,
            '평균 보유 캔들': f"{avg_bars:.1f}",
        }

        return self.metrics
class Backtester:
    """ChoiGPT 방법론 백테스터"""

    def __init__(self, initial_capital: float = BACKTEST_INITIAL_CAPITAL):
        self.initial_capital = initial_capital
        self.strategy = ChoiGPTStrategy(min_confidence=0.70)
        self.commission = BACKTEST_COMMISSION
        self.slippage = BACKTEST_SLIPPAGE
        try:
            self.spread = BACKTEST_SPREAD
        except NameError:
            self.spread = 0.00005  # V4.2: 스프레드 추가
        self.fixed_margin = None # V7.3 1회 진입 고정 증거금 옵션 추가

    def run(self, df: pd.DataFrame, symbol: str = "BTCUSDT",
            warmup_bars: int = 100) -> BacktestResult:
        """
        백테스트 실행

        Args:
            df: OHLCV 데이터프레임
            symbol: 심볼명
            warmup_bars: 초기 워밍업 기간 (지표 계산용)
        """
        result = BacktestResult()
        capital = self.initial_capital
        equity_values = [capital]
        equity_dates = [df.index[warmup_bars]]

        open_trade: Optional[Trade] = None

        logger.info(f"백테스트 시작: {symbol} | {df.index[warmup_bars]} ~ {df.index[-1]}")
        logger.info(f"초기 자본: ${capital:,.2f} | 총 캔들: {len(df)-warmup_bars}개")

        for i in range(warmup_bars, len(df) - 1):
            current_bar = df.iloc[:i+1]
            current_candle = df.iloc[i]
            next_candle = df.iloc[i+1]

            # ── 열린 포지션 관리 ──
            if open_trade:
                open_trade.bars_held += 1

                # 스탑로스 / 테이크프로핏 체크 (다음 캔들 기준)
                if open_trade.direction == "LONG":
                    open_trade.max_favorable = max(open_trade.max_favorable,
                                                    next_candle['high'] - open_trade.entry_price)
                    open_trade.max_adverse = min(open_trade.max_adverse,
                                                  next_candle['low'] - open_trade.entry_price)

                    # SL 터치
                    if next_candle['low'] <= open_trade.stop_loss:
                        exit_price = open_trade.stop_loss * (1 - self.slippage)
                        open_trade = self._close_trade(
                            open_trade, exit_price, next_candle.name, "LOSS", capital)
                        capital += open_trade.pnl
                        result.trades.append(open_trade)
                        open_trade = None

                    # TP 터치
                    elif next_candle['high'] >= open_trade.take_profit:
                        exit_price = open_trade.take_profit * (1 - self.slippage)
                        open_trade = self._close_trade(
                            open_trade, exit_price, next_candle.name, "WIN", capital)
                        capital += open_trade.pnl
                        result.trades.append(open_trade)
                        open_trade = None

                elif open_trade.direction == "SHORT":
                    open_trade.max_favorable = max(open_trade.max_favorable,
                                                    open_trade.entry_price - next_candle['low'])
                    open_trade.max_adverse = min(open_trade.max_adverse,
                                                  open_trade.entry_price - next_candle['high'])

                    if next_candle['high'] >= open_trade.stop_loss:
                        exit_price = open_trade.stop_loss * (1 + self.slippage)
                        open_trade = self._close_trade(
                            open_trade, exit_price, next_candle.name, "LOSS", capital)
                        capital += open_trade.pnl
                        result.trades.append(open_trade)
                        open_trade = None

                    elif next_candle['low'] <= open_trade.take_profit:
                        exit_price = open_trade.take_profit * (1 + self.slippage)
                        open_trade = self._close_trade(
                            open_trade, exit_price, next_candle.name, "WIN", capital)
                        capital += open_trade.pnl
                        result.trades.append(open_trade)
                        open_trade = None

            # ── 신호 탐색 (열린 포지션 없을 때) ──
            if not open_trade:
                try:
                    analysis = self.strategy.analyze(current_bar, symbol)

                    if analysis.signal:
                        sig = analysis.signal

                        # 슬리피지 적용된 실제 진입가
                        if sig.direction == "LONG":
                            actual_entry = sig.entry_price * (1 + self.slippage)
                        else:
                            actual_entry = sig.entry_price * (1 - self.slippage)

                        # 포지션 사이즈 계산
                        risk_per_unit = abs(actual_entry - sig.stop_loss)
                        if risk_per_unit > 0:
                            if self.fixed_margin:
                                quantity = (self.fixed_margin * sig.leverage) / actual_entry
                            else:
                                risk_amount = capital * (RISK_PER_TRADE / 100)
                                quantity = (risk_amount * sig.leverage) / actual_entry
                        else:
                            continue

                        # 수수료 차감
                        commission_cost = actual_entry * quantity * self.commission * 2  # 진입+청산

                        trade = Trade(
                            direction=sig.direction,
                            entry_price=actual_entry,
                            stop_loss=sig.stop_loss,
                            take_profit=sig.take_profit,
                            entry_time=current_candle.name,
                            quantity=quantity,
                            leverage=sig.leverage,
                            confidence=sig.confidence,
                            reasons=sig.reasons
                        )
                        open_trade = trade

                except Exception as e:
                    logger.debug(f"분석 실패 {i}: {e}")
                    continue

            equity_values.append(capital)
            equity_dates.append(current_candle.name)

        # 마지막 열린 포지션 강제 청산
        if open_trade:
            last_price = df['close'].iloc[-1]
            open_trade = self._close_trade(
                open_trade, last_price, df.index[-1], "CLOSED", capital)
            capital += open_trade.pnl
            result.trades.append(open_trade)

        result.equity_curve = pd.Series(equity_values, index=equity_dates)
        result.calculate_metrics(self.initial_capital)

        return result

    def _close_trade(self, trade: Trade, exit_price: float,
                     exit_time, status: str, capital: float) -> Trade:
        """거래 청산"""
        trade.exit_price = exit_price
        trade.exit_time = exit_time
        trade.status = status

        if trade.direction == "LONG":
            raw_pnl = (exit_price - trade.entry_price) * trade.quantity
        else:
            raw_pnl = (trade.entry_price - exit_price) * trade.quantity

        # V4.2: 수수료 + 스프레드 비용
        commission = (trade.entry_price + exit_price) * trade.quantity * self.commission
        spread_cost = (trade.entry_price + exit_price) * trade.quantity * self.spread
        total_cost = commission + spread_cost

        trade.pnl = raw_pnl - total_cost
        trade.pnl_pct = trade.pnl / capital * 100

        return trade

    def print_results(self, result: BacktestResult):
        """결과 출력"""
        print("\n" + "="*60)
        print("📊 백테스트 결과")
        print("="*60)
        for key, value in result.metrics.items():
            if key != '승률_raw':
                print(f"  {key:<20}: {value}")

        # 최근 10개 거래 출력
        print("\n📋 최근 거래 내역 (최대 10개):")
        print(f"  {'시간':<20} {'방향':<6} {'진입가':<12} {'청산가':<12} {'손익':<10} {'결과'}")
        print("  " + "-"*75)
        for trade in result.trades[-10:]:
            if trade.exit_price:
                print(f"  {str(trade.entry_time)[:19]:<20} "
                      f"{'📗' if trade.direction=='LONG' else '📕'}{trade.direction:<5} "
                      f"{trade.entry_price:<12.2f} "
                      f"{trade.exit_price:<12.2f} "
                      f"{trade.pnl:+<10.2f} "
                      f"{'✅' if trade.status=='WIN' else '❌'}")
        print("="*60)

    def optimize_parameters(self, df: pd.DataFrame, symbol: str,
                             param_grid: dict = None) -> pd.DataFrame:
        """
        파라미터 최적화 (그리드 서치)
        가장 좋은 파라미터 조합 탐색
        """
        if param_grid is None:
            param_grid = {
                'min_confidence': [0.55, 0.60, 0.65, 0.70, 0.75],
            }

        results = []
        from itertools import product

        keys = list(param_grid.keys())
        values = list(param_grid.values())

        print(f"\n🔍 파라미터 최적화 시작... (총 {len(list(product(*values)))}개 조합)")

        for combo in product(*values):
            params = dict(zip(keys, combo))

            # 파라미터 적용
            self.strategy.min_confidence = params.get('min_confidence', 0.60)

            try:
                result = self.run(df, symbol)
                metrics = result.metrics

                results.append({
                    **params,
                    'win_rate': result.metrics.get('승률_raw', 0),
                    'total_return': float(metrics.get('총 수익률', '0%').replace('%', '')),
                    'max_drawdown': float(metrics.get('최대 낙폭 (MDD)', '0%').replace('%', '')),
                    'profit_factor': float(metrics.get('프로핏 팩터', '0').replace('inf', '999')),
                    'sharpe': float(metrics.get('샤프 비율', '0')),
                    'total_trades': int(metrics.get('총 거래 수', 0)),
                })

                print(f"  {params} → 수익률: {metrics.get('총 수익률', 'N/A')} | "
                      f"MDD: {metrics.get('최대 낙폭 (MDD)', 'N/A')} | "
                      f"승률: {metrics.get('승률', 'N/A')}")
            except Exception as e:
                logger.error(f"최적화 실패 {params}: {e}")

        opt_df = pd.DataFrame(results)
        if len(opt_df) > 0:
            # 종합 점수 계산 (수익률 * 승률 / |MDD|)
            opt_df['score'] = (opt_df['total_return'] * opt_df['win_rate']
                              / (opt_df['max_drawdown'].abs() + 1))
            opt_df = opt_df.sort_values('score', ascending=False)

        return opt_df
