"""FlyClaw - Flight information aggregation CLI tool.

Usage:
    flyclaw query --flight CA981
    flyclaw search --from PVG --to JFK --date 2026-04-01
"""

import argparse
import json
import logging
import sys
import time as _time
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

from __init__ import __version__
import config as cfg
from airport_manager import airport_manager
from route_cache import route_cache
from sources.fr24 import FR24Source
from sources.google_flights import GoogleFlightsSource
from sources.airplaneslive import AirplanesLiveSource

__version__ = __version__

logger = logging.getLogger("flyclaw")


# ---------------------------------------------------------------------------
# Field merge logic
# ---------------------------------------------------------------------------

def _normalize_flight_number(fn: str) -> str:
    """Normalize flight number by stripping leading zeros from numeric part.

    Examples: IJ004→IJ4, CA0981→CA981, 3U0088→3U88.
    Handles airline codes like "3U" (digit + letter).
    Needed because Fliggy pads numeric part with zeros while GF/SK do not.
    """
    if not fn:
        return fn
    # Airline code is 2-3 chars (may start with digit, e.g. "3U", "9C")
    # Find the boundary: last non-digit before the all-digit tail
    # Strategy: find the longest trailing digit-only suffix
    i = len(fn)
    while i > 0 and fn[i - 1].isdigit():
        i -= 1
    if i == 0 or i == len(fn):
        return fn  # All digits or no digits — can't normalize
    prefix = fn[:i]
    numeric = fn[i:]
    stripped = numeric.lstrip("0") or "0"
    return prefix + stripped


def _get_source_priority(record: dict) -> int:
    """Return the configured priority for a record's source.

    Lower number = higher priority.  Unknown sources get 999.
    """
    source = record.get("source", "")
    conf = cfg.get_config()
    sources_cfg = conf.get("sources", {})
    for name, scfg in sources_cfg.items():
        if name == source:
            return scfg.get("priority", 999)
    return 999


def _extract_date(iso_str: str | None) -> str:
    """Extract date part (YYYY-MM-DD) from ISO-8601 timestamp."""
    if not iso_str:
        return ""
    return iso_str[:10] if len(iso_str) >= 10 else ""


def _merge_records(records: list[dict], *, date_aware: bool = False) -> list[dict]:
    """Merge records from different sources for the same flight.

    Strategy: normalize flight numbers, sort by source priority (high-priority
    first), then group by flight_number and fill missing fields from
    lower-priority sources.  Records without flight_number are kept as-is.

    After standard merge, picks the **lowest price** across all sources for
    each merged flight (comparing in USD for cross-currency fairness).

    Args:
        date_aware: If True, group by flight_number + date (from
            scheduled_departure).  This preserves multi-day records
            returned by FR24 for the same flight number.
    """
    # Normalize flight numbers before merge (IJ004→IJ4, CA0981→CA981)
    for rec in records:
        fn = rec.get("flight_number")
        if fn:
            rec["flight_number"] = _normalize_flight_number(fn)

    sorted_records = sorted(records, key=_get_source_priority)

    grouped: dict[str, dict] = {}       # merge_key → merged record
    raw_groups: dict[str, list[dict]] = {}  # merge_key → all original records
    ungrouped: list[dict] = []

    for rec in sorted_records:
        fn = rec.get("flight_number", "")
        if not fn:
            ungrouped.append(rec)
            continue

        if date_aware:
            date_part = _extract_date(rec.get("scheduled_departure"))
            key = f"{fn}|{date_part}"
        else:
            key = fn

        # Keep raw records for price_priority override
        raw_groups.setdefault(key, []).append(rec)

        if key not in grouped:
            grouped[key] = rec.copy()
        else:
            # Fill-in: existing non-empty values take priority
            existing = grouped[key]
            for k, val in rec.items():
                if k == "source":
                    # Combine unique sources
                    sources = set(existing.get("source", "").split(","))
                    sources.add(val)
                    sources.discard("")
                    existing["source"] = ",".join(sorted(sources))
                elif not existing.get(k) and val:
                    existing[k] = val

    result = list(grouped.values()) + ungrouped

    # --- Lowest price selection ---
    # When multiple sources provide prices for the same flight, pick the
    # lowest price (comparing in USD for cross-currency fairness).
    # The original currency + price of the cheapest source is kept.
    conf = cfg.get_config()
    rate = conf.get("output", {}).get("exchange_rate_cny_usd", 7.25)

    for merged_rec in result:
        fn = merged_rec.get("flight_number", "")
        if not fn:
            continue
        if date_aware:
            dep = merged_rec.get("scheduled_departure", "")
            date_part = dep[:10] if dep and len(dep) >= 10 else ""
            group_key = f"{fn}|{date_part}"
        else:
            group_key = fn
        raw = raw_groups.get(group_key, [])
        if len(raw) <= 1:
            continue  # No merge happened, nothing to override

        # Find the lowest price across all sources (compare in USD)
        best_price_usd = None
        best_record = None
        for r in raw:
            p = r.get("price")
            if p is None or p == 0:
                continue
            cur = r.get("currency", "USD").upper()
            price_usd = p / rate if cur == "CNY" else p
            if best_price_usd is None or price_usd < best_price_usd:
                best_price_usd = price_usd
                best_record = r

        # Write lowest price (keep original currency of cheapest source)
        merged_rec.pop("price", None)
        merged_rec.pop("currency", None)
        if best_record:
            merged_rec["price"] = best_record["price"]
            merged_rec["currency"] = best_record.get("currency", "USD")

    # Sort by date descending when date_aware (most recent first)
    if date_aware:
        result.sort(
            key=lambda r: _extract_date(r.get("scheduled_departure")),
            reverse=True,
        )

    return result


