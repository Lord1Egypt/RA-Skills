#!/usr/bin/env python3
"""
AI-Sentinel 安全版 HTTP 请求模块

本模块使用 Python 标准库 urllib 替代 requests
避免被某些杀软误报

使用方法:
    from safe_http import safe_get
    data = safe_get("https://api.github.com/search/repositories", params={"q": "python"})
"""
from urllib.request import urlopen, Request
from urllib.parse import urlencode, urlparse
import json
import ssl
from typing import Optional, Dict, Any


# 默认请求头
DEFAULT_HEADERS = {
    "User-Agent": "AI-Sentinel/1.4.1 (+https://github.com/xiaopengs/ai-sentinel)",
    "Accept": "application/json, text/plain, */*"
}


class SafeHTTPError(Exception):
    """安全的HTTP错误"""
    pass


class RateLimitError(SafeHTTPError):
    """速率限制错误"""
    pass


class DomainNotAllowedError(SafeHTTPError):
    """域名不在白名单"""
    pass


# 安全域名白名单
ALLOWED_DOMAINS = {
    # GitHub
    "api.github.com",
    "github.com",
    "githubusercontent.com",
    # arXiv
    "export.arxiv.org",
    "arxiv.org",
    # HackerNews
    "hacker-news.firebaseio.com",
    "ycombinator.com",
    "news.ycombinator.com",
    # Twitter
    "api.twitter.com",
    "x.com",
    "twitter.com",
}


def is_domain_allowed(url: str) -> bool:
    """检查域名是否在白名单中"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        # 移除端口号
        if ":" in domain:
            domain = domain.split(":")[0]
        # 检查是否匹配
        for allowed in ALLOWED_DOMAINS:
            if domain == allowed or domain.endswith("." + allowed):
                return True
        return False
    except Exception:
        return False


def safe_get(
    url: str,
    params: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    timeout: int = 30,
    verify_ssl: bool = True
) -> Dict[str, Any]:
    """
    安全的GET请求
    
    Args:
        url: 请求URL
        params: 查询参数
        headers: 请求头
        timeout: 超时时间（秒）
        verify_ssl: 是否验证SSL证书
    
    Returns:
        解析后的JSON响应
    
    Raises:
        DomainNotAllowedError: 域名不在白名单
        RateLimitError: 请求被限流
        SafeHTTPError: 其他HTTP错误
    """
    # 1. 安全检查
    if not is_domain_allowed(url):
        raise DomainNotAllowedError(f"域名不在白名单中: {urlparse(url).netloc}")
    
    # 2. 构建URL
    if params:
        query_string = urlencode(params)
        if "?" in url:
            url = f"{url}&{query_string}"
        else:
            url = f"{url}?{query_string}"
    
    # 3. 构建请求头
    request_headers = DEFAULT_HEADERS.copy()
    if headers:
        request_headers.update(headers)
    
    # 4. 创建请求
    try:
        request = Request(url, headers=request_headers, method="GET")
        
        # 5. 配置SSL上下文
        if not verify_ssl:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
        else:
            ssl_context = None
        
        # 6. 发送请求
        with urlopen(request, timeout=timeout, context=ssl_context) as response:
            content = response.read().decode("utf-8")
            
            # 7. 解析响应
            content_type = response.headers.get("Content-Type", "")
            if "json" in content_type:
                return json.loads(content)
            else:
                return {"_raw": content, "_content_type": content_type}
                
    except Exception as e:
        error_msg = str(e)
        
        if "timed out" in error_msg.lower():
            raise SafeHTTPError(f"请求超时: {url}")
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            raise RateLimitError(f"请求被限流: {url}")
        elif "403" in error_msg:
            raise SafeHTTPError(f"访问被拒绝(403): {url}")
        elif "404" in error_msg:
            raise SafeHTTPError(f"资源不存在(404): {url}")
        else:
            raise SafeHTTPError(f"请求失败: {error_msg}")


def safe_get_text(url: str, **kwargs) -> str:
    """获取纯文本响应"""
    result = safe_get(url, **kwargs)
    if isinstance(result, dict) and "_raw" in result:
        return result["_raw"]
    return json.dumps(result, ensure_ascii=False)


def safe_get_raw(url: str, timeout: int = 30) -> bytes:
    """获取原始字节数据"""
    if not is_domain_allowed(url):
        raise DomainNotAllowedError(f"域名不在白名单中")
    
    request = Request(url, headers=DEFAULT_HEADERS)
    with urlopen(request, timeout=timeout) as response:
        return response.read()


# 示例用法
if __name__ == "__main__":
    # 测试 GitHub API
    try:
        result = safe_get(
            "https://api.github.com/search/repositories",
            params={"q": "language:python", "sort": "stars", "per_page": 5}
        )
        print(f"✅ GitHub API 请求成功，共 {result.get('total_count', 0)} 个仓库")
        for item in result.get("items", [])[:3]:
            print(f"  - {item['full_name']}: ⭐ {item['stargazers_count']}")
    except SafeHTTPError as e:
        print(f"❌ 请求失败: {e}")
    
    # 测试 HackerNews API
    try:
        result = safe_get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        print(f"✅ HackerNews API 请求成功，共 {len(result)} 个热门故事")
    except SafeHTTPError as e:
        print(f"❌ HackerNews 请求失败: {e}")
    
    # 测试域名白名单（应该被拒绝）
    try:
        result = safe_get("https://malicious-site.com/api")
        print("❌ 应该被拒绝的请求通过了！")
    except DomainNotAllowedError as e:
        print(f"✅ 恶意域名被正确拦截: {e}")
