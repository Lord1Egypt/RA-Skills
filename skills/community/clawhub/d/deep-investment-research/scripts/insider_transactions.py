"""insider_transactions.py — 内部人交易数据（SEC Form 4）

Primary: Finnhub /stock/insider-transactions API (SEC Form 4)
Fallback: openinsider.com cluster-buys (best effort, often blocked)

输出字段: filing_date, trade_date, ticker, insider_name, title, trade_type,
          price, qty, value, source
"""
import os, json, sys, time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

FINNHUB_BASE = "https://finnhub.io/api/v1"
CLUSTER_URL = "http://openinsider.com/cluster-buys"

# Map Finnhub transactionCode to readable types
TX_CODE_MAP = {
    "P": "P",   # Purchase
    "S": "S",   # Sale
    "A": "A",   # Grant/Award
    "D": "D",   # Disposition (non-open-market)
    "G": "G",   # Gift
    "F": "F",   # Tax withholding
    "C": "C",   # Conversion
    "M": "M",   # Exercise/Conversion
    "W": "W",   # Will/Inheritance
    "X": "X",   # Exercise of in-the-money
    "I": "I",   # Discretionary
}

REQUIRED_FIELDS = {"filing_date", "trade_date", "ticker", "insider_name", "trade_type", "price", "qty"}
VALID_TRADE_TYPES = set(TX_CODE_MAP.values())


def _get_key():
    return os.environ.get("FINNHUB_API_KEY", "")


class Fetcher(BaseFetcher):
    name = "insider_transactions"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.watchlist = self._get_priority_symbols()

    def _get_priority_symbols(self):
        """Only fetch insider data for positions + focus (not full 335 watchlist)"""
        try:
            wl_path = os.path.join(os.path.dirname(__file__), "watchlist.yaml")
            if os.path.exists(wl_path):
                import yaml
                with open(wl_path) as f:
                    data = yaml.safe_load(f) or {}
                symbols = []
                # Positions first (highest priority)
                for item in data.get("positions", []):
                    sym = item["symbol"]
                    if ".HK" not in sym and sym not in symbols:
                        symbols.append(sym)
                # Focus list (capped at 30 to stay within rate limits)
                for item in data.get("focus", [])[:30]:
                    sym = item["symbol"]
                    if ".HK" not in sym and sym not in symbols:
                        symbols.append(sym)
                return symbols if symbols else ["LLY", "MOS", "HSY"]
        except Exception:
            pass
        return ["LLY", "MOS", "HSY"]

    def fetch_raw(self):
        """Fetch insider transactions via Finnhub API (rate limit: 60/min)"""
        key = _get_key()
        if not key:
            raise RuntimeError("FINNHUB_API_KEY not set")

        all_data = {}
        errors = []
        call_count = 0

        def _fetch_one(symbol):
            nonlocal call_count
            try:
                resp = requests.get(
                    f"{FINNHUB_BASE}/stock/insider-transactions",
                    params={"symbol": symbol, "token": key},
                    timeout=15,
                )
                if resp.status_code == 200:
                    return symbol, resp.json()
                elif resp.status_code == 429:
                    time.sleep(2)
                    return symbol, None
                return symbol, None
            except Exception as e:
                return symbol, None

        # Sequential with rate limiting (60 calls/min = 1/sec safe)
        for symbol in self.watchlist:
            sym, data = _fetch_one(symbol)
            call_count += 1
            if data and data.get("data"):
                all_data[sym] = data["data"]
            # Rate limit: ~50 calls/min to stay safe
            if call_count % 10 == 0:
                time.sleep(1)
            else:
                time.sleep(0.3)

        # Best-effort: openinsider cluster buys (often blocked)
        try:
            from bs4 import BeautifulSoup
            resp = requests.get(
                CLUSTER_URL,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                timeout=8,
            )
            if resp.status_code == 200:
                all_data["_cluster_html"] = resp.text
        except Exception:
            pass

        if not all_data:
            return None

        return json.dumps(all_data, ensure_ascii=False)

    def parse(self, raw):
        all_data = json.loads(raw)
        records = []

        for symbol, entries in all_data.items():
            if symbol == "_cluster_html":
                # Parse openinsider HTML table
                cluster = self._parse_cluster_html(entries)
                records.extend(cluster)
                continue

            # Finnhub insider transaction records
            # Only keep S (Sale) and P (Purchase) - open market transactions
            # A/M/F/G/C/J are grants/exercises/tax/gifts = noise, not informative signals
            for tx in entries[:50]:  # Cap per symbol
                code = tx.get("transactionCode", "")
                if code not in ("S", "P"):
                    continue  # Skip non-open-market transactions
                qty = abs(tx.get("change", 0))
                price = tx.get("transactionPrice", 0)
                record = {
                    "filing_date": tx.get("filingDate", ""),
                    "trade_date": tx.get("transactionDate", ""),
                    "ticker": tx.get("symbol", symbol),
                    "insider_name": tx.get("name", ""),
                    "title": "",
                    "trade_type": TX_CODE_MAP.get(code, code),
                    "price": str(price) if price else "0",
                    "qty": str(qty),
                    "value": str(round(qty * price)) if price and qty else "0",
                    "source": "finnhub",
                    "is_derivative": tx.get("isDerivative", False),
                    "sec_filing_id": tx.get("id", ""),
                }
                if record["trade_type"] and record["ticker"]:
                    records.append(record)

        return records

    def _parse_cluster_html(self, html):
        """Parse openinsider cluster buys HTML (best effort)"""
        records = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", class_="tinytable")
            if not table:
                return records
            rows = table.find_all("tr")[1:]
            for row in rows[:50]:
                cells = row.find_all("td")
                if len(cells) < 12:
                    continue
                record = {
                    "filing_date": cells[1].get_text(strip=True),
                    "trade_date": cells[2].get_text(strip=True),
                    "ticker": cells[3].get_text(strip=True),
                    "insider_name": cells[4].get_text(strip=True),
                    "title": cells[5].get_text(strip=True),
                    "trade_type": cells[6].get_text(strip=True),
                    "price": cells[7].get_text(strip=True).replace("$", "").replace(",", ""),
                    "qty": cells[8].get_text(strip=True).replace(",", "").replace("+", "").replace("-", ""),
                    "owned": cells[9].get_text(strip=True).replace(",", ""),
                    "value": cells[11].get_text(strip=True).replace("$", "").replace(",", "").replace("+", "").replace("-", ""),
                    "source": "cluster_buys",
                }
                if record["trade_type"] and record["ticker"]:
                    records.append(record)
        except Exception:
            pass
        return records

    def validate(self, records):
        if len(records) > 12000:
            raise ValueError(f"Abnormal record count: {len(records)}")
        for r in records[:20]:
            missing = REQUIRED_FIELDS - set(r.keys())
            if missing:
                raise ValueError(f"Missing fields: {missing}")
            if r.get("trade_type") and r["trade_type"][0] not in VALID_TRADE_TYPES and r["trade_type"] not in VALID_TRADE_TYPES:
                raise ValueError(f"Invalid trade_type: {r['trade_type']}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
