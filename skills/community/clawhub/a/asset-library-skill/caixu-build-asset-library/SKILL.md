---
name: caixu-build-asset-library
description: "Build Personal Asset Library. Use when the user wants to convert parsed materials into asset cards and a queryable library at the asset-build stage, including “建资产库”“生成资产卡”“去重整理版本”. Prefer caixu-skill when the user asks for the full end-to-end mainline or is unsure which stage to run. This skill creates a build_asset_library pipeline run, reads parsed files from caixu-data-mcp, extracts canonical asset cards from trustworthy parsed text, merges likely duplicate versions conservatively, persists assets and merged groups, and completes the pipeline run with library_id. Do not use it for querying, lifecycle judgment, package creation, or submission."
---

# Build Personal Asset Library

在用户要“建资产库”“生成资产卡”“去重整理版本”时使用这个 skill。

## Quick flow

1. 读取已解析文件
2. 先做 document triage，再抽取 `asset_card`
3. 保守归并并写入资产库

## Read next only when needed

- 要确认本批次和全库读取策略时，读 [references/workflow.md](references/workflow.md)
- 要确认 `BuildAssetLibraryData`、`asset_card` 或归并字段时，读 [references/tool-contracts.md](references/tool-contracts.md)
- 要对齐 triage / extraction / merge 的 JSON 形状时，读 [references/output-patterns.md](references/output-patterns.md)
- 遇到低置信、`binary_only`、归并不确定时，读 [references/failure-modes.md](references/failure-modes.md)

## Required tools

- `caixu-data-mcp.create_pipeline_run`
- `caixu-data-mcp.get_parsed_files`
- `caixu-data-mcp.append_pipeline_step`
- `caixu-data-mcp.upsert_asset_cards`
- `caixu-data-mcp.upsert_merged_assets`
- `caixu-data-mcp.complete_pipeline_run`

## Required input

- `library_id`
- `file_ids[]?`

## Workflow

1. 先创建 `build_asset_library` pipeline run，并在关键阶段追加 `append_pipeline_step`。
2. 调用 `get_parsed_files`，优先限定到当前批次的 `file_ids[]`。
3. 跳过没有可信文本的文件；`binary_only` 不能仅靠文件名生成 `asset_card`。
4. 先逐文件做 document triage，判断是否应进入资产库，并给出保守的文档角色提示。
5. 只对 triage 通过的文件，从 parsed text 和 file metadata 抽取 canonical `asset_card`。
6. 先写入 `upsert_asset_cards`，再本地构造保守的 `merged_assets`。
7. 如果存在可确认的归并组，再调用 `upsert_merged_assets`；没有归并组不是失败。
8. 用 `complete_pipeline_run` 结束 build run，并返回 `BuildAssetLibraryData`，必须包含 `library_id`、`asset_cards`、`merged_assets` 和 summary。

## Guardrails

- 不得虚构 holder、issuer、日期或高置信度。
- 高歧义字段返回 `null`，不要输出 `"unknown"`。
- 不确定是否同一材料时，不合并。
- 不得删除原始 `asset_card`。
- 这是单人个人资产库；公示、名单、团队材料只有在能保守映射到 owner 时才允许进入。
- 简历类材料必须视为 `experience`，且不得携带 issuer/date。
- 没有任何可信材料时，返回结构化 `partial` 或 `failed`，不要伪造资产库。
- 如果 `document_triage` 遇到 recoverable model failure，允许 pipeline 保守放行到 `asset_extraction`，但必须留下 warning / audit。
