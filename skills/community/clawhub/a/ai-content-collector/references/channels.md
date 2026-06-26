# AI 资料收集渠道参考

本文件是搜索关键词和来源的参考，**不是用来逐个抓取的URL列表**。

> ⚠️ **重要提醒**：
> - 搜索阶段：使用 **web_search + site:** 限定权威来源
> - 抓取阶段：使用 **web_fetch** 抓取原文详情
> - **禁止使用知乎/微博/论坛来源**

---

# 一、搜索工具选择

## 1.1 搜索引擎

| 工具 | 调用方式 | 优势 | 适用场景 |
|------|----------|------|----------|
| **web_search + site:** | `web_search({query: "site:ithome.com AI 发布", ...})` | 限定权威来源，排除不可靠来源 | 主力搜索 |
| **web_search + 排除** | `web_search({query: "AI 最新 -site:zhihu.com -site:weibo.com", ...})` | 排除论坛和社交媒体 | 补充搜索 |

## 1.2 内容抓取

| 工具 | 调用方式 | 优势 | 适用场景 |
|------|----------|------|----------|
| **web_fetch** | `web_fetch({url, ...})` | 内置工具，获取原文 | IT之家/36kr/澎湃/新浪等权威媒体 |

---

# 二、权威搜索来源（必须使用）

## 2.1 中文科技媒体（搜索优先引用）

| 来源 | 搜索关键词示例 | 内容特点 | web_fetch可用性 |
|------|----------------|----------|----------------|
| IT之家 | `site:ithome.com AI 大模型 发布` | 时效性高，覆盖全面 | ✅ 可用 |
| 腾讯新闻 | `site:new.qq.com AI 芯片 动态` | 深度报道多 | ✅ 可用 |
| 新华网 | `site:xinhuanet.com 人工智能 政策` | 官方政策权威 | ✅ 可用 |
| 澎湃新闻 | `site:thepaper.cn AI 机器人` | 深度调查 | ✅ 可用 |
| 36氪 | `site:36kr.com AI 创业 融资` | 行业融资信息 | ✅ 可用 |
| 新浪财经 | `site:finance.sina.com.cn 汽车 产销` | 财经数据 | ✅ 可用 |
| 每日经济新闻 | `site:nbd.com.cn AI 大模型` | 财经+科技 | ✅ 可用 |
| 机器之心 | `site:jiqizhixin.com 大模型` | AI专业媒体 | ⚠️ 部分可能403 |
| 第一财经 | `site:yicai.com AI 产业` | 财经+产业 | ✅ 可用 |
| 财新网 | `site:caixin.com AI 政策` | 财经权威 | ✅ 可用 |
| 中国新闻网 | `site:chinanews.com AI` | 官方新闻 | ✅ 可用 |

## 2.2 禁止使用的来源（不可靠，不可交叉印证）

| 来源 | 原因 | 处理方式 |
|------|------|----------|
| 知乎 zhihu.com | 用户生成内容，观点非事实 | 搜索时 `-site:zhihu.com`，结果中直接跳过 |
| 微博 weibo.com | 社交媒体，信息未经核实 | 搜索时 `-site:weibo.com`，结果中直接跳过 |
| 各类论坛/BBS | 用户讨论，非权威报道 | 搜索时排除，结果中直接跳过 |
| 贴吧、Reddit | UGC内容 | 同上 |

## 2.3 英文科技媒体

| 来源 | 搜索关键词示例 | 内容特点 |
|------|----------------|----------|
| TechCrunch | `site:techcrunch.com AI model launch` | 硅谷动态 |
| VentureBeat | `site:venturebeat.com AI` | 行业新闻 |
| The Verge | `site:theverge.com OpenAI Anthropic` | 科技报道 |
| Ars Technica | `site:arstechnica.com AI` | 技术深度 |

## 2.4 官方来源（搜索时引用，不直接抓取）

