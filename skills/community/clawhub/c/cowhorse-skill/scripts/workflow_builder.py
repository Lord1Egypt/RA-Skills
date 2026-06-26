#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workflow Builder Helper Script
Aids in the iterative workflow refinement process.

Usage:
    python workflow_builder.py --step discovery|confirm|build|present
    python workflow_builder.py --prompt "用户描述的工作流"
"""

import argparse
import json
import os
import sys
from datetime import datetime


def discovery_prompt(user_input):
    """Generate discovery questions based on user input"""
    print("=" * 60)
    print("【Step 1: 需求挖掘 — 主动提问，逐一确认】")
    print("=" * 60)
    print(f"用户描述: {user_input}")
    print()
    print("请依次询问以下问题（不要批量提问）：")
    print()
    print("【1.1 目标澄清】")
    print("  - 您最终要交付什么结果？")
    print("  - '完成'的定义是什么？怎么算做好了？")
    print("  - 这个工作流解决的核心问题是什么？")
    print()
    print("【1.2 输入规格】(7个维度，逐个问)")
    print("  - 数据来源：文件/API/数据库/手动输入？")
    print("  - 文件格式：.xlsx/.csv/.json/.txt？")
    print("  - 文件位置：本地路径/网盘/飞书文档？")
    print("  - 数据结构：有哪些列/字段？有表头吗？")
    print("  - 数据量：大概多少条/多少文件？")
    print("  - 数据质量：有脏数据吗？缺失值怎么处理？")
    print("  - 输入参数：需要什么筛选条件/阈值/范围？")
    print("  【追问】如果用户说'一个Excel'，必须问：")
    print("    → 有哪些sheet？表头是什么？合并单元格？多少行？")
    print()
    print("【1.3 输出规格】(6个维度，逐个问)")
    print("  - 产出形式：文件/报表/图表/动作？")
    print("  - 输出格式：.xlsx/.pdf/.html/控制台？")
    print("  - 输出位置：本地/飞书/邮件？")
    print("  - 输出内容：包含哪些字段/信息？")
    print("  - 排序/筛选/统计：按什么排？过滤条件？求和/平均？")
    print("  - 格式要求：有模板吗？需要特定排版/颜色？")
    print("  【追问】如果用户说'生成报表'，必须问：")
    print("    → 具体字段？排序？筛选？统计计算？")
    print()
    print("【1.4 流程步骤】")
    print("  - 整个流程分几步？每步做什么？")
    print("  - 哪些手动？哪些自动化？顺序能变吗？")
    print()
    print("【1.5 约束条件】")
    print("  - 时间要求？技术限制？业务规则？性能要求？")
    print()
    print("【核心原则】不假设，不猜测，不确定就问！")
    print("【处理输入】接受拼写错误，允许模糊匹配，不确定时确认")


def confirmation_summary(data):
    """Generate a structured confirmation summary with input/output specs"""
    print("=" * 60)
    print("【Step 2: 需求确认 — 结构化总结】")
    print("=" * 60)
    print()
    print("## 工作流需求确认")
    print()
    print("### 目标")
    print(data.get("goal", "[待填写]"))
    print()
    print("### 输入规格")
    input_spec = data.get("input_spec", {})
    print(f"| 项目 | 详情 |")
    print(f"|------|------|")
    for key, label in [
        ("source", "数据来源"), ("format", "文件格式"), ("location", "文件位置"),
        ("structure", "数据结构"), ("volume", "数据量"), ("quality", "脏数据处理"),
        ("params", "输入参数")
    ]:
        val = input_spec.get(key, "[待填写]")
        print(f"| {label} | {val} |")
    print()
    print("### 输出规格")
    output_spec = data.get("output_spec", {})
    print(f"| 项目 | 详情 |")
    print(f"|------|------|")
    for key, label in [
        ("form", "产出形式"), ("format", "输出格式"), ("location", "输出位置"),
        ("content", "输出内容"), ("sort_filter", "排序/筛选"), ("stats", "统计计算"),
        ("style", "格式要求")
    ]:
        val = output_spec.get(key, "[待填写]")
        print(f"| {label} | {val} |")
    print()
    print("### 流程步骤")
    steps = data.get("steps", [])
    if steps:
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
    else:
        print("1. [待填写]")
    print()
    print("### 约束条件")
    constraints = data.get("constraints", [])
    if constraints:
        for c in constraints:
            print(f"- {c}")
    else:
        print("- [待填写]")
    print()
    print("### 确认问题")
    print("1. 以上输入/输出规格是否正确？")
    print("2. 步骤顺序和依赖关系对吗？")
    print("3. 哪些步骤需要自动化，哪些保留手动？")
    print("4. 有遗漏的字段或规则吗？")
    print()
    print("等待用户确认...")


def build_skill_skeleton(skill_name, data):
    """Generate a skeleton for the new skill"""
    print("=" * 60)
    print("【Step 3: 构建Skill】")
    print("=" * 60)
    print()
    print(f"Skill名称: {skill_name}")
    print()
    print("建议结构：")
    print(f"  {skill_name}/")
    print("  ├── SKILL.md")
    print("  ├── scripts/")
    print("  │   └── main.py  # 主脚本")
    print("  ├── references/")
    print("  │   └── workflow_guide.md")
    print("  └── assets/")
    print("      └── (模板文件等)")
    print()
    print("创建命令：")
    print(f"  cd ~/.npm-global/lib/node_modules/openclaw/skills/skill-creator")
    print(f"  python3 scripts/init_skill.py <skill-name> --path /home/spark/.openclaw/workspace/skills --resources scripts,references")
    print()
    print("完成后编辑 SKILL.md，填写：")
    print("  - name: skill名称")
    print("  - description: 触发条件和使用场景")
    print("  - 工作流步骤")
    print("  - 资源引用")


def main():
    parser = argparse.ArgumentParser(description="Workflow Builder Helper")
    parser.add_argument("--step", choices=["discovery", "confirm", "build", "present"],
                        help="Which step to execute")
    parser.add_argument("--prompt", help="User input prompt for discovery")
    parser.add_argument("--data", help="JSON data for confirmation/build")
    parser.add_argument("--skill-name", help="Name for new skill")
    args = parser.parse_args()

    if args.step == "discovery":
        if not args.prompt:
            print("Error: --prompt required for discovery step")
            sys.exit(1)
        discovery_prompt(args.prompt)

    elif args.step == "confirm":
        if not args.data:
            print("Error: --data (JSON) required for confirm step")
            sys.exit(1)
        data = json.loads(args.data)
        confirmation_summary(data)

    elif args.step == "build":
        if not args.skill_name:
            print("Error: --skill-name required for build step")
            sys.exit(1)
        data = json.loads(args.data) if args.data else {}
        build_skill_skeleton(args.skill_name, data)

    elif args.step == "present":
        print("【Step 4: 呈现确认】")
        print("1. 展示skill结构")
        print("2. 展示SKILL.md关键内容")
        print("3. 测试运行（如可能）")
        print("4. 询问用户反馈")
        print("5. 迭代修改")


if __name__ == "__main__":
    main()