def _deduplicate_codeshares(records: list[dict]) -> list[dict]:
    """Detect and remove codeshare duplicates, keeping operating carrier.

    Flights with identical (dep_time, arr_time, origin, dest, stops) are
    treated as codeshare variants of the same physical flight.
    """
    if not records:
        return records

    groups: dict[tuple, list[dict]] = {}
    ungrouped: list[dict] = []

    for rec in records:
        dep = rec.get("scheduled_departure", "")
        arr = rec.get("scheduled_arrival", "")
        orig = rec.get("origin_iata", "")
        dest = rec.get("destination_iata", "")
        stops = rec.get("stops")
        if dep and arr and orig and dest:
            key = (dep, arr, orig, dest, stops)
            groups.setdefault(key, []).append(rec)
        else:
            ungrouped.append(rec)

    result = []
    for group in groups.values():
        if len(group) == 1:
            result.append(group[0])
        else:
            main = _pick_main_flight(group)
            result.append(main)
    return result + ungrouped


def _pick_main_flight(group: list[dict]) -> dict:
    """Pick operating carrier from codeshare group, merge fields."""
    scored = []
    for rec in group:
        score = sum(1 for v in rec.values() if v is not None and v != "")
        if rec.get("price") is not None:
            score += 5
        scored.append((score, rec))
    scored.sort(key=lambda x: x[0], reverse=True)
    main = scored[0][1].copy()

    alt_fns = [r["flight_number"] for _, r in scored[1:]
               if r.get("flight_number") and r["flight_number"] != main.get("flight_number")]
    if alt_fns:
        main["codeshare_variants"] = alt_fns

    for _, rec in scored[1:]:
        for k, v in rec.items():
            if k in ("flight_number", "source", "codeshare_variants"):
                continue
            if not main.get(k) and v:
                main[k] = v
    return main


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _apply_currency_conversion(records: list[dict], args, conf: dict) -> None:
    """Apply currency conversion in-place based on --currency arg / config.

    Ensures every priced record has a ``currency`` field, then converts
    CNY↔USD when the target currency is not ``original``.
    """
    # Ensure currency field exists on all priced records
    for r in records:
        if r.get("price") is not None:
            r.setdefault("currency", "USD")

    out_currency = (
        getattr(args, "currency", None)
        or conf.get("output", {}).get("currency", "original")
    )
    if out_currency not in ("usd", "cny"):
        return  # "original" — keep each source's native currency

    rate = conf.get("output", {}).get("exchange_rate_cny_usd", 7.25)
    if rate <= 0:
        return

    for r in records:
        if r.get("price") is None:
            continue
        cur = r.get("currency", "USD").upper()
        if out_currency == "usd" and cur == "CNY":
            r["price"] = round(r["price"] / rate, 2)
            r["currency"] = "USD"
        elif out_currency == "cny" and cur == "USD":
            r["price"] = round(r["price"] * rate, 2)
            r["currency"] = "CNY"


def _format_table(records: list[dict], verbose: bool = False) -> str:
    """Format records as a human-readable table."""
    if not records:
        return "No flights found."

    lines = []
    sep = "-" * 90

    for i, rec in enumerate(records):
        if i > 0:
            lines.append(sep)

        fn = rec.get("flight_number", "N/A")
        airline = rec.get("airline", "") or ""
        status = rec.get("status", "") or ""
        origin = rec.get("origin_city", rec.get("origin_iata", ""))
        dest = rec.get("destination_city", rec.get("destination_iata", ""))
        dep = _format_time(rec.get("scheduled_departure"))
        arr = _format_time(rec.get("scheduled_arrival"))
        aircraft = rec.get("aircraft_type", "") or ""
        price = rec.get("price")
        delay = rec.get("delay_minutes")
        source = rec.get("source", "")
        stops = rec.get("stops")

        header = f"  {fn}"
        codeshare_alts = rec.get("codeshare_variants", [])
        if codeshare_alts:
            header += f"  (+{len(codeshare_alts)} codeshare)"
        if airline:
            header += f"  ({airline})"
        if status:
            header += f"  [{status}]"
        lines.append(header)

        lines.append(f"  {origin} → {dest}")
        lines.append(f"  Departure: {dep}    Arrival: {arr}")

        extras = []
        if aircraft:
            extras.append(f"Aircraft: {aircraft}")
        trip_type = rec.get("trip_type", "")
        price_label = "(round-trip)" if trip_type == "round_trip" else ""
        if price is not None:
            extras.append(f"Price: ${price} {price_label}".strip())
        if stops is not None:
            extras.append(f"Stops: {stops}")
        duration = rec.get("duration_minutes")
        if duration is not None:
            extras.append(f"Duration: {duration}min")
        if delay is not None:
            extras.append(f"Delay: {delay}min")
        altitude = rec.get("altitude_ft")
        speed = rec.get("ground_speed_kts")
        if altitude is not None:
            extras.append(f"Alt: {altitude}ft")
        if speed is not None:
            extras.append(f"Speed: {speed}kts")
        if extras:
            lines.append(f"  {' | '.join(extras)}")

        # Round-trip return flight block
        if trip_type == "round_trip":
            ret_fn = rec.get("return_flight_number", "")
            ret_airline = rec.get("return_airline", "")
            ret_dep = _format_time(rec.get("return_departure"))
            ret_arr = _format_time(rec.get("return_arrival"))
            ret_stops = rec.get("return_stops")
            ret_dur = rec.get("return_duration_minutes")

            lines.append("  ── Return ──")
            ret_header = f"  {ret_fn}" if ret_fn else "  N/A"
            if ret_airline:
                ret_header += f"  ({ret_airline})"
            lines.append(ret_header)
            lines.append(f"  Departure: {ret_dep}    Arrival: {ret_arr}")
            ret_extras = []
            if ret_stops is not None:
                ret_extras.append(f"Stops: {ret_stops}")
            if ret_dur is not None:
                ret_extras.append(f"Duration: {ret_dur}min")
            if ret_extras:
                lines.append(f"  {' | '.join(ret_extras)}")

        if verbose:
            cabin_class = rec.get("cabin_class", "")
            if cabin_class:
                lines.append(f"  Cabin: {cabin_class}")
            lines.append(f"  Source: {source}")

    return "\n".join(lines)


