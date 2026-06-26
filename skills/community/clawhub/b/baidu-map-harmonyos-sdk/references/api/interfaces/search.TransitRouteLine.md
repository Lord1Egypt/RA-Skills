[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / TransitRouteLine

# Interface: TransitRouteLine

[search](../modules/search.md).TransitRouteLine

表示一个换乘路线，换乘路线将根据既定策略调配多种交通工具。
<p>
换乘路线可能包含：城市公交路段，地铁路段，步行路段
</p>

## Hierarchy

- [`RouteLine`](search.RouteLine.md)\<[`TransitStep`](search.TransitStep.md)\>

  ↳ **`TransitRouteLine`**

## Table of contents

### Properties

- [starting](search.TransitRouteLine.md#starting)
- [terminal](search.TransitRouteLine.md#terminal)
- [title](search.TransitRouteLine.md#title)
- [steps](search.TransitRouteLine.md#steps)
- [distance](search.TransitRouteLine.md#distance)
- [duration](search.TransitRouteLine.md#duration)

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

• **steps**: [`TransitStep`](search.TransitStep.md)[]

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
