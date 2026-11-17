#!/usr/bin/env python3
"""domain-recon — passive domain / infrastructure OSINT over keyless HTTP APIs.

Zero third-party runtime dependencies (Python 3.8+ standard library only).

Sources wrapped:
  certs    crt.sh + certspotter  Certificate Transparency -> subdomains + cert history
  rdap     IANA bootstrap/rdap.org  Modern WHOIS for domain / IP / ASN (JSON)
  dns      Google / Cloudflare   DNS-over-HTTPS record lookups
  ip       ip-api.com            IP -> geo / ISP / ASN / hosting+proxy flags
  asn      RIPEstat Data API     ASN / prefix / IP ownership (BGPView replacement)
  wayback  archive.org           Wayback Machine availability + CDX capture history
  profile  (orchestrator)        Chains the above into one structured domain report

Everything here is passive: it only queries public third-party databases. It never
touches the target host directly. All network input is passed as URL-encoded query
parameters or path segments -- no shell is ever invoked, so there is no command
injection surface.
"""
from __future__ import annotations

import argparse
import errno
import ipaddress
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

__version__ = "0.6.0"

USER_AGENT = "domain-recon/{v} (+https://github.com/maggiedev-bot/domain-recon)".format(v=__version__)

# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class ReconError(Exception):
    """Base error for all recon failures (surfaced to the CLI as a clean message)."""


class RateLimitError(ReconError):
    """Upstream returned HTTP 429 and retries were exhausted."""


class HTTPStatusError(ReconError):
    def __init__(self, status: int, url: str, body: str = ""):
        self.status = status
        self.url = url
        self.body = body
        super().__init__("HTTP {s} from {u}".format(s=status, u=url))


class NetworkError(ReconError):
    """DNS failure, connection refused, timeout, etc.

    Carries the originating exception on `.cause` (when known) so callers can
    tell a narrow, retryable transport failure (connection reset / TLS RST /
    read timeout) apart from a hard failure (DNS resolution, refused).
    """

    def __init__(self, message: str, cause: "BaseException | None" = None):
        super().__init__(message)
        self.cause = cause


class RdapUnreachable(NetworkError):
    """A bootstrap/supplement-listed authoritative RDAP endpoint was reachable
    in principle but the connection was reset / TLS handshake RST / read timed
    out from our egress.

    This is a *distinct, retryable* condition — the RDAP server demonstrably
    exists (it is delegated in the IANA RDAP bootstrap or the curated
    supplement), so it must never be misfiled as 'unsupported' (no server) nor
    as an opaque error. Subclasses NetworkError so existing
    `except NetworkError` / `except ReconError` handlers still catch it, while
    `fetch_rdap` intercepts it to emit a first-class `rdap_source == "unreachable"`
    result.
    """

    def __init__(self, endpoint: str, origin: str, detail: str, cause=None):
        self.endpoint = endpoint
        self.origin = origin
        self.detail = detail
        super().__init__(
            "RDAP endpoint {e} ({o}) unreachable: {d}".format(e=endpoint, o=origin, d=detail),
            cause=cause,
        )


class RdapBroken(ReconError):
    """A bootstrap/supplement-listed authoritative RDAP endpoint *responded*, but
    with an unusable response — an untrusted / self-signed TLS certificate, or an
    HTTP error status (4xx / 5xx).

    This is a *fourth* first-class outcome, distinct from all three neighbours:
      * NOT 'unsupported' (`rdap_source == "none"`): a server demonstrably EXISTS
        (the TLD is delegated in the IANA bootstrap or the curated supplement) —
        it is just serving garbage / erroring, not absent.
      * NOT 'unreachable' (`rdap_source == "unreachable"`): there we got no HTTP
        response at all (connection reset / TLS-RST / read timeout at the
        transport layer). Here the endpoint answered — we just can't use it.
      * NOT an opaque crash: it is classified and labelled honestly.

    Retryability differs by cause and is carried on `.retryable`: a bad TLS cert
    or a 4xx is a persistent registry-side fault (retry won't help →
    `retryable=False`); a 5xx is a server-side error class that per HTTP
    semantics warrants a later retry (`retryable=True`). `fetch_rdap` intercepts
    it to emit a first-class `rdap_source == "broken"` result; the exit code is
    driven by `.retryable` (retryable → 3, non-retryable → 4) so a shell caller
    can branch "retry later" from "don't bother".
    """

    def __init__(self, endpoint: str, origin: str, cause: str, retryable: bool,
                 http_status: "int | None" = None, detail: str = ""):
        self.endpoint = endpoint
        self.origin = origin
        self.cause = cause            # short slug: 'bad-cert' | 'http-<status>'
        self.retryable = retryable
        self.http_status = http_status
        self.detail = detail
        super().__init__(
            "RDAP endpoint {e} ({o}) broken ({c}): {d}".format(
                e=endpoint, o=origin, c=cause, d=detail or cause
            )
        )


def _is_unreachable_signal(err: "BaseException") -> bool:
    """True iff `err` is the narrow, retryable 'endpoint reset the connection /
    TLS handshake RST / read timed out' condition.

    Deliberately narrow so it never swallows a genuine ban or a real absence:
      * excludes RateLimitError (429/ban) and HTTPStatusError (any HTTP status),
      * excludes DNS-resolution failure (socket.gaierror) and connection-refused
        (ECONNREFUSED),
      * matches only connection-reset (ECONNRESET / errno 104), read timeouts
        (socket.timeout / TimeoutError), and TLS handshake resets / unexpected
        EOF (ssl.SSLError signalling a reset).
    """
    if isinstance(err, (RateLimitError, HTTPStatusError)):
        return False
    # Unwrap: NetworkError carries the raw cause; urllib.error.URLError nests
    # the transport error under `.reason`.
    inner = getattr(err, "cause", None) or err
    inner = getattr(inner, "reason", inner)
    if isinstance(inner, (socket.timeout, TimeoutError)):
        return True
    if isinstance(inner, ConnectionResetError):
        return True
    # gaierror (DNS) and ConnectionRefusedError are OSErrors too — gate on errno.
    if isinstance(inner, ssl.SSLError):
        s = str(inner).lower()
        if any(k in s for k in ("reset", "unexpected eof", "eof occurred", "handshake")):
            return True
        return False
    if isinstance(inner, OSError) and getattr(inner, "errno", None) == errno.ECONNRESET:
        return True
    # Last-resort string sniff for transports that surface the reset/timeout
    # opaquely (e.g. wrapped in a bare URLError string).
    s = str(err).lower()
    return any(
        k in s
        for k in ("reset by peer", "econnreset", "errno 104", "read timed out", "timed out reading")
    )


def _endpoint_fault(err: "BaseException") -> "tuple[str, bool, int | None] | None":
    """Classify a *definitive endpoint fault* on a delegated RDAP server — the
    endpoint responded, but with something we cannot use.

    Returns `(cause_slug, retryable, http_status)` or `None` when `err` is not a
    definitive endpoint fault (so the caller keeps its existing behaviour —
    e.g. fall through to the rdap.org redirector).

    Deliberately narrow and mutually-exclusive with `_is_unreachable_signal`
    (which the caller checks *first*, so any transport reset / TLS-RST / read
    timeout is already claimed by 'unreachable' before we get here):
      * bad TLS certificate  → ('bad-cert', False, None) — untrusted / self-signed
        chain; a persistent registry-side fault, retry cannot help.
      * HTTP 4xx (≠429)      → ('http-<st>', False, st) — the endpoint answered
        definitively (426 upgrade-required, 404 apex, …); not retryable.
      * HTTP 5xx             → ('http-<st>', True,  st) — server-side error class;
        per HTTP semantics a later retry may succeed → retryable.

    A 429/ban (`RateLimitError`), a DNS-resolution failure, a connection-refused,
    and a genuine 'no server' absence can NEVER be misfiled here — the first two
    are excluded explicitly, the last never reaches this path (it is decided by
    bootstrap membership upstream, not by an exception).
    """
    # A 429/ban is never a 'broken endpoint' — it is a rate-limit to honour.
    if isinstance(err, RateLimitError):
        return None
    if isinstance(err, HTTPStatusError):
        st = err.status
        if st == 429:                       # defensive: real 429s are RateLimitError
            return None
        if 500 <= st < 600:
            return ("http-{}".format(st), True, st)      # server error: retryable
        if 400 <= st < 500:
            return ("http-{}".format(st), False, st)     # client/definitive: not retryable
        return None
    # Transport layer: only an untrusted/self-signed *certificate verification*
    # failure is a 'broken' endpoint. A reset / TLS-RST / timeout is 'unreachable'
    # and was already claimed by _is_unreachable_signal upstream. SSLCertVerificationError
    # is a distinct subclass of ssl.SSLError, so this never catches a plain reset.
    inner = getattr(err, "cause", None) or err
    inner = getattr(inner, "reason", inner)
    if isinstance(inner, ssl.SSLCertVerificationError):
        return ("bad-cert", False, None)
    return None


class ParseError(ReconError):
    """Upstream returned a body we could not parse as the expected JSON."""


class InputError(ReconError):
    """Caller supplied an invalid domain / IP / ASN."""


# ---------------------------------------------------------------------------
# HTTP layer (single seam for tests: patch `_open` or `http_get_json`)
# ---------------------------------------------------------------------------

# Indirection so tests can stub the actual network call and the sleep between
# retries without monkeypatching urllib/time globally.
_sleep = time.sleep


