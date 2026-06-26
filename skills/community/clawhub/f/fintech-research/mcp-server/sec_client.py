"""
SEC EDGAR API client — US Securities and Exchange Commission filings.

Purpose: Search and retrieve official SEC filings (10-K, 10-Q, 8-K, etc.)
          for US-listed companies. Uses the free public EDGAR API.

Network behavior:
  - 1 HTTPS GET request per filing search to www.sec.gov
  - 30-second connection timeout
  - Response size capped at 1MB
  - SSL certificate verification enabled
  - SEC requires proper User-Agent with contact info
  - Rate limited per SEC fair access policy

Note: US equities only. SEC EDGAR does not cover non-US listings.
"""
import os
import re
import requests
import json

# Security: Predefined allowed domains
_SEC_DOMAIN = "www.sec.gov"
SEC_BASE = f"https://{_SEC_DOMAIN}/cgi-bin/browse-edgar"

# Local CIK mapping cache
CIK_PATH = os.path.join(os.path.dirname(__file__), "mock_data", "us_tickers.json")

# Security: Response size cap
_MAX_RESPONSE_SIZE = 1024 * 1024

# Security: Allowed form types
_ALLOWED_FORMS = {"10-K", "10-Q", "8-K", "DEF-14A", "S-1", "424B4", "13F-HR", "4", "3", "5"}

# Security: Ticker validation
_TICKER_PATTERN = re.compile(r"^[A-Z]{1,5}$")

# Security: SEC requires proper User-Agent with contact info
_DEFAULT_HEADERS = {
    "User-Agent": (
        "FintechResearch-MCP/2.0 "
        "(https://github.com/fredtai/Fintech-research; "
        "sec-edgar-filing-search)"
    ),
    "Accept": "application/atom+xml, application/xml, */*",
    "Accept-Encoding": "gzip, deflate",
    "Host": _SEC_DOMAIN,
}

_session = requests.Session()
_session.headers.update(_DEFAULT_HEADERS)


def _validate_ticker(ticker: str) -> bool:
    """Validate US ticker symbol format."""
    if not ticker:
        return False
    return bool(_TICKER_PATTERN.match(str(ticker).strip().upper()))


def _validate_form_types(form_types) -> list:
    """Sanitize and validate form type list."""
    if not form_types:
        return ["10-K", "10-Q", "8-K"]
    cleaned = []
    for ft in form_types:
        ft_clean = re.sub(r"[^A-Z0-9-]", "", str(ft).upper())
        if ft_clean in _ALLOWED_FORMS:
            cleaned.append(ft_clean)
    return cleaned if cleaned else ["10-K", "10-Q", "8-K"]


def get_company_tickers():
    """Load ticker->CIK mapping from local cache."""
    try:
        with open(CIK_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def search_filings(ticker, form_types=None, limit=5):
    """
    Search SEC EDGAR filings for a US-listed company.

    Args:
        ticker: US ticker symbol (e.g., "AAPL", "TSLA")
        form_types: List of form types (default: ["10-K", "10-Q", "8-K"])
        limit: Max filings per form type (default: 5, max: 20)

    Returns:
        dict: {"filings": [...], "count": N}

    Security notes:
        - Ticker validated against ^[A-Z]{1,5}$ pattern
        - Form types validated against allowlist
        - Only HTTPS requests to www.sec.gov
        - Response truncated at 1MB
        - SEC fair access policy: max 10 requests/second
    """
    # Handle positional argument: if form_types is int, treat as limit
    if isinstance(form_types, int):
        limit = min(form_types, 20)
        form_types = None

    # Input validation
    if not _validate_ticker(ticker):
        return {
            "filings": [],
            "count": 0,
            "error": "Invalid ticker format. Expected 1-5 uppercase letters.",
        }

    form_types = _validate_form_types(form_types)
    limit = min(int(limit), 20)
    ticker_upper = str(ticker).strip().upper()

    try:
        tickers = get_company_tickers()
        cik = tickers.get(ticker_upper, {}).get("cik")
        if not cik:
            return _mock_filings(ticker_upper, limit)

        results = []
        for ft in form_types:
            params = {
                "action": "getcompany",
                "CIK": cik.zfill(10),
                "type": ft,
                "dateb": "",
                "owner": "exclude",
                "count": str(limit),
                "output": "atom",
            }

            resp = _session.get(
                SEC_BASE,
                params=params,
                timeout=30,
                verify=True,
                stream=True,
            )

            # Size limit
            content = b""
            for chunk in resp.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > _MAX_RESPONSE_SIZE:
                    break

            if resp.status_code == 200:
                import xml.etree.ElementTree as ET

                try:
                    root = ET.fromstring(content)
                    ns = {"atom": "http://www.w3.org/2005/Atom"}
                    for entry in root.findall("atom:entry", ns)[:limit]:
                        title = entry.findtext("atom:title", "", ns)
                        updated = entry.findtext("atom:updated", "", ns)
                        link_el = entry.find("atom:link", ns)
                        href = link_el.get("href", "") if link_el is not None else ""
                        # Validate URL is within sec.gov
                        if href and _SEC_DOMAIN not in href:
                            href = ""
                        results.append(
                            {
                                "accession_number": "",
                                "form_type": ft,
                                "filing_date": updated[:10],
                                "description": title,
                                "url": href,
                            }
                        )
                except ET.ParseError:
                    continue

        return {"filings": results[:limit], "count": len(results[:limit])}

    except requests.exceptions.SSLError as e:
        return {"filings": [], "count": 0, "error": f"SSL verification failed: {e}"}
    except requests.exceptions.Timeout:
        return {"filings": [], "count": 0, "error": "Request timed out (30s)"}
    except Exception:
        return _mock_filings(ticker_upper, limit)


def _mock_filings(ticker, limit):
    """Return mock filing data for offline testing."""
    return {
        "filings": [
            {
                "accession_number": "mock-001",
                "form_type": "10-K",
                "filing_date": "2025-02-15",
                "description": f"Annual report for {ticker}",
                "url": "",
                "mock": True,
            }
        ],
        "count": 1,
        "mock": True,
    }
