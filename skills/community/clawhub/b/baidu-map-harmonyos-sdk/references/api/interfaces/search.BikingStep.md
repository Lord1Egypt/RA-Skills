[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BikingStep

# Interface: BikingStep

[search](../modules/search.md).BikingStep

描述一个骑行路段

## Hierarchy

- [`RouteStep`](search.RouteStep.md)

  ↳ **`BikingStep`**

## Table of contents

### Properties

- [distance](search.BikingStep.md#distance)
- [duration](search.BikingStep.md#duration)
- [name](search.BikingStep.md#name)
- [wayPoints](search.BikingStep.md#waypoints)
- [direction](search.BikingStep.md#direction)
- [entrance](search.BikingStep.md#entrance)
- [exit](search.BikingStep.md#exit)
- [pathString](search.BikingStep.md#pathstring)
- [entranceInstructions](search.BikingStep.md#entranceinstructions)
- [exitInstructions](search.BikingStep.md#exitinstructions)
- [instructions](search.BikingStep.md#instructions)
- [turnType](search.BikingStep.md#turntype)
- [restrictionsInfo](search.BikingStep.md#restrictionsinfo)
- [restrictionsStatus](search.BikingStep.md#restrictionsstatus)

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

### direction

• `Optional` **direction**: `number`

当前道路的方向角

___

### entrance

• `Optional` **entrance**: [`RouteNode`](search.RouteNode.md)

路线起点

___

### exit

• `Optional` **exit**: [`RouteNode`](search.RouteNode.md)

路线终点

___

### pathString

• `Optional` **pathString**: `string`

路段位置坐标描述

___

### entranceInstructions

• `Optional` **entranceInstructions**: `string`

路段起点信息描述

___

### exitInstructions

• `Optional` **exitInstructions**: `string`

路段终点信息描述

___

### instructions

• `Optional` **instructions**: `string`

路段描述

___

### turnType

• `Optional` **turnType**: `string`

行驶转向方向（如"直行", "左前方转弯"）

___

### restrictionsInfo

• `Optional` **restrictionsInfo**: `string`

限行信息

___

### restrictionsStatus

• `Optional` **restrictionsStatus**: `number`

限行类型，1：禁行；2：逆行
