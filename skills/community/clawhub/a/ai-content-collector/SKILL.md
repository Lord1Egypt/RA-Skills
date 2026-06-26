---
name: ai-content-collector
description: "AI及汽车行业信息扫描收集工具。从指定渠道搜索和收集AI/汽车行业最新动态，整理为结构化Excel表格。覆盖：研发、营销、制造运营、财经人力、AI基础设施、模型能力、智能体开发平台、AI安全。触发：(1)收集AI/汽车行业动态、新闻、资讯 (2)扫描行业信息 (3)整理资料到Excel (4)信息周报/日报"
tools: ["WebSearch", "WebFetch", "Bash", "Read", "Write"]
---

# AI 资料收集工具

从指定渠道搜索和收集 AI 及汽车行业最新资料，整理成结构化 Excel 表格。

---

## 🔴 强制规则（违反任何一条即判定为失败）

### 规则1: 禁止使用不可靠来源

**禁止收录的来源**（这些是论坛/社区/UGC，不是新闻，不可交叉印证）：

| 禁止来源 | 原因 |
|----------|------|
| zhihu.com（知乎） | 用户生成内容，观点非事实，无法交叉验证 |
| weibo.com（微博） | 社交媒体，信息未经核实 |
| bbs、论坛、贴吧 | 用户讨论，非权威报道 |
| quora.com、reddit.com | UGC内容，同上 |
| 任何问答页面 | "如何评价XX"不是新闻 |
| toutiao.com（今日头条） | 算法推荐聚合，信息源混杂不可靠 |

**必须使用的来源**（权威媒体，可交叉印证）：

| 来源 | 域名 | 可靠性 |
|------|------|--------|
| IT之家 | ithome.com | ✅ 科技新闻 |
| 腾讯新闻 | new.qq.com | ✅ 综合新闻 |
| 新华网 | xinhuanet.com | ✅ 官方权威 |
| 澎湃新闻 | thepaper.cn | ✅ 深度报道 |
| 36氪 | 36kr.com | ✅ 行业资讯 |
| 新浪财经 | finance.sina.com.cn | ✅ 财经数据 |
| 每日经济新闻 | nbd.com.cn | ✅ 财经+科技 |
| 机器之心 | jiqizhixin.com | ✅ AI专业媒体 |
| 财新网 | caixin.com | ✅ 财经权威 |
| 第一财经 | yicai.com | ✅ 财经+产业 |
| 中国新闻网 | chinanews.com | ✅ 官方新闻 |
| 证券时报 | stcn.com | ✅ 上市公司信息 |
| 各公司官方博客 | blog.google、openai.com | ✅ 一手信息 |

> ⚠️ 搜索结果中出现 zhihu.com/weibo.com/toutiao.com 链接时，**直接跳过**，不要点击、不要抓取、不要收录。

### 规则2: 必须抓取详情页，禁止使用搜索摘要

**搜索结果中的 snippet ≠ 摘要**。每条收录的信息必须经过以下流程：

```
搜索发现链接 → web_fetch抓取原文 → 从原文提取核心要点 → 写入摘要
```

**禁止的摘要写法**：
```
❌ "关键词搜索结果：个人怎么才能使用OpenAI?"     → 这是搜索snippet
❌ "如何评价OpenAI最新发布的GPT-5.4 mini?"        → 这是搜索snippet
❌ "OpenAI发布了新模型"                            → 没有从原文提取
```

**合格的摘要写法**：
```
✅ "谷歌在Cloud Next大会发布第八代TPU，首次拆分训练与推理专用芯片。推理成本降低40%，Meta和Anthropic已签大单。"  → 从原文提取，含具体数据
✅ "K2.6开源发布，1T参数MoE架构，256K上下文。SWE-Bench Pro超越GPT-5.4和Claude Opus 4.6。"  → 从原文提取，含评测数据
```

### 规则3: 每次执行必须重新搜索，禁止复用历史数据

- 用户每次要求收集信息时，**必须从头执行全部搜索**，不得复用之前的搜索结果
- 即使同一用户短时间内多次请求，也要重新搜索
- 不得使用缓存的搜索结果或之前生成的数据
- **所有搜索调用必须实际执行**，不能假设"上次搜过了所以跳过"
- **绝对不能因为"上次已搜索过同类信息"而省略任何搜索步骤**

### 规则4: 日期必须精确到日

- 发布时间必须是 `YYYY-MM-DD` 格式
- `YYYY-MM` 格式 → **丢弃**
- `YYYY` 格式 → **丢弃**
- 无法确认精确日期的记录 → **丢弃**

### 规则5: 禁止回退到纯英文来源

- **不允许因为"中文站点无法访问"而放弃中文来源**
- 当 `web_search` 中文结果不足时，必须使用 `web_fetch` 直接抓取中文新闻站列表页（见步骤2B降级策略）
- 英文来源（The Verge、TechCrunch等）**只能作为补充，不能成为主体**
- 最终报告中，中文来源占比必须 ≥60%

