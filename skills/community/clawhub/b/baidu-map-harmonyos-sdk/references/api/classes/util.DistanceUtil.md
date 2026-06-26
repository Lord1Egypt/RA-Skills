[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / DistanceUtil

# Class: DistanceUtil

[util](../modules/util.md).DistanceUtil

测距工具

## Table of contents

### Constructors

- [constructor](util.DistanceUtil.md#constructor)

### Methods

- [getDistance](util.DistanceUtil.md#getdistance)
- [getDistanceByPath](util.DistanceUtil.md#getdistancebypath)

## Constructors

### constructor

• **new DistanceUtil**(): [`DistanceUtil`](util.DistanceUtil.md)

#### Returns

[`DistanceUtil`](util.DistanceUtil.md)

## Methods

### getDistance

▸ **getDistance**(`p1ll`, `p2ll`): `number`

返回两个点之间的距离

#### Parameters

| Name | Type |
| :------ | :------ |
| `p1ll` | [`LatLng`](base.LatLng.md) |
| `p2ll` | [`LatLng`](base.LatLng.md) |

#### Returns

`number`

两点距离，单位为： 米,转换错误时返回-1.

___

### getDistanceByPath

▸ **getDistanceByPath**(`ll`): `number`

返回序列点间的距离之和

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `ll` | [`LatLng`](base.LatLng.md)[] | {Array<LatLng>} 序列坐标点 |

#### Returns

`number`
