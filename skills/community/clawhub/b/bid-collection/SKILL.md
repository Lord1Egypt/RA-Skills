---
name: bid-collection
<<<<<<< HEAD
description: 招投标商机采集 — 7x24自动监控全网招投标公开信息，智能筛选适配公司业务范围的高价值商机线索
=======
description: Tender & procurement lead collection — 24/7 automated scraping of public tender/procurement notices, intelligently filtering high-value leads matching your business scope
>>>>>>> 5210fda (Initial release: bid-collection v1.0.0 — Tender & Procurement Lead Collection Skill for Claude Code)
argument-hint: [scan|monitor|report|list-sources|add-source] [keywords] [--days=N] [--budget-min=N] [--budget-max=N]
allowed-tools: [WebSearch, WebFetch, Read, Write, Glob, Grep, Bash]
---

<<<<<<< HEAD
# 🎯 招投标商机采集 Skill

招投标商机采集是一个自动化监控与采集工具，覆盖各级政府公共资源交易平台、国企采购平台、行业招投标网站及第三方信息平台，精准抓取适配公司业务范围的招投标商机线索，实现招投标项目**早发现、早跟进、早布局**，助力公司业务拓展与项目落地。

## 工作流程概览

```
用户输入 /bid-collection
  │
  ├─ scan <keywords>     → 实时全网扫描招投标商机线索
  ├─ monitor             → 启动定时监控（后台循环扫描）
  ├─ report              → 生成近期商机线索汇总报告
  ├─ list-sources        → 列出当前监控的渠道清单
  ├─ add-source <url>    → 添加自定义监控源
  └─ (无参数)            → 交互式引导采集
=======
# 🎯 bid-collection

**Tender & Procurement Lead Collection Skill for Claude Code**

Bid-collection is an automated tender/procurement monitoring and lead generation tool. It covers government public resource trading platforms, state-owned enterprise procurement platforms, industry-specific tendering websites, and third-party bid information aggregators. It accurately captures procurement opportunities relevant to your business, enabling **early discovery, early follow-up, and early positioning** for business development and project success.

## Command Overview

```
User types /bid-collection
  │
  ├─ scan <keywords>     → Real-time global scan for tender/procurement leads
  ├─ monitor             → Start scheduled background monitoring
  ├─ report              → Generate a summary report of recent leads
  ├─ list-sources        → List currently monitored channels
  ├─ add-source <url>    → Add a custom monitoring source
  └─ (no args)           → Interactive guided collection
