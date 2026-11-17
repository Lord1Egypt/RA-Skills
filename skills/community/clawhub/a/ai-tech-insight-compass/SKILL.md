---
name: ai-tech-insight-compass
description: AI科技资讯深度追踪与分析工作流。每日自动采集AI前沿动态、GitHub热门项目，生成3000-5000字技术深度文章并发布到公众号。
category: AI
triggers: AI资讯, 科技洞察, 技术日报, 每日科技, 科技趋势
---

# AI Tech Insight Compass

AI科技资讯深度追踪与分析 Skill Combo。每天自动采集AI前沿动态、GitHub热门项目，生成3000-5000字技术深度文章，一站式完成从信息采集到内容发布的完整闭环。

## 定位

| 维度 | 说明 |
|------|------|
| 输入 | 当天AI/大模型技术热点关键词 |
| 输出 | 3000-5000字技术深度文章，发布到公众号 |
| 核心价值 | 减少人工搜索+写作时间，从4小时→30分钟 |
| 协作Skill | brave-search（搜索）+ github（趋势验证）+ summarize（聚合）+ tech-article-pro（写作发布）|

## 工作流程

```
[1. brave-search] → 搜索当日AI/大模型最新技术动态
       ↓
[2. github gh trending] → 验证技术趋势，获取开源项目数据
       ↓
[3. summarize] → 聚合多源信息，提炼关键洞察
       ↓
[4. tech-article-pro] → 生成3000-5000字技术深度文章
       ↓
[5. 发布到公众号/飞书文档]
```

## 详细步骤

### Step 1: 搜索当日AI技术动态

使用 brave-search 搜索当日最热AI技术动态：

```bash
cd ~/Projects/agent-scripts/skills/brave-search
./search.js "AI大模型 最新进展 2026" -n 8 --content
./search.js "LLM reasoning RLHF 2026" -n 8 --content
./search.js "arXiv AI 论文 2026 最新" -n 5 --content
```

推荐搜索词模式：
- `AI大模型 {当前月份} 最新进展`
- `LLM {具体技术如MoE/LongContext/Agent} 2026`
- `arXiv AI 论文 {热门方向}`

### Step 2: 验证GitHub趋势

使用 github skill 的 `gh` CLI 查看GitHub热门仓库：

```bash
gh api graphql -f query='
{
  search(query: "AI LLM created:>2026-08-01", type: REPOSITORY, first: 10) {
    nodes { ... on Repository { nameWithOwner stars: stargazerCount description url } }
  }
}'
```

查看当日GitHub Trending：
```bash
gh api graphql -f query='
{
  viewer { 
    trick: repository(owner: "github", name: "trend") {
      object(expression: "master") { commit { resourcePath } }
    }
  }
}'
```

### Step 3: 信息聚合与洞察提炼

使用 summarize skill 聚合多源信息：

```bash
python3 scripts/summarize.py --input /tmp/tech_intel.md --mode insight
```

生成结构化的信息摘要，包含：
- 核心事件/突破
- 技术原理简述
- 相关开源项目
- 行业影响分析

### Step 4: 撰写技术深度文章

调用 tech-article-pro skill 的写作流程：

1. 选取最值得深入的一个技术角度
2. 使用机器之心/InfoQ风格撰写
3. 包含≥4处代码示例，每处≥10行
4. 技术标签：MoE/LongContext/CoT/Transformer/SFT/RLHF/KV Cache等

### Step 5: 保存与发布

```bash
# 保存到 workspace
cp /tmp/article.md /root/articles/$(date +%Y-%m-%d)/tech-insight-daily.md

# 发布到公众号
curl -X POST http://118.25.114.18:3001/api/articles \
  -H "Content-Type: application/json" \
  -d '{"title": "...", "content": "...", "category": "AI技术"}'
```

## 输出示例

```json
{
  "date": "2026-08-10",
  "topic": "MoE大模型推理优化",
  "sources": {
    "search_results": 16,
    "github_repos": 5,
    "papers": 3
  },
  "article": {
    "title": "《MoE大模型推理优化深度解析：从原理到代码实现》",
    "word_count": 4200,
    "code_examples": 4,
    "tech_tags": ["MoE", "LLM", "推理优化", "KV Cache", "专家并行"]
  },
  "status": "published"
}
```

## 使用示例

**触发词**：
- "生成今日AI科技资讯"
- "写一篇技术深度文章"
- "AI日报"
- "科技洞察"

**执行命令**：
```bash
cd /root/skills/ai-tech-insight-compass
python3 scripts/daily_intel.py --topic "AI Agent 2026最新进展"
```

## 技术规范

- 文章字数：3000-5000字（正文）
- 代码示例：≥4处，每处≥10行有效代码
- 技术标签：≥5个精确技术标签
- 技术内容占比：≥70%
- 数据来源：搜索结果 + GitHub trending + arXiv论文
