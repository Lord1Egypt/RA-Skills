"""
BiliYouTik2Brain — 反爬中间件层 (v4.0)

一等公民设计：反爬不是事后补的补丁，而是夹在平台适配器和网络请求
之间的独立层。所有 HTTP 请求必须经过此层，自动注入反爬策略。

功能:
  - UA 轮转（10+ 真实浏览器 UA）
  - Cookie 管理（浏览器自动提取 + 过期刷新）
  - 代理轮转（多代理池，按平台自动选最优）
  - 请求节流（指数退避 + 平台专属冷却）
  - 指纹预热（抖音 Session / B站首页 cookie）
  - 降级策略（逐级回退，不硬刚）
"""

import os
import re
import time
import random
import json
import http.client
import subprocess
import urllib.request
import ssl
from typing import Dict, List, Optional, Tuple, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


def _create_insecure_ssl_context():
    """创建跳过证书验证的 SSL 上下文。

    ⚠️ WARNING: 仅用于反爬/代理穿透场景，不得用于任何需验证
    peer 身份的环境。此函数存在的唯一理由是某些 CDN/代理/WAF
    组合下 HTTPS 握手会因证书链不完整而失败，且无备选修复路径。
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


# ═══════════════════════════════════════════════════════════
#  UA 池
# ═══════════════════════════════════════════════════════════

# 通用 UA 池（桌面浏览器，按市场份额加权）
_UA_POOL_DESKTOP = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

# 移动端 UA（抖音等平台需要）
_UA_POOL_MOBILE = [
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
]

# B站专属 UA（B站对桌面 Chrome 最友好）
_UA_POOL_BILIBILI = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]


def get_ua(platform: str = "", mobile: bool = False) -> str:
    """获取随机 UA

    Args:
        platform: 平台名（bilibili/douyin/youtube/xiaohongshu），为空则用通用池
        mobile: 是否用移动端 UA

    Returns:
        随机选中的 UA 字符串
    """
    if platform == "bilibili" and not mobile:
        pool = _UA_POOL_BILIBILI
    elif mobile:
        pool = _UA_POOL_MOBILE
    else:
        pool = _UA_POOL_DESKTOP
    return random.choice(pool)


# ═══════════════════════════════════════════════════════════
#  Cookie 管理
# ═══════════════════════════════════════════════════════════

# 浏览器 Cookie 路径
_COOKIE_PATHS = {
    "chrome": {
        "win32": os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies"),
        "darwin": os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/Cookies"),
        "linux": os.path.expanduser("~/.config/google-chrome/Default/Cookies"),
    },
    "edge": {
        "win32": os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies"),
        "darwin": os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default/Cookies"),
        "linux": os.path.expanduser("~/.config/microsoft-edge/Default/Cookies"),
    },
}

# 平台对应的 Cookie 域名
_COOKIE_DOMAINS = {
    "bilibili": [".bilibili.com"],
    "youtube": [".youtube.com", ".google.com"],
    "douyin": [".douyin.com", ".iesdouyin.com"],
    "xiaohongshu": [".xiaohongshu.com", ".xhslink.com"],
}


def extract_cookies(browser: str = "edge", platform: str = "") -> List[Dict]:
    """从浏览器提取 Cookie

    策略：用 yt-dlp 的 --cookies-from-browser 功能提取，安全且可靠。

    Args:
        browser: 浏览器名（chrome / edge）
        platform: 平台名，用于过滤只取该平台相关 cookie

    Returns:
        Cookie 列表 [{name, value, domain, path, expires}]
    """
    sys_platform = os.sys.platform if hasattr(os, 'sys') else 'linux'
    cookie_path = _COOKIE_PATHS.get(browser, {}).get(sys_platform, "")

    if not cookie_path or not os.path.exists(cookie_path):
        return []

    cookies = []
    domains = _COOKIE_DOMAINS.get(platform, [])

    try:
        # 用 yt-dlp 提取（最安全的方式，不直接读 SQLite）
        result = subprocess.run(
            ["yt-dlp", "--cookies-from-browser", browser, "--no-download",
             "--dump-single-json", "https://www.example.com"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            cookies = data.get("cookies", [])
    except Exception:
        pass

    # 按平台过滤
    if domains:
        cookies = [c for c in cookies if any(c.get("domain", "").endswith(d.lstrip(".")) for d in domains)]

    return cookies


def get_cookies_for_platform(platform: str) -> Optional[Dict[str, str]]:
    """获取指定平台的 Cookie 字典（name → value）"""
    cookies = []
    for browser in ["edge", "chrome"]:
        cookies = extract_cookies(browser, platform)
        if cookies:
            break

    if not cookies:
        return None

    return {c["name"]: c["value"] for c in cookies if "name" in c and "value" in c}


# ═══════════════════════════════════════════════════════════
#  代理管理
# ═══════════════════════════════════════════════════════════

# 常见代理端口（按常见程度排序）
_KNOWN_PROXY_PORTS = [7890, 7897, 9981, 10809, 1080, 20170]

# 代理名称映射
_PROXY_NAMES = {
    7890: "clash",
    7897: "mihomo",
    9981: "clash-verge",
    10809: "v2ray",
    1080: "socks5",
}


def _probe_proxy(port: int, test_url: str = "https://www.google.com") -> bool:
    """探测某个端口是否是可用 HTTP 代理"""
    proxy_url = f"http://127.0.0.1:{port}"
    ctx = _create_insecure_ssl_context()
    try:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url}),
            urllib.request.HTTPSHandler(context=ctx)
        )
        req = urllib.request.Request(test_url, method="HEAD")
        resp = opener.open(req, timeout=5)
        return resp.status in (200, 301, 302, 307, 308)
    except Exception:
        return False


def find_available_proxy(platform: str = "") -> Optional[Tuple[str, int]]:
    """查找可用代理

    Returns:
        (proxy_url, port) 或 None（直连可达时）
    """
    # 先测直连
    test_url = "https://www.youtube.com" if platform == "youtube" else "https://www.google.com"
    try:
        ctx = _create_insecure_ssl_context()
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ctx)
        )
        req = urllib.request.Request(test_url, method="HEAD")
        resp = opener.open(req, timeout=5)
        if resp.status in (200, 301, 302, 307, 308):
            return None  # 直连可达，不需要代理
    except Exception:
        pass

    # 扫描代理端口
    for port in _KNOWN_PROXY_PORTS:
        if _probe_proxy(port, test_url):
            name = _PROXY_NAMES.get(port, f"port:{port}")
            return (f"http://127.0.0.1:{port}", port)

    return None


# ═══════════════════════════════════════════════════════════
#  请求节流 & 熔断
# ═══════════════════════════════════════════════════════════

@dataclass
class ThrottleState:
    """节流状态"""
    fail_count: int = 0
    last_fail_time: float = 0.0
    throttled_until: float = 0.0
    is_throttled: bool = False


_throttle: Dict[str, ThrottleState] = {}


def check_throttle(platform: str) -> Tuple[bool, str]:
    """检查是否被节流（熔断）

    Returns:
        (allowed, reason)
    """
    state = _throttle.get(platform)
    if not state:
        return True, "ok"

    if state.is_throttled and time.time() < state.throttled_until:
        remaining = state.throttle_until - time.time()
        return False, f"熔断中，还需 {remaining:.0f} 秒"

    # 冷却期已过，重置
    if state.is_throttled and time.time() >= state.throttle_until:
        state.is_throttled = False
        state.fail_count = 0

    return True, "ok"


def record_success(platform: str):
    """记录成功请求，重置节流"""
    _throttle.pop(platform, None)


def record_failure(platform: str, cooldown: int = 900, threshold: int = 3):
    """记录失败请求，达到阈值触发熔断

    Args:
        platform: 平台名
        cooldown: 熔断冷却时间（秒）
        threshold: 连续失败阈值
    """
    if platform not in _throttle:
        _throttle[platform] = ThrottleState()

    state = _throttle[platform]
    state.fail_count += 1
    state.last_fail_time = time.time()

    if state.fail_count >= threshold:
        state.is_throttled = True
        state.throttled_until = time.time() + cooldown


# ═══════════════════════════════════════════════════════════
#  反爬中间件主入口
# ═══════════════════════════════════════════════════════════

@dataclass
class AntiCrawlContext:
    """反爬上下文（每次请求创建）"""
    platform: str
    url: str
    timeout: int = 30
    max_retries: int = 3


def anti_crawl_request(
    url: str,
    platform: str = "",
    method: str = "GET",
    data: Optional[bytes] = None,
    headers: Optional[Dict] = None,
    timeout: int = 30,
    use_proxy: bool = False,
    mobile: bool = False,
) -> "http.client.HTTPResponse":
    """带反爬保护的 HTTP 请求

    自动注入:
    - UA 轮转
    - Cookie（从浏览器提取）
    - 代理（如 need_proxy 或 use_proxy=True）
    - 节流检查
    - 重试 + 指数退避

    Args:
        url: 请求 URL
        platform: 平台名（用于选择 UA 池和 Cookie）
        method: HTTP 方法
        data: 请求体
        headers: 额外 headers（会覆盖自动注入的）
        timeout: 超时时间
        use_proxy: 是否强制走代理
        mobile: 是否用移动端 UA

    Returns:
        http.client.HTTPResponse

    Raises:
        AntiCrawlError: 请求失败
    """
    ctx = AntiCrawlContext(platform=platform, url=url, timeout=timeout)

    # 1. 检查熔断
    allowed, reason = check_throttle(platform)
    if not allowed:
        raise AntiCrawlError(f"平台 {platform} {reason}")

    # 2. 准备请求头
    req_headers = {
        "User-Agent": get_ua(platform, mobile),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    # Referer
    referers = {
        "bilibili": "https://www.bilibili.com/",
        "douyin": "https://www.douyin.com/",
        "xiaohongshu": "https://www.xiaohongshu.com/",
        "youtube": "https://www.youtube.com/",
    }
    if platform in referers:
        req_headers["Referer"] = referers[platform]

    if headers:
        req_headers.update(headers)

    # 3. Cookie
    cookies = get_cookies_for_platform(platform)
    if cookies:
        cookie_str = "; ".join(f"{k}={v}" for k, v in cookies.items())
        req_headers["Cookie"] = cookie_str

    # 4. 代理
    proxy_handler = None
    if use_proxy or (platform == "youtube"):
        proxy = find_available_proxy(platform)
        if proxy:
            proxy_handler = urllib.request.ProxyHandler(
                {"http": proxy[0], "https": proxy[0]}
            )

    # 5. SSL（不禁用证书验证，除非代理特殊需要）
    ctx_ssl = ssl.create_default_context()
    # 注意：不再默认禁用 CERT_NONE

    # 6. 执行请求（带重试 + 指数退避）
    last_error = None
    for attempt in range(ctx.max_retries if hasattr(ctx, 'max_retries') else 3):
        try:
            if proxy_handler:
                opener = urllib.request.build_opener(proxy_handler, urllib.request.HTTPSHandler(context=ctx_ssl))
            else:
                opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx_ssl))

            req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
            resp = opener.open(req, timeout=timeout)

            # 成功 → 重置节流
            record_success(platform)
            return resp

        except urllib.error.HTTPError as e:
            last_error = e
            if e.code == 412:
                # B站 412 → 直接熔断，不重试
                record_failure(platform, cooldown=900, threshold=1)
                raise AntiCrawlError(f"B站 API 412 反爬拦截", code=412)
            elif e.code == 403:
                # 403 → 可能是 cookie 过期，尝试刷新
                cookies = get_cookies_for_platform(platform)  # 重新提取
                if cookies:
                    req_headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in cookies.items())
                # 指数退避
                time.sleep(2 ** attempt)
            elif e.code == 429:
                # 429 → 限流，等更久
                wait = min(30, 5 * (attempt + 1))
                time.sleep(wait)
            else:
                break

        except urllib.error.URLError as e:
            last_error = e
            # 网络错误 → 指数退避
            time.sleep(2 ** attempt)

        except Exception as e:
            last_error = e
            time.sleep(2 ** attempt)

    # 全部重试失败
    if platform:
        record_failure(platform)
    raise AntiCrawlError(f"请求失败 ({ctx.max_retries} 次重试耗尽): {last_error}")


class AntiCrawlError(Exception):
    """反爬相关错误"""
    def __init__(self, message: str, code: int = 0):
        super().__init__(message)
        self.code = code


# ═══════════════════════════════════════════════════════════
#  指纹预热
# ═══════════════════════════════════════════════════════════

def warmup_session(platform: str) -> bool:
    """Session 预热（某些平台需要先访问首页才能正常下载）

    Args:
        platform: 平台名

    Returns:
        是否成功
    """
    warmup_urls = {
        "bilibili": "https://www.bilibili.com/",
        "douyin": "https://www.douyin.com/",
        "xiaohongshu": "https://www.xiaohongshu.com/",
        "youtube": "https://www.youtube.com/",
    }

    url = warmup_urls.get(platform)
    if not url:
        return True  # 不需要预热

    try:
        anti_crawl_request(url, platform=platform, timeout=10)
        return True
    except AntiCrawlError:
        return False


# ═══════════════════════════════════════════════════════════
#  降级策略
# ═══════════════════════════════════════════════════════════

@dataclass
class FallbackResult:
    """降级结果"""
    success: bool
    method: str           # 成功的方法名
    data: Any = None
    error: str = ""


def try_fallback(actions: List[Callable], platform: str = "") -> FallbackResult:
    """逐级降级尝试

    Args:
        actions: 降级动作列表，按优先级从高到低排列
        platform: 平台名（用于节流记录）

    Returns:
        FallbackResult
    """
    for action in actions:
        try:
            result = action()
            if result:
                record_success(platform)
                return FallbackResult(success=True, method=action.__name__, data=result)
        except Exception as e:
            continue

    if platform:
        record_failure(platform)

    last_action = actions[-1] if actions else None
    return FallbackResult(
        success=False,
        method=last_action.__name__ if last_action else "none",
        error="所有降级动作均失败"
    )
