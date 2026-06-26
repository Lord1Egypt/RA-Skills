"""
万能反爬 Skill - 懂车帝（dongchedi.com）车辆信息采集
目标: 采集二手车列表和详情页，输出统一 VehicleInfo 格式

懂车帝反爬特点:
- 大量数据通过 SSR + hydration 渲染（window.__INITIAL_STATE__）
- 二手车频道使用 API 接口返回 JSON
- 有较强的设备指纹检测和请求频次限制
- 部分接口需要签名参数（_signature）
"""

import re
import json
import time
import hashlib
import logging
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config import DONGCHEDI_CONFIG, REQUEST_TIMEOUT, MAX_RETRIES
from data_models import VehicleInfo, ScrapeResult
from anti_detect import (
    build_headers,
    RateLimiter,
    CookieManager,
    detect_block,
    generate_device_fingerprint,
    generate_trace_id,
)

logger = logging.getLogger("dongchedi_scraper")


class DongchediScraper:
    """
    懂车帝车辆信息采集器

    采集策略:
    1. 初始化会话获取基础 Cookie
    2. 通过二手车 API 接口获取列表数据
    3. 通过详情页提取内嵌 JSON 数据（__INITIAL_STATE__）
    4. 全部数据转为统一 VehicleInfo

    反爬对策:
    - 需要首次加载主页获取 ttwid / __ac_nonce 等 Cookie
    - 请求间隔不低于 3 秒
    - User-Agent 与 sec-ch-ua 保持一致
    - 接口请求附带 device_platform / aid 等参数
    """

    # 懂车帝二手车 API (Web端)
    API_LIST = "https://www.dongchedi.com/motor/pc/car/series/used_car_list"

    def __init__(self):
        self.config = DONGCHEDI_CONFIG
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(min_delay=3.0, max_delay=6.0)
        self.cookie_mgr = CookieManager()
        self._device_fp = generate_device_fingerprint()

    def _request(
        self, url: str,
        referer: Optional[str] = None,
        params: Optional[dict] = None,
        is_api: bool = False,
        **kwargs,
    ) -> Optional[requests.Response]:
        """带反爬保护的请求"""
        self.rate_limiter.wait()

        extra_headers = dict(self.config.extra_headers)
        if is_api:
            extra_headers.update({
                "Accept": "application/json, text/plain, */*",
                "X-Requested-With": "XMLHttpRequest",
            })

        headers = build_headers(
            url, referer=referer, extra=extra_headers,
        )

        for attempt in range(MAX_RETRIES):
            try:
                resp = self.session.get(
                    url, headers=headers, params=params,
                    timeout=REQUEST_TIMEOUT, **kwargs,
                )

                is_blocked, reason = detect_block(resp.status_code, resp.text)
                if is_blocked:
                    logger.warning(f"被拦截 [{reason}]: {url} (尝试 {attempt+1}/{MAX_RETRIES})")
                    self.rate_limiter.increase_backoff()
                    self.rate_limiter.wait()
                    continue

                self.rate_limiter.reset_backoff()
                self.cookie_mgr.update_cookies("dongchedi.com", dict(resp.cookies))
                return resp

            except requests.RequestException as e:
                logger.error(f"请求异常: {url} - {e}")
                if attempt < MAX_RETRIES - 1:
                    self.rate_limiter.wait()

        return None

    def _init_session(self):
        """初始化: 访问首页获取必要 Cookie"""
        logger.info("初始化懂车帝会话...")
        resp = self._request(self.config.base_url)
        if resp:
            logger.info(f"懂车帝会话初始化成功, Cookies: {list(self.session.cookies.keys())}")

        # 访问二手车频道获取额外 Cookie
        self.rate_limiter.wait()
        self._request(
            "https://www.dongchedi.com/usedcar",
            referer=self.config.base_url,
        )

    def scrape_list_api(self, page: int = 0, city_name: str = "", count: int = 20) -> list[dict]:
        """
        通过 API 接口采集列表

        懂车帝二手车 Web 端接口参数:
        - page: 页码 (从0开始)
        - count: 每页条数
        - city_name: 城市名 (可空，表示全国)
        """
        params = {
            "page": page,
            "count": count,
            "aid": "1839",
            "app_name": "auto_web_pc",
        }
        if city_name:
            params["city_name"] = city_name

        resp = self._request(
            self.API_LIST,
            referer="https://www.dongchedi.com/usedcar",
            params=params,
            is_api=True,
        )

        if not resp:
            return []

        try:
            data = resp.json()
        except json.JSONDecodeError:
            logger.error("懂车帝 API 返回非 JSON")
            return []

        if data.get("status") != 0 and data.get("code") != 0:
            logger.warning(f"懂车帝 API 异常: {data.get('message', 'unknown')}")
            return []

        raw_list = data.get("data", {}).get("car_source_list", [])
        if not raw_list:
            raw_list = data.get("data", {}).get("list", [])

        cars = []
        for item in raw_list:
            cars.append(self._parse_api_item(item))

        logger.info(f"懂车帝 API 第{page}页: {len(cars)} 辆车")
        return cars

    def scrape_list_html(self, page: int = 1) -> list[dict]:
        """
        备用: 通过 HTML 列表页采集（当 API 不可用时降级使用）
        """
        url = f"{self.config.list_url}?page={page}"
        resp = self._request(url, referer=self.config.base_url)
        if not resp:
            return []

        # 懂车帝 SSR 通常在 script 中内嵌数据
        data = self._extract_ssr_data(resp.text)
        if data:
            car_list = (
                data.get("usedCarData", {}).get("carList", []) or
                data.get("data", {}).get("list", [])
            )
            return [self._parse_api_item(item) for item in car_list]

        # 纯 HTML 降级解析
        soup = BeautifulSoup(resp.text, "html.parser")
        cars = []
        for card in soup.select("[class*='car-item'], [class*='vehicle-card'], [class*='used-car']"):
            parsed = self._parse_html_card(card)
            if parsed:
                cars.append(parsed)

        logger.info(f"懂车帝 HTML 第{page}页: {len(cars)} 辆车")
        return cars

    def _parse_api_item(self, item: dict) -> dict:
        """解析 API 返回的列表项"""
        car_info = item.get("car_info", item)
        return {
            "id": str(car_info.get("id", car_info.get("car_source_id", ""))),
            "title": car_info.get("title", car_info.get("car_name", "")),
            "price": self._safe_float(car_info.get("price", 0)) / 10000 if car_info.get("price", 0) > 1000 else self._safe_float(car_info.get("price", 0)),
            "original_price": self._safe_float(car_info.get("new_car_price", car_info.get("guide_price", 0))),
            "mileage": car_info.get("mileage", car_info.get("mileage_str", "")),
            "year": car_info.get("year", car_info.get("reg_year", "")),
            "plate_date": car_info.get("reg_date", car_info.get("plate_date", "")),
            "brand": car_info.get("brand_name", ""),
            "series": car_info.get("series_name", ""),
            "city": car_info.get("city_name", ""),
            "thumbnail": car_info.get("cover_image", car_info.get("image", "")),
            "url": car_info.get("detail_url", ""),
            "tags": car_info.get("tags", []),
            "transmission": car_info.get("gearbox", car_info.get("transmission", "")),
            "displacement": car_info.get("displacement", ""),
        }

    def _parse_html_card(self, card) -> Optional[dict]:
        """解析 HTML 卡片"""
        try:
            link = card.select_one("a[href]")
            title_el = card.select_one("[class*='title'], [class*='name'], h3")
            price_el = card.select_one("[class*='price']")
            img_el = card.select_one("img")

            href = link["href"] if link and link.get("href") else ""
            car_id = re.search(r'/(\d+)', href)

            return {
                "id": car_id.group(1) if car_id else "",
                "title": title_el.get_text(strip=True) if title_el else "",
                "price": self._extract_price(price_el.get_text(strip=True)) if price_el else 0,
                "thumbnail": img_el.get("src", img_el.get("data-src", "")) if img_el else "",
                "url": href,
            }
        except Exception as e:
            logger.debug(f"HTML卡片解析失败: {e}")
            return None

    def scrape_detail(self, car_id: str, detail_url: str = "") -> Optional[VehicleInfo]:
        """
        采集详情页
        懂车帝详情页以 SSR 数据为主，优先提取 __INITIAL_STATE__
        """
        if not detail_url:
            detail_url = self.config.detail_url_pattern.format(car_id=car_id)
        if detail_url.startswith("/"):
            detail_url = self.config.base_url + detail_url

        resp = self._request(detail_url, referer="https://www.dongchedi.com/usedcar")
        if not resp:
            return None

        vehicle = VehicleInfo(
            source="dongchedi",
            source_id=car_id,
            source_url=detail_url,
            scraped_at=datetime.now().isoformat(),
        )

        # 优先提取 SSR JSON 数据
        ssr_data = self._extract_ssr_data(resp.text)
        if ssr_data:
            self._fill_from_ssr(vehicle, ssr_data)
            return vehicle

        # 降级 HTML 解析
        soup = BeautifulSoup(resp.text, "html.parser")
        self._fill_from_html(vehicle, soup)
        return vehicle

    def _extract_ssr_data(self, html: str) -> Optional[dict]:
        """提取 SSR 内嵌数据"""
        patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*;?\s*</script>',
            r'window\._SSR_DATA\s*=\s*({.+?})\s*;?\s*</script>',
            r'<script[^>]*>\s*window\.__NEXT_DATA__\s*=\s*({.+?})\s*;?\s*</script>',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue
        return None

    def _fill_from_ssr(self, vehicle: VehicleInfo, data: dict):
        """从 SSR 数据填充车辆信息"""
        # 懂车帝的数据结构可能嵌套在不同的 key 下
        car = (
            data.get("usedCarDetail", {}).get("carInfo", {}) or
            data.get("carDetail", {}).get("data", {}) or
            data.get("data", {}).get("car_info", {}) or
            data
        )

        vehicle.title = car.get("title", car.get("car_name", ""))
        vehicle.brand = car.get("brand_name", car.get("brand", ""))
        vehicle.series = car.get("series_name", car.get("series", ""))
        vehicle.model = car.get("model_name", car.get("car_model", ""))

        year_val = car.get("year", car.get("reg_year", 0))
        vehicle.year = int(year_val) if year_val else 0

        price_val = car.get("price", 0)
        vehicle.price = self._safe_float(price_val) / 10000 if self._safe_float(price_val) > 1000 else self._safe_float(price_val)
        vehicle.original_price = self._safe_float(car.get("new_car_price", car.get("guide_price", 0)))

        vehicle.mileage = str(car.get("mileage", car.get("mileage_str", "")))
        vehicle.mileage_km = self._safe_float(car.get("mileage_num", 0))
        vehicle.color = car.get("color", car.get("body_color", ""))
        vehicle.plate_city = car.get("city_name", car.get("plate_city", ""))
        vehicle.plate_date = car.get("reg_date", car.get("plate_date", ""))
        vehicle.vin = car.get("vin", "")

        # 技术参数
        vehicle.fuel_type = car.get("fuel_type", car.get("fuel_type_name", ""))
        vehicle.engine = car.get("engine", car.get("engine_desc", ""))
        vehicle.transmission = car.get("gearbox", car.get("transmission", ""))
        vehicle.drive_type = car.get("drive_type", "")
        vehicle.body_type = car.get("body_type", car.get("body_type_name", ""))
        vehicle.displacement = car.get("displacement", "")
        vehicle.emission_standard = car.get("emission_standard", car.get("emission", ""))
        vehicle.seats = int(car.get("seats", 0) or 0)

        # 电动车参数
        vehicle.battery_capacity = car.get("battery_capacity", "")
        vehicle.range_km = self._safe_float(car.get("range", car.get("endurance_mileage", 0)))

        # 图片
        images = car.get("images", car.get("image_list", car.get("car_images", [])))
        if isinstance(images, list):
            vehicle.images = [
                img if isinstance(img, str) else img.get("url", img.get("image_url", ""))
                for img in images
            ]
        vehicle.thumbnail = car.get("cover_image", car.get("main_image", ""))

        # 商家
        dealer = car.get("dealer", car.get("dealer_info", car.get("shop_info", {})))
        if isinstance(dealer, dict):
            vehicle.dealer_name = dealer.get("name", dealer.get("dealer_name", ""))
            vehicle.dealer_phone = dealer.get("phone", "")
            vehicle.dealer_city = dealer.get("city_name", "")
            vehicle.dealer_address = dealer.get("address", "")

        # 标签/车况
        tags = car.get("tags", car.get("car_tags", []))
        if isinstance(tags, list):
            vehicle.condition_tags = [
                t if isinstance(t, str) else t.get("name", "")
                for t in tags
            ]

        vehicle.highlights = car.get("highlights", car.get("selling_point", ""))
        vehicle.description = car.get("description", car.get("remark", ""))

    def _fill_from_html(self, vehicle: VehicleInfo, soup: BeautifulSoup):
        """HTML 降级解析"""
        title = soup.select_one("h1, [class*='car-title'], [class*='detail-title']")
        if title:
            vehicle.title = title.get_text(strip=True)

        price_el = soup.select_one("[class*='price']")
        if price_el:
            vehicle.price = self._extract_price(price_el.get_text(strip=True))

        # 参数表
        params = {}
        for item in soup.select("[class*='param-item'], [class*='info-item'], [class*='detail-item']"):
            label = item.select_one("[class*='label'], [class*='key']")
            value = item.select_one("[class*='value'], [class*='val']")
            if label and value:
                params[label.get_text(strip=True)] = value.get_text(strip=True)

        vehicle.mileage = params.get("表显里程", params.get("里程数", ""))
        vehicle.plate_date = params.get("上牌时间", "")
        vehicle.transmission = params.get("变速箱", "")
        vehicle.fuel_type = params.get("燃油类型", "")
        vehicle.emission_standard = params.get("排放标准", "")
        vehicle.displacement = params.get("排量", "")
        vehicle.color = params.get("车身颜色", "")

        # 图片
        for img in soup.select("[class*='gallery'] img, [class*='swiper'] img, [class*='carousel'] img"):
            src = img.get("src") or img.get("data-src") or ""
            if src and src not in vehicle.images:
                vehicle.images.append(src)

    def scrape(self, pages: Optional[int] = None, city: str = "") -> ScrapeResult:
        """完整采集流程"""
        result = ScrapeResult(
            source="dongchedi",
            started_at=datetime.now().isoformat(),
        )

        pages = pages or self.config.pages_to_scrape
        self._init_session()

        all_list_items = []

        # 优先使用 API
        for page in range(pages):
            items = self.scrape_list_api(page=page, city_name=city)
            if not items:
                # API 失败则尝试 HTML
                items = self.scrape_list_html(page=page + 1)
            if not items:
                logger.info(f"第{page}页无数据，停止翻页")
                break
            all_list_items.extend(items)
            result.pages_scraped = page + 1

        result.total_found = len(all_list_items)
        logger.info(f"懂车帝列表采集完成: 共 {len(all_list_items)} 条")

        # 采集详情
        for idx, item in enumerate(all_list_items):
            car_id = item.get("id", "")
            detail_url = item.get("url", "")
            if not car_id and not detail_url:
                continue

            logger.info(f"采集详情 [{idx+1}/{len(all_list_items)}]: {item.get('title', car_id)}")
            vehicle = self.scrape_detail(car_id, detail_url)

            if vehicle:
                if not vehicle.title:
                    vehicle.title = item.get("title", "")
                if not vehicle.price:
                    vehicle.price = self._safe_float(item.get("price", 0))
                if not vehicle.thumbnail:
                    vehicle.thumbnail = item.get("thumbnail", "")
                if not vehicle.brand:
                    vehicle.brand = item.get("brand", "")
                if not vehicle.series:
                    vehicle.series = item.get("series", "")
                result.vehicles.append(vehicle)
            else:
                result.errors.append(f"详情采集失败: {car_id}")

        result.finished_at = datetime.now().isoformat()
        result.success = len(result.errors) < len(all_list_items) * 0.5
        logger.info(result.summary())
        return result

    @staticmethod
    def _safe_float(val) -> float:
        try:
            return float(val)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _extract_price(text: str) -> float:
        match = re.search(r'([\d.]+)', text)
        return float(match.group(1)) if match else 0.0


# ─── 入口 ─────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
    scraper = DongchediScraper()
    result = scraper.scrape(pages=2)
    print(result.summary())
    for v in result.vehicles[:3]:
        print(v.to_json())
