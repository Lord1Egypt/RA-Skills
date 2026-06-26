import os
from dotenv import load_dotenv

# .env 파일 로드 (config 디렉토리 내 .env 우선)
env_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path, override=True)
else:
    load_dotenv()

# ============================================================
# API Keys & Exchange Settings
# ============================================================
API_KEY = os.getenv("BINANCE_API_KEY", "")
API_SECRET = os.getenv("BINANCE_API_SECRET", "")
USE_TESTNET = os.getenv("USE_TESTNET", "false").lower() == "true"
EXCHANGE = "binance"

# Google Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

# Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_IDS = [id.strip() for id in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if id.strip()]
# 하위 호환성용 단일 ID
TELEGRAM_CHAT_ID = TELEGRAM_CHAT_IDS[0] if TELEGRAM_CHAT_IDS else ""

# 학습용 텔레그램 채널
TELEGRAM_LEARNING_CHANNELS = [
    "https://t.me/sweepzone"
]

# ============================================================
# Trading Parameters
# ============================================================
TIMEFRAME = "1d"
TARGET_COINS = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "XRP/USDT", "DOGE/USDT", "LINK/USDT"]

# 리스크 관리 (PositionRiskManager용)
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "2.0")) # 거래당 리스크 (%)
KELLY_FRACTION = 0.25      # 보수적 켈리 비율
MAX_KELLY_SIZE_PCT = 15.0  # 최대 포지션 비중 (%)
MAX_POSITION_SIZE = 25.0   # 계좌 대비 최대 포지션 (%)
MAX_TOTAL_EXPOSURE = 100.0 # 전체 포지션 최대 노출 (%)
MIN_POSITION_USDT = 15.0   # 최소 주문 증거금 ($)
SNIPER_MIN_POSITION_USDT = 80.0 # 스나이퍼 모드 최소 증거금 ($)

# 레버리지 설정
DEFAULT_LEVERAGE = 10
LEVERAGE_CONF_THRESH_HIGH = 0.85 # 고신뢰도 기준
ALT_LEVERAGE_CONF_HIGH = 20      # 고신뢰도 시 레버리지

# 매매 자동화 설정
AUTO_TRADE_ENABLED = os.getenv("AUTO_TRADE_ENABLED", "false").lower() == "true"
AUTO_TRADE_MIN_CONFIDENCE = 0.70 # 자동 매매 진입 최소 신뢰도
DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"

# ============================================================
# Charting & Logging
# ============================================================
CHART_CANDLES = 60
CHART_DPI = 100
CHART_FIGSIZE = (12, 7)
CHART_TF = "1h"

LOG_FILE = "logs/bot.log"
MA_PERIOD = 20
ICHIMOKU_PERIODS = {
    'tenkan': 9,
    'kijun': 26,
    'senkou_b': 52,
    'displacement': 26
}

# ============================================================
# Backtest Parameters
# ============================================================
BACKTEST_INITIAL_CAPITAL = 1000.0
BACKTEST_COMMISSION = 0.0004 # 0.04% (Taker 기준)
BACKTEST_SLIPPAGE = 0.0002   # 0.02%
BACKTEST_SPREAD = 0.0001     # 0.01%

