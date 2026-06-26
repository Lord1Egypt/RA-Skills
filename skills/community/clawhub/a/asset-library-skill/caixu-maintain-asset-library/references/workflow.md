# Workflow

## Trigger examples

- “看一下这个资产库现在什么状态”
- “把这条资产修正一下”
- “把这条不该进入库的材料归档”
- “看有哪些待复核材料”

## Sequencing

1. `list_libraries` 或直接进入指定 `library_id`
2. `get_library_overview`
3. 需要人工复核时用 `list_review_queue`
4. 逐条执行：
   - `patch_asset_card`
   - `archive_asset`
   - `restore_asset`
5. 用 `query_assets` 或 `get_library_overview` 验证结果

## Maintenance defaults

- 默认一次只处理一条资产
- 默认优先修订字段，其次归档
- 归档后默认不再被下游 query/lifecycle/package 消费

## Non-goals

- 不重跑整库 ingest/build
- 不做 merge 的人工编辑
- 不做 package 或 submit
