---
name: aut-grade-checker
slug: aut-grade-checker
displayName: 车辆驾驶自动化等级判定器
version: 1.0.2
category: it-ops-security
display_name: 车辆驾驶自动化等级判定器
title: 车辆驾驶自动化等级判定器
author: 诺卫(SynomosAI)
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 车辆驾驶自动化等级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-AUT-001域。 适用场景：当需要车辆驾驶自动化等级判定器能力时使用本技能；触发词：合规、判定器、TH-AUT-001、aut-grade-checker。
tags: [合规, 判定器, TH-AUT-001, aut-grade-checker]
description_zh: "车辆驾驶自动化等级判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-AUT-001域。"
description_en: "Vehicle driving-automation level determination tool: zero-dependency decision support with JSON IR output (domain TH-AUT-001)."
read_when:
  - 需按 TH-AUT-001 域官方规则判定驾驶自动化等级
  - 零依赖离线决策（无法连外部规则库/数据库）
  - 合规报告生成前对车辆功能/驾驶任务做等级校准
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high。"
platforms: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: aut-grade-checker.py
  runtime: python3
  call_pattern: args
input_schema:
  - name: demo
    type: bool
    description: 内置冒烟案例
    required: false
  - name: json
    type: bool
    description: JSON 输出
    required: false
output_schema:
  stdout: 车辆驾驶自动化等级判定 JSON IR（决策支持·须人工复核）
  exit_code:
    type: integer
    description: "0=OK/PASS; 1=findings/warnings; 2=usage or argument error"
capabilities:
  - autonomous_driving
  - classification
  - decision_support
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.2: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate（外部公开评测门禁文档）

## English

### When to use
1. Vehicle driving-automation level must be determined strictly per TH-AUT-001 official rules.
2. Zero-dependency offline decision making (no external rule DB reachable).
3. Calibrate vehicle functions / driving tasks to the right automation level before compliance reporting.

### Usage
Doc-style tool; no executable script. Interact via JSON IR: send task goals, vehicle sensor capabilities and function config; the built-in rule base matches and outputs the final level with confidence.

### Flow
1. User prepares a JSON request with driving scenario and hardware capabilities.
2. Parse the function combination per the built-in official rule source.
3. Auto-match TH-AUT-001 level criteria.
4. Generate a logic report with level number, applicable conditions and rationale.
5. Validate the JSON IR format; return to the user.
6. End the call; wait for the next analysis.

### Evidence & safety
- Evidence: TBD. Version: 1.0.2. Security: no independent scan (TBD).

## 中文

### 何时用
1. 当需要车辆驾驶自动化等级判定，且必须严格遵循 TH-AUT-001 域官方规则时。
2. 在系统执行零依赖决策场景，无法连接外部规则库或数据库时使用。
3. 用于生成合规性报告前，对当前车辆功能与驾驶任务进行自动化级别校准时。

### 用法
该技能为文档型工具，需通过 JSON IR 接口交互获取结果。请向技能发送包含任务目标、车辆传感器能力及功能配置的输入参数，系统将内置规则库匹配并输出最终判定等级及置信度。直接请求推理接口即可。

### 流程
1. 用户准备包含驾驶场景描述与车辆硬件能力的 JSON 请求。
2. 技能基于内置的官方规则源解析输入参数中的功能组合。
3. 系统自动匹配 TH-AUT-001 域等级判定标准。
4. 生成包含等级编号、适用条件及依据的逻辑报告。
5. 校验输出格式是否符合 JSON IR 规范并返回给用户。
6. 结束调用，等待新的分析指令或完成本次判定任务。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.2
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