def _open(req: "urllib.request.Request", timeout: float):
    """Thin wrapper around urlopen. Patch this in tests to simulate the network."""
    return urllib.request.urlopen(req, timeout=timeout)


def http_get(
    url: str,
    headers: "dict[str, str] | None" = None,
    timeout: float = 15.0,
    retries: int = 3,
    backoff: float = 0.5,
    max_backoff: float = 8.0,
) -> str:
    """GET a URL and return the decoded text body.

    Retries on 429 and 5xx with exponential backoff, honoring an integer
    Retry-After header when present. Raises a ReconError subclass on failure.
    """
    hdrs = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs, method="GET")

    attempt = 0
    while True:
        attempt += 1
        try:
            resp = _open(req, timeout)
            raw = resp.read()
            charset = "utf-8"
            # Best-effort charset sniff from Content-Type.
            ctype = ""
            try:
                ctype = resp.headers.get("Content-Type", "") or ""
            except Exception:
                ctype = ""
            m = re.search(r"charset=([\w-]+)", ctype)
            if m:
                charset = m.group(1)
            return raw.decode(charset, errors="replace")
        except urllib.error.HTTPError as e:
            status = e.code
            if status == 429 or 500 <= status < 600:
                if attempt > retries:
                    if status == 429:
                        raise RateLimitError(
                            "rate limited by {u} after {n} attempts".format(u=url, n=attempt)
                        )
                    raise HTTPStatusError(status, url)
                _sleep(_retry_delay(e, attempt, backoff, max_backoff))
                continue
            # Non-retryable client errors (404, 400, ...): read body for context.
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                body = ""
            raise HTTPStatusError(status, url, body)
        except (urllib.error.URLError, socket.timeout, TimeoutError) as e:
            # DNS failure, connection refused, timeout.
            if attempt > retries:
                raise NetworkError("network error for {u}: {e}".format(u=url, e=e), cause=e)
            _sleep(min(max_backoff, backoff * (2 ** (attempt - 1))))
            continue


def _retry_delay(err, attempt, backoff, max_backoff):
    """Compute the backoff delay, preferring an integer Retry-After header."""
    try:
        ra = err.headers.get("Retry-After")
        if ra is not None and str(ra).strip().isdigit():
            return min(max_backoff, float(int(ra)))
    except Exception:
        pass
    return min(max_backoff, backoff * (2 ** (attempt - 1)))


def http_get_json(url: str, headers=None, timeout: float = 15.0, retries: int = 3):
    """GET and parse JSON. Raises ParseError if the body is not valid JSON."""
    text = http_get(url, headers=headers, timeout=timeout, retries=retries)
    if text is None or text.strip() == "":
        raise ParseError("empty response body from {u}".format(u=url))
    try:
        return json.loads(text)
    except (ValueError, json.JSONDecodeError) as e:
        snippet = text[:120].replace("\n", " ")
        raise ParseError("invalid JSON from {u}: {e} :: {s!r}".format(u=url, e=e, s=snippet))


# ---------------------------------------------------------------------------
# Input validation / normalization  (no shell, ever)
# ---------------------------------------------------------------------------

_LABEL_RE = re.compile(r"^(?!-)[A-Za-z0-9_-]{1,63}(?<!-)$")


def normalize_domain(value: str) -> str:
    """Validate and IDNA/punycode-encode a domain name to its ASCII form.

    Accepts unicode (IDN) input like 'bücher.example' and returns
    'xn--bcher-kva.example'. Raises InputError on anything that is not a
    plausible hostname. Never shells out.
    """
    if not value or not isinstance(value, str):
        raise InputError("empty domain")
    d = value.strip().strip(".").lower()
    if not d:
        raise InputError("empty domain")
    if "/" in d or " " in d or ".." in d:
        raise InputError("invalid domain: {!r}".format(value))
    labels = d.split(".")
    if len(labels) < 2:
        raise InputError("not a fully-qualified domain: {!r}".format(value))
    out = []
    for label in labels:
        if not label:
            raise InputError("empty label in domain: {!r}".format(value))
        try:
            enc = label.encode("idna").decode("ascii") if _needs_idna(label) else label
        except UnicodeError as e:
            raise InputError("invalid IDN label {!r}: {}".format(label, e))
        if not _LABEL_RE.match(enc):
            raise InputError("invalid domain label: {!r}".format(label))
        out.append(enc)
    return ".".join(out)


def _needs_idna(label: str) -> bool:
    return any(ord(ch) > 127 for ch in label)


def normalize_ip(value: str) -> str:
    """Validate an IPv4 or IPv6 address and return its canonical string form."""
    if not value or not isinstance(value, str):
        raise InputError("empty IP address")
    try:
        return str(ipaddress.ip_address(value.strip()))
    except ValueError:
        raise InputError("invalid IP address: {!r}".format(value))


def normalize_asn(value: str) -> int:
    """Accept 'AS15169', 'as15169' or '15169' and return the integer 15169."""
    if value is None:
        raise InputError("empty ASN")
    s = str(value).strip().upper()
    if s.startswith("AS"):
        s = s[2:]
    if not s.isdigit():
        raise InputError("invalid ASN: {!r}".format(value))
    n = int(s)
    if not (0 <= n <= 4294967295):
        raise InputError("ASN out of range: {!r}".format(value))
    return n


def classify_resource(value: str) -> str:
    """Return 'ip', 'asn', or 'domain' for a free-form resource string."""
    s = (value or "").strip()
    try:
        ipaddress.ip_address(s)
        return "ip"
    except ValueError:
        pass
    if re.fullmatch(r"(?i:as)?\d+", s):
        return "asn"
    return "domain"


# ---------------------------------------------------------------------------
# Source: crt.sh  (Certificate Transparency)
# ---------------------------------------------------------------------------


def parse_certs(entries, domain: str, include_wildcards: bool = True, limit: "int | None" = None,
                max_certs: "int | None" = None) -> dict:
    """Normalize a crt.sh JSON array into subdomains + cert history.

    Pure function: takes the already-decoded list, returns a normalized dict.
    Handles the newline-delimited `name_value` field, wildcard entries, and
    de-duplicates the subdomain set deterministically (sorted).

    `limit` caps the returned subdomain list (crt.sh returns huge payloads for
    popular domains); the full unique count is always reported in
    `subdomain_count` and `subdomains_truncated` flags whether capping occurred.
    `max_certs` similarly caps the returned cert-history rows.
    """
    if entries is None:
        entries = []
    if not isinstance(entries, list):
        raise ParseError("crt.sh: expected a JSON array, got {}".format(type(entries).__name__))

    suffix = "." + domain
    names = set()
    certs = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        raw_names = []
        nv = e.get("name_value") or ""
        raw_names.extend(nv.split("\n"))
        cn = e.get("common_name")
        if cn:
            raw_names.append(cn)
        for n in raw_names:
            n = (n or "").strip().lower().rstrip(".")
            if not n:
                continue
            is_wild = n.startswith("*.")
            if is_wild and not include_wildcards:
                continue
            bare = n[2:] if is_wild else n
            # Keep only names within the queried apex.
            if bare == domain or bare.endswith(suffix):
                names.add(n)
        certs.append(
            {
                "id": e.get("id"),
                "issuer": e.get("issuer_name"),
                "common_name": e.get("common_name"),
                "not_before": e.get("not_before"),
                "not_after": e.get("not_after"),
                "serial_number": e.get("serial_number"),
                "entry_timestamp": e.get("entry_timestamp"),
            }
        )

    all_subdomains = sorted(names)
    subdomains = all_subdomains[:limit] if limit is not None else all_subdomains
    cert_total = len(certs)
    shown_certs = certs[:max_certs] if max_certs is not None else certs
    return {
        "source": "crt.sh",
        "target": domain,
        "domain": domain,
        "subdomain_count": len(all_subdomains),
        "subdomains_truncated": len(subdomains) < len(all_subdomains),
        "subdomains": subdomains,
        "cert_count": cert_total,
        "certs_truncated": len(shown_certs) < cert_total,
        "certs": shown_certs,
    }


def parse_certspotter(entries, domain: str, include_wildcards: bool = True, limit: "int | None" = None,
                      max_certs: "int | None" = None) -> dict:
    """Normalize a certSpotter `/v1/issuances` JSON array into subdomains + certs.

    certSpotter is the secondary Certificate Transparency source (used when
    crt.sh is unreachable). Its schema differs from crt.sh: names live in a
    `dns_names` list per issuance, and the issuer is a nested object. This maps
    it onto the SAME normalized contract as `parse_certs` so the two can merge.
    """
    if entries is None:
        entries = []
    # certSpotter returns an error object (not an array) on rejection.
    if isinstance(entries, dict):
        msg = entries.get("message") or entries.get("code") or "unexpected object response"
        raise ParseError("certspotter: {}".format(msg))
    if not isinstance(entries, list):
        raise ParseError("certspotter: expected a JSON array, got {}".format(type(entries).__name__))

    suffix = "." + domain
    names = set()
    certs = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        for n in (e.get("dns_names") or []):
            n = (n or "").strip().lower().rstrip(".")
            if not n:
                continue
            is_wild = n.startswith("*.")
            if is_wild and not include_wildcards:
                continue
            bare = n[2:] if is_wild else n
            if bare == domain or bare.endswith(suffix):
                names.add(n)
        issuer = e.get("issuer")
        issuer_name = issuer.get("name") if isinstance(issuer, dict) else issuer
        certs.append(
            {
                "id": e.get("id"),
                "issuer": issuer_name,
                "common_name": None,  # certSpotter does not expose a distinct CN
                "not_before": e.get("not_before"),
                "not_after": e.get("not_after"),
                "serial_number": None,
                "entry_timestamp": None,
            }
        )

    all_subdomains = sorted(names)
    subdomains = all_subdomains[:limit] if limit is not None else all_subdomains
    cert_total = len(certs)
    shown_certs = certs[:max_certs] if max_certs is not None else certs
    return {
        "source": "certspotter",
        "target": domain,
        "domain": domain,
        "subdomain_count": len(all_subdomains),
        "subdomains_truncated": len(subdomains) < len(all_subdomains),
        "subdomains": subdomains,
        "cert_count": cert_total,
        "certs_truncated": len(shown_certs) < cert_total,
        "certs": shown_certs,
    }


