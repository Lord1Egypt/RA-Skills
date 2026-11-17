from binance.client import Client
from .config import BINANCE_API_KEY, BINANCE_API_SECRET, FUTURES_TESTNET

class BinanceFuturesClient:
    def __init__(self):
        self.client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=FUTURES_TESTNET)

    def get_futures_account(self):
        """ดึงข้อมูลบัญชี Futures"""
        return self.client.futures_account()

    def get_futures_klines(self, symbol, interval, limit=500):
        """ดึงข้อมูลแท่งเทียน (Kline) ย้อนหลัง"""
        return self.client.futures_klines(symbol=symbol, interval=interval, limit=limit)

    def place_futures_order(self, symbol, side, order_type, quantity, price=None, stopPrice=None):
        """ส่งคำสั่งซื้อขาย Futures"""
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        if price:
            params['price'] = price
        if stopPrice:
            params['stopPrice'] = stopPrice
            
        return self.client.futures_create_order(**params)

    def get_futures_position(self, symbol):
        """ดึงข้อมูลสถานะ (Position) ปัจจุบัน"""
        positions = self.client.futures_position_information()
        for pos in positions:
            if pos['symbol'] == symbol:
                return pos
        return None

    def change_leverage(self, symbol, leverage):
        """เปลี่ยน Leverage"""
        return self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
