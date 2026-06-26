# 搜索策略

## 内容提取方式

### 主方案：web_fetch
使用 OpenClaw 原生 `web_fetch` 工具获取页面内容，参数：
- `extractMode`: markdown（默认，自动过滤广告和无用内容）
- `maxChars`: 10000（单次获取上限）

### 备选方案：markdown.new
web_fetch 失败时使用 markdown.new 服务：
- URL 格式：`https://markdown.new/{原始URL}`
- 适用场景：境外网站、web_fetch 超时或返回空内容
- 示例：`web_fetch(url: "https://markdown.new/https://openai.com/blog")`

通常 web_fetch 可满足需求，境外网站无法访问时启用备选。

### 直接抓取源（不经搜索引擎）

以下来源直接用 web_fetch 抓取，不经过 SearXNG 搜索引擎。这些来源信息密度高、更新稳定，是搜索的重要补充。

| 来源 | URL | 用途 | 语言 |
|------|-----|------|------|
| GitHub Trending | `https://github.com/trending` | 新兴开源项目、热门仓库 | 英文 |
| Hacker News | `https://news.ycombinator.com/` | 技术社区热门讨论 | 英文 |
| Reddit r/LocalLLaMA | `https://www.reddit.com/r/LocalLLaMA/hot/.json` | 开源模型讨论 | 英文 |
| Reddit r/MachineLearning | `https://www.reddit.com/r/MachineLearning/hot/.json` | ML 研究动态 | 英文 |
| X/Twitter AI 讨论 | `https://nitter.net/search?f=tweets&q=AI+agent` | 实时 AI 讨论（nitter 镜像） | 英文 |
| 36kr AI | `https://www.36kr.com/information/AI/` | 中文 AI 新闻 | 中文 |
| 机器之心 | `https://www.jiqizhixin.com/` | 中文 AI 深度报道 | 中文 |
| 量子位 | `https://www.qbitai.com/` | 中文 AI 快讯 | 中文 |
| InfoQ AI | `https://www.infoq.cn/topic/AI` | 中文技术深度文章 | 中文 |
| 知乎 AI 热榜 | `https://www.zhihu.com/hot` | 中文社区讨论热点 | 中文 |
| 掘金 AI | `https://juejin.cn/tag/AI` | 中文开发者社区 | 中文 |
| Product Hunt | `https://www.producthunt.com/` | 新产品发布 | 英文 |
| ArXiv AI | `https://arxiv.org/list/cs.AI/recent` | 最新 AI 论文 | 英文 |
| 自游人 | `https://www.17you.com/` | AI 变现/副业/赚钱思路 | 中文 |

**使用规则**：
- 每次执行至少抓取 2-3 个直接抓取源
- 英文源和中文源各至少 1 个
- Reddit 使用 `.json` 后缀获取结构化数据
- X/Twitter 通过 nitter 镜像站访问（无需登录）
- web_fetch 失败时跳过该源，不阻塞流程

---

## 语言策略

- **英文搜索**：模型发布、开源项目、国际行业动态、GitHub
- **中文搜索**：中国AI平台、国内政策、中文社区讨论
- **同一话题中英文各搜一次**：避免单一语言的信息茧房

---

## 信息源分级

### Tier 1（一手，可单独作为来源）

- 官方博客和公告
- GitHub release 页面、GitHub trending
- 论文页面（arXiv 等）
- 官方文档和 changelog

### Tier 2（聚合，需交叉验证）

- Hacker News 热帖
- Reddit（r/LocalLLaMA, r/MachineLearning, r/artificial 等）
- 技术社区首发文章（机器之心、量子位、InfoQ、36氪AI等）
- 中文社区：知乎AI话题热榜、掘金AI板块、少数派AI专栏
- 独立内容源：AI领域深度博主
- 国内大模型官方公告
- API status 页面
- 产品更新日志
- CSDN、博客园等技术博客中的工具推荐

### Tier 2+（垂直专业源，单源可进入"值得留意"区）

- AI 变现/副业垂直源（如自游人等专注于 AI 商业化的平台）
- 垂直领域专业媒体（单一领域信息密度高于通用媒体）

### Tier 3（分析，只能作为线索）

- 科技媒体深度文章（36kr 等）
- 行业分析师长文
- 播客摘要和访谈记录
- Newsletter（Ben's Bites, a16z AI 等）

---

## 搜索维度

每次执行从以下 12 个维度中选择至少 4 个轮换覆盖，避免与 history.md 最近 7 天重复。

