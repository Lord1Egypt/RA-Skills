# 多平台搜索指南

本指南提供在各平台高效搜索技术内容的技巧和策略。

## 学术资源

### arXiv

**搜索技巧**：
```
基础查询: "Model Context Protocol"
高级查询: "MCP" AND ("protocol" OR "framework") ANDNOT "medical"
分类筛选: cs.AI, cs.SE, cs.CL, cs.LG
时间筛选: last 12 months
```

**URL构建**：
```
https://arxiv.org/search/?query=Model+Context+Protocol
&searchtype=all&abstracts=show&order=-announced_date_first
&size=25
```

**Python获取**：
```python
import arxiv

search = arxiv.Search(
    query="Model Context Protocol",
    max_results=10,
    sort_by=arxiv.SortCriterion.SubmittedDate
)
for result in search.results():
    print(result.title, result.pdf_url)
```

### Google Scholar

**搜索技巧**：
```
精确匹配: "Model Context Protocol"
作者搜索: author:"John Smith"
年份筛选: 2024..2026
引用排序: sort by citations
```

**API使用**：
```python
from scholarly import scholarly

search_query = scholarly.search_pubs('Model Context Protocol')
for i, paper in enumerate(search_query):
    if i >= 10:
        break
    print(paper['bib']['title'])
```

---

## 国内社区

### 知乎

**搜索技巧**：
```
关键词组合:
- "MCP协议" "详解"
- "MCP协议" "实战" "案例"
- "Claude MCP" "开发"

筛选条件:
- 按赞同数排序
- 筛选高质量回答（>100赞）
- 关注话题：AI、大模型、编程
```

**URL构建**：
```
https://www.zhihu.com/search?type=content&q=MCP协议+详解
```

**Python获取**（需登录）：
```python
# 使用Browser Relay或API
# 知乎反爬严格，建议使用官方API或手动获取
```

### CSDN

**搜索技巧**：
```
关键词:
- "MCP协议" + "教程"
- "MCP" + "代码实现"
- "Model Context Protocol" + "入门"

筛选:
- 按热度排序
- 筛选原创文章
- 查看代码量/附件
```

**URL构建**：
```
https://so.csdn.net/so/search?q=MCP协议+教程&t=all
```

### 微信公众号

**搜索方式**：

1. **搜狗微信搜索**（推荐）
```
http://weixin.sogou.com/
查询: MCP协议 site:mp.weixin.qq.com
```

2. **微信内搜索**
```
搜索："MCP协议" + "技术"
筛选：最近半年 + 阅读量>1000
```

3. **推荐公众号**
- 机器之心（AI前沿）
- AI前线（工程实践）
- InfoQ（架构技术）

### B站

**搜索技巧**：
```
关键词:
- "MCP协议讲解"
- "Claude MCP教程"
- "AI Agent Skill"

筛选:
- 时长 > 10分钟
- 播放量 > 1万
- 弹幕数 > 100
- 发布时间：最近1年
```

**URL构建**：
```
https://search.bilibili.com/all?keyword=MCP协议讲解
```

**UP主推荐**：
- 马克的技术工作坊（Agent系列）
- 秋芝2046（AI科普）
- 九天Hector（OpenClaw）

---

## 国际社区

### GitHub

**搜索技巧**：
```
基本搜索: "MCP" "Model Context Protocol"
语言筛选: language:Python language:TypeScript
星级筛选: stars:>100
时间筛选: created:>2024-01-01

高级搜索:
- topic:ai-agent
- topic:mcp
- awesome list: awesome-mcp
```

**API使用**：
```python
from github import Github

g = Github("your_token")
repos = g.search_repositories(
    query="Model Context Protocol language:Python stars:>100",
    sort="stars",
    order="desc"
)
for repo in repos[:10]:
    print(repo.name, repo.stargazers_count)
```

### Hacker News

**搜索方式**：
```
Algolia搜索: https://hn.algolia.com/
查询: "Model Context Protocol"
排序: by popularity
时间: past year
```

**API**：
```python
import requests

url = "https://hn.algolia.com/api/v1/search"
params = {
    "query": "Model Context Protocol",
    "tags": "story",
    "numericFilters": "created_at_i>1609459200"
}
response = requests.get(url, params=params)
```

### Reddit

**搜索技巧**：
```
社区: r/MachineLearning, r/OpenAI, r/ClaudeAI
查询: "MCP" "Model Context Protocol"
排序: Top (past year)
```

**Python获取**：
```python
import praw

reddit = praw.Reddit(
    client_id="your_id",
    client_secret="your_secret",
    user_agent="research_bot"
)

subreddit = reddit.subreddit("MachineLearning")
for submission in subreddit.search("MCP", limit=10):
    print(submission.title, submission.url)
```

