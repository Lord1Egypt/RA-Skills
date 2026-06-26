[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ILocationConfig

# Interface: ILocationConfig

[map](../modules/map.md).ILocationConfig

定位图层配置参数接口

## Table of contents

### Properties

- [locationMode](map.ILocationConfig.md#locationmode)
- [enableDirection](map.ILocationConfig.md#enabledirection)
- [enableRotation](map.ILocationConfig.md#enablerotation)
- [arrow](map.ILocationConfig.md#arrow)
- [arrowSize](map.ILocationConfig.md#arrowsize)
- [customMarker](map.ILocationConfig.md#custommarker)
- [gifMarker](map.ILocationConfig.md#gifmarker)
- [markerSize](map.ILocationConfig.md#markersize)
- [isNeedAnimation](map.ILocationConfig.md#isneedanimation)
- [accuracyCircleFillColor](map.ILocationConfig.md#accuracycirclefillcolor)
- [isEnableCustom](map.ILocationConfig.md#isenablecustom)

## Properties

### locationMode

• `Optional` **locationMode**: [`LocationMode`](../enums/map.SysEnum.LocationMode.md)

定位图层显示方式

**`Since`**

2.0.0

___

### enableDirection

• `Optional` **enableDirection**: `boolean`

是否显示方向信息

**`Default`**

```ts
true
```

**`Since`**

2.0.0

___

### enableRotation

• `Optional` **enableRotation**: `boolean`

是否支持图标旋转

**`Default`**

```ts
false
```

**`Since`**

2.0.0

___

### arrow

• `Optional` **arrow**: `any`

自定义定位箭头图标

**`Since`**

2.0.0

___

### arrowSize

• `Optional` **arrowSize**: `number`

箭头大小比例（范围 0.2~3.0）

**`Default`**

```ts
1.0
```

**`Since`**

2.0.0

___

### customMarker

• `Optional` **customMarker**: `any`

用户自定义定位图标（支持 png、jpg）

**`Since`**

2.0.0

___

### gifMarker

• `Optional` **gifMarker**: `string`

用户自定义 GIF 定位图标路径

**`Default`**

```ts
null（与 customMarker 二选一）
```

**`Since`**

2.0.0

___

### markerSize

• `Optional` **markerSize**: `number`

定位图标大小比例（范围 0.1~2.0）

**`Default`**

```ts
1.0
```

**`Since`**

2.0.0

___

### isNeedAnimation

• `Optional` **isNeedAnimation**: `boolean`

图标是否需要呼吸动画（仅箭头+图标模式下生效）

**`Default`**

```ts
true
```

**`Since`**

2.0.0

___

### accuracyCircleFillColor

• `Optional` **accuracyCircleFillColor**: [`ColorString`](../modules/map.md#colorstring)

精度圈填充颜色

**`Since`**

2.0.0

___

### isEnableCustom

• `Optional` **isEnableCustom**: `boolean`

是否支持图标自定义

**`Since`**

2.0.0
