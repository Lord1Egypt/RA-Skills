# B2B SDR Agent Template — Launch Content

All marketing copy for the open-source B2B SDR Agent Template.
GitHub: https://github.com/iPythoning/b2b-sdr-agent-template

---

## 1. Show HN Post

**Title:** Show HN: Open-source AI SDR that automates full B2B export sales pipeline

**Body:**

I've been building AI agents for B2B export companies for the past year. Most "AI sales tools" are glorified chatbots — they handle one message, forget context, and fall apart after the first conversation. So I built an open-source template that handles the entire 10-stage sales pipeline, from lead capture to deal closing.

The core idea is a 7-layer context architecture. Instead of a single system prompt, the AI reads 7 Markdown files on every conversation: Identity (who am I), Soul (how I behave), Agents (full sales workflow), User (owner's ICP and products), Heartbeat (automated pipeline inspection), Memory (3-engine recall system), and Tools (CRM, channels, integrations). This gives it deep, persistent understanding of your business.

It runs 13 automated cron jobs — daily pipeline reports, stalled lead detection, email follow-up sequences, AI-powered lead discovery rotating across African, Middle Eastern, SEA, and Latin American markets. Dynamic ICP scoring adjusts in real-time based on buyer behavior (fast reply +1, asks for quote +2, 7 days silent -1).

Multi-channel orchestration across WhatsApp, Telegram, and Email. The delivery-queue skill adds human-like message pacing (3-90s delays, message splitting) so it doesn't feel like a bot. Cultural adaptation for 5 market regions. Auto-detects and responds in the customer's language.

Built on OpenClaw. Battle-tested with real export companies selling heavy vehicles, electronics, and textiles. Includes 3 industry example configs you can deploy in 5 minutes.

MIT licensed. Markdown-driven — no code changes needed for customization.

https://github.com/iPythoning/b2b-sdr-agent-template

---

## 2. Reddit Posts

### r/SaaS Post

**Title:** I open-sourced my AI SDR instead of charging $200/month — handles full B2B sales pipeline across WhatsApp, Email, and Telegram

**Body:**

I spent a year building AI SDR agents for B2B export clients. Watched them pay $200-500/month each for tools like Apollo, Instantly, and Smartlead — and still need 3-4 tools stitched together with Zapier.

So I packaged everything into one open-source template. It covers the entire pipeline: lead capture, BANT qualification, CRM entry, company research, quotation generation, negotiation tracking, daily reporting, nurture campaigns, cold email sequences, and multi-channel orchestration.

The whole thing is configured through 7 Markdown files — no code. You describe your company, products, ICP scoring criteria, and sales workflow in plain text. The AI reads all of it on every conversation.

It runs 13 automated cron jobs (pipeline reports, stalled lead detection, email follow-ups, AI lead discovery). Has 3-engine memory so it remembers customer context across sessions. Supports WhatsApp, Telegram, and Email.

Already battle-tested with companies selling heavy vehicles to Africa, electronics to SEA, and textiles to Europe.

MIT license. Clone, customize 7 files, deploy.

GitHub: https://github.com/iPythoning/b2b-sdr-agent-template

---

### r/sales Post

**Title:** My AI handles 10 stages of B2B sales while I sleep — lead capture through deal closing, and I open-sourced it

**Body:**

I run export sales for B2B companies. The pain: leads come in on WhatsApp at 3 AM from different time zones, follow-ups slip through cracks, and qualification takes forever with manual back-and-forth.

Built an AI SDR that handles the full pipeline automatically:

1. Captures leads from WhatsApp/Telegram/ads
2. Qualifies via natural BANT conversation
3. Logs structured data to CRM
4. Researches the company (web scraping + analysis)
5. Generates PDF quotes (multi-language)
6. Tracks negotiation rounds
7. Sends daily pipeline reports at 9 AM
8. Runs nurture sequences for cold leads
9. Manages personalized email outreach (Day 1/3/7/14)
10. Coordinates across WhatsApp + Email + Telegram

It scores leads dynamically — fast reply bumps score up, silence drops it. Hot leads (7+/10) trigger instant owner notification. It sends messages with human-like pacing so buyers never suspect automation.

Running it for clients in heavy machinery, electronics, and textiles across Africa, Middle East, and Southeast Asia. It handles time zones, language detection, and cultural adaptation automatically.

Open-sourced the whole thing: https://github.com/iPythoning/b2b-sdr-agent-template

---

### r/artificial Post

**Title:** Built a 7-layer context architecture for AI sales agents — 3-engine memory, dynamic ICP scoring, multi-channel orchestration. Open-sourced it.

**Body:**

Most AI agent implementations use a single system prompt. That breaks down fast in production sales environments where the agent needs persistent knowledge about the business, products, customers, and ongoing deals.

I built a 7-layer context system where each layer is a separate Markdown file:

- **Identity**: Company info, pipeline stages, lead tiering rules
- **Soul**: Personality traits, communication style, hard constraints
- **Agents**: 10-stage sales workflow with decision trees
- **User**: ICP scoring (5 weighted dimensions), competitor intelligence
- **Heartbeat**: Automated pipeline inspection — 13-item checklist on every cycle
- **Memory**: 3-engine architecture (Supermemory for semantic recall, MemoryLake for session context, MemOS for cross-session patterns)
- **Tools**: CRM commands, channel configs, web research APIs

The memory architecture is the interesting part. Supermemory uses vector embeddings (LanceDB) to store customer facts, conversation insights, market signals, and effective scripts — each with different TTLs. Before any outreach, the agent queries relevant memories and injects them into context.

Dynamic ICP scoring starts with 5 weighted dimensions (purchase volume 30%, product match 25%, region 20%, payment capacity 15%, decision authority 10%) and auto-adjusts based on interaction signals.

13 cron jobs handle pipeline automation. The delivery-queue skill implements human-like message timing with configurable delays and quiet hours.

MIT licensed: https://github.com/iPythoning/b2b-sdr-agent-template

---

## 3. X/Twitter Thread

**Tweet 1 (Hook):**
I open-sourced an AI SDR that handles full B2B sales — from lead capture to deal closing — across WhatsApp, Telegram, and Email.

Not a chatbot. A complete 10-stage sales pipeline that runs 24/7.

Here's the architecture behind it:

**Tweet 2:**
The problem with most AI sales tools: they handle ONE conversation. No memory. No pipeline. No follow-up.

Real B2B sales has 10 stages. Lead capture, BANT qualification, CRM entry, research, quotation, negotiation, reporting, nurture, email outreach, multi-channel orchestration.

This template handles all 10.

**Tweet 3:**
The secret: a 7-layer context system.

Instead of cramming everything into one prompt, the AI reads 7 Markdown files:

- Identity (company + role)
- Soul (personality + rules)
- Agents (sales workflow)
- User (ICP + products)
- Heartbeat (pipeline inspection)
- Memory (3-engine recall)
- Tools (CRM + channels)

**Tweet 4:**
The memory architecture is 3 engines deep:

1. Supermemory — vector search for customer facts, market signals, effective scripts
2. MemoryLake — session context and conversation summaries
3. MemOS Cloud — cross-session behavior patterns

Your AI SDR remembers that Ahmed from Dubai buys 50 units/quarter and prefers WhatsApp.

**Tweet 5:**
13 automated cron jobs run without you touching anything:

- Every 30 min: Gmail inbox scan
- 9 AM: Pipeline report via WhatsApp
- 10 AM: AI lead discovery (rotating markets)
- 11 AM: Email follow-up check
- 3 PM: Stalled lead detection
- Weekly: Nurture campaigns, competitor intel, summaries

**Tweet 6:**
Dynamic ICP scoring that evolves with every interaction:

Base score = 5 weighted dimensions (purchase volume, product match, region, payment capacity, decision authority)

Then auto-adjusts:
- Fast reply → +1
- Asks for quote → +2
- Mentions competitor → +2
- 7 days silent → -1

Hot lead (7+)? Owner gets notified instantly.

**Tweet 7:**
The humanizer makes it feel real:

- Messages split into 2-3 natural chunks
- 3-90 second delays between messages
- Cultural adaptation for 5 regions (Middle East, Africa, SEA, LatAm, Europe)
- Auto-detects language, responds natively
- Quiet hours awareness
- Never says "As an AI..."

**Tweet 8:**
Everything is Markdown. No code changes needed.

Clone the repo. Edit 7 files with your business info. Deploy.

Includes ready-to-use configs for heavy vehicles, electronics, and textiles.

MIT licensed. Built on OpenClaw. Battle-tested with real companies.

https://github.com/iPythoning/b2b-sdr-agent-template

---

## 4. LinkedIn Post

**How AI Is Changing B2B Export Sales — And Why I Open-Sourced Our Solution**

I've spent the last year working with B2B export companies across heavy machinery, electronics, and textiles. The pattern is always the same:

Leads come in from WhatsApp at 2 AM because your buyer is in Lagos. Your sales rep follows up 14 hours later. By then, they've already messaged three of your competitors. The quote sits in "pending" for a week because nobody tracked the follow-up. The CRM is half-empty because manual data entry is the first thing dropped when things get busy.

Sound familiar?

We built an AI SDR that handles the complete sales pipeline — not just the first message, but all 10 stages from lead capture to deal closing. It qualifies leads through natural BANT conversations, researches companies automatically, generates PDF quotes in the buyer's language, tracks negotiations, sends daily pipeline reports, runs nurture campaigns, manages email sequences, and coordinates across WhatsApp, Telegram, and Email.

Three things make it different from typical AI tools:

**1. Deep context, not shallow prompts.** A 7-layer context architecture where the AI reads your company identity, sales workflow, ICP scoring, product catalog, and competitive intelligence on every conversation. It knows your business like a veteran sales rep.

**2. Real memory.** A 3-engine memory system stores customer facts, conversation insights, and market signals. Before reaching out to any lead, the AI queries its memory for relevant context. It remembers that your buyer in Dubai prefers WhatsApp, orders quarterly, and was comparing prices with your competitor last month.

**3. Human-like execution.** Messages are split into natural chunks with realistic delays. Cultural adaptation for Middle Eastern, African, Southeast Asian, Latin American, and European markets. Auto-detects language. Never sends during the buyer's nighttime. The buyer never knows they're talking to AI.

We've tested this with real export companies. It handles time zones, multi-language conversations, and cross-channel coordination without supervision.

Today we're open-sourcing the entire system. The whole thing is configured through Markdown files — no coding required. Clone, customize 7 files with your business info, deploy in 5 minutes.

If you're running B2B export sales and tired of leads falling through the cracks, take a look.

GitHub: https://github.com/iPythoning/b2b-sdr-agent-template

#B2BExport #AIinSales #WhatsAppBusiness #OpenSource #SalesAutomation #B2BSales #ExportBusiness #ArtificialIntelligence #SalesTech

---

## 5. Product Hunt Launch Copy

**Tagline:**
AI SDR for B2B export — full pipeline, open-source

**Description:**
Open-source AI Sales Development Representative for B2B export businesses. 7-layer context architecture, 10-stage sales pipeline, 3-engine memory, dynamic ICP scoring. Handles lead capture through deal closing across WhatsApp, Telegram, and Email. Configure with Markdown, deploy in 5 minutes.

**3 Key Features:**

1. Full 10-stage pipeline: lead capture, BANT qualification, quoting, negotiation, nurture, and closing
2. 3-engine memory system with semantic search — your AI remembers every customer detail
3. Multi-channel orchestration across WhatsApp, Telegram, and Email with human-like pacing

**Maker Comment:**

I started building this out of frustration. I was helping B2B export companies set up their sales processes, and the same problem kept appearing: leads coming in from different time zones on WhatsApp, falling through the cracks because the sales team couldn't respond fast enough. One client lost a $40K truck deal because they replied 16 hours late to a buyer in Nigeria.

So I built an AI agent to handle the first response. Then qualification. Then CRM entry. Then follow-ups. Before I knew it, I had a complete 10-stage pipeline running autonomously.

The key insight was that a single system prompt isn't enough for real sales. The AI needs to understand your company, products, pricing strategy, competitors, customer profiles, and ongoing deals — all at once. That's why I designed the 7-layer context system: each layer is a Markdown file you customize for your business.

After testing it with companies selling heavy vehicles to Africa, electronics to Southeast Asia, and textiles to Europe, I decided to open-source the whole thing. The export industry has too many small-to-medium businesses paying $200-500/month for fragmented SaaS tools that still require manual work.

This template is production-ready, MIT licensed, and takes 5 minutes to deploy. No code changes needed — just edit 7 Markdown files and you have an AI SDR that works 24/7 across WhatsApp, Telegram, and Email.

---

## 6. Dev.to Article

**Title:** How I Built an AI That Handles Full B2B Sales Pipeline — Architecture Deep Dive

---

Most AI sales tools are glorified chatbots. They handle one conversation, forget everything, and have no concept of a sales pipeline. After a year of building AI agents for real B2B export companies, I open-sourced a production-ready template that handles the entire 10-stage sales process. Here's how the architecture works.

### The Problem

B2B export sales is complex. A single deal involves: capturing a lead from WhatsApp at 2 AM, qualifying them through natural conversation, researching their company, generating a quote in their language, tracking negotiation rounds, following up when things stall, and coordinating across multiple messaging channels. Most AI tools handle step 1 and call it done.

### Architecture: 7-Layer Context System

The core design decision was rejecting the single-prompt approach. Instead, the AI loads 7 Markdown files on every conversation, each serving a distinct purpose:

```
+--------------------------------------------------+
|              AI SDR Agent                         |
+--------------------------------------------------+
|  IDENTITY.md   -> Who am I? Company, role         |
|  SOUL.md       -> Personality, values, rules      |
|  AGENTS.md     -> Full sales workflow (10 stages) |
|  USER.md       -> Owner profile, ICP, scoring     |
|  HEARTBEAT.md  -> 13-item pipeline inspection     |
|  MEMORY.md     -> 3-engine memory architecture    |
|  TOOLS.md      -> CRM, channels, integrations     |
+--------------------------------------------------+
|  Skills        -> Extensible capabilities         |
|  Product KB    -> Your product catalog            |
|  Cron Jobs     -> 13 automated scheduled tasks    |
+--------------------------------------------------+
|  OpenClaw Gateway (WhatsApp / Telegram / Email)   |
+--------------------------------------------------+
```

**Why Markdown?** Because the people configuring this are sales directors, not developers. Every layer is a file you edit in plain text. No JSON schemas, no YAML indentation headaches, no code changes.

### Layer Deep Dive

**Identity Layer** (`IDENTITY.md`) defines who the AI is: company name, brand, business description, target markets. It also defines the pipeline status flow (`new -> contacted -> interested -> quote_sent -> negotiating -> closed_won`) and lead tiering rules (hot leads get 24h first contact, warm leads 48h, cold leads go to nurture pool).

**Soul Layer** (`SOUL.md`) sets personality and hard constraints. The AI is a "pragmatic B2B sales consultant, research-driven, not a script machine." Hard rules include: never send generic templates, price commitments require owner confirmation, customer information is strictly confidential.

**Agents Layer** (`AGENTS.md`) contains the full 10-stage sales workflow with decision trees for each stage. This is the operational brain — it defines exactly how the AI handles qualification, when to escalate, how to structure negotiations.

**User Layer** (`USER.md`) is the business-specific configuration: product lines, ICP scoring criteria, competitor intelligence, and communication preferences. ICP scoring uses 5 weighted dimensions:

| Dimension | Weight |
|-----------|--------|
| Purchase Volume | 30% |
| Product Match | 25% |
| Region Reachability | 20% |
| Payment Capacity | 15% |
| Decision Authority | 10% |

Scores auto-adjust based on interaction: fast reply +1, asks for quote +2, mentions competitor +2, 7 days silent -1.

### The 10-Stage Pipeline

1. **Lead Capture** — Auto-detect inbound messages from WhatsApp, Telegram, CTWA ads. Create CRM record.
2. **BANT Qualification** — Natural conversation to assess Budget, Authority, Need, Timeline.
3. **CRM Entry** — Structured data extraction: name, company, country, ICP score, product interest.
4. **Research & Enrichment** — Web search via Jina AI + company website analysis. 3-layer enrichment.
5. **Quotation** — Auto-generate PDF quotes, multi-language, sent to owner for approval.
6. **Negotiation** — Track counter-offers, recommend strategy, escalate when needed.
7. **Reporting** — Daily 09:00 pipeline reports, 15:00 stalled alerts, weekly summaries.
8. **Nurture** — Automated follow-ups, industry news, post-sale care, quarterly check-ins.
9. **Email Outreach** — Personalized cold email sequences (Day 1/3/7/14), auto follow-up.
10. **Multi-Channel Orchestration** — Cross-channel coordination, auto-switching between WhatsApp, Email, Telegram.

### Memory Architecture: 3 Engines

This is where it gets interesting. A sales agent without memory is useless after the first session.

**Supermemory** is a semantic memory engine backed by vector search (LanceDB). It stores 4 types of memories with different TTLs:

- Customer facts (permanent): "Ahmed from Dubai, buys 50 units/quarter"
- Conversation insights (90 days): "Interested in bulk pricing for Model X"
- Market signals (30 days): "East Africa demand spike for product Y"
- Effective scripts (permanent): "Opening with local market data gives 3x reply rate"

Before any outreach, the agent queries Supermemory for relevant context and injects it into the conversation.

**MemoryLake** handles session-level context: conversation summaries, ongoing deal status, last interaction timestamp. Auto-recalled per conversation.

**MemOS Cloud** captures cross-session behavior patterns: which opening lines work best for which regions, optimal follow-up timing, common objections by industry.

### Making It Human: The SDR Humanizer

The `sdr-humanizer` skill defines rules for natural conversation:

- Break messages into 2-3 short chunks instead of walls of text
- Add 3-90 second delays between consecutive messages via the `delivery-queue` skill
- Match the customer's formality level
- Cultural adaptation for 5 regions (Middle East: relationship-first; Europe: data-driven; LatAm: personal touch)
- Never reply instantly (feels robotic) — simulate 1-5 minute response time during business hours
- Quiet hours awareness: don't send during the prospect's nighttime

### Automation: 13 Cron Jobs

The agent runs scheduled tasks without human intervention:

- Every 30 min: Gmail inbox scan for client replies
- Daily 09:00: Pipeline report to owner via WhatsApp
- Daily 10:00: AI lead discovery (market rotation: Africa/ME/SEA/LatAm)
- Daily 11:00: Email follow-up sequence check
- Daily 15:00: Stalled lead detection
- Weekly Wednesday: Nurture campaign
- Weekly Friday: Competitor intelligence gathering
- Weekly Monday: Weekly summary report

### How to Customize It

Clone the repo, edit 7 Markdown files, deploy:

```bash
git clone https://github.com/iPythoning/b2b-sdr-agent-template.git
cd b2b-sdr-agent-template

# Edit for your business
vim workspace/IDENTITY.md   # Company info, pipeline stages
vim workspace/USER.md       # Products, ICP, competitors
vim workspace/SOUL.md       # AI personality and rules

# Deploy
cd deploy && ./deploy.sh my-company
```

The repo includes ready-to-use industry configurations for heavy vehicles, consumer electronics, and textiles. Copy an example, customize the specifics, and you're live.

### What's Next

This is MIT licensed and built on OpenClaw. I'm looking for contributors to add more industry templates, build new skills, and improve documentation. If you're working on AI agents for vertical use cases, I'd love to hear how you're approaching context management and memory.

GitHub: https://github.com/iPythoning/b2b-sdr-agent-template

---

## 7. 知乎/公众号文章

**标题：** 外贸老板的AI销售员：从线索获取到成交的全自动化实战

---

### 每个外贸老板都遇到过的场景

凌晨两点，一个尼日利亚客户在 WhatsApp 上询价。你的销售第二天上午十点才看到消息，回复时对方已经和三家竞品聊完了。

一个迪拜客户询价后沉默了一周，没人跟进，线索就这么丢了。

CRM 里的数据残缺不全，因为手动录入是销售最先放弃的事。

月底复盘发现，本月 30 条线索，真正走完整个流程的不到 5 条。其余的要么跟丢了，要么卡在报价审批上，要么压根没做 BANT 筛选就浪费了大量时间。

这些不是个案。在过去一年服务外贸企业的过程中，我发现这是行业通病。人工 SDR 的成本高（一个成熟外贸销售年薪 15-30 万），时差问题无解，多语言沟通能力有限，而市面上的 SaaS 工具（Apollo、Instantly、Smartlead）加起来每月 200-500 美元，还要 3-4 个工具拼接才能覆盖全流程。

### 一套开源的 AI SDR 系统

所以我把过去一年给客户搭建的 AI 销售系统，打包成了一个开源模板。

它不是一个简单的聊天机器人。它覆盖了完整的 10 阶段销售流水线：

| 阶段 | AI 做什么 |
|------|----------|
| 线索获取 | 自动识别 WhatsApp/Telegram/广告入站消息，创建 CRM 记录 |
| BANT 筛选 | 通过自然对话评估预算、决策权、需求、时间线 |
| CRM 录入 | 结构化数据采集：姓名、公司、国家、ICP 评分、产品意向 |
| 背调充实 | AI 搜索客户公司官网、行业信息，3 层数据充实 |
| 自动报价 | 生成 PDF 报价单，多语言，发给老板审批 |
| 谈判追踪 | 记录每轮还价，推荐策略，超出授权自动升级 |
| 每日汇报 | 09:00 Pipeline 报告，15:00 停滞预警，周报 |
| 线索养育 | 自动跟进、行业资讯推送、售后关怀、季度回访 |
| 邮件开发 | 个性化冷开发信序列（第1/3/7/14天），自动跟进 |
| 多渠道协同 | WhatsApp + Email + Telegram 跨渠道协调，自动切换 |

### 为什么它比普通 AI 工具靠谱？

**7 层上下文架构**。普通 AI 工具用一段 system prompt 就上了。这套系统有 7 层上下文，每层是一个 Markdown 文件：身份层（公司信息）、灵魂层（人格和底线）、操作层（10 阶段工作流）、用户层（ICP 评分和竞品）、巡检层（自动 Pipeline 检查）、记忆层（三引擎记忆）、工具层（CRM 和渠道配置）。AI 每次对话都加载全部 7 层——它了解你的公司，就像一个干了三年的老销售。

**三引擎记忆**。Supermemory 存储客户事实和市场洞察（语义搜索，向量数据库）；MemoryLake 管理会话上下文；MemOS Cloud 捕获跨会话行为模式。外联之前，AI 会自动查询记忆库，调取相关客户信息。它记得 Ahmed 来自迪拜，每季度采购 50 台，上次在比较竞品价格。

**动态 ICP 评分**。初始分数基于 5 个维度（采购量 30%、产品匹配 25%、区域 20%、支付能力 15%、决策权 10%）。然后根据互动自动调整：快速回复 +1，索要报价 +2，提及竞品 +2，7 天无回复 -1。热线索（7 分以上）自动标记，立即通知老板。

**拟人化对话**。消息拆分成 2-3 条自然片段，3-90 秒延迟发送。自动检测客户语言回复。5 个市场区域的文化适配（中东讲关系、欧洲讲数据、拉美讲热情）。有安静时间设置，不在客户的深夜发消息。客户永远不会知道自己在和 AI 对话。

### 13 个自动化定时任务

不需要你操心的事：

- 每 30 分钟扫描 Gmail 收件箱
- 每天 09:00 Pipeline 报告推送到 WhatsApp
- 每天 10:00 AI 主动获客（非洲/中东/东南亚/拉美轮换）
- 每天 11:00 检查邮件跟进序列
- 每天 15:00 检测停滞线索
- 每周三跑养育活动
- 每周五收集竞品情报
- 每周一发周报

### 5 分钟部署

整套系统的配置就是编辑 7 个 Markdown 文件，不需要写代码：

```bash
git clone https://github.com/iPythoning/b2b-sdr-agent-template.git
cd b2b-sdr-agent-template

# 编辑你的业务信息
vim workspace/IDENTITY.md   # 公司信息
vim workspace/USER.md       # 产品、ICP、竞品

# 部署
cd deploy && ./deploy.sh my-company
```

仓库里有重型车辆、消费电子、纺织服装三个行业的现成配置，复制过来改改就能用。

### 实际效果

在已部署的客户中：

- 线索首次响应时间从平均 14 小时降到 5 分钟以内
- 跟进遗漏率从 60%+ 降到接近 0
- CRM 数据完整度从不到 30% 提升到 95%+
- 销售团队可以把时间花在真正需要人判断的谈判和关系维护上

这不是要取代销售团队，而是让 AI 处理重复性的前端工作（获客、筛选、录入、跟进），让人专注于高价值环节。

MIT 开源协议，随意使用。

GitHub: https://github.com/iPythoning/b2b-sdr-agent-template

---

## 8. Awesome List PR Descriptions

### awesome-ai-agents

**b2b-sdr-agent-template** — Open-source AI SDR template for B2B export sales. 7-layer context architecture, 10-stage pipeline (lead capture to deal closing), 3-engine memory, dynamic ICP scoring. Multi-channel orchestration across WhatsApp, Telegram, and Email. Built on OpenClaw, configured via Markdown.

### awesome-sales-tools

**b2b-sdr-agent-template** — Production-ready AI Sales Development Representative for B2B export. Handles full pipeline: lead capture, BANT qualification, quotation, negotiation, nurture, and multi-channel outreach (WhatsApp/Email/Telegram). 13 automated cron jobs, dynamic lead scoring. Open-source, MIT licensed.

### awesome-chatgpt

**b2b-sdr-agent-template** — AI agent template that turns LLMs into full-pipeline B2B sales reps. 7-layer context system (Identity, Soul, Agents, User, Heartbeat, Memory, Tools) with 3-engine memory architecture. Supports any AI model (OpenAI, Anthropic, Google, etc.). Open-source.

### awesome-whatsapp

**b2b-sdr-agent-template** — AI-powered sales agent for WhatsApp Business. Handles full B2B sales pipeline with human-like message pacing, cultural adaptation, auto language detection, and quiet hours. Integrates with Telegram and Email for multi-channel orchestration. Open-source.

### awesome-opensource

**b2b-sdr-agent-template** — Open-source AI SDR (Sales Development Representative) for B2B export businesses. Full 10-stage sales pipeline, 7-layer context architecture, 3-engine memory, multi-channel support (WhatsApp/Telegram/Email). Markdown-driven configuration, deploy in 5 minutes. MIT licensed.
