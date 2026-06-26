"""
X/Twitter抓取器
通过网页爬虫或第三方服务抓取X/Twitter内容
"""
import asyncio
import logging
import time
from typing import List, Dict, Any
from datetime import datetime, timedelta

from .base_fetcher import BaseFetcher, NewsItem


class XFetcher(BaseFetcher):
    """X/Twitter抓取器"""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.username = config.get("username", "")
        self.usernames = config.get("usernames", [])
        self.logger = logging.getLogger(f"XFetcher.{self.name}")

        # 如果只有一个用户名，添加到列表中
        if self.username and not self.usernames:
            self.usernames = [self.username]

    async def fetch(self) -> List[NewsItem]:
        """
        抓取X/Twitter内容

        Returns:
            新闻条目列表
        """
        if not self.enabled:
            self.logger.info(f"数据源已禁用: {self.name}")
            return []

        if not self.usernames:
            self.logger.error(f"用户名列表为空: {self.name}")
            return []

        self.logger.info(f"开始抓取X/Twitter: {self.name} ({self.usernames})")
        start_time = time.time()

        # 尝试使用Playwright进行真实抓取
        try:
            # 创建Playwright抓取器配置，合并全局fetch配置
            playwright_config = self.config.copy()
            playwright_config["use_playwright"] = True

            # 获取全局抓取配置
            from .config import get_config_loader
            config_loader = get_config_loader()
            fetch_config = config_loader.get_fetch_config()

            # 合并重要配置
            if "playwright_wait_seconds" in fetch_config:
                playwright_config["playwright_wait_seconds"] = fetch_config["playwright_wait_seconds"]
            if "user_agent" in fetch_config:
                playwright_config["user_agent"] = fetch_config["user_agent"]
            if "timeout_seconds" in fetch_config:
                playwright_config["timeout_seconds"] = fetch_config["timeout_seconds"]

            self.logger.debug(f"创建XPlaywrightFetcher配置: {list(playwright_config.keys())}")
            playwright_fetcher = XPlaywrightFetcher(playwright_config)
            items = await playwright_fetcher.fetch()

            elapsed = time.time() - start_time
            if items:
                self.logger.info(f"X/Twitter Playwright抓取成功: {self.name}, 获取 {len(items)} 个条目, 耗时 {elapsed:.2f}秒")
                return items
            else:
                self.logger.warning(f"X/Twitter Playwright抓取返回空结果: {self.name}, 耗时 {elapsed:.2f}秒")
                return []

        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.warning(f"X/Twitter Playwright抓取失败，跳过模拟数据: {self.name}, 耗时 {elapsed:.2f}秒, 错误: {e}")
            # 不返回模拟数据，只返回空列表
            return []





