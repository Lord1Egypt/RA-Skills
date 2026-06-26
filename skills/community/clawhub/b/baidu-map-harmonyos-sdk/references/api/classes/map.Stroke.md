[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Stroke

# Class: Stroke

[map](../modules/map.md).Stroke

描边样式类

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Table of contents

### Constructors

- [constructor](map.Stroke.md#constructor)

### Accessors

- [strokeWidth](map.Stroke.md#strokewidth)
- [color](map.Stroke.md#color)
- [strokeStyle](map.Stroke.md#strokestyle)
- [strokeTexture](map.Stroke.md#stroketexture)
- [textureOption](map.Stroke.md#textureoption)

### Methods

- [getStrokeWidth](map.Stroke.md#getstrokewidth)
- [setStrokeWidth](map.Stroke.md#setstrokewidth)
- [getColor](map.Stroke.md#getcolor)
- [setColor](map.Stroke.md#setcolor)
- [getStrokeStyle](map.Stroke.md#getstrokestyle)
- [setStrokeStyle](map.Stroke.md#setstrokestyle)
- [setStrokeTexture](map.Stroke.md#setstroketexture)
- [setTextureOption](map.Stroke.md#settextureoption)
- [getTextureOption](map.Stroke.md#gettextureoption)
- [toString](map.Stroke.md#tostring)

## Constructors

### constructor

• **new Stroke**(`opts`): [`Stroke`](map.Stroke.md)

构造函数，默认参数如下
``` Typescript
{
 color: '#e91e63',
 strokeWidth: 16,
 strokeStyle: SysEnum.StrokeStyle.REAL
}
```

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`IStrokeOption`](../interfaces/map.IStrokeOption.md) |

#### Returns

[`Stroke`](map.Stroke.md)

**`Since`**

1.0.0

## Accessors

### strokeWidth

• `get` **strokeWidth**(): `number`

获取描边宽度，单位：像素

#### Returns

`number`

**`Since`**

1.0.0

• `set` **strokeWidth**(`stroke_width`): `void`

设置描边宽度，单位：像素

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke_width` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### color

• `get` **color**(): [`ColorString`](../modules/map.md#colorstring)

获取描边颜色

#### Returns

[`ColorString`](../modules/map.md#colorstring)

**`Since`**

1.0.0

• `set` **color**(`color`): `void`

设置描边颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.0.0

___

### strokeStyle

• `get` **strokeStyle**(): [`StrokeStyle`](../enums/map.SysEnum.StrokeStyle.md)

获取描边样式

#### Returns

[`StrokeStyle`](../enums/map.SysEnum.StrokeStyle.md)

**`Since`**

1.0.0

• `set` **strokeStyle**(`stroke_style`): `void`

设置描边样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke_style` | [`StrokeStyle`](../enums/map.SysEnum.StrokeStyle.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### strokeTexture

• `get` **strokeTexture**(): [`ImageEntity`](map.ImageEntity.md)

获取描边纹理

#### Returns

[`ImageEntity`](map.ImageEntity.md)

**`Since`**

1.2.0

• `set` **strokeTexture**(`stroke_texture`): `void`

设置描边纹理，与描边颜色进行叠加现实

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke_texture` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`void`

**`Since`**

1.2.0

___

### textureOption

• `get` **textureOption**(): [`TextureOption`](../enums/map.SysEnum.TextureOption.md)

获取描边纹理样式

#### Returns

[`TextureOption`](../enums/map.SysEnum.TextureOption.md)

**`Default`**

```ts
SysEnum.StrokeStyle.REAL
```

**`Since`**

1.2.0

• `set` **textureOption**(`texture_opt`): `void`

设置描边纹理样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `texture_opt` | [`TextureOption`](../enums/map.SysEnum.TextureOption.md) |

#### Returns

`void`

**`Default`**

```ts
SysEnum.StrokeStyle.REAL
```

**`Since`**

1.2.0

## Methods

### getStrokeWidth

▸ **getStrokeWidth**(): `number`

获取描边宽度，单位：像素

#### Returns

`number`

**`Since`**

1.0.0

___

### setStrokeWidth

▸ **setStrokeWidth**(`stroke_width`): [`Stroke`](map.Stroke.md)

设置描边宽度，单位：像素

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke_width` | `number` |

#### Returns

[`Stroke`](map.Stroke.md)

**`Since`**

1.0.0

___

### getColor

▸ **getColor**(): [`ColorString`](../modules/map.md#colorstring)

获取描边颜色

#### Returns

[`ColorString`](../modules/map.md#colorstring)

**`Since`**

1.0.0

___

### setColor

▸ **setColor**(`color`): [`Stroke`](map.Stroke.md)

设置描边颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Stroke`](map.Stroke.md)

**`Since`**

1.0.0

___

### getStrokeStyle

▸ **getStrokeStyle**(): [`StrokeStyle`](../enums/map.SysEnum.StrokeStyle.md)

获取描边样式

#### Returns

[`StrokeStyle`](../enums/map.SysEnum.StrokeStyle.md)

**`Since`**

1.0.0

___

### setStrokeStyle

▸ **setStrokeStyle**(`stroke_style`): [`Stroke`](map.Stroke.md)

设置描边样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke_style` | [`StrokeStyle`](../enums/map.SysEnum.StrokeStyle.md) |

#### Returns

[`Stroke`](map.Stroke.md)

**`Since`**

1.0.0

___

### setStrokeTexture

▸ **setStrokeTexture**(`stroke_texture`): [`Stroke`](map.Stroke.md)

设置描边纹理，与描边颜色进行叠加现实

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke_texture` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

[`Stroke`](map.Stroke.md)

**`Since`**

1.2.0

___

### setTextureOption

▸ **setTextureOption**(`texture_opt`): [`Stroke`](map.Stroke.md)

设置描边纹理样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `texture_opt` | [`TextureOption`](../enums/map.SysEnum.TextureOption.md) |

#### Returns

[`Stroke`](map.Stroke.md)

**`Default`**

```ts
SysEnum.StrokeStyle.REAL
```

**`Since`**

1.2.0

___

### getTextureOption

▸ **getTextureOption**(): [`TextureOption`](../enums/map.SysEnum.TextureOption.md)

获取描边纹理样式

#### Returns

[`TextureOption`](../enums/map.SysEnum.TextureOption.md)

**`Default`**

```ts
SysEnum.StrokeStyle.REAL
```

**`Since`**

1.2.0

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

**`Since`**

1.0.1
