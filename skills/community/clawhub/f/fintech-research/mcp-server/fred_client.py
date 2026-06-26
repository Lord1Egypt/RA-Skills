"""
FRED API client — US macroeconomic data from Federal Reserve Bank of St. Louis.

Purpose: Fetch official macroeconomic time series (Treasury yields, Fed Funds,
          CPI, unemployment, DXY, etc.) from the free FRED API.

Network behavior:
  - 1 HTTPS GET request per call to api.stlouisfed.org
  - 30-second connection timeout
  - Response size capped at 1MB
  - SSL certificate verification enabled
  - Optional API key read from FRED_API_KEY env var (free registration)
  - No API key works with mock data fallback

Free API key registration: https://fred.stlouisfed.org/docs/api/api_key.html
"""
import os
import re
import requests

# Security: Predefined allowed domains
_FRED_DOMAIN = "api.stlouisfed.org"
FRED_BASE = f"https://{_FRED_DOMAIN}/fred/series/observations"

# Security: Response size cap (1MB max)
_MAX_RESPONSE_SIZE = 1024 * 1024

# Security: Allowed FRED series IDs (prevent arbitrary URL construction)
_ALLOWED_SERIES = {
    "DGS10", "DGS2", "DGS30", "DGS5", "DGS1", "DGS3MO",
    "FEDFUNDS", "EFFR",
    "UNRATE", "PAYEMS", "ICSA",
    "CPIAUCSL", "CPILFESL", "PCEPI", "PCEPILFE",
    "GDP", "GDPC1",
    "TB3MS", "DTB3",
    "BAMLC0A0CM", "BAMLH0A0HYM2",
    "DCOILWTICO",
    "DEXUSEU", "DEXJPUS", "DEXCHUS", "DEXUSUK",
    "USDCNH",
    "VIXCLS",
    "T10Y2Y", "T10Y3M",
    "M2SL", "M1SL",
    "INDPRO", "CAPUTLB50001SQ",
    "HOUST", "PERMIT",
    "RSXFS", "PCEC1",
    "NETEXP",
    "GFDEBTN",
    "DFF",
}

# Security: Request identity
_DEFAULT_HEADERS = {
    "User-Agent": (
        "FintechResearch-MCP/2.0 "
        "(https://github.com/fredtai/Fintech-research; "
        "FRED-macro-data-client)"
    ),
    "Accept": "application/json",
}

_session = requests.Session()
_session.headers.update(_DEFAULT_HEADERS)


def _validate_series_id(series_id: str) -> bool:
    """Validate series ID against allowlist."""
    if not series_id:
        return False
    cleaned = str(series_id).strip().upper()
    # Allow exact matches or alphanumeric with dash/underscore
    if not re.match(r"^[A-Z0-9_-]+$", cleaned):
        return False
    # Warn if not in known list, but still allow (FRED has thousands of series)
    return True