# Certificate Transparency sources tried in order (crt.sh primary, certSpotter
# fallback). Both are keyless/passive.
CT_SOURCES = ("crtsh", "certspotter")


def _fetch_crtsh_raw(domain: str, timeout: float, retries: int):
    """GET crt.sh and return the decoded JSON array. Empty body -> [] (no certs)."""
    q = urllib.parse.quote("%." + domain, safe="")
    url = "https://crt.sh/?q={q}&output=json".format(q=q)
    text = http_get(url, timeout=timeout, retries=retries)
    if text.strip() == "":
        return []
    try:
        return json.loads(text)
    except (ValueError, json.JSONDecodeError) as e:
        raise ParseError("crt.sh returned non-JSON: {e}".format(e=e))


def _fetch_certspotter_raw(domain: str, timeout: float, retries: int):
    """GET certSpotter issuances and return the decoded JSON array."""
    q = urllib.parse.quote(domain, safe="")
    url = (
        "https://api.certspotter.com/v1/issuances?domain={q}"
        "&include_subdomains=true&expand=dns_names&expand=issuer".format(q=q)
    )
    text = http_get(url, timeout=timeout, retries=retries)
    if text.strip() == "":
        return []
    try:
        return json.loads(text)
    except (ValueError, json.JSONDecodeError) as e:
        raise ParseError("certspotter returned non-JSON: {e}".format(e=e))


def _ct_source_names_certs(source: str, domain: str, include_wildcards: bool, timeout: float, retries: int):
    """Query one CT source and return (names:set, certs:list). Raises on failure.

    A successful HTTP 200 with an empty result set is a valid answer (the domain
    simply has no logged certificates) — it does NOT raise, which is how the
    caller distinguishes "no certs logged" from "source is down".
    """
    if source == "crtsh":
        norm = parse_certs(_fetch_crtsh_raw(domain, timeout, retries), domain, include_wildcards=include_wildcards)
    elif source == "certspotter":
        norm = parse_certspotter(_fetch_certspotter_raw(domain, timeout, retries), domain, include_wildcards=include_wildcards)
    else:
        raise InputError("unknown CT source: {!r}".format(source))
    return set(norm["subdomains"]), norm["certs"]


def fetch_certs(domain: str, include_wildcards=True, limit=None, max_certs=None, timeout=20.0, retries=3,
                sources=None, merge_all=False) -> dict:
    """Enumerate subdomains via Certificate Transparency with source fallback.

    Tries crt.sh first; if it is unreachable (5xx / 4xx / timeout / bad JSON)
    the query falls back to certSpotter so subdomain enumeration survives a
    crt.sh outage. Names from every source that answered are merged and
    de-duplicated. `sources_used` records which source(s) actually answered and
    `errors` records any that failed, so a result is always auditable.

    Default behavior stops at the first source that answers (courtesy: don't
    hammer the fallback when the primary is healthy). Pass ``merge_all=True`` to
    query every source and union the results for wider coverage.

    Raises a ReconError only when *no* source could be reached.
    """
    d = normalize_domain(domain)
    order = tuple(sources) if sources else CT_SOURCES
    names = set()
    certs = []
    used = []
    errors = []
    for src in order:
        try:
            s_names, s_certs = _ct_source_names_certs(src, d, include_wildcards, timeout, retries)
        except ReconError as e:
            errors.append({"source": src, "error": str(e)})
            continue
        used.append(src)
        names.update(s_names)
        certs.extend(s_certs)
        if not merge_all:
            break

    if not used:
        detail = "; ".join("{}: {}".format(e["source"], e["error"]) for e in errors) or "no CT sources configured"
        raise ReconError("all CT sources failed ({})".format(detail))

    all_subdomains = sorted(names)
    subdomains = all_subdomains[:limit] if limit is not None else all_subdomains
    cert_total = len(certs)
    shown_certs = certs[:max_certs] if max_certs is not None else certs
    return {
        "source": "ct",
        "target": d,
        "domain": d,
        "sources_used": used,
        "errors": errors,
        "subdomain_count": len(all_subdomains),
        "subdomains_truncated": len(subdomains) < len(all_subdomains),
        "subdomains": subdomains,
        "cert_count": cert_total,
        "certs_truncated": len(shown_certs) < cert_total,
        "certs": shown_certs,
    }


# ---------------------------------------------------------------------------
# Source: rdap.org  (RDAP / modern WHOIS)
# ---------------------------------------------------------------------------


def _rdap_events(obj) -> dict:
    out = {}
    for ev in (obj.get("events") or []):
        action = ev.get("eventAction")
        if action:
            out[action] = ev.get("eventDate")
    return out


def _rdap_entities(obj) -> list:
    ents = []
    for ent in (obj.get("entities") or []):
        ents.append({"handle": ent.get("handle"), "roles": ent.get("roles")})
    return ents


def parse_rdap(obj, kind: str) -> dict:
    """Normalize an RDAP object (domain / ip / autnum) into a compact dict."""
    if not isinstance(obj, dict):
        raise ParseError("rdap: expected a JSON object")
    base = {
        "source": "rdap",
        "kind": kind,
        "handle": obj.get("handle"),
        "status": obj.get("status") or [],
        "events": _rdap_events(obj),
        "entities": _rdap_entities(obj),
    }
    if kind == "domain":
        base["ldhName"] = obj.get("ldhName")
        base["nameservers"] = sorted(
            (ns.get("ldhName") or "").lower() for ns in (obj.get("nameservers") or []) if ns.get("ldhName")
        )
        secure = obj.get("secureDNS") or {}
        base["dnssec"] = bool(secure.get("delegationSigned"))
    elif kind == "ip":
        base["name"] = obj.get("name")
        base["startAddress"] = obj.get("startAddress")
        base["endAddress"] = obj.get("endAddress")
        base["ipVersion"] = obj.get("ipVersion")
        base["country"] = obj.get("country")
        base["type"] = obj.get("type")
    elif kind == "asn":
        base["name"] = obj.get("name")
        base["startAutnum"] = obj.get("startAutnum")
        base["endAutnum"] = obj.get("endAutnum")
    return base


# IANA RDAP bootstrap: maps a TLD -> the authoritative RDAP base URL. rdap.org
# is only a redirector and its coverage is incomplete (e.g. it 404s `.io` and
# other ccTLDs/newer TLDs), so we resolve the authoritative server ourselves and
# fall back to rdap.org only when the TLD is absent from the registry.
_RDAP_BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"

# RFC 7480 §4.2: RDAP servers serve the `application/rdap+json` media type. Some
# strict registry servers (e.g. rdap.nic.cat / .aco / .barcelona) reject a plain
# `application/json` Accept with HTTP 406, so RDAP requests must ask for the RDAP
# type first (json kept as a lenient fallback for servers that only speak it).
_RDAP_ACCEPT = "application/rdap+json, application/json"

# Process-lifetime memo of the parsed {tld: base_url} map (fetched at most once
# per run). Reset between tests via recon._RDAP_BOOTSTRAP_CACHE.clear().
_RDAP_BOOTSTRAP_CACHE: "dict[str, dict]" = {}

# Curated supplement: TLDs that IANA *omits* from its RDAP bootstrap yet that run
# a public RDAP server anyway. rdap.org 404s these, so without this map they are
# unresolvable. This is what actually fixes `.io` (the reported case): `.io` is
# NOT in data.iana.org/rdap/dns.json, but Identity Digital serves its RDAP.
# Each base verified live (HTTP 200 for a real domain) on 2026-07-26; keep the
# list short + verified. Bootstrap always wins when it covers the TLD.
_RDAP_SUPPLEMENT = {
    "io": "https://rdap.identitydigital.services/rdap",
    "sh": "https://rdap.identitydigital.services/rdap",
    "ac": "https://rdap.identitydigital.services/rdap",
    "us": "https://rdap.nic.us",
    # DENIC runs a public RDAP server for .de but does not publish it to IANA's
    # bootstrap, so rdap.org 404s .de. Verified HTTP 200 with real registration
    # data (status/nameservers/events) for google.de on 2026-07-26.
    "de": "https://rdap.denic.de",
    # ccTLD registries that run a public RDAP server absent from IANA's bootstrap.
    # Each verified live on 2026-07-27 with a two-part check: HTTP 200 + real RDAP
    # data for the registry's own domain, AND a clean 404 (not a connection error)
    # for a bogus name in the same TLD — i.e. a genuine general-purpose server, not
    # a one-off. Bootstrap always wins when it later covers any of these, so only
    # TLDs *genuinely omitted* from the bootstrap are listed here (e.g. .ch/.nl/.no
    # are already in the bootstrap and are intentionally NOT duplicated).
    "ch": "https://rdap.nic.ch",  # SWITCH (Switzerland)
    "af": "https://rdap.nic.af",
    "aw": "https://rdap.nic.aw",
    "ci": "https://rdap.nic.ci",
    "ga": "https://rdap.nic.ga",
    "kn": "https://rdap.nic.kn",
    "kz": "https://rdap.nic.kz",
    "mr": "https://rdap.nic.mr",
    "mz": "https://rdap.nic.mz",
    "sb": "https://rdap.nic.sb",
    "so": "https://rdap.nic.so",
    "td": "https://rdap.nic.td",
    "tl": "https://rdap.nic.tl",
}


