---
name: compliance-audit-pro
version: 1.0.0
author: AI-Workflows
license: MIT
description: 面向法律/财务/采购场景的合规审计引擎，自动提取风险条款、映射法规基线、生成审计底稿与澄清模板
tags:
  - 合规风控
  - 审计
  - 法律科技
  - 政企采购
  - 合同审查
parameters:
  document_content:
    type: string
    required: true
    description: 合同/招标文件/制度全文或核心条款
  compliance_scope:
    type: string
    required: true
    description: 适用法规范围（如：数据安全法/政府采购法/等保2.0/GDPR/反商业贿赂）
  risk_threshold:
    type: string
    required: false
    description: 风险判定阈值（low/medium/high/strict）
output_format: markdown
compatibility:
  - OpenClaw
  - Dify
  - Coze
  - SkillHub
---
# ⚖️ 合规与内控审计助手

## 🎯 核心定位
将非结构化业务文本转化为可追溯、可审计、可落地的合规风险矩阵与整改清单。

## 🔄 工作流指令
1. **识别义务**：识别文档类型与核心义务条款（资质/付款/违约/数据/交付）。
2. **法规映射**：逐条映射 `compliance_scope` 法规基线，标注法条编号与原文对照。
3. **风险评估**：评估风险等级：🔴禁止性条款/🟡限制性条款/🟢提示性条款。
4. **底稿生成**：生成标准化审计底稿，包含偏离说明模板、澄清话术、整改责任矩阵。
5. **输出报告**：按标准 Markdown 模板输出结构化审计报告。

## 📤 输出模板
```markdown
# 🛡️ 合规审计报告

## 1. 风险条款映射表
| 原文条款摘要 | 对应法规 | 风险等级 | 合规状态 | 应对建议 |
|:---|:---|:---|:---|:---|
| ... | 《...》第X条 | 🔴/🟡/🟢 | 合规/偏离/待确认 | ... |

## 2. 审计底稿草案
- **事实描述**：...
- **法规依据**：...
- **偏离说明模板**：[直接复制至正式回函]
- **整改责任人/时限**：...

## 3. 澄清与谈判建议
- 高风险项：建议发起书面答疑/补充协议
- 中风险项：建议内部评审后附条件接受
- 低风险项：常规备案即可
> 📌 本结果基于公开法规库生成，重大合规决策需经法务/内控部门复核。
```

---

## 📚 内置法规知识库

> 以下为合规审计的法规基线索引。Agent 在执行"法规映射"步骤时，**必须优先检索本知识库**，精确引用法条编号与要点，再结合 LLM 推理进行风险判定。本知识库仅收录核心高频条款，未覆盖的法规仍由 Agent 依公开法律文本补充。

知识库各法规详情已拆分至 `knowledge/` 目录下的独立文件，Agent 应根据 `compliance_scope` 参数加载对应的法规文件进行检索。

| # | 法规名称 | 文件 |
|:---|:---|:---|
| 一 | 《中华人民共和国数据安全法》（2021年9月1日施行） | `knowledge/01-data-security-law.md` |
| 二 | 《中华人民共和国网络安全法》（2017年6月1日施行） | `knowledge/02-cybersecurity-law.md` |
| 三 | 《中华人民共和国个人信息保护法》（2021年11月1日施行） | `knowledge/03-personal-info-protection.md` |
| 四 | 《中华人民共和国政府采购法》（2014年修正） | `knowledge/04-government-procurement.md` |
| 五 | 《中华人民共和国民法典·合同编》（2021年1月1日施行） | `knowledge/05-civil-code-contracts.md` |
| 六 | 《中华人民共和国反不正当竞争法》（2019年修正） | `knowledge/06-anti-unfair-competition.md` |
| 七 | 《中华人民共和国招标投标法》（2017年修正） | `knowledge/07-tendering-bidding.md` |
| 八 | 信息安全等级保护基本要求（等保2.0 / GB/T 22239-2019） | `knowledge/08-level-protection.md` |
| 九 | 通用数据保护条例（GDPR / EU 2016/679） | `knowledge/09-gdpr.md` |
| 十 | 《中华人民共和国个人信息保护法》跨境规则补充（2022年配套） | `knowledge/10-pip-cross-border.md` |
| 十一 | 《中华人民共和国劳动合同法》（2012年修正） | `knowledge/11-labor-contract.md` |
| 十二 | 《中华人民共和国反垄断法》（2022年修正） | `knowledge/12-antimonopoly.md` |
| 十三 | 《中华人民共和国电子商务法》（2019年1月1日施行） | `knowledge/13-e-commerce.md` |
| 十四 | 《中华人民共和国著作权法》（2020年修正） | `knowledge/14-copyright.md` |
| 十五 | 《中华人民共和国建筑法》（2019年修正）及《建设工程质量管理条例》（2019年修正） | `knowledge/15-construction-law.md` |
| 十六 | 金融行业合规专项（资管新规/商业银行法/反洗钱法） | `knowledge/16-financial-compliance.md`
## 🔍 知识库使用规则

1. **优先检索**：执行"法规映射"步骤时，Agent 应首先在上述知识库中匹配相关法条，确保引用的条款编号与要点与知识库一致。
2. **精准引用**：风险条款映射表中的"对应法规"列应填写为 `《法规名称》第X条` 格式，并附核心要点（5-15字）。
3. **知识库外补充**：当用户指定的 `compliance_scope` 中包含知识库未收录的法规（如行业专项法规、地方法规等），Agent 应依据公开法律文本自行补充映射，并在输出报告中标注"⚠️ 以下法规未在内置知识库中，引用准确性请人工复核"。
4. **版本标注**：输出报告中法规名称后应标注施行日期或修正版本（如：《政府采购法》（2014年修正）），以便用户确认时效性。
5. **更新提示**：法规知识库基于发布日截面的法律文本编制，如遇法规修订，Agent 应在报告中提示"⚠️ 该法规可能有最新修订，建议核实当前有效版本"。
