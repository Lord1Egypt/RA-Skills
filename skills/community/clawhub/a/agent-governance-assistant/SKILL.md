---
name: "Agent Governance Assistant"
slug: agent-gov
description: "UPDATED 2026: Covers China AI Agent governance regulations (generative AI regulations), MCP protocol governance implications, and enterprise AI audit frameworks. AI-powered enterprise AI agent governance framework — audit agent behavior, enforce security policies, ensure CBIRC/CFCA compliance, detect shadow AI, and generate governance reports. Built for IT risk managers, compliance officers, and enterprise AI leaders in financial institutions. Keywords: AI agent governance, enterprise AI, agent compliance, AI security policy, CBIRC, CFCA, shadow AI detection, agent audit, Microsoft Agent 365, Copilot Studio, China AI regulation, Agent治理, 企业AI, AI合规, 影子AI检测, AI审计, NFRA AI合规, AI治理."
version: "4.0.1"
---

# Agent Governance Assistant


### AI技术最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| AI技术 | 2026年MCP标准治理升级至Linux Foundation AAIF | Agent治理框架需纳入MCP标准化和AAIF治理要求 |
| AI技术 | AI Agent治理框架持续演进，需关注权限控制和审计日志 | Agent治理框架需纳入MCP标准化和AAIF治理要求 |
| AI技术 | 企业AI治理要求提升：可解释性、公平性、隐私保护合规 | Agent治理框架需纳入MCP标准化和AAIF治理要求 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Overview

A comprehensive AI-powered framework for governing enterprise AI agents — from audit trails and policy enforcement to regulatory compliance and risk reporting. As enterprise AI agents (Microsoft Agent 365, Copilot Studio, custom agents) proliferate, governance has become the #1 blocker to adoption. This skill bridges the gap between AI capability and enterprise control.

## Title

**Enterprise AI Agent Governance Framework** — Audit · Secure · Comply

## Triggers

- "agent governance" / "AI agent管理" / "代理治理"
- "enterprise AI compliance" / "企业AI合规"
- "shadow AI detection" / "影子AI排查"
- "AI policy enforcement" / "AI策略执行"
- "agent audit trail" / "代理审计日志"
- "Microsoft Agent 365 governance" / "Agent 365治理"
- "AI risk report" / "AI风险报告"
- "Copilot Studio compliance" / "Copilot合规"
- "China AI regulation" / "中国AI监管"
- "CBIRC AI guidance" / "银保监会AI指引"

---

### 0. 2026 企业AI Agent治理最新趋势

| 时间 | 动态 | 治理含义 |
|------|------|---------|
| **2025年7月** | 中国《生成式人工智能服务管理暂行办法》正式施行 | AI Agent服务纳入互联网信息服务管理，算法备案要求扩展至Agent |
| **2025年11月** | MCP协议移交Linux Foundation | AI Agent工具集成标准化带来新的审计盲点，需纳入治理范围 |
| **2026年1月** | NFRA召开2026年监管工作会议，AI治理列为重点 | 金融行业AI Agent应用监管框架加速制定 |
| **2026年** | Microsoft Agent 365/Copilot Studio企业大规模部署 | Agent行为审计、数据隔离、权限管控成为合规核心 |
| **2026年** | 影子AI检测升级：从API监控到行为分析 | 传统DLP监控不足，需引入UEBA（用户实体行为分析）技术 |

> **2026年核心治理挑战：** 企业AI Agent数量激增（从10个→100+），传统Agent Inventory已无法满足监管要求。建议采用"零信任Agent架构"——每个Agent独立身份认证、最小权限、数据隔离、完整审计日志。

---

## Workflow

### Phase 1 — Agent Inventory Discovery

**Step 1.1: Scan for Active AI Agents**

Generate a structured inventory of all AI agents in the enterprise environment.

**Input required:**
- List of known AI platforms in use (e.g., Microsoft 365 Copilot, Salesforce Einstein, custom LangChain agents, RPA bots)
- Department ownership mapping
- API endpoints or integration points

**Output: Agent Inventory Table**

| Agent ID | Platform | Owner | Department | Capabilities | Data Access Level | Last Active |
|----------|----------|-------|------------|--------------|-------------------|------------|
| AG-001 | Microsoft Agent 365 | IT Admin | Finance | Email drafting, meeting prep | Full mailbox | 2026-05-07 |

**Step 1.2: Classify Agent Risk Level**

Assign risk tier (Low / Medium / High / Critical) based on:
- Data sensitivity (PII, financial, health, IP)
- External interaction (internet, customers, third parties)
- Autonomy level (advisory only → full automation)
- Regulatory exposure (CBIRC, CFCA, personal information protection)

**Risk Classification Matrix:**

| Tier | Criteria | Example | Audit Frequency |
|------|----------|---------|----------------|
| Critical | Customer-facing + financial data + high autonomy | AI underwriting agent | Weekly |
| High | Internal + sensitive data + medium autonomy | AI claims processor | Monthly |
| Medium | Internal + general data + advisory only | AI meeting summarizer | Quarterly |
| Low | Internal + no sensitive data | AI email categorizer | Bi-annual |

---

### Phase 2 — Policy Framework Design

**Step 2.1: Define Governance Policies**

