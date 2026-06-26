---
name: aky-public-opinion
description: "Professional-grade Chinese social media sentiment analysis report writer for government and enterprise use. Generates structured public opinion analysis reports covering risk assessment, communication data analysis, and actionable countermeasures. Supports 5 daily report types and 5 special event types including International Pressure, Diplomatic Sensitivity, and Ethnic/Ideological analysis. Enhanced with multi-tool international media collection: X.com trending (x-news-daily), headless browser scraping (agent-browser), built-in browser automation (browser-automation), web_fetch, and web_search for comprehensive international media information gathering and cross-validation. Use when the user asks: write a sentiment analysis report, analyze public opinion risk, do sentiment assessment, monthly sentiment summary, or any event requiring international public opinion tracking."
---

# Chinese Public Opinion & Sentiment Analysis Report Writer
## — 增强版：整合欧美媒体多工具采集

## Overview

本技能生成专业级中文舆情分析报告。在原版基础上，深度融合五大数据采集工具链，显著增强对**欧美媒体、国际舆论场**的信息收集与分析能力。涵盖从社交媒体实时热点到传统新闻媒体报道的多层次、多源交叉验证体系。

**整合的工具链：**
| 工具/技能 | 定位 | 适用场景 |
|-----------|------|---------|
| **`x-news-daily`** | X/Twitter 社交热点 | 实时趋势、西方社交舆论、热搜话题 |
| **`agent-browser`** | 无头浏览器自动化 | 访问互动型网站、搜索表单、获取动态页面、登录后抓取 |
| **`browser-automation`** | 内置浏览器工具 | 复杂 SPA 网站、需要截图的媒体页面、多 Tab 协作 |
| **`web_fetch`** | 网页内容抓取 | 简单静态页面、RSS 摘要、快速获取文本 |
| **`web_search`** | 搜索引擎 | 背景调查、多源检索、时效性新闻搜索 |

## Report Categories

### A. Daily Reports (5 types, 9 subtypes)

| Type | Purpose | Typical Length |
|------|---------|---------------|
| **Investigation & Analysis Report (调研分析报告)** | 多维度调研：事实发现 + 法律框架 + 社会/政治/经济/文化影响 + 风险评估 | 2,000-5,000 chars |
| **Rapid Assessment (快报)** | 突发事件快速研判 | 800-1,500 chars |
| **Special Report (专报)** | 特定事件系统性深度分析 | 2,000-4,000 chars |
| **Deep Research Report (研报)** | 政策导向深度研究 & 行业分析 | 3,000-6,000 chars |
| **Retrospective Report (复盘)** | 重大事件事后全面复盘 | 2,000-4,000 chars |
| **Monthly Report (月报)** | 月度综述 + 风险预判 | 2,500-4,000 chars |

### B. Special Event Reports (5 types)

| Type | Purpose | Typical Length |
|------|---------|---------------|
| **International/Pressure** | Foreign pressure, trade friction, geopolitics | 3,000-6,000 chars |
| **Ethnic/Religious/Ideological** | Ethnic policy, anti-China narratives, ideology | 2,500-5,000 chars |
| **Industrial-Economic Security** | Supply chain security, trade barriers, sanctions | 3,000-6,000 chars |
| **Governance Innovation/Social Phenomena** | Social governance innovation, emerging trends | 2,500-5,000 chars |
| **Diplomatic Sensitivity (JP/US etc.)** | Bilateral relations-triggered sentiment | 2,000-4,000 chars |

## Pre-flight Checklist

1. Verify user provides sufficient event details (time, location, actors, sequence, communication data)
2. If info is insufficient, proactively ask: event basics, current communication landscape, available data
3. For **Investigation & Analysis** type, additionally verify: phenomenon timeline, key actors/players, operational/business model, legal/regulatory framework, domestic/local impact channels, existing warnings or prior incidents, social/political/economic/cultural impact dimensions
3. Confirm report type with user. If unclear, infer:
   - Emerging tech/finance/cross-border phenomenon needing investigation → Investigation & Analysis
   - Single breaking incident → Rapid Assessment
   - Developed incident needing multi-dimensional analysis → Special Report
   - Macro policy / intl relations / industry security → Deep Research
   - Incident mostly resolved, needs lessons learned → Retrospective
   - Periodic summary → Monthly
   - Foreign pressure / intl conflict → Special Event

