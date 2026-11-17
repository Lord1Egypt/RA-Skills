---
name: evidence-chain-builder
slug: evidence-chain-builder
display_name: AI 论断有证证据链（LGD-II 有证）
display_name_en: "AI Claim Evidence-Chain Builder (LGD-II Evidenced)"
description: >-
  Decompose AI claims into verifiable evidence chains (LGD-II): each item tagged by source type (official, paper, data, internal, assertion) with independent verifiability status.

  当用户要『验证 AI 论断 / 防幻觉 / 给结论找证据 / 判断信源可信度』时用。把论断拆成可验证证据链：每条证据标来源类型(official/paper/data/internal/assertion)、是否可独立验证、可信度，输出『证成度』与未支撑论断清单。对齐 EIFP 不编造原教旨——本工具不判定论断真假，只评估证据质量；缺可验证证据的论断明确标『勿作结论』。这是 LGD-II 有证的落地执行器。触发词：证据链、论断验证、防幻觉、信源可信、有证、claim 证据、论断举证。
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
category: AI 治理
platforms: [windows, macos, linux]
read_when:
  - 用户要验证某个 AI 论断是否站得住脚
  - 用户要防止幻觉、给结论配可核验证据
  - 做事实核查、合规举证、技术写作的引用背书
  - 要落地「凡所行必有证据」的有证原则
tags: [LGD, 有证, 证据链, 防幻觉, 事实核查, 信源, 证成度, 不编造]
copyright: SynomosAI
description_zh: "当用户要『验证 AI 论断 / 防幻觉 / 给结论找证据 / 判断信源可信度』时用。把论断拆成可验证证据链：每条证据标来源类型(official/paper/data/internal/assertion)、是否可独立验证、可信度，输出『证成度』与未支撑论断清单。对齐 EIFP 不编造原教旨——本工具不判定论断真假，只评估证据质量；缺可验证证据的论断明确标『勿作结论』。这是 LGD-II 有证的落地执行器。触发词：证据链、论断验证、防幻觉、信源可信、有证、claim 证据、论断举证。"
description_en: "Decompose AI claims into verifiable evidence chains (LGD-II): each item tagged by source type (official, paper, data, internal, assertion) with independent verifiability status."
classification:
  skillhub: ["ai-governance"]
  iso_25010: ["Security", "Maintainability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（按默认策略设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走人工批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/evidence_chain.py
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
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"

---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：见平台质量门禁规范

## English

### When to use
- When the user presents an unverified AI claim, opinion summary or news item and needs to prevent hallucination while finding supporting evidence.
- When verifying conclusions or assessing source credibility, needing to be explicit about the evidence quality of each source kind (official / paper / data, etc.).
- When running the LGD-II "evidenced" executor, making sure every conclusion is traceable and EIFP-compliant.
- When trigger words such as "evidence chain", "anti-hallucination" or "claim evidence" demand a structured decomposition of the verification process.

### Usage
- Call the Python script `evidence_chain.py` from the CLI or API, passing the claim text to be analyzed as the core input.
- Optionally configure the source types (e.g. official / paper) and verification depth; by default the system runs the EIFP no-fabrication logic.
- To get a detailed evidence-chain report, enable `--verbose` to surface the unsupported-claim list in full.
- After reading the input, the script returns structured JSON: each evidence item's id, source and credibility score.

### Workflow
- **Step 1**: receive the target claim and extract the core assertion, scoping what must be verified.
- **Step 2**: decompose complex claims into atomic evidence fragments, identifying each fragment's type and independence.
- **Step 3**: match candidate evidence sources; assess how credible and independently verifiable the information is.
- **Step 4**: per the EIFP no-fabrication principle, flag missing evidence or information gaps.
- **Step 5**: aggregate all evidence quality into an overall justification score and generate a structured verification report.
- **Step 6**: emit the result; claims that cannot be supported are explicitly marked "do not conclude" together with the gap list.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once it is produced)
- Version: 1.0.1
- Security: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 当用户提出未经证实的 AI 论断、观点摘要或新闻信息，需防止幻觉并寻找支撑证据时。
- 进行结论验证或信源可信度评估，需明确各类来源（官方/论文/数据等）的证据质量时。
- 执行 LGD-II 有证落地执行器任务，确保所有结论均有据可查且符合 EIFP 原则时。
- 当触发「证据链」「防幻觉」或「论断举证」等关键词，要求结构化拆解验证过程时。

### 用法
- 通过命令行或 API 调用 Python 脚本 `evidence_chain.py`，指定待分析论断文本作为核心输入参数。
- 可选配置源信源类型（如 official/paper）及验证深度，系统默认按 EIFP 标准执行不编造逻辑。
- 若需输出详细证据链报告，需在脚本调用中开启 `--verbose` 模式以获取未支撑清单细节。
- 脚本读取输入后，将返回结构化 JSON 数据，包含每条证据的标号、来源及可信度评分。

### 流程
- **步骤 1**：接收用户输入的目标论断，提取核心主张并明确待验证的范围。
- **步骤 2**：将复杂论断拆解为原子级证据片段，识别每个片段的类型与独立性。
- **步骤 3**：匹配潜在证据库或来源，评估信息的真实可信度与是否可独立验证。
- **步骤 4**：依据 EIFP 不编造原教旨原则，标记是否存在缺位证据或缺口信息。
- **步骤 5**：综合所有证据质量计算整体证成度数值，生成结构化验证报告。
- **步骤 6**：输出结果，对无法得到支持的论断明确标注『勿作结论』及缺失清单。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evidence-chain-builder
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/evidence-chain-builder/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
