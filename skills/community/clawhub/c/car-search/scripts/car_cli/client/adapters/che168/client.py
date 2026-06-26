"""Che168 (che168.com / 汽车之家) adapter for searching used cars.

URL patterns (verified 2026-03):
    List:   https://www.che168.com/{city_pinyin}/list/
    Nation: https://www.che168.com/china/list/
    Brand:  https://www.che168.com/{city_pinyin}/{brand_pinyin}/
    Page:   ...a0_0msdgscncgpi1ltocsp{page}exx0/
    Detail: https://www.che168.com/dealer/{dealer_id}/{car_id}.html

Anti-bot: the site sets a cookie via inline JS on first request.  We
parse the cookie values from the JS challenge and replay them on a
second request to get the actual page content.
"""

import re

from car_cli.client.base import BaseClient
from car_cli.client.http import HttpClient
from car_cli.client.adapters.che168.brands import get_brand_slug
from car_cli.client.adapters.che168.cities import get_city_slug
from car_cli.client.adapters.che168.parser import parse_list, parse_detail, extract_series_list
from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail
from car_cli.models.filter import SearchFilter

_log = get_logger("che168")

# Price range segments used in che168 URL paths
_PRICE_RANGES: list[tuple[float, float, str]] = [
    (0, 3, "0_3"),
    (3, 5, "3_5"),
    (5, 8, "5_8"),
    (8, 10, "8_10"),
    (10, 15, "10_15"),
    (15, 20, "15_20"),
    (20, 25, "20_25"),
    (25, 35, "25_35"),
    (35, 50, "35_50"),
    (50, 80, "50_80"),
    (80, 100, "80_100"),
    (100, 0, "100_0"),  # 100万以上
]

# che168 anti-bot challenge marker
_CHALLENGE_MARKER = "__tst_status"


def _parse_challenge_cookies(html: str) -> dict[str, str]:
    """Extract cookie name=value pairs from the che168 JS challenge page.

    The challenge page sets cookies via:
        document.cookie = "__tst_status=" + value + "#;"
        document.cookie = "EO_Bot_Ssid=" + value + ";"
    """
    cookies: dict[str, str] = {}

    # __tst_status cookie
    tst_m = re.search(r'__tst_status="\s*\+\s*a\(0\)\s*\+\s*"', html)
    if tst_m:
        # The value is computed from JS: a(0) returns a numeric sum
        val = _eval_challenge_value(html, 0)
        if val is not None:
            cookies["__tst_status"] = f"{val}#"

    # EO_Bot_Ssid cookie
    eo_m = re.search(r'EO_Bot_Ssid=', html)
    if eo_m:
        val = _eval_challenge_value(html, 1)
        if val is not None:
            cookies["EO_Bot_Ssid"] = str(val)

    _log.debug("parsed challenge cookies: %s", list(cookies.keys()))
    return cookies


def _eval_challenge_value(html: str, index: int) -> int | None:
    """Evaluate the challenge JS function a(index).

    The JS defines an object with numeric values (WTKkN, bOYDu, wyeCN)
    and computes: t = WTKkN + bOYDu + wyeCN.
    a(0) returns t (the numeric sum).
    a(1) returns the EO_Bot_Ssid cookie string (computed from a nested function).
    """
    if index == 0:
        # Extract numeric values: WTKkN, bOYDu, wyeCN
        nums = re.findall(r'(?:WTKkN|bOYDu|wyeCN)\s*:\s*(\d+)', html)
        if len(nums) >= 3:
            total = sum(int(n) for n in nums)
            _log.debug("challenge a(0) values=%s sum=%d", nums, total)
            return total
    elif index == 1:
        # EO_Bot_Ssid: inner function n() computes value with nested numbers
        # Format: t=iTyzs(t, NUMBER) where iTyzs is addition
        inner_num = re.search(r'iTyzs.*?(\d{5,})', html)
        if inner_num:
            val = int(inner_num.group(1))
            _log.debug("challenge a(1) inner_num=%d", val)
            return val
    return None


