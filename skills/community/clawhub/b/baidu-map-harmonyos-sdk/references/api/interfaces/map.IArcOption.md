[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IArcOption

# Interface: IArcOption

[map](../modules/map.md).IArcOption

弧线样式设置

**`Since`**

2.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`IArcOption`**

## Table of contents

### Properties

- [alpha](map.IArcOption.md#alpha)
- [visible](map.IArcOption.md#visible)
- [isClickable](map.IArcOption.md#isclickable)
- [zIndex](map.IArcOption.md#zindex)
- [startLevel](map.IArcOption.md#startlevel)
- [endLevel](map.IArcOption.md#endlevel)
- [color](map.IArcOption.md#color)
- [width](map.IArcOption.md#width)
- [startPoint](map.IArcOption.md#startpoint)
- [middlePoint](map.IArcOption.md#middlepoint)
- [endPoint](map.IArcOption.md#endpoint)
- [pixelRadius](map.IArcOption.md#pixelradius)

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

### color

• `Optional` **color**: [`ColorString`](../modules/map.md#colorstring)

线颜色（ARGB 整数），

**`Since`**

2.0.0

___

### width

• `Optional` **width**: `number`

线宽（像素），

**`Since`**

2.0.0

___

### startPoint

• **startPoint**: [`LatLng`](../classes/base.LatLng.md)

起点坐标，可与 middlePoint、endPoint 一起定义圆弧

**`Since`**

2.0.0

___

### middlePoint

• **middlePoint**: [`LatLng`](../classes/base.LatLng.md)

中点坐标，用于确定圆弧方向与圆心

**`Since`**

2.0.0

___

### endPoint

• **endPoint**: [`LatLng`](../classes/base.LatLng.md)

终点坐标，与起点、中点共同定义圆弧

**`Since`**

2.0.0

___

### pixelRadius

• `Optional` **pixelRadius**: `number`

像素半径

**`Since`**

2.0.0
