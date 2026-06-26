[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ILabelOption

# Interface: ILabelOption

[map](../modules/map.md).ILabelOption

文字样式设置

**`Since`**

1.0.0

## Hierarchy

- [`IBaseMarkerOption`](map.IBaseMarkerOption.md)

  ↳ **`ILabelOption`**

## Table of contents

### Properties

- [alpha](map.ILabelOption.md#alpha)
- [visible](map.ILabelOption.md#visible)
- [isClickable](map.ILabelOption.md#isclickable)
- [zIndex](map.ILabelOption.md#zindex)
- [startLevel](map.ILabelOption.md#startlevel)
- [endLevel](map.ILabelOption.md#endlevel)
- [text](map.ILabelOption.md#text)
- [fontcolorstr](map.ILabelOption.md#fontcolorstr)
- [fontsize](map.ILabelOption.md#fontsize)
- [bordercolorstr](map.ILabelOption.md#bordercolorstr)
- [bordersize](map.ILabelOption.md#bordersize)
- [fontType](map.ILabelOption.md#fonttype)
- [bgcolorstr](map.ILabelOption.md#bgcolorstr)
- [position](map.ILabelOption.md#position)
- [located](map.ILabelOption.md#located)
- [isPerspective](map.ILabelOption.md#isperspective)
- [isDraggable](map.ILabelOption.md#isdraggable)
- [rotate](map.ILabelOption.md#rotate)
- [xOffset](map.ILabelOption.md#xoffset)
- [yOffset](map.ILabelOption.md#yoffset)
- [isRotateItem](map.ILabelOption.md#isrotateitem)
- [isRotateNorth](map.ILabelOption.md#isrotatenorth)
- [isFlat](map.ILabelOption.md#isflat)
- [isFixed](map.ILabelOption.md#isfixed)
- [period](map.ILabelOption.md#period)
- [scaleX](map.ILabelOption.md#scalex)
- [scaleY](map.ILabelOption.md#scaley)
- [fixedScreenPosition](map.ILabelOption.md#fixedscreenposition)
- [isJoinCollision](map.ILabelOption.md#isjoincollision)
- [popView](map.ILabelOption.md#popview)

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

### text

• `Optional` **text**: `string`

文字

**`Since`**

1.0.0

___

### fontcolorstr

• `Optional` **fontcolorstr**: [`ColorString`](../modules/map.md#colorstring)

文字颜色设置

**`Since`**

1.0.1

___

### fontsize

• `Optional` **fontsize**: `number`

文字大小

**`Since`**

1.0.0

___

### bordercolorstr

• `Optional` **bordercolorstr**: [`ColorString`](../modules/map.md#colorstring)

文字描边颜色设置

**`Since`**

1.2.0

___

### bordersize

• `Optional` **bordersize**: `number`

文字描边宽度

**`Since`**

1.2.0

___

### fontType

• `Optional` **fontType**: `number`

文字类型

**`Since`**

1.0.0

___

### bgcolorstr

• `Optional` **bgcolorstr**: [`ColorString`](../modules/map.md#colorstring)

背景色设置

**`Deprecated`**

**`Since`**

1.2.0

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
