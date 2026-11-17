import os

# Binance API Configuration
# สำหรับการใช้งานจริง ควรตั้งค่าผ่าน Environment Variables
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', 'YOUR_API_KEY')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', 'YOUR_API_SECRET')

# Trading Parameters
SYMBOL = 'BTCUSDT'
TIMEFRAME = '1h'
LEVERAGE = 10
RISK_PER_TRADE = 0.01  # 1% of account balance

# Technical Indicators Parameters
SMA_FAST = 50
SMA_SLOW = 200
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# API Endpoints
FUTURES_TESTNET = True # ตั้งค่าเป็น True สำหรับการทดสอบบน Testnet
