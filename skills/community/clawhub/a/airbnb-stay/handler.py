"""
airbnb-stay skill handler — single-listing Airbnb lookups via the Staying API.

Pure standard library. Bearer token in STAYINGAPI_KEY.
Errors are returned as {"error": "...", "detail": "..."} dicts rather than raised.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.stayingapi.com/v1"
USER_AGENT = "airbnb-skills/1.0.1 (+https://github.com/nikhonit/airbnb-skills)"
TIMEOUT_SECONDS = 30


def _key():
    k = os.environ.get("STAYINGAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "STAYINGAPI_KEY environment variable is not set. "
            "Get a free key in 30 seconds at https://stayingapi.com/app/keys "
            "(100 credits, no card required). Then export STAYINGAPI_KEY=sk_..."
        )
    return k


def _request(path, params=None):
    try:
        url = API_BASE + path
        if params:
            filtered = {k: v for k, v in params.items() if v is not None}
            if filtered:
                url = url + "?" + urllib.parse.urlencode(filtered)
        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "Authorization": "Bearer " + _key(),
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8")[:1000]
        except Exception:
            detail = ""
        return {"error": "HTTP " + str(e.code), "detail": detail}
    except urllib.error.URLError as e:
        return {"error": "network", "detail": str(e.reason)}
    except RuntimeError as e:
        return {"error": "auth", "detail": str(e)}
    except Exception as e:
        return {"error": "unexpected", "detail": str(e)}


def lookup_stay_by_id(stay_id, fields=None):
    """
    Look up a single Airbnb listing by its numeric id.

    fields: optional comma-separated projection (e.g. "id,title,pricing,star_rating").
    Returns the canonical Stay record, or {"error": ..., "detail": ...} on failure.
    """
    return _request("/stays/" + str(stay_id), params={"fields": fields})


def lookup_stay_by_url(url, fields=None):
    """Look up a listing by its airbnb.com/rooms/<id> URL."""
    return _request("/stays/by-url", params={"url": url, "fields": fields})


def lookup_stay_by_address(address, fields=None):
    """
    Resolve a listing from a street address (weighted at 3 credits per call).
    Use this only when you have an address rather than an id or URL.
    """
    return _request("/stays/by-address", params={"address": address, "fields": fields})


def get_stay_photos(stay_id=None, url=None, address=None):
    """Get a listing's photo gallery. Pass stay_id (cheapest), url, or address."""
    return _subresource("photos", stay_id, url, address)


def get_stay_reviews(stay_id=None, url=None, address=None):
    """Get a listing's reviews and rating breakdown."""
    return _subresource("reviews", stay_id, url, address)


def get_stay_host(stay_id=None, url=None, address=None):
    """Get a listing's host profile."""
    return _subresource("host", stay_id, url, address)


def get_stay_amenities(stay_id=None, url=None, address=None):
    """Get a listing's amenities grouped by category."""
    return _subresource("amenities", stay_id, url, address)


def get_stay_availability(stay_id=None, url=None, address=None):
    """Get a listing's per-date availability calendar."""
    return _subresource("availability", stay_id, url, address)


def get_stay_pricing(stay_id=None, url=None, address=None):
    """Get a listing's pricing block (nightly rate, fees, currency)."""
    return _subresource("pricing", stay_id, url, address)


def get_stay_location(stay_id=None, url=None, address=None):
    """Get a listing's coordinates and address."""
    return _subresource("location", stay_id, url, address)


def get_stay_rating(stay_id=None, url=None, address=None):
    """Get a listing's star rating and review-count summary."""
    return _subresource("rating", stay_id, url, address)


def _subresource(name, stay_id, url, address):
    sid = _resolve_stay_id(stay_id, url, address)
    if isinstance(sid, dict):
        return sid
    return _request("/stays/" + sid + "/" + name)


def _resolve_stay_id(stay_id=None, url=None, address=None):
    if stay_id:
        return str(stay_id)
    if url:
        record = _request("/stays/by-url", params={"url": url, "fields": "id"})
    elif address:
        record = _request("/stays/by-address", params={"address": address, "fields": "id"})
    else:
        return {"error": "invalid_argument", "detail": "Provide stay_id, url, or address"}
    if "error" in record:
        return record
    resolved = record.get("id") or (record.get("data") or {}).get("id")
    if not resolved:
        return {"error": "not_found", "detail": "Could not resolve a stay id"}
    return str(resolved)
