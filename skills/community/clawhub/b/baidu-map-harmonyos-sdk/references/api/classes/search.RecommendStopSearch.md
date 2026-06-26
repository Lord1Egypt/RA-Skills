[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / RecommendStopSearch

# Class: RecommendStopSearch

[search](../modules/search.md).RecommendStopSearch

## Table of contents

### Methods

- [newInstance](search.RecommendStopSearch.md#newinstance)
- [requestRecommendStop](search.RecommendStopSearch.md#requestrecommendstop)
- [destroy](search.RecommendStopSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`RecommendStopSearch`](search.RecommendStopSearch.md)

新建推荐上车点检索对象

#### Returns

[`RecommendStopSearch`](search.RecommendStopSearch.md)

推荐上车点检索对象

___

### requestRecommendStop

▸ **requestRecommendStop**(`option`): `Promise`\<[`RecommendStopResult`](../interfaces/search.RecommendStopResult.md)\>

发起推荐上车点检索请求

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`RecommendStopSearchOption`](../interfaces/search.RecommendStopSearchOption.md) | 请求参数。 请求参数的位置经纬度信息不能为空 |

#### Returns

`Promise`\<[`RecommendStopResult`](../interfaces/search.RecommendStopResult.md)\>

成功发起检索返回true , 失败返回false

___

### destroy

▸ **destroy**(): `void`

销毁RecommendStopSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
