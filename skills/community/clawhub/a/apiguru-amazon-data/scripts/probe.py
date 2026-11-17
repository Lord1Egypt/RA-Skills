#!/usr/bin/env python3
"""Call the Apiguru Amazon Data API from the command line.

Standard library only. Talks to exactly two first-party hosts, both fixed
below and never taken from the environment or from arguments:

  * https://agent.apiguru.app  the API: keyless (free probes, then HTTP 402),
                               or keyed when --api-key is given
  * https://dash.apiguru.app   the unauthenticated feedback wall (`feedback`)

Every request is pinned to one of those origins and redirects away from it are
refused, so an API key cannot be carried to a third host by a redirect.

A keyed call goes to the same gateway as a keyless one, so --limit, --compact
and --fields shape it the same way. It bills the key's account (the answer's
X-Billed-Requests and X-Balance-USD say how much), never the free probes.

This script never pays. A 402 is reported and the script exits; it contains
no wallet, no x402 client and no automatic retry with payment. Whether to
spend money is the user's decision. On an API key a call that got no answer
(a timeout or a dropped connection) is never repeated: it may already be
billed, so the script stops and says so. Only answered, unbilled statuses
(429 and 5xx) are retried on a key.

A key is never taken from the command line, from the environment, or from any
file the user did not name -- a value in `argv` is visible in shell history and
in the process table to every other local user. Three explicit ways in, all
requiring the user to act:

  * --api-key             prompt (getpass; the key is not echoed and not stored)
  * --api-key-file PATH   read it from a file the user names
  * --api-key-stdin       read it from standard input, e.g. from a secret store

    python probe.py capabilities                      # prices, the free-probe policy and
                                                      # THIS caller's remaining probes; free
    python probe.py product-details --asin B09DJLW458 --geo US
    python probe.py product --asins B09DJLW458,B0BSHF7WHW --geo DE --compact
                                                      # one light row per ASIN, with
                                                      # brand, weight and dimension
    python probe.py search --query "wireless earbuds" --geo UK --limit 10 --compact
    python probe.py best-sellers --category fashion --subcategory-code "women's shoes"
    python probe.py deals --geo DE --min-discount 30 --param categories=Elektronik
    python probe.py product-details --asin B09DJLW458 --geo US --api-key
    pass show apiguru | python probe.py product-details --asin B09DJLW458 --api-key-stdin
    python probe.py feedback --message "search: titles are brand-only" --category bug

Every list endpoint takes --limit N, --compact and --fields a,b,c (see
SKILL.md, "Big responses"); any parameter this script has no flag for yet
goes through --param name=value, repeatable.

Input is checked against the published API spec BEFORE any request is made
(required parameters, geo and enum values, ASIN / seller-id shape, integer
ranges, batch sizes); ASINs are upper-cased for you. A rejected input prints
the same error shape the API uses and exits 2 without touching the network.

Exit status: 0 the answer is usable; 1 an HTTP error, a body that reports
failure, or a batch in which every item failed; 2 bad input or usage; 3 a
batch in which some items failed (the rest are in the output). Read the body
either way -- it says what happened and whether anything was billed.
"""

from __future__ import annotations

import argparse
import getpass
import http.client
import json
import math
import pathlib
import re
import socket
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

# Fixed on purpose. Making these configurable would let a poisoned
# environment or prompt redirect requests (and an API key) elsewhere.
KEYLESS_BASE = "https://agent.apiguru.app/agent/v1"
# The same gateway. dash.apiguru.app/api/v1 bills the same account, but the
# backend behind it ignores `limit`, `compact` and `fields`: a keyed
# `product --compact` returned 145 KB for one ASIN there, 4.7 KB here.
KEYED_BASE = "https://agent.apiguru.app/agent/v1"
CAPABILITIES_URL = "https://agent.apiguru.app/.well-known/x402"
# Reports the caller's own free-probe standing without spending a probe.
HEALTH_URL = "https://agent.apiguru.app/health"
# The feedback wall. Unauthenticated, never billed, and the only POST this
# script makes. It sends exactly the text passed on the command line.
FEEDBACK_URL = "https://dash.apiguru.app/api/v1/feedback"
GITHUB_ISSUES = "https://github.com/apiguru-app/agent-kit/issues"
# Kept in step with the kit's release by spec/generate.py. It goes into the
# User-Agent and into every feedback entry, so a report can be read against
# the skill text that produced it.
SKILL_VERSION = "1.1.65"
USER_AGENT = f"apiguru-skill-probe/{SKILL_VERSION}"

# command -> path. Mirrors the endpoint list; see references/endpoints.md.
COMMANDS = {
    "product-details": "/v2/product-details",
    "product-reviews": "/v2/product-reviews",
    "search": "/search",
    "product": "/product",
    "stock": "/stock",
    "best-sellers": "/v2/best-sellers",
    "deals": "/v2/deals",
    "seller-profile": "/seller-profile",
    "seller-products": "/v2/seller-products",
    "seller-reviews": "/v2/seller-reviews",
}

