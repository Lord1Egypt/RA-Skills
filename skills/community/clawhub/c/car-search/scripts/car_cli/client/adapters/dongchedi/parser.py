"""HTML and JSON parsing logic for dongchedi.com used car pages."""

import json
import re
from html import unescape

from car_cli.client.adapters.dongchedi.font_decoder import decode_text, decode_number
from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail

_log = get_logger("dongchedi.parser")


def try_extract_next_data(html: str) -> dict | None:
    """Extract __NEXT_DATA__ JSON from Next.js SSR pages."""
    marker = '__NEXT_DATA__'
    idx = html.find(marker)
    if idx == -1:
        _log.debug("__NEXT_DATA__ marker not found in html")
        return None

    start = html.find('>', idx)
    if start == -1:
        _log.debug("__NEXT_DATA__ closing '>' not found")
        return None
    start += 1

    end = html.find('</script>', start)
    if end == -1:
        _log.debug("__NEXT_DATA__ closing </script> not found")
        return None

    raw = html[start:end].strip()
    _log.debug("__NEXT_DATA__ raw len=%s", len(raw))
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError) as e:
        _log.debug("__NEXT_DATA__ JSON parse failed: %s", e)
        return None


def extract_series_list(html: str) -> list[dict[str, str]]:
    """Extract available series from a brand-filtered listing page.

    Returns list of {"series_id": "145", "series_name": "宝马3系"}.
    The data lives in __NEXT_DATA__ > props.pageProps.seriesList.
    """
    data = try_extract_next_data(html)
    if not data:
        return []

    try:
        props = data.get("props", {}).get("pageProps", {})
    except (AttributeError, TypeError):
        return []

    series_list = props.get("seriesList") or []
    if not isinstance(series_list, list):
        return []

    result: list[dict[str, str]] = []
    for item in series_list:
        if not isinstance(item, dict):
            continue
        sid = str(item.get("series_id") or "")
        name = item.get("series_name") or ""
        if sid and name:
            result.append({"series_id": sid, "series_name": name})

    _log.debug("extracted %d series from __NEXT_DATA__", len(result))
    return result


# ── List page parsing ──────────────────────────────────────────


def parse_list(html: str, city: str) -> list[Car]:
    cars: list[Car] = []

    json_data = try_extract_next_data(html)
    if json_data:
        _log.debug("parse path=__NEXT_DATA__")
        parsed = _parse_next_data_list(json_data, city)
        if parsed:
            _log.debug("__NEXT_DATA__ sku count=%s", len(parsed))
            return parsed
        _log.debug("__NEXT_DATA__ had no usable car list, falling through to HTML")

    _log.debug("parse path=html_cards")

    card_pattern = re.compile(
        r'<a[^>]*href="/usedcar/(\d{7,})"[^>]*class="[^"]*card[^"]*"[^>]*>(.*?)</a>',
        re.DOTALL,
    )
    for m in card_pattern.finditer(html):
        try:
            car = _parse_card(m.group(2), m.group(1), city)
            if car:
                cars.append(car)
        except Exception:
            continue

    if not cars:
        _log.debug("card_pattern empty, trying generic link scan")
        cars = _parse_cards_generic(html, city)

    _log.debug("html total cars=%s", len(cars))
    return cars


