---
name: brand-knowledge-base-builder
description: Build a reusable brand knowledge package from uploaded brand documents and/or a filled intake form. Use when the user wants a standardized brand SSOT containing company intro, products/services, target users, selling points, cases, FAQ, contact info, website links, competitors, banned words, and brand tone.
---

# Brand Knowledge Base Builder

## Purpose

Use this skill to turn scattered brand materials into a standardized, reusable brand package that can feed downstream content, sales, support, FAQ, RAG, or Agent workflows.

This skill is for building a **Single Source of Truth**, not for writing one-off marketing copy.

## What It Accepts

Use one or both of these input modes:

1. `Upload raw materials`
   - 官网文案
   - 公司介绍
   - 产品资料
   - 销售话术
   - FAQ 草稿
   - 客户案例
   - 访谈或语音转文字

2. `Fill an intake form`
   - Run the skill in template mode to generate `intake_form.md`, `intake_form.yaml`, or `intake_form.json`
   - Let the user fill key fields first, then append raw materials if needed

## First-Use Requirement

On the **first turn this skill is used**, do not jump straight into extraction.

You must first clearly tell the user:

1. This skill builds a reusable brand SSOT, so the company needs to provide source materials first.
2. The company can provide materials in either of these ways:
   - Upload raw materials directly
   - Fill the intake form first, then optionally append raw materials
3. If the company does not provide enough information, the skill may still generate a draft, but missing fields must be marked as `待确认`, and the analysis report must list follow-up questions.

You must explicitly ask the user to provide the following **minimum required materials**:

- 公司基础信息：品牌名称、公司名称、所属行业、产品类别、一句话定义、100 到 300 字公司简介
- 官网与公开链接：官网首页、产品页、案例页、FAQ 页；如果没有完整官网，至少提供对外介绍页或文档
- 产品与服务说明：卖什么、解决什么问题、怎么交付、如何收费
- 目标客户信息：核心客户、次级客户、决策人、使用者、不适合客户
- 核心卖点：至少 3 条卖点，并尽量附证据、数据、客户反馈或资质依据
- 联系方式：销售邮箱、支持邮箱、电话、微信/社媒、地址、工作时间、预约方式
- 品牌语气与表达规范：语气关键词、必须出现的说法、禁用词、禁用承诺、安全替代表达
- 合规边界：哪些能说、哪些不能说、哪些效果不能承诺、哪些内容必须人工审核

You should then strongly recommend these **additional materials**:

- 客户案例 2 到 5 条：客户类型、原问题、解决方案、结果、证据
- FAQ 种子问题 10 到 20 条：价格、效果、安全、交付周期、合作方式
- 竞品与替代方案：直接竞品、间接竞品、传统做法、外包方案、行业 SaaS
- 销售或客服话术：开场白、异议处理、报价说明、边界说明
- 原始素材：官网文案、宣传册、访谈纪要、录音转文字、产品说明、案例文档

## Required Coverage

The final package should cover:

- 公司简介
- 产品与服务
- 目标客户
- 核心卖点
- 使用场景与客户案例
- FAQ
- 联系方式
- 官网链接
- 竞品与替代方案
- 品牌语气
- 禁用词与禁用承诺
- 合规边界

## Workflow

1. Intake
   - On first use, explicitly tell the user what the company must provide
   - Collect files and/or a filled intake template
   - Prefer mixed mode when the user has partial structure plus raw docs
   - If the user has not prepared enough material, direct them to the intake template instead of proceeding silently

2. Core extraction
   - Produce a canonical JSON package
   - Prioritize factual sections over derivative writing assets

3. Analysis
   - Score completeness
   - Identify missing fields, conflicts, assumptions, and follow-up questions

4. Asset generation
   - Generate FAQ, glossary, standard messaging, and `llms.txt` inputs

5. Export
   - Render the full package into:
     - `brand_knowledge_base.json`
     - `brand_knowledge_base.yaml`
     - `brand_knowledge_base.md`
     - `faq.md`
     - `glossary.md`
     - `standard_messaging.md`
     - `llms.txt`
     - `analysis_report.md`

## Safety Rules

- Do not invent missing facts.
- Use conservative wording.
- Strip or rewrite unverified absolute claims.
- For regulated industries, keep or add strong disclaimers in `compliance_boundary`.
- Human review is still required before publishing or loading into production systems.
- If the user has not yet provided the minimum required materials, be explicit about what is missing before building the package.

## Files To Read

- For intake guidance: `prompts/intake.md`
- For extraction rules: `prompts/extraction.md`
- For analysis rules: `prompts/normalization.md`
- For derivative assets: `prompts/asset_generation.md`
- For schema shape: `templates/brand_knowledge_base.json`

## Runtime Notes

- `main.py` is the executable entrypoint.
- `--generate_intake_template` creates fillable intake files.
- `--input` and `--inputs` accept raw material files.
- `--intake_file` accepts a structured intake form.
- `--render_from_json` re-renders the full artifact set from an existing package JSON.

## First Reply Pattern

When the skill is first invoked, the assistant should lead with a message equivalent to:

`使用本 Skill 前，请先按要求提供品牌资料。至少需要：公司简介、官网链接、产品服务、目标客户、核心卖点、联系方式、品牌语气与禁用词、合规边界。强烈建议同时提供客户案例、FAQ、竞品信息、销售话术和其他原始素材。你可以直接上传资料，或者先填写 intake 表单。若资料不完整，系统会生成初稿，并把缺失项标记为“待确认”。`