### 规则6: 多渠道交叉印证，禁止单一来源垄断

- **单一域名链接占比不得超过50%**：如果超过50%的记录链接来自同一域名（如全部来自ithome.com），必须从其他渠道补充
- **每条记录至少2个不同渠道验证**：对每个事件，必须从至少2个不同权威媒体搜索确认，选择最权威可信的链接作为主链接
- **摘要应综合多渠道信息**：核心要点摘要应融合多个渠道的报道内容，而非仅依赖单一来源
- **文档/链接选择最权威来源**：优先选择：官方来源 > 通讯社(新华社等) > 深度媒体(澎湃/财新) > 综合媒体(腾讯新闻) > 科技媒体(IT之家/36氪)

---

## 依赖检查（必须首先执行）

```bash
python3 -c "import openpyxl" 2>/dev/null || echo "MISSING: openpyxl"
```

| 依赖 | 用途 | 安装命令 |
|------|------|----------|
| python3 | 生成Excel | 系统自带 |
| openpyxl | Excel文件生成 | `pip3 install openpyxl` |

**如果依赖缺失，输出以下提示后停止**：
```
⚠️ 缺少必要依赖：[依赖名]
请运行：[安装命令]
安装完成后重新执行本技能。
```

---

## 📊 质量基线（必须达标）

以下标准基于实际产出周报的质量验证，每条记录必须对标：

| 指标 | 最低标准 | 优秀标准 | 实际案例 |
|------|----------|----------|----------|
| 总记录数 | ≥15条 | ≥25条 | 25条（周报） |
| 类别覆盖 | ≥6个类别 | 8个类别全覆盖 | 8/8全覆盖 |
| 摘要字数 | 50-100字 | 70-100字含具体数据 | 平均76字 |
| 日期格式 | YYYY-MM-DD | YYYY-MM-DD | 100%合规 |
| 链接有效性 | ≥90%可访问 | 100%可访问 | 100%有效 |
| 来源具体度 | 公司/机构名 | 公司+部门/团队 | "Google Cloud"非"Google" |
| 不可靠来源占比 | 0% | 0% | 0%知乎/微博 |
| 中文来源占比 | ≥60% | ≥80% | 80%中文来源 |
| 单一域名占比 | ≤50% | ≤30% | 无单一域名超50% |
| 交叉印证率 | ≥50%记录 | ≥80%记录 | 至少2渠道验证 |

### 每条记录质量对照

**优秀记录示例**（必须达到此质量）：

```
材料类别: AI基础设施
来源/发布机构: Google Cloud                    ← 具体到部门
材料名称: 谷歌发布第八代TPU v8双芯：TPU 8t训练+TPU 8i推理  ← 事件+具体型号+关键差异
发布时间: 2026-04-22                           ← 精确到日
核心要点摘要: 谷歌在Cloud Next大会发布第八代TPU，首次拆分训练与推理专用芯片。推理成本降低40%，Meta和Anthropic已签大单。同时宣布7.5亿美元基金推动企业AI采用。  ← 从原文提取，含具体数据
文档/链接: https://www.thepaper.cn/newsDetail_forward_33029483  ← 深度媒体为主链接
印证来源: https://www.36kr.com/p/xxx, https://www.ithome.com/0/941/418.htm  ← 不同域名佐证
```

**不合格记录示例**（必须避免）：

```
❌ 来源/发布机构: 知乎               → 禁止来源
❌ 来源/发布机构: 科技公司            → 太泛
❌ 材料名称: 如何评价OpenAI最新发布   → 这是知乎问答标题，不是新闻事件
❌ 核心要点摘要: 关键词搜索结果：...   → 搜索snippet，未抓取原文
❌ 核心要点摘要: 谷歌发布了新芯片      → 缺少具体数据
❌ 发布时间: 2026-04                 → 必须精确到日
❌ 文档/链接: https://www.zhihu.com/  → 禁止来源
❌ 文档/链接: https://www.theverge.com/... → 英文来源，必须有中文源交叉印证
❌ 印证来源: https://www.ithome.com/0/941/xxx → 与主链接同域名，不算交叉印证
❌ 印证来源: 无 → 每条记录应有≥1个不同域名的佐证
❌ 全部15条链接都是ithome.com → 单渠道垄断，必须分散到多个媒体
```

### 类别最低记录数

| 类别 | 周报最低条数 | 说明 |
|------|-------------|------|
| AI基础设施 | ≥3 | 含算力、芯片、数据中心 |
| 模型能力 | ≥3 | 含大模型发布、开源、评测 |
| 智能体开发平台 | ≥2 | 含Agent、MCP、开发平台 |
| AI安全 | ≥2 | 含合规、治理、政策 |
| 研发 | ≥2 | 含技术创新、政策支持 |
| 制造运营 | ≥2 | 含量产、产线、机器人 |
| 财经人力 | ≥1 | 含融资、营收、人事 |
| 营销 | ≥1 | 含市场、品牌、合作 |

