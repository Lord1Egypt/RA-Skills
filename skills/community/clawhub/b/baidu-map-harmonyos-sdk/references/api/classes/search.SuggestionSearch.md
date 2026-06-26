[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / SuggestionSearch

# Class: SuggestionSearch

[search](../modules/search.md).SuggestionSearch

sug检索

## Table of contents

### Methods

- [newInstance](search.SuggestionSearch.md#newinstance)
- [requestSuggestion](search.SuggestionSearch.md#requestsuggestion)
- [destroy](search.SuggestionSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`SuggestionSearch`](search.SuggestionSearch.md)

#### Returns

[`SuggestionSearch`](search.SuggestionSearch.md)

___

### requestSuggestion

▸ **requestSuggestion**(`option`): `Promise`\<[`SuggestionResult`](../interfaces/search.SuggestionResult.md)\>

sug检索

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`SuggestionSearchOption`](../interfaces/search.SuggestionSearchOption.md) | 请求参数 |

#### Returns

`Promise`\<[`SuggestionResult`](../interfaces/search.SuggestionResult.md)\>

异步返回检索结果 SuggestionResult

___

### destroy

▸ **destroy**(): `void`

销毁SuggestionSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
