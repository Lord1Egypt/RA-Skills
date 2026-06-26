#!/usr/bin/env python3
"""
Technical Indicators Calculator
Calculates RSI, MACD, Moving Averages, Support/Resistance, ATR

Usage:
    python calculate_indicators.py --file data.json
    python calculate_indicators.py --file data.json --indicators rsi macd ma
"""

import argparse
import json
import sys
from typing import Dict, List, Optional, Tuple

import numpy as np


class TechnicalIndicators:
    """Calculate technical indicators from price data using numpy"""

    @staticmethod
    def _to_array(values: List[float]) -> np.ndarray:
        if not values:
            raise ValueError('Cannot process empty price series')
        return np.asarray(values, dtype=float)

    @staticmethod
    def _mean(values: List[float]) -> float:
        arr = TechnicalIndicators._to_array(values)
        return float(np.mean(arr))

    @staticmethod
    def _diff(values: List[float]) -> np.ndarray:
        arr = TechnicalIndicators._to_array(values)
        return np.diff(arr)

    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> Optional[float]:
        """
        Calculate Relative Strength Index (RSI)

        Args:
            prices: List of closing prices
            period: RSI period (default: 14)

        Returns:
            RSI value (0-100) or None if insufficient data
        """
        if len(prices) < period + 1:
            return None

        deltas = TechnicalIndicators._diff(prices)
        recent = deltas[-period:]
        gains = np.where(recent > 0, recent, 0.0)
        losses = np.where(recent < 0, -recent, 0.0)

        avg_gain = float(np.mean(gains))
        avg_loss = float(np.mean(losses))

        if avg_loss == 0:
            return 100.0

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(float(rsi), 2)

    @staticmethod
    def calculate_macd(
        prices: List[float],
        fast_period: int = 12,
        slow_period: int = 26,
        signal_period: int = 9,
    ) -> Optional[Dict]:
        """
        Calculate MACD (Moving Average Convergence Divergence)
        """
        minimum_points = slow_period + signal_period
        if len(prices) < minimum_points:
            return None

        fast_ema = TechnicalIndicators._calculate_ema_series(prices, fast_period)
        slow_ema = TechnicalIndicators._calculate_ema_series(prices, slow_period)

        valid_mask = ~np.isnan(fast_ema) & ~np.isnan(slow_ema)
        macd_values = fast_ema[valid_mask] - slow_ema[valid_mask]

        if macd_values.size < signal_period:
            return None

        signal_series = TechnicalIndicators._calculate_ema_series(macd_values.tolist(), signal_period)
        signal_values = signal_series[~np.isnan(signal_series)]
        if signal_values.size == 0:
            return None

        macd_line = float(macd_values[-1])
        signal_line = float(signal_values[-1])
        histogram = macd_line - signal_line

        return {
            'macd_line': round(macd_line, 2),
            'signal_line': round(signal_line, 2),
            'histogram': round(histogram, 2),
            'signal': 'bullish' if histogram > 0 else 'bearish',
            'crossover': 'bullish_cross' if macd_line > signal_line else 'bearish_cross'
        }

    @staticmethod
    def calculate_moving_averages(prices: List[float], periods: List[int] = [20, 50, 200]) -> Dict:
        """
        Calculate Simple and Exponential Moving Averages
        """
        result = {}
        arr = TechnicalIndicators._to_array(prices)

        for period in periods:
            if arr.size >= period:
                sma = float(np.mean(arr[-period:]))
                ema = TechnicalIndicators._calculate_ema(prices, period)
                if ema is None:
                    continue

                result[f'MA{period}'] = {
                    'sma': round(sma, 2),
                    'ema': round(ema, 2),
                }

        return result

    @staticmethod
    def calculate_support_resistance(
        highs: List[float],
        lows: List[float],
        current_price: float,
        num_levels: int = 3,
    ) -> Dict:
        """
        Calculate support and resistance levels based on recent highs/lows
        """
        high_arr = np.unique(TechnicalIndicators._to_array(highs))
        low_arr = np.unique(TechnicalIndicators._to_array(lows))

        resistance_candidates = np.sort(high_arr)[::-1]
        support_candidates = np.sort(low_arr)

        resistances = resistance_candidates[resistance_candidates > current_price][:num_levels]
        supports = support_candidates[support_candidates < current_price][-num_levels:]

        return {
            'resistance_levels': [round(float(r), 2) for r in resistances],
            'support_levels': [round(float(s), 2) for s in supports[::-1]],
            'current_price': round(current_price, 2),
        }

    @staticmethod
    def calculate_atr(
        highs: List[float],
        lows: List[float],
        closes: List[float],
        period: int = 14,
    ) -> Optional[float]:
        """
        Calculate Average True Range (ATR)
        """
        if len(highs) < period + 1 or len(lows) < period + 1 or len(closes) < period + 1:
            return None

        high_arr = TechnicalIndicators._to_array(highs)
        low_arr = TechnicalIndicators._to_array(lows)
        close_arr = TechnicalIndicators._to_array(closes)
        prev_close = close_arr[:-1]

        high_low = high_arr[1:] - low_arr[1:]
        high_close = np.abs(high_arr[1:] - prev_close)
        low_close = np.abs(low_arr[1:] - prev_close)
        true_ranges = np.maximum.reduce([high_low, high_close, low_close])

        atr = float(np.mean(true_ranges[-period:]))
        return round(atr, 2)

    @staticmethod
    def detect_trend(prices: List[float], period: int = 20) -> Dict:
        """
        Detect trend based on recent price action (HH/HL, LL/LH, or consolidation)
        """
        if len(prices) < period:
            period = len(prices)

        recent_prices = TechnicalIndicators._to_array(prices)[-period:]
        highs = []
        lows = []

        for i in range(1, len(recent_prices) - 1):
            if recent_prices[i] > recent_prices[i - 1] and recent_prices[i] > recent_prices[i + 1]:
                highs.append(float(recent_prices[i]))
            elif recent_prices[i] < recent_prices[i - 1] and recent_prices[i] < recent_prices[i + 1]:
                lows.append(float(recent_prices[i]))

        trend = 'consolidation'
        structure = 'sideways'

        if len(highs) >= 2 and len(lows) >= 2:
            higher_highs = all(highs[i] > highs[i - 1] for i in range(1, len(highs)))
            higher_lows = all(lows[i] > lows[i - 1] for i in range(1, len(lows)))
            lower_lows = all(lows[i] < lows[i - 1] for i in range(1, len(lows)))
            lower_highs = all(highs[i] < highs[i - 1] for i in range(1, len(highs)))

            if higher_highs and higher_lows:
                trend = 'uptrend'
                structure = 'HH/HL'
            elif lower_lows and lower_highs:
                trend = 'downtrend'
                structure = 'LL/LH'

        return {
            'trend': trend,
            'structure': structure,
            'recent_highs': [round(h, 2) for h in highs[-3:]],
            'recent_lows': [round(l, 2) for l in lows[-3:]],
        }

    @staticmethod
    def _calculate_ema(prices: List[float], period: int) -> Optional[float]:
        series = TechnicalIndicators._calculate_ema_series(prices, period)
        values = series[~np.isnan(series)]
        return float(values[-1]) if values.size else None

    @staticmethod
    def _calculate_ema_series(prices: List[float], period: int) -> np.ndarray:
        """
        Calculate full EMA series aligned with input prices.
        Values before enough history are NaN.
        """
        if period <= 0:
            raise ValueError('period must be positive')

        arr = np.asarray(prices, dtype=float)
        if arr.size < period:
            return np.full(arr.shape, np.nan, dtype=float)

        multiplier = 2.0 / (period + 1)
        ema_values = np.full(arr.shape, np.nan, dtype=float)
        ema = float(np.mean(arr[:period]))
        ema_values[period - 1] = ema

        for i in range(period, arr.size):
            ema = (float(arr[i]) - ema) * multiplier + ema
            ema_values[i] = ema

        return ema_values


