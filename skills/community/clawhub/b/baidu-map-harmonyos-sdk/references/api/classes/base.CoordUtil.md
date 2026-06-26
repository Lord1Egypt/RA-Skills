[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / CoordUtil

# Class: CoordUtil

[base](../modules/base.md).CoordUtil

坐标系工具

## Table of contents

### Constructors

- [constructor](base.CoordUtil.md#constructor)

### Methods

- [decodeLocation](base.CoordUtil.md#decodelocation)
- [ll2point](base.CoordUtil.md#ll2point)
- [point2ll](base.CoordUtil.md#point2ll)
- [decodeLocationList2D](base.CoordUtil.md#decodelocationlist2d)
- [getDistanceByLL](base.CoordUtil.md#getdistancebyll)
- [getMCDistanceByOneLatLngAndRadius](base.CoordUtil.md#getmcdistancebyonelatlngandradius)

## Constructors

### constructor

• **new CoordUtil**(): [`CoordUtil`](base.CoordUtil.md)

#### Returns

[`CoordUtil`](base.CoordUtil.md)

## Methods

### decodeLocation

▸ **decodeLocation**(`geo`): ``null`` \| [`LatLng`](base.LatLng.md)

解密经纬度坐标

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `geo` | `string` | 加密的经纬度 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

BD09MC 坐标

___

### ll2point

▸ **ll2point**(`latLng`): [`Point`](base.Point.md)

经纬度坐标转百度墨卡托坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) |

#### Returns

[`Point`](base.Point.md)

___

### point2ll

▸ **point2ll**(`point`): [`LatLng`](base.LatLng.md)

百度墨卡托坐标转经纬度坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `point` | [`Point`](base.Point.md) |

#### Returns

[`LatLng`](base.LatLng.md)

___

### decodeLocationList2D

▸ **decodeLocationList2D**(`strGeoList`): ``null`` \| [`LatLng`](base.LatLng.md)[][]

解析加密geo为二维LatLng数组

#### Parameters

| Name | Type |
| :------ | :------ |
| `strGeoList` | `string` |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)[][]

___

### getDistanceByLL

▸ **getDistanceByLL**(`p1`, `p2`): `number`

两个经纬度点之间的距离

#### Parameters

| Name | Type |
| :------ | :------ |
| `p1` | ``null`` \| [`LatLng`](base.LatLng.md) |
| `p2` | ``null`` \| [`LatLng`](base.LatLng.md) |

#### Returns

`number`

-1: error

___

### getMCDistanceByOneLatLngAndRadius

▸ **getMCDistanceByOneLatLngAndRadius**(`p1`, `radius`): `number`

根据半径和已知经纬度估算墨卡托坐标下的半径

#### Parameters

| Name | Type |
| :------ | :------ |
| `p1` | [`LatLng`](base.LatLng.md) |
| `radius` | `number` |

#### Returns

`number`
