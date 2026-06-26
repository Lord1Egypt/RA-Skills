[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ITrackOption

# Interface: ITrackOption

[map](../modules/map.md).ITrackOption

Track设置

**`Since`**

2.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`ITrackOption`**

## Table of contents

### Properties

- [alpha](map.ITrackOption.md#alpha)
- [visible](map.ITrackOption.md#visible)
- [isClickable](map.ITrackOption.md#isclickable)
- [zIndex](map.ITrackOption.md#zindex)
- [startLevel](map.ITrackOption.md#startlevel)
- [endLevel](map.ITrackOption.md#endlevel)
- [points](map.ITrackOption.md#points)
- [trackType](map.ITrackOption.md#tracktype)
- [heights](map.ITrackOption.md#heights)
- [width](map.ITrackOption.md#width)
- [color](map.ITrackOption.md#color)
- [gradientColors](map.ITrackOption.md#gradientcolors)
- [palette](map.ITrackOption.md#palette)
- [paletteOpacity](map.ITrackOption.md#paletteopacity)
- [projectionPalette](map.ITrackOption.md#projectionpalette)
- [animationTime](map.ITrackOption.md#animationtime)
- [trackMove](map.ITrackOption.md#trackmove)
- [traceAnimationListener](map.ITrackOption.md#traceanimationlistener)

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

### points

• **points**: [`LatLng`](../classes/base.LatLng.md)[]

设置轨迹点

___

### trackType

• `Optional` **trackType**: [`TrackType`](../enums/map.SysEnum.TrackType.md)

设置轨迹线的类型

___

### heights

• `Optional` **heights**: `number`[]

设置轨迹线的高度
注：高度必须 >= 0，否则不绘制 单位:米

___

### width

• `Optional` **width**: `number`

设置轨迹线的宽度,默认为5

___

### color

• `Optional` **color**: [`ColorString`](../modules/map.md#colorstring)

设置轨迹线的颜色

___

### gradientColors

• `Optional` **gradientColors**: [`ColorString`](../modules/map.md#colorstring)[]

设置轨迹线渐变色数组,只在设置trackType为渐变色类型时生效

___

### palette

• `Optional` **palette**: [`ImageEntity`](../classes/map.ImageEntity.md)

设置轨迹调色板

___

### paletteOpacity

• `Optional` **paletteOpacity**: `number`

___

### projectionPalette

• `Optional` **projectionPalette**: [`ImageEntity`](../classes/map.ImageEntity.md)

设置3d轨迹映射到2d轨迹的调色板,
注：type = 4 时必传,其余类型不生效

___

### animationTime

• `Optional` **animationTime**: `number`

设置动画时间，默认300ms

___

### trackMove

• `Optional` **trackMove**: `boolean`

设置地图中心是否跟随轨迹线移动

___

### traceAnimationListener

• `Optional` **traceAnimationListener**: [`TraceAnimationListener`](map.TraceAnimationListener.md)

设置轨迹动画的状态监听
