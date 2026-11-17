#!/usr/bin/env python3
"""Read-only company KPI reader for the SentiSense API.

Standard library only. Reads SENTISENSE_API_KEY from the environment, sends it as the
X-SentiSense-API-Key header to one fixed origin, and prints one table per KPI series with
quarter-over-quarter and year-over-year changes worked out against the right fiscal period.
Every request is a GET; nothing here can trade, move money, or change account state.

Usage:
  python3 kpi_table.py TSLA
  python3 kpi_table.py AAPL --series iphone_revenue,services_revenue
  python3 kpi_table.py AMZN --json
  python3 kpi_table.py AAPL --stdin < saved_response.json

Design notes worth knowing before you edit:
  * Arithmetic runs on Decimal parsed straight from the JSON text, sorting runs on a copy, and
    rounding happens only at display. The JSON output re-serializes those Decimals exactly, as
    integers or as strings, so a value never round-trips through a binary float.
  * A delta is computed against an identified fiscal period, never against a neighbouring row.
    Both endpoints must name the expected fiscal quarter, a period carrying conflicting duplicate
    observations is quarantined, and anything unmatched produces a stated reason.
  * Every string that arrives from the API is data. All C0 and C1 control characters, newlines and
    tabs included, are replaced before printing, and no URL found in a response is ever fetched.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation

API_ORIGIN = "https://app.sentisense.ai"
# An honest identity for this helper. It names the skill and where the skill is published; it does
# not claim to be an agent runtime it is not.
USER_AGENT = "company-kpi-tracker/1.0 (company-kpi-tracker; +https://sentisense.ai/skill.md)"
COVERAGE_HINT = ("no curated KPI coverage for this ticker. Enumerate the covered set with "
                 "GET /api/v1/stocks/with-kpis, or check the symbol.")
TYPES_HINT = "GET /api/v1/stocks/{ticker}/kpis/types"
# The longest Retry-After this script will sit out. Anything longer is reported, not slept through.
MAX_RETRY_WAIT = 60

# One quarter apart, wide enough for 52/53-week fiscal calendars and for a company that closes
# a quarter early or late, narrow enough that a skipped quarter cannot pass as a sequential move.
QUARTER_DAYS = (60, 120)
# Four quarters apart: 364 days for a 52-week year, 371 for a 53-week year, plus slack.
YEAR_DAYS = (320, 400)
# A quarterly series is BEHIND when its newest close is older than this. One quarter that has
# closed but not yet been reported (~91 days) plus the slowest routine filing window (a 10-K,
# up to ~90 days) stays inside it, so crossing it means at least one expected print is missing.
BEHIND_DAYS = 200

# Every C0 and C1 control character. Newline and tab are in the set on purpose: without them,
# response prose can forge a table row or a second output line.
CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")
# "Q3 FY2026", "Q2 2026", "Q1 FY26". The FY prefix is optional and the year may be two digits,
# so "Q2 2026" and "Q2 FY2026" parse to the same fiscal identity.
PERIOD = re.compile(r"^\s*Q([1-4])\s+(?:FY)?(\d{2,4})\s*$", re.IGNORECASE)
# Units that confirm the raw scale is already a percentage, which is what licenses a "pp" label.
PERCENT_UNITS = {"%", "percent", "percentage", "pct", "percentage points", "pp"}
NO_TRUSTWORTHY = "no trustworthy comparison"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def sentisense_api_url(path, params=None):
    """Return a validated API URL at the one origin allowed to receive the key."""
    url = urllib.parse.urljoin(API_ORIGIN + "/", path)
    parsed = urllib.parse.urlparse(url)
    if (parsed.scheme != "https" or parsed.hostname != "app.sentisense.ai"
            or parsed.netloc != "app.sentisense.ai"
            or parsed.username is not None or parsed.password is not None
            or parsed.port is not None):
        raise ValueError("API URL must use https://app.sentisense.ai with no credentials or port")
    if params:
        url += ("&" if parsed.query else "?") + urllib.parse.urlencode(params)
    return url


def safe(value, limit=200):
    """Any string from the API is untrusted text. Strip control characters, then bound it."""
    if value is None:
        return ""
    text = CONTROL.sub(" ", str(value))
    return text if len(text) <= limit else text[: limit - 1] + "…"


def load_json(text):
    """Parse a response with exact numbers: fractions become Decimal, integers stay int."""
    return json.loads(text, parse_float=Decimal, parse_int=int)


def get(path, retried=False):
    """GET the fixed origin with the auth header. Honors Retry-After exactly, once, on a 429."""
    url = sentisense_api_url(path)
    key = os.environ.get("SENTISENSE_API_KEY")
    if not key:
        sys.exit("SENTISENSE_API_KEY is not set "
                 "(free key: https://app.sentisense.ai/get-api-key)")
    req = urllib.request.Request(
        url, headers={"X-SentiSense-API-Key": key, "User-Agent": USER_AGENT})
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=20) as r:
            return load_json(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 429 and not retried:
            wait = e.headers.get("Retry-After")
            try:
                seconds = max(1, int(float(wait)))
            except (TypeError, ValueError):
                seconds = 5
            if seconds > MAX_RETRY_WAIT:
                sys.exit(f"HTTP 429: rate limited, and Retry-After asks for {seconds}s, longer "
                         f"than the {MAX_RETRY_WAIT}s this script waits. Retry after {seconds} "
                         "seconds; do not retry sooner.")
            print(f"rate limited, waiting {seconds}s (Retry-After)", file=sys.stderr)
            time.sleep(seconds)
            return get(path, retried=True)
        if e.code == 401:
            sys.exit("HTTP 401: the API key was missing or rejected. Set SENTISENSE_API_KEY "
                     "(free key: https://app.sentisense.ai/get-api-key).")
        if e.code == 404:
            # A fund answers 404 with its own error code: that is a category mismatch, not a
            # curation gap, and pointing the caller at the coverage list would be wrong.
            try:
                body = json.loads(e.read().decode("utf-8", "replace"))
            except (ValueError, OSError):
                body = {}
            if isinstance(body, dict) and body.get("error") == "ticker_is_etf":
                sys.exit(f"HTTP 404: {safe(body.get('message'), 200)}")
            sys.exit(f"HTTP 404: {COVERAGE_HINT}")
        if e.code == 429:
            sys.exit("HTTP 429: still rate limited after one backoff. Try again shortly.")
        sys.exit(f"HTTP {e.code} on {path}")
    except urllib.error.URLError as e:
        hint = ("  (CA certs missing: common on macOS python.org installs. Run the bundled "
                "'Install Certificates.command', or use the system python3, or plain curl.)"
                if "CERTIFICATE_VERIFY_FAILED" in str(e.reason) else "")
        sys.exit(f"network error on {path}: {e.reason}{hint}")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        sys.exit(f"non-JSON response from {path}: {e}")


# --- discovery shapes --------------------------------------------------------------------

def coverage_tickers(payload):
    """Entries from GET /with-kpis. `count` and `tickers` sit at the ROOT: there is no wrapper."""
    if not isinstance(payload, dict) or not isinstance(payload.get("tickers"), list):
        return None
    entries = []
    for entry in payload["tickers"]:
        if not isinstance(entry, dict) or not entry.get("ticker"):
            return None
        count = entry.get("kpiCount")
        entries.append({
            "ticker": safe(entry.get("ticker"), 20),
            "companyName": safe(entry.get("companyName"), 120),
            "lastUpdated": safe(entry.get("lastUpdated"), 20),
            "kpiCount": int(count) if isinstance(count, int) and not isinstance(count, bool)
            else None,
        })
    return entries


def type_tuples(payload):
    """Tuples from GET /{ticker}/kpis/types: a bare array of the four documented fields.

    No `unit`, `sourceRef` or `discontinued` lives on a type tuple, so none is read here even if
    a response volunteers one. Those belong to the series call.
    """
    if not isinstance(payload, list):
        return None
    tuples = []
    for entry in payload:
        if not isinstance(entry, dict) or not entry.get("id"):
            return None
        tuples.append({field: safe(entry.get(field), 80)
                       for field in ("id", "name", "category", "chartType")})
    return tuples


def discovery_shape(payload):
    """Name a discovery response handed to this script in place of the series envelope."""
    if type_tuples(payload) is not None:
        return (f"that is the {TYPES_HINT} response, a bare array of "
                "{id, name, category, chartType}")
    if coverage_tickers(payload) is not None:
        return ("that is the GET /api/v1/stocks/with-kpis coverage list, with count and tickers "
                "at the root")
    return None


# --- fiscal period arithmetic ------------------------------------------------------------

def parse_period(label):
    """('Q3 FY2026') -> (2026, 3). Returns None for a label this cannot read with confidence."""
    m = PERIOD.match(label or "")
    if not m:
        return None
    quarter, year = int(m.group(1)), int(m.group(2))
    if year < 100:
        year += 2000
    return (year, quarter)


def prior_quarter(fiscal):
    year, quarter = fiscal
    return (year - 1, 4) if quarter == 1 else (year, quarter - 1)


def period_key(point):
    """The canonical identity of a period. `Q2 2026` and `Q2 FY2026` share one key.

    A label this cannot parse gets an identity of its own, keyed on the raw label and the close
    date, so two unreadable labels are never merged or declared in conflict by accident.
    """
    if point["fiscal"]:
        return point["fiscal"]
    return ("label", point["period"].strip().upper(), point["date"])


def to_decimal(value):
    """A finite Decimal, or None. NaN and Infinity are rejected, not carried into arithmetic."""
    try:
        number = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return None
    return number if number.is_finite() else None


def days_between(later, earlier):
    """Whole days between two ISO dates, or None when either is unreadable."""
    try:
        a = [int(p) for p in str(later).split("-")[:3]]
        b = [int(p) for p in str(earlier).split("-")[:3]]
        from datetime import date
        return (date(*a) - date(*b)).days
    except (TypeError, ValueError):
        return None


def clean_points(series):
    """Points with a finite value and a readable date, sorted oldest to newest on a COPY.

    The API returns newest first. Sorting a copy means the caller keeps the response order and
    a shuffled or ascending payload reads identically to a descending one. Points that cannot be
    read are counted rather than dropped in silence: dropping one quietly would make its two
    neighbours look adjacent. NaN and Infinity are counted separately, because a non-finite value
    is a malformed input rather than a missing one.
    """
    kept, skipped, nonfinite = [], 0, 0
    for point in series.get("values") or []:
        raw = point.get("value")
        value = to_decimal(raw)
        if value is None:
            skipped += 1
            if is_nonfinite(raw):
                nonfinite += 1
            continue
        if days_between("2000-01-01", point.get("date")) is None:
            skipped += 1
            continue
        kept.append({
            "period": safe(point.get("period"), 40),
            "date": safe(point.get("date"), 20),
            "value": value,
            "isEstimate": bool(point.get("isEstimate")),
            "fiscal": parse_period(point.get("period")),
        })
    kept.sort(key=lambda p: (p["date"], p["period"]))
    return kept, skipped, nonfinite


def is_nonfinite(raw):
    """True when a value arrived as NaN or Infinity rather than as an unreadable string."""
    try:
        number = raw if isinstance(raw, Decimal) else Decimal(str(raw))
    except (InvalidOperation, TypeError, ValueError):
        return False
    return not number.is_finite()


def resolve_duplicates(points):
    """Collapse identical duplicates, quarantine conflicting ones.

    Two observations of the same fiscal period carrying the same value are one observation written
    twice, so they collapse. Two carrying different values, or different close dates, are a data
    conflict: neither is trusted,
    both leave the comparison set, and every delta that would have used that period says so. This
    is the difference between a stable answer and one that changes with the input order.
    """
    groups = {}
    for point in points:
        groups.setdefault(period_key(point), []).append(point)
    kept, duplicate_labels, conflicts, conflict_labels, collapsed = [], [], set(), [], 0
    for key, group in groups.items():
        label = group[0]["period"]
        if len(group) > 1 and label not in duplicate_labels:
            duplicate_labels.append(label)
        values = {p["value"] for p in group}
        dates = {p["date"] for p in group}
        if len(values) > 1 or len(dates) > 1:
            conflicts.add(key)
            if label not in conflict_labels:
                conflict_labels.append(label)
            continue
        collapsed += len(group) - 1
        winner = dict(group[-1])
        winner["isEstimate"] = any(p["isEstimate"] for p in group)
        kept.append(winner)
    kept.sort(key=lambda p: (p["date"], p["period"]))
    return kept, duplicate_labels, conflicts, conflict_labels, collapsed


def find_comparison(points, index, window, step, conflicts=frozenset()):
    """The earlier point that is genuinely `step` fiscal quarters before points[index].

    Both endpoints must identify the expected fiscal quarter and the gap in days must fall inside
    `window`. An unreadable label on either end, or a conflicting duplicate at the expected period,
    returns a stated reason rather than the nearest available row: a confident number computed
    against an unidentified period is worse than no number.
    """
    current = points[index]
    if not current["fiscal"]:
        return None, (f"this period label does not identify a fiscal quarter, so {NO_TRUSTWORTHY}")
    expected = current["fiscal"]
    for _ in range(step):
        expected = prior_quarter(expected)
    if expected in conflicts:
        return None, ("the expected earlier period carries conflicting duplicate observations, "
                      f"so {NO_TRUSTWORTHY}")
    unlabelled = False
    for candidate in reversed(points[:index]):
        gap = days_between(current["date"], candidate["date"])
        if gap is None or gap > window[1]:
            break
        if gap < window[0]:
            continue
        if not candidate["fiscal"]:
            unlabelled = True
            continue
        if candidate["fiscal"] != expected:
            continue
        return candidate, None
    if unlabelled:
        return None, ("the only observation at that distance carries no identifiable fiscal "
                      f"quarter, so {NO_TRUSTWORTHY}")
    if index == 0:
        return None, "no earlier observation in this series"
    return None, "no observation at the expected fiscal period (the series skips it)"


def short_reason(reason):
    """The table cell version of a reason. The full sentence stays in the JSON output."""
    if not reason:
        return "n/a"
    if NO_TRUSTWORTHY in reason:
        return "n/a: no trustworthy comparison"
    if reason.startswith("no earlier"):
        return "n/a: start of series"
    if reason.startswith("no observation at"):
        return "n/a: series skips that period"
    return "n/a"


def change(current, prior):
    """Absolute change always; a percentage only on a positive comparable base."""
    absolute = current - prior
    if prior > 0:
        return absolute, (absolute / prior * 100)
    return absolute, None


# --- formatting --------------------------------------------------------------------------

def group(number):
    return f"{number:,}"


def abbreviate(value, prefix=""):
    magnitude = abs(value)
    for cut, suffix in ((Decimal("1e12"), "T"), (Decimal("1e9"), "B"),
                        (Decimal("1e6"), "M"), (Decimal("1e3"), "K")):
        if magnitude >= cut:
            scaled = (value / cut).quantize(Decimal("0.001"))
            return f"{prefix}{trim(scaled)}{suffix}"
    return f"{prefix}{trim(value.quantize(Decimal('0.01')))}"


def trim(number):
    text = format(number, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"


def percent_scale(series):
    """True only when the series unit confirms the raw values are already percentages."""
    return (series.get("unit") or "").strip().lower() in PERCENT_UNITS


def format_value(value, series):
    """Render per displayFormat, falling back to the raw value plus its unit."""
    fmt = (series.get("displayFormat") or "").lower()
    unit = safe(series.get("unit"), 24)
    if fmt == "currency_abbreviated":
        sign = "-" if value < 0 else ""
        return abbreviate(abs(value), f"{sign}$")
    if fmt == "currency":
        return f"${trim(value.quantize(Decimal('0.01')))}"
    if fmt in ("abbreviated", "number_abbreviated"):
        return with_unit(abbreviate(value), unit)
    if fmt == "percent":
        text = trim(value.quantize(Decimal("0.01")))
        # A percent hint with no percent unit leaves the scale unconfirmed, so it prints as the
        # plain number it arrived as rather than gaining a % that may be a factor of 100 wrong.
        return f"{text}%" if percent_scale(series) else with_unit(text, unit, keep_currency=True)
    if fmt == "number":
        if value == value.to_integral_value():
            return with_unit(group(int(value)), unit)
        return with_unit(trim(value.quantize(Decimal("0.001"))), unit)
    # Unknown or absent hint: print the number as it arrived and name its unit, USD included.
    return with_unit(trim(value), unit, keep_currency=True)


def with_unit(text, unit, keep_currency=False):
    if not unit:
        return text
    if unit.upper() == "USD" and not keep_currency:
        return text
    return f"{text} {unit}"


def format_change(delta, series):
    """A percent-scaled series moves in percentage points, everything else in its own unit."""
    absolute, percent = delta
    sign = "+" if absolute >= 0 else ""
    if percent_scale(series):
        return f"{sign}{trim(absolute.quantize(Decimal('0.01')))} pp"
    body = format_value(absolute, series)
    if absolute >= 0 and not body.startswith("+"):
        body = "+" + body
    if percent is None:
        return f"{body} (not meaningful)"
    return f"{body} ({sign}{trim(percent.quantize(Decimal('0.01')))}%)"


# --- series analysis ---------------------------------------------------------------------

def analyse(series, today=None):
    """One series reduced to the numbers the card needs, with reasons for what is missing.

    `today` is an ISO date; it defaults to the local date and is injectable for tests."""
    raw_points, skipped, nonfinite = clean_points(series)
    points, dupes, conflicts, conflict_labels, collapsed = resolve_duplicates(raw_points)
    result = {
        "unreadablePoints": skipped,
        "nonFiniteValues": nonfinite,
        "id": safe(series.get("id"), 60),
        "name": safe(series.get("name"), 80),
        "category": safe(series.get("category"), 40),
        "unit": safe(series.get("unit"), 24),
        "displayFormat": safe(series.get("displayFormat"), 40),
        "chartType": safe(series.get("chartType"), 20),
        "sourceRef": safe(series.get("sourceRef"), 400),
        "discontinued": bool(series.get("discontinued")),
        "discontinuedNote": safe(series.get("discontinuedNote"), 400),
        "duplicatePeriods": dupes,
        "conflictingPeriods": conflict_labels,
        "collapsedDuplicates": collapsed,
        "points": len(points),
        "rows": [],
        "acceleration": None,
        "accelerationEstimate": False,
        "accelerationPeriods": [],
        "accelerationReason": "fewer than two comparable sequential changes",
        "accelerationBasis": None,
        "newestDate": None,
        "daysSinceNewest": None,
        "behind": False,
    }
    if not points:
        result["accelerationReason"] = "no usable observations"
        return result

    for index in range(len(points) - 1, -1, -1):
        point = points[index]
        qoq, qoq_reason = find_comparison(points, index, QUARTER_DAYS, 1, conflicts)
        yoy, yoy_reason = find_comparison(points, index, YEAR_DAYS, 4, conflicts)
        row = {
            "period": point["period"],
            "date": point["date"],
            "value": point["value"],
            "isEstimate": point["isEstimate"],
            "qoq": change(point["value"], qoq["value"]) if qoq else None,
            "qoqAgainst": qoq["period"] if qoq else None,
            "qoqReason": qoq_reason,
            "qoqEstimate": bool(qoq and qoq["isEstimate"]),
            "yoy": change(point["value"], yoy["value"]) if yoy else None,
            "yoyAgainst": yoy["period"] if yoy else None,
            "yoyReason": yoy_reason,
            "yoyEstimate": bool(yoy and yoy["isEstimate"]),
        }
        result["rows"].append(row)

    rows = result["rows"]

    # A quarterly series whose newest close is long past is behind, not current. lastUpdated
    # cannot say this: it records when curation last touched the file, not what it contains.
    # Cadence is read from the whole history, not the newest pair: real series skip quarters, so
    # one long gap at the top must not hide a quarterly series. Any quarter-length gap anywhere
    # makes it quarterly; with no usable gap (a single observation) a quarter label decides. A
    # series reported only once a year (Q4-only, or FY labels) has no quarter-length gap and is
    # never judged on a quarterly clock.
    if not today:
        from datetime import date
        today = date.today().isoformat()
    result["newestDate"] = rows[0]["date"]
    age = days_between(today, rows[0]["date"])
    result["daysSinceNewest"] = age
    gaps = [g for g in (days_between(rows[i]["date"], rows[i + 1]["date"])
                        for i in range(len(rows) - 1)) if g is not None and g > 0]
    if gaps:
        quarterly = min(gaps) <= QUARTER_DAYS[1]
    else:
        quarterly = parse_period(rows[0]["period"]) is not None
    result["behind"] = bool(
        quarterly and age is not None and age > BEHIND_DAYS and not result["discontinued"])

    # Acceleration is the change between the two most recent sequential rates, so it needs the
    # newest row, the row it measured itself against, and a meaningful base under both. On a
    # series whose values are already percentages, the sequential rate IS the pp change, so the
    # acceleration is the difference of two pp changes. A relative change of a percentage
    # ("Azure growth rose 7.5%") is not a rate anyone reads, and printing it as pp mislabels it.
    pp_series = percent_scale(series)
    if len(rows) >= 2 and rows[0]["qoq"] and rows[1]["qoq"]:
        if rows[0]["qoqAgainst"] != rows[1]["period"]:
            result["accelerationReason"] = "the two latest sequential changes are not successive"
        elif pp_series:
            result["acceleration"] = rows[0]["qoq"][0] - rows[1]["qoq"][0]
            result["accelerationBasis"] = "pp_changes"
            result["accelerationReason"] = None
        elif rows[0]["qoq"][1] is None or rows[1]["qoq"][1] is None:
            result["accelerationReason"] = "a sequential change had no meaningful percentage base"
        else:
            result["acceleration"] = rows[0]["qoq"][1] - rows[1]["qoq"][1]
            result["accelerationBasis"] = "growth_rates"
            result["accelerationReason"] = None
    elif len(rows) >= 2:
        result["accelerationReason"] = "only one sequential change is available"
    if result["acceleration"] is not None:
        # An acceleration figure is only as final as its weakest input, and one of those
        # inputs can sit below the visible rows. The flag travels with the number.
        result["accelerationPeriods"] = [p for p in (
            rows[0]["period"], rows[1]["period"], rows[1]["qoqAgainst"]) if p]
        result["accelerationEstimate"] = bool(
            rows[0]["isEstimate"] or rows[0]["qoqEstimate"]
            or rows[1]["isEstimate"] or rows[1]["qoqEstimate"])
    return result


# --- output ------------------------------------------------------------------------------

def print_card(analysis, series, rows_shown):
    flags = []
    if analysis["discontinued"]:
        flags.append("DISCONTINUED")
    if analysis["behind"]:
        flags.append("BEHIND")
    print(f"\n{analysis['name']} ({analysis['id']})"
          + (f"  [{', '.join(flags)}]" if flags else ""))
    if analysis["behind"]:
        print(f"  Behind: the newest period closed {analysis['newestDate']}, "
              f"{analysis['daysSinceNewest']} days ago, so expected quarterly observations may "
              "be missing. Present it as the latest available here, not the latest reported.")
    meta = [analysis["category"] or "uncategorized", analysis["unit"] or "unit unstated"]
    print(f"  {' | '.join(m for m in meta if m)}")
    if analysis["discontinued"] and analysis["rows"]:
        print(f"  Last reported period: {analysis['rows'][0]['period']}. "
              f"{analysis['discontinuedNote'] or 'The company stopped reporting this metric.'}")
    if analysis["conflictingPeriods"]:
        print("  Conflicting duplicate observations, so no trustworthy comparison is offered "
              "against: " + ", ".join(analysis["conflictingPeriods"]))
    elif analysis["duplicatePeriods"]:
        print("  Duplicate period labels, read this series with care: "
              + ", ".join(analysis["duplicatePeriods"]))
    if analysis["unreadablePoints"]:
        detail = (f"; {analysis['nonFiniteValues']} of them non-finite"
                  if analysis["nonFiniteValues"] else "")
        print(f"  {analysis['unreadablePoints']} observation(s) could not be read and are "
              f"excluded (missing value or unreadable date{detail}).")
    if not analysis["rows"]:
        print("  No usable observations in this series.")
        return

    print(f"  {'Period':<14}{'Close':<13}{'Value':<22}{'q/q':<34}y/y")
    for row in analysis["rows"][:rows_shown]:
        value = format_value(row["value"], series)
        if row["isEstimate"]:
            value += " *"
        qoq = format_change(row["qoq"], series) if row["qoq"] else short_reason(row["qoqReason"])
        yoy = format_change(row["yoy"], series) if row["yoy"] else short_reason(row["yoyReason"])
        if row["qoq"] and row["qoqEstimate"]:
            qoq += " (vs preliminary)"
        if row["yoy"] and row["yoyEstimate"]:
            yoy += " (vs preliminary)"
        print(f"  {row['period']:<14}{row['date']:<13}{value:<22}{qoq:<34}{yoy}")

    shown = analysis["rows"][:rows_shown]
    if any(r["isEstimate"] for r in shown):
        print("  * preliminary or estimated value")
    if any(d and d[1] is None for r in shown for d in (r["qoq"], r["yoy"])):
        print("  not meaningful: the earlier period was zero or negative, so only the "
              "absolute change is defined.")
    if analysis["acceleration"] is not None:
        direction = "+" if analysis["acceleration"] >= 0 else ""
        note = ""
        if analysis["accelerationEstimate"]:
            note = (" (built on a preliminary value in "
                    + ", ".join(analysis["accelerationPeriods"]) + ")")
        what = ("latest q/q change minus the previous q/q change, both already in pp"
                if analysis["accelerationBasis"] == "pp_changes"
                else "latest q/q rate minus the previous q/q rate")
        print(f"  Acceleration ({what}): "
              f"{direction}{trim(analysis['acceleration'].quantize(Decimal('0.01')))} "
              f"percentage points{note}")
    else:
        print(f"  Acceleration: not available, {analysis['accelerationReason']}")
    if analysis["sourceRef"]:
        print(f"  Source: {analysis['sourceRef']}")


def json_safe(value):
    """Serialize exactly. A Decimal leaves as an int or a string, never as a binary float."""
    if isinstance(value, Decimal):
        if not value.is_finite():
            return str(value)
        return int(value) if value == value.to_integral_value() else str(value)
    if isinstance(value, tuple):
        return [json_safe(v) for v in value]
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    return value


PREVIEW_NOTE = (
    "This is the free preview: company metadata with no numeric history. No series id can be "
    "resolved or rejected from it, so an id you asked for is unavailable here rather than "
    f"unknown. List this company's series names with {TYPES_HINT}, which a free key reads in "
    "full, and PRO returns the values. An empty kpis list is a tier boundary, not zero activity.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Read-only SentiSense company KPI reader.")
    parser.add_argument("ticker", help="stock ticker, for example AAPL")
    parser.add_argument("--series", help="comma-separated KPI ids to show; default is all")
    parser.add_argument("--rows", type=int, default=8, help="rows per series (default 8)")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="machine-readable output on stdout")
    parser.add_argument("--stdin", action="store_true",
                        help="read a saved KPI response from stdin instead of calling the API")
    args = parser.parse_args(argv)

    ticker = args.ticker.upper()
    if args.stdin:
        try:
            payload = load_json(sys.stdin.read())
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            sys.exit(f"could not read a JSON response from stdin: {e}")
    else:
        payload = get(f"/api/v1/stocks/{urllib.parse.quote(ticker, safe='')}/kpis")

    if isinstance(payload, dict) and payload.get("error"):
        code = safe(payload.get("error"), 40)
        if code == "ticker_is_etf":
            sys.exit(f"{ticker} is a fund, and company KPIs describe operating companies. "
                     "Fund data lives on the ETF endpoints.")
        sys.exit(f"{code}: {safe(payload.get('message'), 200)}")

    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, dict):
        shape = discovery_shape(payload)
        sys.exit("unexpected response shape: no data object on the KPI envelope"
                 + (f". {shape}; this script reads the /kpis series envelope." if shape else ""))

    kpis = data.get("kpis") or []
    company = safe(data.get("companyName"), 120)
    resolved = safe(data.get("ticker"), 20) or ticker
    preview = bool(payload.get("isPreview"))
    requested = [s.strip() for s in (args.series or "").split(",") if s.strip()] or None

    # The free preview is answered before any id is validated. A paid metric that this tier does
    # not carry is an access boundary, and calling it an unknown id would be a false rejection.
    if preview:
        if args.as_json:
            print(json.dumps({
                "ticker": resolved,
                "requestedTicker": ticker,
                "companyName": company,
                "lastUpdated": safe(data.get("lastUpdated"), 20),
                "isPreview": True,
                "previewReason": safe(payload.get("previewReason"), 60),
                "requestedSeries": requested or [],
                "seriesCount": 0,
                "series": [],
                "note": PREVIEW_NOTE,
            }, indent=2))
            return 0
        print(f"{company or resolved} ({resolved})"
              + (f", requested as {ticker}" if resolved != ticker else ""))
        print(f"KPI data last refreshed {safe(data.get('lastUpdated'), 20) or 'date not stated'}")
        if requested:
            print(f"\nRequested series: {', '.join(safe(s, 60) for s in requested)}")
        print("\n" + PREVIEW_NOTE)
        return 0

    if requested:
        available = [safe(k.get("id"), 60) for k in kpis]
        unknown = [s for s in requested if s not in available]
        if unknown:
            print(f"unknown series id(s): {', '.join(unknown)}", file=sys.stderr)
            print(f"available for {resolved}: "
                  + (", ".join(available) if available else "none in this response"),
                  file=sys.stderr)
            return 2
        kpis = [k for k in kpis if safe(k.get("id"), 60) in requested]

    analyses = [(analyse(series), series) for series in kpis]

    if args.as_json:
        print(json.dumps(json_safe({
            "ticker": resolved,
            "requestedTicker": ticker,
            "companyName": company,
            "lastUpdated": safe(data.get("lastUpdated"), 20),
            "isPreview": preview,
            "previewReason": safe(payload.get("previewReason"), 60),
            "seriesCount": len(analyses),
            "series": [a for a, _ in analyses],
        }), indent=2))
        return 0

    print(f"{company or resolved} ({resolved})"
          + (f", requested as {ticker}" if resolved != ticker else ""))
    print(f"KPI data last refreshed {safe(data.get('lastUpdated'), 20) or 'date not stated'}")
    if not analyses:
        print("\nNo KPI series in this response for this ticker.")
        return 0

    for analysis, series in analyses:
        print_card(analysis, series, args.rows)
    print("\nInformational and educational use only, not investment advice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
