#!/usr/bin/env python3
"""
ebrun-original-news - 获取亿邦动力网最新电商新闻
通过本地脚本获取新闻数据，避免 Claude Code 网络限制

用法:
    python3 fetch_news.py <channel_path_or_url>               # 默认输出 JSON
    python3 fetch_news.py <channel_path_or_url> --json        # 强制输出 JSON
    python3 fetch_news.py <channel_path_or_url> --table       # 强制输出 ASCII 表格
    python3 fetch_news.py <channel_path_or_url> --limit 10    # 仅返回前 10 条
    python3 fetch_news.py --help                              # 显示帮助
"""

import argparse
import json
import re
import sys
import socket
import time
from urllib import request
from urllib.error import HTTPError, URLError
from typing import List, Dict, Optional
from urllib.parse import urlparse

# 安全配置
ALLOWED_DOMAINS = ['www.ebrun.com', 'api.ebrun.com']
DEFAULT_BASE_URL = 'https://www.ebrun.com/'
DEFAULT_LIMIT = 10
DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 3
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.ebrun.com/'
}
CONTROL_CHAR_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


class FetchNewsError(Exception):
    """用于向 CLI 返回稳定错误码和错误信息。"""

    def __init__(self, message: str, exit_code: int):
        super().__init__(message)
        self.exit_code = exit_code


def print_error(message: str):
    print(f"[ERROR] {message}", file=sys.stderr)


def print_warning(message: str):
    print(f"[WARN] {message}", file=sys.stderr)

def is_safe_url(url: str) -> bool:
    """校验 URL 安全性"""
    try:
        parsed = urlparse(url)
        if parsed.scheme != 'https':
            return False
        return any(parsed.hostname == d or (parsed.hostname and parsed.hostname.endswith('.' + d)) 
                   for d in ALLOWED_DOMAINS)
    except Exception:
        return False


def validate_limit(limit: int) -> int:
    """校验 limit 参数，确保其为非负整数。"""
    if limit < 0:
        raise FetchNewsError('参数错误: --limit 必须大于等于 0', 2)
    return limit


def validate_base_url(base_url: str) -> str:
    """校验 base_url，防止通过参数绕过域名白名单。"""
    normalized = base_url.strip()
    if not normalized:
        raise FetchNewsError('参数错误: --base-url 不能为空', 2)
    if not is_safe_url(normalized.rstrip('/') + '/'):
        raise FetchNewsError(f'安全性风险: 非授权基础地址 -> {base_url}', 3)
    return normalized

def resolve_api_url(channel_path_or_url: str, base_url: str) -> str:
    """将频道路径或完整 URL 解析成最终 API URL"""
    value = channel_path_or_url.strip()
    if not value:
        raise FetchNewsError('参数错误: channel_path_or_url 不能为空', 2)
    if value.startswith(('http://', 'https://')):
        return value

    normalized_base = base_url.rstrip('/') + '/'
    normalized_path = value.lstrip('/')
    if not normalized_path.endswith('.json'):
        normalized_path += '.json'
    return normalized_base + normalized_path


def validate_articles(data: object) -> List[Dict]:
    """校验响应结构，只接受对象数组。"""
    if not isinstance(data, list):
        raise FetchNewsError('接口返回格式异常: 顶层数据不是数组', 7)

    articles: List[Dict] = []
    for item in data:
        if not isinstance(item, dict):
            raise FetchNewsError('接口返回格式异常: 数组元素不是对象', 7)
        sanitized = dict(item)
        for field in ('title', 'author', 'summary', 'description', 'publish_time', 'publishTime'):
            if field in sanitized:
                sanitized[field] = normalize_text(sanitized.get(field))
        for field in ('url', 'link'):
            if field in sanitized:
                sanitized[field] = normalize_article_url(sanitized.get(field))
        articles.append(sanitized)
    return articles


def normalize_text(value: object) -> str:
    if value is None:
        return ''
    text = str(value).replace('\r', ' ').replace('\n', ' ').replace('\t', ' ')
    text = CONTROL_CHAR_RE.sub('', text)
    return ' '.join(text.split())


def normalize_article_url(value: object) -> str:
    normalized = normalize_text(value)
    if not normalized:
        return ''
    return normalized if is_safe_url(normalized) else ''


def get_error_reason(error: BaseException) -> Optional[str]:
    reason = getattr(error, 'reason', None)
    if reason is None:
        return None
    if isinstance(reason, BaseException):
        return str(reason)
    return str(reason)


def should_retry_http(status_code: int) -> bool:
    return status_code in RETRYABLE_STATUS_CODES


def should_retry_network(error: BaseException) -> bool:
    if isinstance(error, TimeoutError):
        return True
    if isinstance(error, socket.timeout):
        return True
    if isinstance(error, URLError):
        reason = getattr(error, 'reason', None)
        return isinstance(reason, (TimeoutError, socket.timeout))
    return False


