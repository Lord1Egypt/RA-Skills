# AI 开发博客工厂 (ai-devblog-factory)

> GitHub Trending + 技术资讯 → AI 分析 → 结构化博客 → 飞书文档

## 🎯 业务场景

技术团队需要持续追踪 GitHub 开源动态和技术趋势，但：
- GitHub Trending 每天成千上万项目，人工刷不过来
- 技术资讯分散在 Hacker News、dev.to、Twitter/X 等多个平台
- 每周技术周报全靠人工整理，耗时 1-2 小时
- 好内容看完就忘，无法形成团队知识积累

**AI 开发博客工厂** 将这个流程完全自动化，每天早上自动生成一份结构化的技术博客，包含 GitHub Trending 精选、技术趋势分析和推荐学习路径，自动发布到飞书文档。

## 💔 痛点分析

| 痛点 | 影响 | 传统解法 | 本方案 |
|------|------|---------|--------|
| GitHub Trending 信息过载 | 错过好项目 | 人工刷，耗时 30min+ | 自动筛选 + AI 分析 |
| 技术资讯分散 | 遗漏重要内容 | 订阅多个 RSS | 统一抓取 + 聚合 |
| 周报整理耗时 | 挤压开发时间 | 每周 1-2h 手动整理 | 自动生成，5min |
| 内容难以沉淀 | 知识流失 | 看完即忘 | 飞书文档持久化 |

## 🔄 工作流

```
┌─────────────────────────────────────────────────────────────┐
│                        输入层                                │
│   GitHub Trending  ·  dev.to RSS  ·  Hacker News           │
└────────────────────────┬────────────────────────────────────┘
                         │ Agent-Reach 统一抓取
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                        分析层                                │
│   summarize (AI)—趋势分析 · 项目洞察 · 热点识别             │
└────────────────────────┬────────────────────────────────────┘
                         │ 结构化分析结果
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                        生成层                                │
│   wechat-article-pro—3000-4000 字结构化技术博客             │
└────────────────────────┬────────────────────────────────────┘
                         │ 完整文章
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                        发布层                                │
│   feishu_doc—发布至飞书云文档 / Wiki，自动通知              │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Skill 编排图谱

```
Agent-Reach (GitHub/RSS 抓取)
    │
    │ raw_trending.json + raw_news.json
    ▼
summarize (AI 分析)
    │
    │ analysis.json + insights.md
    ▼
wechat-article-pro (博客生成)
    │
    │ article.md
    ▼
feishu_doc (飞书发布)
    │
    │ doc_url → 团队通知
    ▼
feishu_chat (可选通知)
```

### 各 Skill 职责

| Skill | 输入 | 输出 | 核心能力 |
|-------|------|------|---------|
| **Agent-Reach** | GitHub / RSS URL | 原始内容 JSON | 多源内容抓取、加密参数自动处理 |
| **summarize** | 原始内容 | 结构化分析 | 趋势识别、要点提炼、AI 洞察 |
| **wechat-article-pro** | 分析结果 | 完整文章 | 技术博客风格写作、自动配图提示 |
| **feishu_doc** | 文章 Markdown | 飞书文档 URL | 创建文档、写入内容、权限管理 |

## 📝 使用示例

### 场景：每天早 9 点自动生成技术博客

**Step 1: 创建 cron 定时任务**

```bash
# 建议 cron 表达式：每天 UTC 9:00 (=北京时间17:00)
# 放到 OpenClaw 里执行
```

**Step 2: 查看输出**

```
✅ 博客已生成并发布至飞书
📄 文档链接: https://feishu.cn/docx/xxx
📅 生成时间: 2026-04-15 09:00 UTC
📊 涵盖内容: GitHub Trending Top10 + 15 条技术资讯
```

### 单次手动执行

```bash
# 抓取 + 生成 + 发布
openclaw run ai-devblog-factory

# 指定语言 (Python 为例)
openclaw run ai-devblog-factory --language python

# 仅生成草稿（不发布）
openclaw run ai-devblog-factory --draft true
```

## 📊 效率对比

| 任务 | 传统方式 | 本方案 | 提升 |
|------|---------|--------|------|
| 刷 Trending | 30 分钟/天 | 0 分钟 | 全自动 |
| 收集技术资讯 | 20 分钟/天 | 0 分钟 | 全自动 |
| 整理周报 | 60-120 分钟/周 | 0 分钟 | 全自动 |
| **合计/年** | **110-170 小时** | **0 小时** | **∞** |

## 🔧 高级配置

### 自定义 RSS 源

编辑 `workflow.json` 中的 `sources.rss.feeds`：

```json
{
  "feeds": [
    "https://dev.to/feed",
    "https://news.ycombinator.com/rss",
    "https://www.techcrunch.com/feed/",
    "https://feeds.feedburner.com/oreilly/radar"
  ]
}
```

### 多语言 Trending

```bash
# 每日生成多语言版本
openclaw run ai-devblog-factory --language python
openclaw run ai-devblog-factory --language rust
openclaw run ai-devblog-factory --language javascript
```

### 推送到指定飞书群

```json
{
  "notify": {
    "enabled": true,
    "channel": "feishu",
    "chat_id": "oc_xxxxx",
    "message": "📬 今日技术博客已更新：${doc_url}"
  }
}
```

## 📂 文件结构

```
ai-devblog-factory/
├── SKILL.md               # 技能定义（含 frontmatter）
├── README.md              # 本文档
├── workflow.json          # 工作流配置
└── example/
    ├── sample-output.md   # 示例输出
    └── sample-analysis.json  # 示例分析结果
```

## 🆚 竞品对比

| 方案 | GitHub Trending | 多源资讯 | AI 分析 | 飞书发布 | 开源定制 |
|------|:--------------:|:--------:|:-------:|:--------:|:--------:|
| 传统方案（人工） | ✅ | ❌ | ❌ | ❌ | N/A |
| 现有工具（GitHub App） | ✅ | ❌ | ❌ | 部分 | ❌ |
| **AI DevBlog Factory** | ✅ | ✅ | ✅ | ✅ | ✅ |

## 🚨 注意事项

1. **API 频率限制**：GitHub API 受速率限制，建议 cron 间隔 ≥ 12h
2. **内容版权**：抓取内容仅供学习，商用请注意许可证
3. **飞书权限**：首次使用需确认 feishu_doc 机器人有文档写入权限

---

**版本**: 1.0.0
**Skill 数量**: 4
**维护者**: zhonglongshen
**创建日期**: 2026-04-15