---

## 🚫 绝对禁止事项

1. **禁止编造日期**：发布时间必须是文章中明确标注的日期
2. **禁止使用模糊日期**：发布时间必须是 `YYYY-MM-DD` 格式，不接受 `YYYY-MM` 或 `YYYY`
3. **禁止收录旧数据**：严格按用户指定时间范围过滤
4. **禁止收录产品介绍页**：只收录新闻/事件/报告发布，不收录常驻产品页面
5. **禁止自行推测内容**：无法核实的内容直接丢弃
6. **禁止收录知乎/微博/论坛/今日头条内容**：只收录权威新闻媒体和官方来源
7. **禁止用搜索snippet当摘要**：必须抓取原文提取核心要点
8. **禁止摘要无数据**：核心要点摘要必须包含至少1个具体数值（百分比、金额、数量、排名等）
9. **禁止来源笼统**：来源/发布机构必须具体到公司/部门，不能写"行业"、"科技公司"等泛称
10. **禁止标题空洞**：材料名称必须包含具体事件或关键差异点
11. **禁止复用历史搜索数据**：每次执行必须重新搜索
12. **禁止跳过详情抓取**：每条记录必须从原文页面获取信息
13. **禁止因中文搜索不足就放弃中文来源**：必须执行降级策略（步骤2B），不得直接回退英文媒体
14. **禁止提示用户"技术限制"作为借口**：中文来源不足时主动用web_fetch抓取列表页，不得输出"部分中文站点无法访问"
15. **禁止单渠道垄断**：单一域名链接占比超过50%时，必须从其他渠道补充并替换
16. **禁止无交叉印证**：每条记录至少应有1个不同域名的佐证链接，重大事件必须有2个不同渠道

---

## ✅ 搜索策略：三级搜索确保中文来源

### 核心原则：绝不放弃中文来源

```
第一级：web_search + site: 限定权威来源（主力）
    ↓ 结果不足？
第二级：web_fetch 直接抓取中文新闻站列表页（降级）
    ↓ 仍不足？
第三级：web_search 英文来源补充（仅补充，不超过40%）
```

### 第一级：站内搜索锁定权威来源

用 `site:` 限定权威媒体，避免泛搜返回知乎：

```javascript
// ✅ 正确：限定权威媒体来源
web_search({ query: "site:ithome.com 大模型 发布 最新", freshness: "week", count: 10 })
web_search({ query: "site:new.qq.com AI 芯片 最新", freshness: "week", count: 10 })

// ❌ 错误：泛搜返回大量知乎结果
web_search({ query: "AI大模型 最新" })  // 会返回大量 zhihu.com 链接
```

### 第二级：web_fetch 直接抓取中文新闻站列表页（关键降级策略）

**当 `web_search` 返回的中文结果不足10条时，必须执行此步骤。这是解决"中文站点无法访问"问题的核心策略。**

直接 `web_fetch` 访问以下中文新闻站的列表页/频道页，从页面中提取最新文章标题和链接：

```javascript
// IT之家 AI频道 - 最可靠的中文科技新闻源
web_fetch({ url: "https://www.ithome.com/tag/AI/", fetchInfo: "提取页面中所有AI相关新闻的标题、链接和日期" })
web_fetch({ url: "https://www.ithome.com/tag/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/", fetchInfo: "提取页面中所有人工智能相关新闻的标题、链接和日期" })

// 36氪 AI频道
web_fetch({ url: "https://36kr.com/information/AI/", fetchInfo: "提取页面中所有AI相关新闻的标题、链接和日期" })

// 机器之心 - AI专业媒体
web_fetch({ url: "https://www.jiqizhixin.com/", fetchInfo: "提取首页所有文章的标题、链接和日期" })

// 澎湃新闻 科技频道
web_fetch({ url: "https://www.thepaper.cn/channel_25951", fetchInfo: "提取科技频道所有新闻的标题、链接和日期" })

// 腾讯新闻 科技频道
web_fetch({ url: "https://new.qq.com/ch/tech/", fetchInfo: "提取科技频道所有新闻的标题、链接和日期" })

// 新浪财经 科技频道
web_fetch({ url: "https://finance.sina.com.cn/tech/", fetchInfo: "提取科技频道所有新闻的标题、链接和日期" })
```

**执行条件**：
- 步骤2A 的 `web_search` 返回的中文权威来源链接 < 10条
- 或者搜索结果中超过50%是知乎/微博等不可靠来源

**从列表页提取信息后**：
1. 从页面中找到日期在 `DATE_START` ~ `DATE_END` 范围内的文章
2. 对每篇文章执行 `web_fetch` 抓取详情页
3. 提取核心要点写入摘要

### 第三级：英文来源补充（严格限制）

英文来源**只能作为中文来源的补充**，不得超过总记录数的40%：

