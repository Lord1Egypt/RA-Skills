---
name: "AI News Aggregator"
slug: finance-news-aggregator
version: "5.0.2"
homepage: https://github.com/lanyasheng/ai-news-aggregator
description: "AI/技术新闻聚合引擎。100+ RSS源并发抓取、兴趣评分、跨天去重、统一预取。"
changelog: "v2.2: unified prefetch, interest scoring, cross-day dedup, repo restructure"
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python3"]},"os":["linux","darwin","win32"]}}

capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - code-examples-reference
---

# AI News Aggregator — AI/技术新闻高性能聚合引擎
> **⚠️ SECURITY NOTICE**
> - **Type:** Educational reference / analytical framework ONLY
> - **本技能本身不包含可执行代码**，但描述和引用了本地运行的Python脚本（需用户自行部署）
> - **No persistent storage, background execution, or credential collection**
> - **No credential collection, PII processing, or system access**
> - **All outputs require human review before real-world application**
> - **NOT financial, legal, or insurance advice**
>
> **⚠️ 数据安全警告**
> - 本技能仅输出新闻聚合方法的参考框架，**技能本身不自动执行任何代码**
> - 文中描述的RSS抓取/API调用为**架构说明**，用户如需实际部署，需注意：
>   - 查询关键词、IP地址、时间戳等信息将由用户自行部署的脚本发送至第三方RSS源/API
>   - 请确保遵守目标网站的服务条款和robots.txt规则
> - 本技能**不主动联网**，不会自动访问外部资源或收集用户数据
> - 引用新闻时请务必核实原始来源，本技能不保证新闻的实时性和准确性

并发抓取 100+ RSS 源，12秒完成，支持 ETag/Last-Modified 缓存、日期过滤。

## Setup

确保 Python 3.8+ 可用，无需额外依赖（纯标准库）。

## When to Use

用户需要查看 AI/技术新闻、技术趋势、最新论文、GitHub 热门项目、AI 公司动态时使用。

**⚠️ 精确触发规则**（仅当用户明确表达以下意图时才激活，避免日常对话误触发）：
- 触发词必须与**新闻聚合/技术资讯/论文搜索**直接相关
- **不会**因用户提及"新闻"或"论文"等通用词汇而自动激活
- **不会**在用户讨论日常话题时误触发

触发关键词（精确匹配，需用户明确表达需求）：
- "AI 新闻" / "技术新闻" / "科技新闻"
- "今天有什么AI新闻" / "最近技术动态"
- "最新论文" / "arXiv 论文" / "AI 研究论文"
- "GitHub 热门项目" / "GitHub trending"
- "OpenAI 动态" / "Anthropic 更新"
- "新闻聚合" / "RSS 聚合"

## Architecture

```
ai-news-aggregator/
├── scripts/
│   ├── rss_aggregator.py      # 核心 RSS 抓取器
│   ├── rss_sources.json       # 100+ RSS 源配置
│   ├── arxiv_papers.py        # arXiv 论文搜索
│   ├── github_trending.py     # GitHub 热门项目
│   └── summarize_url.py       # 文章摘要
└── SKILL.md                   # 本文件
```

## Data Sources

| 分类 | 源数 | 内容 |
|------|------|------|
| company | 16 | OpenAI, Anthropic, Google, Meta, NVIDIA, Apple, Mistral 等官方博客 |
| papers | 6 | arXiv AI/ML/NLP/CV, HuggingFace Daily Papers, BAIR |
| media | 16 | MIT Tech Review, TechCrunch, Wired, The Verge, VentureBeat 等 |
| newsletter | 15 | Simon Willison, Lilian Weng, Andrew Ng, Karpathy 等专家 |
| community | 12 | HN, GitHub Trending, Product Hunt, V2EX 等 |
| cn_media | 5 | 机器之心, 量子位, 36氪, 少数派, InfoQ |
| ai-agent | 5 | LangChain, LlamaIndex, Mem0, Ollama, vLLM 博客 |
| twitter | 10 | Sam Altman, Karpathy, LeCun, Hassabis 等 AI 领袖 |

## Core Commands

### RSS 聚合
```bash
# 抓取所有源（最近3天新闻）
python3 skills/ai-news-aggregator/scripts/rss_aggregator.py --category all --days 3 --limit 10

# 只看公司博客
python3 skills/ai-news-aggregator/scripts/rss_aggregator.py --category company --days 1 --limit 5

# 只看中文媒体
python3 skills/ai-news-aggregator/scripts/rss_aggregator.py --category cn_media --days 3 --limit 10

# AI Agent 相关
python3 skills/ai-news-aggregator/scripts/rss_aggregator.py --category ai-agent --days 7 --limit 10

# 输出 JSON 格式
python3 skills/ai-news-aggregator/scripts/rss_aggregator.py --category all --days 1 --json
```

