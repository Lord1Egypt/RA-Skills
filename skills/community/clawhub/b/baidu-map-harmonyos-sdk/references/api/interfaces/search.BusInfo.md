[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BusInfo

# Interface: BusInfo

[search](../modules/search.md).BusInfo

## Hierarchy

- [`TransitBaseInfo`](search.TransitBaseInfo.md)

  ↳ **`BusInfo`**

## Table of contents

### Properties

- [name](search.BusInfo.md#name)
- [departureStation](search.BusInfo.md#departurestation)
- [arriveStation](search.BusInfo.md#arrivestation)
- [departureTime](search.BusInfo.md#departuretime)
- [arriveTime](search.BusInfo.md#arrivetime)
- [type](search.BusInfo.md#type)
- [stopNum](search.BusInfo.md#stopnum)
- [directText](search.BusInfo.md#directtext)
- [lineUid](search.BusInfo.md#lineuid)
- [endUid](search.BusInfo.md#enduid)
- [startUid](search.BusInfo.md#startuid)
- [passStopInfoList](search.BusInfo.md#passstopinfolist)

## Properties

### name

• **name**: `string`

#### Inherited from

[TransitBaseInfo](search.TransitBaseInfo.md).[name](search.TransitBaseInfo.md#name)

___

### departureStation

• **departureStation**: `string`

#### Inherited from

[TransitBaseInfo](search.TransitBaseInfo.md).[departureStation](search.TransitBaseInfo.md#departurestation)

___

### arriveStation

• **arriveStation**: `string`

#### Inherited from

[TransitBaseInfo](search.TransitBaseInfo.md).[arriveStation](search.TransitBaseInfo.md#arrivestation)

___

### departureTime

• **departureTime**: `string`

#### Inherited from

[TransitBaseInfo](search.TransitBaseInfo.md).[departureTime](search.TransitBaseInfo.md#departuretime)

___

### arriveTime

• **arriveTime**: `string`

#### Inherited from

[TransitBaseInfo](search.TransitBaseInfo.md).[arriveTime](search.TransitBaseInfo.md#arrivetime)

___

### type

• `Optional` **type**: `number`

市内公交的具体类型

___

### stopNum

• `Optional` **stopNum**: `number`

途经站点数

___

### directText

• `Optional` **directText**: `string`

方向信息

___

### lineUid

• `Optional` **lineUid**: `string`

公交路线id

___

### endUid

• `Optional` **endUid**: `string`

下车点站uid

___

### startUid

• `Optional` **startUid**: `string`

上车点站uid

___

### passStopInfoList

• `Optional` **passStopInfoList**: [`RouteNode`](search.RouteNode.md)[]

途径站点