---

## Workflow

### Step 1: Multi-Tool Information Collection（信息采集四层级）

这是本增强版的核心环节。按以下四个层级依次或按需展开数据采集：

---

#### 🟢 第一层：X.com 社交媒体实时热点（Tier 1 — Social Media Pulse）

**工具：** `x-news-daily` 技能

**适用场景：** 了解事件在西方社交媒体上的实时热度、舆论走向、KOL 发言、Hashtag 趋势

**操作指引：**
1. 确定关键词（事件名、人物名、国家/地区名、政策名等），建议中英文关键词各一个
2. 调用 x-news-daily，传入英文关键词（如无英文关键词，使用事件对应的英文翻译）
3. 分析返回的 X 热门新闻 Top 10：
   - 提取主流叙事框架（framing）
   - 识别高频负面关键词
   - 记录互动量较高的帖文倾向（点赞/转推比）
   - 标记是否有政治人物、主流媒体账号参与讨论
4. 如果需要对比观点，可以切换关键词（如 `China+tariff` / `China+trade`）多次调用

**常见欧美相关关键词示例：**
- `China` / `Beijing` — 对华整体舆论
- `Taiwan` — 台湾议题
- `South China Sea` — 南海争端
- `Xinjiang` / `Uyghur` — 新疆议题
- `US China` / `China trade` / `tariff` — 中美贸易
- `TikTok ban` / `Huawei` — 科技压制
- `human rights` / `Hong Kong` — 人权/香港
- `CHIPS act` / `Semiconductor` — 半导体/芯片
- `Belt and Road` — 一带一路
- `South China Sea` / `PH China` — 南海/中菲

---

#### 🔵 第二层：欧美主流媒体直接内容抓取（Tier 2 — Direct Media Scraping）

**工具：** `agent-browser` 技能（首选） / `browser-automation` 内置浏览器（备选）

**适用场景：** 需要获取特定欧美媒体的新闻报道原文、评论、深度报道；网站有搜索功能、登录墙（有限绕过）、复杂交互

**两大工具定位差异：**
| 维度 | agent-browser | browser-automation (内置工具) |
|------|---------------|------------------------------|
| 速度 | 极快（Rust 核心） | 一般 |
| 元素选取 | 基于 Access Tree ref 确定性选取 | ARIA ref / role 选取 |
| JSON 输出 | 原生支持 | 不支持 |
| Session 隔离 | 支持多 session | 支持 Tab 标签管理 |
| 截图/PDF | 支持 | 支持（功能更丰富） |
| 首选场景 | 快速搜索 + 提取内容 | 复杂页面 + 多标签 + 视觉验证 |

**操作指引（agent-browser）：**

```bash
# 1. 导航到媒体首页或搜索页
agent-browser open <URL>

# 2. 等待加载完成，截取交互元素
agent-browser wait --load networkidle
agent-browser snapshot -i --json

# 3. 根据 ref 找到搜索框，输入关键词
agent-browser fill @<ref> "<keyword>"
agent-browser press "Enter"
agent-browser wait --load networkidle

# 4. 再次截图，获取搜索结果
agent-browser snapshot -i --json

# 5. 点击结果链接进入文章
agent-browser click @<ref>
agent-browser wait --load networkidle

# 6. 获取文章标题和正文
agent-browser get text @<title-ref> --json
agent-browser get html @<content-ref> --json
# 或直接使用 JavaScript 获取全文
agent-browser eval "document.querySelector('article').innerText" --json
```

**操作指引（browser-automation 内置浏览器）：**

```bash
# 1. 检查浏览器状态
action="status"

# 2. 打开新的标签页（带 label 便于追踪）
action="open" url="<媒体URL>" label="media-scrape"

# 3. 获取页面快照
action="snapshot" targetId="media-scrape" refs="aria"

# 4. 交互操作（填写搜索框、点击等）
action="act" targetId="media-scrape" kind="fill" ref="<ref>" text="<keyword>"
action="act" targetId="media-scrape" kind="click" ref="<ref>"

# 5. 等待加载后再次快照获取结果
action="snapshot" targetId="media-scrape" refs="aria"
```

---

#### 🟡 第三层：搜索引擎 + 快速网页抓取（Tier 3 — Search & Quick Fetch）

