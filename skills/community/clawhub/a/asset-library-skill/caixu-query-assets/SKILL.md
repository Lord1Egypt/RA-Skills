---
name: caixu-query-assets
description: "Search Personal Asset Library. Use when the user wants to search or filter an existing 材序 asset library at the query stage, including “查我有哪些材料”“看哪些可复用”“按类型筛资产”“用自然语言找相关材料”. Prefer caixu-skill when the user asks for the full end-to-end mainline or is unsure which stage to run. This skill normalizes filters into precise retrieval inputs, uses agent tags plus FTS by default, and only calls the optional semantic vector retrieval function when the user explicitly asks for similar or related materials."
---

# Search Personal Asset Library

在用户要“查我有哪些材料”“看哪些可复用”“按类型筛资产”时使用这个 skill。

## Quick flow

1. 归一化查询条件
2. 调用 `query_assets`
3. 返回结构化结果或推荐先建库

## Read next only when needed

- 需要映射中文类别、场景或有效期状态时，读 [references/workflow.md](references/workflow.md)
- 需要确认 `QueryAssetsData` 字段或 tool 边界时，读 [references/tool-contracts.md](references/tool-contracts.md)
- 需要对齐 filter 归一化输出时，读 [references/output-patterns.md](references/output-patterns.md)
- 遇到空库、空结果、SQLite 不可用时，读 [references/failure-modes.md](references/failure-modes.md)

## Required tools

- `caixu-data-mcp.query_assets`
- `caixu-data-mcp.query_assets_vector`
- `caixu-data-mcp.reindex_library_search`

## Required input

- `library_id`
- `material_types[]?`
- `keyword?`
- `semantic_query?`
- `tag_filters_any[]?`
- `tag_filters_all[]?`
- `validity_statuses[]?`

## Workflow

1. 要求一个明确的 `library_id`，不要猜测库。
2. 把用户表达归一化成 canonical filters + semantic query + agent tag filters。
3. 当用户明确要自然语言检索，或当前库看起来是旧库且索引状态不明确时，先调用 `reindex_library_search` 一次，再进入正式查询。
4. 如果用户完全没给过滤条件，做一个安全的有界查询，不要无界倾倒全库。
5. 默认调用 `query_assets`，它只做 `agent_tags + FTS + 结构过滤` 的精确检索。
6. 只有当用户明确要求“相似材料”“相关材料”“语义扩展召回”时，才额外调用 `query_assets_vector`。
7. 如果库还没有 `asset_card`，停止并推荐 `build-asset-library`。

## Guardrails

- 这是精确检索优先的 skill：agent 只负责意图归一化与结果摘要，不重新抽取材料。
- 正式默认检索路径是 `agent_tags + FTS + 结构过滤`。
- `query_assets_vector` 是可选函数，只在用户明确要求“相似/相关材料”时才使用。
- 若向量检索暂时不可用，不得影响默认 `query_assets`。
- 不得把“没有命中”包装成假错误。
- 不得把 SQLite 错误伪装成空结果。
- `merged_assets` 只能跟随命中的资产返回，不要把无关归并组混进结果。
