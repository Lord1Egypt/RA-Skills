"""edgar_filings.py — SEC EDGAR 文件监控

抓取 watchlist 美股标的最新 SEC filings (8-K, 10-Q, 10-K, Form 4)。
接口: https://data.sec.gov/submissions/CIK{10位}.json
限制: 10 req/s, 需 User-Agent header
"""
import os, json, time, sys
import requests

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

# CIK 映射 (symbol -> CIK 10位补零)
# 可从 https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK={ticker}&type=&dateb=&owner=include&count=40&search_text=&action=getcompany 获取
CIK_MAP = {
    "AAPL": "0000320193",
    "ABBV": "0001551152",
    "ABT": "0000001800",
    "ADM": "0000007084",
    "ALB": "0000915913",
    "AMAT": "0000006951",
    "AMD": "0000002488",
    "AMT": "0001053507",
    "AMZN": "0001018724",
    "ARM": "0001973239",
    "ASML": "0000937966",
    "BA": "0000012927",
    "BABA": "0001577552",
    "BIDU": "0001329099",
    "CAT": "0000018230",
    "CCJ": "0001009001",
    "CF": "0001324404",
    "COIN": "0001679788",
    "COST": "0000909832",
    "CRM": "0001108524",
    "CRWD": "0001535527",
    "DAL": "0000027904",
    "DDOG": "0001561550",
    "DELL": "0001571996",
    "ENPH": "0001463101",
    "FCX": "0000831259",
    "GOOGL": "0001652044",
    "GS": "0000886982",
    "HSY": "0000047111",
    "INTC": "0000050863",
    "ISRG": "0001035267",
    "JD": "0001549802",
    "JNJ": "0000200406",
    "JPM": "0000019617",
    "KLAC": "0000319201",
    "LLY": "0000059478",
    "LMT": "0000936468",
    "LRCX": "0000707549",
    "META": "0001326801",
    "MOS": "0001285785",
    "MRNA": "0001682852",
    "MRVL": "0001058057",
    "MSFT": "0000789019",
    "NEE": "0000753308",
    "NEM": "0001164727",
    "NET": "0001477333",
    "NOW": "0001373715",
    "NVDA": "0001045810",
    "NVO": "0000353278",
    "O": "0000726728",
    "PDD": "0001737806",
    "PFE": "0000078003",
    "QCOM": "0000804328",
    "RIVN": "0001874178",
    "RTX": "0000101829",
    "SBUX": "0000829224",
    "SLV": "0001330568",
    "SMCI": "0001375365",
    "SNOW": "0001640147",
    "TCEHY": "0001293310",
    "TSLA": "0001318605",
    "V": "0001403161",
    "VKTX": "0001607678",
    "WMT": "0000104169",
    "XOM": "0000034088",
}

USER_AGENT = "OpenClawTrading research@openclaw.local"
BASE_URL = "https://data.sec.gov/submissions/CIK{cik}.json"

# 关注的文件类型
RELEVANT_FORMS = {"8-K", "10-K", "10-Q", "4", "SC 13G", "SC 13G/A", "13F-HR"}


class Fetcher(BaseFetcher):
    name = "edgar_filings"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.watchlist = self._get_us_symbols()

    def _get_us_symbols(self):
        """获取 watchlist 中有 CIK 映射的美股标的"""
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
                        # 只取美股 (无 .HK 后缀)
                        if ".HK" not in sym and sym in CIK_MAP:
                            symbols.append(sym)
                return symbols if symbols else list(CIK_MAP.keys())[:5]
        except Exception:
            pass
        return list(CIK_MAP.keys())[:5]

    def fetch_raw(self):
        """抓取所有 watchlist 标的的 EDGAR submissions"""
        all_filings = {}
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

        for symbol in self.watchlist:
            cik = CIK_MAP.get(symbol)
            if not cik:
                continue
            url = BASE_URL.format(cik=cik)
            try:
                resp = requests.get(url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    all_filings[symbol] = resp.json()
                time.sleep(0.15)  # respect rate limit
            except Exception:
                continue

        if not all_filings:
            return None

        return json.dumps(all_filings, ensure_ascii=False)

    def parse(self, raw):
        """解析 EDGAR submissions，提取最近30天的相关 filings"""
        from datetime import datetime, timedelta
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data).__name__}")
        cutoff = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        records = []
        for symbol, submission in data.items():
            recent = submission.get("filings", {}).get("recent", {})
            forms = recent.get("form", [])
            dates = recent.get("filingDate", [])
            accessions = recent.get("accessionNumber", [])
            descriptions = recent.get("primaryDocDescription", [])

            for i in range(min(len(forms), 50)):  # check up to 50 most recent
                filing_date = dates[i] if i < len(dates) else ""
                if filing_date < cutoff:
                    break
                form_type = forms[i] if i < len(forms) else ""
                if form_type not in RELEVANT_FORMS:
                    continue
                records.append({
                    "symbol": symbol,
                    "form_type": form_type,
                    "filing_date": filing_date,
                    "accession_number": accessions[i] if i < len(accessions) else "",
                    "description": descriptions[i] if i < len(descriptions) else "",
                })

        return records

    def validate(self, records):
        """校验：记录数合理"""
        # EDGAR 可能某些天没有新 filing，空列表是正常的
        if len(records) > 1200:
            raise ValueError(f"Abnormal record count: {len(records)}, possible parse error")
        # 验证必需字段
        for r in records[:10]:
            if not r.get("symbol") or not r.get("form_type") or not r.get("filing_date"):
                raise ValueError(f"Missing required fields in record: {r}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
