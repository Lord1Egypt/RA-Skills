---
name: caixu-maintain-asset-library
description: "Maintain Personal Asset Library. Use when the user wants to inspect, review, patch, archive, restore, or verify a personal material asset library after initial build, including “看库概览”“修一条资产”“归档这条不该进库的材料”“看待复核队列”. Prefer caixu-skill when the user asks for the full end-to-end mainline or is unsure which stage to run. This skill loads library overviews and review queues from caixu-data-mcp, applies minimal maintenance actions such as patching or archiving one asset at a time, and re-checks query results. Do not use it for fresh ingest, asset extraction, lifecycle judgment, package building, or submission."
---

# Maintain Personal Asset Library

在用户要“看库概览”“修一条资产”“归档这条不该进库的材料”“看待复核队列”时使用这个 skill。

## Quick flow

1. 先看库概览或 review queue
2. 逐条做 patch / archive / restore
3. 再查一次资产库确认结果生效

## Read next only when needed

- 需要确认维护顺序和何时 patch / archive 时，读 [references/workflow.md](references/workflow.md)
- 需要确认 overview、review queue、patch 返回结构时，读 [references/tool-contracts.md](references/tool-contracts.md)
- 需要最小 JSON 输出模板时，读 [references/output-patterns.md](references/output-patterns.md)
- 遇到找不到库、误归档、patch 冲突时，读 [references/failure-modes.md](references/failure-modes.md)

## Required tools

- `caixu-data-mcp.list_libraries`
- `caixu-data-mcp.get_library_overview`
- `caixu-data-mcp.list_review_queue`
- `caixu-data-mcp.patch_asset_card`
- `caixu-data-mcp.archive_asset`
- `caixu-data-mcp.restore_asset`
- `caixu-data-mcp.query_assets`

## Required input

- `library_id?`
- `maintenance_goal?`
- `asset_id?`

## Workflow

1. 用户未给 `library_id` 时，先用 `list_libraries` 找候选，再落到单库维护。
2. 先读 `get_library_overview`；涉及低置信或边界材料时再读 `list_review_queue`。
3. 默认一次只改一条资产：`patch_asset_card`、`archive_asset` 或 `restore_asset`。
4. 修改后必须再跑一次 `query_assets` 或重新读取 `get_library_overview` 验证结果已生效。
5. 成功返回维护后的关键事实：库概览、改动后的资产、仍待复核的数量。

## Guardrails

- 这是维护 skill，不负责重新 ingest、重建整库、生命周期判断、打包或提交。
- 不要直接发明资产字段；只在用户明确要修正且证据充分时 patch。
- 不要批量修改多条资产，除非用户明确要求并且每条改动都能解释。
- 归档优先于删除；MVP 不做物理删除。
- `query-assets` 只负责验证，不负责修改。
- 如果 patch 证据不足，保留 `needs_review`，不要硬改成高置信完成态。
