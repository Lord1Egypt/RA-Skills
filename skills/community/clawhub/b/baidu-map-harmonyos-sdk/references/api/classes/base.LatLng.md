[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / LatLng

# Class: LatLng

[base](../modules/base.md).LatLng

经纬度点封装类

**`Package`**

@bdmap/base

**`Since`**

1.0.0

## Table of contents

### Constructors

- [constructor](base.LatLng.md#constructor)

### Properties

- [lat](base.LatLng.md#lat)
- [lng](base.LatLng.md#lng)

### Methods

- [clone](base.LatLng.md#clone)
- [equals](base.LatLng.md#equals)
- [toString](base.LatLng.md#tostring)

## Constructors

### constructor

• **new LatLng**(`_lat`, `_lng`): [`LatLng`](base.LatLng.md)

经纬度构造函数

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `_lat` | `number` | 纬度，取值范围[-90,90]。 |
| `_lng` | `number` | 经度，取值范围[-180,180]。 |

#### Returns

[`LatLng`](base.LatLng.md)

**`Since`**

1.0.0

## Properties

### lat

• **lat**: `number`

___

### lng

• **lng**: `number`

## Methods

### clone

▸ **clone**(): [`LatLng`](base.LatLng.md)

#### Returns

[`LatLng`](base.LatLng.md)

___

### equals

▸ **equals**(`other`): `boolean`

判断经纬度坐标点是否相等，坐标值差小于1e-8

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `other` | [`LatLng`](base.LatLng.md) | 待比较的坐标 |

#### Returns

`boolean`

boolean

___

### toString

▸ **toString**(): `string`

字符串描述对象数据

#### Returns

`string`

string
