"""run_monitor skill - 批量巡检多云多产品文档"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..contracts.response import ErrorCode, SkillResponse
from ..detector import ChangeDetector
from ..models import Document, Notification
from ..utils import compute_content_hash
from .runtime import SkillRuntime

SUPPORTED_CLOUDS = {"aliyun", "tencent", "baidu", "volcano"}


class RunMonitorSkill:
    def __init__(self, runtime: SkillRuntime):
        self._rt = runtime
        self._detector = ChangeDetector()

    def run(
        self,
        clouds: List[str] = None,
        products: List[str] = None,
        mode: str = "check_now",
        max_pages: int = 50,
        days: int = 1,
        send_notification: bool = False,
    ) -> Dict[str, Any]:
        clouds = [c.lower() for c in (clouds or [])]
        products = products or []

        if not clouds:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "clouds 参数必填").to_dict()
        if not products:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "products 参数必填").to_dict()

        invalid = [c for c in clouds if c not in SUPPORTED_CLOUDS]
        if invalid:
            return SkillResponse.fail(ErrorCode.INVALID_PARAM, f"不支持的云厂商: {invalid}").to_dict()

        all_changes = []
        total_checked = 0
        errors = []

        for cloud in clouds:
            for product in products:
                try:
                    result = self._check_one(cloud, product, days, max_pages)
                    total_checked += result["checked"]
                    all_changes.extend(result["changes"])
                except Exception as e:
                    logging.error(f"巡检 {cloud}/{product} 失败: {e}")
                    errors.append({"cloud": cloud, "product": product, "error": str(e)})

        report_summary = self._build_report_summary(all_changes, total_checked, clouds, products)

        notification_result = {"attempted": False, "sent": False, "channel": None}
        if send_notification and (mode == "scheduled" or all_changes):
            try:
                notification = Notification(
                    title=f"云文档巡检日报 - 发现 {len(all_changes)} 处变化",
                    summary=report_summary,
                    changes=[],
                    timestamp=datetime.now(),
                    metadata={
                        "total_checked": total_checked,
                        "changes_count": len(all_changes),
                        "clouds": clouds,
                        "products": products,
                    },
                )
                results = self._rt.notifier.send_all(notification)
                notification_result["attempted"] = True
                notification_result["sent"] = any(results.values())
                notification_result["channel"] = list(results.keys())[0] if results else None
            except Exception as e:
                logging.error(f"发送通知失败: {e}")
                notification_result["attempted"] = True

        lines = [
            "# 云文档巡检日报",
            f"\n## 今日概览",
            f"- 检查 {total_checked} 篇文档",
            f"- 发现 {len(all_changes)} 处变化",
        ]
        if notification_result["sent"]:
            lines.append(f"- 已发送通知")
        if errors:
            lines.append(f"- {len(errors)} 个任务失败")
        if all_changes:
            lines.append("\n## 变更详情")
            for c in all_changes[:20]:
                lines.append(f"- [{c['cloud']}] {c['product']} - {c['title']}")
            if len(all_changes) > 20:
                lines.append(f"... 还有 {len(all_changes) - 20} 条变更")

        return SkillResponse.ok(
            machine={
                "mode": mode,
                "clouds": clouds,
                "products": products,
                "total_checked": total_checked,
                "changes": all_changes,
                "errors": errors,
                "notification": notification_result,
            },
            human={"summary_markdown": "\n".join(lines)},
        ).to_dict()

    def _check_one(self, cloud: str, product: str, days: int, max_pages: int) -> Dict[str, Any]:
        """从本地数据库读取已存储的文档，重新抓取对比变更"""
        stored_docs = self._rt.storage.search_local(keyword=product, cloud=cloud, limit=max_pages)
        crawler = self._rt.get_crawler(cloud)
        changes = []
        checked = 0

        for stored in stored_docs:
            try:
                fresh_doc = self._refetch_doc(cloud, crawler, stored.url)
                if fresh_doc is None:
                    continue

                checked += 1
                change = self._detector.detect(stored, fresh_doc)
                if change is None:
                    self._rt.storage.save(fresh_doc)
                    continue

                self._rt.storage.save(fresh_doc)
                changes.append({
                    "cloud": cloud,
                    "product": product,
                    "change_type": change.change_type.value,
                    "title": fresh_doc.title,
                    "url": fresh_doc.url,
                    "diff": change.diff,
                })
            except Exception as e:
                logging.warning(f"处理文档失败 {cloud}/{product}: {e}")

        return {"checked": checked, "changes": changes}

    def _refetch_doc(self, cloud: str, crawler, url: str) -> Optional[Document]:
        """根据 URL 重新抓取文档最新版本"""
        import re
        try:
            if cloud == "aliyun":
                return crawler.crawl_page(url)
            elif cloud == "tencent":
                match = re.search(r"/document/product/(\d+)/(\d+)", url)
                if not match:
                    return None
                raw = crawler.fetch_doc(match.group(2), match.group(1))
                return self._raw_to_doc(raw) if raw else None
            elif cloud == "baidu":
                match = re.search(r"/doc/([A-Za-z0-9_-]+)/s/([^/?#]+)", url)
                if not match:
                    return None
                raw = crawler.fetch_doc(match.group(1), match.group(2))
                return self._raw_to_doc(raw) if raw else None
            elif cloud == "volcano":
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

    @staticmethod
    def _build_report_summary(changes: List[Dict], total_checked: int,
                               clouds: List[str], products: List[str]) -> str:
        return (
            f"本次巡检覆盖 {', '.join(clouds)} 的 {', '.join(products)} 产品，"
            f"共检查 {total_checked} 篇文档，发现 {len(changes)} 处变更。"
        )