def parse_rdap_bootstrap(obj) -> dict:
    """Parse IANA `dns.json` into a {tld: authoritative_base_url} mapping.

    Each service entry is `[[tlds...], [urls...]]`; we prefer an https base and
    strip the trailing slash for clean joining.
    """
    if not isinstance(obj, dict) or "services" not in obj:
        raise ParseError("rdap bootstrap: missing 'services'")
    mapping = {}
    for svc in obj.get("services") or []:
        if not isinstance(svc, list) or len(svc) < 2:
            continue
        tlds, urls = svc[0], svc[1]
        base = None
        for u in urls or []:
            if isinstance(u, str) and u.startswith("https"):
                base = u
                break
        if base is None:
            for u in urls or []:
                if isinstance(u, str) and u:
                    base = u
                    break
        if not base:
            continue
        for t in tlds or []:
            key = str(t).strip(".").lower()
            if key:
                mapping[key] = base.rstrip("/")
    return mapping


def _load_rdap_bootstrap(timeout: float, retries: int) -> dict:
    """Fetch + parse the IANA bootstrap once, memoized for the process."""
    cached = _RDAP_BOOTSTRAP_CACHE.get("dns")
    if cached is not None:
        return cached
    mapping = parse_rdap_bootstrap(http_get_json(_RDAP_BOOTSTRAP_URL, headers={"Accept": _RDAP_ACCEPT}, timeout=timeout, retries=retries))
    _RDAP_BOOTSTRAP_CACHE["dns"] = mapping
    return mapping


def _rdap_base_for_domain(domain: str, timeout: float, retries: int):
    """Resolve the authoritative RDAP domain URL for `domain`.

    Returns (url, origin, bootstrap_ok):
      * url    — the authoritative RDAP domain URL, or None if the TLD is in
                 neither the IANA bootstrap nor the curated supplement.
      * origin — 'iana-bootstrap' or 'supplement', or None when url is None.
      * bootstrap_ok — True if the IANA bootstrap was successfully consulted
                 (so *absence* of the TLD from it is authoritative — the basis
                 for the "unsupported" signal), False if the bootstrap itself
                 was unreachable (absence is then inconclusive → fall through
                 to rdap.org rather than claiming the TLD is unsupported).

    The bootstrap is consulted first; the supplement fills only the gaps IANA
    leaves (e.g. `.io`), and still applies if the bootstrap itself is unreachable.
    """
    tld = domain.rsplit(".", 1)[-1]
    base, origin = None, None
    bootstrap_ok = False
    try:
        mapping = _load_rdap_bootstrap(timeout, retries)
        bootstrap_ok = True
        if tld in mapping:
            base, origin = mapping[tld], "iana-bootstrap"
    except ReconError:
        pass  # bootstrap unavailable -> supplement / rdap.org still available
    if base is None and tld in _RDAP_SUPPLEMENT:
        base, origin = _RDAP_SUPPLEMENT[tld], "supplement"
    if base is None:
        return None, None, bootstrap_ok
    return "{b}/domain/{d}".format(b=base.rstrip("/"), d=urllib.parse.quote(domain, safe="")), origin, bootstrap_ok


def _fetch_rdap_domain(domain: str, timeout: float, retries: int, use_bootstrap: bool = True):
    """Fetch a domain RDAP object, preferring the authoritative server.

    Returns (obj, rdap_source). Tries the bootstrap/supplement-resolved
    authoritative server first; on any failure falls back to the rdap.org
    redirector. When the IANA bootstrap was consulted successfully but the TLD
    is absent from it *and* the curated supplement, no public RDAP server
    exists for that TLD — rdap.org (a bootstrap-backed redirector) would only
    404 — so we return (None, "none") to signal a first-class "unsupported"
    result rather than a spurious error. (With bootstrap disabled or the
    bootstrap unreachable, we cannot make that determination, so we still fall
    back to rdap.org.)
    """
    auth_base = None
    auth_origin = None
    auth_fault = None  # a definitive endpoint fault seen on the authoritative server
    if use_bootstrap:
        base, origin, bootstrap_ok = _rdap_base_for_domain(domain, timeout, retries)
        if base:
            auth_base, auth_origin = base, origin
            try:
                return http_get_json(base, headers={"Accept": _RDAP_ACCEPT}, timeout=timeout, retries=retries), origin
            except ReconError as e:
                # The authoritative endpoint is delegated (bootstrap/supplement).
                #   (1) transport reset / TLS-RST / read timeout -> 'unreachable'
                #       (retryable — we got no HTTP response). rdap.org only
                #       *redirects* the client back to this same backend, so a
                #       reset would just recur; short-circuit as unreachable.
                if _is_unreachable_signal(e):
                    raise RdapUnreachable(endpoint=base, origin=origin or "iana-bootstrap", detail=str(e), cause=e) from e
                #   (2) endpoint *responded* unusably (bad TLS cert / HTTP 4xx /
                #       5xx). Remember it, but still try the rdap.org redirector —
                #       it may resolve to a different server that answers (e.g.
                #       .io). Only if the redirector ALSO fails do we surface the
                #       authoritative fault as the first-class 'broken' state, so
                #       'broken' means "both the authoritative server and the
                #       redirector were exhausted", not one transient 404.
                auth_fault = _endpoint_fault(e)
                pass  # fall through to the redirector
        elif bootstrap_ok:
            # TLD authoritatively absent from bootstrap + supplement: no coverage.
            return None, "none"
    url = "https://rdap.org/domain/{}".format(urllib.parse.quote(domain, safe=""))
    try:
        return http_get_json(url, headers={"Accept": _RDAP_ACCEPT}, timeout=timeout, retries=retries), "rdap.org"
    except ReconError as e2:
        # The redirector failed too. If the authoritative server had a definitive
        # endpoint fault, surface THAT (the real registry cause) as 'broken'
        # rather than the opaque redirector error; otherwise propagate as before.
        if auth_fault is not None:
            cause, retryable, status = auth_fault
            raise RdapBroken(
                endpoint=auth_base, origin=auth_origin or "iana-bootstrap",
                cause=cause, retryable=retryable, http_status=status, detail=str(e2),
            ) from e2
        raise


def _rdap_unsupported(resource: str, kind: str, domain: str) -> dict:
    """Build a first-class 'RDAP not supported for this TLD' result.

    This is a *capability gap*, not a failure: the registry runs no public RDAP
    server, so there is nothing to retry. A caller (agent) should read
    `supported is False` / `rdap_source == "none"` and simply skip the field.
    """
    tld = domain.rsplit(".", 1)[-1]
    return {
        "source": "rdap",
        "kind": kind,
        "target": resource,
        "supported": False,
        "rdap_source": "none",
        "tld": tld,
        "reason": (
            "no public RDAP server for .{tld} (absent from the IANA RDAP "
            "bootstrap and the curated supplement; the registry is likely "
            "WHOIS-only)".format(tld=tld)
        ),
    }


def _rdap_unreachable(resource: str, kind: str, domain: str, err: "RdapUnreachable") -> dict:
    """Build a first-class 'RDAP endpoint unreachable (retryable)' result.

    Distinct from `_rdap_unsupported`: here a public RDAP server *does* exist
    (the TLD is delegated in the IANA bootstrap or the curated supplement) — we
    simply could not reach it from our egress this time (connection reset / TLS
    handshake RST / read timeout). The signal to a consuming agent: the data
    exists, we could not fetch it, skip the field but know it is **retryable** —
    NOT "this TLD has no RDAP server".
    """
    tld = domain.rsplit(".", 1)[-1]
    origin = getattr(err, "origin", None) or "iana-bootstrap"
    return {
        "source": "rdap",
        "kind": kind,
        "target": resource,
        "supported": True,
        "rdap_source": "unreachable",
        "tld": tld,
        "endpoint": getattr(err, "endpoint", None),
        "origin": origin,
        "retryable": True,
        "reason": (
            "registry RDAP endpoint for .{tld} was unreachable from our egress — "
            "the connection was reset / TLS handshake RST / read timed out "
            "(errno 104 / connection reset class). The endpoint is delegated via "
            "the IANA RDAP {origin}, so this is reachable-but-unreachable and "
            "retryable, NOT 'unsupported'. detail: {detail}".format(
                tld=tld, origin=origin, detail=getattr(err, "detail", None) or str(err)
            )
        ),
    }


