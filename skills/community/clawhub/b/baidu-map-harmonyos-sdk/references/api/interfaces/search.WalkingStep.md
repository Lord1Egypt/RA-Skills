[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / WalkingStep

# Interface: WalkingStep

[search](../modules/search.md).WalkingStep

描述一个步行路段

## Hierarchy

- [`RouteStep`](search.RouteStep.md)

  ↳ **`WalkingStep`**

## Table of contents

### Properties

- [distance](search.WalkingStep.md#distance)
- [duration](search.WalkingStep.md#duration)
- [name](search.WalkingStep.md#name)
- [direction](search.WalkingStep.md#direction)
- [entrance](search.WalkingStep.md#entrance)
- [wayPoints](search.WalkingStep.md#waypoints)
- [exit](search.WalkingStep.md#exit)
- [pathString](search.WalkingStep.md#pathstring)
- [entranceInstructions](search.WalkingStep.md#entranceinstructions)
- [exitInstructions](search.WalkingStep.md#exitinstructions)
- [instructions](search.WalkingStep.md#instructions)

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

### direction

• **direction**: `number`

该路段起点方向值 单位：度。 正北方向为0度，顺时针

___

### entrance

• **entrance**: [`RouteNode`](search.RouteNode.md)

路段起点信息

___

### wayPoints

• **wayPoints**: [`LatLng`](../classes/base.LatLng.md)[]

路段所经过的地理坐标集合

#### Overrides

[RouteStep](search.RouteStep.md).[wayPoints](search.RouteStep.md#waypoints)

___

### exit

• **exit**: [`RouteNode`](search.RouteNode.md)

路段终点信息

___

### pathString

• **pathString**: `string`

pathString 需要时可以解析

___

### entranceInstructions

• **entranceInstructions**: `string`

路段入口提示信息

___

### exitInstructions

• **exitInstructions**: `string`

路段出口指示信息

___

### instructions

• **instructions**: `string`

路段整体指示信息
