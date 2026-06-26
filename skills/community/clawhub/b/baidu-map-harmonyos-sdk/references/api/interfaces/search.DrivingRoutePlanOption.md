[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / DrivingRoutePlanOption

# Interface: DrivingRoutePlanOption

[search](../modules/search.md).DrivingRoutePlanOption

驾车路线规划参数

## Table of contents

### Properties

- [mFrom](search.DrivingRoutePlanOption.md#mfrom)
- [mTo](search.DrivingRoutePlanOption.md#mto)
- [mCityName](search.DrivingRoutePlanOption.md#mcityname)
- [mPolicy](search.DrivingRoutePlanOption.md#mpolicy)
- [mWayPoints](search.DrivingRoutePlanOption.md#mwaypoints)
- [mtrafficPolicy](search.DrivingRoutePlanOption.md#mtrafficpolicy)

## Properties

### mFrom

• **mFrom**: [`PlanNode`](../classes/search.PlanNode.md)

起点

___

### mTo

• **mTo**: [`PlanNode`](../classes/search.PlanNode.md)

终点

___

### mCityName

• `Optional` **mCityName**: `string`

当前城市名称

___

### mPolicy

• `Optional` **mPolicy**: [`DrivingPolicy`](../enums/search.DrivingPolicy.md)

驾车路线规划策略

___

### mWayPoints

• `Optional` **mWayPoints**: [`PlanNode`](../classes/search.PlanNode.md)[]

途径点

___

### mtrafficPolicy

• `Optional` **mtrafficPolicy**: [`DrivingTrafficPolicy`](../enums/search.DrivingTrafficPolicy.md)

是否支持路况数据