**工具：** `web_search` + `web_fetch`

**适用场景：** 背景调查、补全上下文、获取多个信源对比、事件全貌梳理

**操作指引：**

```bash
# 1. 搜索引擎检索（多种搜索策略）
web_search query="<英文关键词> site:reuters.com OR site:apnews.com <时间范围>"
web_search query="<中文关键词> <事件名> 外媒报道"
web_search query="<英文关键词> opinion analysis <年月>"

# 2. 时效性过滤（设置 freshness 参数）
web_search query="<关键词>" freshness="day"    # 当天新闻
web_search query="<关键词>" freshness="week"   # 近一周
web_search query="<关键词>" freshness="month"  # 近一月

# 3. 地域偏好（设置 country 参数）
web_search query="<关键词>" country="US"       # 美媒倾向结果
web_search query="<关键词>" country="GB"       # 英媒倾向结果

# 4. 抓取命中文章内容
web_fetch url="<文章URL>"
```

---

#### 🟣 第四层：多源交叉验证与去重（Tier 4 — Cross-Validation & Dedup）

**目的：** 将前三层收集到的信息进行合并、去重、交叉验证

**操作流程：**
1. **合并来源**：将 X 热点、媒体文章、搜索结果汇总成一个原始素材池
2. **去重**：剔除不同源的同篇报道（同一家通讯社的不同转载）
3. **立场标注**：给每条素材标记倾向性（正面/负面/中立 + 政治光谱定位）
4. **信源可靠性评级**：
   | 评级 | 典型信源 |
   |------|---------|
   | A+（直接引用） | Reuters, AP, AFP, Bloomberg |
   | A（可信度高） | BBC, NYT, WSJ, FT, The Guardian, The Economist |
   | B+（需交叉验证） | CNN, Politico, Axios, The Hill |
   | B（有一定倾向） | Fox News, MSNBC, Washington Post |
   | C（显著倾向，仅作参考） | Breitbart, Daily Wire, HuffPost, The Intercept |
   | UGC（需谨慎） | X/Twitter 个人账号帖文 |
5. **记录时间戳**：每条信息的采集时间和网站更新时间

---

### Step 2: 分析并确定报告类型

综合用户需求和采集到的素材特征确定报告类型。对涉及欧美舆论的事件，额外判断：

- **是否存在"西方叙事框架"**—— 事件是否被西方媒体赋予特定 framing（如"democracy vs authoritarian"、"human rights concern"、"rule of law"）
- **是否存在多国媒体报道差异**—— 美、英、法、德、日、澳等国的报道侧重点是否不同
- **是否被政治人物利用**—— 是否有拜登、国会、欧盟议员等官方表态
- **社交媒体是否成为扩音器**—— X 上的 trending 讨论是否放大了媒体报道

### Step 3: 撰写报告

Strictly follow the selected type's structure. Core requirements:

1. **Precise title**: Summarizes event essence. No exclamation marks or question marks
2. **Data citation**: Use specific numbers. Attribute sources and time points. **对于欧美来源，必须标明媒体名称 + 日期，如"据路透社6月2日报道..."**
3. **Risk elaboration**: Each risk point follows the chain: "trigger condition -> risk behavior -> risk consequence"
4. **Practical recommendations**: Each recommendation must be actionable, assignable to a responsible body, with expected outcomes
5. **Formal language**: Official document style. No colloquial or emotional expressions
6. **国际舆论维度（新增）**：对于涉及国际舆情的事件，增设一个 **"国际舆论反应"** 小节，总结欧美媒体/政府/社交平台的舆情态势

### Step 4: 交付

Output as Markdown. The report uses Chinese throughout since it targets Chinese government/enterprise audiences.

---

## 欧美媒体源快速参考（Media Source Quick Reference）

以下列出常用欧美主流媒体及其访问策略：

### 综合新闻通讯社

| 媒体 | URL | 推荐工具 | 备注 |
|------|-----|---------|------|
| **Reuters** | reuters.com | web_fetch（最简单） | 无 paywall，直接抓取 |
| **Associated Press** | apnews.com | web_fetch（最简单） | 无 paywall，直接抓取 |
| **AFP** | afp.com | web_search 检索 | 通过新闻聚合获取 |
| **Bloomberg** | bloomberg.com | web_search + web_fetch | 部分 paywall，用检索摘要 |

