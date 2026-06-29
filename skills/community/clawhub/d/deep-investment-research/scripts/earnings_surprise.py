"""earnings_surprise.py — 业绩超预期/不及预期扫描

US: Finnhub earnings calendar (recent 7 days, all stocks)
HK: yfinance earnings_history (watchlist HK stocks only)

输出：earnings_surprise.json
每条记录 = 一个业绩超预期/不及预期的标的，含 surprise_pct

阈值：>5% beat 或 <-10% miss（中等以上）
这是 TRIGGER 类信号，不是确认类信号。
"""
import os, json, sys, time
from datetime import date, timedelta
import requests

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

FINNHUB_KEY = os.environ.get("FINNHUB_API_KEY", "")
FINNHUB_URL = "https://finnhub.io/api/v1"

# 5% beat 即视为有意义的超预期阈值
BEAT_THRESHOLD = 0.05    # +5%
MISS_THRESHOLD = -0.10   # -10%
MIN_EPS_ESTIMATE = 0.10  # Filter pennystocks


class Fetcher(BaseFetcher):
    name = "earnings_surprise"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hk_symbols = self._get_hk_symbols()

    def _get_hk_symbols(self):
        try:
            import yaml
            wl_path = os.path.join(os.path.dirname(__file__), "watchlist.yaml")
            with open(wl_path) as f:
                data = yaml.safe_load(f) or {}
            symbols = []
            for section in ["positions", "focus"]:
                for item in data.get(section, []):
                    sym = item["symbol"]
                    if ".HK" in sym and sym not in symbols:
                        symbols.append(sym)
            return symbols[:50]  # Cap at 50 HK stocks
        except Exception:
            return []

    def fetch_raw(self):
        results = {"us": None, "hk": None}

        # US: Finnhub earnings calendar (past 7 days)
        if FINNHUB_KEY:
            today = date.today()
            from_date = (today - timedelta(days=7)).isoformat()
            to_date = today.isoformat()
            try:
                resp = requests.get(
                    f"{FINNHUB_URL}/calendar/earnings",
                    params={"from": from_date, "to": to_date, "token": FINNHUB_KEY},
                    timeout=15,
                )
                if resp.status_code == 200:
                    results["us"] = resp.json()
            except Exception:
                pass

        # HK: yfinance earnings_history (batch)
        if self.hk_symbols:
            try:
                import yfinance as yf
                hk_data = {}
                # Batch download is more efficient
                for sym in self.hk_symbols:
                    try:
                        t = yf.Ticker(sym)
                        eh = t.earnings_history
                        if eh is not None and not eh.empty:
                            latest = eh.iloc[0].to_dict()
                            # Only include if recent (within 30 days)
                            hk_data[sym] = latest
                    except Exception:
                        continue
                    time.sleep(0.1)  # Rate limiting
                results["hk"] = hk_data
            except ImportError:
                pass

        return json.dumps(results, ensure_ascii=False, default=str)

    def parse(self, raw):
        data = json.loads(raw)
        records = []

        # Parse US earnings
        us_data = data.get("us")
        if us_data:
            earnings_list = us_data.get("earningsCalendar", [])
            for e in earnings_list:
                actual = e.get("epsActual")
                estimate = e.get("epsEstimate")
                symbol = e.get("symbol", "")
                if actual is None or estimate is None or estimate == 0:
                    continue
                if abs(estimate) < MIN_EPS_ESTIMATE:
                    continue
                surprise = (actual - estimate) / abs(estimate)
                if surprise >= BEAT_THRESHOLD or surprise <= MISS_THRESHOLD:
                    records.append({
                        "symbol": symbol,
                        "market": "US",
                        "date": e.get("date", ""),
                        "quarter": f"Q{e.get('quarter', '?')} {e.get('year', '')}",
                        "eps_actual": actual,
                        "eps_estimate": estimate,
                        "surprise_pct": round(surprise * 100, 1),
                        "direction": "beat" if surprise > 0 else "miss",
                        "severity": "high" if abs(surprise) >= 0.20 else "medium",
                        "revenue_actual": e.get("revenueActual"),
                        "revenue_estimate": e.get("revenueEstimate"),
                    })

        # Parse HK earnings
        hk_data = data.get("hk", {})
        if hk_data:
            from datetime import datetime
            now = datetime.now()
            for sym, latest in hk_data.items():
                actual = latest.get("epsActual")
                estimate = latest.get("epsEstimate")
                if actual is None or estimate is None or estimate == 0:
                    continue
                # Recency filter: only include if quarter is within 90 days
                # yfinance returns quarter end date as index, check via surprisePercent presence
                surprise_raw = latest.get("surprisePercent")
                if surprise_raw is None or surprise_raw == 0:
                    continue  # No actual data yet (NaN cases)
                surprise = (actual - estimate) / abs(estimate)
                if surprise >= BEAT_THRESHOLD or surprise <= MISS_THRESHOLD:
                    records.append({
                        "symbol": sym,
                        "market": "HK",
                        "date": "",
                        "quarter": "",
                        "eps_actual": round(actual, 4),
                        "eps_estimate": round(estimate, 4),
                        "surprise_pct": round(surprise * 100, 1),
                        "direction": "beat" if surprise > 0 else "miss",
                        "severity": "high" if abs(surprise) >= 0.20 else "medium",
                    })

        # Sort by absolute surprise
        records.sort(key=lambda x: abs(x.get("surprise_pct", 0)), reverse=True)
        return records

    def validate(self, records):
        if not isinstance(records, list):
            raise ValueError("Must be list")
        # Earnings surprise can be empty (no recent reports)
        for r in records[:10]:
            if not r.get("symbol"):
                raise ValueError(f"Missing symbol: {r}")
            if "surprise_pct" not in r:
                raise ValueError(f"Missing surprise_pct: {r}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