# Transient AND unbilled, so retrying is free: the gateway refunds the probe
# (and never settles a payment) on every one of these. Matches
# references/errors-and-costs.md; a body that says `retryable: false` wins.
RETRYABLE = {429, 500, 502, 503, 504}
# A request the server never answered costs nothing either, so a client-side
# timeout or a dropped connection is retried the same way.
RETRIES = 3
TIMEOUT_SECONDS = 180

# Exit statuses. 2 is argparse's own "usage error", reused for rejected input.
EXIT_OK, EXIT_FAILED, EXIT_USAGE, EXIT_PARTIAL = 0, 1, 2, 3

# Per-item outcomes that mean "this row carries no data". The batch
# endpoints report them under `status`; a bare `error` string on a row, a
# `success: false` on a row, or a null row means the same thing.
FAILED_ITEM_STATUSES = {"not_found", "unavailable", "error", "failed"}

# --- BEGIN GENERATED RULES (spec/generate.py, from spec/endpoints.json) ---
# Do not edit by hand: the block is rewritten on every release so the local
# check can never disagree with what the API publishes.
GEOS = ['US', 'CA', 'DE', 'MX', 'UK', 'FR', 'IT', 'ES', 'AU', 'BR', 'IN', 'JP', 'NL', 'AE', 'PL', 'SA', 'SG', 'SE', 'TR', 'BE', 'IE', 'ZA', 'EG']
RULES = {
    '/v2/product-details': {
        'required': ['asin'],
        'params': {
            'asin': {'type': 'string', 'pattern': '^[A-Z0-9]{10}$'},
            'geo': {'type': 'string', 'enum': GEOS},
            'compact': {'type': 'boolean'},
        },
    },
    '/v2/product-reviews': {
        'required': ['asin'],
        'params': {
            'asin': {'type': 'string', 'pattern': '^[A-Z0-9]{10}$'},
            'geo': {'type': 'string', 'enum': GEOS},
            'from_rating': {'type': 'integer', 'minimum': 1, 'maximum': 5},
            'to_rating': {'type': 'integer', 'minimum': 1, 'maximum': 5},
            'max_reviews': {'type': 'integer', 'minimum': 0},
        },
    },
    '/search': {
        'required': ['query'],
        'params': {
            'page': {'type': 'integer', 'minimum': 1},
            'geo': {'type': 'string', 'enum': GEOS},
            'sort_by': {'type': 'string', 'enum': ['RELEVANCE', 'BEST_SELLERS', 'LOW_HIGH_PRICE', 'HIGH_LOW_PRICE', 'REVIEWS', 'NEWEST']},
            'min_price': {'type': 'number', 'minimum': 0},
            'max_price': {'type': 'number', 'minimum': 0},
            'product_condition': {'type': 'string', 'enum': ['NEW', 'USED', 'RENEWED']},
            'seller_id': {'type': 'string', 'pattern': '^[Aa][A-Za-z0-9]{9,20}$'},
            'today_deals': {'type': 'boolean'},
            'deal_type': {'type': 'string', 'enum': ['today_deals', 'all_discounts', 'coupons', 'buy_more_save_more']},
            'limit': {'type': 'integer', 'minimum': 0},
            'compact': {'type': 'boolean'},
        },
    },
    '/product': {
        'required': ['asins'],
        'params': {
            'asins': {'type': 'string', 'item_pattern': '^[A-Z0-9]{10}$', 'max_items': 20},
            'geo': {'type': 'string', 'enum': GEOS},
            'compact': {'type': 'boolean'},
        },
    },
    '/stock': {
        'required': ['asins'],
        'params': {
            'asins': {'type': 'string', 'item_pattern': '^[A-Z0-9]{10}$', 'max_items': 10},
            'geo': {'type': 'string', 'enum': GEOS},
            'check_inventory': {'type': 'boolean'},
            'page': {'type': 'integer', 'minimum': 1, 'maximum': 100},
        },
    },
    '/v2/best-sellers': {
        'required': [],
        'params': {
            'page': {'type': 'integer', 'minimum': 1, 'maximum': 5},
            'geo': {'type': 'string', 'enum': GEOS},
            'limit': {'type': 'integer', 'minimum': 0},
            'compact': {'type': 'boolean'},
        },
    },
    '/v2/deals': {
        'required': [],
        'params': {
            'geo': {'type': 'string', 'enum': GEOS},
            'offset': {'type': 'integer', 'minimum': 0},
            'min_product_star_rating': {'type': 'string', 'enum': ['4', 'ALL']},
            'min_price': {'type': 'number', 'minimum': 0},
            'max_price': {'type': 'number', 'minimum': 0},
            'min_discount': {'type': 'integer', 'minimum': 0, 'maximum': 100},
            'max_discount': {'type': 'integer', 'minimum': 0, 'maximum': 100},
            'prime_exclusive': {'type': 'boolean'},
            'prime_early_access': {'type': 'boolean'},
            'limit': {'type': 'integer', 'minimum': 0},
            'compact': {'type': 'boolean'},
        },
    },
    '/seller-profile': {
        'required': ['seller_ids'],
        'params': {
            'seller_ids': {'type': 'string', 'item_pattern': '^[Aa][A-Za-z0-9]{9,20}$', 'max_items': 10},
            'geo': {'type': 'string', 'enum': GEOS},
        },
    },
    '/v2/seller-products': {
        'required': ['seller_id'],
        'params': {
            'seller_id': {'type': 'string', 'pattern': '^[Aa][A-Za-z0-9]{9,20}$'},
            'page': {'type': 'integer', 'minimum': 1},
            'geo': {'type': 'string', 'enum': GEOS},
            'sort_by': {'type': 'string', 'enum': ['RELEVANCE', 'BEST_SELLERS', 'LOW_HIGH_PRICE', 'HIGH_LOW_PRICE', 'REVIEWS', 'NEWEST']},
            'min_price': {'type': 'number', 'minimum': 0},
            'max_price': {'type': 'number', 'minimum': 0},
            'product_condition': {'type': 'string', 'enum': ['NEW', 'USED', 'RENEWED']},
            'today_deals': {'type': 'boolean'},
            'deal_type': {'type': 'string', 'enum': ['today_deals', 'all_discounts', 'coupons', 'buy_more_save_more']},
            'limit': {'type': 'integer', 'minimum': 0},
            'compact': {'type': 'boolean'},
        },
    },
    '/v2/seller-reviews': {
        'required': ['seller_id'],
        'params': {
            'seller_id': {'type': 'string', 'pattern': '^[Aa][A-Za-z0-9]{9,20}$'},
            'page': {'type': 'integer', 'minimum': 1},
            'from_rating': {'type': 'integer', 'minimum': 1, 'maximum': 5},
            'to_rating': {'type': 'integer', 'minimum': 1, 'maximum': 5},
            'geo': {'type': 'string', 'enum': GEOS},
            'limit': {'type': 'integer', 'minimum': 0},
            'compact': {'type': 'boolean'},
        },
    },
}
# --- END GENERATED RULES ---


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse every redirect.

    Fixing the base URL in the source is not enough on its own: urlopen
    follows redirects by default and keeps the request headers, so a redirect
    from the API host would carry `X-API-KEY` to wherever it pointed. Neither
    of these two endpoints redirects, so any redirect is either a
    misconfiguration or an attempt to move the credential -- both are errors.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.URLError(
            f"refused a {code} redirect to {newurl!r}: this script does not follow "
            "redirects, so an API key can never leave the host it was sent to"
        )


def opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(NoRedirect)


def open_url(req, timeout: int):
    """Every request in this file goes through here, redirects refused."""
    return opener().open(req, timeout=timeout)


def read_api_key(args) -> str | None:
    """Get the key from the one place the user chose, never from argv.

    A secret passed as a command-line value lands in shell history and in the
    process table, where any other local user can read it. A source the user
    named explicitly but which turns out empty is an error, not a silent
    fall-back to the keyless path: the user asked for their account to be
    used, and a keyless call would spend a free probe instead and mislead
    them about which mode answered.
    """
    sources = [bool(args.api_key), bool(args.api_key_file), bool(args.api_key_stdin)]
    if sum(sources) > 1:
        print("Choose one of --api-key, --api-key-file, --api-key-stdin.", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)

    if args.api_key_file:
        path = pathlib.Path(args.api_key_file)
        try:
            key = path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            print(f"Could not read the key file: {exc}", file=sys.stderr)
            raise SystemExit(EXIT_USAGE) from exc
        try:
            mode = path.stat().st_mode
            if mode & (stat.S_IRGRP | stat.S_IROTH):
                print(f"Warning: {path} is readable by other users; make it readable only by you.",
                      file=sys.stderr)
        except OSError:
            pass
        if not key:
            print(f"The key file {path} is empty. Put the API key in it, or drop "
                  "--api-key-file to make a keyless call on purpose.", file=sys.stderr)
            raise SystemExit(EXIT_USAGE)
        return key

    if args.api_key_stdin:
        key = sys.stdin.readline().strip()
        if not key:
            print("No key on stdin.", file=sys.stderr)
            raise SystemExit(EXIT_USAGE)
        return key

    if args.api_key:
        if not sys.stdin.isatty():
            print("--api-key prompts for the key and needs a terminal. "
                  "Use --api-key-stdin or --api-key-file PATH instead.", file=sys.stderr)
            raise SystemExit(EXIT_USAGE)
        key = getpass.getpass("Apiguru API key (not echoed, not stored): ").strip()
        if not key:
            print("No key entered. Drop --api-key to make a keyless call on purpose.",
                  file=sys.stderr)
            raise SystemExit(EXIT_USAGE)
        return key

    return None


