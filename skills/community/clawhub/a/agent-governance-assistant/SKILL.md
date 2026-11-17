---
name: "Agent Governance Assistant"
slug: agent-governance-assistant
description: "UPDATED 2026: Covers China AI Agent governance regulations (generative AI regulations), MCP protocol governance implications, and enterprise AI audit frameworks. AI-powered enterprise AI agent governance framework — audit agent behavior, enforce security policies, ensure CBIRC/CFCA compliance, detect shadow AI, and generate governance reports. Built for IT risk managers, compliance officers, and enterprise AI leaders in financial institutions. Keywords: AI agent governance, enterprise AI, agent compliance, AI security policy, CBIRC, CFCA, shadow AI detection, agent audit, Microsoft Agent 365, Copilot Studio, China AI regulation, Agent治理, 企业AI, AI合规, 影子AI检测, AI审计, NFRA AI合规, AI治理."
version: "5.0.3"
---

# Agent Governance Assistant


### AI Agent治理最新动态 [2026-09-18更新]（历史存档，最新口径见下方 2026-11-16 更新）

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 治理应对 |
|---------|---------|---------|---------|---------|
| 协议发布 | MCP 2.0正式发布：无状态协议革命，6个SEP驱动无状态化 | 2026-06 | Agent架构/部署模式重大变革 | 无状态化后更依赖外部审计日志，需补齐留痕 |
| 协议发布 | MCP Apps：Server端渲染交互界面（SEP-1865），沙盒iframe安全运行 | 2026-06 | Agent UI/用户体验 | UI侧输出也需纳入内容合规审查 |
| 协议发布 | Tasks扩展：长时运行任务支持，非阻塞式taskHandle | 2026-06 | Agent编排/工作流 | 长时任务的中间状态需可追溯、可中断 |
| 安全更新 | OpenAI Secure MCP Tunnel：零入站端口企业级安全部署 | 2026-06 | 企业Agent安全 | 仍需配合出网管控与身份鉴别 |
| 互操作 | Google A2A与MCP互操作性测试通过（6月12日联合宣布） | 2026-06 | 多Agent协作 | 跨Agent调用链的责任划分需事先约定 |
| 安全更新 | MCP 2.0安全沙箱：权限声明/执行沙箱/审计日志/用户确认 | 2026-06 | Agent安全治理 | 对应零信任架构的四项控制点 |
| **监管路径分化** | G20期间美方主张轻触式AI监管，与欧盟AI法案、中国分类分级治理形成三条不同路径（以官方最新发布为准） | 2026-09-02 | 跨境AI合规 | 跨国机构需按区域分别设定Agent上线门槛 |
| **AI基建国家化** | AI基础设施被定位为国家级基础设施，主权算力与本土应用能力成为政策议题（以官方最新发布为准） | 2026-09-02 | 金融行业AI基建 | 金融机构的自建算力须同步满足数据不出境要求 |

> **数据截止**: 2026-09-18（历史存档） | 来源：MCP官方规范、Anthropic官方博客、OpenAI公告、G20公开报道
> **声明**: 以上动态供参考，具体以官方最新发布为准

### AI Agent治理最新动态 [2026-11-16更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 治理应对 | 落地检查点（新增） |
|---------|---------|---------|---------|---------|---------|
| 协议演进 | MCP 2.0 无状态化、Tasks 长时任务、Apps 服务端渲染等能力陆续落地 | 2026-H1 | Agent 架构与部署模式 | 无状态化后更依赖外部审计日志 | 长时任务的中间状态须可追溯、可中断 |
| 安全能力 | 安全沙箱、权限声明、执行沙箱、审计日志、用户确认成为标配讨论项 | 2026-H1 | 企业 Agent 安全 | 对应零信任架构的四项控制点 | 每项控制点需有可出示的验收证据 |
| 互操作 | 多 Agent 协议之间的互操作性推进 | 2026-H1 | 多 Agent 协作 | 跨 Agent 调用链的责任划分须事先约定 | 在注册表中登记调用链与责任人 |
| 监管路径分化 | 美、欧、中三条监管路径并存（以官方最新发布为准） | 2026-Q3 | 跨境 AI 合规 | 按区域设定差异化上线门槛，底线取最严 | 上线评审表中增加"适用辖区"字段 |
| 基础设施属性（新增） | AI 基础设施被作为国家级基础设施讨论，主权算力与本土应用能力成为政策议题（以官方最新发布为准） | 2026-Q3 | 金融机构 AI 基建 | 自建算力同步满足数据不出境与安全要求 | 算力方案评审增加数据出境评估环节 |
| 长时任务治理（新增） | 支持长时运行的 Agent 需要中断、回滚与状态留痕能力 | 2026-Q3 | Agent 编排与审计 | 可中断与可解释纳入零信任清单 | 定期做中断演练并留存记录 |

