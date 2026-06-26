[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / FileTileProvider

# Class: FileTileProvider

[map](../modules/map.md).FileTileProvider

## Hierarchy

- `default`

  ↳ **`FileTileProvider`**

## Table of contents

### Constructors

- [constructor](map.FileTileProvider.md#constructor)

### Methods

- [getMaxDisLevel](map.FileTileProvider.md#getmaxdislevel)
- [getMinDisLevel](map.FileTileProvider.md#getmindislevel)

## Constructors

### constructor

• **new FileTileProvider**(): [`FileTileProvider`](map.FileTileProvider.md)

#### Returns

[`FileTileProvider`](map.FileTileProvider.md)

#### Inherited from

TileProvider.constructor

## Methods

### getMaxDisLevel

▸ **getMaxDisLevel**(): `number`

设置TileOverlay最大显示级别

#### Returns

`number`

已设置的TileOverlay的最大显示级别
默认为 20

#### Inherited from

TileProvider.getMaxDisLevel

___

### getMinDisLevel

▸ **getMinDisLevel**(): `number`

设置TileOverlay的最小显示级别

#### Returns

`number`

已设置的TileOverlay的最小显示级别
默认为 3

#### Inherited from

TileProvider.getMinDisLevel
