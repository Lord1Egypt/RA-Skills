"""
CMC Kline Data Collector Skill

从 CoinMarketCap 获取加密货币历史数据，计算技术指标（EMA7、EMA30、RSI14）
"""

import sys
from pathlib import Path

# 添加技能目录到路径
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from src.cmc_client import CMCClient
from src.data_processor import DataProcessor
from src.indicators import calc_indicators
from src.models import KlineData, Quote
from config import SYMBOL_TO_ID, OUTPUT_DIR, CONVERT_ID


class CMCKlineDataCollector:
    """CMC Kline Data Collector Skill 主类"""

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir) if output_dir else Path(OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.client = CMCClient()
        self.processor = DataProcessor(str(self.output_dir))

    def fetch_symbol(self, symbol: str, days: int = 35) -> dict:
        """
        获取单个币种的 K 线数据

        Args:
            symbol: 币种符号（ETH, SOL, BNB 等）
            days: 获取最近 N 天数据（默认 35 天，确保有足够数据计算指标）

        Returns:
            包含 OHLCV + 指标的字典
        """
        if symbol not in SYMBOL_TO_ID:
            raise ValueError(f"Unknown symbol: {symbol}. Available: {list(SYMBOL_TO_ID.keys())}")

        print(f"[CMC Kline] Fetching {symbol}...")
        kline = self.client.get_historical(symbol)

        # 确保有足够数据
        if len(kline.quotes) < 35:
            print(f"  Warning: Only {len(kline.quotes)} quotes, need 35+")

        # 计算指标
        kline = calc_indicators(kline)

        # 转换为输出格式
        return {
            symbol: [
                {
                    "O": float(q.open),
                    "H": float(q.high),
                    "L": float(q.low),
                    "C": float(q.close),
                    "E7": float(q.ema7) if q.ema7 else None,
                    "E30": float(q.ema30) if q.ema30 else None,
                    "R14": float(q.rsi14) if q.rsi14 else None,
                    "D": q.time_open[5:10].replace("-", "")  # MMDD 格式
                }
                for q in kline.quotes[-7:]  # 最近 7 天
            ]
        }

    def fetch_all(self, symbols: list = None) -> dict:
        """
        获取多个币种的 K 线数据

        Args:
            symbols: 币种列表（默认 ["ETH", "SOL", "BNB"]）

        Returns:
            包含所有币种数据的字典
        """
        if symbols is None:
            symbols = ["ETH", "SOL", "BNB"]

        results = {}
        for symbol in symbols:
            try:
                data = self.fetch_symbol(symbol)
                results.update(data)
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")

        return results

    def save_json(self, data: dict, filename: str = None) -> str:
        """保存为 JSON 文件"""
        return self.processor.save_json(
            type('KlineData', (), {
                'symbol': 'MULTI',
                'quotes': [],
                'to_json': lambda: data
            })(),
            filename
        )

    def save_csv(self, data: dict, symbol: str, filename: str = None) -> str:
        """保存单个币种为 CSV"""
        if symbol not in data:
            raise ValueError(f"Symbol {symbol} not in data")

        # 转为 KlineData 格式
        kline = type('KlineData', (), {
            'symbol': symbol,
            'quotes': []
        })()

        return self.processor.save_csv(kline, filename)


# 便捷函数
def fetch_eth(days: int = 35) -> dict:
    """快速获取 ETH 数据"""
    collector = CMCKlineDataCollector()
    return collector.fetch_symbol("ETH", days)


def fetch_all_daily() -> dict:
    """获取每日默认币种数据（ETH/SOL/BNB）"""
    collector = CMCKlineDataCollector()
    return collector.fetch_all()


def to_js_object(data: dict) -> str:
    """
    转为纯文本格式（无引号，保留 2 位小数）
    用于直接粘贴到 JS 代码中
    """
    def format_value(v, is_key=False):
        if isinstance(v, dict):
            items = ",".join(f"{k}:{format_value(v2)}" for k, v2 in v.items())
            return "{" + items + "}"
        elif isinstance(v, list):
            items = ",".join(format_value(item) for item in v)
            return "[" + items + "]"
        elif isinstance(v, (float, int)):
            return f"{v:.2f}"
        elif isinstance(v, str):
            return v  # 不加引号
        elif v is None:
            return "null"
        else:
            return str(v)

    return format_value(data)
