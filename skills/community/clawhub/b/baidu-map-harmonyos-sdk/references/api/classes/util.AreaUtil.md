[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [util](../modules/util.md) / AreaUtil

# Class: AreaUtil

[util](../modules/util.md).AreaUtil

/**
* 面积工具

## Table of contents

### Constructors

- [constructor](util.AreaUtil.md#constructor)

### Methods

- [calculateArea](util.AreaUtil.md#calculatearea)
- [calculateAreaByList](util.AreaUtil.md#calculateareabylist)

## Constructors

### constructor

• **new AreaUtil**(): [`AreaUtil`](util.AreaUtil.md)

#### Returns

[`AreaUtil`](util.AreaUtil.md)

## Methods

### calculateArea

▸ **calculateArea**(`northeast`, `southwest`): `number`

计算地图上矩形区域的面积，单位平方米

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `northeast` | [`LatLng`](base.LatLng.md) | northeast - 矩形区域东北角点坐标 |
| `southwest` | [`LatLng`](base.LatLng.md) | southwest - 矩形区域西南角点坐标 |

#### Returns

`number`

返回地图上矩形区域的面积，单位平方米

___

### calculateAreaByList

▸ **calculateAreaByList**(`latLngs`): `number`

计算地图上任意的多边形面积。
该计算是将地球视为标准球体(R = 6378137.0)得到的面积,与实际地理面积存在一定的误差

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `latLngs` | [`LatLng`](base.LatLng.md)[] | 构成多边形的顶点坐标 |

#### Returns

`number`

多边形面积，单位：平方米
