#!/usr/bin/env python3
"""AI PM PRD 模板生成器 — 生成结构化的AI产品需求文档"""

import json
import sys
from datetime import datetime

PRD_TEMPLATE = """# PRD: {product_name}

> 版本: v{version} | 日期: {date} | 作者: {author} | 状态: {status}

---

## 一、背景与目标

### 1.1 业务背景
{background}

### 1.2 产品目标
{goals}

### 1.3 成功指标 (OKR/KPI)
| 指标 | 当前值 | 目标值 | 测量方式 |
|------|--------|--------|---------|
{metrics}

---

## 二、用户分析

### 2.1 目标用户画像
{user_personas}

### 2.2 用户故事
| ID | 作为... | 我想要... | 以便... | 优先级 |
|----|---------|----------|--------|:------:|
{user_stories}

### 2.3 用户旅程
{user_journey}

---

## 三、功能详情

{features}

---

## 四、AI 能力设计

### 4.1 AI 功能概述
{ai_overview}

### 4.2 模型选型
| 功能 | 推荐模型 | 输入Token | 输出Token | 单价 | 预估日成本 |
|------|---------|-----------|-----------|------|-----------|
{model_selection}

### 4.3 Prompt 策略
{prompt_strategy}

### 4.4 降级方案
{fallback_plan}

### 4.5 RAG 方案 (如适用)
{rag_plan}

### 4.6 Agent 工作流 (如适用)
{agent_workflow}

---

## 五、人机协同设计

### 5.1 HITL 检查点
{hitl_checkpoints}

### 5.2 权限与审核流程
{review_flow}

---

## 六、数据闭环

### 6.1 反馈收集
{feedback_collection}

### 6.2 数据飞轮
{data_flywheel}

---

## 七、非功能需求

| 维度 | 要求 |
|------|------|
| 延迟 | {latency} |
| 准确率 | {accuracy} |
| 可用性 | {availability} |
| 安全合规 | {compliance} |

---

## 八、上线计划

### 8.1 灰度策略
{grayscale}

### 8.2 评估方案
{eval_plan}

### 8.3 监控指标
{monitoring}

---

## 九、风险与依赖

| 风险 | 影响 | 概率 | 应对措施 |
|------|------|:----:|---------|
{risks}

---

## 十、验收标准

{acceptance_criteria}

---

## 附录

### A. 竞品参考
{competitors}

### B. 技术依赖
{tech_dependencies}
"""


def generate_prd_template(
    product_name="未命名产品",
    version="1.0",
    author="AI PM",
    status="Draft",
    background="(待填写)",
    goals="(待填写)",
    metrics="| - | - | - | - |",
    user_personas="(待填写)",
    user_stories="| - | - | - | - | - |",
    user_journey="(待填写)",
    features="### 3.1 核心功能\n(待填写)\n\n### 3.2 辅助功能\n(待填写)",
    ai_overview="(待填写)",
    model_selection="| - | - | - | - | - | - |",
    prompt_strategy="(待填写)",
    fallback_plan="(待填写)",
    rag_plan="(待填写 - 如不涉及RAG请删除本节)",
    agent_workflow="(待填写 - 如不涉及Agent请删除本节)",
    hitl_checkpoints="(待填写)",
    review_flow="(待填写)",
    feedback_collection="(待填写)",
    data_flywheel="(待填写)",
    latency="(待填写)",
    accuracy="(待填写)",
    availability="(待填写)",
    compliance="(待填写)",
    grayscale="(待填写)",
    eval_plan="(待填写)",
    monitoring="(待填写)",
    risks="| - | - | - | - |",
    acceptance_criteria="(待填写)",
    competitors="(待填写)",
    tech_dependencies="(待填写)",
):
    """生成 PRD 模板"""
    return PRD_TEMPLATE.format(
        product_name=product_name,
        version=version,
        date=datetime.now().strftime("%Y-%m-%d"),
        author=author,
        status=status,
        background=background,
        goals=goals,
        metrics=metrics,
        user_personas=user_personas,
        user_stories=user_stories,
        user_journey=user_journey,
        features=features,
        ai_overview=ai_overview,
        model_selection=model_selection,
        prompt_strategy=prompt_strategy,
        fallback_plan=fallback_plan,
        rag_plan=rag_plan,
        agent_workflow=agent_workflow,
        hitl_checkpoints=hitl_checkpoints,
        review_flow=review_flow,
        feedback_collection=feedback_collection,
        data_flywheel=data_flywheel,
        latency=latency,
        accuracy=accuracy,
        availability=availability,
        compliance=compliance,
        grayscale=grayscale,
        eval_plan=eval_plan,
        monitoring=monitoring,
        risks=risks,
        acceptance_criteria=acceptance_criteria,
        competitors=competitors,
        tech_dependencies=tech_dependencies,
    )


if __name__ == "__main__":
    args = sys.argv[1:]
    kwargs = {}
    
    if "--json" in args:
        idx = args.index("--json")
        if idx + 1 < len(args):
            with open(args[idx + 1], "r", encoding="utf-8") as f:
                kwargs = json.load(f)
    else:
        kwargs["product_name"] = args[0] if args else "未命名产品"
    
    print(generate_prd_template(**kwargs))
