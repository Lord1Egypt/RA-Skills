[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / GeoBound

# Class: GeoBound

[map](../modules/map.md).GeoBound

**`Fileoverview`**

地理范围数据结构，由西南以及东北坐标点确认

**`Author`**

donghsuifeng

**`Version`**

1.0

**`Date`**

2021-12-06

## Table of contents

### Constructors

- [constructor](map.GeoBound.md#constructor)

### Properties

- [sw](map.GeoBound.md#sw)
- [ne](map.GeoBound.md#ne)

### Methods

- [setBox](map.GeoBound.md#setbox)
- [getBox](map.GeoBound.md#getbox)
- [contains](map.GeoBound.md#contains)
- [getCenter](map.GeoBound.md#getcenter)
- [destroy](map.GeoBound.md#destroy)
- [toString](map.GeoBound.md#tostring)

## Constructors

### constructor

• **new GeoBound**(`lb?`, `rt?`): [`GeoBound`](map.GeoBound.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `lb?` | [`Point`](base.Point.md) |
| `rt?` | [`Point`](base.Point.md) |

#### Returns

[`GeoBound`](map.GeoBound.md)

## Properties

### sw

• **sw**: [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

___

### ne

• **ne**: [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

## Methods

### setBox

▸ **setBox**(`lb?`, `rt?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `lb?` | [`Point`](base.Point.md) |
| `rt?` | [`Point`](base.Point.md) |

#### Returns

`void`

___

### getBox

▸ **getBox**(): [`MapStatusMapBound`](../interfaces/map.MapStatusMapBound.md)

#### Returns

[`MapStatusMapBound`](../interfaces/map.MapStatusMapBound.md)

___

### contains

▸ **contains**(`point`): `boolean`

判断该地理范围是否包含一个地理位置

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point` | [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\> | 被判断的地理位置 |

#### Returns

`boolean`

该地理范围是否包含一个地理位置

___

### getCenter

▸ **getCenter**(): [`LatLng`](base.LatLng.md)

获取该地理范围的中心地理坐标

#### Returns

[`LatLng`](base.LatLng.md)

该地理范围的中心地理坐标

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`

___

### toString

▸ **toString**(): `string`

#### Returns

`string`
