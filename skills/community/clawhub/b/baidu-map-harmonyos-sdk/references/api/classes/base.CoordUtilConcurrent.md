[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / CoordUtilConcurrent

# Class: CoordUtilConcurrent

[base](../modules/base.md).CoordUtilConcurrent

跨线程同步坐标工具类
用于在工作线程中执行坐标转换，不依赖主线程的 Initializer.coordType

## Table of contents

### Constructors

- [constructor](base.CoordUtilConcurrent.md#constructor)

### Methods

- [setCoordType](base.CoordUtilConcurrent.md#setcoordtype)
- [getCoordType](base.CoordUtilConcurrent.md#getcoordtype)
- [decodeLocation](base.CoordUtilConcurrent.md#decodelocation)
- [ll2point](base.CoordUtilConcurrent.md#ll2point)
- [point2ll](base.CoordUtilConcurrent.md#point2ll)
- [decodeLocationList2D](base.CoordUtilConcurrent.md#decodelocationlist2d)
- [getDistanceByLL](base.CoordUtilConcurrent.md#getdistancebyll)

## Constructors

### constructor

• **new CoordUtilConcurrent**(): [`CoordUtilConcurrent`](base.CoordUtilConcurrent.md)

#### Returns

[`CoordUtilConcurrent`](base.CoordUtilConcurrent.md)

## Methods

### setCoordType

▸ **setCoordType**(`coordType`): `void`

设置当前线程的坐标系类型
在工作线程使用坐标工具前必须先调用此方法设置坐标系类型

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `coordType` | `number` | 坐标系类型，默认为 BD09LL |

#### Returns

`void`

___

### getCoordType

▸ **getCoordType**(): `number`

获取当前线程的坐标系类型

#### Returns

`number`

当前坐标系类型

___

### decodeLocation

▸ **decodeLocation**(`geo`, `coordType?`): ``null`` \| [`LatLng`](base.LatLng.md)

解密经纬度坐标（并发版本）
不依赖主线程的 Initializer.coordType，使用线程本地变量或参数

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `geo` | `string` | 加密的经纬度 |
| `coordType?` | `number` | 可选，坐标系类型。如果传入则优先使用，否则使用线程本地变量 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

BD09LL 坐标

___

### ll2point

▸ **ll2point**(`latLng`, `coordType?`): [`Point`](base.Point.md)

经纬度坐标转百度墨卡托坐标（并发版本）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) | 经纬度坐标 |
| `coordType?` | `number` | 可选，坐标系类型。如果传入则优先使用，否则使用线程本地变量 |

#### Returns

[`Point`](base.Point.md)

百度墨卡托坐标

___

### point2ll

▸ **point2ll**(`point`, `coordType?`): [`LatLng`](base.LatLng.md)

百度墨卡托坐标转经纬度坐标（并发版本）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point` | [`Point`](base.Point.md) | 百度墨卡托坐标 |
| `coordType?` | `number` | 可选，坐标系类型。如果传入则优先使用，否则使用线程本地变量 |

#### Returns

[`LatLng`](base.LatLng.md)

经纬度坐标

___

### decodeLocationList2D

▸ **decodeLocationList2D**(`strGeoList`, `coordType?`): ``null`` \| [`LatLng`](base.LatLng.md)[][]

解析加密geo为二维LatLng数组（并发版本）
注意：此方法内部仍使用 Initializer.coordType，需要改造

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `strGeoList` | `string` | 加密的geo字符串列表 |
| `coordType?` | `number` | 可选，坐标系类型。如果传入则优先使用，否则使用线程本地变量 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)[][]

二维LatLng数组

___

### getDistanceByLL

▸ **getDistanceByLL**(`p1`, `p2`, `coordType?`): `number`

两个经纬度点之间的距离（并发版本）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `p1` | ``null`` \| [`LatLng`](base.LatLng.md) | 第一个点 |
| `p2` | ``null`` \| [`LatLng`](base.LatLng.md) | 第二个点 |
| `coordType?` | `number` | 可选，坐标系类型。如果传入则优先使用，否则使用线程本地变量 |

#### Returns

`number`

距离（米），-1 表示错误
