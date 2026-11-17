"""从元素清单生成渲染计划 render_plan.json。

内部返修会把"这个元素该降到哪一级"写进 repair/forced_strategies.json。
这里读它，交给 build_render_plan 去校验——只许沿降级链往下，往回调会被拒。
文件不存在就当没有返修，计划完全由清单和档位决定。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 按 README 的写法 `python3 scripts/X.py` 运行时，sys.path 里只有 scripts/，
# 没有仓库根，academic_pdf_translation 包就 import 不到。先把根加进去。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
from pathlib import Path  # noqa: E402

from academic_pdf_translation.analysis.element_overrides import (  # noqa: E402
    apply_all,
    load_overrides,
)
from academic_pdf_translation.analysis.source_elements import (  # noqa: E402
    analyze_job_elements,
)
from academic_pdf_translation.contracts.migration import (
    derive_quality_mode,  # noqa: E402
)
from academic_pdf_translation.planning.render_plan import (  # noqa: E402
    build_figure_inventory,
    build_render_plan,
    write_plan,
)

from _common import SkillError, import_fitz, load_json, write_json  # noqa: E402

FORCED_STRATEGIES_FILE = Path("repair") / "forced_strategies.json"


def load_forced_strategies(job_dir: Path) -> dict[str, str]:
    """读内部返修指定的降级目标。没有就返回空。"""

    path = job_dir / FORCED_STRATEGIES_FILE
    if not path.is_file():
        return {}
    payload = load_json(path)
    forced = payload.get("forced_strategies")
    if not isinstance(forced, dict):
        raise SkillError(
            f"{path} 里的 forced_strategies 必须是元素 id 到策略名的字典"
        )
    return {str(key): str(value) for key, value in forced.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--write-figure-inventory",
        action="store_true",
        help="兼容保留：图表清单现在默认自动写回，此开关不再需要",
    )
    args = parser.parse_args()
    job_dir = args.job_dir.resolve()
    try:
        job = load_json(job_dir / "job.json")
        quality_mode = derive_quality_mode(job)
        fitz = import_fitz()
        inventory = analyze_job_elements(
            job_dir,
            pymupdf_version=getattr(fitz, "VersionBind", "0"),
        )
        apply_all(inventory, load_overrides(job_dir))
        forced = load_forced_strategies(job_dir)
        plan = build_render_plan(
            inventory, quality_mode, forced_strategies=forced
        )
        path = write_plan(job_dir, plan)
        # 图表清单是计划的派生视图，默认自动写回——不再手写、不再漂移。
        write_json(
            job_dir / "figure_inventory.json",
            build_figure_inventory(inventory, plan),
        )
    except (SkillError, OSError, ValueError) as exc:
        print(f"错误: {exc}")
        return 1

    print(f"渲染计划已写入: {path}")
    print(f"质量档位: {plan.quality_mode}")
    print(f"必需元素: {plan.required_elements}")
    print(f"已安排: {plan.planned_elements}  合法省略: {plan.omitted_elements}")
    print(f"未解决: {plan.unresolved_elements}")
    print(f"完整（程序计算）: {plan.complete}")
    if forced:
        print(f"内部返修指定的降级: {len(forced)} 个元素")
    counts: dict[str, int] = {}
    for item in plan.elements:
        counts[item.strategy] = counts.get(item.strategy, 0) + 1
    print("策略分布:")
    for name, count in sorted(counts.items()):
        print(f"  {name:<48}{count:>4}")
    if plan.problems:
        print("问题:")
        for problem in plan.problems:
            print(f"  - {problem}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
