"""transcripts.py — 财报电话会纪要（Motley Fool）

策略:
1. 从 /earnings-call-transcripts/ 列表页获取最近发布的 transcripts
2. 匹配 watchlist 标的的 ticker
3. 从 URL slug 中提取 ticker (格式: company-name-TICKER-q1-2026...)

无登录, 无反爬
"""
import os, json, sys, re, time
import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

TRANSCRIPT_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "state", "transcript_index.json")

# Exchange mappings for Fool URLs (legacy, kept for reference)
EXCHANGE_MAP = {
    "LLY": "NYSE",
    "MOS": "NYSE",
    "HSY": "NYSE",
    "NVDA": "NASDAQ",
    "QQQM": "NASDAQ",
    "VOO": "NYSEARCA",
    "BABA": "NYSE",
    "TCEHY": "OTC",
    "JD": "NASDAQ",
    "BIDU": "NASDAQ",
}


class Fetcher(BaseFetcher):
    name = "transcripts"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbols = self._get_us_symbols()
        self.index = self._load_index()

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
                        if ".HK" not in sym:
                            symbols.append(sym)
                return symbols if symbols else ["LLY"]
        except Exception:
            pass
        return ["LLY"]

    def _load_index(self):
        try:
            with open(TRANSCRIPT_INDEX_PATH) as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_index(self):
        os.makedirs(os.path.dirname(TRANSCRIPT_INDEX_PATH), exist_ok=True)
        with open(TRANSCRIPT_INDEX_PATH, "w") as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def _extract_ticker_from_slug(self, slug, text=""):
        """Extract ticker from transcript slug or title text.
        
        Slug format: company-name-TICKER-q1-2026-earnings-call-transcript
        Title format: Company Name (TICKER) Q1 2026 Earnings Transcript
        """
        # Try title first: "Company (TICKER) Q1..."
        match = re.search(r'\(([A-Z]{1,5})\)', text)
        if match:
            return match.group(1)
        
        # Try slug: look for ticker pattern before qN-YYYY
        match = re.search(r'-([a-z]{1,5})-q[1-4]-\d{4}', slug)
        if match:
            return match.group(1).upper()
        
        return None

    def fetch_raw(self):
        """从 Fool earnings-call-transcripts 列表页获取最近 transcripts"""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        all_transcripts = []
        symbols_lower = set(s.lower() for s in self.symbols)

        # Scan up to 5 pages of recent transcripts
        for page in range(1, 6):
            try:
                url = f"https://www.fool.com/earnings-call-transcripts/?page={page}"
                resp = requests.get(url, headers=headers, timeout=15)
                if resp.status_code != 200:
                    break
                
                soup = BeautifulSoup(resp.text, "html.parser")
                links = soup.find_all("a", href=True)
                found_any = False
                
                for a in links:
                    href = a["href"]
                    if "/earnings/call-transcripts/2026/" not in href and "/earnings/call-transcripts/2025/" not in href:
                        continue
                    text = a.get_text(strip=True)
                    if not text:
                        continue
                    
                    found_any = True
                    ticker = self._extract_ticker_from_slug(href, text)
                    
                    all_transcripts.append({
                        "href": href,
                        "text": text,
                        "ticker": ticker,
                    })
                
                if not found_any:
                    break
                time.sleep(1)
            except Exception:
                continue

        if not all_transcripts:
            return None

        return json.dumps(all_transcripts, ensure_ascii=False)

    def parse(self, raw):
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError(f"Expected list, got {type(data).__name__}")
        
        symbols_set = set(s.upper() for s in self.symbols)
        records = []
        seen = set()
        
        for item in data:
            href = item.get("href", "")
            text = item.get("text", "")
            ticker = item.get("ticker", "")
            
            if not ticker or ticker not in symbols_set:
                continue
            
            # Extract date from URL: /earnings/call-transcripts/YYYY/MM/DD/slug/
            match = re.search(r"/earnings/call-transcripts/(\d{4})/(\d{2})/(\d{2})/(.+?)/?$", href)
            if not match:
                continue
            
            year, month, day, slug = match.groups()
            transcript_id = f"{ticker}_{year}{month}{day}_{slug}"
            
            if transcript_id in seen:
                continue
            seen.add(transcript_id)
            
            records.append({
                "symbol": ticker,
                "date": f"{year}-{month}-{day}",
                "title": text,
                "slug": slug,
                "url": f"https://www.fool.com{href}" if href.startswith("/") else href,
                "transcript_id": transcript_id,
                "already_fetched": transcript_id in self.index,
            })

        return records

    def validate(self, records):
        # Transcripts 可能没有新的（不在财报季），空列表正常
        if len(records) > 200:
            raise ValueError(f"Abnormal count: {len(records)}")
        for r in records[:10]:
            if not r.get("symbol") or not r.get("url"):
                raise ValueError(f"Missing required fields: {r}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