class Che168Client(BaseClient):
    """Che168 (汽车之家) adapter for used car search."""

    platform_name = "che168"

    async def list_series(self, brand: str) -> list[dict[str, str]]:
        """Fetch series list for a brand from che168 brand listing page."""
        brand_slug = get_brand_slug(brand)
        if not brand_slug:
            return []

        city_slug = "china"
        url = f"https://www.che168.com/{city_slug}/{brand_slug}/"
        referer = "https://www.che168.com/"

        _log.debug("fetching series for brand=%s slug=%s", brand, brand_slug)
        html = await self._fetch_with_cookie_challenge(url, referer)

        series_list = extract_series_list(html, brand_slug)
        # Normalize to standard {"series_id", "series_name"} format
        return [
            {"series_id": s["series_slug"], "series_name": s["series_name"]}
            for s in series_list
        ]

    async def _resolve_series_slug(
        self, brand: str, series: str
    ) -> str | None:
        """Match a series name to its che168 URL slug via list_series."""
        brand_slug = get_brand_slug(brand)
        if not brand_slug:
            return None

        url = f"https://www.che168.com/china/{brand_slug}/"
        referer = "https://www.che168.com/"

        _log.debug("resolving series slug for brand=%s series=%s", brand, series)
        html = await self._fetch_with_cookie_challenge(url, referer)
        series_list = extract_series_list(html, brand_slug)

        if not series_list:
            _log.debug("no series data found for brand=%s", brand)
            return None

        _log.debug(
            "available series: %s",
            [s["series_name"] for s in series_list[:20]],
        )

        for s in series_list:
            if s["series_name"] == series:
                _log.debug("series exact match: %s -> %s", series, s["series_slug"])
                return s["series_slug"]

        for s in series_list:
            sname = s["series_name"]
            if series in sname or sname in series:
                _log.debug(
                    "series fuzzy match: %s -> %s (%s)",
                    series, s["series_slug"], sname,
                )
                return s["series_slug"]

        _log.debug("no series match for %r", series)
        return None

    def _build_list_url(
        self, filters: SearchFilter, series_slug: str = ""
    ) -> str:
        city_slug = get_city_slug(filters.city)

        # Base path
        parts: list[str] = [city_slug]

        # Brand filter
        if filters.brand:
            brand_slug = get_brand_slug(filters.brand)
            if brand_slug:
                parts.append(brand_slug)
                _log.debug("brand %r -> slug %s", filters.brand, brand_slug)

                # Series slug appended after brand
                if series_slug:
                    parts.append(series_slug)
                    _log.debug("series slug=%s", series_slug)

        # Build URL base
        base = f"https://www.che168.com/{'/'.join(parts)}/"

        # Price range
        price_seg = self._get_price_segment(filters.min_price, filters.max_price)

        # Pagination segment: a0_0msdgscncgpi1ltocsp{page}exx0
        page = max(filters.page, 1)

        # Construct filter path
        if price_seg or page > 1:
            filter_path = f"a0_0msdgscncgpi1lto{price_seg}csp{page}exx0/"
            url = base + filter_path
        else:
            # Default list path (no filters)
            if not filters.brand:
                url = base + "list/"
            else:
                url = base

        return url

    def _get_price_segment(
        self, min_price: float | None, max_price: float | None
    ) -> str:
        """Map min/max price (万元) to a che168 URL price segment."""
        if min_price is None and max_price is None:
            return ""

        lo = min_price or 0
        hi = max_price or 0

        # Find exact match
        for rng_lo, rng_hi, seg in _PRICE_RANGES:
            if rng_lo == lo and rng_hi == hi:
                return seg
            if rng_hi == 0 and lo >= rng_lo and hi == 0:
                return seg

        # Find best enclosing range
        for rng_lo, rng_hi, seg in _PRICE_RANGES:
            if rng_hi == 0:
                if lo >= rng_lo:
                    return seg
            elif lo >= rng_lo and (hi <= rng_hi or hi == 0):
                return seg

        return ""

    async def _fetch_with_cookie_challenge(
        self, url: str, referer: str
    ) -> str:
        """Fetch a URL, handling the che168 cookie challenge if encountered."""
        async with HttpClient(referer=referer) as client:
            resp = await client.get(url)
            html = resp.text

            if _CHALLENGE_MARKER not in html or len(html) > 5000:
                return html

            _log.debug("cookie challenge detected, parsing cookies")
            cookies = _parse_challenge_cookies(html)
            if not cookies:
                _log.debug("failed to parse challenge cookies")
                return html

            # Retry with challenge cookies
            resp2 = await client.get(url, cookies=cookies)
            return resp2.text

    async def search(self, filters: SearchFilter) -> list[Car]:
        # Resolve series name to slug if both brand and series are specified
        series_slug = ""
        if filters.series and filters.brand:
            series_slug = await self._resolve_series_slug(
                filters.brand, filters.series
            ) or ""
            if series_slug:
                _log.debug(
                    "series %r resolved to slug %s", filters.series, series_slug
                )
            else:
                _log.debug(
                    "series %r not resolved, searching without series filter",
                    filters.series,
                )

        url = self._build_list_url(filters, series_slug)
        referer = "https://www.che168.com/"
        _log.debug("search url=%s", url)

        html = await self._fetch_with_cookie_challenge(url, referer)
        _log.debug("list response html_len=%d", len(html))

        if len(html) < 2000:
            raise RuntimeError(
                "che168.com 返回了异常短的页面，可能是反爬拦截。"
                "请稍后再试。"
            )

        city = filters.city if filters.city and filters.city != "全国" else ""
        cars = parse_list(html, city)
        _log.debug("parsed list count=%d", len(cars))

        # Client-side filtering for fields not in URL
        if filters.min_price:
            cars = [c for c in cars if c.price >= filters.min_price]
        if filters.max_price:
            cars = [c for c in cars if c.price <= filters.max_price]

        return cars

    async def detail(self, car_id: str) -> CarDetail:
        # car_id format: {dealer_id}_{info_id}
        if "_" in car_id:
            dealer_id, info_id = car_id.split("_", 1)
        else:
            dealer_id, info_id = "0", car_id

        url = f"https://www.che168.com/dealer/{dealer_id}/{info_id}.html"
        referer = "https://www.che168.com/"
        _log.debug("detail url=%s car_id=%s", url, car_id)

        html = await self._fetch_with_cookie_challenge(url, referer)
        _log.debug("detail html_len=%d", len(html))

        if len(html) < 2000:
            raise RuntimeError(
                "che168.com 返回了异常短的详情页，可能是反爬拦截。"
            )

        detail = parse_detail(html, car_id)
        _log.debug("detail title=%r price=%s", detail.title, detail.price)
        return detail