# --------------------------------------------------------------------------
# Local validation, driven by the generated RULES block.

def local_error(message: str, *, code: str, param: str | None, next_step: str,
                **extra) -> dict:
    """The API's own error shape, marked as produced here (no request made)."""
    body = {
        "error": message,
        "code": code,
        "http_status": 0,
        "billed": False,
        "retryable": False,
        "param": param,
        "next_step": next_step,
        "checked_locally": True,
    }
    body.update(extra)
    return body


def _coerce_number(rule: dict, name: str, value: str) -> tuple[str | None, dict | None]:
    kind = rule.get("type")
    try:
        number = int(value) if kind == "integer" else float(value)
    except (TypeError, ValueError):
        return None, local_error(
            f"'{value}' is not a valid {name}: expected {'an integer' if kind == 'integer' else 'a number'}.",
            code="invalid_parameter", param=name, next_step=f"Retry with a numeric {name}.")
    # float() happily parses "nan" and "inf", and a minimum-only bound does
    # not catch either (NaN compares false, +inf compares above).
    if not math.isfinite(number):
        return None, local_error(
            f"'{value}' is not a valid {name}: it must be a finite number.",
            code="invalid_parameter", param=name, next_step=f"Retry with a finite {name}.")
    low, high = rule.get("minimum"), rule.get("maximum")
    if low is not None and number < low:
        return None, local_error(
            f"{name}={value} is below the minimum of {low}.", code="invalid_parameter",
            param=name, next_step=f"Retry with {name} >= {low}.", minimum=low, maximum=high)
    if high is not None and number > high:
        return None, local_error(
            f"{name}={value} is above the maximum of {high}.", code="invalid_parameter",
            param=name, next_step=f"Retry with {name} <= {high}.", minimum=low, maximum=high)
    return str(number) if kind == "integer" else value, None


def validate(path: str, params: dict[str, str]) -> dict | None:
    """Check `params` against the published rules for `path`, normalising
    in place (ASINs upper-cased, enums canonicalised, booleans folded).

    Returns an error body for the first problem found, or None. Parameters
    the spec does not know are passed through untouched: the server decides.
    Mirrors gateway/validate.py plus the integer ranges the backend enforces.
    """
    rules = RULES.get(path)
    if not rules:
        return None
    props = rules.get("params", {})

    for name in rules.get("required", []):
        if not str(params.get(name) or "").strip():
            flag = "--" + name.replace("_", "-")
            return local_error(
                f"'{name}' is required for {path} and was not given.",
                code="missing_parameter", param=name,
                next_step=f"Retry with {flag} VALUE.")

    for name, value in list(params.items()):
        rule = props.get(name)
        if rule is None or value is None:
            continue
        value = str(value).strip()
        if value == "":
            continue

        allowed = rule.get("enum")
        if allowed:
            folded = {str(a).lower(): a for a in allowed}
            canonical = folded.get(value.lower())
            if canonical is None:
                return local_error(
                    f"'{value}' is not a valid {name}. Allowed: {', '.join(map(str, allowed))}.",
                    code="invalid_parameter", param=name,
                    next_step=f"Retry with one of the listed {name} values.", allowed=allowed)
            params[name] = str(canonical)
            continue

        if rule.get("type") == "boolean":
            truthy, falsy = {"true", "1", "yes", "on"}, {"false", "0", "no", "off"}
            if value.lower() in truthy:
                params[name] = "true"
            elif value.lower() in falsy:
                params[name] = "false"
            else:
                return local_error(
                    f"'{value}' is not a valid {name}: expected true or false.",
                    code="invalid_parameter", param=name, next_step=f"Retry with {name}=true or false.")
            continue

        if rule.get("type") in ("integer", "number"):
            fixed, error = _coerce_number(rule, name, value)
            if error:
                return error
            params[name] = fixed
            continue

        pattern = rule.get("item_pattern") or rule.get("pattern")
        if pattern:
            compiled = re.compile(pattern)
            is_list = bool(rule.get("item_pattern"))
            parts = [p.strip() for p in value.split(",")] if is_list else [value]
            parts = [p for p in parts if p]
            if not parts:
                # ",,," is not empty as a string but is empty as a list.
                return local_error(
                    f"'{name}' has no items in it (got {value!r}).",
                    code="missing_parameter" if name in rules.get("required", []) else "invalid_parameter",
                    param=name, next_step=f"Retry with a comma-separated {name} list.")
            fixed = []
            for part in parts:
                if compiled.fullmatch(part):
                    fixed.append(part)
                elif compiled.fullmatch(part.upper()):
                    # ASINs are upper-case by definition; a lower-case one is
                    # the caller's copy-paste, not a different product.
                    fixed.append(part.upper())
                else:
                    return local_error(
                        f"'{part}' is not a valid {name}. It must match {pattern}.",
                        code="invalid_parameter", param=name,
                        next_step=("ASINs are ten UPPERCASE alphanumeric characters."
                                   if name in ("asin", "asins") else "Correct the value and retry."),
                        pattern=pattern)
            if is_list:
                # Duplicates are dropped here, after normalisation: /product
                # collapses them anyway, while /stock and /seller-profile
                # fetch and bill each copy as given -- and the batch cap is
                # a cap on distinct items.
                unique = list(dict.fromkeys(fixed))
                if len(unique) < len(fixed):
                    print(f"  dropped {len(fixed) - len(unique)} duplicate {name} entr"
                          f"{'y' if len(fixed) - len(unique) == 1 else 'ies'}", file=sys.stderr)
                fixed = unique
                limit = rule.get("max_items")
                if limit and len(fixed) > limit:
                    return local_error(
                        f"{len(fixed)} distinct {name} given; the maximum is {limit} per call.",
                        code="too_many_items", param=name,
                        next_step=f"Split the list into calls of at most {limit}.", max_items=limit)
            params[name] = ",".join(fixed)

    return None


