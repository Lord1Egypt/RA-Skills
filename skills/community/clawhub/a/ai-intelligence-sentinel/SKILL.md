---
slug: ai-intelligence-sentinel
name: AI前沿哨兵
version: 2.1.0
description: AI情报追踪系统 + 大数据业界洞察双引擎。当用户需要追踪AI领域动态、生成AI晨报/晚报时使用。触发词：AI情报、AI哨兵、AI资讯、AI动态、科技新闻、论文追踪、开源项目追踪、晨报、晚报。**大数据洞察模块**：大数据洞察、数据中台、湖仓一体、数据治理、荣耀对标、华为OPPOvivo数据平台。
trigger: "AI情报|AI哨兵|AI资讯|AI动态|科技新闻|论文追踪|开源项目追踪|晨报|晚报|大数据洞察|数据中台|湖仓一体|数据治理|荣耀对标"
tools: [shell, filesystem, http]
author: xiaopengs
license: MIT
---

# AI前沿哨兵

> 你的AI情报指挥中心 + 大数据业界洞察双引擎。一键采集、智能分析、自动生成报告。

---

## 🔒 安全声明

**本技能是合法的开源情报工具，具备以下安全特性：**

| 安全特性 | 说明 |
|---------|------|
| ✅ 开源透明 | 所有代码开源，可审计 |
| ✅ 无恶意代码 | 不包含后门、木马或恶意脚本 |
| ✅ 无数据窃取 | 不收集用户隐私数据 |
| ✅ 合规采集 | 仅获取公开可访问的信息 |
| ✅ MIT许可 | 开源协议，可自由使用 |

**项目地址**：https://github.com/xiaopengs/ai-sentinel

---

## ⚠️ 执行指南（核心）

### 🎯 报告质量标准

**必须达到以下三条标准，否则重做：**

| 角色 | 必须满足的价值 |
|------|---------------|
| **CEO** | 看完能在3分钟内做出一个战略决策 |
| **产品经理** | 能发现一个竞品动态或用户机会 |
| **程序员** | 能找到一个可用的技术方案或开源项目 |

---

### 📋 执行流程（严格执行）

#### 🔵 模式一：AI情报追踪

**Step 1: 信息采集（并行搜索）**

**使用 search_web 工具，一次性搜索以下关键词：**

```
1. "AI 大模型 发布 2026年4月" （当月最新发布）
2. "OpenAI Google Anthropic 最新" （三巨头动态）
3. "GitHub AI 开源项目 trending" （技术趋势）
4. "AI 融资 产品 2026年4月" （行业动态）
5. "Agent 具身智能 技术" （前沿技术）
```

**Step 2: 深度追踪（获取完整内容）**

**对关键链接使用 fetch_web 获取完整内容：**
- 官方博客文章 → 提取关键数据点
- GitHub项目 → 提取星标数、技术栈、核心功能
- 技术媒体 → 提取具体数字和趋势判断

**Step 3: 加载用户配置（个性化定制）**

```bash
# 加载用户自定义配置文件（由用户自行创建和维护）
load_config ./USER.md    # 用户偏好设置：关注领域、行业背景
load_config ./MEMORY.md  # 项目上下文：当前关注的技术方向
```

> 📌 **说明**：以上文件为用户自行创建的配置文件，用于实现报告个性化，非隐私收集。

**Step 4: 生成报告**

**保存路径：** `./AI哨兵/晚报/YYYY-MM-DD.md`

---

#### 🟢 模式二：大数据业界洞察（新增）

**适用场景：** 数据中台建设追踪、湖仓一体、实时数仓、数据治理、荣耀/手机厂商对标分析

**Step 1: 信息采集（并行搜索）**

**使用 search_web 工具，一次性搜索以下关键词：**

```
1. "数据中台 2026 趋势" （行业趋势）
2. "湖仓一体 实时数仓 最新" （架构演进）
3. "华为 荣耀 OPPO vivo 数据平台" （竞品对标）
4. "数据治理 隐私计算 2026" （治理与安全）
5. "大模型 数据中台 融合" （AI+Data融合）
```

**Step 2: 深度追踪**

**对关键链接使用 fetch_web 获取完整内容：**
- 白皮书/研究报告 → 提取核心观点和关键数据
- 企业技术博客 → 提取实战案例和经验教训
- 开源项目 → 提取技术选型和最佳实践

**Step 3: 结构化整理**

按以下维度整理：
- 核心观点（3-5条）
- 与荣耀数据中台的关联
- 可落地的行动建议

**Step 4: 生成报告**

**保存路径：** `./大数据洞察/日报/YYYY-MM-DD.md`

---

## 📝 报告模板（严格执行，飞书适配版）

