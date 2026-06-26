"""HTML parsing logic for che168.com (汽车之家) used car pages.

che168 serves SSR HTML with no __NEXT_DATA__ JSON.

List page structure (verified 2026-03):
    <ul class="viewlist_ul">
      <li class="cards-li ..." infoid="57815088" carname="..." price="16.8"
          milage="4" regdate="2021/03" dealerid="98140" ...>
        <a href="/dealer/{dealerid}/{infoid}.html?..." class="carinfo">
          <h4 class="card-name">Title</h4>
          <p class="cards-unit">4万公里／2021-03／北京／14年黄金会员</p>
          <span class="pirce"><em>16.80</em>万</span>
        </a>
      </li>

    The <li> data attributes are the most reliable extraction source.

Detail page: spec key-value pairs in various HTML patterns.
"""

import re
from html import unescape

from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail

_log = get_logger("che168.parser")


# ── Series extraction ──────────────────────────────────────────


def extract_series_list(html: str, brand_slug: str) -> list[dict[str, str]]:
    """Extract available series from a brand-filtered listing page.

    Returns list of {"series_slug": "baoma3xi", "series_name": "宝马3系"}.
    Series links live in the filter bar as:
        <a href="/{city}/{brand}/{series}/#pvareaid=...">宝马3系</a>
    """
    result: list[dict[str, str]] = []
    seen: set[str] = set()

    # Match links under the brand path; href may contain #fragment anchors
    pattern = re.compile(
        rf'href="/[^/]+/{re.escape(brand_slug)}/([^/#"]+)/?[^"]*"[^>]*>([^<]+)</a>',
        re.IGNORECASE,
    )
    for m in pattern.finditer(html):
        slug = m.group(1).strip()
        name = _clean(m.group(2))
        if not slug or not name or slug in seen:
            continue
        # Skip non-series links (pagination, price filters, etc.)
        if re.match(r'^a\d+_', slug) or slug in ("list",):
            continue
        seen.add(slug)
        result.append({"series_slug": slug, "series_name": name})

    _log.debug("extracted %d series for brand_slug=%s", len(result), brand_slug)
    return result


# ── List page parsing ──────────────────────────────────────────


def parse_list(html: str, city: str) -> list[Car]:
    """Parse car list from che168.com listing page HTML."""
    # Strategy 1 (primary): extract from <li> data attributes
    cars = _parse_li_attributes(html, city)
    if cars:
        _log.debug("li-attr parse yielded %d cars", len(cars))
        return cars

    # Strategy 2 (fallback): regex on <a> cards
    _log.debug("li-attr empty, trying card regex")
    cars = _parse_card_regex(html, city)
    _log.debug("card regex total cars=%d", len(cars))
    return cars


