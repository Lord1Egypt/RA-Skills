"""
Crypto Data Processor Configuration
"""

# CMC API 配置
CMC_BASE_URL = "https://api.coinmarketcap.com/data-api/v3.1"

# 计价货币 ID: 2781 = USD
CONVERT_ID = 2781

# 币种 ID 映射
SYMBOL_TO_ID = {
    "BTC": 1,
    "ETH": 1027,
    "BNB": 1839,
    "SOL": 5426,
    "XRP": 52,
    "ADA": 2010,
    "DOGE": 74,
}

# 默认获取天数（CMC API 返回所有历史，我们默认过滤最近 N 天）
DEFAULT_DAYS = 90

# 输出目录
OUTPUT_DIR = "output"
