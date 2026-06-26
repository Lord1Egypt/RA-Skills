"""check_changes skill - 检测文档变更"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from ..contracts.response import ErrorCode, SkillResponse
from ..detector import ChangeDetector
from ..models import Document
from ..utils import compute_content_hash
from .runtime import SkillRuntime

SUPPORTED_CLOUDS = {"aliyun", "tencent", "baidu", "volcano"}


class CheckChangesSkill:
    def __init__(self, runtime: SkillRuntime):
        self._rt = runtime
        self._detector = ChangeDetector()

    def run(
        self,
        cloud: str,
        product: str,
        keyword: Optional[str] = None,
        days: int = 7,
        max_pages: int = 200,
    ) -> Dict[str, Any]:
        if not cloud:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "cloud 参数必填").to_dict()
        if cloud not in SUPPORTED_CLOUDS:
            return SkillResponse.fail(ErrorCode.INVALID_PARAM, f"不支持的云厂商: {cloud}").to_dict()
        if not product:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "product 参数必填").to_dict()

        # 从本地数据库搜索已存储的文档，不再调用搜索接口
        search_term = keyword or product
        stored_docs = self._rt.storage.search_local(keyword=search_term, cloud=cloud, limit=max_pages)

        if not stored_docs:
            return SkillResponse.ok(
                machine={"cloud": cloud, "product": product, "changes": [], "total_checked": 0},
                human={"summary_markdown": f"本地数据库中未找到 {cloud} {product} 相关文档。请先通过 fetch_doc + doc_ref 抓取文档建立基线。"},
            ).to_dict()

        # 重新抓取每篇文档的最新版本，与数据库中的版本对比
        crawler = self._rt.get_crawler(cloud)
        changes = []
        checked = 0
        errors = []
        cutoff = datetime.now() - timedelta(days=days)

        for stored in stored_docs:
            try:
                fresh_doc = self._refetch_doc(cloud, crawler, stored.url)
                if fresh_doc is None:
                    errors.append(stored.url)
                    continue
                checked += 1

                change = self._detector.detect(stored, fresh_doc)
                if change is None:
                    # 无变更，更新存储时间
                    self._rt.storage.save(fresh_doc)
                    continue

                # 有变更，保存新版本
                self._rt.storage.save(fresh_doc)

                change_item: Dict[str, Any] = {
                    "change_type": change.change_type.value,
                    "title": fresh_doc.title,
                    "url": fresh_doc.url,
                    "doc_ref": fresh_doc.url,
                    "old_hash": stored.content_hash,
                    "new_hash": fresh_doc.content_hash,
                    "diff": change.diff,
                }
                changes.append(change_item)
            except Exception as e:
                logging.warning(f"检查文档变更失败 {stored.url}: {e}")
                errors.append(stored.url)

        # 构建 human 摘要
        if not changes:
            human_text = f"检查了 {checked} 篇文档，最近 {days} 天内无变更。"
        else:
            lines = [f"# 最近 {days} 天变更摘要\n"]
            for c in changes:
                summary = c.get("summary", "")
                lines.append(f"- [{c['change_type']}] {c['title']}: {summary}")
            human_text = "\n".join(lines)

        if errors:
            human_text += f"\n\n⚠️ {len(errors)} 篇文档重新抓取失败。"

        return SkillResponse.ok(
            machine={
                "cloud": cloud,
                "product": product,
                "days": days,
                "total_checked": checked,
                "changes": changes,
                "fetch_errors": len(errors),
            },
            human={"summary_markdown": human_text},
        ).to_dict()

    def _refetch_doc(self, cloud: str, crawler, url: str) -> Optional[Document]:
        """根据 URL 重新抓取文档最新版本"""
        try:
            if cloud == "aliyun":
                return crawler.crawl_page(url)
            elif cloud == "tencent":
                # 从 URL 提取 product_id 和 doc_id
                import re
                match = re.search(r"/document/product/(\d+)/(\d+)", url)
                if not match:
                    return None
                raw = crawler.fetch_doc(match.group(2), match.group(1))
                return self._raw_to_doc(raw) if raw else None
            elif cloud == "baidu":
                import re
                match = re.search(r"/doc/([A-Za-z0-9_-]+)/s/([^/?#]+)", url)
                if not match:
                    return None
                raw = crawler.fetch_doc(match.group(1), match.group(2))
                return self._raw_to_doc(raw) if raw else None
            elif cloud == "volcano":
                import re
                match = re.search(r"/docs/(\d+)/(\d+)", url)
                if not match:
                    return None
                raw = crawler.fetch_doc(match.group(1), match.group(2))
                return self._raw_to_doc(raw) if raw else None
        except Exception as e:
            logging.error(f"重新抓取文档失败 {url}: {e}")
        return None

    @staticmethod
    def _raw_to_doc(raw: Dict[str, Any]) -> Document:
        content = raw.get("text", "")
        return Document(
            url=raw.get("url", ""),
            title=raw.get("title", ""),
            content=content,
            content_hash=compute_content_hash(content),
            last_modified=None,
            crawled_at=datetime.now(),
            metadata={"image_urls": raw.get("image_urls", [])},
        )
