[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Label

# Class: Label

[map](../modules/map.md).Label

Label覆盖物

**`Abstract`**

提供Label覆盖物创建、操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- `default`

  ↳ **`Label`**

## Table of contents

### Constructors

- [constructor](map.Label.md#constructor)

### Properties

- [uuid](map.Label.md#uuid)
- [type](map.Label.md#type)
- [eventListener](map.Label.md#eventlistener)
- [isDestroyed](map.Label.md#isdestroyed)

### Accessors

- [typeName](map.Label.md#typename)
- [visible](map.Label.md#visible)
- [zIndex](map.Label.md#zindex)

### Methods

- [scaleX](map.Label.md#scalex)
- [getScaleX](map.Label.md#getscalex)
- [setScaleX](map.Label.md#setscalex)
- [scaleY](map.Label.md#scaley)
- [getScaleY](map.Label.md#getscaley)
- [setScaleY](map.Label.md#setscaley)
- [setScale](map.Label.md#setscale)
- [yOffset](map.Label.md#yoffset)
- [getYOffset](map.Label.md#getyoffset)
- [setYOffset](map.Label.md#setyoffset)
- [xOffset](map.Label.md#xoffset)
- [getXOffset](map.Label.md#getxoffset)
- [setXOffset](map.Label.md#setxoffset)
- [draggable](map.Label.md#draggable)
- [getDraggable](map.Label.md#getdraggable)
- [setDraggable](map.Label.md#setdraggable)
- [flat](map.Label.md#flat)
- [getFlat](map.Label.md#getflat)
- [setFlat](map.Label.md#setflat)
- [period](map.Label.md#period)
- [getPeriod](map.Label.md#getperiod)
- [setPeriod](map.Label.md#setperiod)
- [position](map.Label.md#position)
- [getPosition](map.Label.md#getposition)
- [setPosition](map.Label.md#setposition)
- [setBmPosition](map.Label.md#setbmposition)
- [changePosition](map.Label.md#changeposition)
- [popView](map.Label.md#popview)
- [setPopView](map.Label.md#setpopview)
- [getPopView](map.Label.md#getpopview)
- [located](map.Label.md#located)
- [setLocated](map.Label.md#setlocated)
- [getLocated](map.Label.md#getlocated)
- [anchor](map.Label.md#anchor)
- [getAnchor](map.Label.md#getanchor)
- [setAnchor](map.Label.md#setanchor)
- [getRotate](map.Label.md#getrotate)
- [setRotate](map.Label.md#setrotate)
- [isJoinCollision](map.Label.md#isjoincollision)
- [getIsJoinCollision](map.Label.md#getisjoincollision)
- [setIsJoinCollision](map.Label.md#setisjoincollision)
- [isFixed](map.Label.md#isfixed)
- [setIsFixed](map.Label.md#setisfixed)
- [getFixedScreen](map.Label.md#getfixedscreen)
- [isRotateItem](map.Label.md#isrotateitem)
- [getIsRotateItem](map.Label.md#getisrotateitem)
- [setIsRotateItem](map.Label.md#setisrotateitem)
- [isRotateNorth](map.Label.md#isrotatenorth)
- [getIsRotateNorth](map.Label.md#getisrotatenorth)
- [setIsRotateNorth](map.Label.md#setisrotatenorth)
- [fixedScreenPosition](map.Label.md#fixedscreenposition)
- [setFixedScreenPosition](map.Label.md#setfixedscreenposition)
- [perspective](map.Label.md#perspective)
- [getPerspective](map.Label.md#getperspective)
- [setPerspective](map.Label.md#setperspective)
- [priority](map.Label.md#priority)
- [getPriority](map.Label.md#getpriority)
- [setPriority](map.Label.md#setpriority)
- [toDrawItem](map.Label.md#todrawitem)
- [getText](map.Label.md#gettext)
- [text](map.Label.md#text)
- [setText](map.Label.md#settext)
- [getFontColor](map.Label.md#getfontcolor)
- [fontcolor](map.Label.md#fontcolor)
- [setFontColor](map.Label.md#setfontcolor)
- [getBorderColor](map.Label.md#getbordercolor)
- [borderColor](map.Label.md#bordercolor)
- [setBorderColor](map.Label.md#setbordercolor)
- [borderSize](map.Label.md#bordersize)
- [setBorderSize](map.Label.md#setbordersize)
- [getBorderSize](map.Label.md#getbordersize)
- [getBgColor](map.Label.md#getbgcolor)
- [bgcolor](map.Label.md#bgcolor)
- [setBgColor](map.Label.md#setbgcolor)
- [getFontSize](map.Label.md#getfontsize)
- [fontSize](map.Label.md#fontsize)
- [setFontSize](map.Label.md#setfontsize)
- [getFontType](map.Label.md#getfonttype)
- [fontType](map.Label.md#fonttype)
- [setFontType](map.Label.md#setfonttype)
- [getAlign](map.Label.md#getalign)
- [align](map.Label.md#align)
- [setAlign](map.Label.md#setalign)
- [toString](map.Label.md#tostring)
- [putPointsInfoIntoBundle](map.Label.md#putpointsinfointobundle)
- [addEventListener](map.Label.md#addeventlistener)
- [removeEventListener](map.Label.md#removeeventlistener)
- [addDragListener](map.Label.md#adddraglistener)
- [removeDragListener](map.Label.md#removedraglistener)
- [getDragListener](map.Label.md#getdraglistener)
- [fireEvent](map.Label.md#fireevent)
- [getType](map.Label.md#gettype)
- [setAnimation](map.Label.md#setanimation)
- [getAnimation](map.Label.md#getanimation)
- [setVisible](map.Label.md#setvisible)
- [getVisible](map.Label.md#getvisible)
- [alpha](map.Label.md#alpha)
- [getAlpha](map.Label.md#getalpha)
- [setAlpha](map.Label.md#setalpha)
- [startLevel](map.Label.md#startlevel)
- [getStartLevel](map.Label.md#getstartlevel)
- [setStartLevel](map.Label.md#setstartlevel)
- [endLevel](map.Label.md#endlevel)
- [showLevel](map.Label.md#showlevel)
- [getEndLevel](map.Label.md#getendlevel)
- [setShowLevel](map.Label.md#setshowlevel)
- [setEndLevel](map.Label.md#setendlevel)
- [clickable](map.Label.md#clickable)
- [getClickable](map.Label.md#getclickable)
- [setClickable](map.Label.md#setclickable)
- [setZIndex](map.Label.md#setzindex)
- [getZIndex](map.Label.md#getzindex)
- [setExtraInfo](map.Label.md#setextrainfo)
- [getExtraInfo](map.Label.md#getextrainfo)
- [getBmDrawItem](map.Label.md#getbmdrawitem)
- [update](map.Label.md#update)
- [remove](map.Label.md#remove)
- [isRemoved](map.Label.md#isremoved)
- [destroy](map.Label.md#destroy)

## Constructors

### constructor

• **new Label**(`opts?`): [`Label`](map.Label.md)

构造函数，默认参数如下
``` Typescript
{
    text: '',
    position: new LatLng(39.914935, 116.403119),
    bgcolorstr: '#999',
    fontcolorstr: '#fff',
    fontsize: 12,
    fontType: SysEnum.FontType.NORMAL,
    rotate: 0,
    alignX: SysEnum.FontAlign.ALIGN_CENTER_HORIZONTAL,
    alignY: SysEnum.FontAlign.ALIGN_CENTER_VERTICAL
}

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts?` | [`ILabelOption`](../interfaces/map.ILabelOption.md) |

#### Returns

[`Label`](map.Label.md)

#### Overrides

BaseMarker.constructor

## Properties

### uuid

• **uuid**: `string`

#### Inherited from

BaseMarker.uuid

___

### type

• **type**: `default`

#### Inherited from

BaseMarker.type

___

### eventListener

• **eventListener**: `TOverlayListener` = `{}`

#### Inherited from

BaseMarker.eventListener

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

#### Inherited from

BaseMarker.isDestroyed

## Accessors

### typeName

• `get` **typeName**(): `string`

#### Returns

`string`

#### Overrides

BaseMarker.typeName

___

### visible

• `get` **visible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.visible

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

BaseMarker.visible

___

### zIndex

• `get` **zIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.zIndex

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

BaseMarker.zIndex

## Methods

### scaleX

▸ **scaleX**(`scaleX`): [`Label`](map.Label.md)

设置X轴图标缩放比例

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `scaleX` | `number` | 取值范围[0,} |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.scaleX

___

### getScaleX

▸ **getScaleX**(): `number`

获取X轴图标缩放比例

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getScaleX

___

### setScaleX

▸ **setScaleX**(`scaleX`): `void`

设置X轴图标缩放比例

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `scaleX` | `number` | 取值范围[0,} |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setScaleX

___

### scaleY

▸ **scaleY**(`scaleY`): [`Label`](map.Label.md)

设置Y轴图标缩放比例

#### Parameters

| Name | Type |
| :------ | :------ |
| `scaleY` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.scaleY

___

### getScaleY

▸ **getScaleY**(): `number`

获取Y轴图标缩放比例

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getScaleY

___

### setScaleY

▸ **setScaleY**(`scaleY`): `void`

设置Y轴图标缩放比例

#### Parameters

| Name | Type |
| :------ | :------ |
| `scaleY` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setScaleY

___

### setScale

▸ **setScale**(`scaleX`, `scaleY`): `void`

设置缩放比例

#### Parameters

| Name | Type |
| :------ | :------ |
| `scaleX` | `number` |
| `scaleY` | `number` |

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

BaseMarker.setScale

___

### yOffset

▸ **yOffset**(`yOffset`): [`Label`](map.Label.md)

设置Y轴图标偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `yOffset` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.yOffset

___

### getYOffset

▸ **getYOffset**(): `number`

获取Y轴图标偏移量

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getYOffset

___

### setYOffset

▸ **setYOffset**(`yOffset`): `void`

设置Y轴图标偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `yOffset` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setYOffset

___

### xOffset

▸ **xOffset**(`xOffset`): [`Label`](map.Label.md)

设置X轴图标偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `xOffset` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.1.0

#### Inherited from

BaseMarker.xOffset

___

### getXOffset

▸ **getXOffset**(): `number`

获取X轴图标偏移量

#### Returns

`number`

**`Since`**

1.1.0

#### Inherited from

BaseMarker.getXOffset

___

### setXOffset

▸ **setXOffset**(`xOffset`): `void`

设置X轴图标偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `xOffset` | `number` |

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

BaseMarker.setXOffset

___

### draggable

▸ **draggable**(`draggable`): [`Label`](map.Label.md)

设置是否可拖动

#### Parameters

| Name | Type |
| :------ | :------ |
| `draggable` | `boolean` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

2.0.3

#### Inherited from

BaseMarker.draggable

___

### getDraggable

▸ **getDraggable**(): `boolean`

获取是否可拖动状态

#### Returns

`boolean`

**`Since`**

2.0.3

#### Inherited from

BaseMarker.getDraggable

___

### setDraggable

▸ **setDraggable**(`draggable`): `void`

设置是否可拖动

#### Parameters

| Name | Type |
| :------ | :------ |
| `draggable` | `boolean` |

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

BaseMarker.setDraggable

___

### flat

▸ **flat**(`flat`): [`Label`](map.Label.md)

设置贴地模式

#### Parameters

| Name | Type |
| :------ | :------ |
| `flat` | `boolean` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.2.0

#### Inherited from

BaseMarker.flat

___

### getFlat

▸ **getFlat**(): `boolean`

获取是否使用旋转基准是地理北方向

#### Returns

`boolean`

**`Since`**

1.2.0

#### Inherited from

BaseMarker.getFlat

___

### setFlat

▸ **setFlat**(`flat`): `void`

设置是否使用旋转基准是地理北方向

#### Parameters

| Name | Type |
| :------ | :------ |
| `flat` | `boolean` |

#### Returns

`void`

**`Since`**

1.2.0

#### Inherited from

BaseMarker.setFlat

___

### period

▸ **period**(`period`): [`Label`](map.Label.md)

设置多少帧刷新一次图片资源

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `period` | `number` | 帧数，刷新周期，值越小速度越快。默认为20，最小为1 |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.period

___

### getPeriod

▸ **getPeriod**(): `number`

获取多少帧刷新一次图片资源

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getPeriod

___

### setPeriod

▸ **setPeriod**(`period`): `void`

设置多少帧刷新一次图片资源

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `period` | `number` | 帧数，刷新周期，值越小速度越快。默认为20，最小为1 |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setPeriod

___

### position

▸ **position**(`position`): [`Label`](map.Label.md)

设置图标位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `position` | [`LatLng`](base.LatLng.md) |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.position

___

### getPosition

▸ **getPosition**(): [`LatLng`](base.LatLng.md)

获取图标位置

#### Returns

[`LatLng`](base.LatLng.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getPosition

___

### setPosition

▸ **setPosition**(`position`): `void`

设置图标位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `position` | [`LatLng`](base.LatLng.md) |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setPosition

___

### setBmPosition

▸ **setBmPosition**(`position`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `position` | [`Point`](base.Point.md) |

#### Returns

`void`

#### Inherited from

BaseMarker.setBmPosition

___

### changePosition

▸ **changePosition**(`position`): `void`

改变图标位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `position` | [`LatLng`](base.LatLng.md) |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.changePosition

___

### popView

▸ **popView**(`popView`): [`Label`](map.Label.md)

设置消息气泡

#### Parameters

| Name | Type |
| :------ | :------ |
| `popView` | [`PopView`](map.PopView.md) |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.1.0

#### Inherited from

BaseMarker.popView

___

### setPopView

▸ **setPopView**(`popView`): `void`

设置消息气泡

#### Parameters

| Name | Type |
| :------ | :------ |
| `popView` | [`PopView`](map.PopView.md) |

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

BaseMarker.setPopView

___

### getPopView

▸ **getPopView**(): [`Maybe`](../modules/map.md#maybe)\<[`PopView`](map.PopView.md)\>

获取消息气泡

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`PopView`](map.PopView.md)\>

**`Since`**

1.1.0

#### Inherited from

BaseMarker.getPopView

___

### located

▸ **located**(`located`): `void`

设置绘制元素位于「基准Anchor」的方位

#### Parameters

| Name | Type |
| :------ | :------ |
| `located` | [`Located`](../enums/map.SysEnum.Located.md) |

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

BaseMarker.located

___

### setLocated

▸ **setLocated**(`located`): `void`

设置绘制元素位于「基准Anchor」的方位

#### Parameters

| Name | Type |
| :------ | :------ |
| `located` | [`Located`](../enums/map.SysEnum.Located.md) |

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

BaseMarker.setLocated

___

### getLocated

▸ **getLocated**(): [`Located`](../enums/map.SysEnum.Located.md)

获取绘制元素位于「基准Anchor」的方位

#### Returns

[`Located`](../enums/map.SysEnum.Located.md)

**`Since`**

1.1.0

#### Inherited from

BaseMarker.getLocated

___

### anchor

▸ **anchor**(`anchorX`, `anchorY`): [`Label`](map.Label.md)

设置 marker 覆盖物的锚点比例，默认（0.5, 1.0）水平居中，垂直下对齐

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `anchorX` | `number` | 取值范围[0.0 , 1.0]， 否则不生效 |
| `anchorY` | `number` | 取值范围[0.0 , 1.0]， 否则不生效 |

#### Returns

[`Label`](map.Label.md)

**`Deprecated`**

请使用located替代

**`Since`**

1.0.0

#### Inherited from

BaseMarker.anchor

___

### getAnchor

▸ **getAnchor**(): `Record`\<`string`, `number`\>

获取 marker 覆盖物的锚点比例

#### Returns

`Record`\<`string`, `number`\>

**`Deprecated`**

请使用getLocated替代

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getAnchor

___

### setAnchor

▸ **setAnchor**(`anchorX`, `anchorY`): `void`

设置 marker 覆盖物的锚点比例，默认（0.5, 1.0）水平居中，垂直下对齐

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `anchorX` | `number` | 取值范围[0.0 , 1.0]， 否则不生效 |
| `anchorY` | `number` | 取值范围[0.0 , 1.0]， 否则不生效 |

#### Returns

`void`

**`Deprecated`**

请使用setLocated替代

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setAnchor

___

### getRotate

▸ **getRotate**(): `number`

获取旋转角度

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getRotate

___

### setRotate

▸ **setRotate**(`rotate`): `void`

设置旋转角度

#### Parameters

| Name | Type |
| :------ | :------ |
| `rotate` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setRotate

___

### isJoinCollision

▸ **isJoinCollision**(`isJoinCollision`): [`Label`](map.Label.md)

设置marker是否参与碰撞检测

#### Parameters

| Name | Type |
| :------ | :------ |
| `isJoinCollision` | [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md) |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.1.0

#### Inherited from

BaseMarker.isJoinCollision

___

### getIsJoinCollision

▸ **getIsJoinCollision**(): [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md)

获取置marker是否参与碰撞检测

#### Returns

[`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md)

**`Since`**

1.1.0

#### Inherited from

BaseMarker.getIsJoinCollision

___

### setIsJoinCollision

▸ **setIsJoinCollision**(`isJoinCollision`): `void`

设置marker是否参与碰撞检测

#### Parameters

| Name | Type |
| :------ | :------ |
| `isJoinCollision` | [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md) |

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

BaseMarker.setIsJoinCollision

___

### isFixed

▸ **isFixed**(`isFix`): `void`

设置 Marker 覆盖物是否固定屏幕位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `isFix` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.isFixed

___

### setIsFixed

▸ **setIsFixed**(`isFix`): `void`

设置 Marker 覆盖物是否固定屏幕位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `isFix` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setIsFixed

___

### getFixedScreen

▸ **getFixedScreen**(): `boolean`

获取 Marker 是否启用屏幕固定位置

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getFixedScreen

___

### isRotateItem

▸ **isRotateItem**(`isRotateItem`): [`Label`](map.Label.md)

设置是否使用外部设置的Rotate

#### Parameters

| Name | Type |
| :------ | :------ |
| `isRotateItem` | `boolean` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

2.0.4

#### Inherited from

BaseMarker.isRotateItem

___

### getIsRotateItem

▸ **getIsRotateItem**(): `boolean`

获取是否使用外部设置的Rotate

#### Returns

`boolean`

**`Since`**

2.0.4

#### Inherited from

BaseMarker.getIsRotateItem

___

### setIsRotateItem

▸ **setIsRotateItem**(`isRotateItem`): `void`

设置是否使用外部设置的Rotate

#### Parameters

| Name | Type |
| :------ | :------ |
| `isRotateItem` | `boolean` |

#### Returns

`void`

**`Since`**

2.0.4

#### Inherited from

BaseMarker.setIsRotateItem

___

### isRotateNorth

▸ **isRotateNorth**(`isRotateNorth`): [`Label`](map.Label.md)

设置是否使用旋转基准是地理北方向

#### Parameters

| Name | Type |
| :------ | :------ |
| `isRotateNorth` | `boolean` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

2.0.4

#### Inherited from

BaseMarker.isRotateNorth

___

### getIsRotateNorth

▸ **getIsRotateNorth**(): `boolean`

获取是否使用旋转基准是地理北方向

#### Returns

`boolean`

**`Since`**

2.0.4

#### Inherited from

BaseMarker.getIsRotateNorth

___

### setIsRotateNorth

▸ **setIsRotateNorth**(`isRotateNorth`): `void`

设置是否使用旋转基准是地理北方向

#### Parameters

| Name | Type |
| :------ | :------ |
| `isRotateNorth` | `boolean` |

#### Returns

`void`

**`Since`**

2.0.4

#### Inherited from

BaseMarker.setIsRotateNorth

___

### fixedScreenPosition

▸ **fixedScreenPosition**(`point`): [`Label`](map.Label.md)

设置 Marker 覆盖物的屏幕位置,用于固定marker不随地图移动

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point` | [`Nullable`](../modules/map.md#nullable)\<[`Point`](base.Point.md)\> | 如果设置坐标，则代表启用固定屏幕像素坐标显示marker |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.1

#### Inherited from

BaseMarker.fixedScreenPosition

___

### setFixedScreenPosition

▸ **setFixedScreenPosition**(`point`): `void`

设置 Marker 覆盖物的屏幕位置,用于固定marker不随地图移动

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point` | [`Nullable`](../modules/map.md#nullable)\<[`Point`](base.Point.md)\> | 如果设置坐标，则代表启用固定屏幕像素坐标显示marker |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setFixedScreenPosition

___

### perspective

▸ **perspective**(`perspective`): [`Label`](map.Label.md)

设置是否开启 marker 覆盖物近大远小效果，默认开启

#### Parameters

| Name | Type |
| :------ | :------ |
| `perspective` | `boolean` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.perspective

___

### getPerspective

▸ **getPerspective**(): `boolean`

获取是否开启 marker 覆盖物近大远小效果

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getPerspective

___

### setPerspective

▸ **setPerspective**(`perspective`): `void`

设置是否开启 marker 覆盖物近大远小效果，默认开启

#### Parameters

| Name | Type |
| :------ | :------ |
| `perspective` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setPerspective

___

### priority

▸ **priority**(`priority`): [`Label`](map.Label.md)

设置碰撞时显示的优先级,取值范围 [0, 65535]

#### Parameters

| Name | Type |
| :------ | :------ |
| `priority` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.priority

___

### getPriority

▸ **getPriority**(): `number`

获取碰撞时显示的优先级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getPriority

___

### setPriority

▸ **setPriority**(`priority`): `void`

设置碰撞时显示的优先级,取值范围 [0, 65535]

#### Parameters

| Name | Type |
| :------ | :------ |
| `priority` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.setPriority

___

### toDrawItem

▸ **toDrawItem**(): `void`

#### Returns

`void`

#### Overrides

BaseMarker.toDrawItem

___

### getText

▸ **getText**(): `string`

获取文字内容

#### Returns

`string`

**`Since`**

1.0.0

___

### text

▸ **text**(`text`): [`Label`](map.Label.md)

设置文字内容

#### Parameters

| Name | Type |
| :------ | :------ |
| `text` | `string` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

___

### setText

▸ **setText**(`text`): `void`

设置文字内容

#### Parameters

| Name | Type |
| :------ | :------ |
| `text` | `string` |

#### Returns

`void`

**`Since`**

1.0.0

___

### getFontColor

▸ **getFontColor**(): [`ColorInfo`](../interfaces/map.ColorInfo.md)

获取文字颜色

#### Returns

[`ColorInfo`](../interfaces/map.ColorInfo.md)

**`Since`**

1.0.0

___

### fontcolor

▸ **fontcolor**(`color`): [`Label`](map.Label.md)

设置文字颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

___

### setFontColor

▸ **setFontColor**(`color`): `void`

设置文字颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getBorderColor

▸ **getBorderColor**(): [`ColorInfo`](../interfaces/map.ColorInfo.md)

获取文字描边颜色

#### Returns

[`ColorInfo`](../interfaces/map.ColorInfo.md)

**`Since`**

1.2.0

___

### borderColor

▸ **borderColor**(`color`): [`Label`](map.Label.md)

设置文字描边颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.2.0

___

### setBorderColor

▸ **setBorderColor**(`color`): `void`

设置文字描边颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Since`**

1.2.0

___

### borderSize

▸ **borderSize**(`width`): [`Label`](map.Label.md)

设置文字描边宽度

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.2.0

___

### setBorderSize

▸ **setBorderSize**(`width`): `void`

设置文字描边宽度

#### Parameters

| Name | Type |
| :------ | :------ |
| `width` | `number` |

#### Returns

`void`

**`Since`**

1.2.0

___

### getBorderSize

▸ **getBorderSize**(): `number`

获取文字描边宽度

#### Returns

`number`

**`Since`**

1.2.0

___

### getBgColor

▸ **getBgColor**(): [`ColorInfo`](../interfaces/map.ColorInfo.md)

获取文字背景颜色

#### Returns

[`ColorInfo`](../interfaces/map.ColorInfo.md)

**`Deprecated`**

**`Since`**

1.2.0

___

### bgcolor

▸ **bgcolor**(`color`): [`Label`](map.Label.md)

设置文字背景颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Label`](map.Label.md)

**`Deprecated`**

**`Since`**

1.2.0

___

### setBgColor

▸ **setBgColor**(`color`): `void`

设置文字背景颜色

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

`void`

**`Deprecated`**

**`Since`**

1.2.0

___

### getFontSize

▸ **getFontSize**(): `number`

获取字体大小

#### Returns

`number`

**`Since`**

1.0.0

___

### fontSize

▸ **fontSize**(`size`): [`Label`](map.Label.md)

设置字体大小

#### Parameters

| Name | Type |
| :------ | :------ |
| `size` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

___

### setFontSize

▸ **setFontSize**(`size`): `void`

设置字体大小

#### Parameters

| Name | Type |
| :------ | :------ |
| `size` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### getFontType

▸ **getFontType**(): [`FontType`](../enums/map.SysEnum.FontType.md)

获取字体

#### Returns

[`FontType`](../enums/map.SysEnum.FontType.md)

**`Since`**

1.0.0

___

### fontType

▸ **fontType**(`type`): [`Label`](map.Label.md)

设置字体

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`FontType`](../enums/map.SysEnum.FontType.md) |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

___

### setFontType

▸ **setFontType**(`type`): `void`

设置字体

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`FontType`](../enums/map.SysEnum.FontType.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getAlign

▸ **getAlign**(): `void`

获取对齐方式

#### Returns

`void`

**`Deprecated`**

请使用located替代

**`Since`**

1.2.0

___

### align

▸ **align**(`alignx`, `aligny`): [`Label`](map.Label.md)

设置对齐方式

#### Parameters

| Name | Type |
| :------ | :------ |
| `alignx` | [`FontAlign`](../enums/map.SysEnum.FontAlign.md) |
| `aligny` | [`FontAlign`](../enums/map.SysEnum.FontAlign.md) |

#### Returns

[`Label`](map.Label.md)

**`Deprecated`**

请使用located替代

**`Since`**

1.2.0

___

### setAlign

▸ **setAlign**(`alignx`, `aligny`): `void`

设置对齐方式

#### Parameters

| Name | Type |
| :------ | :------ |
| `alignx` | [`FontAlign`](../enums/map.SysEnum.FontAlign.md) |
| `aligny` | [`FontAlign`](../enums/map.SysEnum.FontAlign.md) |

#### Returns

`void`

**`Deprecated`**

请使用located替代

**`Since`**

1.1.1

___

### toString

▸ **toString**(): `string`

#### Returns

`string`

**`Since`**

1.0.1

#### Overrides

BaseMarker.toString

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

BaseMarker.putPointsInfoIntoBundle

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

BaseMarker.addEventListener

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

BaseMarker.removeEventListener

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

BaseMarker.addDragListener

___

### removeDragListener

▸ **removeDragListener**(): `void`

移除拖拽监听器

#### Returns

`void`

**`Since`**

2.0.3

#### Inherited from

BaseMarker.removeDragListener

___

### getDragListener

▸ **getDragListener**(): [`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

获取拖拽监听器

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`OverlayDragListener`](../interfaces/map.OverlayDragListener.md)\>

**`Since`**

2.0.3

#### Inherited from

BaseMarker.getDragListener

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

BaseMarker.fireEvent

___

### getType

▸ **getType**(): `default`

#### Returns

`default`

#### Inherited from

BaseMarker.getType

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

BaseMarker.setAnimation

___

### getAnimation

▸ **getAnimation**(): [`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<[`Animation`](map.Animation.md)\>

#### Inherited from

BaseMarker.getAnimation

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

BaseMarker.setVisible

___

### getVisible

▸ **getVisible**(): `boolean`

获取显示状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getVisible

___

### alpha

▸ **alpha**(`alpha`): [`Label`](map.Label.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.alpha

___

### getAlpha

▸ **getAlpha**(): `number`

获取透明度

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getAlpha

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

BaseMarker.setAlpha

___

### startLevel

▸ **startLevel**(`startLevel`): [`Label`](map.Label.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.startLevel

___

### getStartLevel

▸ **getStartLevel**(): `number`

获取覆盖物开始显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getStartLevel

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

BaseMarker.setStartLevel

___

### endLevel

▸ **endLevel**(`endLevel`): [`Label`](map.Label.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.endLevel

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

BaseMarker.showLevel

___

### getEndLevel

▸ **getEndLevel**(): `number`

获取marker结束显示的地图缩放层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getEndLevel

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

BaseMarker.setShowLevel

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

BaseMarker.setEndLevel

___

### clickable

▸ **clickable**(`isClickable`): [`Label`](map.Label.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Label`](map.Label.md)

**`Since`**

1.0.0

#### Inherited from

BaseMarker.clickable

___

### getClickable

▸ **getClickable**(): `boolean`

获取是否可点击状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getClickable

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

BaseMarker.setClickable

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

BaseMarker.setZIndex

___

### getZIndex

▸ **getZIndex**(): `number`

获取覆盖物显示层级

#### Returns

`number`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getZIndex

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

BaseMarker.setExtraInfo

___

### getExtraInfo

▸ **getExtraInfo**(): `AnyObject`

获取覆盖物属性数据

#### Returns

`AnyObject`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.getExtraInfo

___

### getBmDrawItem

▸ **getBmDrawItem**(): `undefined` \| `default`

#### Returns

`undefined` \| `default`

#### Inherited from

BaseMarker.getBmDrawItem

___

### update

▸ **update**(): `void`

#### Returns

`void`

#### Inherited from

BaseMarker.update

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

BaseMarker.remove

___

### isRemoved

▸ **isRemoved**(): `undefined` \| `boolean`

获取是否移除状态

#### Returns

`undefined` \| `boolean`

**`Since`**

1.0.0

#### Inherited from

BaseMarker.isRemoved

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

#### Inherited from

BaseMarker.destroy