def _format_time(iso_str: str | None) -> str:
    """Format ISO timestamp to readable form."""
    if not iso_str:
        return "--"
    # Show date + time portion
    return iso_str.replace("T", " ")[:19]


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_update_airports(args):
    """Handle 'update-airports' subcommand: manually update airport data."""
    conf = cfg.get_config()
    cache_cfg = conf["cache"]

    # URL priority: CLI --url > config.yaml > AIRPORT_UPDATE_URL constant
    url = getattr(args, "url", None) or cache_cfg.get("airport_update_url", "") or cfg.AIRPORT_UPDATE_URL
    if not url:
        print("Error: no update URL provided. Use --url or set airport_update_url in config.yaml",
              file=sys.stderr)
        sys.exit(1)

    print(f"Updating airport data from: {url}")
    ok = airport_manager.update_from_url(url)
    if ok:
        print("Airport data updated successfully.")
    else:
        print("Airport data update failed. See log for details.", file=sys.stderr)
        sys.exit(1)


def _auto_update_airports():
    """Check and auto-update airport data at startup (silent on failure)."""
    try:
        conf = cfg.get_config()
        cache_cfg = conf["cache"]
        update_days = cache_cfg.get("airport_update_days", 30)
        url = cache_cfg.get("airport_update_url", "") or cfg.AIRPORT_UPDATE_URL

        if not url or update_days <= 0:
            return

        if airport_manager.check_staleness(update_days):
            logger.info("Airport data is stale, auto-updating...")
            airport_manager.update_from_url(url)
    except Exception as e:
        logger.debug("Auto-update check skipped: %s", e)


# ---------------------------------------------------------------------------
# Concurrent query infrastructure
# ---------------------------------------------------------------------------

def _query_fr24_flight(flight_number: str, timeout: int) -> list[dict]:
    """Wrapper: query FR24 by flight number."""
    src = FR24Source(timeout=timeout)
    return src.query_by_flight(flight_number)


def _query_fr24_route(origin: str, dest: str, date: str | None, timeout: int) -> list[dict]:
    """Wrapper: query FR24 by route."""
    src = FR24Source(timeout=timeout)
    return src.query_by_route(origin, dest, date)


def _query_gf_route(
    origin: str | list[str], dest: str | list[str], date: str,
    timeout: int, serpapi_key: str,
    *, return_date: str | None = None, adults: int = 1,
    children: int = 0, infants: int = 0,
    cabin: str = "economy", stops: int | str = 0,
    sort: str | None = None, limit: int | None = None,
    retry: int = 3,
    retry_delay: float = 0.5, retry_backoff: float = 2.0,
) -> list[dict]:
    """Wrapper: query Google Flights by route.

    origin/dest can be str or list[str] for multi-airport city searches.
    """
    src = GoogleFlightsSource(timeout=timeout, serpapi_key=serpapi_key,
                              retry=retry,
                              retry_delay=retry_delay,
                              retry_backoff=retry_backoff)
    return src.query_by_route(
        origin, dest, date,
        return_date=return_date, adults=adults, children=children,
        infants=infants, cabin=cabin, stops=stops,
        sort=sort, limit=limit,
    )


def _query_gf_flight(flight_number: str, timeout: int, serpapi_key: str) -> list[dict]:
    """Wrapper: query Google Flights by flight number (via route cache)."""
    src = GoogleFlightsSource(timeout=timeout, serpapi_key=serpapi_key)
    return src.query_by_flight(flight_number)


def _query_al_flight(flight_number: str, timeout: int) -> list[dict]:
    """Wrapper: query Airplanes.live by flight number."""
    src = AirplanesLiveSource(timeout=timeout)
    return src.query_by_flight(flight_number)


def _query_fliggy_route(
    origin_name: str, dest_name: str, date: str, timeout: int,
    *, cabin: str = "economy", stops: int | str = 0,
    limit: int | None = None, return_date: str | None = None,
    api_key: str = "", sign_secret: str = "",
) -> list[dict]:
    """Wrapper: query Fliggy MCP by route (ThreadPoolExecutor compatible)."""
    from sources.fliggy_mcp import FliggyMCPSource
    src = FliggyMCPSource(
        timeout=timeout,
        api_key=api_key or None,
        sign_secret=sign_secret or None,
    )
    return src.query_by_route(
        origin_name, dest_name, date,
        cabin=cabin, stops=stops, limit=limit,
        return_date=return_date, timeout=timeout,
    )


def _query_sk_route(origin: str, dest: str, date: str, timeout: int,
                    *, stops: int | str = 0, limit: int | None = None,
                    retry: int = 3, cabin: str = "economy",
                    mcp_enabled: bool = False, mcp_url: str = "",
                    return_date: str | None = None,
                    retry_delay: float = 0.5,
                    retry_backoff: float = 2.0) -> list[dict]:
    """Wrapper: query Skiplagged by route (ThreadPoolExecutor compatible)."""
    from sources.skiplagged import SkiplaggedSource
    src = SkiplaggedSource(timeout=timeout, retry=retry,
                           mcp_enabled=mcp_enabled, mcp_url=mcp_url,
                           retry_delay=retry_delay,
                           retry_backoff=retry_backoff)
    return src.query_by_route(origin, dest, date, stops=stops, limit=limit,
                              cabin=cabin, return_date=return_date)