def _rdap_broken(resource: str, kind: str, domain: str, err: "RdapBroken") -> dict:
    """Build a first-class 'RDAP endpoint broken' result.

    Distinct from `_rdap_unsupported` (no server exists) and `_rdap_unreachable`
    (transport reset/timeout — no HTTP response): here a public RDAP server
    *does* exist and *did* respond, but with an untrusted/self-signed TLS cert
    or an HTTP error status. The signal to a consuming agent: the endpoint is
    faulty — skip the field; `retryable` says whether trying later can help (a
    5xx may recover; a bad cert / 4xx will not until the registry fixes it).
    """
    tld = domain.rsplit(".", 1)[-1]
    origin = getattr(err, "origin", None) or "iana-bootstrap"
    cause = getattr(err, "cause", None) or "endpoint-error"
    retryable = bool(getattr(err, "retryable", False))
    status = getattr(err, "http_status", None)
    if cause == "bad-cert":
        what = ("presented an untrusted / self-signed TLS certificate that fails "
                "verification (we do NOT disable TLS verification)")
    elif status is not None and 500 <= status < 600:
        what = "returned HTTP {} (server-side error)".format(status)
    elif status == 426:
        what = ("returned HTTP 426 Upgrade Required — it demands a protocol upgrade "
                "a standard RDAP client will not satisfy")
    elif status == 404:
        what = ("returned HTTP 404 for this apex — the delegated server does not "
                "serve an RDAP object here (registry edge), though the domain "
                "resolves in DNS")
    elif status is not None:
        what = "returned HTTP {}".format(status)
    else:
        what = "returned an unusable response"
    return {
        "source": "rdap",
        "kind": kind,
        "target": resource,
        "supported": True,
        "rdap_source": "broken",
        "tld": tld,
        "endpoint": getattr(err, "endpoint", None),
        "origin": origin,
        "cause": cause,
        "http_status": status,
        "retryable": retryable,
        "reason": (
            "registry RDAP endpoint for .{tld} is broken — it {what}. The endpoint "
            "is delegated via the IANA RDAP {origin} (a server exists and answered), "
            "so this is a genuine registry-side fault, NOT 'unsupported' (no server) "
            "and NOT 'unreachable' (transport reset). {retry}.".format(
                tld=tld, what=what, origin=origin,
                retry=("Retryable — a later attempt may succeed" if retryable
                       else "Not retryable — retrying will not help until the registry fixes it"),
            )
        ),
    }


def fetch_rdap(resource: str, kind: "str | None" = None, timeout=20.0, retries=3, use_bootstrap=True) -> dict:
    kind = kind or classify_resource(resource)
    rdap_source = None
    if kind == "domain":
        d = normalize_domain(resource)
        try:
            obj, rdap_source = _fetch_rdap_domain(d, timeout, retries, use_bootstrap=use_bootstrap)
        except RdapUnreachable as e:
            return _rdap_unreachable(resource, kind, d, e)
        except RdapBroken as e:
            return _rdap_broken(resource, kind, d, e)
        if rdap_source == "none":
            return _rdap_unsupported(resource, kind, d)
    elif kind == "ip":
        ip = normalize_ip(resource)
        url = "https://rdap.org/ip/{}".format(urllib.parse.quote(ip, safe=""))
        obj = http_get_json(url, headers={"Accept": _RDAP_ACCEPT}, timeout=timeout, retries=retries)
        rdap_source = "rdap.org"
    elif kind == "asn":
        asn = normalize_asn(resource)
        url = "https://rdap.org/autnum/{}".format(asn)
        obj = http_get_json(url, headers={"Accept": _RDAP_ACCEPT}, timeout=timeout, retries=retries)
        rdap_source = "rdap.org"
    else:
        raise InputError("unknown RDAP kind: {!r}".format(kind))
    res = parse_rdap(obj, kind)
    res["target"] = resource
    res["rdap_source"] = rdap_source
    res["supported"] = True
    return res


# ---------------------------------------------------------------------------
# Source: DNS-over-HTTPS  (Google + Cloudflare)
# ---------------------------------------------------------------------------

DOH_PROVIDERS = {
    "google": "https://dns.google/resolve",
    "cloudflare": "https://cloudflare-dns.com/dns-query",
}

SUPPORTED_DNS_TYPES = {"A", "AAAA", "MX", "TXT", "NS", "CNAME", "SOA", "CAA", "PTR"}

