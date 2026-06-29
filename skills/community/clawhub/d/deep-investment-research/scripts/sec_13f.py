"""sec_13f.py — SEC 13F 机构持仓变动

查询知名机构最新 13F-HR filing，提取 watchlist 标的的持仓变化。
数据源: SEC EDGAR API（免费，10 req/s，需 User-Agent）
注意: 13F 是季度数据，records=0 是正常的。
"""
import os, json, sys, time
import xml.etree.ElementTree as ET
import requests

sys.path.insert(0, os.path.dirname(__file__))
from _base import BaseFetcher, FetchResult

USER_AGENT = "openclaw-research research@openclaw.ai"
HEADERS = {"User-Agent": USER_AGENT, "Accept": "application/json"}

# 知名机构 CIK 列表
TOP_FILERS = {
    "Berkshire Hathaway": "0001067983",
    "Bridgewater": "0001350694",
    "Renaissance Technologies": "0001037389",
    "Citadel": "0001423053",
    "Two Sigma": "0001179392",
}

SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik}.json"
FILING_INDEX_URL = "https://www.sec.gov/Archives/edgar/data/{cik_num}/{acc_clean}/index.json"
FILING_FILE_URL = "https://www.sec.gov/Archives/edgar/data/{cik_num}/{acc_clean}/{filename}"

# 13F XML namespace
NS = {"ns": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}