# --------------------------------------------------------------------------
# Output

def emit(obj) -> None:
    """Print `obj` as JSON without ever crashing on the console's encoding.

    Amazon titles carry non-breaking hyphens, curly quotes and en dashes.
    On a Windows console (cp1251, cp1252, ...) printing them raised
    UnicodeEncodeError from inside print() -- a traceback instead of the
    answer, exit 1, on a perfectly good response. Readable Unicode is tried
    first; when the stream cannot encode it, the same document goes out with
    \\uXXXX escapes, which is still valid, lossless JSON.
    """
    try:
        print(json.dumps(obj, indent=2, ensure_ascii=False))
    except UnicodeEncodeError:
        print(json.dumps(obj, indent=2, ensure_ascii=True))


def robust_stderr() -> None:
    """Never let a diagnostic line crash the run: stderr is for people, so
    an unencodable character becomes an escape rather than an exception."""
    try:
        sys.stderr.reconfigure(errors="backslashreplace")
    except (AttributeError, ValueError):
        pass


# --------------------------------------------------------------------------
# HTTP

def _lower_headers(headers) -> dict[str, str]:
    """HTTP header names are case-insensitive and HTTP/2 sends them in lower
    case, so every lookup goes through a lower-cased copy."""
    return {str(k).lower(): v for k, v in dict(headers or {}).items()}


def header(headers: dict, name: str):
    return headers.get(name.lower())


def _parse_body(raw: bytes, status: int) -> dict:
    """A body that is not JSON is reported, never raised: an HTML error page
    from a proxy, or a truncated answer, is still a result to act on."""
    text = raw.decode("utf-8", "replace")
    try:
        return json.loads(text)
    except ValueError:
        return {
            "error": f"the response (HTTP {status}) was not JSON",
            "code": "malformed_response",
            "http_status": status,
            "billed": False,
            "retryable": True,
            "body_preview": text[:500],
            "next_step": "Retry once; if it persists, report it with `feedback`.",
        }