>>>>>>> 5210fda (Initial release: bid-collection v1.0.0 — Tender & Procurement Lead Collection Skill for Claude Code)
```

---

<<<<<<< HEAD
## 核心采集范围

### 一、政府公共资源交易平台（核心渠道）

| 类别 | 渠道 | 重点内容 |
|------|------|---------|
| **国家级** | 中国政府采购网 (ccgp.gov.cn) | 中央预算单位采购、协议供货、定点采购 |
| **国家级** | 中国招标投标公共服务平台 (cebpubservice.com) | 全国招标公告、变更公告、中标公示 |
| **省级** | 各省公共资源交易中心 | 省本级及地市招标采购项目 |
| **市级** | 各地市公共资源交易网 | 市县级政府采购、工程建设、服务采购 |
| **央企** | 中国招标投标网 (cncbid.com) | 央企集采、专项招标 |

### 二、国企及大型企业采购平台

| 平台 | 网址 | 重点内容 |
|------|------|---------|
| **中国移动** | 采购与招标网 (b2b.10086.cn) | 苏研采购、ICT服务、系统建设 |
| **中国联通** | 采购与招标网 (chinaunicombidding.cn) | 应用软件开发、运维服务、信息化系统 |
| **中国电信** | 阳光采购网 (ctyun.cn) | 云服务采购、集成服务、数智化项目 |
| **中国电子** | CEC电子采购平台 | 信创项目、网络安全、系统集成 |
| **国网** | 国家电网电子商务平台 (ecp.sgcc.com.cn) | 数字化建设、智能电网IT服务 |
| **中石油** | 能源一号网 (www.energyahead.com) | 信息化建设、工业互联网 |
| **中铁** | 中铁采购平台 | 智能建造、BIM系统、工程管理 |
| **招商局** | 招商局集团招投标平台 | 数字化转型、物流科技 |

### 三、行业专属招投标网站

| 领域 | 平台 | 网址 | 监控重点 |
|------|------|------|---------|
| **AI/大模型** | 各地智算中心采购平台 | — | 算力租赁、模型训练服务、AI中台 |
| **数字化** | 数字政府/智慧城市采购 | — | 政务云、数据治理、一网通办 |
| **IT服务** | 软交所/信息化采购平台 | — | 软件开发、系统集成、运维服务 |
| **科研** | 高校/科研院所采购平台 | — | 科研设备、实验室系统、技术开发 |
| **医疗** | 医采云等医疗采购平台 | — | 医疗信息化、智慧医疗、HIS系统 |
| **教育** | 教育装备采购平台 | — | 智慧教育、数字校园、教学平台 |

### 四、第三方招投标信息聚合平台（辅助渠道）

| 平台 | 网址 | 用途 |
|------|------|------|
| **千里马招标网** | qianlima.com | 综合类招标信息聚合 |
| **采招网** | bidcenter.com.cn | 全国采购招标信息汇总 |
| **招标雷达** | zhaobiaord.com | AI智能推荐匹配 |
| **比地招标** | bidizhaobiao.com | 大数据精准推送 |
| **剑鱼标讯** | jianyu360.com | 商机实时推送、竞争分析 |

---

## 核心能力

### 1. 按公司业务赛道智能化匹配

根据公司业务领域、产品服务类型，将采集到的招投标信息自动匹配到以下业务赛道：

| 业务赛道 | 匹配关键字 | 适配分析 |
|---------|-----------|---------|
| 🏢 **AI技术服务** | AI、人工智能、机器学习、NLP、CV、大模型 | 高适配 |
| 🧠 **大模型相关** | 大模型、LLM、GPT、生成式AI、向量数据库、RAG | 专项适配 |
| 🔬 **苏研采购** | 苏研、苏州研发、中移苏研 | 专项覆盖 |
| 🖥 **系统建设/开发** | 软件开发、系统集成、平台开发、微服务、前后端 | 核心业务 |
| ☁️ **算力与模型服务** | 算力、GPU、智算、模型训练、推理服务、AI算力 | 核心业务 |
| 📊 **数字化建设** | 数字化转型、数据治理、数据中台、数据资产 | 核心业务 |
| 🔒 **信息安全** | 网络安全、数据安全、等保、密码应用 | 扩展业务 |
| 🌐 **云服务** | 云平台、公有云、私有云、混合云、IaaS/PaaS | 扩展业务 |
| 📱 **智慧应用** | 智慧城市、智慧园区、智慧政务、数字政府 | 扩展业务 |
| 👁 **AI视觉/内容** | 数字人、AIGC、视频生成、虚拟现实 | 关注领域 |

### 2. 项目全生命周期覆盖

采集覆盖招投标全周期的各阶段信息：

| 阶段 | 信息类型 | 价值 |
|------|---------|------|
| ⏳ **招标预告** | 采购意向、需求公示、询价公告 | **提前布局**，筹备应标材料 |
| 📢 **正式招标** | 招标公告、竞争性磋商、竞争性谈判 | **核心商机**，投标准备 |
| 🔄 **变更公告** | 更正公告、补充通知、答疑 | 及时调整投标策略 |
| 🏆 **中标公示** | 中标候选人、成交公告 | 竞对分析、行业洞察 |
| ❌ **废标/流标公告** | 废标公告、终止公告 | 潜在二次机会 |

### 3. 商机线索精准分级

| 优先级 | 判定标准 | 标记 |
|--------|---------|------|
| 🔴 **紧急** | 距投标截止<7天 或 预算/核心赛道高匹配 | 立即响应 |
| 🟡 **重要** | 距投标截止7-30天，且匹配核心业务赛道 | 本周内评估 |
| 🟢 **关注** | 距投标截止>30天 或 扩展业务赛道 | 纳入跟踪列表 |
| ⚪ **参考** | 中标公示/竞对分析/行业风向 | 信息备查 |

### 4. 线索标注体系

采集到的线索自动标记以下标签：

| 标签 | 含义 |
|------|------|
| `[招标预告]` | 采购意向公示，尚未正式发标 |
| `[正式招标]` | 已发布正式招标文件 |
| `[变更公告]` | 项目有更正/补充 |
| `[中标公示]` | 已出结果 |
| `[废标公告]` | 项目终止/废标 |

---

## 使用方式

### 快捷扫描

```
/bid-collection scan AI 大模型 采购 --days=7
/bid-collection scan 苏研 采购
/bid-collection scan 数字化转型 招标 --budget-min=1000000
/bid-collection scan 算力 租赁 招标 --days=30
```

### 启动定时监控

```
/bid-collection monitor
/bid-collection monitor --interval=60    # 每60分钟扫描一次
```

### 生成汇总报告

```
/bid-collection report
/bid-collection report --track=core              # 仅核心赛道
/bid-collection report --priority=urgent         # 仅紧急商机
/bid-collection report --output=detail           # 含内容摘要
```

### 管理监控源

```
/bid-collection list-sources
/bid-collection add-source https://example-bid-platform.cn
=======
## Core Collection Scope

