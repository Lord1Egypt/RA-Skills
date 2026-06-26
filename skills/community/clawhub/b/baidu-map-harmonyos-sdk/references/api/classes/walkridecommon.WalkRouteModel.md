[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / WalkRouteModel

# Class: WalkRouteModel

[walkridecommon](../modules/walkridecommon.md).WalkRouteModel

## Table of contents

### Constructors

- [constructor](walkridecommon.WalkRouteModel.md#constructor)

### Properties

- [startX](walkridecommon.WalkRouteModel.md#startx)
- [startY](walkridecommon.WalkRouteModel.md#starty)
- [startStr](walkridecommon.WalkRouteModel.md#startstr)
- [routeItemList](walkridecommon.WalkRouteModel.md#routeitemlist)
- [endX](walkridecommon.WalkRouteModel.md#endx)
- [endY](walkridecommon.WalkRouteModel.md#endy)
- [endStr](walkridecommon.WalkRouteModel.md#endstr)
- [type](walkridecommon.WalkRouteModel.md#type)
- [distanceStr](walkridecommon.WalkRouteModel.md#distancestr)
- [distance](walkridecommon.WalkRouteModel.md#distance)
- [duration](walkridecommon.WalkRouteModel.md#duration)
- [isFocus](walkridecommon.WalkRouteModel.md#isfocus)
- [index](walkridecommon.WalkRouteModel.md#index)
- [lightNum](walkridecommon.WalkRouteModel.md#lightnum)
- [labelName](walkridecommon.WalkRouteModel.md#labelname)
- [markItemList](walkridecommon.WalkRouteModel.md#markitemlist)
- [label](walkridecommon.WalkRouteModel.md#label)
- [viaPoints](walkridecommon.WalkRouteModel.md#viapoints)
- [endMarkerX](walkridecommon.WalkRouteModel.md#endmarkerx)
- [endMarkerY](walkridecommon.WalkRouteModel.md#endmarkery)

### Methods

- [getStartAndEndPoint](walkridecommon.WalkRouteModel.md#getstartandendpoint)

## Constructors

### constructor

• **new WalkRouteModel**(): [`WalkRouteModel`](walkridecommon.WalkRouteModel.md)

#### Returns

[`WalkRouteModel`](walkridecommon.WalkRouteModel.md)

## Properties

### startX

• **startX**: `number` = `0`

___

### startY

• **startY**: `number` = `0`

___

### startStr

• **startStr**: `string` = `""`

___

### routeItemList

• **routeItemList**: `RouteItemModel`[] = `[]`

___

### endX

• **endX**: `number` = `0`

___

### endY

• **endY**: `number` = `0`

___

### endStr

• **endStr**: `string` = `""`

___

### type

• **type**: `number` = `-1`

___

### distanceStr

• **distanceStr**: `string` = `''`

___

### distance

• **distance**: `number` = `0`

___

### duration

• **duration**: `string` = `''`

___

### isFocus

• **isFocus**: `boolean` = `false`

___

### index

• **index**: `number` = `0`

___

### lightNum

• **lightNum**: `string` = `''`

___

### labelName

• **labelName**: `string` = `''`

___

### markItemList

• **markItemList**: `MarkInfo`[] = `[]`

___

### label

• **label**: `string` = `''`

___

### viaPoints

• **viaPoints**: `number`[] = `[]`

途径点

**`Description`**

x,y 墨卡托坐标构成的途径点数组

___

### endMarkerX

• **endMarkerX**: `number` = `0`

___

### endMarkerY

• **endMarkerY**: `number` = `0`

## Methods

### getStartAndEndPoint

▸ **getStartAndEndPoint**(): `number`[]

#### Returns

`number`[]
