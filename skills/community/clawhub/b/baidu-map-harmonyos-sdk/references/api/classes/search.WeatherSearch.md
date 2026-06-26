[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / WeatherSearch

# Class: WeatherSearch

[search](../modules/search.md).WeatherSearch

## Table of contents

### Methods

- [newInstance](search.WeatherSearch.md#newinstance)
- [request](search.WeatherSearch.md#request)
- [destroy](search.WeatherSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`WeatherSearch`](search.WeatherSearch.md)

创建天气检索实例

#### Returns

[`WeatherSearch`](search.WeatherSearch.md)

___

### request

▸ **request**(`option`): `Promise`\<[`WeatherResult`](../interfaces/search.WeatherResult.md)\>

发起天气请求

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `option` | [`WeatherSearchOption`](../interfaces/search.WeatherSearchOption.md) | 天气请求参数 |

#### Returns

`Promise`\<[`WeatherResult`](../interfaces/search.WeatherResult.md)\>

___

### destroy

▸ **destroy**(): `void`

销毁WeatherSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
