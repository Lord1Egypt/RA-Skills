---
name: ai_news_fetcher
description: >
  采集公开网页 AI 新闻并写入飞书原始新闻表。
  触发场景：抓取AI新闻、采集新闻源、更新原始新闻表、补抓某个源、维护新闻池、
  指定时间范围或来源写入飞书、cron新闻采集、爬取AI资讯、拉取最新新闻、
  跑一轮采集、新闻入库、补跑新闻源、加新的新闻源。
  不触发（交给 ai_news_reporter）：生成日报、写signal、发早报导读、归并事件、
  阅读全文写判断、筛选高价值新闻、更新关注清单。
  不触发（交给 ai_weekly_reporter）：生成周报、合成趋势线、更新观察链。
---

# AI 新闻抓取 Skill

`采集公开网页新闻 → 标准化 → 写入飞书原始新闻表`。不负责日报/周报/早报/判断。

## 前置依赖

- **飞书 Bitable**：`bitable_target.json`（参考 `.example.json`）
- **[Agent Reach](https://github.com/Panniantong/Agent-Reach)** + **Python 3.10+**

> **凭证说明**：不内置飞书凭证。`bitable_target.json` 用户本地创建，`.gitignore` 已排除，仓库仅含占位符。

> **第三方服务**：使用 [Jina Reader](https://r.jina.ai)（免费、无需 key）将网页转 markdown。目标 URL 发送至 r.jina.ai，不发送凭证或用户数据。

## 执行前必读

- `references/execution.md` — 执行流程、门控检查点、模式说明
- `references/data-model.md` — 字段定义
- `references/sources.md` — 源地址和源级规则
- `references/gotchas.md` — 仅排障时读

## 管道（不可跳步）

```
curl r.jina.ai → normalize_agent_reach.py → build_source_items.py → 去重 → 入表
```

## 硬约束

1. 必须走 `normalize_agent_reach.py` + `build_source_items.py`，禁止手算时间戳或手工构造 JSON
2. 只做"抓取并写入"，不顺带生成日报、发消息、查整表、回写分析字段
3. 写入成功即结束，不补抓不重跑
4. cron 模式：不用浏览器、不进调试模式、不临时编写脚本
5. 用 `curl r.jina.ai`，不用 `web_fetch` 工具
6. 时间/链接/来源不可信时，不写入
7. 任务结束只返回：`写入N条` 或 `0条写入`
