[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Ground

# Class: Ground

[map](../modules/map.md).Ground

Ground覆盖物

**`Abstract`**

提供Ground覆盖物创建、操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`Ground`**

## Table of contents

### Constructors

- [constructor](map.Ground.md#constructor)

### Properties

- [uuid](map.Ground.md#uuid)
- [type](map.Ground.md#type)
- [eventListener](map.Ground.md#eventlistener)
- [isDestroyed](map.Ground.md#isdestroyed)

### Accessors

- [typeName](map.Ground.md#typename)
- [visible](map.Ground.md#visible)
- [zIndex](map.Ground.md#zindex)

### Methods

- [toDrawItem](map.Ground.md#todrawitem)
- [getImage](map.Ground.md#getimage)
- [image](map.Ground.md#image)
- [setImage](map.Ground.md#setimage)
- [getDimensions](map.Ground.md#getdimensions)
- [getAnchor](map.Ground.md#getanchor)
- [anchor](map.Ground.md#anchor)
- [setAnchor](map.Ground.md#setanchor)
- [bounds](map.Ground.md#bounds)
- [getBound](map.Ground.md#getbound)
- [setBound](map.Ground.md#setbound)
- [transparency](map.Ground.md#transparency)
- [setTransparency](map.Ground.md#settransparency)
- [getTransparency](map.Ground.md#gettransparency)
- [toString](map.Ground.md#tostring)
- [putPointsInfoIntoBundle](map.Ground.md#putpointsinfointobundle)
- [addEventListener](map.Ground.md#addeventlistener)
- [removeEventListener](map.Ground.md#removeeventlistener)
- [addDragListener](map.Ground.md#adddraglistener)
- [removeDragListener](map.Ground.md#removedraglistener)
- [getDragListener](map.Ground.md#getdraglistener)
- [fireEvent](map.Ground.md#fireevent)
- [getType](map.Ground.md#gettype)
- [setAnimation](map.Ground.md#setanimation)
- [getAnimation](map.Ground.md#getanimation)
- [setVisible](map.Ground.md#setvisible)
- [getVisible](map.Ground.md#getvisible)
- [alpha](map.Ground.md#alpha)
- [getAlpha](map.Ground.md#getalpha)
- [setAlpha](map.Ground.md#setalpha)
- [startLevel](map.Ground.md#startlevel)
- [getStartLevel](map.Ground.md#getstartlevel)
- [setStartLevel](map.Ground.md#setstartlevel)
- [endLevel](map.Ground.md#endlevel)
- [showLevel](map.Ground.md#showlevel)
- [getEndLevel](map.Ground.md#getendlevel)
- [setShowLevel](map.Ground.md#setshowlevel)
- [setEndLevel](map.Ground.md#setendlevel)
- [clickable](map.Ground.md#clickable)
- [getClickable](map.Ground.md#getclickable)
- [setClickable](map.Ground.md#setclickable)
- [setZIndex](map.Ground.md#setzindex)
- [getZIndex](map.Ground.md#getzindex)
- [setExtraInfo](map.Ground.md#setextrainfo)
- [getExtraInfo](map.Ground.md#getextrainfo)
- [getBmDrawItem](map.Ground.md#getbmdrawitem)
- [update](map.Ground.md#update)
- [remove](map.Ground.md#remove)
- [isRemoved](map.Ground.md#isremoved)
- [destroy](map.Ground.md#destroy)

## Constructors

### constructor

• **new Ground**(`opts`): [`Ground`](map.Ground.md)

构造函数，默认参数如下
``` Typescript
{
   bounds: [new LatLng(30.5,110.5),new LatLng(40,120)],
   anchorX: 0.5,
   anchorY: 0.5,
   transparency: 1
}

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`IGroundOption`](../interfaces/map.IGroundOption.md) |

#### Returns

[`Ground`](map.Ground.md)

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

#### Overrides

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

### toDrawItem

▸ **toDrawItem**(): `Promise`\<`void`\>

#### Returns

`Promise`\<`void`\>

#### Overrides

[Overlay](map.Overlay.md).[toDrawItem](map.Overlay.md#todrawitem)

___

### getImage

▸ **getImage**(): [`Maybe`](../modules/map.md#maybe)\<[`ImageEntity`](map.ImageEntity.md)\>

获取填充图像

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`ImageEntity`](map.ImageEntity.md)\>

**`Since`**

1.0.0

#### Overrides

Overlay.getImage

___

### image

▸ **image**(`image`): `Promise`\<[`Ground`](map.Ground.md)\>

设置填充图像

#### Parameters

| Name | Type |
| :------ | :------ |
| `image` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`Promise`\<[`Ground`](map.Ground.md)\>

**`Since`**

1.0.0

___

### setImage

▸ **setImage**(`image`): `void`

设置填充图像

#### Parameters

| Name | Type |
| :------ | :------ |
| `image` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getDimensions

▸ **getDimensions**(): [`IDimension`](../interfaces/map.IDimension.md)

获取填充区域宽高，单位米

#### Returns

[`IDimension`](../interfaces/map.IDimension.md)

**`Since`**

1.0.0

___

### getAnchor

▸ **getAnchor**(): [`IAnchor`](../interfaces/map.IAnchor.md)

获取锚点

#### Returns

[`IAnchor`](../interfaces/map.IAnchor.md)

**`Since`**

1.0.0

___

### anchor

▸ **anchor**(`anchorx`, `anchory`): [`Ground`](map.Ground.md)

设置锚点比例，取值[0,1]

#### Parameters

| Name | Type |
| :------ | :------ |
| `anchorx` | `number` |
| `anchory` | `number` |

#### Returns

[`Ground`](map.Ground.md)

**`Abstract`**

默认0.5，水平/垂直方向都居中

**`Since`**

1.0.0

___

### setAnchor

▸ **setAnchor**(`anchorx`, `anchory`): `void`

设置锚点比例，取值[0,1]

#### Parameters

| Name | Type |
| :------ | :------ |
| `anchorx` | `number` |
| `anchory` | `number` |

#### Returns

`void`

**`Abstract`**

默认0.5，水平/垂直方向都居中

**`Since`**

1.0.0

___

### bounds

▸ **bounds**(`southwest`, `northeast`): [`Ground`](map.Ground.md)

设置显示区域

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `southwest` | [`LatLng`](base.LatLng.md) | 左下角坐标 |
| `northeast` | [`LatLng`](base.LatLng.md) | 右上角坐标 |

#### Returns

[`Ground`](map.Ground.md)

**`Since`**

1.0.0

___

### getBound

▸ **getBound**(): [[`LatLng`](base.LatLng.md), [`LatLng`](base.LatLng.md)]

获取显示区域坐标

#### Returns

[[`LatLng`](base.LatLng.md), [`LatLng`](base.LatLng.md)]

**`Since`**

1.0.0

___

### setBound

▸ **setBound**(`southwest`, `northeast`): `void`

设置显示区域

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `southwest` | [`LatLng`](base.LatLng.md) | 左下角坐标 |
| `northeast` | [`LatLng`](base.LatLng.md) | 右上角坐标 |

#### Returns

`void`

**`Since`**

1.0.0

___

### transparency

▸ **transparency**(`num`): [`Ground`](map.Ground.md)

设置图片透明度

#### Parameters

| Name | Type |
| :------ | :------ |
| `num` | `number` |

#### Returns

[`Ground`](map.Ground.md)

**`Since`**

1.0.0

___

### setTransparency

▸ **setTransparency**(`num`): `void`

设置图片透明度

#### Parameters

| Name | Type |
| :------ | :------ |
| `num` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### getTransparency

▸ **getTransparency**(): `number`

获取图片透明度

#### Returns

`number`

**`Since`**

1.0.0

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

**`Since`**

1.0.1

#### Overrides

[Overlay](map.Overlay.md).[toString](map.Overlay.md#tostring)

___

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

▸ **alpha**(`alpha`): [`Ground`](map.Ground.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Ground`](map.Ground.md)

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

▸ **startLevel**(`startLevel`): [`Ground`](map.Ground.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Ground`](map.Ground.md)

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

▸ **endLevel**(`endLevel`): [`Ground`](map.Ground.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Ground`](map.Ground.md)

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

▸ **clickable**(`isClickable`): [`Ground`](map.Ground.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Ground`](map.Ground.md)

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

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

#### Inherited from

[Overlay](map.Overlay.md).[destroy](map.Overlay.md#destroy)