# Numeric DNS type -> mnemonic, for normalizing answer records.
_DNS_TYPE_NAMES = {1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX", 16: "TXT", 28: "AAAA", 257: "CAA"}

# RFC 8914 / RFC 1035 response status codes we care about surfacing.
_DNS_STATUS = {0: "NOERROR", 2: "SERVFAIL", 3: "NXDOMAIN", 5: "REFUSED"}


def parse_dns(obj, name: str, rrtype: str) -> dict:
    """Normalize a DoH JSON response into a flat, provider-independent record set."""
    if not isinstance(obj, dict):
        raise ParseError("dns: expected a JSON object")
    status = obj.get("Status")
    answers = []
    for a in (obj.get("Answer") or []):
        t = a.get("type")
        answers.append(
            {
                "name": (a.get("name") or "").rstrip("."),
                "type": _DNS_TYPE_NAMES.get(t, t),
                "ttl": a.get("TTL"),
                "data": a.get("data"),
            }
        )
    return {
        "source": "doh",
        "target": name,
        "name": name,
        "query_type": rrtype,
        "status": status,
        "status_text": _DNS_STATUS.get(status, str(status)),
        "answer_count": len(answers),
        "answers": answers,
    }


def _dns_query_name(name: str, rrtype: str) -> str:
    """Resolve the actual DNS name to query.

    For a PTR lookup (or when the target is an IP address), build the reverse
    in-addr.arpa / ip6.arpa pointer name from the address. Otherwise validate
    and IDNA-encode the hostname.
    """
    if rrtype == "PTR" or _is_ip(name):
        try:
            return ipaddress.ip_address(name.strip()).reverse_pointer
        except ValueError:
            # Not an IP after all -> treat as a literal reverse-pointer hostname.
            return normalize_domain(name)
    return normalize_domain(name)


def _is_ip(value: str) -> bool:
    try:
        ipaddress.ip_address((value or "").strip())
        return True
    except ValueError:
        return False


def fetch_dns(name: str, rrtype: str = "A", provider: str = "google", timeout=15.0, retries=3) -> dict:
    rrtype = rrtype.upper()
    # A bare IP target implies a reverse (PTR) lookup — nobody asks for the A
    # record of an IP literal.
    if _is_ip(name) and rrtype in ("A", "AAAA"):
        rrtype = "PTR"
    if rrtype not in SUPPORTED_DNS_TYPES:
        raise InputError(
            "unsupported DNS type {!r} (supported: {})".format(rrtype, ", ".join(sorted(SUPPORTED_DNS_TYPES)))
        )
    if provider not in DOH_PROVIDERS:
        raise InputError("unknown DoH provider: {!r}".format(provider))
    qname = _dns_query_name(name, rrtype)
    base = DOH_PROVIDERS[provider]
    qs = urllib.parse.urlencode({"name": qname, "type": rrtype})
    url = "{b}?{qs}".format(b=base, qs=qs)
    # Both providers accept the application/dns-json content type.
    obj = http_get_json(url, headers={"Accept": "application/dns-json"}, timeout=timeout, retries=retries)
    return parse_dns(obj, qname, rrtype)


def fetch_dns_many(name: str, rrtypes, provider="google", timeout=15.0, retries=3) -> dict:
    results = {}
    for t in rrtypes:
        results[t.upper()] = fetch_dns(name, t, provider=provider, timeout=timeout, retries=retries)
    resolved = normalize_domain(name) if not _is_ip(name) else ipaddress.ip_address(name.strip()).reverse_pointer
    return {"source": "doh", "target": name, "name": resolved, "provider": provider, "records": results}


# ---------------------------------------------------------------------------
# Source: ip-api.com  (geo / ISP)   -- respects 45 req/min
# ---------------------------------------------------------------------------


def parse_ip(obj) -> dict:
    """Normalize an ip-api.com response. Raises ReconError on API-level failure."""
    if not isinstance(obj, dict):
        raise ParseError("ip: expected a JSON object")
    if obj.get("status") == "fail":
        raise ReconError("ip-api error: {}".format(obj.get("message", "unknown")))
    return {
        "source": "ip-api.com",
        "target": obj.get("query"),
        "ip": obj.get("query"),
        "country": obj.get("country"),
        "country_code": obj.get("countryCode"),
        "region": obj.get("regionName"),
        "city": obj.get("city"),
        "lat": obj.get("lat"),
        "lon": obj.get("lon"),
        "timezone": obj.get("timezone"),
        "isp": obj.get("isp"),
        "org": obj.get("org"),
        "as": obj.get("as"),
        "reverse": obj.get("reverse"),
        "mobile": obj.get("mobile"),
        "proxy": obj.get("proxy"),
        "hosting": obj.get("hosting"),
    }


def fetch_ip(ip: str, timeout=15.0, retries=3) -> dict:
    addr = normalize_ip(ip)
    # Request the extended field set (geo + ISP + AS + proxy/hosting flags).
    fields = "status,message,country,countryCode,regionName,city,lat,lon,timezone,isp,org,as,reverse,mobile,proxy,hosting,query"
    url = "http://ip-api.com/json/{ip}?fields={f}".format(ip=urllib.parse.quote(addr, safe=""), f=fields)
    obj = http_get_json(url, timeout=timeout, retries=retries)
    return parse_ip(obj)


# ---------------------------------------------------------------------------
# Source: RIPEstat Data API  (ASN / prefix / IP ownership) -- BGPView replacement
# ---------------------------------------------------------------------------


def parse_asn_overview(obj, announced_prefixes=None) -> dict:
    """Normalize RIPEstat as-overview (+ optional announced-prefixes) output."""
    if not isinstance(obj, dict) or "data" not in obj:
        raise ParseError("ripestat: missing 'data' in as-overview response")
    data = obj["data"]
    out = {
        "source": "ripestat",
        "kind": "asn",
        "asn": data.get("resource"),
        "holder": data.get("holder"),
        "announced": data.get("announced"),
        "block": data.get("block"),
    }
    if announced_prefixes is not None:
        prefixes = [p.get("prefix") for p in (announced_prefixes.get("data", {}).get("prefixes") or [])]
        out["prefix_count"] = len(prefixes)
        out["prefixes"] = prefixes
    return out


def parse_network_info(obj) -> dict:
    """Normalize RIPEstat network-info (IP -> announcing ASN(s) + covering prefix)."""
    if not isinstance(obj, dict) or "data" not in obj:
        raise ParseError("ripestat: missing 'data' in network-info response")
    data = obj["data"]
    return {
        "source": "ripestat",
        "kind": "ip",
        "prefix": data.get("prefix"),
        "asns": data.get("asns") or [],
    }


def fetch_asn(resource: str, with_prefixes=True, timeout=20.0, retries=3) -> dict:
    """Look up an ASN or an IP against RIPEstat.

    ASN input -> as-overview (holder/announced) plus announced-prefixes.
    IP input  -> network-info (announcing ASN(s) + covering prefix).
    """
    kind = classify_resource(resource)
    if kind == "ip":
        ip = normalize_ip(resource)
        url = "https://stat.ripe.net/data/network-info/data.json?resource={}".format(
            urllib.parse.quote(ip, safe="")
        )
        res = parse_network_info(http_get_json(url, timeout=timeout, retries=retries))
        res["target"] = resource
        return res
    # Treat everything else as an ASN (validates / normalizes).
    asn = normalize_asn(resource)
    ov_url = "https://stat.ripe.net/data/as-overview/data.json?resource=AS{}".format(asn)
    overview = http_get_json(ov_url, timeout=timeout, retries=retries)
    prefixes = None
    if with_prefixes:
        pf_url = "https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{}".format(asn)
        prefixes = http_get_json(pf_url, timeout=timeout, retries=retries)
    res = parse_asn_overview(overview, announced_prefixes=prefixes)
    res["target"] = resource
    return res


# ---------------------------------------------------------------------------
# Source: archive.org Wayback  (availability fast-path + CDX capture history)
# ---------------------------------------------------------------------------

_WAYBACK_SNAP = "http://web.archive.org/web/{ts}/{orig}"


def parse_wayback(obj, url: str) -> dict:
    """Parse the fast availability endpoint (closest snapshot only)."""
    if not isinstance(obj, dict):
        raise ParseError("wayback: expected a JSON object")
    snap = (obj.get("archived_snapshots") or {}).get("closest") or {}
    return {
        "source": "wayback",
        "target": url,
        "url": url,
        "archived": bool(snap.get("available")),
        "snapshot_url": snap.get("url"),
        "timestamp": snap.get("timestamp"),
        "status": snap.get("status"),
    }


def parse_cdx(rows) -> list:
    """Normalize a CDX `output=json` array-of-arrays (first row is the header).

    Returns a list of capture dicts in the order the CDX API returned them
    (ascending timestamp). Robust to an empty body / header-only response.
    """
    if rows is None:
        return []
    if not isinstance(rows, list):
        raise ParseError("cdx: expected a JSON array, got {}".format(type(rows).__name__))
    if len(rows) <= 1:
        return []
    header = rows[0]
    idx = {name: i for i, name in enumerate(header)}
    out = []
    for row in rows[1:]:
        if not isinstance(row, list):
            continue

        def col(key):
            i = idx.get(key)
            return row[i] if i is not None and i < len(row) else None

        ts = col("timestamp")
        original = col("original")
        out.append(
            {
                "timestamp": ts,
                "original": original,
                "statuscode": col("statuscode"),
                "mimetype": col("mimetype"),
                "snapshot_url": _WAYBACK_SNAP.format(ts=ts, orig=original) if ts and original else None,
            }
        )
    return out


def _cdx_get(url: str, timeout: float, retries: int):
    """GET a CDX endpoint. An empty body means 'no captures', not an error."""
    text = http_get(url, timeout=timeout, retries=retries)
    if not text or not text.strip():
        return []
    try:
        return json.loads(text)
    except (ValueError, json.JSONDecodeError) as e:
        raise ParseError("cdx returned non-JSON: {e}".format(e=e))


def fetch_cdx(url: str, cdx_limit: int = 10, count: bool = False, timeout=20.0, retries=3) -> dict:
    """Query the Wayback CDX index for capture history.

    Two bounded, fast calls by default: the single oldest capture and the most
    recent `cdx_limit` captures (the newest of which is the last capture). An
    exact total requires an unbounded server-side scan, so it is opt-in via
    `count=True` (adds a month-collapsed scan reported as `active_months`).

    Degrades gracefully: CDX is frequently slow/rate-limited, so any failure
    here is captured under an `error` key rather than aborting the lookup.
    """
    q = urllib.parse.quote(url, safe="")
    base = "http://web.archive.org/cdx/search/cdx?url={q}&output=json".format(q=q)
    fl = "&fl=timestamp,original,statuscode,mimetype"
    out = {}
    try:
        first = parse_cdx(_cdx_get(base + fl + "&limit=1", timeout, retries))
        recent = parse_cdx(_cdx_get(base + fl + "&limit=-{n}".format(n=max(1, cdx_limit)), timeout, retries))
        out["first_capture"] = first[0] if first else None
        # CDX returns the recent window ascending; newest is last.
        out["last_capture"] = recent[-1] if recent else (first[0] if first else None)
        out["recent_count"] = len(recent)
        out["recent"] = list(reversed(recent))  # present newest-first
        if count:
            months = parse_cdx(_cdx_get(base + "&fl=timestamp&collapse=timestamp:6", timeout, retries))
            out["active_months"] = len(months)
    except ReconError as e:
        out["error"] = str(e)
    return out


def fetch_wayback(url: str, cdx=True, cdx_limit=10, count=False, timeout=15.0, retries=3) -> dict:
    if not url or not isinstance(url, str) or " " in url:
        raise InputError("invalid URL: {!r}".format(url))
    q = urllib.parse.urlencode({"url": url})
    api = "http://archive.org/wayback/available?{q}".format(q=q)
    result = parse_wayback(http_get_json(api, timeout=timeout, retries=retries), url)
    if cdx:
        result["cdx"] = fetch_cdx(url, cdx_limit=cdx_limit, count=count, timeout=timeout, retries=retries)
    return result


# ---------------------------------------------------------------------------
# Orchestrator: `profile` — chain the primitives into one structured report
# ---------------------------------------------------------------------------

# Subdomain prefixes worth resolving first when profiling a domain.
_HIGH_VALUE_PREFIXES = [
    "www", "mail", "api", "app", "dev", "staging", "stage", "test", "admin",
    "portal", "vpn", "remote", "autodiscover", "mx", "ns1", "ns2", "blog",
    "shop", "git", "cdn", "assets", "static",
]

# DNS record types pulled for the apex in a profile run.
_PROFILE_DNS_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "CAA"]

# Seconds to space out ip-api calls (free tier: 45 req/min). Patchable seam.
_IP_API_SPACING = 1.5


def _select_resolve_targets(apex: str, subs, limit: int) -> list:
    """Pick which hostnames to resolve: the apex first, then high-value
    subdomains that actually appear in the CT data, then fill alphabetically."""
    subset = [s for s in (subs or []) if not s.startswith("*.") and s != apex]
    seen = set(subset)
    chosen = [apex]
    for pref in _HIGH_VALUE_PREFIXES:
        cand = "{}.{}".format(pref, apex)
        if cand in seen and cand not in chosen:
            chosen.append(cand)
        if len(chosen) >= limit:
            break
    if len(chosen) < limit:
        for s in sorted(subset):
            if s in chosen:
                continue
            chosen.append(s)
            if len(chosen) >= limit:
                break
    return chosen[:limit]


def _ips_from_dns_answers(answers) -> list:
    out = []
    for a in answers or []:
        if a.get("type") in ("A", "AAAA") and a.get("data"):
            out.append(a["data"])
    return out


def _resolve_host(name: str, timeout, retries) -> dict:
    a = fetch_dns(name, "A", timeout=timeout, retries=retries)
    aaaa = fetch_dns(name, "AAAA", timeout=timeout, retries=retries)
    return {
        "name": name,
        "a": _ips_from_dns_answers(a["answers"]),
        "aaaa": _ips_from_dns_answers(aaaa["answers"]),
    }


