# AI 周报数据源参考

## 英文信息源

### 综合新闻与行业动态
| 来源 | URL | 特点 |
|------|-----|------|
| AI Critique | aicritique.org | 每周AI新闻汇总，按类别整理 |
| StartupHub AI | startuphub.ai | AI创业公司动态、融资信息 |
| AI Funding | aifunding.me | AI融资数据库，按周更新 |
| The AI Track | theaitrack.com | AI模型发布、基准测试更新 |
| TechCrunch AI | techcrunch.com/category/artificial-intelligence | 实时AI新闻 |

### 市场数据与统计
| 来源 | URL | 特点 |
|------|-----|------|
| Resourcera AI Stats | resourcera.com/data/artificial-intelligence/ai-statistics | 综合AI市场统计数据 |
| Companies History | companieshistory.com/artificial-intelligence-market | AI市场规模历史与预测 |
| MarketsandMarkets | marketsandmarkets.com | AI市场预测报告 |
| Gartner | gartner.com | 企业AI采用研究 |
| Stanford AI Index | aiindex.stanford.edu | 年度AI指数报告 |

### 政策与监管
| 来源 | URL | 特点 |
|------|-----|------|
| AI Policy | aipolicy.com | AI政策追踪 |
| White House | whitehouse.gov | 美国AI行政令 |
| EU AI Act Tracker | claudd.ai/eu-ai-act-tracker | 欧盟AI法案进展 |

## 中文信息源

### 综合新闻
| 来源 | URL | 特点 |
|------|-----|------|
| 投资界AI栏目 | pe.pedaily.cn/ai | 中文AI投融资新闻 |
| 36氪人工智能 | 36kr.com/tag/人工智能 | 中国AI行业动态 |
| 机器之心 | jiqizhixin.com | AI技术新闻与论文 |
| 量子位 | qbitai.com | AI行业新闻与访谈 |
| 新智元 | ai.jiqizhixin.com | AI产业动态 |

### 融资与并购（中文）
搜索关键词组合：
- `AI融资 本周` + `site:36kr.com OR site:pedaily.cn`
- `大模型融资 2026`
- `AI并购` + 当前月份年份

### 政策与监管（中文）
搜索关键词组合：
- `AI监管 2026` + `site:gov.cn`
- `人工智能法规` + 当前月份
- `AI拟人化交互服务管理办法`（中国专项）

## 搜索策略

### 第一轮：广域搜索
```
英文：AI news week of [当前日期] 2026
中文：AI行业新闻 [当前月份] 2026
```

### 第二轮：定向搜索（补充第一轮遗漏）
```
英文：
- AI model release benchmark [当前月份] 2026
- AI funding round [当前月份] 2026
- AI regulation policy update 2026

中文：
- 大模型发布 [当前月份] 2026
- AI融资 [当前月份] 2026
- 人工智能政策 [当前月份] 2026
```

### 第三轮：数据验证
对报告中使用的所有量化数据（市场规模、融资额、市场份额等），至少找到2个独立来源交叉验证。

## RSS Feed 源（优先使用）

RSS 抓取比 HTML 解析更稳定，推荐优先使用。`scripts/fetch_ai_news.py` 内置以下已验证可用的源：

> 2026-09-10 实测：**14/14 全部可用（国内 7/7 · 国外 7/7）**。下表 `region` 用于分区健康统计。

| 来源 | Feed URL | 语言 | region | 分类倾向 |
|------|----------|------|--------|---------|
| 量子位 | https://www.qbitai.com/rss | 中文 | cn | industry |
| 36氪 | https://www.36kr.com/feed | 中文 | cn | industry |
| 雷峰网 AI 科技评论 | https://www.leiphone.com/feed | 中文 | cn | ai-models |
| 智东西 | https://www.zhidx.com/rss | 中文 | cn | industry |
| 极客公园 | https://www.geekpark.net/rss | 中文 | cn | industry |
| InfoQ 中国 | https://www.infoq.cn/feed | 中文 | cn | industry |
| 钛媒体 | https://www.tmtpost.com/rss | 中文 | cn | industry |
| TechCrunch AI | https://techcrunch.com/category/artificial-intelligence/feed/ | 英文 | global | industry |
| MIT Tech Review | https://www.technologyreview.com/feed/ | 英文 | global | industry |
| Hugging Face Blog | https://huggingface.co/blog/feed.xml | 英文 | global | ai-models |
| TechMeme | https://www.techmeme.com/feed.xml | 英文 | global | industry |
| MIT News AI | https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml | 英文 | global | paper |
| VentureBeat AI | https://venturebeat.com/category/ai/feed/ | 英文 | global | industry |
| Google AI Blog | https://blog.google/technology/ai/rss/ | 英文 | global | industry |

