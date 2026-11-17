"""首次交付的唯一入口：生成、核查、最多返修一次、再核查，给一个结论。

之前每一步都有自己的脚本，各自打印一份"看起来还行"。合起来就出事了：
生成脚本说 READY_TO_REGISTER，核查脚本说少了一张图，谁也不为最后那个
"能不能给读者"负责。这个脚本负责。

退出码就是结论，方便脚本串联：
    0 = 可以交付
    2 = 交给人处理（机器已经修过一轮，剩下的需要判断）
    1 = 停下别交（生成失败，或者返修把别的地方弄坏了）
"""

from __future__ import annotations

import sys
from pathlib import Path

# 按 README 的写法 `python3 scripts/X.py` 运行时，sys.path 里只有 scripts/，
# 没有仓库根，academic_pdf_translation 包就 import 不到。先把根加进去。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
import json  # noqa: E402
import uuid  # noqa: E402
from pathlib import Path  # noqa: E402

from academic_pdf_translation.analysis.element_overrides import (  # noqa: E402
    apply_all,
    load_overrides,
)
from academic_pdf_translation.analysis.source_elements import (  # noqa: E402
    analyze_job_elements,
)
from academic_pdf_translation.contracts.migration import (  # noqa: E402
    derive_quality_mode,
)
from academic_pdf_translation.delivery.evidence import (  # noqa: E402
    EVIDENCE_STALE,
    attempt_dir,
    read_current_run,
    verify_binding,
)
from academic_pdf_translation.delivery.first_delivery import (  # noqa: E402
    STATUS_BLOCKED,
    STATUS_DELIVERED,
    STATUS_HANDOVER,
    FirstDeliveryError,
    format_result,
    run_first_delivery,
)
from academic_pdf_translation.delivery.models import (  # noqa: E402
    FORMULA_CROPS_FILE,
    KNOWN_BUILD_STATUSES,
    BuildOutcome,
    build_outcome_from_report,
    file_sha256,
)
from academic_pdf_translation.planning.render_plan import (  # noqa: E402
    PLAN_FILE_NAME,
    build_render_plan,
    write_plan,
)
from academic_pdf_translation.verify.repair import (  # noqa: E402
    ACTION_PRESERVE_REGION,
    RepairPlan,
)
from academic_pdf_translation.verify.visual_result import (  # noqa: E402
    VisualResultError,
    result_from_dict,
)

from _common import (  # noqa: E402
    SkillError,
    import_fitz,
    load_json,
    write_json,
)
from build_first_candidate import build_first_candidate  # noqa: E402
from build_render_plan import (  # noqa: E402
    FORCED_STRATEGIES_FILE,
    load_forced_strategies,
)

EXIT_CODES = {
    STATUS_DELIVERED: 0,
    STATUS_HANDOVER: 2,
    STATUS_BLOCKED: 1,
}

#: 返修计划里只有这些动作能落到渲染计划上。其余的（比如图题绑组）
#: 由页面合成器按绑定组处理，不经过这里。
STRATEGY_ACTIONS = frozenset({ACTION_PRESERVE_REGION})


def _job_inputs(job_dir: Path) -> tuple[list, list, list]:
    elements = load_json(job_dir / "source_elements.json").get("elements") or []
    units = load_json(job_dir / "translation.json").get("units") or []
    bindings = load_json(job_dir / "unit_bindings.json").get("bindings") or []
    if not elements:
        raise SkillError(f"{job_dir} 的 source_elements.json 里没有元素")
    if not bindings:
        raise SkillError(
            f"{job_dir} 的 unit_bindings.json 里没有绑定；"
            "没有绑定就没法按译文定位元素"
        )
    return (elements, units, bindings)


def read_render_plan(job_dir: Path) -> tuple[str, dict | None]:
    """读作业里**当前**这一份渲染计划，返回（哈希, 计划正文）。

    调用点很关键：必须在一轮生成结束之后读，读到的才是这一轮真正
    用过的那份。返修会重算计划，提前读会把旧身份带到新候选上。
    """

    path = job_dir / PLAN_FILE_NAME
    if not path.is_file():
        return ("", None)
    return (file_sha256(path), load_json(path))


