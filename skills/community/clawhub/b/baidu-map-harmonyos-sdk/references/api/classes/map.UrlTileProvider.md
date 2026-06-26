[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / UrlTileProvider

# Class: UrlTileProvider

[map](../modules/map.md).UrlTileProvider

在线TileOverlay的显示Provider构造器

**`Since`**

1.2.0

## Hierarchy

- `default`

  ↳ **`UrlTileProvider`**

## Table of contents

### Constructors

- [constructor](map.UrlTileProvider.md#constructor)

### Methods

- [getMaxDisLevel](map.UrlTileProvider.md#getmaxdislevel)
- [getMinDisLevel](map.UrlTileProvider.md#getmindislevel)
- [getTileUrl](map.UrlTileProvider.md#gettileurl)

## Constructors

### constructor

• **new UrlTileProvider**(): [`UrlTileProvider`](map.UrlTileProvider.md)

#### Returns

[`UrlTileProvider`](map.UrlTileProvider.md)

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

___

### getTileUrl

▸ **getTileUrl**(): `string`

设置在线显示TileOverlay的Url

#### Returns

`string`

在线TileOverlay的URL
注：URL中必须包括"{x},{y},{z}"属性,在绘制过程中，会根据地图真实的x,y,z进行替换
eg: http://server?&x={x}&y={y}&z={z}
