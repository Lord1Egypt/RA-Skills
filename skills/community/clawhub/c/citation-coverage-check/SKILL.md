---
name: citation-coverage-check
description: citation-coverage-check — 扫描文章中含数字/日期/论断的句子，统计带来源标注（据/来源/source/链接/文献）的比例；低于阈值 rc=1，逐句列出缺出处清单。 适用场景：当需要引用覆盖率检查器能力时使用本技能；触发词：citation-coverage-check。
slug: citation-coverage-check
title: citation-coverage-check
version: 1.0.1
display_name: 引用覆盖率检查器
display_name_en: Citation Coverage Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [claude-code, codebuddy, openai-agents, cli]
copyright: SynomosAI
description_zh: "citation-coverage-check — 扫描文章中含数字/日期/论断的句子，统计带来源标注（据/来源/source/链接/文献）的比例；低于阈值 rc=1，逐句列出缺出处清单。"
description_en: "Scan articles for sentences with numbers, dates or claims and measure source-attribution coverage; below threshold rc=1 with a per-sentence missing-citation list."
read_when:
  - 学术论文/技术报告关键论断是否带来源标注
  - 数字/日期等事实性信息的引用覆盖率是否达标
  - 内容审核要求文献出处比例不低于阈值
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [citation-coverage-check, AI 治理]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/citation_coverage_check.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: file
    type: string
    description: 文件
    required: false
  - name: text
    type: string
    description: 内联文本
    required: false
  - name: threshold
    type: float
    description: 覆盖率阈值默认0.6
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 无出处论断清单与覆盖率
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - citation
  - academic_writing
  - fact_check
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
- Review whether key claims in academic papers / technical reports carry source attribution.
- Verify citation coverage of factual info (numbers, dates) meets the bar.
- Content review requires a minimum share of cited claims.

### Usage
- Run `python scripts/citation_coverage_check.py --input article.txt`.
- Recognized markers: 据 / 来源 / source / 链接 / 文献.
- `--threshold` sets the coverage bar (default 0.6).

### Flow
1. Parse input; extract candidate sentences with numbers, dates or claims.
2. Scan each sentence tail for citation markers.
3. Compute the covered ratio; compare with the threshold.
4. Emit a per-sentence missing-citation list with positions and fragments.
5. Output a summary of under-covered segments.
6. Help the user locate and add missing citations.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
- 在撰写学术论文或技术报告时，审查关键论断是否附带来源标注。
- 用于验证文档中涉及数字、日期等事实性信息的引用覆盖率是否达标。
- 当内容审核要求明确文献出处比例不低于阈值时调用此技能。

### 用法
- 执行命令行命令：`python scripts/citation_coverage_check.py --input article.txt`。
- 指定引用标注类型为"据/来源/source/链接/文献"以适配不同文档风格。
- 通过 `--threshold` 设置覆盖率阈值（默认 0.6）。

### 流程
1. 解析输入文本，提取包含数字、日期及论断的候选句子。
2. 扫描每句末尾是否匹配"据/来源/source/链接/文献"等引用标记。
3. 统计标注句子比例并与阈值进行数值比对判定。
4. 生成缺失引用的逐句清单，列出具体位置及对应原文片段。
5. 输出分析结果摘要，提示不达标段落数量及占比情况。
6. 辅助用户定位并补充缺失的文献引用信息或标注。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