### YouTube

**搜索技巧**：
```
查询:
- "Model Context Protocol explained"
- "MCP tutorial 2026"
- "Claude MCP guide"

筛选:
- HD视频
- 时长 > 10分钟
- 上传时间：今年
- 观看次数 > 1000
```

**频道推荐**：
- Fireship（快速技术概览）
- NetworkChuck（AI工具）
- sentdex（Python/AI教程）

---

## 播客

### 小宇宙（中文）

**搜索**：
```
关键词: "AI Agent" "大模型" "Claude"
筛选: 科技/编程标签
```

**推荐节目**：
- 捕蛇者说（Python）
- 乱翻书（科技商业）
- 声东击西（技术人文）

### Podcast（英文）

**推荐节目**：
- Machine Learning Street Talk
- Latent Space
- The TWIML AI Podcast
- Lex Fridman Podcast

**搜索平台**：
- Apple Podcasts
- Spotify
- Google Podcasts
- Overcast

---

## 官方来源

### 官方文档优先级

1. **必读**（★★★★★）
   - 官方文档首页
   - Quick Start / Getting Started
   - Core Concepts

2. **重要**（★★★★☆）
   - API Reference
   - Architecture Overview
   - Best Practices

3. **参考**（★★★☆☆）
   - Release Notes
   - Changelog
   - Migration Guide

### GitHub README 重点

```markdown
必看部分:
- Overview / Introduction
- Installation / Quick Start
- Usage Examples
- Architecture (如果有)

参考部分:
- Contributing Guide
- Roadmap
- FAQ
```

---

## 搜索策略

### 时间范围策略

```
技术概念类: 不限时间（了解演进）
实现教程类: 最近2年（保持时效）
API文档类: 当前版本（确保准确）
前沿研究类: 最近1年（追踪最新）
```

### 质量评估策略

```
高可信度（直接使用）:
- 官方文档
- 顶会论文
- 大厂技术博客
- 知名开源项目

中可信度（参考验证）:
- 技术博客（知名作者）
- 社区高赞回答
- 视频教程（高播放）

低可信度（谨慎参考）:
- 个人博客（无背景）
- 低互动内容
- 过时教程
```

### 交叉验证策略

```
重要结论需要至少2个独立来源验证:
- 官方文档 + 社区实践
- 论文 + 开源实现
- 多个社区一致观点

冲突处理:
- 优先官方说法
- 看发布时间（新>旧）
- 看作者背景
- 看社区反馈
```

---

## 自动化工具

### Python 搜索聚合

```python
import asyncio
from typing import List, Dict

async def search_all_platforms(query: str) -> Dict[str, List[Dict]]:
    """多平台并行搜索"""
    tasks = {
        "github": search_github(query),
        "arxiv": search_arxiv(query),
        "zhihu": search_zhihu(query),
        "youtube": search_youtube(query),
    }
    
    results = await asyncio.gather(*tasks.values())
    return dict(zip(tasks.keys(), results))
```

### 搜索结果去重

```python
from difflib import SequenceMatcher

def is_similar(title1: str, title2: str, threshold: float = 0.8) -> bool:
    """判断两个标题是否相似"""
    return SequenceMatcher(None, title1, title2).ratio() > threshold

def deduplicate_results(results: List[Dict]) -> List[Dict]:
    """去重搜索结果"""
    unique = []
    for result in results:
        if not any(is_similar(result['title'], u['title']) for u in unique):
            unique.append(result)
    return unique
```

---

## 常见问题

### Q: 如何处理平台反爬？

**A:**
- 使用官方API（优先）
- 控制请求频率
- 使用Browser Relay
- 考虑付费API

### Q: 如何判断内容时效性？

**A:**
- 查看发布/更新时间
- 关注版本号变化
- 看评论区时间
- 对比多个来源

### Q: 如何评估作者权威性？

**A:**
- 查看作者背景
- 看历史作品质量
- 看社区认可度
- 看是否有实际项目经验

### Q: 如何处理信息冲突？

**A:**
- 优先官方文档
- 看发布时间
- 看具体场景
- 标注不确定性

---

## 推荐工具

### 搜索增强
- **Zapier / Make**: 自动化工作流
- **RSSHub**: 订阅各平台更新
- **Feedly**: RSS聚合阅读

### 知识管理
- **Notion**: 笔记整理
- **Obsidian**: 知识图谱
- **Zotero**: 文献管理

### 协作工具
- **Git**: 版本控制
- **GitHub**: 协作和分享
- **HackMD**: 协作文档

---

**最后更新**：2026-03-27
