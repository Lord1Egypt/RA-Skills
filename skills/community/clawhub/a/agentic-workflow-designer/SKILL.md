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
version: "3.3.9"
---

# Agentic Workflow Designer

> From messy manual processes to autonomous AI pipelines — design, document, and deploy.

> **⚠️ CAPABILITY NOTICE / 能力说明**
> - **Type:** Design and advisory framework — produces workflow blueprints, JSON/YAML specs, and ROI estimates as reference material
> - **No code is executed by this skill**; generated specs are for the user to review and import into their own environment
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs require human review before production deployment**
> - Workflows touching PII or regulated data must include retention, access control, and audit considerations

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

### 平台与技术动态（截至 2026-11-24）

**2026-08 更新要点**：
- **MCP 成为事实标准**：Model Context Protocol 于 2025 年底转入 Linux 基金会中立治理后，2026 年官方与社区服务器数量持续扩张，企业内部 MCP 注册表逐步成为新的基础设施层。
- **国内合规要求趋严**：涉及个人信息与重要数据的工作流，需满足最小必要采集、境内存储与可审计要求，自托管方案的优先级上升。
- **长上下文成本下探**：长文档场景（招股书、年报、长合同）的单位 Token 成本持续下降，使得"全文入参 + 结构化抽取"逐步替代早期分段检索方案。
- **可观测性成为刚需**：生产级 agentic 工作流普遍补齐链路追踪、成本归因与失败重放能力，缺乏可观测性的方案难以通过投产评审。
- **[2026-09 新增] 从"能不能跑"转向"能不能管"**：试点期关注功能实现，规模化后真正的瓶颈变成命名规范、版本管理、灰度发布与故障定位，设计阶段就要预留这些能力。
- **[2026-09 新增] 选型标准从跑分转向可控性**：受监管行业（金融、医疗、政务）更看重私线部署、数据不出境与审计留痕，模型跑分高不再是唯一决策依据。
- **[2026-09 新增] 成本归因细化到工作流**：单位 Token 成本需要能分摊到具体工作流与具体节点，否则规模化后无法判断哪些流程值得继续投入。
- **[2026-09-24 新增] 智能体身份与权限被单独治理**：工作流里的 agent 逐步被当作"非人类身份"管理，需要独立的凭据、最小权限与回收机制，共用一把管理员 Key 的做法在审计中难以通过。
- **[2026-09-24 新增] 评测集先于优化**：团队在实践中发现，没有评测集就做提示词调优等于盲调；先用 30-100 条真实样本建最小评测集，再谈优化，成为投产前的默认动作。
- **[2026-09-24 新增] 失败重放成为交付标准**：无法复现失败现场的工作流在验收时被直接打回，输入、输出、版本、耗时、成本五项留痕被视为最低要求。

**本期新增观察（截至 2026-11-24）**

| 维度 | 变化 | 对流程设计的意义 | 落地动作 | 可信度标注 |
|------|------|----------------|
| 治理 | 企业内部 MCP 注册表从"可选"变为"基础件"，工具接入需统一登记与权限控制 | 设计时把工具来源收敛到注册表，避免各流程各接一套 | 建立工具清单与负责人，禁止流程内硬编码凭据 | 以官方最新发布为准 |
| 运维 | 工作流数量增长后，命名与版本混乱成为主要故障源 | 约定命名规范与语义化版本，变更需留 changelog | 采用"业务域-动作-对象-版本"命名，变更走评审 | 以官方最新发布为准 |
| 成本 | 成本归因要求下沉到节点级 | 每个节点标注预期调用量与成本上限，超限告警 | 为高成本节点设单日预算与熔断 | 以官方最新发布为准 |
| 合规 | 涉及个人信息与重要数据的流程需满足最小必要与可审计 | 在蓝图阶段即标注数据分类与留存期限 | 数据分类标签前置到 Step 1 盘点表 | 以官方最新发布为准 |
| 身份 | agent 作为"非人类身份"需独立凭据与最小权限 | 共用管理员凭据的做法不可审计 | 一个工作流一套凭据，定期轮换与回收 | 以官方最新发布为准 |
| 评测 | 最小评测集成为投产前置条件 | 没有评测集就调优等于盲调 | 先建 30-100 条真实样本的最小评测集 | 以官方最新发布为准 |

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

**示例：报销流程的 Step 1 拆解（访谈 → 结构化盘点）**

