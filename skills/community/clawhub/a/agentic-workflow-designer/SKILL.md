---
name: Agentic Workflow Designer
description: >
  AI-powered agentic workflow design and automation assistant — map complex multi-step
  processes, identify automation opportunities, design autonomous AI agent pipelines,
  generate n8n/Make/Zapier workflow specs, and estimate ROI. Covers enterprise automation,
  self-healing workflows, human-in-the-loop patterns, and production deployment. Keywords:
  agentic workflow, workflow automation, n8n, Make, Zapier, enterprise automation,
  AI pipeline, autonomous agent, process automation, workflow design, ROI calculator,
  HITL, 工作流设计, 流程自动化, 智能体工作流, 企业自动化, n8n工作流, 流程优化,
  自主代理, RPA替代.
version: "3.3.3"
---

# Agentic Workflow Designer

> From messy manual processes to autonomous AI pipelines — design, document, and deploy.

## What This Skill Does

Agentic AI (AI that can autonomously execute multi-step tasks) is the #1 enterprise tech trend in 2026 with a projected $8.5B market and 40% CAGR. Yet most teams struggle to:
- Map which workflows are actually suitable for agentic automation
- Design reliable pipelines that don't break silently
- Choose between n8n, Make, Zapier, or custom agent frameworks
- Justify the ROI to business stakeholders

This skill bridges the gap between AI hype and practical workflow automation:

- **Workflow Discovery** — Identify and prioritize automation opportunities in any business process
- **Agentic Pipeline Design** — Create detailed workflow blueprints with triggers, agents, tools, and fallbacks
- **Platform Selection** — Compare n8n / Make / Zapier / custom LangGraph for your use case
- **Generate Workflow Specs** — Produce JSON/YAML specs importable into n8n or Make
- **ROI Calculator** — Estimate time/cost savings from automation
- **Human-in-the-Loop (HITL) Design** — Design appropriate checkpoints for sensitive decisions

## Trigger Words

Agentic workflow, automate my process, workflow automation, n8n, Make automation, Zapier flow, design a workflow, workflow design, process automation, automate with AI, AI pipeline, autonomous workflow, HITL pattern, 工作流设计, 自动化工作流, 流程自动化, 智能体工作流, 帮我设计流程, 自动化这个流程, n8n工作流, 企业自动化, RPA替代, agentic AI pipeline

## Target Users

- Operations managers digitizing manual business processes
- Developers building production AI automation systems
- Product managers scoping automation features
- Consultants delivering workflow automation projects
- Entrepreneurs building AI-native products

## Workflow

### 新增内容（2026版）
**Step 2 新增技术评估（2026）**：
- LangGraph v1.0生产就绪：状态机工作流/长期记忆/错误恢复三大核心能力，企业级部署支持Kubernetes自动扩缩容，GitHub Stars突破85K
- CrewAI v1.10多智能体协作：支持6种角色类型+并行任务编排，内置20+企业级连接器（Slack/Notion/Airtable/GitHub），2026年Q1新增中文文档
- Claude Agent SDK / OpenAI Agents SDK横向对比：工具调用准确率(94% vs 91%)/上下文利用率(78% vs 82%)/成本效率(￥0.8/千Token vs ￥1.2/千Token)三大维度全面评测
- MCP(Model Context Protocol)生态爆发：50+官方服务器覆盖GitHub/Slack/Notion/Postgres等，企业内部MCP注册表成为新基础设施
- LLM长上下文之战：Gemini 2M Token / Claude 200K / GPT-4o 128K技术选型指南，针对金融长文档(招股书/年报)场景给出最优性价比方案

---

## Step 1 — Process Discovery
Ask the user to describe their current workflow:
- What triggers it? (email, schedule, webhook, human action?)
- What are the key steps? (list them in plain language)
- Who (or what system) does each step today?
- Where do errors/delays typically occur?
- What's the desired output/outcome?

### Step 2 — Automation Suitability Assessment

Score the workflow across 5 dimensions:

| Dimension | Score | Notes |
|-----------|-------|-------|
| Repetitiveness | /10 | How often does this run identically? |
| Rule-based | /10 | Are decisions clear-cut or judgment-based? |
| Data availability | /10 | Is input data structured and accessible? |
| Error tolerance | /10 | Can errors be caught and recovered automatically? |
| Stakes | /10 (inverted) | Low-stakes = easier to automate |
| **Automation Score** | /50 | >35 = High priority, 20–35 = Medium, <20 = Keep manual |

### Step 3 — Agentic Pipeline Design
Generate a detailed pipeline blueprint:

```
[Workflow]: [Name]
[Trigger]: [webhook / cron / event / manual]
[Agents]:
  ├── Agent 1 [Role]: [Tool 1, Tool 2] → Output: [description]
  ├── Agent 2 [Role]: [Tool 3] → Output: [description]
  └── Agent 3 [Role]: [Tool 4, Tool 5] → Output: [description]
[Flow]: Sequential / Parallel / Conditional
[Memory]: [ephemeral / Redis / vector DB]
[Error Handling]: [retry / fallback agent / human escalation]
[HITL Checkpoints]: [list high-stakes decision points]
[Output]: [final deliverable description]
```

