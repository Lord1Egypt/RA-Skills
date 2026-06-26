"""RSC data extraction and parsing for guazi.com pages.

Guazi uses Next.js App Router with React Server Components.  The HTML
contains ``<script>`` tags that call ``self.__next_f.push(…)`` with
flight-data payloads.  The payloads are JavaScript arrays where the
second element is a string containing RSC wire-format data.  JSON
objects within these strings are escaped (``\\"`` for quotes etc.).

We use two strategies:
1. Try to find and parse JSON from unescaped RSC fragments
2. Fall back to regex on the raw HTML to extract individual fields
"""

import json
import re

from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail

_log = get_logger("guazi.parser")


# ── RSC / Next.js flight-data extraction ──────────────────────


def _unescape_js_string(s: str) -> str:
    """Unescape a JavaScript string literal (handles \\", \\n, \\u00xx etc)."""
    # Handle \\uXXXX sequences first
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    # Replace \\\\ with a placeholder, then handle \\", then restore
    s = s.replace("\\\\", "\x00")
    s = s.replace('\\"', '"')
    s = s.replace("\\n", "\n")
    s = s.replace("\\t", "\t")
    s = s.replace("\x00", "\\")
    return s


def _strip_rsc_escaping(s: str) -> str:
    """Aggressively strip RSC/JS escaping for regex matching.

    RSC wire format uses multiple levels of escaping (\\\\\\\"key\\\\\\\").
    We repeatedly unescape until stable, then strip remaining backslashes
    before quotes.
    """
    # Repeatedly apply unescape until stable
    for _ in range(4):
        prev = s
        s = _unescape_js_string(s)
        if s == prev:
            break
    # Final fallback: strip any remaining backslashes before quotes
    s = re.sub(r'\\+(["\'])', r'\1', s)
    return s


def _extract_rsc_json_objects(html: str) -> list[dict]:
    """Extract JSON objects from ``self.__next_f.push()`` RSC payloads.

    RSC chunks look like:
        self.__next_f.push([1,"rsc-wire-format-data..."])

    The string payload may contain embedded JSON with escaped quotes.
    """
    objects: list[dict] = []

    # Find the string payload inside each push call
    # Format: self.__next_f.push([<id>,"<payload>"])
    for m in re.finditer(
        r'self\.__next_f\.push\(\[[\d,\s]*"((?:[^"\\]|\\.)*)"\]\)',
        html,
    ):
        raw = m.group(1)
        if len(raw) < 50:
            continue

        # Unescape the JS string
        unescaped = _unescape_js_string(raw)

        # Try to find JSON objects in the unescaped content
        # RSC wire format has lines like: N:JSON_OBJECT
        # e.g. 3:{"carList":[...]}
        for json_m in re.finditer(r'(?:^|[\n:])\s*(\{.+)', unescaped, re.MULTILINE):
            candidate = json_m.group(1)
            # Try to parse balanced JSON
            obj = _try_parse_json(candidate)
            if obj and isinstance(obj, dict):
                objects.append(obj)

    _log.debug("extracted %d JSON objects from RSC chunks", len(objects))
    return objects


def _try_parse_json(s: str) -> dict | None:
    """Try to parse a JSON object from the start of a string."""
    # First try parsing the whole string
    try:
        obj = json.loads(s)
        if isinstance(obj, dict):
            return obj
    except (json.JSONDecodeError, ValueError):
        pass

    # Try balanced brace matching
    depth = 0
    for i, ch in enumerate(s):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(s[:i + 1])
                    if isinstance(obj, dict):
                        return obj
                except (json.JSONDecodeError, ValueError):
                    pass
                break
        # Skip string content
        elif ch == '"':
            j = i + 1
            while j < len(s):
                if s[j] == '\\':
                    j += 2
                elif s[j] == '"':
                    break
                else:
                    j += 1
    return None


def _find_in_nested(data, key: str, max_depth: int = 8) -> list:
    """Recursively search for a key in nested dicts/lists."""
    results = []
    if max_depth <= 0:
        return results
    if isinstance(data, dict):
        if key in data:
            results.append(data[key])
        for v in data.values():
            results.extend(_find_in_nested(v, key, max_depth - 1))
    elif isinstance(data, list):
        for item in data:
            results.extend(_find_in_nested(item, key, max_depth - 1))
    return results


