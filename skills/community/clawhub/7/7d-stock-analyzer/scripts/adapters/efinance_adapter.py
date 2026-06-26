"""
EFinance 数据适配器
"""

import pandas as pd
from typing import Optional, Dict, Any

try:
    import efinance as ef
except ImportError:
    ef = None


class EfinanceAdapter:
    """EFinance 适配器"""

    def __init__(self):
        """初始化适配器"""
        if ef is None:
            raise ImportError("efinance 未安装，请运行: pip install efinance")

    def get_realtime_quotes(self) -> pd.DataFrame:
        """获取实时行情"""
        return ef.stock.get_realtime_quotes()

    def get_base_info(self, symbol: str) -> Optional[Dict]:
        """获取基础信息"""
        try:
            # 通过行情数据获取基础信息
            quotes = self.get_realtime_quotes()
            symbol_df = quotes[quotes['股票代码'].astype(str) == symbol]

            if not symbol_df.empty:
                return symbol_df.iloc[0].to_dict()
            return None
        except Exception:
            return None

    def get_financial_data(self, symbol: str) -> Optional[Dict]:
        """获取财务数据"""
        try:
            # 获取历史K线数据（简化版财务数据）
            hist = ef.stock.get_quote_history(symbol)
            if hist is not None and not hist.empty:
                return hist.tail(5).to_dict('records')
            return None
        except Exception:
            return None

    def get_billboard(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """获取龙虎榜"""
        try:
            if start_date and end_date:
                return ef.stock.get_daily_billboard(start_date=start_date, end_date=end_date)
            return ef.stock.get_daily_billboard()
        except Exception:
            return pd.DataFrame()

    def get_sector_quotes(self) -> pd.DataFrame:
        """获取行业板块行情"""
        # efinance 可能没有直接的板块行情，这里返回空
        return pd.DataFrame()
