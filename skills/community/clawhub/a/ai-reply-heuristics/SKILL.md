---
name: ai-reply-heuristics
description: ai-reply-heuristics — 启发式估计一段文字的 AI 痕迹强度：套话密度/破折号频率/句长均匀度/排比结构 → 0-100 分与三档区间（启发式，不构成判定，附免责）。 适用场景：当需要AI痕迹启发式检查器能力时使用本技能；触发词：ai-reply-heuristics。
slug: ai-reply-heuristics
title: ai-reply-heuristics
version: 1.0.1
display_name: AI痕迹启发式检查器
display_name_en: AI Reply Heuristics
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "ai-reply-heuristics — 启发式估计一段文字的 AI 痕迹强度：套话密度/破折号频率/句长均匀度/排比结构 → 0-100 分与三档区间（启发式，不构成判定，附免责）。"
description_en: "Heuristic estimation of AI-flavor intensity in a text: boilerplate density, dash frequency, sentence-length uniformity and parallelism, scored 0-100 with three bands (heuristic only, with disclaimer)."
read_when:
  - 需初步量化文本 AI 痕迹强度（草稿审核/风格对比）
  - 怀疑文字套话过多、标点异常、结构过于均匀等机械化特征
  - 仅作参考、非法律/医疗等高风险正式判定
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [ai-reply-heuristics, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/ai_reply_heuristics.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: file
    type: string
    description: 文本文件
    required: false
  - name: text
    type: string
    description: 内联文本
    required: false
output_schema:
  stdout: AI 痕迹启发式评分与特征清单
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - ai_detection
  - text_analysis
  - heuristic
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
Preliminary quantification of AI-flavor intensity in text — draft review or style comparison. Use when suspecting over-boilerplate, abnormal punctuation or overly uniform structure. Use only as a reference, not as formal judgment in legal contracts or medical diagnosis.

### Usage
Core script: `ai_reply_heuristics.py`. Run via CLI or as a Python module. Pass the text as an argument; the script extracts features and emits JSON output. No extra dependencies.

### Flow
1. Prepare the text; confirm source allows public analysis.
2. Run `ai_reply_heuristics.py` with the text param.
3. Auto-compute boilerplate density, parallelism and other metrics → score.
4. Read the 0-100 score and three-band label.
5. Apply the "non-definitive" disclaimer; fold the result into human decision-making.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
适用于需要初步量化文本 AI 生成痕迹强度的场景，如草稿审核或内容风格对比。当怀疑文字存在过度套话、标点使用异常或结构过于均匀等机械化特征时，可使用本技能作为参考工具。请在非法律合同及医疗诊断等高风险领域使用，明确理解其不构成正式判定依据。

### 用法
核心脚本文件为 `ai_reply_heuristics.py`，支持命令行直接运行或 Python 环境模块导入方式调用。调用时需传入待分析文本字符串作为参数，系统会自动提取特征并生成 JSON 格式输出。无需额外配置依赖库，运行过程会基于预设逻辑自动读取执行。

### 流程
1. 准备合规的待检测文本，确认来源允许公开分析。
2. 执行 `ai_reply_heuristics.py` 脚本并将文本参数传入函数。
3. 系统自动计算套话密度、排比结构等指标生成分数。
4. 获取返回的 0-100 分及对应的三档区间标识信息。
5. 结合"非绝对判定"说明，将结果纳入人工决策流程中并签署免责确认。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