```javascript
// 仅在中文来源不足时使用
web_search({ query: "site:theverge.com AI latest", freshness: "week", count: 5 })
web_search({ query: "site:techcrunch.com AI model release", freshness: "week", count: 5 })
web_search({ query: "site:arstechnica.com AI chip", freshness: "week", count: 5 })
```

> ⚠️ 英文来源必须有中文权威媒体交叉印证。如果某个事件只有英文媒体报道、无任何中文来源提及，可以收录但需在摘要末尾标注 `[仅英文来源]`。

---

## 收集流程（7步）

```
步骤1: 解析需求 → 计算日期范围
  ↓
步骤2A: 站内搜索（site:限定权威来源，排除知乎微博）
  ↓ 中文结果不足10条？
步骤2B: web_fetch 直接抓取中文新闻站列表页（降级策略，必须执行）
  ↓ 仍不足？
步骤2C: 英文来源补充（不超过总数40%）
  ↓
步骤3: 逐条 web_fetch 抓取原文详情（必须步骤，不可跳过）
  ↓
步骤4: 从原文提取结构化信息 + 日期验证 + 事实核查
  ↓
步骤5: 生成 Excel 文件（必须完成）
  ↓
步骤6: 输出文本表格 + 质量自检
```

---

## 步骤1: 解析需求，计算日期范围

| 用户表述 | 计算方式 | 示例（今天是2026-04-23） |
|----------|----------|--------------------------|
| 最近一周 | 今天 - 6天 ~ 今天 | 2026-04-16 ~ 2026-04-23 |
| 最近两周 | 今天 - 13天 ~ 今天 | 2026-04-09 ~ 2026-04-23 |
| 最近一个月 | 今天 - 29天 ~ 今天 | 2026-03-24 ~ 2026-04-23 |

将日期范围记录为 `DATE_START` 和 `DATE_END`，后续搜索必须使用。

---

## 步骤2A: 站内搜索锁定权威来源

### 搜索方式

```javascript
// 方式1：site: 限定权威来源（推荐）
web_search({ query: "site:ithome.com 大模型 发布 最新", freshness: "week", count: 10 })

// 方式2：OR 组合多个权威来源
web_search({ query: "site:ithome.com OR site:36kr.com OR site:new.qq.com AI 发布", freshness: "week", count: 10 })

// 方式3：负向排除不可靠来源
web_search({ query: "AI大模型 发布 最新 -site:zhihu.com -site:weibo.com -site:toutiao.com", freshness: "week", count: 10 })
```

> ⚠️ 搜索结果中如果出现 zhihu.com / weibo.com / toutiao.com 链接，**直接丢弃**，不要点击或抓取。

### 搜索模板（共15次，确保多渠道覆盖）

> ⚠️ **关键原则**：每组搜索必须分散到不同权威媒体站点，不得全部集中在 ithome.com。每次搜索应交替使用不同的 site: 组合。

#### 搜索组A：模型厂商动态（4次，覆盖4组不同媒体）

```javascript
// A1：国际厂商 - IT之家+36氪
web_search({ query: "site:ithome.com OR site:36kr.com OpenAI Anthropic Google Gemini 大模型 发布", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// A2：国际厂商 - 腾讯新闻+澎湃（与A1不同渠道交叉）
web_search({ query: "site:new.qq.com OR site:thepaper.cn OpenAI Anthropic Google 大模型 发布 最新", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// A3：国内厂商 - 每经+新浪财经
web_search({ query: "site:nbd.com.cn OR site:finance.sina.com.cn 阿里千问 字节豆包 智谱 腾讯混元 Kimi 发布", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// A4：开源模型 - 机器之心+第一财经（排除知乎）
web_search({ query: "site:jiqizhixin.com OR site:yicai.com DeepSeek Meta Llama 开源模型 发布 -site:zhihu.com -site:weibo.com -site:toutiao.com", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })
```

#### 搜索组B：AI基础设施与智能体（3次，覆盖3组不同媒体）

```javascript
// B1：AI算力/芯片 - IT之家+新浪财经
web_search({ query: "site:ithome.com OR site:finance.sina.com.cn AI算力 芯片 GPU TPU 数据中心 英伟达", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// B2：AI算力/芯片 - 36氪+每经（与B1交叉）
web_search({ query: "site:36kr.com OR site:nbd.com.cn AI算力 英伟达 AMD 芯片 数据中心", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// B3：智能体/Agent - 机器之心+腾讯新闻
web_search({ query: "site:jiqizhixin.com OR site:new.qq.com AI Agent 智能体 MCP 框架 平台", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })
```

#### 搜索组C：AI安全与政策（2次，覆盖2组不同媒体）

```javascript
// C1：AI安全 - 新华网+澎湃
web_search({ query: "site:xinhuanet.com OR site:thepaper.cn AI安全 合规 治理 监管 政策", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// C2：AI政策 - 政府官方+财新
web_search({ query: "site:gov.cn OR site:caixin.com 人工智能 政策 法规 工信部 国务院", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })
```

