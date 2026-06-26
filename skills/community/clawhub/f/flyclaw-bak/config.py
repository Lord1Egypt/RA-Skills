"""FlyClaw configuration loader.

Reads config.yaml and provides defaults for all settings.
"""

import json
import logging
import os
import yaml

logger = logging.getLogger("flyclaw.config")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(PROJECT_DIR, "config.yaml")
AIRLINES_FILE = os.path.join(PROJECT_DIR, "cache", "airlines_iata_icao.json")

# ---------------------------------------------------------------------------
# Network constants
# ---------------------------------------------------------------------------
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)
FR24_API_BASE = "https://api.flightradar24.com/common/v1"
AIRPLANESLIVE_API_BASE = "https://api.airplanes.live/v2"
ADSB_LOL_API_BASE = "https://api.adsb.lol/v2"

# Default airport data update URL (set to GitHub raw URL after project is published)
AIRPORT_UPDATE_URL = ""

# ---------------------------------------------------------------------------
# IATA → ICAO airline code mapping (for ADS-B callsign conversion)
# ---------------------------------------------------------------------------
IATA_TO_ICAO_AIRLINE = {
    # China
    "CA": "CCA",   # Air China
    "MU": "CES",   # China Eastern
    "CZ": "CSN",   # China Southern
    "3U": "CSC",   # Sichuan Airlines
    "HU": "CHH",   # Hainan Airlines
    "ZH": "CSZ",   # Shenzhen Airlines
    "MF": "CXA",   # Xiamen Airlines
    "FM": "CSH",   # Shanghai Airlines
    "KN": "CUA",   # China United Airlines
    "GS": "GCR",   # Tianjin Airlines
    "TV": "TBA",   # Tibet Airlines
    "SC": "CDG",   # Shandong Airlines
    "PN": "CHB",   # West Air
    "9C": "CQH",   # Spring Airlines
    "HO": "DKH",   # Juneyao Airlines
    "EU": "UEA",   # Chengdu Airlines
    "GJ": "CDC",   # Loong Air
    "QW": "CQN",   # Qingdao Airlines
    # Asia
    "JL": "JAL",   # Japan Airlines
    "NH": "ANA",   # ANA
    "KE": "KAL",   # Korean Air
    "OZ": "AAR",   # Asiana Airlines
    "SQ": "SIA",   # Singapore Airlines
    "CX": "CPA",   # Cathay Pacific
    "TG": "THA",   # Thai Airways
    "VN": "HVN",   # Vietnam Airlines
    "BR": "EVA",   # EVA Air
    "CI": "CAL",   # China Airlines (Taiwan)
    # North America
    "AA": "AAL",   # American Airlines
    "UA": "UAL",   # United Airlines
    "DL": "DAL",   # Delta Air Lines
    "WN": "SWA",   # Southwest Airlines
    "AC": "ACA",   # Air Canada
    "B6": "JBU",   # JetBlue
    "AS": "ASA",   # Alaska Airlines
    # Europe
    "BA": "BAW",   # British Airways
    "LH": "DLH",   # Lufthansa
    "AF": "AFR",   # Air France
    "KL": "KLM",   # KLM
    "SK": "SAS",   # SAS
    "AY": "FIN",   # Finnair
    "IB": "IBE",   # Iberia
    "TK": "THY",   # Turkish Airlines
    "LX": "SWR",   # Swiss International
    "OS": "AUA",   # Austrian Airlines
    # Middle East / Oceania
    "EK": "UAE",   # Emirates
    "QR": "QTR",   # Qatar Airways
    "EY": "ETD",   # Etihad Airways
    "QF": "QFA",   # Qantas
    "NZ": "ANZ",   # Air New Zealand
    "SV": "SVA",   # Saudia
}


def _load_airline_mapping() -> dict[str, str]:
    """Load IATA→ICAO airline mapping from JSON file.

    Falls back to built-in IATA_TO_ICAO_AIRLINE dict if file is missing
    or corrupt.
    """
    try:
        with open(AIRLINES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and len(data) > 0:
            return data
    except (OSError, json.JSONDecodeError, TypeError) as e:
        logger.debug("Airline mapping file not available (%s), using built-in", e)
    return IATA_TO_ICAO_AIRLINE


_AIRLINE_MAPPING = _load_airline_mapping()


def iata_flight_to_icao_callsign(flight_number: str) -> str | None:
    """Convert IATA flight number (e.g. 'CA981') to ICAO callsign (e.g. 'CCA981').

    Returns None if the airline code is not in the mapping.
    """
    if not flight_number:
        return None
    fn = flight_number.strip().upper()
    # Try 2-char airline prefix first, then 1-char (unlikely but safe)
    for prefix_len in (2, 1):
        airline = fn[:prefix_len]
        numeric = fn[prefix_len:]
        if airline in _AIRLINE_MAPPING and numeric:
            return f"{_AIRLINE_MAPPING[airline]}{numeric}"
    return None

# ---------------------------------------------------------------------------
# Default config (used when config.yaml is missing or incomplete)
# ---------------------------------------------------------------------------
DEFAULTS = {
    "sources": {
        "fr24": {"enabled": True, "priority": 1, "timeout": 10},
        "google_flights": {
            "enabled": True,
            "priority": 2,
            "timeout": 15,
            "serpapi_key": "",
            "retry": 2,
            "retry_delay": 0.5,
            "retry_backoff": 2.0,
        },
        "skiplagged": {
            "enabled": True, "priority": 2, "timeout": 12,
            "retry": 4, "retry_delay": 0.5, "retry_backoff": 2.0,
            "mcp_enabled": False,
            "mcp_url": "https://mcp.skiplagged.com/mcp",
        },
        "fliggy_mcp": {
            "enabled": True, "priority": 2, "timeout": 10,
            "api_key": "", "sign_secret": "",
        },
        "airplanes_live": {"enabled": True, "priority": 3, "timeout": 6},
        "fast_flights": {"enabled": False, "timeout": 15},
    },
    "cache": {"dir": "cache", "airport_update_days": 99999, "airport_update_url": ""},
    "query": {
        "timeout": 20, "return_time": 12, "route_relay": True,
        "relay_timeout": 8,
        "filter_inactive_airports": True,
        "relay_engines": {"google_flights": True, "skiplagged": True},
        "sufficient_source": "fliggy_mcp",
    },
    "output": {
        "format": "json", "language": "both",
        "currency": "cny",
        "exchange_rate_cny_usd": 7.25,
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    """Merge *override* into *base*, returning a new dict."""
    result = base.copy()
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def get_config(config_path: str | None = None) -> dict:
    """Load configuration from YAML, falling back to defaults."""
    path = config_path or CONFIG_FILE
    cfg = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
    return _deep_merge(DEFAULTS, cfg)
