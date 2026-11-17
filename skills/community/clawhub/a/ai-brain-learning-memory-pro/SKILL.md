---
name: ai-brain-learning-memory-pro
title: AI记忆工程实战版
display_name: AI记忆工程实战版
display_name_en: AI Memory Engineering Pro
description: "ai-brain-learning-memory 的进阶工程版，面向 AI 开发者 / 认知科学爱好者 / agent 架构师。在基础版（概念+例子+速查）之上往工程化推一步：三层记忆的参考实现（Python）、与 agent-memory 工具集成、评测电池 memory_eval_battery.py 的跑法与 6 维解读、OWASP ASI06 记忆投毒防御的代码落地、复习四节点的自动化 rrule 配置、认知科学证据→工程决策映射。建议先读基础版再读本版。触发词：大脑学习记忆进阶、记忆系统实现、memory system design、记忆架构代码、agent-memory 集成、记忆评测电池、记忆投毒防御、ASI06、间隔重复实现、遗忘曲线代码、记忆溯源、reference implementation、学习记忆工程版、brain memory pro。"
description_zh: "ai-brain-learning-memory 的进阶工程版，面向 AI 开发者 / 认知科学爱好者 / agent 架构师。在基础版（概念+例子+速查）之上往工程化推一步：三层记忆的参考实现（Python）、与 agent-memory 工具集成、评测电池 memory_eval_battery.py 的跑法与 6 维解读、OWASP ASI06 记忆投毒防御的代码落地、复习四节点的自动化 rrule 配置、认知科学证据→工程决策映射。建议先读基础版再读本版。触发词：大脑学习记忆进阶、记忆系统实现、memory system design、记忆架构代码、agent-memory 集成、记忆评测电池、记忆投毒防御、ASI06、间隔重复实现、遗忘曲线代码、记忆溯源、reference implementation、学习记忆工程版、brain memory pro。"
description_en: "Advanced engineering version of ai-brain-learning-memory. Aimed at AI developers, cognitive-science enthusiasts, and agent architects. Pushes beyond the basic version (concepts + examples + cheatsheet) into engineering-grade depth: three-tier memory reference implementation (Python), integration with the agent-memory tool, how to run memory_eval_battery.py and interpret its 6 dimensions, code-level defense against OWASP ASI06 memory poisoning, automated rrule config for the four review nodes, and cognitive-science evidence → engineering decision mapping. Recommend reading the basic version first."
version: 1.0.1
agent_created: true
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch, WebSearch, Task
category: AI学习方法论
platforms: [windows, macos, linux]
read_when:
  - 要把「学习记忆方法论」落地成可运行的 agent 记忆系统（写代码）时
  - 需要参考实现 / 集成 agent-memory 工具时
  - 要跑记忆评测电池、出量化结果时
  - 要在代码层防御记忆投毒（OWASP ASI06）时
  - 要配置复习四节点的自动化（rrule）时
  - 已读过基础版 ai-brain-learning-memory，想深入工程细节时
tags:
  - 学习记忆
  - 记忆架构
  - 参考实现
  - 记忆安全
  - 评测电池
  - 自动化
  - AI工程
  - 认知科学
classification:
  skillhub: ["knowledge"]
  iso_25010: ["Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
standards_ref: ["OWASP Agentic Top 10"]
slug: ai-brain-learning-memory-pro
ai_protocol: true

changelog: "1.0.1: bilingual rewrite (English-first, Chinese-after, full body) + read_when/desensitization"
---
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/memory_eval_battery.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: out
    type: string
    description: 结果 JSON 输出路径，默认 memory_eval_results.json
    required: false
output_schema:
  stdout: 六维 0-5 分评测 JSON
  rc=0
capabilities:
  - memory_eval
  - benchmark
  - llm_memory
permissions:
  network: false
  filesystem: true
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.0: initial upload (USK v3)"
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）


## English

### When to use
When you are building an AI agent's memory subsystem and need production-ready three-tier memory architecture code beyond concept explanations; when your system faces privacy or poisoning risk and needs OWASP ASI06-level defensive code; or when you own the agent's long-term planning and must turn cognitive-science theory into engineering practice including spaced repetition and an automated evaluation battery.

### Usage
Run `memory_eval_battery.py` directly for memory performance evaluation and six-dimension interpretation; consult the built-in code reference for the Python implementation of the three-tier memory structure; and use the OWASP ASI06 defense module for memory-safety hardening scripts.

### Process
1. Confirm whether project requirements include memory architecture implementation and safety evaluation metrics.
2. Read the basic-version docs to review core concepts and example comparisons.
3. Set up the environment using the three-tier memory reference implementation or the OWASP ASI06 defense code.
4. Tune memory-module parameters against the agent-memory tool interface.
5. Run `memory_eval_battery.py` and generate the six-dimension interpretation report.
6. Using the cognitive-science evidence mapping table, turn evaluation results into engineering optimization decisions.

### Evidence & safety statement
- Evidence: TBD (no evaluation/badge link yet; fill in the real link here once produced).
- Version: 1.0.1
- Safety: No independent security scan has been done (TBD); the conclusion is pending. No endorsement is given until it is completed.

## 中文

## 何时用
当你正在构建 AI Agent 的记忆子系统，需超越概念说明而获取可落地的三层记忆架构代码时；当你的系统面临隐私或投毒风险，需要实施 OWASP ASI06 级别的防御性代码落地方案；或当你负责 Agent 的长期规划，需要将认知科学理论转化为包含间隔重复复述与自动化评测电池的工程实践。

## 用法
支持直接运行 `memory_eval_battery.py` 进行记忆性能评估与六维解读输出；可查阅内置代码参考获取三层记忆结构的 Python 实现细节；以及访问 OWASP ASI06 防御模块获取记忆安全加固脚本。

## 流程
1. 确认项目需求是否包含记忆架构落地与安全评测指标；
2. 运行基础版文档快速回顾核心概念与实例对比；
3. 调用三层记忆参考实现或 OWASP ASI06 防御代码进行环境配置；
4. 根据 agent-memory 工具接口调整内存模块参数；
5. 输入 `memory_eval_battery.py` 执行测试并生成六维解读报告；
6. 基于认知科学证据映射表，将评测结果转化为工程优化决策。

## 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.0
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
