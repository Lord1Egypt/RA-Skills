#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""functional-food-officers 提示词合并导出脚本。

用法：
    python export_prompt.py                 # 在技能根目录执行，输出 functional-food-officers-prompt.md
    python export_prompt.py <技能根目录> <输出文件>

合并顺序：SKILL.md → catalog → requirements（含行业校准总表与合规红线速查）→ exemplars → FFO 域范本（按 X0→N1-N4→B1-B10）。
"""
import sys
from pathlib import Path

DOMAIN_ORDER = [
    "FFO-X0-路由编排域范本.md",
    "FFO-N1-人力资源域范本.md",
    "FFO-N2-财务会计域范本.md",
    "FFO-N3-行政办公域范本.md",
    "FFO-N4-信息技术域范本.md",
    "FFO-B1-情报采集与监测域范本.md",
    "FFO-B2-资质认证与监管域范本.md",
    "FFO-B3-内容生产与传播域范本.md",
    "FFO-B4-活动运营与执行域范本.md",
    "FFO-B5-客户与伙伴运营域范本.md",
    "FFO-B6-供应链与运营保障域范本.md",
    "FFO-B7-数据分析与决策域范本.md",
    "FFO-B8-流程协同与项目管理域范本.md",
    "FFO-B9-合规审核与风控域范本.md",
    "FFO-B10-知识管理与培训域范本.md",
]

CORE = [
    "SKILL.md",
    "references/FFO-catalog.md",
    "references/FFO-requirements.md",
    "references/FFO-exemplars.md",
]


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else root / "functional-food-officers-prompt.md"
    parts: list[str] = []
    missing: list[str] = []
    for rel in CORE + [f"references/{n}" for n in DOMAIN_ORDER]:
        p = root / rel
        if p.exists():
            parts.append(p.read_text(encoding="utf-8"))
        else:
            missing.append(rel)
    out.write_text("\n\n".join(parts), encoding="utf-8")
    print(f"OK: merged {len(parts) - len(missing)} files -> {out}")
    if missing:
        print("MISSING (skipped): " + ", ".join(missing))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
