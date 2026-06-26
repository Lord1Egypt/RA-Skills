[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IPolylineOption

# Interface: IPolylineOption

[map](../modules/map.md).IPolylineOption

线样式设置

**`Since`**

1.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`IPolylineOption`**

## Table of contents

### Properties

- [alpha](map.IPolylineOption.md#alpha)
- [visible](map.IPolylineOption.md#visible)
- [isClickable](map.IPolylineOption.md#isclickable)
- [zIndex](map.IPolylineOption.md#zindex)
- [startLevel](map.IPolylineOption.md#startlevel)
- [endLevel](map.IPolylineOption.md#endlevel)
- [points](map.IPolylineOption.md#points)
- [width](map.IPolylineOption.md#width)
- [fillcolor](map.IPolylineOption.md#fillcolor)
- [strokeWidth](map.IPolylineOption.md#strokewidth)
- [strokeColor](map.IPolylineOption.md#strokecolor)
- [textures](map.IPolylineOption.md#textures)
- [textureOption](map.IPolylineOption.md#textureoption)
- [join](map.IPolylineOption.md#join)
- [cap](map.IPolylineOption.md#cap)
- [startCapType](map.IPolylineOption.md#startcaptype)
- [endCapType](map.IPolylineOption.md#endcaptype)
- [isGeodesic](map.IPolylineOption.md#isgeodesic)
- [directionCross180](map.IPolylineOption.md#directioncross180)
- [isThined](map.IPolylineOption.md#isthined)
- [thinFactor](map.IPolylineOption.md#thinfactor)
- [smoothType](map.IPolylineOption.md#smoothtype)
- [smoothFactor](map.IPolylineOption.md#smoothfactor)
- [dottedline](map.IPolylineOption.md#dottedline)
- [dottedlineType](map.IPolylineOption.md#dottedlinetype)
- [colorList](map.IPolylineOption.md#colorlist)
- [indexList](map.IPolylineOption.md#indexlist)
- [isGradient](map.IPolylineOption.md#isgradient)
- [lineBloomType](map.IPolylineOption.md#linebloomtype)
- [lineBloomWidth](map.IPolylineOption.md#linebloomwidth)
- [lineBloomAlpha](map.IPolylineOption.md#linebloomalpha)
- [lineBloomGradientASPeed](map.IPolylineOption.md#linebloomgradientaspeed)
- [lineBloomBlurTimes](map.IPolylineOption.md#linebloomblurtimes)
- [collisionBehavior](map.IPolylineOption.md#collisionbehavior)
- [lineResourceId](map.IPolylineOption.md#lineresourceid)

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

坐标序列点

**`Since`**

1.0.0

___

### width

• `Optional` **width**: `number`

线宽

**`Since`**

1.0.0

___

### fillcolor

• `Optional` **fillcolor**: [`ColorString`](../modules/map.md#colorstring)

填充颜色

**`Since`**

1.0.0

___

### strokeWidth

• `Optional` **strokeWidth**: `number`

描边线宽

**`Since`**

1.2.0

___

### strokeColor

• `Optional` **strokeColor**: [`ColorString`](../modules/map.md#colorstring)

描边线颜色

**`Since`**

1.2.0

___

### textures

• `Optional` **textures**: [`ImageEntity`](../classes/map.ImageEntity.md)[]

填充纹理

**`Since`**

1.0.0

___

### textureOption

• `Optional` **textureOption**: [`TextureOption`](../enums/map.SysEnum.TextureOption.md)

设置纹理填充样式

**`Default`**

```ts
SysEnum.StrokeStyle.REAL
```

**`Since`**

1.2.0

___

### join

• `Optional` **join**: [`LineJoinType`](../enums/map.SysEnum.LineJoinType.md)

线拐点样式

**`Since`**

1.0.0

___

### cap

• `Optional` **cap**: [`LineCapType`](../enums/map.SysEnum.LineCapType.md)

线端点样式

**`Since`**

1.0.0

___

### startCapType

• `Optional` **startCapType**: [`LineCapType`](../enums/map.SysEnum.LineCapType.md)

线开始端点样式

**`Since`**

1.2.0

___

### endCapType

• `Optional` **endCapType**: [`LineCapType`](../enums/map.SysEnum.LineCapType.md)

线终点端点样式

**`Since`**

1.2.0

___

### isGeodesic

• `Optional` **isGeodesic**: `boolean`

是否启用大地线模式

**`Since`**

1.0.0

___

### directionCross180

• `Optional` **directionCross180**: [`LineDirectionCross`](../enums/map.SysEnum.LineDirectionCross.md)

跨域180度绘制方式

**`Since`**

1.0.0

___

### isThined

• `Optional` **isThined**: `boolean`

是否启用坐标点抽稀

**`Since`**

1.0.0

___

### thinFactor

• `Optional` **thinFactor**: `number`

抽稀容差值 >=0

**`Since`**

1.2.0

___

### smoothType

• `Optional` **smoothType**: [`SmoothType`](../enums/map.SysEnum.SmoothType.md)

平滑类型

**`Since`**

1.2.0

___

### smoothFactor

• `Optional` **smoothFactor**: `number`

平滑控制值

**`Since`**

1.2.0

___

### dottedline

• `Optional` **dottedline**: `boolean`

是否启用虚线绘制

**`Since`**

1.0.0

___

### dottedlineType

• `Optional` **dottedlineType**: [`PolylineDottedLineType`](../enums/map.SysEnum.PolylineDottedLineType.md)

虚线类型

**`Since`**

1.0.0

___

### colorList

• `Optional` **colorList**: [`ColorString`](../modules/map.md#colorstring)[]

填充颜色列表

**`Since`**

1.1.0

___

### indexList

• `Optional` **indexList**: `number`[]

填充多纹理的索引 数量等于点数减1

**`Since`**

1.1.0

___

### isGradient

• `Optional` **isGradient**: `boolean`

是否是渐变线

**`Since`**

1.1.0 *

___

### lineBloomType

• `Optional` **lineBloomType**: [`ELineBloomType`](../enums/map.SysEnum.ELineBloomType.md)

发光样式

**`Since`**

1.1.0 *

___

### lineBloomWidth

• `Optional` **lineBloomWidth**: `number`

发光线段的宽度 宽度 >0 ,默认普通线宽 * 2

**`Since`**

1.1.0 *

___

### lineBloomAlpha

• `Optional` **lineBloomAlpha**: `number`

发光线段的透明度 （0～1） 默认1

**`Since`**

1.1.0 *

___

### lineBloomGradientASPeed

• `Optional` **lineBloomGradientASPeed**: `number`

透明度渐变发光效果的渐变速率（1.0 ~ 10.0）默认5.0

**`Since`**

1.1.0 *

___

### lineBloomBlurTimes

• `Optional` **lineBloomBlurTimes**: `number`

模糊发光效果的模糊次数(1~10) 默认1次

**`Since`**

1.1.0 *

___

### collisionBehavior

• `Optional` **collisionBehavior**: [`CollisionBehavior`](../enums/map.SysEnum.CollisionBehavior.md)

___

### lineResourceId

• `Optional` **lineResourceId**: `number`