### arXiv 论文
```bash
# 最新 AI 论文（按热度排序）
python3 skills/ai-news-aggregator/scripts/arxiv_papers.py --limit 5 --top 10

# 搜索特定主题
python3 skills/ai-news-aggregator/scripts/arxiv_papers.py --query "multi-agent" --top 5
```

### GitHub Trending
```bash
# AI 相关热门项目（今日）
python3 skills/ai-news-aggregator/scripts/github_trending.py --ai-only

# 本周热门
python3 skills/ai-news-aggregator/scripts/github_trending.py --since weekly
```

## Core Rules

### 1. 优先使用 --days 参数
默认抓取最近 N 天的新闻，避免获取过期内容：
- 日报：`--days 1`
- 周报：`--days 7`
- 月报：`--days 30`

### 2. 分类选择策略
| 用户需求 | 推荐分类 |
|----------|----------|
| 公司动态 | `--category company` |
| 技术论文 | `--category papers` |
| 中文资讯 | `--category cn_media` |
| 社区趋势 | `--category community` |
| AI Agent | `--category ai-agent` |

### 3. 缓存机制
- 首次抓取后自动缓存（ETag/Last-Modified）
- 缓存有效期 1 小时
- 重复抓取秒级完成

## Configuration

编辑 `scripts/rss_sources.json` 添加/删除 RSS 源：
```json
{
  "name": "OpenAI Blog",
  "url": "https://openai.com/blog/rss.xml",
  "category": "company"
}
```## Appendix G. Alibaba Dianjin Fusion — finance-news-aggregator v5.0.0

> **Source**: Alibaba Dianjin Digital Employee — `researcher` (AI研究员)  
> **Essence**: 全球财经资讯聚合、多语言新闻翻译、热点事件追踪、舆情风险评估  
> **Integrated**: 2026-05-31

---

### G.1 Core Workflow (Dianjin essence)

```
Input: 用户请求（"今日财经要闻" / "XX事件最新进展"）
  ↓
Data Collection:
  - 国内源：新华社、人民日报、央视财经、第一财经
  - 国际源：Reuters, Bloomberg, Financial Times, CNBC
  - 社交源：Twitter(X), Weibo, 雪球, 东方财富论坛
  ↓
Processing:
  1. 去重（相似新闻合并）
  2. 分类（宏观/行业/公司/国际）
  3. 翻译（英文→中文，自动摘要）
  4. 评分（重要性 1-5星）
  ↓
Output:
  - 财经早报（TOP 10要闻）
  - 专题追踪（XX事件时间线）
  - 舆情预警（负面新闻预警）
```

---

### G.2 News Classification & Scoring (Dianjin method)

**新闻分类体系**：

| 类别 | 关键词 | 重要性阈值 |
|------|--------|------------|
| 🔴 宏观政策 | 央行、降准、降息、GDP | 5星（必读） |
| 🟠 行业动态 | 新能源、AI、芯片、医药 | 4星（重要） |
| 🟡 公司新闻 | 财报、并购、减持、ST | 3星（关注） |
| 🟢 国际市场 | 美联储、美元、原油、黄金 | 4星（重要） |
| 🔵 社交媒体 | 雪球热帖、微博热议 | 2星（参考） |

**评分模型（Dianjin风格）**：

```
重要性评分 = 基础分 + 热度分 + 影响分

基础分（0-3）：
  - 官方媒体（新华社/人民日报）：+3
  - 权威财经（第一财经/财新）：+2
  - 社交媒体（雪球/微博）：+1

热度分（0-2）：
  - 阅读量 > 10万：+2
  - 阅读量 1-10万：+1
  - 阅读量 < 1万：+0

影响分（0-2）：
  - 涉及大盘/板块：+2
  - 涉及个股：+1
  - 无关市场：+0

总分 → 星标：
  - 5-7分：⭐⭐⭐⭐⭐（必读）
  - 3-4分：⭐⭐⭐⭐（重要）
  - 1-2分：⭐⭐⭐（关注）
  - 0分：⭐⭐（参考）
```

---

### G.3 Multi-language News Translation (Dianjin essence)

**英文新闻自动翻译+摘要模板**：

```
【英文原文】
"The Federal Reserve raised interest rates by 25 basis points on Wednesday, 
bringing the benchmark rate to 5.25%-5.5%, the highest level in 16 years. 
Fed Chair Jerome Powell said the central bank remains committed to bringing 
inflation down to its 2% target."

【自动翻译+摘要】
📰 **美联储加息25基点，基准利率达16年新高**

**核心内容**：
- 美联储周三加息25基点，基准利率升至5.25%-5.5%
- 为16年来最高水平
- 鲍威尔表示致力于将通胀降至2%目标

**市场影响**：
- 美股：短期承压（加息利空）
- 美债：收益率上升（债券价格下跌）
- 美元：走强（利差扩大）
- A股：北向资金可能流出（美元资产吸引力上升）

**后续关注**：
- 6月议息会议（是否暂停加息）
- 通胀数据（CPI/PCE）
- 就业数据（非农/失业率）
```

