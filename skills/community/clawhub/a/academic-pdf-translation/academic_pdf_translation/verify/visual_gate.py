"""视觉门槛：计划和结果对得上，才算看过。

纯函数。输入是计划、结果和当前这一轮的身份，输出一个判定，不写文件。

对账的唯一键是 ``(候选页, 元素 ID, 检查码)``。按"页 → 检查码"折叠会漏：
第 7 页有 table-001 和 table-002 两个表格都触发同一个检查码时，
折叠后一条答案就把两个表格都算看过了，其中一个可能根本没人看。

判定码：

- ``NOT_REQUIRED``：没有风险页，不需要看，门放行。
- ``WAITING_FOR_VISUAL_REVIEW``：有风险页但还没有结果，禁止交付。
- ``STALE``：结果的五元绑定与当前这一轮对不上，等于没看，禁止交付。
- ``UNKNOWN_ELEMENT``：结果里出现计划中不存在的元素，禁止交付。
- ``DUPLICATE_ANSWER``：同一个键答了两次，禁止交付。
- ``INCOMPLETE``：该看的元素或该答的问题没答全，禁止交付。
- ``TRUNCATED``：计划本身被预算截断，有高风险页没进清单，禁止直接通过。
- ``FAIL``：看了，发现问题。带出失败条目供返修/人工。
- ``PASS``：每页每个元素每项都有答案且全部通过。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from academic_pdf_translation.delivery.evidence import (
    RunIdentity,
    verify_binding,
)
from academic_pdf_translation.verify.visual_plan import VisualReviewPlan
from academic_pdf_translation.verify.visual_result import (
    DECISION_PASS,
    AnswerKey,
    ReviewItem,
    VisualReviewResult,
)

VISUAL_PASS = "PASS"
VISUAL_NOT_REQUIRED = "NOT_REQUIRED"
VISUAL_WAITING = "WAITING_FOR_VISUAL_REVIEW"
VISUAL_STALE = "STALE"
VISUAL_UNKNOWN_ELEMENT = "UNKNOWN_ELEMENT"
VISUAL_DUPLICATE_ANSWER = "DUPLICATE_ANSWER"
VISUAL_INCOMPLETE = "INCOMPLETE"
VISUAL_TRUNCATED = "TRUNCATED"
VISUAL_FAIL = "FAIL"

#: 这些判定放行。注意 NOT_REQUIRED 是"不用看"，不是"看过了"。
PASSING_CODES = frozenset({VISUAL_PASS, VISUAL_NOT_REQUIRED})


class VisualGateError(RuntimeError):
    """门槛的调用方式不对。"""


@dataclass
class VisualGateResult:
    """视觉门的判定。"""

    code: str
    reasons: list[str] = field(default_factory=list)
    failed_items: list[ReviewItem] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.code in PASSING_CODES


def required_answers(plan: VisualReviewPlan) -> set[AnswerKey]:
    """计划要求的答案清单：每个 (选中页, 元素 ID, 检查码) 一条。"""

    answers: set[AnswerKey] = set()
    for page in plan.selected:
        for signal in page.signals:
            answers.add((page.candidate_page, signal.element_id, signal.code))
    return answers


def required_answers_from_document(
    plan: dict[str, Any],
) -> set[AnswerKey]:
    """从落盘的计划 JSON 读出同一份清单，供录入脚本核对覆盖。"""

    answers: set[AnswerKey] = set()
    for page in plan.get("selected", []):
        if not isinstance(page, dict):
            continue
        page_no = page.get("candidate_page")
        if not isinstance(page_no, int):
            continue
        for signal in page.get("signals", []):
            if not isinstance(signal, dict):
                continue
            code = str(signal.get("code") or "")
            element_id = str(signal.get("element_id") or "")
            if code and element_id:
                answers.add((page_no, element_id, code))
    return answers


def _describe(key: AnswerKey) -> str:
    page, element_id, code = key
    return f"第 {page} 页 {element_id} 的 {code}"


def check_visual_gate(
    plan: VisualReviewPlan,
    result: VisualReviewResult | None,
    *,
    identity: RunIdentity | None = None,
    candidate_sha256: str = "",
) -> VisualGateResult:
    """计划 + 结果 + 当前这一轮的身份 → 一个判定。

    ``identity`` 是完整的五元身份，走 ``verify_binding`` 全量比对；
    只拿得到候选哈希的老调用方可以传 ``candidate_sha256``，那时只比
    这一项——但它证明不了渲染计划和渲染器也没换。两个都不给是调用错误。
    """

    if identity is None and not candidate_sha256:
        raise VisualGateError(
            "视觉门必须知道当前这一轮的身份：给 identity（五元）"
            "或至少给 candidate_sha256"
        )

    if plan.truncated:
        pages = "、".join(
            f"第 {item.candidate_page} 页（风险分 {item.score}）"
            for item in plan.skipped
        )
        return VisualGateResult(
            VISUAL_TRUNCATED,
            [
                f"视觉检查计划被页数预算截断，{pages} 有风险但没进清单；"
                "增加预算重新计划，或交给人"
            ],
        )

    if not plan.selected:
        return VisualGateResult(
            VISUAL_NOT_REQUIRED, ["没有风险页，本轮不需要视觉检查"]
        )

    if result is None:
        return VisualGateResult(
            VISUAL_WAITING,
            [
                f"计划要求细看 {len(plan.selected)} 页，"
                "但还没有任何真实检查结果；计划不是结果，禁止交付"
            ],
        )

    # 第一步永远是绑定。看的不是这一轮的东西，后面比什么都没意义。
    if identity is not None:
        problems = verify_binding(result.binding_dict, identity)
        if problems:
            return VisualGateResult(VISUAL_STALE, problems)
    elif result.candidate_sha256 != candidate_sha256:
        return VisualGateResult(
            VISUAL_STALE,
            [
                "检查结果绑定的候选哈希 "
                f"{result.candidate_sha256[:12]}… 与当前候选 "
                f"{candidate_sha256[:12]}… 不一致——看的不是这份文件，"
                "结果作废"
            ],
        )

    required = required_answers(plan)
    known_elements = {(page, element_id) for page, element_id, _ in required}

    unknown = sorted(
        {
            (item.candidate_page, item.element_id)
            for item in result.items
            if (item.candidate_page, item.element_id) not in known_elements
        }
    )
    if unknown:
        return VisualGateResult(
            VISUAL_UNKNOWN_ELEMENT,
            [
                "结果里的这些元素不在计划里，对不上任何要检查的对象: "
                + "；".join(
                    f"第 {page} 页 {element_id}"
                    for page, element_id in unknown[:8]
                )
            ],
        )

    duplicates = result.duplicate_keys
    if duplicates:
        return VisualGateResult(
            VISUAL_DUPLICATE_ANSWER,
            [
                "同一个检查项答了两次，重复答案掩盖矛盾: "
                + "；".join(_describe(key) for key in duplicates[:8])
            ],
        )

    missing = sorted(required - result.answer_keys)
    if missing:
        return VisualGateResult(
            VISUAL_INCOMPLETE,
            [
                "以下检查项没有答案，只答一部分不算看过: "
                + "；".join(_describe(key) for key in missing[:8])
                + (f"；…另有 {len(missing) - 8} 项" if len(missing) > 8 else "")
            ],
        )

    failed = result.failed_items
    if failed:
        return VisualGateResult(
            VISUAL_FAIL,
            [
                f"视觉检查发现 {len(failed)} 项问题: "
                + "；".join(
                    f"第 {item.candidate_page} 页 {item.element_id} "
                    f"{item.check_code}（{item.detail or '无说明'}）"
                    for item in failed[:6]
                )
            ],
            failed_items=list(failed),
        )

    assert result.decision == DECISION_PASS
    return VisualGateResult(VISUAL_PASS)