def request(path: str, params: dict[str, str], api_key: str | None, retries: int = RETRIES):
    """GET the endpoint; keyed when an API key was passed explicitly.

    Returns (status, body, headers). `status` is 0 when no HTTP answer was
    received (timeout, connection failure); `body` is then a structured error
    with `code`, `billed: false` and `retryable`, never an exception. Header
    names in `headers` are lower-cased.
    """
    base = KEYED_BASE if api_key else KEYLESS_BASE
    query = {k: v for k, v in params.items() if v is not None}
    url = f"{base}{path}?{urllib.parse.urlencode(query)}"

    headers = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if api_key:
        # Only ever sent to KEYED_BASE above.
        headers["X-API-KEY"] = api_key

    def transport_error(code: str, message: str) -> tuple[int, dict, dict]:
        return 0, {
            "error": message,
            "code": code,
            "http_status": 0,
            "billed": False,
            "retryable": True,
            "next_step": "Nothing was billed for a request the server never answered; retry.",
        }, {}

    last_error = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers=headers)
        try:
            with open_url(req, timeout=TIMEOUT_SECONDS) as response:
                return response.status, _parse_body(response.read(), response.status), \
                    _lower_headers(response.headers)
        except urllib.error.HTTPError as exc:
            body = _parse_body(exc.read(), exc.code)
            answer = (exc.code, body, _lower_headers(exc.headers))
            # The body knows better than the status table: a 5xx whose
            # cause is permanent says `retryable: false`.
            body_says_no = isinstance(body, dict) and body.get("retryable") is False
            if exc.code in RETRYABLE and not body_says_no and attempt < retries:
                delay = 2**attempt
                print(
                    f"  [{exc.code}] transient and not billed, retrying in {delay}s "
                    f"({attempt + 1}/{retries})",
                    file=sys.stderr,
                )
                time.sleep(delay)
                last_error = answer
                continue
            return answer
        except (TimeoutError, urllib.error.URLError, OSError, http.client.HTTPException) as exc:
            # socket.timeout is TimeoutError since 3.10; URLError wraps the
            # rest (and is itself an OSError). A connection dropped while the
            # answer was read arrives unwrapped (RemoteDisconnected,
            # IncompleteRead). A refused redirect lands here too and is
            # final: retrying would repeat the refusal.
            reason = getattr(exc, "reason", exc)
            text = str(reason)
            if "refused a" in text and "redirect" in text:
                status, body, hdrs = transport_error("redirect_refused", text)
                body["retryable"] = False
                body["next_step"] = "Report it: neither API host redirects."
                return status, body, hdrs
            if isinstance(reason, TimeoutError) or isinstance(exc, TimeoutError) \
                    or "timed out" in text.lower():
                last_error = transport_error(
                    "client_timeout", f"no response within {TIMEOUT_SECONDS}s: {text}")
            else:
                last_error = transport_error("connection_failed", f"connection failed: {text}")
            if api_key:
                # On a key the API bills a call when its answer is ready, just
                # before sending it, so a timeout or a connection dropped after
                # the request went out may already be billed. Repeating it on
                # our own could charge twice (ClawHub audits: timeouts
                # 2026-09-30, dropped connections 2026-10-27), so a keyed call
                # is never repeated here; the decision goes back to the user.
                if isinstance(reason, (socket.gaierror, ConnectionRefusedError)):
                    # The name did not resolve or nothing accepted the
                    # connection: the request never left this machine.
                    last_error[1]["next_step"] = (
                        "The API never received this call, so nothing was billed. "
                        "It is safe to run it again.")
                else:
                    last_error[1].update(
                        billed="unknown", retryable=False,
                        next_step=("The API may have answered and billed this call before the answer "
                                   "was lost. Do not repeat it automatically: tell the user, and retry "
                                   "only if they agree."))
                return last_error
            if attempt < retries:
                delay = 2**attempt
                print(f"  [{last_error[1]['code']}] not billed, retrying in {delay}s "
                      f"({attempt + 1}/{retries})", file=sys.stderr)
                time.sleep(delay)
                continue
    return last_error or transport_error("request_failed", "request failed")


def explain(status: int, headers: dict, keyed: bool = False) -> None:
    """Say what a status means for cost and for what to do next.

    A 402 means different things on the two paths: keyless, the free probes
    are spent; keyed, the account cannot pay for this call (its body says
    what it can still cover). Both used to read "the free probes for this
    machine are spent"."""
    # The live figure beats any number in the docs, and some answers report
    # yes/no rather than a count.
    left = header(headers, "X-Free-Probes-Remaining")
    available = header(headers, "X-Free-Probes-Available")
    note = header(headers, "X-Price-Next-Call") or ""
    if left is not None:
        print(f"  free probes remaining: {left}"
              + (f" (next call would cost {note})" if note else ""), file=sys.stderr)
    elif available is not None:
        print(f"  free probes available: {available}"
              + (f" (a paid call would cost {note})" if note else ""), file=sys.stderr)

    messages = {
        0: ("No HTTP answer (timeout or connection failure). Keyless: not billed. With an API key the "
            "call may have been billed and is not retried; see the body."),
        402: (
            "Payment required: the free probes for this machine are spent. "
            "This script does not pay. Stop and ask the user how to proceed: "
            "they can provide an Apiguru API key (--api-key, bills their account) "
            "or, if they explicitly want pay-per-call, run their own x402 client "
            "with a spend cap. Do not set either up on your own."
        ),
        404: "Not found. BILLED on the keyed path: the ASIN is absent from this marketplace; try another geo.",
        400: "Bad input, not billed. ASINs must be 10 UPPERCASE alphanumeric chars.",
        413: "Too many items for one call, not billed. Split the list.",
        429: "Rate limited, not billed. Back off and retry.",
        500: "Internal error on our side, not billed. Retried; if it persists, report it.",
        502: "Bad gateway, not billed. Retried with backoff.",
        503: "Temporary failure on our side, not billed. Safe to retry.",
        504: "Gateway timeout, not billed. Retried; a narrower query often succeeds.",
    }
    if keyed:
        messages[402] = (
            "Payment required: the account behind this API key cannot pay for this call. "
            "Nothing was billed. The body says what it can still cover (affordable_requests, "
            "max_items) and what to do (next_step): a smaller call may fit. This script does "
            "not pay or top up; tell the user, who can top up at https://dash.apiguru.app/top-up."
        )
    if status in messages:
        print(f"  {messages[status]}", file=sys.stderr)


