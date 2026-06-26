"""Parse youxinpai listing API responses and detail page HTML.

Detail page data is embedded as SSR JSON in window.__SSR_DATA__.
We extract individual fields with targeted regex patterns against the raw
JSON text — avoids parsing the full 350KB+ JSON blob which is very slow.
"""

import re

from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail

_log = get_logger("youxinpai.parser")

_DETAIL_BASE = "https://www.youxinpai.com/home/trade/detail"


# --------------------------------------------------------------------------- #
# List page parsing (JSON API response)                                        #
# --------------------------------------------------------------------------- #

def parse_list(data: dict, platform: str = "youxinpai") -> list[Car]:
    """Parse getTradeList API JSON response into Car objects.

    Expected structure:
        data.entities.immediately.auctionListEntity -> list of items
    """
    entities = data.get("data", {}).get("entities", {})
    immediately = entities.get("immediately", {})
    items = immediately.get("auctionListEntity", [])

    if not items:
        _log.debug("no items found in response, keys=%s", list(entities.keys()))
        return []

    _log.debug("found %d items in auctionListEntity", len(items))
    cars: list[Car] = []

    for item in items:
        try:
            car = _parse_item(item, platform)
            if car:
                cars.append(car)
        except Exception:
            _log.debug("failed to parse item id=%s", item.get("id"), exc_info=True)

    return cars


def _parse_item(item: dict, platform: str) -> Car | None:
    auction_id = str(item.get("id", ""))
    crykey = item.get("crykey", "")
    if not auction_id:
        return None

    car_id = f"{auction_id}_{crykey}" if crykey else auction_id

    title = item.get("auctionTitle", "")
    city = item.get("carCityName", "")
    # 标题通常有城市前缀: "[上海.沪A] 马自达 CX-5 2019款 ..."
    clean_title = re.sub(r"^\[.*?\]\s*", "", title)

    brand = item.get("brandName", "")
    if not brand:
        parts = clean_title.split()
        brand = parts[0] if parts else ""

    price = _parse_price_item(item)
    mileage = _parse_mileage_item(item)

    year = item.get("year", "")
    model_year = f"20{year}款" if year and len(year) == 2 else ""

    color = item.get("carColor", "")
    detail_url = f"{_DETAIL_BASE}/{auction_id}/{crykey}" if crykey else ""

    return Car(
        id=car_id,
        platform=platform,
        title=clean_title or title,
        price=price,
        brand=brand,
        model_year=model_year,
        mileage=mileage,
        city=city,
        color=color,
        url=detail_url,
    )


def _parse_price_item(item: dict) -> float:
    """Extract price in 万元 from list API item."""
    # pricesStart is a string like "3.00" (万元)
    for key in ("pricesStart", "currentPrices", "startPrices"):
        val = item.get(key, "")
        if val:
            try:
                f = float(val)
                # Values > 200 are likely in 元, convert to 万
                return f / 10000 if f > 200 else f
            except (ValueError, TypeError):
                pass
    return 0.0


def _parse_mileage_item(item: dict) -> float:
    """Extract mileage in 万公里 from list API item."""
    # kilometers is a string like "5.14" (万公里)
    km = item.get("kilometers", "")
    if km:
        try:
            return float(km)
        except (ValueError, TypeError):
            pass

    # mileage is raw int in 公里
    raw = item.get("mileage")
    if raw is not None:
        try:
            val = float(raw)
            return val / 10000 if val > 100 else val
        except (ValueError, TypeError):
            pass

    return 0.0


# --------------------------------------------------------------------------- #
# Detail page parsing (SSR JSON regex extraction)                              #
# --------------------------------------------------------------------------- #