# ── List page parsing ──────────────────────────────────────────


def parse_list(html: str, city: str) -> list[Car]:
    """Parse car list from guazi.com listing page HTML (RSC data)."""
    cars: list[Car] = []

    # Strategy 1: Extract from RSC JSON chunks
    json_objects = _extract_rsc_json_objects(html)
    for obj in json_objects:
        car_lists = _find_in_nested(obj, "carList", max_depth=5)
        for car_list in car_lists:
            if isinstance(car_list, list) and len(car_list) > 0:
                _log.debug("found carList with %d items", len(car_list))
                for item in car_list:
                    try:
                        car = _rsc_item_to_car(item, city)
                        if car:
                            cars.append(car)
                    except Exception:
                        continue

    if cars:
        _log.debug("RSC parse yielded %d cars", len(cars))
        return cars

    # Strategy 2: Regex on the raw (possibly escaped) HTML
    # In RSC the keys may appear as \"encryptedClueId\" (escaped quotes)
    _log.debug("trying regex fallback on raw HTML for car data")
    cars = _parse_list_regex(html, city)

    _log.debug("total parsed cars=%d", len(cars))
    return cars


def _rsc_item_to_car(item: dict, city: str) -> Car | None:
    """Convert a single car item from RSC carList to a Car."""
    clue_id = str(item.get("encryptedClueId") or item.get("clueId") or "")
    if not clue_id:
        return None

    # skuBasicArea contains title, mileage, license date, city
    basic = item.get("skuBasicArea") or {}
    title = basic.get("title") or ""

    # Price from priceArea
    price_area = item.get("priceArea") or {}
    purchase_price = price_area.get("purchasePrice") or {}
    price_str = purchase_price.get("priceString") or ""
    price = _parse_wan_price(price_str)

    # Mileage from roadHaul (e.g. "1.02万公里")
    road_haul = basic.get("roadHaul") or ""
    mileage = _parse_wan_km(road_haul)

    # License date / model year (e.g. "2024年")
    license_date = basic.get("licenseDate") or ""
    model_year = ""
    yr_m = re.search(r'(\d{4})', license_date)
    if yr_m:
        model_year = yr_m.group(1)

    # City
    car_city = basic.get("carSourceCityDesc") or city

    # Tags
    tags: list[str] = []
    tag_list = basic.get("tagList") or item.get("tagList") or []
    for tag in tag_list:
        if isinstance(tag, dict):
            text = tag.get("text") or tag.get("name") or ""
            if text:
                tags.append(text)
        elif isinstance(tag, str) and tag:
            tags.append(tag)

    return Car(
        id=clue_id,
        platform="guazi",
        title=title,
        price=price,
        model_year=model_year,
        mileage=mileage,
        first_reg_date=license_date,
        city=car_city,
        url=f"https://www.guazi.com/car-detail/{clue_id}.html",
        tags=tags,
    )


def _parse_list_regex(html: str, city: str) -> list[Car]:
    """Fallback: extract car data from RSC inline strings via regex.

    In RSC payloads, JSON keys appear with escaped quotes: \\"key\\":\\"value\\"
    We match both normal and escaped patterns.
    """
    cars: list[Car] = []
    seen: set[str] = set()

    # Match both "encryptedClueId" and \"encryptedClueId\" patterns
    clue_pattern = re.compile(
        r'(?:\\?")encryptedClueId(?:\\?")\s*:\s*(?:\\?")(c\d+)(?:\\?")'
    )
    for m in clue_pattern.finditer(html):
        clue_id = m.group(1)
        if clue_id in seen:
            continue
        seen.add(clue_id)

        # Extract surrounding context (wide window for RSC data)
        start = max(0, m.start() - 500)
        end = min(len(html), m.end() + 3000)
        context = html[start:end]

        # Aggressively unescape for easier regex matching
        ctx = _strip_rsc_escaping(context)

        title = ""
        t_m = re.search(r'"title"\s*:\s*"([^"]+)"', ctx)
        if t_m:
            title = t_m.group(1)

        price = 0.0
        p_m = re.search(r'"priceString"\s*:\s*"([^"]+)"', ctx)
        if p_m:
            price = _parse_wan_price(p_m.group(1))

        mileage = 0.0
        mil_m = re.search(r'"roadHaul"\s*:\s*"([^"]+)"', ctx)
        if mil_m:
            mileage = _parse_wan_km(mil_m.group(1))

        model_year = ""
        yr_m = re.search(r'"licenseDate"\s*:\s*"(\d{4})[^"]*"', ctx)
        if yr_m:
            model_year = yr_m.group(1)

        car_city = city
        city_m = re.search(r'"carSourceCityDesc"\s*:\s*"([^"]+)"', ctx)
        if city_m:
            car_city = city_m.group(1)

        if title or price:
            cars.append(Car(
                id=clue_id,
                platform="guazi",
                title=title,
                price=price,
                model_year=model_year,
                mileage=mileage,
                city=car_city,
                url=f"https://www.guazi.com/car-detail/{clue_id}.html",
                tags=[],
            ))

    _log.debug("regex fallback found %d cars", len(cars))
    return cars