> **数据截止**: 2026-11-16 | 来源：MCP 官方规范、OpenAI 公告、G20 公开报道及行业公开信息
> **声明**: 以上动态供参考，具体**以官方最新发布为准**

**动态落地示例（新增）**

> 背景：某部门拟上线一个支持长时运行的报销审核 Agent。
> - 对照动态表"长时任务治理"条目：需具备中断开关与状态留痕。
> - 落地检查：在上线评审表中增加"是否可中断""中断后是否可回滚""中间状态是否记录"三项。
> - 评审结论写法：三项未全部满足前不得上线，而不是"上线后补齐"。

## 语言与适用范围声明（Language & Scope Statement）

- **语言**：本 Skill **中英双语**——政策编号、控制点名称与报告标题保留英文（便于与内部制度文档对齐），解释与示例以**简体中文**为主。用户可要求全中文或全英文输出，治理口径与控制点不变。
- **适用**：企业（尤其是银行、保险等受监管金融机构）对内部 AI Agent 的**资产盘点、风险分级、策略制定、影子 AI 排查、成熟度自评与治理报告编制**。
- **能力边界（准确表述）**：本 Skill 未配置任何工具，不具备扫描网络、读取日志、访问终端或调用任何企业系统的能力。文中所有清单、矩阵与报告模板均为**文本方法论材料**，盘点与检测须由使用者在本机构既有平台（出网监控、DLP、终端管理、集成平台审计）中实施，本 Skill 不代其执行。
- **明确不属于本 Skill 产出范围**：① 代替监管机构作出合规认定；② 代替法务出具法律意见；③ 直接生成对外报送的正式监管文件（须经内部审核签发）；④ 实际的账号开通、封禁与配置变更；⑤ 获取或存储任何员工个人信息（排查结论一律使用角色化表述）。

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

| 时间 | 动态 | 治理含义 | 落地动作 |
|------|------|---------|---------|
| **2025年7月** | 中国《生成式人工智能服务管理暂行办法》正式施行 | AI Agent服务纳入互联网信息服务管理，算法备案要求扩展至Agent | 建立Agent算法备案台账 |
| **2025年11月** | MCP协议移交Linux Foundation | AI Agent工具集成标准化带来新的审计盲点，需纳入治理范围 | 把MCP工具调用纳入审计范围 |
| **2026年1月** | NFRA召开2026年监管工作会议，AI治理列为重点 | 金融行业AI Agent应用监管框架加速制定 | 预留季度治理报告报送口径 |
| **2026年** | Microsoft Agent 365/Copilot Studio企业大规模部署 | Agent行为审计、数据隔离、权限管控成为合规核心 | 按部门拆分权限矩阵 |
| **2026年** | 影子AI检测升级：从API监控到行为分析 | 传统DLP监控不足，需引入UEBA（用户实体行为分析）技术 | 网络层API监控 + 行为基线双轨 |
| **2026-09** | AI监管路径区域分化（美国轻触式 / 欧盟AI法案 / 中国分类分级） | 同一Agent在不同区域的可用性不同 | 按区域设定差异化上线门槛 |

> **2026年核心治理挑战：** 企业AI Agent数量激增（从10个→100+），传统Agent Inventory已无法满足监管要求。建议采用"零信任Agent架构"——每个Agent独立身份认证、最小权限、数据隔离、完整审计日志。

---


