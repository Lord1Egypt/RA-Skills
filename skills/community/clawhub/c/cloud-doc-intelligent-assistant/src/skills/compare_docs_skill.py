"""compare_docs skill - 获取两个云厂商的产品文档供客户端对比"""

import logging
import re
from typing import Any, Dict, Optional

from ..contracts.response import ErrorCode, SkillResponse
from .runtime import SkillRuntime

SUPPORTED_CLOUDS = {"aliyun", "tencent", "baidu", "volcano"}


class CompareDocsSkill:
    def __init__(self, runtime: SkillRuntime):
        self._rt = runtime

    def run(
        self,
        left: Dict[str, Any],
        right: Dict[str, Any],
        focus: Optional[str] = None,
    ) -> Dict[str, Any]:
        left_cloud = (left.get("cloud") or "").lower()
        right_cloud = (right.get("cloud") or "").lower()
        left_product = left.get("product") or left.get("doc_ref") or ""
        right_product = right.get("product") or right.get("doc_ref") or ""

        if not left_cloud or not right_cloud:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "left.cloud 和 right.cloud 必填").to_dict()
        if left_cloud not in SUPPORTED_CLOUDS or right_cloud not in SUPPORTED_CLOUDS:
            return SkillResponse.fail(ErrorCode.INVALID_PARAM, f"不支持的云厂商").to_dict()
        if not left_product or not right_product:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "left.product 和 right.product 必填").to_dict()

        try:
            left_content, left_title = self._fetch_content(left_cloud, left)
            right_content, right_title = self._fetch_content(right_cloud, right)
        except Exception as e:
            return SkillResponse.fail(ErrorCode.CRAWL_FAILED, f"文档获取失败: {e}").to_dict()

        if not left_content:
            return SkillResponse.fail(ErrorCode.CRAWL_FAILED, f"无法获取 {left_cloud} {left_product} 文档").to_dict()
        if not right_content:
            return SkillResponse.fail(ErrorCode.CRAWL_FAILED, f"无法获取 {right_cloud} {right_product} 文档").to_dict()

        return SkillResponse.ok(
            machine={
                "left": {"cloud": left_cloud, "product": left_product, "title": left_title, "content": left_content},
                "right": {"cloud": right_cloud, "product": right_product, "title": right_title, "content": right_content},
                "focus": focus or "",
            },
            human={"summary_text": f"已获取 {left_cloud}/{left_title} 和 {right_cloud}/{right_title} 的文档内容，请对比分析。"},
        ).to_dict()

    def _fetch_content(self, cloud: str, side: Dict[str, Any]) -> tuple:
        """获取文档内容，优先 doc_ref 直接抓取，否则从本地数据库查"""
        doc_ref = side.get("doc_ref", "")
        product = side.get("product", "")
        keyword = side.get("keyword", "")
        crawler = self._rt.get_crawler(cloud)

        if doc_ref:
            return self._fetch_by_ref(cloud, crawler, doc_ref)

        return self._fetch_by_product(cloud, product, keyword)

    def _fetch_by_ref(self, cloud: str, crawler, doc_ref: str) -> tuple:
        if cloud == "aliyun":
            doc = crawler.crawl_page(doc_ref)
            return doc.content, doc.title
        elif cloud == "tencent":
            parts = doc_ref.split("/")
            raw = crawler.fetch_doc(parts[-1], parts[0] if len(parts) > 1 else "")
            return (raw or {}).get("text", ""), (raw or {}).get("title", "")
        elif cloud == "baidu":
            parts = doc_ref.split("/", 1)
            raw = crawler.fetch_doc(parts[0], parts[1]) if len(parts) == 2 else None
            return (raw or {}).get("text", ""), (raw or {}).get("title", "")
        elif cloud == "volcano":
            parts = doc_ref.split("/")
            raw = crawler.fetch_doc(parts[0], parts[1]) if len(parts) == 2 else None
            return (raw or {}).get("text", ""), (raw or {}).get("title", "")
        return "", ""

    def _fetch_by_product(self, cloud: str, product: str, keyword: str = "") -> tuple:
        """从本地数据库搜索已存储的文档"""
        search_term = keyword or product
        stored_docs = self._rt.storage.search_local(keyword=search_term, cloud=cloud, limit=10)

        if not stored_docs:
            return "", ""

        if keyword:
            for doc in stored_docs:
                if keyword.lower() in doc.title.lower():
                    return doc.content, doc.title

        return stored_docs[0].content, stored_docs[0].title
