import pandas as pd
import datetime
from typing import Dict, List, Optional

class StockAnalyzer:
    def __init__(self, data_path: str = "finance/AAPL.csv"):
        self.df = pd.read_csv(data_path)
        # Normalize column names to lowercase
        self.df.columns = [c.strip().lower() for c in self.df.columns]
        # Clean up data
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["close"] = self.df["close"].replace(r'\$', '', regex=True).astype(float)
        self.df["open"] = self.df["open"].replace(r'\$', '', regex=True).astype(float)
        self.df["high"] = self.df["high"].replace(r'\$', '', regex=True).astype(float)
        self.df["low"] = self.df["low"].replace(r'\$', '', regex=True).astype(float)
        # Compute adjusted close for total return calculations
        # If adj_close column exists, use it; otherwise derive from close + dividends
        if "adj_close" in self.df.columns:
            self.df["adj_close"] = self.df["adj_close"].replace(r'\$', '', regex=True).astype(float)
        else:
            self.df["adj_close"] = self.df["close"].copy()
        # Track dividends if present (handle both 'dividend' and 'dividends')
        div_col = "dividends" if "dividends" in self.df.columns else "dividend"
        if div_col in self.df.columns:
            self.df["dividend"] = pd.to_numeric(self.df[div_col], errors="coerce").fillna(0)
        else:
            self.df["dividend"] = 0.0
        # Always sort newest-first (descending by date)
        self.df = self.df.sort_values("date", ascending=False).reset_index(drop=True)
        # Recompute adjusted close incorporating dividends
        self._recompute_adj_close()
        
    def get_latest_price(self) -> Dict:
        """Get latest stock price"""
        latest = self.df.iloc[0]
        return {
            "date": latest["date"].strftime("%Y-%m-%d"),
            "close": latest["close"],
            "open": latest["open"],
            "high": latest["high"],
            "low": latest["low"],
            "volume": latest["volume"]
        }
    
    def _recompute_adj_close(self):
        """Recompute adjusted close incorporating dividends for total return.

        Works backward from the latest date: each dividend reduces the
        adjustment factor for all earlier prices so that total return
        (adj_close gain) equals price return + reinvested dividend return.
        """
        # Data is sorted newest-first; work in chronological order
        df_asc = self.df.sort_values("date").reset_index(drop=True)
        adj = [df_asc.iloc[0]["close"]]
        factor = 1.0
        for i in range(1, len(df_asc)):
            div = df_asc.iloc[i]["dividend"]
            if div > 0:
                # On ex-div date, prior close drops by ~div amount;
                # adjustment factor shrinks earlier prices proportionally
                prev_close = df_asc.iloc[i - 1]["close"]
                factor *= (prev_close - div) / prev_close
            adj.append(df_asc.iloc[i]["close"] * factor)
        # Map back to original (descending) index
        adj_series = pd.Series(adj[::-1], index=self.df.index)
        self.df["adj_close"] = adj_series

    def calculate_returns(self, days: int = 30, use_adj: bool = True) -> float:
        """Calculate percentage total return over the past N days.

        Args:
            days: Number of trading days to look back.
            use_adj: If True, use adjusted close (includes dividends) for
                     total return. If False, use raw close (price return only).
        """
        if days >= len(self.df):
            days = len(self.df) - 1

        price_col = "adj_close" if use_adj else "close"
        current_price = self.df.iloc[0][price_col]
        past_price = self.df.iloc[days][price_col]

        return ((current_price - past_price) / past_price) * 100
    
    def generate_quarterly_report(self, quarter: int, year: int = 2026) -> Dict:
        """Generate quarterly performance report with total return."""
        # Filter data for the quarter
        start_month = (quarter - 1) * 3 + 1
        end_month = start_month + 2

        quarter_data = self.df[
            (self.df["date"].dt.year == year) &
            (self.df["date"].dt.month >= start_month) &
            (self.df["date"].dt.month <= end_month)
        ]

        if len(quarter_data) == 0:
            return {"error": "No data available for this quarter"}

        # Use adjusted close for total return (includes dividends)
        start_adj = quarter_data.iloc[-1]["adj_close"]
        end_adj = quarter_data.iloc[0]["adj_close"]
        total_return = ((end_adj - start_adj) / start_adj) * 100

        # Price return (raw close, no dividends)
        start_price = quarter_data.iloc[-1]["close"]
        end_price = quarter_data.iloc[0]["close"]
        price_return = ((end_price - start_price) / start_price) * 100

        # Dividends paid during quarter
        total_dividends = quarter_data["dividend"].sum()

        return {
            "quarter": f"Q{quarter} {year}",
            "start_date": quarter_data.iloc[-1]["date"].strftime("%Y-%m-%d"),
            "end_date": quarter_data.iloc[0]["date"].strftime("%Y-%m-%d"),
            "start_price": start_price,
            "end_price": end_price,
            "price_return_pct": round(price_return, 4),
            "total_return_pct": round(total_return, 4),
            "dividends_per_share": round(total_dividends, 6),
            "highest_price": quarter_data["high"].max(),
            "lowest_price": quarter_data["low"].min(),
            "average_volume": round(quarter_data["volume"].mean(), 0),
        }

if __name__ == "__main__":
    analyzer = StockAnalyzer()
    print("Latest AAPL Price:", analyzer.get_latest_price())
    print("30-Day Return:", f"{analyzer.calculate_returns(30):.2f}%")
    print("Q1 2026 Report:", analyzer.generate_quarterly_report(1, 2026))