def run_profile(
    domain: str,
    cert_limit: int = 25,
    resolve_limit: int = 6,
    ip_limit: int = 10,
    wayback_subs: int = 2,
    do_wayback: bool = True,
    timeout: float = 20.0,
    retries: int = 3,
    pause: "float | None" = None,
    wayback_timeout: float = 8.0,
    wayback_retries: int = 0,
) -> dict:
    """Chain certs -> rdap -> dns -> resolve -> ip/asn -> wayback into one report.

    Every step is fault-isolated: an upstream failure on one source is recorded
    under `errors` and the profile continues, so a flaky crt.sh never sinks the
    whole run. Repeated IP lookups are de-duplicated (an in-session memo), and
    ip-api calls are spaced out to respect its 45 req/min limit.
    """
    apex = normalize_domain(domain)
    pause = _IP_API_SPACING if pause is None else pause
    errors = []

    def step(name, fn):
        try:
            return fn()
        except ReconError as e:
            errors.append({"step": name, "error": str(e)})
            return None

    # 1. Certificate Transparency -> subdomains (capped). fetch_certs already
    #    falls back crt.sh -> certSpotter internally; a *partial* failure (one
    #    CT source down, another answered) is surfaced here so it stays auditable.
    certs = step("certs", lambda: fetch_certs(apex, limit=cert_limit, timeout=timeout, retries=retries))
    subs = certs["subdomains"] if certs else []
    sub_count = certs["subdomain_count"] if certs else 0
    ct_sources = certs.get("sources_used") if certs else []
    if certs:
        for ce in certs.get("errors") or []:
            errors.append({"step": "certs:{}".format(ce["source"]), "error": ce["error"]})

    # 2. RDAP on the apex.
    rdap = step("rdap", lambda: fetch_rdap(apex, kind="domain", timeout=timeout, retries=retries))

    # 3. DNS on the apex (A/AAAA/MX/TXT/NS/CAA).
    dns = step("dns", lambda: fetch_dns_many(apex, _PROFILE_DNS_TYPES, timeout=timeout, retries=retries))

    # 4. Resolve the apex + high-value subdomains, collecting unique IPs.
    ips = set()
    if dns:
        for t in ("A", "AAAA"):
            rec = (dns.get("records") or {}).get(t)
            if rec:
                ips.update(_ips_from_dns_answers(rec.get("answers")))
    resolve_targets = _select_resolve_targets(apex, subs, resolve_limit)
    resolved = []
    for name in resolve_targets:
        if name == apex and dns:
            # apex A/AAAA already came from the dns step above.
            continue
        rec = step("resolve:{}".format(name), lambda name=name: _resolve_host(name, timeout, retries))
        if rec:
            resolved.append(rec)
            ips.update(rec["a"])
            ips.update(rec["aaaa"])

    # 5. IP geo/ISP + ASN ownership per unique IP (deduped, rate-limit spaced).
    unique_ips = sorted(ips)
    hosts_truncated = len(unique_ips) > ip_limit
    hosts = {}
    for i, ip in enumerate(unique_ips[:ip_limit]):
        if i > 0:
            _sleep(pause)  # courtesy spacing for ip-api's 45/min limit
        info = step("ip:{}".format(ip), lambda ip=ip: fetch_ip(ip, timeout=timeout, retries=retries))
        asn = step("asn:{}".format(ip), lambda ip=ip: fetch_asn(ip, timeout=timeout, retries=retries))
        hosts[ip] = {"ip": info, "asn": asn}

    # 6. Wayback summary on the apex + a couple high-value subdomains.
    #    This is the lowest-value / slowest step: the Wayback CDX index is
    #    frequently slow (single-target lookups seen in the tens of seconds),
    #    so it runs on a deliberately tight budget (short timeout, no retries).
    #    A slow archive.org must never make the orchestrator read as hung; a
    #    timed-out Wayback lookup is fault-isolated into `errors` like any other.
    wayback = []
    if do_wayback:
        wb_targets = [apex] + [s for s in resolve_targets if s != apex][:wayback_subs]
        for t in wb_targets:
            r = step("wayback:{}".format(t), lambda t=t: fetch_wayback(t, cdx=True, cdx_limit=5, timeout=wayback_timeout, retries=wayback_retries))
            if r:
                wayback.append(r)

    return {
        "source": "profile",
        "target": apex,
        "apex": {"rdap": rdap, "dns": dns},
        "subdomains": {
            "count": sub_count,
            "returned": len(subs),
            "truncated": bool(certs and certs.get("subdomains_truncated")),
            "ct_sources": ct_sources,
            "sample": subs,
            "resolved": resolved,
        },
        "hosts": hosts,
        "hosts_truncated": hosts_truncated,
        "wayback": wayback,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Human-readable rendering
# ---------------------------------------------------------------------------


# In --human mode, cap long prefix lists so ASN output stays readable.
# Full JSON output (the default) always includes every prefix.
_HUMAN_PREFIX_CAP = 15


def render_human(result: dict) -> str:
    src = result.get("source")
    lines = []
    if src in ("ct", "crt.sh", "certspotter"):
        via = ", ".join(result.get("sources_used") or [src])
        lines.append("certs — {} (via {})".format(result["domain"], via))
        lines.append("  subdomains ({}):".format(result["subdomain_count"]))
        for s in result["subdomains"]:
            lines.append("    {}".format(s))
        lines.append("  certificates: {}".format(result["cert_count"]))
        for err in result.get("errors") or []:
            lines.append("  ! {} unavailable: {}".format(err["source"], err["error"]))
    elif src == "rdap":
        if result.get("rdap_source") == "unreachable":
            lines.append("RDAP ({}) — .{} endpoint unreachable (retryable)".format(result.get("kind"), result.get("tld")))
            lines.append("  {}".format(result.get("reason")))
            return "\n".join(lines)
        if result.get("rdap_source") == "broken":
            rtag = "retryable" if result.get("retryable") else "not retryable"
            lines.append("RDAP ({}) — .{} endpoint broken [{}] ({})".format(
                result.get("kind"), result.get("tld"), result.get("cause"), rtag))
            lines.append("  {}".format(result.get("reason")))
            return "\n".join(lines)
        if result.get("supported") is False:
            lines.append("RDAP ({}) — unsupported for .{}".format(result.get("kind"), result.get("tld")))
            lines.append("  {}".format(result.get("reason")))
            return "\n".join(lines)
        # Some registries redact the top-level handle (e.g. .io/.de); fall back to
        # the domain/name/target so the header never reads "— None".
        title = result.get("handle") or result.get("ldhName") or result.get("name") or result.get("target")
        lines.append("RDAP ({}) — {}".format(result["kind"], title))
        for k in ("ldhName", "name", "startAddress", "endAddress", "country", "startAutnum", "endAutnum", "dnssec"):
            if result.get(k) is not None:
                lines.append("  {}: {}".format(k, result[k]))
        if result.get("nameservers"):
            lines.append("  nameservers: {}".format(", ".join(result["nameservers"])))
        if result.get("status"):
            lines.append("  status: {}".format(", ".join(result["status"])))
        for action, date in (result.get("events") or {}).items():
            lines.append("  {}: {}".format(action, date))
    elif src == "doh":
        if "records" in result:
            lines.append("DNS ({}) — {}".format(result["provider"], result["name"]))
            for t, rec in result["records"].items():
                vals = ", ".join(str(a["data"]) for a in rec["answers"]) or "(none)"
                lines.append("  {:5} {}".format(t, vals))
        else:
            lines.append("DNS {} {} [{}]".format(result["query_type"], result["name"], result["status_text"]))
            for a in result["answers"]:
                lines.append("  {:5} ttl={} {}".format(a["type"], a["ttl"], a["data"]))
    elif src == "ip-api.com":
        lines.append("ip-api — {}".format(result["ip"]))
        for k in ("country", "region", "city", "isp", "org", "as", "timezone"):
            if result.get(k):
                lines.append("  {}: {}".format(k, result[k]))
        flags = [k for k in ("mobile", "proxy", "hosting") if result.get(k)]
        if flags:
            lines.append("  flags: {}".format(", ".join(flags)))
    elif src == "ripestat":
        if result["kind"] == "asn":
            lines.append("RIPEstat ASN {} — {}".format(result["asn"], result.get("holder")))
            lines.append("  announced: {}".format(result.get("announced")))
            if "prefix_count" in result:
                shown = result["prefixes"][:_HUMAN_PREFIX_CAP]
                more = result["prefix_count"] - len(shown)
                suffix = " (+{} more)".format(more) if more > 0 else ""
                lines.append("  prefixes ({}): {}{}".format(result["prefix_count"], ", ".join(shown), suffix))
        else:
            lines.append("RIPEstat IP — prefix {}".format(result.get("prefix")))
            lines.append("  ASNs: {}".format(", ".join(result.get("asns", []))))
    elif src == "wayback":
        lines.extend(_render_wayback(result, indent="  "))
    elif src == "profile":
        return _render_profile(result)
    else:
        return json.dumps(result, indent=2, sort_keys=True)
    return "\n".join(lines)


def _render_wayback(result: dict, indent: str = "") -> list:
    lines = ["{}Wayback — {}".format(indent, result["url"])]
    lines.append("{}  archived: {}".format(indent, result["archived"]))
    if result.get("snapshot_url"):
        lines.append("{}  closest: {} ({})".format(indent, result["snapshot_url"], result.get("timestamp")))
    cdx = result.get("cdx") or {}
    if cdx.get("error"):
        lines.append("{}  cdx: unavailable ({})".format(indent, cdx["error"]))
    elif cdx:
        fc = cdx.get("first_capture") or {}
        lc = cdx.get("last_capture") or {}
        if fc.get("timestamp"):
            lines.append("{}  first capture: {}".format(indent, fc["timestamp"]))
        if lc.get("timestamp"):
            lines.append("{}  last capture:  {}".format(indent, lc["timestamp"]))
        if "active_months" in cdx:
            lines.append("{}  active months: {}".format(indent, cdx["active_months"]))
        if cdx.get("recent_count"):
            lines.append("{}  recent captures: {}".format(indent, cdx["recent_count"]))
    return lines


def _render_profile(result: dict) -> str:
    apex = result["target"]
    lines = ["profile — {}".format(apex)]

    rdap = (result.get("apex") or {}).get("rdap")
    if rdap and rdap.get("rdap_source") == "unreachable":
        lines.append("  rdap: unreachable (.{} endpoint reset/timed out — retryable)".format(rdap.get("tld")))
    elif rdap and rdap.get("rdap_source") == "broken":
        rtag = "retryable" if rdap.get("retryable") else "not retryable"
        lines.append("  rdap: broken (.{} endpoint {} — {})".format(rdap.get("tld"), rdap.get("cause"), rtag))
    elif rdap and rdap.get("supported") is False:
        lines.append("  rdap: unsupported (.{} has no public RDAP server)".format(rdap.get("tld")))
    elif rdap:
        reg = (rdap.get("events") or {}).get("registration")
        ns = ", ".join(rdap.get("nameservers") or [])
        lines.append("  registration: {}".format(reg))
        if ns:
            lines.append("  nameservers: {}".format(ns))

    dns = (result.get("apex") or {}).get("dns")
    if dns:
        lines.append("  dns:")
        for t, rec in (dns.get("records") or {}).items():
            vals = ", ".join(str(a["data"]) for a in rec["answers"]) or "(none)"
            lines.append("    {:5} {}".format(t, vals))

    subs = result.get("subdomains") or {}
    trunc = " (of {})".format(subs.get("count")) if subs.get("truncated") else ""
    lines.append("  subdomains: {}{}".format(subs.get("count"), trunc))
    for r in subs.get("resolved") or []:
        addrs = ", ".join((r.get("a") or []) + (r.get("aaaa") or [])) or "(no A/AAAA)"
        lines.append("    {} -> {}".format(r["name"], addrs))

    hosts = result.get("hosts") or {}
    if hosts:
        lines.append("  hosts:")
        for ip, h in hosts.items():
            info = h.get("ip") or {}
            asn = h.get("asn") or {}
            who = info.get("as") or (", ".join(asn.get("asns", [])) if asn else "")
            loc = " / ".join(x for x in (info.get("country"), info.get("city")) if x)
            lines.append("    {} — {} {}".format(ip, who, "[{}]".format(loc) if loc else "").rstrip())
    if result.get("hosts_truncated"):
        lines.append("    (host list truncated)")

    for wb in result.get("wayback") or []:
        lines.extend(_render_wayback(wb, indent="  "))

    errs = result.get("errors") or []
    if errs:
        lines.append("  errors ({}):".format(len(errs)))
        for e in errs:
            lines.append("    {}: {}".format(e["step"], e["error"]))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _emit(result, args):
    if getattr(args, "human", False):
        print(render_human(result))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="recon", description="Passive domain / infra OSINT over keyless HTTP APIs.")
    p.add_argument("--version", action="version", version="domain-recon {}".format(__version__))
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--human", action="store_true", help="human-readable output instead of JSON")
    common.add_argument("--timeout", type=float, default=20.0, help="per-request timeout in seconds")
    common.add_argument("--retries", type=int, default=3, help="retry attempts on 429/5xx/network errors")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("certs", parents=[common], help="crt.sh subdomain enumeration + cert history")
    c.add_argument("domain")
    c.add_argument("--no-wildcards", action="store_true", help="exclude *.wildcard subdomains")
    c.add_argument("--limit", type=int, default=None, help="cap the returned subdomain list (full count still reported)")
    c.add_argument("--max-certs", type=int, default=None, help="cap the returned certificate-history rows")
    c.add_argument("--all-ct", action="store_true",
                   help="query every CT source (crt.sh + certSpotter) and merge, instead of stopping at the first")

    r = sub.add_parser("rdap", parents=[common], help="RDAP (WHOIS) for domain / IP / ASN")
    r.add_argument("resource")
    r.add_argument("--kind", choices=["domain", "ip", "asn"], help="force resource kind (default: auto-detect)")
    r.add_argument("--no-bootstrap", action="store_true",
                   help="skip the IANA bootstrap; query rdap.org directly (domains only)")

    d = sub.add_parser("dns", parents=[common], help="DNS-over-HTTPS record lookup (PTR auto for IP targets)")
    d.add_argument("name")
    d.add_argument("--type", "-t", default="A", help="record type or comma list (A,AAAA,MX,TXT,NS,CNAME,SOA,CAA,PTR)")
    d.add_argument("--provider", choices=list(DOH_PROVIDERS), default="google")

    i = sub.add_parser("ip", parents=[common], help="ip-api.com geo / ISP / ASN lookup")
    i.add_argument("ip")

    a = sub.add_parser("asn", parents=[common], help="RIPEstat ASN / prefix / IP-ownership lookup")
    a.add_argument("resource")
    a.add_argument("--no-prefixes", action="store_true", help="skip announced-prefixes for ASN lookups")

    w = sub.add_parser("wayback", parents=[common], help="archive.org Wayback availability + CDX history")
    w.add_argument("url")
    w.add_argument("--no-cdx", action="store_true", help="availability only; skip the CDX capture-history lookup")
    w.add_argument("--cdx-limit", type=int, default=10, help="number of recent captures to list (default 10)")
    w.add_argument("--cdx-count", action="store_true", help="also compute active-months (an extra, slower scan)")

    pr = sub.add_parser("profile", parents=[common], help="orchestrate all sources into one domain report")
    pr.add_argument("domain")
    pr.add_argument("--cert-limit", type=int, default=25, help="cap subdomains pulled from crt.sh (default 25)")
    pr.add_argument("--resolve-limit", type=int, default=6, help="max hostnames to resolve, incl. apex (default 6)")
    pr.add_argument("--ip-limit", type=int, default=10, help="max unique IPs to enrich with ip+asn (default 10)")
    pr.add_argument("--no-wayback", action="store_true", help="skip the Wayback summary step")
    return p


