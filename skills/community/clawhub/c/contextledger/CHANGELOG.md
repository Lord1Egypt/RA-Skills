# Changelog

## 1.0.0

Release theme: 从“能连接知识”升级到“能审计结论”。

What changed:
- 发布 `ContextLedger / 知识账本`，明确定位为知识审计层而不是知识库
- 支持把一个结论拆回到 2 到 5 份关键来源，标出 newest / oldest / undated / likely stale
- 强化证据分级，区分 direct evidence、corroborated evidence、inference、assumption、unknown
- 强化冲突表达，要求把 factual、time、scope、definition 等冲突留在结果里，而不是抹平
- 默认输出证据账本式结果：来源、时效、冲突、证据与推断、当前最稳判断、下一步核查

Suggested one-line changelog:
- Launched ContextLedger, an evidence-first knowledge audit skill that traces sources, judges freshness, surfaces conflicts, and separates evidence from inference.
