#!/usr/bin/env python3
"""
Amber Url to Markdown - URL 请求模块（V3.1 优化版）
负责抓取网页内容，包含错误处理、UA 模拟、robots.txt 检查、重试机制、编码识别

作者：小文
时间：2026-03-24
版本：V3.1
"""

import requests
from requests.exceptions import RequestException, Timeout, HTTPError, ConnectionError
import time
import random
from typing import Optional, Dict, Callable, TypeVar
from functools import wraps
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

# 导入配置
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from config import get_fetch_config

# 类型变量
T = TypeVar('T')


# ============================================================================
# 常量定义（从配置获取）
# ============================================================================

def get_default_headers() -> Dict[str, str]:
    """获取默认请求头"""
    cfg = get_fetch_config()
    return {
        "User-Agent": cfg.USER_AGENT,
        "Accept": cfg.ACCEPT,
        "Accept-Language": cfg.ACCEPT_LANGUAGE,
        "Connection": cfg.CONNECTION,
    }


# ============================================================================
# 重试装饰器
# ============================================================================

def retry_decorator(
    max_retries: int = None,
    delay: float = None,
    exceptions: tuple = None,
    log_prefix: str = ""
):
    """
    通用重试装饰器（仅适配幂等请求）
    
    Args:
        max_retries: 最大重试次数（默认从配置读取）
        delay: 重试延迟（秒，默认从配置读取）
        exceptions: 需要重试的异常类型（默认：RequestException）
        log_prefix: 日志前缀
    
    Returns:
        callable: 装饰器函数
    """
    cfg = get_fetch_config()
    
    if max_retries is None:
        max_retries = cfg.RETRY_TIMES
    if delay is None:
        delay = cfg.RETRY_DELAY
    if exceptions is None:
        exceptions = (RequestException,)
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[T]:
            last_exception = None
            
            for attempt in range(1, max_retries + 2):  # +1 为原始请求
                try:
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt > max_retries:
                        # 超过最大重试次数，放弃
                        print(f"[ERROR] ❌ {log_prefix}{func.__name__} 失败（已重试{max_retries}次）: {str(e)[:80]}")
                        break
                    
                    # 等待后重试
                    print(f"[WARN] ⚠️ {log_prefix}{func.__name__} 失败（第{attempt}次），{delay}秒后重试：{str(e)[:60]}")
                    time.sleep(delay)
                    
                except Exception as e:
                    # 非预期异常，直接抛出
                    print(f"[ERROR] ❌ {log_prefix}{func.__name__} 未知错误：{type(e).__name__}: {str(e)[:80]}")
                    raise
            
            return None
        
        return wrapper
    return decorator


# ============================================================================
# robots.txt 检查
# ============================================================================

