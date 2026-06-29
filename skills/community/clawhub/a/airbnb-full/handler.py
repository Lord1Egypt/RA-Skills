"""
airbnb-full skill handler — calls the Staying API REST surface.

Pure standard library. No third-party dependencies.
Auth: bearer token in `STAYINGAPI_KEY` env var.
Errors are returned as {"error": "...", "detail": "..."} dicts rather than raised.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

API_BASE = "https://api.stayingapi.com/v1"
USER_AGENT = "airbnb-skills/1.0.1 (+https://github.com/nikhonit/airbnb-skills)"
TIMEOUT_SECONDS = 60


def _key():
    k = os.environ.get("STAYINGAPI_KEY", "").strip()
    if not k:
        raise RuntimeError(
            "STAYINGAPI_KEY environment variable is not set. "
            "Get a free key in 30 seconds at https://stayingapi.com/app/keys "
            "(100 credits, no card required). Then export STAYINGAPI_KEY=sk_..."
        )
    return k


def _request(method, path, params=None, body=None):
    try:
        url = API_BASE + path
        if params:
            filtered = {k: v for k, v in params.items() if v is not None}
            if filtered:
                url = url + "?" + urllib.parse.urlencode(filtered)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": "Bearer " + _key(),
                "Content-Type": "application/json",
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


# --- single listing -------------------------------------------------------
def lookup_stay_by_id(stay_id, fields=None):
    """Look up a single Airbnb listing by its numeric id. fields: optional projection."""
    return _request("GET", "/stays/" + str(stay_id), params={"fields": fields})


def lookup_stay_by_url(url, fields=None):
    """Look up a listing by its airbnb.com/rooms/<id> URL."""
    return _request("GET", "/stays/by-url", params={"url": url, "fields": fields})


def lookup_stay_by_address(address, fields=None):
    """Resolve a listing from a street address (weighted at 3 credits per call)."""
    return _request("GET", "/stays/by-address", params={"address": address, "fields": fields})


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


# --- search ---------------------------------------------------------------
def search_stays(
    location=None,
    search_urls=None,
    check_in=None,
    check_out=None,
    price_min=None,
    price_max=None,
    min_beds=None,
    min_bedrooms=None,
    min_bathrooms=None,
    adults=None,
    children=None,
    infants=None,
    pets=None,
    currency=None,
    locale=None,
    max_items=50,
    fields=None,
):
    """
    Search Airbnb listings by location and structured filters.

    Either `location` (e.g. "Austin, TX") or `search_urls` (a list of Airbnb
    search URLs) is required. check_in/check_out are "YYYY-MM-DD". Search costs
    1 credit per result; max_items (default 50, max 240) is your spend cap.
    """
    if not location and not search_urls:
        return {"error": "invalid_argument", "detail": "Provide either location or search_urls"}
    return _request("POST", "/search", body=_build_filters(locals()))


def search_superhost(**filters):
    """Superhost-only preset. Same filters as search_stays()."""
    return _preset_search("/listings/superhost", filters)


def search_instant_book(**filters):
    """Instant-bookable preset. Same filters as search_stays()."""
    return _preset_search("/listings/instant-book", filters)


def search_luxury(**filters):
    """Luxury-tier preset. Same filters as search_stays()."""
    return _preset_search("/listings/luxury", filters)


def search_stays_with_details(**filters):
    """
    Search then fetch full detail per result. Always async — returns a job
    envelope; poll with get_job / get_job_results. Same filters as search_stays().
    """
    return _preset_search("/search/with-details", filters)


# --- batch + jobs ---------------------------------------------------------
def batch_stays(targets, webhook_id=None):
    """
    Batch-resolve up to 500 listings asynchronously. `targets` is a list whose
    items are each a listing id, an airbnb.com/rooms URL, or a street address.
    Returns a job envelope; poll with get_job / get_job_results, or pass a
    webhook_id to be notified on completion.
    """
    if not targets:
        return {"error": "invalid_argument", "detail": "Provide a non-empty list of ids, URLs, or addresses"}
    entries = []
    for t in targets:
        t = str(t)
        if t.startswith("http"):
            entries.append({"url": t})
        elif t.isdigit():
            entries.append({"id": t})
        else:
            entries.append({"address": t})
    body = {"entries": entries}
    if webhook_id:
        body["webhook_id"] = webhook_id
    return _request("POST", "/stays/batch", body=body)


def list_jobs(status=None, type=None, since=None, limit=50, offset=0):
    """List async jobs for the account. Filter by status or type. limit max 200."""
    return _request(
        "GET",
        "/jobs",
        params={"status": status, "type": type, "since": since, "limit": limit, "offset": offset},
    )


def get_job(job_id):
    """Get the status of a single async job."""
    return _request("GET", "/jobs/" + str(job_id))


def get_job_results(job_id, limit=50, offset=0, format="json"):
    """Read paginated results for a succeeded job. format: json | csv | ndjson. limit max 100."""
    return _request(
        "GET",
        "/jobs/" + str(job_id) + "/results",
        params={"limit": limit, "offset": offset, "format": format},
    )


# --- webhooks -------------------------------------------------------------
def create_webhook(url, events, description=None):
    """
    Create an outbound webhook subscription. `events` is a list from:
    job.queued, job.running, job.succeeded, job.failed, stay.cached.
    Deliveries are HMAC-signed.
    """
    if not url or not events:
        return {"error": "invalid_argument", "detail": "Provide url and a non-empty events list"}
    body = {"url": url, "events": events}
    if description:
        body["description"] = description
    return _request("POST", "/webhooks", body=body)


def list_webhooks():
    """List webhook subscriptions for the account."""
    return _request("GET", "/webhooks")


def get_webhook(webhook_id):
    """Get a single webhook subscription."""
    return _request("GET", "/webhooks/" + str(webhook_id))


def delete_webhook(webhook_id):
    """Revoke a webhook subscription."""
    return _request("DELETE", "/webhooks/" + str(webhook_id))


def get_webhook_deliveries(webhook_id):
    """List the last 200 delivery attempts for a webhook."""
    return _request("GET", "/webhooks/" + str(webhook_id) + "/deliveries")


# --- account --------------------------------------------------------------
def get_account():
    """Get the authenticated account, plan, and credit balance."""
    return _request("GET", "/me")


def get_usage(since=None, limit=50):
    """List recent metered API calls, most recent first. limit max 500."""
    return _request("GET", "/usage", params={"since": since, "limit": limit})


# --- internals ------------------------------------------------------------
def _build_filters(opts):
    location = opts.get("location")
    body = {
        "locationQueries": [location] if location else None,
        "searchUrls": opts.get("search_urls"),
        "checkIn": opts.get("check_in"),
        "checkOut": opts.get("check_out"),
        "priceMin": opts.get("price_min"),
        "priceMax": opts.get("price_max"),
        "minBeds": opts.get("min_beds"),
        "minBedrooms": opts.get("min_bedrooms"),
        "minBathrooms": opts.get("min_bathrooms"),
        "adults": opts.get("adults"),
        "children": opts.get("children"),
        "infants": opts.get("infants"),
        "pets": opts.get("pets"),
        "currency": opts.get("currency"),
        "locale": opts.get("locale"),
        "maxItems": opts.get("max_items", 50),
        "fields": opts.get("fields"),
    }
    return {k: v for k, v in body.items() if v is not None}


def _preset_search(path, filters):
    if not filters.get("location") and not filters.get("search_urls"):
        return {"error": "invalid_argument", "detail": "Provide either location or search_urls"}
    return _request("POST", path, body=_build_filters(filters))


def _subresource(name, stay_id, url, address):
    sid = _resolve_stay_id(stay_id, url, address)
    if isinstance(sid, dict):
        return sid
    return _request("GET", "/stays/" + sid + "/" + name)


def _resolve_stay_id(stay_id=None, url=None, address=None):
    if stay_id:
        return str(stay_id)
    if url:
        record = _request("GET", "/stays/by-url", params={"url": url, "fields": "id"})
    elif address:
        record = _request("GET", "/stays/by-address", params={"address": address, "fields": "id"})
    else:
        return {"error": "invalid_argument", "detail": "Provide stay_id, url, or address"}
    if "error" in record:
        return record
    resolved = record.get("id") or (record.get("data") or {}).get("id")
    if not resolved:
        return {"error": "not_found", "detail": "Could not resolve a stay id"}
    return str(resolved)
