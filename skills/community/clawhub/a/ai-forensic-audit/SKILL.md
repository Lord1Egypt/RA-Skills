---
name: ai-forensic-audit
slug: ai-forensic-audit
displayName: AI 溯源审计 · 证据链报告
description: "AI 溯源审计技能：对 AI 生成内容/Agent 行为/对话记录执行溯源审计——采集证据链（来源/时间线/操作日志/生成痕迹）→ 交叉验证 → 输出结构化审计报告（证据清单+可信度+风险点+建议）。对标国际标准：C2PA 内容溯源 / SLSA 供应链 / EU AI Act Art.50 / 审计准则（ISSAI/COBIT）。适用：AI 内容是否由某 AI 生成、Agent 操作合规审计、泄密溯源、医疗 AI 审计（细分第一）。触发词：溯源、审计、证据链、AI 审计、这是谁生成的、provenance、forensic、audit trail、内容溯源。"
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
description_zh: "AI 溯源审计：证据链采集→交叉验证→审计报告，对标 C2PA/SLSA/EU AI Act Art.50，适用内容溯源、Agent 审计、泄密溯源"
description_en: "AI provenance & forensic audit: evidence chain collection → cross-validation → audit report. Aligned with C2PA, SLSA, EU AI Act Art.50, ISSAI/COBIT. For content attribution, agent compliance audits, leak tracing."
author: 注册老炮
license: MIT
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
category: 战略 · AI 溯源
tags: [溯源, 审计, 证据链, forensic, provenance, audit, C2PA, SLSA, 追踪]
---

# AI 溯源审计 · 证据链报告（Forensic Audit）

> **像警察破案一样审计 AI**：采集证据 → 交叉验证 → 出报告。
> 国际对标：C2PA（内容溯源）/ SLSA（供应链）/ EU AI Act Art.50 / 审计准则 ISSAI·COBIT。

## 这是什么

对 AI 生成内容 / Agent 行为 / 对话记录，执行 **五步溯源审计**，输出**结构化审计报告**：

```text
【五步溯源审计全景】
界定范围 → 采集证据 → 交叉验证 → 定级结论 → 审计报告
    │         │           │           │          │
 审计目标   来源/时间线  多源比对   可信度L1-4  证据清单+风险+建议
            操作日志     矛盾检测
            生成痕迹
```

## 五步审计流程

| 步骤 | 做什么 | 输出 |
|------|--------|------|
| **1. 界定范围** | 明确审计对象（内容/Agent/对话）、审计目标（来源？合规？泄密？）、时间窗口 | 审计范围声明 |
| **2. 采集证据** | 收集：生成元数据（C2PA 若存在）、时间线（创建/修改/发布）、操作日志、API 调用记录、生成痕迹（风格/指纹）| 证据链清单 |
| **3. 交叉验证** | 多源比对（不同渠道的证据是否一致）、矛盾检测（时间/内容/主体冲突）、指纹比对 | 验证矩阵 |
| **4. 定级结论** | 按证据充分度输出可信度 L1-L4（同三锚一票分级体系）| 审计定级 |
| **5. 审计报告** | 结构化报告：证据清单 + 验证矩阵 + 定级 + 风险点 + 整改建议 | 可分发报告 |

## 可信度定级（与 ai-identity-verification 对齐）

| 级别 | 含义 |
|------|------|
| L4 | 密码学证据（C2PA 签名/SLSA 可验证）支撑，溯源链条完整 |
| L3 | 多源证据一致，无矛盾，但无密码学签名 |
| L2 | 单一来源证据，或存在轻微矛盾 |
| L1 | 证据不足或硬矛盾，无法确证 |

## 使用示例

**示例 1 · 内容溯源**
问："这篇市场报告是 AI 写的吗？谁写的？"
→ 检查 C2PA 元数据 → 无则采集：生成时间线（文档属性）、写作风格指纹、引用来源 → 交叉验证 → 输出 L2/L3 结论 + "建议发布平台启用 C2PA 签名" 建议

**示例 2 · Agent 操作合规审计**
问："审计一下这个 Agent 昨天的所有操作是否合规"
→ 采集操作日志 → 对照合规边界（权限/数据访问/外部调用）→ 输出合规矩阵（通过/违规/存疑）+ 风险点 + 整改建议

**示例 3 · 泄密溯源**
问："这份内部文件泄露了，源头在哪？"
→ 采集：文件元数据（作者/创建时间）、不可见追踪码（若已嵌入）、分享链记录 → 时间线重建 → 输出泄露路径假设 + 证据 + 建议加强密文追踪

**示例 4 · 医疗 AI 审计**
问："审计这个医疗 AI 的回答是否合规（不承诺疗效、不越权诊断）"
→ 采样回答 → 对照《医疗器械广告审查办法》/医疗合规边界 → 输出合规率 + 违规样本 + 整改建议

## 边界（Boundary）

- **审计≠执法**：本技能输出证据与建议，不具执法效力；司法/监管场景需专业机构
- **证据有限则如实**：缺密码学证据就定级 L2/L3，不臆断
- **隐私保护**：审计不扩大采集范围，只用用户提供的材料；涉及个人信息遵守个保法
- **时效性**：AI 工具与平台日新月异，C2PA/SLSA 等标准在演进，结论标注审计日期

## 常见坑（Gotchas）

| # | 坑 | 正确做法 |
|---|----|---------|
| 1 | 把"看起来像"当证据 | 风格相似是弱证据，需时间线/元数据/密码学证据支撑 |
| 2 | 单源证据定级过高 | 至少 2 个独立来源交叉验证才可 L3 |
| 3 | 忽略元数据可篡改 | 文档元数据可改，需结合多源；只有签名（C2PA）防篡改 |
| 4 | 医疗审计给绝对结论 | 医疗 AI 审计必须标注"需监管/专业机构确认" |
| 5 | 审计报告不带日期 | 标准在演进，报告必须含审计日期与依据版本 |

## 错误处理（Error Handling）

| 情况 | 处理 |
|------|------|
| 证据链断裂（中间环节缺失）| 标注断点位置，定级降一档，给出补证路径 |
| 无任何元数据 | 说明"纯内容型无元数据"，走风格/来源分析，定级上限 L2 |
| 用户要求"查出真凶"式的绝对结论 | 如实给证据与可能性，不迎合 |
| 跨平台证据格式不一致 | 先归一化（时间戳/格式），否则标注差异 |

## 国际标准对标（2026-08 查证）

| 标准 | 状态 | 应用 |
|------|------|------|
| C2PA | 2026 一致性计划进行中 | 内容溯源密码学层（OpenAI/Google 已用）|
| SLSA + Sigstore | 生产级 | AI 供应链溯源（模型训练/部署血缘）|
| EU AI Act Art.50 | 生效 | AI 内容披露义务的合规基准 |
| ISSAI / COBIT | 成熟审计准则 | 审计流程方法论参照 |
| W3C DID/VC | 标准 | 与 ai-identity-verification 联动（身份→行为→内容全链）|

> **理论增量**：五步审计把「身份核验（三锚一票）」与「内容溯源（C2PA）」打通为完整审计链——身份锚定谁、行为审计做了什么、内容溯源产出什么，三者合一才是完整 AI 问责闭环。这对应战略「专家→警察」的警察角色工具。

## 版本记录
- v1.0.0（2026-08-22）：五步溯源审计方法论首发，对标 C2PA/SLSA/EU AI Act Art.50/ISSAI/COBIT

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-forensic-audit
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-forensic-audit/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
