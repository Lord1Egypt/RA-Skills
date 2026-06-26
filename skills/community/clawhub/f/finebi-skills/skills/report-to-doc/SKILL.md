---
name: report-to-doc
description: "把 FineBI 看板导出件和真实数据整理成结构化分析文档。"
---

# Report To Doc

## 适用范围

这个子技能用于“把看板内容沉淀成文档”的场景。适合：

- 查询某个看板或仪表板的数据
- 洞察或者分析某个看板的数据
- 导出 EXCEL、PDF 后生成分析报告
- 把看板整理成经营分析文档
- 沉淀图表、结论和业务建议

## 必要流程

1. 先读取 `references/dashboard-question-answer-flow.md`，按看板问答取数链路执行。
2. 再读取 `references/dashboard-id-resolution-flow.md`，解析唯一的 `dashboardId`。不要把用户输入名称直接当成 id。
3. 如果是整体仪表板分析、经营分析文档或报告沉淀，优先调用 `export-dashboard-excel` 获取仪表板中组件的详细数据，如需快照，则用 `export-dashboard-pdf` 获取完整快照。
4. 只有用户明确询问某个具体组件、图表或指标卡的数据时，再读取 `references/dashboard-widget-data-flow.md`，先调用 `resolve-dashboard-widgets`，再调用 `get-widget-data`。
5. 最后根据导出结果和组件数据生成结构化文档。

## 必要 CLI 使用

- `get-entry-tree`
- `get-published-subject-resources`
- `search-my-dashboards`
- `export-dashboard-pdf`
- `export-dashboard-excel`
- `resolve-dashboard-widgets`
- `get-widget-data`

## 规则

- 所有需要 `dashboardId` 的场景，先走共享的 dashboardId 解析流程。
- 定位仪表板时，先查挂出目录，再查“我的分析”。
- 不要自写 JS、Python、浏览器自动化或抓包逻辑来查找看板、组件或数据。
- 整体仪表板分析优先使用 PDF 或 excel，优先基于导出内容生成文档，不主动查询组件数据。
- 只有用户明确要求具体组件、图表或指标卡数据时，才解析可取数组件并取 widget 数据。
- 先拿到 FineBI 真实输出，再写文档。
- 如果导出失败，要明确报错，不要伪造附件。
- 复核 FineBI Excel 导出内容时，必须使用 `read_only=False` 打开工作簿检查真实单元格内容。
- 不要仅凭 read-only 模式下的 `max_row`、`max_column` 或首行预览判断“无数据”或“只有表头”。
- 文档中的结论必须能够回溯到看板数据或导出内容。
- 如果用户指定文档类型，优先遵循该类型的结构。
- 如果已经导出了PDF或EXCEL，则不要执行导出PNG了。

## Excel 导出复核

当使用 `export-dashboard-excel` 得到 `.xlsx` 后：

- 每个 sheet 对应一个组件，sheet 名就是组件显示名。
- 文件名、sheet 名、组件显示名和单元格内容都可能包含中文，必须原样保留，不要转拼音、截断或自行重命名。
- `.xlsx` 必须用 Excel 解析库读取，不要按文本文件或 CSV 方式指定编码读取。
- 处理导出文件路径时使用支持 Unicode 的文件 API；在命令行中传递路径时必须加引号。
- 用非 read-only 模式读取工作簿，例如 `openpyxl.load_workbook(path, read_only=False, data_only=True)`。
- 逐 sheet 检查实际单元格值，确认是否存在业务数据行、合并单元格、隐藏行列或公式结果。
- read-only 模式下的维度信息和首行预览只能辅助排查，不能作为“无数据/只有表头”的最终依据。

## 建议输出

- 文档标题
- 执行摘要
- 关键指标与发现
- 趋势与风险
- 后续建议
