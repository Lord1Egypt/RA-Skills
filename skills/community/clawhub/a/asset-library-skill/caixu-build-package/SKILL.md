---
name: caixu-build-package
description: "Build Application Document Package. Use when the user wants export files and a submission bundle from an existing library at the packaging stage, including “生成材料包”“导出资产总表和续办清单”“准备提交包”. Prefer caixu-skill when the user asks for the full end-to-end mainline or is unsure which stage to run. This skill loads the latest validated lifecycle result, a RuleProfileBundle, assets and parsed files, asks an agent to choose package contents, validates the decision, runs deterministic docgen exports, persists the package run with an audit sidecar, and prepares the final bundle for downstream use."
---

# Build Application Document Package

在用户要“生成材料包”“导出资产总表和续办清单”“准备提交包”时使用这个 skill。

## Quick flow

1. 读取最近一次已验证的 lifecycle 结果
2. 让 agent 选材
3. 预检、导出、写 package run

## Read next only when needed

- 要确认顺序和输入前提时，读 [references/workflow.md](references/workflow.md)
- 要确认 `PackageRunData`、`package_plan`、导出物约定时，读 [references/tool-contracts.md](references/tool-contracts.md)
- 要对齐 `package_plan` 和 truthful package 输出时，读 [references/output-patterns.md](references/output-patterns.md)
- 遇到阻塞 readiness、缺真实文件、truthful package 边界时，读 [references/failure-modes.md](references/failure-modes.md)

## Required tools

- `caixu-data-mcp.query_assets`
- `caixu-data-mcp.get_parsed_files`
- `caixu-data-mcp.get_rule_profile`
- `caixu-data-mcp.get_latest_lifecycle_run`
- `caixu-data-mcp.write_package_run`

## Required local code

- 使用共享 `@caixu/docgen`
- 不要自行发明第二套导出格式

## Workflow

1. 要求 `library_id`、`goal`、`output_dir`、`submission_profile`。
2. 先读 `get_latest_lifecycle_run`；没有已验证 lifecycle 时直接失败并推荐 `check-lifecycle`。
3. 读取 `RuleProfileBundle`、资产和 parsed files。
4. 让 agent 决定 `selected_asset_ids`、`operator_notes` 和包内顺序。
5. 在导出前运行 `scripts/preflight-package-output.mjs`，确认输出目录和源文件都可用。
6. 用共享 docgen 生成 ledger 和 zip。
7. 调用 `write_package_run` 持久化 package plan 与 audit。
8. 成功后推荐下一步 `submit-demo`。

## Guardrails

- `build-package` 只能消费 lifecycle readiness，不能重写 readiness。
- 即使阻塞，也只允许 truthful package，不能把 blocked 翻成 ready。
- 不得声称文件已导出，除非文件真实存在。
- zip 必须包含真实源文件，不是空 manifest。