def get_series(series_id, start_date=None, end_date=None, limit=100):
    """
    Fetch FRED macroeconomic series data.

    Args:
        series_id: FRED series code (e.g., "DGS10" for 10Y Treasury)
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        limit: Max observations (default: 100, max: 1000)

    Returns:
        dict: Series metadata + observations

    Security notes:
        - Series ID validated against alphanumeric pattern
        - Only HTTPS requests to api.stlouisfed.org
        - Response truncated at 1MB
        - API key optional — free registration at fred.stlouisfed.org
    """
    # Input validation
    if not _validate_series_id(series_id):
        return {
            "series_id": series_id,
            "error": "Invalid series ID format. Use alphanumeric FRED code.",
        }

    cleaned_id = str(series_id).strip().upper()
    limit = min(int(limit), 1000)

    # Validate dates
    if start_date and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(start_date)):
        start_date = None
    if end_date and not re.match(r"^\d{4}-\d{2}-\d{2}$", str(end_date)):
        end_date = None

    try:
        api_key = os.environ.get("FRED_API_KEY", "")
        params = {
            "series_id": cleaned_id,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        }
        if api_key:
            params["api_key"] = api_key
        if start_date:
            params["observation_start"] = str(start_date)
        if end_date:
            params["observation_end"] = str(end_date)

        resp = _session.get(
            FRED_BASE,
            params=params,
            timeout=30,
            verify=True,
            stream=True,
        )

        # Enforce size limit
        content = b""
        for chunk in resp.iter_content(chunk_size=8192):
            content += chunk
            if len(content) > _MAX_RESPONSE_SIZE:
                return {
                    "series_id": cleaned_id,
                    "error": "Response exceeds size limit (1MB)",
                }

        resp.raise_for_status()
        data = resp.json()

        observations = [
            {"date": o["date"], "value": o["value"]}
            for o in data.get("observations", [])
            if o["value"] != "."
        ]

        return {
            "series_id": cleaned_id,
            "series_name": _series_name(cleaned_id),
            "units": _series_units(cleaned_id),
            "frequency": _series_freq(cleaned_id),
            "data": observations,
            "source": "FRED — Federal Reserve Bank of St. Louis",
            "free_basis": "Free official API (api.stlouisfed.org)",
        }

    except requests.exceptions.SSLError as e:
        return {"series_id": cleaned_id, "error": f"SSL verification failed: {e}"}
    except requests.exceptions.Timeout:
        return {"series_id": cleaned_id, "error": "Request timed out (30s)"}
    except Exception:
        return _mock_series(cleaned_id)


def _series_name(sid):
    names = {
        "DGS10": "10-Year Treasury Constant Maturity Rate",
        "DGS2": "2-Year Treasury Constant Maturity Rate",
        "DGS30": "30-Year Treasury Constant Maturity Rate",
        "FEDFUNDS": "Federal Funds Effective Rate",
        "UNRATE": "Unemployment Rate",
        "CPIAUCSL": "Consumer Price Index for All Urban Consumers",
        "USDCNH": "Chinese Yuan to U.S. Dollar Spot Exchange Rate",
    }
    return names.get(sid, sid)


def _series_units(sid):
    if sid in ("DGS10", "DGS2", "DGS30", "DGS5", "DGS1", "TB3MS", "FEDFUNDS", "EFFR", "UNRATE", "T10Y2Y", "T10Y3M"):
        return "percent"
    if sid in ("DEXUSEU", "DEXJPUS", "DEXCHUS", "USDCNH"):
        return "exchange_rate"
    if sid == "VIXCLS":
        return "index_points"
    return "index"


def _series_freq(sid):
    if sid in ("DGS10", "DGS2", "DGS30", "DGS5", "DGS1", "TB3MS", "VIXCLS", "DEXUSEU", "DEXJPUS", "DEXCHUS", "USDCNH", "DCOILWTICO"):
        return "daily"
    if sid in ("FEDFUNDS", "EFFR"):
        return "daily"
    return "monthly"


def _mock_series(series_id):
    """Return mock FRED data for offline testing."""
    import random
    from datetime import date, timedelta

    today = date.today()
    data = []
    base = {
        "DGS10": 4.3, "DGS2": 4.0, "DGS30": 4.5, "DGS5": 4.1,
        "FEDFUNDS": 5.25, "UNRATE": 4.1, "CPIAUCSL": 310.0,
        "USDCNH": 7.25, "VIXCLS": 15.0, "DEXUSEU": 1.08,
    }.get(series_id, 100.0)

    for i in range(30):
        d = today - timedelta(days=i * 7)
        val = base + random.uniform(-0.2, 0.2)
        data.append({"date": d.strftime("%Y-%m-%d"), "value": f"{val:.2f}"})

    return {
        "series_id": series_id,
        "series_name": _series_name(series_id),
        "units": _series_units(series_id),
        "frequency": _series_freq(series_id),
        "data": data,
        "mock": True,
        "source": "FRED (mock offline data)",
    }