def _parse_li_attributes(html: str, city: str) -> list[Car]:
    """Parse cars from <li> element data attributes.

    Each <li class="cards-li ..."> has attributes:
        infoid, carname, price, milage, regdate, dealerid, brandid, seriesid, cid, pid
    """
    cars: list[Car] = []
    seen: set[str] = set()

    # Match <li> with infoid attribute
    li_pattern = re.compile(
        r'<li[^>]*\sinfoid="(\d+)"[^>]*>',
        re.DOTALL,
    )
    for m in li_pattern.finditer(html):
        info_id = m.group(1)
        if info_id in seen:
            continue
        seen.add(info_id)

        li_tag = m.group(0)

        carname = _attr(li_tag, "carname")
        price_str = _attr(li_tag, "price")
        milage_str = _attr(li_tag, "milage")
        regdate = _attr(li_tag, "regdate")
        dealer_id = _attr(li_tag, "dealerid")

        # ID format: {dealer_id}_{info_id} so detail can reconstruct the URL
        car_id = f"{dealer_id}_{info_id}" if dealer_id else info_id

        price = float(price_str) if price_str else 0.0

        mileage = 0.0
        if milage_str:
            try:
                mileage = float(milage_str)
            except ValueError:
                pass

        model_year = ""
        if regdate:
            yr_m = re.search(r'(\d{4})', regdate)
            if yr_m:
                model_year = yr_m.group(1)

        # Extract tags from the card HTML following this <li>
        li_end = html.find("</li>", m.end())
        card_html = html[m.start():li_end] if li_end > 0 else ""

        tags: list[str] = []
        for tag_m in re.finditer(r'class="text">([^<]+)</span>', card_html):
            tags.append(tag_m.group(1))

        # Determine city from cards-unit metadata or default
        car_city = city
        unit_m = re.search(r'class="cards-unit"[^>]*>([^<]+)', card_html)
        if unit_m:
            parts = re.split(r'[／/]', unit_m.group(1))
            for part in parts:
                part = part.strip()
                if re.match(r'^[\u4e00-\u9fff]{2,4}$', part):
                    car_city = part
                    break

        href = f"/dealer/{dealer_id}/{info_id}.html" if dealer_id else f"/dealer/0/{info_id}.html"

        if carname or price:
            cars.append(Car(
                id=car_id,
                platform="che168",
                title=carname,
                price=price,
                model_year=model_year,
                mileage=mileage,
                first_reg_date=regdate.replace("/", "-") if regdate else "",
                city=car_city,
                url=f"https://www.che168.com{href}",
                tags=tags,
            ))

    return cars


def _parse_card_regex(html: str, city: str) -> list[Car]:
    """Fallback: parse from <a> card links with surrounding context."""
    cars: list[Car] = []
    seen: set[str] = set()

    # href may contain query params after .html
    for m in re.finditer(r'href="(/dealer/(\d+)/(\d+)\.html)[^"]*"', html):
        dealer_id = m.group(2)
        info_id = m.group(3)
        car_id = f"{dealer_id}_{info_id}"
        if car_id in seen:
            continue
        seen.add(car_id)
        href = m.group(1)

        start = max(0, m.start() - 500)
        end = min(len(html), m.end() + 3000)
        context = html[start:end]

        title = ""
        t_m = re.search(r'<h4[^>]*>(?:<[^>]*>)*([^<]+)', context)
        if not t_m:
            t_m = re.search(r'title="([^"]{5,60})"', context)
        if t_m:
            title = _clean(t_m.group(1))

        price = 0.0
        p_m = re.search(r'<em>(\d+\.?\d*)</em>', context)
        if p_m:
            price = _parse_price(p_m.group(1))

        mileage = 0.0
        model_year = ""
        car_city = city
        unit_m = re.search(r'class="cards-unit"[^>]*>([^<]+)', context)
        if unit_m:
            mileage, model_year, car_city = _parse_meta(unit_m.group(1), city)
        else:
            mil_m = re.search(r'([\d.]+)万公里', context)
            if mil_m:
                mileage = float(mil_m.group(1))
            yr_m = re.search(r'(\d{4})-(\d{2})', context)
            if yr_m:
                model_year = yr_m.group(1)

        if title or price:
            cars.append(Car(
                id=car_id,
                platform="che168",
                title=title,
                price=price,
                model_year=model_year,
                mileage=mileage,
                city=car_city,
                url=f"https://www.che168.com{href}",
                tags=[],
            ))

    return cars


def _attr(tag: str, name: str) -> str:
    """Extract attribute value from an HTML tag string."""
    m = re.search(rf'{name}="([^"]*)"', tag)
    return m.group(1) if m else ""


# ── Detail page parsing ────────────────────────────────────────


