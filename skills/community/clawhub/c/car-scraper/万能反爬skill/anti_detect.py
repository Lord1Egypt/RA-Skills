"""
万能反爬 Skill - 反检测工具集
提供请求伪装、指纹随机化、速率控制、Cookie管理等反爬能力
"""

import random
import time
import hashlib
import logging
from typing import Optional
from urllib.parse import urlparse

logger = logging.getLogger("anti_detect")

# ─── User-Agent 池 ────────────────────────────────────

_DESKTOP_UAS = [
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    # Chrome Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    # Firefox Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    # Safari Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
]

_MOBILE_UAS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
]


def random_ua(mobile: bool = False) -> str:
    """随机返回一个 User-Agent"""
    pool = _MOBILE_UAS if mobile else _DESKTOP_UAS
    return random.choice(pool)


# ─── 请求头生成 ────────────────────────────────────────

_ACCEPT_LANGUAGES = [
    "zh-CN,zh;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "zh-CN,zh;q=0.9",
    "zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7",
]

_SEC_CH_UA_TEMPLATES = [
    '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    '"Not_A Brand";v="8", "Chromium";v="119", "Google Chrome";v="119"',
    '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"',
]


def build_headers(
    url: str,
    referer: Optional[str] = None,
    extra: Optional[dict] = None,
    mobile: bool = False,
) -> dict:
    """
    构建仿真请求头
    - 自动设置 Referer 为同域
    - 随机 User-Agent 和 Accept-Language
    - 添加现代浏览器的 sec-ch-* 头
    """
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"

    headers = {
        "User-Agent": random_ua(mobile),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": random.choice(_ACCEPT_LANGUAGES),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin" if referer else "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    # Chrome 特有头部
    if "Chrome" in headers["User-Agent"]:
        headers["sec-ch-ua"] = random.choice(_SEC_CH_UA_TEMPLATES)
        headers["sec-ch-ua-mobile"] = "?1" if mobile else "?0"
        headers["sec-ch-ua-platform"] = '"Android"' if mobile else '"Windows"'

    if referer:
        headers["Referer"] = referer
    else:
        headers["Referer"] = origin + "/"

    if extra:
        headers.update(extra)

    return headers


# ─── 速率控制 ─────────────────────────────────────────

class RateLimiter:
    """
    请求速率控制器
    - 随机延时避免固定模式
    - 支持退避策略（被检测后自动加长间隔）
    """

    def __init__(self, min_delay: float = 2.0, max_delay: float = 5.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self._backoff_level = 0
        self._last_request_time = 0.0

    def wait(self):
        """等待随机时间后才允许下一次请求"""
        backoff_multiplier = 1.0 + (self._backoff_level * 0.5)
        delay = random.uniform(
            self.min_delay * backoff_multiplier,
            self.max_delay * backoff_multiplier,
        )

        elapsed = time.time() - self._last_request_time
        if elapsed < delay:
            sleep_time = delay - elapsed
            logger.debug(f"速率控制: 等待 {sleep_time:.1f}s")
            time.sleep(sleep_time)

        self._last_request_time = time.time()

    def increase_backoff(self):
        """检测到反爬时增加退避等级"""
        self._backoff_level = min(self._backoff_level + 1, 5)
        logger.warning(f"退避等级提升至 {self._backoff_level}")

    def reset_backoff(self):
        """请求恢复正常后重置退避"""
        if self._backoff_level > 0:
            self._backoff_level = max(self._backoff_level - 1, 0)


# ─── Cookie 管理 ──────────────────────────────────────

class CookieManager:
    """
    Cookie 智能管理
    - 首次访问自动获取 Cookie
    - 定期刷新避免过期
    """

    def __init__(self):
        self._cookies: dict[str, dict] = {}  # domain -> cookies
        self._last_refresh: dict[str, float] = {}
        self._refresh_interval = 300  # 5分钟刷新一次

    def get_cookies(self, domain: str) -> dict:
        """获取域名对应的 cookies"""
        return self._cookies.get(domain, {})

    def update_cookies(self, domain: str, cookies: dict):
        """更新 cookies"""
        if domain not in self._cookies:
            self._cookies[domain] = {}
        self._cookies[domain].update(cookies)
        self._last_refresh[domain] = time.time()

    def needs_refresh(self, domain: str) -> bool:
        """是否需要刷新"""
        last = self._last_refresh.get(domain, 0)
        return (time.time() - last) > self._refresh_interval

    def clear(self, domain: Optional[str] = None):
        """清除 cookies"""
        if domain:
            self._cookies.pop(domain, None)
            self._last_refresh.pop(domain, None)
        else:
            self._cookies.clear()
            self._last_refresh.clear()


# ─── 代理管理 ─────────────────────────────────────────

class ProxyRotator:
    """代理轮换器"""

    def __init__(self, proxies: list[str]):
        self._proxies = proxies.copy()
        self._index = 0
        self._failed: set[str] = set()

    def get_proxy(self) -> Optional[dict]:
        """获取下一个可用代理"""
        available = [p for p in self._proxies if p not in self._failed]
        if not available:
            logger.warning("无可用代理，使用直连")
            return None

        proxy = available[self._index % len(available)]
        self._index += 1
        return {"http": proxy, "https": proxy}

    def mark_failed(self, proxy_url: str):
        """标记代理失败"""
        self._failed.add(proxy_url)
        logger.warning(f"代理标记失败: {proxy_url}")

    def reset(self):
        """重置失败列表"""
        self._failed.clear()


# ─── 反爬检测诊断 ─────────────────────────────────────

def detect_block(status_code: int, response_text: str) -> tuple[bool, str]:
    """
    检测响应是否被反爬拦截
    返回 (是否被拦截, 拦截类型描述)
    """
    # HTTP 状态码检测
    if status_code == 403:
        return True, "HTTP 403 禁止访问"
    if status_code == 429:
        return True, "HTTP 429 请求过于频繁"
    if status_code == 503:
        return True, "HTTP 503 服务暂不可用（可能是WAF）"
    if status_code == 521:
        return True, "HTTP 521 CloudFlare 拦截"

    # 内容检测
    text_lower = response_text[:5000].lower()
    block_signatures = [
        ("验证码", "需要验证码"),
        ("captcha", "CAPTCHA 验证"),
        ("人机验证", "人机验证"),
        ("访问频率", "访问频率过高"),
        ("请求过于频繁", "请求频率限制"),
        ("access denied", "访问被拒绝"),
        ("系统检测到您的请求", "系统反爬检测"),
        ("滑动验证", "滑动验证码"),
        ("请完成安全验证", "安全验证"),
    ]

    for keyword, desc in block_signatures:
        if keyword in text_lower:
            return True, desc

    return False, ""


# ─── 指纹随机化 ───────────────────────────────────────

def generate_device_fingerprint() -> dict:
    """
    生成随机设备指纹参数（用于传递给需要设备指纹的 API）
    """
    screen_resolutions = [
        (1920, 1080), (2560, 1440), (1366, 768),
        (1536, 864), (1440, 900), (1680, 1050),
    ]
    width, height = random.choice(screen_resolutions)

    return {
        "screen_width": width,
        "screen_height": height,
        "color_depth": random.choice([24, 32]),
        "timezone_offset": -480,  # UTC+8
        "language": "zh-CN",
        "platform": random.choice(["Win32", "MacIntel"]),
        "hardware_concurrency": random.choice([4, 8, 12, 16]),
        "device_memory": random.choice([4, 8, 16]),
    }


def generate_trace_id() -> str:
    """生成类似于各平台追踪ID的随机字符串"""
    seed = f"{time.time()}{random.random()}"
    return hashlib.md5(seed.encode()).hexdigest()