def _parse_next_data_list(data: dict, city: str) -> list[Car]:
    """Parse car list from __NEXT_DATA__ JSON structure.

    The live site (2026-03) puts brand/series metadata in
    ``pageProps.list`` (type 1000=ad, 1001=brand card).  Actual car
    listings are SSR-rendered into HTML but **not** stored under a
    simple ``skuList`` key.  We still probe multiple paths in case
    the site reverts to an older schema.
    """
    cars: list[Car] = []
    try:
        props = data.get("props", {}).get("pageProps", {})
    except (AttributeError, TypeError) as e:
        _log.debug("next_data pageProps navigation failed: %s", e)
        return cars

    _log.debug(
        "pageProps top keys=%s",
        list(props.keys())[:25] if isinstance(props, dict) else "n/a",
    )

    sku_list: list = []

    for candidate_path in (
        lambda p: p.get("carList"),
        lambda p: p.get("skuList"),
        lambda p: p.get("data", {}).get("skuList"),
        lambda p: p.get("data", {}).get("sku_list"),
        lambda p: (p.get("initialState") or {}).get("usedCarList", {}).get("skuList"),
    ):
        try:
            result = candidate_path(props)
            if result and isinstance(result, list) and len(result) > 0:
                sku_list = result
                break
        except (AttributeError, TypeError):
            continue

    _log.debug("sku_list len=%s", len(sku_list) if isinstance(sku_list, list) else "n/a")

    for item in sku_list:
        try:
            car = _sku_to_car(item, city)
            if car:
                cars.append(car)
        except Exception:
            continue
    return cars


def _sku_to_car(item: dict, city: str) -> Car | None:
    sku_id = str(item.get("sku_id") or item.get("id") or "")
    if not sku_id:
        return None

    title = item.get("title") or item.get("car_name") or ""
    title = decode_text(title)

    raw_price = item.get("sh_price") or item.get("price") or ""
    price = decode_number(str(raw_price)) if raw_price else 0.0
    if price and price > 1000:
        price = price / 10000  # convert 元 -> 万

    brand = item.get("brand_name") or ""
    series = item.get("series_name") or ""
    model_year = item.get("model_year") or ""

    raw_mileage = item.get("mileage") or ""
    mileage = decode_number(str(raw_mileage)) if raw_mileage else 0.0
    if mileage and mileage > 100:
        mileage = mileage / 10000  # convert km -> 万公里

    first_reg = item.get("first_registration_time") or item.get("first_reg_date") or ""
    transmission = item.get("gearbox") or item.get("transmission") or ""
    displacement = item.get("displacement") or ""
    color = item.get("color") or ""
    car_city = item.get("car_source_city_name") or city

    tags_raw = item.get("tags") or item.get("tag_list") or []
    tags = []
    if isinstance(tags_raw, list):
        for t in tags_raw:
            if isinstance(t, dict):
                tags.append(t.get("text") or t.get("name") or "")
            elif isinstance(t, str):
                tags.append(t)
    tags = [t for t in tags if t]

    return Car(
        id=sku_id,
        platform="dongchedi",
        title=title,
        price=price or 0.0,
        brand=brand,
        series=series,
        model_year=model_year,
        mileage=mileage or 0.0,
        first_reg_date=first_reg,
        transmission=transmission,
        displacement=displacement,
        city=car_city,
        color=color,
        url=f"https://www.dongchedi.com/usedcar/{sku_id}",
        tags=tags,
    )


def _parse_card(card_html: str, sku_id: str, city: str) -> Car | None:
    title = ""
    title_m = re.search(r'class="[^"]*title[^"]*"[^>]*>([^<]+)', card_html)
    if title_m:
        title = decode_text(_clean(title_m.group(1)))

    price = 0.0
    price_m = re.search(r'class="[^"]*price[^"]*"[^>]*>(.*?)</\w+>', card_html, re.DOTALL)
    if price_m:
        price = decode_number(_strip_tags(price_m.group(1))) or 0.0

    mileage = 0.0
    info_m = re.search(r'class="[^"]*info[^"]*"[^>]*>(.*?)</\w+>', card_html, re.DOTALL)
    info_text = ""
    if info_m:
        info_text = decode_text(_strip_tags(info_m.group(1)))

    segments = [s.strip() for s in re.split(r'[|/·]', info_text) if s.strip()]
    model_year = ""
    transmission = ""
    for seg in segments:
        if re.search(r'\d+\.\d+万公里', seg):
            m = re.search(r'([\d.]+)', seg)
            if m:
                mileage = float(m.group(1))
        elif re.search(r'\d{4}', seg):
            model_year = seg.strip()
        elif "自动" in seg or "手动" in seg or "AT" in seg or "MT" in seg:
            transmission = seg.strip()

    if not title and not price:
        return None

    return Car(
        id=sku_id,
        platform="dongchedi",
        title=title,
        price=price,
        brand="",
        series="",
        model_year=model_year,
        mileage=mileage,
        first_reg_date="",
        transmission=transmission,
        displacement="",
        city=city,
        color="",
        url=f"https://www.dongchedi.com/usedcar/{sku_id}",
        tags=[],
    )


