#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业技能体系成熟度自测器（Enterprise Skills Maturity Assessor）

对组织在"企业技能体系"上的成熟度做量化自测，输出：
  - 综合成熟度等级（L0–L4）
  - 各维度分项得分（含可选的 Agentic 维度）
  - 最短板维度与下一步建议

维度（与 references/planning.md / references/agentic-governance.md 对齐）：
  governance 治理（注册表/四前提）
  capability 技能能力（厚技能/复用度）
  adoption   采用规模（技能数/使用者）
  security   安全（审查/最小权限/审计）
  evolution  持续进化（度量/迭代闭环）
  agentic   【可选】Agentic AI 成熟度（评测/护栏/可观测/人机协同）

打分：每个维度 0–4（0=无，4=成熟）。agentic 为可选维度——不传则自动忽略，
其余五维权重归一化，保证向后兼容。可经 JSON 文件传入或交互输入。

纯标准库实现，无外部依赖；可在任意装了 Python 的环境运行。

用法：
  python maturity_assess.py --answers answers.json
  python maturity_assess.py                      # 交互式逐维度打分
  python maturity_assess.py --answers answers.json --json
  python maturity_assess.py --answers answers.json --md
"""
import argparse
import json
import sys

# 维度定义：权重 + 说明 + 该维度的"成熟度锚点"
DIMENSIONS = {
    "governance": {
        "label": "治理（注册表/四前提）",
        "weight": 0.25,
        "anchors": [
            "无注册表、无作用域隔离",
            "有初步注册表，四前提部分满足",
            "注册表+四前提齐全，集中管理",
            "治理自动化（intake 审批+版本 pin）",
            "治理融入 CI/CD 与 SIEM，持续可审计",
        ],
    },
    "capability": {
        "label": "技能能力（厚技能/复用度）",
        "weight": 0.20,
        "anchors": [
            "全是个人的薄 prompt，无复用",
            "少量脚本化技能，复用有限",
            "模板化+脚本，可跨人复用",
            "厚技能库+共享模板，复用率高",
            "能力市场化，业务自助组合编排",
        ],
    },
    "adoption": {
        "label": "采用规模（技能数/使用者）",
        "weight": 0.15,
        "anchors": [
            "0–2 个试点，单人或小组",
            "3–5 试点，1 个团队",
            "多团队使用，≥10 技能",
            "跨部门规模采用，≥30 技能",
            "组织级默认工作方式",
        ],
    },
    "security": {
        "label": "安全（审查/最小权限/审计）",
        "weight": 0.20,
        "anchors": [
            "无安全审查",
            "发布前人工过 8 项清单",
            "自动化审查+最小权限+审计日志",
            "CISO 5/AST10 映射+职责分离",
            "安全左移+月度证据复审+演练",
        ],
    },
    "evolution": {
        "label": "持续进化（度量/迭代闭环）",
        "weight": 0.20,
        "anchors": [
            "无度量无迭代",
            "有 Evolution Log，月度人工复盘",
            "周期重评+ROI 度量",
            "会话挖掘自动建议迭代",
            "度量驱动的自愈式进化闭环",
        ],
    },
    "agentic": {
        "label": "Agentic 成熟度（评测/护栏/可观测/人机协同）",
        "weight": 0.18,
        "anchors": [
            "无 Agentic，全单轮问答",
            "少量脚本化 Agent，无评测/无护栏",
            "关键 Agent 有评测+人工确认门+基础日志",
            "评测自动化+护栏体系+可观测+职责分离",
            "评估/护栏/可观测/责任闭环，事故自愈式复盘",
        ],
    },
}

LEVELS = [
    (0.8, "L0", "未启动", "先立项 sponsor，做 2–5 个试点，引入模板与基础注册表。"),
    (1.6, "L1", "试点探索", "固化模板，建立注册表与四前提自检，准备标准化。"),
    (2.4, "L2", "标准化", "启用安全审查与分发机制，向多团队推广。"),
    (3.2, "L3", "规模化", "建度量体系与持续进化闭环，控技能蔓延。"),
    (4.01, "L4", "嵌入式", "技能融入业务 SOP，治理与业务系统深度耦合并闭环。"),
]


def level_for(score):
    for threshold, code, name, _ in LEVELS:
        if score < threshold:
            return code, name
    return "L4", "嵌入式"


def assess(scores):
    # 只评估调用方实际传入的维度（agentic 可选），并对这些维度归一化权重，
    # 保证旧版只传 5 维时得分不变（向后兼容）。
    present = {k: d for k, d in DIMENSIONS.items() if k in scores}
    wsum = sum(d["weight"] for d in present.values()) or 1.0
    total = 0.0
    for k, d in present.items():
        s = scores.get(k, 0)
        s = max(0, min(4, int(s)))
        total += s * (d["weight"] / wsum)
    code, name = level_for(total)
    weakest = min(present.keys(), key=lambda k: scores.get(k, 0))
    return total, code, name, weakest


def render_text(scores, total, code, name, weakest, md=False):
    if md:
        out = ["# 企业技能体系成熟度自测", ""]
        out.append(f"**综合等级**: {code} {name} · **得分**: {total:.2f}/4.00")
        out.append("")
        out.append("| 维度 | 得分 | 现状锚点 |")
        out.append("|------|------|----------|")
        for k, d in DIMENSIONS.items():
            s = scores.get(k, 0)
            out.append(f"| {d['label']} | {s}/4 | {d['anchors'][s]} |")
        out.append("")
        out.append(f"**最短板**: {DIMENSIONS[weakest]['label']} → {DIMENSIONS[weakest]['anchors'][scores.get(weakest,0)]}")
        out.append("")
        out.append(f"**下一步**: {next((r for t,c,n,r in LEVELS if c==code), LEVELS[-1][3])}")
        return "\n".join(out)

    lines = []
    lines.append("企业技能体系成熟度自测")
    lines.append("=" * 50)
    lines.append(f"综合等级: {code} {name}   得分: {total:.2f}/4.00")
    lines.append("=" * 50)
    for k, d in DIMENSIONS.items():
        s = scores.get(k, 0)
        lines.append(f"  [{k:11s}] {s}/4  {d['label']}")
        lines.append(f"             现状: {d['anchors'][s]}")
    lines.append("-" * 50)
    lines.append(f"最短板: {DIMENSIONS[weakest]['label']}")
    lines.append(f"        {DIMENSIONS[weakest]['anchors'][scores.get(weakest, 0)]}")
    lines.append("")
    rec = next((r for t, c, n, r in LEVELS if c == code), LEVELS[-1][3])
    lines.append(f"下一步建议: {rec}")
    return "\n".join(lines)


def load_answers(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 只取文件里实际提供的维度（agentic 可选）；缺失维度不计入，保证旧 5 维输入得分不变
    return {k: int(v) for k, v in data.items() if k in DIMENSIONS}


def interactive():
    print("请为每个维度打 0–4 分（0=无，4=成熟）：")
    scores = {}
    for k, d in DIMENSIONS.items():
        while True:
            try:
                v = input(f"  {d['label']} ({k}) [0-4]: ").strip()
                v = int(v)
                if 0 <= v <= 4:
                    scores[k] = v
                    break
                print("    请输入 0–4 的整数。")
            except EOFError:
                scores[k] = 0
                break
            except ValueError:
                print("    请输入数字。")
    return scores


def main():
    ap = argparse.ArgumentParser(description="企业技能体系成熟度自测器")
    ap.add_argument("--answers", help="JSON 文件：各维度 0–4 分，如 {\"governance\":3,...}")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--md", action="store_true", help="输出 Markdown")
    args = ap.parse_args()

    if args.answers:
        try:
            scores = load_answers(args.answers)
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"错误: {e}", file=sys.stderr)
            return 2
    else:
        scores = interactive()

    total, code, name, weakest = assess(scores)

    if args.json:
        print(json.dumps({
            "score": round(total, 2),
            "level": code,
            "level_name": name,
            "dimensions": {k: scores.get(k, 0) for k in DIMENSIONS},
            "weakest": weakest,
            "recommendation": next((r for t, c, n, r in LEVELS if c == code), LEVELS[-1][3]),
        }, ensure_ascii=False, indent=2))
    elif args.md:
        print(render_text(scores, total, code, name, weakest, md=True))
    else:
        print(render_text(scores, total, code, name, weakest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