| 子步骤 | 执行人 | 输入 | 输出 | 耗时 | 是否需判断 | 系统 |
|-------|-------|------|------|------|-----------|------|
| 提交发票与事由 | 员工 | 发票影像 | 报销单 | 3 分钟 | 否 | OA |
| 发票真伪校验 | 财务 | 发票号码 | 校验结果 | 5 分钟 | 否（规则明确） | 税务接口 |
| 预算占用查询 | 财务 | 部门+科目 | 可用余额 | 4 分钟 | 否 | ERP |
| 超标准判断 | 财务主管 | 报销单+标准 | 通过/驳回 | 8 分钟 | **是**（需解释） | 人工 |
| 领导审批 | 部门负责人 | 报销单 | 签字 | 不定 | **是**（担责） | OA |
| 付款 | 出纳 | 审批单 | 付款凭证 | 5 分钟 | 否 | 资金系统 |

**访谈关键问题（用于发现隐性规则）**
- 哪些步骤你会凭经验"感觉不对"？——这一步通常隐含未写明的规则。
- 上一次出错是怎么发现的？——说明现有校验缺口在哪。
- 哪些步骤你会跳过或补做？——说明流程设计与实际执行脱节。
- 拆解结论：6 个子步骤中 4 步可自动化、2 步（超标准判断、领导审批）必须保留人工，与后续 Step 2 打分结论一致。


### Step 2 — Automation Suitability Assessment

Score the workflow across 5 dimensions:

| Dimension | Score | 判断依据 | 打分示例（周报自动化） | 打分示例（客户投诉处理） | 低分时的拆解建议 |
|-----------|-------|---------|---------------------|----------------------|
| Repetitiveness | /10 | How often does this run identically? | 9（每周一次，步骤固定） | 4（内容差异大） | 拆出"固定格式部分"单独自动化 |
| Rule-based | /10 | Are decisions clear-cut or judgment-based? | 8（汇总规则明确） | 3（需人工判断责任与情绪） | 把判断拆为"分类"与"处置"两步，只自动化分类 |
| Data availability | /10 | Is input data structured and accessible? | 8（5 张表结构固定） | 5（邮件正文非结构化） | 增加"结构化抽取"前置节点后再评 |
| Error tolerance | /10 | Can errors be caught and recovered automatically? | 7（数字错误可在复核环节发现） | 4（误判会直接损害客户关系） | 增加复核节点与灰度放行，提升容错后再评 |
| Stakes | /10 (inverted) | Low-stakes = easier to automate | 8（内部参考，出错影响小） | 2（涉及对外承诺与赔偿） | 高风险部分保留人工，低风险子环节单独评分 |
| **Automation Score** | /50 | >35 = High priority, 20–35 = Medium, <20 = Keep manual | **40/50 → 高优先级** | **18/50 → 暂不自动化** |

**评分补充说明**
- **Stakes 为反向计分**：风险越高得分越低。涉及资金、对外承诺、数据删除的流程，即使前四项得分高，总分也会被拉低。
- **两例对照的意义**：周报自动化 40 分应直接推进；客户投诉处理 18 分不宜整体自动化，但可拆出"分类 + 路由"子环节单独自动化（该子环节约 32 分）。
- **拆解法**：整体分数偏低时，不要放弃，而是把流程拆到子步骤重新评分——大多数流程都存在可自动化的局部环节。

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

**Example — 保险理赔单据预审 Pipeline:**
```
[Workflow]: 理赔单据完整性预审
[Trigger]: 理赔系统上传事件（webhook）
[Agents]:
  ├── 分类 Agent [OCR + 规则表] → 单据类型与置信度
  ├── 校验 Agent [规则引擎] → 缺失项清单
  ├── 决策门 [规则 + 人工] → 通过 / 退回补件 / 转人工
  └── 通知 Agent [短信 API + 工单 API] → 补件提醒 + 工单创建
[Flow]: 先并行分类，后串行校验（Conditional）
[Memory]: PostgreSQL（单据状态机），不含原始影像
[Error]: OCR 置信度 < 0.85 → 强制转人工，不自动退回
[HITL]: 涉及拒赔、金额调整、个人信息变更的一律转人工；仅限"是否缺件"自动判定
[Output]: 预审结论 + 缺失项清单 + 工单号
```

