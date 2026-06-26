"""
基础抓取器：定义统一接口 + 共享 HTTP 请求逻辑
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from urllib.parse import urlparse
from utils.http_client import get_with_retry, DEFAULT_USER_AGENT
from utils.logger import logger


class BaseFetcher(ABC):
    """基础抓取器抽象类"""

    # 所有子类共享的默认请求头
    DEFAULT_HEADERS = {
        'User-Agent': DEFAULT_USER_AGENT,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    def __init__(self, cookies_file: str = None):
        self.cookies_file = cookies_file
        # 结构化存储: [{'domain': '.zhihu.com', 'name': 'xxx', 'value': 'yyy'}, ...]
        self.cookies_list = self._load_cookies() if cookies_file else []
        self.headers = dict(self.DEFAULT_HEADERS)

    def _load_cookies(self) -> list:
        """加载 Netscape 格式 Cookies 文件，返回结构化列表"""
        try:
            cookies = []
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('# ') or line.startswith('#\t'):
                        continue
                    if line.startswith('#HttpOnly'):
                        line = line[len('#HttpOnly'):].strip()
                    if '\t' not in line:
                        continue
                    parts = line.split('\t')
                    # Netscape: domain\tflag\tpath\tsecure\texpiration\tname\tvalue
                    if len(parts) >= 7 and '=' not in parts[0]:
                        cookies.append({
                            'domain': parts[0].lower(),
                            'name': parts[5],
                            'value': parts[6],
                        })
            logger.debug(f"加载 Cookies: {len(cookies)} 个 ({self.cookies_file})")
            return cookies
        except Exception as e:
            logger.warning(f"加载 Cookies 失败：{e}")
            return []

    @staticmethod
    def _domain_matches(cookie_domain: str, hostname: str) -> bool:
        """检查 cookie domain 是否与目标 hostname 匹配"""
        hostname = hostname.lower()
        if cookie_domain.startswith('.'):
            # 子域名匹配: .zhihu.com 匹配 www.zhihu.com、zhihu.com
            return hostname == cookie_domain[1:] or hostname.endswith(cookie_domain)
        return hostname == cookie_domain

    def _apply_cookies_for_url(self, url: str):
        """仅将匹配目标 URL 域名的 Cookies 添加到请求头"""
        if not self.cookies_list:
            return
        hostname = urlparse(url).hostname
        if not hostname:
            return
        matched = [
            c for c in self.cookies_list
            if self._domain_matches(c['domain'], hostname)
        ]
        if matched:
            cookie_header = '; '.join(f"{c['name']}={c['value']}" for c in matched)
            self.headers['Cookie'] = cookie_header
            logger.debug(f"应用 Cookies: {len(matched)}/{len(self.cookies_list)} 个 → {hostname}")

    def _fetch_html(self, url: str, headers: dict = None, timeout: int = 30) -> str:
        """发送 GET 请求并返回 HTML 文本"""
        resp = get_with_retry(url, headers=headers or self.headers, timeout=timeout)
        resp.encoding = 'utf-8'
        return resp.text

    @abstractmethod
    def fetch_article(self, url: str) -> Dict:
        """
        抓取文章内容

        Returns:
            dict: title, author, pub_date, content (HTML), images, original_url
        """
        pass