def is_allowed_by_robots(url: str, user_agent: str = "amber-url-to-markdown") -> bool:
    """
    判断是否允许爬取目标 URL（遵循 robots.txt 协议）
    
    Args:
        url: 目标 URL
        user_agent: 用户代理标识
    
    Returns:
        bool: 是否允许爬取（True=允许，False=禁止，无法获取时默认允许）
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return True
        
        # 构建 robots.txt URL
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        # 使用官方 RobotFileParser
        parser = RobotFileParser()
        parser.set_url(robots_url)
        
        # 获取并解析 robots.txt
        try:
            parser.read()
            return parser.can_fetch(user_agent, url)
        except Exception:
            # 无法获取 robots.txt 时默认允许（可按需调整）
            return True
            
    except Exception as e:
        print(f"[WARN] robots.txt 检查失败：{str(e)[:50]}，默认允许爬取")
        return True


# ============================================================================
# 编码检测
# ============================================================================

def detect_encoding(content: bytes, fallback: str = "utf-8") -> str:
    """
    自动检测编码格式
    
    Args:
        content: 原始字节内容
        fallback: 检测失败时的默认编码
    
    Returns:
        str: 检测到的编码格式
    """
    try:
        import chardet
        result = chardet.detect(content)
        confidence = result.get('confidence', 0)
        encoding = result.get('encoding', fallback)
        
        # 置信度低于 0.5 时使用默认编码
        if confidence < 0.5:
            print(f"[WARN] 编码检测置信度低（{confidence:.2f}），使用默认编码：{fallback}")
            return fallback
        
        # 编码别名映射
        encoding_map = {
            "gbk": "gb2312",
            "gb2312": "gb2312",
            "utf-8-sig": "utf-8",
            "utf8": "utf-8",
            "ascii": "utf-8",
        }
        
        detected = encoding_map.get(encoding.lower() if encoding else "", encoding)
        print(f"[INFO] 编码检测：{encoding} → {detected} (置信度：{confidence:.2f})")
        return detected
        
    except ImportError:
        print("[WARN] chardet 未安装，使用默认编码：utf-8")
        print("[INFO] 安装：pip install chardet")
        return fallback
        
    except Exception as e:
        print(f"[WARN] 编码检测失败：{str(e)[:50]}，使用默认编码：{fallback}")
        return fallback


# ============================================================================
# URL 请求函数
# ============================================================================

@retry_decorator(log_prefix="URL 请求：")
def fetch_url_content(
    url: str, 
    timeout: int = None,
    headers: Optional[Dict[str, str]] = None,
    allow_redirects: bool = True,
    detect_encoding_flag: bool = True
) -> Optional[str]:
    """
    抓取 URL 的 HTML 内容，包含异常处理、浏览器 UA 模拟、编码自动识别
    
    Args:
        url: 目标 URL
        timeout: 请求超时时间（秒）
        headers: 自定义请求头（可选）
        allow_redirects: 是否允许重定向
        detect_encoding_flag: 是否自动检测编码
    
    Returns:
        str: HTML 内容（失败返回 None）
    """
    cfg = get_fetch_config()
    
    if timeout is None:
        timeout = cfg.TIMEOUT
    
    # 默认请求头（浏览器 UA 模拟）
    default_headers = get_default_headers()
    
    # 合并自定义请求头
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.get(
            url, 
            headers=default_headers, 
            timeout=timeout, 
            allow_redirects=allow_redirects
        )
        response.raise_for_status()  # 触发 4xx/5xx HTTP 错误
        
        # 编码处理
        if detect_encoding_flag:
            # 优先使用响应头编码，再使用 chardet 检测
            encoding = response.encoding or detect_encoding(response.content)
            # 编码别名映射
            encoding_map = {"gbk": "gb2312", "utf-8-sig": "utf-8"}
            encoding = encoding_map.get(encoding.lower() if encoding else "", encoding)
            return response.content.decode(encoding, errors="replace")
        else:
            return response.text
        
    except Timeout:
        print(f"[ERROR] ❌ 请求{url}超时（{timeout}秒）")
        return None
        
    except HTTPError as e:
        status_code = e.response.status_code if e.response else "未知"
        print(f"[ERROR] ❌ {url}返回 HTTP 错误：{status_code}")
        return None
        
    except ConnectionError as e:
        print(f"[ERROR] ❌ 连接{url}失败：{str(e)[:80]}")
        return None
        
    except RequestException as e:
        print(f"[ERROR] ❌ 请求{url}失败：{str(e)[:80]}")
        # 重试装饰器会处理重试逻辑
        raise  # 重新抛出，让装饰器处理
        
    except Exception as e:
        print(f"[ERROR] ❌ 未知错误：{type(e).__name__}: {str(e)[:80]}")
        return None


def fetch_with_encoding_detect(url: str, timeout: int = None) -> Optional[str]:
    """
    自动识别编码，修复中文/特殊语言乱码（兼容旧接口）
    
    Args:
        url: 目标 URL
        timeout: 请求超时时间
    
    Returns:
        str: 解码后的内容
    """
    return fetch_url_content(url, timeout=timeout, detect_encoding_flag=True)


# ============================================================================
# 批量请求
# ============================================================================

def batch_fetch_urls(
    urls: list, 
    timeout: int = None,
    check_robots: bool = True,
    random_delay: bool = True
) -> list:
    """
    批量抓取 URL 内容，含限流与合规检查
    
    Args:
        urls: URL 列表
        timeout: 请求超时时间
        check_robots: 是否检查 robots.txt
        random_delay: 是否添加随机延迟
    
    Returns:
        list: [(url, html_content), ...] 成功抓取的元组列表
    """
    cfg = get_fetch_config()
    
    if timeout is None:
        timeout = cfg.TIMEOUT
    
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"[INFO] 抓取进度：{i}/{len(urls)} - {url[:60]}...")
        
        # robots.txt 检查
        if check_robots and not is_allowed_by_robots(url):
            print(f"[WARN] 🚫 跳过禁止爬取的 URL：{url}")
            continue
        
        # 抓取内容
        content = fetch_url_content(url, timeout)
        if content:
            results.append((url, content))
        
        # 随机延迟（降低反爬风险）
        if random_delay and i < len(urls):
            delay = random.uniform(cfg.RANDOM_DELAY_MIN, cfg.RANDOM_DELAY_MAX)
            print(f"[INFO] 等待 {delay:.1f} 秒...")
            time.sleep(delay)
    
    return results


# ============================================================================
# 动态内容抓取（可选扩展）
# ============================================================================

def fetch_dynamic_content(url: str, timeout: int = 10) -> Optional[str]:
    """
    抓取动态渲染页面（JS 加载），失败则降级为普通请求
    
    注意：此功能需要安装 requests-html
    `pip install requests-html`
    
    Args:
        url: 目标 URL
        timeout: 渲染超时时间
    
    Returns:
        str: HTML 内容（失败返回 None）
    """
    try:
        from requests_html import HTMLSession
        session = HTMLSession()
        r = session.get(url)
        r.html.render(timeout=timeout * 1000)  # 毫秒
        return r.html.html
        
    except ImportError:
        print("[WARN] ⚠️ requests-html 未安装，降级为普通请求")
        print("[INFO] 安装：pip install requests-html")
        return fetch_url_content(url)
        
    except Exception as e:
        print(f"[WARN] ⚠️ 动态渲染失败，降级为普通请求：{str(e)[:60]}")
        return fetch_url_content(url)


# ============================================================================
# 鉴权请求（可选扩展）
# ============================================================================

def fetch_with_auth(
    url: str, 
    cookies: Optional[Dict] = None, 
    token: Optional[str] = None,
    timeout: int = None
) -> Optional[str]:
    """
    带 Cookie/Token 的鉴权请求
    
    Args:
        url: 目标 URL
        cookies: Cookie 字典
        token: Bearer Token
        timeout: 超时时间
    
    Returns:
        str: HTML 内容（失败返回 None）
    """
    cfg = get_fetch_config()
    
    if timeout is None:
        timeout = cfg.TIMEOUT
    
    headers = get_default_headers()
    
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(
            url, 
            headers=headers, 
            cookies=cookies, 
            timeout=timeout
        )
        response.raise_for_status()
        
        # 简单校验登录状态（可根据具体网站调整）
        if "登录" in response.text and "退出" not in response.text:
            print("[WARN] ⚠️ 鉴权失败：Cookie/Token 可能无效")
            return None
        
        return response.text
        
    except Exception as e:
        print(f"[ERROR] ❌ 鉴权请求失败：{str(e)[:80]}")
        return None


# ============================================================================
# 测试入口
# ============================================================================

if __name__ == "__main__":
    # 简单测试
    test_url = "https://example.com"
    print(f"测试抓取：{test_url}")
    content = fetch_url_content(test_url)
    if content:
        print(f"✅ 抓取成功，HTML 长度：{len(content)}")
    else:
        print("❌ 抓取失败")
    
    # robots.txt 测试
    print(f"\nrobots.txt 检查：{test_url}")
    allowed = is_allowed_by_robots(test_url)
    print(f"{'✅ 允许爬取' if allowed else '❌ 禁止爬取'}")
    
    # 编码检测测试
    print(f"\n编码检测测试：{test_url}")
    content_bytes = requests.get(test_url).content
    encoding = detect_encoding(content_bytes)
    print(f"检测到的编码：{encoding}")