### AI治理最新动态 [2026-09-18更新]（历史存档，最新口径见下方 2026-11-16 更新）

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 治理应对 |
|---------|---------|---------|---------|---------|
| 监管发布 | 金融监管总局《关于银行业保险业人工智能安全开发应用的指导意见》从七大方面提出32项意见，AI治理从指导意见走向刚性规章 | 2026-06-18 | 金融机构AI治理框架 | 对照32项意见逐条建立台账 |
| 标准治理 | MCP 2026路线图将治理成熟度列为四大优先方向，Agent协议治理标准化加速 | 2026-06 | Agent治理与工具标准 | 采用L1–L5成熟度自评对齐 |
| 合规重点 | 高风险AI应用场景明确：资金交易、资产评估、信贷审批、承保理赔、风险管理 | 2026-06-18 | AI应用合规审查 | 上述场景一律要求人工复核 |
| **国际治理分化** | G20期间美方主张轻触式监管以保持创新速度，与欧盟AI法案、中国分类分级治理形成三条路径（以官方最新发布为准） | 2026-09-02 | 跨境合规与集团统一策略 | 跨国机构按区域设差异化门槛，底线取最严 |
| **基础设施属性** | AI基础设施被作为国家级基础设施讨论，主权算力与本土应用能力成为政策议题（以官方最新发布为准） | 2026-09-02 | 金融机构AI基建 | 自建算力需同步满足数据不出境与安全要求 |

> **数据截止**: 2026-09-18（历史存档） | 来源：国家金融监督管理总局、G20公开报道、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准；
> 涉及具体合规判定时，请以监管机构最新正式文件与机构法务意见为准。

### AI治理最新动态 [2026-11-16更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 治理应对 | 落地检查点（新增） |
|---------|---------|---------|---------|---------|---------|
| 监管要求 | 银行业保险业人工智能安全开发应用指导意见从多方面提出要求，AI 治理从指导意见走向刚性规章 | 2026-H1 | 金融机构 AI 治理框架 | 对照要求逐条建立台账 | 台账须含责任部门与完成时限 |
| 标准治理 | Agent 协议治理标准化加速，治理成熟度成为优先方向 | 2026-H1 | Agent 治理与工具标准 | 采用 L1–L5 成熟度自评对齐 | 每半年复评一次并留存记录 |
| 合规重点 | 高风险 AI 应用场景明确：资金交易、资产评估、信贷审批、承保理赔、风险管理 | 2026-H1 | AI 应用合规审查 | 上述场景一律要求人工复核 | 复核须有阈值条件而非原则表述 |
| 国际治理分化 | 美、欧、中三条监管路径并存（以官方最新发布为准） | 2026-Q3 | 跨境合规与集团统一策略 | 按区域设差异化门槛，底线取最严 | 集团统一策略须标注最严口径来源 |
| 基础设施属性 | AI 基础设施被作为国家级基础设施讨论（以官方最新发布为准） | 2026-Q3 | 金融机构 AI 基建 | 自建算力同步满足数据不出境与安全要求 | 方案评审增加数据出境评估 |
| 数据合规（新增） | 网络与数据安全管理要求升格，客户数据采集与使用边界更明确 | 2026-Q3 | Agent 数据范围 | 注册表中须写明数据范围与最小化依据 | 抽查 Agent 实际读取字段是否超范围 |

> **数据截止**: 2026-11-16 | 来源：国家金融监督管理总局、G20 公开报道及行业公开信息
> **声明**: 以上动态供参考，具体**以官方最新发布为准**；
> 涉及具体合规判定时，请以监管机构最新正式文件与机构法务意见为准。

## Workflow

### Phase 1 — Agent Inventory Discovery

**Step 1.1: Scan for Active AI Agents**

Generate a structured inventory of all AI agents in the enterprise environment.

**Input required:**
- List of known AI platforms in use (e.g., Microsoft 365 Copilot, Salesforce Einstein, custom LangChain agents, RPA bots)
- Department ownership mapping
- API endpoints or integration points

**Output: Agent Inventory Table**

| Agent ID | Platform | Owner | Department | Capabilities | Data Access Level | Autonomy | Registered | Last Active |
|----------|----------|-------|------------|--------------|-------------------|----------|-----------|------------|
| AG-001 | Microsoft Agent 365 | IT Admin | Finance | Email drafting, meeting prep | Full mailbox | Advisory | Yes | 2026-05-07 |
| AG-002 | Custom LangChain | Claims Lead | Claims | Document review, fraud flag | Claims data | Semi-auto | No | 2026-09-02 |
| AG-003 | Copilot Studio | Sales Ops | Sales | Lead scoring | CRM data | Advisory | Yes | 2026-09-10 |

