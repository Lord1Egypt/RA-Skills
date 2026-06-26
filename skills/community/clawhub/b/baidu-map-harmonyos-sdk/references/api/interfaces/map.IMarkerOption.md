[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IMarkerOption

# Interface: IMarkerOption

[map](../modules/map.md).IMarkerOption

Marker覆盖物初始化设置

**`Since`**

1.0.0

## Hierarchy

- [`IBaseMarkerOption`](map.IBaseMarkerOption.md)

  ↳ **`IMarkerOption`**

## Table of contents

### Properties

- [alpha](map.IMarkerOption.md#alpha)
- [visible](map.IMarkerOption.md#visible)
- [isClickable](map.IMarkerOption.md#isclickable)
- [zIndex](map.IMarkerOption.md#zindex)
- [startLevel](map.IMarkerOption.md#startlevel)
- [endLevel](map.IMarkerOption.md#endlevel)
- [position](map.IMarkerOption.md#position)
- [located](map.IMarkerOption.md#located)
- [isPerspective](map.IMarkerOption.md#isperspective)
- [isDraggable](map.IMarkerOption.md#isdraggable)
- [rotate](map.IMarkerOption.md#rotate)
- [xOffset](map.IMarkerOption.md#xoffset)
- [yOffset](map.IMarkerOption.md#yoffset)
- [isRotateItem](map.IMarkerOption.md#isrotateitem)
- [isRotateNorth](map.IMarkerOption.md#isrotatenorth)
- [isFlat](map.IMarkerOption.md#isflat)
- [isFixed](map.IMarkerOption.md#isfixed)
- [period](map.IMarkerOption.md#period)
- [scaleX](map.IMarkerOption.md#scalex)
- [scaleY](map.IMarkerOption.md#scaley)
- [fixedScreenPosition](map.IMarkerOption.md#fixedscreenposition)
- [isJoinCollision](map.IMarkerOption.md#isjoincollision)
- [popView](map.IMarkerOption.md#popview)
- [icon](map.IMarkerOption.md#icon)
- [icons](map.IMarkerOption.md#icons)
- [delPreIconResource](map.IMarkerOption.md#delpreiconresource)
- [color](map.IMarkerOption.md#color)
- [animateType](map.IMarkerOption.md#animatetype)
- [resource](map.IMarkerOption.md#resource)
- [interval](map.IMarkerOption.md#interval)

## Properties

### alpha

• `Optional` **alpha**: `number`

设置透明度 [0，1]

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[alpha](map.IBaseMarkerOption.md#alpha)

___

### visible

• `Optional` **visible**: `boolean`

是否显示

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[visible](map.IBaseMarkerOption.md#visible)

___

### isClickable

• `Optional` **isClickable**: `boolean`

是否启用点击

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isClickable](map.IBaseMarkerOption.md#isclickable)

___

### zIndex

• `Optional` **zIndex**: `number`

设置层级

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[zIndex](map.IBaseMarkerOption.md#zindex)

___

### startLevel

• `Optional` **startLevel**: `number`

开始显示地图缩放级别

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[startLevel](map.IBaseMarkerOption.md#startlevel)

___

### endLevel

• `Optional` **endLevel**: `number`

结束显示地图缩放级别

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[endLevel](map.IBaseMarkerOption.md#endlevel)

___

### position

• `Optional` **position**: [`LatLng`](../classes/base.LatLng.md)

位置

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[position](map.IBaseMarkerOption.md#position)

___

### located

• `Optional` **located**: [`Located`](../enums/map.SysEnum.Located.md)

绘制元素位于「基准Anchor」的方位，默认 Located.TOP

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[located](map.IBaseMarkerOption.md#located)

___

### isPerspective

• `Optional` **isPerspective**: `boolean`

是否启用透视效果

**`Since`**

1ma.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isPerspective](map.IBaseMarkerOption.md#isperspective)

___

### isDraggable

• `Optional` **isDraggable**: `boolean`

是否启用拖动效果

**`Since`**

2.0.3

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isDraggable](map.IBaseMarkerOption.md#isdraggable)

___

### rotate

• `Optional` **rotate**: `number`

旋转角度

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[rotate](map.IBaseMarkerOption.md#rotate)

___

### xOffset

• `Optional` **xOffset**: `number`

X轴偏移量

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[xOffset](map.IBaseMarkerOption.md#xoffset)

___

### yOffset

• `Optional` **yOffset**: `number`

Y轴偏移量

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[yOffset](map.IBaseMarkerOption.md#yoffset)

___

### isRotateItem

• `Optional` **isRotateItem**: `boolean`

是否使用使用外部设置的Rotate，默认false

**`Since`**

2.0.4

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isRotateItem](map.IBaseMarkerOption.md#isrotateitem)

___

### isRotateNorth

• `Optional` **isRotateNorth**: `boolean`

是否使用旋转基准是地理北方向，默认false

**`Since`**

2.0.4

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isRotateNorth](map.IBaseMarkerOption.md#isrotatenorth)

___

### isFlat

• `Optional` **isFlat**: `boolean`

是否启用贴地效果

**`Since`**

1.0.2

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isFlat](map.IBaseMarkerOption.md#isflat)

___

### isFixed

• `Optional` **isFixed**: `boolean`

是否启用固定像素坐标效果

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isFixed](map.IBaseMarkerOption.md#isfixed)

___

### period

• `Optional` **period**: `number`

刷新周期

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[period](map.IBaseMarkerOption.md#period)

___

### scaleX

• `Optional` **scaleX**: `number`

图标X轴缩放比例

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[scaleX](map.IBaseMarkerOption.md#scalex)

___

### scaleY

• `Optional` **scaleY**: `number`

图标Y轴缩放比例

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[scaleY](map.IBaseMarkerOption.md#scaley)

___

### fixedScreenPosition

• `Optional` **fixedScreenPosition**: [`Point`](../classes/base.Point.md)

固定像素坐标位置

**`Since`**

1.0.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[fixedScreenPosition](map.IBaseMarkerOption.md#fixedscreenposition)

___

### isJoinCollision

• `Optional` **isJoinCollision**: [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md)

是否参与碰撞

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[isJoinCollision](map.IBaseMarkerOption.md#isjoincollision)

___

### popView

• `Optional` **popView**: [`PopView`](../classes/map.PopView.md)

附加消息气泡

**`Since`**

1.1.0

#### Inherited from

[IBaseMarkerOption](map.IBaseMarkerOption.md).[popView](map.IBaseMarkerOption.md#popview)

___

### icon

• `Optional` **icon**: [`ImageEntity`](../classes/map.ImageEntity.md)

图标资源

**`Since`**

1.0.0

___

### icons

• `Optional` **icons**: [`ImageEntity`](../classes/map.ImageEntity.md)[]

图标资源

**`Since`**

1.0.0

___

### delPreIconResource

• `Optional` **delPreIconResource**: `boolean`

清除之前设置的图标资源，避免内存持续增加

**`Since`**

1.2.1

___

### color

• `Optional` **color**: [`ColorString`](../modules/map.md#colorstring)

图标颜色叠加设置

**`Since`**

1.2.0

___

### animateType

• `Optional` **animateType**: [`AnimateDefine`](../enums/map.SysEnum.AnimateDefine.md)

动画类型

**`Since`**

1.0.0

___

### resource

• `Optional` **resource**: `string` \| `number`

___

### interval

• `Optional` **interval**: `number`

多帧动画间隔

**`Since`**

2.0.4
