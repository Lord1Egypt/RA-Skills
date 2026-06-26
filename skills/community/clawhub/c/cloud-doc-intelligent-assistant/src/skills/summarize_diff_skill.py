"""summarize_diff skill - 对新旧文档内容进行 diff"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from ..contracts.response import ErrorCode, SkillResponse
from ..detector import ChangeDetector
from ..models import Document
from ..utils import compute_content_hash
from .runtime import SkillRuntime


class SummarizeDiffSkill:
    def __init__(self, runtime: SkillRuntime):
        self._rt = runtime
        self._detector = ChangeDetector()

    def run(
        self,
        title: str,
        old_content: str,
        new_content: str,
        focus: Optional[str] = None,
        url: str = "",
    ) -> Dict[str, Any]:
        if not title:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "title 参数必填").to_dict()
        if old_content is None or new_content is None:
            return SkillResponse.fail(ErrorCode.MISSING_PARAM, "old_content 和 new_content 必填").to_dict()

        old_hash = compute_content_hash(old_content)
        new_hash = compute_content_hash(new_content)

        if old_hash == new_hash:
            return SkillResponse.ok(
                machine={
                    "title": title,
                    "change_type": "unchanged",
                    "focus": focus,
                    "diff": "",
                    "old_hash": old_hash,
                    "new_hash": new_hash,
                },
                human={"summary_text": "文档内容无变化。"},
            ).to_dict()

        old_doc = Document(
            url=url or "temp://old", title=title, content=old_content,
            content_hash=old_hash, last_modified=None, crawled_at=datetime.now(), metadata={},
        )
        new_doc = Document(
            url=url or "temp://new", title=title, content=new_content,
            content_hash=new_hash, last_modified=None, crawled_at=datetime.now(), metadata={},
        )

        change = self._detector.detect(old_doc, new_doc)
        if change is None:
            change_type = "modified"
            diff_text = f"旧内容长度: {len(old_content)}, 新内容长度: {len(new_content)}"
        else:
            change_type = change.change_type.value
            diff_text = change.diff

        return SkillResponse.ok(
            machine={
                "title": title,
                "change_type": change_type,
                "focus": focus,
                "diff": diff_text,
                "old_hash": old_hash,
                "new_hash": new_hash,
            },
            human={"summary_text": f"文档《{title}》发生了 {change_type} 级别的变更，请根据 diff 内容进行分析。"},
        ).to_dict()
