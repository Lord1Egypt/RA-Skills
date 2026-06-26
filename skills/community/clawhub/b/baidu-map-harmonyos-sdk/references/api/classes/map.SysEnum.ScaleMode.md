[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / [SysEnum](../modules/map.SysEnum.md) / ScaleMode

# Class: ScaleMode

[map](../modules/map.md).[SysEnum](../modules/map.SysEnum.md).ScaleMode

## Table of contents

### Constructors

- [constructor](map.SysEnum.ScaleMode.md#constructor)

### Properties

- [NO\_SCALE\_DPI](map.SysEnum.ScaleMode.md#no_scale_dpi)
- [SCALE\_DPI](map.SysEnum.ScaleMode.md#scale_dpi)
- [AUTO\_SCALE](map.SysEnum.ScaleMode.md#auto_scale)

### Methods

- [value](map.SysEnum.ScaleMode.md#value)

## Constructors

### constructor

• **new ScaleMode**(`id`): [`ScaleMode`](map.SysEnum.ScaleMode.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `id` | `number` |

#### Returns

[`ScaleMode`](map.SysEnum.ScaleMode.md)

## Properties

### NO\_SCALE\_DPI

▪ `Static` `Readonly` **NO\_SCALE\_DPI**: ``0``

不使用ScaleDpi缩放系数，使用绝对Pixel

**`Since`**

1.1.0

___

### SCALE\_DPI

▪ `Static` `Readonly` **SCALE\_DPI**: ``1``

使用ScaleDpi缩放系数

**`Since`**

1.1.0

___

### AUTO\_SCALE

▪ `Static` `Readonly` **AUTO\_SCALE**: ``2``

根据Marker 的 BitmapResource是否使用了ScaleDpi

**`Since`**

1.1.0

## Methods

### value

▸ **value**(): `number`

#### Returns

`number`