---

### G.4 Sentiment Analysis & Risk Warning (Dianjin method)

> **⚠️ 教育声明**：以下风险分类框架为**纯教育培训参考**，展示新闻舆情分析的方法论。所有涉及风险等级的示例均为假设性教学展示，**不构成任何投资建议或操作指导**。

**舆情风险评估框架**：

```
舆情风险等级（客观分析方法参考）：

🔴 高风险信号（需核实的客观事实）：
  - 公司高管被查/逮捕
  - 财务造假曝光
  - 产品重大安全事故
  - 监管处罚

🟠 中风险信号（需持续关注）：
  - 大股东大额减持
  - 业绩大幅下滑
  - 诉讼/仲裁
  - 行业政策利空

🟡 低风险信号（正常跟踪）：
  - 高管变动（非核心岗位）
  - 小额诉讼
  - 行业竞争加剧
  - 产品投诉增多
```

---

### G.5 Compliance & Risk Constraints (Dianjin standards)

**合规要求（研究员精髓）**：

1. **新闻真实性验证**：
   - 必须标注新闻来源（新华社/Reuters/ Bloomberg）
   - 未经证实的传闻必须标注"未经证实"
   - 社交媒体消息必须标注"来源：Twitter/雪球"

2. **翻译准确性**：
   - 专业术语必须准确（Fed=美联储，rate=利率，not"价格"）
   - 数字必须核对（25 basis points = 25基点，not"25%"）
   - 人名/机构名保留英文原文（Jerome Powell，not"杰罗姆·鲍威尔"）

3. **风险提示**：
   - 舆情预警必须客观（不夸大/不缩小）
   - 负面新闻必须标注"仅供参考，请核实官方公告"
   - 禁止传播谣言（未经证实的消息）

---

### G.6 Test Case (Dianjin quality)

**Test Case 1: 财经早报生成**

```
Input: "生成今日财经早报"

Expected Output:
1. TOP 10要闻（⭐⭐⭐⭐⭐优先）
2. 每条新闻：标题 + 核心内容（50字）+ 市场影响
3. 分类：宏观/行业/公司/国际
4. 风险提示（如有负面新闻）

Quality Check:
- ✅ 新闻时效性（今日/昨日）
- ✅ 分类准确性
- ✅ 影响分析合理性
- ✅ 来源标注完整
```

**Test Case 2: 英文新闻翻译**

```
Input: "翻译这条新闻：Fed raises rates by 25bps, signals pause"

Expected Output:
1. 中文标题
2. 核心内容摘要（100字）
3. 市场影响分析
4. 后续关注点

Quality Check:
- ✅ 翻译准确性（25bps=25基点）
- ✅ 内容完整性（不遗漏关键信息）
- ✅ 影响分析专业（A股/美股/美债/美元）
```

---

**End of Dianjin Fusion Content — finance-news-aggregator v5.0.0**## Appendix G. Alibaba Dianjin Fusion — finance-news-aggregator v5.0.0

> **Source**: Alibaba Dianjin Digital Employee — `researcher` (AI研究员)  
> **Essence**: 全球财经资讯聚合、多语言新闻翻译、热点事件追踪、舆情风险评估  
> **Integrated**: 2026-05-31

---

### G.1 Core Workflow (Dianjin essence)

```
Input: 用户请求（"今日财经要闻" / "XX事件最新进展"）
  ↓
Data Collection:
  - 国内源：新华社、人民日报、央视财经、第一财经
  - 国际源：Reuters, Bloomberg, Financial Times, CNBC
  - 社交源：Twitter(X), Weibo, 雪球, 东方财富论坛
  ↓
Processing:
  1. 去重（相似新闻合并）
  2. 分类（宏观/行业/公司/国际）
  3. 翻译（英文→中文，自动摘要）
  4. 评分（重要性 1-5星）
  ↓
Output:
  - 财经早报（TOP 10要闻）
  - 专题追踪（XX事件时间线）
  - 舆情预警（负面新闻预警）
```

---

### G.2 News Classification & Scoring (Dianjin method)

**新闻分类体系**：

| 类别 | 关键词 | 重要性阈值 |
|------|--------|------------|
| 🔴 宏观政策 | 央行、降准、降息、GDP | 5星（必读） |
| 🟠 行业动态 | 新能源、AI、芯片、医药 | 4星（重要） |
| 🟡 公司新闻 | 财报、并购、减持、ST | 3星（关注） |
| 🟢 国际市场 | 美联储、美元、原油、黄金 | 4星（重要） |
| 🔵 社交媒体 | 雪球热帖、微博热议 | 2星（参考） |

