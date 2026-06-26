---
name: ai_weekly_reporter
description: >
  基于本周日报和产业链图谱生成 AI 周报，合成趋势线并更新观察链判断基线。
  触发场景：生成周报、写本周趋势、合成本周信号、更新产业链判断、周度回顾、
  cron周报生成、本周AI总结。
  不触发：生成日报、写早报导读、抓取新闻、采集新闻源 → 这些交给 ai_news_reporter 或 ai_news_fetcher。
---

# AI 周报生成 Skill

只做一件事：`读取本周日报 → 跨天信号关联 → 合成趋势线 → 深度解读 → 生成周报 → 更新观察链`

不负责：每日新闻采集、日报生成、早报导读 → 交给 `ai_news_fetcher` / `ai_news_reporter`

## 核心规则

周报 = 把一周的日报信号关联起来，找出趋势线，更新产业链判断基线。周报不是日报合集，是趋势文档。

## 前置依赖

- **ai_news_reporter**：周报依赖日报数据（本地 MD 或飞书 wiki）、产业链图谱（`watch_chains.md`）和关注清单表配置（`watch_target.json`）
- **飞书 wiki 知识库**：周报文档挂载到飞书知识库（可选）

> **凭证说明**：本 skill 不内置任何飞书凭证。凭证配置在 `ai_news_reporter` 中管理，已被 `.gitignore` 排除。

> **第三方服务**：深度解读环节需要阅读原文全文，使用 [Jina Reader](https://r.jina.ai)（免费、无需 API key）读取公开网页。目标文章的 URL 会发送到 `r.jina.ai`，不会发送飞书凭证或用户数据。

> **跨 skill 文件读写**：本 skill 会读取并更新 `ai_news_reporter/references/watch_chains.md`（产业链观察图谱），以及读取 `ai_news_reporter/watch_target.json`（关注清单表配置）。这是设计上的协作关系：三个 skill 共享同一套产业链观察体系，日报产出信号 → 周报合成趋势并更新判断基线 → 更新后的基线反过来指导下一周日报的高价值筛选。

## 执行前必读

- `references/reporting.md` — 执行流程、门控检查点、信号关联规则
- `references/output-template.md` — 周报输出模板与风格要求
- `../ai_news_reporter/references/watch_chains.md` — 产业链关注图谱（读取 + 周报后更新）
- `../ai_news_reporter/watch_target.json` — 关注清单表配置

## 管道（不可跳步）

```
读取本周日报（本地优先，fallback 飞书）
    ↓
读取 watch_chains.md + 关注清单表
    ↓
跨天信号关联 → 合成趋势线
    ↓
选最重要话题 → 阅读原文 → 深度解读
    ↓
按模板生成周报文档 → 保存本地 + 挂飞书 wiki
    ↓
更新 watch_chains.md（判断基线）
    ↓
审视关注清单（批量清理过期问题）
```

## 硬约束

1. 周报基于日报生成，不读取原始新闻表；但深度解读环节必须阅读原文
2. 优先从 `workspace/daily_reports/` 读取本地 MD；本地没有的日期，从飞书 wiki 日报文档读取
3. 信号关联必须有依据（同链路/因果/同玩家/对立面/待验证被回答），不硬关联
4. 每条趋势线必须包含"对照观察链"字段（所属链路、原判断基线、本周变化、更新后判断）
5. 必须包含一篇深度解读（商业/产品/技术/政策任选），必须先读原文再写
6. 周报生成后，必须更新 `watch_chains.md` 并在过程日志中记录变更数量
7. 周报生成后，必须审视关注清单并在过程日志中记录回答/超期/新增数量
8. 飞书文档内容必须和本地 MD 副本完全一致，不得省略
9. 周报保存到 `workspace/weekly_reports/YYYY-MM-DD.md`（以周末日期命名）
10. 任务结束需附过程日志
