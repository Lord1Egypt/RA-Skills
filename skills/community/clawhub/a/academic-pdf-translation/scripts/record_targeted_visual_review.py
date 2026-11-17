"""把一次真正做过的视觉检查录成结果文件。

评审（人或审查代理）逐页逐项看完之后，把答案写成一个简单的 JSON：

    {
      "reviewer_type": "targeted-agent",
      "items": [
        {"candidate_page": 2, "element_id": "p0002-table-001",
         "check_code": "element-missing",
         "decision": "PASS", "detail": "表 1 在，位置正确"}
      ]
    }

每条答案都要写 ``element_id``：同一页上的两个表格可能触发同一个检查码，
不写元素就分不清看的是哪一个。

本脚本负责三件事，评审自己不用管：

1. 把**当前这一轮的五元身份**盖进结果——run_id、attempt_id、
   candidate_sha256、render_plan_sha256、renderer_build_id 全部按现场
   计算或从 current-run.json 读出，不接受评审手填。少一个、错一个，
   视觉门都会判 EVIDENCE_STALE；
2. 对照交付目录里的检查计划，逐 (页, 元素, 检查码) 核对覆盖；
3. 写出规范的 visual-review-result.json，供交付入口 --visual-result 使用。

退出码：0 = 已录入且覆盖完整；1 = 输入不合法或覆盖不完整。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402

from academic_pdf_translation.delivery.evidence import (  # noqa: E402
    attempt_dir,
    read_current_run,
)
from academic_pdf_translation.delivery.models import file_sha256  # noqa: E402
from academic_pdf_translation.verify.visual_gate import (  # noqa: E402
    required_answers_from_document,
)
from academic_pdf_translation.verify.visual_result import (  # noqa: E402
    VisualResultError,
    result_from_dict,
)

from _common import SkillError, load_json, write_json  # noqa: E402


def _current_attempt_dir(delivery_dir: Path) -> Path | None:
    """按 current-run.json 指针找"现在算数"的那一轮证据目录。

    禁止按固定文件名摸旧报告——旧证据还在，但它属于历史。
    """

    identity = read_current_run(delivery_dir)
    if identity is None:
        return None
    directory = attempt_dir(delivery_dir, identity.run_id, identity.attempt_id)
    return directory if directory.is_dir() else None


def _stamp_binding(
    raw: dict, delivery_dir: Path, candidate: Path
) -> dict:
    """把当前这一轮的五元身份盖进结果，评审填的一律覆盖。

    候选哈希按磁盘上的文件现算。算出来和 current-run.json 记的对不上，
    说明手上这份候选不是"现在算数"的那一份，这时候录进去只会得到一份
    注定 EVIDENCE_STALE 的证据，不如当场停下。
    """

    identity = read_current_run(delivery_dir)
    if identity is None:
        raise SkillError(
            f"{delivery_dir} 里没有 current-run.json，不知道现在算数的是哪一轮；"
            "先跑一次 deliver_first_candidate"
        )
    digest = file_sha256(Path(candidate))
    if identity.candidate_sha256 and identity.candidate_sha256 != digest:
        raise SkillError(
            f"候选 {candidate} 的哈希 {digest[:12]}… 与当前这一轮登记的 "
            f"{identity.candidate_sha256[:12]}… 不一致；"
            "看的不是现在算数的那份候选"
        )
    binding = identity.as_dict()
    binding["candidate_sha256"] = digest
    return {**raw, "binding": binding}


def _latest_build_candidate(delivery_dir: Path) -> Path | None:
    directory = _current_attempt_dir(delivery_dir)
    if directory is None:
        return None
    bundled = directory / "candidate.pdf"
    if bundled.is_file():
        return bundled
    for path in sorted(directory.glob("round-*-build.json"), reverse=True):
        candidate = load_json(path).get("candidate_path")
        if candidate and Path(candidate).is_file():
            return Path(candidate)
    return None


def _latest_plan(delivery_dir: Path) -> dict | None:
    directory = _current_attempt_dir(delivery_dir)
    if directory is None:
        return None
    for path in sorted(directory.glob("round-*-review.json"), reverse=True):
        return load_json(path)
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--result",
        type=Path,
        required=True,
        help="评审写的答案 JSON（reviewer_type + items）",
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        default=None,
        help="被检查的候选 PDF；默认取交付证据里最后一轮的候选",
    )
    parser.add_argument(
        "--delivery-dir",
        type=Path,
        default=None,
        help="交付证据目录，默认 <job_dir>/delivery",
    )
    args = parser.parse_args()

    job_dir = args.job_dir.resolve()
    delivery_dir = (args.delivery_dir or job_dir / "delivery").resolve()

    try:
        raw = load_json(args.result)
        candidate = args.candidate or _latest_build_candidate(delivery_dir)
        if candidate is None or not Path(candidate).is_file():
            raise SkillError(
                "找不到被检查的候选 PDF；用 --candidate 指明，"
                "或先跑一次 deliver_first_candidate 生成构建证据"
            )
        # 五元身份由脚本按现场计算/读取，不接受评审手填。
        result = result_from_dict(
            _stamp_binding(raw, delivery_dir, Path(candidate))
        )
    except (SkillError, VisualResultError, OSError, ValueError) as exc:
        print(f"错误: {exc}")
        return 1

    problems: list[str] = []
    plan = _latest_plan(delivery_dir)
    if plan is None:
        problems.append(
            "交付目录里没有检查计划（round-*-review.json）；"
            "结果照录，但无法核对覆盖是否完整"
        )
    else:
        # 逐 (页, 元素, 检查码) 核对。按页折叠会让同页同码的第二个元素
        # 白白蒙混过关。
        for page_no, element_id, code in sorted(
            required_answers_from_document(plan)
        ):
            if not result.answered(page_no, element_id, code):
                problems.append(
                    f"第 {page_no} 页 {element_id} 的 {code} 没有答案"
                )

    output = delivery_dir / "visual-review-result.json"
    write_json(output, result.as_dict())
    print(f"已录入: {output}")
    print(f"绑定: run={result.run_id} attempt={result.attempt_id}")
    print(f"候选哈希: {result.candidate_sha256}")
    print(f"渲染计划哈希: {result.render_plan_sha256}")
    print(f"渲染器构建: {result.renderer_build_id}")
    print(f"条目 {len(result.items)} 条，总结论 {result.decision}")
    if problems:
        print()
        print("覆盖不完整:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
