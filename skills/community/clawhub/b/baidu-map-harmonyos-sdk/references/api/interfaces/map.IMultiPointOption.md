[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IMultiPointOption

# Interface: IMultiPointOption

[map](../modules/map.md).IMultiPointOption

海量point设置

**`Since`**

2.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`IMultiPointOption`**

## Table of contents

### Properties

- [alpha](map.IMultiPointOption.md#alpha)
- [visible](map.IMultiPointOption.md#visible)
- [isClickable](map.IMultiPointOption.md#isclickable)
- [zIndex](map.IMultiPointOption.md#zindex)
- [startLevel](map.IMultiPointOption.md#startlevel)
- [endLevel](map.IMultiPointOption.md#endlevel)
- [multiPointItems](map.IMultiPointOption.md#multipointitems)
- [pointSize](map.IMultiPointOption.md#pointsize)
- [anchor](map.IMultiPointOption.md#anchor)
- [icon](map.IMultiPointOption.md#icon)

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

### multiPointItems

• **multiPointItems**: [`MultiPointItem`](../classes/map.MultiPointItem.md)[]

添加海量点数据集合（必填）@since 2.0.0

___

### pointSize

• `Optional` **pointSize**: `IPointSize`

纹理渲染大小，默认为icon图片大小，

**`Since`**

2.0.0

___

### anchor

• `Optional` **anchor**: [`IAnchor`](map.IAnchor.md)

设置 MultiPoint 覆盖物的锚点比例，默认（0.5, 0.5）水平居中，垂直下对齐

**`Since`**

2.0.0

___

### icon

• **icon**: [`ImageEntity`](../classes/map.ImageEntity.md)

设置 MultiPoint 覆盖物的图标 （必填）

**`Since`**

2.0.0
