[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / RouteLine

# Interface: RouteLine\<T\>

[search](../modules/search.md).RouteLine

路线数据结构的基础接口,表示一条路线，路线可能包括：路线规划中的换乘/驾车/步行路线
<p>
此接口为路线数据结构的基础接口，一般关注其子接口即可，无需直接使用基础接口
</p>

## Type parameters

| Name | Type |
| :------ | :------ |
| `T` | extends [`RouteStep`](search.RouteStep.md) |

## Hierarchy

- **`RouteLine`**

  ↳ [`MassTransitRouteLine`](search.MassTransitRouteLine.md)

  ↳ [`BikingRouteLine`](search.BikingRouteLine.md)

  ↳ [`DrivingRouteLine`](search.DrivingRouteLine.md)

  ↳ [`WalkingRouteLine`](search.WalkingRouteLine.md)

  ↳ [`TransitRouteLine`](search.TransitRouteLine.md)

## Table of contents

### Properties

- [starting](search.RouteLine.md#starting)
- [terminal](search.RouteLine.md#terminal)
- [title](search.RouteLine.md#title)
- [steps](search.RouteLine.md#steps)
- [distance](search.RouteLine.md#distance)
- [duration](search.RouteLine.md#duration)

## Properties

### starting

• **starting**: ``null`` \| [`RouteNode`](search.RouteNode.md)

___

### terminal

• **terminal**: ``null`` \| [`RouteNode`](search.RouteNode.md)

___

### title

• **title**: `string`

___

### steps

• **steps**: `T`[]

___

### distance

• **distance**: `number`

___

### duration

• **duration**: `number`