class XPlaywrightFetcher(BaseFetcher):
    """
    使用Playwright的X/Twitter抓取器
    需要安装Playwright: pip install playwright && playwright install
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.username = config.get("username", "")
        self.usernames = config.get("usernames", [])
        self.use_playwright = config.get("use_playwright", True)
        self.playwright_wait_seconds = config.get("playwright_wait_seconds", 2)
        self.logger = logging.getLogger(f"XPlaywrightFetcher.{self.name}")

        # 如果只有一个用户名，添加到列表中
        if self.username and not self.usernames:
            self.usernames = [self.username]

    async def fetch(self) -> List[NewsItem]:
        """
        使用Playwright抓取X/Twitter内容

        Returns:
            新闻条目列表
        """
        if not self.use_playwright:
            self.logger.warning("Playwright未启用，返回空列表")
            return []

        self.logger.info(f"使用Playwright抓取X/Twitter: {self.name}")
        start_time = time.time()

        try:
            # 导入Playwright（延迟导入）
            from playwright.async_api import async_playwright

            items = []
            async with async_playwright() as p:
                # 使用更真实的浏览器配置
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-accelerated-2d-canvas',
                        '--disable-gpu',
                    ]
                )
                context = await browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    locale='en-US',
                    timezone_id='America/New_York',
                    permissions=[],
                    extra_http_headers={
                        'Accept-Language': 'en-US,en;q=0.9',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                    }
                )
                page = await context.new_page()

                # 隐藏自动化特征
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """)

                for username in self.usernames:
                    user_items = await self._fetch_user_with_playwright(page, username)
                    items.extend(user_items)

                await browser.close()

            # 应用过滤
            filtered_items = self.apply_filters(items)
            elapsed = time.time() - start_time
            self.logger.info(f"Playwright抓取完成: {self.name}, 获取 {len(filtered_items)} 个条目, 耗时 {elapsed:.2f}秒")
            return filtered_items

        except ImportError:
            elapsed = time.time() - start_time
            self.logger.error(f"Playwright未安装，请运行: pip install playwright && playwright install, 耗时 {elapsed:.2f}秒")
            return []
        except Exception as e:
            elapsed = time.time() - start_time
            self.logger.error(f"Playwright抓取失败, 耗时 {elapsed:.2f}秒: {e}")
            return []

    async def _fetch_user_with_playwright(self, page, username: str) -> List[NewsItem]:
        """
        使用Playwright抓取用户推文

        Args:
            page: Playwright页面对象
            username: 用户名

        Returns:
            新闻条目列表
        """
        self.logger.info(f"爬取用户: @{username}")

        # Nitter实例列表（按优先级排序） - 更新列表，基于可用性测试
        nitter_instances = [
            "https://nitter.tiekoetter.com",  # 已验证可用
            "https://nitter.weiler.rocks",     # 返回内容但需验证选择器
            "https://nitter.net",              # 主要实例（可能被屏蔽）
            "https://nitter.privacydev.net",   # 证书错误
            "https://nitter.fdn.fr",           # 连接关闭
            "https://nitter.1d4.us",           # 连接关闭
            "https://nitter.unixfox.eu",       # 连接关闭
            "https://nitter.nixnet.services",  # 401 需要认证
            "https://nitter.poast.org",        # 连接失败
            "https://nitter.sethforprivacy.com", # 连接关闭
        ]

        for nitter_base in nitter_instances:
            try:
                # 使用Nitter进行无登录采集
                url = f"{nitter_base}/{username}"
                self.logger.info(f"尝试Nitter实例: {url}")

                # 设置更真实的请求头
                await page.set_extra_http_headers({
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Cache-Control': 'max-age=0',
                })

                # 尝试不同等待策略
                response = await page.goto(url, wait_until="domcontentloaded", timeout=20000)

                if response and response.status != 200:
                    self.logger.warning(f"Nitter实例返回状态码 {response.status}: {nitter_base}")
                    continue

                # 等待更长的时间让页面加载，使用配置的等待时间
                wait_times = [
                    self.playwright_wait_seconds,
                    self.playwright_wait_seconds * 2,
                    self.playwright_wait_seconds * 3
                ]
                for wait_seconds in wait_times:
                    await page.wait_for_timeout(wait_seconds * 1000)

                    # 检查页面是否包含有效内容
                    content = await page.content()
                    content_length = len(content)
                    self.logger.info(f"等待 {wait_seconds} 秒后内容大小: {content_length} 字节")

                    # 如果内容过少，跳过这个实例（提高阈值）
                    if content_length < 10000:
                        self.logger.warning(f"Nitter实例返回内容过少 ({content_length} 字节): {nitter_base}")
                        continue

                    # 检查是否有错误消息
                    error_selectors = [
                        'text=User not found',
                        'text=User suspended',
                        'text=This account is private',
                        'text=Something went wrong',
                        'text=Rate limit exceeded',
                        'text=doesn\'t exist',
                        'text=not found',
                    ]

                    has_error = False
                    for selector in error_selectors:
                        if await page.is_visible(selector):
                            self.logger.warning(f"页面包含错误: {selector}")
                            has_error = True
                            break

                    if has_error:
                        continue

                    # 检查是否有推文内容 - 扩展选择器
                    tweet_selectors = [
                        'article[data-testid="tweet"]',
                        'div[data-testid="tweet"]',
                        'div[role="article"]',
                        '.tweet',
                        'article.tweet',
                        'div.tweet',
                        '.timeline-item',
                        '.tweet-body',
                        'article',
                        'div[class*="tweet"]',
                    ]

                    items = []
                    for selector in tweet_selectors:
                        try:
                            tweets = await page.locator(selector).all()
                            if tweets:
                                self.logger.info(f"找到 {len(tweets)} 个推文 (选择器: {selector})")
                                for tweet_locator in tweets[:self.max_items]:
                                    try:
                                        # 将Locator转换为ElementHandle
                                        tweet_element = await tweet_locator.element_handle()
                                        if not tweet_element:
                                            continue
                                        item = await self._parse_tweet_element(tweet_element, username, nitter_base)
                                        if item:
                                            items.append(item)
                                    except Exception as e:
                                        self.logger.debug(f"解析推文失败: {e}")
                                break
                        except Exception as e:
                            self.logger.debug(f"选择器 {selector} 失败: {e}")
                            continue

                    if items:
                        self.logger.info(f"成功从 {nitter_base} 获取 {len(items)} 个推文")
                        return items
                    else:
                        self.logger.warning(f"从 {nitter_base} 未找到推文，尝试下一等待周期")

            except Exception as e:
                self.logger.warning(f"Nitter实例 {nitter_base} 失败: {e}")
                # 尝试下一个实例
                continue

        self.logger.error(f"所有Nitter实例均失败: @{username}")
        return []

    async def _parse_tweet_element(self, tweet_element, username: str, nitter_base: str = None) -> NewsItem:
        """
        解析推文元素

        Args:
            tweet_element: 推文元素 (ElementHandle)
            username: 用户名
            nitter_base: Nitter实例基址，用于构建绝对链接

        Returns:
            新闻条目
        """
        # 改进的解析逻辑，针对nitter实例优化
        # 首先尝试获取推文正文内容
        content_elem = await tweet_element.query_selector('.tweet-content')
        if content_elem:
            title = await content_elem.inner_text()
        else:
            title = await tweet_element.inner_text()

        title = title.strip()
        if len(title) > 200:
            title = title[:200]  # 截断

        # 默认实例基址
        if nitter_base is None:
            nitter_base = "https://nitter.tiekoetter.com"

        # 尝试提取推文链接
        link_elements = await tweet_element.query_selector_all('a[href*="/status/"]')
        url = f"{nitter_base}/{username}"  # 使用当前实例
        if link_elements:
            href = await link_elements[0].get_attribute("href")
            if href:
                # 转换为绝对链接
                if href.startswith('/'):
                    # 使用当前实例基址
                    url = f"{nitter_base}{href}"
                elif href.startswith('http'):
                    url = href

        # 尝试提取时间
        time_elements = await tweet_element.query_selector_all('time')
        publish_date = datetime.now()
        if time_elements:
            datetime_str = await time_elements[0].get_attribute("datetime")
            if datetime_str:
                try:
                    publish_date = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
                except ValueError:
                    pass
        else:
            # 备选：查找包含日期的元素
            date_elem = await tweet_element.query_selector('.tweet-date, .date, .published')
            if date_elem:
                date_text = await date_elem.inner_text()
                # 简单解析日期文本（可改进）
                # 暂时忽略

        title_clean = self.cleanup_content(title)
        # 从nitter_base提取实例名
        instance_name = nitter_base.replace('https://', '').replace('http://', '').split('/')[0]
        item = NewsItem(
            title=title_clean,
            url=url,
            content=title_clean,
            summary=self.cleanup_content(title_clean[:150]),
            source=self.name,
            source_type="twitter",
            publish_date=publish_date,
            author=username,
            metadata={
                "username": username,
                "platform": "twitter",
                "fetched_with": "playwright",
                "nitter_instance": instance_name,
            }
        )

        return item