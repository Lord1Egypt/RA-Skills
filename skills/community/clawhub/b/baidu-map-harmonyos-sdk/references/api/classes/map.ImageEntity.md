[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ImageEntity

# Class: ImageEntity

[map](../modules/map.md).ImageEntity

图像资源类

**`Abstract`**

提供地图覆盖物需要的图像资源

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Table of contents

### Constructors

- [constructor](map.ImageEntity.md#constructor)

### Properties

- [imageSource](map.ImageEntity.md#imagesource)

### Accessors

- [src](map.ImageEntity.md#src)
- [width](map.ImageEntity.md#width)
- [height](map.ImageEntity.md#height)

### Methods

- [getPixesArrayBufferSync](map.ImageEntity.md#getpixesarraybuffersync)
- [getPixesMapSync](map.ImageEntity.md#getpixesmapsync)
- [getPixesMap](map.ImageEntity.md#getpixesmap)
- [getArrayBufferSync](map.ImageEntity.md#getarraybuffersync)
- [getArrayBuffer](map.ImageEntity.md#getarraybuffer)
- [getBitmap](map.ImageEntity.md#getbitmap)
- [toString](map.ImageEntity.md#tostring)
- [destroy](map.ImageEntity.md#destroy)

## Constructors

### constructor

• **new ImageEntity**(`source`, `width?`, `height?`, `options?`): [`ImageEntity`](map.ImageEntity.md)

构造函数，示例如下：
```typescript
// 网络图像数据源
const image_net:ImageEntity = new ImageEntity('https://webmap0.bdimg.com/wolfman/static/common/images/new/newlogo-new_3c175be.png');
// rawfile图像数据源
const image_rawfile:ImageEntity = new ImageEntity('rawfile://custom_logo.png');
// PixelMap图像像素类,可以通过OffscreenCanvas获取
private settings: RenderingContextSettings = new RenderingContextSettings(true)
let offContext = this.offCanvas.getContext("2d", this.settings);
/**** 省略画布图像操作 ****/
let pixelmap = offContext.getPixelMap(150, 150, 130, 130);
const image_pixelmap:ImageEntity = new ImageEntity(pixelmap, vp2px(130), vp2px(130));
```

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `source` | [`ImageSourceType`](../modules/map.md#imagesourcetype) | 图像来源 必填 |
| `width?` | `number` \| [`ImageOpt`](../interfaces/map.ImageOpt.md) | 图像宽度 选填 |
| `height?` | `number` | 图像高度 选填 |
| `options?` | [`ImageOpt`](../interfaces/map.ImageOpt.md) | 图像操作 选填 |

#### Returns

[`ImageEntity`](map.ImageEntity.md)

**`Since`**

1.0.0

## Properties

### imageSource

• **imageSource**: [`Maybe`](../modules/map.md#maybe)\<`ArrayBuffer`\>

图像数据

**`Since`**

1.1.0

## Accessors

### src

• `get` **src**(): [`ImageSourceType`](../modules/map.md#imagesourcetype)

#### Returns

[`ImageSourceType`](../modules/map.md#imagesourcetype)

___

### width

• `get` **width**(): `number`

#### Returns

`number`

___

### height

• `get` **height**(): `number`

#### Returns

`number`

## Methods

### getPixesArrayBufferSync

▸ **getPixesArrayBufferSync**(): `Promise`\<`any`\>

PixesArrayBuffer获取（Sync版本）

#### Returns

`Promise`\<`any`\>

___

### getPixesMapSync

▸ **getPixesMapSync**(): `Promise`\<`any`\>

获取图像像素对象（Sync版本）

#### Returns

`Promise`\<`any`\>

Promise<image.PixelMap | void>

**`Since`**

1.0.0

___

### getPixesMap

▸ **getPixesMap**(`callback`): `void`

获取图像像素对象

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `callback` | `Callback`\<`PixelMap`\> | 回调函数，返回PixelMap |

#### Returns

`void`

**`Since`**

1.0.0

___

### getArrayBufferSync

▸ **getArrayBufferSync**(): `Promise`\<`void` \| `ArrayBuffer`\>

获取图像ArrayBuffer数据（Sync版本）

#### Returns

`Promise`\<`void` \| `ArrayBuffer`\>

Promise<ArrayBuffer | void>

**`Since`**

1.1.0

___

### getArrayBuffer

▸ **getArrayBuffer**(`callback?`): `void`

获取图像像素对象，会生成内部缓存

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `callback?` | `Callback`\<`ArrayBuffer`\> | [可选]回调函数，返回ArrayBuffer |

#### Returns

`void`

**`Since`**

1.1.0

___

### getBitmap

▸ **getBitmap**(): [`Maybe`](../modules/map.md#maybe)\<`default`\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<`default`\>

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

**`Since`**

1.0.1

___

### destroy

▸ **destroy**(`deep?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `deep?` | `boolean` |

#### Returns

`void`
