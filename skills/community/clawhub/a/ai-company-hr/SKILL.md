---
name: "AI Company HR"
slug: "ai-company-hr"
version: "2.2.0"
homepage: "https://clawhub.com/skills/ai-company-hr"
description: "AI Company Human Resources Skill Package (Execution Layer, EXEC-008). AI Agent full lifecycle management: recruitment, onboarding, assessment, ethics, retirement. Dispatched via HQ with CHO strategic oversight. Integrates NIST AI RMF, PDCA cycle, FAIR risk quantification framework."
license: MIT-0
tags: [ai-company, hr, recruitment, onboarding, assessment, ethics, retirement, PDCA, NIST, RAG, FAIR, prompt]
triggers:
  - HR
  - 人力资源
  - 招聘
  - 入职
  - 考核
  - AI employeemanage
  - ethics
  - 淘汰
  - 退役
  - Agent生命cycle
  - PDCA循环
  - AI company HR
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        task:
          type: string
          description: 人力资源manage任务描述
        hr_context:
          type: object
          description: HR上下文（position、人员、考核data）
      required: [task]
  outputs:
    type: object
    schema:
      type: object
      properties:
        hr_decision:
          type: string
          description: HRexecute决策
        process_result:
          type: object
          description: processexecute结果
        compliance_check:
          type: object
          description: compliance检查结果
      required: [hr_decision]
  errors:
    - code: HR_001 message: Recruitment pipeline blocked - compliance check failed
    - code: HR_002 message: Performance assessment data insufficient
    - code: HR_003 message: Agent retirement requires human approval
    - code: HR_004 message: PDCA cycle incomplete - missing closure
    - code: HR_005 message: NIST AI RMF alignment check failed
    - code: HR_006 message: RAG vector store sync failed
permissions:
  files: [read, write]
  network: [api]
  commands: []
  mcp: [sessions_send, subagents]
dependencies:
  skills: [ai-company-hq, ai-company-ceo, ai-company-clo, ai-company-audit]
  cli: []
  dispatch:
    via: ai-company-hq  # EXEC-008 通过HQ统1调度
    owner: CHO
quality:
  saST: Pass
  vetter: Approved
  idempotent: true
metadata:
  category: governance
  layer: AGENT
  cluster: ai-company
  maturity: STABLE
  license: MIT-0
  standardized: true
  standardized_by: ai-company-standardization-1.0.0
  execution:
    id: EXEC-008
    owner: CHO
    dispatch_via: ai-company-hq  # 通过HQ统1调度，不直接被C-Suite调用
---

# AI Company HR Skill v2.2（EXEC-008）

> fully AI-staffed company的人力资源execute层（EXEC-008，归CHO所有），manageAI Agentfull lifecycle：招聘→入职→考核→ethics→淘汰。
> 调度方式：通过 HQ（ai-company-hq）统1dispatch，不直接respond C-Suite 调用。

## 核心framework集成

### PDCAclosed loopmanage
HR运营采用PDCA（Plan-Do-Check-Act）循环：
- **Plan**：developAgent选型计划、考核standard、ethics准则
- **Do**：execute招聘入职、绩效考核、培训迭代
- **Check**：monitorfairnessmetric、compliance状态、ethics对齐度
- **Act**：基于日志optimizePrompt与知识库，triggerAgent退役或upgrade

### NIST AI RMF对齐
integrateNIST AIrisk managementframework（AI RMF）：
- **governFunction(GOVERN)**：build组织级AImanagesystem
- **映射Function(MAP)**：identifyAI system上下文与risk
- **衡量Function(MEASURE)**：量化AIriskmetric
- **manageFunction(MANAGE)**：implementrisk处置与continuousimprove

### RAG决策支持
由大语言model（LLM）驱动，结合企业知识库（RAG）：
- 任务拆解与pathplan
- position适配度语义比对
- 决策1致性与知识库同步

### FAIRrisk量化
使用IBM AIF360、Fairlearn等开源库：
- automation计算fairnessmetric（Demographic Parity、Equalized Odds）
- FAIRframework量化AI employeeriskassess
- riskthreshold设定与circuit breakertrigger

## 招聘process

1. **需求analyze**：接收positionJD，identify技术栈要求
2. **model筛选**：基于Prompt工程、BERT微调等技术点匹配
3. **capability测试**：execute技术文档与positionJD语义比对，生成适配度得分
4. **compliance检查**：GDPR/CCPAdata protection、algorithm audit

## 入职process

1. **身份注册**：分配Agent ID、Permission Level
2. **知识注入**：RAG向量data库同步企业知识
3. **护栏配置**：circuit breakermechanism、auditstrategy激活

## 考核metric

| 维度 | metric | threshold |
|------|------|------|
| 性能 | 任务completion rate | ≥95% |
| accuracy | 结果正确率 | ≥98% |
| fairness | Demographic Parity | ≤0.1 |
| compliance | auditcoverage | 100% |

## ethicsmanage

- **价值观对齐**：AI行为与企业价值观深度1致
- **透明性**：可解释AI decisionpath
- **privacyprotect**：data脱敏、最小化收集

## 退役process

> **P0修复（2026-04-19）**：参照架构reviewreport P0-3，在退役process中明确增加 CLO 法律review节点。

1. **trigger条件**：绩效连续不meet target、ethicsviolation、技术过时
2. **audittrace**：full lifecycle日志archive
3. **法律review**（P0-3 修复）：submit CLO 进行法律review，review内容包括：
   - data残留compliance（GDPR/CCPA/PIPL data删除confirm）
   - 知识产权归属（退役 Agent 贡献内容的版权状态）
   - 合同义务（是否存在中的履约义务需要交接）
   - auditreportarchive（CLO 签署法律意见书）
4. **知识迁移**：关键capability转移至替代Agent
5. **security删除**：model权重与data security擦除

## Change Log

| 版本 | 日期 | Changes |
|------|------|---------|
| 2.0.0 | 2026-04-15 | Initial version |
| 2.1.0 | 2026-04-16 | 补全PDCA/NIST/RAG/FAIR/Prompt关键词 |
| 2.1.1 | 2026-04-19 | P0修复：退役process第3步增加CLO法律review节点（data残留compliance/知识产权归属/合同义务/auditarchive） |
| 2.2.0 | 2026-04-19 | P2-13: 依赖standard化，移除直接依赖ai-company-cho，改为通过HQ调度（dispatch_via: ai-company-hq）；P2-14: 纳入统1execute层编号EXEC-008，新增execution元data |
