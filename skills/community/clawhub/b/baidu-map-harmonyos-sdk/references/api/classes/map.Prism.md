[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Prism

# Class: Prism

[map](../modules/map.md).Prism

覆盖物基类

**`Abstract`**

提供覆盖物基础的操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`Prism`**

  ↳↳ [`Building`](map.Building.md)

## Table of contents

### Constructors

- [constructor](map.Prism.md#constructor)

### Properties

- [uuid](map.Prism.md#uuid)
- [type](map.Prism.md#type)
- [eventListener](map.Prism.md#eventlistener)
- [isDestroyed](map.Prism.md#isdestroyed)

### Accessors

- [typeName](map.Prism.md#typename)
- [visible](map.Prism.md#visible)
- [zIndex](map.Prism.md#zindex)

### Methods

- [putPointsInfoIntoBundle](map.Prism.md#putpointsinfointobundle)
- [addEventListener](map.Prism.md#addeventlistener)
- [removeEventListener](map.Prism.md#removeeventlistener)
- [addDragListener](map.Prism.md#adddraglistener)
- [removeDragListener](map.Prism.md#removedraglistener)
- [getDragListener](map.Prism.md#getdraglistener)
- [fireEvent](map.Prism.md#fireevent)
- [getType](map.Prism.md#gettype)
- [setAnimation](map.Prism.md#setanimation)
- [getAnimation](map.Prism.md#getanimation)
- [setVisible](map.Prism.md#setvisible)
- [getVisible](map.Prism.md#getvisible)
- [alpha](map.Prism.md#alpha)
- [getAlpha](map.Prism.md#getalpha)
- [setAlpha](map.Prism.md#setalpha)
- [startLevel](map.Prism.md#startlevel)
- [getStartLevel](map.Prism.md#getstartlevel)
- [setStartLevel](map.Prism.md#setstartlevel)
- [endLevel](map.Prism.md#endlevel)
- [showLevel](map.Prism.md#showlevel)
- [getEndLevel](map.Prism.md#getendlevel)
- [setShowLevel](map.Prism.md#setshowlevel)
- [setEndLevel](map.Prism.md#setendlevel)
- [clickable](map.Prism.md#clickable)
- [getClickable](map.Prism.md#getclickable)
- [setClickable](map.Prism.md#setclickable)
- [setZIndex](map.Prism.md#setzindex)
- [getZIndex](map.Prism.md#getzindex)
- [setExtraInfo](map.Prism.md#setextrainfo)
- [getExtraInfo](map.Prism.md#getextrainfo)
- [getBmDrawItem](map.Prism.md#getbmdrawitem)
- [update](map.Prism.md#update)
- [remove](map.Prism.md#remove)
- [isRemoved](map.Prism.md#isremoved)
- [toString](map.Prism.md#tostring)
- [toDrawItem](map.Prism.md#todrawitem)
- [height](map.Prism.md#height)
- [setHeight](map.Prism.md#setheight)
- [getHeight](map.Prism.md#getheight)
- [points](map.Prism.md#points)
- [setPoints](map.Prism.md#setpoints)
- [getPoints](map.Prism.md#getpoints)
- [topFaceColor](map.Prism.md#topfacecolor)
- [setTopFaceColor](map.Prism.md#settopfacecolor)
- [getTopFaceColor](map.Prism.md#gettopfacecolor)
- [sideFaceColor](map.Prism.md#sidefacecolor)
- [setSideFaceColor](map.Prism.md#setsidefacecolor)
- [getSideFaceColor](map.Prism.md#getsidefacecolor)
- [customSideImage](map.Prism.md#customsideimage)
- [setCustomSideImage](map.Prism.md#setcustomsideimage)
- [destroy](map.Prism.md#destroy)
- [getCustomSideImage](map.Prism.md#getcustomsideimage)

## Constructors

### constructor

• **new Prism**(`opts`): [`Prism`](map.Prism.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | `IPrismOption` |

#### Returns

[`Prism`](map.Prism.md)

#### Overrides

Overlay.constructor

## Properties

### uuid

• **uuid**: `string`

#### Inherited from

[Overlay](map.Overlay.md).[uuid](map.Overlay.md#uuid)

___

### type

• **type**: `default`

#### Inherited from

[Overlay](map.Overlay.md).[type](map.Overlay.md#type)

___

### eventListener

• **eventListener**: `TOverlayListener` = `{}`

#### Inherited from

[Overlay](map.Overlay.md).[eventListener](map.Overlay.md#eventlistener)

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

#### Inherited from

[Overlay](map.Overlay.md).[isDestroyed](map.Overlay.md#isdestroyed)

## Accessors

### typeName

• `get` **typeName**(): `string`

#### Returns

`string`

#### Inherited from

Overlay.typeName

___

### visible

• `get` **visible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

Overlay.visible

• `set` **visible**(`val`): `void`

设置显示状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

Overlay.visible

___

### zIndex

• `get` **zIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

Overlay.zIndex

• `set` **zIndex**(`val`): `void`

设置覆盖物显示层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

Overlay.zIndex

## Methods

### putPointsInfoIntoBundle

▸ **putPointsInfoIntoBundle**(`points`, `b`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] |
| `b` | `undefined` |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[putPointsInfoIntoBundle](map.Overlay.md#putpointsinfointobundle)

___

### addEventListener

▸ **addEventListener**(`model`, `fun`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` |
| `fun` | `Function` |

#### Returns

`void`

**`Since`**

1.0.1

**`History`**

包1.0.0 版本中 model:string , 取值范围 'CLICK'、'TOUCH'

#### Inherited from

[Overlay](map.Overlay.md).[addEventListener](map.Overlay.md#addeventlistener)

___

### removeEventListener

▸ **removeEventListener**(`model`, `fun`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` |
| `fun` | `Function` |

#### Returns

`void`

**`Since`**

1.0.1

**`History`**

包1.0.0 版本中 model:string , 取值范围 'CLICK'、'TOUCH'

#### Inherited from

[Overlay](map.Overlay.md).[removeEventListener](map.Overlay.md#removeeventlistener)

___

### addDragListener

▸ **addDragListener**(`listener`): `void`

添加拖拽监听器，当前仅支持Marker、Label

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener` | [`OverlayDragListener`](../interfaces/map.OverlayDragListener.md) |

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

[Overlay](map.Overlay.md).[addDragListener](map.Overlay.md#adddraglistener)

___

### removeDragListener

▸ **removeDragListener**(): `void`

移除拖拽监听器

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

[Overlay](map.Overlay.md).[removeDragListener](map.Overlay.md#removedraglistener)

___

### getDragListener

▸ **getDragListener**(): [`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

获取拖拽监听器

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

**`Since`**

2.0.3

#### Inherited from

[Overlay](map.Overlay.md).[getDragListener](map.Overlay.md#getdraglistener)

___

### fireEvent

▸ **fireEvent**(`model`, `content`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `model` | `OverlayEvent` |
| `content` | [`EventOverlayBundle`](../interfaces/map.EventOverlayBundle.md) |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[fireEvent](map.Overlay.md#fireevent)

___

### getType

▸ **getType**(): `default`

#### Returns

`default`

#### Inherited from

[Overlay](map.Overlay.md).[getType](map.Overlay.md#gettype)

___

### setAnimation

▸ **setAnimation**(`animation`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `animation` | [`Animation`](map.Animation.md) |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[setAnimation](map.Overlay.md#setanimation)

___

### getAnimation

▸ **getAnimation**(): [`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Inherited from

[Overlay](map.Overlay.md).[getAnimation](map.Overlay.md#getanimation)

___

### setVisible

▸ **setVisible**(`val`): `void`

设置显示状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setVisible](map.Overlay.md#setvisible)

___

### getVisible

▸ **getVisible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getVisible](map.Overlay.md#getvisible)

___

### alpha

▸ **alpha**(`alpha`): [`Prism`](map.Prism.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Prism`](map.Prism.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[alpha](map.Overlay.md#alpha)

___

### getAlpha

▸ **getAlpha**(): `number`

获取透明度

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getAlpha](map.Overlay.md#getalpha)

___

### setAlpha

▸ **setAlpha**(`alpha`): `void`

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setAlpha](map.Overlay.md#setalpha)

___

### startLevel

▸ **startLevel**(`startLevel`): [`Prism`](map.Prism.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Prism`](map.Prism.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[startLevel](map.Overlay.md#startlevel)

___

### getStartLevel

▸ **getStartLevel**(): `number`

获取覆盖物开始显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getStartLevel](map.Overlay.md#getstartlevel)

___

### setStartLevel

▸ **setStartLevel**(`startLevel`): `void`

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setStartLevel](map.Overlay.md#setstartlevel)

___

### endLevel

▸ **endLevel**(`endLevel`): [`Prism`](map.Prism.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Prism`](map.Prism.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[endLevel](map.Overlay.md#endlevel)

___

### showLevel

▸ **showLevel**(`from`, `to`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `from` | `number` |
| `to` | `number` |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[showLevel](map.Overlay.md#showlevel)

___

### getEndLevel

▸ **getEndLevel**(): `number`

获取marker结束显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getEndLevel](map.Overlay.md#getendlevel)

___

### setShowLevel

▸ **setShowLevel**(`from`, `to`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `from` | `number` |
| `to` | `number` |

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[setShowLevel](map.Overlay.md#setshowlevel)

___

### setEndLevel

▸ **setEndLevel**(`endLevel`): `void`

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setEndLevel](map.Overlay.md#setendlevel)

___

### clickable

▸ **clickable**(`isClickable`): [`Prism`](map.Prism.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Prism`](map.Prism.md)

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[clickable](map.Overlay.md#clickable)

___

### getClickable

▸ **getClickable**(): `boolean`

获取是否可点击状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getClickable](map.Overlay.md#getclickable)

___

### setClickable

▸ **setClickable**(`isClickable`): `void`

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setClickable](map.Overlay.md#setclickable)

___

### setZIndex

▸ **setZIndex**(`val`): `void`

设置覆盖物显示层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setZIndex](map.Overlay.md#setzindex)

___

### getZIndex

▸ **getZIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getZIndex](map.Overlay.md#getzindex)

___

### setExtraInfo

▸ **setExtraInfo**(`extraInfo`): `void`

设置覆盖物属性数据

#### Parameters

| Name | Type |
| :------ | :------ |
| `extraInfo` | `AnyObject` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[setExtraInfo](map.Overlay.md#setextrainfo)

___

### getExtraInfo

▸ **getExtraInfo**(): `AnyObject`

获取覆盖物属性数据

#### Returns

`AnyObject`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[getExtraInfo](map.Overlay.md#getextrainfo)

___

### getBmDrawItem

▸ **getBmDrawItem**(): `undefined` \| `default`

#### Returns

`undefined` \| `default`

#### Inherited from

[Overlay](map.Overlay.md).[getBmDrawItem](map.Overlay.md#getbmdrawitem)

___

### update

▸ **update**(): `void`

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[update](map.Overlay.md#update)

___

### remove

▸ **remove**(`noUpdate?`): `void`

移除覆盖物

#### Parameters

| Name | Type |
| :------ | :------ |
| `noUpdate?` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[remove](map.Overlay.md#remove)

___

### isRemoved

▸ **isRemoved**(): `undefined` \| `boolean`

获取是否移除状态

#### Returns

`undefined` \| `boolean`

**`Since`**

1.0.0

#### Inherited from

[Overlay](map.Overlay.md).[isRemoved](map.Overlay.md#isremoved)

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

#### Inherited from

[Overlay](map.Overlay.md).[toString](map.Overlay.md#tostring)

___

### toDrawItem

▸ **toDrawItem**(): `Promise`\<`void`\>

#### Returns

`Promise`\<`void`\>

#### Overrides

[Overlay](map.Overlay.md).[toDrawItem](map.Overlay.md#todrawitem)

___

### height

▸ **height**(`height`): [`Prism`](map.Prism.md)

设置3D棱柱高度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `height` | `number` | 高度 |

#### Returns

[`Prism`](map.Prism.md)

___

### setHeight

▸ **setHeight**(`height`): `void`

设置3D棱柱高度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `height` | `number` | 高度 |

#### Returns

`void`

___

### getHeight

▸ **getHeight**(): `number`

获取高度

#### Returns

`number`

高度

___

### points

▸ **points**(`points`): `undefined` \| [`Prism`](map.Prism.md)

设置3D棱柱坐标点列表

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] | 设置3D棱柱坐标点列表 |

#### Returns

`undefined` \| [`Prism`](map.Prism.md)

___

### setPoints

▸ **setPoints**(`points`): `void`

设置3D棱柱坐标点列表

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] | 设置3D棱柱坐标点列表 |

#### Returns

`void`

___

### getPoints

▸ **getPoints**(): ``null`` \| [`LatLng`](base.LatLng.md)[]

获取棱柱坐标点

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)[]

棱柱坐标点列表

___

### topFaceColor

▸ **topFaceColor**(`topFaceColor`): [`Prism`](map.Prism.md)

设置3D棱柱顶面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `topFaceColor` | `ColorType` | 3D棱柱顶面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

[`Prism`](map.Prism.md)

___

### setTopFaceColor

▸ **setTopFaceColor**(`topFaceColor`): `void`

设置3D棱柱顶面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `topFaceColor` | `ColorType` | 3D棱柱顶面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

`void`

___

### getTopFaceColor

▸ **getTopFaceColor**(): `ColorType`

获取3D棱柱顶面颜色

#### Returns

`ColorType`

3D棱柱顶面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前

___

### sideFaceColor

▸ **sideFaceColor**(`sideFaceColor`): [`Prism`](map.Prism.md)

设置3D棱柱侧面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `sideFaceColor` | `ColorType` | 3D棱柱侧面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

[`Prism`](map.Prism.md)

___

### setSideFaceColor

▸ **setSideFaceColor**(`sideFaceColor`): `void`

设置3D棱柱侧面颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `sideFaceColor` | `ColorType` | 3D棱柱侧面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前 |

#### Returns

`void`

___

### getSideFaceColor

▸ **getSideFaceColor**(): `ColorType`

获取3D棱柱侧面颜色

#### Returns

`ColorType`

3D棱柱侧面颜色。注意颜色值得格式为：0xAARRGGBB，透明度值在前

___

### customSideImage

▸ **customSideImage**(`customSideImage?`): `Promise`\<`undefined` \| [`Prism`](map.Prism.md)\>

设置3D棱柱自定义侧面纹理图片

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `customSideImage?` | [`ImageEntity`](map.ImageEntity.md) | 纹理图片需要256 * 256 |

#### Returns

`Promise`\<`undefined` \| [`Prism`](map.Prism.md)\>

___

### setCustomSideImage

▸ **setCustomSideImage**(`customSideImage`): `void`

设置3D棱柱自定义侧面纹理图片

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `customSideImage` | [`ImageEntity`](map.ImageEntity.md) | 纹理图片需要256 * 256 |

#### Returns

`void`

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`

**`Description`**

prism 销毁

**`Time`**

2025-06-12

#### Overrides

[Overlay](map.Overlay.md).[destroy](map.Overlay.md#destroy)

___

### getCustomSideImage

▸ **getCustomSideImage**(): ``null`` \| [`ImageEntity`](map.ImageEntity.md)

获取自定义侧面纹理图片

#### Returns

``null`` \| [`ImageEntity`](map.ImageEntity.md)

纹理图片
