# Tool Contracts

## Required objects

- `PackageRunData`
- `package_plan`
- `RuleProfileBundle`

## package_plan must preserve

- `library_id`
- `package_id`
- `target_goal`
- `selected_asset_ids`
- `generated_files`
- `submission_profile`
- `readiness`
- `operator_notes`

## Export expectations

至少围绕以下结果物组织：

- 资产总表
- 续办清单
- 目标材料包 zip

文件名可以由共享 docgen 决定，但不能声称存在未生成的导出物。
