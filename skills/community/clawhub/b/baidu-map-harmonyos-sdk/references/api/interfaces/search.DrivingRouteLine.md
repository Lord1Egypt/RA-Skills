[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / DrivingRouteLine

# Interface: DrivingRouteLine

[search](../modules/search.md).DrivingRouteLine

表示驾车路线

## Hierarchy

- [`RouteLine`](search.RouteLine.md)\<[`DrivingStep`](search.DrivingStep.md)\>

  ↳ **`DrivingRouteLine`**

## Table of contents

### Properties

- [starting](search.DrivingRouteLine.md#starting)
- [terminal](search.DrivingRouteLine.md#terminal)
- [title](search.DrivingRouteLine.md#title)
- [steps](search.DrivingRouteLine.md#steps)
- [distance](search.DrivingRouteLine.md#distance)
- [duration](search.DrivingRouteLine.md#duration)
- [isSupportTraffic](search.DrivingRouteLine.md#issupporttraffic)
- [wayPoints](search.DrivingRouteLine.md#waypoints)
- [congestionDistance](search.DrivingRouteLine.md#congestiondistance)
- [lightNum](search.DrivingRouteLine.md#lightnum)
- [toll](search.DrivingRouteLine.md#toll)

## Properties

### starting

• **starting**: ``null`` \| [`RouteNode`](search.RouteNode.md)

#### Inherited from

[RouteLine](search.RouteLine.md).[starting](search.RouteLine.md#starting)

___

### terminal

• **terminal**: ``null`` \| [`RouteNode`](search.RouteNode.md)

#### Inherited from

[RouteLine](search.RouteLine.md).[terminal](search.RouteLine.md#terminal)

___

### title

• **title**: `string`

#### Inherited from

[RouteLine](search.RouteLine.md).[title](search.RouteLine.md#title)

___

### steps

• **steps**: [`DrivingStep`](search.DrivingStep.md)[]

#### Inherited from

[RouteLine](search.RouteLine.md).[steps](search.RouteLine.md#steps)

___

### distance

• **distance**: `number`

#### Inherited from

[RouteLine](search.RouteLine.md).[distance](search.RouteLine.md#distance)

___

### duration

• **duration**: `number`

#### Inherited from

[RouteLine](search.RouteLine.md).[duration](search.RouteLine.md#duration)

___

### isSupportTraffic

• **isSupportTraffic**: `boolean`

该路线所在区域是否含有交通流量信息

___

### wayPoints

• **wayPoints**: [`RouteNode`](search.RouteNode.md)[]

路线途经点

___

### congestionDistance

• **congestionDistance**: `number`

拥堵米数

___

### lightNum

• **lightNum**: `number`

红绿灯个数

___

### toll

• **toll**: `number`

路线收费数
