"""视觉检查的**结果**。计划说"该看什么"，这里记"看到了什么"。

之前只有计划没有结果——"已生成检查任务"被当成了"检查已通过"。
结果必须满足三条，缺一不可：

1. **绑定这一轮。** ``binding`` 是完整的五元身份：run_id、attempt_id、
   candidate_sha256、render_plan_sha256、renderer_build_id。只比候选哈希
   不够——同一份候选可以出自不同的渲染计划或不同版本的渲染器，
   那时旧结论对新链路并不成立。五个里差一个就是 ``EVIDENCE_STALE``。
2. **逐元素逐项。** 答案的唯一键是 ``(候选页, 元素 ID, 检查码)``。
   同一页上的两个表格都触发了同一个检查码时，那就是两条答案；
   只答一条不算把这一页看完。
3. **结论是算出来的。** ``decision`` 由条目推导，不接受手写。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from academic_pdf_translation.delivery.evidence import RunIdentity

SCHEMA_VERSION = "1.1"

DECISION_PASS = "PASS"
DECISION_FAIL = "FAIL"

VALID_DECISIONS = frozenset({DECISION_PASS, DECISION_FAIL})

#: 一条答案的唯一键：(候选页, 元素 ID, 检查码)。
AnswerKey = tuple[int, str, str]


class VisualResultError(RuntimeError):
    """结果文件不合法。"""


@dataclass
class ReviewItem:
    """一页上**一个元素**的一项检查的答案。

    没有 ``element_id`` 的答案没有意义：第 7 页有两个表格都触发了
    "线有没有错位"，只写一条 PASS 说明不了看的是哪一个。
    """

    candidate_page: int
    element_id: str
    check_code: str
    decision: str
    detail: str = ""

    @property
    def key(self) -> AnswerKey:
        return (self.candidate_page, self.element_id, self.check_code)

    def as_dict(self) -> dict[str, Any]:
        return {
            "candidate_page": self.candidate_page,
            "element_id": self.element_id,
            "check_code": self.check_code,
            "decision": self.decision,
            "detail": self.detail,
        }


@dataclass
class VisualReviewResult:
    """一次真正做过的视觉检查。"""

    schema_version: str = SCHEMA_VERSION
    #: 这次检查属于哪一轮。空绑定等于没有绑定，门槛会判 EVIDENCE_STALE。
    binding: RunIdentity | None = None
    reviewer_type: str = ""
    items: list[ReviewItem] = field(default_factory=list)

    @property
    def binding_dict(self) -> dict[str, Any]:
        return {} if self.binding is None else self.binding.as_dict()

    @property
    def run_id(self) -> str:
        return "" if self.binding is None else self.binding.run_id

    @property
    def attempt_id(self) -> int:
        return 0 if self.binding is None else self.binding.attempt_id

    @property
    def candidate_sha256(self) -> str:
        return "" if self.binding is None else self.binding.candidate_sha256

    @property
    def render_plan_sha256(self) -> str:
        return "" if self.binding is None else self.binding.render_plan_sha256

    @property
    def renderer_build_id(self) -> str:
        return "" if self.binding is None else self.binding.renderer_build_id

    @property
    def reviewed_pages(self) -> list[int]:
        return sorted({item.candidate_page for item in self.items})

    @property
    def answer_keys(self) -> set[AnswerKey]:
        return {item.key for item in self.items}

    @property
    def duplicate_keys(self) -> list[AnswerKey]:
        """同一个键答了两次。重复答案掩盖矛盾，一律拒绝。"""

        seen: set[AnswerKey] = set()
        duplicates: list[AnswerKey] = []
        for item in self.items:
            if item.key in seen:
                duplicates.append(item.key)
            seen.add(item.key)
        return duplicates

    @property
    def decision(self) -> str:
        """总结论由条目推导。没有条目就没有 PASS。"""

        if not self.items:
            return DECISION_FAIL
        if any(item.decision != DECISION_PASS for item in self.items):
            return DECISION_FAIL
        return DECISION_PASS

    @property
    def failed_items(self) -> list[ReviewItem]:
        return [
            item for item in self.items if item.decision != DECISION_PASS
        ]

    def answered(
        self, candidate_page: int, element_id: str, check_code: str
    ) -> bool:
        return (candidate_page, element_id, check_code) in self.answer_keys

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "binding": self.binding_dict,
            "reviewer_type": self.reviewer_type,
            "reviewed_pages": self.reviewed_pages,
            "decision": self.decision,
            "items": [item.as_dict() for item in self.items],
        }


def _binding_from_dict(data: dict[str, Any]) -> RunIdentity:
    """读绑定。旧格式把五元摊在顶层，这里一并兼容读入。

    读得进来不等于验得过：缺项会在视觉门被 ``verify_binding`` 判成
    ``EVIDENCE_STALE``，这里不替它补默认值。
    """

    raw = data.get("binding")
    source = raw if isinstance(raw, dict) else data
    try:
        attempt_id = int(source.get("attempt_id") or 0)
    except (TypeError, ValueError):
        raise VisualResultError(
            f"attempt_id 必须是整数，拿到 {source.get('attempt_id')!r}"
        ) from None
    return RunIdentity(
        run_id=str(source.get("run_id") or ""),
        attempt_id=attempt_id,
        candidate_sha256=str(source.get("candidate_sha256") or ""),
        render_plan_sha256=str(source.get("render_plan_sha256") or ""),
        renderer_build_id=str(source.get("renderer_build_id") or ""),
    )


def result_from_dict(data: dict[str, Any]) -> VisualReviewResult:
    """从 JSON 载入结果并校验形状。手写的 ``decision`` 字段一律忽略。"""

    if not isinstance(data, dict):
        raise VisualResultError("结果必须是对象")
    raw_items = data.get("items")
    if not isinstance(raw_items, list):
        raise VisualResultError("结果缺少 items 列表")
    items: list[ReviewItem] = []
    for index, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            raise VisualResultError(f"items[{index}] 不是对象")
        page = raw.get("candidate_page")
        element_id = raw.get("element_id")
        code = raw.get("check_code")
        decision = raw.get("decision")
        if not isinstance(page, int) or page < 1:
            raise VisualResultError(f"items[{index}] 的 candidate_page 非法")
        if not element_id or not isinstance(element_id, str):
            raise VisualResultError(
                f"items[{index}] 缺少 element_id，"
                "答案必须说清楚看的是哪一个元素"
            )
        if not code or not isinstance(code, str):
            raise VisualResultError(f"items[{index}] 缺少 check_code")
        if decision not in VALID_DECISIONS:
            raise VisualResultError(
                f"items[{index}] 的 decision 必须是 PASS 或 FAIL，"
                f"拿到 {decision!r}"
            )
        items.append(
            ReviewItem(
                candidate_page=page,
                element_id=element_id,
                check_code=code,
                decision=decision,
                detail=str(raw.get("detail") or ""),
            )
        )
    binding = _binding_from_dict(data)
    if not binding.candidate_sha256:
        raise VisualResultError(
            "结果没有 candidate_sha256，无法证明看的是哪一份候选"
        )
    return VisualReviewResult(
        schema_version=str(data.get("schema_version") or SCHEMA_VERSION),
        binding=binding,
        reviewer_type=str(data.get("reviewer_type") or ""),
        items=items,
    )
