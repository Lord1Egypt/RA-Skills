import pandas as pd
import pandas_ta as ta

class TechnicalIndicators:
    @staticmethod
    def add_indicators(df):
        """เพิ่มตัวชี้วัดทางเทคนิคลงใน DataFrame"""
        # คำนวณ Simple Moving Averages (SMA)
        df['sma_fast'] = ta.sma(df['close'], length=50)
        df['sma_slow'] = ta.sma(df['close'], length=200)
        
        # คำนวณ Relative Strength Index (RSI)
        df['rsi'] = ta.rsi(df['close'], length=14)
        
        # คำนวณ MACD
        macd = ta.macd(df['close'])
        df = pd.concat([df, macd], axis=1)
        
        return df

    @staticmethod
    def prepare_dataframe(klines):
        """แปลงข้อมูล Kline เป็น DataFrame และจัดการรูปแบบข้อมูล"""
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # แปลงข้อมูลเป็นตัวเลข
        numeric_cols = ['open', 'high', 'low', 'close', 'volume']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
        
        # แปลง timestamp เป็น datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
