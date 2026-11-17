"""交付门槛：纯函数，进来是事实，出去是判定。

每道门只回答一个问题，答案只有三种：

- ``continue``：这一步没问题，流程往下走；
- ``repair-required``：有问题，允许走一轮受控返修，但不许直接交付；
- ``blocked``：立即停下，后面的检查一步都不做。

门不修东西、不写文件、不打日志——它只判定。这样每道门都能单独测试，
也没有任何一条路径能"顺便"把状态改好看。
"""

from __future__ import annotations

from dataclasses import dataclass, field

from academic_pdf_translation.delivery.models import (
    BUILD_BLOCKED,
    BUILD_NEEDS_REPAIR,
    BUILD_READY,
    KNOWN_BUILD_STATUSES,
    BuildOutcome,
)

GATE_CONTINUE = "continue"
GATE_REPAIR = "repair-required"
GATE_BLOCKED = "blocked"

#: 生成器报了一个谁也不认识的状态。未知不是"大概没事"，未知就是停。
BLOCKED_UNKNOWN_BUILD_STATUS = "BLOCKED_UNKNOWN_BUILD_STATUS"


@dataclass
class GateResult:
    """一道门的判定。``reasons`` 里写清楚凭什么。"""

    verdict: str
    reasons: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.verdict == GATE_CONTINUE

    @property
    def blocked(self) -> bool:
        return self.verdict == GATE_BLOCKED


def check_build_gate(outcome: BuildOutcome) -> GateResult:
    """构建门：生成器自己说不行，外层就不许说行。

    规则：

    - ``BLOCKED_BEFORE_PREFLIGHT`` → 立即停。不做候选映射、不生成
      视觉结论、不允许 delivered。候选文件可以留作证据，但只是证据。
    - ``NEEDS_REPAIR`` → 记录问题，允许一轮受控返修，不能直接交付。
    - ``READY_TO_REGISTER`` → 候选文件真实存在才放行。
    - 未知状态 → 立即停，报 ``BLOCKED_UNKNOWN_BUILD_STATUS``。
    """

    status = outcome.status
    if status not in KNOWN_BUILD_STATUSES:
        return GateResult(
            GATE_BLOCKED,
            [
                f"{BLOCKED_UNKNOWN_BUILD_STATUS}: 生成器报告了未知状态 "
                f"{status!r}，未知状态一律按失败处理"
            ],
        )

    if status == BUILD_BLOCKED:
        stage = outcome.blocked_stage or "未知阶段"
        reasons = [
            f"生成器在 {stage} 就停了（{BUILD_BLOCKED}），"
            "候选未通过内部检查，禁止继续核查与交付"
        ]
        reasons.extend(_format_issues(outcome))
        return GateResult(GATE_BLOCKED, reasons)

    if status == BUILD_NEEDS_REPAIR:
        reasons = [
            f"生成器预检报告 {BUILD_NEEDS_REPAIR}，候选保留为证据，"
            "允许一轮受控返修，但不能直接交付"
        ]
        reasons.extend(_format_issues(outcome))
        return GateResult(GATE_REPAIR, reasons)

    # READY_TO_REGISTER：生成器说好，还得真有文件。
    if outcome.candidate_path is None or not outcome.candidate_path.is_file():
        return GateResult(
            GATE_BLOCKED,
            [
                f"生成器报告 {BUILD_READY} 却没有产出候选文件 "
                f"{outcome.candidate_path}，报告与产物对不上，停下"
            ],
        )
    return GateResult(GATE_CONTINUE)


def _format_issues(outcome: BuildOutcome) -> list[str]:
    formatted = []
    for item in outcome.issues[:5]:
        formatted.append(f"构建问题: {item}")
    remaining = len(outcome.issues) - 5
    if remaining > 0:
        formatted.append(f"…另有 {remaining} 条构建问题见构建报告")
    return formatted