def _parse_cards_generic(html: str, city: str) -> list[Car]:
    """Extract car data from SSR-rendered card HTML.

    Each card is an ``<a>`` with ``href="/usedcar/{sku_id}"``.  The
    surrounding HTML contains PUA-encoded price/mileage and plaintext
    title, transfer count, and city.
    """
    cars: list[Car] = []
    seen: set[str] = set()
    for m in re.finditer(r'href="/usedcar/(\d{7,})"', html):
        sku_id = m.group(1)
        if sku_id in seen:
            continue
        seen.add(sku_id)

        start = max(0, m.start() - 200)
        end = min(len(html), m.end() + 3500)
        context = html[start:end]

        title = ""
        t_m = re.search(r'title="([^"]+)"', context)
        if not t_m:
            t_m = re.search(r'alt="二手([^"]+)"', context)
        if t_m:
            title = decode_text(_clean(t_m.group(1)))

        price = 0.0
        price_m = re.search(
            r'tw-text-color-red[^"]*"[^>]*>([\s\S]*?)</dd>',
            context,
        )
        if price_m:
            price_text = _strip_tags(price_m.group(1)).split("新车指导价")[0]
            price = decode_number(price_text) or 0.0

        mileage = 0.0
        model_year = ""
        info_dd = re.search(
            r'<dd[^>]*font-\w+[^>]*>(.*?)</dd>',
            context,
            re.DOTALL,
        )
        if info_dd:
            decoded_info = decode_text(_strip_tags(info_dd.group(1)))
            parts = [p.strip() for p in decoded_info.split("|")]
            for part in parts:
                yr = re.search(r'(\d{4})', part)
                if yr and not model_year:
                    model_year = yr.group(1)
                mil = re.search(r'([\d.]+)\s*万', part)
                if mil and not mileage:
                    mileage = float(mil.group(1))

        transfer = ""
        tr_m = re.search(r'过户(\d+)次', context)
        if tr_m:
            transfer = tr_m.group(0)

        tags: list[str] = []
        if re.search(r'检测报告', context):
            tags.append("检测报告")
        if transfer:
            tags.append(transfer)

        if title or price:
            cars.append(Car(
                id=sku_id,
                platform="dongchedi",
                title=title,
                price=price,
                model_year=model_year,
                mileage=mileage,
                city=city,
                url=f"https://www.dongchedi.com/usedcar/{sku_id}",
                tags=tags,
            ))
    _log.debug("generic scan found %d unique sku links", len(seen))
    return cars


# ── Detail page parsing ────────────────────────────────────────


def parse_detail(html: str, car_id: str) -> CarDetail:
    json_data = try_extract_next_data(html)
    if json_data:
        detail = _parse_next_data_detail(json_data, car_id)
        if detail:
            _log.debug("detail parse path=__NEXT_DATA__")
            return detail
        _log.debug("detail __NEXT_DATA__ present but sku detail missing, fallback HTML")

    _log.debug("detail parse path=html")
    return _parse_detail_html(html, car_id)


