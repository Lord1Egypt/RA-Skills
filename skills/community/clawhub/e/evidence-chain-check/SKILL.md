---
name: evidence-chain-check
description: evidence-chain-check — LGD 三律在法律 / 电子证据链完整性域的纵深合规工具（零依赖）：证据链时间单调 / 主体一致 / 哈希链不断裂校验，对 AI 系统/数据做可执行合规校验。 适用场景：当需要法律证据链校验能力时使用本技能；触发词：evidence-chain-check。
slug: evidence-chain-check
version: 1.0.1
display_name: 法律证据链校验
display_name_en: Legal Evidence-Chain Check
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
copyright: SynomosAI
description_zh: "evidence-chain-check — LGD 三律在法律 / 电子证据链完整性域的纵深合规工具（零依赖）：证据链时间单调 / 主体一致 / 哈希链不断裂校验，对 AI 系统/数据做可执行合规校验。"
description_en: "LGD three-laws compliance for legal and electronic evidence chains (zero-dependency): time monotonicity, subject consistency and unbroken hash-chain checks."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
tags: [evidence-chain-check, AI 治理]
read_when:
  - AI 系统决策日志或证据归档要过 LGD 三律合规，先做前置校验
  - 电子数据取证中要验证哈希链连续性、防篡改
  - 审计场景要检查主体身份与时间戳逻辑是否一致完整
  - 需要零依赖、无需第三方库的证据链合规校验
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/evidence_chain_check.py
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
- Before AI-system decision logs or evidence archives must satisfy LGD three-laws compliance — as a front gate check.
- In electronic data forensics, when verifying hash-chain continuity and preventing tampering.
- In audits, when checking whether subject identity and timestamp logic are consistent and complete.
- When a zero-dependency compliance check with no extra third-party libraries is required.

### Usage
- **Main command**: `python evidence_chain_check.py --verify all`
- **Selected checks**: use `--mode time` (time monotonicity), `--mode entity` (subject consistency) or `--mode hash` (hash chain) to trigger each one separately.
- **Input data**: point `--input <path>` at the evidence file under check.

### Workflow
1. Prepare the evidence data source containing timestamps, signatures and hash values.
2. Run the Python command to load `evidence_chain_check.py` into the runtime.
3. Select or enable the three-laws check mode(s) as needed (time / subject / hash).
4. The system compares the input data automatically, detecting monotonicity consistency and chain-break risk.
5. Emit a compliance report flagging anomalies and potential evidence-integrity gaps.
6. Close the loop: archive, repair or block based on the findings.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- AI 系统决策日志或证据归档需满足 LGD 三律合规前，进行前置校验。
- 电子数据取证中验证哈希链连续性、防止篡改时调用。
- 审计场景中检查主体身份与时间戳逻辑是否一致且完整时。
- 需要零依赖且无需额外第三方库的合规校验工具执行环境时。

### 用法
- **主命令**：`python evidence_chain_check.py --verify all`
- **指定校验项**：支持 `--mode time`（时间单调）、`--mode entity`（主体一致）、`--mode hash`（哈希链）分别触发。
- **输入数据**：通过 `--input <路径>` 参数指向待检的证据文件。

### 流程
1. 准备包含时间戳、签名及哈希值的证据数据源。
2. 执行 Python 命令加载 `evidence_chain_check.py` 脚本进入运行环境。
3. 根据需求选择或启用三律校验模式（时间/主体/哈希）。
4. 系统自动比对输入数据，检测单调性一致性与链断裂风险。
5. 输出合规报告并标记异常项与潜在证据完整性漏洞。
6. 依据检测结果执行归档、修复或阻断操作闭环。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
