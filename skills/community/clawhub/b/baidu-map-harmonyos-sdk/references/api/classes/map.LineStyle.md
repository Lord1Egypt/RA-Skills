[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / LineStyle

# Class: LineStyle

[map](../modules/map.md).LineStyle

## Table of contents

### Constructors

- [constructor](map.LineStyle.md#constructor)

### Properties

- [bmLineStyle](map.LineStyle.md#bmlinestyle)
- [color](map.LineStyle.md#color)
- [width](map.LineStyle.md#width)
- [strokeWidth](map.LineStyle.md#strokewidth)
- [strokeColor](map.LineStyle.md#strokecolor)
- [textureOption](map.LineStyle.md#textureoption)

### Methods

- [setColor](map.LineStyle.md#setcolor)
- [setStrokeColor](map.LineStyle.md#setstrokecolor)
- [setWidth](map.LineStyle.md#setwidth)
- [setStrokeWidth](map.LineStyle.md#setstrokewidth)
- [setBitmapResource](map.LineStyle.md#setbitmapresource)
- [setTextureOption](map.LineStyle.md#settextureoption)
- [setLineResourceId](map.LineStyle.md#setlineresourceid)

## Constructors

### constructor

• **new LineStyle**(): [`LineStyle`](map.LineStyle.md)

#### Returns

[`LineStyle`](map.LineStyle.md)

## Properties

### bmLineStyle

• **bmLineStyle**: `default`

___

### color

• **color**: [`ColorString`](../modules/map.md#colorstring) = `Color.Black`

___

### width

• **width**: `number` = `1`

___

### strokeWidth

• **strokeWidth**: `number` = `1`

___

### strokeColor

• **strokeColor**: [`ColorString`](../modules/map.md#colorstring) = `Color.White`

___

### textureOption

• **textureOption**: `number` = `TextureOption.REPEAT`

## Methods

### setColor

▸ **setColor**(`argb`): `void`

设置线段纹理的颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `argb` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

___

### setStrokeColor

▸ **setStrokeColor**(`argb`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `argb` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

___

### setWidth

▸ **setWidth**(`width`): `void`

设置线段的宽度

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

___

### setStrokeWidth

▸ **setStrokeWidth**(`width`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

___

### setBitmapResource

▸ **setBitmapResource**(`bitmapDescriptor`): `Promise`\<`void`\>

设置线段纹理资源

#### Parameters

| Name | Type |
| :------ | :------ |
| `bitmapDescriptor` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`Promise`\<`void`\>

___

### setTextureOption

▸ **setTextureOption**(`option`): `void`

设置线段纹理类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`TextureOption`](../enums/map.SysEnum.TextureOption.md) |

#### Returns

`void`

___

### setLineResourceId

▸ **setLineResourceId**(`id`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `id` | `number` |

#### Returns

`void`