def run(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.cmd == "certs":
            res = fetch_certs(
                args.domain,
                include_wildcards=not args.no_wildcards,
                limit=args.limit,
                max_certs=args.max_certs,
                timeout=args.timeout,
                retries=args.retries,
                merge_all=args.all_ct,
            )
        elif args.cmd == "rdap":
            res = fetch_rdap(
                args.resource,
                kind=args.kind,
                timeout=args.timeout,
                retries=args.retries,
                use_bootstrap=not args.no_bootstrap,
            )
        elif args.cmd == "dns":
            types = [t.strip() for t in args.type.split(",") if t.strip()]
            if len(types) == 1:
                res = fetch_dns(args.name, types[0], provider=args.provider, timeout=args.timeout, retries=args.retries)
            else:
                res = fetch_dns_many(args.name, types, provider=args.provider, timeout=args.timeout, retries=args.retries)
        elif args.cmd == "ip":
            res = fetch_ip(args.ip, timeout=args.timeout, retries=args.retries)
        elif args.cmd == "asn":
            res = fetch_asn(args.resource, with_prefixes=not args.no_prefixes, timeout=args.timeout, retries=args.retries)
        elif args.cmd == "wayback":
            res = fetch_wayback(
                args.url,
                cdx=not args.no_cdx,
                cdx_limit=args.cdx_limit,
                count=args.cdx_count,
                timeout=args.timeout,
                retries=args.retries,
            )
        elif args.cmd == "profile":
            res = run_profile(
                args.domain,
                cert_limit=args.cert_limit,
                resolve_limit=args.resolve_limit,
                ip_limit=args.ip_limit,
                do_wayback=not args.no_wayback,
                timeout=args.timeout,
                retries=args.retries,
            )
        else:  # pragma: no cover - argparse enforces this
            raise InputError("unknown command: {}".format(args.cmd))
    except ReconError as e:
        print("error: {}".format(e), file=sys.stderr)
        return 2
    _emit(res, args)
    # Quint-state RDAP contract, kept honest via the exit code. The code encodes
    # the *actionable retryability tier*; the JSON `rdap_source` names the
    # mechanism (unreachable = transport, broken = endpoint answered with a fault):
    #   0 = clean data (a real answer, OR a definitive 'unsupported'/WHOIS-only
    #       TLD — a terminal, non-retryable capability gap)
    #   2 = genuine error / crash (unhandled ReconError above — incl. 429/ban)
    #   3 = RETRYABLE failure: the endpoint is delegated (a server exists) but we
    #       could not get usable data this time and a later attempt may succeed —
    #       'unreachable' (transport reset/TLS-RST/timeout) OR 'broken' 5xx.
    #   4 = NON-retryable endpoint fault: 'broken' with an untrusted/self-signed
    #       TLS cert or an HTTP 4xx — the server answered definitively; retrying
    #       will not help until the registry fixes it.
    # Neither 3 nor 4 is collapsed into success: the field was not fetched, so a
    # caller branching on exit status can tell "skip, retry later" (3) from
    # "skip, don't bother" (4) from "clean result" (0).
    if isinstance(res, dict) and res.get("source") == "rdap":
        rs = res.get("rdap_source")
        if rs == "unreachable":
            return 3
        if rs == "broken":
            return 3 if res.get("retryable") else 4
    return 0


if __name__ == "__main__":
    sys.exit(run())
