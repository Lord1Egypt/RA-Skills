---
name: morning-briefing
description: 每天早上定时生成并发送数据分析与项目进展汇报。适用场景：1) 触发晨检 cron（每日 09:00）；2) 用户要求查看当前项目状态/进展摘要；3) 需要整合 memory 日志、WPS 日历、Ezone 卡片、PG 压测状态等多源数据生成简报。触发词包括：早报、晨检、数据汇报、进展汇报、项目状态、今天怎么样。
---

# Morning Briefing

每天 09:00 Asia/Shanghai 触发，向霞姐发送早安 + 项目进展简报。

## 数据源

| 来源 | 读取内容 | 优先级 |
|------|---------|--------|
| MEMORY.md | 核心项目状态索引 | 必读 |
| memory/YYYY-MM-DD.md | 今天 + 昨天的工作日志 | 必读 |
| WPS 日历 | 今日日程 | 可选 |
| Ezone | 待办卡片（如有权限） | 可选 |

## 输出格式

见 [references/template.md](references/template.md)。

## 执行流程

1. 读取 MEMORY.md（核心索引）
2. 读取今天和昨天的日志文件（`memory/YYYY-MM-DD.md`）
3. 提取 `#pending` 标签的条目 → 待处理事项
4. 从 MEMORY.md 的"项目进展"部分提取各项目状态
5. （可选）调用 WPS 日历查今日日程：
   ```
   mcporter --config skills/wps-cli/mcporter.json call 'ksc-mcp-wps.mcp_calendar.list_events(query: {"start_time": "今日00:00 ISO8601", "end_time": "今日23:59 ISO8601"})'
   ```
6. 按模板生成简报文本
7. 用 message 工具发送到当前会话（无需指定 target，自动路由）

## 内容原则

- **结论优先**：每个项目只写一句状态 + 最关键风险
- **待处理事项单列**：从日志的 `#pending` 条目提取，带机器名/具体行动
- **不废话**：不写"根据日志分析"这类过渡语，直接上内容
- **异常高亮**：磁盘满/压测停止/服务宕机等用 ⚠️ 标注

## Cron 配置

```
# 当前生效的晨检任务（cron ID: 008a8882-a71a-4b97-b257-6438022e00bf）
openclaw cron list  # 验证任务存在

# 若需重建：
openclaw cron add --session main --schedule "0 9 * * *" --timezone "Asia/Shanghai" \
  --name "morning-memory-check" \
  "读取 MEMORY.md 和今天昨天的日志，向霞姐发晨报，包含：早安问候、各项目进展状态、#pending 待处理事项、今日 WPS 日历日程"
```

## 注意事项

- cron 任务 target 必须是 `main`（isolated session 容易超时）
- WPS 日历调用失败时静默跳过，不阻塞发送
- 发完消息回复 `NO_REPLY`，避免重复消息
