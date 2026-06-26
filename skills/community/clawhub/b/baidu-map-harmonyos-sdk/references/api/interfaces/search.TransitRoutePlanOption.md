[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / TransitRoutePlanOption

# Interface: TransitRoutePlanOption

[search](../modules/search.md).TransitRoutePlanOption

公交路线规划参数

## Table of contents

### Properties

- [from](search.TransitRoutePlanOption.md#from)
- [to](search.TransitRoutePlanOption.md#to)
- [cityName](search.TransitRoutePlanOption.md#cityname)
- [policy](search.TransitRoutePlanOption.md#policy)

## Properties

### from

• **from**: [`PlanNode`](../classes/search.PlanNode.md)

起点

___

### to

• **to**: [`PlanNode`](../classes/search.PlanNode.md)

终点

___

### cityName

• `Optional` **cityName**: `string`

所在城市名，默认为北京

___

### policy

• `Optional` **policy**: [`TransitPolicy`](../enums/search.TransitPolicy.md)

换乘策略,默认时间优先