### 英美国主流

| 媒体 | URL | 推荐工具 | 备注 |
|------|-----|---------|------|
| **BBC** | bbc.com/news | web_fetch | 无 paywall，可直接抓取 |
| **The Guardian** | theguardian.com | web_fetch | 无 paywall，可直接抓取 |
| **NYT** | nytimes.com | agent-browser / browser-automation | 有 paywall，需利用搜索结果 |
| **WSJ** | wsj.com | web_search + 摘要 | 强 paywall |
| **Washington Post** | washingtonpost.com | web_search + 摘要 | 强 paywall |
| **CNN** | cnn.com | web_fetch / agent-browser | 无 paywall，但页面动态加载 |
| **Fox News** | foxnews.com | web_fetch | 无 paywall |
| **NBC News** | nbcnews.com | web_fetch | 无 paywall |
| **ABC News** | abcnews.go.com | web_fetch | 无 paywall |
| **The Economist** | economist.com | web_search + 摘要 | 强 paywall |

### 政治 & 政策

| 媒体 | URL | 推荐工具 | 备注 |
|------|-----|---------|------|
| **Politico** | politico.com | web_fetch / agent-browser | 部分动态加载 |
| **The Hill** | thehill.com | web_fetch | 无 paywall |
| **Axios** | axios.com | web_fetch | 无 paywall |
| **Foreign Affairs** | foreignaffairs.com | web_search + 摘要 | 有 paywall |
| **Foreign Policy** | foreignpolicy.com | web_search + 摘要 | 有 paywall |

### 国际关系 & 中国报道专项

| 媒体 | URL | 推荐工具 | 备注 |
|------|-----|---------|------|
| **SCMP** | scmp.com | web_search + web_fetch | 部分 paywall |
| **Nikkei Asia** | asia.nikkei.com | web_fetch | 有限 paywall |
| **DW** | dw.com | web_fetch | 德语/英语，无 paywall |
| **France24** | france24.com | web_fetch | 英语版，无 paywall |
| **Al Jazeera** | aljazeera.com | web_fetch | 无 paywall |
| **The Diplomat** | thediplomat.com | web_fetch | 有限 paywall |

---

## 报告中国际舆论部分的核心分析框架

当事件涉及欧美舆论时，在标准报告结构中嵌入 **第五部分：国际舆论反应**：

### 国际舆论反应（示例结构）

```
## 五、国际舆论反应

### 5.1 欧美主流媒体报道基调
[直接引用 Reuters / AP / BBC / NYT 等报道标题和核心论点]
[标注各媒体报道的倾向性：负面/中立/正面]
[分析是否存在统一的"叙事框架"（framing）]

### 5.2 西方政府及政要表态
[引用白宫声明、国务院发言人、欧盟理事会、议员提案等]
[分析其表态是象征性还是实质性]
[关注背后的政策走向信号]

### 5.3 社交媒体与国际舆论场
[引用 X/Twitter 相关趋势数据]
[关键 KOL 或智库学者的表态]
[分析舆论发酵的扩散路径]

### 5.4 与中国驻外使领馆、官媒的舆论对抗
[我国驻外使领馆发言、大使投书]
[CGTN / Xinhua 等外宣报道的传播效果]
[是否存在舆论反制措施及效果]
```

---

## 典型场景速查表

| 用户需求 | 采集策略 | 推荐工作流 |
|---------|---------|-----------|
| "分析西方媒体怎么报这个事" | 第二层优先 | agent-browser 搜索主要媒体 + web_fetch 无墙站点 |
| "国外社交媒体上什么风向" | 第一层优先 | x-news-daily 关键词检索 + 分析叙事框架 |
| "这个事件在国际上整体舆论如何" | 第一层 + 第二层 + 第三层 | X热点 + 主流媒体 + 搜索引擎全面扫描 |
| "美国/英国/欧盟官方的表态" | 第三层 + 第二层 | web_search 政府官网 + agent-browser 抓取发言人页面 |
| "借这个事件写一份舆情专报" | 第一层 -> 第二层 -> 第三层 -> 第四层 | 全链路由浅入深，交叉验证 |
| "做一份中美关系月度舆情" | 第一层（多关键词）+ 第二层 + 第三层 | 多次 x-news-daily + 定期媒体扫描 |
| "帮我查查今天欧美主要报纸的头版" | 第二层 + 第三层 | agent-browser 截图报纸首页 + web_search 新闻聚合 |