### 1. Government Public Resource Trading Platforms (Core Channels)

| Category | Channel | Focus |
|----------|---------|-------|
| **National** | China Government Procurement (ccgp.gov.cn) | Central budget procurement, framework agreements, designated procurement |
| **National** | China Tendering & Bidding Public Service Platform (cebpubservice.com) | National tender notices, change notices, award announcements |
| **Provincial** | Provincial Public Resource Trading Centers | Provincial and municipal procurement projects |
| **Municipal** | Municipal Public Resource Trading Networks | City/county government procurement, construction, service procurement |
| **State-owned** | China Tendering & Bidding Network (cncbid.com) | Central SOE centralized procurement, specialized tenders |

### 2. SOE & Large Enterprise Procurement Platforms

| Platform | URL | Focus |
|----------|-----|-------|
| **China Mobile** | Procurement & Bidding (b2b.10086.cn) | SuYan procurement, ICT services, system construction |
| **China Unicom** | Procurement & Bidding (chinaunicombidding.cn) | Application development, O&M services, IT systems |
| **China Telecom** | Sunshine Procurement (ctyun.cn) | Cloud services, integration services, digital-intelligence projects |
| **CEC** | CEC E-Procurement Platform | Xinchuang projects, cybersecurity, system integration |
| **State Grid** | SGCC E-Commerce Platform (ecp.sgcc.com.cn) | Digital transformation, smart grid IT services |
| **CNPC** | Energy No.1 (energyahead.com) | IT infrastructure, industrial internet |
| **China Railway** | CREC Procurement Platform | Smart construction, BIM systems, project management |
| **CMHK/China Merchants** | CMHK Tendering Platform | Digital transformation, logistics technology |

### 3. Industry-Specific Tendering Websites

| Domain | Platform | URL | Focus |
|--------|----------|-----|-------|
| **AI/LLM** | Smart Computing Centers Procurement | — | Computing power leasing, model training, AI middleware |
| **Digitalization** | Digital Gov / Smart City Procurement | — | Government cloud, data governance, integrated services |
| **IT Services** | Software Exchange / IT Procurement | — | Software dev, system integration, O&M services |
| **Research** | University / Research Institute Procurement | — | Research equipment, lab systems, technology development |
| **Healthcare** | Medical Procurement Platforms | — | Healthcare IT, smart healthcare, HIS systems |
| **Education** | Education Equipment Procurement | — | Smart education, digital campus, teaching platforms |

### 4. Third-Party Tender Information Aggregators (Auxiliary Channels)

