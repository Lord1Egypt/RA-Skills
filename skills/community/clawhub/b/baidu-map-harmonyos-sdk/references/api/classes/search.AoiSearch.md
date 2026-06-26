[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / AoiSearch

# Class: AoiSearch

[search](../modules/search.md).AoiSearch

Aoi检索

## Table of contents

### Methods

- [newInstance](search.AoiSearch.md#newinstance)
- [requestAoi](search.AoiSearch.md#requestaoi)
- [destroy](search.AoiSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`AoiSearch`](search.AoiSearch.md)

获取检索Aoi对象

#### Returns

[`AoiSearch`](search.AoiSearch.md)

Aoi检索对象

___

### requestAoi

▸ **requestAoi**(`option`): `Promise`\<[`AoiResult`](../interfaces/search.AoiResult.md)\>

发起Aoi检索请求

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`AoiSearchOption`](../interfaces/search.AoiSearchOption.md) | 建筑检索参数，经纬度不能为null |

#### Returns

`Promise`\<[`AoiResult`](../interfaces/search.AoiResult.md)\>

异步aoi检索结果

___

### destroy

▸ **destroy**(): `void`

销毁AoiSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
