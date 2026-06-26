---
name: daily-news-brief
description: 聚合并整理多源新闻，按科技/财经/AI/智能体分类排序，生成 Markdown 摘要并可定时执行。当用户提到"新闻"、"今日新闻"、"整理新闻"、"科技新闻"、"财经新闻"、"AI 新闻"、"智能体新闻"、"聚合新闻"或需要定时获取新闻摘要时使用。
---

# Daily News Brief

自动新闻聚合工具，每天定时整理科技、财经、AI、智能体领域的热门新闻。

## 使用场景（When to Use）

- 需要每天自动生成新闻摘要
- 需要按领域（科技/财经/AI/智能体）分类展示
- 需要从多个免费新闻源聚合并去重
- 需要将新闻保存为本地 Markdown 文档
- 需要手动抓取某一天或某一类新闻
- 需要调整定时任务或新闻源配置

## 功能特性

- **多源聚合**：从多个免费新闻源抓取内容
- **智能分类**：自动分类为科技、财经、AI、智能体
- **热度排序**：按发布时间和阅读量排序
- **定时执行**：默认每晚 9 点执行（可自定义）
- **多种输出**：发送到聊天窗口 + 生成本地 MD 文档
- **媒体筛选**：仅使用正规专业媒体的数据
- **多通道推送**：通过 OpenClaw 通道发送摘要（Telegram/飞书/WhatsApp 等）

## 技术亮点

- **自建抓取链路**：RSS + 网页抓取直连源站，不依赖 tavily/web_fetch 搜索
- **来源均衡摘要**：避免单一媒体霸榜，提升聚合价值
- **来源上限控制**：全量与摘要分开控制，每类/每来源数量可配置
- **去重与排序**：标题/链接去重，按新鲜度优先
- **OpenClaw 一体化**：通道推送 + cron 调度统一管理
- **低依赖低成本**：无需外部搜索 API，稳定可控
- **更快与潜在省 token**：直连源站获取结构化内容，减少搜索请求与长上下文传输

## Workflow Routing

| Workflow | 触发条件 | 文件 |
|----------|---------|------|
| **Setup** | 首次安装、配置新闻源或修改定时任务时 | `workflows/Setup.md` |
| **FetchNews** | 手动获取新闻、执行定时任务时 | `workflows/FetchNews.md` |
| **Configure** | 修改新闻源、分类规则、定时时间时 | `workflows/Configure.md` |

## 使用流程

1. **首次使用**：运行 Setup workflow，配置新闻源和定时任务
2. **日常使用**：定时任务自动执行 FetchNews workflow
3. **手动获取**：随时可手动触发 FetchNews workflow
4. **配置调整**：运行 Configure workflow 修改设置

## 输出说明

- **聊天窗口输出**：按分类汇总 + 数量概览
- **本地文档**：`~/daily-news-brief/每日新闻/YYYY-MM-DD.md`
- **日志**：`~/.daily-news-brief/logs/`（抓取与错误日志）
- **成功标准**：输出包含 4 类分类标题，且本地文件可读
- **推送摘要**：每条新闻包含来源（来源字段必填）

## 示例

**示例 1：首次安装和配置**
```text
用户："帮我设置新闻聚合，每晚 9 点整理新闻"
→ 运行 Setup workflow
→ 选择新闻源（推荐：36氪、虎嗅、澎湃、财新等免费源）
→ 配置定时任务为每晚 9 点
→ 提示：是否保留本地 MD 文档？（可随时删除）
→ 完成
```

**示例 2：手动获取今日新闻**
```text
用户："整理一下今天的科技和 AI 新闻"
→ 运行 FetchNews workflow
→ 抓取最新新闻
→ 按类别分类
→ 生成 Markdown 文档并发送到聊天窗口
→ 完成
```

**示例 3：命令行手动执行（项目根目录）**
```bash
# 测试模式（只抓少量新闻）
node tools/FetchNews.ts --test

# 仅抓取 AI 分类
node tools/FetchNews.ts --category AI
```

**示例 4：修改定时任务时间**
```text
用户："把新闻整理时间改成早上 8 点"
→ 运行 Configure workflow
→ 修改定时任务为早上 8 点
→ 保存配置
→ 完成
```

## 新闻源说明

**推荐的免费新闻源：**

| 领域 | 新闻源 | 获取方式 |
|------|--------|---------|
| 科技 | 36氪 (36kr.com) | RSS / 网页抓取 |
| 科技 | 虎嗅网 (huxiu.com) | RSS / 网页抓取 |
| 财经 | 财新网 (caixin.com) | RSS / 网页抓取 |
| 财经 | 澎湃新闻 (thepaper.cn) | RSS / 网页抓取 |
| AI | 机器之心 (jiqizhixin.com) | RSS / 网页抓取 |
| AI | 新智元 (xinzhiyuan.ai) | RSS / 网页抓取 |
| 智能体 | AI 研习社 | RSS / 网页抓取 |

**注意**：所有推荐源均为免费访问，无需付费订阅。

## 本地文档说明

默认保存位置：`~/daily-news-brief/每日新闻/YYYY-MM-DD.md`

- 文档会按日期命名，方便归档
- 用户可随时删除或保留
- 可在 Setup workflow 中修改保存路径

## 定时任务说明

默认时间：每天 21:00（晚上 9 点）

可通过 Configure workflow 修改为任意时间。

**macOS/Linux 定时任务：** 使用 cron
**Windows 定时任务：** 使用任务计划程序
**推荐：** 使用 OpenClaw cron 统一调度与日志管理

## OpenClaw 通道推送

在 Setup workflow 中由 OpenClaw 智能体询问用户推送渠道与时间，并完成通道登录。
目标（群/频道/联系人）由 OpenClaw 内部配置管理，本技能只记录通道列表与推送开关。

**常用通道**：Telegram、飞书（Feishu）、WhatsApp、Slack、Discord

## 故障排查

- **抓取失败或 RSS 不可达**：先检查网络，再尝试更换新闻源或切换为网页抓取模式  
- **定时任务未执行**：检查 `cron` 是否生效，查看 `~/.daily-news-brief/logs/cron.log`
- **本地文档未生成**：确认 `localDocPath` 可写，检查目录权限
- **分类不准确**：在 `tools/NewsClassifier.ts` 调整关键词
- **重复新闻过多**：检查去重逻辑，确保标题与链接同时参与去重
- **OpenClaw 推送失败**：检查 `openclaw channels status` 与通道登录状态

## Tips

- 优先使用 RSS 源，稳定性高于网页抓取
- 同一站点源过多会拖慢抓取速度，建议控制在 5-10 个
- 针对易变页面，优先使用官方 RSS 或公开 API
- 建议每天只抓取一次，避免被目标站点限流
- 本地文档按日期归档，便于做后续统计
- 需要更高质量分类时，可将关键词扩展为正则或引入轻量 NLP
- 若来源重复，优先保留发布方权威站点的内容

## 目录结构

```text
daily-news-brief/
├── SKILL.md                      # 主文件（本文件）
├── QuickStartGuide.md            # 快速开始指南
├── workflows/
│   ├── Setup.md                  # 安装和配置流程
│   ├── FetchNews.md              # 新闻抓取流程
│   └── Configure.md              # 配置修改流程
└── tools/
    ├── FetchNews.ts              # 抓取主入口
    ├── Configure.ts              # 配置管理 CLI
    ├── NewsFetcher.ts            # 新闻抓取工具
    ├── NewsClassifier.ts         # 新闻分类工具
    ├── MarkdownGenerator.ts      # MD 文档生成工具
    └── types.ts                  # TypeScript 类型
```
