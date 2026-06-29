"""southbound_top10.py — 港股通南向十大成交（AAStocks）

接口: https://www.aastocks.com/en/cnhk/market/top-turnover/southbound
HTML TR 结构: rank|name|code.HK|price|change|total_turnover|buy_sell|direction|net_flow
"""
import os, json, sys, re
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

URL = "https://www.aastocks.com/en/cnhk/market/top-turnover/southbound"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0 Safari/537.36"}


class Fetcher(BaseFetcher):
    name = "southbound_top10"

    def fetch_raw(self):
        resp = requests.get(URL, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            return resp.text
        return None

    def parse(self, raw):
        if not isinstance(raw, str) or len(raw) < 100:
            raise ValueError("Invalid or empty HTML response")
        soup = BeautifulSoup(raw, "html.parser")
        records = []

        for tr in soup.find_all("tr"):
            text = tr.get_text("|", strip=True)
            # Match rows with HK stock codes
            if not re.search(r"\d{5}\.HK", text):
                continue
            parts = text.split("|")
            if len(parts) < 8:
                continue
            try:
                # Extract fields
                code_match = re.search(r"(\d{5})\.HK", text)
                code = f"{code_match.group(1)}.HK" if code_match else ""

                # Find name (usually parts[1])
                name = parts[1].strip() if len(parts) > 1 else ""

                # Price
                price = parts[3].strip() if len(parts) > 3 else ""

                # Change
                change = parts[4].strip() if len(parts) > 4 else ""

                # Total turnover
                turnover = parts[5].strip() if len(parts) > 5 else ""

                # Direction (IN/OUT)
                direction = ""
                for p in parts:
                    if p.strip() in ("IN", "OUT"):
                        direction = p.strip()
                        break

                # Net flow (last numeric-like field with M/B)
                net_flow = parts[-1].strip() if parts else ""

                records.append({
                    "code": code,
                    "name": name,
                    "price": price,
                    "change": change,
                    "turnover": turnover,
                    "direction": direction,
                    "net_flow": net_flow,
                })
            except (IndexError, ValueError):
                continue

        return records[:20]

    def validate(self, records):
        if not records:
            raise ValueError("No southbound data found")
        if len(records) > 50:
            raise ValueError(f"Abnormal count: {len(records)}")
        for r in records[:5]:
            if not r.get("code") or not re.match(r"\d{5}\.HK", r["code"]):
                raise ValueError(f"Invalid code format: {r.get('code')}")
            if not r.get("name"):
                raise ValueError(f"Missing name for {r.get('code')}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
