[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IGroundOption

# Interface: IGroundOption

[map](../modules/map.md).IGroundOption

贴图样式设置

**`Since`**

1.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`IGroundOption`**

## Table of contents

### Properties

- [alpha](map.IGroundOption.md#alpha)
- [visible](map.IGroundOption.md#visible)
- [isClickable](map.IGroundOption.md#isclickable)
- [zIndex](map.IGroundOption.md#zindex)
- [startLevel](map.IGroundOption.md#startlevel)
- [endLevel](map.IGroundOption.md#endlevel)
- [image](map.IGroundOption.md#image)
- [bounds](map.IGroundOption.md#bounds)
- [anchorX](map.IGroundOption.md#anchorx)
- [anchorY](map.IGroundOption.md#anchory)
- [transparency](map.IGroundOption.md#transparency)

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

### image

• **image**: [`ImageEntity`](../classes/map.ImageEntity.md)

填充图像

**`Since`**

1.0.0

___

### bounds

• **bounds**: [[`LatLng`](../classes/base.LatLng.md), [`LatLng`](../classes/base.LatLng.md)]

坐标范围

**`Since`**

1.0.0

___

### anchorX

• `Optional` **anchorX**: `number`

X轴锚点

**`Since`**

1.0.0

___

### anchorY

• `Optional` **anchorY**: `number`

Y轴锚点

**`Since`**

1.0.0

___

### transparency

• `Optional` **transparency**: `number`

透明度

**`Since`**

1.0.0