# Common company name to ticker mapping (top holdings in 13F)
# SEC 13F uses abbreviated names - map generously
NAME_TO_TICKER = {
    # Mega-cap tech
    "APPLE INC": "AAPL",
    "MICROSOFT CORP": "MSFT",
    "AMAZON COM INC": "AMZN",
    "AMAZON.COM INC": "AMZN",
    "ALPHABET INC": "GOOGL",
    "META PLATFORMS INC": "META",
    "NVIDIA CORP": "NVDA",
    "TESLA INC": "TSLA",
    "BROADCOM INC": "AVGO",
    "TAIWAN SEMICONDUCTOR MANUFAC": "TSM",
    "ASML HLDG NV": "ASML",
    "ASML HOLDING NV": "ASML",
    "ARM HOLDINGS PLC": "ARM",
    "PALANTIR TECHNOLOGIES INC": "PLTR",
    "SERVICENOW INC": "NOW",
    "CROWDSTRIKE HLDGS INC": "CRWD",
    "CLOUDFLARE INC": "NET",
    "APPLOVIN CORP": "APP",
    "SYNOPSYS INC": "SNPS",
    "ARISTA NETWORKS INC": "ANET",
    "MARVELL TECHNOLOGY INC": "MRVL",
    "MICRON TECHNOLOGY INC": "MU",
    "KLA CORP": "KLAC",
    "LAM RESEARCH CORP": "LRCX",
    "APPLIED MATLS INC": "AMAT",
    "APPLIED MATERIALS INC": "AMAT",
    "TERADYNE INC": "TER",
    "DELL TECHNOLOGIES INC": "DELL",
    "SEAGATE TECHNOLOGY HLDNGS PL": "STX",
    "WESTERN DIGITAL CORP": "WDC",
    "SANDISK CORP": "SNDK",
    "TOWER SEMICONDUCTOR LTD": "TSEM",
    "CELESTICA INC": "CLS",
    "CREDO TECHNOLOGY GROUP HOLDI": "CRDO",
    "ASTERA LABS INC": "ALAB",
    "VERTIV HOLDINGS CO": "VRT",
    # Software/Internet
    "ORACLE CORP": "ORCL",
    "SALESFORCE INC": "CRM",
    "ADOBE INC": "ADBE",
    "CISCO SYSTEMS INC": "CSCO",
    "INTEL CORP": "INTC",
    "AMD INC": "AMD",
    "ADVANCED MICRO DEVICES": "AMD",
    "QUALCOMM INC": "QCOM",
    "TEXAS INSTRUMENTS INC": "TXN",
    "NETFLIX INC": "NFLX",
    "ROBLOX CORP": "RBLX",
    "DOORDASH INC": "DASH",
    "AIRBNB INC": "ABNB",
    "COINBASE GLOBAL INC": "COIN",
    "REDDIT INC": "RDDT",
    "ROBINHOOD MKTS INC": "HOOD",
    "ETSY INC": "ETSY",
    "WAYFAIR INC": "W",
    "STRATEGY INC": "MSTR",
    # Finance
    "BERKSHIRE HATHAWAY": "BRK.B",
    "JPMORGAN CHASE & CO": "JPM",
    "VISA INC": "V",
    "MASTERCARD INC": "MA",
    "BANK OF AMERICA CORP": "BAC",
    "BANK AMERICA CORP": "BAC",
    "WELLS FARGO & CO": "WFC",
    "CITIGROUP INC": "C",
    "GOLDMAN SACHS GROUP INC": "GS",
    "MORGAN STANLEY": "MS",
    "AMERICAN EXPRESS CO": "AXP",
    "CHARLES SCHWAB CORP": "SCHW",
    "SCHWAB CHARLES CORP": "SCHW",
    "BLACKROCK INC": "BLK",
    "S&P GLOBAL INC": "SPGI",
    "MOODYS CORP": "MCO",
    "CAPITAL ONE FINL CORP": "COF",
    "CAPITAL ONE FINANCIAL CORP": "COF",
    "ALLY FINL INC": "ALLY",
    "INTERACTIVE BROKERS GROUP IN": "IBKR",
    "JEFFERIES FINANCIAL GROUP IN": "JEF",
    "PROGRESSIVE CORP": "PGR",
    "CHUBB LTD SWITZ": "CB",
    "CHUBB LTD": "CB",
    # Healthcare
    "UNITEDHEALTH GROUP INC": "UNH",
    "ELI LILLY & CO": "LLY",
    "ELI LILLY AND CO": "LLY",
    "ABBVIE INC": "ABBV",
    "PFIZER INC": "PFE",
    "MERCK & CO INC": "MRK",
    "JOHNSON & JOHNSON": "JNJ",
    "BRISTOL-MYERS SQUIBB CO": "BMY",
    "GILEAD SCIENCES INC": "GILD",
    "REGENERON PHARMACEUTICALS": "REGN",
    "INTUITIVE SURGICAL INC": "ISRG",
    "BOSTON SCIENTIFIC CORP": "BSX",
    "HCA HEALTHCARE INC": "HCA",
    "DAVITA INC": "DVA",
    "ALNYLAM PHARMACEUTICALS INC": "ALNY",
    "NEUROCRINE BIOSCIENCES INC": "NBIX",
    "INCYTE CORP": "INCY",
    "EXELIXIS INC": "EXEL",
    "CORCEPT THERAPEUTICS INC": "CORT",
    "ALKERMES PLC": "ALKS",
    "MEDPACE HLDGS INC": "MEDP",
    "UNITED THERAPEUTICS CORP DEL": "UTHR",
    "ABBOTT LABORATORIES": "ABT",
    # Consumer
    "COSTCO WHOLESALE CORP": "COST",
    "WALMART INC": "WMT",
    "HOME DEPOT INC": "HD",
    "LOWES COS INC": "LOW",
    "MCDONALDS CORP": "MCD",
    "STARBUCKS CORP": "SBUX",
    "NIKE INC": "NKE",
    "PROCTER & GAMBLE CO": "PG",
    "COCA COLA CO": "KO",
    "COCA-COLA CO": "KO",
    "PEPSICO INC": "PEP",
    "KRAFT HEINZ CO": "KHC",
    "CONSTELLATION BRANDS INC": "STZ",
    "KIMBERLY-CLARK CORP": "KMB",
    "TJX COS INC NEW": "TJX",
    "TJX COS INC": "TJX",
    "ROSS STORES INC": "ROST",
    "KROGER CO": "KR",
    "MACYS INC": "M",
    "ALTRIA GROUP INC": "MO",
    # Industrials
    "CATERPILLAR INC": "CAT",
    "BOEING CO": "BA",
    "LOCKHEED MARTIN CORP": "LMT",
    "RAYTHEON TECHNOLOGIES": "RTX",
    "RTX CORP": "RTX",
    "GENERAL ELECTRIC CO": "GE",
    "GE VERNOVA INC": "GEV",
    "3M CO": "MMM",
    "HONEYWELL INTERNATIONAL": "HON",
    "UNION PACIFIC CORP": "UNP",
    "UNION PAC CORP": "UNP",
    "CSX CORP": "CSX",
    "PACCAR INC": "PCAR",
    "WASTE MGMT INC DEL": "WM",
    "WASTE CONNECTIONS INC": "WCN",
    "COMFORT SYS USA INC": "FIX",
    "STERLING INFRASTRUCTURE INC": "STRL",
    "ALLISON TRANSMISSION HLDGS I": "ALSN",
    "BAKER HUGHES COMPANY": "BKR",
    "LENNAR CORP": "LEN",
    "NVR INC": "NVR",
    "LOUISIANA PAC CORP": "LPX",
    # Energy/Materials
    "EXXON MOBIL CORP": "XOM",
    "CHEVRON CORP": "CVX",
    "OCCIDENTAL PETE CORP": "OXY",
    "OCCIDENTAL PETROLEUM CORP": "OXY",
    "NRG ENERGY INC": "NRG",
    "TALEN ENERGY CORP": "TLN",
    "BLOOM ENERGY CORP": "BE",
    "NUCOR CORP": "NUE",
    "STEEL DYNAMICS INC": "STLD",
    "ALBEMARLE CORP": "ALB",
    "NEWMONT CORP": "NEM",
    "BARRICK MNG CORP": "GOLD",
    "BARRICK GOLD CORP": "GOLD",
    "FRANCO NEV CORP": "FNV",
    "FRANCO NEVADA CORP": "FNV",
    "KINROSS GOLD CORP": "KGC",
    "ALAMOS GOLD INC": "AGI",
    # Telecom/Media
    "AT&T INC": "T",
    "VERIZON COMMUNICATIONS": "VZ",
    "T-MOBILE US INC": "TMUS",
    "COMCAST CORP": "CMCSA",
    "CHARTER COMMUNICATIONS": "CHTR",
    "WALT DISNEY CO": "DIS",
    "SIRIUSXM HOLDINGS INC": "SIRI",
    "NEW YORK TIMES CO MTN BE": "NYT",
    # Transport/Auto
    "DELTA AIR LINES INC": "DAL",
    "CARVANA CO": "CVNA",
    # Chinese ADRs / International
    "ALIBABA GROUP HOLDING": "BABA",
    "JD.COM INC": "JD",
    "PINDUODUO INC": "PDD",
    "BAIDU INC": "BIDU",
    "NETEASE INC": "NTES",
    "NIO INC": "NIO",
    "LI AUTO INC": "LI",
    "XPENG INC": "XPEV",
    "SEA LTD": "SE",
    "MERCADOLIBRE": "MELI",
    "NU HLDGS LTD": "NU",
    "AERCAP HOLDINGS NV": "AER",
    "LINDE PLC": "LIN",
    "VALE S A": "VALE",
    "PETROLEO BRASILEIRO S A": "PBR",
    "NOVA LTD": "NVMI",
    # Real Estate / Other
    "LIBERTY LIVE HOLDINGS INC": "LLYVA",
    "ARGAN INC": "AGX",
    "CBOE GLOBAL MKTS INC": "CBOE",
    "VERISIGN INC": "VRSN",
    "AMPHENOL CORP": "APH",
    "BOOKING HOLDINGS INC": "BKNG",
    # ETFs (map common ones)
    "INVESCO QQQ TR": "QQQ",
    "STATE STR SPDR S&P 500 ETF T": "SPY",
    "STATE STR SPDR DOW JONES IND": "DIA",
    "SPDR GOLD TR": "GLD",
    "ISHARES SILVER TR": "SLV",
    "UNITED STS OIL FD LP": "USO",
    "VANGUARD INDEX FDS": "VOO",
    "DIREXION SHARES ETF TRUST": "_ETF",
    "SELECT SECTOR SPDR TR": "_ETF",
    "ISHARES TR": "_ETF",
    "ISHARES INC": "_ETF",
    "VANECK ETF TRUST": "_ETF",
    "INVESCO EXCH TRADED FD TR II": "_ETF",
    "VANGUARD INTL EQUITY INDEX F": "_ETF",
    "SPDR SERIES TRUST": "_ETF",
}

