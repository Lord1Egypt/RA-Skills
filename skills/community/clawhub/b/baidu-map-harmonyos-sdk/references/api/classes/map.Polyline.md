[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Polyline

# Class: Polyline

[map](../modules/map.md).Polyline

Polyline覆盖物

**`Abstract`**

提供Polyline覆盖物创建、操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- [`Overlay`](map.Overlay.md)

  ↳ **`Polyline`**

## Table of contents

### Constructors

- [constructor](map.Polyline.md#constructor)

### Properties

- [uuid](map.Polyline.md#uuid)
- [type](map.Polyline.md#type)
- [eventListener](map.Polyline.md#eventlistener)
- [isDestroyed](map.Polyline.md#isdestroyed)

### Accessors

- [visible](map.Polyline.md#visible)
- [zIndex](map.Polyline.md#zindex)
- [typeName](map.Polyline.md#typename)

### Methods

- [putPointsInfoIntoBundle](map.Polyline.md#putpointsinfointobundle)
- [addEventListener](map.Polyline.md#addeventlistener)
- [removeEventListener](map.Polyline.md#removeeventlistener)
- [addDragListener](map.Polyline.md#adddraglistener)
- [removeDragListener](map.Polyline.md#removedraglistener)
- [getDragListener](map.Polyline.md#getdraglistener)
- [fireEvent](map.Polyline.md#fireevent)
- [getType](map.Polyline.md#gettype)
- [setAnimation](map.Polyline.md#setanimation)
- [getAnimation](map.Polyline.md#getanimation)
- [setVisible](map.Polyline.md#setvisible)
- [getVisible](map.Polyline.md#getvisible)
- [alpha](map.Polyline.md#alpha)
- [getAlpha](map.Polyline.md#getalpha)
- [setAlpha](map.Polyline.md#setalpha)
- [startLevel](map.Polyline.md#startlevel)
- [getStartLevel](map.Polyline.md#getstartlevel)
- [setStartLevel](map.Polyline.md#setstartlevel)
- [endLevel](map.Polyline.md#endlevel)
- [showLevel](map.Polyline.md#showlevel)
- [getEndLevel](map.Polyline.md#getendlevel)
- [setShowLevel](map.Polyline.md#setshowlevel)
- [setEndLevel](map.Polyline.md#setendlevel)
- [clickable](map.Polyline.md#clickable)
- [getClickable](map.Polyline.md#getclickable)
- [setClickable](map.Polyline.md#setclickable)
- [setZIndex](map.Polyline.md#setzindex)
- [getZIndex](map.Polyline.md#getzindex)
- [setExtraInfo](map.Polyline.md#setextrainfo)
- [getExtraInfo](map.Polyline.md#getextrainfo)
- [getBmDrawItem](map.Polyline.md#getbmdrawitem)
- [update](map.Polyline.md#update)
- [remove](map.Polyline.md#remove)
- [isRemoved](map.Polyline.md#isremoved)
- [destroy](map.Polyline.md#destroy)
- [setTrackForwardStyle](map.Polyline.md#settrackforwardstyle)
- [setTrackBackwardStyle](map.Polyline.md#settrackbackwardstyle)
- [setTrackForwardStyles](map.Polyline.md#settrackforwardstyles)
- [setTrackBackwardStyles](map.Polyline.md#settrackbackwardstyles)
- [textureOption](map.Polyline.md#textureoption)
- [setTextureOption](map.Polyline.md#settextureoption)
- [getTextureOption](map.Polyline.md#gettextureoption)
- [getColor](map.Polyline.md#getcolor)
- [color](map.Polyline.md#color)
- [setColor](map.Polyline.md#setcolor)
- [getPoints](map.Polyline.md#getpoints)
- [points](map.Polyline.md#points)
- [setPoints](map.Polyline.md#setpoints)
- [getWidth](map.Polyline.md#getwidth)
- [width](map.Polyline.md#width)
- [setWidth](map.Polyline.md#setwidth)
- [getStrokeWidth](map.Polyline.md#getstrokewidth)
- [strokeWidth](map.Polyline.md#strokewidth)
- [setStrokeWidth](map.Polyline.md#setstrokewidth)
- [getStrokeColor](map.Polyline.md#getstrokecolor)
- [strokeColor](map.Polyline.md#strokecolor)
- [setStrokeColor](map.Polyline.md#setstrokecolor)
- [getJoinType](map.Polyline.md#getjointype)
- [joinType](map.Polyline.md#jointype)
- [setJoinType](map.Polyline.md#setjointype)
- [getCapType](map.Polyline.md#getcaptype)
- [capType](map.Polyline.md#captype)
- [setCapType](map.Polyline.md#setcaptype)
- [startCap](map.Polyline.md#startcap)
- [setStartCap](map.Polyline.md#setstartcap)
- [getStartCap](map.Polyline.md#getstartcap)
- [endCap](map.Polyline.md#endcap)
- [setEndCap](map.Polyline.md#setendcap)
- [getEndCap](map.Polyline.md#getendcap)
- [getIsThined](map.Polyline.md#getisthined)
- [isThined](map.Polyline.md#isthined)
- [setIsThined](map.Polyline.md#setisthined)
- [thinFactor](map.Polyline.md#thinfactor)
- [setThinFactor](map.Polyline.md#setthinfactor)
- [getThinFactor](map.Polyline.md#getthinfactor)
- [collisionBehavior](map.Polyline.md#collisionbehavior)
- [setCollisionBehavior](map.Polyline.md#setcollisionbehavior)
- [getCollisionBehavior](map.Polyline.md#getcollisionbehavior)
- [getDirectionCross180](map.Polyline.md#getdirectioncross180)
- [directionCross180](map.Polyline.md#directioncross180)
- [setDirectionCross180](map.Polyline.md#setdirectioncross180)
- [getGeodesic](map.Polyline.md#getgeodesic)
- [isGeodesic](map.Polyline.md#isgeodesic)
- [setGeodesic](map.Polyline.md#setgeodesic)
- [getIsDotted](map.Polyline.md#getisdotted)
- [isDottedline](map.Polyline.md#isdottedline)
- [setIsDottedline](map.Polyline.md#setisdottedline)
- [getDottedLineType](map.Polyline.md#getdottedlinetype)
- [dottedLineType](map.Polyline.md#dottedlinetype)
- [setDottedLineType](map.Polyline.md#setdottedlinetype)
- [textures](map.Polyline.md#textures)
- [getTextures](map.Polyline.md#gettextures)
- [setTexture](map.Polyline.md#settexture)
- [setTextures](map.Polyline.md#settextures)
- [colorList](map.Polyline.md#colorlist)
- [setColorList](map.Polyline.md#setcolorlist)
- [getColorList](map.Polyline.md#getcolorlist)
- [indexList](map.Polyline.md#indexlist)
- [setIndexList](map.Polyline.md#setindexlist)
- [getIndexList](map.Polyline.md#getindexlist)
- [isGradient](map.Polyline.md#isgradient)
- [setIsGradient](map.Polyline.md#setisgradient)
- [getIsGradient](map.Polyline.md#getisgradient)
- [lineBloomType](map.Polyline.md#linebloomtype)
- [setLineBloomType](map.Polyline.md#setlinebloomtype)
- [getLineBloomType](map.Polyline.md#getlinebloomtype)
- [lineBloomWidth](map.Polyline.md#linebloomwidth)
- [setLineBloomWidth](map.Polyline.md#setlinebloomwidth)
- [getLineBloomWidth](map.Polyline.md#getlinebloomwidth)
- [lineBloomAlpha](map.Polyline.md#linebloomalpha)
- [setLineBloomAlpha](map.Polyline.md#setlinebloomalpha)
- [getLineBloomAlpha](map.Polyline.md#getlinebloomalpha)
- [lineBloomGradientASPeed](map.Polyline.md#linebloomgradientaspeed)
- [setLineBloomGradientASPeed](map.Polyline.md#setlinebloomgradientaspeed)
- [getLineBloomGradientASPeed](map.Polyline.md#getlinebloomgradientaspeed)
- [lineBloomBlurTimes](map.Polyline.md#linebloomblurtimes)
- [setLineBloomBlurTimes](map.Polyline.md#setlinebloomblurtimes)
- [getLineBloomBlurTimes](map.Polyline.md#getlinebloomblurtimes)
- [smooth](map.Polyline.md#smooth)
- [setSmooth](map.Polyline.md#setsmooth)
- [getSmooth](map.Polyline.md#getsmooth)
- [smoothFactor](map.Polyline.md#smoothfactor)
- [setSmoothFactor](map.Polyline.md#setsmoothfactor)
- [getSmoothFactor](map.Polyline.md#getsmoothfactor)
- [toString](map.Polyline.md#tostring)

## Constructors

### constructor

• **new Polyline**(`opts?`): [`Polyline`](map.Polyline.md)

构造函数，默认参数
```Typescript
{
points: [],
width: 20;
textures: [],
join: SysEnum.LineJoinType.BEVEL,
cap: SysEnum.LineCapType.BUTT,
isGeodesic: false,
directionCross180: SysEnum.LineDirectionCross.NONE;,
fillcolor: 'rgba(255, 235, 59 ,0.7)',
isThined: false,
dottedline: false,
dottedlineType: SysEnum.PolylineDottedLineType.DOTTED_LINE_SQUARE
}

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts?` | [`Nullable`](../modules/map.md#nullable)\<[`IPolylineOption`](../interfaces/map.IPolylineOption.md)\> |

#### Returns

[`Polyline`](map.Polyline.md)

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

▸ **alpha**(`alpha`): [`Polyline`](map.Polyline.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Polyline`](map.Polyline.md)

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

▸ **startLevel**(`startLevel`): [`Polyline`](map.Polyline.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Polyline`](map.Polyline.md)

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

▸ **endLevel**(`endLevel`): [`Polyline`](map.Polyline.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Polyline`](map.Polyline.md)

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

▸ **clickable**(`isClickable`): [`Polyline`](map.Polyline.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Polyline`](map.Polyline.md)

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

### setTrackForwardStyle

▸ **setTrackForwardStyle**(`forwardStyle`): `void`

PolyLine有trackAnimation时，还未执行的进度，当前点前方的样式
注：不适用于多纹理/多颜色线段绘制

#### Parameters

| Name | Type |
| :------ | :------ |
| `forwardStyle` | [`LineStyle`](map.LineStyle.md) |

#### Returns

`void`

___

### setTrackBackwardStyle

▸ **setTrackBackwardStyle**(`backwardStyle`): `void`

PolyLine有TrackAnimation时，已执行过的进度，当前点后方的样式
  注：不适用于多纹理/多颜色线段绘制

#### Parameters

| Name | Type |
| :------ | :------ |
| `backwardStyle` | [`LineStyle`](map.LineStyle.md) |

#### Returns

`void`

___

### setTrackForwardStyles

▸ **setTrackForwardStyles**(`forwardStyles`): `void`

PolyLine有trackAnimation时，还未执行的进度，当前点前方的样式
注：仅适用于多纹理/多颜色的polyline，数组长度必须和纹理/颜色数组的长度相等

#### Parameters

| Name | Type |
| :------ | :------ |
| `forwardStyles` | [`LineStyle`](map.LineStyle.md)[] |

#### Returns

`void`

___

### setTrackBackwardStyles

▸ **setTrackBackwardStyles**(`backwardStyles`): `void`

PolyLine有trackAnimation时，还未执行的进度，当前点前方的样式
注：仅适用于多纹理/多颜色的polyline，数组长度必须和纹理/颜色数组的长度相等

#### Parameters

| Name | Type |
| :------ | :------ |
| `backwardStyles` | [`LineStyle`](map.LineStyle.md)[] |

#### Returns

`void`

___

### textureOption

▸ **textureOption**(`val`): [`Polyline`](map.Polyline.md)

设置纹理填充样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`TextureOption`](../enums/map.SysEnum.TextureOption.md) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.2.0

___

### setTextureOption

▸ **setTextureOption**(`val`): `void`

设置纹理填充样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`TextureOption`](../enums/map.SysEnum.TextureOption.md) |

#### Returns

`void`

**`Since`**

1.2.0

___

### getTextureOption

▸ **getTextureOption**(): [`TextureOption`](../enums/map.SysEnum.TextureOption.md)

获取纹理填充样式

#### Returns

[`TextureOption`](../enums/map.SysEnum.TextureOption.md)

**`Since`**

1.2.0

___

### getColor

▸ **getColor**(): `string`

获取线颜色

#### Returns

`string`

**`Since`**

1.0.0

___

### color

▸ **color**(`color`): [`Polyline`](map.Polyline.md)

设置线颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setColor

▸ **setColor**(`color`): `void`

设置线颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getPoints

▸ **getPoints**(): [`LatLng`](base.LatLng.md)[]

获取线图形坐标点串

#### Returns

[`LatLng`](base.LatLng.md)[]

**`Since`**

1.0.0

___

### points

▸ **points**(`points`): [`Polyline`](map.Polyline.md)

设置线图形坐标点串

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setPoints

▸ **setPoints**(`points`): `void`

设置线图形坐标点串

#### Parameters

| Name | Type |
| :------ | :------ |
| `points` | [`LatLng`](base.LatLng.md)[] |

#### Returns

`void`

**`Since`**

1.0.0

___

### getWidth

▸ **getWidth**(): `number`

获取线宽

#### Returns

`number`

**`Since`**

1.0.0

___

### width

▸ **width**(`width`): [`Polyline`](map.Polyline.md)

设置线宽

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setWidth

▸ **setWidth**(`width`): `void`

设置线宽

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### getStrokeWidth

▸ **getStrokeWidth**(): `number`

获取描边线宽

#### Returns

`number`

**`Since`**

1.2.0

___

### strokeWidth

▸ **strokeWidth**(`width`): [`Polyline`](map.Polyline.md)

设置描边线宽

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.2.0

___

### setStrokeWidth

▸ **setStrokeWidth**(`width`): `void`

设置描边线宽

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getStrokeColor

▸ **getStrokeColor**(): `string`

获取描边线颜色

#### Returns

`string`

**`Since`**

1.2.0

___

### strokeColor

▸ **strokeColor**(`color`): [`Polyline`](map.Polyline.md)

设置描边线颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.2.0

___

### setStrokeColor

▸ **setStrokeColor**(`color`): `void`

设置描边线颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.2.0

___

### getJoinType

▸ **getJoinType**(): [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md)

获取线拐点类型

#### Returns

[`LineJoinType`](../enums/map.SysEnum.LineJoinType.md)

**`Since`**

1.0.0

___

### joinType

▸ **joinType**(`type`): [`Polyline`](map.Polyline.md)

设置线拐点类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setJoinType

▸ **setJoinType**(`type`): `void`

设置线拐点类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getCapType

▸ **getCapType**(): [`LineCapType`](../enums/map.SysEnum.LineCapType.md)

获取线端点样式类型

#### Returns

[`LineCapType`](../enums/map.SysEnum.LineCapType.md)

**`Since`**

1.0.0

___

### capType

▸ **capType**(`type`): [`Polyline`](map.Polyline.md)

设置线端点样式类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`LineCapType`](../enums/map.SysEnum.LineCapType.md) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setCapType

▸ **setCapType**(`type`): `void`

设置线端点样式类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`LineCapType`](../enums/map.SysEnum.LineCapType.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### startCap

▸ **startCap**(`val`): [`Polyline`](map.Polyline.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`LineCapType`](../enums/map.SysEnum.LineCapType.md) |

#### Returns

[`Polyline`](map.Polyline.md)

___

### setStartCap

▸ **setStartCap**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`LineCapType`](../enums/map.SysEnum.LineCapType.md) |

#### Returns

`void`

___

### getStartCap

▸ **getStartCap**(): [`LineCapType`](../enums/map.SysEnum.LineCapType.md)

#### Returns

[`LineCapType`](../enums/map.SysEnum.LineCapType.md)

___

### endCap

▸ **endCap**(`val`): [`Polyline`](map.Polyline.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`LineCapType`](../enums/map.SysEnum.LineCapType.md) |

#### Returns

[`Polyline`](map.Polyline.md)

___

### setEndCap

▸ **setEndCap**(`val`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`LineCapType`](../enums/map.SysEnum.LineCapType.md) |

#### Returns

`void`

___

### getEndCap

▸ **getEndCap**(): [`LineCapType`](../enums/map.SysEnum.LineCapType.md)

#### Returns

[`LineCapType`](../enums/map.SysEnum.LineCapType.md)

___

### getIsThined

▸ **getIsThined**(): `boolean`

获取是否启用抽稀

#### Returns

`boolean`

**`Since`**

1.0.0

___

### isThined

▸ **isThined**(`isThined`): `undefined` \| [`Polyline`](map.Polyline.md)

设置是否启用抽稀

#### Parameters

| Name | Type |
| :------ | :------ |
| `isThined` | `boolean` |

#### Returns

`undefined` \| [`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setIsThined

▸ **setIsThined**(`isThined`): `void`

设置是否启用抽稀

#### Parameters

| Name | Type |
| :------ | :------ |
| `isThined` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

___

### thinFactor

▸ **thinFactor**(`val`): [`Polyline`](map.Polyline.md)

设置抽稀容差值

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.2.0

___

### setThinFactor

▸ **setThinFactor**(`val`): `void`

设置抽稀容差值

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

### collisionBehavior

▸ **collisionBehavior**(`behave`): [`Polyline`](map.Polyline.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `behave` | [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md) |

#### Returns

[`Polyline`](map.Polyline.md)

___

### setCollisionBehavior

▸ **setCollisionBehavior**(`behave`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `behave` | [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md) |

#### Returns

`void`

___

### getCollisionBehavior

▸ **getCollisionBehavior**(): [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md)

#### Returns

[`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md)

___

### getDirectionCross180

▸ **getDirectionCross180**(): [`LineDirectionCross`](../enums/map.SysEnum.LineDirectionCross.md)

获取是否启用跨越180度

#### Returns

[`LineDirectionCross`](../enums/map.SysEnum.LineDirectionCross.md)

**`Since`**

1.0.0

___

### directionCross180

▸ **directionCross180**(`cross`): [`Polyline`](map.Polyline.md)

设置是否启用跨越180度

#### Parameters

| Name | Type |
| :------ | :------ |
| `cross` | [`LineDirectionCross`](../enums/map.SysEnum.LineDirectionCross.md) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setDirectionCross180

▸ **setDirectionCross180**(`cross`): `void`

设置是否启用跨越180度

#### Parameters

| Name | Type |
| :------ | :------ |
| `cross` | [`LineDirectionCross`](../enums/map.SysEnum.LineDirectionCross.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getGeodesic

▸ **getGeodesic**(): `boolean`

获取是否启用绘制大地线

#### Returns

`boolean`

**`Since`**

1.0.0

___

### isGeodesic

▸ **isGeodesic**(`geodesic`): [`Polyline`](map.Polyline.md)

设置是否启用绘制大地线

#### Parameters

| Name | Type |
| :------ | :------ |
| `geodesic` | `boolean` |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setGeodesic

▸ **setGeodesic**(`geodesic`): `void`

设置是否启用绘制大地线

#### Parameters

| Name | Type |
| :------ | :------ |
| `geodesic` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

___

### getIsDotted

▸ **getIsDotted**(): `boolean`

获取是否启用虚线样式

#### Returns

`boolean`

**`Since`**

1.0.0

___

### isDottedline

▸ **isDottedline**(`dotted`): `undefined` \| [`Polyline`](map.Polyline.md)

设置是否启用虚线样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `dotted` | `boolean` |

#### Returns

`undefined` \| [`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setIsDottedline

▸ **setIsDottedline**(`dotted`): `void`

设置是否启用虚线样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `dotted` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

___

### getDottedLineType

▸ **getDottedLineType**(): [`PolylineDottedLineType`](../enums/map.SysEnum.PolylineDottedLineType.md)

获取虚线样式

#### Returns

[`PolylineDottedLineType`](../enums/map.SysEnum.PolylineDottedLineType.md)

**`Since`**

1.0.0

___

### dottedLineType

▸ **dottedLineType**(`val`): [`Polyline`](map.Polyline.md)

设置虚线样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`PolylineDottedLineType`](../enums/map.SysEnum.PolylineDottedLineType.md) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.0.0

___

### setDottedLineType

▸ **setDottedLineType**(`val`): `void`

设置虚线样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`PolylineDottedLineType`](../enums/map.SysEnum.PolylineDottedLineType.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### textures

▸ **textures**(`textures`): `Promise`\<[`Polyline`](map.Polyline.md)\>

设置填充纹理

#### Parameters

| Name | Type |
| :------ | :------ |
| `textures` | [`ImageEntity`](map.ImageEntity.md)[] |

#### Returns

`Promise`\<[`Polyline`](map.Polyline.md)\>

**`Since`**

1.0.0

___

### getTextures

▸ **getTextures**(): [`ImageEntity`](map.ImageEntity.md)[]

获取填充纹理

#### Returns

[`ImageEntity`](map.ImageEntity.md)[]

**`Since`**

1.0.0

___

### setTexture

▸ **setTexture**(`texture`): `void`

设置填充纹理

#### Parameters

| Name | Type |
| :------ | :------ |
| `texture` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### setTextures

▸ **setTextures**(`textures`): `void`

设置填充纹理

#### Parameters

| Name | Type |
| :------ | :------ |
| `textures` | [`ImageEntity`](map.ImageEntity.md)[] |

#### Returns

`void`

**`Since`**

1.0.0

___

### colorList

▸ **colorList**(`cList`): `undefined` \| [`Polyline`](map.Polyline.md)

设置填充颜色列表

#### Parameters

| Name | Type |
| :------ | :------ |
| `cList` | [`ColorString`](../modules/map.md#colorstring)[] |

#### Returns

`undefined` \| [`Polyline`](map.Polyline.md)

**`Since`**

1.1.0

___

### setColorList

▸ **setColorList**(`cList`): `void`

设置填充颜色列表

#### Parameters

| Name | Type |
| :------ | :------ |
| `cList` | [`ColorString`](../modules/map.md#colorstring)[] |

#### Returns

`void`

**`Since`**

1.1.0

___

### getColorList

▸ **getColorList**(): `string`[]

获取填充颜色列表

#### Returns

`string`[]

**`Since`**

1.1.0

___

### indexList

▸ **indexList**(`iList`): [`Polyline`](map.Polyline.md)

设置多纹理的索引

#### Parameters

| Name | Type |
| :------ | :------ |
| `iList` | `number`[] |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.1.0

___

### setIndexList

▸ **setIndexList**(`iList`): `void`

设置多纹理的索引

#### Parameters

| Name | Type |
| :------ | :------ |
| `iList` | `number`[] |

#### Returns

`void`

**`Since`**

1.1.0

___

### getIndexList

▸ **getIndexList**(): `number`[]

获取多纹理的索引

#### Returns

`number`[]

**`Since`**

1.1.0

___

### isGradient

▸ **isGradient**(`enable`): `undefined` \| [`Polyline`](map.Polyline.md)

设置是否是渐变线

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `boolean` |

#### Returns

`undefined` \| [`Polyline`](map.Polyline.md)

**`Since`**

1.1.0

___

### setIsGradient

▸ **setIsGradient**(`enable`): `void`

设置是否是渐变线

#### Parameters

| Name | Type |
| :------ | :------ |
| `enable` | `boolean` |

#### Returns

`void`

**`Since`**

1.1.0

___

### getIsGradient

▸ **getIsGradient**(): `boolean`

是否是渐变线

#### Returns

`boolean`

**`Since`**

1.1.0

___

### lineBloomType

▸ **lineBloomType**(`type`): [`Polyline`](map.Polyline.md)

设置发光样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`ELineBloomType`](../enums/map.SysEnum.ELineBloomType.md) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.1.0

___

### setLineBloomType

▸ **setLineBloomType**(`type`): `void`

设置发光样式

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`ELineBloomType`](../enums/map.SysEnum.ELineBloomType.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### getLineBloomType

▸ **getLineBloomType**(): [`ELineBloomType`](../enums/map.SysEnum.ELineBloomType.md)

获取发光样式

#### Returns

[`ELineBloomType`](../enums/map.SysEnum.ELineBloomType.md)

**`Since`**

1.1.0

___

### lineBloomWidth

▸ **lineBloomWidth**(`bloomWidth`): [`Polyline`](map.Polyline.md)

设置发光线段的宽度 宽度 >0

#### Parameters

| Name | Type |
| :------ | :------ |
| `bloomWidth` | `number` |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.1.0

___

### setLineBloomWidth

▸ **setLineBloomWidth**(`bloomWidth`): `void`

设置发光线段的宽度 宽度 >0

#### Parameters

| Name | Type |
| :------ | :------ |
| `bloomWidth` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

___

### getLineBloomWidth

▸ **getLineBloomWidth**(): `number`

获取发光线段的宽度

#### Returns

`number`

**`Since`**

1.1.0

___

### lineBloomAlpha

▸ **lineBloomAlpha**(`bloomAlpha`): `void`

设置发光线段的透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bloomAlpha` | `number` | 取值范围0～1 |

#### Returns

`void`

**`Since`**

1.1.0

___

### setLineBloomAlpha

▸ **setLineBloomAlpha**(`bloomAlpha`): `void`

设置发光线段的透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `bloomAlpha` | `number` | 取值范围0～1 |

#### Returns

`void`

**`Since`**

1.1.0

___

### getLineBloomAlpha

▸ **getLineBloomAlpha**(): `number`

获取发光线段的透明度

#### Returns

`number`

**`Since`**

1.1.0

___

### lineBloomGradientASPeed

▸ **lineBloomGradientASPeed**(`speed`): [`Polyline`](map.Polyline.md)

设置透明度渐变发光效果的渐变速率

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `speed` | `number` | 取值范围1.0 ~ 10.0 |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.1.0

___

### setLineBloomGradientASPeed

▸ **setLineBloomGradientASPeed**(`speed`): `void`

设置透明度渐变发光效果的渐变速率

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `speed` | `number` | 取值范围1.0 ~ 10.0 |

#### Returns

`void`

**`Since`**

1.1.0

___

### getLineBloomGradientASPeed

▸ **getLineBloomGradientASPeed**(): `number`

获取透明度渐变发光效果的渐变速率

#### Returns

`number`

**`Since`**

1.1.0

___

### lineBloomBlurTimes

▸ **lineBloomBlurTimes**(`times`): [`Polyline`](map.Polyline.md)

设置模糊发光效果的模糊次数

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `times` | `number` | 取值范围 1~10 |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.1.0

___

### setLineBloomBlurTimes

▸ **setLineBloomBlurTimes**(`times`): `void`

设置模糊发光效果的模糊次数

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `times` | `number` | 取值范围 1~10 |

#### Returns

`void`

**`Since`**

1.1.0

___

### getLineBloomBlurTimes

▸ **getLineBloomBlurTimes**(): `number`

模糊发光效果的模糊次数

#### Returns

`number`

**`Since`**

1.1.0

___

### smooth

▸ **smooth**(`val`): [`Polyline`](map.Polyline.md)

设置平滑类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`SmoothType`](../enums/map.SysEnum.SmoothType.md) |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.2.0

___

### setSmooth

▸ **setSmooth**(`val`): `void`

设置平滑类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`SmoothType`](../enums/map.SysEnum.SmoothType.md) |

#### Returns

`void`

**`Since`**

1.2.0

___

### getSmooth

▸ **getSmooth**(): (`val`: [`SmoothType`](../enums/map.SysEnum.SmoothType.md)) => [`Polyline`](map.Polyline.md)

获取平滑类型

#### Returns

`fn`

▸ (`val`): [`Polyline`](map.Polyline.md)

设置平滑类型

##### Parameters

| Name | Type |
| :------ | :------ |
| `val` | [`SmoothType`](../enums/map.SysEnum.SmoothType.md) |

##### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.2.0

**`Since`**

1.2.0

___

### smoothFactor

▸ **smoothFactor**(`val`): [`Polyline`](map.Polyline.md)

设置平滑控制值

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

[`Polyline`](map.Polyline.md)

**`Since`**

1.2.0

___

### setSmoothFactor

▸ **setSmoothFactor**(`val`): `void`

设置平滑控制值

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getSmoothFactor

▸ **getSmoothFactor**(): `number`

获取平滑控制值

#### Returns

`number`

**`Since`**

1.2.0

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

**`Since`**

1.0.1

#### Overrides

[Overlay](map.Overlay.md).[toString](map.Overlay.md#tostring)