def _query_sk_route_multi(
    origins: list[str], dests: list[str], date: str, timeout: int,
    *, stops: int | str = 0, limit: int | None = None,
    retry: int = 3, cabin: str = "economy",
    mcp_enabled: bool = False, mcp_url: str = "",
    retry_delay: float = 0.5, retry_backoff: float = 2.0,
) -> list[dict]:
    """Query Skiplagged for all origin x dest combinations.

    SK API accepts single IATA codes only.  For city-level searches
    (e.g. Shanghai = PVG + SHA) we iterate all origin x dest pairs,
    deduplicate by flight_number, and return the cheapest results.

    Uses concurrent queries (max 2 workers) when multiple pairs exist.
    Research (v0.2.3 Step 1) confirmed SK has no rate limiting at 2s intervals.
    """
    from sources.skiplagged import SkiplaggedSource
    src = SkiplaggedSource(timeout=timeout, retry=retry,
                           mcp_enabled=mcp_enabled, mcp_url=mcp_url,
                           retry_delay=retry_delay,
                           retry_backoff=retry_backoff)
    pairs = [(o, d) for o in origins for d in dests]

    if len(pairs) <= 1:
        # Single pair — no concurrency needed
        all_results: list[dict] = []
        for o, d in pairs:
            try:
                recs = src.query_by_route(o, d, date, stops=stops, limit=limit,
                                          cabin=cabin)
                all_results.extend(recs)
            except Exception as e:
                logger.warning("Skiplagged %s→%s failed: %s", o, d, e)
        return all_results[:limit] if limit is not None else all_results

    # Multiple pairs — concurrent with max 2 workers
    def _fetch_pair(pair):
        o, d = pair
        try:
            return src.query_by_route(o, d, date, stops=stops, limit=limit,
                                      cabin=cabin)
        except Exception as e:
            logger.warning("Skiplagged %s→%s failed: %s", o, d, e)
            return []

    all_results = []
    seen: set[str] = set()
    with ThreadPoolExecutor(max_workers=min(2, len(pairs))) as executor:
        futures = {executor.submit(_fetch_pair, p): p for p in pairs}
        for future in futures:
            try:
                recs = future.result(timeout=timeout + 5)
                for r in recs:
                    fn = r.get("flight_number", "")
                    if fn and fn not in seen:
                        seen.add(fn)
                        all_results.append(r)
                    elif not fn:
                        all_results.append(r)
            except Exception as e:
                p = futures[future]
                logger.warning("Skiplagged %s→%s future failed: %s",
                               p[0], p[1], e)
    all_results.sort(key=lambda r: r.get("price") or float("inf"))
    return all_results[:limit] if limit is not None else all_results


def _iata_to_city_cn(iata: str) -> str:
    """Return Chinese city name for an IATA code, fallback to the code itself.

    Fliggy API accepts both IATA codes and Chinese city names, and handles
    city-level search natively (e.g. "上海" covers both PVG and SHA).
    """
    info = airport_manager.get_info(iata)
    if info:
        return info.get("city_cn") or info.get("city_en") or iata
    return iata


def _execute_concurrent_queries(
    tasks: list[tuple],
    global_timeout: int,
    return_time: int | None = None,
    sufficient_sources: list[str] | None = None,
) -> list[dict]:
    """Execute query tasks concurrently and collect results.

    Args:
        tasks: list of (name, callable, args_tuple) triples
        global_timeout: max seconds to wait for all tasks
        return_time: if set, return early once this many seconds have
            elapsed AND at least one result is available.  ``None`` or
            0 disables smart-return (wait for all / global timeout).
        sufficient_sources: if set, exit immediately when a task whose
            name matches any entry returns results with prices.  This
            enables "fast return" when a reliable source (e.g. Fliggy)
            responds quickly with priced data.

    Returns:
        Combined list of result dicts from all successful tasks.
        Partial results returned if global timeout or return_time expires.
    """
    if not tasks:
        return []

    results = []
    start = _time.monotonic()
    executor = ThreadPoolExecutor(max_workers=len(tasks))

    future_to_name = {}
    for name, fn, args in tasks:
        future = executor.submit(fn, *args)
        future_to_name[future] = name

    pending = set(future_to_name.keys())
    early_exit = False
    while pending:
        elapsed = _time.monotonic() - start
        remaining = global_timeout - elapsed
        if remaining <= 0:
            logger.warning(
                "Global timeout (%ds) reached, returning partial results",
                global_timeout,
            )
            early_exit = True
            break

        # If smart return is enabled and we already have results,
        # use a short wait so we can exit at the return_time boundary.
        wait_timeout = remaining
        if return_time and results:
            time_to_return = max(0, return_time - elapsed)
            wait_timeout = min(remaining, time_to_return) if time_to_return > 0 else 0

        if wait_timeout <= 0 and return_time and results:
            logger.info(
                "Smart return at %.1fs with %d results (%d sources pending)",
                elapsed, len(results), len(pending),
            )
            early_exit = True
            break

        done, pending = wait(pending, timeout=wait_timeout, return_when=FIRST_COMPLETED)

        for future in done:
            name = future_to_name[future]
            try:
                data = future.result()
                results.extend(data)
                logger.info("%s: %d results", name, len(data))

                # Sufficient source: exit immediately if a trusted source
                # returned priced results (no need to wait for others)
                if sufficient_sources and data and not early_exit:
                    name_lower = name.lower()
                    for ss in sufficient_sources:
                        # Match: config "fliggy_mcp" matches task "Fliggy"
                        ss_key = ss.lower().replace("_", "")
                        if ss_key in name_lower.replace("_", "") or name_lower in ss_key:
                            has_price = any(
                                r.get("price") is not None for r in data
                            )
                            if has_price:
                                logger.info(
                                    "Sufficient source '%s': %d results with "
                                    "prices, skipping remaining sources",
                                    name, len(data),
                                )
                                early_exit = True
                                break
            except Exception as e:
                logger.warning("%s query failed: %s", name, e)

        if early_exit:
            break

        # Smart return: if return_time reached and we have results
        if (
            return_time
            and results
            and pending
            and (_time.monotonic() - start) >= return_time
        ):
            logger.info(
                "Smart return at %.1fs with %d results (%d sources pending)",
                _time.monotonic() - start, len(results), len(pending),
            )
            early_exit = True
            break

    if early_exit:
        executor.shutdown(wait=False, cancel_futures=True)
    else:
        executor.shutdown(wait=False)

    return results


