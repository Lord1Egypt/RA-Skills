#!/usr/bin/env python3
"""coverage_seed.py — coverage.md 自动播种器（纪律 11 ③ · references/coverage-seeding.md 落地脚本，M 级）。

从目标技能 SKILL.md 的 description（frontmatter）解析自声明范围，按覆盖播种规则
预填 references/coverage.md 骨架；创作者确认/修改后定稿（锻造炉不强制覆盖创作修改）。

用法：
  python scripts/coverage_seed.py <技能目录>            # 播种（已存在则不覆盖）
  python scripts/coverage_seed.py <技能目录> --force    # 强制重新播种（覆盖已有）
  python scripts/coverage_seed.py <技能目录> --dry      # 只打印将生成的维度，不写文件
退出码：0=已生成或已存在；2=目标无效/无 description
"""
import argparse
import os
import re
import sys

# description 模式 → 覆盖维度（coverage-seeding.md 第一节）
PATTERN_RULES = [
    (r"支持\s*[^，。；、]{1,40}?(?:平台|格式|系统|工具|渠道)", "platform"),
    (r"用于\s*[^，。；、]{1,40}?(?:场景|任务|分析|检索|生成|整理|审计|审查)", "scenario"),
    (r"生成\s*[^，。；、]{1,30}?(?:风格|类型|文档|报告|视频|图表)", "genre"),
    (r"封装|对接|接入|API|接口", "endpoint"),
    (r"部署|发布|上线|运维", "platform"),
    (r"诊断|排查|排障|修复|报错|错误|异常", "symptom"),
    (r"工作流|流程|SOP|管道|流水线", "step"),
    (r"分析|研究|评估|审计|评测|评分", "method"),
]
# 原型 → 默认维度（coverage-seeding.md 第二节，宽松兜底）
DEFAULT_DIMS = {
    "method": ["discipline", "method"],          # 方法谋士
    "vertical": ["vertical", "platform", "doc_type", "scenario"],
    "api": ["endpoint", "operation", "error_code"],
    "diagnose": ["symptom", "error_family"],
    "workflow": ["step", "scenario"],
    "create": ["genre", "tone", "form", "provider"],
    "analyze": ["method", "dataset", "source"],
    "meta": ["skill_aspect", "meta_concept"],
    "deploy": ["platform", "scenario"],
    "fallback": ["task_type", "domain"],
}


def read_description(skill_dir):
    p = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(p):
        return None
    md = open(p, encoding="utf-8").read()
    if not md.startswith("---"):
        return None
    end = md.find("\n---", 3)
    fm = md[3:end] if end != -1 else md[3:]
    m = re.search(r"^description:\s*(.*)$", fm, re.M | re.I)
    if not m:
        return None
    desc = m.group(1).strip()
    if desc.startswith("|"):
        # 多行块：取后续缩进行直到非缩进
        lines = [m.group(1)]
        rest = fm.splitlines()[fm.splitlines().index(m.group(0)) + 1:]
        for ln in rest:
            if ln.startswith("  "):
                lines.append(ln.strip())
            else:
                break
        desc = " ".join(lines)
    return desc


def pick_dims(desc):
    """按 PATTERN_RULES 提取维度；无命中给宽松兜底（task_type/domain）。"""
    dims = []
    for pat, dim in PATTERN_RULES:
        if re.search(pat, desc) and dim not in dims:
            dims.append(dim)
    if not dims:
        dims = list(DEFAULT_DIMS["fallback"])
    return dims


def extract_values(desc, dim):
    """尽力从 description 提取候选值（M 级：简单模式，失败留占位）。"""
    if dim == "platform":
        m = re.search(r"支持\s*([^，。；]+?)(?:平台|格式)", desc)
    elif dim == "scenario":
        m = re.search(r"(?:用于|适用)\s*([^，。；]+?)(?:场景|任务)", desc)
    elif dim == "genre":
        m = re.search(r"生成\s*([^，。；]+?)(?:风格|类型)", desc)
    else:
        m = None
    if not m:
        return None
    vals = [v.strip() for v in re.split(r"[、,，/]", m.group(1)) if v.strip()][:6]
    return vals or None


def render_coverage(skill_dir, dims):
    slug = os.path.basename(skill_dir.rstrip("/\\"))
    desc = read_description(skill_dir) or ""
    lines = [
        "# 覆盖维度表 / Coverage Taxonomy",
        "",
        f"> 本技能按以下维度组织覆盖。维度值由锻造炉自动播种（coverage_seed.py）+ 创作者补充。",
        "> 缺口信号参照此表判断 in_taxonomy。",
        "",
    ]
    for dim in dims:
        vals = extract_values(desc, dim)
        lines.append(f"## dimension: {dim}")
        if vals:
            lines.append(" · ".join(vals))
        else:
            lines.append(f"（待创作者补充 {dim} 候选值，用 · 分隔）")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(prog="coverage_seed.py",
                                 description="coverage.md 自动播种器（从 SKILL.md description 解析自声明范围，预填覆盖维度骨架）")
    ap.add_argument("skill_dir", help="目标技能目录（含 SKILL.md）")
    ap.add_argument("--force", action="store_true", help="强制重新播种（覆盖已有 coverage.md）")
    ap.add_argument("--dry", action="store_true", help="只打印将生成的维度，不写文件")
    args = ap.parse_args()

    skill_dir = os.path.abspath(args.skill_dir)
    if not os.path.isdir(skill_dir) or not os.path.exists(os.path.join(skill_dir, "SKILL.md")):
        print(f"✗ 目标不是技能目录（缺 SKILL.md）: {skill_dir}")
        return 2
    desc = read_description(skill_dir)
    if desc is None:
        print(f"✗ SKILL.md 无 description frontmatter，无法播种")
        return 2

    dims = pick_dims(desc)
    print(f"== 覆盖播种 {os.path.basename(skill_dir)} ==")
    print(f"  维度: {', '.join(dims)}")
    if args.dry:
        print("  (dry-run，未写文件)")
        return 0

    dst = os.path.join(skill_dir, "references", "coverage.md")
    if os.path.exists(dst) and not args.force:
        print(f"  - 已存在（跳过，--force 可重播种）: references/coverage.md")
        return 0
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as f:
        f.write(render_coverage(skill_dir, dims))
    print(f"  ✓ 已生成骨架: references/coverage.md（请创作者确认/补充候选值后定稿）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