def map_http_error(error: HTTPError) -> FetchNewsError:
    status_code = error.code
    if status_code == 403:
        return FetchNewsError('请求被拒绝: HTTP 403，请检查请求来源或访问限制', 6)
    if status_code == 404:
        return FetchNewsError('资源不存在: HTTP 404，请检查频道路径或该频道当前是否有数据', 5)
    if status_code == 503:
        return FetchNewsError('服务暂时不可用: HTTP 503，可稍后重试', 4)
    return FetchNewsError(f'请求失败: HTTP {status_code}', 4)


def map_network_error(error: BaseException) -> FetchNewsError:
    if should_retry_network(error):
        return FetchNewsError('网络请求超时，请稍后重试', 4)
    reason = get_error_reason(error)
    if reason:
        return FetchNewsError(f'网络请求失败: {reason}', 4)
    return FetchNewsError(f'网络请求失败: {error}', 4)

def fetch_news(api_url: str, limit: int, retries: int = DEFAULT_RETRIES, timeout: int = DEFAULT_TIMEOUT) -> List[Dict]:
    """从 API 获取新闻数据"""
    if not is_safe_url(api_url):
        raise FetchNewsError(f'安全性风险: 禁止请求非授权域名或不安全协议 -> {api_url}', 3)

    last_error: Optional[FetchNewsError] = None
    for attempt in range(1, retries + 1):
        try:
            req = request.Request(api_url, headers=HEADERS)
            with request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode('utf-8')
                data = json.loads(content)
                articles = validate_articles(data)
                return articles[:limit] if limit > 0 else articles
        except HTTPError as error:
            last_error = map_http_error(error)
            if not should_retry_http(error.code) or attempt >= retries:
                raise last_error
            print_warning(f'{last_error}. 第 {attempt} 次请求失败，准备重试...')
        except json.JSONDecodeError as error:
            raise FetchNewsError(f'JSON 解析失败: {error}', 7) from error
        except (URLError, TimeoutError, socket.timeout) as error:
            last_error = map_network_error(error)
            if not should_retry_network(error) or attempt >= retries:
                raise last_error
            print_warning(f'{last_error}. 第 {attempt} 次请求失败，准备重试...')
        except Exception as error:
            raise FetchNewsError(f'获取数据异常: {error}', 4) from error

        time.sleep(min(attempt, 2))

    if last_error is not None:
        raise last_error

    raise FetchNewsError('获取数据失败: 未知错误', 4)

def print_ascii_table(articles: List[Dict]):
    """以 ASCII 表格格式输出文章列表"""
    if not articles:
        print("暂无文章数据")
        return

    width = 72
    print(f"\n┌{'─' * (width - 2)}┐")
    print(f"│  亿邦动力网 - 最新电商新闻{' ' * (width - 2 - 24)}│")
    print(f"├{'─' * (width - 2)}┤")

    for i, article in enumerate(articles):
        title = str(article.get('title', '无标题'))[:58]
        author = str(article.get('author', '未知'))[:12]
        pub_time = str(article.get('publish_time', article.get('publishTime', '')))[:16]
        summary = str(article.get('summary', article.get('description', '暂无摘要')))[:64]
        url = str(article.get('url', article.get('link', '')))[:64]

        print(f"│  {i+1:2d}. {title:<58} │")
        print(f"│       👤 {author:<12}  🕐 {pub_time:<16} │")
        print(f"│       {summary:<68} │")
        if url:
            print(f"│       {url:<68} │")
        if i < len(articles) - 1:
            print(f"├{'─' * (width - 2)}┤")

    print(f"└{'─' * (width - 2)}┘")
    print(f"\n共 {len(articles)} 篇文章")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='获取亿邦动力网最新电商新闻',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('channel_path_or_url', help='频道路径或 API 接口 URL')
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument('--json', action='store_true', help='强制输出 JSON 格式')
    output_group.add_argument('--table', action='store_true', help='强制输出 ASCII 表格')
    parser.add_argument('--base-url', default=DEFAULT_BASE_URL, help='基础 URL，默认 https://www.ebrun.com/')
    parser.add_argument('--limit', type=int, default=DEFAULT_LIMIT, help='返回文章条数，默认 10，传 0 表示不限制')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help='单次请求超时时间（秒），默认 10')
    parser.add_argument('--retries', type=int, default=DEFAULT_RETRIES, help='最大请求次数，默认 3')

    try:
        args = parser.parse_args()
        limit = validate_limit(args.limit)
        if args.timeout <= 0:
            raise FetchNewsError('参数错误: --timeout 必须大于 0', 2)
        if args.retries <= 0:
            raise FetchNewsError('参数错误: --retries 必须大于 0', 2)

        base_url = validate_base_url(args.base_url)
        api_url = resolve_api_url(args.channel_path_or_url, base_url)
        articles = fetch_news(api_url, limit, retries=args.retries, timeout=args.timeout)
    except FetchNewsError as error:
        print_error(str(error))
        sys.exit(error.exit_code)

    if args.table:
        output_format = 'table'
    else:
        output_format = 'json'

    if output_format == 'table':
        print_ascii_table(articles)
    else:
        print(json.dumps(articles, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
