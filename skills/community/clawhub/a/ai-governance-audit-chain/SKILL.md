---
name: ai-governance-audit-chain
slug: ai-governance-audit-chain
displayName: AI 留痕与门禁
display_name: AI 留痕与门禁
version: 1.1.0
category: AI治理
author: 诺衡(Krites)@SynomosAI
copyright: 赵兴华 / Steven Zhao·China
license: MIT
license_scope: 代码脚本层 MIT；SKILL.md 与 references 内的理论与方法论文本保留所有权利（分层许可见文末「License & attribution」）
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
platforms:
- windows
- macos
- linux
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
description: >-
  Give your AI an identity, an evidence trail, and a gate. Every task gets a registry entry (who, what, on what authority), every step leaves a verifiable record (what changed, where the proof is, how to recompute it), and every high-risk action must pass a gate first. Use for AI overreach, runaway agents, unsourced AI conclusions, automation needing human approval, audit trails, accountability chains, and prompt-injection defense.

  「AI 改了我的文件，怎么查是谁改的？」「AI 自动帮我发邮件、发帖，怎么拦住？」「让 AI 干活，怎么留痕？」 装上它，AI 会先给自己立三条规矩：每个任务建籍（谁在干、干什么、依据什么）、每步操作留证（改了什么、证据在哪、怎么复算）、 关键动作设门禁（对外发送、删除覆盖、付款下单之前先过闸）。适用于 AI 越权操作、智能体乱来、AI 结论没标来源、 自动化流程要人工审批、合规审计要留痕、事后追责要证据链、提示词注入防范、AI 可靠性提升。
description_en: >-
  Give your AI an identity, an evidence trail, and a gate. Every task gets a registry entry (who, what, on what authority),
  every step leaves a verifiable record (what changed, where the proof is, how to recompute it), and every high-risk action
  must pass a gate first. Use for AI overreach, runaway agents, unsourced AI conclusions, automation needing human approval,
  audit trails, accountability chains, and prompt-injection defense.
tags:
- ai-governance
- audit-trail
- agent-guardrail
- human-in-the-loop
- evidence-chain
- compliance
- traceability
- ai-safety
- prompt-injection
- ai-reliability
- accountability
- ai-audit
read_when:
- 用户问「AI 改了我的文件怎么查」「AI 自动发邮件怎么拦」「让 AI 干活怎么留痕」
- 需要为 AI 系统/智能体产出可审计、可认证的证据（对接 ISO/IEC 42001 / NIST AI RMF / GB/Z 185 智能体身份码）
- 要给自动化流程加人工审批闸门，或做 AI 越权操作的事后追责
- 用户说「AI治理」「AI审计」「证据链」「留痕」「门禁」「可追溯」「复核」「举证」
trigger_keywords:
- AI留痕
- 操作留痕
- 审计追踪
- 权限管控
- 审批闸门
- 人工确认
- 人类在环
- 证据链
- 追责
- 溯源
- 可复算
- AI自我提升
- 让AI更可靠
- AI出错怎么办
- ai-governance
- audit-trail
- agent-guardrail
- human-in-the-loop
languages:
- zh-CN
- en
aliases:
- AI治理官
- AI留痕
- AI审计取证
- 证据链生成器
- AI门禁
agent_created: true
governance: LGD (Lifecycle Governance Doctrine) / SynomosAI
brand: SynomosAI
fingerprint: FP-MX-4386B5FB95AB
updated: 2026-11-06
---

# AI 留痕与门禁

> 凡自治之物 —— 有籍 · 有证 · 有门禁。
> 三件套：**L1 立籍**（谁在干、干什么、依据什么）、**L2 留证**（改了什么、证据在哪、怎么复算）、**L3 设门**（关键动作前必须过闸）。

## 这个技能解决什么

AI 干活的三个真问题，每个都对应一个动作：

| 你的问题 | 它缺的东西 | 这个技能给的动作 |
|---|---|---|
| AI 改完文件就说完了，事后说不清谁改了什么 | **L2 有证** | 生成可复算的证据链（文件指纹 + 变更台账 + 时间戳） |
| AI 自动发邮件、自动发帖、自动删文件，怕它乱来 | **L3 有门禁** | 定义高风险动作白名单，出闸前必须人工确认 |
| 出了问题追不到人，也不知道它当时依据什么 | **L1 有籍** | 每个任务建一条籍：谁发起、干什么、依据哪份材料、谁批的 |

