"""Guazi (guazi.com) adapter for searching used cars.

URL patterns:
    List:   https://www.guazi.com/{city_abbr}/buy/
    Page N: https://www.guazi.com/{city_abbr}/buy/o{N}/
    Detail: https://www.guazi.com/car-detail/{clueId}.html

The site is a Next.js app with React Server Components.  All car data
is embedded in ``self.__next_f.push()`` RSC chunks within the HTML.
See parser.py for extraction logic.
"""

import asyncio
import sys
import webbrowser

import click

from car_cli.client.base import BaseClient
from car_cli.client.http import HttpClient
from car_cli.client.adapters.guazi.parser import parse_list, parse_detail
from car_cli.logging_config import get_logger
from car_cli.models.car import Car, CarDetail
from car_cli.client.adapters.guazi.cities import CITY_ABBR
from car_cli.models.filter import SearchFilter

_log = get_logger("guazi")

# Mobile UA reduces captcha rate on guazi.com
_MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/17.5 Mobile/15E148 Safari/604.1"
)

_EXTRA_HEADERS = {
    "User-Agent": _MOBILE_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
}

# Minimum response size for a valid page (captcha pages are ~4KB)
_MIN_VALID_SIZE = 10000


def _is_captcha(html: str, final_url: str) -> bool:
    """Detect if the response is a captcha/block page."""
    if "captcha" in final_url.lower():
        return True
    if len(html) < _MIN_VALID_SIZE and "captcha" in html.lower():
        return True
    return False


def _is_interactive() -> bool:
    """Check if stdin is a terminal (interactive mode)."""
    return hasattr(sys.stdin, "isatty") and sys.stdin.isatty()


class GuaziClient(BaseClient):
    """Guazi adapter for used car search."""

    platform_name = "guazi"

    def _get_city_abbr(self, city: str) -> str:
        """Get guazi city abbreviation from Chinese city name."""
        if not city or city == "全国":
            return "www"
        return CITY_ABBR.get(city, "www")

    def _build_list_url(self, filters: SearchFilter) -> str:
        city_abbr = self._get_city_abbr(filters.city)
        page = max(filters.page, 1)

        if page > 1:
            url = f"https://www.guazi.com/{city_abbr}/buy/o{page}/"
        else:
            url = f"https://www.guazi.com/{city_abbr}/buy/"

        return url

    async def _fetch_with_retry(
        self, url: str, referer: str, max_retries: int = 2
    ) -> str:
        """Fetch a URL with captcha-retry logic.

        When a captcha is detected and stdin is a terminal, automatically opens
        the captcha URL in the user's default browser and waits for them to
        complete verification before retrying.
        """
        captcha_url = ""

        for attempt in range(max_retries + 1):
            if attempt > 0 and not captcha_url:
                # Simple backoff when not doing interactive captcha
                delay = 3.0 * attempt
                _log.debug("retry attempt %d after %.1fs delay", attempt, delay)
                await asyncio.sleep(delay)

            async with HttpClient(
                referer=referer, extra_headers=_EXTRA_HEADERS
            ) as client:
                resp = await client.get(url)
                html = resp.text
                final_url = str(resp.url)

            _log.debug(
                "response html_len=%d final_url=%s", len(html), final_url
            )

            if not _is_captcha(html, final_url):
                return html

            captcha_url = final_url if "captcha" in final_url else ""
            _log.debug("captcha detected on attempt %d, url=%s", attempt, captcha_url)

            # Interactive captcha solving: open browser and wait for user
            if captcha_url and _is_interactive() and attempt < max_retries:
                click.echo(
                    "\n⚠️  瓜子二手车触发了验证码，正在打开浏览器...",
                    err=True,
                )
                webbrowser.open(captcha_url)
                # Wait for user to complete captcha (blocking prompt in thread)
                await asyncio.to_thread(
                    click.pause,
                    "   请在浏览器中完成验证，然后按任意键继续...",
                )
                click.echo("   正在重试请求...", err=True)
                # Reset so next loop retries immediately without extra delay
                captcha_url = ""
                continue

        # All retries exhausted
        _log.warning("captcha persisted after %d retries", max_retries)
        return html

    async def search(self, filters: SearchFilter) -> list[Car]:
        url = self._build_list_url(filters)
        referer = "https://www.guazi.com/"
        _log.debug("search url=%s", url)

        html = await self._fetch_with_retry(url, referer)

        if len(html) < _MIN_VALID_SIZE:
            raise RuntimeError(
                "guazi.com 返回了异常短的页面，可能是验证码拦截。"
                "请稍后再试，或在浏览器中访问 guazi.com 完成验证。"
            )

        cars = parse_list(html, filters.city or "全国")
        _log.debug("parsed list count=%s", len(cars))

        # Apply client-side filters that aren't in the URL
        if filters.brand:
            brand_lower = filters.brand.lower()
            cars = [c for c in cars if brand_lower in c.title.lower()]

        if filters.min_price:
            cars = [c for c in cars if c.price >= filters.min_price]
        if filters.max_price:
            cars = [c for c in cars if c.price <= filters.max_price]

        return cars

    async def detail(self, car_id: str) -> CarDetail:
        url = f"https://www.guazi.com/car-detail/{car_id}.html"
        referer = "https://www.guazi.com/"
        _log.debug("detail url=%s car_id=%s", url, car_id)

        html = await self._fetch_with_retry(url, referer, max_retries=3)
        _log.debug("detail html_len=%s", len(html))

        if _is_captcha(html, ""):
            _log.warning("detail page blocked by captcha for car_id=%s", car_id)
            return CarDetail(
                id=car_id,
                platform="guazi",
                title="[验证码拦截] 请在浏览器中打开链接查看详情",
                price=0.0,
                url=url,
                description="瓜子二手车的反爬机制阻止了详情获取，请直接在浏览器中访问链接。",
            )

        detail = parse_detail(html, car_id)
        _log.debug("detail title=%r price=%s", detail.title, detail.price)
        return detail
