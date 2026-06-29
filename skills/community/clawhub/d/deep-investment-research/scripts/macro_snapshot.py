"""macro_snapshot.py — 宏观数据快照（yfinance）

使用 yfinance 获取关键宏观指标，避免 FRED API 在中国大陆的连接问题。
"""
import os, json, sys, time
import yfinance as yf

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

# Yahoo Finance tickers for macro indicators
MACRO_TICKERS = {
    "^TNX": "10-Year Treasury Rate",
    "^FVX": "5-Year Treasury Rate",
    "^TYX": "30-Year Treasury Rate",
    "^IRX": "13-Week Treasury Bill",
    "^VIX": "CBOE Volatility Index",
    "DX-Y.NYB": "US Dollar Index (DXY)",
    "GC=F": "Gold Futures",
    "CL=F": "Crude Oil WTI",
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ Composite",
}


class Fetcher(BaseFetcher):
    name = "macro_snapshot"

    def fetch_raw(self):
        tickers_list = list(MACRO_TICKERS.keys())
        try:
            data = yf.download(tickers_list, period="5d", progress=False, threads=True)
            if data.empty:
                return None

            results = {}
            close = data["Close"]
            for ticker, desc in MACRO_TICKERS.items():
                if ticker in close.columns:
                    series = close[ticker].dropna()
                    if len(series) >= 1:
                        latest_val = series.iloc[-1]
                        prev_val = series.iloc[-2] if len(series) >= 2 else None
                        results[ticker] = {
                            "description": desc,
                            "latest_value": round(float(latest_val), 4),
                            "latest_date": str(series.index[-1].date()),
                            "previous_value": round(float(prev_val), 4) if prev_val is not None else None,
                            "change": round(float(latest_val - prev_val), 4) if prev_val is not None else None,
                            "change_pct": round(float((latest_val - prev_val) / prev_val * 100), 2) if prev_val is not None and prev_val != 0 else None,
                        }

            if not results:
                return None
            return json.dumps(results, ensure_ascii=False)

        except Exception as e:
            # Fallback: return None to signal fetch failure
            return None

    def parse(self, raw):
        data = json.loads(raw)
        records = []
        for ticker, info in data.items():
            records.append({
                "ticker": ticker,
                "description": info.get("description", ""),
                "latest_value": info.get("latest_value"),
                "latest_date": info.get("latest_date"),
                "previous_value": info.get("previous_value"),
                "change": info.get("change"),
                "change_pct": info.get("change_pct"),
            })
        return records

    def validate(self, records):
        if not records:
            raise ValueError("No macro data retrieved")
        # Must have at least TNX and VIX
        tickers_got = {r["ticker"] for r in records}
        required = {"^TNX", "^VIX"}
        missing = required - tickers_got
        if missing:
            raise ValueError(f"Missing critical indicators: {missing}")


if __name__ == "__main__":
    f = Fetcher()
    result = f.run()
    print(f"Status: {result.status}")
    print(f"Records: {result.records}")
    if result.reason:
        print(f"Error: {result.reason}")
    if result.data:
        for item in result.data:
            desc = item.get('description', '')
            val = item.get('latest_value', '')
            chg = item.get('change_pct', '')
            print(f"  {desc}: {val} ({chg}%)")
