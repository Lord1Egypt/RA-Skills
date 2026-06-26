"""
HKEX News disclosure scraper — Hong Kong Exchange regulatory announcements.

Purpose: Fetch public regulatory disclosures from HKEX News Portal
          (https://www1.hkexnews.hk) — an official free public service
          provided by Hong Kong Exchanges and Clearing Limited.

Network behavior:
  - 1 HTTPS GET request per call to www1.hkexnews.hk
  - 2-second rate limit between requests
  - 30-second connection timeout
  - Response size capped at 2MB
  - SSL certificate verification enabled
  - Input validated against allowed stock code format
"""
import time
import requests
import re
from bs4 import BeautifulSoup

# Security: Predefined allowed domains — prevents SSRF
_ALLOWED_DOMAIN = "www1.hkexnews.hk"
_BASE_URL = f"https://{_ALLOWED_DOMAIN}/search/titlesearch.xhtml"

# Security: Response size cap (2MB max)
_MAX_RESPONSE_SIZE = 2 * 1024 * 1024

# Security: Input validation — stock codes must be 4-5 digits
_STOCK_CODE_PATTERN = re.compile(r"^\d{4,5}$")

# Security: Request identity — transparent User-Agent
_DEFAULT_HEADERS = {
    "User-Agent": (
        "FintechResearch-MCP/2.0 "
        "(https://github.com/fredtai/Fintech-research; "
        "HKEX-public-disclosure-scraper)"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

# Reuse TCP connections for same domain
_session = requests.Session()
_session.headers.update(_DEFAULT_HEADERS)


def _validate_stock_code(stock_code: str) -> bool:
    """Validate stock code format to prevent injection."""
    if not stock_code:
        return False
    return bool(_STOCK_CODE_PATTERN.match(str(stock_code).strip()))


def search_disclosures(stock_code, category="announcements", since=None, limit=5):
    """
    Search HKEX News for regulatory disclosures.

    Args:
        stock_code: 4-5 digit HKEX stock code (e.g., "0700" for Tencent)
        category: Disclosure category (default: "announcements")
        since: Date filter string (default: None)
        limit: Max results to return (default: 5, max: 20)

    Returns:
        dict: {"announcements": [...], "count": N, "mock": bool}

    Security notes:
        - Stock code is validated against ^[0-9]{4,5}$ pattern
        - Only HTTPS requests to www1.hkexnews.hk are made
        - Response truncated at 2MB to prevent memory exhaustion
        - 2-second rate limit enforced between requests
    """
    # Input validation
    if not _validate_stock_code(stock_code):
        return {
            "announcements": [],
            "count": 0,
            "error": "Invalid stock code format. Expected 4-5 digits.",
        }

    limit = min(int(limit), 20)  # Cap at 20
    category = re.sub(r"[^a-zA-Z0-9_-]", "", str(category))  # Sanitize

    try:
        resp = _session.get(
            _BASE_URL,
            params={"stockCode": str(stock_code).strip(), "category": category},
            timeout=30,
            verify=True,  # SSL certificate verification
            stream=True,  # Stream to enforce size limit
        )

        # Security: Enforce response size limit
        content = b""
        for chunk in resp.iter_content(chunk_size=8192):
            content += chunk
            if len(content) > _MAX_RESPONSE_SIZE:
                return {
                    "announcements": [],
                    "count": 0,
                    "error": "Response exceeds size limit (2MB)",
                }

        resp.raise_for_status()
        soup = BeautifulSoup(content, "html.parser")

        results = []
        rows = soup.select("table.table-responsive tbody tr")
        for row in rows[:limit]:
            cols = row.find_all("td")
            if len(cols) >= 3:
                date_text = cols[0].get_text(strip=True)
                title = cols[1].get_text(strip=True)
                pdf_link = cols[1].find("a", href=True)
                pdf_url = pdf_link["href"] if pdf_link else ""
                if pdf_url and not pdf_url.startswith("http"):
                    pdf_url = f"https://{_ALLOWED_DOMAIN}" + pdf_url
                # Validate PDF URL is within allowed domain
                if pdf_url and _ALLOWED_DOMAIN not in pdf_url:
                    pdf_url = ""
                if since and date_text < since:
                    continue
                results.append(
                    {
                        "date": date_text,
                        "title": title,
                        "category": category,
                        "pdf_url": pdf_url,
                        "stock_code": str(stock_code).strip(),
                    }
                )

        # Rate limiting: 2-second delay
        time.sleep(2)
        return {"announcements": results, "count": len(results)}

    except requests.exceptions.SSLError as e:
        return {"announcements": [], "count": 0, "error": f"SSL verification failed: {e}"}
    except requests.exceptions.Timeout:
        return {"announcements": [], "count": 0, "error": "Request timed out (30s)"}
    except Exception as e:
        # Fallback to mock data on any error
        return _mock_disclosures(str(stock_code).strip(), limit)


def _mock_disclosures(stock_code, limit):
    """Return mock disclosure data for offline testing."""
    mocks = {
        "0700": [
            {
                "date": "2025-05-14",
                "title": "Quarterly Results Announcement",
                "category": "announcements",
                "pdf_url": "",
                "stock_code": "0700",
            },
            {
                "date": "2025-04-02",
                "title": "Connected Transaction",
                "category": "announcements",
                "pdf_url": "",
                "stock_code": "0700",
            },
            {
                "date": "2025-03-19",
                "title": "Annual Report 2024",
                "category": "reports",
                "pdf_url": "",
                "stock_code": "0700",
            },
        ]
    }
    announcements = mocks.get(stock_code, [])
    return {
        "announcements": announcements[:limit],
        "count": len(announcements[:limit]),
        "mock": True,
    }
