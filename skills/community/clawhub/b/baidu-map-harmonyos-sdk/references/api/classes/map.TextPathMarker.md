[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / TextPathMarker

# Class: TextPathMarker

[map](../modules/map.md).TextPathMarker

TextPathMarker覆盖物

**`Abstract`**

提供路名绘制创建、操作方法

**`Since`**

2.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`TextPathMarker`**

## Table of contents

### Constructors

- [constructor](map.TextPathMarker.md#constructor)

### Properties

- [uuid](map.TextPathMarker.md#uuid)
- [type](map.TextPathMarker.md#type)
- [eventListener](map.TextPathMarker.md#eventlistener)
- [isDestroyed](map.TextPathMarker.md#isdestroyed)

### Accessors

- [typeName](map.TextPathMarker.md#typename)
- [visible](map.TextPathMarker.md#visible)
- [zIndex](map.TextPathMarker.md#zindex)

### Methods

- [putPointsInfoIntoBundle](map.TextPathMarker.md#putpointsinfointobundle)
- [addEventListener](map.TextPathMarker.md#addeventlistener)
- [removeEventListener](map.TextPathMarker.md#removeeventlistener)
- [addDragListener](map.TextPathMarker.md#adddraglistener)
- [removeDragListener](map.TextPathMarker.md#removedraglistener)
- [getDragListener](map.TextPathMarker.md#getdraglistener)
- [fireEvent](map.TextPathMarker.md#fireevent)
- [getType](map.TextPathMarker.md#gettype)
- [setAnimation](map.TextPathMarker.md#setanimation)
- [getAnimation](map.TextPathMarker.md#getanimation)
- [setVisible](map.TextPathMarker.md#setvisible)
- [getVisible](map.TextPathMarker.md#getvisible)
- [alpha](map.TextPathMarker.md#alpha)
- [getAlpha](map.TextPathMarker.md#getalpha)
- [setAlpha](map.TextPathMarker.md#setalpha)
- [startLevel](map.TextPathMarker.md#startlevel)
- [getStartLevel](map.TextPathMarker.md#getstartlevel)
- [setStartLevel](map.TextPathMarker.md#setstartlevel)
- [endLevel](map.TextPathMarker.md#endlevel)
- [showLevel](map.TextPathMarker.md#showlevel)
- [getEndLevel](map.TextPathMarker.md#getendlevel)
- [setShowLevel](map.TextPathMarker.md#setshowlevel)
- [setEndLevel](map.TextPathMarker.md#setendlevel)
- [clickable](map.TextPathMarker.md#clickable)
- [getClickable](map.TextPathMarker.md#getclickable)
- [setClickable](map.TextPathMarker.md#setclickable)
- [setZIndex](map.TextPathMarker.md#setzindex)
- [getZIndex](map.TextPathMarker.md#getzindex)
- [setExtraInfo](map.TextPathMarker.md#setextrainfo)
- [getExtraInfo](map.TextPathMarker.md#getextrainfo)
- [getBmDrawItem](map.TextPathMarker.md#getbmdrawitem)
- [update](map.TextPathMarker.md#update)
- [remove](map.TextPathMarker.md#remove)
- [isRemoved](map.TextPathMarker.md#isremoved)
- [destroy](map.TextPathMarker.md#destroy)
- [setText](map.TextPathMarker.md#settext)
- [setTextColor](map.TextPathMarker.md#settextcolor)
- [getTextColor](map.TextPathMarker.md#gettextcolor)
- [setTextSize](map.TextPathMarker.md#settextsize)
- [getTextSize](map.TextPathMarker.md#gettextsize)
- [setTextBorderColor](map.TextPathMarker.md#settextbordercolor)
- [getTextBorderColor](map.TextPathMarker.md#gettextbordercolor)
- [setTextBorderWidth](map.TextPathMarker.md#settextborderwidth)
- [getTextBorderWidth](map.TextPathMarker.md#gettextborderwidth)
- [setTextFontOption](map.TextPathMarker.md#settextfontoption)
- [getTextFontOption](map.TextPathMarker.md#gettextfontoption)
- [getText](map.TextPathMarker.md#gettext)
- [setPoints](map.TextPathMarker.md#setpoints)
- [getPoints](map.TextPathMarker.md#getpoints)
- [toDrawItem](map.TextPathMarker.md#todrawitem)
- [toString](map.TextPathMarker.md#tostring)

## Constructors

### constructor

• **new TextPathMarker**(`textPathMarkerOption`): [`TextPathMarker`](map.TextPathMarker.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `textPathMarkerOption` | [`ITextPathMarkerOption`](../interfaces/map.ITextPathMarkerOption.md) |

#### Returns

[`TextPathMarker`](map.TextPathMarker.md)

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

▸ **alpha**(`alpha`): [`TextPathMarker`](map.TextPathMarker.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`TextPathMarker`](map.TextPathMarker.md)

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

▸ **startLevel**(`startLevel`): [`TextPathMarker`](map.TextPathMarker.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`TextPathMarker`](map.TextPathMarker.md)

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

▸ **endLevel**(`endLevel`): [`TextPathMarker`](map.TextPathMarker.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`TextPathMarker`](map.TextPathMarker.md)

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

▸ **clickable**(`isClickable`): [`TextPathMarker`](map.TextPathMarker.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`TextPathMarker`](map.TextPathMarker.md)

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

### setText

▸ **setText**(`text`): `void`

设置路名

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `text` | `string` | 路名字符串 |

#### Returns

`void`

___

### setTextColor

▸ **setTextColor**(`argb`): `void`

设置文字颜色（ARGB 格式）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `argb` | [`ColorString`](../modules/map.md#colorstring) | 颜色值（如 0xFF0000FF 表示蓝色） |

#### Returns

`void`

___

### getTextColor

▸ **getTextColor**(): `number`

获取文字颜色

#### Returns

`number`

文字颜色（ARGB 格式）

___

### setTextSize

▸ **setTextSize**(`size`): `void`

设置文字大小

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `size` | `number` | 文字大小（单位：px） |

#### Returns

`void`

___

### getTextSize

▸ **getTextSize**(): `number`

获取文字大小

#### Returns

`number`

文字大小（px）

___

### setTextBorderColor

▸ **setTextBorderColor**(`argb`): `void`

设置文字描边颜色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `argb` | [`ColorString`](../modules/map.md#colorstring) | 描边颜色（ARGB 格式） |

#### Returns

`void`

___

### getTextBorderColor

▸ **getTextBorderColor**(): `number`

获取文字描边颜色

#### Returns

`number`

描边颜色（ARGB 格式）

___

### setTextBorderWidth

▸ **setTextBorderWidth**(`width`): `void`

设置文字描边宽度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `width` | `number` | 描边宽度（px） |

#### Returns

`void`

___

### getTextBorderWidth

▸ **getTextBorderWidth**(): `number`

获取文字描边宽度

#### Returns

`number`

描边宽度（px）

___

### setTextFontOption

▸ **setTextFontOption**(`option`): `void`

设置字体格式

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | `number` |

#### Returns

`void`

___

### getTextFontOption

▸ **getTextFontOption**(): `number`

获取字体格式

#### Returns

`number`

number

___

### getText

▸ **getText**(): `string`

获取路名

#### Returns

`string`

路名字符串

___

### setPoints

▸ **setPoints**(`points`): `void`

设置展示路名的道路坐标点（需至少 2 个点）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] | 经纬度坐标列表 |

#### Returns

`void`

___

### getPoints

▸ **getPoints**(): ``null`` \| [`LatLng`](base.LatLng.md)[]

获取道路坐标点列表

#### Returns

``null`` \| [`LatLng`](base.LatLng.md)[]

经纬度坐标列表（可能为 null）

___

### toDrawItem

▸ **toDrawItem**(): ``null`` \| `default`

#### Returns

``null`` \| `default`

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
