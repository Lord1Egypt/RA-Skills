---
name: csv-slice
description: CSV 切片器 — CSV 快速查看/取列/去重/条件筛选/统计行数，纯标准库 csv 模块（零依赖） 适用场景：当需要CSV 切片器能力时使用本技能；触发词：csv-slice。
slug: csv-slice
title: csv-slice
version: 1.0.1
display_name: CSV 切片器
display_name_en: CSV Slice
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write
category: 效率工具
platforms: [claude, codex, cursor, windsurf, cli]
copyright: SynomosAI
description_zh: "CSV 切片器 — CSV 快速查看/取列/去重/条件筛选/统计行数，纯标准库 csv 模块（零依赖）"
description_en: "Quick CSV inspection: view or filter columns, dedupe, conditional filtering, row counts, using the pure standard-library csv module (zero-dependency)."
read_when:
  - 处理本地 CSV 需轻量工具、无法装第三方库
  - 快速数据预览/提取特定列/基础去重
  - 自动化流程前置步骤做初步数据清洗
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
tags: [csv-slice, 效率工具]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/csv_slice.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: file
    type: string
    description: CSV 文件
    required: true
  - name: head
    type: int
    description: 前 N 行
    required: false
  - name: cols
    type: string
    description: 列号逗号串如 1,3
    required: false
  - name: where
    type: string
    description: 条件 列号=值
    required: false
  - name: dedup
    type: bool
    description: 整行去重
    required: false
  - name: count
    type: bool
    description: 只统计行数
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 切片后表格或行数
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - csv
  - data_inspection
  - productivity
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
1. Handling a local CSV with a lightweight tool when third-party libs can't be installed.
2. Quick data preview, extracting specific columns, or basic dedup.
3. Upstream step in an automated pipeline for initial data cleaning.

### Usage
1. Core command: `python csv_slice.py -i <file>`.
2. Common params: `--column <name>`, `--mode unique`, `--filter <expr>`.
3. Invoke as CLI or wrapped API.

### Flow
1. Confirm the Python stdlib env; prepare the CSV path.
2. Run `csv_slice.py` with file path and slice/filter params.
3. Parse params and CSV header; init the in-memory processing context.
4. Iterate rows per mode: dedup, column slice, or conditional filter.
5. Emit the result CSV to stdout or a target file.
6. Return a row-count summary and status code.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 何时用
1. 在处理本地 CSV 文件时，需使用轻量级工具且无法安装第三方库依赖。
2. 需要快速查看数据预览、提取特定列或进行基础去重操作的场景。
3. 在自动化流程中作为前置步骤，利用 Python 标准库执行初步的数据清洗任务。

### 用法
1. 核心命令：`python csv_slice.py -i <file>`。
2. 常用参数：`--column <列名>` 指定提取特定列数据；`--mode unique` 执行行去重模式；`--filter <条件表达式>` 根据内容筛选数据。
3. 通过脚本 `csv_slice.py` 作为主要入口，支持标准命令行交互或封装后的 API 调用。

### 流程
1. 确认 Python 标准库运行环境就绪，并准备待处理的 CSV 数据源路径。
2. 执行 `python csv_slice.py` 命令，传入文件路径及必要的过滤或切片参数。
3. 解析请求的参数配置与 CSV 头部信息，初始化内存中的数据处理上下文。
4. 根据设定的模式遍历数据行，执行去重、列切片或条件筛选逻辑。
5. 将处理后的 CSV 内容输出至标准终端或直接写入指定文件路径。
6. 返回处理结果的行数统计摘要及最终状态码供调用方进行下一步验证。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