**示例 — 监管报送数据校验 Pipeline（2026-09-24 新增）：**
```
[Workflow]: 报送数据口径校验与差错清单生成
[Trigger]: 每日定时任务（cron，T+1 凌晨）
[Agents]:
  ├── 抽取 Agent [SQL + 文件解析] → 原始报送数据集
  ├── 校验 Agent [规则库] → 差错项清单（含记录定位）
  ├── 归因 Agent [LLM] → 差错原因归类与整改建议
  └── 决策门 [人工] → 确认差错清单与整改责任人
[Flow]: 串行，校验后可并行归因
[Memory]: 仅保存差错摘要与规则版本，不落原始明细
[Error]: 规则库版本未对齐即中止，禁止带疑点报送
[HITL]: 任何涉及数据修改的动作必须人工确认；仅"生成差错清单"可自动
[Output]: 差错清单 + 归因建议 + 待确认事项
```

**三个示例的设计差异对比（2026-09-24 新增）：**

| 示例 | 风险等级 | 自动化边界 | HITL 位置 | 能否自动放行 |
|------|---------|-----------|----------|-------------|
| Lead Qualification | 低 | 全流程（除边缘分数） | 评分区间 50-80 | 能（>80 自动） |
| 理赔单据预审 | 高（受监管） | 仅完整性检查 | 拒赔/金额/信息变更 | 不能（客户权益相关一律人工） |
| 监管报送校验 | 高（合规） | 仅差错发现与归因 | 数据修改与对外报送 | 不能（对外报送须人工签发） |

**判断口诀的延伸**：自动化可以覆盖**判断过程**，但不应覆盖**责任归属**；对于受监管流程，
还要再加一句——**可以自动生成结论，但不能自动生成对外口径**。
- Lead Qualification 属**低风险、可容忍误判**场景，因此允许 80 分以上自动放行。
- 理赔预审属**受监管、不可自动决策**场景，自动化边界严格限定在"完整性检查"，任何影响客户权益的结论必须人工确认。
- 判断依据：自动化可以覆盖**判断过程**，但不应覆盖**责任归属**。

### Step 4 — Platform Recommendation

| Platform | Best For | Agent Support | Self-host | Price | 学习曲线 | 典型用例 | 主要风险 | HITL 实现成本 |
|----------|----------|--------------|-----------|-------|---------|---------|---------|
| n8n | Technical teams, complex logic | [Yes] via AI nodes | [Yes] | Free/OSS | 较陡 | 内部数据同步、单据预审、带审批的批处理 | 自托管需自行承担运维与升级 | 中（加等待节点 + 外部审批表） |
| Make (Integromat) | Non-technical, API integrations | Partial | [No] | ~$9+/mo | 平缓 | 跨 SaaS 数据流转、市场活动自动化 | 国内访问海外 SaaS 稳定性差 | 中（需外挂审批存储） |
| Zapier | Simple triggers, non-technical | Partial | [No] | ~$20+/mo | 最平缓 | 表单→通知、 CRM 字段回写 | 任务量上去后成本增长快 | 中高（复杂审批链难维护） |
| LangGraph (custom) | Complex state machines, production | [Yes] Native | [Yes] | Dev hours | 陡（需开发） | 长时间运行的对话式业务、需要中断恢复的流程 | 需自建可观测与灰度能力 | 低（原生 interrupt） |
| CrewAI | Role-based agent teams | [Yes] Native | [Yes] | Dev hours | 中等 | 研究分析、多角色报告生成 | 角色编排调试成本较高 | 中（需自行实现中断与恢复） |


### Step 4.5 — 2026平台详细对比表（生产选型参考）