#### 搜索组D：汽车行业（2次，覆盖2组不同媒体）

```javascript
// D1：汽车行业 - 新浪财经+每经
web_search({ query: "site:finance.sina.com.cn OR site:nbd.com.cn 汽车 智驾 产销 比亚迪 吉利", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// D2：智能制造 - 证券时报+腾讯新闻
web_search({ query: "site:stcn.com OR site:new.qq.com 上汽 美的 三一 智能制造 AI", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })
```

#### 搜索组E：机器人与咨询报告（2次，覆盖2组不同媒体）

```javascript
// E1：机器人 - 澎湃+第一财经
web_search({ query: "site:thepaper.cn OR site:yicai.com 人形机器人 量产 特斯拉 宇树 优必选", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })

// E2：咨询报告 - 36氪+IT之家
web_search({ query: "site:36kr.com OR site:ithome.com 麦肯锡 德勤 Gartner IDC 行业报告 AI", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 10, country: "CN", language: "zh" })
```

#### 搜索组F：交叉印证搜索（2次，确保多渠道覆盖）

```javascript
// F1：本周重大事件 - 多站交叉（不限定site:，排除不可靠来源）
web_search({ query: "AI 大模型 发布 芯片 最新新闻 -site:zhihu.com -site:weibo.com -site:toutiao.com", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 15, country: "CN", language: "zh" })

// F2：汽车+AI交叉 - 多站交叉
web_search({ query: "汽车 智能制造 机器人 AI 最新 -site:zhihu.com -site:weibo.com -site:toutiao.com", freshness: "week", date_after: DATE_START, date_before: DATE_END, count: 15, country: "CN", language: "zh" })
```

---

## 步骤2B: 降级策略 — web_fetch 直接抓取中文新闻站

**触发条件**：步骤2A返回的中文权威来源链接 < 10条

**执行方式**：并行 web_fetch 以下列表页，从中提取文章标题、链接、日期：

| 站点 | 列表页URL | 抓取目标 |
|------|-----------|----------|
| IT之家 | `https://www.ithome.com/tag/AI/` | AI标签页所有文章 |
| IT之家 | `https://www.ithome.com/tag/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD/` | 人工智能标签页 |
| 36氪 | `https://36kr.com/information/AI/` | AI频道 |
| 机器之心 | `https://www.jiqizhixin.com/` | 首页文章列表 |
| 澎湃新闻 | `https://www.thepaper.cn/channel_25951` | 科技频道 |
| 腾讯新闻 | `https://new.qq.com/ch/tech/` | 科技频道 |
| 新浪科技 | `https://finance.sina.com.cn/tech/` | 科技频道 |
| 每经网 | `https://www.nbd.com.cn/columns/232/` | 科技频道 |

**操作步骤**：

```
1. 并行 web_fetch 所有列表页
2. 从返回的HTML/Markdown中提取：
   - 文章标题
   - 文章链接（补全为完整URL）
   - 发布日期（与 DATE_START~DATE_END 比对）
3. 筛选日期范围内的文章
4. 对筛选出的文章逐条 web_fetch 抓取详情页
5. 从详情页提取核心要点
```

> ⚠️ 列表页 web_fetch 可能返回403（部分站点有反爬），如果某个站点403，跳过该站点，继续抓取其他站点。不要因为一个站点403就放弃所有中文来源。

---

## 步骤2C: 英文来源补充（严格限制）

**触发条件**：步骤2A + 2B 仍无法收集到 ≥15条中文来源记录

**执行方式**：

```javascript
web_search({ query: "site:theverge.com AI model release latest", freshness: "week", count: 5 })
web_search({ query: "site:techcrunch.com AI chip infrastructure", freshness: "week", count: 5 })
web_search({ query: "site:arstechnica.com AI safety policy", freshness: "week", count: 5 })
web_search({ query: "site:blog.google OR site:openai.com announcement", freshness: "week", count: 5 })
```

**限制**：
- 英文来源记录数 ≤ 总记录数的40%
- 每条英文记录必须有中文权威媒体交叉印证
- 无中文印证的标注 `[仅英文来源]`

---

## 步骤3: 抓取原文详情（核心步骤，不可跳过）

**这是防止"搜索snippet当摘要"的关键步骤。**

对每一条搜索结果：

1. **检查链接域名**：如果是 zhihu.com/weibo.com/论坛/toutiao.com → 直接跳过
2. **web_fetch 抓取原文**：获取完整文章内容
3. **从原文提取**：发布日期、核心数据、事件细节
4. **如果 web_fetch 返回403或空**：跳过该链接，不要用搜索snippet替代

### 不同站点的抓取策略