# ── Detail page parsing ────────────────────────────────────────


def parse_detail(html: str, car_id: str) -> CarDetail:
    """Parse car detail from guazi.com detail page HTML (RSC data)."""

    # Try RSC JSON extraction first
    json_objects = _extract_rsc_json_objects(html)

    detail_data: dict = {}
    commodity_info: dict = {}
    record_info: dict = {}

    for obj in json_objects:
        # Look for carCommodityInfo (basic info)
        for found in _find_in_nested(obj, "carCommodityInfo", max_depth=5):
            if isinstance(found, dict) and found:
                commodity_info = found
                _log.debug("found carCommodityInfo keys=%s", list(found.keys())[:20])

        # Look for carRecordInfo (registration/transfer history)
        for found in _find_in_nested(obj, "carRecordInfo", max_depth=5):
            if isinstance(found, dict) and found:
                record_info = found

        # Look for detail top-level
        for found in _find_in_nested(obj, "detail", max_depth=3):
            if isinstance(found, dict) and found:
                detail_data = found

    # If we found detail_data, look inside it
    if detail_data and not commodity_info:
        commodity_info = detail_data.get("carCommodityInfo") or {}
        record_info = detail_data.get("carRecordInfo") or {}

    if commodity_info:
        return _rsc_detail_to_car(commodity_info, record_info, car_id)

    # Fallback: regex extraction from raw RSC stream
    _log.debug("RSC JSON extraction failed for detail, trying regex")
    return _parse_detail_regex(html, car_id)


def _rsc_detail_to_car(
    commodity: dict, record: dict, car_id: str
) -> CarDetail:
    """Build CarDetail from RSC commodity/record info."""
    title = commodity.get("title") or commodity.get("carName") or ""

    # Price
    price_str = ""
    price_info = commodity.get("priceArea") or commodity.get("purchasePrice") or {}
    if isinstance(price_info, dict):
        price_str = price_info.get("priceString") or ""
    if not price_str:
        price_str = str(commodity.get("price") or "")
    price = _parse_wan_price(price_str)

    # Mileage
    road_haul = commodity.get("roadHaul") or ""
    mileage = _parse_wan_km(road_haul)

    # Basic fields
    license_date = commodity.get("licenseDate") or ""
    model_year = ""
    yr_m = re.search(r'(\d{4})', license_date)
    if yr_m:
        model_year = yr_m.group(1)

    city = commodity.get("carSourceCityDesc") or ""

    # Core config: parse carCoreConfigItemList
    core_configs = commodity.get("carCoreConfigItemList") or []
    config_map: dict[str, str] = {}
    for cfg in core_configs:
        if isinstance(cfg, dict):
            name = cfg.get("name") or cfg.get("configName") or ""
            value = cfg.get("value") or cfg.get("configValue") or ""
            if name and value:
                config_map[name] = value

    _log.debug("core config map=%s", config_map)

    transmission = config_map.get("变速箱") or config_map.get("变速器") or ""
    fuel_type = config_map.get("燃料类型") or config_map.get("燃油类型") or ""
    displacement = config_map.get("排量") or ""
    engine_power = config_map.get("最大马力") or config_map.get("发动机") or ""
    emission_standard = config_map.get("排放标准") or ""
    body_type = config_map.get("车身类型") or config_map.get("车辆类型") or ""
    drive_type = config_map.get("驱动方式") or ""
    color = config_map.get("车身颜色") or config_map.get("颜色") or ""

    # Record info
    transfer_count = ""
    if record:
        transfer_count = str(record.get("transferCount") or record.get("transfer_count") or "")

    # Images
    images: list[str] = []
    img_list = commodity.get("imageList") or commodity.get("images") or []
    for img in img_list[:10]:
        if isinstance(img, dict):
            url = img.get("url") or img.get("src") or img.get("imageUrl") or ""
            if url:
                images.append(url)
        elif isinstance(img, str) and img:
            images.append(img)

    return CarDetail(
        id=car_id,
        platform="guazi",
        title=title,
        price=price,
        model_year=model_year,
        mileage=mileage,
        first_reg_date=license_date,
        transmission=transmission,
        displacement=displacement,
        city=city,
        color=color,
        url=f"https://www.guazi.com/car-detail/{car_id}.html",
        tags=[],
        description="",
        emission_standard=emission_standard,
        engine_power=engine_power,
        fuel_type=fuel_type,
        body_type=body_type,
        drive_type=drive_type,
        license_plate="",
        transfer_count=transfer_count,
        images=images,
    )


