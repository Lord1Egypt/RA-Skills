[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / MultiRouteDisplayOption

# Class: MultiRouteDisplayOption

[walkridecommon](../modules/walkridecommon.md).MultiRouteDisplayOption

多路线显示配置
多条路线的分类: 第 1 条路线为焦点路线, 其他的为非焦点路线
路线绘画优先级: 纹理图片 > 线路颜色 > 默认颜色
焦点路线默认颜色: 0xFF49A6FF
非焦点路线默认颜色: 0xFF3b69d3

## Table of contents

### Constructors

- [constructor](walkridecommon.MultiRouteDisplayOption.md#constructor)

### Accessors

- [focusRouteBitmapDescriptor](walkridecommon.MultiRouteDisplayOption.md#focusroutebitmapdescriptor)
- [noFocusRouteBitmapDescriptor](walkridecommon.MultiRouteDisplayOption.md#nofocusroutebitmapdescriptor)
- [focusRouteWidth](walkridecommon.MultiRouteDisplayOption.md#focusroutewidth)
- [noFocusRouteWidth](walkridecommon.MultiRouteDisplayOption.md#nofocusroutewidth)
- [focusColor](walkridecommon.MultiRouteDisplayOption.md#focuscolor)
- [noFocusColor](walkridecommon.MultiRouteDisplayOption.md#nofocuscolor)

### Methods

- [withFocusRouteBitmapDescriptor](walkridecommon.MultiRouteDisplayOption.md#withfocusroutebitmapdescriptor)
- [withNoFocusRouteBitmapDescriptor](walkridecommon.MultiRouteDisplayOption.md#withnofocusroutebitmapdescriptor)
- [withFocusRouteWidth](walkridecommon.MultiRouteDisplayOption.md#withfocusroutewidth)
- [withNoFocusRouteWidth](walkridecommon.MultiRouteDisplayOption.md#withnofocusroutewidth)
- [withFocusColor](walkridecommon.MultiRouteDisplayOption.md#withfocuscolor)
- [withNoFocusColor](walkridecommon.MultiRouteDisplayOption.md#withnofocuscolor)

## Constructors

### constructor

• **new MultiRouteDisplayOption**(): [`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

#### Returns

[`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

## Accessors

### focusRouteBitmapDescriptor

• `get` **focusRouteBitmapDescriptor**(): ``null`` \| [`ImageEntity`](map.ImageEntity.md)

#### Returns

``null`` \| [`ImageEntity`](map.ImageEntity.md)

• `set` **focusRouteBitmapDescriptor**(`descriptor`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `descriptor` | ``null`` \| [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`void`

___

### noFocusRouteBitmapDescriptor

• `get` **noFocusRouteBitmapDescriptor**(): ``null`` \| [`ImageEntity`](map.ImageEntity.md)

#### Returns

``null`` \| [`ImageEntity`](map.ImageEntity.md)

• `set` **noFocusRouteBitmapDescriptor**(`descriptor`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `descriptor` | ``null`` \| [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`void`

___

### focusRouteWidth

• `get` **focusRouteWidth**(): `number`

#### Returns

`number`

• `set` **focusRouteWidth**(`width`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

___

### noFocusRouteWidth

• `get` **noFocusRouteWidth**(): `number`

#### Returns

`number`

• `set` **noFocusRouteWidth**(`width`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

___

### focusColor

• `get` **focusColor**(): `number`

#### Returns

`number`

• `set` **focusColor**(`color`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | `number` |

#### Returns

`void`

___

### noFocusColor

• `get` **noFocusColor**(): `number`

#### Returns

`number`

• `set` **noFocusColor**(`color`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | `number` |

#### Returns

`void`

## Methods

### withFocusRouteBitmapDescriptor

▸ **withFocusRouteBitmapDescriptor**(`descriptor`): [`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `descriptor` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

[`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

___

### withNoFocusRouteBitmapDescriptor

▸ **withNoFocusRouteBitmapDescriptor**(`descriptor`): [`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `descriptor` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

[`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

___

### withFocusRouteWidth

▸ **withFocusRouteWidth**(`width`): [`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

[`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

___

### withNoFocusRouteWidth

▸ **withNoFocusRouteWidth**(`width`): [`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

[`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

___

### withFocusColor

▸ **withFocusColor**(`color`): [`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | `number` |

#### Returns

[`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

___

### withNoFocusColor

▸ **withNoFocusColor**(`color`): [`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | `number` |

#### Returns

[`MultiRouteDisplayOption`](walkridecommon.MultiRouteDisplayOption.md)
