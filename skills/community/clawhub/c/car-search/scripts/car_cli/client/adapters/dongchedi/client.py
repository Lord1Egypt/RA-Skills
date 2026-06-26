"""Dongchedi (dongchedi.com) adapter for searching used cars.

List page URL pattern (28 hyphen-separated slots, 0-indexed):
    https://www.dongchedi.com/usedcar/{s0}-{s1}-...-{s27}?sh_city_name={city}

    Slot mapping (verified against live site 2026-03):
         0: price range "min,max" in 万元, e.g. "3,5" = 3-5万
      1-18: other filters (body type, fuel type, year, mileage, etc.) — mostly x
        19: brand_id
        20: series_id (x if unset)
        21: city adcode (e.g. 110000 for 北京)
        22: page number (1-based)
     23-27: reserved (x)

    When no filter is active the site shows a 19-segment all-x path, but as
    soon as ANY filter is applied (including city) the path expands to 28
    segments.  We always use 28 for consistency.

Detail page:
    https://www.dongchedi.com/usedcar/{sku_id}

Numbers (price, mileage) are obfuscated with PUA-codepoint custom fonts.
See font_decoder.py for the decoding logic.
"""

from dataclasses import asdict

from car_cli.client.base import BaseClient
from car_cli.client.http import HttpClient
from car_cli.client.adapters.dongchedi.brands import get_brand_id
from car_cli.client.adapters.dongchedi.parser import parse_list, parse_detail, extract_series_list
from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail
from car_cli.client.adapters.dongchedi.cities import get_city_adcode
from car_cli.models.filter import SearchFilter

_log = get_logger("dongchedi")

_NUM_SLOTS = 28
_SLOT_PRICE = 0
_SLOT_BRAND = 19
_SLOT_SERIES = 20
_SLOT_CITY = 21
_SLOT_PAGE = 22


class DongchediClient(BaseClient):
    """Dongchedi adapter for used car search."""

    platform_name = "dongchedi"

    async def list_series(self, brand: str) -> list[dict[str, str]]:
        """Fetch series list for a brand from dongchedi __NEXT_DATA__."""
        bid = get_brand_id(brand)
        if not bid:
            return []

        slots = ["x"] * _NUM_SLOTS
        slots[_SLOT_BRAND] = bid
        slots[_SLOT_PAGE] = "1"
        path = "-".join(slots)
        url = f"https://www.dongchedi.com/usedcar/{path}?sh_city_name=全国"

        _log.debug("fetching series for brand=%s bid=%s", brand, bid)
        async with HttpClient(referer="https://www.dongchedi.com/usedcar") as client:
            resp = await client.get(url)
            return extract_series_list(resp.text)

    async def _resolve_series_id(self, brand: str, series: str) -> str | None:
        """Match a series name to its ID via list_series."""
        series_list = await self.list_series(brand)
        if not series_list:
            _log.debug("no series data found for brand=%s", brand)
            return None

        _log.debug("available series: %s", [s["series_name"] for s in series_list])

        for s in series_list:
            if s["series_name"] == series:
                _log.debug("series exact match: %s -> %s", series, s["series_id"])
                return s["series_id"]

        for s in series_list:
            sname = s["series_name"]
            if series in sname or sname in series:
                _log.debug("series fuzzy match: %s -> %s (%s)", series, s["series_id"], sname)
                return s["series_id"]

        _log.debug("no series match for %r", series)
        return None

    def _build_list_url(self, filters: SearchFilter, series_id: str = "") -> str:
        slots = ["x"] * _NUM_SLOTS

        # Price range: "min,max" in 万元
        if filters.min_price is not None or filters.max_price is not None:
            lo = int(filters.min_price) if filters.min_price else 0
            hi = int(filters.max_price) if filters.max_price else 0
            if hi:
                slots[_SLOT_PRICE] = f"{lo},{hi}"
            elif lo:
                slots[_SLOT_PRICE] = f"{lo},"

        # Brand
        if filters.brand:
            bid = get_brand_id(filters.brand)
            if bid:
                slots[_SLOT_BRAND] = bid
                _log.debug("brand %r -> id %s", filters.brand, bid)

        # Series
        if series_id:
            slots[_SLOT_SERIES] = series_id

        # City adcode
        city = filters.city if filters.city else "全国"
        adcode = get_city_adcode(city)
        if adcode:
            slots[_SLOT_CITY] = adcode

        # Page (always write; default to 1)
        slots[_SLOT_PAGE] = str(max(filters.page, 1))

        path = "-".join(slots)
        url = f"https://www.dongchedi.com/usedcar/{path}?sh_city_name={city}"
        return url

    async def search(self, filters: SearchFilter) -> list[Car]:
        # Resolve series name to ID if both brand and series are specified
        series_id = ""
        if filters.series and filters.brand:
            series_id = await self._resolve_series_id(filters.brand, filters.series) or ""
            if series_id:
                _log.debug("series %r resolved to id %s", filters.series, series_id)
            else:
                _log.debug("series %r not resolved, searching without series filter", filters.series)

        url = self._build_list_url(filters, series_id)
        referer = "https://www.dongchedi.com/usedcar"
        _log.debug("search url=%s", url)
        _log.debug("search filters=%s", asdict(filters))

        async with HttpClient(referer=referer) as client:
            resp = await client.get(url)
            html = resp.text

        _log.debug("list response html_len=%s", len(html))

        if len(html) < 2000:
            raise RuntimeError(
                "dongchedi.com returned an unexpectedly short page. "
                "The site may be blocking requests or requiring verification."
            )

        cars = parse_list(html, filters.city)
        _log.debug("parsed list count=%s", len(cars))
        return cars

    async def detail(self, car_id: str) -> CarDetail:
        url = f"https://www.dongchedi.com/usedcar/{car_id}"
        referer = "https://www.dongchedi.com/usedcar"
        _log.debug("detail url=%s car_id=%s", url, car_id)

        async with HttpClient(referer=referer) as client:
            resp = await client.get(url)
            html = resp.text

        _log.debug("detail html_len=%s", len(html))

        if len(html) < 2000:
            raise RuntimeError(
                "dongchedi.com returned an unexpectedly short detail page."
            )

        detail = parse_detail(html, car_id)
        _log.debug("detail title=%r price=%s", detail.title, detail.price)
        return detail