**抓取要点（都是踩过的坑）**：
- **36氪必须带 `www`**：`36kr.com/feed` 返回反爬 HTML 页（200 但 0 条），`www.36kr.com/feed` 才返回真实 RSS（30 条）。
- **UA 不能用自报爬虫身份**：VentureBeat 对 `compatible; AIWeeklyReport/x.y` 直接返回 **429**，改用常规浏览器 UA 即 200。现统一为常量 `FEED_UA`。
- **镜像回退**：`FEED_MIRRORS` 给 Hugging Face Blog 配了 `hf-mirror.com` 国内镜像，主源失败时自动切换。

> **已失效（已从列表移除）**：The Verge AI（`/rss/index.xml` 返回 404）、机器之心（`jiqizhixin.com/rss` 已变为「数据服务」落地页，2026-09-10 起由雷峰网替代）、arXiv cs.AI（返回 0 条目，不稳定）。
> 如发现某源持续失效，用 `--check-feeds` 发现后从 `RSS_FEEDS` 移除或替换。

---

## 外部 API 配置（可选增强）

如需更高质量的数据，可配置以下 API。`scripts/fetch_ai_news.py` 支持读取这些 API。

### News API（`newsapi.org`）

- **用途**：结构化 AI 新闻搜索
- **免费层**：100 req/天
- **获取 key**：注册 https://newsapi.org/register
- **配置方法**：
  ```
  在 ~/.workbuddy/skills/ai-weekly/.env 中添加：
  NEWSAPI_KEY=your_key_here
  ```
- **调用示例**：
  ```bash
  NEWSAPI_KEY=xxx python scripts/fetch_ai_news.py --news-api --output news.json
  ```

### Hugging Face API（模型排行榜）

- **用途**：获取开源模型最新排行榜
- **免费**：无需 API key
- **端点**：`https://huggingface.co/api/spaces/open-llm-leaderboard/open_llm_leaderboard/api/leaderboard`
- **无需配置**，脚本直接调用

### 融资数据（无 API，人工誊录快照）

- **用途**：全球 / 中国 AI 融资规模图的数据来源
- **当前实现**：**无可配置 API**。融资数字来自 `assets/market_snapshot.json`，
  由人工从公开报道誊录（Crunchbase / CB Insights / 新浪创投Plus / IT桔子 等），
  并在页脚标注为「静态快照引用」。**没有任何代码会去读 `.env` 里的融资类 key**，
  所以配置了也不会生效——这是刻意的：与其做一个假装能连的接口，不如如实说明。
- **更新方式**：改`assets/market_snapshot.json` 的 `series` 与 `chart_sources`，
  并更新 `retrieved_at`（快照超过 90 天会被判过期并在页面显式标注）。
  相关代码见 `scripts/aiweekly/market_snapshot.py`。

### .env 文件模板

在 `~/.workbuddy/skills/ai-weekly/.env` 中配置（该文件不提交到 git）：

```bash
# News API（可选）
NEWSAPI_KEY=

# 出站代理（仅企业内网等需要统一出网代理的场景）
HTTP_PROXY=
HTTPS_PROXY=
```

### 代理配置

`fetch_ai_news.py` 自动从以下位置读取代理（优先级从高到低）：

1. 环境变量 `HTTPS_PROXY` / `HTTP_PROXY`
2. `.env` 文件中的 `HTTP_PROXY` / `HTTPS_PROXY` 行

仅在「企业内网要求经统一代理出网」这类网络架构下才需要填写。公网直连环境留空即可，技能会自行按国内源优先策略工作。

### RSS 健康检查

定期检查 RSS 源可用性，结果保存到 `data/feed_health.json`：

```bash
python scripts/fetch_ai_news.py --check-feeds
```

如发现某个源持续失效（`status: "error"` 或 `status: "empty"`），应从 `RSS_FEEDS` 列表中移除或替换为新 URL。

---

## 搜索工具使用

- **WebSearch**：用于发现信息源（获取URL列表）
- **WebFetch**：用于从已发现的信息源提取具体内容
- **优先顺序**：先 RSS Feed → 再 WebSearch 发现 → 再 WebFetch 提取
- **并发**：同一轮次的多组关键词可并发搜索
