[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IInfoWindow

# Interface: IInfoWindow

[map](../modules/map.md).IInfoWindow

InfoWindow覆盖物初始化设置

**`Since`**

1.1.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`IInfoWindow`**

## Table of contents

### Properties

- [alpha](map.IInfoWindow.md#alpha)
- [visible](map.IInfoWindow.md#visible)
- [isClickable](map.IInfoWindow.md#isclickable)
- [zIndex](map.IInfoWindow.md#zindex)
- [startLevel](map.IInfoWindow.md#startlevel)
- [endLevel](map.IInfoWindow.md#endlevel)
- [position](map.IInfoWindow.md#position)
- [content](map.IInfoWindow.md#content)
- [anchorX](map.IInfoWindow.md#anchorx)
- [anchorY](map.IInfoWindow.md#anchory)
- [isPerspective](map.IInfoWindow.md#isperspective)
- [rotate](map.IInfoWindow.md#rotate)
- [yOffset](map.IInfoWindow.md#yoffset)
- [isFlat](map.IInfoWindow.md#isflat)

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

1.1.0

___

### content

• `Optional` **content**: [`ImageEntity`](../classes/map.ImageEntity.md)

显示内容

**`Since`**

1.1.0

___

### anchorX

• `Optional` **anchorX**: `number`

X轴锚点位置

**`Since`**

1.1.0

___

### anchorY

• `Optional` **anchorY**: `number`

Y轴锚点位置

**`Since`**

1.1.0

___

### isPerspective

• `Optional` **isPerspective**: `boolean`

是否启用透视效果

**`Since`**

1.1.0

___

### rotate

• `Optional` **rotate**: `number`

旋转角度

**`Since`**

1.1.0

___

### yOffset

• `Optional` **yOffset**: `number`

Y轴偏移量

**`Since`**

1.1.0

___

### isFlat

• `Optional` **isFlat**: `boolean`

是否启用贴地效果

**`Since`**

1.1.0