def _parse_next_data_detail(data: dict, car_id: str) -> CarDetail | None:
    try:
        props = data.get("props", {}).get("pageProps", {})
        sku = (
            props.get("skuDetail")
            or props.get("data", {}).get("skuDetail")
            or props.get("data", {}).get("sku_detail")
            or props.get("data", {})
        )
        if not sku:
            return None
    except (AttributeError, TypeError):
        return None

    _log.debug(
        "skuDetail top keys=%s",
        list(sku.keys())[:30] if isinstance(sku, dict) else "n/a",
    )

    title = decode_text(str(sku.get("title") or sku.get("car_name") or ""))

    # Price: prefer source_sh_price (raw int, unit=元) over PUA-encoded sh_price
    price = 0.0
    source_price = sku.get("source_sh_price")
    if source_price and isinstance(source_price, (int, float)) and source_price > 0:
        price = source_price / 1000000  # 元 -> 万元 (divide by 100万)
        _log.debug("price from source_sh_price=%s -> %.2f万", source_price, price)
    else:
        raw_price = sku.get("sh_price") or sku.get("price") or 0
        price = decode_number(str(raw_price)) if raw_price else 0.0
        if price and price > 1000:
            price = price / 10000

    # Mileage / city / reg date: parse from important_text (plaintext summary)
    # Format: "2022年上牌 | 4.67万公里 | 北京车源"
    important_text = sku.get("important_text") or ""
    mileage = 0.0
    city = ""
    first_reg = ""

    if important_text:
        _log.debug("important_text=%r", important_text)
        mil_m = re.search(r'([\d.]+)\s*万公里', important_text)
        if mil_m:
            mileage = float(mil_m.group(1))
        city_m = re.search(r'[\|｜]\s*(\S+?)车源', important_text)
        if city_m:
            city = city_m.group(1)
        reg_m = re.search(r'(\d{4})\s*年上牌', important_text)
        if reg_m:
            first_reg = reg_m.group(1)

    # Fallback: mileage from car_info or direct field (PUA-encoded)
    if not mileage:
        car_info = sku.get("car_info") or {}
        raw_mileage = car_info.get("mileage") or sku.get("mileage") or 0
        mileage = decode_number(str(raw_mileage)) if raw_mileage else 0.0
        if mileage and mileage > 100:
            mileage = mileage / 10000

    # Fallback: try sh_car_desc for mileage ("【行驶里程】4.67万公里")
    if not mileage:
        sh_desc = sku.get("sh_car_desc") or ""
        mil_m = re.search(r'行驶里程[】\s]*([\d.]+)\s*万公里', sh_desc)
        if mil_m:
            mileage = float(mil_m.group(1))

    car_info = sku.get("car_info") or {}
    brand = sku.get("brand_name") or car_info.get("brand_name") or ""
    series = sku.get("series_name") or car_info.get("series_name") or ""
    model_year = sku.get("model_year") or str(car_info.get("year") or "")

    if not first_reg:
        first_reg = sku.get("first_registration_time") or ""

    if not city:
        city = sku.get("car_source_city_name") or ""

    # other_params: [{name, value}, ...] for transmission, displacement, color, etc.
    params: dict[str, str] = {}
    for item in sku.get("other_params") or []:
        if isinstance(item, dict) and "name" in item and "value" in item:
            params[item["name"]] = item["value"]

    _log.debug("other_params=%s", params)

    transmission = sku.get("gearbox") or sku.get("transmission") or params.get("变速箱") or ""
    displacement = sku.get("displacement") or params.get("排量") or ""
    color = sku.get("color") or car_info.get("body_color") or params.get("车身颜色") or ""
    transfer_count = str(sku.get("transfer_count") or params.get("过户次数") or "")
    license_plate = sku.get("license_city") or params.get("上牌地") or ""

    if not first_reg and params.get("上牌时间"):
        first_reg = params["上牌时间"]

    # car_config_overview for fuel_type, drive_type, engine_power
    config = sku.get("car_config_overview") or {}
    power_cfg = config.get("power") or {}
    manip_cfg = config.get("manipulation") or {}

    fuel_type = sku.get("fuel_type") or power_cfg.get("fuel_form") or ""
    drive_type = sku.get("drive_type") or manip_cfg.get("driver_form") or ""
    engine_power = sku.get("engine_power") or ""
    emission_standard = sku.get("emission_standard") or params.get("排放标准") or ""

    images = []
    img_list = sku.get("images") or sku.get("image_list") or []
    for img in img_list[:10]:
        if isinstance(img, dict):
            images.append(img.get("url") or img.get("src") or "")
        elif isinstance(img, str):
            images.append(img)
    images = [u for u in images if u]

    return CarDetail(
        id=car_id,
        platform="dongchedi",
        title=title,
        price=price or 0.0,
        brand=brand,
        series=series,
        model_year=model_year,
        mileage=mileage or 0.0,
        first_reg_date=first_reg,
        transmission=transmission,
        displacement=displacement,
        city=city,
        color=color,
        url=f"https://www.dongchedi.com/usedcar/{car_id}",
        tags=[],
        description=sku.get("description") or sku.get("seller_remark") or "",
        emission_standard=emission_standard,
        engine_power=engine_power,
        fuel_type=fuel_type,
        body_type=sku.get("body_type") or "",
        drive_type=drive_type,
        seats=sku.get("seats"),
        license_plate=license_plate,
        transfer_count=transfer_count,
        annual_inspection=sku.get("annual_inspection") or "",
        insurance_expiry=sku.get("insurance_expiry") or "",
        images=images,
        price_history=[],
    )