def read_formula_crops(job_dir: Path) -> dict[str, dict]:
    """读生成器这一轮写出的公式裁切记录：element_id → formula_crop。

    只有带 source_element_id 的桥接条目才有裁切记录；老式手写条目没有，
    对应公式就拿不出"确定完整"的证据，视觉计划会默认要求看它。
    """

    path = job_dir / "complex_content.json"
    if not path.is_file():
        return {}
    crops: dict[str, dict] = {}
    for item in load_json(path).get("items") or []:
        if not isinstance(item, dict):
            continue
        payload = item.get("payload") or {}
        element_id = str(item.get("source_element_id") or "")
        crop = payload.get("formula_crop") if isinstance(payload, dict) else None
        if element_id and isinstance(crop, dict):
            crops[element_id] = crop
    return crops


def read_formula_crop_snapshot(directory: Path) -> dict[str, dict]:
    """读这一轮 attempt 目录里的公式裁切快照。

    没有快照就返回空：拿不出裁切证据的公式一律进视觉检查。宁可多看
    几页，也不能让一份可以被改的作业文件把公式变成免检。
    """

    path = Path(directory) / FORMULA_CROPS_FILE
    if not path.is_file():
        return {}
    data = load_json(path)
    if not isinstance(data, dict):
        return {}
    return {
        str(key): value
        for key, value in data.items()
        if isinstance(value, dict)
    }


def generate_render_plan(job_dir: Path, forced: dict[str, str]):
    """按当前元素清单算一份渲染计划并写进作业目录。"""

    fitz = import_fitz()
    inventory = analyze_job_elements(
        job_dir, pymupdf_version=getattr(fitz, "VersionBind", "0")
    )
    apply_all(inventory, load_overrides(job_dir))
    plan = build_render_plan(
        inventory,
        derive_quality_mode(load_json(job_dir / "job.json")),
        forced_strategies=forced,
    )
    write_plan(job_dir, plan)
    return plan


#: 缺渲染计划时的唯一出路：自动生成，或者报这个码停下。
#: 「没有计划所以合同通过」这条逃生通道已经关掉了。
BLOCKED_RENDER_PLAN_MISSING = "BLOCKED_RENDER_PLAN_MISSING"


def ensure_render_plan(job_dir: Path) -> Path:
    """v2 作业必须有渲染计划：没有就现算一份，算不出来就停。"""

    path = job_dir / PLAN_FILE_NAME
    if path.is_file():
        return path
    try:
        generate_render_plan(job_dir, load_forced_strategies(job_dir))
    except (SkillError, OSError, ValueError, KeyError, TypeError) as exc:
        raise SkillError(
            f"{BLOCKED_RENDER_PLAN_MISSING}: 作业里没有 {PLAN_FILE_NAME}，"
            f"自动生成也没成功（{exc}）。"
            "旧作业要跳过元素级合同，必须显式加 --legacy-no-render-plan"
        ) from exc
    if not path.is_file():
        raise SkillError(
            f"{BLOCKED_RENDER_PLAN_MISSING}: 自动生成之后仍然没有 "
            f"{PLAN_FILE_NAME}"
        )
    return path


def rebuild_render_plan(job_dir: Path) -> dict[str, str]:
    """按返修指定的降级重算渲染计划，并返回实际生效的降级。"""

    forced = load_forced_strategies(job_dir)
    plan = generate_render_plan(job_dir, forced)
    applied = {
        item.element_id: item.strategy
        for item in plan.elements
        if item.element_id in forced and item.strategy == forced[item.element_id]
    }
    write_json(
        job_dir / "repair" / "applied_strategies.json",
        {
            "requested": forced,
            "applied": applied,
            "plan_problems": list(plan.problems),
        },
    )
    return applied