def body_outcome(body) -> tuple[int, int]:
    """(failed, total) for the answer: (0, 1) is a clean success, (1, 1) a
    body-level failure, and a batch reports its failed rows over all rows.

    A 200 with `success: false`, or with a top-level `error`, is a failure
    the exit status must reflect; an automated job that only checked the
    status code used to record such answers as successes. Endpoints that
    omit `success` are not penalised for it.
    """
    if not isinstance(body, dict):
        return 0, 1
    if body.get("success") is False or body.get("error"):
        return 1, 1
    results = body.get("results")
    if isinstance(results, list) and results:
        failed = 0
        for item in results:
            if item is None:
                failed += 1
            elif isinstance(item, dict) and (
                item.get("error") or item.get("success") is False
                or item.get("status") in FAILED_ITEM_STATUSES
            ):
                failed += 1
        return failed, len(results)
    return 0, 1


def cmd_capabilities() -> int:
    """Show prices and this caller's own standing.

    Two sources: the x402 discovery document gives prices; /health says how
    many probes THIS caller has left right now, over what window. The
    catalogue no longer states the general allowance (a gateway from before
    2026-09-21 still does, and is printed if so) -- the figure that counts
    is the caller's own, and some answers report yes/no rather than a figure.
    Neither request spends a probe.
    """
    try:
        with open_url(urllib.request.Request(CAPABILITIES_URL), timeout=30) as response:
            data = json.load(response)
    except Exception as exc:
        print(f"Could not fetch capabilities: {exc}", file=sys.stderr)
        return EXIT_FAILED

    print(f"{data['service']}")
    print(f"  rails: {', '.join(data['rails']) or 'none'}")
    policy, window = data.get("freeProbesPerIp"), data.get("freeProbeWindowHours")
    if policy is not None and window is not None:
        print(
            f"  free-probe policy: {policy} per machine per {window}h "
            "(the general rule, not your balance); this script never pays a 402"
        )
    else:
        print("  free probes: a small allowance per caller before the 402 "
              "(your own figure is below, not a general rule); this script never pays a 402")

    try:
        with open_url(urllib.request.Request(HEALTH_URL, headers={"User-Agent": USER_AGENT}),
                      timeout=30) as response:
            health = json.load(response)
    except Exception as exc:
        health = {"error": str(exc)}
    if "free_calls_remaining" in health:
        hours = health.get("window_hours", window)
        print(f"  free probes remaining for this caller: {health['free_calls_remaining']} "
              + (f"({hours}h window)" if hours is not None else ""))
    elif "free_calls_available" in health:
        print(f"  free probes available for this caller: "
              f"{'yes' if health['free_calls_available'] else 'no'} "
              "(the exact count is not reported)")
    else:
        print(f"  free probes remaining: unknown ({health.get('error', 'no figure in /health')}); "
              "every data answer reports free_calls_remaining for this caller")

    if data.get("howToPay"):
        print(f"  how paying works (for the user to read): {data['howToPay']}")
    print("  endpoints:")
    for resource in data["resources"]:
        print(f"    {resource['name']:24} {resource['price']:22} {resource['method']} "
              f"{resource['resource']}")
    return EXIT_OK


def unmangled_path(value):
    """`--endpoint /v2/best-sellers` as it was typed.

    Git Bash on Windows rewrites an argument that starts with "/" into a
    path under its own install directory before Python sees it, so the wall
    received "C:/Program Files/Git/v2/best-sellers". Put the path back."""
    if not value:
        return value
    text = str(value).replace("\\", "/")
    for marker in ("/Git/", "/git/"):
        head, found, tail = text.partition(marker)
        if found and len(head) >= 2 and head[1] == ":" and head[0].isalpha():
            return "/" + tail
    return value


