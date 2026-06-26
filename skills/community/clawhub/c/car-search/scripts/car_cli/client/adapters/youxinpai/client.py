"""Youxinpai (youxinpai.com / 优信拍) adapter for used car auctions.

API endpoints (verified 2026-04):
    List:   POST https://www.youxinpai.com/trade/getTradeList
    Brands: GET  https://www.youxinpai.com/car/getBrand?type=1
    Detail: GET  https://www.youxinpai.com/home/trade/detail/{auctionId}/{crykey}

The list API uses a JSON body with a double-encoded `entities` field:
    {"entities": "{\"req\":{...},\"page\":[{...}]}"}

Anti-bot: the API requires csrfToken / jwt_token cookies obtained from an
initial GET to the trade page.  We perform a session-init GET first, then
POST the search using the same client (cookie jar).

Series filtering: the brand API returns carSerialList for each brand.
We look up the carSeiralId and pass it as serialIds in the search payload.
"""

import json

from car_cli.client.base import BaseClient
from car_cli.client.http import HttpClient
from car_cli.client.adapters.youxinpai.cities import get_city_id
from car_cli.client.adapters.youxinpai.parser import parse_list, parse_detail
from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail
from car_cli.models.filter import SearchFilter

_log = get_logger("youxinpai")

_BASE_URL = "https://www.youxinpai.com"
_TRADE_PAGE = f"{_BASE_URL}/trade"
_LIST_API = f"{_BASE_URL}/trade/getTradeList"
_BRAND_API = f"{_BASE_URL}/car/getBrand?type=1"
_DETAIL_URL = f"{_BASE_URL}/home/trade/detail"

# 优信拍价格区间枚举 (万元) -> carPriceLevel 值
_PRICE_LEVELS: list[tuple[float, float, int]] = [
    (0, 3, 1),
    (3, 5, 2),
    (5, 8, 3),
    (8, 12, 4),
    (12, 15, 5),
    (15, 20, 6),
    (20, 30, 7),
    (30, 50, 8),
    (50, 100, 9),
    (100, 0, 10),  # 100万以上
]

# 优信拍年份区间 -> carYearLevel 值
_YEAR_LEVELS: list[tuple[int, int, int]] = [
    (2024, 9999, 1),  # 1年内
    (2022, 2024, 2),  # 1-3年
    (2019, 2022, 3),  # 3-5年
    (2017, 2019, 4),  # 5-8年
    (2014, 2017, 5),
    (0, 2014, 6),     # 8年以上
]

# sort_by 映射
_SORT_MAP = {
    "default": 10,
    "price_asc": 2,
    "price_desc": 1,
    "date": 10,
}


def _make_client() -> HttpClient:
    return HttpClient(
        base_url=_BASE_URL,
        referer=_TRADE_PAGE,
        extra_headers={"Origin": _BASE_URL},
    )


def _brand_name_matches(api_name: str, query: str) -> bool:
    """Fuzzy-match brand name, tolerating '汽车' suffix differences."""
    if api_name == query:
        return True
    if api_name == query + "汽车":
        return True
    if api_name.removesuffix("汽车") == query:
        return True
    return False


