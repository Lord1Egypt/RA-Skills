"""腾讯云文档爬虫模块"""

import logging
import re
import time
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


TENCENT_DOC_DETAIL_API = "https://cloud.tencent.com/document/cgi/document/getDocPageDetail"
TENCENT_DOC_URL_TEMPLATE = "https://cloud.tencent.com/document/product/{product_id}/{doc_id}"
TENCENT_SEARCH_API_V2 = "https://cloud.tencent.com/portal/search/api/result/startup"


class TencentDocCrawler:
    """腾讯云文档爬虫 - 基于搜索 API + 文档详情 API"""

    def __init__(self, request_delay: float = 0.5, timeout: int = 30):
        self.request_delay = request_delay
        self.timeout = timeout
        self.session = requests.Session()
        self.last_request_time = 0.0

    def _rate_limit(self) -> None:
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_request_time = time.time()

    @staticmethod
    def _normalize_digits(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, int):
            return str(value)
        text = str(value).strip()
        if not text:
            return ""
        if text.isdigit():
            return text
        match = re.search(r"(\d+)", text)
        return match.group(1) if match else ""

    def _normalize_url(self, url: str) -> str:
        if not url:
            return ""
        clean = url.strip()
        if clean.startswith("//"):
            return f"https:{clean}"
        if clean.startswith("/"):
            return f"https://cloud.tencent.com{clean}"
        return clean

    def _search_docs_by_keyword(self, search_query: str, product_name: str = "", limit: int = 0) -> List[Dict[str, str]]:
        docs: List[Dict[str, str]] = []
        seen: set = set()
        page = 1
        max_pages = 100

        while page <= max_pages:
            self._rate_limit()
            filter_config = {}
            if product_name:
                filter_config["productName"] = product_name
            payload = {
                "action": "startup",
                "payload": {
                    "type": 7,
                    "keyword": search_query,
                    "page": page,
                    "preferSynonym": True,
                    "filter": filter_config,
                    "sort": None,
                },
            }
            try:
                encoded_name = quote(search_query, safe="")
                response = self.session.post(
                    TENCENT_SEARCH_API_V2,
                    json=payload,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                result = response.json()
            except Exception as e:
                logging.error(f"搜索腾讯云文档失败 (page={page}): {e}")
                break

            data = result.get("data", {})
            doc_list = data.get("list", [])
            total_pages = data.get("totalPage", 1)
            if not doc_list:
                break

            for doc in doc_list:
                url = doc.get("url", "")
                match = re.search(r"/document/product/(\d+)/(\d+)", url)
                if not match:
                    continue
                pid = match.group(1)
                doc_id = match.group(2)
                key = (pid, doc_id)
                if key in seen:
                    continue
                seen.add(key)
                docs.append({
                    "product_id": pid,
                    "doc_id": doc_id,
                    "title": doc.get("title", f"doc-{doc_id}"),
                    "url": url,
                    "category": doc.get("productName", ""),
                    "recent_release_time": (
                        doc.get("recentReleaseTime") or doc.get("releaseTime")
                        or doc.get("updateTime") or doc.get("publishTime") or ""
                    ),
                })
                if limit > 0 and len(docs) >= limit:
                    return docs

            if page >= total_pages:
                break
            page += 1

        return docs

    def discover_product_docs(self, product_name: str, keyword: str = "", limit: int = 0) -> List[Dict[str, str]]:
        normalized_product_name = product_name.strip()
        search_query = keyword.strip() or normalized_product_name
        if not normalized_product_name:
            return []
        logging.info(f"[腾讯云] 搜索「{search_query}」，产品过滤={normalized_product_name}")
        docs = self._search_docs_by_keyword(search_query, normalized_product_name, limit)
        logging.info(f"发现腾讯云产品 {normalized_product_name} 文档 {len(docs)} 篇")
        return docs

    def _deep_find_string(self, obj: Any, keys: List[str]) -> str:
        if isinstance(obj, dict):
            for key in keys:
                value = obj.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()
            for value in obj.values():
                found = self._deep_find_string(value, keys)
                if found:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = self._deep_find_string(item, keys)
                if found:
                    return found
        return ""

    def _deep_collect_strings(self, obj: Any, out: List[str]) -> None:
        if isinstance(obj, str):
            text = obj.strip()
            if len(text) >= 80:
                out.append(text)
            return
        if isinstance(obj, dict):
            for value in obj.values():
                self._deep_collect_strings(value, out)
            return
        if isinstance(obj, list):
            for item in obj:
                self._deep_collect_strings(item, out)

    def fetch_doc(self, doc_id: str, product_id: str = "", lang: str = "zh") -> Optional[Dict[str, str]]:
        normalized_doc_id = self._normalize_digits(doc_id)
        normalized_product_id = self._normalize_digits(product_id)
        if not normalized_doc_id:
            logging.error(f"无效的腾讯云 doc_id: {doc_id}")
            return None

        self._rate_limit()
        referer = "https://cloud.tencent.com/"
        if normalized_product_id:
            referer = TENCENT_DOC_URL_TEMPLATE.format(
                product_id=normalized_product_id, doc_id=normalized_doc_id
            )

        payload = {
            "action": "getDocPageDetail",
            "payload": {"id": normalized_doc_id, "lang": lang, "isPreview": False, "isFromClient": True},
        }

        try:
            response = self.session.post(
                TENCENT_DOC_DETAIL_API,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            logging.error(f"获取腾讯云文档失败 doc_id={normalized_doc_id}: {e}")
            return None

        if isinstance(result, dict):
            data = result.get("data") or result.get("result") or result
        else:
            logging.error(f"腾讯云文档 API 返回非 JSON 对象: doc_id={normalized_doc_id}")
            return None

        title = self._deep_find_string(data, ["title", "name", "docTitle", "pageTitle"])
        html_content = self._deep_find_string(data, ["content", "html", "docContent", "body"])
        if not html_content:
            candidates: List[str] = []
            self._deep_collect_strings(data, candidates)
            if candidates:
                html_content = max(candidates, key=len)

        if not html_content:
            logging.error(f"腾讯云文档内容为空: doc_id={normalized_doc_id}")
            return None

        if "<" in html_content and ">" in html_content:
            soup = BeautifulSoup(html_content, "lxml")
            text = soup.get_text(separator="\n", strip=True)
            html = html_content
        else:
            text = html_content
            html = ""

        url = self._normalize_url(self._deep_find_string(data, ["url", "link", "docUrl"]))
        url_match = re.search(r"/document/product/(\d+)/(\d+)", url)
        if url_match:
            normalized_product_id = normalized_product_id or url_match.group(1)
            normalized_doc_id = normalized_doc_id or url_match.group(2)

        if not normalized_product_id:
            normalized_product_id = self._normalize_digits(
                self._deep_find_string(data, ["productId", "product_id", "pid"])
            )

        if not url:
            if normalized_product_id:
                url = TENCENT_DOC_URL_TEMPLATE.format(
                    product_id=normalized_product_id, doc_id=normalized_doc_id
                )
            else:
                url = f"https://cloud.tencent.com/document/{normalized_doc_id}"

        recent_release_time = self._deep_find_string(data, ["recentReleaseTime", "releaseTime"])
        last_modified = recent_release_time or self._deep_find_string(
            data, ["lastModified", "lastModifiedTime", "updateTime", "updatedAt", "publishTime"]
        )

        return {
            "title": title or f"doc-{normalized_doc_id}",
            "text": text,
            "html": html,
            "url": url,
            "doc_id": normalized_doc_id,
            "product_id": normalized_product_id,
            "recent_release_time": recent_release_time,
            "last_modified": last_modified,
        }
