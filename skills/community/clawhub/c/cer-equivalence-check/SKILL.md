---
name: cer-equivalence-check
slug: cer-equivalence-check
title: 临床评价报告等同性论证要素检查器
displayName: 临床评价报告等同性论证要素检查器
display_name: 临床评价报告等同性论证要素检查器
display_name_en: CER Equivalence Argument Element Checker
version: 1.0.1
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch, WebSearch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
author: SynomosAI (LGD initiative)
copyright: SynomosAI
category: 医疗器械合规
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
tags: ["医疗器械","医械合规","临床评价报告等同性论证要素检查器","判定器","TH-MED-009","决策支持"]
description: "临床评价选了等同器械这条捷径，结果被问「数据访问权在哪」——要素缺一项，整条路走不通。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例） 适用场景：当需要临床评价报告等同性论证要素检查器能力时使用本技能；触发词：医疗器械、医械合规、临床评价报告等同性论证要素检查器、判定器、TH-MED-009。"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (cer-equivalence-check). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
description_zh: "临床评价选了等同器械这条捷径，结果被问「数据访问权在哪」——要素缺一项，整条路走不通。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
classification:
  skillhub: ["medtech-reg"]
  clawhub: ["productivity", "data-analytics", "development"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
ai_protocol: true

read_when:
  - 用户提及本技能触发词或面临描述中的典型问题时
  - 用户说「医疗器械」或需要该能力时
  - 用户说「医械合规」或需要该能力时
  - 用户说「临床评价报告等同性论证要素检查器」或需要该能力时
  - 用户说「判定器」或需要该能力时

changelog: "1.0.1: bilingual rewrite (English-first, Chinese-after, full body) + read_when/desensitization"
---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：[skill-quality-gate](../skill-quality-gate/SKILL.md)


## English

### When to use
For clinical-evaluation submissions that plan the equivalent-device route, when regulators question the source and authorization of data. Use it to check JSON element completeness and produce deterministic, immutable results in a zero-dependency environment. In automated review, it returns codes (0/1/2) to quickly locate missing data-access grants or format errors.

### Usage
Call via CLI with no extra Python deps. Format: `cer-equivalence-check [options]`. Key params: `--input` (raw JSON data file), `--demo` (built-in clinical-eval test case), `--force-json-output` (force standardized output). The input must carry complete device fields and authorization markers; insufficient permissions auto-fail with a return code.

### Process
1. Build a JSON input package with the device registration certificate, comparison data source, and access agreement.
2. Run with `--input` pointing at the data file, or `--demo` for the preset compliant case.
3. The tool parses element completeness, focusing on whether data-access credentials required for clinical evaluation exist.
4. It generates deterministic JSON IR with an immutable analysis log.
5. Use the return code (0/1/2) to judge pass, missing permission, or execution error.

### Evidence & safety statement
- Evidence: TBD (no evaluation/badge link yet; fill in the real link here once produced).
- Version: 1.0.1
- Safety: No independent security scan has been done (TBD); the conclusion is pending. No endorsement is given until it is completed.

## 中文

## 何时用
适用于临床评价申报中拟采用等同器械验证路径，但面临监管对数据来源与权限合规性存疑的场景。用于检测 JSON 要素完整性，确保在零依赖环境下生成确定性不可变的结果报告。用于自动化审核流程，需明确返回码含义（0/1/2）以快速定位数据访问缺失或格式错误问题。

## 用法
直接通过命令行接口调用，无需安装额外 Python 库依赖。命令格式支持 `cer-equivalence-check [options]`，核心参数含 `--input`（原始 JSON 数据文件路径）、`--demo`（触发内置临床评价测试用例）及 `--force-json-output`（强制标准化输出）。调用时需确保输入对象包含完整的器械信息字段与授权标识，若权限不足将自动判定失败并返回代码。

## 流程
第一步：构建包含器械注册证、对比数据源及访问协议在内的 JSON 输入包。第二步：执行命令时传入 `--input` 参数指向数据文件，或添加 `--demo` 使用预置的合规案例。第三步：技能解析要素完整性，重点核验临床评价中所需的数据访问权凭证是否存在。第四步：系统根据校验结果生成确定性 JSON IR，并附带不可更改的分析日志。第五步：依据最终返回码（0/1/2）判断流程通过、权限缺失或执行异常状态。

## 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.0
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
