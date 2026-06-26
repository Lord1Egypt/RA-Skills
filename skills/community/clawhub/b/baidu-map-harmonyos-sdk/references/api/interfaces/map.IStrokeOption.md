[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / IStrokeOption

# Interface: IStrokeOption

[map](../modules/map.md).IStrokeOption

描边样式设置

**`Since`**

1.0.0

## Table of contents

### Properties

- [strokeWidth](map.IStrokeOption.md#strokewidth)
- [color](map.IStrokeOption.md#color)
- [strokeStyle](map.IStrokeOption.md#strokestyle)
- [strokeTexture](map.IStrokeOption.md#stroketexture)
- [textureOption](map.IStrokeOption.md#textureoption)

## Properties

### strokeWidth

• `Optional` **strokeWidth**: `number`

设置描边宽度，单位：像素

**`Since`**

1.0.0

___

### color

• `Optional` **color**: [`ColorString`](../modules/map.md#colorstring)

设置描边颜色：颜色名、rgb或rgba或者#十六进制

**`Since`**

1.0.0

___

### strokeStyle

• `Optional` **strokeStyle**: [`StrokeStyle`](../enums/map.SysEnum.StrokeStyle.md)

设置描边样式
[SysEnum.StrokeStyle](../enums/map.SysEnum.StrokeStyle.html)枚举值

**`Default`**

```ts
SysEnum.StrokeStyle.REAL
```

**`Since`**

1.0.0

___

### strokeTexture

• `Optional` **strokeTexture**: [`ImageEntity`](../classes/map.ImageEntity.md)

设置描边纹理，与描边颜色进行叠加现实

**`Since`**

1.2.0

___

### textureOption

• `Optional` **textureOption**: [`TextureOption`](../enums/map.SysEnum.TextureOption.md)

设置描边纹理样式

**`Default`**

```ts
SysEnum.StrokeStyle.REAL
```

**`Since`**

1.2.0