# ---------------------------------------------------------------------------
# Error / degradation warnings
# ---------------------------------------------------------------------------

def _classify_source_failures(task_names: list[str], results: list[dict]) -> dict:
    """Classify source failures for user-facing warnings.

    Args:
        task_names: list of task names submitted (e.g. ["FR24", "GoogleFlights", "Skiplagged"])
        results: combined results from all tasks

    Returns:
        {"google_failed": bool, "sk_failed": bool, "all_failed": bool}
    """
    has_google_task = any("google" in n.lower() for n in task_names)
    has_google_result = any(
        "google" in r.get("source", "").lower() for r in results
    )
    google_failed = has_google_task and not has_google_result

    has_sk_task = any("skiplagged" in n.lower() for n in task_names)
    has_sk_result = any(
        "skiplagged" in r.get("source", "").lower() for r in results
    )
    sk_failed = has_sk_task and not has_sk_result

    has_fliggy_task = any("fliggy" in n.lower() for n in task_names)
    has_fliggy_result = any(
        "fliggy" in r.get("source", "").lower() for r in results
    )
    fliggy_failed = has_fliggy_task and not has_fliggy_result

    all_failed = len(results) == 0 and len(task_names) > 0

    return {
        "google_failed": google_failed,
        "sk_failed": sk_failed,
        "fliggy_failed": fliggy_failed,
        "all_failed": all_failed,
    }


def _print_degradation_warnings(failures: dict) -> None:
    """Print user-friendly warnings to stderr based on failure classification."""
    if failures.get("all_failed"):
        print(
            "[Error] 请检查网络连接 / Please check your network connection",
            file=sys.stderr,
        )
    elif failures.get("google_failed"):
        print(
            "[Note] Google 相关服务在您所在地区可能不可用或网络不佳",
            file=sys.stderr,
        )
    if failures.get("sk_failed"):
        print(
            "[Note] Skiplagged 数据源暂时不可用 / Skiplagged source temporarily unavailable",
            file=sys.stderr,
        )
    if failures.get("fliggy_failed"):
        print(
            "[Note] 飞猪数据源暂时不可用 / Fliggy source temporarily unavailable",
            file=sys.stderr,
        )


# ---------------------------------------------------------------------------
# Route relay helpers
# ---------------------------------------------------------------------------

def _extract_relay_route(results: list[dict], flight_number: str) -> dict | None:
    """Extract origin/destination from Phase 1 results for relay query.

    Returns {"origin": "PVG", "destination": "JFK"} or None if route
    cannot be determined.
    """
    fn_upper = flight_number.strip().upper()
    for r in results:
        if r.get("flight_number", "").upper() == fn_upper:
            o = r.get("origin_iata", "")
            d = r.get("destination_iata", "")
            if o and d:
                return {"origin": o, "destination": d}

    # Fallback: any record with both origin and destination
    for r in results:
        o = r.get("origin_iata", "")
        d = r.get("destination_iata", "")
        if o and d:
            return {"origin": o, "destination": d}

    return None


def _extract_relay_date(results: list[dict], user_date: str | None) -> str:
    """Determine the best date for relay price queries.

    Priority:
    1. User-specified --date (if provided and not 'today')
    2. Nearest future scheduled_departure from Phase 1 results
    3. Today as fallback
    """
    from datetime import date as date_type, datetime
    today = date_type.today().isoformat()

    # 1. User explicitly specified a date
    if user_date and user_date != "today":
        return user_date
    if user_date == "today":
        return today

    # 2. Find nearest future departure from results
    best_date = None
    for r in results:
        dep = r.get("scheduled_departure", "")
        if dep and len(dep) >= 10:
            d = dep[:10]
            if d >= today:
                if best_date is None or d < best_date:
                    best_date = d
    if best_date:
        return best_date

    # 3. Fallback
    return today


def _has_price(results: list[dict]) -> bool:
    """Check if any result has price data."""
    return any(r.get("price") is not None for r in results)


# ---------------------------------------------------------------------------
# CLI commands (query / search)
# ---------------------------------------------------------------------------

