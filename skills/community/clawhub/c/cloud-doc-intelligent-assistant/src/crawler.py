"""文档爬虫模块 - 使用阿里云文档 JSON API"""

import logging
import time
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from .models import Document
from .utils import compute_content_hash


ALIYUN_DOC_API = "https://help.aliyun.com/help/json/document_detail.json"
ALIYUN_SEARCH_API = "https://help.aliyun.com/help/json/search.json"


def url_to_alias(doc_url: str) -> str:
    path = urlparse(doc_url).path
    if path.startswith("/zh/"):
        path = path[3:]
    elif path.startswith("/zh"):
        path = path[3:]
    return path.rstrip("/").split("?")[0]


def alias_to_url(alias: str) -> str:
    if not alias.startswith("/"):
        alias = "/" + alias
    return f"https://help.aliyun.com/zh{alias}"


class DocumentCrawler:
    """文档爬虫类 - 基于阿里云 JSON API"""

    def __init__(self, request_delay: float = 1.0, max_retries: int = 3, timeout: int = 30):
        self.request_delay = request_delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.session = requests.Session()
        self.last_request_time = 0.0
        self._consecutive_failures = 0

    def _rate_limit(self) -> None:
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_request_time = time.time()

    @staticmethod
    def _normalize_alias(alias: str) -> str:
        alias = alias.strip().lower()
        if not alias.startswith("/"):
            alias = "/" + alias
        return alias.rstrip("/")

    def _fetch_api_data(self, api_url: str, params: dict, api_name: str) -> Optional[dict]:
        last_error = None
        for attempt in range(1, self.max_retries + 1):
            self._rate_limit()
            try:
                resp = self.session.get(api_url, params=params, timeout=self.timeout)
                resp.raise_for_status()
                content_type = resp.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    raise RuntimeError(f"{api_name} 返回非 JSON 响应")
                result = resp.json()
                if result.get("code") == 200 and result.get("data") is not None:
                    self._consecutive_failures = 0
                    return result["data"]
                code = result.get("code")
                raise RuntimeError(f"{api_name} 返回异常 code={code}")
            except Exception as exc:
                last_error = exc
                logging.error(f"{api_name} 失败 (尝试 {attempt}/{self.max_retries}): {exc}")
                if attempt < self.max_retries:
                    wait = min(3 * (2 ** (attempt - 1)), 30)
                    time.sleep(wait)
        self._consecutive_failures += 1
        logging.error(f"{api_name} 最终失败: params={params}, error={last_error}")
        return None

    def fetch_doc_by_alias(self, alias: str) -> Optional[dict]:
        alias = self._normalize_alias(alias)
        params = {"alias": alias, "pageNum": 1, "pageSize": 20, "website": "cn", "language": "zh", "channel": ""}
        return self._fetch_api_data(ALIYUN_DOC_API, params, api_name="文档详情 API")

    def search_docs(self, keywords: str, page_size: int = 20, page_num: int = 1) -> Optional[dict]:
        """使用搜索接口查找文档
        
        Args:
            keywords: 搜索关键词
            page_size: 每页数量
            page_num: 页码
            
        Returns:
            搜索结果数据，包含 documents 和 categories
        """
        params = {
            "keywords": keywords,
            "categoryId": 25365,  # 默认搜索所有分类
            "topics": "DOCUMENT,PRODUCT",
            "level": 3,
            "website": "cn",
            "language": "zh",
            "pageSize": page_size,
            "pageNum": page_num,
        }
        return self._fetch_api_data(ALIYUN_SEARCH_API, params, api_name="搜索 API")

    def extract_aliases_from_search(self, search_data: dict) -> List[str]:
        """从搜索结果中提取文档 alias 列表"""
        aliases = []
        documents = search_data.get("documents", {}).get("data", [])
        for doc in documents:
            url = doc.get("url", "")
            if url:
                alias = url_to_alias(url)
                # 过滤掉产品首页等无效路径（通常只有一级路径，如 /ecs）
                # 有效的文档路径至少包含两级，如 /ecs/user-guide/xxx
                if alias and alias.count('/') >= 2:
                    aliases.append(alias)
        return aliases

    def discover_product_docs(self, product_alias: str, strict: bool = False) -> List[str]:
        """使用搜索接口发现产品下所有文档

        Args:
            product_alias: 产品别名或关键词，如 /vpn 或 NAT网关
            strict: 失败时是否抛异常
        """
        all_aliases = []
        
        # 如果是路径格式（如 /nat），提取产品名
        search_keyword = product_alias.strip().strip("/").replace("-", " ")
        
        logging.info(f"使用搜索接口查找文档: {search_keyword}")
        
        # 搜索多页结果
        max_pages = 5  # 最多搜索5页
        for page in range(1, max_pages + 1):
            search_data = self.search_docs(search_keyword, page_size=20, page_num=page)
            if search_data is None:
                if strict and page == 1:
                    raise RuntimeError(f"搜索文档失败: {search_keyword}")
                break
                
            page_aliases = self.extract_aliases_from_search(search_data)
            if not page_aliases:
                break
                
            all_aliases.extend(page_aliases)
            logging.info(f"搜索第 {page} 页发现 {len(page_aliases)} 个文档")
            
            # 检查是否还有更多结果
            total = search_data.get("documents", {}).get("total", 0)
            if len(all_aliases) >= total:
                break
        
        logging.info(f"搜索共发现 {len(all_aliases)} 个文档 (关键词: {search_keyword})")
        return all_aliases

    def parse_api_response(self, data: dict, alias: str) -> Document:
        url = alias_to_url(alias)
        html_content = data.get("content", "")
        soup = BeautifulSoup(html_content, "lxml")
        
        text_content = "\n".join(
            line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()
        )
        title = data.get("title", "")
        if not title:
            h1 = soup.find("h1")
            title = h1.get_text(strip=True) if h1 else alias.split("/")[-1]
        last_modified = None
        last_modified_ms = data.get("lastModifiedTime")
        if last_modified_ms:
            last_modified = datetime.fromtimestamp(last_modified_ms / 1000)
        return Document(
            url=url,
            title=title,
            content=text_content,
            content_hash=compute_content_hash(text_content),
            last_modified=last_modified,
            crawled_at=datetime.now(),
            metadata={
                "desc": str(data.get("desc", "") or "").strip(),
                "node_id": data.get("nodeId"),
                "version": data.get("version"),
                "product_url": str(data.get("productUrl", "") or "").strip(),
                "developer_url": str(data.get("developerUrl", "") or "").strip(),
                "path": str(data.get("path", "") or "").strip(),
                "seo_title": str(data.get("seoTitle", "") or "").strip(),
            },
        )

    def crawl_page(self, url: str) -> Document:
        if url.startswith("http"):
            alias = url_to_alias(url)
        else:
            alias = url if url.startswith("/") else f"/{url}"
        logging.info(f"正在获取文档: {alias}")
        data = self.fetch_doc_by_alias(alias)
        if data is None:
            raise RuntimeError(f"无法获取文档: {alias}")
        return self.parse_api_response(data, alias)
