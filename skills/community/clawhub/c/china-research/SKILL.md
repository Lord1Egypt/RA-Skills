---
name: china-research
description: 国内社交媒体调研工具。触发条件：(1) 用户想了解某个领域的真实需求 (2) 用户想调研国内市场机会 (3) 用户想做产品需求验证 (4) 用户问"最近国内XX有什么动态" (5) 用户提及"国内调研"、"市场调研"、"用户反馈"
---

# china-research

国内社交媒体调研技能，给定话题后自动搜索国内主流平台的真实用户讨论，生成带引用的调研报告。

## 技术方案

通过 mcporter 调用 glm-web-search 或 tavily-search，使用 site: 指令间接搜索各平台内容，然后用 AI 整合生成报告。

## 执行流程

### 步骤 1: 确认搜索话题

向用户确认要调研的话题，并了解：
- 调研目的（产品验证/市场分析/竞品研究）
- 关注的侧重点（用户痛点/市场机会/现有方案）

### 步骤 2: 执行多轮搜索

对每个话题，分多轮搜索不同平台组合：

**第1轮 - 通用搜索：**
```bash
mcporter call glm-search.webSearchPrime search_query="<话题> site:xiaohongshu.com OR site:zhihu.com OR site:weibo.com"
```

**第2轮 - 痛点搜索：**
```bash
mcporter call glm-search.webSearchPrime search_query="<话题> 痛点 site:v2ex.com OR site:jike.city OR site:sspai.com"
```

**第3轮 - 商业搜索：**
```bash
mcporter call glm-search.webSearchPrime search_query="<话题> site:36kr.com OR site:huxiu.com"
```

**第4轮 - 技术搜索（如适用）：**
```bash
mcporter call glm-search.webSearchPrime search_query="<话题> 推荐 site:zhihu.com OR site:v2ex.com"
```

每次搜索取 top 5 结果，总共最多 20 条来源。

### 步骤 3: 整合分析

根据搜索结果，按以下结构整理：
1. 提取核心发现（3-5个要点）
2. 归纳用户真实痛点
3. 总结现有解决方案
4. 分析市场空白与机会

### 步骤 4: 生成报告

按标准格式输出调研报告。

## 搜索策略模板

### 平台组合搜索

| 搜索目的 | 平台组合 | 搜索模板 |
|---------|---------|---------|
| 大众反馈 | 小红书+知乎+微博 | `<话题> site:xiaohongshu.com OR site:zhihu.com OR site:weibo.com` |
| 深度痛点 | V2EX+即刻+少数派 | `<话题> 痛点/抱怨/问题 site:v2ex.com OR site:jike.city OR site:sspai.com` |
| 商业分析 | 36氪+虎嗅 | `<话题> site:36kr.com OR site:huxiu.com` |
| 技术讨论 | 知乎+V2EX | `<话题> site:zhihu.com OR site:v2ex.com` |

### 关键词变体

对同一话题，尝试不同关键词：
- `<话题> 痛点`
- `<话题> 体验`
- `<话题> 推荐`
- `<话题> 吐槽`
- `<话题> 评测`

## 输出格式

```markdown
## 📋 [话题] 调研报告

**时间：YYYY-MM-DD | 数据来源：N条**

### 一、核心发现（3-5个要点）
- 发现1
- 发现2
- 发现3

### 二、用户真实痛点
（从知乎/V2EX/即刻提取的抱怨和需求）
- 痛点1：描述 + 来源
- 痛点2：描述 + 来源

### 三、现有解决方案
（市场上已有的产品/方案）
- 方案1：描述 + 来源
- 方案2：描述 + 来源

### 四、市场空白与机会
（有需求但解决方案不完善的领域）
- 机会1
- 机会2

### 五、参考来源
1. [标题](url) - 来源平台 - 摘要
2. [标题](url) - 来源平台 - 摘要
...
```

## 注意事项

1. **来源必须可追溯**：每个观点都要有来源链接
2. **区分事实与观点**：用户评论是主观观点，媒体报道是客观信息
3. **时效性**：优先引用近期内容（1年内）
4. **平台特性**：不同平台用户画像不同，结论要注明来源平台

## 参考文件

- [平台列表和搜索策略](references/platforms.md)
