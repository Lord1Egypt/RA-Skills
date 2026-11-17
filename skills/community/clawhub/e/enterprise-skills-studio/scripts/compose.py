#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能编排器生成器（厚技能化，纯标准库）。

读入一份工作流 spec（JSON），生成"薄编排器技能"的 SKILL.md 骨架：
  - 声明式 steps（原子技能 + 顺序/并行/条件/人工门/降级）
  - 业务逻辑全在原子技能，编排器只描述控制流

用法：
  python compose.py --spec workflow.json [--out orchestrator/SKILL.md] [--md]
  python compose.py --spec workflow.json --json        # 仅输出结构化 spec 回显
  echo '<json>' | python compose.py --spec -            # 从 stdin 读

spec 示例：
{
  "name": "order-fulfill",
  "description": "当用户要完成订单履约（询价→库存→支付→通知）时使用。",
  "owner": "订单平台组",
  "steps": [
    {"skill": "quote-price", "type": "atomic"},
    {"skill": "check-inventory", "type": "atomic"},
    {"skill": "charge-payment", "type": "atomic", "human_gate": true},
    {"skill": "notify-customer", "type": "atomic", "on_fail": "fallback-notify"}
  ]
}
"""
import argparse
import json
import sys


def render_spec(spec):
    name = spec.get("name", "untitled-orchestrator")
    desc = spec.get("description", "（待补充：端到端目标）")
    owner = spec.get("owner", "（待补 owner）")
    steps = spec.get("steps", [])
    lines = [
        "---",
        f"name: {name}",
        f"description: {desc}",
        "agent_created: true",
        "---",
        "",
        f"# {name}（编排器）",
        "",
        "> 薄编排器：只描述控制流；业务逻辑全在各原子技能内。详见 `references/composer.md`。",
        "",
        f"> **维护者 / owner**：{owner}",
        "",
        "## 工作流步骤",
        "",
        "| # | 调用技能 | 类型 | 人工门 | 失败兜底 |",
        "|---|----------|------|--------|----------|",
    ]
    for i, st in enumerate(steps, 1):
        sk = st.get("skill", "?")
        typ = st.get("type", "atomic")
        gate = "✅" if st.get("human_gate") else "—"
        fb = st.get("on_fail", "—")
        lines.append(f"| {i} | {sk} | {typ} | {gate} | {fb} |")
    lines += ["", "## 编排规则", ""]
    prev = None
    for st in steps:
        sk = st.get("skill", "?")
        typ = st.get("type", "atomic")
        branch = st.get("if")
        if typ == "parallel":
            lines.append(f"- **并行**：{sk} 与前步并发，结果汇聚后继续。")
        elif branch:
            lines.append(f"- **条件**：当 {branch} 时调用 {sk}。")
        else:
            lines.append(f"- 顺序调用 `{sk}`" + ("，**写动作前需人工确认**。" if st.get("human_gate") else "。"))
        if st.get("on_fail"):
            lines.append(f"  - 失败兜底：转 `{st['on_fail']}`（或告警/回滚）。")
        prev = sk
    lines += [
        "",
        "## 控制流要点",
        "- 编排器保持薄：不含业务细节，只调度原子技能。",
        "- 跨技能传递数据需有 schema 约束（见 process-systems 强 schema）。",
        "- 端到端使用统一 trace id 贯穿各步（见 agentic-governance 可观测）。",
        "- 任意步失败：按上表兜底，不可逆步骤前必须 human gate。",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="技能编排器生成器")
    ap.add_argument("--spec", required=True, help="工作流 spec JSON（文件路径，或 '-' 读 stdin）")
    ap.add_argument("--out", help="输出到文件（默认 stdout）")
    ap.add_argument("--md", action="store_true", help="同 stdout（markdown 骨架）")
    ap.add_argument("--json", action="store_true", help="回显结构化 spec（不生成 SKILL.md）")
    args = ap.parse_args()

    try:
        if args.spec == "-":
            raw = sys.stdin.read()
        else:
            with open(args.spec, "r", encoding="utf-8") as f:
                raw = f.read()
        spec = json.loads(raw)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(spec, ensure_ascii=False, indent=2))
        return 0

    out = render_spec(spec)
    if args.out:
        import os
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"已生成编排器: {args.out}")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