| 维度 | n8n (v1.90) | Make (2026) | Zapier (2026) | LangGraph | CrewAI |
|------|--------------|-------------|---------------|-----------|--------|
| **AI节点** | [Yes] 原生AI节点（OpenAI/Claude/本地LLM）| [!] 需通过HTTP节点调用 | [!] 需通过Code节点调用 | [Yes] 原生 | [Yes] 原生 |
| **定价（月）** | 免费（OSS）/ $20/月（Cloud Pro）| $9/月（Core）~$16/月（Enterprise）| $20/月（Starter）~$69/月（Company）| Dev成本 | Dev成本 |
| **自托管** | [Yes] Docker一键部署 | [No] 仅SaaS | [No] 仅SaaS | [Yes] | [Yes] |
| **企业连接器** | 400+（含国内钉钉/企微）| 1000+（偏海外）| 6000+（全球最多）| 自接 | 自接 |
| **适合场景** | 技术研发/复杂逻辑/数据敏感 | 非技术/跨部门/快速原型 | 销售/市场/简单自动化 | 复杂状态机/生产级 | 角色协作/研究分析 |
| **最大短板** | 学习曲线陡峭 | 国内SaaS访问慢 | 国内SaaS访问慢+贵 | 需开发资源 | 需开发资源 |
| **可观测性** | [Yes] 执行历史与重放 | [!] 仅运行日志 | [!] 仅运行日志 | 需自建（LangSmith 等） | 需自建 |
| **人工介入（HITL）** | [!] 需手动加等待节点 | [!] 需手动加等待节点 | [!] 需手动加等待节点 | [Yes] 原生 interrupt | [!] 需自行实现 |
| **失败回滚** | 重跑单节点 | 重跑场景 | 重跑 Zap | 依赖检查点设计 | 依赖任务设计 |
| **国产化适配** | [Yes] 可接国产 LLM/私有化部署 | [No] | [No] | [Yes] 自行选型 | [Yes] 自行选型 |
| **审计留痕** | [Yes] 执行历史可导出 | [!] 日志留存期有限 | [!] 日志留存期有限 | 需自行落库 | 需自行落库 |
| **凭据治理** | [Yes] 凭据集中管理 | [!] 连接器各自持有 | [!] 连接器各自持有 | [Yes] 走环境变量/密钥管理 | [Yes] 走环境变量/密钥管理 |

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

| Metric | Before Automation | After Automation | Savings | 示例（周一销售周报） |
|--------|------------------|-----------------|---------|-------------------|
| Time per run | [X hours] | [Y minutes] | [Z%] | 3 小时 → 15 分钟 = 92% |
| Runs per week | [N] | [N] | — | 1 次 |
| Total time saved/week | — | — | [hours] | 2.75 小时 |
| Cost saved/month | — | — | [$$$] | 11.5 小时 × 50 元 ≈ 575 元 |
| Automation setup cost | — | — | [one-time] | 约 16 小时搭建 ≈ 800 元 |
| **Payback period** | — | — | [weeks] | **约 6 周** |
| 年度维护成本 | — | — | [one-time×比例] | 800 元 × 20% ≈ 160 元/年 |
| 净年化收益 | — | — | [$$$] | 575×12 − 800 − 160 ≈ 6,140 元/年 |

**ROI 计算注意事项**
- **只计入真实节省的时间**：若节省的时间并未转化为其他产出（例如员工只是多了空闲），不宜直接折算为现金收益，应改为"释放工时"表述。
- **必须计入运维成本**：工作流会因接口变更、页面改版而失效，建议按初始搭建成本的 15%-25%/年 计入维护。
- **隐性收益单独列示**：如响应时效提升、差错率下降，可用定性描述补充，不要强行货币化。
- **示例 2（客服工单分类路由）**：单次从 4 分钟降至 30 秒，日均 300 单 → 每日节省约 17.5 小时；但因需保留人工复核，净节省按 60% 折算更稳妥。

## 可观测性与灰度发布 / Observability & Rollout（2026-09-24 新增）

**最小可观测指标集（投产前必须能回答）**

| 指标 | 定义 | 用途 | 建议告警阈值 |
|------|------|------|-------------|
| 成功率 | 成功运行数 / 总运行数 | 判断流程是否健康 | 低于 95% 告警 |
| P95 耗时 | 95 分位运行时长 | 发现性能退化 | 超过基线 2 倍告警 |
| 单次成本 | 单次运行的模型与接口费用 | 成本归因 | 超过预算 1.5 倍告警 |
| 人工介入率 | 触发 HITL 的比例 | 判断自动化边界是否合理 | 超过 40% 需复盘阈值 |
| 失败重放成功率 | 重放能否复现原失败 | 验证留痕完整性 | 无法重放即视为不合格 |
| 数据留痕完整率 | 含输入/输出/版本/耗时/成本的记录占比 | 合规举证 | 要求 100% |

**灰度发布四步**
1. **影子运行**：只跑不落结论，输出与现状对照，验证差异率；
2. **小流量放行**：选低风险子集（如内部部门）先行，人工 100% 复核；
3. **阈值收紧再放开**：先用高阈值只放行最有把握的部分，逐步下调；
4. **随时可回滚**：保留手动开关与旧流程，回滚时间目标明确（示例：10 分钟内）。