| 站点 | 抓取方式 | 说明 |
|------|----------|------|
| IT之家、36氪、澎湃、腾讯新闻 | **web_fetch** | 通常允许访问 |
| 新华网、新浪财经、第一财经 | **web_fetch** | 通常允许访问 |
| 财新网、每经网 | **web_fetch** | 通常允许访问 |
| 机器之心 | **web_fetch** | AI专业媒体，通常允许 |
| 知乎、微博、微信、今日头条 | **直接跳过** | 禁止收录 |

> ⚠️ 如果 web_fetch 返回 403 或空内容，**丢弃该条记录**。绝不能用搜索snippet代替原文摘要。

---

## 步骤4: 提取结构化信息 + 交叉印证 + 日期验证

### 7个字段

| 字段 | 格式要求 | 合格示例 | 不合格示例 |
|------|----------|----------|------------|
| 材料类别 | 8选1 | AI基础设施 | 科技 |
| 来源/发布机构 | 具体到公司/部门 | Google Cloud | 知乎、行业 |
| 材料名称 | 具体事件+关键指标 | 谷歌发布第八代TPU v8双芯：TPU 8t训练+TPU 8i推理 | AI芯片发布 |
| 发布时间 | **必须 YYYY-MM-DD** | 2026-04-22 | 2026-04 |
| 核心要点摘要 | 50-100字，含≥1个具体数据，综合多渠道 | 推理成本降低40%（36氪），Meta和Anthropic已签大单（澎湃） | 关键词搜索结果：... |
| 文档/链接 | 最权威可信的原文URL | https://www.thepaper.cn/... | https://www.zhihu.com/... |
| 印证来源 | ≥1个不同域名的佐证链接 | https://www.36kr.com/..., https://finance.sina.com.cn/... | 无、同域名链接 |

### 交叉印证流程（每条记录必须执行）

```
1. 识别事件关键词 → 提取核心实体（如"谷歌 TPUv8"）
2. 用关键词在至少1个不同权威媒体搜索验证
   web_search({ query: "谷歌 TPUv8 发布 site:new.qq.com OR site:36kr.com", freshness: "week", count: 5 })
3. 找到佐证链接 → 记录到「印证来源」字段
4. 选择最权威的链接作为主「文档/链接」
5. 综合多渠道信息写入摘要，重要数据标注来源
```

**链接权威性优先级**（选择主链接时参考）：

```
1. 官方来源（openai.com、blog.google）     → 最高权威
2. 通讯社/官方媒体（xinhuanet.com）         → 官方背书
3. 深度媒体（thepaper.cn、caixin.com）      → 深度调查
4. 综合新闻（new.qq.com、chinanews.com）    → 广泛传播
5. 行业媒体（36kr.com、jiqizhixin.com）     → 专业领域
6. 科技媒体（ithome.com）                   → 快速报道
```

> ⚠️ 如果某个事件只能找到单一来源，在「印证来源」列填"单源"，摘要末尾标注 `[待核实]`。

### 日期验证（每条记录必须通过，任一不通过则丢弃）

```
□ 发布时间是否为 YYYY-MM-DD 格式？（不是则丢弃）
□ 发布时间是否 >= DATE_START？（不是则丢弃）
□ 发布时间是否 <= DATE_END？（不是则丢弃）
□ 发布时间是否合理？（不是未来日期，不是1年前的日期）
```

### 来源可靠性验证

```
□ 链接域名是否为权威媒体？（知乎/微博/论坛/今日头条 → 丢弃）
□ 来源/发布机构是否具体？（"行业"/"科技公司" → 丢弃）
□ 摘要是否从原文提取？（搜索snippet → 丢弃）
□ 摘要是否含具体数据？（无数据 → 重写或丢弃）
□ 英文来源是否≤40%？（超过 → 减少英文记录）
□ 印证来源是否≥1个不同域名？（单一来源标注[待核实]）
□ 单一域名链接是否≤50%？（超过 → 必须从其他渠道补充）
```

### 事实核查

对重大事件（新模型发布、政策法规、企业重大合作、融资数据），必须2个不同权威来源交叉验证。只能找到1个来源时，摘要末尾标注 `[待核实]`。

### 去重

- 按 URL 去重
- 按事件去重：同一事件保留信息最全且日期最新的一条
- 按标题去重：标题高度相似(>80%)视为同一事件

---

## 步骤5: 生成 Excel 文件（必须完成）

使用 Python + openpyxl 生成：

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from datetime import datetime

wb = Workbook()
ws = wb.active
ws.title = "信息扫描周报"

headers = ["材料类别", "来源/发布机构", "材料名称", "发布时间", "核心要点摘要", "文档/链接", "印证来源"]
hfont = Font(name='Arial', bold=True, color='FFFFFF', size=11)
hfill = PatternFill(start_color='2F5496', end_color='2F5496', fill_type='solid')
border = Border(left=Side(style='thin'), right=Side(style='thin'),
    top=Side(style='thin'), bottom=Side(style='thin'))

for col, h in enumerate(headers, 1):
    c = ws.cell(row=1, column=col, value=h)
    c.font, c.fill, c.border = hfont, hfill, border
    c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

