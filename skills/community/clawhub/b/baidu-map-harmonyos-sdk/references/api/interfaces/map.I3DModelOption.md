[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / I3DModelOption

# Interface: I3DModelOption

[map](../modules/map.md).I3DModelOption

3DModel设置

**`Since`**

2.0.0

## Hierarchy

- [`IOverlayOption`](map.IOverlayOption.md)

  ↳ **`I3DModelOption`**

## Table of contents

### Properties

- [alpha](map.I3DModelOption.md#alpha)
- [visible](map.I3DModelOption.md#visible)
- [isClickable](map.I3DModelOption.md#isclickable)
- [zIndex](map.I3DModelOption.md#zindex)
- [startLevel](map.I3DModelOption.md#startlevel)
- [endLevel](map.I3DModelOption.md#endlevel)
- [modelPath](map.I3DModelOption.md#modelpath)
- [modelName](map.I3DModelOption.md#modelname)
- [position](map.I3DModelOption.md#position)
- [bm3DModelType](map.I3DModelOption.md#bm3dmodeltype)
- [alwaysShow](map.I3DModelOption.md#alwaysshow)
- [scale](map.I3DModelOption.md#scale)
- [zoomFixed](map.I3DModelOption.md#zoomfixed)
- [rotateX](map.I3DModelOption.md#rotatex)
- [rotateY](map.I3DModelOption.md#rotatey)
- [rotateZ](map.I3DModelOption.md#rotatez)
- [offsetX](map.I3DModelOption.md#offsetx)
- [offsetY](map.I3DModelOption.md#offsety)
- [offsetZ](map.I3DModelOption.md#offsetz)
- [animationIsEnable](map.I3DModelOption.md#animationisenable)
- [animationRepeatCount](map.I3DModelOption.md#animationrepeatcount)
- [animationSpeed](map.I3DModelOption.md#animationspeed)
- [animationIndex](map.I3DModelOption.md#animationindex)

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

### modelPath

• **modelPath**: `string`

模型文件沙盒路径（必填）

___

### modelName

• **modelName**: `string`

模型文件名（必填）

___

### position

• **position**: [`LatLng`](../classes/base.LatLng.md)

模型地理坐标（必填）

___

### bm3DModelType

• `Optional` **bm3DModelType**: [`BM3DModelType`](../enums/map.SysEnum.BM3DModelType.md)

3D模型文件类型（默认：BM3DModelType.BM3DModelTypeObj 即 .obj 格式）
支持类型：.obj（0）、.gltf（2）

___

### alwaysShow

• `Optional` **alwaysShow**: `boolean`

模型是否不被楼栋遮挡（默认：未明确，需根据业务设置）
true：不被遮挡（始终显示在楼栋上层）；false：被楼栋遮挡

___

### scale

• `Optional` **scale**: `number`

模型缩放比例（默认：1.0f）
说明：值越大模型越大，值为0时模型不可见

___

### zoomFixed

• `Optional` **zoomFixed**: `boolean`

缩放比例是否不随地图缩放变化（默认：false）
true：scale 固定，地图缩放时模型大小不变；false：scale 随地图缩放同步变化

___

### rotateX

• `Optional` **rotateX**: `number`

X轴旋转角度（默认：0.0f）
约束：取值范围 [0.0f, 360.0f]（0度~360度）

___

### rotateY

• `Optional` **rotateY**: `number`

Y轴旋转角度（默认：0.0f）
约束：取值范围 [0.0f, 360.0f]（0度~360度）

___

### rotateZ

• `Optional` **rotateZ**: `number`

Z轴旋转角度（默认：0.0f）
约束：取值范围 [0.0f, 360.0f]（0度~360度）

___

### offsetX

• `Optional` **offsetX**: `number`

X轴偏移像素（默认：0.0f）
说明：模型在屏幕X方向的像素偏移（正数向右，负数向左）

___

### offsetY

• `Optional` **offsetY**: `number`

Y轴偏移像素（默认：0.0f）
说明：模型在屏幕Y方向的像素偏移（正数向下，负数向上，具体需结合坐标系）

___

### offsetZ

• `Optional` **offsetZ**: `number`

Z轴偏移像素（默认：0.0f）
说明：模型在3D空间Z方向的像素偏移（影响模型前后层级）

___

### animationIsEnable

• `Optional` **animationIsEnable**: `boolean`

模型骨骼动画是否启用（默认：false）
说明：仅GLTF模型支持，true：添加模型后立即执行动画；false：不执行动画

___

### animationRepeatCount

• `Optional` **animationRepeatCount**: `number`

模型动画重复执行次数（默认：0）
说明：0表示动画一直重复执行；>0表示重复指定次数后停止

___

### animationSpeed

• `Optional` **animationSpeed**: `number`

模型动画播放倍速（默认：1.0）

___

### animationIndex

• `Optional` **animationIndex**: `number`

当前播放的模型动画索引
说明：GLTF模型可能包含多个动画，通过索引指定播放哪个动画
