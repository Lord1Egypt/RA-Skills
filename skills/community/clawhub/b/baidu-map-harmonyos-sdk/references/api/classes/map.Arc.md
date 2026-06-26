[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Arc

# Class: Arc

[map](../modules/map.md).Arc

Arc覆盖物

**`Abstract`**

提供Arc覆盖物创建、操作方法

**`Since`**

2.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`Arc`**

## Table of contents

### Constructors

- [constructor](map.Arc.md#constructor)

### Properties

- [mColor](map.Arc.md#mcolor)
- [mWidth](map.Arc.md#mwidth)
- [mStartPoint](map.Arc.md#mstartpoint)
- [mMiddlePoint](map.Arc.md#mmiddlepoint)
- [mEndPoint](map.Arc.md#mendpoint)
- [mRadius](map.Arc.md#mradius)
- [mPixelRadius](map.Arc.md#mpixelradius)
- [mStartRadian](map.Arc.md#mstartradian)
- [mEndRadian](map.Arc.md#mendradian)
- [mIsClockwise](map.Arc.md#misclockwise)
- [mBMCenterPoint](map.Arc.md#mbmcenterpoint)
- [mCenter](map.Arc.md#mcenter)
- [mLineStyle](map.Arc.md#mlinestyle)
- [uuid](map.Arc.md#uuid)
- [type](map.Arc.md#type)
- [eventListener](map.Arc.md#eventlistener)
- [isDestroyed](map.Arc.md#isdestroyed)

### Accessors

- [typeName](map.Arc.md#typename)
- [visible](map.Arc.md#visible)
- [zIndex](map.Arc.md#zindex)

### Methods

- [getColor](map.Arc.md#getcolor)
- [getStartPoint](map.Arc.md#getstartpoint)
- [getMiddlePoint](map.Arc.md#getmiddlepoint)
- [getEndPoint](map.Arc.md#getendpoint)
- [getWidth](map.Arc.md#getwidth)
- [setColor](map.Arc.md#setcolor)
- [setPoints](map.Arc.md#setpoints)
- [setWidth](map.Arc.md#setwidth)
- [toString](map.Arc.md#tostring)
- [putPointsInfoIntoBundle](map.Arc.md#putpointsinfointobundle)
- [addEventListener](map.Arc.md#addeventlistener)
- [removeEventListener](map.Arc.md#removeeventlistener)
- [addDragListener](map.Arc.md#adddraglistener)
- [removeDragListener](map.Arc.md#removedraglistener)
- [getDragListener](map.Arc.md#getdraglistener)
- [fireEvent](map.Arc.md#fireevent)
- [getType](map.Arc.md#gettype)
- [setAnimation](map.Arc.md#setanimation)
- [getAnimation](map.Arc.md#getanimation)
- [setVisible](map.Arc.md#setvisible)
- [getVisible](map.Arc.md#getvisible)
- [alpha](map.Arc.md#alpha)
- [getAlpha](map.Arc.md#getalpha)
- [setAlpha](map.Arc.md#setalpha)
- [startLevel](map.Arc.md#startlevel)
- [getStartLevel](map.Arc.md#getstartlevel)
- [setStartLevel](map.Arc.md#setstartlevel)
- [endLevel](map.Arc.md#endlevel)
- [showLevel](map.Arc.md#showlevel)
- [getEndLevel](map.Arc.md#getendlevel)
- [setShowLevel](map.Arc.md#setshowlevel)
- [setEndLevel](map.Arc.md#setendlevel)
- [clickable](map.Arc.md#clickable)
- [getClickable](map.Arc.md#getclickable)
- [setClickable](map.Arc.md#setclickable)
- [setZIndex](map.Arc.md#setzindex)
- [getZIndex](map.Arc.md#getzindex)
- [setExtraInfo](map.Arc.md#setextrainfo)
- [getExtraInfo](map.Arc.md#getextrainfo)
- [getBmDrawItem](map.Arc.md#getbmdrawitem)
- [update](map.Arc.md#update)
- [remove](map.Arc.md#remove)
- [isRemoved](map.Arc.md#isremoved)
- [destroy](map.Arc.md#destroy)

## Constructors

### constructor

• **new Arc**(`opts`): [`Arc`](map.Arc.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`IArcOption`](../interfaces/map.IArcOption.md) |

#### Returns

[`Arc`](map.Arc.md)

#### Overrides

Overlay.constructor

## Properties

### mColor

• **mColor**: `number`

___

### mWidth

• **mWidth**: `number` = `5`

___

### mStartPoint

• `Optional` **mStartPoint**: [`LatLng`](base.LatLng.md)

___

### mMiddlePoint

• `Optional` **mMiddlePoint**: [`LatLng`](base.LatLng.md)

___

### mEndPoint

• `Optional` **mEndPoint**: [`LatLng`](base.LatLng.md)

___

### mRadius

• **mRadius**: `number` = `0`

___

### mPixelRadius

• **mPixelRadius**: `number` = `0`

___

### mStartRadian

• **mStartRadian**: `number` = `0`

___

### mEndRadian

• **mEndRadian**: `number` = `0`

___

### mIsClockwise

• **mIsClockwise**: `boolean` = `false`

___

### mBMCenterPoint

• `Optional` **mBMCenterPoint**: `default`

___

### mCenter

• `Optional` **mCenter**: [`LatLng`](base.LatLng.md)

___

### mLineStyle

• `Optional` **mLineStyle**: `default`

___

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

### getColor

▸ **getColor**(): `number`

#### Returns

`number`

___

### getStartPoint

▸ **getStartPoint**(): `undefined` \| [`LatLng`](base.LatLng.md)

#### Returns

`undefined` \| [`LatLng`](base.LatLng.md)

___

### getMiddlePoint

▸ **getMiddlePoint**(): `undefined` \| [`LatLng`](base.LatLng.md)

#### Returns

`undefined` \| [`LatLng`](base.LatLng.md)

___

### getEndPoint

▸ **getEndPoint**(): `undefined` \| [`LatLng`](base.LatLng.md)

#### Returns

`undefined` \| [`LatLng`](base.LatLng.md)

___

### getWidth

▸ **getWidth**(): `number`

#### Returns

`number`

___

### setColor

▸ **setColor**(`color`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

___

### setPoints

▸ **setPoints**(`start`, `middle`, `end`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `start` | [`LatLng`](base.LatLng.md) |
| `middle` | [`LatLng`](base.LatLng.md) |
| `end` | [`LatLng`](base.LatLng.md) |

#### Returns

`void`

___

### setWidth

▸ **setWidth**(`width`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

**`Since`**

2.0.0

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

▸ **alpha**(`alpha`): [`Arc`](map.Arc.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Arc`](map.Arc.md)

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

▸ **startLevel**(`startLevel`): [`Arc`](map.Arc.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Arc`](map.Arc.md)

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

▸ **endLevel**(`endLevel`): [`Arc`](map.Arc.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Arc`](map.Arc.md)

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

▸ **clickable**(`isClickable`): [`Arc`](map.Arc.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Arc`](map.Arc.md)

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