> 灰度期间必须保留**新旧双轨对照**，否则无法判断自动化是否真的带来改善。

---

## 常见设计反模式 / Anti-Patterns

| 反模式 | 症状 | 后果 | 修正方式 | 早期检测信号 |
|-------|------|------|---------|
| 一步全自动 | 把含判断与担责的环节也交给模型自动放行 | 出错后责任无法归属，监管与客户均不可接受 | 拆出"可自动化的判断"与"必须人工的决策"，中间设 HITL 闸口 | 流程图上找不到任何人工节点 |
| 提示词即流程 | 用一段超长提示词描述整个业务流程 | 无法定位失败节点，改动一处影响全局 | 拆成多节点，每节点单一职责并单独可测 | 单个提示词超过一屏，且无人能说清中间态 |
| 无置信度阈值 | 模型输出直接落库 | 低置信结果被当成确定结论 | 设阈值：高置信自动、中置信人工复核、低置信拒绝并提示 | 数据库里没有置信度字段 |
| 静默重试 | 失败后自动重试到成功为止 | 掩盖系统性故障，成本失控 | 限制重试次数，超过即告警并保留失败现场 | 成功率长期 100% 但成本持续上升 |
| 不留痕 | 不记录模型输入输出 | 事后无法复盘，合规检查无法举证 | 全链路留痕，含输入、输出、版本、耗时、成本 | 出问题时无法回答"当时模型看到了什么" |
| 成本无上限 | 没有单次运行的成本约束 | 异常输入导致费用暴涨 | 设单次与单日成本上限，超限熔断 | 无法说出单条流程的月度成本 |

> **判断口诀**：自动化可以覆盖**判断过程**，但不应覆盖**责任归属**；可以加速**执行**，但不应消除**证据**。


## Example Interactions

**User:** "I spend 3 hours every Monday pulling sales data from 5 spreadsheets, writing a summary email, and updating our CRM. Can this be automated?"

**Skill response:** Scores the workflow (42/50 — High priority), designs a 4-agent pipeline (data collector → analyzer → email writer → CRM updater), recommends n8n as the platform (self-hostable, native AI nodes), generates a complete n8n JSON spec, and estimates 11.5 hours/month saved = ~$580 value at $50/hr.

---

**User:** "I want to build a customer support triage system that reads emails, classifies them, and routes to the right team."

**Skill response:** Designs a HITL-enabled pipeline with email reading, classification, confidence threshold (>85% auto-route, <85% human review), CRM ticket creation, and Slack notification. Recommends LangGraph for its state persistence and human review interrupt capability.

---

**User:** "我们的报销单据要先核对发票真伪、再查预算、最后领导审批，能不能全自动？"

**Skill response:** 先按五维打分——重复性 9、规则明确 7、数据可得 6、错误容忍 4、风险（反向）3，合计 **29/50 属中等**。给出结论：**不宜全自动**。建议拆为两段：发票真伪校验与预算占用查询可自动化（该子流程约 36 分），领导审批必须保留人工节点。技术上推荐 n8n 自托管（涉及财务数据与发票信息，数据不出境），并明确指出自动化边界应止于"为审批人提供核对结论"，不得代替审批签字。

---

**User:** "我有一份 200 页的年报，想自动抽取关键财务指标并生成摘要。"

**Skill response:** 评估后指出这是**长上下文单文档处理**场景，不是典型的多步骤工作流，无需引入 agent 编排。给出两条路径：① 长上下文模型全文入参 + 结构化抽取（实现快、成本可控，适合一次性或低频任务）；② 分段检索 + 抽取（适合高频批量）。提示关键风险：抽取结果必须保留**原文定位**（页码/段落），便于人工复核，避免模型生成的数字无法追溯。若涉及未公开信息，须先确认数据合规与使用授权。

---

**User:** "我们有 40 多个自动化流程了，现在最大的问题是不知道哪个挂了、哪个最烧钱，怎么治理？"

**Skill response:** 先指出这是**规模化运维问题，不是设计问题**，不要靠重写流程解决。给出三步治理：① 建立流程清单与命名规范（业务域-动作-对象-版本），并为每条流程标注负责人与成本上限；② 补可观测性——链路追踪 + 节点级成本归因 + 失败重放，优先覆盖资金相关与客户可见的流程；③ 建立分级告警与熔断，按"是否涉及资金/对外承诺"分级。提示关键取舍：治理投入应集中在**高影响流程**，不要 40 条流程平均用力；同时建议对长期无人使用、且无合规要求的流程做下线评估。