def name_to_ticker(name: str) -> str:
    """Map company name to ticker symbol."""
    if not name:
        return ""
    name_upper = name.upper().strip()
    # Direct match
    if name_upper in NAME_TO_TICKER:
        return NAME_TO_TICKER[name_upper]
    # Fuzzy match (prefix)
    for key, ticker in NAME_TO_TICKER.items():
        if name_upper.startswith(key) or key.startswith(name_upper):
            return ticker
    return ""


class Fetcher(BaseFetcher):
    name = "sec_13f"

    def fetch_raw(self):
        results = []
        for filer_name, cik in TOP_FILERS.items():
            try:
                url = SUBMISSIONS_URL.format(cik=cik)
                resp = requests.get(url, headers=HEADERS, timeout=15)
                if resp.status_code != 200:
                    continue
                data = resp.json()
                # Find latest 13F-HR filing
                recent = data.get("filings", {}).get("recent", {})
                forms = recent.get("form", [])
                dates = recent.get("filingDate", [])
                accessions = recent.get("accessionNumber", [])

                for i, form in enumerate(forms):
                    if "13F" in form:
                        results.append({
                            "filer": filer_name,
                            "cik": cik,
                            "form": form,
                            "filing_date": dates[i] if i < len(dates) else "",
                            "accession": accessions[i] if i < len(accessions) else "",
                        })
                        break  # Only latest per filer

                time.sleep(0.2)  # Rate limit: 10 req/s
            except Exception:
                continue

        if not results:
            return None
        return json.dumps(results, ensure_ascii=False)

    def parse(self, raw):
        filings = json.loads(raw)
        records = []
        for f in filings:
            accession = f.get("accession", "").replace("-", "")
            cik = f.get("cik", "")
            filing_date = f.get("filing_date", "")

            # Try to fetch the 13F holdings info table
            holdings = self._fetch_holdings(cik, accession)
            if holdings:
                for h in holdings[:50]:  # Cap at 50 per filer
                    name = h.get("nameOfIssuer", h.get("name", ""))
                    symbol = name_to_ticker(name)  # Map name to ticker
                    records.append({
                        "filer": f["filer"],
                        "symbol": symbol,
                        "name": name,
                        "shares": h.get("shares", 0),
                        "value_usd": h.get("value", 0),  # XML value is in whole dollars
                        "filing_date": filing_date,
                    })
            else:
                # At minimum record the filing existence
                records.append({
                    "filer": f["filer"],
                    "symbol": "",
                    "name": "",
                    "shares": 0,
                    "value_usd": 0,
                    "filing_date": filing_date,
                    "note": "Filing found but holdings not parsed"
                })
        return records

    def _fetch_holdings(self, cik, accession):
        """Fetch and parse 13F holdings from the infotable XML."""
        if not accession:
            return []
        try:
            cik_num = cik.lstrip("0") or "0"
            acc_clean = accession.replace("-", "")

            # Step 1: Get filing index to find the infotable XML
            index_url = FILING_INDEX_URL.format(cik_num=cik_num, acc_clean=acc_clean)
            resp = requests.get(index_url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                return []

            index_data = resp.json()
            items = index_data.get("directory", {}).get("item", [])

            # Find the infotable XML (not the primary_doc which is the cover page)
            xml_file = None
            for item in items:
                name = item.get("name", "")
                if name.endswith(".xml") and name != "primary_doc.xml":
                    xml_file = name
                    break

            if not xml_file:
                return []

            time.sleep(0.15)  # Rate limit

            # Step 2: Fetch and parse the infotable XML
            xml_url = FILING_FILE_URL.format(cik_num=cik_num, acc_clean=acc_clean, filename=xml_file)
            resp = requests.get(xml_url, headers=HEADERS, timeout=20)
            if resp.status_code != 200:
                return []

            root = ET.fromstring(resp.content)
            holdings = []
            seen = {}  # Aggregate by issuer name (multiple sub-entries possible)

            for entry in root.findall("ns:infoTable", NS):
                name = (entry.findtext("ns:nameOfIssuer", "", NS) or "").strip()
                value = int(entry.findtext("ns:value", "0", NS) or 0)  # in thousands
                shares_el = entry.find("ns:shrsOrPrnAmt/ns:sshPrnamt", NS)
                shares = int(shares_el.text or 0) if shares_el is not None else 0
                cusip = (entry.findtext("ns:cusip", "", NS) or "").strip()

                if name in seen:
                    seen[name]["value"] += value
                    seen[name]["shares"] += shares
                else:
                    seen[name] = {
                        "nameOfIssuer": name,
                        "cusip": cusip,
                        "value": value,
                        "shares": shares,
                    }

            # Sort by value descending, return top holdings
            holdings = sorted(seen.values(), key=lambda x: x["value"], reverse=True)
            return holdings

        except Exception:
            return []

    def validate(self, records):
        # 13F is quarterly; empty is acceptable
        if not isinstance(records, list):
            raise ValueError("Records must be a list")
        for r in records:
            if not r.get("filer"):
                raise ValueError(f"Missing filer: {r}")
        return True


if __name__ == '__main__':
    from _base import cli_main
    cli_main(Fetcher)
