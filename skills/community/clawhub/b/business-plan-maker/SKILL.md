---
name: 商业计划生成器
description: 输入产品/业务描述，自动生成完整的商业计划书（执行摘要、市场分析、竞争定位、收入模型、运营计划、财务预测、风险评估）
version: 1.0.0
author: AI Skill 商业生产
tags: [商业计划, 创业, 融资, 商业计划书, 自由职业]
price: 24.9
---

# 商业计划生成器

## 功能概述

给创业者和自由职业者使用的商业计划书工具。输入你的产品/业务描述，一键生成结构完整的商业计划书。

## 使用方法

```bash
# 使用 AI 生成完整商业计划书
python3 business_plan_maker.py --mode full "我的产品是一款AI驱动的健身App"

# 使用快速模式（模板框架，不调用API）
python3 business_plan_maker.py --mode quick "我的产品是一款AI驱动的健身App"

# 保存到文件
python3 business_plan_maker.py --output business_plan.md "我的产品是一款..."

# 指定语言
python3 business_plan_maker.py --lang en "AI fitness app..."
```

## 环境变量

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `OPENAI_API_KEY` | full模式必填 | OpenAI API 密钥 |
| `OPENAI_MODEL` | 否 | 模型名，默认 gpt-4o-mini |

## 输出章节

- 执行摘要
- 市场分析
- 竞争定位
- 收入模型
- 运营计划
- 财务预测
- 风险评估

## 依赖

```bash
pip install openai
```
