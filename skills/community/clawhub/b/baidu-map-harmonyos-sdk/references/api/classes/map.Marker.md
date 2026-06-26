[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Marker

# Class: Marker

[map](../modules/map.md).Marker

Marker覆盖物

**`Abstract`**

提供Marker覆盖物创建、操作方法

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Hierarchy

- `default`

  ↳ **`Marker`**

## Table of contents

### Constructors

- [constructor](map.Marker.md#constructor)

### Properties

- [uuid](map.Marker.md#uuid)
- [type](map.Marker.md#type)
- [eventListener](map.Marker.md#eventlistener)
- [isDestroyed](map.Marker.md#isdestroyed)

### Accessors

- [typeName](map.Marker.md#typename)
- [visible](map.Marker.md#visible)
- [zIndex](map.Marker.md#zindex)

### Methods

- [scaleX](map.Marker.md#scalex)
- [getScaleX](map.Marker.md#getscalex)
- [setScaleX](map.Marker.md#setscalex)
- [scaleY](map.Marker.md#scaley)
- [getScaleY](map.Marker.md#getscaley)
- [setScaleY](map.Marker.md#setscaley)
- [setScale](map.Marker.md#setscale)
- [yOffset](map.Marker.md#yoffset)
- [getYOffset](map.Marker.md#getyoffset)
- [setYOffset](map.Marker.md#setyoffset)
- [xOffset](map.Marker.md#xoffset)
- [getXOffset](map.Marker.md#getxoffset)
- [setXOffset](map.Marker.md#setxoffset)
- [draggable](map.Marker.md#draggable)
- [getDraggable](map.Marker.md#getdraggable)
- [setDraggable](map.Marker.md#setdraggable)
- [flat](map.Marker.md#flat)
- [getFlat](map.Marker.md#getflat)
- [setFlat](map.Marker.md#setflat)
- [period](map.Marker.md#period)
- [getPeriod](map.Marker.md#getperiod)
- [setPeriod](map.Marker.md#setperiod)
- [position](map.Marker.md#position)
- [getPosition](map.Marker.md#getposition)
- [setPosition](map.Marker.md#setposition)
- [setBmPosition](map.Marker.md#setbmposition)
- [popView](map.Marker.md#popview)
- [setPopView](map.Marker.md#setpopview)
- [getPopView](map.Marker.md#getpopview)
- [located](map.Marker.md#located)
- [setLocated](map.Marker.md#setlocated)
- [getLocated](map.Marker.md#getlocated)
- [anchor](map.Marker.md#anchor)
- [getAnchor](map.Marker.md#getanchor)
- [setAnchor](map.Marker.md#setanchor)
- [getRotate](map.Marker.md#getrotate)
- [setRotate](map.Marker.md#setrotate)
- [isJoinCollision](map.Marker.md#isjoincollision)
- [getIsJoinCollision](map.Marker.md#getisjoincollision)
- [setIsJoinCollision](map.Marker.md#setisjoincollision)
- [isFixed](map.Marker.md#isfixed)
- [setIsFixed](map.Marker.md#setisfixed)
- [getFixedScreen](map.Marker.md#getfixedscreen)
- [isRotateItem](map.Marker.md#isrotateitem)
- [getIsRotateItem](map.Marker.md#getisrotateitem)
- [setIsRotateItem](map.Marker.md#setisrotateitem)
- [isRotateNorth](map.Marker.md#isrotatenorth)
- [getIsRotateNorth](map.Marker.md#getisrotatenorth)
- [setIsRotateNorth](map.Marker.md#setisrotatenorth)
- [fixedScreenPosition](map.Marker.md#fixedscreenposition)
- [setFixedScreenPosition](map.Marker.md#setfixedscreenposition)
- [perspective](map.Marker.md#perspective)
- [getPerspective](map.Marker.md#getperspective)
- [setPerspective](map.Marker.md#setperspective)
- [priority](map.Marker.md#priority)
- [getPriority](map.Marker.md#getpriority)
- [setPriority](map.Marker.md#setpriority)
- [toDrawItem](map.Marker.md#todrawitem)
- [changePosition](map.Marker.md#changeposition)
- [icons](map.Marker.md#icons)
- [icon](map.Marker.md#icon)
- [color](map.Marker.md#color)
- [resource](map.Marker.md#resource)
- [setResource](map.Marker.md#setresource)
- [getResource](map.Marker.md#getresource)
- [setColor](map.Marker.md#setcolor)
- [getColor](map.Marker.md#getcolor)
- [setGuessResource](map.Marker.md#setguessresource)
- [getIcon](map.Marker.md#geticon)
- [setIcon](map.Marker.md#seticon)
- [getIcons](map.Marker.md#geticons)
- [setIcons](map.Marker.md#seticons)
- [animateType](map.Marker.md#animatetype)
- [getAnimateType](map.Marker.md#getanimatetype)
- [setAnimateType](map.Marker.md#setanimatetype)
- [setBmpResourceId](map.Marker.md#setbmpresourceid)
- [setInterval](map.Marker.md#setinterval)
- [toString](map.Marker.md#tostring)
- [putPointsInfoIntoBundle](map.Marker.md#putpointsinfointobundle)
- [addEventListener](map.Marker.md#addeventlistener)
- [removeEventListener](map.Marker.md#removeeventlistener)
- [addDragListener](map.Marker.md#adddraglistener)
- [removeDragListener](map.Marker.md#removedraglistener)
- [getDragListener](map.Marker.md#getdraglistener)
- [fireEvent](map.Marker.md#fireevent)
- [getType](map.Marker.md#gettype)
- [setAnimation](map.Marker.md#setanimation)
- [getAnimation](map.Marker.md#getanimation)
- [setVisible](map.Marker.md#setvisible)
- [getVisible](map.Marker.md#getvisible)
- [alpha](map.Marker.md#alpha)
- [getAlpha](map.Marker.md#getalpha)
- [setAlpha](map.Marker.md#setalpha)
- [startLevel](map.Marker.md#startlevel)
- [getStartLevel](map.Marker.md#getstartlevel)
- [setStartLevel](map.Marker.md#setstartlevel)
- [endLevel](map.Marker.md#endlevel)
- [showLevel](map.Marker.md#showlevel)
- [getEndLevel](map.Marker.md#getendlevel)
- [setShowLevel](map.Marker.md#setshowlevel)
- [setEndLevel](map.Marker.md#setendlevel)
- [clickable](map.Marker.md#clickable)
- [getClickable](map.Marker.md#getclickable)
- [setClickable](map.Marker.md#setclickable)
- [setZIndex](map.Marker.md#setzindex)
- [getZIndex](map.Marker.md#getzindex)
- [setExtraInfo](map.Marker.md#setextrainfo)
- [getExtraInfo](map.Marker.md#getextrainfo)
- [getBmDrawItem](map.Marker.md#getbmdrawitem)
- [update](map.Marker.md#update)
- [remove](map.Marker.md#remove)
- [isRemoved](map.Marker.md#isremoved)
- [destroy](map.Marker.md#destroy)

## Constructors

### constructor

• **new Marker**(`opts?`): [`Marker`](map.Marker.md)

构造函数，默认参数
```Typescript
{
position:new LatLng(39.914935, 116.403119),
located: SysEnum.Located.TOP,
isPerspective: true,
rotate: 0,
yOffset: 0,
alpha: 1.0,
animateType: SysEnum.AnimateDefine.NONE,
isFixed: false,
isClickable: true,
icon: new ImageEntity('rawfile://baidu/img/pages/location.png'),
scaleX: 1.0,
scaleY: 1.0,
startLevel: 4,
endLevel: 21
}
```

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts?` | [`Nullable`](../modules/map.md#nullable)\<[`IMarkerOption`](../interfaces/map.IMarkerOption.md)\> |

#### Returns

[`Marker`](map.Marker.md)

**`Since`**

1.0.0

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

获取覆盖物名称

#### Returns

`string`

**`Since`**

1.0.0

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

▸ **scaleX**(`scaleX`): [`Marker`](map.Marker.md)

设置X轴图标缩放比例

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `scaleX` | `number` | 取值范围[0,} |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **scaleY**(`scaleY`): [`Marker`](map.Marker.md)

设置Y轴图标缩放比例

#### Parameters

| Name | Type |
| :------ | :------ |
| `scaleY` | `number` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **yOffset**(`yOffset`): [`Marker`](map.Marker.md)

设置Y轴图标偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `yOffset` | `number` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **xOffset**(`xOffset`): [`Marker`](map.Marker.md)

设置X轴图标偏移量

#### Parameters

| Name | Type |
| :------ | :------ |
| `xOffset` | `number` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **draggable**(`draggable`): [`Marker`](map.Marker.md)

设置是否可拖动

#### Parameters

| Name | Type |
| :------ | :------ |
| `draggable` | `boolean` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **flat**(`flat`): [`Marker`](map.Marker.md)

设置贴地模式

#### Parameters

| Name | Type |
| :------ | :------ |
| `flat` | `boolean` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **period**(`period`): [`Marker`](map.Marker.md)

设置多少帧刷新一次图片资源

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `period` | `number` | 帧数，刷新周期，值越小速度越快。默认为20，最小为1 |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **position**(`position`): [`Marker`](map.Marker.md)

设置图标位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `position` | [`LatLng`](base.LatLng.md) |

#### Returns

[`Marker`](map.Marker.md)

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

### popView

▸ **popView**(`popView`): [`Marker`](map.Marker.md)

设置消息气泡

#### Parameters

| Name | Type |
| :------ | :------ |
| `popView` | [`PopView`](map.PopView.md) |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **anchor**(`anchorX`, `anchorY`): [`Marker`](map.Marker.md)

设置 marker 覆盖物的锚点比例，默认（0.5, 1.0）水平居中，垂直下对齐

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `anchorX` | `number` | 取值范围[0.0 , 1.0]， 否则不生效 |
| `anchorY` | `number` | 取值范围[0.0 , 1.0]， 否则不生效 |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **isJoinCollision**(`isJoinCollision`): [`Marker`](map.Marker.md)

设置marker是否参与碰撞检测

#### Parameters

| Name | Type |
| :------ | :------ |
| `isJoinCollision` | [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md) |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **isRotateItem**(`isRotateItem`): [`Marker`](map.Marker.md)

设置是否使用外部设置的Rotate

#### Parameters

| Name | Type |
| :------ | :------ |
| `isRotateItem` | `boolean` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **isRotateNorth**(`isRotateNorth`): [`Marker`](map.Marker.md)

设置是否使用旋转基准是地理北方向

#### Parameters

| Name | Type |
| :------ | :------ |
| `isRotateNorth` | `boolean` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **fixedScreenPosition**(`point`): [`Marker`](map.Marker.md)

设置 Marker 覆盖物的屏幕位置,用于固定marker不随地图移动

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point` | [`Nullable`](../modules/map.md#nullable)\<[`Point`](base.Point.md)\> | 如果设置坐标，则代表启用固定屏幕像素坐标显示marker |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **perspective**(`perspective`): [`Marker`](map.Marker.md)

设置是否开启 marker 覆盖物近大远小效果，默认开启

#### Parameters

| Name | Type |
| :------ | :------ |
| `perspective` | `boolean` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **priority**(`priority`): [`Marker`](map.Marker.md)

设置碰撞时显示的优先级,取值范围 [0, 65535]

#### Parameters

| Name | Type |
| :------ | :------ |
| `priority` | `number` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **toDrawItem**(): `Promise`\<`void`\>

#### Returns

`Promise`\<`void`\>

#### Overrides

BaseMarker.toDrawItem

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

#### Overrides

BaseMarker.changePosition

___

### icons

▸ **icons**(`icons`): `Promise`\<[`Marker`](map.Marker.md)\>

设置图标源

#### Parameters

| Name | Type |
| :------ | :------ |
| `icons` | [`ImageEntity`](map.ImageEntity.md)[] |

#### Returns

`Promise`\<[`Marker`](map.Marker.md)\>

**`Since`**

1.0.0

___

### icon

▸ **icon**(`_icon`): [`Marker`](map.Marker.md)

设置图标源

#### Parameters

| Name | Type |
| :------ | :------ |
| `_icon` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

[`Marker`](map.Marker.md)

**`Since`**

1.0.0

___

### color

▸ **color**(`color`): [`Marker`](map.Marker.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `color` | [`ColorString`](../modules/map.md#colorstring) |

#### Returns

[`Marker`](map.Marker.md)

___

### resource

▸ **resource**(`r`): [`Marker`](map.Marker.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `r` | `string` \| `number` |

#### Returns

[`Marker`](map.Marker.md)

___

### setResource

▸ **setResource**(`r`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `r` | `string` \| `number` |

#### Returns

`void`

___

### getResource

▸ **getResource**(): [`Maybe`](../modules/map.md#maybe)\<`string` \| `number`\>

#### Returns

[`Maybe`](../modules/map.md#maybe)\<`string` \| `number`\>

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

### getColor

▸ **getColor**(): `string`

#### Returns

`string`

___

### setGuessResource

▸ **setGuessResource**(`res`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `res` | `string` |

#### Returns

`void`

___

### getIcon

▸ **getIcon**(): ``null`` \| [`ImageEntity`](map.ImageEntity.md)

获取图标源

#### Returns

``null`` \| [`ImageEntity`](map.ImageEntity.md)

**`Since`**

1.0.0

___

### setIcon

▸ **setIcon**(`_icon`): `void`

设置图标源

#### Parameters

| Name | Type |
| :------ | :------ |
| `_icon` | [`ImageEntity`](map.ImageEntity.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### getIcons

▸ **getIcons**(): [`ImageEntity`](map.ImageEntity.md)[]

获取图标源

#### Returns

[`ImageEntity`](map.ImageEntity.md)[]

**`Since`**

1.0.0

___

### setIcons

▸ **setIcons**(`icons`): `void`

设置图标源

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `icons` | [`ImageEntity`](map.ImageEntity.md)[] | 当前版本仅读取第一个图像数据源 |

#### Returns

`void`

**`Since`**

1.0.0

___

### animateType

▸ **animateType**(`type`): [`Marker`](map.Marker.md)

设置显示时的动画类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`Nullable`](../modules/map.md#nullable)\<[`AnimateDefine`](../enums/map.SysEnum.AnimateDefine.md)\> |

#### Returns

[`Marker`](map.Marker.md)

**`Since`**

1.0.0

___

### getAnimateType

▸ **getAnimateType**(): [`AnimateDefine`](../enums/map.SysEnum.AnimateDefine.md)

获取显示时的动画类型

#### Returns

[`AnimateDefine`](../enums/map.SysEnum.AnimateDefine.md)

**`Since`**

1.0.0

___

### setAnimateType

▸ **setAnimateType**(`type`): `void`

设置显示时的动画类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`Nullable`](../modules/map.md#nullable)\<[`AnimateDefine`](../enums/map.SysEnum.AnimateDefine.md)\> |

#### Returns

`void`

**`Since`**

1.0.0

___

### setBmpResourceId

▸ **setBmpResourceId**(`bmpResId`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bmpResId` | `number` |

#### Returns

`void`

___

### setInterval

▸ **setInterval**(`interval`): `void`

设置帧动画间隔时间

#### Parameters

| Name | Type |
| :------ | :------ |
| `interval` | `number` |

#### Returns

`void`

**`Since`**

2.0.4

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

▸ **alpha**(`alpha`): [`Marker`](map.Marker.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `alpha` | `number` | 取值范围[0,1] |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **startLevel**(`startLevel`): [`Marker`](map.Marker.md)

设置覆盖物开始显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `startLevel` | `number` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **endLevel**(`endLevel`): [`Marker`](map.Marker.md)

设置覆盖物结束显示的地图缩放层级

#### Parameters

| Name | Type |
| :------ | :------ |
| `endLevel` | `number` |

#### Returns

[`Marker`](map.Marker.md)

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

▸ **clickable**(`isClickable`): [`Marker`](map.Marker.md)

设置是否可点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `isClickable` | `boolean` |

#### Returns

[`Marker`](map.Marker.md)

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
