"""
edgrapi-full skill handler — all five US government sources over the Edgrapi REST
API.

SEC EDGAR:  get_fundamentals, get_ratios, get_company, get_filings
Government: get_opportunities (SAM.gov), get_awards (USAspending),
            get_grants (Grants.gov), get_congress, get_congress_ticker

Pure standard library. API key in EDGRAPI_KEY, sent as the X-API-Key header.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://edgrapi.com"  # hardcoded: the API key is never sent to any other host
USER_AGENT = "edgrapi-skills/1.1.0 (+https://github.com/paperandbeyond23-gif/edgrapi-skills)"
TIMEOUT_SECONDS = 60

SIGNUP_URL = "https://edgrapi.com/app"
KEYS_URL = "https://edgrapi.com/app"
PRICING_URL = "https://edgrapi.com/pricing"

PERIODS = ("annual", "quarterly")
AWARD_CATEGORIES = ("contracts", "idvs", "grants", "loans", "direct_payments", "other")
PTYPES = ("o", "p", "a")
ACTIONS = ("buy", "sell")


def _key():
    k = os.environ.get("EDGRAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "EDGRAPI_KEY environment variable is not set. "
            "Get a free key (100 free credits, no card) at " + SIGNUP_URL + ", "
            "then export EDGRAPI_KEY=edgr_..."
        )
    return k


def _http_error(e):
    try:
        detail = e.read().decode("utf-8")[:1000]
    except Exception:
        detail = ""
    if e.code == 401:
        return {
            "error": "auth_invalid",
            "detail": "EDGRAPI_KEY was rejected. Mint a new key at " + KEYS_URL + ".",
            "keys_url": KEYS_URL,
            "http_status": 401,
        }
    if e.code == 403:
        return {
            "error": "rapidapi_only",
            "detail": (
                "This Edgrapi origin is locked to RapidAPI subscribers. Subscribe via "
                "the RapidAPI listing, or use a direct key against the public host."
            ),
            "http_status": 403,
        }
    if e.code == 404:
        return {
            "error": "not_found",
            "detail": (
                "No record matched. For SEC tools use the exact listed symbol "
                "(e.g. AAPL, BRK-B); for government tools check the filter values."
            ),
            "http_status": 404,
        }
    if e.code == 402:
        return {
            "error": "out_of_credits",
            "detail": "Out of Edgrapi credits. Top up a pack or subscribe at " + PRICING_URL + ".",
            "upgrade_url": PRICING_URL,
            "http_status": 402,
        }
    if e.code == 429:
        return {
            "error": "rate_limit_exceeded",
            "detail": "Plan request limit hit. Back off, or upgrade at " + PRICING_URL + ".",
            "upgrade_url": PRICING_URL,
            "http_status": 429,
        }
    if e.code in (502, 503, 504):
        return {
            "error": "source_unavailable",
            "detail": (
                "The upstream source (SEC EDGAR, SAM.gov, USAspending, Grants.gov or the "
                "House clerk) was unreachable. Retry shortly."
            ),
            "http_status": e.code,
        }
    return {"error": "HTTP " + str(e.code), "detail": detail}


def _get(path, params=None):
    try:
        qs = ""
        if params:
            clean = {k: v for k, v in params.items() if v is not None}
            if clean:
                qs = "?" + urllib.parse.urlencode(clean)
        req = urllib.request.Request(
            API_BASE + path + qs,
            method="GET",
            headers={
                "X-API-Key": _key(),
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        return _http_error(e)
    except urllib.error.URLError as e:
        return {"error": "network", "detail": str(e.reason)}
    except RuntimeError as e:
        return {"error": "auth_required", "detail": str(e), "signup_url": SIGNUP_URL}
    except Exception as e:
        return {"error": "unexpected", "detail": str(e)}


def _ticker(t):
    return urllib.parse.quote((t or "").strip().upper(), safe="")


def get_fundamentals(ticker, period="annual", limit=5):
    """
    Normalized income-statement, balance-sheet, and cash-flow figures for `ticker`,
    parsed from SEC EDGAR XBRL companyfacts.

    period: "annual" (10-K) or "quarterly" (10-Q), default "annual".
    limit:  number of periods to return, 1-20 (default 5).
    Returns a dict with periodized statements, or an {"error": ...} dict.
    """
    if not ticker:
        return {"error": "invalid_argument", "detail": "ticker is required."}
    if period not in PERIODS:
        return {"error": "invalid_argument", "detail": "period must be 'annual' or 'quarterly'."}
    return _get("/v1/fundamentals/" + _ticker(ticker), {"period": period, "limit": limit})


def get_ratios(ticker):
    """
    Computed financial ratios for `ticker` (margins, returns, leverage, liquidity)
    derived from SEC EDGAR fundamentals. Price-based ratios (P/E, P/B) are not
    included — EDGAR carries no market price.
    """
    if not ticker:
        return {"error": "invalid_argument", "detail": "ticker is required."}
    return _get("/v1/ratios/" + _ticker(ticker))


def get_company(ticker):
    """
    Company profile for `ticker`: CIK, legal name, SIC industry, fiscal-year end,
    exchanges, and website, resolved from SEC EDGAR submissions.
    """
    if not ticker:
        return {"error": "invalid_argument", "detail": "ticker is required."}
    return _get("/v1/company/" + _ticker(ticker))


def get_filings(ticker, limit=20, form=None):
    """
    Recent SEC filings for `ticker` with filing/report dates and document links.

    limit: number of filings to return, 1-100 (default 20).
    form:  optional filter by form type, e.g. "10-K", "10-Q", "8-K".
    """
    if not ticker:
        return {"error": "invalid_argument", "detail": "ticker is required."}
    return _get("/v1/filings/" + _ticker(ticker), {"limit": limit, "form": form})


def get_opportunities(posted_from=None, posted_to=None, limit=20, offset=0,
                      naics=None, ptype=None, state=None, set_aside=None, title=None):
    """
    Open federal contract opportunities from SAM.gov.

    posted_from / posted_to: YYYY-MM-DD. Defaults to the last 30 days. SAM.gov caps
        the posted window at one year; a wider range comes back empty rather than erroring.
    naics:     NAICS code, up to 6 digits. Pass it plainly — SAM.gov's own API wants
               `ncode` and silently ignores `naics`; Edgrapi handles that translation.
    ptype:     "o" solicitation, "p" presolicitation, "a" award notice.
    state:     place-of-performance state, e.g. "TX".
    set_aside: e.g. "SBA", "8A", "WOSB", "HZC".
    title:     match on opportunity title.

    Costs 2 credits. Federal only — there is no state or local (SLED) coverage.
    """
    if ptype is not None and ptype not in PTYPES:
        return {"error": "invalid_argument",
                "detail": "ptype must be 'o' (solicitation), 'p' (presolicitation) or 'a' (award)."}
    return _get("/v1/opportunities", {
        "posted_from": posted_from, "posted_to": posted_to, "limit": limit,
        "offset": offset, "naics": naics, "ptype": ptype, "state": state,
        "set_aside": set_aside, "title": title,
    })


def get_awards(category="contracts", keyword=None, agency=None, recipient=None,
               state=None, start=None, end=None, limit=20, page=1,
               sort="amount", order="desc"):
    """
    Federal awards from USAspending: who was paid, how much, by which agency.

    category:  contracts, idvs, grants, loans, direct_payments or other.
    agency:    top-tier awarding agency, exact name, e.g. "Department of Defense".
    recipient: recipient name search, e.g. "Lockheed".
    start/end: action-date range, YYYY-MM-DD. Defaults to the last year. USAspending
               search cannot reach before 2007-10-01.
    sort:      amount, start or end.   order: asc or desc.

    Costs 2 credits. Edgrapi paginates past USAspending's own `hasNext` bug, which
    reports no further pages at record 10,000 while rows continue to 50,000.
    """
    if category not in AWARD_CATEGORIES:
        return {"error": "invalid_argument",
                "detail": "category must be one of: " + ", ".join(AWARD_CATEGORIES) + "."}
    if order not in ("asc", "desc"):
        return {"error": "invalid_argument", "detail": "order must be 'asc' or 'desc'."}
    return _get("/v1/awards", {
        "category": category, "keyword": keyword, "agency": agency,
        "recipient": recipient, "state": state, "start": start, "end": end,
        "limit": limit, "page": page, "sort": sort, "order": order,
    })


def get_grants(keyword=None, status=None, agency=None, category=None,
               eligibility=None, aln=None, limit=20, offset=0):
    """
    Federal grant funding opportunities from Grants.gov.

    status:      pipe or comma separated list of forecasted, posted, closed, archived.
    agency:      agency code, e.g. "HHS-OPHS".
    category:    funding category code, e.g. "HL" for health.
    eligibility: eligibility code filter.
    aln:         Assistance Listing (CFDA) number, e.g. "93.217".

    Costs 2 credits. Federal grants only — no state or foundation programmes.
    """
    return _get("/v1/grants", {
        "keyword": keyword, "status": status, "agency": agency, "category": category,
        "eligibility": eligibility, "aln": aln, "limit": limit, "offset": offset,
    })


def get_congress(action=None, limit=40):
    """
    Recent congressional stock trades from US House STOCK Act disclosures.

    action: "buy" or "sell" to filter, or None for both.
    limit:  trades to return (default 40).

    Costs 2 credits.

    Limits worth stating to any user of this data: US House only — the Senate files
    separately and is not covered. Disclosures lag the trade by up to 45 days by law,
    and amounts are reported as dollar ranges, not exact figures.
    """
    if action is not None and action not in ACTIONS:
        return {"error": "invalid_argument", "detail": "action must be 'buy' or 'sell'."}
    return _get("/v1/congress", {"action": action, "limit": limit})


def get_congress_ticker(ticker, limit=40):
    """
    Congressional trades in one stock, e.g. "NVDA".

    Costs 2 credits. Same limits as get_congress: US House only, up to 45 days
    behind, amounts as dollar ranges.
    """
    if not ticker:
        return {"error": "invalid_argument", "detail": "ticker is required."}
    safe = urllib.parse.quote((ticker or "").strip().upper(), safe="")
    return _get("/v1/congress/" + safe, {"limit": limit})