def cmd_query(args):
    """Handle 'query' subcommand: query by flight number.

    Implements two-phase route relay:
    Phase 1: FR24 + Airplanes.live + GoogleFlights(cache) — all concurrent
    Phase 2: If relay ON + route discovered + no price → query Google Flights
             with the discovered route to get price data.
    """
    if getattr(args, "date", None) and args.date != "today":
        import re
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", args.date):
            print(f"Error: invalid date format '{args.date}', expected YYYY-MM-DD",
                  file=sys.stderr)
            sys.exit(1)

    conf = cfg.get_config()
    sources_cfg = conf["sources"]
    query_cfg = conf["query"]

    # Relay config
    relay_enabled = query_cfg.get("route_relay", True)
    if getattr(args, "no_relay", False):
        relay_enabled = False
    relay_timeout = query_cfg.get("relay_timeout", 8)

    base_timeout = getattr(args, "timeout", None) or query_cfg["timeout"]
    return_time = getattr(args, "return_time", None)
    if return_time is None:
        return_time = query_cfg.get("return_time")

    # Phase 1: concurrent query all sources
    tasks = []

    if sources_cfg["fr24"]["enabled"]:
        timeout = sources_cfg["fr24"]["timeout"]
        tasks.append(("FR24", _query_fr24_flight, (args.flight, timeout)))

    if sources_cfg["google_flights"]["enabled"]:
        timeout = sources_cfg["google_flights"]["timeout"]
        serpapi_key = sources_cfg["google_flights"].get("serpapi_key", "")
        tasks.append(("GoogleFlights", _query_gf_flight, (args.flight, timeout, serpapi_key)))

    if sources_cfg["airplanes_live"]["enabled"]:
        timeout = sources_cfg["airplanes_live"]["timeout"]
        tasks.append(("AirplanesLive", _query_al_flight, (args.flight, timeout)))

    task_names = [t[0] for t in tasks]
    phase1_start = _time.monotonic()
    results = _execute_concurrent_queries(tasks, base_timeout, return_time)
    phase1_elapsed = _time.monotonic() - phase1_start

    # Update route cache from Phase 1 results
    route_cache.update_from_records(results)
    route_cache.save()

    # Phase 2: Route relay (multi-engine: GF + SK)
    if relay_enabled and results and not _has_price(results):
        route = _extract_relay_route(results, args.flight)
        if route:
            remaining = relay_timeout
            relay_date = _extract_relay_date(
                results, getattr(args, "date", None)
            )
            relay_cfg = query_cfg.get(
                "relay_engines", {"google_flights": True, "skiplagged": True}
            )
            relay_tasks = []
            if (relay_cfg.get("google_flights", True)
                    and sources_cfg["google_flights"]["enabled"]):
                gf_timeout = sources_cfg["google_flights"]["timeout"]
                serpapi_key = sources_cfg["google_flights"].get("serpapi_key", "")
                relay_tasks.append((
                    "GoogleFlights-Relay", _query_gf_route,
                    (route["origin"], route["destination"], relay_date,
                     gf_timeout, serpapi_key),
                ))
            if (relay_cfg.get("skiplagged", True)
                    and sources_cfg.get("skiplagged", {}).get("enabled", False)):
                sk_cfg = sources_cfg["skiplagged"]
                sk_timeout = sk_cfg["timeout"]
                import functools
                sk_relay = functools.partial(
                    _query_sk_route,
                    route["origin"], route["destination"], relay_date, sk_timeout,
                    retry=sk_cfg.get("retry", 3),
                    retry_delay=sk_cfg.get("retry_delay", 0.5),
                    retry_backoff=sk_cfg.get("retry_backoff", 2.0),
                    mcp_enabled=sk_cfg.get("mcp_enabled", False),
                    mcp_url=sk_cfg.get("mcp_url", ""),
                )
                relay_tasks.append((
                    "Skiplagged-Relay", lambda: sk_relay(), (),
                ))
            if relay_tasks and remaining > 2:
                logger.info(
                    "Route relay: %d engine(s) for %s→%s date=%s (%.1fs remaining)",
                    len(relay_tasks), route["origin"],
                    route["destination"], relay_date, remaining,
                )
                task_names.extend(t[0] for t in relay_tasks)
                relay_results = _execute_concurrent_queries(
                    relay_tasks, int(remaining), return_time=1
                )
                results.extend(relay_results)

    # Degradation warnings
    failures = _classify_source_failures(task_names, results)
    _print_degradation_warnings(failures)

    merged = _merge_records(results, date_aware=True)

    if not getattr(args, "show_codeshare", False):
        merged = _deduplicate_codeshares(merged)

    if getattr(args, "date", None):
        filter_date = args.date
        if filter_date == "today":
            from datetime import date as date_type
            filter_date = date_type.today().isoformat()
        merged = [r for r in merged
                  if _extract_date(r.get("scheduled_departure")) == filter_date]

    _apply_currency_conversion(merged, args, conf)

    if args.output == "json":
        print(json.dumps(merged, indent=2, ensure_ascii=False, default=str))
    else:
        print(_format_table(merged, verbose=args.verbose))


def _validate_search_args(args):
    """Validate search arguments, print error and exit on failure."""
    import re
    date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    if args.return_date and not args.date:
        print("Error: --return requires --date", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "compare", False) and not args.date:
        print("Error: --compare requires --date", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "browser", False) and not getattr(args, "compare", False):
        print("Error: --browser requires --compare", file=sys.stderr)
        sys.exit(1)

    if args.date and not date_re.match(args.date):
        print(f"Error: invalid date format '{args.date}', expected YYYY-MM-DD",
              file=sys.stderr)
        sys.exit(1)

    if args.return_date:
        if not date_re.match(args.return_date):
            print(f"Error: invalid return date format '{args.return_date}', expected YYYY-MM-DD",
                  file=sys.stderr)
            sys.exit(1)
        if args.return_date < args.date:
            print("Error: return date must be on or after departure date",
                  file=sys.stderr)
            sys.exit(1)

    if args.adults < 1:
        print("Error: --adults must be at least 1", file=sys.stderr)
        sys.exit(1)

    if args.limit is not None and args.limit < 1:
        print("Error: --limit must be at least 1", file=sys.stderr)
        sys.exit(1)


