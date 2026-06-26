"""
Data Models
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class Quote:
    """单条价格数据"""

    time_open: str
    time_close: str
    time_high: str
    time_low: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    market_cap: float
    circulating_supply: float
    timestamp: str

    @property
    def open_datetime(self) -> datetime:
        """开盘时间（datetime）"""
        # 兼容不同 Python 版本
        ts_str = self.time_open.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(ts_str)
        except (AttributeError, ValueError):
            # 旧版本 Python 不支持 fromisoformat，手动解析
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(ts_str)

    @property
    def open_timestamp(self) -> int:
        """开盘时间戳（秒）"""
        return int(self.open_datetime.timestamp())

    def to_dict(self) -> Dict:
        """转为字典"""
        return {
            "time_open": self.time_open,
            "time_close": self.time_close,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "market_cap": self.market_cap,
        }


@dataclass
class KlineData:
    """K 线数据集合"""

    symbol: str
    currency_id: int
    quotes: List[Quote]

    def filter_by_date(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> "KlineData":
        """按日期过滤"""
        filtered = self.quotes

        if start_date:
            try:
                start_ts = datetime.fromisoformat(start_date).timestamp()
            except (AttributeError, ValueError):
                start_ts = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
            filtered = [q for q in filtered if q.open_timestamp >= start_ts]

        if end_date:
            try:
                end_ts = datetime.fromisoformat(end_date).timestamp()
            except (AttributeError, ValueError):
                end_ts = datetime.strptime(end_date, "%Y-%m-%d").timestamp()
            filtered = [q for q in filtered if q.open_timestamp <= end_ts]

        return KlineData(symbol=self.symbol, currency_id=self.currency_id, quotes=filtered)

    def filter_by_days(self, days: int) -> "KlineData":
        """获取最近 N 天数据"""
        if not self.quotes:
            return self

        # 从最新的数据往前推 N 天
        latest = self.quotes[-1].open_datetime
        cutoff = latest.timestamp() - (days * 24 * 60 * 60)

        filtered = [q for q in self.quotes if q.open_timestamp >= cutoff]
        return KlineData(symbol=self.symbol, currency_id=self.currency_id, quotes=filtered)

    def to_csv_rows(self) -> List[List]:
        """转为 CSV 行数据"""
        rows: List[List] = [["time", "open", "high", "low", "close", "volume", "market_cap"]]
        for q in self.quotes:
            rows.append(
                [
                    q.time_open[:10],  # 只要日期部分
                    q.open,
                    q.high,
                    q.low,
                    q.close,
                    q.volume,
                    q.market_cap,
                ]
            )
        return rows

    def to_json(self) -> Dict:
        """转为 JSON 格式"""
        return {
            "symbol": self.symbol,
            "currency_id": self.currency_id,
            "count": len(self.quotes),
            "quotes": [q.to_dict() for q in self.quotes],
        }