> **Autonomy 取值建议**：Advisory（仅建议，人执行）/ Semi-auto（自动执行但可回退）/ Full-auto（自动执行且不可逆）。
> **Registered 为 No 的 Agent 应优先处置**——未注册却在生产运行，是本阶段最常见的高风险项。
> 上表 AG-002 即属于此类：未注册、半自动、且接触理赔数据，应列为 Critical 候选。

**Step 1.2: Classify Agent Risk Level**

Assign risk tier (Low / Medium / High / Critical) based on:
- Data sensitivity (PII, financial, health, IP)
- External interaction (internet, customers, third parties)
- Autonomy level (advisory only → full automation)
- Regulatory exposure (CBIRC, CFCA, personal information protection)

**Risk Classification Matrix:**

| Tier | Criteria | Example | Audit Frequency | 典型失控场景 | 必备控制 |
|------|----------|---------|----------------|-------------|---------|
| Critical | Customer-facing + financial data + high autonomy | AI underwriting agent | Weekly | 自动拒保且无人工复核入口 | 强制人工复核 + 全量留痕 + 可解释文档 |
| High | Internal + sensitive data + medium autonomy | AI claims processor | Monthly | 理赔金额判定错误被直接执行 | 金额阈值触发人工复核 + 抽样质检 |
| Medium | Internal + general data + advisory only | AI meeting summarizer | Quarterly | 会议纪要把敏感信息扩散给无关人员 | 输出范围限制 + 敏感词过滤 |
| Low | Internal + no sensitive data | AI email categorizer | Bi-annual | 误分类导致重要邮件被漏看 | 定期准确率抽查 |

**分级判定举例（本轮新增）**：

| 场景 | 数据 | 面向 | 自主度 | 判定 | 理由 |
|-----|-----|-----|-----|-----|-----|
| 智能核保助手，自动给出核保结论 | 客户健康与财务数据 | 内部+间接面向客户 | Semi-auto | Critical | 涉及承保决策且含敏感个人信息 |
| 理赔材料完整性预检 | 理赔影像件 | 内部 | Semi-auto | High | 敏感数据但可由人工回退 |
| 会议纪要生成 | 内部会议内容 | 内部 | Advisory | Medium | 仅建议、无敏感数据外发 |
| 邮件自动分类 | 邮件元数据 | 内部 | Full-auto | Low | 无敏感数据、后果可恢复 |
| 智能投顾推荐（新增） | 客户风险测评与持仓 | 面向客户 | Advisory | Critical | 面向客户且影响投资决策，须人工确认 |
| 报表自动分发（新增） | 内部经营数据 | 内部 | Full-auto | Medium | 数据敏感且分发范围易失控 |

---

### Phase 1.5 — 零信任 Agent 架构落地清单（本轮新增）

对应"2026年核心治理挑战"提出的零信任Agent架构，下表把四项原则拆成可验收的控制点。
治理不能停在原则层，**每一项都要能拿出证据**。

| 原则 | 控制点 | 具体措施 | 验收证据 |
|-----|-----|-----|-----|
| 独立身份认证 | Agent 有唯一身份 | 每个Agent分配独立服务主体，禁止共享账号 | Agent注册表 + 身份清单 |
| 最小权限 | 按职能授予 | 数据范围、工具清单、操作类型分别授权 | 权限矩阵与审批记录 |
| 数据隔离 | 跨部门不可见 | 按部门/业务域隔离数据访问，禁止越域读取 | 隔离策略配置截图 + 越权测试记录 |
| 完整审计日志 | 全链路留痕 | 记录提示词、工具调用、输出与人工处置 | 日志样本 + 留存周期说明 |
| 可中断（新增） | 长时任务可中止 | 长时运行任务支持随时中断与回滚 | 中断演练记录 |
| 可解释（新增） | 决策可回溯 | 关键决策输出依据与模型版本 | 可解释性文档 |
| 上线评审（新增） | 变更有闸口 | 高风险 Agent 上线前须过评审并留记录 | 评审记录与签字 |
| 退出机制（新增） | 可下线 | 明确停用条件与下线后的数据处置 | 退出预案与处置记录 |

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