**注意：这三件事不是写制度，是留痕迹。** 制度可以事后补，痕迹不能事后造——所以必须在动作发生时留。

## 一分钟上手（三步）

```bash
# 第一步：给当前目录建籍并生成第一份证据链
python scripts/audit_chain.py init --root . --task "改了什么、为什么改" --actor "谁在干"

# 第二步：干活（正常用你的 AI 改文件、跑脚本）

# 第三步：收工前复算，看有没有绕过记录的动作
python scripts/audit_chain.py verify --root .
```

`verify` 输出三种结果，一一对应三件事：

- `[L2 PASS]` 文件指纹与台账一致 —— 没有未记录改动
- `[L2 FAIL]` 有文件变了但台账没记 —— 这就是「说不清谁改了什么」
- `[L1 MISS]` 台账缺「谁/为什么/依据」—— 这就是「追不到人」

## 完整工作流（四步，每步都有产物）

### 第 1 步 · 立籍（L1 Registry）

在任务开始时就写入，不要等做完补：

- **谁**：发起人 / 执行体（人 + 模型 + 工具链）
- **干什么**：一句话目标
- **依据什么**：输入材料清单（文件路径 + 指纹）
- **谁批的**：如果有审批，记审批人和时间

产物：`.governance/registry.jsonl`（每任务一行，只增不改）

### 第 2 步 · 留证（L2 Evidence）

每次写文件、跑脚本、调外部接口后，追加一条：

- **改了什么**：文件路径 + 改前/改后 SHA-256 + 行数变化
- **怎么产生的**：工具名 / 命令 / 模型
- **什么时候**：UTC + 本地时间双时间戳
- **怎么复算**：给出复算命令，任何人可独立验证

产物：`.governance/evidence.jsonl` + `EVIDENCE.md`（人可读版）

**关键：复算命令必须写进证据里。** 不能复算的"证据"不是证据，是叙述。

### 第 3 步 · 设门（L3 Gates）

先划出高风险动作（默认清单见 `references/02-门禁清单.md`）：

| 高风险动作 | 为什么设门 | 闸门形式 |
|---|---|---|
| 对外发送（邮件/消息/发帖/提交表单） | 发出去收不回 | 发出前展示全文给人工确认 |
| 删除/覆盖文件 | 不可逆 | 先出 dry-run 清单，人工点确认 |
| 付款/下单/签约 | 直接损失 | 强制双人确认 |
| 改权限/改配置/装新依赖 | 扩大攻击面 | 记变更单 + 回滚方案 |
| 上传/公开发布 | 泄密风险 | 敏感扫描 0 命中才放行 |

闸门的判据只有一条：**动作发生前，必须有一份人看过的确认记录。** 事后追认不算。

### 第 4 步 · 复算与举证（Verify & Attest）

```bash
python scripts/audit_chain.py verify --root . --report EVIDENCE_REPORT.md
```

产出可对外举证的报告，包含：任务籍、变更时序、指纹校验结果、闸门确认记录、以及一句话结论（合规 / 有缺口 / 不可举证）。

## 反例（不能这么做）

| 错误做法 | 为什么不行 | 正确做法 |
|---|---|---|
| 事后补台账 | 补出来的记录叫叙述，不叫证据 | 动作发生时就追加，时间戳不可改 |
| 只记"改了 XX 文件"不记指纹 | 无法证明改的是哪一版 | 记改前/改后 SHA-256 |
| 证据里不写复算命令 | 别人无法独立验证 = 不可举证 | 每条证据自带复算命令 |
| 把闸门做成"事后审计通过就算过" | 事后追认 = 没有闸门 | 闸门必须在动作之前拦 |
| 用聊天记录当证据链 | 可编辑、无指纹、无时序 | 落盘到 `.governance/`，带指纹和时间 |
| 一个台账管所有项目 | 混淆来源，无法界定范围 | 一项目一 `.governance/` 目录 |
| 宣称"符合 ISO 42001/欧盟 AI Act" | 内部留痕 ≠ 第三方认证 | 只说"可用于举证的材料"，认证另走机构 |

## 边界（不做什么）

