[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / FavoriteManager

# Class: FavoriteManager

[map](../modules/map.md).FavoriteManager

## Table of contents

### Methods

- [getInstance](map.FavoriteManager.md#getinstance)
- [add](map.FavoriteManager.md#add)
- [getFavPoi](map.FavoriteManager.md#getfavpoi)
- [getAllFavPois](map.FavoriteManager.md#getallfavpois)
- [deleteFavPoi](map.FavoriteManager.md#deletefavpoi)
- [clearAllFavPois](map.FavoriteManager.md#clearallfavpois)
- [updateFavPoi](map.FavoriteManager.md#updatefavpoi)
- [destroy](map.FavoriteManager.md#destroy)

## Methods

### getInstance

▸ **getInstance**(): [`FavoriteManager`](map.FavoriteManager.md)

#### Returns

[`FavoriteManager`](map.FavoriteManager.md)

___

### add

▸ **add**(`poiInfo`): `number`

添加收藏点

#### Parameters

| Name | Type |
| :------ | :------ |
| `poiInfo` | [`FavoritePoiInfo`](../interfaces/map.FavoritePoiInfo.md) |

#### Returns

`number`

success: 1; duplicate/name_empty: -1; full: -2;

___

### getFavPoi

▸ **getFavPoi**(`id`): ``null`` \| [`FavoritePoiInfo`](../interfaces/map.FavoritePoiInfo.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `id` | `string` |

#### Returns

``null`` \| [`FavoritePoiInfo`](../interfaces/map.FavoritePoiInfo.md)

___

### getAllFavPois

▸ **getAllFavPois**(): ``null`` \| [`FavoritePoiInfo`](../interfaces/map.FavoritePoiInfo.md)[]

#### Returns

``null`` \| [`FavoritePoiInfo`](../interfaces/map.FavoritePoiInfo.md)[]

___

### deleteFavPoi

▸ **deleteFavPoi**(`id`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `id` | `string` |

#### Returns

`boolean`

___

### clearAllFavPois

▸ **clearAllFavPois**(): `boolean`

#### Returns

`boolean`

___

### updateFavPoi

▸ **updateFavPoi**(`id`, `info`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `id` | `string` |
| `info` | [`FavoritePoiInfo`](../interfaces/map.FavoritePoiInfo.md) |

#### Returns

`boolean`

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`
