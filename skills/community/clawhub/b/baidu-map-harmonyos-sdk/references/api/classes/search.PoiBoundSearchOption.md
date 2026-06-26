[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiBoundSearchOption

# Class: PoiBoundSearchOption

[search](../modules/search.md).PoiBoundSearchOption

poi城市内检索参数

## Table of contents

### Constructors

- [constructor](search.PoiBoundSearchOption.md#constructor)

### Accessors

- [bound](search.PoiBoundSearchOption.md#bound)
- [isExtendAdcode](search.PoiBoundSearchOption.md#isextendadcode)
- [keyword](search.PoiBoundSearchOption.md#keyword)
- [pageNum](search.PoiBoundSearchOption.md#pagenum)
- [pageCapacity](search.PoiBoundSearchOption.md#pagecapacity)
- [tag](search.PoiBoundSearchOption.md#tag)
- [scope](search.PoiBoundSearchOption.md#scope)
- [poiFilter](search.PoiBoundSearchOption.md#poifilter)
- [mPoiFilter](search.PoiBoundSearchOption.md#mpoifilter)
- [languageType](search.PoiBoundSearchOption.md#languagetype)
- [isShowPhotos](search.PoiBoundSearchOption.md#isshowphotos)

## Constructors

### constructor

• **new PoiBoundSearchOption**(`params`): [`PoiBoundSearchOption`](search.PoiBoundSearchOption.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `params` | [`PoiBoundSearchOptionParams`](../interfaces/search.PoiBoundSearchOptionParams.md) |

#### Returns

[`PoiBoundSearchOption`](search.PoiBoundSearchOption.md)

## Accessors

### bound

• `get` **bound**(): [`LatLngBounds`](base.LatLngBounds.md)

#### Returns

[`LatLngBounds`](base.LatLngBounds.md)

• `set` **bound**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | [`LatLngBounds`](base.LatLngBounds.md) |

#### Returns

`void`

___

### isExtendAdcode

• `get` **isExtendAdcode**(): `boolean`

#### Returns

`boolean`

• `set` **isExtendAdcode**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `boolean` |

#### Returns

`void`

___

### keyword

• `get` **keyword**(): `string`

#### Returns

`string`

• `set` **keyword**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `string` |

#### Returns

`void`

___

### pageNum

• `get` **pageNum**(): `number`

#### Returns

`number`

• `set` **pageNum**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `number` |

#### Returns

`void`

___

### pageCapacity

• `get` **pageCapacity**(): `number`

#### Returns

`number`

• `set` **pageCapacity**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `number` |

#### Returns

`void`

___

### tag

• `get` **tag**(): ``null`` \| `string`

#### Returns

``null`` \| `string`

• `set` **tag**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | ``null`` \| `string` |

#### Returns

`void`

___

### scope

• `get` **scope**(): `number`

#### Returns

`number`

• `set` **scope**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `number` |

#### Returns

`void`

___

### poiFilter

• `set` **poiFilter**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | ``null`` \| [`PoiFilter`](search.PoiFilter.md) |

#### Returns

`void`

___

### mPoiFilter

• `get` **mPoiFilter**(): ``null`` \| [`PoiFilter`](search.PoiFilter.md)

#### Returns

``null`` \| [`PoiFilter`](search.PoiFilter.md)

___

### languageType

• `get` **languageType**(): `LanguageType`

#### Returns

`LanguageType`

• `set` **languageType**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `LanguageType` |

#### Returns

`void`

___

### isShowPhotos

• `get` **isShowPhotos**(): `boolean`

#### Returns

`boolean`

• `set` **isShowPhotos**(`value`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `boolean` |

#### Returns

`void`