### AI情报报告模板

```markdown
# 🛡️ AI哨兵日报 | YYYY-MM-DD（周X）

> 🎯 **今日核心洞察**：[一句话总结今天最重要的信号，CEO 3秒看完]

---

## 📰 今日情报

### 🔥 P0 头条（今日最重要，最多3条）

#### [标题](链接)

**一句话价值**：[CEO能看懂的70字核心价值，必须包含数字]

| 维度 | 内容 |
|------|------|
| **来源** | [机构/作者] |
| **发布时间** | YYYY-MM-DD |
| **核心数据** | [关键数字] |
| **技术要点** | [1-2个技术关键词] |

**对我司启示**：⚡ [一句话说明对AI业务的价值]

---

### 📊 P1 重要动态（4-8条）

#### [标题](链接)

**价值速览**：🎯 [50字核心价值]

| 维度 | 内容 |
|------|------|
| **来源** | [机构/作者] |
| **发布时间** | YYYY-MM-DD |
| **关键数字** | [星标数/用户数/性能提升等] |

---

### 🔧 P2 技术追踪（3-5条）

#### [标题](链接)

**技术要点**：🔧 [技术关键词 + 核心功能]

| 维度 | 内容 |
|------|------|
| **GitHub** | [star数/语言/技术栈] |
| **适用场景** | [可落地的使用场景] |

---

### 📈 P3 行业动态（2-3条）

#### [标题](链接)

**一句话价值**：📈 [行业影响]

---

## 🎯 行动建议

| 优先级 | 行动项 | 负责人 | 截止日期 |
|--------|--------|--------|----------|
| P0 | [紧急且重要] | - | - |
| P1 | [重要不紧急] | - | - |

---

> 📅 报告生成时间：YYYY-MM-DD HH:mm | 数据来源：公开网络
```

### 大数据洞察报告模板

```markdown
# 📊 大数据业界洞察 | YYYY-MM-DD

> 🎯 **今日核心洞察**：[一句话总结今天最重要的数据领域信号]

---

## 🏔️ 行业趋势

### [标题](链接)

**核心观点**：📌 [3-5条关键结论]

| 维度 | 内容 |
|------|------|
| **来源** | [机构/作者/发布时间] |
| **核心数据** | [关键数字] |
| **技术方向** | [技术关键词] |

**对荣耀启示**：⚡ [与数据中台建设的关联]

---

## 🏢 竞品动态

### 华为数据中台

#### [标题](链接)

**核心实践**：🔧 [关键做法和经验]

| 维度 | 内容 |
|------|------|
| **发布时间** | YYYY-MM-DD |
| **可借鉴点** | [1-2条] |

### OPPO/vivo/小米

#### [标题](链接)

**核心动态**：📱 [厂商动态]

---

## ⚙️ 技术前沿

### 数据架构

#### [标题](链接)

**技术要点**：🔧 [湖仓一体/实时数仓/数据编织等]

| 维度 | 内容 |
|------|------|
| **技术栈** | [相关技术] |
| **适用场景** | [业务场景] |

### AI+Data融合

#### [标题](链接)

**融合要点**：🤖 [大模型+数据中台]

---

## 💡 行动建议

| 优先级 | 行动项 | 说明 | 参考链接 |
|--------|--------|------|----------|
| P0 | [紧急且重要] | [说明] | [链接] |
| P1 | [重要不紧急] | [说明] | [链接] |

---

> 📅 报告生成时间：YYYY-MM-DD HH:mm | 适用于：荣耀数据中台团队
```

---

## 📚 信息源清单

### 🔵 AI情报信息源

| 类型 | 来源 | URL |
|------|------|-----|
| 官方发布 | OpenAI Blog | https://openai.com/blog |
| 官方发布 | Anthropic Blog | https://www.anthropic.com/news |
| 官方发布 | Google AI Blog | https://blog.google/technology/ai/ |
| 开源趋势 | GitHub Trending | https://github.com/trending |
| 学术论文 | arXiv cs.AI | https://arxiv.org/list/cs.AI/recent |
| 技术社区 | Hacker News | https://news.ycombinator.com |
| 技术媒体 | The Verge | https://www.theverge.com |
| AI追踪 | AI News | https://venturebeat.com/category/ai/ |

### 🌐 Follow Builders 信息源（v2.1.0新增）

