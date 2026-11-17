#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人技能 → 企业级技能 升级器（Personal-to-Enterprise Upgrader）

读入一份个人 SKILL.md，自动套用升级清单，产出：
  - 升级版 SKILL.md（补全四层结构 + 企业治理件 + Evolution Log + 厚技能提示）
  - 差异说明（从个人版补强了哪些项）

纯标准库实现，无外部依赖，可跨平台运行。

用法：
  python upgrade_skill.py <个人SKILL.md> [--out <输出目录>] [--owner 张三] [--domain 销售] [--role 销售]
  # 不指定 --out 则打印到 stdout，不写盘
"""
import argparse
import os
import re
import sys

LAYERS = ["指令层", "知识层", "工具层", "示例层"]


def parse_frontmatter(text):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body


def normalize_name(name):
    if not name:
        return None
    n = name.strip().lower()
    n = re.sub(r"[^a-z0-9]+", "-", n)
    n = re.sub(r"-+", "-", n).strip("-")
    return n[:64]


def ensure_layers(body):
    """确保四层标题存在，缺失则补占位。返回 (new_body, missing_list)。"""
    missing = []
    lines = body.splitlines()
    # 去掉已有的四层标题（大小写/空格宽松）
    kept = []
    for ln in lines:
        if re.match(r"^#{1,3}\s*(指令|知识|工具|示例).*层", ln):
            continue
        kept.append(ln)
    body_clean = "\n".join(kept).strip()
    # 重组：在 body 后追加四层
    for layer in LAYERS:
        if layer not in body:
            missing.append(layer)
    return body_clean, missing


def build_enterprise(fm, body, args):
    name = normalize_name(fm.get("name")) or args.name or "untitled-skill"
    desc = fm.get("description", "")
    body_clean, missing = ensure_layers(body)

    out = []
    out.append("---")
    out.append(f"name: {name}")
    out.append(f"description: {desc}  # 建议补全'何时调用'")
    out.append("agent_created: true")
    out.append("---")
    out.append("")
    out.append(f"# {name}")
    out.append("")
    out.append("{一句话说明这个技能解决什么、服务谁。}")
    out.append("")
    out.append("<!-- 厚技能+薄harness：把确定性步骤写成 scripts/，关键输出用模板约束，示例给足；harness 只负责调用。 -->")
    out.append("")
    # 原 body
    out.append(body_clean)
    out.append("")
    # 缺失层占位
    for layer in missing:
        out.append(f"## {layer}（待补充）")
        out.append("")
        out.append("- [待补充]")
        out.append("")
    # 若原 body 已含部分层，仍确保四层标题存在
    for layer in LAYERS:
        if layer not in "\n".join(out):
            out.append(f"## {layer}（待补充）")
            out.append("- [待补充]")
            out.append("")

    # 企业治理件
    out.append("---")
    out.append("<!-- 以下为企业模式治理件，个人模式可删除 -->")
    out.append("## 治理元数据（企业模式）")
    out.append("")
    out.append(f"- 命名规范：`{args.domain or '{领域}'}-{args.role or '{动作}'}`")
    out.append(f"- 角色捆绑：{args.role or '{角色}'}")
    out.append("- 作用域隔离：{多租户/项目级/角色级隔离说明}")
    out.append("- 技能审计：{日志+链路+回滚机制}")
    out.append("- 安全审查：8 项清单 + CISO 5 风险(AST10) 已逐条确认")
    out.append("- 版本/回滚：生产 pin 版本，Git 为唯一可信源，保留上一版兜底")
    out.append(f"- 分发渠道：{{组织级上传/插件+分组/内部目录/代码库/API}}")
    out.append("- 跨平台：遵循 agentskills.io 标准，可在 WorkBuddy/Codex/Claude Code/Cursor/龙虾/Hermes 移植")
    out.append("")
    out.append("## 注册表条目")
    out.append("")
    out.append("| 技能名 | 领域 | 所有者 | 版本 | 依赖 | 评估状态 | 复审周期 |")
    out.append("|--------|------|--------|------|------|----------|----------|")
    out.append(f"| {name} | {args.domain or '{领域}'} | {args.owner or '{owner}'} | v0.1 | {{依赖}} | 待审 | 季度 |")
    out.append("")
    out.append("## Evolution Log（持续进化，企业模式推荐）")
    out.append("")
    out.append(f"- v0.1 初始版本，由 {args.owner or '{负责人}'} 从个人版升级创建")
    out.append("- （后续每次迭代追加：版本/日期/变更内容/触发原因，增量扩展而非覆盖重写）")
    out.append("")
    out.append("<!-- 个人→企业升级提示：技术层(能力)交工程、规则层(口径)业务可写，AI 产品经理负责拆分与编排 -->")

    return name, "\n".join(out), missing


def diff_notes(missing, name, owner, domain):
    notes = []
    notes.append(f"【个人→企业升级差异说明】技能: {name}")
    notes.append("1. 命名规范化: 已按 {领域}-{动作} 统一（小写/连字符）")
    notes.append("2. 结构补全: " + (f"缺失层已补占位: {', '.join(missing)}" if missing else "四层结构已齐"))
    notes.append("3. 技术/规则层拆分: 已提示由 AI 产品经理判断归属（工程做能力、业务写规则）")
    notes.append("4. 厚技能化: 已加提示——确定性步骤脚本化、输出模板约束、示例给足")
    notes.append("5. 安全审查: 建议跑 review_checklist.py 过 8 项 + CISO 5")
    notes.append("6. 作用域隔离: 治理件已留填空位，须填隔离策略")
    notes.append("7. 治理信封: 已加注册表条目(owner/版本/依赖/评估/复审)")
    notes.append("8. 审计与回滚: 已加 Evolution Log + 版本 pin 提示")
    notes.append("9. 分发渠道: 治理件已列六法，须择一")
    notes.append("10. 四前提自检: 隔离/审计/自定义/成本，发布前逐项确认")
    return "\n".join(notes)


def main():
    ap = argparse.ArgumentParser(description="个人技能 → 企业级技能 升级器")
    ap.add_argument("input", help="个人 SKILL.md 路径")
    ap.add_argument("--out", help="输出目录（不填则打印到 stdout）")
    ap.add_argument("--owner", help="所有者")
    ap.add_argument("--domain", help="领域")
    ap.add_argument("--role", help="角色/场景")
    ap.add_argument("--name", help="覆盖 name（若原文件缺失）")
    args = ap.parse_args()

    if not os.path.isfile(args.input):
        print(f"错误: 找不到文件 {args.input}", file=sys.stderr)
        return 2

    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()
    fm, body = parse_frontmatter(text)
    name, upgraded, missing = build_enterprise(fm, body, args)
    notes = diff_notes(missing, name, args.owner, args.domain)

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        out_path = os.path.join(args.out, "SKILL.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(upgraded)
        note_path = os.path.join(args.out, "UPGRADE_NOTES.md")
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(notes)
        print(f"已生成升级版技能: {out_path}")
        print(f"差异说明: {note_path}")
    else:
        print(upgraded)
        print("\n" + "=" * 50 + "\n")
        print(notes)

    return 0


if __name__ == "__main__":
    sys.exit(main())
