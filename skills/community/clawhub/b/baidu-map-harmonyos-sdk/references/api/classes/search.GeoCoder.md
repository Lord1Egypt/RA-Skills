[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / GeoCoder

# Class: GeoCoder

[search](../modules/search.md).GeoCoder

## Table of contents

### Methods

- [newInstance](search.GeoCoder.md#newinstance)
- [geocode](search.GeoCoder.md#geocode)
- [reverseGeoCode](search.GeoCoder.md#reversegeocode)
- [destroy](search.GeoCoder.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`GeoCoder`](search.GeoCoder.md)

新建地理编码查询

#### Returns

[`GeoCoder`](search.GeoCoder.md)

地理编码查询对象

___

### geocode

▸ **geocode**(`option`): `Promise`\<[`GeoCodeResult`](../interfaces/search.GeoCodeResult.md)\>

发起地理编码(地址信息->经纬度)请求

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`GeoCodeOption`](search.GeoCodeOption.md) | 请求参数 请求参数的城市、地址不为空，否则抛出异常 |

#### Returns

`Promise`\<[`GeoCodeResult`](../interfaces/search.GeoCodeResult.md)\>

成功发起检索返回true , 失败返回false

**`Throws`**

Error

___

### reverseGeoCode

▸ **reverseGeoCode**(`option`): `Promise`\<[`ReverseGeoCodeResult`](../interfaces/search.ReverseGeoCodeResult.md)\>

发起反地理编码请求(经纬度->地址信息)

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`ReverseGeoCodeOption`](search.ReverseGeoCodeOption.md) | 请求参数,请求参数的坐标不为空，否则抛出异常 |

#### Returns

`Promise`\<[`ReverseGeoCodeResult`](../interfaces/search.ReverseGeoCodeResult.md)\>

成功发起检索返回true , 失败返回false

___

### destroy

▸ **destroy**(): `void`

销毁GeoCoder实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
