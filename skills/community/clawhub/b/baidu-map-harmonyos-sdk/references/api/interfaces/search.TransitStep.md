[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / TransitStep

# Interface: TransitStep

[search](../modules/search.md).TransitStep

表示一个换乘路段

## Hierarchy

- [`RouteStep`](search.RouteStep.md)

  ↳ **`TransitStep`**

## Table of contents

### Properties

- [distance](search.TransitStep.md#distance)
- [duration](search.TransitStep.md#duration)
- [name](search.TransitStep.md#name)
- [wayPoints](search.TransitStep.md#waypoints)
- [instructions](search.TransitStep.md#instructions)
- [vehicleInfo](search.TransitStep.md#vehicleinfo)
- [entrance](search.TransitStep.md#entrance)
- [exit](search.TransitStep.md#exit)
- [stepType](search.TransitStep.md#steptype)
- [pathString](search.TransitStep.md#pathstring)

## Properties

### distance

• **distance**: `number`

路段距离

#### Inherited from

[RouteStep](search.RouteStep.md).[distance](search.RouteStep.md#distance)

___

### duration

• **duration**: `number`

路段耗时

#### Inherited from

[RouteStep](search.RouteStep.md).[duration](search.RouteStep.md#duration)

___

### name

• **name**: `string`

路段道路名称

#### Inherited from

[RouteStep](search.RouteStep.md).[name](search.RouteStep.md#name)

___

### wayPoints

• `Optional` **wayPoints**: [`LatLng`](../classes/base.LatLng.md)[]

路段所经过的地理坐标集合

#### Inherited from

[RouteStep](search.RouteStep.md).[wayPoints](search.RouteStep.md#waypoints)

___

### instructions

• `Optional` **instructions**: `string`

该路段换乘说明

___

### vehicleInfo

• `Optional` **vehicleInfo**: [`VehicleInfo`](search.VehicleInfo.md)

交通工具信息

___

### entrance

• `Optional` **entrance**: [`RouteNode`](search.RouteNode.md)

路段入口信息

___

### exit

• `Optional` **exit**: [`RouteNode`](search.RouteNode.md)

路段出口信息

___

### stepType

• `Optional` **stepType**: [`TransitRouteStepType`](../enums/search.TransitRouteStepType.md)

路段类型

___

### pathString

• `Optional` **pathString**: `string`

出于性能考虑，缓存path坐标点，当需要用到时再解析
