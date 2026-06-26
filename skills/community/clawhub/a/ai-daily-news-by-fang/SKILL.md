---
name: ai-daily-news
description: AI 技术进展追踪工具。当用户询问 AI 领域最新动态时触发，如："今天有什么 AI 新闻？""总结一下这周的 AI 动态""最近有什么技术进展？""AI 圈最近在讨论什么？"。专注追踪：模型发布（国际+国内）、AI 工具迭代（新工具/CLI/功能更新）、重要技术公告，社区爆火项目/论文、新理念/新范式/新实践。输出中文摘要列表，按热度排序，附带原文链接。不覆盖融资、商业动态、监管政策。
---

# AI News Collector

## 核心原则

**只追踪技术本身，不关心商业与政策。** 不搜融资、不搜监管政策、不搜 IPO/并购。

**不要口水新闻。** 过滤掉"小扎紧急警报"、"老黄怒怼玩家"类标题党。聚焦：模型、工具、理念、出圈项目。

**时间范围：3 天以内。** 超过 3 天的内容不收录。Newsletter 补漏时只取最新一期。

**多次检索，不是一次性搜索。** 用多组关键词多轮检索，确保全面。必要时直接爬取网页正文。

---

## 输出文件

日报本体存本地：`workspace/ai-daily-news/ai-daily-news-YYYY-MM-DD.md`

每次完成后把内容通过飞书消息直接推送给用户（markdown 格式，飞书可渲染），无需依赖飞书文档权限。

格式：
```markdown
# AI 日报 · YYYY-MM-DD

> 时间范围：近 3 天
> 来源：[量子位](url) · [机器之心](url) · [HN](url) · [Last Week in AI](url) · 等

## 模型

1. [标题](链接)
   > 摘要（30-50字，说明什么、为什么值得关注）

## 工具

...

## 研究/理念

...

## 出圈

...

---
_写入轮次：X 轮 · 共 N 条 · 更新时间：HH:MM_
```

---

## 工作流程（强制多轮，不是一次搜索）

### 第一轮：并行抓取主力来源

**三个来源同时抓取：**
```
量子位首页：https://www.qbitai.com
机器之心首页：https://www.jiqizhixin.com
HN 首页：https://news.ycombinator.com/
```

提取所有 AI 相关条目，标注发布时间，**只保留 3 天以内的**。

---

### 第二轮：多关键词多轮搜索补漏

第一轮之后，用以下关键词继续搜索，每次搜索发现新线索都要深入追查：

**模型类关键词（并行搜）：**
```
"new AI model" 2026
"GPT-5" OR "Claude" OR "Gemini" new version 2026
"DeepSeek" OR "Qwen" OR "Kimi" OR "MiniMax" new model
"LLM" OR "reasoning model" release 2026
```

**工具类关键词：**
```
"Claude Code" OR "Cursor" OR "Codex" new feature 2026
"AI CLI" OR "AI tool" new release 2026
"agent" OR "MCP" new update 2026
```

**研究/开源类关键词：**
```
"AI research" OR "paper" "2026" site:arxiv.org
"open source" AI model 2026
"GitHub" trending AI project
```

**每发现一个新的重要发布，都要进一步搜索该厂商/项目的最新动态。**

---

### 第三轮：针对重要条目直接爬取详情

对于前两轮发现的重要发布，**直接爬取原始页面**获取详细信息：

```
# 直接爬取官方页面（示例）
Astral 加入 OpenAI → https://astral.sh/blog/openai
Claude Code 更新 → https://code.claude.com/docs/en/changelog
OpenAI 新模型 → https://openai.com/index
Anthropic 新模型 → https://www.anthropic.com/news
```

用 `smart-web-fetch` 爬取正文，补充更准确的摘要。

---

### 第四轮：审视与淘汰

对所有收集到的条目逐一审查：

**保留标准：**
- 时间在 3 天以内
- 技术内容有实质（模型/工具/理念/出圈应用）
- 标题中性，无口水味
- 摘要说明"是什么+为什么值得关注"

**淘汰标准（严格）：**
- 超过 3 天
- 口水标题（感叹号多、情绪化词汇）
- 纯商业/融资/财报
- 过于日常化无技术含量的 AI 应用

---

### 第五轮（如有遗漏）：扩展来源

前三轮如果覆盖不足，主动扩展：

```
# 英文来源
HN 搜索：site:news.ycombinator.com AI &tbs=qdr:d
Reddit：site:reddit.com/r/MachineLearning AI &tbs=qdr:d
GitHub Trending：site:github.com/trending?since=daily AI

# Newsletter
Last Week in AI 最新一期（只取最新一期）
The Batch（Andrew Ng）最新一期
```

---

## 搜索工具说明

**主力工具：** `smart-web-fetch`
```
python3 /home/fang/.openclaw/workspace/skills/smart-web-fetch/scripts/fetch.py "<URL>"
```

**搜索工具：** `smart-web-fetch` + DuckDuckGo（加 `&tbs=qdr:d` 当天 或 `&tbs=qdr:w` 一周内）
```
python3 /home/fang/.openclaw/workspace/skills/smart-web-fetch/scripts/fetch.py "https://duckduckgo.com/html/?q=Claude+Code+new+feature+2026&tbs=qdr:d"
```

**直接爬取重要页面：**
```
python3 /home/fang/.openclaw/workspace/skills/smart-web-fetch/scripts/fetch.py "<官方页面URL>"
```

---

## 最终推送

生成完日报后，执行两步：

1. **本地存档**：`workspace/ai-daily-news/ai-daily-news-YYYY-MM-DD.md`

2. **飞书消息推送**（使用 message 工具，channel=feishu）：
   - 目标：`ou_YOUR_OPEN_FEISHU_ID`（替换为你的飞书 open_id）
   - 内容：完整的 markdown 日报内容（飞书可渲染）
   - 推送时机：**日报完成后立即发送，不要等用户来问**

> **安装后必读**：请将 `ou_YOUR_OPEN_FEISHU_ID` 替换为你的飞书 open_id，将本地存档路径改为你想要的目录。

---

## 注意事项

- **3 天以内的硬性限制**，超过即淘汰
- **多轮搜索**：第一轮抓来源 → 第二轮关键词补漏 → 第三轮直接爬详情 → 第四轮审视淘汰 → 第五轮（如需）扩展来源
- 发现重要发布要**深入追查**，不要浅尝辄止
- 标题用中性技术语言，摘要说明内容和价值
- **不搜融资、IPO、并购**
- **不搜监管、法律、政策**
- 每次写入文件都要标注轮次
- **日报完成后立即推送飞书**，不要等用户来问
