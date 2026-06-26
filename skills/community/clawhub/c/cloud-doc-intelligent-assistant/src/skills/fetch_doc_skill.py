"""fetch_doc skill - 抓取指定云厂商的产品文档"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..contracts.response import ErrorCode, SkillResponse
from ..models import Document
from ..utils import compute_content_hash
from .runtime import SkillRuntime

SUPPORTED_CLOUDS = {"aliyun", "tencent", "baidu", "volcano"}


class FetchDocSkill:
    def __init__(self, runtime: SkillRuntime):
        self._rt = runtime

    def run(
        self,
        cloud: str,
        product: Optional[str] = None,
        doc_ref: Optional[str] = None,
        max_pages: int = 10,
        keyword: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not cloud:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "cloud 参数必填").to_dict()
        if cloud not in SUPPORTED_CLOUDS:
            return SkillResponse.fail(
                ErrorCode.INVALID_PARAM, f"不支持的云厂商: {cloud}，支持: {', '.join(SUPPORTED_CLOUDS)}"
            ).to_dict()
        if not product and not doc_ref:
            return SkillResponse.fail(
                ErrorCode.MISSING_PARAM, "product 和 doc_ref 至少填一个"
            ).to_dict()

        try:
            crawler = self._rt.get_crawler(cloud)
        except ValueError as e:
            return SkillResponse.fail(ErrorCode.INVALID_PARAM, str(e)).to_dict()

        if doc_ref:
            return self._fetch_single(cloud, crawler, doc_ref)

        return self._fetch_product(cloud, crawler, product, keyword, max_pages)

    def _fetch_single(self, cloud: str, crawler, doc_ref: str) -> Dict[str, Any]:
        try:
            if cloud == "aliyun":
                doc = crawler.crawl_page(doc_ref)
                items = [self._doc_to_item(doc)]
            elif cloud == "tencent":
                parts = doc_ref.split("/")
                if len(parts) == 2:
                    raw = crawler.fetch_doc(parts[1], parts[0])
                else:
                    raw = crawler.fetch_doc(doc_ref)
                if not raw:
                    return SkillResponse.fail(ErrorCode.CRAWL_FAILED, f"无法获取文档: {doc_ref}").to_dict()
                items = [self._raw_to_item(raw)]
            elif cloud == "baidu":
                parts = doc_ref.split("/", 1)
                if len(parts) != 2:
                    return SkillResponse.fail(ErrorCode.INVALID_PARAM, "百度云 doc_ref 格式: product/slug").to_dict()
                raw = crawler.fetch_doc(parts[0], parts[1])
                if not raw:
                    return SkillResponse.fail(ErrorCode.CRAWL_FAILED, f"无法获取文档: {doc_ref}").to_dict()
                items = [self._raw_to_item(raw)]
            elif cloud == "volcano":
                parts = doc_ref.split("/")
                if len(parts) != 2:
                    return SkillResponse.fail(ErrorCode.INVALID_PARAM, "火山云 doc_ref 格式: lib_id/doc_id").to_dict()
                raw = crawler.fetch_doc(parts[0], parts[1])
                if not raw:
                    return SkillResponse.fail(ErrorCode.CRAWL_FAILED, f"无法获取文档: {doc_ref}").to_dict()
                items = [self._raw_to_item(raw)]
            else:
                return SkillResponse.fail(ErrorCode.INVALID_PARAM, f"不支持的云厂商: {cloud}").to_dict()
        except Exception as e:
            logging.error(f"fetch_doc 单篇抓取失败: {e}")
            return SkillResponse.fail(ErrorCode.CRAWL_FAILED, f"抓取失败: {e}").to_dict()

        return SkillResponse.ok(
            machine={"cloud": cloud, "mode": "doc_ref", "items": items, "total": len(items)},
            human={"summary_text": f"成功抓取 1 篇文档。"},
        ).to_dict()

    def _fetch_product(self, cloud: str, crawler, product: str, keyword: Optional[str],
                       max_pages: int) -> Dict[str, Any]:
        """从本地数据库搜索已存储的文档"""
        search_term = keyword or product
        stored_docs = self._rt.storage.search_local(keyword=search_term, cloud=cloud, limit=max_pages)

        if not stored_docs:
            return SkillResponse.ok(
                machine={"cloud": cloud, "product": product, "mode": "local_search", "items": [], "total": 0},
                human={"summary_text": f"本地数据库中未找到与 {product} 相关的文档。请先通过 fetch_doc + doc_ref 抓取文档。"},
            ).to_dict()

        items = [self._doc_to_item(doc) for doc in stored_docs]

        return SkillResponse.ok(
            machine={"cloud": cloud, "product": product, "mode": "local_search", "items": items, "total": len(items)},
            human={"summary_text": f"从本地数据库找到 {len(items)} 篇与 {product} 相关的文档。"},
        ).to_dict()

    @staticmethod
    def _doc_to_item(doc: Document) -> Dict[str, Any]:
        return {
            "title": doc.title,
            "url": doc.url,
            "doc_ref": doc.url,
            "content": doc.content,
            "last_modified": doc.last_modified.isoformat() if doc.last_modified else None,
        }

    @staticmethod
    def _raw_to_item(raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "title": raw.get("title", ""),
            "url": raw.get("url", ""),
            "doc_ref": raw.get("url", ""),
            "content": raw.get("text", ""),
            "last_modified": raw.get("last_modified") or raw.get("date") or raw.get("recent_release_time"),
        }