## 保存与外发前确认 / Save & Send Confirmation（2026-09-24 新增）

1. 工作流蓝图、JSON/YAML 规格、ROI 测算先在对话中完整展示，供用户逐段预览；
2. 用户明确确认后再写入文件或导入生产环境；未经确认不落盘、不导入；
3. 规格文件中不得包含真实凭据，凭据一律用环境变量占位符表示；
4. 落盘时一并记录：生成时间、平台版本、适用环境、审核人。

---

## 变更记录 / Changelog

| 版本 | 日期 | 变更摘要 |
|------|------|---------|
| 3.3.6 | 2026-09-24 | 新增监管报送校验示例与三示例自动化边界对比、可观测性最小指标集与灰度发布四步、保存确认流程；评分/平台/反模式表各新增维度列；ROI 表新增维护成本与净年化收益；平台动态更新至 2026-09-24 并新增 3 条观察与 2 行维度 |
| 3.3.5 | 2026-09-07 | 补充 2026 年平台治理与成本归因观察 |

---

## Notes & Constraints

- Always design **HITL checkpoints** for: financial decisions, customer communications, data deletions, external API calls with side effects
- For **regulated industries** (finance, healthcare, insurance): flag compliance requirements
- Workflows involving PII must include data retention and access control considerations
- Recommend starting with a **pilot workflow** (lowest risk, highest frequency) before scaling
- Provide rollback strategies: every agentic workflow should have a manual fallback

*GitHub: https://github.com/gechengling/agentic-workflow-designer*

## 本轮增量（2026-11-12）：复核维度与举例补充

> 本节为 2026-11-12 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Step 3 — Agentic Pipeline**：

- 为每个 Agent 节点登记「可调用工具白名单 + 参数校验 + 失败重试上限」，第 3 次工具超时即降级到人工队列而非无限重试，并记录降级原因。
- 对涉及资金、外发或数据导出的节点单列「爆炸半径」标签，未配置审批门与幂等键的设计稿不进入灰度发布清单。

**可观测性与灰度发布 / Observability**：

- 灰度指标除成功率外，增加「步骤数 / 任务」「工具错误率」「人工接管率」「单次任务成本」四项，任一相对基线恶化超阈值即回滚。
- 失败重放固定记录五元组（输入、输出、版本、耗时、成本）并附配置快照哈希，缺任一项视为不可复现、验收不通过。

### 新增复核维度表（2026-11-12）

> 本表新增「由谁执行 / 数据来源 / 风险等级 / 复核要点 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 回归集与发布卡点 | 工作流负责人 + CI | 事故样本 + 标注集 | 开发 / 保留集隔离、基线对比、风险阈值 | 高 | 设计蓝图参考，落地须按机构规范审批 |
| trace 与降级 | 运维 | 链路追踪 + 策略决策日志 | 模型版本、工具入参、审批门命中 | 中 | 导出前脱敏，个人数据不落盘 |

### 同类框架思路补强（全网择优吸收）

参考 2026 年生产级 Agent 可靠性实践，补强「可观测性与评测」模块：评测集先于优化（先写评测再看它失败），离线回归集纳入真实事故、工具失败与超时、权限与提示注入攻击、需澄清的模糊请求等高风险用例，并划分开发集与保留集。

每次提示词、模型或工具变更在 CI 跑确定性检查加判分套件，与固定基线对比并按风险阈值卡发布；生产侧以一次完整运行（trace）为最小调试单元，记录模型版本、提示词哈希、工具入参与策略决策，导出前脱敏；建立低分轨迹人工标注后回写回归集的闭环。护栏从提示词规则升级为「模型提议、确定性系统裁决」的策略即代码，按动作爆炸半径分级，不可逆动作须审批门。

### 适用边界 / 数据最小化 / 执行边界（本期补齐）

**适用边界**：本技能仅用于工作流自动化与智能体流程设计的方法论参考与结构拆解，输出为供具备相应资质人员复核的草稿；不构成对具体主体、标的或客户的最终结论、指令或承诺。超出该范围的场景（如实盘执行、自动审批、对外正式报送）不适用本技能，应转由相应业务系统与授权人员处理。

