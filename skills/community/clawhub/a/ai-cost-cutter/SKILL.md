---
name: ai-cost-cutter
display_name: AI 省钱跑批（AI Cost Cutter）
display_name_en: "AI Cost Cutter"
description: "当用户说『API账单太贵』『token烧太快』『能不能用本地模型』『批处理怎么省钱』『离线跑AI』，或要把大模型调用从烧钱变省钱时使用。四把刀降本：批处理（高峰调度/合并请求）、本地模型回退（贱活本地跑、贵活才上云）、缓存层（相同请求不重复花钱）、模型路由分级（按任务难度选便宜/贵模型）。附可运行成本估算脚本，输入任务量+模型单价即输出月度账单与三档降本方案的差额。触发词：AI省钱、降本、token太贵、本地模型、批处理、离线跑AI、模型路由、缓存层、cost cutter、AI成本、API账单。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Edit
category: AI工程方法
platforms: [windows, macos, linux]
read_when:
  - 月 API 账单过高，想系统性降本
  - 要决定哪些任务上云大模型、哪些用本地小模型
  - 有大量重复/可批处理的 AI 任务（摘要、分类、抽取、翻译）
  - 想搭建缓存层避免重复花钱
  - 用户说「能不能用便宜模型」「离线也能跑吧」
tags: [AI降本, 本地模型, 批处理, 模型路由, 缓存, 离线跑批, 成本估算]
slug: ai-cost-cutter
title: AI 省钱跑批（AI Cost Cutter）
copyright: SynomosAI
description_zh: "当用户说『API账单太贵』『token烧太快』『能不能用本地模型』『批处理怎么省钱』『离线跑AI』，或要把大模型调用从烧钱变省钱时使用。四把刀降本：批处理（高峰调度/合并请求）、本地模型回退（贱活本地跑、贵活才上云）、缓存层（相同请求不重复花钱）、模型路由分级（按任务难度选便宜/贵模型）。附可运行成本估算脚本，输入任务量+模型单价即输出月度账单与三档降本方案的差额。"
description_en: "Four levers to cut LLM spend: batching with off-peak scheduling, local-model fallback, caching, and prompt/output slimming, with a decision table for when cloud is worth it."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/cost_estimator.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: calls
    type: int
    description: 月调用次数
    required: true
  - name: avg-in
    type: int
    description: 平均输入 token，默认800
    required: false
  - name: avg-out
    type: int
    description: 平均输出 token，默认400
    required: false
  - name: price-flagship
    type: float
    description: 旗舰 $/1K tok
    required: false
  - name: price-mid
    type: float
    description: 中档 $/1K tok
    required: false
  - name: price-local
    type: float
    description: 本地 $/1K tok
    required: false
  - name: cheap-frac
    type: float
    description: 贱活占比
    required: false
  - name: local-frac
    type: float
    description: 本地回退占比
    required: false
output_schema:
  stdout: 分模型月成本对比与优化建议
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - cost_estimation
  - llm_budget
  - optimization
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
The user says API bills are too high, tokens burn too fast, or asks how to cut LLM costs. Scenarios: batch-merging large request volumes; evaluating local-model fallback to save compute; routing tasks to cheaper/pricier models by difficulty; or moving AI workloads to offline batch mode.

### Usage
Run `cost_estimator.py` for real-time cost estimation and plan generation. Inputs: expected task volume (`task_volume`) and per-model unit price (`model_price`). The script outputs a monthly bill delta across the four levers (batching, cache, routing, local fallback).

### Flow
1. Detect trigger keywords; confirm cost-optimization intent.
2. Activate the skill; load `cost_estimator.py`.
3. Collect task volume and unit-price params.
4. Run the estimator; produce a current-vs-optimized bill comparison.
5. Output the recommended cut plan with executable local/cache actions.

### Evidence & safety
- Evidence: TBD. Version: 1.1.1. Security: no independent scan (TBD).

## 中文

### 何时用
当用户表达 API 账单成本过高、Token 消耗过快或明确询问如何降低大模型调用费用时。适用于涉及大规模请求批量合并处理、评估本地模型回退策略以节省计算开销的场景。在需要对比不同任务难度的模型路由分级方案，或计划将 AI 部署转为离线跑批模式进行优化时使用。

### 用法
调用技能核心脚本 `cost_estimator.py` 执行实时成本估算与方案生成。参数输入需包含预期任务总量（task_volume）及目标模型的单价（model_price）。通过该能力可直接读取基于四把降本策略（批处理、缓存层、模型路由、本地回退）计算出的月度账单差额报告。

### 流程
1. 检测用户指令中的触发关键词，确认降本或成本优化需求。
2. 激活技能并加载 `cost_estimator.py` 脚本环境。
3. 收集用户指定的任务量与模型单价参数数据。
4. 运行估算算法生成包含当前账单与优化后账单的对比报表。
5. 输出最终降本方案建议，包括可执行的本地部署或缓存策略指示。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
