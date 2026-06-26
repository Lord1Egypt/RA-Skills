[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Polygon

# Class: Polygon

[map](../modules/map.md).Polygon

Polygon覆盖物

**`Abstract`**

提供Polygon覆盖物创建、操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`Polygon`**

## Table of contents

### Constructors

- [constructor](map.Polygon.md#constructor)

### Properties

- [uuid](map.Polygon.md#uuid)
- [type](map.Polygon.md#type)
- [eventListener](map.Polygon.md#eventlistener)
- [isDestroyed](map.Polygon.md#isdestroyed)

### Accessors

- [visible](map.Polygon.md#visible)
- [zIndex](map.Polygon.md#zindex)
- [typeName](map.Polygon.md#typename)

### Methods

- [putPointsInfoIntoBundle](map.Polygon.md#putpointsinfointobundle)
- [addEventListener](map.Polygon.md#addeventlistener)
- [removeEventListener](map.Polygon.md#removeeventlistener)
- [addDragListener](map.Polygon.md#adddraglistener)
- [removeDragListener](map.Polygon.md#removedraglistener)
- [getDragListener](map.Polygon.md#getdraglistener)
- [fireEvent](map.Polygon.md#fireevent)
- [getType](map.Polygon.md#gettype)
- [setAnimation](map.Polygon.md#setanimation)
- [getAnimation](map.Polygon.md#getanimation)
- [setVisible](map.Polygon.md#setvisible)
- [getVisible](map.Polygon.md#getvisible)
- [alpha](map.Polygon.md#alpha)
- [getAlpha](map.Polygon.md#getalpha)
- [setAlpha](map.Polygon.md#setalpha)
- [startLevel](map.Polygon.md#startlevel)
- [getStartLevel](map.Polygon.md#getstartlevel)
- [setStartLevel](map.Polygon.md#setstartlevel)
- [endLevel](map.Polygon.md#endlevel)
- [showLevel](map.Polygon.md#showlevel)
- [getEndLevel](map.Polygon.md#getendlevel)
- [setShowLevel](map.Polygon.md#setshowlevel)
- [setEndLevel](map.Polygon.md#setendlevel)
- [clickable](map.Polygon.md#clickable)
- [getClickable](map.Polygon.md#getclickable)
- [setClickable](map.Polygon.md#setclickable)
- [setZIndex](map.Polygon.md#setzindex)
- [getZIndex](map.Polygon.md#getzindex)
- [setExtraInfo](map.Polygon.md#setextrainfo)
- [getExtraInfo](map.Polygon.md#getextrainfo)
- [getBmDrawItem](map.Polygon.md#getbmdrawitem)
- [update](map.Polygon.md#update)
- [remove](map.Polygon.md#remove)
- [isRemoved](map.Polygon.md#isremoved)
- [destroy](map.Polygon.md#destroy)
- [fillcolor](map.Polygon.md#fillcolor)
- [getFillcolor](map.Polygon.md#getfillcolor)
- [setFillcolor](map.Polygon.md#setfillcolor)
- [points](map.Polygon.md#points)
- [getPoints](map.Polygon.md#getpoints)
- [setPoints](map.Polygon.md#setpoints)
- [holePoints](map.Polygon.md#holepoints)
- [setHolePoints](map.Polygon.md#setholepoints)
- [getHolePoints](map.Polygon.md#getholepoints)
- [getStroke](map.Polygon.md#getstroke)
- [stroke](map.Polygon.md#stroke)
- [setStroke](map.Polygon.md#setstroke)
- [thin](map.Polygon.md#thin)
- [setThin](map.Polygon.md#setthin)
- [getThin](map.Polygon.md#getthin)
- [thinFactor](map.Polygon.md#thinfactor)
- [setThinFactor](map.Polygon.md#setthinfactor)
- [getThinFactor](map.Polygon.md#getthinfactor)
- [jointType](map.Polygon.md#jointtype)
- [setJointType](map.Polygon.md#setjointtype)
- [getJointType](map.Polygon.md#getjointtype)
- [isHoleClickable](map.Polygon.md#isholeclickable)
- [setIsHoleClickable](map.Polygon.md#setisholeclickable)
- [getIsHoleClickable](map.Polygon.md#getisholeclickable)
- [toString](map.Polygon.md#tostring)
- [toDrawItem](map.Polygon.md#todrawitem)

## Constructors

### constructor

• **new Polygon**(`opts`): [`Polygon`](map.Polygon.md)

构造函数，默认参数
```Typescript
{
    points: [],
    fillcolor: 'rgba(255, 235, 59 ,0.7)'
}

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`IPolygonOption`](../interfaces/map.IPolygonOption.md) |

#### Returns

[`Polygon`](map.Polygon.md)

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

___

### typeName

• `get` **typeName**(): `string`

#### Returns

`string`

#### Overrides

Overlay.typeName

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

▸ **alpha**(`alpha`): [`Polygon`](map.Polygon.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Polygon`](map.Polygon.md)

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

▸ **startLevel**(`startLevel`): [`Polygon`](map.Polygon.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Polygon`](map.Polygon.md)

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

▸ **endLevel**(`endLevel`): [`Polygon`](map.Polygon.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Polygon`](map.Polygon.md)

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

▸ **clickable**(`isClickable`): [`Polygon`](map.Polygon.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Polygon`](map.Polygon.md)

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

___

### fillcolor

▸ **fillcolor**(`color`): [`Polygon`](map.Polygon.md)

设置填充颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Polygon`](map.Polygon.md)

**`Since`**

1.0.0

___

### getFillcolor

▸ **getFillcolor**(): `string`

获取填充颜色

#### Returns

`string`

**`Since`**

1.0.0

___

### setFillcolor

▸ **setFillcolor**(`color`): `void`

设置填充颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.0.0

___

### points

▸ **points**(`points`): [`Polygon`](map.Polygon.md)

设置图形坐标串

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | `string` \| [`LatLng`](base.LatLng.md)[] |

#### Returns

[`Polygon`](map.Polygon.md)

**`Since`**

1.0.0

___

### getPoints

▸ **getPoints**(): `string` \| [`LatLng`](base.LatLng.md)[]

获取图形坐标串

#### Returns

`string` \| [`LatLng`](base.LatLng.md)[]

**`Since`**

1.0.0

___

### setPoints

▸ **setPoints**(`points`): `void`

设置图形坐标串

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] |

#### Returns

`void`

**`Since`**

1.0.0

___

### holePoints

▸ **holePoints**(`points`): [`Polygon`](map.Polygon.md)

设置镂空区域

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | [`Maybe`](../modules/map.md#maybe)\<[`LatLng`](base.LatLng.md)[] \| [`LatLng`](base.LatLng.md)[][]\> |

#### Returns

[`Polygon`](map.Polygon.md)

**`Since`**

1.2.1

___

### setHolePoints

▸ **setHolePoints**(`points`): `void`

设置镂空区域

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] \| [`LatLng`](base.LatLng.md)[][] |

#### Returns

`void`

**`Since`**

1.2.1

___

### getHolePoints

▸ **getHolePoints**(): [`Maybe`](../modules/map.md#maybe)\<[`LatLng`](base.LatLng.md)[] \| [`LatLng`](base.LatLng.md)[][]\>

获取镂空区域

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`LatLng`](base.LatLng.md)[] \| [`LatLng`](base.LatLng.md)[][]\>

**`Since`**

1.2.1

___

### getStroke

▸ **getStroke**(): [`Maybe`](../modules/map.md#maybe)\<[`Stroke`](map.Stroke.md)\>

获取描边样式

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`Stroke`](map.Stroke.md)\>

**`Since`**

1.0.0

___

### stroke

▸ **stroke**(`stroke`): [`Polygon`](map.Polygon.md)

设置描边样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke` | [`Stroke`](map.Stroke.md) |

#### Returns

[`Polygon`](map.Polygon.md)

**`Since`**

1.0.0

___

### setStroke

▸ **setStroke**(`stroke`): `void`

设置描边样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke` | [`Stroke`](map.Stroke.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### thin

▸ **thin**(`val`): `void`

是否启用抽稀

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.2.0

___

### setThin

▸ **setThin**(`val`): `void`

是否启用抽稀

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getThin

▸ **getThin**(): `boolean`

启用抽稀状态

#### Returns

`boolean`

**`Since`**

1.2.0

___

### thinFactor

▸ **thinFactor**(`val`): [`Polygon`](map.Polygon.md)

设置抽稀容差值 >=0

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

[`Polygon`](map.Polygon.md)

**`Since`**

1.2.0

___

### setThinFactor

▸ **setThinFactor**(`val`): `void`

设置抽稀容差值 >=0

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getThinFactor

▸ **getThinFactor**(): `number`

获取抽稀容差值

#### Returns

`number`

**`Since`**

1.2.0

___

### jointType

▸ **jointType**(`val`): [`Polygon`](map.Polygon.md)

设置拐点类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md) |

#### Returns

[`Polygon`](map.Polygon.md)

**`Since`**

1.2.0

___

### setJointType

▸ **setJointType**(`val`): `void`

设置拐点类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md) |

#### Returns

`void`

**`Since`**

1.2.0

___

### getJointType

▸ **getJointType**(): [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md)

获取拐点类型

#### Returns

[`LineJoinType`](../enums/map.SysEnum.LineJoinType.md)

**`Since`**

1.2.0

___

### isHoleClickable

▸ **isHoleClickable**(`val`): [`Polygon`](map.Polygon.md)

设置镂空区域是否可点击，默认false

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

[`Polygon`](map.Polygon.md)

**`Since`**

1.2.1

___

### setIsHoleClickable

▸ **setIsHoleClickable**(`val`): `void`

设置镂空区域是否可点击，默认false

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.2.1

___

### getIsHoleClickable

▸ **getIsHoleClickable**(): `boolean`

获取镂空区域是否可点击，默认false

#### Returns

`boolean`

**`Since`**

1.2.1

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

### toDrawItem

▸ **toDrawItem**(): `void`

#### Returns

`void`

#### Overrides

[Overlay](map.Overlay.md).[toDrawItem](map.Overlay.md#todrawitem)
