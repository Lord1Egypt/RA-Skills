[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IPolygonOption

# Interface: IPolygonOption

[map](../modules/map.md).IPolygonOption

面样式设置

**`Since`**

1.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`IPolygonOption`**

## Table of contents

### Properties

- [alpha](map.IPolygonOption.md#alpha)
- [visible](map.IPolygonOption.md#visible)
- [isClickable](map.IPolygonOption.md#isclickable)
- [zIndex](map.IPolygonOption.md#zindex)
- [startLevel](map.IPolygonOption.md#startlevel)
- [endLevel](map.IPolygonOption.md#endlevel)
- [points](map.IPolygonOption.md#points)
- [holePoints](map.IPolygonOption.md#holepoints)
- [fillcolor](map.IPolygonOption.md#fillcolor)
- [stroke](map.IPolygonOption.md#stroke)
- [thin](map.IPolygonOption.md#thin)
- [thinFactor](map.IPolygonOption.md#thinfactor)
- [jointType](map.IPolygonOption.md#jointtype)
- [isHoleClickable](map.IPolygonOption.md#isholeclickable)

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

• **points**: `string` \| [`LatLng`](../classes/base.LatLng.md)[]

坐标序列点

**`Since`**

1.0.0

___

### holePoints

• `Optional` **holePoints**: [`LatLng`](../classes/base.LatLng.md)[] \| [`LatLng`](../classes/base.LatLng.md)[][]

镂空坐标序列点

**`Since`**

1.2.1

___

### fillcolor

• `Optional` **fillcolor**: [`ColorString`](../modules/map.md#colorstring)

填充颜色

**`Since`**

1.0.0

___

### stroke

• `Optional` **stroke**: [`Stroke`](../classes/map.Stroke.md)

描边样式配置

**`Since`**

1.0.0

___

### thin

• `Optional` **thin**: `boolean`

是否启用抽稀@since 1.2.0

___

### thinFactor

• `Optional` **thinFactor**: `number`

抽稀容差值 >=0

**`Since`**

1.2.0

___

### jointType

• `Optional` **jointType**: [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md)

拐点类型

**`Since`**

1.2.0

___

### isHoleClickable

• `Optional` **isHoleClickable**: `boolean`

镂空是否可点击

**`Since`**

1.2.1