def parse_detail(html: str, car_id: str) -> CarDetail:
    """Parse car detail from che168 detail page HTML."""
    # Title: car-brand-name class, <title> meta, or brandText
    title = ""
    # Strategy 1: car-brand-name element (may have nested tags)
    t_m = re.search(r'class="[^"]*car-brand-name[^"]*"[^>]*>(.*?)</[^>]+>', html, re.DOTALL)
    if t_m:
        title = _strip_tags(t_m.group(1)).strip()
    # Strategy 2: <title> tag — format: 【城市】标题_价格_二手车之家
    if not title:
        t_m = re.search(r'<title>(?:【[^】]*】)?(.+?)[_|<]', html)
        if t_m:
            title = _clean(t_m.group(1))
    if title:
        title = re.sub(r'\s*[-_|].*$', '', title)

    # Price: ¥X.XX万 inside span.price
    price = 0.0
    p_m = re.search(r'[¥￥]\s*(\d+\.?\d*)\s*(?:<[^>]*>)?\s*万', html)
    if not p_m:
        p_m = re.search(r'class="[^"]*price[^"]*"[^>]*>.*?(\d+\.?\d*)\s*万', html, re.DOTALL)
    if p_m:
        price = _parse_price(p_m.group(1))

    # Spec key-value pairs from 车辆档案 section
    specs = _extract_specs(html)
    _log.debug("detail specs=%s", specs)

    mileage = 0.0
    for key in ("表显里程", "里程"):
        if key in specs:
            mil_m = re.search(r'([\d.]+)', specs[key])
            if mil_m:
                mileage = float(mil_m.group(1))
            break

    first_reg = specs.get("上牌时间", "") or specs.get("首次上牌", "")
    transmission = specs.get("变速箱", "")
    displacement = specs.get("排量", "")
    engine = specs.get("发动机", "")
    emission = specs.get("排放标准", "")
    fuel_label = specs.get("燃油标号", "")
    fuel_type = specs.get("燃油类型", "") or specs.get("燃料类型", "") or fuel_label
    body_type = specs.get("车辆级别", "") or specs.get("车身类型", "")
    drive_type = specs.get("驱动方式", "")
    color = specs.get("车身颜色", "") or specs.get("颜色", "")
    transfer_count = specs.get("过户次数", "")
    annual_inspection = specs.get("年检到期", "")
    insurance_expiry = specs.get("保险到期", "") or specs.get("交强险到期", "")
    city = specs.get("所在地", "") or specs.get("车源地", "")

    # Images
    images: list[str] = re.findall(
        r'(?:data-src|src)="(https?://[^"]+(?:\.jpg|\.png|\.webp)[^"]*)"',
        html,
    )[:10]

    # Description / seller remark
    description = ""
    desc_m = re.search(
        r'class="[^"]*(?:seller-remark|car-desc|describe)[^"]*"[^>]*>(.*?)</div>',
        html,
        re.DOTALL,
    )
    if desc_m:
        description = _strip_tags(desc_m.group(1)).strip()[:500]

    # car_id format: {dealer_id}_{info_id}
    if "_" in car_id:
        d_id, i_id = car_id.split("_", 1)
        detail_url = f"https://www.che168.com/dealer/{d_id}/{i_id}.html"
    else:
        detail_url = f"https://www.che168.com/dealer/0/{car_id}.html"

    return CarDetail(
        id=car_id,
        platform="che168",
        title=title,
        price=price,
        mileage=mileage,
        first_reg_date=first_reg,
        transmission=transmission,
        displacement=displacement or engine,
        city=city,
        color=color,
        url=detail_url,
        tags=[],
        description=description,
        emission_standard=emission,
        fuel_type=fuel_type,
        body_type=body_type,
        drive_type=drive_type,
        license_plate="",
        transfer_count=transfer_count,
        annual_inspection=annual_inspection,
        insurance_expiry=insurance_expiry,
        images=images,
    )