cat_colors = {
    'AI基础设施': 'E2EFDA', '模型能力': 'D6E4F0', '智能体开发平台': 'FCE4D6',
    'AI安全': 'F2DCDB', '研发': 'D9E2F3', '制造运营': 'E2EFDA',
    '财经人力': 'FFF2CC', '营销': 'EDEDED',
}

link_font = Font(name='Arial', size=10, color='0563C1', underline='single')

for ri, item in enumerate(data, 2):
    for ci, val in enumerate(item, 1):
        ws.cell(row=ri, column=ci, value=val)
    for ci in range(1, 8):
        cell = ws.cell(row=ri, column=ci)
        cell.border = border
        cell.font = Font(name='Arial', size=10)
        cell.alignment = Alignment(vertical='center', wrap_text=True)
    color = cat_colors.get(item[0])
    if color:
        ws.cell(row=ri, column=1).fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
    ws.cell(row=ri, column=1).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.cell(row=ri, column=4).alignment = Alignment(horizontal='center', vertical='center')

    # 文档/链接列（F列）- 设置为可点击超链接
    url_cell = ws.cell(row=ri, column=6)
    url = str(url_cell.value or '')
    if url.startswith('http'):
        url_cell.hyperlink = url
        url_cell.font = link_font
    else:
        url_cell.font = Font(name='Arial', size=10)

    # 印证来源列（G列）- 设为可点击超链接
    # 规则：如果有多个佐证链接，只取第一个设为hyperlink（openpyxl限制），
    #       其余链接以纯文本显示在下方，用户可复制到浏览器打开
    ref_cell = ws.cell(row=ri, column=7)
    ref_val = str(ref_cell.value or '')
    ref_urls = [u.strip() for u in ref_val.replace('，', ',').split(',') if u.strip().startswith('http')]
    if len(ref_urls) >= 1:
        ref_cell.hyperlink = ref_urls[0]
        ref_cell.font = link_font
        if len(ref_urls) > 1:
            # 多个佐证：第一个可点击，其余附在单元格值中
            ref_cell.value = ref_val
    elif ref_val and ref_val != '单源':
        ref_cell.font = Font(name='Arial', size=10)

ws.column_dimensions['A'].width = 16
ws.column_dimensions['B'].width = 22
ws.column_dimensions['C'].width = 52
ws.column_dimensions['D'].width = 12
ws.column_dimensions['E'].width = 65
ws.column_dimensions['F'].width = 50
ws.column_dimensions['G'].width = 50
ws.freeze_panes = 'A2'
ws.auto_filter.ref = f'A1:G{len(data)+1}'

date_str = datetime.now().strftime("%Y-%m-%d")
filepath = f"信息扫描周报_{date_str}.xlsx"
wb.save(filepath)
print(f"已保存: {filepath}，共 {len(data)} 条记录")
```

**openpyxl 未安装时降级为 CSV**：
```python
import csv
date_str = datetime.now().strftime("%Y-%m-%d")
filepath = f"信息扫描周报_{date_str}.csv"
with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(["材料类别", "来源/发布机构", "材料名称", "发布时间", "核心要点摘要", "文档/链接", "印证来源"])
    for item in data:
        writer.writerow(item)
