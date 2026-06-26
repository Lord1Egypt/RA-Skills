[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BikingRoutePlanOption

# Interface: BikingRoutePlanOption

[search](../modules/search.md).BikingRoutePlanOption

骑行路线规划参数

## Table of contents

### Properties

- [from](search.BikingRoutePlanOption.md#from)
- [to](search.BikingRoutePlanOption.md#to)
- [ridingType](search.BikingRoutePlanOption.md#ridingtype)
- [roadPrefer](search.BikingRoutePlanOption.md#roadprefer)
- [wayPoints](search.BikingRoutePlanOption.md#waypoints)

## Properties

### from

• **from**: [`PlanNode`](../classes/search.PlanNode.md)

起点坐标

___

### to

• **to**: [`PlanNode`](../classes/search.PlanNode.md)

终点坐标

___

### ridingType

• `Optional` **ridingType**: [`RidingType`](../enums/search.RidingType.md)

骑行类型（0：普通骑行模式，1：电动车模式）

___

### roadPrefer

• `Optional` **roadPrefer**: [`RoadPrefer`](../enums/search.RoadPrefer.md)

路线偏好（0：智能推荐，3：规避逆行）

___

### wayPoints

• `Optional` **wayPoints**: [`PlanNode`](../classes/search.PlanNode.md)[]

途径点
