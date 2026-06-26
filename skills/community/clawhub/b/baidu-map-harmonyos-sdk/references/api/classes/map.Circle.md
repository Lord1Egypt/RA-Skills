[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Circle

# Class: Circle

[map](../modules/map.md).Circle

Circle覆盖物

**`Abstract`**

提供Circle覆盖物创建、操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`Circle`**

## Table of contents

### Constructors

- [constructor](map.Circle.md#constructor)

### Properties

- [uuid](map.Circle.md#uuid)
- [type](map.Circle.md#type)
- [eventListener](map.Circle.md#eventlistener)
- [isDestroyed](map.Circle.md#isdestroyed)

### Accessors

- [typeName](map.Circle.md#typename)
- [visible](map.Circle.md#visible)
- [zIndex](map.Circle.md#zindex)

### Methods

- [center](map.Circle.md#center)
- [getCenter](map.Circle.md#getcenter)
- [setCenter](map.Circle.md#setcenter)
- [radius](map.Circle.md#radius)
- [getRadius](map.Circle.md#getradius)
- [setRadius](map.Circle.md#setradius)
- [radiusUnit](map.Circle.md#radiusunit)
- [setRadiusUnit](map.Circle.md#setradiusunit)
- [getRadiusUnit](map.Circle.md#getradiusunit)
- [fillcolor](map.Circle.md#fillcolor)
- [getFillcolor](map.Circle.md#getfillcolor)
- [setFillcolor](map.Circle.md#setfillcolor)
- [isGradientCircle](map.Circle.md#isgradientcircle)
- [setIsGradientCircle](map.Circle.md#setisgradientcircle)
- [getIsGradientCircle](map.Circle.md#getisgradientcircle)
- [gradientColors](map.Circle.md#gradientcolors)
- [setGradientColors](map.Circle.md#setgradientcolors)
- [getGradientColors](map.Circle.md#getgradientcolors)
- [gradientRadiusWeight](map.Circle.md#gradientradiusweight)
- [setGradientRadiusWeight](map.Circle.md#setgradientradiusweight)
- [getGradientRadiusWeight](map.Circle.md#getgradientradiusweight)
- [gradientColorWeight](map.Circle.md#gradientcolorweight)
- [setGradientColorWeight](map.Circle.md#setgradientcolorweight)
- [getGradientColorWeight](map.Circle.md#getgradientcolorweight)
- [stroke](map.Circle.md#stroke)
- [getStroke](map.Circle.md#getstroke)
- [setStroke](map.Circle.md#setstroke)
- [toString](map.Circle.md#tostring)
- [putPointsInfoIntoBundle](map.Circle.md#putpointsinfointobundle)
- [addEventListener](map.Circle.md#addeventlistener)
- [removeEventListener](map.Circle.md#removeeventlistener)
- [addDragListener](map.Circle.md#adddraglistener)
- [removeDragListener](map.Circle.md#removedraglistener)
- [getDragListener](map.Circle.md#getdraglistener)
- [fireEvent](map.Circle.md#fireevent)
- [getType](map.Circle.md#gettype)
- [setAnimation](map.Circle.md#setanimation)
- [getAnimation](map.Circle.md#getanimation)
- [setVisible](map.Circle.md#setvisible)
- [getVisible](map.Circle.md#getvisible)
- [alpha](map.Circle.md#alpha)
- [getAlpha](map.Circle.md#getalpha)
- [setAlpha](map.Circle.md#setalpha)
- [startLevel](map.Circle.md#startlevel)
- [getStartLevel](map.Circle.md#getstartlevel)
- [setStartLevel](map.Circle.md#setstartlevel)
- [endLevel](map.Circle.md#endlevel)
- [showLevel](map.Circle.md#showlevel)
- [getEndLevel](map.Circle.md#getendlevel)
- [setShowLevel](map.Circle.md#setshowlevel)
- [setEndLevel](map.Circle.md#setendlevel)
- [clickable](map.Circle.md#clickable)
- [getClickable](map.Circle.md#getclickable)
- [setClickable](map.Circle.md#setclickable)
- [setZIndex](map.Circle.md#setzindex)
- [getZIndex](map.Circle.md#getzindex)
- [setExtraInfo](map.Circle.md#setextrainfo)
- [getExtraInfo](map.Circle.md#getextrainfo)
- [getBmDrawItem](map.Circle.md#getbmdrawitem)
- [update](map.Circle.md#update)
- [remove](map.Circle.md#remove)
- [isRemoved](map.Circle.md#isremoved)
- [destroy](map.Circle.md#destroy)

## Constructors

### constructor

• **new Circle**(`opts?`): [`Circle`](map.Circle.md)

构造函数，默认参数如下
``` Typescript
{
    center: new LatLng(39.914935, 116.403119),
    radius: 1000,
    fillcolor: 'rgba(255, 235, 59 ,0.7)'
}
```

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts?` | [`ICircleOption`](../interfaces/map.ICircleOption.md) |

#### Returns

[`Circle`](map.Circle.md)

**`Since`**

1.0.1

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

### center

▸ **center**(`center`): [`Circle`](map.Circle.md)

设置中心点

#### Parameters

| Name | Type |
| :------ | :------ |
| `center` | [`LatLng`](base.LatLng.md) |

#### Returns

[`Circle`](map.Circle.md)

**`Since`**

1.0.0

___

### getCenter

▸ **getCenter**(): [`LatLng`](base.LatLng.md)

获取中心点

#### Returns

[`LatLng`](base.LatLng.md)

**`Since`**

1.0.0

___

### setCenter

▸ **setCenter**(`center`): `void`

设置中心点

#### Parameters

| Name | Type |
| :------ | :------ |
| `center` | [`LatLng`](base.LatLng.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### radius

▸ **radius**(`radius`): [`Circle`](map.Circle.md)

设置半径

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius` | `number` |

#### Returns

[`Circle`](map.Circle.md)

**`Since`**

1.0.0

___

### getRadius

▸ **getRadius**(): `number`

获取半径

#### Returns

`number`

**`Since`**

1.0.0

___

### setRadius

▸ **setRadius**(`radius`): `void`

设置半径

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### radiusUnit

▸ **radiusUnit**(`radius_unit`): `undefined` \| [`Circle`](map.Circle.md)

设置长度单位

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius_unit` | [`UnitOption`](../enums/map.SysEnum.UnitOption.md) |

#### Returns

`undefined` \| [`Circle`](map.Circle.md)

**`Since`**

1.2.0

___

### setRadiusUnit

▸ **setRadiusUnit**(`radius_unit`): `void`

设置长度单位

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius_unit` | [`UnitOption`](../enums/map.SysEnum.UnitOption.md) |

#### Returns

`void`

**`Since`**

1.2.0

___

### getRadiusUnit

▸ **getRadiusUnit**(): [`UnitOption`](../enums/map.SysEnum.UnitOption.md)

获取长度单位

#### Returns

[`UnitOption`](../enums/map.SysEnum.UnitOption.md)

**`Since`**

1.2.0

___

### fillcolor

▸ **fillcolor**(`color`): [`Circle`](map.Circle.md)

设置填充颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Circle`](map.Circle.md)

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

### isGradientCircle

▸ **isGradientCircle**(`enable`): [`Circle`](map.Circle.md)

是否启用渐变

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `boolean` |

#### Returns

[`Circle`](map.Circle.md)

**`Since`**

1.2.0

___

### setIsGradientCircle

▸ **setIsGradientCircle**(`enable`): `void`

是否启用渐变

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `boolean` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getIsGradientCircle

▸ **getIsGradientCircle**(): `boolean`

启用渐变状态

#### Returns

`boolean`

**`Since`**

1.2.0

___

### gradientColors

▸ **gradientColors**(`colors`): [`Circle`](map.Circle.md)

设置渐变颜色序列

#### Parameters

| Name | Type |
| :------ | :------ |
| `colors` | [`ColorString`](../modules/map.md#colorstring)[] |

#### Returns

[`Circle`](map.Circle.md)

**`Since`**

1.2.0

___

### setGradientColors

▸ **setGradientColors**(`colors`): `void`

设置渐变颜色序列

#### Parameters

| Name | Type |
| :------ | :------ |
| `colors` | [`ColorString`](../modules/map.md#colorstring)[] |

#### Returns

`void`

**`Since`**

1.2.0

___

### getGradientColors

▸ **getGradientColors**(): `string`[]

获取渐变颜色序列

#### Returns

`string`[]

**`Since`**

1.2.0

___

### gradientRadiusWeight

▸ **gradientRadiusWeight**(`weight`): `undefined` \| [`Circle`](map.Circle.md)

设置渐变半径权重 0.0 ～ 1.0

#### Parameters

| Name | Type |
| :------ | :------ |
| `weight` | `number` |

#### Returns

`undefined` \| [`Circle`](map.Circle.md)

**`Since`**

1.2.0

___

### setGradientRadiusWeight

▸ **setGradientRadiusWeight**(`weight`): `void`

设置渐变半径权重 0.0 ～ 1.0

#### Parameters

| Name | Type |
| :------ | :------ |
| `weight` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getGradientRadiusWeight

▸ **getGradientRadiusWeight**(): `number`

获取渐变半径权重 0.0 ～ 1.0

#### Returns

`number`

**`Since`**

1.2.0

___

### gradientColorWeight

▸ **gradientColorWeight**(`weight`): `undefined` \| [`Circle`](map.Circle.md)

设置渐变颜色权重 0.0 ～ 1.0

#### Parameters

| Name | Type |
| :------ | :------ |
| `weight` | `number` |

#### Returns

`undefined` \| [`Circle`](map.Circle.md)

**`Since`**

1.2.0

___

### setGradientColorWeight

▸ **setGradientColorWeight**(`weight`): `void`

设置渐变颜色权重 0.0 ～ 1.0

#### Parameters

| Name | Type |
| :------ | :------ |
| `weight` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getGradientColorWeight

▸ **getGradientColorWeight**(): `number`

获取渐变颜色权重 0.0 ～ 1.0

#### Returns

`number`

**`Since`**

1.2.0

___

### stroke

▸ **stroke**(`stroke`): [`Circle`](map.Circle.md)

设置描边样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `stroke` | [`Stroke`](map.Stroke.md) |

#### Returns

[`Circle`](map.Circle.md)

**`Since`**

1.0.0

___

### getStroke

▸ **getStroke**(): [`Nullable`](../modules/map.md#nullable)\<[`Stroke`](map.Stroke.md)\>

获取描边样式

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`Stroke`](map.Stroke.md)\>

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

▸ **alpha**(`alpha`): [`Circle`](map.Circle.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Circle`](map.Circle.md)

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

▸ **startLevel**(`startLevel`): [`Circle`](map.Circle.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Circle`](map.Circle.md)

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

▸ **endLevel**(`endLevel`): [`Circle`](map.Circle.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Circle`](map.Circle.md)

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

▸ **clickable**(`isClickable`): [`Circle`](map.Circle.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Circle`](map.Circle.md)

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
