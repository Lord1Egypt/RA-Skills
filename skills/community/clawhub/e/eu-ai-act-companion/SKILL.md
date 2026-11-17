---
name: eu-ai-act-companion
display_name: EU AI Act 合规导航（EU AI Act Companion）
display_name_en: "EU AI Act Companion"
description: "当用户问『我的AI产品要过EU AI Act吗』『高风险还是有限风险』『provider还是deployer义务』『合规要做什么』『截止日期』，或要把 AI 系统投放欧盟市场/在欧部署时使用。把 EU AI Act 从法规文本落成导航：风险四级分类（不可接受/高/有限/最小）、按角色的义务清单（provider/deployer/importer）、关键时间节点（2024-08 生效、2025-02 禁止类、2026-08 高危义务、2027-08 全量）、文档与合格评定路径。附可运行分类器，输入用例即输出风险级+义务+节点。泛化自 eu-ai-act-check。触发词：EU AI Act、欧盟人工智能法、AI合规、高风险AI、合格评定、provider义务、deployer义务、AI法案截止、CE标志、AI监管、 conformity assessment。"
version: 1.1.1
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash
category: AI合规
platforms: [windows, macos, linux]
read_when:
  - 要把 AI 系统投放欧盟市场或在欧盟内部署
  - 不确定产品属哪一级风险、要尽什么义务
  - 区分 provider / deployer / importer 责任边界
  - 规划合规时间表、合格评定、CE 标志路径
  - 用户问「EU AI Act 对我有什么影响」
tags: [EU AI Act, AI合规, 高风险, 合格评定, provider义务, 时间节点, 欧盟]
slug: eu-ai-act-companion
title: EU AI Act 合规导航（EU AI Act Companion）
copyright: SynomosAI
description_zh: "当用户问『我的AI产品要过EU AI Act吗』『高风险还是有限风险』『provider还是deployer义务』『合规要做什么』『截止日期』，或要把 AI 系统投放欧盟市场/在欧部署时使用。把 EU AI Act 从法规文本落成导航：风险四级分类（不可接受/高/有限/最小）、按角色的义务清单（provider/deployer/importer）、关键时间节点（2024-08 生效、2025-02 禁止类、2026-08 高危义务、2027-08 全量）、文档与合格评定路径。附可运行分类器，输入用例即输出风险级+义务+节点。泛化自 eu-ai-act-check。触发词：EU AI Act、欧盟人工智能法、AI合规、高风险AI、合格评定、provider义务、deployer义务、AI法案截止、CE标志、AI监管、 conformity assessment。"
description_en: "Navigate the EU AI Act: risk tier of your AI system, provider vs deployer obligations, required compliance actions and deadlines when placing systems on the EU market."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
standards_ref: ["EU AI Act"]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/eu_ai_act_nav.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: "命令行参数透传给主脚本，具体取值见各包 --help"
    required: false
output_schema:
  stdout:
    type: string
    description: "标准输出为 JSON 结果，含逐项检查与总体结论"
  exit_code:
    type: integer
    description: "0=PASS/完成；1=FAIL/有警告或待补强；2=用法或参数错误"
capabilities:
  - cli_tool
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
When the user asks concrete EU AI Act compliance questions — risk-tier classification, provider or deployer obligations, or the Act's deadlines. It fits the moment before deploying an AI system in the EU or placing it on the EU market, when you need to quickly locate the regulatory navigation path and the required documentation. It also fits the need to feed in a concrete AI use-case and get back a runnable risk classification plus a compliance action list.

### Usage
Call the skill interface `eu-ai-act-companion` to run the analysis directly; under the hood it runs the Python logic in `eu_ai_act_nav.py`. Supported parameters: `input_case` (description of the AI use-case), `target_role` (provider / deployer / importer) and `time_target` (a specific date). If documentation generation is involved, a read module can be specified to output a structured compliance report or execution plan.

### Workflow
1. Receive the user's AI use-case and clarify the deployment role and target market region.
2. Run the underlying classifier on the system's characteristics to decide unacceptable / high / limited / minimal risk.
3. Auto-match the provider / deployer legal obligations and CE-marking requirements to the role.
4. Check the key milestones (2024–2027) to determine whether entry-into-force or prohibitions have already been triggered.
5. Merge the conformity-assessment path and documentation checklist into a final compliance-navigation summary with recommended actions.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.1.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed. This skill is a navigation aid, not legal advice.

## 中文

### 何时用
当用户咨询 EU AI Act 的具体合规疑问，如风险等级分类、Provider 或 Deployer 义务及法案截止日期时。适用于在欧部署 AI 系统或投放欧盟市场前需要快速定位法规导航路径与文档要求的场景。适用于输入具体 AI 用例即获取可运行的风险分类结果与合规行动清单的需求。

### 用法
通过调用技能接口 `eu-ai-act-companion` 直接执行分析，底层依赖脚本文件 `eu_ai_act_nav.py` 运行 Python 逻辑。支持参数输入 `input_case`（AI 系统用例描述）、`target_role`（provider/deployer/importer）及 `time_target`（具体日期）。若涉及文档生成，可指定读取模块以输出结构化合规报告或执行计划。

### 流程
1. 接收用户输入的 AI 系统用例并明确其部署角色或目标市场区域。
2. 运行底层脚本分类器模型对系统特性进行不可接受、高、有限、最小风险的判定。
3. 根据角色属性自动匹配 provider/deployer 的特定法律义务与 CE 标志要求。
4. 核对关键时间节点（2024-2027）以确定是否已触发生效或禁止状态。
5. 整合合格评定路径与文档清单，输出最终合规导航摘要及行动建议。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。本技能为导航辅助，不构成法律意见。