---

## Key Writing Principles

- All analysis based on facts. No speculation or exaggeration
- Risk assessment must be concrete and operational
- Use official document stock phrases where appropriate (see references)
- Rigorous wording when covering negative information. No pre-judged positions
- **Attribute external information sources (重要)**:
  - X 热点 -> 标注 "据X平台热门趋势数据（截至某月某日）"
  - 媒体文章 -> 标注 "据路透社/美联社/英国广播公司某月某日报道"
  - 搜索结果 -> 标注 "据公开网络信息汇总"
  - 政府表态 -> 标注 "据美国白宫官网/欧盟理事会官网声明"
- Communication data must be precise to the number
- Timeline marked to the day (hour:minute when necessary)
- For location references, use xx to replace specific city names (maintain consistency)

## Enumeration Standards

Two enumeration systems are available. Match to report type:

### System A: First/Second/Third (for sentiment reports)
Used in: Rapid Assessment, Special Report, Monthly Report, Retrospective
> "First, ... Second, ... Third, ..."

### System B: 一是/二是/三是 (for investigation reports)
Used in: Investigation & Analysis Report
> "一是基本情况...二是运营模式...三是风险分析..."

**Nested enumeration rules:**
- Top-level section markers: 一、二、三、四、五
- Sub-level using: 一是/二是/三是  (with full-width Chinese numbering)
- Third level: (一)(二)(三) or bullet points
- Maximum 3 levels of nesting

## Investigation Report Writing Standards（调研分析报告专有）

| Principle | Description |
|-----------|-------------|
| **Opening formula** | Begin with "工作发现" / "调研发现" / "网络巡查发现" — establishes investigative posture |
| **Fact-first structure** | Facts before analysis: 基本情况->运营模式->境内传播->社会政治经济文化影响->风险评估->对策建议 |
| **Legal citations** | Full regulatory title + issuing body + date. E.g.: "2026年2月，中国人民银行等八部门联合发布《关于进一步防范和处置虚拟货币等相关风险的通知》" |
| **Bilingual naming** | First mention of foreign terms: original + Chinese translation + abbreviation if any |
| **一是/二是/三是 pattern** | Use throughout for structured enumeration of findings |
| **Data precision** | Specific numbers, dates, platform names, currency values |
| **Social/Political/Economic/Cultural impact** | Each dimension separately analyzed: affected groups, governance implications, market consequences, cultural value shifts |

## Legal Citation Format

When citing Chinese laws, regulations, or policy documents:
```
[Issuance date], [Issuing body] [Document Title]
Example: 2026年2月，中国人民银行等八部门联合发布《关于进一步防范和处置虚拟货币等相关风险的通知》
```
Key legal sources commonly cited in investigations:
- 中国人民银行 + multi-ministry notices
- 《中华人民共和国刑法》第X条
- 《中华人民共和国网络安全法》
- 《中华人民共和国数据安全法》
- 《中华人民共和国个人信息保护法》
- State Council opinions and regulations
- Local government risk warnings (cite when applicable)

## Core Risk Analysis Logic (Three-Layer Progression)

Each risk point follows this structure:

1. **Risk trigger / context** - "Currently...", "As... approaches...", "With X node approaching..."
2. **Risk behavior and actors** - "Some netizens may...", "Certain self-media accounts...", "Foreign forces..."
3. **Risk consequences and impact** - "Leading to...", "Triggering...", "Exacerbating...", "Causing damage to..."

**Complete example:**
> Guard against incitement leading to group polarization. As several sensitive anniversaries approach (trigger), certain netizens may exploit "patriotic" framing to spread inflammatory rhetoric on platforms (behavior), escalating social antagonism and undermining stability (consequence).

## Recommendation Writing Standards

Each recommendation: **Responsible body + Specific action + Expected outcome**
- Macro before micro
- Online and offline measures in parallel
- Both "treat symptoms" and "treat root causes"
- Quantity: Rapid Assessment 3-5 / Special Report & Retrospective 5-8 / Research Report 4-6 / Monthly 8-10

## Reference Files

`references/templates.md` - Full template structures, formatting specs, and composition guidelines for all 10 report types
