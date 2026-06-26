# regression queries

Use these queries to quickly sanity-check retrieval quality after refactors.

## Route / config / memory system
- `记忆检索 主路由`
- `昨天更新后为什么记忆搜索变了`
- `memory_search 默认入口`
- `本地 memory-retrieval 主路由`

## Feishu / incident / root-cause
- `飞书昨天为什么断联了`
- `duplicate plugin id gateway timeout`
- `飞书 插件重复`

## User preference / decision recall
- `小红书 配图策略`
- `品牌后置`
- `默认搜索主链路`
- `敏感信息不落盘`

## Expected properties
Good results should usually include:
- correct anchor terms in `explain.anchor_hits`
- strong overlap on domain phrases
- recent daylog entries when the query is time-sensitive
- fewer generic “example” or “current status” false positives
