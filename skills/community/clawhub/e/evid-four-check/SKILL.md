---
name: evid-four-check
slug: evid-four-check
displayName: 电子证据四性审查判定器
version: 1.0.1
category: it-ops-security
display_name: 电子证据四性审查判定器
display_name_en: Electronic Evidence Four-Properties Review
title: 电子证据四性审查判定器
author: 诺律(SynomosAI)
author_note: '"SynomosAI" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, Edit, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 电子证据四性审查判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-LAW-001域。 适用场景：当需要电子证据四性审查判定器能力时使用本技能；触发词：合规、判定器、TH-LAW-001、evid-four-check。
tags: [合规, 判定器, TH-LAW-001, evid-four-check, 电子证据, 四性审查]
description_zh: "电子证据四性审查判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-LAW-001域。"
description_en: "Electronic evidence authenticity and legality (four-properties) review determination tool: zero-dependency decision support with JSON IR output (domain TH-LAW-001)."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
platforms: [windows, macos, linux]
read_when:
  - 法院/仲裁庭等法律环境下要对电子证据做四性（真实/合法/关联/完整）形式审查
  - 要把多源异构证据数据转成标准 JSON IR 供下游系统解析
  - 需要零依赖、可审计、输入不全时从严推定的证据判定
  - 用户说「电子证据能不能用」「四性审查」「聊天记录/合同证据效力」
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: evid-four-check.py
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
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
Use it in legal settings such as courts or arbitral tribunals, when the compliance of electronic evidence must be reviewed against court-admission standards. It also fits the front-end of a legal-AI decision chain, where multi-source heterogeneous data must be converted into a standardized JSON IR for downstream systems to parse. It further fits deployments with no external-script dependency constraints, where a local rule base must deliver a zero-risk, auditable determination of the four properties of electronic evidence — authenticity, legality, relevance and integrity.

### Usage
Submit the electronic evidence dataset to be reviewed directly through the skill's configuration interface, and pass `domain=TH-LAW-001` to lock the rule-source scope. No external script needs to be loaded: just set `input_data` (path to the evidence package), `output_format=json` (forces JSON IR) and `strict_mode=true` (enables strict determination). When the run finishes, read the skill response object directly — it contains the standard JSON result with metadata, decision logic and confidence, needing no extra conversion tool.

### Workflow
1. **Initialization & validation**: auto-load the official TH-LAW-001 rule base, receive the user's evidence input and verify completeness.
2. **Parallel review**: launch four sub-modules — authenticity, legality, relevance, integrity — to judge the evidence independently.
3. **Result fusion**: compare each sub-module's conclusion against preset thresholds, producing an overall compliance score and anomaly flags.
4. **Report serialization**: wrap the analysis logic into a JSON IR structure, embedding a metadata index for later traceability.
5. **Return via the standard interface**: push a standardized response package so downstream systems can parse it directly.
6. **Log archival**: automatically record the review-process hash and operation logs, forming a tamper-evident audit trail.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed. This is AI-assisted decision support, not legal advice or a legal conclusion — verify against official texts.

## 中文

### 何时用
适用于法院、仲裁庭等法律环境下的电子证据合规性审查场景，确保输出结果符合法庭采信标准。
适用于构建法律 AI 决策链路的前端环节，需要将多源异构数据转换为标准化 JSON IR 格式供下游系统解析的集成环境。
适用于无外部脚本依赖约束的项目部署，要求利用本地规则库实现零风险、可审计的电子证据四性（真实性、合法性、关联性、完整性）判定需求。

### 用法
直接通过技能配置接口提交待审查电子证据数据集合，并传入 `domain=TH-LAW-001` 以锁定规则源范围。
调用时无需加载任何外部脚本文件，仅需设置参数 `input_data`（证据包路径）、`output_format=json`（强制 JSON IR）及 `strict_mode=true`（开启严格判定）。
系统运行结束后，直接读取技能响应对象即可获取包含元数据、判定逻辑及置信度的标准 JSON 结果，无需额外转换工具。

### 流程
1. **初始化与校验**：自动加载 TH-LAW-001 官方规则库，接收用户输入的证据数据并验证完整性。
2. **并行审查执行**：分别启动真实性、合法性、关联性、完整性四个子模块对证据进行独立判定。
3. **结果融合分析**：比对各子模块结论与预设阈值，生成综合合规性评分及异常标记。
4. **报告序列化**：将分析逻辑封装为 JSON IR 结构，嵌入元数据索引以便后续溯源验证。
5. **返回标准接口**：向调用方推送标准化响应包，确保下游系统可直接解析使用。
6. **日志归档**：自动记录审查过程哈希值与操作日志，形成不可篡改的审计轨迹。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。本工具为 AI 辅助决策支持，非法律意见、非法律结论——请对照官方文本核实。
