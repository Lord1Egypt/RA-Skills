---
name: ai-tech-news-factory
description: AI全链路科技资讯工厂 — 热点追踪 → RSS深度采集 → 知识卡片+小红书+公众号多平台一键发布
category: AI
triggers: 科技资讯, AI新闻, 每日资讯, 热点追踪, 内容工厂, 多平台发布, 帮我写小红书, 帮我写公众号
---

# AI全链路科技资讯工厂

将多个专业 Skill 编排成完整的科技资讯生产流水线，实现从热点发现到多平台一键发布的全自动化。

## 🎯 核心价值

- **一键启动**: 一句话触发完整资讯生产链路
- **多平台覆盖**: 同时输出小红书卡片笔记 + 公众号深度文章
- **零重复劳动**: 一次采集，多格式生成
- **质量底线**: 竞品分析思路 + 深度内容获取思路不可省略

## 🔧 依赖 Skills

| Skill | 用途 | 来源 |
|-------|------|------|
| `content-trend-weapon` | 热点追踪与趋势分析 | 本地 |
| `rss-ai-reader` | RSS深度内容采集与AI摘要 | clawhub |
| `card-renderer` | 小红书风格知识卡片生成 | 本地 |
| `xiaohongshutools` | 小红书笔记发布 | 本地 |
| `wechat-article-pro` | 公众号深度文章生成与发布 | 本地 |

## 📐 编排架构

```
[content-trend-weapon]
       ↓ 热点话题 + 趋势分析
[rss-ai-reader]
       ↓ 深度内容采集（标题+摘要+正文）
       ↓ 智能去重 + 质量过滤
       ├──→ [card-renderer] → 小红书封面卡片
       │         ↓
       │    [xiaohongshutools] → 小红书笔记发布
       │
       └──→ [wechat-article-pro] → 公众号深度文章（2000-3000字）
                    ↓
              发布到公众号
```

## 🚀 使用方法

### 方式一：完整流水线（推荐）

```markdown
帮我生成今天的AI科技资讯日报：
1. 用 content-trend-weapon 追踪今日AI和大模型热点
2. 用 rss-ai-reader 抓取 techcrunch、verge、MIT Tech Review 的最新文章
3. 生成3张不同风格的 card-renderer 知识卡片
4. 用 xiaohongshutools 发布小红书笔记（3条：热点、应用、深度各1条）
5. 用 wechat-article-pro 生成一篇3000字的公众号深度文章
6. 保存到 /root/articles/YYYY-MM-DD/
```

### 方式二：单步执行

```markdown
用 rss-ai-reader 抓取今天的 AI 新闻，生成摘要
```

```markdown
用 card-renderer 把这段文案渲染成赛博朋克风知识卡片
```

```markdown
用 wechat-article-pro 写一篇关于"AI Agent发展现状"的公众号文章
```

## ⚙️ 配置说明

### RSS 订阅源配置（rss-ai-reader）

编辑 `config/config.yaml` 添加更多订阅源：

```yaml
rss_sources:
  - url: https://techcrunch.com/feed/
    tag: 科技
  - url: https://www.theverge.com/rss/index.xml
    tag: AI
  - url: https://news.mit.edu/topic/artificial-intelligence-rss
    tag: MIT
```

### 小红书发布配置（xiaohongshutools）

确保已配置 cookies 和 session（参考 SKILL.md）。

### 公众号配置（wechat-article-pro）

使用刘润风格深度写作，自动生成封面图。

## 📁 输出结构

```
/root/articles/YYYY-MM-DD/
├── trending-topics.md      # 热点追踪报告
├── rss-summaries.md        # RSS采集摘要
├── cards/                  # 知识卡片图片
│   ├── card-1-cyberpunk.png
│   ├── card-2-macpro.png
│   └── card-3-bauhaus.png
├── xiaohongshu/
│   └── posts.json          # 小红书发布记录
└── wechat-article.md       # 公众号文章 Markdown
```

## 🔄 定时自动化

配合 OpenClaw cron 实现每日自动执行：

```bash
# 每日 08:00 UTC 执行完整流水线
cron add --name "AI科技资讯工厂" \
  --schedule "cron:0 8 * * *" \
  --sessionTarget isolated \
  --payload '{"kind":"agentTurn","message":"执行 ai-tech-news-factory 完整流水线，保存到 /root/articles/{date}/"}'
```

## 💡 质量要求

- **竞品分析思路**：生成内容前必须分析同类内容，指出差异化优势
- **内容获取思路**：明确说明信息来源和抓取策略
- **深度要求**：公众号文章不低于2000字，含代码示例或数据支撑
- **卡片风格**：封面用赛博朋克，详情页用包豪斯或Mac Pro风格

## 🔧 故障排除

| 问题 | 解决方案 |
|------|---------|
| RSS 抓取失败 | 检查网络连接；确认 feed URL 可访问 |
| 小红书发布失败 | 刷新 cookies；检查 session 有效性 |
| 卡片渲染失败 | 确认 canvas依赖安装；检查文案长度 |
| 公众号发布失败 | 确认公众号授权状态；检查封面图大小 |