| Platform | URL | Purpose |
|----------|-----|---------|
| **Qianlima** | qianlima.com | General tender info aggregation |
| **Bidcenter** | bidcenter.com.cn | National procurement & tender info summary |
| **Zhaobiaord** | zhaobiaord.com | AI smart recommendation matching |
| **Bidizhaobiao** | bidizhaobiao.com | Big-data precision targeting |
| **Jianyu360** | jianyu360.com | Real-time lead push, competitive analysis |

---

## Core Capabilities

### 1. Intelligent Matching by Business Track

Based on your company's business domain and service types, tenders are automatically matched to the following tracks:

| Track | Keywords | Match Level |
|-------|----------|-------------|
| 🏢 **AI Technical Services** | AI, artificial intelligence, machine learning, NLP, CV, LLM | High |
| 🧠 **Large Language Models** | LLM, GPT, generative AI, vector database, RAG, fine-tuning | Dedicated |
| 🔬 **SuYan (Suzhou Research) Procurement** | SuYan, Suzhou Research, China Mobile Suzhou | Dedicated |
| 🖥 **System Construction/Dev** | Software dev, system integration, platform dev, microservices | Core |
| ☁️ **Computing Power & Model Services** | GPU, computing power, smart computing, model training, inference | Core |
| 📊 **Digital Transformation** | Digital transformation, data governance, data platform, data assets | Core |
| 🔒 **Information Security** | Cybersecurity, data security, classified protection, cryptography | Extended |
| 🌐 **Cloud Services** | Cloud platform, public/private/hybrid cloud, IaaS/PaaS | Extended |
| 📱 **Smart Applications** | Smart city, smart park, smart government, digital government | Extended |
| 👁 **AI Vision/Content** | Digital human, AIGC, video generation, VR/AR | Emerging |

### 2. Full Project Lifecycle Coverage

Covers all stages of the procurement lifecycle:

| Stage | Info Type | Value |
|-------|-----------|-------|
| ⏳ **Pre-tender Notice** | Procurement意向,需求公示, RFP notice | **Early positioning**, prepare bid materials |
| 📢 **Formal Tender** | Tender announcement, competitive磋商, competitive negotiation | **Core opportunity**, bid preparation |
| 🔄 **Change Notice** | Corrections, supplements, Q&A | Adjust bidding strategy in time |
| 🏆 **Award Announcement** | Winning candidate, deal announcement | Competitor analysis, industry insight |
| ❌ **Failed/Abandoned** | Tender cancellation, termination | Potential second-round opportunity |

### 3. Lead Priority Classification

| Priority | Criteria | Tag |
|----------|----------|-----|
| 🔴 **Urgent** | Deadline <7 days OR high budget/core track match | Respond immediately |
| 🟡 **Important** | Deadline 7-30 days AND matches core business track | Evaluate this week |
| 🟢 **Watch** | Deadline >30 days OR extended business track | Add to tracking list |
| ⚪ **Reference** | Award announcements, competitor analysis, industry trends | Info reference |

### 4. Lead Tagging System

| Tag | Meaning |
|-----|---------|
| `[Pre-tender]` | Procurement意向 announced, not yet formally issued |
| `[Open Tender]` | Formal tender documents released |
| `[Amendment]` | Project corrections/supplements issued |
| `[Awarded]` | Results announced |
| `[Canceled]` | Project terminated/abandoned |

---

## Usage

### Quick Scan

```
/bid-collection scan AI LLM procurement --days=7
/bid-collection scan SuYan procurement
/bid-collection scan digital transformation tender --budget-min=1000000
/bid-collection scan computing power lease tender --days=30
```

### Start Scheduled Monitoring

```
/bid-collection monitor
/bid-collection monitor --interval=60    # Scan every 60 minutes
```

### Generate Summary Report

```
/bid-collection report
/bid-collection report --track=core              # Core tracks only
/bid-collection report --priority=urgent         # Urgent leads only
/bid-collection report --output=detail           # With content summaries
```

### Manage Monitoring Sources

```
/bid-collection list-sources
/bid-collection add-source https://example-bid-platform.com
>>>>>>> 5210fda (Initial release: bid-collection v1.0.0 — Tender & Procurement Lead Collection Skill for Claude Code)
```

---

<<<<<<< HEAD
## 执行流程

