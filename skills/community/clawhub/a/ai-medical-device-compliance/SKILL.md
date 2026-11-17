---
name: ai-medical-device-compliance
slug: ai-medical-device-compliance
display_name: AI医疗器械全球合规
displayName: AI医疗器械全球合规
title: AI医疗器械全球合规
version: 1.0.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
category: 通用技能
platforms:
  - windows
  - macos
  - linux
  - web
author: 注册老炮
license: MIT
description: >-
  A practical guide to getting AI/ML medical devices cleared in the US, EU and China, from pathway selection and classification through clinical evidence and change control. It covers FDA 510(k)/De Novo/PMA and PCCP, EU MDR Rule 11 and AI Act timelines, and NMPA classification and change registration. Use when planning a first submission or deciding whether an algorithm update needs a new filing.

  AI/ML 医疗器械全球注册合规实操手册——覆盖美国FDA（510(k)/De Novo/PMA、PCCP预设变更控制、QMSR、网络安全SBOM）、欧盟（MDR Rule 11分类、AI Act高风险2028-08-02、CER/PMCF临床评价）、中国NMPA（分类界定、2026更新指南、变更注册、1000例数据本地化、创新通道）三地完整注册路径，含临床证据要求对比、变更管理与全生命周期（GMLP/算法漂移）、三地费用周期对比与并行出海策略。面向医械法规工程师、研发与国际业务负责人，附零依赖本地工具一键查询三地分类、路径、费用周期估算与变更触发判定。
description_en: An all-in-one practical playbook for global regulatory compliance of AI/ML medical devices — covering US FDA pathways (510(k)/De Novo/PMA, PCCP predetermined change control, QMSR, cybersecurity SBOM), EU (MDR Rule 11 classification, AI Act high-risk deadline of August 2028, CER/PMCF clinical evaluation), and China NMPA (classification, 2026 updated guidance, change registration, 1,000-case data localisation, innovation channel), with clinical evidence requirements comparison, lifecycle change management (GMLP/algorithm drift), cost and timeline comparisons, and parallel go-to-market strategy. Built for regulatory engineers, R&D and international business leaders. Includes a zero-dependency local toolkit for three-market classification, pathway and cost/timeline queries, and change-trigger checks.
tags:
  - 医疗器械
  - AI医疗器械
  - FDA
  - MDR
  - NMPA
  - 510k
  - PCCP
  - 出海合规
  - SaMD
  - Medical Device
  - EU AI Act
  - GMLP
---

# AI 医疗器械全球合规

AI/ML 医疗器械全球注册合规工作台：**分得清三地分类、选得对注册路径、估得出费用周期、管得住算法变更、出得了海**。面向医械法规工程师、研发与国际业务负责人，覆盖美国、欧盟、中国三大市场从产品定位到上市后全生命周期合规。

## 什么时候用这个技能

- **产品定位**：「我们的 AI 诊断软件在 FDA/欧盟/NMPA 算什么类别？」
- **路径选择**：「AI 辅助诊断产品走 510(k) 还是 De Novo？要 PMA 吗？」
- **变更管理**：「模型重新训练了，需要重新注册吗？PCCP 怎么用？」
- **临床证据**：「三地临床评价要求有什么不同？RWD 能用吗？」
- **出海策略**：「中美欧三地并行申报怎么排？先做哪个市场？」
- **费用周期**：「Class II/III 在三地大概多少钱、多久？」

## 怎么用（两种模式）

### 模式一：直接问（推荐）

把问题直接抛出来，助手结合 `references/` 知识库给出**有依据、可操作**的回答：

> 「我们的 CT 肺结节 AI 辅助诊断软件，中美欧三地分别怎么注册？」
> 「模型要持续学习更新，FDA 的 PCCP 和 NMPA 的变更注册怎么选？」
> 「欧盟 AI Act 对医疗器械 AI 有什么额外要求？什么时候生效？」

### 模式二：本地工具（要结构化结果）

```bash
# ① 三地分类判定：输入产品描述，输出 FDA/欧盟/NMPA 三地风险类别
python tools/ai_meddev_toolkit.py classify --product "CT肺结节AI辅助诊断软件，用于辅助医生阅片"

# ② 注册路径推荐（按市场）
python tools/ai_meddev_toolkit.py path --region us        # us=美国 / eu=欧盟 / cn=中国

# ③ 费用与周期估算（按市场+类别）
python tools/ai_meddev_toolkit.py estimate --region us --class II

# ④ 变更触发判定：输入变更描述，判定是否需重新注册/申报
python tools/ai_meddev_toolkit.py change --desc "模型权重重新训练，训练数据扩至3倍，预期用途不变"

# ⑤ 三地总对比表（分类/周期/费用/临床要求）
python tools/ai_meddev_toolkit.py compare

# 查看全部命令
python tools/ai_meddev_toolkit.py --help
```

