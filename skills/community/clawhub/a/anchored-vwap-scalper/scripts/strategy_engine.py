#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import os
import sys
import logging
sys.path.append(os.path.dirname(__file__))

from avwap_calculator import calculate_avwap
from lighter_client import get_lighter_client

# Logging
os.makedirs("../logs", exist_ok=True)
logging.basicConfig(
    filename=f"../logs/scalper_{date.today()}.log",
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s'
)

class StrategyEngine:
    def __init__(self, symbol: str = "BTC-USD", timeframe: str = "5m", dry_run: bool = True):
        self.raw_symbol = symbol.upper().replace('-', '/')
        self.ccxt_symbol = f"{self.raw_symbol}:USDT" if not self.raw_symbol.endswith(':USDT') else self.raw_symbol
        self.timeframe = timeframe
        self.dry_run = dry_run
        self.exchange = get_lighter_client()
        self.exchange.load_markets()
        self.market = self.exchange.market(self.ccxt_symbol)
        self.config = {
            "risk_percent": 0.01,
            "atr_multiplier_sl": 1.5,
            "rr_min": 2.0,
            "max_positions": 3,
            "daily_loss_limit": 0.03,
            "leverage": 10
        }
        self.state = self._load_state()
        logging.info(f"BTC Engine started → {self.ccxt_symbol} | Dry-run: {self.dry_run}")

    def _load_state(self):
        state_file = os.path.join(os.path.dirname(__file__), "../state/engine_state.json")
        if os.path.exists(state_file):
            with open(state_file) as f:
                return json.load(f)
        return {
            "last_bar_ts": None,
            "daily_pnl": 0.0,
            "last_date": str(date.today())
        }

    def _save_state(self):
        state_file = os.path.join(os.path.dirname(__file__), "../state/engine_state.json")
        with open(state_file, "w") as f:
            json.dump(self.state, f, indent=2)

    def _fetch_candles(self, limit=600):
        ohlcv = self.exchange.fetch_ohlcv(self.ccxt_symbol, self.timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def _calculate_indicators(self, df):
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = tr.rolling(14).mean()

        df['vol_sma'] = df['volume'].rolling(20).mean()
        return df

    def get_current_position(self):
        positions = self.exchange.fetch_positions([self.ccxt_symbol])
        for pos in positions:
            contracts = float(pos.get('contracts', 0) or pos.get('info', {}).get('contracts', 0))
            if contracts != 0:
                return pos
        return None

    def calculate_contracts(self, df):
        balance = self.exchange.fetch_balance()
        equity = float(balance['total'].get('USDC', balance['total'].get('USDT', 1000)))
        risk_usd = equity * self.config["risk_percent"]

        price = float(df['close'].iloc[-1])
        atr = float(df['atr'].iloc[-1])
        stop_distance = atr * self.config["atr_multiplier_sl"]

        contract_size = float(self.market['contractSize'] or 1)
        contracts = risk_usd / (stop_distance * contract_size)

        contracts = min(contracts, (equity * 0.1 / price) / contract_size)
        contracts = max(contracts, self.market['limits']['amount']['min'] or 1)
        contracts = round(contracts / self.market['precision']['amount']) * self.market['precision']['amount']
        return contracts

    def place_order(self, side: str, order_type: str = 'market', amount=None, price=None, params=None):
        if self.dry_run:
            logging.info(f"[DRY-RUN] {side.upper()} {order_type} | Amount: {amount} | Price: {price}")
            return {"id": "dry-run-id", "status": "dry-run"}
        try:
            order = self.exchange.create_order(
                symbol=self.ccxt_symbol,
                type=order_type,
                side=side,
                amount=amount,
                price=price,
                params=params or {}
            )
            logging.info(f"✅ ORDER PLACED → {side.upper()} {order_type} | ID: {order.get('id')}")
            return order
        except Exception as e:
            logging.error(f"Order failed: {e}")
            return None

    def run(self):
        df = self._fetch_candles()
        df = self._calculate_indicators(df)
        avwap = calculate_avwap(df.to_dict('records'), self.ccxt_symbol)

        current_price = float(df['close'].iloc[-1])
        current_atr = float(df['atr'].iloc[-1])
        volume_spike = float(df['volume'].iloc[-1]) > 1.5 * float(df['vol_sma'].iloc[-1])

        position = self.get_current_position()
        if position:
            logging.info(f"Position already open: {position.get('side')} | Contracts: {position.get('contracts')}")
            return

        signals = []

        # 1. Mean-Reversion
        if current_price <= avwap * 0.996 and float(df['rsi'].iloc[-1]) < 35:
            signals.append({"strategy": "Mean-Reversion", "side": "buy"})
        elif current_price >= avwap * 1.004 and float(df['rsi'].iloc[-1]) > 65:
            signals.append({"strategy": "Mean-Reversion", "side": "sell"})

        # 2. Breakout
        if volume_spike and current_price > avwap and df['close'].iloc[-2] <= avwap:
            signals.append({"strategy": "Breakout", "side": "buy"})
        elif volume_spike and current_price < avwap and df['close'].iloc[-2] >= avwap:
            signals.append({"strategy": "Breakout", "side": "sell"})

        # 3+4. Momentum / Volume-Confirmed Trend
        if current_price > avwap and float(df['macd_hist'].iloc[-1]) > float(df['macd_hist'].iloc[-2]) and volume_spike:
            signals.append({"strategy": "Momentum/Trend", "side": "buy"})
        elif current_price < avwap and float(df['macd_hist'].iloc[-1]) < float(df['macd_hist'].iloc[-2]) and volume_spike:
            signals.append({"strategy": "Momentum/Trend", "side": "sell"})

        if signals:
            signal = signals[0]
            side = signal["side"]
            contracts = self.calculate_contracts(df)

            if contracts > 0:
                logging.info(f"🚀 BTC SIGNAL: {signal['strategy']} | {side.upper()} | AVWAP {avwap:.2f} | Price {current_price:.2f}")
                entry_order = self.place_order(side=side, order_type='market', amount=contracts)

                if entry_order and not self.dry_run:
                    # Fixed SL (1.5 × ATR)
                    sl_offset = current_atr * self.config["atr_multiplier_sl"]
                    sl_price = current_price - sl_offset if side == "buy" else current_price + sl_offset
                    self.place_order(
                        side="sell" if side == "buy" else "buy",
                        order_type='stop',
                        amount=contracts,
                        price=sl_price,
                        params={'reduceOnly': True}
                    )

                    # TP at 1:2 RR
                    tp_price = current_price + (current_price - sl_price) * self.config["rr_min"] if side == "buy" else current_price - (sl_price - current_price) * self.config["rr_min"]
                    self.place_order(
                        side="sell" if side == "buy" else "buy",
                        order_type='limit',
                        amount=contracts,
                        price=tp_price,
                        params={'reduceOnly': True}
                    )

        self.state["last_bar_ts"] = str(df['timestamp'].iloc[-1])
        self._save_state()
        return signals

if __name__ == "__main__":
    symbol = os.getenv("SCALPER_SYMBOL", "BTC-USD")
    tf = os.getenv("SCALPER_TIMEFRAME", "5m")
    dry = os.getenv("DRY_RUN", "true").lower() == "true"
    engine = StrategyEngine(symbol, tf, dry)
    engine.run()