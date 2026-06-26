[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ITextPathMarkerOption

# Interface: ITextPathMarkerOption

[map](../modules/map.md).ITextPathMarkerOption

弧线样式设置

**`Since`**

2.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`ITextPathMarkerOption`**

## Table of contents

### Properties

- [alpha](map.ITextPathMarkerOption.md#alpha)
- [visible](map.ITextPathMarkerOption.md#visible)
- [isClickable](map.ITextPathMarkerOption.md#isclickable)
- [zIndex](map.ITextPathMarkerOption.md#zindex)
- [startLevel](map.ITextPathMarkerOption.md#startlevel)
- [endLevel](map.ITextPathMarkerOption.md#endlevel)
- [text](map.ITextPathMarkerOption.md#text)
- [textColor](map.ITextPathMarkerOption.md#textcolor)
- [textSize](map.ITextPathMarkerOption.md#textsize)
- [points](map.ITextPathMarkerOption.md#points)
- [textBorderWidth](map.ITextPathMarkerOption.md#textborderwidth)
- [textBorderColor](map.ITextPathMarkerOption.md#textbordercolor)
- [textFontOption](map.ITextPathMarkerOption.md#textfontoption)

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

### text

• **text**: `string`

路名文字，

**`Since`**

2.0.0

___

### textColor

• **textColor**: [`ColorString`](../modules/map.md#colorstring)

文字颜色，

**`Since`**

2.0.0

___

### textSize

• **textSize**: `number`

文字大小，

**`Since`**

2.0.0

___

### points

• **points**: [`LatLng`](../classes/base.LatLng.md)[]

道路信息，至少两个点，

**`Since`**

2.0.0

___

### textBorderWidth

• `Optional` **textBorderWidth**: `number`

文字描边的宽度），

**`Since`**

2.0.0

___

### textBorderColor

• `Optional` **textBorderColor**: [`ColorString`](../modules/map.md#colorstring)

文字描边的颜色，

**`Since`**

2.0.0

___

### textFontOption

• `Optional` **textFontOption**: `number`

字体格式 0：标准，1：加粗，2：斜体，3：中粗，4：细体
