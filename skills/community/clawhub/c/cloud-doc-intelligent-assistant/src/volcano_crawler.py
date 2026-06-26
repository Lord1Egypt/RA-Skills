"""火山云文档爬虫模块"""

import json
import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import quote

import requests


VOLCANO_KNOWN_LIBS = {
    "6401": "私有网络",
    "6405": "云企业网",
    "6454": "内容分发网络",
    "6404": "NAT网关",
    "6427": "飞连",
    "6638": "证书中心",
    "6737": "全球加速",
    "6752": "WebRTC 传输网络",
}

VOLCANO_SEARCH_ALL_API = "https://www.volcengine.com/api/search/searchAll"


class VolcanoDocCrawler:
    """火山云文档爬虫 - 基于 searchAll + getDocDetail"""

    def __init__(self, request_delay: float = 0.3, timeout: int = 30):
        self.request_delay = request_delay
        self.timeout = timeout
        self.session = requests.Session()
        # 火山云 API 需要特定的请求头才能访问
        self.session.headers.update({
            "accept": "application/json",
            "referer": "https://www.volcengine.com/docs",
            "x-use-bff-version": "1",
        })
        self.last_request_time = 0.0
        self._lib_id_cache: Dict[str, str] = {}

    @staticmethod
    def _pick_first_str(node: Dict[str, Any], keys: List[str]) -> str:
        for key in keys:
            value = node.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    @staticmethod
    def _normalize_doc_url(url: str) -> str:
        text = (url or "").strip()
        if not text:
            return ""
        if text.startswith("//"):
            return f"https:{text}"
        if text.startswith("/"):
            return f"https://www.volcengine.com{text}"
        return text

    @staticmethod
    def _extract_doc_ids(url: str) -> Tuple[str, str]:
        match = re.search(r"/docs/(\d+)/(\d+)", (url or "").strip())
        if not match:
            return "", ""
        return match.group(1), match.group(2)

    @staticmethod
    def _extract_image_urls_from_markdown(markdown_text: str) -> List[str]:
        if not markdown_text:
            return []
        seen: set = set()
        image_urls: List[str] = []
        for url in re.findall(r"!\[[^\]]*\]\((https?://[^)\s]+)", markdown_text):
            clean = url.strip()
            if clean and clean not in seen:
                seen.add(clean)
                image_urls.append(clean)
        return image_urls

    def _to_doc_entry(self, node: Dict[str, Any]) -> Optional[Dict[str, str]]:
        url = self._normalize_doc_url(
            self._pick_first_str(node, ["Url", "URL", "url", "DocURL", "DocUrl", "Link", "link"])
        )
        lib_id, doc_id = self._extract_doc_ids(url)
        if not lib_id or not doc_id:
            return None
        title = self._pick_first_str(node, ["Name", "name", "Title", "title", "DocName", "docName"])
        return {
            "doc_id": doc_id,
            "lib_id": lib_id,
            "name": title or f"doc-{doc_id}",
            "url": url,
            "update_time": self._pick_first_str(node, ["UpdateTime", "updateTime", "RecentReleaseTime"]),
            "search_label": self._pick_first_str(node, ["SearchLabel", "searchLabel"]),
        }

    def _extract_doc_entries_from_search_payload(self, data: Any) -> List[Dict[str, str]]:
        candidates: List[Any] = []
        result = data.get("Result", {})
        list_items = result.get("List", [])
        for item in list_items:
            if isinstance(item, dict) and "DocList" in item:
                doc_list = item.get("DocList", [])
                if isinstance(doc_list, list):
                    candidates.extend(doc_list)

        if not candidates:
            known_paths = [
                ("Result", "List"),
                ("Result", "DocList"),
                ("Data", "List"),
                ("data", "list"),
            ]
            for path in known_paths:
                cur = data
                ok = True
                for key in path:
                    if isinstance(cur, dict) and key in cur:
                        cur = cur[key]
                    else:
                        ok = False
                        break
                if ok and isinstance(cur, list):
                    candidates.extend(cur)
                    break

        docs: List[Dict[str, str]] = []
        seen = set()
        for item in candidates:
            if not isinstance(item, dict):
                continue
            doc = self._to_doc_entry(item)
            if not doc:
                continue
            key = (doc["lib_id"], doc["doc_id"])
            if key in seen:
                continue
            seen.add(key)
            docs.append(doc)
        return docs

    def _rate_limit(self) -> None:
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_delay:
            time.sleep(self.request_delay - elapsed)
        self.last_request_time = time.time()

    def _find_lib_id_by_name(self, product_name: str) -> Optional[Tuple[str, str]]:
        if product_name in self._lib_id_cache:
            lib_id = self._lib_id_cache[product_name]
            return (lib_id, product_name)
        for lib_id, name in VOLCANO_KNOWN_LIBS.items():
            if product_name in name or name in product_name:
                self._lib_id_cache[product_name] = lib_id
                return (lib_id, name)
        docs = self.search_docs(product_name, limit=20)
        if docs:
            first_doc = docs[0]
            lib_id = first_doc["lib_id"]
            self._lib_id_cache[product_name] = lib_id
            logging.info(f"通过 searchAll 找到产品 '{product_name}' -> LibID: {lib_id}")
            return (lib_id, product_name)
        logging.warning(f"未找到产品 '{product_name}' 对应的 LibID")
        return None

    def resolve_lib_id(self, product_name: str) -> str:
        result = self._find_lib_id_by_name(product_name)
        if not result:
            return ""
        return result[0]

    def search_docs(self, query: str, limit: int = 20, offset: int = 0, lib_id: str = "") -> List[Dict[str, str]]:
        query_text = (query or "").strip()
        if not query_text:
            return []

        PAGE_SIZE = 50
        all_docs = []
        current_offset = offset
        need_pagination = limit == 0 or limit > PAGE_SIZE

        while True:
            self._rate_limit()
            # 移除可能包含用户标识的参数，只保留必要的查询参数
            params = {
                "Query": query_text,
                "Offset": current_offset,
                "Limit": PAGE_SIZE,
                "Type": "all",
            }
            try:
                resp = self.session.get(
                    VOLCANO_SEARCH_ALL_API, params=params, timeout=self.timeout
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                logging.error(f"searchAll 查询失败(query={query_text}, offset={current_offset}): {e}")
                break

            page_docs = self._extract_doc_entries_from_search_payload(data)
            if not page_docs:
                break
            all_docs.extend(page_docs)

            if not need_pagination:
                break
            if limit > 0 and len(all_docs) >= limit:
                break
            if len(page_docs) < PAGE_SIZE:
                break
            current_offset += PAGE_SIZE
            logging.info(f"[火山云] 分页获取下一页 (offset={current_offset})")

        if lib_id:
            all_docs = [doc for doc in all_docs if doc.get("lib_id") == str(lib_id)]

        seen = set()
        unique_docs = []
        for doc in all_docs:
            key = (doc.get("lib_id"), doc.get("doc_id"))
            if key not in seen:
                seen.add(key)
                unique_docs.append(doc)

        logging.info(f"[火山云] searchAll(query={query_text}, lib_id={lib_id or '-'}) 共返回 {len(unique_docs)} 篇文档")
        return unique_docs[:limit] if limit > 0 else unique_docs

    def discover_product_docs(self, product_name: str, limit: int = 0) -> List[Dict[str, str]]:
        """发现产品文档
        
        Args:
            product_name: 产品名称或功能关键词（如 私有网络、安全组）
            limit: 返回文档数量限制，0 表示不限制
            
        Returns:
            文档列表，每个文档包含 lib_id、doc_id、name、url 等字段
            
        Note:
            - 如果 product_name 是具体产品名（如 私有网络），会过滤只返回该产品的文档
            - 如果 product_name 是功能关键词（如 安全组），会返回所有相关产品的文档
        """
        result = self._find_lib_id_by_name(product_name)
        if result:
            lib_id, actual_name = result
            search_query = actual_name or product_name
            logging.info(f"[火山云] searchAll 搜索「{search_query}」，LibID={lib_id}")
            docs = self.search_docs(query=search_query, limit=limit, lib_id=lib_id)
            logging.info(f"发现火山云产品 {lib_id} 文档 {len(docs)} 篇")
            if docs:
                return docs
        
        # 如果没找到结果，可能是功能关键词而非产品名，尝试不过滤 lib_id
        logging.info(f"未找到产品 {product_name} 的文档，尝试作为功能关键词搜索")
        docs = self.search_docs(query=product_name, limit=limit, lib_id="")
        logging.info(f"发现火山云 {product_name} 相关文档 {len(docs)} 篇")
        return docs

    def fetch_doc(self, lib_id: str, doc_id: str) -> Optional[Dict]:
        self._rate_limit()
        api_url = "https://www.volcengine.com/api/doc/getDocDetail"
        params = {"LibraryID": lib_id, "DocumentID": doc_id, "type": "online"}

        try:
            resp = self.session.get(api_url, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            result = data.get("Result", {})
            if not result:
                logging.warning(f"火山云文档 {lib_id}/{doc_id} API 返回空")
                return None

            title = result.get("Title", "")
            text = result.get("MDContent", "")
            if not text:
                content_json = result.get("Content", "")
                if content_json:
                    text = self._extract_text_from_content(content_json)

            if not text:
                logging.warning(f"火山云文档 {lib_id}/{doc_id} 内容为空")
                return None

            doc_url = f"https://www.volcengine.com/docs/{lib_id}/{doc_id}"
            updated_time = str(result.get("UpdatedTime", "") or "")
            first_published_time = str(result.get("FirstPublishedTime", "") or "")
            image_urls = self._extract_image_urls_from_markdown(text)
            return {
                "title": title or f"doc-{doc_id}",
                "text": text,
                "html": "",
                "url": doc_url,
                "lib_id": lib_id,
                "doc_id": doc_id,
                "last_modified": updated_time,
                "first_published_time": first_published_time,
                "image_urls": image_urls,
                "keywords": str(result.get("Keywords", "") or ""),
                "language": str(result.get("Language", "") or ""),
            }
        except Exception as e:
            logging.error(f"获取火山云文档失败 {lib_id}/{doc_id}: {e}")
            return None

    def _extract_text_from_content(self, content_json: str) -> str:
        """从 Content 字段提取文本
        
        Content 字段可能是：
        1. JSON 格式的富文本（私有网络等产品）
        2. 纯 HTML/Markdown 文本（边缘计算节点等产品）
        """
        if not content_json:
            return ""
            
        # 尝试作为 JSON 解析
        try:
            data = json.loads(content_json)
            texts = []
            data_obj = data.get("data", {})
            for key in sorted(data_obj.keys(), key=lambda x: int(x) if x.isdigit() else 0):
                value = data_obj[key]
                if isinstance(value, dict) and "ops" in value:
                    for op in value["ops"]:
                        insert = op.get("insert", "")
                        if isinstance(insert, str) and insert and insert != "*":
                            texts.append(insert)
            result = "".join(texts)
            if result:
                return result
        except (json.JSONDecodeError, Exception) as e:
            logging.debug(f"Content 不是 JSON 格式，尝试作为纯文本处理: {e}")
        
        # 如果不是 JSON 或解析失败，直接返回原文本（可能是 HTML/Markdown）
        return content_json.strip()
