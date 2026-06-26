[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / ShareUrlSearch

# Class: ShareUrlSearch

[search](../modules/search.md).ShareUrlSearch

## Table of contents

### Methods

- [newInstance](search.ShareUrlSearch.md#newinstance)
- [requestPoiDetailShareUrl](search.ShareUrlSearch.md#requestpoidetailshareurl)
- [requestLocationShareUrl](search.ShareUrlSearch.md#requestlocationshareurl)
- [requestRouteShareUrl](search.ShareUrlSearch.md#requestrouteshareurl)
- [destroy](search.ShareUrlSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`ShareUrlSearch`](search.ShareUrlSearch.md)

#### Returns

[`ShareUrlSearch`](search.ShareUrlSearch.md)

___

### requestPoiDetailShareUrl

▸ **requestPoiDetailShareUrl**(`option`): `Promise`\<[`ShareUrlResult`](../interfaces/search.ShareUrlResult.md)\>

请求poi详情分享URL

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`PoiDetailShareURLOption`](../interfaces/search.PoiDetailShareURLOption.md) |

#### Returns

`Promise`\<[`ShareUrlResult`](../interfaces/search.ShareUrlResult.md)\>

___

### requestLocationShareUrl

▸ **requestLocationShareUrl**(`option`): `Promise`\<[`ShareUrlResult`](../interfaces/search.ShareUrlResult.md)\>

请求位置信息分享URL

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`LocationShareURLOption`](../interfaces/search.LocationShareURLOption.md) |

#### Returns

`Promise`\<[`ShareUrlResult`](../interfaces/search.ShareUrlResult.md)\>

___

### requestRouteShareUrl

▸ **requestRouteShareUrl**(`option`): `Promise`\<[`ShareUrlResult`](../interfaces/search.ShareUrlResult.md)\>

路线规划短串分享

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`RouteShareURLOption`](../interfaces/search.RouteShareURLOption.md) |

#### Returns

`Promise`\<[`ShareUrlResult`](../interfaces/search.ShareUrlResult.md)\>

___

### destroy

▸ **destroy**(): `void`

销毁ShareUrlSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
