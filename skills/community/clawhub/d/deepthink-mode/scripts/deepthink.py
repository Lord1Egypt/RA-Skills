#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepThink — 深度思考工作流
模拟 Claude Extended Thinking 模式：先分析→再规划→后执行→最后审查。
对复杂任务输出完整思维链，帮助做更好的决策。
"""
import sys
import io
import json
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ── 思考模板 ──────────────────────────────────

ANALYZE_TEMPLATE = """## 🧠 深度分析

### 1️⃣ 问题定义
- **核心问题**: {question}
- **问题类型**: {qtype}
- **紧急程度**: {urgency}
- **影响范围**: {scope}

### 2️⃣ 约束与前提
- **已知条件**: {known}
- **未知因素**: {unknown}
- **硬约束**: {constraints}
- **风险点**: {risks}

### 3️⃣ 多角度分析
{perspectives}

### 4️⃣ 关键洞察
{insights}"""

PLAN_TEMPLATE = """## 📋 执行计划

### 策略选择
{strategy}

### 执行步骤
{steps}

### 预期结果
{expected}

### 备选方案
{alternatives}

### 检查点
{checkpoints}"""

REVIEW_TEMPLATE = """## ✅ 结果审查

### 是否符合预期
{met_expectations}

### 是否有遗漏
{gaps}

### 学到了什么
{learnings}

### 下次改进
{improvements}"""


def generate_analysis(question, qtype="通用", urgency="中",
                      scope="局部", known="", unknown="",
                      constraints="", risks="",
                      perspectives="", insights=""):
    """生成分析框架"""
    if not perspectives:
        perspectives = "\n".join([
            "  • **技术角度**: 待分析",
            "  • **用户角度**: 待分析",
            "  • **风险角度**: 待分析",
        ])
    if not insights:
        insights = "待分析后补充"

    return ANALYZE_TEMPLATE.format(
        question=question, qtype=qtype, urgency=urgency,
        scope=scope, known=known, unknown=unknown,
        constraints=constraints, risks=risks,
        perspectives=perspectives, insights=insights
    )


def generate_plan(strategy="", steps="", expected="",
                  alternatives="", checkpoints=""):
    """生成执行计划"""
    if not strategy:
        strategy = "待确定"
    if not steps:
        steps = "1. \n2. \n3. "
    if not expected:
        expected = "待评估"
    if not alternatives:
        alternatives = "暂无"
    if not checkpoints:
        checkpoints = "待确定"

    return PLAN_TEMPLATE.format(
        strategy=strategy, steps=steps,
        expected=expected, alternatives=alternatives,
        checkpoints=checkpoints
    )


def generate_review(met_expectations="待审查", gaps="待审查",
                    learnings="待补充", improvements="待补充"):
    """生成审查报告"""
    return REVIEW_TEMPLATE.format(
        met_expectations=met_expectations,
        gaps=gaps, learnings=learnings,
        improvements=improvements
    )


def full_think(question, **kwargs):
    """完整深度思考链"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    output = []
    output.append(f"# 🤔 深度思考链")
    output.append(f"*生成时间: {timestamp}*\n")
    output.append("---\n")
    output.append(generate_analysis(question, **kwargs))
    output.append("\n---\n")
    output.append(generate_plan(**{
        k.replace('plan_', ''): v
        for k, v in kwargs.items() if k.startswith('plan_')
    }))

    return "\n".join(output)


def main():
    if len(sys.argv) < 3:
        print("DeepThink — 深度思考工作流")
        print()
        print("用法:")
        print("  python deepthink.py analyze \"问题描述\"")
        print("  python deepthink.py plan \"方案名称\"")
        print("  python deepthink.py review")
        print("  python deepthink.py full \"复杂问题\"")
        print()
        print("示例:")
        print('  python deepthink.py full "如何设计一个高可用API网关"')
        sys.exit(1)

    mode = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else ""

    if mode == 'analyze':
        print(generate_analysis(question))
    elif mode == 'plan':
        print(generate_plan(strategy=question))
    elif mode == 'review':
        print(generate_review())
    elif mode == 'full':
        print(full_think(question))
    else:
        print(f"未知模式: {mode}")
        sys.exit(1)


if __name__ == '__main__':
    main()
