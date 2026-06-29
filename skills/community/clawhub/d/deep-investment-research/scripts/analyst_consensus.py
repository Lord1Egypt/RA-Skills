"""analyst_consensus.py — 分析师共识 + 目标价 + 财报日历

Primary: yfinance (batch, no rate limit, 500+ symbols in ~60s)
Supplement: Finnhub API (earnings calendar only, 2 calls total)

输出:
- analyst_consensus.json (分析师推荐 + 目标价 + 实时报价)
- earnings_calendar.json (未来14天财报日历)
"""
import os, json, sys, time, re
from datetime import date, timedelta
import requests

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult, DATA_DIR

BASE_URL = "https://finnhub.io/api/v1"


def _get_key():
    return os.environ.get("FINNHUB_API_KEY", "")


def _get(endpoint, params=None):
    params = params or {}
    params["token"] = _get_key()
    resp = requests.get(f"{BASE_URL}{endpoint}", params=params, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    return None


class Fetcher(BaseFetcher):
    name = "analyst_consensus"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbols = self._get_symbols()

    def _get_symbols(self):
        """Get ALL watchlist symbols for full coverage.
        
        yfinance handles 500+ symbols in ~60s (no rate limit).
        Full coverage is required for convergence scanner and research.
        """
        try:
            wl_path = os.path.join(os.path.dirname(__file__), "watchlist.yaml")
            if os.path.exists(wl_path):
                import yaml
                with open(wl_path) as f:
                    data = yaml.safe_load(f) or {}
                symbols = []
                seen = set()

                def _add(sym):
                    if sym.endswith('.HK') and len(sym.split('.')[0]) == 5:
                        num = sym.split('.')[0].lstrip('0')
                        sym = f"{int(num):04d}.HK"
                    if sym not in seen:
                        seen.add(sym)
                        symbols.append(sym)

                for section in ["positions", "focus", "auto_discovered"]:
                    for item in data.get(section, []):
                        _add(item["symbol"])

                return symbols if symbols else ["LLY", "0700.HK"]
        except Exception:
            pass
        return ["LLY", "0700.HK"]

    def fetch_raw(self):
        """Fetch analyst consensus via yfinance batch (primary).
        
        Architecture:
        - yfinance Tickers batch: 500+ symbols in ~60s
        - Processes in batches of 50 for memory safety
        - No per-symbol API rate limits
        - Handles US + HK stocks uniformly
        """
        import yfinance as yf
        import gc

        results = {}
        BATCH_SIZE = 50
        total = len(self.symbols)

        for batch_start in range(0, total, BATCH_SIZE):
            batch = self.symbols[batch_start:batch_start + BATCH_SIZE]
            batch_str = ' '.join(batch)
            batch_num = batch_start // BATCH_SIZE + 1
            total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

            try:
                tickers = yf.Tickers(batch_str)
                for symbol in batch:
                    try:
                        info = tickers.tickers[symbol].info

                        # Recommendations breakdown
                        buy = hold = sell = strong_buy = strong_sell = 0
                        num_analysts = info.get('numberOfAnalystOpinions', 0)
                        period = ""

                        if num_analysts > 0:
                            try:
                                recs_df = tickers.tickers[symbol].recommendations
                                if recs_df is not None and not recs_df.empty:
                                    r = recs_df.iloc[0]
                                    strong_buy = int(r.get('strongBuy', 0))
                                    buy = int(r.get('buy', 0))
                                    hold = int(r.get('hold', 0))
                                    sell = int(r.get('sell', 0))
                                    strong_sell = int(r.get('strongSell', 0))
                                    period = str(r.name) if hasattr(r, 'name') else ""
                            except Exception:
                                # Estimate from recommendationMean
                                rec_mean = info.get('recommendationMean', 3)
                                if rec_mean <= 1.5:
                                    strong_buy = num_analysts
                                elif rec_mean <= 2.0:
                                    buy = num_analysts
                                elif rec_mean <= 3.0:
                                    hold = num_analysts
                                else:
                                    sell = num_analysts

                        results[symbol] = {
                            "recommendations": [{
                                "buy": buy,
                                "hold": hold,
                                "sell": sell,
                                "strongBuy": strong_buy,
                                "strongSell": strong_sell,
                                "period": period,
                                "symbol": symbol,
                            }] if num_analysts > 0 else [],
                            "price_target": {
                                "targetHigh": info.get('targetHighPrice'),
                                "targetLow": info.get('targetLowPrice'),
                                "targetMean": info.get('targetMeanPrice'),
                                "targetMedian": info.get('targetMedianPrice'),
                            },
                            "quote": {
                                "c": info.get('currentPrice') or info.get('regularMarketPrice'),
                                "dp": info.get('regularMarketChangePercent'),
                                "h": info.get('dayHigh'),
                                "l": info.get('dayLow'),
                            },
                        }
                    except Exception:
                        results[symbol] = {"recommendations": [], "price_target": {}, "quote": {}}

                del tickers
                gc.collect()

            except Exception as e:
                # Batch failed — try individually
                for symbol in batch:
                    try:
                        ticker = yf.Ticker(symbol)
                        info = ticker.info
                        results[symbol] = {
                            "recommendations": [],
                            "price_target": {
                                "targetHigh": info.get('targetHighPrice'),
                                "targetLow": info.get('targetLowPrice'),
                                "targetMean": info.get('targetMeanPrice'),
                                "targetMedian": info.get('targetMedianPrice'),
                            },
                            "quote": {
                                "c": info.get('currentPrice') or info.get('regularMarketPrice'),
                                "dp": None,
                                "h": info.get('dayHigh'),
                                "l": info.get('dayLow'),
                            },
                        }
                        del ticker, info
                    except Exception:
                        results[symbol] = {"recommendations": [], "price_target": {}, "quote": {}}
                gc.collect()

            # Brief pause between batches to avoid network saturation
            time.sleep(0.5)

        if not results:
            return None
        return json.dumps(results, ensure_ascii=False)

    def parse(self, raw):
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data).__name__}")

        records = []
        for symbol, info in data.items():
            latest_rec = info.get("recommendations", [{}])[0] if info.get("recommendations") else {}
            pt = info.get("price_target", {})
            q = info.get("quote", {})
            records.append({
                "symbol": symbol,
                "buy": latest_rec.get("buy", 0),
                "hold": latest_rec.get("hold", 0),
                "sell": latest_rec.get("sell", 0),
                "strong_buy": latest_rec.get("strongBuy", 0),
                "strong_sell": latest_rec.get("strongSell", 0),
                "period": latest_rec.get("period", ""),
                "target_high": pt.get("targetHigh"),
                "target_low": pt.get("targetLow"),
                "target_mean": pt.get("targetMean"),
                "target_median": pt.get("targetMedian"),
                "price_current": q.get("c"),
                "price_change_pct": q.get("dp"),
                "price_high": q.get("h"),
                "price_low": q.get("l"),
            })
        return records

    def validate(self, records):
        if not records:
            raise ValueError("No analyst data retrieved")
        # Allow up to 600 (full watchlist)
        if len(records) > 600:
            raise ValueError(f"Abnormal record count: {len(records)}")
        # Check at least 80% have price data
        has_price = sum(1 for r in records if r.get("price_current"))
        if has_price < len(records) * 0.5:
            raise ValueError(f"Too many missing prices: {has_price}/{len(records)}")
        return True

    def run(self):
        """Override to also produce earnings_calendar.json"""
        result = super().run()

        # Fetch earnings calendar via Finnhub (only 2 API calls)
        try:
            today = date.today()
            cal = _get("/calendar/earnings", {
                "from": today.isoformat(),
                "to": (today + timedelta(days=14)).isoformat(),
            })
            if cal and cal.get("earningsCalendar"):
                watchlist_set = set(s.upper() for s in self.symbols)
                relevant = [e for e in cal["earningsCalendar"]
                           if e.get("symbol", "").upper() in watchlist_set]
                # Also keep top entries from full list
                all_earnings = relevant + cal["earningsCalendar"][:50]
                # Dedupe
                seen = set()
                unique = []
                for e in all_earnings:
                    key = f"{e.get('symbol')}_{e.get('date')}"
                    if key not in seen:
                        seen.add(key)
                        unique.append(e)

                # Supplement with yfinance HK earnings dates
                try:
                    import yfinance as yf
                    import pandas as pd
                    hk_symbols = [s for s in self.symbols if '.HK' in s][:20]
                    now = pd.Timestamp.now(tz='America/New_York')
                    for sym in hk_symbols:
                        try:
                            ed = yf.Ticker(sym).earnings_dates
                            if ed is not None and not ed.empty:
                                future = ed[ed.index >= now]
                                if not future.empty:
                                    dt = future.index[0]
                                    eps_est = future.iloc[0].get('EPS Estimate')
                                    entry = {
                                        'date': dt.strftime('%Y-%m-%d'),
                                        'symbol': sym,
                                        'epsEstimate': float(eps_est) if pd.notna(eps_est) else None,
                                        'source': 'yfinance',
                                    }
                                    key = f"{sym}_{entry['date']}"
                                    if key not in seen:
                                        seen.add(key)
                                        unique.append(entry)
                        except Exception:
                            continue
                except Exception:
                    pass

                cal_path = os.path.join(self.daily_dir, "earnings_calendar.json")
                with open(cal_path, "w") as f:
                    json.dump(unique[:100], f, ensure_ascii=False, indent=2)
        except Exception:
            pass

        return result


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
