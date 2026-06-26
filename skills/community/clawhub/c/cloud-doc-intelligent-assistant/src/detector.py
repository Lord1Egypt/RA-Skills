"""变更检测模块"""

import difflib
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set

from .models import ChangeReport, ChangeType, Document, DocumentChange


class ChangeDetector:
    NOISE_PATTERNS = ["copyright", "©", "all rights reserved", "last updated", "最后更新", "版权所有"]

    def detect_changes(self, old_docs: List[Document], new_docs: List[Document]) -> ChangeReport:
        old_map: Dict[str, Document] = {doc.url: doc for doc in old_docs}
        new_map: Dict[str, Document] = {doc.url: doc for doc in new_docs}
        old_urls: Set[str] = set(old_map.keys())
        new_urls: Set[str] = set(new_map.keys())

        added = [new_map[url] for url in (new_urls - old_urls)]
        deleted = [old_map[url] for url in (old_urls - new_urls)]
        modified: List[DocumentChange] = []

        for url in old_urls & new_urls:
            old_doc = old_map[url]
            new_doc = new_map[url]
            if new_doc.last_modified and old_doc.last_modified:
                has_changed = new_doc.last_modified > old_doc.last_modified
            else:
                has_changed = old_doc.content_hash != new_doc.content_hash

            if has_changed:
                diff = self.compute_diff(old_doc.content, new_doc.content)
                if not self._is_noise_change(diff):
                    modified.append(DocumentChange(
                        document=new_doc,
                        old_content_hash=old_doc.content_hash,
                        new_content_hash=new_doc.content_hash,
                        diff=diff,
                        change_type=self.categorize_change(diff),
                    ))

        report = ChangeReport(added=added, modified=modified, deleted=deleted, timestamp=datetime.now())
        logging.info(f"变更检测完成: 新增 {len(added)}, 修改 {len(modified)}, 删除 {len(deleted)}")
        return report

    def compute_diff(self, old_content: str, new_content: str) -> str:
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        diff = difflib.unified_diff(old_lines, new_lines, fromfile="旧版本", tofile="新版本", lineterm="")
        return "\n".join(diff)

    def categorize_change(self, diff: str) -> ChangeType:
        lines = diff.split("\n")
        added_lines = sum(1 for l in lines if l.startswith("+") and not l.startswith("+++"))
        removed_lines = sum(1 for l in lines if l.startswith("-") and not l.startswith("---"))
        total_changes = added_lines + removed_lines
        structural_markers = ["# ", "## ", "### ", "#### "]
        has_structural_change = any(
            any(line.lstrip("+-").startswith(m) for m in structural_markers)
            for line in lines
            if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))
        )
        if has_structural_change:
            return ChangeType.STRUCTURAL
        elif total_changes >= 10:
            return ChangeType.MAJOR
        return ChangeType.MINOR

    def detect(self, old_doc: Document, new_doc: Document) -> "Optional[DocumentChange]":
        """对比两个单篇文档，返回 DocumentChange 或 None（无变更）"""
        if old_doc.content_hash == new_doc.content_hash:
            return None
        diff = self.compute_diff(old_doc.content, new_doc.content)
        if self._is_noise_change(diff):
            return None
        return DocumentChange(
            document=new_doc,
            old_content_hash=old_doc.content_hash,
            new_content_hash=new_doc.content_hash,
            diff=diff,
            change_type=self.categorize_change(diff),
        )

    def _is_noise_change(self, diff: str) -> bool:
        lines = diff.split("\n")
        changed_lines = [
            l for l in lines
            if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))
        ]
        if not changed_lines:
            return True
        noise_count = sum(
            1 for l in changed_lines
            if any(p in l.lower() for p in self.NOISE_PATTERNS)
        )
        return noise_count == len(changed_lines)
