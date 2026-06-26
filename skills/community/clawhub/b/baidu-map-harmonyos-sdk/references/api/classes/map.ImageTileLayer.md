[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ImageTileLayer

# Class: ImageTileLayer

[map](../modules/map.md).ImageTileLayer

图像瓦片图层

**`Since`**

1.2.0

## Hierarchy

- `default`

  ↳ **`ImageTileLayer`**

## Table of contents

### Accessors

- [visible](map.ImageTileLayer.md#visible)
- [maxTileTmp](map.ImageTileLayer.md#maxtiletmp)
- [maxDisplay](map.ImageTileLayer.md#maxdisplay)
- [minDisplay](map.ImageTileLayer.md#mindisplay)
- [initRectr](map.ImageTileLayer.md#initrectr)
- [initRectb](map.ImageTileLayer.md#initrectb)
- [initRectl](map.ImageTileLayer.md#initrectl)
- [initRectt](map.ImageTileLayer.md#initrectt)
- [datasource](map.ImageTileLayer.md#datasource)
- [urlString](map.ImageTileLayer.md#urlstring)

### Methods

- [setName](map.ImageTileLayer.md#setname)
- [getName](map.ImageTileLayer.md#getname)
- [getLayerId](map.ImageTileLayer.md#getlayerid)
- [setVisible](map.ImageTileLayer.md#setvisible)
- [clear](map.ImageTileLayer.md#clear)
- [setData](map.ImageTileLayer.md#setdata)
- [getData](map.ImageTileLayer.md#getdata)
- [createWithMapControl](map.ImageTileLayer.md#createwithmapcontrol)
- [setTileProvide](map.ImageTileLayer.md#settileprovide)
- [getUpdateType](map.ImageTileLayer.md#getupdatetype)
- [getTimerEscape](map.ImageTileLayer.md#gettimerescape)
- [setUrlString](map.ImageTileLayer.md#seturlstring)
- [setMaxTileTmp](map.ImageTileLayer.md#setmaxtiletmp)
- [setSourceRegion](map.ImageTileLayer.md#setsourceregion)
- [getSourceRegion](map.ImageTileLayer.md#getsourceregion)
- [setDisplayLevel](map.ImageTileLayer.md#setdisplaylevel)
- [update](map.ImageTileLayer.md#update)

## Accessors

### visible

• `get` **visible**(): `boolean`

获取图层当前状态

#### Returns

`boolean`

**`Since`**

1.0.0

#### Inherited from

TileLayer.visible

• `set` **visible**(`val`): `void`

设置图层当前状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

TileLayer.visible

___

### maxTileTmp

• `get` **maxTileTmp**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.maxTileTmp

___

### maxDisplay

• `get` **maxDisplay**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.maxDisplay

___

### minDisplay

• `get` **minDisplay**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.minDisplay

___

### initRectr

• `get` **initRectr**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.initRectr

___

### initRectb

• `get` **initRectb**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.initRectb

___

### initRectl

• `get` **initRectl**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.initRectl

___

### initRectt

• `get` **initRectt**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.initRectt

___

### datasource

• `get` **datasource**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.datasource

___

### urlString

• `get` **urlString**(): `string`

#### Returns

`string`

#### Inherited from

TileLayer.urlString

## Methods

### setName

▸ **setName**(`name`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `name` | `string` |

#### Returns

`void`

#### Inherited from

TileLayer.setName

___

### getName

▸ **getName**(): `string`

#### Returns

`string`

#### Inherited from

TileLayer.getName

___

### getLayerId

▸ **getLayerId**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.getLayerId

___

### setVisible

▸ **setVisible**(`visible`): `void`

设置图层当前状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `visible` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

#### Inherited from

TileLayer.setVisible

___

### clear

▸ **clear**(): `void`

#### Returns

`void`

#### Inherited from

TileLayer.clear

___

### setData

▸ **setData**(`strJson`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `strJson` | `string` |

#### Returns

`void`

#### Inherited from

TileLayer.setData

___

### getData

▸ **getData**(): `string`

#### Returns

`string`

#### Inherited from

TileLayer.getData

___

### createWithMapControl

▸ **createWithMapControl**(`mapCtrl`, `tileProvider`, `updateType?`, `timerEscap?`): ``null`` \| [`ImageTileLayer`](map.ImageTileLayer.md)

创建一个ImageTileLayer对象

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `mapCtrl` | [`MapController`](map.MapController.md) | `undefined` | 必须，地图控制器对象 |
| `tileProvider` | `default` | `undefined` | 必须，瓦片图层的Provider对象 |
| `updateType` | `number` | `LayerUpdateType.UpdateMapStatusChangeLater` | 可选，更新类型,默认是LayerUpdateType.UpdateMapStatusChangeLater,表示地图状态变化时更新瓦片图层 |
| `timerEscap` | `number` | `1000` | 可选，瓦片图层更新间隔时间,默认是1000ms |

#### Returns

``null`` \| [`ImageTileLayer`](map.ImageTileLayer.md)

___

### setTileProvide

▸ **setTileProvide**(`tileProvider`): ``null`` \| [`ImageTileLayer`](map.ImageTileLayer.md)

设置瓦片图层的Provider

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `tileProvider` | `default` | 瓦片图的Provider对象 |

#### Returns

``null`` \| [`ImageTileLayer`](map.ImageTileLayer.md)

**`Since`**

1.2.0

#### Overrides

TileLayer.setTileProvide

___

### getUpdateType

▸ **getUpdateType**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.getUpdateType

___

### getTimerEscape

▸ **getTimerEscape**(): `number`

#### Returns

`number`

#### Inherited from

TileLayer.getTimerEscape

___

### setUrlString

▸ **setUrlString**(`url`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `url` | `string` |

#### Returns

`void`

#### Inherited from

TileLayer.setUrlString

___

### setMaxTileTmp

▸ **setMaxTileTmp**(`maxTileTmp`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `maxTileTmp` | `number` |

#### Returns

`void`

#### Inherited from

TileLayer.setMaxTileTmp

___

### setSourceRegion

▸ **setSourceRegion**(`bound`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `bound` | [`Bounds`](base.Bounds.md) |

#### Returns

`void`

#### Inherited from

TileLayer.setSourceRegion

___

### getSourceRegion

▸ **getSourceRegion**(): [`Bounds`](base.Bounds.md)

#### Returns

[`Bounds`](base.Bounds.md)

#### Inherited from

TileLayer.getSourceRegion

___

### setDisplayLevel

▸ **setDisplayLevel**(`minDisplay`, `maxDisplay`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `minDisplay` | `number` |
| `maxDisplay` | `number` |

#### Returns

`void`

#### Inherited from

TileLayer.setDisplayLevel

___

### update

▸ **update**(): `void`

#### Returns

`void`

#### Inherited from

TileLayer.update