> 无 Python 环境也可以纯问答使用（模式一）。

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① 全景与定义 | `references/01-AI医械全景与定义.md` | SaMD/AiMD 定义、IMDRF、GMLP、AI 类型（锁定/自适应/生成式） |
| ② 美国 FDA 路径 | `references/02-美国FDA注册路径.md` | 510(k)/De Novo/PMA、PCCP、QMSR、网络安全 SBOM、费用周期 |
| ③ 欧盟 MDR+AI Act | `references/03-欧盟MDR与AIAct.md` | MDR Rule 11 分类、AI Act 高风险义务、公告机构、CER/PMCF |
| ④ 中国 NMPA 路径 | `references/04-中国NMPA注册路径.md` | 分类界定、指导原则、变更注册、1000 例本地化、创新通道 |
| ⑤ 临床证据要求 | `references/05-临床证据与数据要求.md` | 三地临床评价对比、RWD、多中心、金标准 |
| ⑥ 变更与生命周期 | `references/06-变更管理与全生命周期.md` | PCCP vs PACMP vs 变更注册、算法漂移监控、退役 |
| ⑦ 对比与出海策略 | `references/07-三地对比与出海策略.md` | 三地对照总表、并行申报、优先级决策 |
| ⑧ 术语表与 FAQ | `references/08-术语表与FAQ.md` | 高频术语 + 常见问题 |

## 快速上手（三步）

1. **定位产品**：用 `classify` 命令或问「我们的 XX 产品三地算什么类别」；
2. **选路径**：`path` 命令看目标市场注册路径，对照 `02/03/04` 模块细节；
3. **排计划**：`estimate` 估算费用周期，用 `07` 模块出海策略排并行申报节奏。

## 能力边界（如实说明）

- **本技能是方法库与工具，不是监管意见**：分类、路径、费用均基于公开监管信息整理（核对基准日见各模块头部），正式申报请以监管机构最新指南与专业咨询为准；
- **费用数据为公开渠道估算区间**：FDA 费率按财年调整、欧盟公告机构报价差异大、NMPA 费用随产品复杂度和临床方案浮动，申报前需复核；
- **法规时效**：EU AI Act 医疗器械相关高风险义务 2028-08-02 适用、NMPA 分类指南 2026 年更新，引用前复核官方原文；
- **工具不联网**：本地规则匹配与估算，不采集数据、不调用外部服务。

## 常见问题（FAQ）

- **Q：所有医疗 AI 软件都要注册吗？** 是否构成 SaMD（医疗目的软件）决定是否作为医疗器械监管；纯健康管理/生活方式类软件可能不构成 SaMD（见 01 模块定义）。
- **Q：FDA 和 NMPA 的变更要求一样吗？** 不一样——FDA 有 PCCP（预定变更控制计划）可预批算法更新路径，NMPA 核心算法权重重新训练通常触发变更注册（2026 年部分创新通道试点灵活方案），欧盟可用 PACMP（见 06 模块）。
- **Q：CE 标志能替代 AI Act 合规吗？** 不能——医疗器械需同时满足 MDR 和 AI Act（2028-08-02 起高风险义务），同一公告机构一并审核，但两套要求并存（见 03 模块）。
- **Q：外国公司进中国要重新做临床吗？** Class III 诊断 AI 通常需要以中国患者数据在境内验证（1000+ 例要求），不能直接用海外数据（见 04 模块）。
- **Q：工具脚本要装依赖吗？** 不需要，仅 Python 标准库，3.8+ 直接运行。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的 AI 医疗器械合规方法论、注册路径整理、对比分析与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与监管准确性保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「这个AI辅助诊断软件按几类报」 / "Which device class does this AI diagnostic tool fall under?"
- 「算法改了要不要重新注册」 / "We changed the algorithm — does that need a new submission?"
- 「这款软件在美国走哪条申报路径」 / "Which US pathway applies to this software?"
- 「欧盟AI法案对我们什么时候生效」 / "When does the EU AI Act start applying to us?"
- 「同一款产品中美欧能一起报吗」 / "Can we file the same product in the US, EU and China together?"
- 「训练数据一定要放在境内吗」 / "Does the training data have to stay in-country?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-medical-device-compliance
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-medical-device-compliance/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
