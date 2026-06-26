# Workflow

## Trigger examples

- “把我这些材料建成资产库，列出未来 60 天需要续办或补办的事项，并生成一份暑期实习申请材料包。”
- “帮我从头处理这批材料”
- “我不知道现在应该先跑哪个 skill”

## Routing order

1. 有 raw files / 目录路径且还没 ingest：`ingest-materials`
2. 已有 parsed files，但还没资产卡：`build-asset-library`
3. 已有资产库，需要看库概览、修订、归档、恢复：`maintain-asset-library`
4. 已有资产库，只是搜索、筛选、查询：`query-assets`
5. 已有资产库，需要判断续办、补件、readiness：`check-lifecycle`
6. 已有 validated lifecycle，需要导出 ledger / zip：`build-package`

高级可选扩展：

- 已有 package run，且确实要提交到外部演示页时，才手动启用 `submit-demo`

## Stage boundary rules

- 阶段明确时，直接路由到对应子 skill。
- 整条主线或阶段不明时，优先使用 `caixu-skill` 判定当前阶段。
- 一次只选择一个当前阶段，不在这里做多阶段执行。
- 已缺前置条件时，优先回退到最早缺失的阶段。
