# Tool Contracts

## Tool

- `caixu-data-mcp.query_assets`
- `caixu-data-mcp.query_assets_vector`
- `caixu-data-mcp.reindex_library_search`

## Output

返回 `ToolResult<QueryAssetsData>`，其中至少包含：

- `data.library_id`
- `data.asset_cards`
- `data.merged_assets`

## Preconditions

- 该库至少应完成一次成功的 `build-asset-library`
- 若库里只有 parsed files，没有 asset cards，应停止并推荐建库
- 查询可同时携带：
  - 结构过滤
  - `semantic_query`
  - `tag_filters_any`
  - `tag_filters_all`
- 旧库若还没建立 FTS/tag/向量索引，可先调用 `reindex_library_search`
- `query_assets` 是默认精确检索入口，不调用本地向量召回
- `query_assets_vector` 是显式可选函数，只在用户明确要求“相似/相关材料”时调用
