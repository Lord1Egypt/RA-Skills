[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / SpatialRelationUtil

# Class: SpatialRelationUtil

[util](../modules/util.md).SpatialRelationUtil

判断空间关系工具

## Table of contents

### Constructors

- [constructor](util.SpatialRelationUtil.md#constructor)

### Methods

- [isPolygonContainsPoint](util.SpatialRelationUtil.md#ispolygoncontainspoint)
- [isCircleContainsPoint](util.SpatialRelationUtil.md#iscirclecontainspoint)
- [getNearestPointFromLine](util.SpatialRelationUtil.md#getnearestpointfromline)
- [getNearestDistancePointFromLine](util.SpatialRelationUtil.md#getnearestdistancepointfromline)
- [calShortestDistancePoint](util.SpatialRelationUtil.md#calshortestdistancepoint)

## Constructors

### constructor

• **new SpatialRelationUtil**(): [`SpatialRelationUtil`](util.SpatialRelationUtil.md)

#### Returns

[`SpatialRelationUtil`](util.SpatialRelationUtil.md)

## Methods

### isPolygonContainsPoint

▸ **isPolygonContainsPoint**(`mPoints`, `point`): `boolean`

返回一个点是否在一个多边形区域内

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `mPoints` | ``null`` \| [`LatLng`](base.LatLng.md)[] | 多边形坐标点列表 |
| `point` | [`LatLng`](base.LatLng.md) | 待判断点 |

#### Returns

`boolean`

True 多边形包含这个点,false 多边形未包含这个点。

___

### isCircleContainsPoint

▸ **isCircleContainsPoint**(`center`, `radius`, `point`): `boolean`

判断圆形是否包含传入的经纬度点

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `center` | [`LatLng`](base.LatLng.md) | 构成圆的中心点 |
| `radius` | `number` | 圆的半径 |
| `point` | [`LatLng`](base.LatLng.md) | 待判断点 |

#### Returns

`boolean`

true 包含，false 为不包含

___

### getNearestPointFromLine

▸ **getNearestPointFromLine**(`mPoints`, `point`): ``null`` \| [`LatLng`](base.LatLng.md)

返回某点距离线上最近的折点

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `mPoints` | [`LatLng`](base.LatLng.md)[] | 折线折点 |
| `point` | [`LatLng`](base.LatLng.md) | 待判断点 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

某点到线上最近的折点

___

### getNearestDistancePointFromLine

▸ **getNearestDistancePointFromLine**(`mPoints`, `point`): ``null`` \| [`LatLng`](base.LatLng.md)

返回某点距线上最近的点

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `mPoints` | [`LatLng`](base.LatLng.md)[] | 折线折点 |
| `point` | [`LatLng`](base.LatLng.md) | 待判断点 |

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)

某点到线上最近的点

___

### calShortestDistancePoint

▸ **calShortestDistancePoint**(`pointList`, `point`): ``null`` \| [`Point`](base.Point.md)

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `pointList` | [`Point`](base.Point.md)[] | 折线折点 |
| `point` | [`Point`](base.Point.md) | 待判断点 |

#### Returns

``null`` \| [`Point`](base.Point.md)

返回垂点距线上最近的点
