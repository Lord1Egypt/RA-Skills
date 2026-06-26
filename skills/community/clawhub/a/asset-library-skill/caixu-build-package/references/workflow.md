# Workflow

## Preconditions

- 资产库已存在
- 已有通过校验的 lifecycle run
- 已知 `output_dir`
- 已知 `submission_profile`

## Sequential flow

1. `get_latest_lifecycle_run`
2. `get_rule_profile`
3. `query_assets`
4. `get_parsed_files`
5. agent 选材
6. preflight
7. docgen 导出
8. `write_package_run`

## Agent should decide

- `selected_asset_ids`
- `operator_notes`
- 包内说明和顺序

Agent 不应决定：

- readiness 的真假
- lifecycle 是否通过
- 是否伪造缺失文件
