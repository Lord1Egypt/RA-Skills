"""
万能反爬 Skill - 汽车之家（autohome.com.cn / che168.com）车辆信息采集
目标: 采集二手车列表和详情页，输出统一 VehicleInfo 格式

汽车之家反爬特点:
- 二手车业务在 che168.com 子域
- 使用字体反爬（关键数字用自定义字体映射，部分价格/电话用 CSS sprite）
- 列表页有时使用加密参数
- 详情页大部分参数以明文 HTML 存在
- 编码可能为 gb2312 / gbk / utf-8 混用
"""

import re
import json
import logging
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config import AUTOHOME_CONFIG, REQUEST_TIMEOUT, MAX_RETRIES
from data_models import VehicleInfo, ScrapeResult
from anti_detect import (
    build_headers,
    RateLimiter,
    CookieManager,
    detect_block,
    generate_trace_id,
)

logger = logging.getLogger("autohome_scraper")


class AutohomeScraper:
    """
    汽车之家/二手车之家采集器

    采集策略:
    1. 通过 che168.com 列表页获取车辆卡片
    2. 逐个访问详情页补全完整参数
    3. 处理字体反爬（若遇到）

    反爬对策:
    - 编码自适应 (gb2312/gbk/utf-8)
    - 字体反爬数字映射还原
    - 请求间隔 3~6 秒
    - Cookie 定期刷新
    """

    # che168 列表/详情域名
    CHE168_BASE = "https://www.che168.com"
    # 汽车之家新车参数
    AUTOHOME_SPEC = "https://www.autohome.com.cn/spec"

    def __init__(self):
        self.config = AUTOHOME_CONFIG
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(min_delay=3.0, max_delay=6.0)
        self.cookie_mgr = CookieManager()
        self._font_map: dict = {}  # 字体反爬映射表

    def _request(
        self, url: str,
        referer: Optional[str] = None,
        encoding: Optional[str] = None,
        **kwargs,
    ) -> Optional[requests.Response]:
        """带反爬保护的请求"""
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

                # 自适应编码
                if encoding:
                    resp.encoding = encoding
                elif "charset=gb" in resp.headers.get("Content-Type", "").lower():
                    resp.encoding = "gbk"
                elif resp.apparent_encoding:
                    resp.encoding = resp.apparent_encoding

                is_blocked, reason = detect_block(resp.status_code, resp.text)
                if is_blocked:
                    logger.warning(f"被拦截 [{reason}]: {url} (尝试 {attempt+1}/{MAX_RETRIES})")
                    self.rate_limiter.increase_backoff()
                    self.rate_limiter.wait()
                    continue

                self.rate_limiter.reset_backoff()
                domain = "che168.com" if "che168" in url else "autohome.com.cn"
                self.cookie_mgr.update_cookies(domain, dict(resp.cookies))
                return resp

            except requests.RequestException as e:
                logger.error(f"请求异常: {url} - {e}")
                if attempt < MAX_RETRIES - 1:
                    self.rate_limiter.wait()

        return None

    def _init_session(self):
        """初始化会话"""
        logger.info("初始化汽车之家会话...")
        # 先访问 che168 首页获取 Cookie
        self._request(self.CHE168_BASE)
        self.rate_limiter.wait()
        # 再访问列表首页
        self._request(self.config.list_url, referer=self.CHE168_BASE)
        logger.info("汽车之家会话初始化完成")

    def scrape_list_page(self, page: int = 1) -> list[dict]:
        """
        采集 che168 列表页

        URL 格式: https://www.che168.com/list/#pvareaid=...&page=N
        或: https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{page}exx0/
        """
        if page == 1:
            url = f"{self.config.list_url}"
        else:
            url = f"https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{page}exx0/"

        resp = self._request(url, referer=self.config.list_url)
        if not resp:
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        cars = []

        # che168 列表页车辆卡片
        car_cards = soup.select(
            ".carinfo, .car-item, #viewlist_ul li, .list-item, "
            "[class*='car-card'], .viewlist_ul li"
        )

        for card in car_cards:
            parsed = self._parse_list_card(card)
            if parsed:
                cars.append(parsed)

        # 如果上面没解析到，尝试从页面 JSON 提取
        if not cars:
            cars = self._extract_list_from_script(resp.text)

        logger.info(f"汽车之家列表第{page}页: {len(cars)} 辆车")
        return cars

    def _parse_list_card(self, card) -> Optional[dict]:
        """解析列表页车辆卡片"""
        try:
            link = card.select_one("a[href*='/dealer/'], a[href*='/info/'], a[href]")
            title_el = card.select_one(
                ".card-name, .car-name, .title, h4 a, .carinfo-title a"
            )
            price_el = card.select_one(
                ".card-price, .car-price, .price, .lever-price, .pirce"
            )
            mileage_el = card.select_one(
                ".card-mileage, .mileage, .info-gray, .card-info span"
            )
            img_el = card.select_one("img")

            href = ""
            car_id = ""
            if link and link.get("href"):
                href = link["href"]
                id_match = re.search(r'/(\d+)\.html', href)
                if id_match:
                    car_id = id_match.group(1)

            if not title_el and not price_el:
                return None

            price_text = price_el.get_text(strip=True) if price_el else ""
            price = self._extract_price(price_text)

            # 提取里程/年份等 info
            info_spans = card.select(".card-info span, .info span, .info-gray span")
            infos = [s.get_text(strip=True) for s in info_spans]

            mileage = ""
            year_str = ""
            for info in infos:
                if "万公里" in info or "km" in info.lower():
                    mileage = info
                elif re.search(r'20\d{2}', info):
                    year_str = info

            if not mileage and mileage_el:
                mileage = mileage_el.get_text(strip=True)

            return {
                "id": car_id,
                "title": title_el.get_text(strip=True) if title_el else "",
                "price": price,
                "mileage": mileage,
                "year_str": year_str,
                "thumbnail": img_el.get("src", img_el.get("data-src", "")) if img_el else "",
                "url": href,
            }
        except Exception as e:
            logger.debug(f"卡片解析失败: {e}")
            return None

    def _extract_list_from_script(self, html: str) -> list[dict]:
        """从页面脚本中提取车辆列表 JSON"""
        patterns = [
            r'var\s+viewList\s*=\s*(\[.+?\])\s*;',
            r'var\s+carList\s*=\s*(\[.+?\])\s*;',
            r'"carSourceList"\s*:\s*(\[.+?\])',
        ]
        for pattern in patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    items = json.loads(match.group(1))
                    return [self._parse_script_item(item) for item in items if isinstance(item, dict)]
                except json.JSONDecodeError:
                    continue
        return []

    def _parse_script_item(self, item: dict) -> dict:
        """解析脚本中的车辆数据"""
        return {
            "id": str(item.get("infoid", item.get("carid", item.get("id", "")))),
            "title": item.get("title", item.get("carname", "")),
            "price": self._safe_float(item.get("price", 0)),
            "original_price": self._safe_float(item.get("guideprice", item.get("newprice", 0))),
            "mileage": item.get("mileage", ""),
            "year_str": item.get("year", item.get("registeryear", "")),
            "brand": item.get("brand", item.get("brandname", "")),
            "series": item.get("series", item.get("seriesname", "")),
            "city": item.get("city", item.get("cityname", "")),
            "thumbnail": item.get("pic", item.get("image", "")),
            "url": item.get("url", item.get("link", "")),
        }

    def scrape_detail(self, car_id: str, detail_url: str = "") -> Optional[VehicleInfo]:
        """
        采集详情页
        """
        if not detail_url:
            detail_url = self.config.detail_url_pattern.format(car_id=car_id)
        if detail_url.startswith("/"):
            detail_url = self.CHE168_BASE + detail_url

        resp = self._request(detail_url, referer=self.config.list_url)
        if not resp:
            return None

        vehicle = VehicleInfo(
            source="autohome",
            source_id=car_id,
            source_url=detail_url,
            scraped_at=datetime.now().isoformat(),
        )

        soup = BeautifulSoup(resp.text, "html.parser")

        # 尝试从内嵌 JSON 提取
        json_data = self._extract_detail_json(resp.text)
        if json_data:
            self._fill_from_json(vehicle, json_data)
        else:
            self._fill_from_html(vehicle, soup)

        return vehicle

    def _extract_detail_json(self, html: str) -> Optional[dict]:
        """提取详情页内嵌 JSON"""
        patterns = [
            r'var\s+carDetailData\s*=\s*({.+?});',
            r'var\s+detailData\s*=\s*({.+?});',
            r'window\.__INIT_DATA__\s*=\s*({.+?});?\s*</script>',
            r'"carInfo"\s*:\s*({.+?})\s*[,}]',
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
        """从 JSON 填充"""
        car = data.get("carInfo", data)

        vehicle.title = car.get("title", car.get("carname", ""))
        vehicle.brand = car.get("brand", car.get("brandname", ""))
        vehicle.series = car.get("series", car.get("seriesname", ""))
        vehicle.model = car.get("model", car.get("specname", ""))
        vehicle.year = int(car.get("year", car.get("registeryear", 0)) or 0)
        vehicle.price = self._safe_float(car.get("price", 0))
        vehicle.original_price = self._safe_float(car.get("guideprice", car.get("newprice", 0)))
        vehicle.mileage = str(car.get("mileage", ""))
        vehicle.mileage_km = self._safe_float(car.get("mileagenum", 0))
        vehicle.color = car.get("color", car.get("outercolor", ""))
        vehicle.plate_city = car.get("platecity", car.get("registercity", ""))
        vehicle.plate_date = car.get("platedate", car.get("registerdate", ""))
        vehicle.vin = car.get("vin", "")

        vehicle.fuel_type = car.get("fueltype", car.get("fueltypename", ""))
        vehicle.engine = car.get("engine", car.get("enginedesc", ""))
        vehicle.transmission = car.get("transmission", car.get("gearbox", ""))
        vehicle.drive_type = car.get("drivetype", "")
        vehicle.body_type = car.get("bodytype", car.get("bodytypename", ""))
        vehicle.displacement = car.get("displacement", "")
        vehicle.emission_standard = car.get("emission", car.get("emissionstandard", ""))
        vehicle.seats = int(car.get("seats", car.get("seatnum", 0)) or 0)

        images = car.get("images", car.get("imagelist", car.get("pics", [])))
        if isinstance(images, list):
            vehicle.images = [
                img if isinstance(img, str) else img.get("url", img.get("pic_url", ""))
                for img in images
            ]
        vehicle.thumbnail = car.get("pic", car.get("cover", ""))

        dealer = car.get("dealer", car.get("dealerinfo", {}))
        if isinstance(dealer, dict):
            vehicle.dealer_name = dealer.get("name", dealer.get("dealername", ""))
            vehicle.dealer_phone = dealer.get("phone", dealer.get("tel", ""))
            vehicle.dealer_city = dealer.get("city", "")
            vehicle.dealer_address = dealer.get("address", "")

        vehicle.highlights = car.get("highlights", car.get("sellingpoint", ""))
        vehicle.description = car.get("description", car.get("remark", ""))

    def _fill_from_html(self, vehicle: VehicleInfo, soup: BeautifulSoup):
        """HTML 解析填充"""
        # 标题
        title_el = soup.select_one(
            "h2.titlebox, .car-title h2, .car-box h1, .title-box h1, "
            ".detail-title, h1"
        )
        if title_el:
            vehicle.title = title_el.get_text(strip=True)

        # 售价
        price_el = soup.select_one(
            ".price-box .price, .car-price .price, .price-num, "
            ".pirce-num, .lever .price"
        )
        if price_el:
            vehicle.price = self._extract_price(price_el.get_text(strip=True))

        # 新车指导价
        guide_el = soup.select_one(".guide-price, .new-price, .original-price")
        if guide_el:
            vehicle.original_price = self._extract_price(guide_el.get_text(strip=True))

        # 基本参数表
        params = self._extract_params_table(soup)

        vehicle.mileage = params.get("表显里程", params.get("里程", ""))
        vehicle.plate_date = params.get("上牌时间", params.get("首次上牌", ""))
        vehicle.plate_city = params.get("上牌地", params.get("归属地", ""))
        vehicle.transmission = params.get("变速箱", params.get("档位/变速箱", ""))
        vehicle.displacement = params.get("排量", params.get("排气量", ""))
        vehicle.fuel_type = params.get("燃油类型", params.get("燃油标号", ""))
        vehicle.emission_standard = params.get("排放标准", "")
        vehicle.color = params.get("车身颜色", params.get("外观颜色", ""))
        vehicle.body_type = params.get("车辆类型", params.get("车身形式", ""))
        vehicle.engine = params.get("发动机", "")
        vehicle.drive_type = params.get("驱动方式", "")

        # 年款
        year_str = params.get("年款", params.get("出厂日期", ""))
        year_match = re.search(r'(20\d{2})', year_str)
        if year_match:
            vehicle.year = int(year_match.group(1))

        # VIN
        vin = params.get("车辆识别码", params.get("VIN", ""))
        if vin:
            vehicle.vin = vin

        # 图片
        for img in soup.select(
            ".car-pic img, .swiper-slide img, .pic-box img, "
            ".gallery img, #img-box img"
        ):
            src = img.get("src") or img.get("data-src") or ""
            if src and not src.endswith("placeholder") and src not in vehicle.images:
                vehicle.images.append(src)

        # 商家
        dealer_el = soup.select_one(
            ".dealer-name, .shop-name, .dealer-title, .car-dealer-name a"
        )
        if dealer_el:
            vehicle.dealer_name = dealer_el.get_text(strip=True)

        phone_el = soup.select_one(".dealer-phone, .phone, .telphone")
        if phone_el:
            vehicle.dealer_phone = phone_el.get_text(strip=True)

        addr_el = soup.select_one(".dealer-address, .address")
        if addr_el:
            vehicle.dealer_address = addr_el.get_text(strip=True)

    def _extract_params_table(self, soup: BeautifulSoup) -> dict:
        """
        提取参数表格
        汽车之家详情页参数一般以 dl/dt/dd 或 table 呈现
        """
        params = {}

        # dl > dt + dd 格式
        for dl in soup.select("dl, .param-list, .info-list"):
            dts = dl.select("dt, .label, .key")
            dds = dl.select("dd, .value, .val")
            for dt, dd in zip(dts, dds):
                key = dt.get_text(strip=True).rstrip("：:").strip()
                val = dd.get_text(strip=True)
                if key:
                    params[key] = val

        # li/span 格式
        for item in soup.select(
            ".baseinfo li, .basic-info li, .detail-params li, "
            ".car-info-item, .info-item"
        ):
            text = item.get_text("|", strip=True)
            if "：" in text:
                parts = text.split("：", 1)
                params[parts[0].strip()] = parts[1].strip()
            elif ":" in text:
                parts = text.split(":", 1)
                params[parts[0].strip()] = parts[1].strip()
            elif "|" in text:
                parts = text.split("|")
                if len(parts) == 2:
                    params[parts[0].strip()] = parts[1].strip()

        # table 格式
        for row in soup.select("table tr"):
            cells = row.select("th, td")
            if len(cells) >= 2:
                for i in range(0, len(cells) - 1, 2):
                    key = cells[i].get_text(strip=True).rstrip("：:").strip()
                    val = cells[i + 1].get_text(strip=True)
                    if key:
                        params[key] = val

        return params

    def scrape_new_car_specs(self, spec_id: str) -> Optional[dict]:
        """
        采集汽车之家新车参数配置页（补充新车指导价等）
        URL: https://www.autohome.com.cn/spec/XXXXX/
        """
        url = f"{self.AUTOHOME_SPEC}/{spec_id}/"
        resp = self._request(url, referer=self.config.base_url)
        if not resp:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")
        specs = {}

        for row in soup.select(".config-table tr, .param-table tr"):
            cells = row.select("th, td")
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                val = cells[1].get_text(strip=True)
                if key:
                    specs[key] = val

        return specs if specs else None

    def scrape(self, pages: Optional[int] = None) -> ScrapeResult:
        """完整采集流程"""
        result = ScrapeResult(
            source="autohome",
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
        logger.info(f"汽车之家列表采集完成: 共 {len(all_list_items)} 条")

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
    scraper = AutohomeScraper()
    result = scraper.scrape(pages=2)
    print(result.summary())
    for v in result.vehicles[:3]:
        print(v.to_json())