def make_builder(job_dir: Path, output: Path | None):
    """把真实的候选生成器包成交付流程要的 build(round_index)。

    返回 :class:`BuildOutcome`，把生成器自己报告的状态原样带给交付门槛。
    之前这里只要 candidate 路径存在就当成功——生成器说 BLOCKED 也拦不住
    交付流程。现在状态跟着产物一起出去，判定交给 ``check_build_gate``。
    """

    run_id = f"run-{uuid.uuid4().hex[:12]}"

    def build(round_index: int) -> BuildOutcome:
        label = "first" if round_index == 0 else f"repair-{round_index}"
        if round_index > 0:
            # 返修那一轮必须先重算渲染计划，降级指令才有机会生效。
            rebuild_render_plan(job_dir)
        report = build_first_candidate(
            job_dir, output, attempt_label=label
        )
        # 计划要在**生成之后**读：返修那一轮的计划是刚刚重算出来的，
        # 开跑前读到的那一份已经过期了。
        plan_sha, plan = read_render_plan(job_dir)
        return build_outcome_from_report(
            report,
            run_id=run_id,
            attempt_id=f"attempt-{round_index + 1}",
            render_plan_sha256=plan_sha,
            render_plan=plan,
            formula_crops=read_formula_crops(job_dir),
        )

    return build


def make_resume_builder(delivery_dir: Path, job_dir: Path | None = None):
    """--resume 用的构建器：不重建，取当前运行的候选原样核查。

    典型用法：第一遍交付停在 WAITING_FOR_VISUAL_REVIEW，评审看完页、
    录完结果后带 --visual-result 重跑。重建会改变文件字节，让刚录的
    结果立刻 STALE——所以续跑必须复用同一份候选。

    候选可能是返修后的 attempt-2。返回的 outcome 标了 ``reused``，
    交付流程据此接手当前身份，不新建 attempt、不重新复制候选——
    否则 attempt-2 的候选会被写回 attempt-1，覆盖第一轮的历史证据。
    """

    def build(round_index: int) -> BuildOutcome:
        if round_index > 0:
            raise SkillError("--resume 只核查，不做返修重建")
        identity = read_current_run(delivery_dir)
        if identity is None:
            raise SkillError(
                "没有 current-run.json；先跑一次完整交付再 --resume"
            )
        directory = attempt_dir(
            delivery_dir, identity.run_id, identity.attempt_id
        )
        candidate = directory / "candidate.pdf"
        if not candidate.is_file():
            raise SkillError(f"当前运行没有候选副本: {candidate}")
        if file_sha256(candidate) != identity.candidate_sha256:
            raise SkillError(
                "EVIDENCE_STALE: 候选副本与 current-run.json 指纹不一致"
            )
        # 构建记录是这一轮"生成到底成没成"的唯一证据。没有它就没有
        # 结论可恢复：新建 attempt 的写入顺序是 复制候选 → 写指针 →
        # 写计划快照 → 写构建记录，程序在中途挂掉时目录里会只剩候选和
        # 指针。那种半截目录必须停下，不能替它补一个"看起来成功"的状态。
        record_path = (
            directory / f"round-{identity.attempt_id}-build.json"
        )
        if not record_path.is_file():
            raise SkillError(
                f"{EVIDENCE_STALE}: 当前 attempt 缺少构建记录，禁止恢复"
                f"（{record_path}）"
            )
        record = load_json(record_path)
        status = str(record.get("status") or "")
        if status not in KNOWN_BUILD_STATUSES:
            raise SkillError(
                f"{EVIDENCE_STALE}: 构建记录里的状态 {status!r} 不是已知状态，"
                "禁止恢复"
            )
        # 光验候选 PDF 不够：构建记录本身也要属于当前
        # run / attempt / 候选 / 计划 / 渲染器，五项差一项就是旧证据。
        binding_problems = verify_binding(
            record.get("binding") or {}, identity
        )
        if binding_problems:
            raise SkillError(
                "构建记录与当前运行身份对不上：" + "；".join(binding_problems)
            )
        # 计划取这一轮自己的快照，不取作业目录里"现在"那一份——
        # 作业目录里的可能已经是后来重算的了。
        snapshot = directory / "render-plan.json"
        plan = load_json(snapshot) if snapshot.is_file() else None
        if plan is None and job_dir is not None:
            # 老运行没留快照。作业目录里那份只有在哈希对得上当前身份时
            # 才允许顶替——对不上就是别人的计划，宁可没有。
            plan_sha, current_plan = read_render_plan(job_dir)
            if plan_sha and plan_sha == identity.render_plan_sha256:
                plan = current_plan
        return BuildOutcome(
            status=status,
            candidate_path=candidate,
            issues=list(record.get("issues") or []),
            candidate_sha256=identity.candidate_sha256,
            renderer_build_id=identity.renderer_build_id,
            run_id=identity.run_id,
            attempt_id=f"attempt-{identity.attempt_id}",
            render_plan_sha256=identity.render_plan_sha256,
            render_plan=plan,
            reused=True,
            # 裁切证据只认这一轮自己的快照，不重读作业目录——作业目录
            # 里那份两次执行之间可能被改，而候选、计划和五元身份都不会
            # 察觉。快照缺失就当没有裁切证据：公式默认进视觉检查。
            formula_crops=read_formula_crop_snapshot(directory),
        )

    return build


