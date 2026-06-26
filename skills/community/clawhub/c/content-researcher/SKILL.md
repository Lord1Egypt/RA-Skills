---
name: content-researcher
description: 内容研究员：批量搜索、收集、总结文章/视频/新闻，自动生成结构化素材库，支持关键词和趋势分析
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "python": "3.7+", "bins": ["claw", "summarize"] },
      },
  }
---

# content-researcher - 内容研究员

快速批量收集和总结行业素材，为内容创作者提供结构化调研报告。

## 适用场景

- 📰 **自媒体素材库**：批量搜索某一领域的最新文章和观点
- 🎓 **行业研究**：快速了解某个主题的最新动态
- 📊 **竞品分析**：收集竞争对手的信息和报道
- 📈 **趋势追踪**：监控关键词趋势，发现热点话题
- 💡 **灵感获取**：从大量素材中提炼核心观点

## 核心功能

- ✅ **批量搜索**：一次搜索多个关键词，每个关键词独立搜索
- ✅ **自动总结**：集成 summarize 工具，为每个结果生成 AI 摘要
- ✅ **结构化报告**：输出清晰的 Markdown 报告或 JSON 数据
- ✅ **去重处理**：自动去重同一文章（基于 URL）
- ✅ **可定制**：控制每关键词搜索结果数量、总结果数
- ✅ **快速导出**：单文件输出，便于分享和使用

## 依赖说明

- **claw**：用于执行 web_search 工具搜索网络
- **summarize**：用于生成 AI 摘要（可选，--summarize 启用）
- 需要安装这两个工具（均通过 clawhub 安装）

## 快速开始

### 1. 安装依赖

```bash
# 安装本技能
./install.sh

# 确保 summarize 已安装
clawhub install summarize
```

### 2. 基础使用

```bash
# 搜索 AI 相关的最新文章
content-researcher --keywords "AI,人工智能" --output ai_research.md

# 增加搜索深度
content-researcher --keywords "自媒体运营" --per-keyword 20 --max-results 50 --summarize
```

### 3. 输出格式

```bash
# JSON 格式（便于程序处理）
content-researcher --keywords "Python编程" --format json --output python_news.json

# 启用 AI 总结（推荐）
content-researcher --keywords "内容创作" --summarize --output full_report.md
```

## 参数说明

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `--keywords` | 字符串 | 必填 | 搜索关键词，逗号分隔，如"AI,自媒体" |
| `--per-keyword` | 整数 | 10 | 每个关键词搜索结果数量 |
| `--max-results` | 整数 | 20 | 去重后最大结果数 |
| `--output` | 路径 | content_research_report.md | 输出文件路径 |
| `--summarize` | 布尔 | false | 是否为每个结果生成 AI 摘要 |
| `--format` | 枚举 | markdown | 输出格式（markdown, json） |
| `--model` | 字符串 | google/gemini-3-flash-preview | 总结模型（仅 --summarize 有效） |

## 示例输出（Markdown）

```markdown
# 内容调研报告
**生成时间**：2026-03-15 21:00:15
**关键词**：AI, 自媒体

## 📊 搜索结果概览
共找到 15 条相关结果

### 1. 人工智能新突破：GPT-5 即将发布
**来源**：techcrunch.com
**链接**：https://techcrunch.com/...

**摘要**：
OpenAI 宣布 GPT-5 将在下月发布，新模型将具备多模态推理能力...

**AI 总结**：
本文报道 OpenAI GPT-5 即将发布，主要新特性包括多模态推理、代码生成能力提升，预计将推动 AI 应用落地。

---
```

## 输出文件

运行后会生成：

- `<output>`：主报告文件（Markdown 或 JSON）
- 包含：
  - 所有搜索结果的标题、来源、链接、摘要
  - 如果启用 `--summarize`，还有 AI 生成的总结
  - 去重后的唯一结果

## 性能考虑

- 搜索 3 个关键词，每个 10 条：约 30-60 秒
- 启用 `--summarize`：额外增加 2-5 分钟（每个结果单独调用 LLM）
- 如果 summarize 不可用，将跳过总结步骤

## 与其他技能集成

- **social-publisher**：调研报告可直接作为公众号/小红书素材
- **omnipublisher**：将调研报告拆分成多平台版本
- **meeting-minutes**：调研结果可作为会议讨论材料
- **web_search / summarize**：底层依赖技能

## 技术细节

- 使用子进程调用 `claw tools web_search` 进行搜索
- 使用 `summarize` CLI 进行文本摘要（如果安装）
- 自动 URL 去重，避免重复内容
- 输出 UTF-8 编码，兼容所有 Markdown 编辑器

## 示例 Workflow

```bash
# 场景：需要写一篇关于"自媒体运营"的文章

# 步骤 1：快速调研
content-researcher --keywords "自媒体,内容创作,流量密码" --summarize --output research.md

# 步骤 2：查看 report.md，了解行业动态
cat research.md

# 步骤 3：使用 omnipublisher 或 social-publisher 开始写作
omnipublisher research.md --platforms wechat,xiaohongshu
```

## 故障排除

- **"command not found: claw"**：确保 OpenClaw 正常运行，`claw` 命令可用
- **"summarize not found"**：运行 `clawhub install summarize` 安装
- **搜索结果为空**：检查网络连接和关键词是否太专业
- **总结速度慢**：可减少 `--per-keyword` 数量，或禁用 `--summarize`

## 未来规划

- [ ] 支持 RSS 订阅源抓取
- [ ] 趋势图表生成（配合 data-chart-tool）
- [ ] 关键词云图可视化
- [ ] 订阅式自动调研（定时运行）
- [ ] 结果导入 Notion/Obsidian

## 许可证

MIT