| Finding | Risk Level | Data at Risk | Detection Source | Recommended Action | 复检时限 |
|---------|-----------|-------------|-----------------|-------------------|---------|
| Employee using free ChatGPT API for customer email drafting | CRITICAL | Customer PII + contract terms | 出网API监控（非白名单域名） | Immediate block + compliance training | 24小时内 |
| Unsanctioned n8n workflow syncing CRM to personal AI tool | HIGH | Contact data + deal values | DLP + 集成平台审计 | Replace with approved integration | 7日内 |
| 浏览器插件读取企业OA页面内容 | HIGH | 内部公文与审批信息 | 浏览器扩展清单核查 | 移除插件并加入禁用清单 | 7日内 |
| 部门自建Agent未纳入注册表 | MEDIUM | 视其数据范围而定 | 定期资产盘点比对 | 补登记并补做风险评估 | 30日内 |
| 员工用个人账号调用外部大模型处理内部文档（新增） | HIGH | 内部文档与可能的客户信息 | 出网域名聚合 + 自查问卷 | 通知停用并改用已批准渠道 | 7日内 |
| 未授权浏览器扩展读取CRM页面（新增） | HIGH | 客户联系信息与商机金额 | 终端扩展清单核查 | 移除并加入禁用清单 | 7日内 |

**检测指标与对应手段（本轮新增维度）**：

| 检测指标 | 适用手段 | 局限 |
|---------|---------|-----|
| 第三方AI API调用 | 出网流量监控 + 域名白名单 | 加密流量需配合证书策略 |
| AI工具使用日志 | DLP系统 | 覆盖不到未安装客户端的设备 |
| 浏览器扩展访问企业API | 终端管理 + 扩展清单核查 | 需终端管控能力 |
| 未授权自动化工作流 | 集成平台审计日志 | 影子SaaS需单独发现 |
| 行为异常（下载量突增等） | UEBA 行为基线 | 需历史数据积累，误报需调优 |
| 自建Agent未登记（新增） | 定期资产盘点 + 部门自查 | 依赖部门配合，可能漏报 |
| 加密流量中的AI调用（新增） | 证书策略 + 出网代理 | 需终端具备相应管控能力 |

---

### Phase 3.5 — 治理成熟度自评（本轮新增）

在出具审计报告前，先用五级模型给企业的Agent治理定级，避免"报告很厚、水平很初"的情况。

| 级别 | 名称 | 特征 | 下一步 |
|-----|-----|-----|-----|
| L1 初始 | 无台账 | Agent数量不清、无人负责 | 立即做资产盘点 |
| L2 可重复 | 有台账 | 已登记但无分级、无策略 | 建立风险分级与基础策略 |
| L3 已定义 | 有策略 | 策略成文并覆盖主要Agent | 落地技术控制与审计日志 |
| L4 已管理 | 可度量 | 有合规评分、定期复检 | 引入UEBA与自动化监控 |
| L5 优化 | 持续改进 | 治理指标纳入考核、定期演练 | 红队演练与跨机构对标 |

**举例（如何定级）**：某企业已完成12个Agent登记、有策略文档但无合规评分、无定期复检 → 判为 L3。
其下一步应优先建设"可度量"能力（合规评分卡 + 季度复检），而不是直接上UEBA——
**跳过L4直接上高级工具，往往因缺少基线数据而失效**。

**举例二（两个容易定错的情形）**：
- 情形一：企业买了 UEBA 平台并上线了仪表盘，但 Agent 台账不完整、无人负责 → 仍是 **L1**，
  不是 L4。**工具不等于能力**，判据是"有没有稳定的度量与复检机制"，不是"有没有工具"。
- 情形二：企业台账齐全、策略成文、也有季度复检，但治理指标未纳入任何部门考核 → 判为 **L4 但未达 L5**；
  L5 的标志是治理指标进入考核并定期演练，缺了这一环就仍是"有管理、无持续优化"。
- 用法：定级宁可偏低一档。**定高了会让整改清单失去针对性**，是治理报告最常见的失真来源。

---

### Phase 4 — Audit Trail & Reporting

**Step 4.1: Generate Governance Audit Report**

Produce a structured audit report for internal risk committees and external regulators.

**Report Sections:**
1. Executive Summary (1 page)
2. Agent Inventory & Risk Classification
3. Governance Maturity Level (L1–L5) — 本版新增
4. Policy Compliance Scorecard
5. Shadow AI Findings
6. Open Risks & Remediation Roadmap
7. Appendix: Agent Decision Logs (sample)

**合规评分卡建议权重（本轮新增维度）**：