def _parse_detail_html(html: str, car_id: str) -> CarDetail:
    title = ""
    title_m = re.search(r'<h1[^>]*>([^<]+)', html)
    if not title_m:
        title_m = re.search(r'<title>([^<]+)', html)
    if title_m:
        title = decode_text(_clean(title_m.group(1)))

    price = 0.0
    price_m = re.search(
        r'class="[^"]*price[^"]*"[^>]*>(.*?)</\w+>', html, re.DOTALL
    )
    if price_m:
        price = decode_number(_strip_tags(price_m.group(1))) or 0.0

    mileage = 0.0
    mileage_m = re.search(r'里程.*?([\d\ue000-\uf8ff,.]+)\s*万公里', html)
    if mileage_m:
        mileage = decode_number(mileage_m.group(1)) or 0.0

    first_reg = ""
    reg_m = re.search(r'首次上牌.*?(\d{4}[-/年]\d{1,2})', html)
    if reg_m:
        first_reg = reg_m.group(1)

    transmission = ""
    trans_m = re.search(r'变速箱.*?([^<\s]+)', html)
    if trans_m:
        transmission = _clean(trans_m.group(1))

    displacement = ""
    disp_m = re.search(r'排量.*?([^<\s]+)', html)
    if disp_m:
        displacement = _clean(disp_m.group(1))

    emission = ""
    emis_m = re.search(r'排放标准.*?([^<\s]+)', html)
    if emis_m:
        emission = _clean(emis_m.group(1))

    description = ""
    desc_m = re.search(r'class="[^"]*description[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    if desc_m:
        description = _strip_tags(desc_m.group(1)).strip()[:500]

    images: list[str] = re.findall(
        r'(?:data-src|src)="(https?://[^"]+(?:\.jpg|\.png|\.webp)[^"]*)"', html
    )[:10]

    return CarDetail(
        id=car_id,
        platform="dongchedi",
        title=title,
        price=price,
        city="",
        url=f"https://www.dongchedi.com/usedcar/{car_id}",
        mileage=mileage,
        first_reg_date=first_reg,
        transmission=transmission,
        displacement=displacement,
        emission_standard=emission,
        description=description,
        images=images,
        tags=[],
    )


# ── Helpers ────────────────────────────────────────────────────


def _clean(text: str) -> str:
    return unescape(text).strip()


def _strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
