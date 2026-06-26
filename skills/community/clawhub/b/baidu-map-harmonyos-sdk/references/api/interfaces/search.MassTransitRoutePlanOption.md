[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / MassTransitRoutePlanOption

# Interface: MassTransitRoutePlanOption

[search](../modules/search.md).MassTransitRoutePlanOption

换乘路线规划参数

## Table of contents

### Properties

- [from](search.MassTransitRoutePlanOption.md#from)
- [to](search.MassTransitRoutePlanOption.md#to)
- [tacticsInCity](search.MassTransitRoutePlanOption.md#tacticsincity)
- [tacticsIntercity](search.MassTransitRoutePlanOption.md#tacticsintercity)
- [transTypeIntercity](search.MassTransitRoutePlanOption.md#transtypeintercity)
- [pageSize](search.MassTransitRoutePlanOption.md#pagesize)
- [pageIndex](search.MassTransitRoutePlanOption.md#pageindex)

## Properties

### from

• **from**: [`PlanNode`](../classes/search.PlanNode.md)

起点

___

### to

• **to**: [`PlanNode`](../classes/search.PlanNode.md)

终点

___

### tacticsInCity

• `Optional` **tacticsInCity**: [`TacticsInCity`](../enums/search.TacticsInCity.md)

设置市内公交换乘策略

___

### tacticsIntercity

• `Optional` **tacticsIntercity**: [`TacticsIntercity`](../enums/search.TacticsIntercity.md)

设置跨城公交换乘策略

___

### transTypeIntercity

• `Optional` **transTypeIntercity**: [`TransTypeIntercity`](../enums/search.TransTypeIntercity.md)

设置跨城交通方式策略

___

### pageSize

• `Optional` **pageSize**: `number`

设置每页返回几条路线,[1,10]

___

### pageIndex

• `Optional` **pageIndex**: `number`

设置返回第几页 从0开始
