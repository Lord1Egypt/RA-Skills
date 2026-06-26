[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiSearch

# Class: PoiSearch

[search](../modules/search.md).PoiSearch

POI检索接口

## Table of contents

### Properties

- [DEFAULT\_PAGE\_CAPACITY](search.PoiSearch.md#default_page_capacity)

### Methods

- [newInstance](search.PoiSearch.md#newinstance)
- [searchInCity](search.PoiSearch.md#searchincity)
- [searchNearby](search.PoiSearch.md#searchnearby)
- [searchInBound](search.PoiSearch.md#searchinbound)
- [searchPoiDetail](search.PoiSearch.md#searchpoidetail)
- [searchPoiIndoor](search.PoiSearch.md#searchpoiindoor)
- [destroy](search.PoiSearch.md#destroy)

## Properties

### DEFAULT\_PAGE\_CAPACITY

▪ `Static` `Readonly` **DEFAULT\_PAGE\_CAPACITY**: `number` = `10`

## Methods

### newInstance

▸ **newInstance**(): [`PoiSearch`](search.PoiSearch.md)

创建PoiSearch实例

#### Returns

[`PoiSearch`](search.PoiSearch.md)

PoiSearch实例

___

### searchInCity

▸ **searchInCity**(`option`): `Promise`\<[`PoiResult`](../interfaces/search.PoiResult.md)\>

城市内检索

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`PoiCitySearchOption`](search.PoiCitySearchOption.md) | 请求参数 |

#### Returns

`Promise`\<[`PoiResult`](../interfaces/search.PoiResult.md)\>

成功发起检索返回true , 失败返回false

___

### searchNearby

▸ **searchNearby**(`option`): `Promise`\<[`PoiResult`](../interfaces/search.PoiResult.md)\>

周边检索

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`PoiNearbySearchOption`](search.PoiNearbySearchOption.md) |

#### Returns

`Promise`\<[`PoiResult`](../interfaces/search.PoiResult.md)\>

___

### searchInBound

▸ **searchInBound**(`option`): `Promise`\<[`PoiResult`](../interfaces/search.PoiResult.md)\>

范围内检索

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`PoiBoundSearchOption`](search.PoiBoundSearchOption.md) |

#### Returns

`Promise`\<[`PoiResult`](../interfaces/search.PoiResult.md)\>

___

### searchPoiDetail

▸ **searchPoiDetail**(`option`): `Promise`\<[`PoiDetailSearchResult`](../interfaces/search.PoiDetailSearchResult.md)\>

POI详情检索

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`PoiDetailSearchOption`](../interfaces/search.PoiDetailSearchOption.md) |

#### Returns

`Promise`\<[`PoiDetailSearchResult`](../interfaces/search.PoiDetailSearchResult.md)\>

___

### searchPoiIndoor

▸ **searchPoiIndoor**(`option`): `Promise`\<[`PoiIndoorResult`](../interfaces/search.PoiIndoorResult.md)\>

POI 室内检索

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`PoiIndoorOption`](../interfaces/search.PoiIndoorOption.md) |

#### Returns

`Promise`\<[`PoiIndoorResult`](../interfaces/search.PoiIndoorResult.md)\>

___

### destroy

▸ **destroy**(): `void`

销毁PoiSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
