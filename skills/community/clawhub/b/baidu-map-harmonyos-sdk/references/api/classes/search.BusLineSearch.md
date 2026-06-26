[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BusLineSearch

# Class: BusLineSearch

[search](../modules/search.md).BusLineSearch

## Table of contents

### Methods

- [newInstance](search.BusLineSearch.md#newinstance)
- [searchBusLine](search.BusLineSearch.md#searchbusline)
- [destroy](search.BusLineSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`BusLineSearch`](search.BusLineSearch.md)

获取一个新的检索实例

#### Returns

[`BusLineSearch`](search.BusLineSearch.md)

检索实例

___

### searchBusLine

▸ **searchBusLine**(`option`): `Promise`\<[`BusLineResult`](../interfaces/search.BusLineResult.md)\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`BusLineSearchOption`](../interfaces/search.BusLineSearchOption.md) |

#### Returns

`Promise`\<[`BusLineResult`](../interfaces/search.BusLineResult.md)\>

___

### destroy

▸ **destroy**(): `void`

销毁BusLineSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
