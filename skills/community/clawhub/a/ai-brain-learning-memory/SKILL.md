---
name: ai-brain-learning-memory
title: AI大脑学习记忆方法论
display_name: AI大脑学习记忆方法论
description: "AI 大脑学习记忆方法论（汇总版）——把 AI 的学习与记忆按人脑模型组织：三层记忆架构 + 编码→存储→提取三阶段 + 训战省化学习飞轮 + 复习与遗忘机制 + 人脑学习法原理与 AI 对照 + 记忆安全。让 AI 真正「学得进、记得住、用得上」。含 30 秒上手、触发说明、场景例子、问题速查表，普通用户也能直接用。触发词：大脑学习记忆、AI学习记忆、记忆架构、怎么让AI记住、学习记忆机制、海马体、记忆固化、brain memory、learning memory、记忆模型、记忆分层、艾宾浩斯、间隔重复、记忆宫殿、费曼学习法、主动回忆、睡眠巩固、记忆投毒、记忆安全、情节记忆、语义记忆、快速绑定、记忆评测。"
version: 2.4.1
agent_created: true
author: SynomosAI (LGD initiative)
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebSearch, Task
category: AI学习方法论
platforms: [windows, macos, linux]
read_when:
  - 需要决定「这个信息该不该记 / 记到哪」时
  - 任务完成后需要沉淀经验时
  - 发现记忆混乱 / 记不住 / 找不到 / 忘了时
  - 需要给 AI 或团队讲解学习记忆机制时
  - 学习新技能 / 新知识之前
tags:
  - 学习记忆
  - 记忆架构
  - 记忆固化
  - 遗忘曲线
  - 训战省化
  - 记忆卫生
  - 记忆安全
  - 人脑学习法
  - AI学习方法论
slug: SynomosAI-brain-learning-memory
displayName: AI大脑学习记忆方法论
description_zh: "AI 大脑学习记忆方法论（汇总版）——把 AI 的学习与记忆按人脑模型组织：三层记忆架构 + 编码→存储→提取三阶段 + 训战省化学习飞轮 + 复习与遗忘机制 + 人脑学习法原理与 AI 对照 + 记忆安全。让 AI 真正「学得进、记得住、用得上」。含 30 秒上手、触发说明、场景例子、问题速查表，普通用户也能直接用。"
description_en: "Human-brain-inspired methodology for AI learning and memory: three-tier memory architecture, encode-store-retrieve stages, training flywheel, review/forgetting mechanisms and memory safety."
classification:
  skillhub: ["knowledge"]
  iso_25010: ["Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
standards_ref: ["OWASP Agentic Top 10"]
ai_protocol: true
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
  stdout: 六维 0-5 分评测 JSON（编码/单跳/多跳/时序/蒸馏/容量）
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - memory_eval
  - benchmark
  - llm_memory
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "2.4.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
1. Deep memory optimization with hippocampus-model or Ebbinghaus-forgetting applications.
2. Long-term memory stability: prevent "memory poisoning", enable memory safety.
3. Validate human-brain principles (three-tier architecture) mapped into AI and evaluate effect.

### Usage
1. Run `python memory_eval_battery.py` with args to run the memory evaluation battery.
2. Optional params: `--mode=encoding_stage`, `--verify=retrieval_check`.
3. Doc-interaction mode: trigger words auto-load the built-in protocol.

### Flow
1. Encode: layer new information into the three-tier memory architecture per the human-brain model.
2. Spaced repetition: apply Ebbinghaus curve for background review.
3. Retrieval test: run `memory_eval_battery.py` for the full battery.
4. Analyze results; flag risky data to prevent semantic drift / poisoning.
5. Optimize params per the memory-safety report — close the learning-flywheel loop.

### Evidence & safety
- Evidence: TBD. Version: 2.4.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 当需对 AI 进行深度记忆优化，涉及海马体模型或艾宾浩斯遗忘曲线的具体应用时。
2. 当需要进行长期记忆稳定性保障，防止"记忆投毒"并开启记忆安全机制时。
3. 当用户需要验证人脑原理（如三层架构）在 AI 中的实现对照与效果评估时。

### 用法
1. 直接调用脚本命令 `python memory_eval_battery.py` 并附加参数执行记忆电池测试。
2. 可选配置参数包括 `--mode=encoding_stage`、`--verify=retrieval_check`，用于指定学习阶段与评测方式。
3. 文档交互模式下，输入特定触发词自动加载内置协议，无需命令行操作即可读取使用。

### 流程
1. 执行数据编码，按人脑模型将新信息分层存入三层记忆架构。
2. 启动间隔重复存储机制，应用艾宾浩斯遗忘曲线进行后台复习。
3. 触发提取测试环节，调用脚本 `memory_eval_battery.py` 运行完整评测电池。
4. 系统分析结果并标记潜在风险数据，防止语义漂移或信息污染。
5. 根据记忆安全报告优化参数，完成一次学习飞轮循环的反馈闭环。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：2.4.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