def parse_input_data(data: Dict) -> Tuple[List[float], List[float], List[float], List[float]]:
    """
    Parse input JSON data and extract price arrays

    Args:
        data: Input data dictionary

    Returns:
        Tuple of (closes, highs, lows, volumes)
    """
    closes = []
    highs = []
    lows = []
    volumes = []

    if 'candles' in data:
        for candle in data['candles']:
            closes.append(float(candle['close']))
            highs.append(float(candle['high']))
            lows.append(float(candle['low']))
            volumes.append(float(candle.get('volume', 0)))

    elif 'hourly_data' in data and data['hourly_data']:
        for candle in data['hourly_data']:
            closes.append(float(candle['close']))
            highs.append(float(candle['high']))
            lows.append(float(candle['low']))
            volumes.append(float(candle.get('volume', 0)))

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                closes.append(float(item['close']))
                highs.append(float(item.get('high', item['close'])))
                lows.append(float(item.get('low', item['close'])))
                volumes.append(float(item.get('volume', 0)))

    return closes, highs, lows, volumes


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description='Calculate technical indicators from price data')
    parser.add_argument('--file', '-f', required=True, help='Input JSON file with price data')
    parser.add_argument(
        '--indicators', '-i', nargs='+',
        choices=['rsi', 'macd', 'ma', 'sr', 'atr', 'trend', 'all'],
        default=['all'],
        help='Indicators to calculate (default: all)'
    )
    parser.add_argument('--output', '-o', help='Output file (JSON). If not specified, prints to stdout')

    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)

        closes, highs, lows, volumes = parse_input_data(input_data)

        if not closes:
            print(json.dumps({'error': 'No price data found in input file'}), file=sys.stderr)
            sys.exit(1)

        current_price = closes[-1]
        result = {
            'current_price': round(current_price, 2),
            'data_points': len(closes),
        }

        indicators = args.indicators
        if 'all' in indicators:
            indicators = ['rsi', 'macd', 'ma', 'sr', 'atr', 'trend']

        calculator = TechnicalIndicators()

        if 'rsi' in indicators:
            rsi = calculator.calculate_rsi(closes)
            if rsi is not None:
                result['RSI'] = {
                    'value': rsi,
                    'interpretation': 'overbought' if rsi > 70 else 'oversold' if rsi < 30 else 'neutral'
                }

        if 'macd' in indicators:
            macd = calculator.calculate_macd(closes)
            if macd:
                result['MACD'] = macd

        if 'ma' in indicators:
            mas = calculator.calculate_moving_averages(closes)
            if mas:
                result['MovingAverages'] = mas
                result['PriceVsMA'] = {}
                for ma_name, ma_values in mas.items():
                    sma = ma_values['sma']
                    result['PriceVsMA'][ma_name] = {
                        'above': current_price > sma,
                        'distance_pct': round(((current_price - sma) / sma) * 100, 2) if sma else 0
                    }

        if 'sr' in indicators and highs and lows:
            sr = calculator.calculate_support_resistance(highs, lows, current_price)
            result['SupportResistance'] = sr

        if 'atr' in indicators and highs and lows:
            atr = calculator.calculate_atr(highs, lows, closes)
            if atr is not None:
                result['ATR'] = {
                    'value': atr,
                    'pct_of_price': round((atr / current_price) * 100, 2) if current_price else 0
                }

        if 'trend' in indicators:
            trend = calculator.detect_trend(closes)
            result['Trend'] = trend

        json_output = json.dumps(result, indent=2)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"Indicators saved to {args.output}", file=sys.stderr)
        else:
            print(json_output)

    except FileNotFoundError:
        print(json.dumps({'error': f'File not found: {args.file}'}), file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({'error': f'Invalid JSON in file: {args.file}'}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