class YouxinpaiClient(BaseClient):
    """优信拍 adapter for used car auction search and detail."""

    platform_name = "youxinpai"

    @staticmethod
    async def _init_session(client: HttpClient) -> None:
        """GET the trade page to populate csrfToken / jwt_token cookies."""
        _log.debug("session init: GET %s", _TRADE_PAGE)
        resp = await client.get(_TRADE_PAGE)
        _log.debug(
            "session init done status=%s cookies=%s",
            resp.status_code,
            list(resp.cookies.keys()) if resp.cookies else "none",
        )

    def _map_price_level(
        self, min_price: float | None, max_price: float | None
    ) -> list[int]:
        if min_price is None and max_price is None:
            return []
        lo = min_price or 0
        hi = max_price or 0
        levels = []
        for rng_lo, rng_hi, level in _PRICE_LEVELS:
            if rng_hi == 0:
                if lo <= rng_lo or hi == 0:
                    levels.append(level)
            elif (lo <= rng_lo and (hi >= rng_hi or hi == 0)) or (lo >= rng_lo and lo < rng_hi):
                levels.append(level)
        return levels

    def _map_year_level(
        self, min_year: int | None, max_year: int | None
    ) -> list[int]:
        if min_year is None and max_year is None:
            return []
        lo = min_year or 0
        hi = max_year or 9999
        levels = []
        for yr_lo, yr_hi, level in _YEAR_LEVELS:
            if yr_lo <= hi and yr_hi >= lo:
                levels.append(level)
        return levels

    async def _fetch_brand_and_serial_ids(
        self, client: HttpClient, brand_name: str, series_name: str
    ) -> tuple[int | None, int | None]:
        """Return (carBrandId, carSeiralId) from the brand API.

        The brand API returns a list of brands, each containing carSerialList.
        Both brand and series IDs are resolved in a single API call.
        """
        try:
            resp = await client.get(_BRAND_API)
            brands = resp.json()
        except Exception:
            _log.debug("brand API request failed", exc_info=True)
            return None, None

        if not isinstance(brands, list):
            _log.debug("brand API returned unexpected type: %s", type(brands))
            return None, None

        for brand in brands:
            bname = brand.get("brandName", "")
            if not _brand_name_matches(bname, brand_name):
                continue

            brand_id: int = brand.get("carBrandId")
            _log.debug("brand %r -> id %s", brand_name, brand_id)

            if not series_name:
                return brand_id, None

            # Look up series within this brand
            for serial in brand.get("carSerialList", []):
                sname = serial.get("seiralName", "")
                if sname == series_name or series_name in sname or sname in series_name:
                    serial_id: int = serial.get("carSeiralId")
                    _log.debug("series %r -> id %s", series_name, serial_id)
                    return brand_id, serial_id

            _log.debug("series %r not found under brand %r", series_name, brand_name)
            return brand_id, None

        _log.debug("brand %r not found in youxinpai brand list", brand_name)
        return None, None

    async def search(self, filters: SearchFilter) -> list[Car]:
        city_ids: list[int] = []
        if filters.city and filters.city != "全国":
            cid = get_city_id(filters.city)
            if cid:
                city_ids.append(cid)
            else:
                _log.debug("city %r not found, searching nationwide", filters.city)

        req: dict = {
            "cityIds": city_ids,
            "serialIds": [],
            "carPriceLevel": self._map_price_level(filters.min_price, filters.max_price),
            "carYearLevel": self._map_year_level(filters.min_year, filters.max_year),
            "orderFields": _SORT_MAP.get(filters.sort_by, 10),
        }

        async with _make_client() as client:
            await self._init_session(client)

            if filters.brand:
                brand_id, serial_id = await self._fetch_brand_and_serial_ids(
                    client, filters.brand, filters.series
                )
                if brand_id:
                    req["carBrandId"] = brand_id
                if serial_id:
                    req["serialIds"] = [serial_id]

            page_obj = {
                "page": max(filters.page, 1),
                "pageSize": min(filters.page_size, 40),
                "pageTab": "immediately",
            }

            inner = {"req": req, "page": [page_obj]}
            entities_str = json.dumps(inner, ensure_ascii=False)
            body = {"entities": entities_str}

            _log.debug("search payload=%s", json.dumps(body, ensure_ascii=False)[:500])

            resp = await client.post(
                _LIST_API,
                json=body,
                headers={"Content-Type": "application/json"},
            )
            data = resp.json()

        _log.debug(
            "search response code=%s data_keys=%s",
            data.get("code"),
            list(data.get("data", {}).keys()) if isinstance(data.get("data"), dict) else "N/A",
        )

        if data.get("code") == 403:
            raise RuntimeError(f"youxinpai API 拒绝请求：{data.get('msg', '未知错误')}")

        cars = parse_list(data, self.platform_name)
        _log.debug("parsed %d cars", len(cars))
        return cars

    async def detail(self, car_id: str) -> CarDetail:
        if "_" in car_id:
            auction_id, crykey = car_id.split("_", 1)
        else:
            auction_id, crykey = car_id, ""

        if not crykey:
            raise ValueError(
                f"优信拍 car_id 格式应为 '{{auctionId}}_{{crykey}}'，"
                f"收到: {car_id!r}。crykey 是详情页 URL 的必需参数。"
            )

        url = f"{_DETAIL_URL}/{auction_id}/{crykey}"
        _log.debug("detail url=%s", url)

        async with _make_client() as client:
            await self._init_session(client)
            resp = await client.get(url)
            html = resp.text

        _log.debug("detail html_len=%d", len(html))

        if len(html) < 500:
            raise RuntimeError(
                f"youxinpai.com 返回了异常短的详情页 (len={len(html)})，"
                "可能是参数错误或页面已下架。"
            )

        detail = parse_detail(html, car_id)
        if not detail.url:
            detail.url = url
        _log.debug("detail title=%r price=%.2f mileage=%.2f", detail.title, detail.price, detail.mileage)
        return detail
