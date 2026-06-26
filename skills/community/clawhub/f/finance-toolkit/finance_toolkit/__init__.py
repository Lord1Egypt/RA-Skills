"""
A股量化工具包 (Finance Toolkit)

基于腾讯行情API的A股量化分析工具包。
零外部依赖即可获取实时行情和计算技术指标。
"""

__version__ = "1.0.0"
__all__ = [
    "TencentStockAPI", "AStockEngine", "AStockDataFetcher",
    "AStockStrategies", "BacktestEngine", "BacktestReport",
    "score_stock", "monitor_all",
    "analyze_spectrum", "get_strategy_hints",
]

from .mini_realtime import TencentStockAPI, calc_sma, calc_rsi, calc_kdj, calc_macd
from .fourier_analyzer import analyze_spectrum, get_strategy_hints
