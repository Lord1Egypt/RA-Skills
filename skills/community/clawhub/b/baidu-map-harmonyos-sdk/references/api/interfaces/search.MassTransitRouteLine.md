[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / MassTransitRouteLine

# Interface: MassTransitRouteLine

[search](../modules/search.md).MassTransitRouteLine

表示一个跨城交通换乘路线，换乘路线将根据既定策略调配多种交通工具。
<p>
换乘路线可能包含：城市公交路段，地铁路段，步行路段，飞机，大巴
</p>

## Hierarchy

- [`RouteLine`](search.RouteLine.md)\<[`MassTransitStep`](search.MassTransitStep.md)\>

  ↳ **`MassTransitRouteLine`**

## Table of contents

### Properties

- [starting](search.MassTransitRouteLine.md#starting)
- [terminal](search.MassTransitRouteLine.md#terminal)
- [title](search.MassTransitRouteLine.md#title)
- [steps](search.MassTransitRouteLine.md#steps)
- [distance](search.MassTransitRouteLine.md#distance)
- [duration](search.MassTransitRouteLine.md#duration)
- [arriveTime](search.MassTransitRouteLine.md#arrivetime)
- [price](search.MassTransitRouteLine.md#price)
- [priceInfo](search.MassTransitRouteLine.md#priceinfo)
- [newSteps](search.MassTransitRouteLine.md#newsteps)

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

• **steps**: [`MassTransitStep`](search.MassTransitStep.md)[]

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

### arriveTime

• `Optional` **arriveTime**: `string`

本线路预计到达时间，格式：2024-04-05T17：06：10

___

### price

• `Optional` **price**: `number`

本线路的总票价（元）

___

### priceInfo

• `Optional` **priceInfo**: [`PriceInfo`](search.PriceInfo.md)[]

车票详细信息

___

### newSteps

• `Optional` **newSteps**: [`MassTransitStep`](search.MassTransitStep.md)[][]

该线路的step信息
