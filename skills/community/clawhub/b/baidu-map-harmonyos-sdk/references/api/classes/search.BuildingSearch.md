[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BuildingSearch

# Class: BuildingSearch

[search](../modules/search.md).BuildingSearch

建筑物检索

## Table of contents

### Methods

- [newInstance](search.BuildingSearch.md#newinstance)
- [requestBuilding](search.BuildingSearch.md#requestbuilding)
- [destroy](search.BuildingSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`BuildingSearch`](search.BuildingSearch.md)

获取检索建筑物对象

#### Returns

[`BuildingSearch`](search.BuildingSearch.md)

建筑物检索对象

___

### requestBuilding

▸ **requestBuilding**(`option`): `Promise`\<[`BuildingResult`](../interfaces/search.BuildingResult.md)\>

发起建筑物检索请求

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`BuildingSearchOption`](../interfaces/search.BuildingSearchOption.md) | 建筑检索参数，经纬度不能为null |

#### Returns

`Promise`\<[`BuildingResult`](../interfaces/search.BuildingResult.md)\>

异步结果

___

### destroy

▸ **destroy**(): `void`

销毁BuildingSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
