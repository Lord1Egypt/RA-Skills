---
name: ai-news-skills
description: "AI 新闻全自动工作流：采集公开网页新闻、生成日报与早报导读、合成周报趋势与深度解读。包含三个协作 skill：ai_news_fetcher（采集）、ai_news_reporter（日报）、ai_weekly_reporter（周报）。"
license: MIT
version: 1.3.0
---

# AI News Skills

一套完整的 AI 新闻自动化工作流，从采集到日报到周报。

```
公开网页 → 自动采集(fetcher) → 飞书原始新闻表 → AI筛选(reporter) → 日报 & 早报导读
                                                                      ↓ (每周日)
                                                          周报趋势 & 深度解读(weekly_reporter)
                                                                      ↓
                                                          更新产业链观察图谱
```

## 包含的 skill

| Skill | 职责 | 频率 |
|-------|------|------|
| `skills/ai_news_fetcher` | 从公开网页采集 AI 新闻，写入飞书多维表格 | 每天 3-4 次 |
| `skills/ai_news_reporter` | 从飞书表筛选高价值事件，生成日报和早报导读 | 每天 1 次 |
| `skills/ai_weekly_reporter` | 基于本周日报合成趋势线，深度解读，更新观察链 | 每周日 1 次 |

使用时请指定具体 skill，例如 `使用 ai_news_fetcher skill 采集新闻` 或 `使用 ai_news_reporter skill 生成日报`。

## 前置依赖

- **飞书多维表格**：需要配置 `app_token` 和 `table_id`，填入各 skill 的 `bitable_target.json`（参考 `.example.json`）
- **Agent Reach**：[Agent Reach](https://github.com/Panniantong/Agent-Reach) 提供网页读取能力
- **Python 3.10+**：运行数据处理脚本

> **凭证说明**：本 skill 不内置任何飞书凭证或 API 密钥。所有配置文件（`bitable_target.json`、`watch_target.json`）由用户在本地创建，已被 `.gitignore` 排除。仓库中的 `.example.json` 仅包含占位符（`YOUR_APP_TOKEN` 等）。

> **第三方服务**：使用 [Jina Reader](https://r.jina.ai)（免费、无需 API key）将公开网页转为 markdown 文本。采集和阅读原文时，目标网页的 URL 会发送到 `r.jina.ai`，不会发送飞书凭证或用户数据。

## 详细说明

每个 skill 的 SKILL.md 包含完整的执行流程、硬约束和模板，请参阅各自目录。
