#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""functional-food-officers 结构与规范自检脚本。

检查项：
  1. 两级目录硬约束（references/scripts/templates 内不得再有子目录）
  2. SKILL.md frontmatter 必填 5 字段（description/description_zh/description_en/version/author）
  3. SKILL.md 引用的子资源路径真实存在
  4. 企业名禁词扫描（脱敏复查：技能内不得出现任何具体企业数据）

用法：python validate_skill.py <技能根目录>
退出码：0=全部通过；1=存在 FAIL。
"""
import re
import sys
from pathlib import Path

FORBIDDEN_WORDS = [
    "纤仔", "每膳", "纤华", "安壹生", "海博君安", "集福", "向左转",
    "九州通", "王海英", "王兰柱", "南总", "黄总", "蔡总", "张鹤",
    "3000 万个馒头", "19.9", "瘦 8 斤",
]

REQUIRED_FRONTMATTER = ["description", "description_zh", "description_en", "version", "author"]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    errors = 0

    # 1. 两级目录硬约束
    for sub in ("references", "scripts", "templates"):
        d = root / sub
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if p.is_dir():
                fail(f"两级目录违规：{sub}/ 下存在子目录 {p.name}/")
                errors += 1

    # 2. SKILL.md frontmatter 必填字段
    skill = root / "SKILL.md"
    if not skill.exists():
        fail("SKILL.md 不存在")
        return 1
    text = skill.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail("SKILL.md 缺少 YAML frontmatter")
        errors += 1
    else:
        fm = m.group(1)
        for field in REQUIRED_FRONTMATTER:
            if not re.search(rf"^{field}\s*:", fm, re.M):
                fail(f"frontmatter 缺少必填字段：{field}")
                errors += 1

    # 3. SKILL.md 引用的子资源路径存在
    for ref in re.findall(r"references/[\w\-.]+\.md", text):
        if not (root / ref).exists():
            fail(f"SKILL.md 引用的子资源不存在：{ref}")
            errors += 1
    for script in re.findall(r"scripts/[\w\-.]+\.py", text):
        if not (root / script).exists():
            fail(f"SKILL.md 引用的脚本不存在：{script}")
            errors += 1

    # 4. 企业名禁词扫描（全文）
    hits: list[str] = []
    for p in root.rglob("*.md"):
        content = p.read_text(encoding="utf-8", errors="ignore")
        for w in FORBIDDEN_WORDS:
            if w in content:
                hits.append(f"{p.relative_to(root)}: {w}")
    if hits:
        for h in hits:
            fail(f"禁词命中（企业数据脱敏违规）：{h}")
        errors += 1

    if errors == 0:
        print("PASS: 结构、frontmatter、引用、禁词扫描全部通过")
        return 0
    print(f"共 {errors} 项 FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
