"""登记一条元素纠正。

自动识别可能出错，这个命令用来改。但它改不了两件事：
必需元素不能删除；省略必须给固定代码，自由文字理由无效。
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

from academic_pdf_translation.analysis.element_overrides import (  # noqa: E402
    ALLOWED_ACTIONS,
    OMIT_CODES,
    ElementOverride,
    OverrideError,
    apply_all,
    load_overrides,
    save_overrides,
)
from academic_pdf_translation.analysis.source_elements import (  # noqa: E402
    analyze_job_elements,
)

from _common import SkillError, import_fitz  # noqa: E402


def _bbox(value: str | None) -> list[float] | None:
    if not value:
        return None
    parts = [item.strip() for item in value.split(",")]
    if len(parts) != 4:
        raise SkillError("--bbox 必须是 x0,y0,x1,y1")
    try:
        return [float(item) for item in parts]
    except ValueError as exc:
        raise SkillError(f"无效坐标: {value!r}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_dir", type=Path)
    parser.add_argument("--action", required=True, choices=list(ALLOWED_ACTIONS))
    parser.add_argument("--element", required=True, help="被纠正的元素 ID")
    parser.add_argument("--reason", required=True, help="为什么要改")
    parser.add_argument("--author", required=True, help="修改人或智能体 ID")
    parser.add_argument("--new-type", help="retype 的目标类型")
    parser.add_argument(
        "--omit-code",
        choices=list(OMIT_CODES),
        help="omit-nonsemantic 的固定省略代码",
    )
    parser.add_argument("--bbox", help="move-bbox 的新坐标 x0,y0,x1,y1")
    parser.add_argument(
        "--merge-with",
        action="append",
        default=[],
        help="merge 时要并进来的元素 ID，可重复",
    )
    parser.add_argument("--relation", help="link/unlink 的关系名")
    parser.add_argument("--target", help="link/unlink 的目标元素 ID")
    parser.add_argument(
        "--part",
        action="append",
        default=[],
        help="split 的子元素，格式 类型:x0,y0,x1,y1，可重复",
    )
    parser.add_argument(
        "--evidence",
        action="append",
        default=[],
        help="结构化证据，格式 键=值，可重复",
    )
    args = parser.parse_args()

    try:
        parts = []
        for spec in args.part:
            kind, _, box = spec.partition(":")
            parts.append({"type": kind.strip(), "bbox": _bbox(box)})
        evidence = {}
        for item in args.evidence:
            key, _, value = item.partition("=")
            evidence[key.strip()] = value.strip()

        override = ElementOverride(
            action=args.action,
            element_id=args.element,
            reason=args.reason,
            author=args.author,
            evidence=evidence,
            new_type=args.new_type,
            omit_code=args.omit_code,
            bbox=_bbox(args.bbox),
            parts=parts,
            merge_with=list(args.merge_with),
            relation=args.relation,
            target_id=args.target,
        )

        fitz = import_fitz()
        inventory = analyze_job_elements(
            args.job_dir,
            pymupdf_version=getattr(fitz, "VersionBind", "0"),
        )
        overrides = load_overrides(args.job_dir)
        apply_all(inventory, [*overrides, override])
        overrides.append(override)
        path = save_overrides(args.job_dir, overrides)
    except (SkillError, OverrideError, OSError, ValueError) as exc:
        print(f"错误: {exc}")
        return 1

    print(f"纠正已记录: {path}")
    print(json.dumps(override.as_dict(), ensure_ascii=False, indent=2))
    print(f"应用后元素总数: {len(inventory.elements)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