Generate tailored governance policies based on enterprise type and regulatory context.

**For China Financial Institutions (CBIRC/CFCA):**
```
POLICY: CFCA-AI-001 — Agent Data Minimization
All AI agents must process only minimum necessary personal data.
Agents cannot retain PII beyond the transaction completion window.
Annual data audit required.

POLICY: CBIRC-AI-007 — Model Transparency
All AI-assisted decisions in underwriting/claims must provide
human-override capability and explainability documentation.

POLICY: AI-ENTERPRISE-003 — Agent Registration
All production AI agents must be registered in the Enterprise
Agent Registry with documented purpose, data scope, and owner.
Unregistered agents are prohibited from accessing customer data.
```

**Step 2.2: Policy Compliance Checker**

For each registered agent, evaluate against all applicable policies.

**Input:** Agent inventory + policy list
**Output:** Compliance gap matrix with severity scores

---

### Phase 3 — Shadow AI Detection

**Step 3.1: Identify Unauthorized Agent Usage**

Scan for signs of shadow AI — employees using personal AI tools on corporate data.

**Detection indicators:**
- Third-party AI API calls from corporate networks (non-approved domains)
- AI tool usage logs in DLP (Data Loss Prevention) systems
- Browser extensions accessing corporate APIs
- Unsanctioned Zapier/Make/n8n workflows connecting to company data

**Output:** Shadow AI Exposure Report

| Finding | Risk Level | Data at Risk | Recommended Action |
|---------|-----------|-------------|-------------------|
| Employee using free ChatGPT API for customer email drafting | CRITICAL | Customer PII + contract terms | Immediate block + compliance training |
| Unsanctioned n8n workflow syncing CRM to personal AI tool | HIGH | Contact data + deal values | Replace with approved integration |

---

### Phase 4 — Audit Trail & Reporting

**Step 4.1: Generate Governance Audit Report**

Produce a structured audit report for internal risk committees and external regulators.

**Report Sections:**
1. Executive Summary (1 page)
2. Agent Inventory & Risk Classification
3. Policy Compliance Scorecard
4. Shadow AI Findings
5. Open Risks & Remediation Roadmap
6. Appendix: Agent Decision Logs (sample)

**Step 4.2: Generate Regulatory Filing**

Format findings as a CBIRC/CFCA-compliant governance disclosure.

---

## Input / Output Examples

### Example 1: Enterprise Agent Audit

**Input:**
```
We have 12 AI agents across Finance, Claims, and Sales departments.
Recent CBIRC guidance requires quarterly AI governance reporting.
We discovered 3 employees using personal AI tools for work tasks.
```

**Output:**
```
## Phase 1: Agent Inventory
[Structured table of 12 agents with risk tiers]

## Phase 2: Policy Gap Analysis
- 4 agents non-compliant with CFCA-AI-001 (data minimization)
- 2 agents lack human-override capability (CBIRC-AI-007)
- 6 agents unregistered (AI-ENTERPRISE-003 violation)

## Phase 3: Shadow AI Findings
[Shadow AI report with 3 findings]

## Phase 4: Compliance Score — 58/100
Recommended actions prioritized by risk.

## Report ready for CBIRC Q2 submission.
```

### Example 2: Microsoft Agent 365 Governance Setup

**Input:**
```
We are deploying Microsoft Agent 365 across 200 users.
IT needs to configure governance controls before go-live.
Finance and Claims departments need different permission levels.
```

**Output:**
```
## Agent 365 Governance Configuration

### Recommended Permission Matrix
| Department | Agent Capabilities | Data Scope | Human-in-Loop | Audit Level |
|------------|-------------------|------------|---------------|-------------|
| Finance | Report generation, variance analysis | Financial data only | Required for >¥100K | Full |
| Claims | Document review, fraud flag | Claims data | Required for >¥10K | Full |
| Sales | Lead scoring, email drafting | CRM data | Advisory only | Standard |

### Governance Policies to Enable
1. Data Loss Prevention (DLP) rules for PII in agent prompts
2. Agent activity logging to Sentinel/Log Analytics
3. Approval workflows for high-stakes agent actions
4. Monthly governance review dashboard

### Shadow AI Pre-emption
Block list: [personal-ai-tool-1.com, ai-tool-free.xyz]
Allow list: [Copilot, Agent 365, approved-vendor-ai.com]
```

---

## Notes & Best Practices

1. **Start with inventory before policy.** You cannot govern what you cannot see.
2. **China-specific:** For CBIRC/CFCA regulated entities, always include PIPL (个人信息保护法) compliance in the policy framework. Agents processing insurance claims data are subject to strict data minimization requirements.
3. **Human-in-the-loop is non-negotiable** for any agent making or materially influencing financial decisions.
4. **Shadow AI is the #1 undetected risk** — prioritize network-level API monitoring.
5. **Update agent registry quarterly** — AI agent proliferation is fast; stale inventories create blind spots.
6. **Leverage Microsoft Purview** for data classification feeding into agent governance policies.
7. **Regulatory alignment:** Check current CBIRC AI guidance, CFCA fintech guidelines, and the generative AI regulation framework when generating policies.

---

*Author: @gechengling | Skill: agent-governance-assistant | clawhub.ai/gechengling/agent-governance-assistant*