1. **模型能力变化**：新发布、重大更新、能力变化、定价变化
   - 关键词：`AI model release update`, `AI模型发布更新`, `LLM benchmark update`, `大模型价格调整`

2. **工具生态变化**：新产品、重要更新、开源项目里程碑
   - 关键词：`AI tool launch`, `AI工具新品`, `AI open source release`, `开源AI项目更新`

3. **行业结构变化**：融资（战略级）、政策法规、大厂战略调整
   - 关键词：`AI funding`, `AI融资`, `AI policy regulation`, `AI政策法规`, `tech company AI strategy`

4. **办公生态**：新功能、集成变化、合作伙伴动态
   - 关键词：`productivity AI feature update`, `办公AI功能更新`, `workspace AI integration`

5. **开源社区动态**：重大 release、新框架、性能突破
   - 关键词：`open source AI release`, `开源AI框架`, `AI performance breakthrough`, `AI推理优化`

6. **AI 应用层**：新应用模式、用户行为变化、商业模式创新
   - 关键词：`AI application trend`, `AI应用趋势`, `AI business model`, `AI商业化`

7. **AI安全与对齐**：越狱方法、数据泄露、对齐突破、安全漏洞
   - 关键词：`AI security alignment`, `AI安全漏洞`, `大模型越狱`, `AI对齐突破`

8. **监管与合规**：国内生成式AI备案、欧盟AI法案落地、数据合规要求
   - 关键词：`AI regulation compliance`, `生成式AI备案`, `AI监管政策`, `数据合规要求`

9. **AI 赚钱**：变现方法、商业化路径、收入模式
   - 关键词：`AI make money`, `AI变现`, `AI赚钱方法`, `AI商业模式`, `AI revenue`, `AI副业`

10. **GitHub/开源工具**：新兴开源项目、GitHub trending、免费工具
    - 关键词：`GitHub trending AI`, `open source AI assistant free`, `awesome AI agents`
    - 搜索方法：除 web_search 外，可直接 web_fetch GitHub trending 页面

11. **中国AI生态**：运营商AI平台、央企AI战略、国产AI基础设施
    - 关键词：从用户画像关注清单动态生成（如用户关注的公司+`AI`）
    - 注意：用中文搜索为主

12. **AI编程工具/Agent工具**：编程助手、Agent框架、开发工具
    - 关键词：`AI coding assistant free`, `open source AI agent tool`, `AI编程工具`, `AI agent framework`
    - 补充：从用户画像自定义关键词中提取相关工具搜索词

---

## 关注清单驱动搜索

维度 11 和 12 的搜索词**不硬编码**，完全由用户画像的"关注清单"和"自定义关键词"驱动：

1. 读取 `memory/signal/profile.md` 中的"关注清单"和"自定义关键词"
2. 将关注清单中的公司/工具与维度主题组合生成搜索词
3. 将自定义关键词直接作为搜索词补充

---

## 搜索轮次规划

| 轮次 | 方式 | 目的 | 维度/来源 |
|------|------|------|----------|
| 第1轮 | web_search | 宏观动态 | 从 1/3/7/8 中选（英文） |
| 第2轮 | web_search | 工具生态 | 从 2/5/10/12 中选（英文） |
| 第3轮 | web_search | 应用变现 | 从 4/6/9 中选（中文） |
| 第4轮 | web_search | 关注清单 | 11 + 关注清单 + 自定义关键词 |
| 第5轮 | web_fetch | 直接抓取 | GitHub Trending + Hacker News + 1个中文源 |

- web_search 轮次：每轮 1-2 个查询，总计 4-8 个查询
- web_fetch 轮次：直接抓取 2-3 个固定源
- 维度选择避免与最近 7 天历史重复

---

## 降权规则

详见 `quality-gates.md` 第一层门控中的降权规则。搜索阶段仅做初步筛选，正式门控在 Step 5 执行。

---

## 交叉验证规则

- **今日信号区**：至少 2 个独立来源确认
- **值得留意区**：至少 1 个来源 + 1 个佐证
- **单一来源**：标注"待验证"，不能进"今日信号"
- **关注清单匹配项**：单一来源可进入"值得留意"区
- **垂直专业源**（Tier 2+）：单一来源可进入"值得留意"区

---

## 动态信息源

读取 `memory/signal/profile.md` 中的信息源评分部分获取动态评分。优先搜索高评分信息源，降低低评分源搜索频率。

搜索完成后，根据本次搜索结果更新 `memory/signal/profile.md` 的信息源评分：
- 某信息源产出的信号通过了质量门控 → 产出次数 +1，通过次数 +1
- 某信息源产出的信号被门控删除 → 产出次数 +1
