---
name: dashboard-briefing
description: "从 FineBI 看板提炼核心信息，生成日报、周报、群播报卡片和定时简报。"
---

# Dashboard Briefing

## 适用范围

这个子技能用于“消费看板”的场景，而不是回写数据的场景。适合：

- 生成日报、周报、月报摘要
- 把经营看板同步到群聊
- 先发一条测试卡片确认格式
- 配置基于看板的定时简报

## 必要流程

1. 先读取 `references/dashboard-question-answer-flow.md`，按看板问答取数链路执行。
2. 再读取 `references/dashboard-id-resolution-flow.md`，解析唯一的 `dashboardId`。不要把用户输入名称直接当成 id。
3. 如果是整体仪表板分析、日报、周报或经营摘要，优先调用 `export-dashboard-pdf` 获取完整快照。
4. 只有用户明确询问某个具体组件、图表或指标卡的数据时，再读取 `references/dashboard-widget-data-flow.md`，先调用 `resolve-dashboard-widgets`，再调用 `get-widget-data`。
5. 最后再做摘要、卡片或定时播报。

## 必要 CLI 使用

- `get-entry-tree`
- `get-published-subject-resources`
- `search-my-dashboards`
- `get-dashboard-user-info`
- `get-dashboards-by-subject`
- `resolve-dashboard-widgets`
- `get-widget-data`
- `export-dashboard-pdf`

## 规则

- 所有需要 `dashboardId` 的场景，先走共享的 dashboard id 解析流程。
- 定位仪表板时，先查挂出目录，再查“我的分析”。
- 不要自写 JS、Python、浏览器自动化或抓包逻辑来查找看板、组件或数据。
- 整体仪表板分析优先使用 PDF，不主动查询组件数据。
- 只有用户明确要求具体组件、图表或指标卡数据时，才解析可取数组件并取 widget 数据。
- 如果看板不唯一，先澄清。
- 先拿到 FineBI 真实输出，再生成摘要。
- 不要伪造指标、趋势、刷新时间或播报结果。

## 建议输出

- 一段简要结论
- 关键指标列表
- 必要时附带截图或导出件
- 如果是定时播报，明确播报频率和目标群