**评分模型（Dianjin风格）**：

```
重要性评分 = 基础分 + 热度分 + 影响分

基础分（0-3）：
  - 官方媒体（新华社/人民日报）：+3
  - 权威财经（第一财经/财新）：+2
  - 社交媒体（雪球/微博）：+1

热度分（0-2）：
  - 阅读量 > 10万：+2
  - 阅读量 1-10万：+1
  - 阅读量 < 1万：+0

影响分（0-2）：
  - 涉及大盘/板块：+2
  - 涉及个股：+1
  - 无关市场：+0

总分 → 星标：
  - 5-7分：⭐⭐⭐⭐⭐（必读）
  - 3-4分：⭐⭐⭐⭐（重要）
  - 1-2分：⭐⭐⭐（关注）
  - 0分：⭐⭐（参考）
```

---

### G.3 Multi-language News Translation (Dianjin essence)

**英文新闻自动翻译+摘要模板**：

```
【英文原文】
"The Federal Reserve raised interest rates by 25 basis points on Wednesday, 
bringing the benchmark rate to 5.25%-5.5%, the highest level in 16 years. 
Fed Chair Jerome Powell said the central bank remains committed to bringing 
inflation down to its 2% target."

【自动翻译+摘要】
📰 **美联储加息25基点，基准利率达16年新高**

**核心内容**：
- 美联储周三加息25基点，基准利率升至5.25%-5.5%
- 为16年来最高水平
- 鲍威尔表示致力于将通胀降至2%目标

**市场影响**：
- 美股：短期承压（加息利空）
- 美债：收益率上升（债券价格下跌）
- 美元：走强（利差扩大）
- A股：北向资金可能流出（美元资产吸引力上升）

**后续关注**：
- 6月议息会议（是否暂停加息）
- 通胀数据（CPI/PCE）
- 就业数据（非农/失业率）
```

---

### G.4 Sentiment Analysis & Risk Warning (Dianjin method)

> **⚠️ 教育声明**：以下风险分类框架为**纯教育培训参考**，展示新闻舆情分析的方法论。所有涉及风险等级的示例均为假设性教学展示，**不构成任何投资建议或操作指导**。

**舆情风险评估框架**：

```
舆情风险等级（客观分析方法参考）：

🔴 高风险信号（需核实的客观事实）：
  - 公司高管被查/逮捕
  - 财务造假曝光
  - 产品重大安全事故
  - 监管处罚

🟠 中风险信号（需持续关注）：
  - 大股东大额减持
  - 业绩大幅下滑
  - 诉讼/仲裁
  - 行业政策利空

🟡 低风险信号（正常跟踪）：
  - 高管变动（非核心岗位）
  - 小额诉讼
  - 行业竞争加剧
  - 产品投诉增多
```

---

### G.5 Compliance & Risk Constraints (Dianjin standards)

**合规要求（研究员精髓）**：

1. **新闻真实性验证**：
   - 必须标注新闻来源（新华社/Reuters/ Bloomberg）
   - 未经证实的传闻必须标注"未经证实"
   - 社交媒体消息必须标注"来源：Twitter/雪球"

2. **翻译准确性**：
   - 专业术语必须准确（Fed=美联储，rate=利率，not"价格"）
   - 数字必须核对（25 basis points = 25基点，not"25%"）
   - 人名/机构名保留英文原文（Jerome Powell，not"杰罗姆·鲍威尔"）

3. **风险提示**：
   - 舆情预警必须客观（不夸大/不缩小）
   - 负面新闻必须标注"仅供参考，请核实官方公告"
   - 禁止传播谣言（未经证实的消息）

---

### G.6 Test Case (Dianjin quality)

**Test Case 1: 财经早报生成**

```
Input: "生成今日财经早报"

Expected Output:
1. TOP 10要闻（⭐⭐⭐⭐⭐优先）
2. 每条新闻：标题 + 核心内容（50字）+ 市场影响
3. 分类：宏观/行业/公司/国际
4. 风险提示（如有负面新闻）

Quality Check:
- ✅ 新闻时效性（今日/昨日）
- ✅ 分类准确性
- ✅ 影响分析合理性
- ✅ 来源标注完整
```

**Test Case 2: 英文新闻翻译**

```
Input: "翻译这条新闻：Fed raises rates by 25bps, signals pause"

Expected Output:
1. 中文标题
2. 核心内容摘要（100字）
3. 市场影响分析
4. 后续关注点

Quality Check:
- ✅ 翻译准确性（25bps=25基点）
- ✅ 内容完整性（不遗漏关键信息）
- ✅ 影响分析专业（A股/美股/美债/美元）
```

---

**End of Dianjin Fusion Content — finance-news-aggregator v5.0.0**
