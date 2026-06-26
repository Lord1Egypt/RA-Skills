---
slug: expense-categorization-optimizer
version: "1.1.0"
tags: expense-tracking, budget-categorization, financial-planning, spending-analysis, personal-finance
type: descriptive
language: en
---

# Expense Categorization Optimizer

## Overview

Optimizes expense categorization rules and suggests improvements for better financial tracking. This is a descriptive skill that provides templates, frameworks, and heuristic analysis without executing real code, accessing external APIs, or performing actual financial transactions.

## Trigger

Use this skill when the user wants to:
- get structured guidance on expense categorization optimizer
- apply best-practice frameworks to their financial situation
- generate templates and checklists for financial planning

### Example prompts
- "Help me create a personal budget"
- "Analyze my cash flow forecast"
- "Check my expense categorization"
- "Assess my financial health"
- "Review my receivables aging"
- "Check invoice compliance"
- "Develop a pricing strategy"
- "Find cost reduction opportunities"
- "Optimize my tax deductions"
- "Interpret my financial reports"

## Workflow

1. User provides context and goals.
2. Skill applies built-in templates and frameworks.
3. Skill generates structured output with recommendations.
4. User receives actionable insights and next steps.

## Inputs
- User context (financial situation, goals, constraints)
- Optional data inputs (amounts, categories, timeframes)
- Analysis preferences

## Outputs
- Structured analysis report
- Templates and frameworks
- Actionable recommendations
- Next steps checklist

## Usage Scenarios

### Scenario 1

**User input:** "My expense categories are a mess — 'Misc' is 40% of spending. Help me redesign them."

**Expected output:** Tax-aware category hierarchy with 12-15 categories mapped to IRS Schedule A/C logic, subcategory suggestions, and a 3-month transition plan with 'reclassify Misc' checklist.

### Scenario 2

**User input:** "I want categories optimized for both budgeting and tax deduction tracking as a freelancer."

**Expected output:** Dual-purpose category system — core living categories + freelancer-specific categories (home office, equipment, software, travel, meals, professional development) — with deduction-flag rules and quarterly review checklist.

### Scenario 3

**User input:** "Design a shared expense category system for a couple with joint and separate finances."

**Expected output:** Three-tier system: joint-mandatory (housing, utilities, groceries), joint-discretionary (dining, travel), and individual (personal care, hobbies) — with split rules and monthly reconciliation process.
### Scenario 4: 微信支付宝账单太乱了
**User input:** "我每个月微信和支付宝的消费记录混在一起，分不清哪些是生活必需哪些是乱花的，帮我分类一下。"
**Expected output:** 对交易记录进行智能分类：餐饮美食、交通出行、生活缴费、购物消费、娱乐休闲、医疗健康、教育学习等。分析每类占比是否符合健康结构（住房不超过30%、餐饮15-20%、娱乐<10%等）。标记出高频低额的非必要消费（如每天一杯奶茶≈月均450元），给出优化建议：设定每月非必要消费上限、使用记账App自动分类（如随手记/圈子记账）。

## Safety
- No real financial transactions or API calls
- No access to real bank accounts or financial systems
- Recommendations are informational only
- Users should consult financial professionals for actual decisions

## Acceptance Criteria
- Must return structured markdown/JSON output
- Must include actionable recommendations
- Must clearly state the descriptive/non-executable nature
- Must provide templates or frameworks for user adaptation