def _parse_detail_regex(html: str, car_id: str) -> CarDetail:
    """Fallback regex-based detail parser for RSC stream."""
    # Find a reference point in the raw HTML (field names are escaped in RSC)
    # Search for both escaped and unescaped variants
    idx = -1
    for needle in ["carSourceCityDesc", "priceString", "roadHaul", "licenseDate"]:
        idx = html.find(needle)
        if idx >= 0:
            break
        # Try escaped variant
        escaped = needle.replace('"', '\\"')
        idx = html.find(escaped)
        if idx >= 0:
            break

    if idx >= 0:
        start = max(0, idx - 5000)
        end = min(len(html), idx + 10000)
        text = _strip_rsc_escaping(html[start:end])
    else:
        # No reference point found — unescape a generous chunk
        chunk_size = min(len(html), 100000)
        text = _strip_rsc_escaping(html[:chunk_size])

    title = ""
    t_m = re.search(r'"title"\s*:\s*"([^"]{5,80})"', text)
    if t_m:
        title = t_m.group(1)

    price = 0.0
    p_m = re.search(r'"priceString"\s*:\s*"([^"]+)"', text)
    if p_m:
        price = _parse_wan_price(p_m.group(1))

    mileage = 0.0
    mil_m = re.search(r'"roadHaul"\s*:\s*"([^"]+)"', text)
    if mil_m:
        mileage = _parse_wan_km(mil_m.group(1))

    model_year = ""
    yr_m = re.search(r'"licenseDate"\s*:\s*"(\d{4})[^"]*"', text)
    if yr_m:
        model_year = yr_m.group(1)

    city = ""
    city_m = re.search(r'"carSourceCityDesc"\s*:\s*"([^"]+)"', text)
    if city_m:
        city = city_m.group(1)

    return CarDetail(
        id=car_id,
        platform="guazi",
        title=title,
        price=price,
        model_year=model_year,
        mileage=mileage,
        city=city,
        url=f"https://www.guazi.com/car-detail/{car_id}.html",
        tags=[],
    )


# ── Helpers ────────────────────────────────────────────────────


def _parse_wan_price(text: str) -> float:
    """Parse price string like '5.63万' to float (万元)."""
    if not text:
        return 0.0
    text = text.replace(",", "").replace("，", "")
    m = re.search(r'([\d.]+)', text)
    if m:
        val = float(m.group(1))
        # If text contains "万", value is already in 万
        if "万" in text:
            return val
        # If value > 1000, assume it's in 元
        if val > 1000:
            return val / 10000
        return val
    return 0.0


def _parse_wan_km(text: str) -> float:
    """Parse mileage string like '1.02万公里' to float (万公里)."""
    if not text:
        return 0.0
    m = re.search(r'([\d.]+)\s*万', text)
    if m:
        return float(m.group(1))
    # Maybe just a number in km
    m = re.search(r'([\d.]+)', text)
    if m:
        val = float(m.group(1))
        if val > 100:  # probably raw km
            return val / 10000
        return val
    return 0.0
