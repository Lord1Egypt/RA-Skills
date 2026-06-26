# 国内社交媒体平台搜索策略

## 平台列表

### 消费生活类

| 平台 | 域名 | 特点 | 适合话题 |
|-----|------|------|---------|
| 小红书 | xiaohongshu.com | 消费决策、生活方式、女性用户为主 | 产品测评、消费需求、女性市场 |
| 微博 | weibo.com | 热点舆情、大众情绪、传播快 | 舆情监控、热点话题、大众反馈 |
| 抖音 | douyin.com | 短视频趋势（搜索效果可能不佳） | 年轻群体、短视频趋势（可选） |
| B站 | bilibili.com | 年轻群体、Z世代、二次元 | 年轻人需求、兴趣社区 |

### 深度讨论类

| 平台 | 域名 | 特点 | 适合话题 |
|-----|------|------|---------|
| 知乎 | zhihu.com | 深度讨论、专业建议、长文 | 专业问题、深度分析、用户痛点 |
| V2EX | v2ex.com | 程序员社区、技术讨论 | 技术需求、工具推荐、极客视角 |
| 即刻 | jike.city | 互联网圈、产品讨论、年轻从业者 | 产品反馈、行业洞察 |
| 少数派 | sspai.com | 效率工具、数字生活、高质量 | 效率工具、数字生活方式 |

### 商业媒体类

| 平台 | 域名 | 特点 | 适合话题 |
|-----|------|------|---------|
| 36氪 | 36kr.com | 创投、融资、创业 | 商业模式、融资信息、创业 |
| 虎嗅 | huxiu.com | 科技商业分析、深度报道 | 行业分析、商业洞察 |

## Site 语法示例

### 单平台搜索

```bash
# 搜索小红书
mcporter call glm-search.webSearchPrime search_query="AI工具 site:xiaohongshu.com"

# 搜索知乎
mcporter call glm-search.webSearchPrime search_query="AI工具 site:zhihu.com"

# 搜索V2EX
mcporter call glm-search.webSearchPrime search_query="AI工具 site:v2ex.com"

# 搜索即刻
mcporter call glm-search.webSearchPrime search_query="AI工具 site:jike.city"

# 搜索36氪
mcporter call glm-search.webSearchPrime search_query="AI创业 site:36kr.com"

# 搜索虎嗅
mcporter call glm-search.webSearchPrime search_query="AI创业 site:huxiu.com"
```

### 多平台组合搜索

```bash
# 消费类话题
mcporter call glm-search.webSearchPrime search_query="<话题> site:xiaohongshu.com OR site:weibo.com"

# 深度讨论
mcporter call glm-search.webSearchPrime search_query="<话题> site:zhihu.com OR site:v2ex.com"

# 商业分析
mcporter call glm-search.webSearchPrime search_query="<话题> site:36kr.com OR site:huxiu.com"

# 产品反馈
mcporter call glm-search.webSearchPrime search_query="<话题> 体验 site:jike.city OR site:sspai.com"
```

## 平台用户画像速查

| 平台 | 主要用户群 | 内容特点 |
|-----|-----------|---------|
| 小红书 | 18-35岁女性为主 | 种草、测评、生活方式分享 |
| 知乎 | 高学历、专业人士 | 长文深度分析、专业讨论 |
| 微博 | 全年龄段 | 热点、娱乐、舆论 |
| V2EX | 程序员、开发者 | 技术讨论、工具推荐 |
| 即刻 | 互联网从业者 | 产品讨论、行业八卦 |
| 少数派 | 数字生活爱好者 | 效率工具、方法分享 |
| 36氪 | 创业者、投资人 | 商业资讯、融资信息 |
| B站 | Z世代、学生 | 兴趣内容、年轻文化 |

## 搜索策略建议

### 按调研目的选择平台

1. **产品需求验证**：小红书 + 知乎 + 即刻
2. **技术产品调研**：V2EX + 知乎 + 少数派
3. **市场机会分析**：36氪 + 虎嗅 + 知乎
4. **用户痛点挖掘**：知乎 + V2EX + 微博
5. **消费趋势分析**：小红书 + 微博 + B站

### 关键词组合策略

| 调研目标 | 关键词后缀 |
|---------|-----------|
| 发现痛点 | `痛点`、`吐槽`、`抱怨`、`问题` |
| 了解需求 | `需求`、`想要`、`期待`、`希望能` |
| 评估方案 | `推荐`、`评测`、`体验`、`对比` |
| 商业分析 | `市场`、`创业`、`融资`、`行业` |

## 注意事项

1. **抖音搜索**：由于平台限制，site:douyin.com 搜索效果可能不佳，建议作为可选
2. **时效性**：可以在搜索词中加入时间限定，如"2024 AI工具"
3. **结果数量**：每个搜索查询建议取 top 5 结果，避免信息过载
4. **交叉验证**：同一观点在多个平台出现更有参考价值
