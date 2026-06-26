[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IBaseMarkerOption

# Interface: IBaseMarkerOption

[map](../modules/map.md).IBaseMarkerOption

BaseMarker覆盖物初始化设置

**`Since`**

1.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`IBaseMarkerOption`**

  ↳↳ [`ILabelOption`](map.ILabelOption.md)

  ↳↳ [`IMarkerOption`](map.IMarkerOption.md)

## Table of contents

### Properties

- [alpha](map.IBaseMarkerOption.md#alpha)
- [visible](map.IBaseMarkerOption.md#visible)
- [isClickable](map.IBaseMarkerOption.md#isclickable)
- [zIndex](map.IBaseMarkerOption.md#zindex)
- [startLevel](map.IBaseMarkerOption.md#startlevel)
- [endLevel](map.IBaseMarkerOption.md#endlevel)
- [position](map.IBaseMarkerOption.md#position)
- [located](map.IBaseMarkerOption.md#located)
- [isPerspective](map.IBaseMarkerOption.md#isperspective)
- [isDraggable](map.IBaseMarkerOption.md#isdraggable)
- [rotate](map.IBaseMarkerOption.md#rotate)
- [xOffset](map.IBaseMarkerOption.md#xoffset)
- [yOffset](map.IBaseMarkerOption.md#yoffset)
- [isRotateItem](map.IBaseMarkerOption.md#isrotateitem)
- [isRotateNorth](map.IBaseMarkerOption.md#isrotatenorth)
- [isFlat](map.IBaseMarkerOption.md#isflat)
- [isFixed](map.IBaseMarkerOption.md#isfixed)
- [period](map.IBaseMarkerOption.md#period)
- [scaleX](map.IBaseMarkerOption.md#scalex)
- [scaleY](map.IBaseMarkerOption.md#scaley)
- [fixedScreenPosition](map.IBaseMarkerOption.md#fixedscreenposition)
- [isJoinCollision](map.IBaseMarkerOption.md#isjoincollision)
- [popView](map.IBaseMarkerOption.md#popview)

## Properties

### alpha

• `Optional` **alpha**: `number`

设置透明度 [0，1]

**`Since`**

1.1.0

#### Inherited from

[IOverlayOption](map.IOverlayOption.md).[alpha](map.IOverlayOption.md#alpha)

___

### visible

• `Optional` **visible**: `boolean`

是否显示

**`Since`**

1.1.0

#### Inherited from

[IOverlayOption](map.IOverlayOption.md).[visible](map.IOverlayOption.md#visible)

___

### isClickable

• `Optional` **isClickable**: `boolean`

是否启用点击

**`Since`**

1.1.0

#### Inherited from

[IOverlayOption](map.IOverlayOption.md).[isClickable](map.IOverlayOption.md#isclickable)

___

### zIndex

• `Optional` **zIndex**: `number`

设置层级

**`Since`**

1.1.0

#### Inherited from

[IOverlayOption](map.IOverlayOption.md).[zIndex](map.IOverlayOption.md#zindex)

___

### startLevel

• `Optional` **startLevel**: `number`

开始显示地图缩放级别

**`Since`**

1.0.0

#### Inherited from

[IOverlayOption](map.IOverlayOption.md).[startLevel](map.IOverlayOption.md#startlevel)

___

### endLevel

• `Optional` **endLevel**: `number`

结束显示地图缩放级别

**`Since`**

1.0.0

#### Inherited from

[IOverlayOption](map.IOverlayOption.md).[endLevel](map.IOverlayOption.md#endlevel)

___

### position

• `Optional` **position**: [`LatLng`](../classes/base.LatLng.md)

位置

**`Since`**

1.0.0

___

### located

• `Optional` **located**: [`Located`](../enums/map.SysEnum.Located.md)

绘制元素位于「基准Anchor」的方位，默认 Located.TOP

**`Since`**

1.1.0

___

### isPerspective

• `Optional` **isPerspective**: `boolean`

是否启用透视效果

**`Since`**

1ma.0.0

___

### isDraggable

• `Optional` **isDraggable**: `boolean`

是否启用拖动效果

**`Since`**

2.0.3

___

### rotate

• `Optional` **rotate**: `number`

旋转角度

**`Since`**

1.0.0

___

### xOffset

• `Optional` **xOffset**: `number`

X轴偏移量

**`Since`**

1.1.0

___

### yOffset

• `Optional` **yOffset**: `number`

Y轴偏移量

**`Since`**

1.0.0

___

### isRotateItem

• `Optional` **isRotateItem**: `boolean`

是否使用使用外部设置的Rotate，默认false

**`Since`**

2.0.4

___

### isRotateNorth

• `Optional` **isRotateNorth**: `boolean`

是否使用旋转基准是地理北方向，默认false

**`Since`**

2.0.4

___

### isFlat

• `Optional` **isFlat**: `boolean`

是否启用贴地效果

**`Since`**

1.0.2

___

### isFixed

• `Optional` **isFixed**: `boolean`

是否启用固定像素坐标效果

**`Since`**

1.0.0

___

### period

• `Optional` **period**: `number`

刷新周期

**`Since`**

1.0.0

___

### scaleX

• `Optional` **scaleX**: `number`

图标X轴缩放比例

**`Since`**

1.0.0

___

### scaleY

• `Optional` **scaleY**: `number`

图标Y轴缩放比例

**`Since`**

1.0.0

___

### fixedScreenPosition

• `Optional` **fixedScreenPosition**: [`Point`](../classes/base.Point.md)

固定像素坐标位置

**`Since`**

1.0.0

___

### isJoinCollision

• `Optional` **isJoinCollision**: [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md)

是否参与碰撞

**`Since`**

1.1.0

___

### popView

• `Optional` **popView**: [`PopView`](../classes/map.PopView.md)

附加消息气泡

**`Since`**

1.1.0
