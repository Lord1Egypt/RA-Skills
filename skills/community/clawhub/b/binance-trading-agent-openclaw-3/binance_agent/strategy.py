from .config import SMA_FAST, SMA_SLOW, RSI_OVERBOUGHT, RSI_OVERSOLD

class TradingStrategy:
    def __init__(self, df):
        self.df = df

    def generate_signal(self):
        """วิเคราะห์ข้อมูลเพื่อสร้างสัญญาณซื้อขาย"""
        if len(self.df) < 2:
            return None

        last_row = self.df.iloc[-1]
        prev_row = self.df.iloc[-2]

        # เงื่อนไขสำหรับสัญญาณ Long
        # 1. SMA Fast ตัดขึ้นเหนือ SMA Slow
        # 2. RSI เริ่มกลับตัวขึ้นจากโซน Oversold
        # 3. MACD Line ตัดขึ้นเหนือ Signal Line
        long_condition = (
            prev_row['sma_fast'] <= prev_row['sma_slow'] and 
            last_row['sma_fast'] > last_row['sma_slow'] and
            last_row['rsi'] > RSI_OVERSOLD
        )

        # เงื่อนไขสำหรับสัญญาณ Short
        # 1. SMA Fast ตัดลงใต้ SMA Slow
        # 2. RSI เริ่มกลับตัวลงจากโซน Overbought
        # 3. MACD Line ตัดลงใต้ Signal Line
        short_condition = (
            prev_row['sma_fast'] >= prev_row['sma_slow'] and 
            last_row['sma_fast'] < last_row['sma_slow'] and
            last_row['rsi'] < RSI_OVERBOUGHT
        )

        if long_condition:
            return 'LONG'
        elif short_condition:
            return 'SHORT'
        else:
            return 'HOLD'

    def calculate_position_size(self, balance, current_price, risk_per_trade, leverage):
        """คำนวณขนาดไม้ (Quantity) โดยอิงจากความเสี่ยง"""
        risk_amount = balance * risk_per_trade
        # สมมติ Stop Loss ที่ 2% ของราคาปัจจุบัน (สามารถปรับเปลี่ยนได้ตามกลยุทธ์)
        stop_loss_pct = 0.02
        quantity = (risk_amount / (current_price * stop_loss_pct)) * leverage
        return round(quantity, 3)