def _extract_specs(html: str) -> dict[str, str]:
    """Extract key-value spec pairs from che168 detail page.

    The 车辆档案 section uses a text layout where labels contain CJK spaces
    for alignment. We extract by stripping all HTML tags from the archive
    section and parsing "LabelValue" pairs where Label is CJK characters
    (possibly with spaces) and Value follows immediately.
    """
    specs: dict[str, str] = {}

    # Primary: extract from 车辆档案 / all-basic-content section text
    archive_m = re.search(
        r'class="[^"]*all-basic-content[^"]*"[^>]*>(.*?)</div>\s*</div>',
        html,
        re.DOTALL,
    )
    if not archive_m:
        archive_m = re.search(r'车辆档案(.*?)</div>\s*</div>', html, re.DOTALL)

    if archive_m:
        section_text = _strip_tags(archive_m.group(1))
        _parse_archive_text(section_text, specs)

    # Fallback: dt/dd pairs (city selector etc. will also match, filter by key length)
    if not specs:
        for m in re.finditer(
            r'<dt[^>]*>([^<]+)</dt>\s*<dd[^>]*>([^<]+)</dd>',
            html,
        ):
            key = _clean(m.group(1))
            val = _clean(m.group(2))
            if key and val and len(key) <= 10 and key not in specs:
                specs[key] = val

    # Fallback: li with two p children
    for m in re.finditer(
        r'<li[^>]*>\s*<p[^>]*>([^<]+)</p>\s*<p[^>]*>([^<]+)</p>',
        html,
    ):
        key = _clean(m.group(1))
        val = _clean(m.group(2))
        if key and val and len(key) <= 10 and key not in specs:
            specs[key] = val

    return specs


_ARCHIVE_KEYS = [
    "上牌时间", "表显里程", "变速箱", "排放标准", "排量", "发布时间",
    "年检到期", "保险到期", "交强险到期", "质保到期", "过户次数",
    "所在地", "发动机", "车辆级别", "车身颜色", "燃油标号", "驱动方式",
    "燃油类型", "燃料类型", "车身类型",
]


def _parse_archive_text(text: str, specs: dict[str, str]):
    """Parse the flattened text of the 车辆档案 section.

    The text looks like: "上牌时间2018年01月 表显里程9.19万公里 变速箱自动 ..."
    Labels may have spaces for alignment (e.g. "变  速  箱").
    """
    # Normalize: collapse internal spaces within CJK labels
    normalized = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', text)
    normalized = normalized.strip()

    for key in _ARCHIVE_KEYS:
        idx = normalized.find(key)
        if idx == -1:
            continue
        val_start = idx + len(key)
        # Value extends until the next known key or end of string
        val_end = len(normalized)
        for other_key in _ARCHIVE_KEYS:
            if other_key == key:
                continue
            other_idx = normalized.find(other_key, val_start)
            if other_idx != -1 and other_idx < val_end:
                val_end = other_idx

        # Also stop at common non-spec text
        for stop in ("出险查询", "维修保养", "更多", "全部参数", "查看"):
            stop_idx = normalized.find(stop, val_start)
            if stop_idx != -1 and stop_idx < val_end:
                val_end = stop_idx

        val = normalized[val_start:val_end].strip()
        if val and key not in specs:
            specs[key] = val


# ── Helpers ────────────────────────────────────────────────────


def _parse_price(text: str) -> float:
    """Parse price string to float (万元). che168 prices are displayed in 万."""
    if not text:
        return 0.0
    text = text.replace(",", "").replace("，", "").replace("万", "")
    m = re.search(r'([\d.]+)', text)
    if m:
        return float(m.group(1))
    return 0.0


def _parse_meta(text: str, default_city: str) -> tuple[float, str, str]:
    """Parse metadata string like '8.9万公里／2015-07／北京／14年黄金会员'.

    Returns (mileage_wan_km, model_year, city).
    """
    mileage = 0.0
    model_year = ""
    city = default_city

    parts = re.split(r'[／/|·]', text)
    for part in parts:
        part = part.strip()
        mil_m = re.search(r'([\d.]+)\s*万公里', part)
        if mil_m:
            mileage = float(mil_m.group(1))
            continue
        yr_m = re.search(r'(\d{4})', part)
        if yr_m and not model_year:
            model_year = yr_m.group(1)
            continue
        if re.match(r'^[\u4e00-\u9fff]{2,4}$', part):
            city = part

    return mileage, model_year, city


def _clean(text: str) -> str:
    return unescape(text).strip()


def _strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
