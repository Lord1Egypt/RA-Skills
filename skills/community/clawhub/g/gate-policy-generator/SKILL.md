---
name: gate-policy-generator
description: >-
  Generate a policy-as-code permission file that splits an agent's tools into allowed, needs-review and blocked tiers, with four gates covering overreach, accidental deletion or sending, and runaway loops.

  生成 LGD-III 有门禁权限策略
description_zh: "生成 LGD-III 有门禁权限策略"
description_en: "Generate a policy-as-code permission file that splits an agent's tools into allowed, needs-review and blocked tiers, with four gates covering overreach, accidental deletion or sending, and runaway loops. Use it before an agent touches sensitive tools, exports data or ships to production."
slug: gate-policy-generator
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
display_name: 权限有门禁生成器
display_name_en: Gate Policy Generator
category: AI 治理
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
platforms: [windows, macos, linux]
agent_created: true
copyright: SynomosAI
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [gate-policy-generator, AI 治理, 权限策略, policy-as-code, 有门禁]
read_when:
  - Agent 要访问外部敏感工具或执行高危操作前，需划权限边界与四道门禁
  - 项目涉及代码变更/数据导出/文件操作，要自动防越权与误删误发
  - 检测到安全风险模式或失控循环迹象，要快速生成阻断性政策
  - 新环境部署隔离/审计/审批等权限层级的初始化
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/gate_policy.py
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
  network: true
  filesystem: true
  subprocess: true
  scope: project-dir-only   # 只处理调用者指定目录；外发需人逐次确认，无预设接收端
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first), added read_when; 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
1. Before an agent accesses external sensitive tools or performs high-risk operations, when permission boundaries and four-gate rules must be drawn.
2. When a project involves code changes, data export or file operations, for automatic anti-overreach and accidental-deletion/accidental-sending checks.
3. When potential security-risk patterns or runaway-loop signs are detected, to quickly generate a blocking policy config.
4. During the initial setup of new permission tiers in an environment (e.g. isolation, auditing, approval).

### Usage
Run `python gate_policy.py` to invoke the skill's generation logic; it reads `gate_policy.py` directly. Key parameters: `--scenario` (business scenario), `--tool-list` (callable / forbidden tool set), `--review-mode` (review level). The system auto-detects context from the `__pycache__` cache environment and outputs a standard `policy-as-code` YAML file for configuration.

### Workflow
1. Analyze permission needs; pin down the agent's callable tool range and the off-limits zones.
2. Load `gate_policy.py` and pass in the business-scenario parameters to pre-draft the policy.
3. Generate the four gate rules (anti-overreach, anti-accidental-deletion, anti-runaway, anti-violation).
4. Run internal safety checks to confirm the policy introduces no logic loops or permission conflicts.
5. Emit the final `LGD-III_policy.yaml`.
6. Deploy the policy to the runtime environment and verify the permissions take effect.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
1. 当 Agent 计划访问外部敏感工具或执行高危操作前，需划定权限边界与四道门禁规则；
2. 在项目涉及代码变更、数据导出或文件操作时，用于自动防越权与误删/误发校验；
3. 检测到潜在的安全风险模式或失控循环迹象时，快速生成阻断性政策配置；
4. 在环境部署新权限层级（如隔离、审计、审批）的初始化设置阶段。

### 用法
通过执行 `python gate_policy.py` 命令调用技能生成逻辑，直接读取文件 `gate_policy.py`；
关键参数包括：`--scenario` (定义业务场景)、`--tool-list` (可调用/禁止工具集合)、`--review-mode` (评审级别);
系统将基于 `__pycache__` 缓存环境自动识别上下文，输出标准 `policy-as-code` YAML 格式文件供配置使用。

### 流程
1. 分析权限需求，明确 Agent 可调用的工具范围及不可触碰的禁区；
2. 加载 `gate_policy.py` 脚本并传入业务场景参数进行政策预演；
3. 生成四道门禁规则（防越权、防误删、防失控、防违规）；
4. 执行内部安全校验，确认策略未引发逻辑死循环或权限冲突；
5. 输出最终生成的 `LGD-III_policy.yaml` 文件；
6. 将策略部署到运行环境并完成权限生效验证。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「给 agent 划一下哪些工具能用」 / "map out which tools the agent may call"
- 「怎么防止 AI 越权调接口」 / "how do we stop the AI calling privileged APIs"
- 「需要人工审批的动作怎么配」 / "configure which actions need human approval"
- 「把权限规则写成配置文件」 / "write the permission rules as a config file"
- 「失控循环要提前挡住」 / "a runaway loop has to be blocked upfront"
- 「新项目上线前的权限基线」 / "set a permission baseline before the project ships"

Trigger when the user says any of the above, in Chinese or English.

---

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/gate-policy-generator
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/gate-policy-generator/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