def parse_detail(html: str, car_id: str) -> CarDetail:
    """Parse youxinpai detail page HTML into CarDetail.

    Data is stored in window.__SSR_DATA__ as a large JSON blob.
    We extract fields directly via regex to avoid parsing the full JSON.
    """
    auction_id, crykey = _split_car_id(car_id)
    detail_url = f"{_DETAIL_BASE}/{auction_id}/{crykey}" if crykey else ""

    # Primary title from carInfo.carName or auctionTitle
    title = _ssr_str(html, "carName") or _ssr_str(html, "auctionTitle") or ""
    clean_title = re.sub(r"^\[.*?\]\s*", "", title)

    brand = _ssr_str(html, "brandName") or ""
    if not brand and clean_title:
        brand = clean_title.split()[0]

    # Price: startPrice is in 元
    price_raw = _ssr_num(html, "startPrice")
    price = price_raw / 10000 if price_raw > 0 else 0.0

    # Mileage: mileage is in 公里
    mileage_raw = _ssr_num(html, "mileage")
    mileage = mileage_raw / 10000 if mileage_raw > 0 else 0.0

    color = _ssr_str(html, "carBodyColor") or _ssr_str(html, "carOriginalColor") or ""
    city = _ssr_str(html, "carCityName") or ""
    fuel_type = _ssr_str(html, "fuelType") or ""
    transfer_count_raw = _ssr_num(html, "transferCount")
    transfer_count = str(int(transfer_count_raw)) + "次" if transfer_count_raw >= 0 else ""

    # registDate: "2019-06-27T16:00:00.000Z" -> "2019-06"
    regist_date_raw = _ssr_str(html, "registDate") or ""
    first_reg_date = ""
    if regist_date_raw:
        m = re.match(r"(\d{4}-\d{2})", regist_date_raw)
        first_reg_date = m.group(1) if m else regist_date_raw[:7]

    description = _ssr_str(html, "carLevelDesc") or ""

    # Transmission: inferred from title (e.g. "自动" in title is reliable)
    transmission = ""
    if "自动" in clean_title or "CVT" in clean_title:
        transmission = "自动"
    elif "手动" in clean_title:
        transmission = "手动"

    # Images from carImages array
    images = re.findall(
        r'"carImages"\s*:\s*\[([^\]]*)\]', html
    )
    image_urls: list[str] = []
    if images:
        image_urls = re.findall(
            r'https?://[^"]+\.(?:jpg|jpeg|png|webp)(?:\?[^"]*)?',
            images[0]
        )
        image_urls = list(dict.fromkeys(image_urls))[:20]

    _log.debug(
        "detail parsed title=%r price=%.2f mileage=%.2f city=%r",
        clean_title, price, mileage, city,
    )

    return CarDetail(
        id=car_id,
        platform="youxinpai",
        title=clean_title or title,
        price=price,
        brand=brand,
        mileage=mileage,
        city=city,
        color=color,
        url=detail_url,
        description=description,
        transmission=transmission,
        fuel_type=fuel_type,
        first_reg_date=first_reg_date,
        transfer_count=transfer_count,
        images=image_urls,
    )


# --------------------------------------------------------------------------- #
# SSR JSON field extractors (regex, no full JSON parse)                        #
# --------------------------------------------------------------------------- #

def _ssr_str(html: str, key: str) -> str:
    """Extract a string value from SSR JSON: "key":"value"."""
    m = re.search(rf'"{re.escape(key)}"\s*:\s*"((?:[^"\\]|\\.)*)"', html)
    if m:
        # Unescape basic JSON escape sequences
        val = m.group(1)
        val = val.replace('\\"', '"').replace("\\n", " ").replace("\\u002F", "/")
        return val.strip()
    return ""


def _ssr_num(html: str, key: str) -> float:
    """Extract a numeric value from SSR JSON: "key":123."""
    m = re.search(rf'"{re.escape(key)}"\s*:\s*(-?[\d.]+)', html)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return -1.0


def _split_car_id(car_id: str) -> tuple[str, str]:
    if "_" in car_id:
        auction_id, crykey = car_id.split("_", 1)
        return auction_id, crykey
    return car_id, ""