| 评分项 | 权重 | 评分依据 |
|-----|-----|-----|
| Agent 注册覆盖率 | 20% | 已注册数 / 生产运行总数 |
| 数据最小化落实 | 20% | 抽查Agent实际读取字段是否必要 |
| 人工复核覆盖率 | 20% | 高风险决策中具备人工复核的比例 |
| 审计日志完整性 | 15% | 提示词/工具调用/输出三类留痕是否齐全 |
| 影子AI处置率 | 15% | 已处置发现项 / 总发现项 |
| 复检及时性 | 10% | 按期完成复检的比例 |

**举例**：某企业12个Agent中8个已注册（20分得13.3）、数据最小化抽查达标（20）、
人工复核覆盖高风险决策的一半（20分得10）、日志仅记录输出（15分得5）、
影子AI 3项中已处置1项（15分得5）、复检按期率约70%（10分得7），总分约 **60.3/100**，
对应 L3 偏上、尚未达到 L4。

**举例二（同样总分、不同风险）**：A、B 两家企业总分同为 60 分上下。
- A 的短板在"数据最小化"与"人工复核覆盖率"（各得一半分）；
- B 的短板在"影子AI处置率"与"复检及时性"。
- 结论：**A 的风险显著高于 B**。前者意味着敏感数据可能正在被超范围读取、高风险决策可能无人工复核，
  属实质性合规敞口；后者主要是流程效率问题。
- 用法：评分卡必须**逐项看，不能只看总分**；报告中应单列"最低分项"并作为整改第一优先级。

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

### Example 3: 影子AI专项排查（本版新增）

**Input:**
```
监管检查提出影子AI问题。我们只有网络层的出网日志，
没有终端管控，也没有UEBA。怎么在两周内拿出一个可交付的排查结论？
```

**Output:**
```
## 排查策略（按可执行性排序）
第1周：
1. 出网日志按域名聚合，筛出已知AI服务域名与可疑新域名
2. 拉取集成平台（Zapier/Make/n8n）审计日志，找连接企业数据的自动化流程
3. 向各部门发放自查问卷 + 抽查20台终端的浏览器扩展清单

第2周：
4. 对发现项按"数据敏感度 × 使用频率"分级
5. 出报告，明确每项的建议动作与复检时限
6. 同时提出能力缺口：终端管控与UEBA建议列入下一年度预算

## 交付物
- 影子AI Exposure Report（含 Detection Source 与 复检时限 两列）
- 能力缺口说明（说明本次排查的覆盖边界，避免过度承诺）
```

**要点**：只有网络层日志时，**必须显式说明覆盖边界**——未装终端管控的设备和
加密流量中的调用可能未被发现。治理报告宁可写明局限，也不要给出"已全面排查"的结论。

### Example 4: 高风险Agent上线前评审（本版新增）

**Input:**
```
理赔部门要上线一个自动核赔Agent，金额在1万元以下可自动赔付。
需要走什么治理流程？
```

**Output:**
```
## 风险定级：Critical
理由：客户面向 + 理赔敏感数据 + 半自动执行

## 上线前必过六关（对应零信任清单）
1. 独立身份：分配独立服务主体，不与人工账号混用
2. 最小权限：仅可读取理赔必要字段，禁止访问其他业务域
3. 数据隔离：与其他部门数据域隔离
4. 完整留痕：提示词、工具调用、判定依据、赔付结果全部记录
5. 可中断：保留随时暂停自动赔付的开关
6. 可解释：每笔自动赔付需输出判定依据与模型版本

## 人工复核设计
- 1万元以下自动赔付，但按不低于5%比例抽样人工复核
- 出现同一被保险人短期内多次赔付等异常模式时，自动转为人工
- 保留客户申诉与人工重开通道

## 上线后
- 前3个月按 Weekly 审计频率，稳定后可降为 Monthly
```

### Example 5: 治理成熟度自评与整改排序（本版新增）

**Input:**
```
我们刚做完Agent盘点，登记了12个，也写了一份治理策略。
领导问：我们现在到底是什么水平，下一步先做什么？
```