```

---

## 步骤6: 输出文本表格 + 质量自检

输出文本表格后，必须执行质量自检：

```
| 材料类别 | 来源 | 材料名称 | 发布时间 | 核心要点摘要 | 文档/链接 |
|----------|------|----------|----------|--------------|----------|
| 模型能力 | OpenAI | GPT-Image-2发布 | 2026-04-21 | ... | https://... |
```

### 质量自检清单（必须逐项检查并报告）

```
□ 总记录数是否 ≥15条？
□ 8个类别是否都有覆盖？
□ 所有日期是否为 YYYY-MM-DD 格式？
□ 所有链接域名是否为权威媒体（无知乎/微博/论坛/今日头条）？
□ 所有摘要是否从原文提取（无"关键词搜索结果"字样）？
□ 所有摘要是否含具体数据？
□ 所有来源/发布机构是否具体到公司/部门？
□ 是否所有搜索都是本次新执行的（非历史数据复用）？
□ 中文来源占比是否 ≥60%？
□ 英文来源是否 ≤40%？
□ 单一域名链接占比是否 ≤50%？（如ithome.com不超过50%）
□ 交叉印证率是否 ≥50%？（至少一半记录有≥2个不同渠道佐证）
□ 所有「印证来源」是否为不同域名？（不能与「文档/链接」同域名）
```

如果自检不通过，必须补充搜索和修正，直到达标。

---

## 扫描对象参考

### 国家机构
国务院、工信部、信通院、发改委、中国汽车工业协会、自动化所、国家网信办

### 咨询公司
麦肯锡、波士顿、德勤、普华永道、毕马威、安永、IBM、Gartner、IDC

### 模型厂商
Google(Gemini)、OpenAI、Meta(Llama)、阿里(千问)、字节(豆包)、百度(文心)、腾讯(混元)、月之暗面(Kimi)、智谱(GLM)、DeepSeek

### 机器人厂商
特斯拉(Optimus)、波士顿动力、优必选、银河通用、宇树科技、松延动力

### 头部企业
美的、比亚迪、上汽、三一、吉利

---

## 权威搜索来源

搜索时用 `site:` 限定以下来源，或用 `-site:zhihu.com -site:weibo.com` 排除不可靠来源：

| 来源 | 搜索词建议 | 可靠性 |
|------|------------|--------|
| IT之家 | `site:ithome.com` | ✅ 权威科技媒体 |
| 腾讯新闻 | `site:new.qq.com` | ✅ 综合新闻 |
| 新华网 | `site:xinhuanet.com` | ✅ 官方权威 |
| 澎湃新闻 | `site:thepaper.cn` | ✅ 深度报道 |
| 36氪 | `site:36kr.com` | ✅ 行业资讯 |
| 新浪财经 | `site:finance.sina.com.cn` | ✅ 财经数据 |
| 每日经济新闻 | `site:nbd.com.cn` | ✅ 财经+科技 |
| 机器之心 | `site:jiqizhixin.com` | ✅ AI专业媒体 |
| 财新网 | `site:caixin.com` | ✅ 财经权威 |
| 第一财经 | `site:yicai.com` | ✅ 财经+产业 |

### 模型能力评估渠道

| 评估渠道 | 网址 |
|----------|------|
| LMArena | https://lmarena.ai |
| DataLeader | https://www.datalearner.com/leaderboards |
| SuperCLUE | https://www.superclueai.com |
| Artificial Analysis | https://artificialanalysis.ai |

### 上市公司信息

| 渠道 | 网址 |
|------|------|
| 巨潮资讯网 | http://www.cninfo.com.cn |
| 港交所披露易 | https://www.hkexnews.hk |

---

## 可选增强 Skill 安装指南

以下 Skill 非必需，但安装后可显著提升搜索和抓取效果：

### multi-search-engine（推荐，无需 API Key）

```bash
npx clawhub@latest install multi-search-engine
```

增强能力：17引擎聚合搜索 + `tbs=qdr:w` 时间过滤 + 微信公众号搜索 + `site:` 站内搜索

### xcrawl-search + xcrawl-scrape（解决403反爬）

```bash
npx clawhub@latest install xcrawl-search
npx clawhub@latest install xcrawl-scrape
```

增强能力：绕过99%反爬机制 + JS渲染 + 中文位置语言优化

> 安装后需按 xcrawl Skill 的说明配置 API Key。安装和配置请遵循各 Skill 的官方文档。

---

## 注意事项

1. **站内搜索优先**：用 `site:ithome.com` 等限定权威来源，避免泛搜返回知乎
2. **排除不可靠来源**：搜索时加 `-site:zhihu.com -site:weibo.com -site:toutiao.com` 排除论坛和社交媒体
3. **必须抓取原文**：每条记录必须 web_fetch 原文，搜索snippet不能替代摘要
4. **禁止复用历史数据**：每次执行必须重新搜索，不得使用缓存或之前的搜索结果
5. **禁止知乎/微博/今日头条来源**：只收录权威新闻媒体和官方来源，确保可交叉印证
6. **绝不放弃中文来源**：web_search 中文结果不足时，必须执行步骤2B（web_fetch抓取中文站列表页），不得直接回退英文媒体
7. **中文来源占比 ≥60%**：英文来源只能作为补充，不超过40%
8. **时间过滤**：web_search 用 `freshness:"week"`
9. **日期验证不可跳过**：每条记录必须 YYYY-MM-DD 且在范围内
10. **事实核查**：重大事件2源交叉验证
11. **宁缺毋滥**：无法确认日期或事实的条目直接丢弃
12. **必须有链接**：文档/链接列不能为空，且必须是权威媒体
13. **必须生成Excel**：步骤5不能跳过
14. **并行搜索**：所有搜索并行执行
15. **403处理**：web_fetch 返回403时丢弃该条，不用snippet替代
16. **质量自检**：生成Excel前，对照「质量自检清单」逐项检查
17. **摘要必须有数据**：每条摘要必须含≥1个具体数值
18. **来源必须具体**：来源/发布机构必须具体到公司/部门名
19. **列表页降级必执行**：中文搜索结果不足时必须抓取列表页，不能跳过
20. **多渠道搜索**：每次搜索组必须覆盖不同媒体站点，不得全部集中在IT之家
21. **交叉印证必执行**：每个事件至少从2个不同渠道搜索确认，综合多渠道信息写入摘要
22. **链接权威性优先**：主链接选最权威来源（官方>通讯社>深度媒体>综合媒体>科技媒体），IT之家等科技媒体链接不应超过50%
23. **印证来源独立域名**：印证来源必须与主链接不同域名，同域名不算交叉印证
