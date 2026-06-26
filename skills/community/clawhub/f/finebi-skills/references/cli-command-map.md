# CLI 命令索引

这个文件记录了 `finebi-skills` 应优先引用的 FineBI CLI 命令。

## 命令契约

字段语义、工作流字段和常见后续链路见：

- `command-contracts/get-entry-tree.md`
- `command-contracts/get-published-subject-resources.md`
- `command-contracts/resolve-dashboard-widgets.md`
- `command-contracts/get-widget-data.md`
- `command-contracts/search-my-datasets.md`
- `command-contracts/search-public-dataset.md`
- `command-contracts/preview-dataset-data.md`

## 工作流指南

多步骤命令链路见：

- `dashboard-question-answer-flow.md`
- `dashboard-id-resolution-flow.md`
- `published-subject-resource-flow.md`
- `dashboard-widget-data-flow.md`
- `dataset-search-and-preview-flow.md`

## Dashboard 相关命令

- `get-entry-tree`
- `get-published-subject-resources`
- `search-my-dashboards`
- `get-dashboard-user-info`
- `get-dashboards-by-subject`
- `resolve-dashboard-widgets`
- `get-widget-data`
- `get-dashboard-design-configure`
- `export-dashboard-excel`
- `export-dashboard-pdf`
- `export-dashboard-image`

## Dataset 相关命令

- `search-my-datasets`
- `get-publick-datasets-list`
- `search-public-dataset`
- `preview-dataset-data`

## Subject 与目录相关命令

- `get-entry-tree`
- `get-published-subject-resources`

## 使用规则

- 技能优先使用这里列出的 CLI 命令名。
- 定位仪表板时，优先使用 `get-entry-tree -k <keyword> -> get-published-subject-resources` 从挂出目录查找，再使用 `search-my-dashboards` 查“我的分析”。
- 调用 `get-entry-tree` 时应尽量带 `-k <keyword>`，避免目录树响应过大。
- 组件问答优先使用 `resolve-dashboard-widgets`，不要优先解析完整 `get-dashboard-design-configure`。
- 整体看板分析不主动调用 `resolve-dashboard-widgets` 或 `get-widget-data`，除非用户明确要求具体组件数据。
- 复核 `export-dashboard-excel` 结果时，必须用 `read_only=False` 检查真实单元格内容。
- `get-dashboard-design-configure` 只用于需要完整配置细节的补充场景。
- 如果工作流需要 CLI 还没有的能力，写成“缺少 CLI 能力”，不要凭空发明命令。
- 主技能和子技能都不应承诺仓库里不存在的 CLI 命令。