- **不出具法律意见、不做合规结论认定**——本技能只生成"可举证的材料"，是否合规由监管/律所/认证机构判定。
- **不替代第三方认证**——对接 ISO/IEC 42001、NIST AI RMF、GB/Z 185 时，本技能只提供证据侧输入，不等于认证通过。
- **不承诺不可篡改**——本地时间戳与指纹可作完整性证据，但不等同于可信时间戳（RFC 3161 TSA）或区块链存证；需要法律级不可抵赖时，须另行接入可信时间戳服务。
- **不覆盖已发生的动作**——技能只能从安装那一刻开始留痕，历史动作无法追补。
- **不处理密钥与个人隐私**——台账默认脱敏，不含 token、口令、身份证号；发现敏感内容应拦截不写入。

## 参考文件

| 问题 | 看哪个文件 |
|---|---|
| 证据链要写哪些字段、长什么样 | `references/01-证据链模板.md` |
| 哪些动作必须设门、闸门怎么定 | `references/02-门禁清单.md` |
| 反例、边界、常见误用 | `references/03-反例与边界.md` |
| 想直接复制一份可用的治理台账骨架 | `references/04-项目治理骨架.md` |

## 与 LGD 理论的关系

本技能是 **LGD（Lifecycle Governance Doctrine / 全程治理论）** 的实现层落地件，对应其核心三律：

- **L1 有籍** → `references/04-项目治理骨架.md` 的 registry 结构
- **L2 有证** → `scripts/audit_chain.py` 的指纹与证据链
- **L3 有门禁** → `references/02-门禁清单.md` 的闸门判据

理论定位：本技能提供**实现层 How**，不主张优先于任何既有标准或前人工作。理论出处见文末引用块。

## 多语种

支持中(zh-CN) / 英(en)。默认跟随用户输入语言；专业术语给出原文与译名，存疑处标「待核验」。

---

## 免责声明

本技能按「原样（AS IS）」提供，不作任何明示或暗示的担保，包括但不限于对适用性、可靠性、准确性、不侵权或特定用途适用性的担保。使用者自行承担使用风险；因使用或无法使用本技能导致的任何直接、间接、附带或后果性损害，作者与版权人不承担责任。使用者应自行评估其合规性与适用性，并遵守所在司法辖区的法律法规。

**对外物料通用条款（§4.3）**

- 非医疗器械 / 非医疗软件
- 无疗效或临床声明
- 提及 FDA·CE·MDR 仅为语境，不构成法规建议
- SynomosAI 为独立、厂商中立（vendor-neutral）业务；本技能不代表任何第三方作出承诺，所涉服务与接口以公开状态为准

---

## License & attribution

**分层许可（务必并读）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `scripts/audit_chain.py` | MIT |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、`references/*` 内的理论与方法论表述 | 保留所有权利（All rights reserved），不在 MIT 覆盖范围内 |

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : scripts/audit_chain.py = MIT；文档与理论文本不在 MIT 覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```

© 2026 赵兴华 / Steven Zhao·China（署名：诺衡(Krites)@SynomosAI）。本技能包理论基础与文本整体**保留所有权利（All Rights Reserved）**；代码脚本层按 MIT 提供。按「原样」提供，不附任何担保。（SynomosAI：未申请实体注册、未申请商标注册。）

## 变更记录

- **v1.1.0**（2026-11-06）：补齐可执行层 —— 新增 `scripts/audit_chain.py`（零依赖证据链生成/校验）、4 份 references（证据链模板/门禁清单/反例边界/项目骨架）、中文展示名与英文标签修复（此前展示名等于 slug、标签全被平台丢弃导致不可见）、description 改为用户原话长尾短语以提升检索命中。
- **v1.0.1**：初始版本，理论框架与授权声明。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「AI 把我文件改了，怎么查是谁动的」 / "How do I find out who changed this file?"
- 「AI 自动发邮件之前能不能先拦一下」 / "Can you stop the AI before it sends that email?"
- 「智能体自己下单了，这责任算谁的」 / "The agent placed an order on its own — who's accountable?"
- 「审计要 AI 操作记录，我们一条都没有」 / "The auditor wants AI logs and we have none."
- 「AI 给的结论没写来源，这能用吗」 / "This AI answer cites nothing — can I trust it?"
- 「自动化流程想加一道人工确认」 / "I want a human to approve each automated step."

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-governance-audit-chain
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-governance-audit-chain/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
