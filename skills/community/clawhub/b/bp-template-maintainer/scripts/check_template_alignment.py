#!/usr/bin/env python3
"""用于检查 BP 母版一致性的工作区脚本。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


METADATA_KEYS = [
    "所属项目",
    "节点编号",
    "文档类型",
    "文档编号",
    "文档标题",
    "文档状态",
    "责任 Agent",
    "版本",
    "创建时间",
    "更新时间",
    "标签",
]

EXPECTED_BP_BLOCKS = [
    (
        "2.1 经营与利润目标达成",
        "P4432-1",
        "G-1.1 / G-1.2 / G-1.3 / G-16.2 / G-2.4",
    ),
    ("2.2 产品力发展战略与价值闭环", "P4432-2", "G-8.4 / G-7 / G-4.1"),
    (
        "2.3 管理方式向机制与数据驱动转型",
        "P4432-3",
        "G-3.2 / G-3.1 / G-13.2 / G-15.1",
    ),
    (
        "2.4 组织与价值分配稳定机制建设",
        "P4432-4",
        "G-5.1 / G-5.2 / G-14.3",
    ),
    (
        "2.5 院外业务第二增长曲线推进",
        "P4432-5",
        "G-9.1 / G-9.3 / G-9.7 / G-9.2",
    ),
    (
        "2.6 重大风险与合规事件全过程可控",
        "P4432-6",
        "G-6.1 / G-6.2 / G-18.1",
    ),
]

TEMPLATES = {
    "month": {
        "path": "P001-T001-MONTH-TPL-01_月报模板_v1.md",
        "sections": [
            "## 1. 汇报综述",
            "## 2. BP目标承接与对齐情况",
            "## 3. 核心结果与经营表现",
            "## 4. 关键举措推进情况",
            "## 5. 问题、偏差与原因分析",
            "## 6. 风险预警与资源需求",
            "## 7. 下月重点安排",
            "## 8. 需决策 / 需协同事项",
        ],
    },
    "quarter": {
        "path": "P001-T001-QUARTER-TPL-01_季报模板_v1.md",
        "sections": [
            "## 1. 汇报综述",
            "## 2. BP目标承接与对齐情况",
            "## 3. 核心结果与经营表现",
            "## 4. 关键举措推进情况",
            "## 5. 问题、偏差与原因分析",
            "## 6. 风险预警与资源需求",
            "## 7. 下季度重点安排",
            "## 8. 需决策 / 需协同事项",
        ],
    },
    "halfyear": {
        "path": "P001-T001-HALFYEAR-TPL-01_半年报模板_v1.md",
        "sections": [
            "## 1. 汇报综述",
            "## 2. BP目标承接与对齐情况",
            "## 3. 核心结果与经营表现",
            "## 4. 关键举措推进情况",
            "## 5. 问题、偏差与原因分析",
            "## 6. 风险预警与资源需求",
            "## 7. 下半程重点安排",
            "## 8. 需决策 / 需协同事项",
        ],
    },
    "year": {
        "path": "P001-T001-YEAR-TPL-01_年报模板_v1.md",
        "sections": [
            "## 1. 汇报综述",
            "## 2. BP目标承接与对齐情况",
            "## 3. 核心结果与经营表现",
            "## 4. 关键举措推进情况",
            "## 5. 问题、偏差与原因分析",
            "## 6. 风险预警与资源需求",
            "## 7. 下一年度重点安排",
            "## 8. 需决策 / 需协同事项",
        ],
    },
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_block(text: str, heading: str) -> str | None:
    pattern = re.compile(
        rf"^### {re.escape(heading)}\n(?P<body>.*?)(?=^### |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        return None
    return match.group("body")


def check_metadata(text: str, issues: list[str]) -> None:
    for key in METADATA_KEYS:
        marker = f"- {key}："
        if marker not in text:
            issues.append(f"缺少元数据字段 `{key}`")


def check_sections(text: str, expected_sections: list[str], issues: list[str]) -> None:
    headings = [line.strip() for line in text.splitlines() if line.startswith("## ")]
    for section in expected_sections:
        if section not in headings:
            issues.append(f"缺少章节 `{section}`")
    if len(headings) != len(expected_sections):
        issues.append(
            f"一级章节数量异常：期望 {len(expected_sections)} 个，实际 {len(headings)} 个"
        )


def check_bp_blocks(text: str, issues: list[str]) -> None:
    for heading, personal_bp, organization_bp in EXPECTED_BP_BLOCKS:
        block = extract_block(text, heading)
        if block is None:
            issues.append(f"缺少 BP 区块 `{heading}`")
            continue

        personal_marker = f"- 对应个人 BP：{personal_bp}"
        if personal_marker not in block:
            issues.append(f"`{heading}` 缺少个人 BP `{personal_bp}`")

        organization_marker = f"- 对应组织 BP：{organization_bp}"
        if organization_marker not in block:
            issues.append(f"`{heading}` 缺少组织 BP `{organization_bp}`")


def check_template(path: Path, expected_sections: list[str]) -> list[str]:
    issues: list[str] = []

    if not path.exists():
        return ["文件不存在"]

    text = read_text(path)
    check_metadata(text, issues)
    check_sections(text, expected_sections, issues)
    check_bp_blocks(text, issues)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查工作区 BP 母版是否发生共同结构漂移。"
    )
    parser.add_argument(
        "--root",
        default=".",
        help="包含 P001-T001 模板文件的工作区根目录。",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    failures = 0

    for name, config in TEMPLATES.items():
        path = root / config["path"]
        issues = check_template(path, config["sections"])
        if issues:
            failures += 1
            print(f"[失败] {name}: {path}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[通过] {name}: {path}")

    if failures:
        print(f"\n共有 {failures} 个模板文件检查失败。")
        return 1

    print("\n全部模板文件检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