### 模式1: `scan` — 实时扫描

```
1. 解析用户输入的关键词和参数（业务赛道、预算范围等）
2. 遍历所有监控渠道，使用WebSearch进行搜索
3. 对每个搜索结果使用WebFetch获取详情
4. 按业务赛道 + 项目阶段自动标注
5. 计算优先级评分（预算金额 × 赛道匹配度 × 时效因子）
6. 按[优先级][标签]排序输出结果表格
7. 结果保存至桌面 leads-output/bid/ 目录
```

### 模式2: `monitor` — 后台定时监控

```
1. 使用CronCreate创建定时任务
2. 默认每120分钟执行一次全渠道扫描
3. 每次扫描后增量比对（去重，基于URL/项目编号）
4. 新发现的商机通过PushNotification推送通知
5. 运行日志保存至 leads-output/bid/monitor.log
```

### 模式3: `report` — 报告生成

```
1. 读取 leads-output/bid/ 目录下历史数据
2. 按业务赛道、项目阶段汇总统计
3. 生成结构化Markdown报告
   - 📊 赛道分布统计（按预算规模和数量）
   - 📋 高价值商机TOP10
   - ⏰ 近期截止提醒（7天/15天/30天）
   - 🏢 重点采购方动态
   - 🔄 vs 上期新增/流失商机分析
4. 输出至桌面和控制台
=======
## Execution Flow

### Mode 1: `scan` — Real-Time Scan

```
1. Parse user keywords and parameters (business track, budget range, etc.)
2. Iterate through all monitored channels, use WebSearch to search
3. For each result, use WebFetch to get details
4. Auto-tag by business track + project stage
5. Calculate priority score (budget × track match × timeliness factor)
6. Output sorted table by [priority][tag]
7. Save results to desktop leads-output/bid/ directory
```

### Mode 2: `monitor` — Background Scheduled Scan

```
1. Create scheduled task using CronCreate
2. Default: full channel scan every 120 minutes
3. Incremental comparison each scan (dedup by URL/project ID)
4. PushNotification for newly discovered leads
5. Log to leads-output/bid/monitor.log
```

### Mode 3: `report` — Report Generation

```
1. Read historical data from leads-output/bid/
2. Aggregate by business track and project stage
3. Generate structured Markdown report
   - 📊 Track distribution (by budget and count)
   - 📋 Top 10 high-value leads
   - ⏰ Upcoming deadline reminders (7d/15d/30d)
   - 🏢 Key buyer activity
   - 🔄 New/lost leads vs. previous period
4. Output to desktop and console
>>>>>>> 5210fda (Initial release: bid-collection v1.0.0 — Tender & Procurement Lead Collection Skill for Claude Code)
```

---

<<<<<<< HEAD
## 输出格式示例

```
┌──────┬──────────────────────────────────────┬──────────────┬──────────────┬───────────┬────────────┐
│ 优先级 │ 项目名称                             │ 采购单位       │ 业务赛道      │ 预算(万)   │ 截止日期   │
├──────┼──────────────────────────────────────┼──────────────┼──────────────┼───────────┼────────────┤
│ 🔴   │ 2026年AI大模型训练平台建设项目           │ 中移苏研       │ 🧠 大模型     │ 800       │ 06-20     │
│ 🔴   │ 政务云数据中台建设项目                  │ 省大数据中心    │ 📊 数字化      │ 1200      │ 06-25     │
│ 🟡   │ 智慧园区综合管理平台开发                 │ 某高新区管委会   │ 📱 智慧应用    │ 500       │ 07-10     │
│ 🟡   │ AI算力资源池租赁服务                    │ 智算中心        │ ☁️ 算力       │ 300       │ 07-15     │
│ 🟢   │ 信息安全等级保护测评服务                 │ 市教育局        │ 🔒 安全       │ 80        │ 08-01     │
│ ⚪   │ XX省数字政府建设规划方案征集              │ 省政务办        │ 📊 数字化      │ —         │ —         │
└──────┴──────────────────────────────────────┴──────────────┴──────────────┴───────────┴────────────┘