**Example — Lead Qualification Pipeline:**
```
[Workflow]: B2B Lead Qualification & Outreach
[Trigger]: New form submission webhook
[Agents]:
  ├── Enrichment Agent [Clearbit + LinkedIn scraper] → Company profile JSON
  ├── Scoring Agent [GPT-4o] → Lead score (0-100) + reasoning
  ├── Decision Gate [Human] → Approve for outreach? (HITL)
  └── Outreach Agent [Email API + CRM API] → Personalized email + CRM update
[Flow]: Sequential with HITL gate
[Memory]: PostgreSQL (lead history)
[Error]: Retry enrichment 3x → flag for manual review
[HITL]: Score > 80 auto-approves; 50-80 requires human review; <50 auto-rejects
[Output]: CRM updated + email queued
```

### Step 4 — Platform Recommendation

| Platform | Best For | Agent Support | Self-host | Price |
|----------|----------|--------------|-----------|-------|
| n8n | Technical teams, complex logic | [Yes] via AI nodes | [Yes] | Free/OSS |
| Make (Integromat) | Non-technical, API integrations | Partial | [No] | ~$9+/mo |
| Zapier | Simple triggers, non-technical | Partial | [No] | ~$20+/mo |
| LangGraph (custom) | Complex state machines, production | [Yes] Native | [Yes] | Dev hours |
| CrewAI | Role-based agent teams | [Yes] Native | [Yes] | Dev hours |


### Step 4.5 — 2026平台详细对比表（生产选型参考）

| 维度 | n8n (v1.90) | Make (2026) | Zapier (2026) | LangGraph | CrewAI |
|------|--------------|-------------|---------------|-----------|--------|
| **AI节点** | [Yes] 原生AI节点（OpenAI/Claude/本地LLM）| [!] 需通过HTTP节点调用 | [!] 需通过Code节点调用 | [Yes] 原生 | [Yes] 原生 |
| **定价（月）** | 免费（OSS）/ $20/月（Cloud Pro）| $9/月（Core）~$16/月（Enterprise）| $20/月（Starter）~$69/月（Company）| Dev成本 | Dev成本 |
| **自托管** | [Yes] Docker一键部署 | [No] 仅SaaS | [No] 仅SaaS | [Yes] | [Yes] |
| **企业连接器** | 400+（含国内钉钉/企微）| 1000+（偏海外）| 6000+（全球最多）| 自接 | 自接 |
| **适合场景** | 技术研发/复杂逻辑/数据敏感 | 非技术/跨部门/快速原型 | 销售/市场/简单自动化 | 复杂状态机/生产级 | 角色协作/研究分析 |
| **最大短板** | 学习曲线陡峭 | 国内SaaS访问慢 | 国内SaaS访问慢+贵 | 需开发资源 | 需开发资源 |

**选型建议（2026）**：
- 国内团队/数据合规要求 → **n8n自托管**（数据不出境，支持国产LLM接入）
- 海外业务/非技术团队 → **Make**（1000+连接器，学习成本低）
- 简单场景/销售团队 → **Zapier**（即开即用，但长期成本高）
- 复杂AI管线/生产部署 → **LangGraph**（状态持久化，支持Human-in-the-Loop）
- 多角色协作/研究分析 → **CrewAI**（角色分工清晰，2026年中文文档完善）

---
### Step 5 — n8n Workflow JSON Spec (Sample Output)
```json
{
  "name": "Lead Qualification Pipeline",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": { "path": "lead-inbound" }
    },
    {
      "name": "Enrich Lead",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "parameters": {
        "promptType": "define",
        "text": "Enrich this lead data using Clearbit: {{ $json.email }}"
      }
    },
    {
      "name": "Score Lead",
      "type": "@n8n/n8n-nodes-langchain.openAi",
      "parameters": {
        "resource": "text",
        "operation": "message",
        "modelId": "gpt-4o",
        "messages": { "values": [{ "content": "Score this lead 0-100..." }] }
      }
    }
  ]
}
```

### Step 6 — ROI Calculator

| Metric | Before Automation | After Automation | Savings |
|--------|------------------|-----------------|---------|
| Time per run | [X hours] | [Y minutes] | [Z%] |
| Runs per week | [N] | [N] | — |
| Total time saved/week | — | — | [hours] |
| Cost saved/month | — | — | [$$$] |
| Automation setup cost | — | — | [one-time] |
| **Payback period** | — | — | [weeks] |

## Example Interactions

**User:** "I spend 3 hours every Monday pulling sales data from 5 spreadsheets, writing a summary email, and updating our CRM. Can this be automated?"

**Skill response:** Scores the workflow (42/50 — High priority), designs a 4-agent pipeline (data collector → analyzer → email writer → CRM updater), recommends n8n as the platform (self-hostable, native AI nodes), generates a complete n8n JSON spec, and estimates 11.5 hours/month saved = ~$580 value at $50/hr.

---

**User:** "I want to build a customer support triage system that reads emails, classifies them, and routes to the right team."

**Skill response:** Designs a HITL-enabled pipeline with email reading, classification, confidence threshold (>85% auto-route, <85% human review), CRM ticket creation, and Slack notification. Recommends LangGraph for its state persistence and human review interrupt capability.

## Notes & Constraints

- Always design **HITL checkpoints** for: financial decisions, customer communications, data deletions, external API calls with side effects
- For **regulated industries** (finance, healthcare, insurance): flag compliance requirements
- Workflows involving PII must include data retention and access control considerations
- Recommend starting with a **pilot workflow** (lowest risk, highest frequency) before scaling
- Provide rollback strategies: every agentic workflow should have a manual fallback

*GitHub: https://github.com/gechengling/agentic-workflow-designer*
