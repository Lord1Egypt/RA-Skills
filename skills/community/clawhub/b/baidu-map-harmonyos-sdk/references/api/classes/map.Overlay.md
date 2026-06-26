[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Overlay

# Class: Overlay

[map](../modules/map.md).Overlay

覆盖物基类

**`Abstract`**

提供覆盖物基础的操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- **`Overlay`**

  ↳ [`Circle`](map.Circle.md)

  ↳ [`Polygon`](map.Polygon.md)

  ↳ [`Polyline`](map.Polyline.md)

  ↳ [`Ground`](map.Ground.md)

  ↳ [`Arc`](map.Arc.md)

  ↳ [`MultiPoint`](map.MultiPoint.md)

  ↳ [`Bd_3DModel`](map.Bd_3DModel.md)

  ↳ [`TextPathMarker`](map.TextPathMarker.md)

  ↳ [`Track`](map.Track.md)

  ↳ [`Prism`](map.Prism.md)

  ↳ [`ClusterGroup`](map.ClusterGroup.md)

## Table of contents

### Properties

- [uuid](map.Overlay.md#uuid)
- [type](map.Overlay.md#type)
- [eventListener](map.Overlay.md#eventlistener)
- [isDestroyed](map.Overlay.md#isdestroyed)

### Accessors

- [typeName](map.Overlay.md#typename)
- [visible](map.Overlay.md#visible)
- [zIndex](map.Overlay.md#zindex)

### Methods

- [putPointsInfoIntoBundle](map.Overlay.md#putpointsinfointobundle)
- [toDrawItem](map.Overlay.md#todrawitem)
- [addEventListener](map.Overlay.md#addeventlistener)
- [removeEventListener](map.Overlay.md#removeeventlistener)
- [addDragListener](map.Overlay.md#adddraglistener)
- [removeDragListener](map.Overlay.md#removedraglistener)
- [getDragListener](map.Overlay.md#getdraglistener)
- [fireEvent](map.Overlay.md#fireevent)
- [getType](map.Overlay.md#gettype)
- [setAnimation](map.Overlay.md#setanimation)
- [getAnimation](map.Overlay.md#getanimation)
- [setVisible](map.Overlay.md#setvisible)
- [getVisible](map.Overlay.md#getvisible)
- [alpha](map.Overlay.md#alpha)
- [getAlpha](map.Overlay.md#getalpha)
- [setAlpha](map.Overlay.md#setalpha)
- [startLevel](map.Overlay.md#startlevel)
- [getStartLevel](map.Overlay.md#getstartlevel)
- [setStartLevel](map.Overlay.md#setstartlevel)
- [endLevel](map.Overlay.md#endlevel)
- [showLevel](map.Overlay.md#showlevel)
- [getEndLevel](map.Overlay.md#getendlevel)
- [setShowLevel](map.Overlay.md#setshowlevel)
- [setEndLevel](map.Overlay.md#setendlevel)
- [clickable](map.Overlay.md#clickable)
- [getClickable](map.Overlay.md#getclickable)
- [setClickable](map.Overlay.md#setclickable)
- [setZIndex](map.Overlay.md#setzindex)
- [getZIndex](map.Overlay.md#getzindex)
- [setExtraInfo](map.Overlay.md#setextrainfo)
- [getExtraInfo](map.Overlay.md#getextrainfo)
- [getBmDrawItem](map.Overlay.md#getbmdrawitem)
- [update](map.Overlay.md#update)
- [remove](map.Overlay.md#remove)
- [isRemoved](map.Overlay.md#isremoved)
- [destroy](map.Overlay.md#destroy)
- [toString](map.Overlay.md#tostring)

## Properties

### uuid

• **uuid**: `string`

___

### type

• **type**: `default`

___

### eventListener

• **eventListener**: `TOverlayListener` = `{}`

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

## Accessors

### typeName

• `get` **typeName**(): `string`

#### Returns

`string`

___

### visible

• `get` **visible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

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

___

### zIndex

• `get` **zIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

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

___

### toDrawItem

▸ **toDrawItem**(): `void`

#### Returns

`void`

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

___

### removeDragListener

▸ **removeDragListener**(): `void`

移除拖拽监听器

#### Returns

`void`

**`Since`**

2.0.3

___

### getDragListener

▸ **getDragListener**(): [`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

获取拖拽监听器

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

**`Since`**

2.0.3

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

___

### getType

▸ **getType**(): `default`

#### Returns

`default`

___

### setAnimation

▸ **setAnimation**(`animation`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `animation` | [`Animation`](map.Animation.md) |

#### Returns

`void`

___

### getAnimation

▸ **getAnimation**(): [`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

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

___

### getVisible

▸ **getVisible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

___

### alpha

▸ **alpha**(`alpha`): [`Overlay`](map.Overlay.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Overlay`](map.Overlay.md)

**`Since`**

1.0.0

___

### getAlpha

▸ **getAlpha**(): `number`

获取透明度

#### Returns

`number`

**`Since`**

1.0.0

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

___

### startLevel

▸ **startLevel**(`startLevel`): [`Overlay`](map.Overlay.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Overlay`](map.Overlay.md)

**`Since`**

1.0.0

___

### getStartLevel

▸ **getStartLevel**(): `number`

获取覆盖物开始显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

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

___

### endLevel

▸ **endLevel**(`endLevel`): [`Overlay`](map.Overlay.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Overlay`](map.Overlay.md)

**`Since`**

1.0.0

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

___

### getEndLevel

▸ **getEndLevel**(): `number`

获取marker结束显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

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

___

### clickable

▸ **clickable**(`isClickable`): [`Overlay`](map.Overlay.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Overlay`](map.Overlay.md)

**`Since`**

1.0.0

___

### getClickable

▸ **getClickable**(): `boolean`

获取是否可点击状态

#### Returns

`boolean`

**`Since`**

1.0.0

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

___

### getZIndex

▸ **getZIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

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

___

### getExtraInfo

▸ **getExtraInfo**(): `AnyObject`

获取覆盖物属性数据

#### Returns

`AnyObject`

**`Since`**

1.0.0

___

### getBmDrawItem

▸ **getBmDrawItem**(): `undefined` \| `default`

#### Returns

`undefined` \| `default`

___

### update

▸ **update**(): `void`

#### Returns

`void`

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

___

### isRemoved

▸ **isRemoved**(): `undefined` \| `boolean`

获取是否移除状态

#### Returns

`undefined` \| `boolean`

**`Since`**

1.0.0

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

___

### toString

▸ **toString**(): `string`

#### Returns

`string`