def make_repair_applier(job_dir: Path):
    """把返修计划落成渲染计划能读的降级指定。"""

    def apply_repair(plan: RepairPlan) -> None:
        forced = {
            item.element_id: item.action
            for item in plan.actions
            if item.action in STRATEGY_ACTIONS and item.element_id
        }
        write_json(
            job_dir / FORCED_STRATEGIES_FILE,
            {
                "schema_version": "1.0",
                "round_index": plan.round_index,
                "forced_strategies": forced,
                "actions": [item.as_dict() for item in plan.actions],
                "manual": [item.as_dict() for item in plan.manual],
            },
        )

    return apply_repair


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--delivery-dir",
        type=Path,
        default=None,
        help="证据写到哪里，默认 <job_dir>/delivery",
    )
    parser.add_argument(
        "--page-budget",
        type=int,
        default=6,
        help="最多渲染几页给人细看",
    )
    parser.add_argument(
        "--no-repair",
        action="store_true",
        help="只核查，不执行那一轮返修",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="不重建，对当前运行的候选直接核查（配合 --visual-result 用）",
    )
    parser.add_argument(
        "--visual-result",
        type=Path,
        default=None,
        help="真实视觉检查结果（visual-review-result.json）；"
        "有风险页而不提供时，结论最多到 handover，不会是 delivered",
    )
    parser.add_argument(
        "--legacy-no-render-plan",
        action="store_true",
        help="旧作业兼容：跳过元素级渲染合同。v2 作业不要用——"
        "没有渲染计划的交付不等于合同通过",
    )
    parser.add_argument("--json", action="store_true", help="只输出 JSON")
    args = parser.parse_args()

    job_dir = args.job_dir.resolve()
    delivery_dir = (args.delivery_dir or job_dir / "delivery").resolve()
    try:
        visual_result = None
        if args.visual_result is not None:
            visual_result = result_from_dict(load_json(args.visual_result))
        elements, units, bindings = _job_inputs(job_dir)
        # v2 作业二选一：要么有渲染计划（没有就现算一份），要么显式声明
        # 自己是旧作业。删掉 render_plan.json 不能变成"合同通过"。
        if not args.legacy_no_render_plan and not args.resume:
            ensure_render_plan(job_dir)
        result = run_first_delivery(
            job_dir / "source.pdf",
            elements,
            units,
            bindings,
            build=(
                make_resume_builder(delivery_dir, job_dir)
                if args.resume
                else make_builder(job_dir, args.output)
            ),
            apply_repair=(
                None
                if args.no_repair or args.resume
                else make_repair_applier(job_dir)
            ),
            output_dir=delivery_dir,
            page_budget=args.page_budget,
            visual_result=visual_result,
            require_render_plan=not args.legacy_no_render_plan,
        )
    except (
        SkillError,
        FirstDeliveryError,
        VisualResultError,
        OSError,
        ValueError,
    ) as exc:
        print(f"错误: {exc}")
        return 1

    write_json(delivery_dir / "delivery.json", result.as_dict())
    if args.json:
        print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(format_result(result))
    return EXIT_CODES.get(result.status, 1)


if __name__ == "__main__":
    raise SystemExit(main())
