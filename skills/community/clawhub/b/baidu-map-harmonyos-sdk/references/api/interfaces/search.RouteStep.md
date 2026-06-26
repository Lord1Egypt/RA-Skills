[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / RouteStep

# Interface: RouteStep

[search](../modules/search.md).RouteStep

路线中的一个路段

## Hierarchy

- **`RouteStep`**

  ↳ [`MassTransitStep`](search.MassTransitStep.md)

  ↳ [`DrivingStep`](search.DrivingStep.md)

  ↳ [`WalkingStep`](search.WalkingStep.md)

  ↳ [`TransitStep`](search.TransitStep.md)

  ↳ [`BikingStep`](search.BikingStep.md)

  ↳ [`BusStep`](search.BusStep.md)

## Table of contents

### Properties

- [distance](search.RouteStep.md#distance)
- [duration](search.RouteStep.md#duration)
- [name](search.RouteStep.md#name)
- [wayPoints](search.RouteStep.md#waypoints)

## Properties

### distance

• **distance**: `number`

路段距离

___

### duration

• **duration**: `number`

路段耗时

___

### name

• **name**: `string`

路段道路名称

___

### wayPoints

• `Optional` **wayPoints**: [`LatLng`](../classes/base.LatLng.md)[]

路段所经过的地理坐标集合
