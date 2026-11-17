"""统一首次交付入口。

之前每一步都有自己的脚本，各自打印一份"看起来还行"。合起来就出事了：
生成脚本说 READY_TO_REGISTER，核查脚本说少了一张图，谁也不为最后那个
"能不能给读者"负责。

这里只给**一个**结论，而且只有三种：

- ``delivered``：核查全过。
- ``handover``：还有问题，但机器已经修过一轮，剩下的必须人来看。
- ``blocked``：返修把别的地方弄坏了，或者生成本身失败了。停下，别交。

三条硬规矩写在流程里，不靠调用方自觉：

1. **最多重建一次。** 第二轮返修计划会被 :mod:`repair` 直接拒绝，
   这里再加一道断言，防止有人绕过去。
2. **"通过"是算出来的。** 只有结构对账 passed 且映射核查零问题才算交付，
   任何人往结果里写 ``status`` 都不作数。
3. **证据落盘。** 映射、对账、视觉检查计划、返修计划、渲染出来的页，
   全部写进交付目录。没有证据的结论不算结论。
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from academic_pdf_translation.delivery.evidence import (
    EVIDENCE_STALE,
    RunIdentity,
    attempt_dir,
    new_run_id,
    read_current_run,
    verify_binding,
    write_current_run,
)
from academic_pdf_translation.delivery.gates import (
    GATE_REPAIR,
    check_build_gate,
)
from academic_pdf_translation.delivery.models import (
    BUILD_READY,
    FORMULA_CROPS_FILE,
    KNOWN_BUILD_STATUSES,
    BuildOutcome,
    file_sha256,
    formula_crops_sha256,
)
from academic_pdf_translation.verify.candidate_mapping import (
    CandidateMapping,
    build_mapping,
    element_texts_from_units,
    verify_mapping,
)
from academic_pdf_translation.verify.render_contract import (
    contract_from_documents,
    derive_candidate_elements,
)
from academic_pdf_translation.verify.repair import (
    MAX_REPAIR_ROUNDS,
    RepairPlan,
    compare_rounds,
    fallback_levels_by_element,
    plan_repair,
)
from academic_pdf_translation.verify.structural_audit import (
    StructuralAudit,
    audit_structure,
)
from academic_pdf_translation.verify.visual_gate import (
    VisualGateResult,
    check_visual_gate,
)
from academic_pdf_translation.verify.visual_result import VisualReviewResult
from academic_pdf_translation.verify.visual_review import (
    DEFAULT_PAGE_BUDGET,
    VisualReviewPlan,
    build_review_plan,
    render_review_pages,
)

SCHEMA_VERSION = "1.0"

STATUS_DELIVERED = "delivered"
STATUS_HANDOVER = "handover"
STATUS_BLOCKED = "blocked"

#: 返修跑完却一个字没改，说明降级根本没落到生成器上。
#: 这比"修了没修好"严重得多，必须单独报出来。
REPAIR_MADE_NO_DIFFERENCE = (
    "返修重建出来的候选与返修前内容完全相同——降级指令没有落到生成器上，这一轮返修等于没跑"
)

#: v2 作业必须有渲染计划。缺计划时报这个码，不许静默当成"合同通过"。
BLOCKED_RENDER_PLAN_MISSING = "BLOCKED_RENDER_PLAN_MISSING"

STAGE_BUILD = "build"
STAGE_MAP = "map"
STAGE_AUDIT = "audit"
STAGE_REVIEW = "visual-review"
STAGE_REPAIR = "repair"
STAGE_REBUILD = "rebuild"
STAGE_REVERIFY = "re-verify"


class FirstDeliveryError(RuntimeError):
    """首次交付流程本身出了问题。"""


@dataclass
class StageRecord:
    """一步的结果。写清楚做了什么、成没成、凭什么。"""

    name: str
    ok: bool
    detail: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class DeliveryResult:
    """一次首次交付的完整结论与证据。"""

    schema_version: str = SCHEMA_VERSION
    status: str = STATUS_BLOCKED
    rebuilds: int = 0
    stages: list[StageRecord] = field(default_factory=list)
    problems: list[str] = field(default_factory=list)
    manual_items: list[dict[str, Any]] = field(default_factory=list)
    evidence: dict[str, str] = field(default_factory=dict)
    candidate_path: str = ""
    #: 每一轮生成的完整构建状态（含构建报告哈希），一轮一条。
    builds: list[dict[str, Any]] = field(default_factory=list)
    #: 本次交付的运行身份。attempt_id 指向"现在算数"的那一轮。
    run_id: str = ""
    attempt_id: int = 0

    @property
    def delivered(self) -> bool:
        return self.status == STATUS_DELIVERED

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "delivered": self.delivered,
            "rebuilds": self.rebuilds,
            "candidate_path": self.candidate_path,
            "stages": [item.as_dict() for item in self.stages],
            "problem_count": len(self.problems),
            "problems": list(self.problems),
            "manual_count": len(self.manual_items),
            "manual_items": list(self.manual_items),
            "evidence": dict(self.evidence),
            "builds": list(self.builds),
            "run_id": self.run_id,
            "attempt_id": self.attempt_id,
        }


def _open(path: Path) -> Any:
    import fitz

    if not Path(path).is_file():
        raise FirstDeliveryError(f"PDF 不存在: {path}")
    return fitz.open(path)


def candidate_content_hash(path: Path) -> str:
    """候选的内容哈希。

    用页面文字、绘图对象数量、图像数量算，不用文件字节——PDF 里有时间戳，
    字节每次都不一样，内容却可能一模一样。要判断"返修到底改没改东西"，
    只能看内容。
    """

    import hashlib

    digest = hashlib.sha256()
    document = _open(path)
    for index in range(document.page_count):
        page = document[index]
        digest.update(page.get_text("text").encode("utf-8"))
        digest.update(str(len(page.get_drawings())).encode("ascii"))
        digest.update(str(len(page.get_images())).encode("ascii"))
    return digest.hexdigest()


def _write_json(path: Path, payload: Any) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return str(path)


@dataclass
class VerifyRound:
    """一轮核查的三件产物。"""

    mapping: CandidateMapping
    audit: StructuralAudit
    review: VisualReviewPlan
    mapping_problems: list[str]

    @property
    def clean(self) -> bool:
        """通过与否是算出来的，不看任何人写进来的字段。"""

        return self.audit.passed and not self.mapping_problems


def verify_candidate(
    source_document: Any,
    candidate_path: Path,
    elements: list[dict[str, Any]],
    *,
    element_texts: dict[str, str],
    output_dir: Path,
    label: str,
    page_budget: int = DEFAULT_PAGE_BUDGET,
    render_pages: bool = True,
    binding: dict[str, Any] | None = None,
    render_plan: dict[str, Any] | None = None,
    formula_crops: dict[str, dict[str, Any]] | None = None,
) -> tuple[VerifyRound, dict[str, str]]:
    """对一份候选跑完阶段 9、10、11，并把证据落盘。

    ``binding`` 是这一轮的运行身份，写进每份证据——报告要能证明
    "我说的就是这一份候选"。
    """

    candidate = _open(candidate_path)
    mapping = build_mapping(
        source_document, candidate, elements, element_texts=element_texts
    )
    audit = audit_structure(mapping, elements)
    # 视觉计划要知道每个元素是什么类型、计划怎么处理、公式裁得干不干净：
    # 结构映射全绿不代表版面没问题，复杂内容默认进视觉检查。
    review = build_review_plan(
        mapping,
        audit,
        page_budget=page_budget,
        elements=elements,
        render_plan=render_plan,
        formula_crops=formula_crops,
    )
    if render_pages and review.selected:
        render_review_pages(candidate, review, output_dir / f"{label}-pages")

    def _bound(payload: dict[str, Any]) -> dict[str, Any]:
        if binding is None:
            return payload
        return {"binding": dict(binding), **payload}

    evidence = {
        f"{label}-mapping": _write_json(
            output_dir / f"{label}-mapping.json", _bound(mapping.as_dict())
        ),
        f"{label}-audit": _write_json(
            output_dir / f"{label}-audit.json", _bound(audit.as_dict())
        ),
        f"{label}-review": _write_json(
            output_dir / f"{label}-review.json", _bound(review.as_dict())
        ),
    }
    return (
        VerifyRound(
            mapping=mapping,
            audit=audit,
            review=review,
            mapping_problems=verify_mapping(mapping),
        ),
        evidence,
    )


def _collect_problems(round_result: VerifyRound) -> list[str]:
    return list(round_result.audit.problems) + list(
        round_result.mapping_problems
    )


def _as_outcome(value: Any) -> BuildOutcome:
    """把构建回调的返回值规整成 :class:`BuildOutcome`。

    正式调用方（CLI）必须返回带真实状态的 ``BuildOutcome``。裸路径
    只留给测试里的合成候选用——返回裸路径等于调用方**显式声明**这一轮
    是 READY_TO_REGISTER，声明错了责任在调用方，不在门槛。
    """

    if isinstance(value, BuildOutcome):
        return value
    return BuildOutcome(status=BUILD_READY, candidate_path=Path(value))


def _attempt_number(outcome: BuildOutcome, default: int) -> int:
    """取 BuildOutcome 自报的 attempt 序号。

    生成器写的是 ``attempt-2`` 这种带前缀的字符串，恢复流程写的可能是
    纯数字。取不出来才退回 ``default``——退回是兜底，不是常态。
    """

    raw = str(outcome.attempt_id or "").strip()
    if raw.startswith("attempt-"):
        raw = raw[len("attempt-") :]
    try:
        number = int(raw)
    except ValueError:
        return default
    return number if number > 0 else default


def _bind_attempt(
    result: DeliveryResult,
    outcome: BuildOutcome,
    output_dir: Path,
    run_id: str,
    attempt_id: int,
) -> RunIdentity:
    """建立这一轮的运行身份：候选拷进 attempt 目录，指针原子更新。

    指针更新后，上一轮的证据自动变成历史——它还在磁盘上，
    但五元绑定对不上当前身份，谁也不能再拿它验证新候选。

    渲染计划哈希取自 ``outcome``，也就是**这一轮真正用过的**那份。
    返修会重算计划，用流程开始时读到的旧哈希会让证据身份写错。
    """

    candidate_sha = outcome.candidate_sha256 or ""
    if (
        not candidate_sha
        and outcome.candidate_path is not None
        and outcome.candidate_path.is_file()
    ):
        candidate_sha = file_sha256(outcome.candidate_path)
    identity = RunIdentity(
        run_id=run_id,
        attempt_id=attempt_id,
        candidate_sha256=candidate_sha,
        render_plan_sha256=outcome.render_plan_sha256,
        renderer_build_id=outcome.renderer_build_id,
    )
    directory = attempt_dir(output_dir, run_id, attempt_id)
    directory.mkdir(parents=True, exist_ok=True)
    if outcome.candidate_path is not None and outcome.candidate_path.is_file():
        bundled = directory / "candidate.pdf"
        if outcome.candidate_path.resolve() != bundled.resolve():
            import shutil

            shutil.copy2(outcome.candidate_path, bundled)
    write_current_run(output_dir, identity)
    result.run_id = run_id
    result.attempt_id = attempt_id
    return identity


def _adopt_attempt(
    result: DeliveryResult,
    outcome: BuildOutcome,
    output_dir: Path,
) -> RunIdentity:
    """复用已有候选：原样接手当前运行身份，一个字节都不改。

    ``--resume`` 要做的事只有"把没做完的门槛做完"。它不新建 attempt、
    不重新复制候选、不动 ``current-run.json``——否则第二轮的候选会被
    重新写回第一轮，把历史证据覆盖掉。

    接手前先核对：磁盘上的"现在"必须就是这份候选。对不上说明中途换过
    候选，那就不是恢复，是另一次运行，必须停。
    """

    identity = read_current_run(output_dir)
    if identity is None:
        raise FirstDeliveryError(
            "没有 current-run.json，无从恢复；复用候选必须有当前运行身份"
        )
    candidate_sha = outcome.candidate_sha256 or ""
    if candidate_sha and candidate_sha != identity.candidate_sha256:
        raise FirstDeliveryError(
            f"{EVIDENCE_STALE}: 要复用的候选与 current-run.json 指纹不一致"
        )
    result.run_id = identity.run_id
    result.attempt_id = identity.attempt_id
    return identity


def _write_plan_snapshot(
    result: DeliveryResult,
    outcome: BuildOutcome,
    evidence_dir: Path,
    label: str,
) -> None:
    """把这一轮用过的渲染计划副本存进本轮的 attempt 目录。

    磁盘上 ``render_plan.json`` 只有"现在"这一份，返修一重算就没了。
    要事后证明"第二轮是按第二份计划渲染的"，只能在当轮存副本。
    """

    if outcome.render_plan is None:
        return
    result.evidence[f"{label}-render-plan"] = _write_json(
        evidence_dir / "render-plan.json", outcome.render_plan
    )


def _write_formula_crop_snapshot(
    result: DeliveryResult,
    outcome: BuildOutcome,
    evidence_dir: Path,
    label: str,
) -> None:
    """把这一轮的公式裁切证据存进本轮的 attempt 目录。

    作业目录里的 ``complex_content.json`` 只有"现在"这一份，两次执行
    之间可能被改。恢复时重读它，等于让一份可变的文件去决定"这个公式
    要不要人看"，而候选、计划、五元身份全都察觉不到。存快照之后，
    恢复只认自己这一轮的证据。

    空字典也要写：空快照和"没有快照"是两回事，前者是这一轮确实没有
    裁切证据，后者是证据丢了。
    """

    result.evidence[f"{label}-formula-crops"] = _write_json(
        evidence_dir / FORMULA_CROPS_FILE, outcome.formula_crops
    )


def _record_build(
    result: DeliveryResult,
    outcome: BuildOutcome,
    evidence_dir: Path,
    label: str,
    *,
    identity: RunIdentity,
) -> None:
    """构建状态与报告哈希落进结论和证据，谁也删不掉。"""

    record = outcome.as_dict()
    record["report_sha256"] = outcome.report_sha256()
    record["formula_crops_sha256"] = formula_crops_sha256(
        outcome.formula_crops
    )
    record["binding"] = identity.as_dict()
    result.builds.append(record)
    result.evidence[f"{label}-build"] = _write_json(
        evidence_dir / f"{label}-build.json", record
    )


def verify_existing_attempt_evidence(
    result: DeliveryResult,
    evidence_dir: Path,
    label: str,
    *,
    identity: RunIdentity,
) -> None:
    """恢复时只核对既有构建证据，一个字节都不写。

    ``--resume`` 造出来的 :class:`BuildOutcome` 是从磁盘反推的简化版，
    缺预检路径、缺 issues 原文。拿它再写一遍 ``round-N-build.json`` 和
    ``render-plan.json``，等于用简化记录替换原件——历史证据当场被改。

    所以恢复只做三件事：确认记录在、确认状态是已知状态、确认记录的
    五元绑定就是当前身份。任何一条不成立都停，绝不替它补一个默认值。
    """

    record_path = evidence_dir / f"{label}-build.json"
    if not record_path.is_file():
        raise FirstDeliveryError(
            f"{EVIDENCE_STALE}: 当前 attempt 缺少构建记录，禁止恢复"
            f"（{record_path}）"
        )
    record = json.loads(record_path.read_text(encoding="utf-8"))
    status = str(record.get("status") or "")
    if status not in KNOWN_BUILD_STATUSES:
        raise FirstDeliveryError(
            f"{EVIDENCE_STALE}: 构建记录里的状态 {status!r} 不是已知状态，"
            "禁止恢复"
        )
    problems = verify_binding(record.get("binding") or {}, identity)
    if problems:
        raise FirstDeliveryError(
            "构建记录与当前运行身份对不上：" + "；".join(problems)
        )
    crops_path = evidence_dir / FORMULA_CROPS_FILE
    expected_crops = str(record.get("formula_crops_sha256") or "")
    if crops_path.is_file() and expected_crops:
        # 快照还在就必须和构建记录对得上：有人改过它就是旧证据。
        # 快照丢了不拦——没有裁切证据意味着公式默认进视觉检查，
        # 那是更保守的方向，不是放松。
        actual = formula_crops_sha256(
            json.loads(crops_path.read_text(encoding="utf-8"))
        )
        if actual != expected_crops:
            raise FirstDeliveryError(
                f"{EVIDENCE_STALE}: 公式裁切快照与构建记录的指纹不一致"
            )
    result.builds.append(record)
    result.evidence[f"{label}-build"] = str(record_path)
    snapshot = evidence_dir / "render-plan.json"
    if snapshot.is_file():
        result.evidence[f"{label}-render-plan"] = str(snapshot)
    if crops_path.is_file():
        result.evidence[f"{label}-formula-crops"] = str(crops_path)


def _apply_visual_gate(
    result: DeliveryResult,
    plan: VisualReviewPlan,
    visual_result: VisualReviewResult | None,
    candidate_path: Path,
    *,
    identity: RunIdentity,
    label: str,
    output_dir: Path,
) -> VisualGateResult:
    """算视觉门、落证据、写阶段记录。

    没有真实结果时 ``ok`` 必须为 False——"已生成检查任务"不是
    "检查已通过"。FAIL 条目转成给人的返修任务。
    """

    # 结果必须对上这一轮的五元身份（run / attempt / 候选 / 计划 / 渲染器），
    # 差一项就是 EVIDENCE_STALE。只比候选哈希证明不了计划和渲染器没换。
    gate = check_visual_gate(plan, visual_result, identity=identity)
    if visual_result is not None:
        result.evidence[f"{label}-visual-result"] = _write_json(
            output_dir / f"{label}-visual-result.json",
            visual_result.as_dict(),
        )
    result.stages.append(
        StageRecord(
            STAGE_REVIEW,
            gate.passed,
            f"视觉门 {gate.code}：计划细看 {len(plan.selected)} 页，"
            f"{len(plan.skipped)} 页超预算",
        )
    )
    if not gate.passed:
        result.problems.extend(
            f"[{gate.code}] {reason}" for reason in gate.reasons
        )
    for item in gate.failed_items:
        result.manual_items.append(
            {
                # 返修任务要指到具体元素。只写页码等于让人自己去找
                #「第 7 页到底哪儿不对」。
                "element_id": item.element_id,
                "signal": "visual-fail",
                "reason": (
                    f"视觉检查不通过：第 {item.candidate_page} 页 "
                    f"{item.element_id} 的 {item.check_code}"
                    f"（{item.detail or '无说明'}），需要返修"
                ),
            }
        )
    return gate


def _apply_render_contract(
    result: DeliveryResult,
    mapping: Any,
    elements: list[dict[str, Any]],
    render_plan: dict[str, Any] | None,
    evidence_dir: Path,
    label: str,
    *,
    require_render_plan: bool,
) -> bool:
    """按元素 ID 对账三份清单，证据落盘。

    候选元素视图由映射派生（没有手写字段）。``require_render_plan``
    为真时没有计划就是硬失败：删掉 ``render_plan.json`` 不能变成
    "合同通过"。只有显式声明的老作业才允许跳过这道合同。
    """

    candidate_view = derive_candidate_elements(mapping)
    result.evidence[f"{label}-candidate-elements"] = _write_json(
        evidence_dir / "candidate-elements.json", candidate_view
    )
    if render_plan is None:
        if require_render_plan:
            result.problems.append(
                f"[{BLOCKED_RENDER_PLAN_MISSING}] 这一轮没有渲染计划，"
                "元素级合同无从对账；缺计划不等于合同通过"
            )
            return False
        return True
    contract = contract_from_documents(
        {"elements": elements}, render_plan, candidate_view
    )
    result.evidence[f"{label}-render-contract"] = _write_json(
        evidence_dir / "render-contract.json", contract.as_dict()
    )
    if not contract.passed:
        result.problems.extend(
            f"[render-contract] {problem}" for problem in contract.problems
        )
    return contract.passed


def run_first_delivery(
    source_path: Path,
    elements: list[dict[str, Any]],
    units: list[dict[str, Any]],
    bindings: list[dict[str, Any]],
    *,
    build: Callable[[int], BuildOutcome | Path],
    output_dir: Path,
    apply_repair: Callable[[RepairPlan], None] | None = None,
    page_budget: int = DEFAULT_PAGE_BUDGET,
    render_pages: bool = True,
    visual_result: VisualReviewResult | None = None,
    # 默认就要求渲染计划。放过"没有计划"等于给旧链路留逃生通道，
    # 旧作业要跳过元素级合同必须由调用方显式关掉。
    require_render_plan: bool = True,
) -> DeliveryResult:
    """跑完首次交付，给出唯一结论。

    ``build(round_index)`` 由调用方提供，返回这一轮的 :class:`BuildOutcome`。
    交付流程不关心是谁生成的，但**关心生成器自己怎么说**：生成器说
    BLOCKED，这里就是 blocked，候选文件存在与否都改变不了这一点。

    渲染计划不是流程参数，而是 :class:`BuildOutcome` 的一部分：每一轮
    带上自己真正用过的那份计划与哈希。返修会重算计划，用开跑时读到的
    那一份去核查第二轮候选，等于用错的身份签发证据。
    """

    if not elements:
        raise FirstDeliveryError("元素清单为空，无法交付")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    result = DeliveryResult()
    element_texts = element_texts_from_units(elements, units, bindings=bindings)
    source_document = _open(Path(source_path))

    try:
        outcome = _as_outcome(build(0))
    except Exception as exc:  # noqa: BLE001 - 生成失败要变成结论，不是崩溃
        result.stages.append(StageRecord(STAGE_BUILD, False, f"生成失败: {exc}"))
        result.problems.append(f"候选生成失败: {exc}")
        result.status = STATUS_BLOCKED
        return result

    # 新建候选才绑定新 attempt；复用已有候选只接手当前身份。
    # 这条分界线就是"历史证据不可修改"的全部实现。
    if outcome.reused:
        try:
            identity = _adopt_attempt(result, outcome, output_dir)
        except FirstDeliveryError as exc:
            result.stages.append(
                StageRecord(STAGE_BUILD, False, f"恢复失败: {exc}")
            )
            result.problems.append(str(exc))
            result.status = STATUS_BLOCKED
            return result
        run_id = identity.run_id
        first_attempt = identity.attempt_id
    else:
        run_id = outcome.run_id or new_run_id()
        first_attempt = _attempt_number(outcome, 1)
        identity = _bind_attempt(
            result, outcome, output_dir, run_id, first_attempt
        )
    evidence_dir = attempt_dir(output_dir, run_id, first_attempt)
    first_label = f"round-{first_attempt}"
    if outcome.reused:
        # 恢复只允许新增（新视觉结果、新门槛结果、新 delivery.json），
        # 不许重写原候选、原计划快照、原构建记录。
        try:
            verify_existing_attempt_evidence(
                result, evidence_dir, first_label, identity=identity
            )
        except FirstDeliveryError as exc:
            result.stages.append(
                StageRecord(STAGE_BUILD, False, f"恢复失败: {exc}")
            )
            result.problems.append(str(exc))
            result.status = STATUS_BLOCKED
            return result
    else:
        _write_plan_snapshot(result, outcome, evidence_dir, first_label)
        _write_formula_crop_snapshot(
            result, outcome, evidence_dir, first_label
        )
        _record_build(
            result, outcome, evidence_dir, first_label, identity=identity
        )
    if outcome.candidate_path is not None:
        # 候选留作证据——它是不是"能交付的候选"由门槛说了算。
        result.candidate_path = str(outcome.candidate_path)

    build_gate = check_build_gate(outcome)
    result.stages.append(
        StageRecord(
            STAGE_BUILD,
            build_gate.passed,
            f"生成器状态 {outcome.status}"
            + (
                f"，候选 {outcome.candidate_path.name}"
                if outcome.candidate_path is not None
                else "，没有候选文件"
            ),
        )
    )
    if build_gate.blocked:
        # 生成器自己说不行：不做候选映射，不生成视觉结论，立即停。
        result.problems = list(build_gate.reasons)
        result.status = STATUS_BLOCKED
        return result

    if require_render_plan and outcome.render_plan is None:
        # 没有渲染计划就没有元素级合同。缺计划必须停，不能悄悄退回旧链路。
        result.stages.append(
            StageRecord(
                STAGE_BUILD,
                False,
                f"{BLOCKED_RENDER_PLAN_MISSING}：这一轮没有渲染计划",
            )
        )
        result.problems.append(
            f"[{BLOCKED_RENDER_PLAN_MISSING}] 这一轮没有渲染计划，"
            "元素级合同无从对账"
        )
        result.status = STATUS_BLOCKED
        return result

    build_needs_repair = build_gate.verdict == GATE_REPAIR
    if build_needs_repair:
        result.problems.extend(build_gate.reasons)
        if (
            outcome.candidate_path is None
            or not outcome.candidate_path.is_file()
        ):
            result.problems.append(
                "生成器要求返修却没有留下候选文件，无从核查，停下"
            )
            result.status = STATUS_BLOCKED
            return result

    candidate_path = Path(outcome.candidate_path)

    first, evidence = verify_candidate(
        source_document,
        candidate_path,
        elements,
        element_texts=element_texts,
        output_dir=evidence_dir,
        label=first_label,
        page_budget=page_budget,
        render_pages=render_pages,
        binding=identity.as_dict(),
        render_plan=outcome.render_plan,
        formula_crops=outcome.formula_crops,
    )
    result.evidence.update(evidence)
    result.stages.append(
        StageRecord(
            STAGE_MAP,
            not first.mapping_problems,
            f"{len(first.mapping.located)}/{len(first.mapping.locations)} 个元素定位到候选",
        )
    )
    result.stages.append(
        StageRecord(
            STAGE_AUDIT,
            first.audit.passed,
            f"{len(first.audit.problems)} 条结构问题",
        )
    )
    first_contract_ok = _apply_render_contract(
        result,
        first.mapping,
        elements,
        outcome.render_plan,
        evidence_dir,
        first_label,
        require_render_plan=require_render_plan,
    )
    first_gate = _apply_visual_gate(
        result, first.review, visual_result, candidate_path, label=first_label,
        identity=identity,
        output_dir=evidence_dir,
    )

    if first.clean:
        if build_needs_repair:
            # 核查层没查出可修的点，但生成器自己说要修——两边说法对不上，
            # 这种矛盾要人看，不能当没听见直接交付。
            result.status = STATUS_HANDOVER
            return result
        if not first_gate.passed:
            # 计划不是结果。该看的页没看完（或看出了问题），不许交付。
            result.status = STATUS_HANDOVER
            return result
        if not first_contract_ok:
            # 元素级合同没对上：有必需元素没计划、被计两次或非法省略。
            result.status = STATUS_HANDOVER
            return result
        result.status = STATUS_DELIVERED
        return result

    repair = plan_repair(
        first.mapping,
        first.audit,
        round_index=0,
        fallback_levels=fallback_levels_by_element(outcome.render_plan),
    )
    result.evidence["repair-plan"] = _write_json(
        evidence_dir / "repair-plan.json", repair.as_dict()
    )
    result.manual_items = result.manual_items + [
        item.as_dict() for item in repair.manual
    ]

    if not repair.actions:
        result.stages.append(
            StageRecord(
                STAGE_REPAIR, False, "没有机器能安全执行的返修动作"
            )
        )
        result.problems = result.problems + _collect_problems(first)
        result.status = STATUS_HANDOVER
        return result

    result.stages.append(
        StageRecord(
            STAGE_REPAIR,
            True,
            f"{len(repair.actions)} 条降级/重排动作，"
            f"{len(repair.manual)} 条交给人",
        )
    )

    if apply_repair is None or outcome.reused:
        result.stages.append(
            StageRecord(
                STAGE_REBUILD,
                False,
                "恢复模式只做未完成的门槛，不重建"
                if outcome.reused
                else "调用方没有提供返修执行器，不重建",
            )
        )
        result.problems = result.problems + _collect_problems(first)
        result.status = STATUS_HANDOVER
        return result

    try:
        apply_repair(repair)
        repaired_outcome = _as_outcome(build(1))
    except Exception as exc:  # noqa: BLE001 - 返修失败同样要变成结论
        result.stages.append(
            StageRecord(STAGE_REBUILD, False, f"返修重建失败: {exc}")
        )
        result.problems = (
            result.problems
            + _collect_problems(first)
            + [f"返修重建失败: {exc}"]
        )
        result.status = STATUS_BLOCKED
        return result

    second_attempt = _attempt_number(repaired_outcome, first_attempt + 1)
    identity = _bind_attempt(
        result, repaired_outcome, output_dir, run_id, second_attempt
    )
    evidence_dir = attempt_dir(output_dir, run_id, second_attempt)
    second_label = f"round-{second_attempt}"
    _write_plan_snapshot(result, repaired_outcome, evidence_dir, second_label)
    _write_formula_crop_snapshot(
        result, repaired_outcome, evidence_dir, second_label
    )
    _record_build(
        result, repaired_outcome, evidence_dir, second_label, identity=identity
    )
    rebuild_gate = check_build_gate(repaired_outcome)
    if rebuild_gate.blocked or repaired_outcome.candidate_path is None:
        result.stages.append(
            StageRecord(
                STAGE_REBUILD,
                False,
                f"返修重建后生成器状态 {repaired_outcome.status}，停下",
            )
        )
        result.problems = (
            result.problems
            + _collect_problems(first)
            + list(rebuild_gate.reasons)
        )
        result.status = STATUS_BLOCKED
        return result
    rebuild_needs_repair = rebuild_gate.verdict == GATE_REPAIR
    if rebuild_needs_repair:
        result.problems.extend(rebuild_gate.reasons)

    repaired_path = Path(repaired_outcome.candidate_path)
    result.rebuilds = 1
    result.candidate_path = str(repaired_path)
    unchanged = candidate_content_hash(candidate_path) == (
        candidate_content_hash(repaired_path)
    )
    result.stages.append(
        StageRecord(
            STAGE_REBUILD,
            not unchanged,
            f"重建候选 {repaired_path.name}"
            + ("（内容与返修前完全相同）" if unchanged else ""),
        )
    )

    second, evidence = verify_candidate(
        source_document,
        repaired_path,
        elements,
        element_texts=element_texts,
        output_dir=evidence_dir,
        label=second_label,
        page_budget=page_budget,
        render_pages=render_pages,
        binding=identity.as_dict(),
        render_plan=repaired_outcome.render_plan,
        formula_crops=repaired_outcome.formula_crops,
    )
    result.evidence.update(evidence)

    outcome = compare_rounds(first.mapping, second.mapping)
    result.evidence["repair-outcome"] = _write_json(
        evidence_dir / "repair-outcome.json", outcome.as_dict()
    )
    result.stages.append(
        StageRecord(STAGE_REVERIFY, second.clean, outcome.verdict)
    )

    # 这里再挡一道：返修只有一轮，任何绕过 repair 模块的调用都到不了第三轮。
    if plan_repair(
        second.mapping, second.audit, round_index=MAX_REPAIR_ROUNDS
    ).allowed:
        raise FirstDeliveryError("返修轮数上限失效，流程必须停下")

    # 返修产生的是**新候选**，round-1 的视觉结果对它天然无效——
    # 门槛按新候选的哈希重新判定（旧结果会得到 STALE）。
    second_contract_ok = _apply_render_contract(
        result,
        second.mapping,
        elements,
        repaired_outcome.render_plan,
        evidence_dir,
        second_label,
        require_render_plan=require_render_plan,
    )
    second_gate = _apply_visual_gate(
        result, second.review, visual_result, repaired_path, label=second_label,
        identity=identity,
        output_dir=evidence_dir,
    )

    result.problems = result.problems + _collect_problems(second)
    if unchanged:
        result.problems.insert(0, REPAIR_MADE_NO_DIFFERENCE)
        result.status = STATUS_BLOCKED
        return result
    if outcome.regressions:
        result.problems.insert(
            0,
            "返修把原本没问题的地方弄坏了: " + "、".join(outcome.regressions),
        )
        result.status = STATUS_BLOCKED
    elif second.clean:
        # 重建那一轮生成器若仍报 NEEDS_REPAIR，唯一的返修已经用掉，
        # 剩下的矛盾交给人；视觉门没过同样不许交付。
        result.status = (
            STATUS_DELIVERED
            if not rebuild_needs_repair
            and second_gate.passed
            and second_contract_ok
            else STATUS_HANDOVER
        )
    else:
        result.status = STATUS_HANDOVER
    return result


def format_result(result: DeliveryResult) -> str:
    """给人看的一页纸。"""

    label = {
        STATUS_DELIVERED: "可以交付",
        STATUS_HANDOVER: "交给人处理",
        STATUS_BLOCKED: "停下，别交",
    }.get(result.status, result.status)
    lines = [f"结论: {label}（重建 {result.rebuilds} 次）"]
    for stage in result.stages:
        lines.append(f"  [{'ok' if stage.ok else '!!'}] {stage.name}: {stage.detail}")
    if result.problems:
        lines.append("")
        lines.append(f"剩余问题 {len(result.problems)} 条:")
        lines.extend(f"  - {problem}" for problem in result.problems[:12])
        if len(result.problems) > 12:
            lines.append(f"  …另有 {len(result.problems) - 12} 条见证据文件")
    if result.manual_items:
        lines.append("")
        lines.append(f"需要人判断 {len(result.manual_items)} 条")
    if result.evidence:
        lines.append("")
        lines.append("证据:")
        lines.extend(
            f"  {name}: {path}" for name, path in sorted(result.evidence.items())
        )
    return "\n".join(lines)
