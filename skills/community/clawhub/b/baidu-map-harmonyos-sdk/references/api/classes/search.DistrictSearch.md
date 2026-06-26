[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / DistrictSearch

# Class: DistrictSearch

[search](../modules/search.md).DistrictSearch

行政区域检索接口

## Table of contents

### Methods

- [newInstance](search.DistrictSearch.md#newinstance)
- [searchDistrict](search.DistrictSearch.md#searchdistrict)
- [destroy](search.DistrictSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`DistrictSearch`](search.DistrictSearch.md)

获取行政区域检索对象

#### Returns

[`DistrictSearch`](search.DistrictSearch.md)

___

### searchDistrict

▸ **searchDistrict**(`option`): `Promise`\<[`DistrictResult`](../interfaces/search.DistrictResult.md)\>

行政区域检索入口

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`DistrictSearchOption`](../interfaces/search.DistrictSearchOption.md) | 行政区域检索参数 |

#### Returns

`Promise`\<[`DistrictResult`](../interfaces/search.DistrictResult.md)\>

行政区域信息查询结果

___

### destroy

▸ **destroy**(): `void`

销毁DistrictSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
