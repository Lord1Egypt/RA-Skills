# 操作字段与清洗规则

## 检查数据

`clean.inspect` 上传一个不超过 10 MiB 的 CSV/XLSX。结果包含工作表、列、数据行、空单元格、类型、重复候选、公式数量和 `document_fingerprint`。存在公式时 `can_clean=false`，应先让用户另存为值。

## 预览清洗

`clean.preview` 接收 `inspect_task_id` 和 1 至 30 条结构化 `rules`。支持：

- `trim_text`、`fill_missing`
- `normalize_type`、`normalize_date`、`normalize_amount`
- `flag_outliers`、`drop_duplicates`

每条规则显式指定 `sheet_index` 和 `columns`。转换失败策略为 `keep`、`null` 或 `reject`；去重必须指定 `keep=first|last` 与 `nulls_equal`。返回 `checked_cells`、`billing_units`、`changed_cells`、`affected_rows`、样本、指纹和 `confirmation_token`。

## 确认执行

`clean.execute` 只接收 `preview_task_id` 与原样 `confirmation_token`，对冻结快照和规则执行，生成 CSV/XLSX 私有 `artifacts` 与审计摘要。令牌长度为 64，不能由 Agent 自行构造。
