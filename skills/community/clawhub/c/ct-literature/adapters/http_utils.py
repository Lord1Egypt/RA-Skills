#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http_utils.py — shared HTTP helper for ct-literature (exponential-backoff retry).

Used by all three fetchers (OpenAlex / Europe PMC / Semantic Scholar) to centralize:
  - HTTP 429: read the `Retry-After` header and wait that many seconds before retry (compliant backoff)
  - 5xx / connection errors / timeouts: exponential backoff (backoff ** (attempt-1))
  - 4xx parameter errors: treated as non-retryable and raised immediately
  - retries exhausted: raise HttpError; the caller decides degradation or abort

Background: OpenAlex has required an API key since 2026-02-13 — without a key only
100 credits/day (officially "not suitable for production"); a free key lifts the cap
to 100k/day. A key enters the keyed pool via the `Authorization: Bearer <key>` header;
even with a key, keep the polite-pool `mailto` identity. This module provides
build_openalex_headers() to construct those headers uniformly.

Zero confidential data or information input; reads only public literature.
"""
import base64
import http.client
import io
import json
import os
import ssl
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

UA = "ct-literature/0.3.3"

# ── Pooled connections (per-thread keep-alive + per-host concurrency cap) ─────
# urllib.request.urlopen opens a fresh TCP+TLS connection per request. During
# citation verification (~2 HTTP round-trips per work) that means hundreds of
# handshakes. We keep one HTTPS connection per thread per host (thread-local) and
# reuse it across requests; a per-host semaphore caps concurrent in-flight requests
# so the politeness / anti-throttle posture is preserved — the cap is the *rate
# limit*, independent of the caller's worker-pool size.
_POOL_LOCAL = threading.local()
_POOL_HOST_SEMS = {}
_POOL_HOST_SEMS_LOCK = threading.Lock()
# Per-host concurrency caps (polite pools). Unknown hosts fall back to 4.
_POOL_HOST_MAX = {
    "doi.org": 8,
    "api.crossref.org": 4,
    "api.openalex.org": 6,
    "ebi.ac.uk": 6,
    "api.semanticscholar.org": 2,
    "export.arxiv.org": 2,
    # NCBI E-utilities：无 API key 限 3 req/s、有 key 10 req/s。并发上限压到 2，
    # 配合 fetch_pubmed._throttle() 的串行节拍，避免触发 429。
    "eutils.ncbi.nlm.nih.gov": 2,
}


def _pool_sem(host):
    with _POOL_HOST_SEMS_LOCK:
        sem = _POOL_HOST_SEMS.get(host)
        if sem is None:
            sem = threading.Semaphore(_POOL_HOST_MAX.get(host, 4))
            _POOL_HOST_SEMS[host] = sem
        return sem


def _pool_conn(host, timeout):
    key = "conn_" + host
    conn = getattr(_POOL_LOCAL, key, None)
    if conn is None:
        conn = http.client.HTTPSConnection(host, timeout=timeout)
        setattr(_POOL_LOCAL, key, conn)
    return conn


def _pooled_request(url, headers, timeout, max_redirects=5, data=None, method="GET"):
    """GET (or POST when `data` is given) with pooled keep-alive connections +
    manual redirect following.

    Mirrors urllib.request.urlopen semantics (redirects, HTTPError) so the retry
    loop in _request_with_retry stays unchanged. One connection per thread per host
    is reused; a stale/failed connection is dropped and rebuilt. The per-host
    semaphore caps concurrent in-flight requests (politeness / anti-throttle).

    `data` (bytes / None) is the request body; `method` is honoured as given
    (redirects re-issue the same method, matching urllib's 307/308 behaviour).
    """
    target = url
    for _ in range(max_redirects + 1):
        parts = urllib.parse.urlsplit(target)
        host = parts.netloc
        path = parts.path or "/"
        if parts.query:
            path += "?" + parts.query
        conn = None
        try:
            with _pool_sem(host):
                conn = _pool_conn(host, timeout)
                conn.request(method, path, body=data, headers=headers)
                resp = conn.getresponse()
                body = resp.read()
            if resp.status in (301, 302, 303, 307, 308) and resp.getheader("Location"):
                target = urllib.parse.urljoin(target, resp.getheader("Location"))
                continue
            if resp.status >= 400:
                raise urllib.error.HTTPError(
                    target, resp.status, "HTTP %s" % resp.status,
                    resp.getheaders(), io.BytesIO(body))
            return body
        except urllib.error.HTTPError:
            raise
        except (http.client.HTTPException, OSError, ValueError) as e:
            # stale/failed connection (server closed keep-alive, TLS reset, ...):
            # drop it so the next request rebuilds a fresh one.
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
                setattr(_POOL_LOCAL, "conn_" + host, None)
            raise urllib.error.URLError(reason=e)
    raise urllib.error.HTTPError(url, 302, "too many redirects", [], None)

# ── Lightweight .env key obfuscation (XOR+base64) ──────────────────────────────
# If the .env (holding the user's PRIVATE OpenAlex/S2 key) is ever accidentally
# packaged by a platform that ignores .gitignore/.clawhubignore (e.g. SkillHub),
# the shipped value is NOT the plaintext key — it fails naive grep/scan matching.
# NOT cryptography (the XOR key below is public); the real safeguard is that .env
# stays git/clawhub-ignored AND is stripped before any publish. _deobfuscate() is
# backward-compatible with a plaintext .env (returns the value unchanged on failure).
_OBF_XOR_KEY = b"ct-lit-obf-2026"


def _deobfuscate(val):
    """Reverse XOR+base64; return `val` unchanged if it isn't an obfuscated blob."""
    if not val:
        return val
    try:
        raw = base64.b64decode(val, validate=True)
        return bytes(c ^ _OBF_XOR_KEY[i % len(_OBF_XOR_KEY)]
                      for i, c in enumerate(raw)).decode("utf-8")
    except Exception:
        return val


class HttpError(Exception):
    """Unrecoverable HTTP / request error (retries exhausted or non-retryable 4xx)."""

    def __init__(self, message, status=None, retryable=False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable

    def __str__(self):
        if self.status is not None:
            return "[HTTP %s] %s" % (self.status, super().__str__())
        return super().__str__()


class RateLimitError(HttpError):
    """HTTP 429 — rate limit / quota exhausted.

    Carries the server's suggested `retry_after` (seconds, may be None) and whether
    the request was `keyless` (no Authorization header -> keyless pool, 100 credits/day).
    Callers should treat this as a *degradation* signal: stop hammering the API, surface
    a friendly notice, and continue with other sources instead of aborting.
    """

    def __init__(self, message, retry_after=None, keyless=False):
        super().__init__(message, status=429, retryable=True)
        self.retry_after = retry_after
        self.keyless = keyless


def _is_keyless(headers):
    """True when no Authorization header is present -> the request hits the keyless pool."""
    if not headers:
        return True
    for k in headers:
        if k.lower() == "authorization":
            return False
    return True


def _emit_429_notice(url, keyless, retry_after):
    """Print a concise, localized notice on the FIRST 429 of a request so the user
    sees the rate-limit event early (before retries finish). Never blocks execution."""
    try:
        from i18n import t
        if keyless:
            print(t("http.429.keyless_notice"))
        else:
            print(t("http.429.notice", secs=("%.0f" % retry_after) if retry_after else "—"))
    except Exception:
        print("[WARN] HTTP 429 rate limit hit on %s (keyless=%s)" % (_short(url), keyless))


def _request_with_retry(url, headers=None, timeout=45, max_retries=4, backoff=2.0,
                        rate_limit_max_retries=2, data=None, method="GET"):
    """Single request (GET by default, POST when `data` is given) returning raw
    bytes, with unified retry/backoff.

    Retry policy:
      - 429 + `Retry-After`: honor server's wait, retry up to `max_retries`
      - 429 WITHOUT Retry-After (OpenAlex keyless pool returns this on quota
        exhaustion, NOT transient): cap retries to `rate_limit_max_retries`, then
        raise RateLimitError (fast give-up instead of blind 4x retries)
      - 5xx / network / timeout: exponential backoff, retry up to `max_retries`
      - other 4xx: non-retryable, raise immediately
    """
    hdrs = {"User-Agent": UA}
    if headers:
        hdrs.update(headers)
    keyless = _is_keyless(hdrs)
    rl_seen = 0
    first_429 = False
    for attempt in range(1, max_retries + 1):
        try:
            return _pooled_request(url, hdrs, timeout, data=data, method=method)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                rl_seen += 1
                ra = _retry_after(e)
                if not first_429:
                    first_429 = True
                    _emit_429_notice(url, keyless, ra)
                if ra:
                    wait = ra
                    will_retry = attempt < max_retries
                else:
                    wait = backoff ** (attempt - 1)
                    will_retry = attempt < max_retries and rl_seen <= rate_limit_max_retries
                if will_retry:
                    print("[WARN] HTTP 429 on %s (attempt %d/%d, keyless=%s) -> retry in %.1fs"
                          % (_short(url), attempt, max_retries, keyless, wait))
                    time.sleep(wait)
                    continue
                raise RateLimitError(
                    "HTTP 429 after %d retry attempt(s) (keyless=%s)"
                    % (rl_seen, keyless), retry_after=ra, keyless=keyless)
            if 500 <= e.code < 600:
                if attempt < max_retries:
                    wait = backoff ** (attempt - 1)
                    print("[WARN] HTTP %s on %s (attempt %d/%d) -> retry in %.1fs"
                          % (e.code, _short(url), attempt, max_retries, wait))
                    time.sleep(wait)
                    continue
                raise HttpError("HTTP %s after %d retries" % (e.code, max_retries),
                                status=e.code, retryable=True)
            raise HttpError("HTTP %s (non-retryable)" % e.code, status=e.code, retryable=False)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as e:
            if attempt < max_retries:
                wait = backoff ** (attempt - 1)
                print("[WARN] request error on %s (attempt %d/%d): %s -> retry in %.1fs"
                      % (_short(url), attempt, max_retries, e, wait))
                time.sleep(wait)
                continue
            raise HttpError("request failed after %d retries: %s" % (max_retries, e),
                            retryable=True)
        except Exception as e:  # noqa: BLE001 - catch-all fallback, keep context
            if attempt < max_retries:
                wait = backoff ** (attempt - 1)
                print("[WARN] unexpected error on %s (attempt %d/%d): %s -> retry in %.1fs"
                      % (_short(url), attempt, max_retries, e, wait))
                time.sleep(wait)
                continue
            raise HttpError("unexpected failure after %d retries: %s" % (max_retries, e),
                            retryable=True)
    raise HttpError("unreachable retry loop", retryable=True)


def get_json(url, headers=None, timeout=45, max_retries=4, backoff=2.0,
             rate_limit_max_retries=2):
    """GET `url` and parse JSON, with built-in exponential-backoff retries.

    Returns: parsed dict / list.
    Raises:
      - HttpError: retries exhausted or unrecoverable 4xx.
      - RateLimitError: HTTP 429 (a *degradation* signal — see RateLimitError).
        Callers must catch it and continue with other sources.

    Retry policy:
      - 429 + Retry-After: honor server wait, retry up to `max_retries`
      - 429 without Retry-After (keyless quota exhaustion): cap to
        `rate_limit_max_retries` then raise RateLimitError (fail fast)
      - 5xx / network / timeout: exponential backoff, retry up to `max_retries`
      - 4xx (other than 429): non-retryable; raise immediately
    """
    raw = _request_with_retry(url, headers, timeout, max_retries, backoff,
                              rate_limit_max_retries)
    return json.loads(raw.decode("utf-8"))


def get_text(url, headers=None, timeout=45, max_retries=4, backoff=2.0,
             rate_limit_max_retries=2):
    """GET `url` and return decoded text, with built-in exponential-backoff retries.

    Used by sources (e.g. PROSPERO) that may return non-JSON (XML) payloads.
    Returns decoded str (lossy replacement on bad bytes). Mirrors get_json's retry
    policy (incl. RateLimitError on 429); caller degrades as needed.
    """
    raw = _request_with_retry(url, headers, timeout, max_retries, backoff,
                              rate_limit_max_retries)
    return raw.decode("utf-8", "replace")


def post_text(url, data, headers=None, timeout=45, max_retries=4, backoff=2.0,
              rate_limit_max_retries=2, method="POST"):
    """POST `data` (bytes) to `url` and return decoded text, with the same
    retry/backoff policy as get_text (incl. RateLimitError on 429).

    Added 2026-11-03 for PROSPERO's POST /PROSPERO/api/search endpoint (reverse-
    ported from meta-analysis, which verified it against the live registry). Kept
    generic so other POST-only sources can reuse the unified executor instead of
    hand-rolling urllib calls.
    """
    if isinstance(data, str):
        data = data.encode("utf-8")
    raw = _request_with_retry(url, headers, timeout, max_retries, backoff,
                              rate_limit_max_retries, data=data, method=method)
    return raw.decode("utf-8", "replace")


def build_openalex_headers(api_key=None, mailto="dev@example.com"):
    """Build OpenAlex request headers: polite-pool mailto (in UA) + optional Bearer key.

    OpenAlex recommends the polite-pool via a `mailto` query param or a mailto in the
    UA. With a key, additionally inject `Authorization: Bearer <key>` to enter the
    keyed pool.
    """
    hdrs = {"User-Agent": UA}
    if mailto:
        hdrs["User-Agent"] = "%s (mailto:%s)" % (UA, mailto)
    if api_key:
        hdrs["Authorization"] = "Bearer %s" % api_key
    return hdrs


def load_openalex_key(env_var="OPENALEX_API_KEY"):
    """Load the OpenAlex key, zero-dependency and ready out of the box:

    1. Prefer the env var `OPENALEX_API_KEY` (shell export / container injection);
    2. Otherwise try `.env` at the skill root or in scripts/ (hand-parsed, no python-dotenv);
       on a hit, write back to `os.environ` so later calls reuse it.

    Returns the key string or None. The key itself is NEVER printed to logs / stdout.
    """
    val = os.environ.get(env_var)
    if val:
        return val
    here = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(here)
    for cand in (os.path.join(skill_root, ".env"), os.path.join(here, ".env")):
        if not os.path.exists(cand):
            continue
        try:
            with open(cand, "r", encoding="utf-8") as _f:
                for _line in _f:
                    _line = _line.strip()
                    if not _line or _line.startswith("#"):
                        continue
                    if _line.startswith(env_var + "="):
                        _, _, _v = _line.partition("=")
                        _v = _v.strip().strip('"').strip("'")
                        _v = _deobfuscate(_v)
                        if _v:
                            os.environ[env_var] = _v
                            return _v
        except Exception:
            pass
    return None


def get_openalex_key(env_var="OPENALEX_API_KEY"):
    """Backward-compatible alias of load_openalex_key."""
    return load_openalex_key(env_var)


def get_openalex_key_status(env_var="OPENALEX_API_KEY"):
    """Return a SAFE status string only ('configured' | 'missing').

    Used by the provenance audit trail so the evidence log records whether a
    keyed source was used or the search fell back to keyless mode — this avoids
    silently taking the wrong (throttled) path. The key VALUE itself is never
    returned (ct-base §5: no credentials in logs).
    """
    return "configured" if load_openalex_key(env_var) else "missing"


# Public, free OpenAlex registration URL (keyless runs are rate-limited to
# 100 credits/day since 2026-02-13; a key raises this dramatically).
OPENALEX_SIGNUP_URL = "https://docs.openalex.org/about-openalex/api-key"


def build_s2_headers(api_key=None):
    """Build Semantic Scholar request headers: optional `x-api-key` for the keyed pool
    (much looser rate limit).

    Unauthenticated S2 Graph API is extremely strict (~1 req/s; shared-IP bursts get
    blocklisted for minutes); with a key it enters the keyed pool and throughput jumps.
    Runs without a key too, but easily hits 429 and degrades.
    """
    hdrs = {"User-Agent": UA}
    if api_key:
        hdrs["x-api-key"] = api_key
    return hdrs


def load_s2_key(env_var="SEMANTIC_SCHOLAR_API_KEY"):
    """Load the Semantic Scholar API key; same logic as load_openalex_key
    (env first, then .env fallback).

    Returns the key string or None. The key itself is NEVER printed to logs / stdout.
    """
    val = os.environ.get(env_var)
    if val:
        return val
    here = os.path.dirname(os.path.abspath(__file__))
    skill_root = os.path.dirname(here)
    for cand in (os.path.join(skill_root, ".env"), os.path.join(here, ".env")):
        if not os.path.exists(cand):
            continue
        try:
            with open(cand, "r", encoding="utf-8") as _f:
                for _line in _f:
                    _line = _line.strip()
                    if not _line or _line.startswith("#"):
                        continue
                    if _line.startswith(env_var + "="):
                        _, _, _v = _line.partition("=")
                        _v = _v.strip().strip('"').strip("'")
                        _v = _deobfuscate(_v)
                        if _v:
                            os.environ[env_var] = _v
                            return _v
        except Exception:
            pass
    return None


def key_status(api_key=None, env_var="OPENALEX_API_KEY"):
    """Return the *presence* of a configured API key as a machine-readable status
    string — never the key itself.

    Returns one of:
      "configured"  — a key was resolved for this run (env / .env / explicit arg)
      "missing"     — no key found; the skill runs keyless (rate-limited) or skips
      "not-required" — this source needs no key at all (e.g. Europe PMC)
    Used by the evidence log so a run records which sources had keys and which
    degraded to keyless / were skipped — "which path did this run take".
    """
    if api_key:
        return "configured"
    resolved = load_openalex_key(env_var)
    return "configured" if resolved else "missing"


# Module-level guard so the "no key" notice prints at most once per process.
_S2_KEY_NOTICE_SHOWN = False


def notify_s2_key_if_missing(api_key=None, env_var="SEMANTIC_SCHOLAR_API_KEY"):
    """Print a one-time, locale-aware notice when no Semantic Scholar API key is configured.

    Informational only — never blocks execution. S2's key requires a manual form
    review (not auto-issued), so a key is usually absent short-term; when absent the
    source is skipped entirely (no doomed 429 request) rather than degraded. Routing
    through i18n keeps the notice locale-correct.
    """
    global _S2_KEY_NOTICE_SHOWN
    if _S2_KEY_NOTICE_SHOWN:
        return
    _S2_KEY_NOTICE_SHOWN = True
    if api_key:
        return
    resolved = load_s2_key(env_var)
    if resolved:
        return
    from i18n import t
    print(t("semantic_scholar.key_notice"))


# Module-level guard so the "no key" notice prints at most once per day (用户 2026-09-07 要求每天提醒).
_KEY_NOTICE_SHOWN_DATE = None


def notify_openalex_key_if_missing(api_key=None, env_var="OPENALEX_API_KEY"):
    """Print a one-time-per-day, locale-aware notice when no OpenAlex API key is configured.

    Intended for the runtime entry points (ct_literature.run / fetch_openalex.fetch):
    when the key is absent the skill still works in keyless mode (100 credits/day since
    2026-02-13), but the user should be told how to apply for a FREE key so production-scale
    searches are not throttled. The notice is **informational only** — it never blocks execution.

    Args:
        api_key: the key already resolved for this run (may be None).
        env_var: env var name used to look up the key if api_key is None.
    """
    global _KEY_NOTICE_SHOWN_DATE
    from datetime import date
    today = date.today().isoformat()
    if _KEY_NOTICE_SHOWN_DATE == today:
        return
    if api_key:
        _KEY_NOTICE_SHOWN_DATE = today
        return
    # Re-resolve from env / .env; load_openalex_key() sets os.environ on a hit and
    # never prints the key value.
    resolved = load_openalex_key(env_var)
    if resolved:
        _KEY_NOTICE_SHOWN_DATE = today
        return
    from i18n import t
    print(t("openalex.key_notice", url=OPENALEX_SIGNUP_URL))
    _KEY_NOTICE_SHOWN_DATE = today


def _retry_after(e):
    """Read the real backoff seconds from an HTTP 429 response, by priority:
      1. the `Retry-After` response header (HTTP standard);
      2. the `duration` / `retryAfter` field in the response body JSON (some APIs like
         Semantic Scholar put the wait seconds in the 429 body instead of the header).
    Returns None if missing or invalid.
    """
    try:
        ra = e.headers.get("Retry-After")
        if ra:
            return float(ra)
    except Exception:
        pass
    # Many APIs (e.g. Semantic Scholar) place the wait seconds in the 429 body JSON's duration field
    try:
        if getattr(e, "code", None) == 429:
            body = e.read()
            d = json.loads(body.decode("utf-8", "replace"))
            if isinstance(d, dict):
                for k in ("duration", "retryAfter", "retry_after"):
                    v = d.get(k)
                    if v:
                        return float(v)
    except Exception:
        pass
    return None


def _short(url, n=72):
    return url if len(url) <= n else url[:n] + "..."
