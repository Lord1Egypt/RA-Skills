[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ICircleOption

# Interface: ICircleOption

[map](../modules/map.md).ICircleOption

圆样式设置

**`Since`**

1.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`ICircleOption`**

## Table of contents

### Properties

- [alpha](map.ICircleOption.md#alpha)
- [visible](map.ICircleOption.md#visible)
- [isClickable](map.ICircleOption.md#isclickable)
- [zIndex](map.ICircleOption.md#zindex)
- [startLevel](map.ICircleOption.md#startlevel)
- [endLevel](map.ICircleOption.md#endlevel)
- [center](map.ICircleOption.md#center)
- [radius](map.ICircleOption.md#radius)
- [radiusUnit](map.ICircleOption.md#radiusunit)
- [fillcolor](map.ICircleOption.md#fillcolor)
- [stroke](map.ICircleOption.md#stroke)
- [isGradientCircle](map.ICircleOption.md#isgradientcircle)
- [gradientColors](map.ICircleOption.md#gradientcolors)
- [gradientRadiusWeight](map.ICircleOption.md#gradientradiusweight)
- [gradientColorWeight](map.ICircleOption.md#gradientcolorweight)

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

### center

• `Optional` **center**: [`LatLng`](../classes/base.LatLng.md)

圆心坐标

**`Since`**

1.0.0

___

### radius

• `Optional` **radius**: `number`

半径

**`Since`**

1.0.0

___

### radiusUnit

• `Optional` **radiusUnit**: [`UnitOption`](../enums/map.SysEnum.UnitOption.md)

长度单位

**`Since`**

1.2.0

___

### fillcolor

• `Optional` **fillcolor**: [`ColorString`](../modules/map.md#colorstring)

填充颜色

**`Since`**

1.0.0

___

### stroke

• `Optional` **stroke**: [`Stroke`](../classes/map.Stroke.md)

描边样式

**`Since`**

1.0.0

___

### isGradientCircle

• `Optional` **isGradientCircle**: `boolean`

是否启用渐变

**`Since`**

1.2.0

___

### gradientColors

• `Optional` **gradientColors**: [`ColorString`](../modules/map.md#colorstring)[]

渐变颜色序列

**`Since`**

1.2.0

___

### gradientRadiusWeight

• `Optional` **gradientRadiusWeight**: `number`

渐变半径权重 0.0 ～ 1.0

**`Since`**

1.2.0

___

### gradientColorWeight

• `Optional` **gradientColorWeight**: `number`

渐变颜色权重 0.0 ～ 1.0

**`Since`**

1.2.0
