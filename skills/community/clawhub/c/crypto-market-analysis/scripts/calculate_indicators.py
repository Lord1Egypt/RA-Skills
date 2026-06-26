import pandas as pd
import numpy as np
import json
import sys
import talib

def calculate_all_indicators(klines_data):
    print("Starting calculate_all_indicators...", file=sys.stderr)
    # print(f"Klines Data received: {json.dumps(klines_data[:2])}", file=sys.stderr) # Print first 2 klines for sanity check

    df = pd.DataFrame(klines_data)
    
    # Ensure numerical types
    try:
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')
        df['open'] = pd.to_numeric(df['open'])
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['close'] = pd.to_numeric(df['close'])
        df['volume'] = pd.to_numeric(df['volume'])
        df = df.set_index('open_time') # Set open_time as index for time series operations
        print(f"DataFrame head after type conversion:\n{df.head()}", file=sys.stderr)
        print(f"DataFrame dtypes:\n{df.dtypes}", file=sys.stderr)
    except Exception as e:
        print(f"Error in DataFrame type conversion or index setting: {e}", file=sys.stderr)
        raise # Re-raise to propagate the error

    close = df['close'].values
    high = df['high'].values
    low = df['low'].values
    open_price = df['open'].values
    
    indicators = {}
    print(f"Number of data points: {len(df)}", file=sys.stderr)

    # MACD (12,26,9,close)
    if len(close) >= 26: # MACD needs at least slowperiod
        macd, macdsignal, macdhist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        if not np.isnan(macd[-1]):
            indicators['MACD'] = {'MACD': round(macd[-1], 2), 'DIFF': round(macdsignal[-1], 2), 'DEA': round(macdhist[-1], 2)}
        else:
            indicators['MACD'] = {'MACD': None, 'DIFF': None, 'DEA': None}
        print(f"MACD calculated: {indicators.get('MACD')}", file=sys.stderr)
    else:
        indicators['MACD'] = {'MACD': None, 'DIFF': None, 'DEA': None}
        print("Not enough data for MACD calculation.", file=sys.stderr)

    # KDJ(14,3,3) - Using STOCH for K and D, then calculate J
    if len(high) >= 14: # STOCH needs at least fastk_period for calculation
        fastk, fastd = talib.STOCH(high, low, close, fastk_period=14, slowk_period=3, slowd_period=3)
        if not np.isnan(fastk[-1]):
            k_value = round(fastk[-1], 2)
            d_value = round(fastd[-1], 2)
            j_value = round(3 * d_value - 2 * k_value, 2) # J = 3D - 2K
            indicators['KDJ'] = {'K': k_value, 'D': d_value, 'J': j_value}
        else:
            indicators['KDJ'] = {'K': None, 'D': None, 'J': None}
        print(f"KDJ calculated: {indicators.get('KDJ')}", file=sys.stderr)
    else:
        indicators['KDJ'] = {'K': None, 'D': None, 'J': None}
        print("Not enough data for KDJ calculation.", file=sys.stderr)


    # RSI (close,6,12,24)
    if len(close) >= 24: # Need enough data for largest period
        rsi6 = talib.RSI(close, timeperiod=6)
        rsi12 = talib.RSI(close, timeperiod=12)
        rsi24 = talib.RSI(close, timeperiod=24)
        indicators['RSI'] = {
            'RSI_6': round(rsi6[-1], 2) if not np.isnan(rsi6[-1]) else None,
            'RSI_12': round(rsi12[-1], 2) if not np.isnan(rsi12[-1]) else None,
            'RSI_24': round(rsi24[-1], 2) if not np.isnan(rsi24[-1]) else None
        }
        print(f"RSI calculated: {indicators.get('RSI')}", file=sys.stderr)
    else:
        indicators['RSI'] = {'RSI_6': None, 'RSI_12': None, 'RSI_24': None}
        print("Not enough data for RSI calculation.", file=sys.stderr)

    # CCI(20)
    if len(high) >= 20:
        cci = talib.CCI(high, low, close, timeperiod=20)
        indicators['CCI'] = round(cci[-1], 2) if not np.isnan(cci[-1]) else None
        print(f"CCI calculated: {indicators.get('CCI')}", file=sys.stderr)
    else:
        indicators['CCI'] = None
        print("Not enough data for CCI calculation.", file=sys.stderr)

    # BOLL (20,2,close)
    if len(close) >= 20:
        upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
        indicators['BOLL'] = {
            'Upper': round(upperband[-1], 2) if not np.isnan(upperband[-1]) else None,
            'Middle': round(middleband[-1], 2) if not np.isnan(middleband[-1]) else None,
            'Lower': round(lowerband[-1], 2) if not np.isnan(lowerband[-1]) else None
        }
        print(f"BOLL calculated: {indicators.get('BOLL')}", file=sys.stderr)
    else:
        indicators['BOLL'] = {'Upper': None, 'Middle': None, 'Lower': None}
        print("Not enough data for BOLL calculation.", file=sys.stderr)

    # WR(9) - Williams %R
    if len(high) >= 9:
        wr = talib.WILLR(high, low, close, timeperiod=9)
        indicators['WR'] = round(wr[-1], 2) if not np.isnan(wr[-1]) else None
        print(f"WR calculated: {indicators.get('WR')}", file=sys.stderr)
    else:
        indicators['WR'] = None
        print("Not enough data for WR calculation.", file=sys.stderr)

    # PSY (12,6) - Psychological Line
    def calculate_psy_series(data, period):
        closes = pd.Series(data)
        changes = closes.diff()
        ups = (changes > 0).astype(int)
        
        psy_values = [np.nan] * (period - 1)
        for i in range(period - 1, len(ups)):
            psy_values.append((ups[i - period + 1 : i + 1].sum() / period) * 100)
        return pd.Series(psy_values)

    psy12_series = calculate_psy_series(close, 12)
    psy6_series = calculate_psy_series(close, 6)
    indicators['PSY'] = {
        'PSY_12': round(psy12_series.iloc[-1], 2) if not np.isnan(psy12_series.iloc[-1]) else None,
        'PSY_6': round(psy6_series.iloc[-1], 2) if not np.isnan(psy6_series.iloc[-1]) else None
    }
    print(f"PSY calculated: {indicators.get('PSY')}", file=sys.stderr)
    
    # BRAR (26) - BR (Buying Ratio) and AR (Selling Ratio)
    if len(df) >= 27: # Need at least N+1 data points for prev_close + N periods
        prev_close_series = df['close'].shift(1)
        
        # Calculate BR
        br_num = (df['high'] - prev_close_series).apply(lambda x: max(0, x))
        br_den = (prev_close_series - df['low']).apply(lambda x: max(0, x))
        
        br_values = [np.nan] * (26)
        for i in range(26, len(df)):
            num_sum = br_num.iloc[i-26+1 : i+1].sum()
            den_sum = br_den.iloc[i-26+1 : i+1].sum()
            br_values.append(round((num_sum / den_sum * 100), 2) if den_sum != 0 else np.nan)
        br_series = pd.Series(br_values)

        # Calculate AR
        ar_num = df['high'] - df['open']
        ar_den = df['open'] - df['low']

        ar_values = [np.nan] * (26)
        for i in range(26, len(df)):
            num_sum = ar_num.iloc[i-26+1 : i+1].sum()
            den_sum = ar_den.iloc[i-26+1 : i+1].sum()
            ar_values.append(round((num_sum / den_sum * 100), 2) if den_sum != 0 else np.nan)
        ar_series = pd.Series(ar_values)

        indicators['BRAR'] = {
            'BR': br_series.iloc[-1] if not np.isnan(br_series.iloc[-1]) else None,
            'AR': ar_series.iloc[-1] if not np.isnan(ar_series.iloc[-1]) else None
        }
        print(f"BRAR calculated: {indicators.get('BRAR')}", file=sys.stderr)
    else:
        indicators['BRAR'] = {'BR': None, 'AR': None}
        print("Not enough data for BRAR calculation.", file=sys.stderr)

    # DMI (14,6) - ADX, DI+, DI-
    if len(high) >= 14: # ADX needs at least timeperiod
        adx, minus_di, plus_di = talib.ADX(high, low, close, timeperiod=14)
        indicators['DMI'] = {
            'ADX': round(adx[-1], 2) if not np.isnan(adx[-1]) else None,
            'DI_Minus': round(minus_di[-1], 2) if not np.isnan(minus_di[-1]) else None,
            'DI_Plus': round(plus_di[-1], 2) if not np.isnan(plus_di[-1]) else None
        }
        print(f"DMI calculated: {indicators.get('DMI')}", file=sys.stderr)
    else:
        indicators['DMI'] = {'ADX': None, 'DI_Minus': None, 'DI_Plus': None}
        print("Not enough data for DMI calculation.", file=sys.stderr)

    print("Finished calculate_all_indicators.", file=sys.stderr)
    return indicators

if __name__ == "__main__":
    if sys.stdin.isatty():
        print(json.dumps({"error": "This script expects Klines data via stdin. Usage: cat klines.json | py calculate_indicators.py"}))
        sys.exit(1)
    
    try:
        klines_data = json.load(sys.stdin)
        if not isinstance(klines_data, list):
            raise ValueError("Input JSON must be a list of kline objects.")
        
        calculated_indicators = calculate_all_indicators(klines_data)
        print(json.dumps(calculated_indicators))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input."}))
        sys.exit(1)
    except ValueError as ve:
        print(json.dumps({"error": str(ve)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"An unexpected error occurred: {e}"}))
        sys.exit(1)