📋 详细商机卡片:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 [紧急] 🧠 AI大模型训练平台建设项目
  采购单位: 中移（苏州）软件技术有限公司
  项目阶段: 正式招标
  预算金额: 800万元
  招标时间: 2026年6月10日
  截止日期: 2026年6月20日（剩余9天）
  项目需求: 采购AI大模型训练所需的高性能计算集群、分布式训练框架、数据标注平台……
  联系方式: 张工 0512-XXXXXXX
  信息来源: 中国移动采购与招标网
  链接: https://b2b.10086.cn/...
  ────────
  🎯 赛道匹配: AI大模型/高
  ⏰ 建议动作: 立即组织投标小组，筹备技术方案
=======
## Output Example

```
┌──────┬──────────────────────────────────────────────────┬──────────────────┬──────────────────┬──────────┬────────────┐
│ Pri  │ Project Name                                     │ Buyer             │ Track            │ Budget   │ Deadline   │
├──────┼──────────────────────────────────────────────────┼──────────────────┼──────────────────┼──────────┼────────────┤
│ 🔴   │ 2026 AI LLM Training Platform Construction       │ China Mobile SuYan│ 🧠 LLM           │ ¥8M      │ 06-20     │
│ 🔴   │ Government Cloud Data Middle Platform            │ Provincial Big Data│ 📊 Digital       │ ¥12M     │ 06-25     │
│ 🟡   │ Smart Park Integrated Management Platform Dev    │ Hi-tech Zone Admin│ 📱 Smart Apps    │ ¥5M      │ 07-10     │
│ 🟡   │ AI Computing Power Resource Pool Lease           │ Computing Center  │ ☁️ Computing      │ ¥3M      │ 07-15     │
│ 🟢   │ Information Security Classified Protection Audit │ City Education Bu.│ 🔒 Security      │ ¥800K    │ 08-01     │
│ ⚪   │ XX Province Digital Gov Planning Solicitation    │ Provincial Gov Of.│ 📊 Digital       │ —        │ —         │
└──────┴──────────────────────────────────────────────────┴──────────────────┴──────────────────┴──────────┴────────────┘

📋 Detailed Lead Card:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 [Urgent] 🧠 AI LLM Training Platform Construction
  Buyer: China Mobile (Suzhou) Software Technology Co.
  Stage: Open Tender
  Budget: ¥8,000,000
  Issue Date: 2026-06-10
  Deadline: 2026-06-20 (9 days remaining)
  Requirements: High-performance computing cluster, distributed training framework,
               data annotation platform for LLM training...
  Contact: Mr. Zhang +86-512-XXXXXXX
  Source: China Mobile Procurement & Bidding Network
  URL: https://b2b.10086.cn/...
  ────────
  🎯 Track Match: AI/LLM — High
  ⏰ Suggested Action: Assemble bid team immediately, prepare technical proposal
>>>>>>> 5210fda (Initial release: bid-collection v1.0.0 — Tender & Procurement Lead Collection Skill for Claude Code)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

<<<<<<< HEAD
## 注意事项

- 采集的信息均为**公开信息**，不涉及非公开/需登录内容
- 各公共资源交易平台接口各异，建议对重点渠道定期人工确认
- 监控频率建议不低于60分钟/次，避免被目标网站限流
- **高价值商机建议人工二次确认**后再投入应标资源
- 预算金额一般含暂列金，投标报价需结合招标文件详细要求
- 支持自定义添加行业/区域监控源
- 合规使用：遵守目标网站的 robots.txt 和使用条款
=======
## Notes

- All collected information is **publicly available**; no login or private data involved
- Different platforms have varying interfaces; regular manual verification of key channels is recommended
- Recommended monitoring interval ≥60 minutes to avoid rate limiting
- **High-value leads should be manually verified** before committing bid resources
- Budget figures typically include provisional sums; final pricing should reference detailed tender docs
- Custom industry/regional monitoring sources are supported
- Compliance: respect target websites' robots.txt and terms of service
>>>>>>> 5210fda (Initial release: bid-collection v1.0.0 — Tender & Procurement Lead Collection Skill for Claude Code)
