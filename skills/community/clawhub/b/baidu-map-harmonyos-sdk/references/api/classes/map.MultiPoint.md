[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / MultiPoint

# Class: MultiPoint

[map](../modules/map.md).MultiPoint

MultiPoint覆盖物

**`Abstract`**

提供MultiPoint覆盖物创建、操作方法

**`Since`**

2.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`MultiPoint`**

## Table of contents

### Constructors

- [constructor](map.MultiPoint.md#constructor)

### Properties

- [uuid](map.MultiPoint.md#uuid)
- [type](map.MultiPoint.md#type)
- [eventListener](map.MultiPoint.md#eventlistener)
- [isDestroyed](map.MultiPoint.md#isdestroyed)

### Accessors

- [typeName](map.MultiPoint.md#typename)
- [visible](map.MultiPoint.md#visible)
- [zIndex](map.MultiPoint.md#zindex)

### Methods

- [setMultiPointItems](map.MultiPoint.md#setmultipointitems)
- [setIcon](map.MultiPoint.md#seticon)
- [setPointSize](map.MultiPoint.md#setpointsize)
- [anchor](map.MultiPoint.md#anchor)
- [getMultiPointItems](map.MultiPoint.md#getmultipointitems)
- [getMultiPointItem](map.MultiPoint.md#getmultipointitem)
- [getIcon](map.MultiPoint.md#geticon)
- [getAnchorX](map.MultiPoint.md#getanchorx)
- [getAnchorY](map.MultiPoint.md#getanchory)
- [getPointSizeHeight](map.MultiPoint.md#getpointsizeheight)
- [getPointSizeWidth](map.MultiPoint.md#getpointsizewidth)
- [toDrawItem](map.MultiPoint.md#todrawitem)
- [toString](map.MultiPoint.md#tostring)
- [putPointsInfoIntoBundle](map.MultiPoint.md#putpointsinfointobundle)
- [addEventListener](map.MultiPoint.md#addeventlistener)
- [removeEventListener](map.MultiPoint.md#removeeventlistener)
- [addDragListener](map.MultiPoint.md#adddraglistener)
- [removeDragListener](map.MultiPoint.md#removedraglistener)
- [getDragListener](map.MultiPoint.md#getdraglistener)
- [fireEvent](map.MultiPoint.md#fireevent)
- [getType](map.MultiPoint.md#gettype)
- [setAnimation](map.MultiPoint.md#setanimation)
- [getAnimation](map.MultiPoint.md#getanimation)
- [setVisible](map.MultiPoint.md#setvisible)
- [getVisible](map.MultiPoint.md#getvisible)
- [alpha](map.MultiPoint.md#alpha)
- [getAlpha](map.MultiPoint.md#getalpha)
- [setAlpha](map.MultiPoint.md#setalpha)
- [startLevel](map.MultiPoint.md#startlevel)
- [getStartLevel](map.MultiPoint.md#getstartlevel)
- [setStartLevel](map.MultiPoint.md#setstartlevel)
- [endLevel](map.MultiPoint.md#endlevel)
- [showLevel](map.MultiPoint.md#showlevel)
- [getEndLevel](map.MultiPoint.md#getendlevel)
- [setShowLevel](map.MultiPoint.md#setshowlevel)
- [setEndLevel](map.MultiPoint.md#setendlevel)
- [clickable](map.MultiPoint.md#clickable)
- [getClickable](map.MultiPoint.md#getclickable)
- [setClickable](map.MultiPoint.md#setclickable)
- [setZIndex](map.MultiPoint.md#setzindex)
- [getZIndex](map.MultiPoint.md#getzindex)
- [setExtraInfo](map.MultiPoint.md#setextrainfo)
- [getExtraInfo](map.MultiPoint.md#getextrainfo)
- [getBmDrawItem](map.MultiPoint.md#getbmdrawitem)
- [update](map.MultiPoint.md#update)
- [remove](map.MultiPoint.md#remove)
- [isRemoved](map.MultiPoint.md#isremoved)
- [destroy](map.MultiPoint.md#destroy)

## Constructors

### constructor

• **new MultiPoint**(`opts`): [`MultiPoint`](map.MultiPoint.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`IMultiPointOption`](../interfaces/map.IMultiPointOption.md) |

#### Returns

[`MultiPoint`](map.MultiPoint.md)

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

### setMultiPointItems

▸ **setMultiPointItems**(`multiPointItems`): `void`

添加海量点数据（必填）

#### Parameters

| Name | Type |
| :------ | :------ |
| `multiPointItems` | [`MultiPointItem`](map.MultiPointItem.md)[] |

#### Returns

`void`

___

### setIcon

▸ **setIcon**(`icon`): `Promise`\<`void`\>

设置 MultiPoint 覆盖物的图标 （必填）

#### Parameters

| Name | Type |
| :------ | :------ |
| `icon` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`Promise`\<`void`\>

___

### setPointSize

▸ **setPointSize**(`pointSizeWidth`, `pointSizeHeight`): `void`

纹理渲染大小

#### Parameters

| Name | Type |
| :------ | :------ |
| `pointSizeWidth` | `number` |
| `pointSizeHeight` | `number` |

#### Returns

`void`

___

### anchor

▸ **anchor**(`anchorX`, `anchorY`): `void`

设置锚点

#### Parameters

| Name | Type |
| :------ | :------ |
| `anchorX` | `number` |
| `anchorY` | `number` |

#### Returns

`void`

___

### getMultiPointItems

▸ **getMultiPointItems**(): [`MultiPointItem`](map.MultiPointItem.md)[]

#### Returns

[`MultiPointItem`](map.MultiPointItem.md)[]

___

### getMultiPointItem

▸ **getMultiPointItem**(`index`): ``null`` \| [`MultiPointItem`](map.MultiPointItem.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `index` | `number` |

#### Returns

``null`` \| [`MultiPointItem`](map.MultiPointItem.md)

___

### getIcon

▸ **getIcon**(): ``null`` \| [`ImageEntity`](map.ImageEntity.md)

#### Returns

``null`` \| [`ImageEntity`](map.ImageEntity.md)

___

### getAnchorX

▸ **getAnchorX**(): `number`

#### Returns

`number`

___

### getAnchorY

▸ **getAnchorY**(): `number`

#### Returns

`number`

___

### getPointSizeHeight

▸ **getPointSizeHeight**(): `number`

#### Returns

`number`

___

### getPointSizeWidth

▸ **getPointSizeWidth**(): `number`

#### Returns

`number`

___

### toDrawItem

▸ **toDrawItem**(): `Promise`\<`void`\>

#### Returns

`Promise`\<`void`\>

#### Overrides

[Overlay](map.Overlay.md).[toDrawItem](map.Overlay.md#todrawitem)

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

▸ **alpha**(`alpha`): [`MultiPoint`](map.MultiPoint.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`MultiPoint`](map.MultiPoint.md)

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

▸ **startLevel**(`startLevel`): [`MultiPoint`](map.MultiPoint.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`MultiPoint`](map.MultiPoint.md)

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

▸ **endLevel**(`endLevel`): [`MultiPoint`](map.MultiPoint.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`MultiPoint`](map.MultiPoint.md)

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

▸ **clickable**(`isClickable`): [`MultiPoint`](map.MultiPoint.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`MultiPoint`](map.MultiPoint.md)

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
