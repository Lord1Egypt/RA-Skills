"""生成原文元素清单 source_elements.json。

命令行入口只做三件事：读参数、调用正式包、打印结果。
"""

from __future__ import annotations

import sys
from pathlib import Path

# 按 README 的写法 `python3 scripts/X.py` 运行时，sys.path 里只有 scripts/，
# 没有仓库根，academic_pdf_translation 包就 import 不到。先把根加进去。
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import argparse  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

from academic_pdf_translation.analysis.source_elements import (  # noqa: E402
    ELEMENTS_FILE_NAME,
    analyze_job_elements,
)
from academic_pdf_translation.planning.mode_policy import policy_for_job  # noqa: E402

from _common import SkillError, import_fitz  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument(
        "--json",
        action="store_true",
        help="输出完整清单而不是摘要",
    )
    args = parser.parse_args()
    try:
        fitz = import_fitz()
        inventory = analyze_job_elements(
            args.job_dir,
            pymupdf_version=getattr(fitz, "VersionBind", "0"),
        )
    except (SkillError, OSError, ValueError) as exc:
        print(f"错误: {exc}")
        return 1

    if args.json:
        print(json.dumps(inventory.as_dict(), ensure_ascii=False, indent=2))
        return 0

    try:
        job = json.loads(
            (args.job_dir.resolve() / "job.json").read_text(encoding="utf-8")
        )
        floor = policy_for_job(job).element_confidence_floor
    except (OSError, ValueError):
        floor = 0.70

    print(f"元素清单已写入: {args.job_dir.resolve() / ELEMENTS_FILE_NAME}")
    print(f"元素总数: {len(inventory.elements)}")
    print(f"必需元素: {len(inventory.required_elements())}")
    print("各类型数量:")
    for name, count in inventory.type_counts().items():
        print(f"  {name:<22}{count:>4}")
    print(f"未解决元素: {len(inventory.unresolved_elements)}")
    print(f"高风险页面: {inventory.high_risk_pages()}")
    low = inventory.low_confidence_elements(floor)
    print(f"低置信度元素（低于 {floor}）: {len(low)}")
    for element in low[:10]:
        print(f"  {element.id} {element.type.value} conf={element.confidence}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