| 来源 | 搜索关键词示例 | 说明 |
|------|----------------|------|
| Google AI Blog | `site:blog.google AI Gemini` | Google官方 |
| OpenAI Blog | `site:openai.com blog` | OpenAI官方 |
| 阿里千问博客 | `site:qwenlm.github.io` | Qwen官方 |
| 工信部 | `site:miit.gov.cn 人工智能` | 政策文件 |
| 国务院 | `site:gov.cn 人工智能 政策` | 顶层政策 |

---

# 三、扫描对象

## 3.1 国家机构

国务院、工信部、信通院、发改委、中国汽车工业协会、自动化所、国家网信办

## 3.2 咨询公司

| 公司 | 中文站 |
|------|--------|
| 麦肯锡 | mckinsey.com.cn |
| 波士顿 | bcg.com |
| 德勤 | deloitte.com/cn |
| 普华永道 | pwccn.com |
| 毕马威 | kpmg/cn |
| 安永 | ey.com/en_cn |
| IBM | ibm.com |
| Gartner | gartner.com/cn |
| IDC | idc.com/cn |

**报告聚合捷径**：GitHub [reportcamp](https://github.com/reportcamp/reportcamp.github.io) — 8100+篇行业报告

## 3.3 模型厂商

| 厂商 | 产品 |
|------|------|
| Google | Gemini |
| OpenAI | GPT |
| Meta | Llama |
| 阿里巴巴 | 千问(Qwen) |
| 字节跳动 | 豆包(Doubao) |
| 百度 | 文心(ERNIE) |
| 腾讯 | 混元(Hunyuan) |
| 月之暗面 | Kimi |
| 智谱 | GLM |
| DeepSeek | DeepSeek |

## 3.4 机器人厂商

特斯拉(Optimus)、波士顿动力(Atlas/Spot)、优必选、银河通用、宇树科技、松延动力

## 3.5 头部企业

美的、比亚迪、上汽、三一、吉利

## 3.6 上市公司信息

| 渠道 | 说明 |
|------|------|
| 巨潮资讯网 http://www.cninfo.com.cn | A股公告 |
| 港交所披露易 https://www.hkexnews.hk | H股公告 |

---

# 四、模型能力评估渠道

| 评估渠道 | 网址 | 说明 |
|----------|------|------|
| LMArena | https://lmarena.ai | 全球权威盲测排行榜 |
| DataLeader | https://www.datalearner.com/leaderboards | 实时评测排名 |
| Open LLM Leaderboard | https://huggingface.co/spaces/open-llm-leaderboard | 开源模型排行 |
| SuperCLUE | https://www.superclueai.com | 中文大模型评测基准 |
| 猫目AI评测 | https://maomu.com/rank/chatbot-arena | 国内外模型评测排名聚合 |
| Artificial Analysis | https://artificialanalysis.ai | API价格/速度/质量对比 |

---

# 五、材料分类

| 大类 | 子类 | 搜索关键词方向 |
|------|------|----------------|
| 客车/汽车行业 | 研发 | 技术、创新、专利、智驾 |
| 客车/汽车行业 | 营销 | 市场、品牌、合作、销量 |
| 客车/汽车行业 | 制造运营 | 制造、量产、产线、工厂 |
| 客车/汽车行业 | 财经人力 | 融资、营收、投资、人事 |
| AI领域 | AI基础设施 | 算力、芯片、数据中心、GPU/TPU |
| AI领域 | 模型能力 | 大模型、发布、开源、评测 |
| AI领域 | 智能体开发平台 | Agent、智能体、框架、MCP |
| AI领域 | AI安全 | 安全、合规、治理、伦理、监管 |

---

# 六、注意事项

1. **site: 限定权威来源**：搜索时用 `site:ithome.com` 等限定权威媒体
2. **排除不可靠来源**：搜索时加 `-site:zhihu.com -site:weibo.com`
3. **必须抓取原文**：web_fetch 获取原文，搜索snippet不能替代摘要
4. **来源可信度**：官方来源 > 权威媒体 > 行业媒体 > 禁止使用论坛/社交媒体
5. **交叉验证**：重大事件需从2个不同权威来源确认
6. **日期核实**：搜索结果中的日期必须与原文一致
7. **禁止复用历史数据**：每次执行必须重新搜索
