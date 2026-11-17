---
name: ai-governance-playbook
slug: ai-governance-playbook
display_name: 企业AI治理实操手册
displayName: 企业AI治理实操手册
title: 企业AI治理实操手册
version: 1.1.0
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
  Answer practical enterprise AI governance questions and hand back ready-to-use policy drafts, risk tiering checklists and registration workflows.

  企业AI治理综合实操手册——覆盖AI治理全景框架、AI使用政策与制度模板、AI风险分级评估清单、AI应用登记审批流程，以及中国/欧盟/美国/亚太最新AI治理法规速查（含欧盟AI Act 2026年8月全面适用与Digital Omnibus修订时间线、中国2026年智能体与拟人化AI新规、韩国AI基本法、医疗与金融行业AI治理专项）。面向企业管理者、合规、法务与信息安全负责人，一问即答，附本地工具一键生成政策草案、风险分级与成熟度自评。
description_en: "Answer practical enterprise AI governance questions and hand back ready-to-use policy drafts, risk tiering checklists and registration workflows. Managers, legal, compliance and security teams use it to classify a use case, decide whether approval is needed, and check current rules across the EU, China, the US and Asia-Pacific."
tags: [ai-governance, compliance, policy-template, risk-assessment, eu-ai-act, enterprise, regulation]
  - AI治理
  - AI合规
  - AI风险管理
  - 欧盟AI法案
  - 生成式AI
  - 企业制度
  - 合规速查
  - 亚太合规
  - 医疗AI
  - AI Governance
  - EU AI Act
  - ISO 42001
description_zh: "企业AI治理综合实操手册——覆盖AI治理全景框架、AI使用政策与制度模板、AI风险分级评估清单、AI应用登记审批流程，以及中国/欧盟/美国/亚太最新AI治理法规速查（含欧盟AI Act 2026年8月全面适用与Digital Omnibus修订时间线、中国2026年智能体与拟人化AI新规、韩国AI基本法、医疗与金融行业AI治理专项）。面向企业管理者、合规、法务与信息安全负责人，一问即答，附本地工具一键生成政策草案、风险分级与成熟度自评。"
icon: "lucide:Landmark"
---

# 企业AI治理实操手册

一站式企业 AI 治理工作台：**看得懂框架、拿得出制度、分得清风险、对得上法规、落得了地**。面向企业管理者、合规、法务与信息安全负责人，从"要不要治理"到"怎么治理落地"，全流程给答案、给模板、给清单。

## 什么时候用这个技能

当遇到以下任何场景，直接提问即可：

- **治理起步**：「我们公司 AI 用得越来越多，怎么搭 AI 治理体系？」「AI 治理委员会该设吗？怎么设？」
- **制度建设**：「帮我起草一份员工 AI 使用政策」「AI 使用守则里应该包含哪些条款？」
- **风险评估**：「用 AI 做简历筛选算高风险吗？」「这个 AI 应用要不要走审批？」
- **合规速查**：「欧盟 AI Act 现在执行到哪一步了？我们公司要不要管？」「中国对生成式 AI 有哪些要求？算法备案怎么备？」
- **对标体系**：「ISO 42001 和 NIST AI RMF 怎么选？要不要做认证？」
- **落地推进**：「AI 治理 90 天怎么落地？第一步做什么？」

## 怎么用（两种模式）

### 模式一：直接问（推荐，日常使用）

把问题直接抛出来，助手会结合 `references/` 知识库给出**有依据、可操作**的回答，并附带对应模板或清单。例如：

> 「帮我生成一份公司 AI 使用政策草案」
> 「员工拿内部数据喂给 AI 工具，风险怎么评估、怎么管？」
> 「欧盟 AI Act 2026 年 8 月之后，我们作为部署方要做什么？」

### 模式二：本地工具生成（要文件、要结果）

需要**结构化产出**（政策草案、风险分级、登记表、成熟度评分）时，使用附带的本地工具（零网络、不采集任何数据）：

```bash
# ① AI 风险分级评估：输入使用场景，输出风险等级 + 对应义务清单
python tools/ai_governance_toolkit.py classify --scenario "用AI筛选候选人简历，辅助HR做初筛"

# ② 生成 AI 使用政策草案（Markdown 全文，可直接修改使用）
python tools/ai_governance_toolkit.py policy --company "示例科技有限公司" --sector "医疗器械"

# ③ 生成 AI 应用登记表模板（CSV，可直接填）
python tools/ai_governance_toolkit.py registry --company "示例科技有限公司"

# ④ AI 治理成熟度自评：按 6 个维度 1-5 分自评，输出总分与短板提示
python tools/ai_governance_toolkit.py maturity --scores 3,4,2,5,3,4

# ⑤ 落地行动清单：按区域输出合规动作清单（cn=中国 / eu=欧盟 / intl=国际通用）
python tools/ai_governance_toolkit.py checklist --region cn

# 查看全部命令
python tools/ai_governance_toolkit.py --help
```

> 无 Python 环境也可以纯问答使用（模式一），工具只是加速产出。

## 知识库导航（references/）