def cmd_search(args):
    """Handle 'search' subcommand: search by route."""
    _validate_search_args(args)

    # Resolve airport codes from user input (city-level: may return multiple)
    conf = cfg.get_config()
    filter_inactive = conf["query"].get("filter_inactive_airports", True)
    origins = airport_manager.resolve_all(args.from_station,
                                          filter_inactive=filter_inactive)
    dests = airport_manager.resolve_all(args.to_station,
                                        filter_inactive=filter_inactive)

    if not origins:
        print(f"Error: cannot resolve origin '{args.from_station}'", file=sys.stderr)
        sys.exit(1)
    if not dests:
        print(f"Error: cannot resolve destination '{args.to_station}'", file=sys.stderr)
        sys.exit(1)

    origin_str = ",".join(origins)
    dest_str = ",".join(dests)
    if len(origins) > 1 or len(dests) > 1:
        logger.info("City-level search: %s → %s", origin_str, dest_str)
    else:
        logger.info("Resolved: %s → %s", origin_str, dest_str)

    sources_cfg = conf["sources"]
    global_timeout = getattr(args, "timeout", None) or conf["query"]["timeout"]
    return_time = getattr(args, "return_time", None)
    if return_time is None:
        return_time = conf["query"].get("return_time")

    # Limit: only truncate when user specifies --limit
    stops_val = int(args.stops) if args.stops != "any" else "any"
    effective_limit = args.limit  # None if user didn't specify

    # Keyword arguments for Google Flights advanced search
    gf_cfg = sources_cfg["google_flights"]
    gf_kw = dict(
        return_date=args.return_date, adults=args.adults,
        children=args.children, infants=args.infants,
        cabin=args.cabin, stops=stops_val,
        sort=args.sort, limit=effective_limit,
        retry=gf_cfg.get("retry", 3),
        retry_delay=gf_cfg.get("retry_delay", 0.5),
        retry_backoff=gf_cfg.get("retry_backoff", 2.0),
    )

    # For multi-airport: pass list to Google Flights, single to FR24
    gf_origin = origins if len(origins) > 1 else origins[0]
    gf_dest = dests if len(dests) > 1 else dests[0]

    # SK config
    sk_cfg = sources_cfg.get("skiplagged", {})

    tasks = []

    # FR24 (single airport only — use primary)
    if sources_cfg["fr24"]["enabled"]:
        timeout = sources_cfg["fr24"]["timeout"]
        tasks.append(("FR24", _query_fr24_route, (origins[0], dests[0], args.date, timeout)))

    # Google Flights (supports multi-airport)
    if sources_cfg["google_flights"]["enabled"] and args.date:
        timeout = sources_cfg["google_flights"]["timeout"]
        serpapi_key = sources_cfg["google_flights"].get("serpapi_key", "")
        import functools
        gf_task = functools.partial(
            _query_gf_route, gf_origin, gf_dest, args.date, timeout, serpapi_key,
            **gf_kw,
        )
        tasks.append(("GoogleFlights", lambda: gf_task(), ()))

    # Skiplagged (price complement — each airport pair as independent future)
    if sk_cfg.get("enabled", False) and args.date:
        sk_timeout = sk_cfg["timeout"]
        sk_kw = dict(
            stops=stops_val, limit=effective_limit,
            retry=sk_cfg.get("retry", 3),
            retry_delay=sk_cfg.get("retry_delay", 0.5),
            retry_backoff=sk_cfg.get("retry_backoff", 2.0),
            cabin=args.cabin,
            return_date=args.return_date,
            mcp_enabled=sk_cfg.get("mcp_enabled", False),
            mcp_url=sk_cfg.get("mcp_url", ""),
        )
        import functools
        for o in origins:
            for d in dests:
                pair_task = functools.partial(
                    _query_sk_route, o, d, args.date, sk_timeout, **sk_kw,
                )
                label = f"Skiplagged-{o}\u2192{d}" if len(origins) * len(dests) > 1 else "Skiplagged"
                tasks.append((label, lambda t=pair_task: t(), ()))

    # Fliggy MCP (city-level: one request covers all airports)
    fg_cfg = sources_cfg.get("fliggy_mcp", {})
    if fg_cfg.get("enabled", False) and args.date:
        import functools
        fg_origin = _iata_to_city_cn(origins[0])
        fg_dest = _iata_to_city_cn(dests[0])
        fg_timeout = fg_cfg.get("timeout", 10)
        fg_task = functools.partial(
            _query_fliggy_route,
            fg_origin, fg_dest, args.date, fg_timeout,
            cabin=args.cabin, stops=stops_val,
            limit=effective_limit, return_date=args.return_date,
            api_key=fg_cfg.get("api_key", ""),
            sign_secret=fg_cfg.get("sign_secret", ""),
        )
        tasks.append(("Fliggy", lambda t=fg_task: t(), ()))

    task_names = [t[0] for t in tasks]
    ss_cfg = conf["query"].get("sufficient_source", "")
    sufficient = [ss_cfg] if ss_cfg else None
    results = _execute_concurrent_queries(
        tasks, global_timeout, return_time,
        sufficient_sources=sufficient,
    )

    # Degradation warnings
    failures = _classify_source_failures(task_names, results)
    _print_degradation_warnings(failures)

    # Update route cache from results
    route_cache.update_from_records(results)
    route_cache.save()

    merged = _merge_records(results)

    if not getattr(args, "show_codeshare", False):
        merged = _deduplicate_codeshares(merged)

    # When searching with stops (not nonstop-only) and no explicit --sort,
    # sort by stops ascending: nonstop first, then 1-stop, 2-stop...
    if args.stops != "0" and args.sort is None:
        merged.sort(key=lambda r: (
            r.get("stops") if r.get("stops") is not None else 999
        ))

    # Save full merged for fair compare before truncation
    full_merged = list(merged)

    if effective_limit is not None:
        merged = merged[:effective_limit]

    _apply_currency_conversion(merged, args, conf)

    if args.output == "json":
        print(json.dumps(merged, indent=2, ensure_ascii=False, default=str))
    else:
        print(_format_table(merged, verbose=args.verbose))

    # Cross-verification via fast-flights (optional) — uses full_merged
    if getattr(args, "compare", False):
        _run_compare(
            origin=origins[0],
            destination=dests[0],
            date=args.date,
            fli_records=full_merged,
            adults=args.adults,
            children=args.children,
            infants=args.infants,
            cabin=args.cabin,
            max_stops=stops_val if stops_val != "any" else None,
            use_browser=getattr(args, "browser", False),
            output_format=args.output,
        )