**数据最小化**：仅处理完成当前任务所必需的最小数据集；对可识别个人、账户、持仓、健康或未公开经营信息，优先脱敏、聚合或以标识符替代。不复制、不留存、不外传原始敏感数据；任何外部数据或服务的使用须以用户明确授权为前提，并保留可追溯的取数与复核留痕。

**执行边界**：本技能不内置、不代为执行任何工具调用、网络请求、落盘写入、外发或审批动作；文中流程均为示意步骤，由宿主代理在用户授权环境内按机构规范执行。涉及不可逆或高影响动作须经人工预览与确认，并保留输入、输出、版本、耗时与责任人的最小留痕；无人工确认环节不得自动推进。

### 时效性说明

- 本期时效性核查：**截至 2026-11-12**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-17）：复核维度与举例补充

> 本节为 2026-11-17 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Step 1 — Process Discovery**：

- 流程盘点表补「人工确认点」一列：每个步骤标注需要人工判断还是可按规则流转，判断依据缺项的按待补处理，草稿不替使用者决定自动化范围。
- 步骤清单新增「例外路径」占位：常态路径与至少一条例外分支并列，草稿只记录分支触发条件的描述，标注需人工复核后使用。

**可观测性与灰度发布 / Observability & Rollout**：

- 留痕清单补「五项要素」核对位：输入、输出、版本、耗时、成本逐项标注是否齐备，缺一项即标注证据不完整，不写入验收结论。
- 灰度对照新增「回滚条件」两栏纸面记录：变更内容与对应的回退前提分栏，草稿只写条件描述，是否切换由具备权限的人员确认。

### 新增复核维度表（2026-11-17）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 人工确认点标注 | 流程设计者 + 复核人 | 流程盘点表 / 草稿 | 每步骤是否标注人工判断或规则流转、依据是否齐备 | 中 | 纸面对照，自动化范围须人工确认 |
| 留痕五要素完整性 | 开发者 | 可观测性清单 | 输入 / 输出 / 版本 / 耗时 / 成本是否逐项齐全 | 中 | 文档记录，不构成验收结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于Agent 工作流方法论设计的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及生产环境部署、权限开通与上线放行的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-17）

> 参考公开 Agent 工程方法论中「非人类身份单独治理与最小权限」「评测集先于提示词优化」与「失败重放五项留痕」的思路，在流程盘点后补一个纸面小节：逐项标注每个 Agent 的身份标识、所需最小工具集、凭据归属与复核角色，并提示评测样本齐备前不宜讨论优化，相关配置与权限变更由具备权限的人员在既有系统中执行。

### 时效性说明

- 本期时效性核查：**截至 2026-11-17**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-24）：复核维度与举例补充

> 本节为 2026-11-24 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Step 3 — Agentic Pipeline Design / 智能体流水线设计**：

- 设计清单补一条「每个动作是否具备独立最小权限标签」的占位项，由使用者圈选并留白说明，草稿不写入任何凭据或密钥。
- 为「读写工具分离」新增一张纸面对照：左列列工具标签，右列留白标注需人工审批的动作类别，不预置执行步骤。

**常见设计反模式 / Anti-Patterns**：

- 反模式清单补一条「失败是否可重放」的占位检查项，记录输入 / 输出 / 版本 / 耗时 / 成本五项留痕标签，具体内容留白。
- 为「无评测集先调优」新增一行纸面提示位：标注需先建的最小评测集条目数占位，数量由人工确认。

### 新增复核维度表（2026-11-24）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 最小权限标签核对 | 设计人 + 复核人 | 流水线设计清单 | 是否逐动作标注权限标签、未写入凭据 | 高 | 纸面设计，审批由人员完成 |
| 轨迹重放留痕 | 设计人 | 反模式核对表 | 是否登记五项留痕标签、内容留白待人工确认 | 中 | 文档记录，不构成上线方案 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于智能体工作流的方法论设计与反模式核对的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及正式上线、生产环境写操作与对外发布的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-24）

> 参考同类公开框架把「评测集先行」「策略即代码（权限与审批由中间件执行而非提示词）」「每个智能体作为非人类身份以最小权限治理」「轨迹留痕与失败重放」「默认只读 / dry-run 后再逐步放开写权限」整理为方向性设计清单；强调不可逆动作须由人员审批，草稿只保留占位标签与待确认项。

### 时效性说明

- 本期时效性核查：**截至 2026-11-24**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