| 模块 | 文件 | 解决什么问题 |
|---|---|---|
| ① AI 治理全景框架 | `references/01-AI治理全景框架.md` | 治理为什么、治理什么、谁来治理、怎么运转（PDCA） |
| ② 组织与制度模板 | `references/02-AI治理组织与制度模板.md` | AI 治理委员会章程、AI 使用政策全文、员工使用守则（可直接改） |
| ③ 风险评估清单 | `references/03-AI风险评估清单.md` | 风险分类、分级矩阵、场景库、审批触发条件 |
| ④ 中国法规速查 | `references/04-中国AI治理法规速查.md` | 中国 2022-2026 AI 法规全谱系、核心义务、备案与标识要点、AI 版权司法动态 |
| ⑤ 欧盟法规速查 | `references/05-欧盟AI治理法规速查.md` | EU AI Act 分级、义务、Digital Omnibus 最新时间线、罚款、GPAI 与透明度实务 |
| ⑥ 国际框架与标准 | `references/06-国际框架与标准速查.md` | NIST AI RMF、ISO/IEC 42001、OECD 原则、美国州法 |
| ⑦ 登记与审批流程 | `references/07-AI应用登记与审批流程.md` | 登记表字段、审批流、供应商 AI 评估 |
| ⑧ 落地路线与自评 | `references/08-落地路线与成熟度自评.md` | 90 天落地路线、6 维度成熟度自评表 |
| ⑨ 常见问题 FAQ | `references/09-FAQ.md` | 高频疑问与常见误区 |
| ⑩ 亚太与全球速查 | `references/10-亚太与全球治理速查.md` | 韩国/日本/新加坡/香港/澳洲等出海合规、全球版图 |
| ⑪ 行业 AI 治理专项 | `references/11-行业AI治理专项.md` | 医疗 AI（FDA/MDR/NMPA）、金融 AI、行业治理叠加 |

## 快速上手（三步）

1. **定位现状**：问「AI 治理成熟度怎么自评」，用 `maturity` 命令或对照 `08-落地路线与成熟度自评.md` 打一次分；
2. **补齐短板**：根据短板进对应模块——缺制度看 02、没评估看 03、不懂法规看 04/05/06；
3. **落地运转**：按 `08` 的 90 天路线推进，用 `07` 登记表把 AI 应用管起来，制度用 `02` 模板改完发布。

## 能力边界（如实说明）

- **本技能是治理方法库与工具，不是法律意见**：法规速查基于公开官方信息整理，随法规更新异步修订；重大决策请咨询执业律师/合规顾问。
- **法规时效**：欧盟 AI Act 时间线含 2026-08 最新修订（Digital Omnibus），中国法规含 2026 年 7 月最新规章；内容核对基准日见各速查表头部，引用前请复核官方原文。
- **工具不联网**：本地脚本只做规则匹配与模板生成，不采集数据、不调用任何外部服务。
- **成熟度自评为相对参考**：基于 6 维度主观自评，非第三方认证结论。

## 常见问题（FAQ）

- **Q：我们是小公司，也要做 AI 治理吗？** 看是否满足三个条件之一：员工大量使用生成式 AI、对外提供 AI 功能或服务、处理敏感/个人数据。满足其一建议至少建立"使用政策 + 登记 + 分级"最小治理包（见 08 落地路线）。
- **Q：AI 治理和一般信息安全治理什么关系？** 治理体系可复用（制度、组织、审计），AI 治理额外覆盖算法风险、数据合规、内容标识、伦理责任等 AI 特有维度；建议挂接而非另起炉灶。
- **Q：欧盟 AI Act 管到我们公司吗？** 只要在欧盟市场投放 AI 系统、或在欧盟境内部署使用 AI 系统/模型，无论公司注册地在哪都受影响（域外管辖），见 05 速查表"适用范围"。
- **Q：生成式 AI 内容标识怎么做？** 中国自 2025-09-01 起按《人工智能生成合成内容标识办法》执行显式+隐式标识；欧盟自 2026-08-02 起执行 Article 50 透明度义务（旧系统过渡至 2026-12-02），详见 04/05。
- **Q：工具脚本要不要装依赖？** 不需要，仅用 Python 标准库，任何 Python 3.8+ 直接运行。

## 版权与许可

**版权与许可**：© 2026 注册老炮。本作品（含方法论、模板、法规整理与原创表达）依 MIT License 提供，详见 `LICENSE.md`。

**知识版权声明**：本作品汇集的 AI 治理方法论、制度模板、风险清单与法规梳理之编排与原创表达，归 注册老炮 所有。未经许可，不得复制、转载、转售本作品全部或实质部分，不得用于任何模型训练或二次分发牟利。

**免责声明**：本作品按「现状」(AS IS) 提供，不作任何明示或暗示的担保，包括但不限于适销性、特定用途适用性与法规准确性保证。使用者应自行核实并承担使用后果，作者不对因使用本作品产生的任何直接或间接损失负责。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「公司想搭治理体系，从哪开始」 / "where do we start building an AI governance program"
- 「帮我起草一份员工使用政策」 / "draft an employee AI usage policy for us"
- 「用算法筛简历算不算高风险」 / "is AI resume screening high risk"
- 「欧盟法案现在管到哪一步」 / "how far has the EU AI Act gone"
- 「这个应用要不要走审批流程」 / "does this AI use case need approval"
- 「治理体系认证该选哪套标准」 / "which certification framework should we pick"

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
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-governance-playbook
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/ai-governance-playbook/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