**集成方式**：安装 [follow-builders](https://github.com/zarazhangrui/follow-builders) 技能后，通过其中央Feed获取AI Builder动态。

**追踪的X/Twitter账号（25人）：**

| Builder | Handle | 身份 |
|---------|--------|------|
| Andrej Karpathy | @karpathy | AI研究者 |
| Swyx | @swyx | AI Engineer |
| Josh Woodward | @joshwoodward | Google |
| Kevin Weil | @kevinweil | OpenAI |
| Peter Yang | @petergyang | 产品 |
| Nan Yu | @thenanyu | 研究 |
| Madhu Guru | @realmadhuguru | 工程 |
| Amanda Askell | @AmandaAskell | Anthropic |
| Cat Wu | @_catwu | 产品 |
| Thariq | @trq212 | 研究 |
| Google Labs | @GoogleLabs | Google |
| Amjad Masad | @amasad | Replit CEO |
| Guillermo Rauch | @rauchg | Vercel CEO |
| Alex Albert | @alexalbert__ | Anthropic |
| Aaron Levie | @levie | Box CEO |
| Ryo Lu | @ryolu_ | 工程 |
| Garry Tan | @garrytan | YC |
| Matt Turck | @mattturck | FirstMark |
| Zara Zhang | @zarazhangrui | 记者 |
| Nikunj Kothari | @nikunj | 工程 |
| Peter Steinberger | @steipete | iOS开发 |
| Dan Shipper | @danshipper | Every |
| Aditya Agarwal | @adityaag | 工程 |
| Sam Altman | @sama | OpenAI CEO |
| Claude | @claudeai | Anthropic |

**追踪的AI播客（6个）：**

| 播客 | URL |
|------|-----|
| Latent Space | https://www.youtube.com/@LatentSpacePod |
| Training Data | https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8 |
| No Priors | https://www.youtube.com/@NoPriorsPodcast |
| Unsupervised Learning | https://www.youtube.com/@RedpointAI |
| The MAD Podcast | https://www.youtube.com/@DataDrivenNYC/videos |
| AI & I by Every | https://www.youtube.com/playlist?list=PLuMcoKK9mKgHtW_o9h5sGO2vXrffKHwJL |

**使用方式**：在信息采集阶段，执行 `cd .skills/follow-builders/scripts && node prepare-digest.js 2>/dev/null`，从输出JSON的 `x` 和 `podcasts` 字段提取Builder动态，作为辅助信息源融入报告。

### 🟢 大数据洞察信息源

| 类型 | 来源 | URL |
|------|------|-----|
| 权威报告 | Gartner | https://www.gartner.com/en |
| 权威报告 | IDC | https://www.idc.com |
| 企业白皮书 | 阿里云数据中台 | https://dp.alibaba.com |
| 企业白皮书 | 华为云 | https://www.huaweicloud.com |
| 技术博客 | 字节跳动技术博客 | https://bytedance.tech |
| 技术博客 | 美团技术团队 | https://tech.meituan.com |
| 技术媒体 | InfoQ | https://www.infoq.com |
| 技术媒体 | 36氪 | https://36kr.com |
| 技术媒体 | 虎嗅 | https://huxiu.com |
| 开源项目 | Apache Flink | https://flink.apache.org |
| 开源项目 | Apache Spark | https://spark.apache.org |
| 开发者社区 | 掘金 | https://juejin.cn |

---

## 📁 项目结构

```
ai-sentinel/
├── SKILL.md              # 技能定义文件
├── README.md             # 项目说明
├── docs/                 # 文档目录
│   └── BIGDATA_INSIGHT_REQUIREMENT.md  # 大数据洞察需求文档
├── templates/            # 报告模板
│   ├── morning_report.md  # AI晨报模板
│   ├── evening_report.md  # AI晚报模板
│   └── bigdata_report.md # 大数据洞察报告模板
├── scripts/              # 脚本目录
│   └── reporter.py       # 报告生成脚本
├── reports/              # 报告输出
│   ├── AI哨兵/           # AI情报报告
│   │   ├── 晨报/
│   │   └── 晚报/
│   └── 大数据洞察/       # 大数据洞察报告
│       ├── 日报/
│       └── 月报/
├── config/               # 配置目录
├── references/           # 参考资料
└── webui/                # Web界面
```

---

## 🚀 使用方式

### AI情报追踪
```
使用 ai-intelligence-sentinel 技能生成今日AI情报报告
使用 AI哨兵 生成今日AI晚报
```

### 大数据洞察
```
使用 ai-intelligence-sentinel 技能生成大数据洞察日报
使用 AI哨兵 追踪华为数据中台最新动态
```

---

## 📈 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 2.1.0 | 2026-05-14 | 新增Follow Builders信息源：25个AI Builder X动态 + 6个顶级AI播客 |
| 2.0.0 | 2026-04-21 | 新增大数据业界洞察模块 |
| 1.4.2 | 2026-04-10 | 优化搜索策略和报告模板 |
| 1.0.0 | 2026-04-08 | 初始版本 |
