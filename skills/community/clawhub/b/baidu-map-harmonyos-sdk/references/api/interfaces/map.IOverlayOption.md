[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IOverlayOption

# Interface: IOverlayOption

[map](../modules/map.md).IOverlayOption

覆盖物基础样式设置

**`Since`**

1.1.0

## Hierarchy

- **`IOverlayOption`**

  ↳ [`ICircleOption`](map.ICircleOption.md)

  ↳ [`IDotOption`](map.IDotOption.md)

  ↳ [`IGroundOption`](map.IGroundOption.md)

  ↳ [`IPolygonOption`](map.IPolygonOption.md)

  ↳ [`IPolylineOption`](map.IPolylineOption.md)

  ↳ [`IBaseMarkerOption`](map.IBaseMarkerOption.md)

  ↳ [`IInfoWindow`](map.IInfoWindow.md)

  ↳ [`I3DModelOption`](map.I3DModelOption.md)

  ↳ [`ITrackOption`](map.ITrackOption.md)

  ↳ [`IMultiPointOption`](map.IMultiPointOption.md)

  ↳ [`ITextPathMarkerOption`](map.ITextPathMarkerOption.md)

  ↳ [`IArcOption`](map.IArcOption.md)

## Table of contents

### Properties

- [alpha](map.IOverlayOption.md#alpha)
- [visible](map.IOverlayOption.md#visible)
- [isClickable](map.IOverlayOption.md#isclickable)
- [zIndex](map.IOverlayOption.md#zindex)
- [startLevel](map.IOverlayOption.md#startlevel)
- [endLevel](map.IOverlayOption.md#endlevel)

## Properties

### alpha

• `Optional` **alpha**: `number`

设置透明度 [0，1]

**`Since`**

1.1.0

___

### visible

• `Optional` **visible**: `boolean`

是否显示

**`Since`**

1.1.0

___

### isClickable

• `Optional` **isClickable**: `boolean`

是否启用点击

**`Since`**

1.1.0

___

### zIndex

• `Optional` **zIndex**: `number`

设置层级

**`Since`**

1.1.0

___

### startLevel

• `Optional` **startLevel**: `number`

开始显示地图缩放级别

**`Since`**

1.0.0

___

### endLevel

• `Optional` **endLevel**: `number`

结束显示地图缩放级别

**`Since`**

1.0.0
