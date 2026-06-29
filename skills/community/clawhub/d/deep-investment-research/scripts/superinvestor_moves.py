"""superinvestor_moves.py — 知名投资者持仓跟踪（Dataroma）

接口: https://www.dataroma.com/m/stock.php?sym={SYMBOL}
必须完整 Chrome UA + Accept-Language + --compressed，否则 406
"""
import os, json, sys, re, time
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml",
}


class Fetcher(BaseFetcher):
    name = "superinvestor_moves"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbols = self._get_us_symbols()

    def _get_us_symbols(self):
        try:
            wl_path = os.path.join(os.path.dirname(__file__), "watchlist.yaml")
            if os.path.exists(wl_path):
                import yaml
                with open(wl_path) as f:
                    data = yaml.safe_load(f) or {}
                symbols = []
                for section in ["positions", "focus"]:
                    for item in data.get(section, []):
                        sym = item["symbol"]
                        if ".HK" not in sym and sym not in ("QQQM", "VOO"):
                            symbols.append(sym)
                return symbols if symbols else ["LLY"]
        except Exception:
            pass
        return ["LLY"]

    def fetch_raw(self):
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = {}

        def _fetch_one(symbol):
            url = f"https://www.dataroma.com/m/stock.php?sym={symbol}"
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                return symbol, resp.text
            return symbol, None

        # Concurrent fetch with staggered starts
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for symbol in self.symbols:
                time.sleep(0.3)  # stagger submissions
                futures.append(executor.submit(_fetch_one, symbol))

            for future in as_completed(futures):
                try:
                    symbol, html = future.result(timeout=20)
                    if html:
                        results[symbol] = html
                except Exception:
                    continue

        if not results:
            return None
        return json.dumps(results, ensure_ascii=False)

    def parse(self, raw):
        data = json.loads(raw)
        records = []
        for symbol, html in data.items():
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find("table", id="grid")
            if not table:
                continue
            rows = table.find_all("tr")[1:]
            for row in rows[:20]:
                cells = row.find_all("td")
                if len(cells) < 5:
                    continue
                try:
                    records.append({
                        "symbol": symbol,
                        "manager": cells[1].get_text(strip=True),
                        "portfolio_pct": cells[2].get_text(strip=True),
                        "change_pct": cells[3].get_text(strip=True),
                        "shares": cells[4].get_text(strip=True).replace(",", ""),
                        "value": cells[5].get_text(strip=True).replace(",", "") if len(cells) > 5 else "",
                        "reported_date": "",
                    })
                except (IndexError, ValueError):
                    continue
        return records

    def validate(self, records):
        # Dataroma 对小票可能无数据
        if len(records) > 2500:
            raise ValueError(f"Abnormal count: {len(records)}")
        for r in records[:10]:
            if not r.get("symbol") or not r.get("manager"):
                raise ValueError(f"Missing fields: {r}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