def _run_compare(
    origin, destination, date, fli_records, *,
    adults=1, children=0, infants=0, cabin="economy",
    max_stops=None, use_browser=False, output_format="table",
):
    """Cross-verify fli results with fast-flights (and optionally browser baseline)."""
    try:
        from sources.fast_flights_source import FastFlightsSource, _check_ff
    except ImportError:
        print("\n[compare] fast-flights module not found", file=sys.stderr)
        return

    if not _check_ff():
        print(
            "\n[compare] fast-flights not installed. "
            "Install with: pip install fast-flights>=3.0rc0",
            file=sys.stderr,
        )
        return

    from compare import match_flights, compute_diffs
    from compare import format_comparison_table, format_comparison_json

    ff_source = FastFlightsSource()
    ff_records, gf_url = ff_source.query_by_route(
        origin, destination, date,
        adults=adults, children=children, infants=infants, cabin=cabin,
        max_stops=max_stops,
    )

    comparison = match_flights(fli_records, ff_records)
    diffs = compute_diffs(comparison["matched"])

    print()  # blank line separator
    if output_format == "json":
        print(json.dumps(
            format_comparison_json(comparison, diffs, gf_url),
            indent=2, ensure_ascii=False, default=str,
        ))
    else:
        print(format_comparison_table(comparison, diffs, gf_url))

    # Browser baseline (optional, --browser flag)
    if use_browser:
        try:
            from baseline import BrowserBaseline, _check_playwright
        except ImportError:
            print("\n[compare] baseline module not found", file=sys.stderr)
            return
        if not _check_playwright():
            print(
                "\n[compare] playwright not installed. "
                "Install with: pip install playwright && playwright install chromium",
                file=sys.stderr,
            )
            return
        from compare import compare_against_baseline, format_baseline_table

        baseline = BrowserBaseline()
        baseline_records = baseline.verify_route(
            origin, destination, date, cabin=cabin, adults=adults,
        )
        if baseline_records:
            result = compare_against_baseline(fli_records, ff_records, baseline_records)
            print()
            if output_format == "json":
                print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
            else:
                print(format_baseline_table(result))
        else:
            print("\n[compare] Browser baseline returned no results", file=sys.stderr)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flyclaw",
        description=f"FlyClaw - Flight Information Aggregation CLI (v{__version__})",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False,
        help="Enable verbose output",
    )
    parser.add_argument(
        "-o", "--output", choices=["table", "json"], default=None,
        help="Output format (default: from config.yaml)",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Shared arguments for subparsers
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-v", "--verbose", action="store_true", default=False,
        help="Enable verbose output",
    )
    common.add_argument(
        "-o", "--output", choices=["table", "json"], default=None,
        help="Output format (default: from config.yaml)",
    )
    common.add_argument(
        "--currency", choices=["original", "usd", "cny"], default=None,
        help="Output currency: original (keep source currency), usd, cny (overrides config)",
    )
    common.add_argument(
        "--timeout", type=int, default=None,
        help="Global query timeout in seconds (overrides config)",
    )
    common.add_argument(
        "--return-time", type=int, default=None, dest="return_time",
        help="Smart return time in seconds (overrides config; 0 = disable)",
    )

    # query subcommand
    query_p = subparsers.add_parser(
        "query", help="Query by flight number", parents=[common],
    )
    query_p.add_argument(
        "--flight", "-f", required=True,
        help="Flight number (e.g. CA981)",
    )
    query_p.add_argument(
        "--no-relay", action="store_true", default=False, dest="no_relay",
        help="Disable route relay (skip Phase 2 Google Flights price lookup)",
    )
    query_p.add_argument(
        "--date", "-d", default=None,
        help="Filter results by date (YYYY-MM-DD or 'today')",
    )
    query_p.add_argument(
        "--show-codeshare", action="store_true", default=False,
        dest="show_codeshare",
        help="Show all codeshare variants (default: deduplicated)",
    )
    query_p.set_defaults(func=cmd_query)

    # search subcommand
    search_p = subparsers.add_parser(
        "search", help="Search by route", parents=[common],
    )
    search_p.add_argument(
        "--from", dest="from_station", required=True,
        help="Origin airport/city (IATA code, Chinese, or English)",
    )
    search_p.add_argument(
        "--to", dest="to_station", required=True,
        help="Destination airport/city",
    )
    search_p.add_argument(
        "--date", "-d", required=False, default=None,
        help="Travel date (YYYY-MM-DD)",
    )
    search_p.add_argument(
        "--return", "-r", dest="return_date", default=None,
        help="Return date for round-trip (YYYY-MM-DD)",
    )
    search_p.add_argument(
        "--adults", "-a", type=int, default=1,
        help="Number of adult passengers (default: 1)",
    )
    search_p.add_argument(
        "--children", type=int, default=0,
        help="Number of child passengers (default: 0)",
    )
    search_p.add_argument(
        "--infants", type=int, default=0,
        help="Number of infant passengers (default: 0)",
    )
    search_p.add_argument(
        "--cabin", "-C", default="economy",
        choices=["economy", "premium", "business", "first"],
        help="Cabin class (default: economy)",
    )
    search_p.add_argument(
        "--limit", "-l", type=int, default=None,
        help="Max results (default: 99 for nonstop, 20 for with-stops)",
    )
    search_p.add_argument(
        "--sort", "-s", default=None,
        choices=["cheapest", "fastest", "departure", "arrival"],
        help="Sort results by criteria",
    )
    search_p.add_argument(
        "--stops", type=str, default="0",
        choices=["0", "1", "2", "any"],
        help="Max stops: 0=nonstop (default), 1=one stop, 2=two stops, any=all",
    )
    search_p.add_argument(
        "--compare", action="store_true", default=False,
        help="Cross-verify with fast-flights (optional dependency)",
    )
    search_p.add_argument(
        "--browser", action="store_true", default=False,
        help="Use Playwright browser baseline for verification (requires --compare)",
    )
    search_p.add_argument(
        "--show-codeshare", action="store_true", default=False,
        dest="show_codeshare",
        help="Show all codeshare variants (default: deduplicated)",
    )
    search_p.set_defaults(func=cmd_search)

    # update-airports subcommand
    update_p = subparsers.add_parser(
        "update-airports", help="Update airport data from remote URL",
    )
    update_p.add_argument(
        "--url", required=False, default=None,
        help="URL to download airport data from (overrides config)",
    )
    update_p.set_defaults(func=cmd_update_airports)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    log_level = logging.DEBUG if getattr(args, "verbose", False) else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Resolve output format: CLI flag > config.yaml > "table"
    if getattr(args, "output", None) is None:
        conf = cfg.get_config()
        args.output = conf.get("output", {}).get("format", "table")

    # Auto-update airport data (skip for update-airports command itself)
    if args.command != "update-airports":
        _auto_update_airports()

    args.func(args)


if __name__ == "__main__":
    main()
