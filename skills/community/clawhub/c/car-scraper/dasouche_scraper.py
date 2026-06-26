"""
万能反爬 Skill - 大搜车（souche.com）车辆信息采集
目标: 采集二手车/新车列表和详情，输出统一 VehicleInfo 格式
"""

import re
import json
import logging
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config import DASOUCHE_CONFIG, REQUEST_TIMEOUT, MAX_RETRIES
from data_models import VehicleInfo, ScrapeResult
from anti_detect import (
    build_headers,
    RateLimiter,
    CookieManager,
    detect_block,
    generate_trace_id,
)

logger = logging.getLogger("dasouche_scraper")


class DasoucheScraper:
    """
    大搜车车辆信息采集器

    采集策略:
    1. 先访问列表页获取 Cookie
    2. 通过列表页接口获取车辆卡片数据
    3. 逐个访问详情页补充完整信息
    4. 所有数据统一转为 VehicleInfo

    反爬对策:
    - 模拟浏览器请求头（含 sec-ch-* 系列）
    - 请求间隔随机化 (2~5秒)
    - 自动退避（被拦截后加长间隔）
    - Cookie 自动管理
    """

    def __init__(self):
        self.config = DASOUCHE_CONFIG
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(min_delay=2.0, max_delay=5.0)
        self.cookie_mgr = CookieManager()

    def _request(self, url: str, referer: Optional[str] = None, **kwargs) -> Optional[requests.Response]:
        """带反爬保护的请求方法"""
        self.rate_limiter.wait()

        headers = build_headers(
            url, referer=referer,
            extra=self.config.extra_headers,
        )

        for attempt in range(MAX_RETRIES):
            try:
                resp = self.session.get(
                    url, headers=headers,
                    timeout=REQUEST_TIMEOUT, **kwargs,
                )

                is_blocked, reason = detect_block(resp.status_code, resp.text)
                if is_blocked:
                    logger.warning(f"请求被拦截 [{reason}]: {url} (尝试 {attempt+1}/{MAX_RETRIES})")
                    self.rate_limiter.increase_backoff()
                    self.rate_limiter.wait()
                    continue

                self.rate_limiter.reset_backoff()
                # 更新 cookies
                self.cookie_mgr.update_cookies(
                    "souche.com",
                    dict(resp.cookies),
                )
                return resp

            except requests.RequestException as e:
                logger.error(f"请求异常: {url} - {e}")
                if attempt < MAX_RETRIES - 1:
                    self.rate_limiter.wait()

        return None

    def _init_session(self):
        """初始化会话，先访问首页获取 Cookie"""
        logger.info("初始化大搜车会话...")
        resp = self._request(self.config.base_url)
        if resp:
            logger.info("大搜车会话初始化成功")

    def scrape_list_page(self, page: int = 1) -> list[dict]:
        """
        采集列表页

        大搜车列表页通常有两种模式:
        1. 服务端渲染 HTML - 直接解析
        2. AJAX 接口返回 JSON - 解析接口数据
        """
        url = f"{self.config.list_url}?page={page}"
        referer = self.config.base_url

        resp = self._request(url, referer=referer)
        if not resp:
            return []

        cars = []

        # 尝试解析 JSON 数据（API 模式）
        try:
            data = resp.json()
            if isinstance(data, dict):
                items = data.get("data", {}).get("list", [])
                if not items:
                    items = data.get("result", {}).get("list", [])
                for item in items:
                    cars.append(self._parse_list_item_json(item))
                if cars:
                    return cars
        except (json.JSONDecodeError, AttributeError):
            pass

        # HTML 模式解析
        soup = BeautifulSoup(resp.text, "html.parser")
        car_cards = soup.select(".car-card, .car-item, .vehicle-item, [data-car-id]")

        for card in car_cards:
            parsed = self._parse_list_item_html(card)
            if parsed:
                cars.append(parsed)

        logger.info(f"大搜车列表第{page}页: 解析到 {len(cars)} 辆车")
        return cars

    def _parse_list_item_json(self, item: dict) -> dict:
        """解析 JSON 列表项"""
        return {
            "id": str(item.get("id", item.get("carId", ""))),
            "title": item.get("title", item.get("carName", "")),
            "price": self._safe_float(item.get("price", item.get("sellPrice", 0))),
            "original_price": self._safe_float(item.get("guidePrice", item.get("originalPrice", 0))),
            "mileage": item.get("mileage", item.get("runMiles", "")),
            "year": item.get("year", item.get("registYear", "")),
            "thumbnail": item.get("image", item.get("coverImage", "")),
            "brand": item.get("brand", item.get("brandName", "")),
            "series": item.get("series", item.get("seriesName", "")),
            "city": item.get("city", item.get("cityName", "")),
            "url": item.get("detailUrl", ""),
        }

    def _parse_list_item_html(self, card) -> Optional[dict]:
        """解析 HTML 列表卡片"""
        try:
            car_id = card.get("data-car-id", "")
            link = card.select_one("a[href]")
            title_el = card.select_one(".car-name, .title, h3, h4")
            price_el = card.select_one(".car-price, .price, .price-num")
            mileage_el = card.select_one(".mileage, .car-mileage")
            img_el = card.select_one("img")

            return {
                "id": car_id or (link["href"].split("/")[-1] if link else ""),
                "title": title_el.get_text(strip=True) if title_el else "",
                "price": self._extract_price(price_el.get_text(strip=True)) if price_el else 0,
                "mileage": mileage_el.get_text(strip=True) if mileage_el else "",
                "thumbnail": img_el.get("src", img_el.get("data-src", "")) if img_el else "",
                "url": link["href"] if link and link.get("href") else "",
            }
        except Exception as e:
            logger.debug(f"解析卡片失败: {e}")
            return None

    def scrape_detail(self, car_id: str, detail_url: str = "") -> Optional[VehicleInfo]:
        """
        采集车辆详情页
        """
        if not detail_url:
            detail_url = self.config.detail_url_pattern.format(car_id=car_id)

        if detail_url.startswith("/"):
            detail_url = self.config.base_url + detail_url

        resp = self._request(detail_url, referer=self.config.list_url)
        if not resp:
            return None

        vehicle = VehicleInfo(
            source="dasouche",
            source_id=car_id,
            source_url=detail_url,
            scraped_at=datetime.now().isoformat(),
        )

        # 尝试从页面 JSON 数据提取（很多 SPA 页面会内嵌数据）
        json_data = self._extract_embedded_json(resp.text)
        if json_data:
            self._fill_from_json(vehicle, json_data)
            return vehicle

        # HTML 解析模式
        soup = BeautifulSoup(resp.text, "html.parser")
        self._fill_from_html(vehicle, soup)

        return vehicle

    def _extract_embedded_json(self, html: str) -> Optional[dict]:
        """从页面中提取内嵌的 JSON 数据（如 window.__INITIAL_STATE__）"""
        patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*({.+?});?\s*</script>',
            r'window\.__DATA__\s*=\s*({.+?});?\s*</script>',
            r'window\.pageData\s*=\s*({.+?});?\s*</script>',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue
        return None

    def _fill_from_json(self, vehicle: VehicleInfo, data: dict):
        """从 JSON 数据填充车辆信息"""
        car = data.get("carDetail", data.get("car", data))

        vehicle.title = car.get("title", car.get("carName", ""))
        vehicle.brand = car.get("brand", car.get("brandName", ""))
        vehicle.series = car.get("series", car.get("seriesName", ""))
        vehicle.model = car.get("model", car.get("modelName", ""))
        vehicle.year = int(car.get("year", car.get("registYear", 0)) or 0)
        vehicle.price = self._safe_float(car.get("price", car.get("sellPrice", 0)))
        vehicle.original_price = self._safe_float(car.get("guidePrice", car.get("originalPrice", 0)))
        vehicle.mileage = str(car.get("mileage", car.get("runMiles", "")))
        vehicle.mileage_km = self._safe_float(car.get("mileageKm", 0))
        vehicle.color = car.get("color", car.get("outerColor", ""))
        vehicle.plate_city = car.get("plateCity", car.get("registCity", ""))
        vehicle.plate_date = car.get("plateDate", car.get("registDate", ""))
        vehicle.fuel_type = car.get("fuelType", car.get("fuelTypeName", ""))
        vehicle.engine = car.get("engine", car.get("engineDesc", ""))
        vehicle.transmission = car.get("transmission", car.get("gearboxType", ""))
        vehicle.displacement = car.get("displacement", "")
        vehicle.emission_standard = car.get("emissionStandard", car.get("emission", ""))
        vehicle.body_type = car.get("bodyType", car.get("bodyTypeName", ""))

        # 图片
        images = car.get("images", car.get("imageList", []))
        if isinstance(images, list):
            vehicle.images = [img if isinstance(img, str) else img.get("url", "") for img in images]
        vehicle.thumbnail = car.get("coverImage", car.get("mainImage", ""))

        # 商家
        dealer = car.get("dealer", car.get("shopInfo", {}))
        if isinstance(dealer, dict):
            vehicle.dealer_name = dealer.get("name", dealer.get("shopName", ""))
            vehicle.dealer_phone = dealer.get("phone", dealer.get("tel", ""))
            vehicle.dealer_city = dealer.get("city", dealer.get("cityName", ""))

    def _fill_from_html(self, vehicle: VehicleInfo, soup: BeautifulSoup):
        """从 HTML 解析填充车辆信息"""
        # 标题
        title = soup.select_one("h1, .car-title, .detail-title")
        if title:
            vehicle.title = title.get_text(strip=True)

        # 价格
        price_el = soup.select_one(".price, .car-price, .sell-price")
        if price_el:
            vehicle.price = self._extract_price(price_el.get_text(strip=True))

        # 参数表（通常为 key-value 对）
        params = {}
        for row in soup.select(".params-item, .info-item, tr, .detail-item"):
            label = row.select_one(".label, th, .key, dt")
            value = row.select_one(".value, td, .val, dd")
            if label and value:
                params[label.get_text(strip=True)] = value.get_text(strip=True)

        vehicle.brand = params.get("品牌", params.get("厂商", ""))
        vehicle.mileage = params.get("表显里程", params.get("里程", ""))
        vehicle.plate_date = params.get("上牌时间", params.get("上牌日期", ""))
        vehicle.transmission = params.get("变速箱", params.get("变速器", ""))
        vehicle.fuel_type = params.get("燃油类型", params.get("燃料", ""))
        vehicle.displacement = params.get("排量", "")
        vehicle.emission_standard = params.get("排放标准", "")
        vehicle.color = params.get("车身颜色", params.get("外观颜色", ""))

        # 图片
        for img in soup.select(".car-gallery img, .swiper img, .detail-img img"):
            src = img.get("src") or img.get("data-src") or ""
            if src and src not in vehicle.images:
                vehicle.images.append(src)

    def scrape(self, pages: Optional[int] = None) -> ScrapeResult:
        """
        完整采集流程
        """
        result = ScrapeResult(
            source="dasouche",
            started_at=datetime.now().isoformat(),
        )

        pages = pages or self.config.pages_to_scrape
        self._init_session()

        all_list_items = []
        for page in range(1, pages + 1):
            items = self.scrape_list_page(page)
            if not items:
                logger.info(f"第{page}页无数据，停止翻页")
                break
            all_list_items.extend(items)
            result.pages_scraped = page

        result.total_found = len(all_list_items)
        logger.info(f"大搜车列表采集完成: 共 {len(all_list_items)} 条")

        # 采集详情
        for idx, item in enumerate(all_list_items):
            car_id = item.get("id", "")
            detail_url = item.get("url", "")
            if not car_id and not detail_url:
                continue

            logger.info(f"采集详情 [{idx+1}/{len(all_list_items)}]: {item.get('title', car_id)}")
            vehicle = self.scrape_detail(car_id, detail_url)

            if vehicle:
                # 用列表数据补充详情中缺失的字段
                if not vehicle.title:
                    vehicle.title = item.get("title", "")
                if not vehicle.price:
                    vehicle.price = item.get("price", 0)
                if not vehicle.thumbnail:
                    vehicle.thumbnail = item.get("thumbnail", "")
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
        """从文本中提取价格数字（万元）"""
        match = re.search(r'([\d.]+)', text)
        return float(match.group(1)) if match else 0.0


# ─── 入口 ─────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
    scraper = DasoucheScraper()
    result = scraper.scrape(pages=2)
    print(result.summary())
    for v in result.vehicles[:3]:
        print(v.to_json())