**Output:**
```
## 定级：L3 已定义
依据：有台账、有策略文档并覆盖主要Agent；但无合规评分、无定期复检 → 未达L4

## 容易定错的两点
- 买了UEBA平台 ≠ 达到L4，台账不全仍是L1
- 有季度复检但治理指标未纳入考核 → L4，不是L5

## 下一步（按投入产出排序）
1. 建合规评分卡（六项权重），先把"可度量"补上
2. 设季度复检机制与复检时限
3. 补齐高风险场景的人工复核阈值（金额/异常模式/申诉）
4. 待基线数据积累后再评估是否引入UEBA
```

### Example 6: 同样总分、整改优先级不同（本版新增）

**Input:**
```
两家分公司的治理评分都是60分左右，整改计划能共用一份吗？
```

**Output:**
```
## 结论：不能共用，必须逐项看

| 分公司 | 最低分项 | 风险性质 | 整改优先级 |
|-------|---------|---------|-----------|
| A | 数据最小化、人工复核覆盖率 | 实质性合规敞口 | 立即整改，30日内 |
| B | 影子AI处置率、复检及时性 | 流程效率问题 | 按季度整改 |

## 报告写法
- 单列"最低分项"并说明其风险性质
- 不因总分相同而给出同一份整改清单
- 总分用于横向对比，分项用于定优先级
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
8. **先定级再选工具（本版新增）**：成熟度处于 L1–L2 的企业先做台账与分级，不要直接采购UEBA等高级工具；缺少基线数据会让高级工具失效。
9. **写清覆盖边界（本版新增）**：任何排查与评估报告都要明确说明"哪些没查到"，治理报告的可信度来自坦诚的边界说明，而不是全覆盖的承诺。
10. **人工复核要设计阈值而非口号（本版新增）**：把"必须人工复核"落成具体条件（金额、异常模式、客户申诉），否则执行时会被绕过。
11. **长时任务必须可中断（本版新增）**：支持长时运行的Agent要保留随时暂停与回滚的开关，并定期做中断演练。
12. **总分只用于对比，分项才用于排优先级（本版新增）**：合规评分卡的六项权重中，最低分项决定整改顺序；同样总分的两家机构可能风险完全不同。
13. **成熟度定级宁可偏低一档（本版新增）**：判据是"有没有稳定的度量与复检机制"，不是"有没有工具"；定高了会让整改清单失去针对性。
14. **排查结论使用角色化表述（本版新增）**：影子AI报告中出现具体员工姓名时应改为岗位或编号，报告本身也要纳入最小必要与访问控制。

---

*Author: @gechengling | Skill: agent-governance-assistant | clawhub.ai/gechengling/agent-governance-assistant*

## 本轮增量（2026-11-16）：复核维度与举例补充

> 本节为 2026-11-16 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Phase 1 — Agent Inventory Discovery / Agent 盘点**：

- Agent 清单补「最小权限核对」两列：每个 Agent 记录已授予的数据范围与工具权限、以及任务实际所需的最小集合，二者不一致的条目标注需人工复核。
- 清单新增「负责人与复核周期」占位：每个 Agent 标注业务负责人、技术负责人与最近复核日期，缺负责人的按待补处理。

**Phase 4 — Audit Trail & Reporting / 审计轨迹与报告**：

- 审计轨迹报告补「行为与授权关联」纸面位：把关键动作、对应身份、所用权限与业务目的分栏记录，四者缺一即标注证据不完整。
- 合规评分报告新增「例外项留痕」占位：被临时豁免的控制项单独成栏，记录豁免理由、审批角色与到期复核日期。

### 新增复核维度表（2026-11-16）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 最小权限差距 | IT 风险管理员 + 复核人 | 权限矩阵 / 任务说明 | 授予权限与任务所需最小集合是否逐项比对 | 高 | 纸面核对，正式收权须人工执行 |
| 行为与授权关联 | 合规专员 | 审计日志草稿 | 动作、身份、权限、业务目的是否四者齐全 | 中 | 文档记录，不构成合规结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于企业 AI Agent 治理的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及权限变更、上线放行与正式合规结论的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-16）

> 参考公开 AI 治理框架中「Govern / Map / Measure / Manage 四功能」与「最小权限、Agent 身份清单、全链路可审计」的思路，在盘点清单后补一个纸面小节：逐项标注每个 Agent 的身份标识、可触达数据、工具权限、负责人与复核周期，并提示权限边界与审计记录须由相应责任人员定期复核。

### 时效性说明

- 本期时效性核查：**截至 2026-11-16**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