def cmd_feedback(args) -> int:
    """Post one entry to the public feedback wall. Free, no key, no signup."""
    if not args.message:
        print("feedback needs --message. Example:", file=sys.stderr)
        print('  python probe.py feedback --message "search: product_title is the brand" '
              '--category bug --endpoint /search', file=sys.stderr)
        print(f"With a GitHub account, prefer an issue: {GITHUB_ISSUES}", file=sys.stderr)
        return EXIT_USAGE

    payload = {
        "message": args.message,
        "category": (args.category or "other").lower(),
        "endpoint": unmangled_path(args.endpoint),
        # The skill version rides along so a report can be read against
        # the text that produced it (an install can lag the release).
        "agent": f"{args.agent or 'apiguru-skill-probe'} (skill {SKILL_VERSION})",
        "contact": args.contact,
        "source": "skill",
    }
    body = json.dumps({k: v for k, v in payload.items() if v}).encode("utf-8")
    request_obj = urllib.request.Request(
        FEEDBACK_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with open_url(request_obj, timeout=30) as response:
            emit(json.load(response))
            return EXIT_OK
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8", "replace"), file=sys.stderr)
    except (urllib.error.URLError, OSError) as exc:
        print(f"Could not reach the feedback wall: {exc}", file=sys.stderr)
    print(f"Open an issue instead: {GITHUB_ISSUES}", file=sys.stderr)
    return EXIT_FAILED


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Query the Apiguru Amazon Data API. Keyless by default; never pays a 402.",
    )
    parser.add_argument("command", choices=[*COMMANDS, "capabilities", "feedback"])
    for flag in (
        "asin", "asins", "geo", "query", "page", "sort_by", "seller_id",
        "seller_ids", "category", "subcategory_code", "category_id", "offset",
        "categories", "brands", "brand", "min_price", "max_price", "min_discount",
        "condition", "product_condition", "deal_type", "offers_count",
        "from_rating", "to_rating", "max_reviews",
        # what every list endpoint returns: `--limit N` rows, `--fields a,b`
        "limit", "fields",
        # feedback-only (`category` above is reused)
        "message", "endpoint", "agent", "contact",
    ):
        parser.add_argument(f"--{flag.replace('_', '-')}", dest=flag, default=None)
    parser.add_argument("--check-inventory", dest="check_inventory", action="store_true")
    parser.add_argument("--today-deals", dest="today_deals", action="store_true")
    parser.add_argument("--compact", action="store_true",
                        help="Light rows only (the REST default is the full row). On `product` "
                             "each row keeps title, brand, price, availability, bullets, "
                             "weight and dimension.")
    # The API grows faster than this flag list; an argparse that did not know
    # a parameter used to mean the caller could not send it at all.
    parser.add_argument("--param", action="append", default=[], metavar="NAME=VALUE",
                        help="Any other query parameter, repeatable.")
    # A key is never a command-line VALUE: argv is visible in shell history and
    # in the process table. These three make the user choose how it arrives.
    parser.add_argument(
        "--api-key",
        dest="api_key",
        action="store_true",
        help="Prompt for an Apiguru API key (not echoed, not stored) and bill that "
             "account instead of using free probes. Only with the user's explicit consent.",
    )
    parser.add_argument(
        "--api-key-file",
        dest="api_key_file",
        default=None,
        help="Read the API key from this file (keep it readable only by you).",
    )
    parser.add_argument(
        "--api-key-stdin",
        dest="api_key_stdin",
        action="store_true",
        help="Read the API key from standard input, e.g. piped from a secret store.",
    )
    parser.add_argument("--raw", action="store_true", help="Print raw JSON only.")

    args = parser.parse_args(argv)
    robust_stderr()

    if args.command == "capabilities":
        return cmd_capabilities()
    if args.command == "feedback":
        return cmd_feedback(args)

    params = {
        k: v
        for k, v in vars(args).items()
        if k not in ("command", "raw", "check_inventory", "today_deals", "compact", "param",
                     "api_key", "api_key_file", "api_key_stdin",
                     "message", "endpoint", "agent", "contact")
        and v is not None
    }
    if args.check_inventory:
        params["check_inventory"] = "true"
    if args.today_deals:
        params["today_deals"] = "true"
    if args.compact:
        params["compact"] = "true"
    for item in args.param:
        name, sep, value = item.partition("=")
        if not sep or not name.strip():
            print(f"--param takes NAME=VALUE, got {item!r}", file=sys.stderr)
            return EXIT_USAGE
        params[name.strip()] = value

    path = COMMANDS[args.command]

    # Checked before the key is read and before any request: a rejected
    # input costs nothing and never touches the network.
    problem = validate(path, params)
    if problem:
        emit(problem)
        print(f"  rejected locally, no request made: {problem['error']}", file=sys.stderr)
        return EXIT_USAGE

    api_key = read_api_key(args)

    if not args.raw:
        mode = "keyed: this call bills the account behind that key" if api_key else "keyless: free probe"
        print(f"-> {args.command} ({mode})", file=sys.stderr)

    status, body, headers = request(path, params, api_key)

    if not args.raw:
        explain(status, headers, keyed=bool(api_key))

    emit(body)

    if status != 200:
        return EXIT_FAILED
    failed, total = body_outcome(body)
    if failed == 0:
        return EXIT_OK
    if failed < total:
        print(f"  partial: {failed} of {total} items failed; see their status/error fields",
              file=sys.stderr)
        return EXIT_PARTIAL
    print("  the answer reports failure (see error/status in the body)", file=sys.stderr)
    return EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
