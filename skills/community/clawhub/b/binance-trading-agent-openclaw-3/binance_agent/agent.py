import time
import logging
from .binance_client import BinanceFuturesClient
from .indicators import TechnicalIndicators
from .strategy import TradingStrategy
from .config import SYMBOL, TIMEFRAME, LEVERAGE, RISK_PER_TRADE

# ตั้งค่า Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BinanceTradingAgent:
    def __init__(self):
        self.api_client = BinanceFuturesClient()
        self.indicators = TechnicalIndicators()
        logger.info(f"Agent เริ่มต้นทำงานสำหรับคู่เทรด: {SYMBOL}")

    def run_once(self):
        """การทำงาน 1 รอบของ Agent"""
        try:
            # 1. ดึงข้อมูลแท่งเทียน
            klines = self.api_client.get_futures_klines(SYMBOL, TIMEFRAME)
            df = self.indicators.prepare_dataframe(klines)
            df = self.indicators.add_indicators(df)

            # 2. วิเคราะห์สัญญาณ
            strategy = TradingStrategy(df)
            signal = strategy.generate_signal()
            current_price = df.iloc[-1]['close']
            
            logger.info(f"ราคาปัจจุบัน {SYMBOL}: {current_price} | สัญญาณ: {signal}")

            # 3. ตรวจสอบสถานะปัจจุบัน
            position = self.api_client.get_futures_position(SYMBOL)
            has_position = float(position['positionAmt']) != 0 if position else False

            if signal == 'LONG' and not has_position:
                self.execute_trade('BUY', current_price)
            elif signal == 'SHORT' and not has_position:
                self.execute_trade('SELL', current_price)
            elif signal != 'HOLD' and has_position:
                # ตัวอย่าง: ปิดสถานะถ้าสัญญาณเปลี่ยน (สามารถปรับปรุงให้ซับซ้อนขึ้นได้)
                pos_amt = float(position['positionAmt'])
                if (signal == 'SHORT' and pos_amt > 0) or (signal == 'LONG' and pos_amt < 0):
                    logger.info(f"ปิดสถานะ {SYMBOL} เนื่องจากสัญญาณเปลี่ยน")
                    side = 'SELL' if pos_amt > 0 else 'BUY'
                    self.api_client.place_futures_order(SYMBOL, side, 'MARKET', abs(pos_amt))

        except Exception as e:
            logger.error(f"เกิดข้อผิดพลาดในการทำงาน: {e}")

    def execute_trade(self, side, current_price):
        """ดำเนินการส่งคำสั่งซื้อขาย"""
        try:
            account = self.api_client.get_futures_account()
            balance = float(account['totalWalletBalance'])
            
            strategy = TradingStrategy(None)
            quantity = strategy.calculate_position_size(balance, current_price, RISK_PER_TRADE, LEVERAGE)
            
            logger.info(f"ดำเนินการ {side} {SYMBOL} จำนวน {quantity} ที่ราคา {current_price}")
            
            # ปรับ Leverage ก่อนเทรด
            self.api_client.change_leverage(SYMBOL, LEVERAGE)
            
            # ส่งคำสั่ง Market Order
            order = self.api_client.place_futures_order(SYMBOL, side, 'MARKET', quantity)
            logger.info(f"ส่งคำสั่งสำเร็จ: {order['orderId']}")
            
        except Exception as e:
            logger.error(f"ไม่สามารถดำเนินการเทรดได้: {e}")

    def start_loop(self, interval_seconds=60):
        """รัน Agent แบบต่อเนื่อง"""
        logger.info(f"เริ่มรันระบบอัตโนมัติ (Interval: {interval_seconds} วินาที)")
        while True:
            self.run_once()
            time.sleep(interval_seconds)

if __name__ == "__main__":
    agent = BinanceTradingAgent()
    agent.start_loop()
