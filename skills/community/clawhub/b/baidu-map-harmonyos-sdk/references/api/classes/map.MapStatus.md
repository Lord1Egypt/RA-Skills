[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / MapStatus

# Class: MapStatus

[map](../modules/map.md).MapStatus

地图显示状态类

**`Abstract`**

提供地图显示状态设置

## Table of contents

### Constructors

- [constructor](map.MapStatus.md#constructor)

### Accessors

- [rotate](map.MapStatus.md#rotate)
- [level](map.MapStatus.md#level)
- [overlooking](map.MapStatus.md#overlooking)
- [centerPoint](map.MapStatus.md#centerpoint)
- [zoomUnits](map.MapStatus.md#zoomunits)
- [ptOffset](map.MapStatus.md#ptoffset)
- [geoRound](map.MapStatus.md#georound)
- [winRound](map.MapStatus.md#winround)
- [isAnimate](map.MapStatus.md#isanimate)
- [animationTime](map.MapStatus.md#animationtime)
- [maxZoom](map.MapStatus.md#maxzoom)
- [minZoom](map.MapStatus.md#minzoom)

### Methods

- [setRotate](map.MapStatus.md#setrotate)
- [setRotatePlus](map.MapStatus.md#setrotateplus)
- [getRotate](map.MapStatus.md#getrotate)
- [setLevel](map.MapStatus.md#setlevel)
- [getLevel](map.MapStatus.md#getlevel)
- [setOverlooking](map.MapStatus.md#setoverlooking)
- [setOverlookingPlus](map.MapStatus.md#setoverlookingplus)
- [getOverlooking](map.MapStatus.md#getoverlooking)
- [setCenterPoint](map.MapStatus.md#setcenterpoint)
- [getCenterPoint](map.MapStatus.md#getcenterpoint)
- [getCenterPointMC](map.MapStatus.md#getcenterpointmc)
- [getPtOffset](map.MapStatus.md#getptoffset)
- [setPtOffset](map.MapStatus.md#setptoffset)
- [getGeoRound](map.MapStatus.md#getgeoround)
- [setWinRound](map.MapStatus.md#setwinround)
- [getWinRound](map.MapStatus.md#getwinround)
- [setIsAnimate](map.MapStatus.md#setisanimate)
- [setAnimationTime](map.MapStatus.md#setanimationtime)
- [getAnimationTime](map.MapStatus.md#getanimationtime)
- [updateLevel](map.MapStatus.md#updatelevel)
- [parseFromBundle](map.MapStatus.md#parsefrombundle)
- [toBundle](map.MapStatus.md#tobundle)
- [updateConfig](map.MapStatus.md#updateconfig)
- [refresh](map.MapStatus.md#refresh)
- [destroy](map.MapStatus.md#destroy)
- [toString](map.MapStatus.md#tostring)

## Constructors

### constructor

• **new MapStatus**(`opts?`): [`MapStatus`](map.MapStatus.md)

如果opts为空，则默认IMapStatusOption参数如下：
```Typescript
{
center: new LatLng(39.914935, 116.403119),
zoom: 3,
rotate: 0,
overlook: 0,
ptOffset: [0, 0]
}
```

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts?` | [`IMapStatusOption`](../interfaces/map.IMapStatusOption.md) |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

## Accessors

### rotate

• `get` **rotate**(): `number`

获取旋转角度

#### Returns

`number`

**`Default`**

```ts
0
```

**`Since`**

1.0.0

• `set` **rotate**(`deg`): `void`

设置旋转角度

#### Parameters

| Name | Type |
| :------ | :------ |
| `deg` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### level

• `get` **level**(): `number`

获取地图显示级别

#### Returns

`number`

**`Since`**

1.0.0

• `set` **level**(`val`): `void`

设置地图显示级别

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `val` | `number` | 取值范围[minZoom,maxZoom] |

#### Returns

`void`

**`Since`**

1.0.0

___

### overlooking

• `get` **overlooking**(): `number`

获取地图俯仰角

#### Returns

`number`

**`Since`**

1.0.0

• `set` **overlooking**(`deg`): `void`

设置地图俯仰角

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `deg` | `number` | 取值范围[0,90] |

#### Returns

`void`

**`Since`**

1.0.0

___

### centerPoint

• `get` **centerPoint**(): [`LatLng`](base.LatLng.md)

获取地图地理坐标中心点

#### Returns

[`LatLng`](base.LatLng.md)

**`Since`**

1.0.0

• `set` **centerPoint**(`input`): `void`

设置地图中心点，百度地理坐标或者平面坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `input` | [`LatLng`](base.LatLng.md) \| [`Point`](base.Point.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### zoomUnits

• `get` **zoomUnits**(): `number`

获取当前地图每像素代表多少墨卡托

#### Returns

`number`

**`Since`**

1.0.0

___

### ptOffset

• `set` **ptOffset**(`ptOffset`): `void`

设置锚点位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `ptOffset` | [`number`, `number`] |

#### Returns

`void`

**`Since`**

1.0.0

___

### geoRound

• `get` **geoRound**(): [`GeoBound`](map.GeoBound.md)

获取地理显示范围

#### Returns

[`GeoBound`](map.GeoBound.md)

**`Since`**

1.1.0

___

### winRound

• `get` **winRound**(): [`WinBound`](map.WinBound.md)

获取地图窗口范围

#### Returns

[`WinBound`](map.WinBound.md)

**`Since`**

1.1.0

• `set` **winRound**(`winRound`): `void`

设置地图窗口范围

#### Parameters

| Name | Type |
| :------ | :------ |
| `winRound` | [`WinBound`](map.WinBound.md) |

#### Returns

`void`

**`Since`**

1.1.0

___

### isAnimate

• `get` **isAnimate**(): `boolean`

是否启用动画显示

#### Returns

`boolean`

• `set` **isAnimate**(`aniAble`): `void`

设置是否启用动画显示

#### Parameters

| Name | Type |
| :------ | :------ |
| `aniAble` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

___

### animationTime

• `get` **animationTime**(): `number`

动画持续时间

#### Returns

`number`

**`Since`**

1.1.0

• `set` **animationTime**(`aniTime`): `void`

动画持续时间

#### Parameters

| Name | Type |
| :------ | :------ |
| `aniTime` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### maxZoom

• `get` **maxZoom**(): `number`

获取地图显示最大级别

#### Returns

`number`

**`Since`**

1.0.0

• `set` **maxZoom**(`zoom`): `void`

设置地图显示最大级别

#### Parameters

| Name | Type |
| :------ | :------ |
| `zoom` | `number` |

#### Returns

`void`

**`Default`**

```ts
22
```

**`Since`**

1.0.0

___

### minZoom

• `get` **minZoom**(): `number`

获取地图显示最小级别

#### Returns

`number`

**`Since`**

1.0.0

• `set` **minZoom**(`zoom`): `void`

设置地图显示最小级别

#### Parameters

| Name | Type |
| :------ | :------ |
| `zoom` | `number` |

#### Returns

`void`

**`Default`**

```ts
3
```

**`Since`**

1.0.0

## Methods

### setRotate

▸ **setRotate**(`deg`): [`MapStatus`](map.MapStatus.md)

设置旋转角度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `deg` | `number` | 顺时针表达，取值范围[0,360] |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### setRotatePlus

▸ **setRotatePlus**(`val`): [`MapStatus`](map.MapStatus.md)

设置旋转增量

#### Parameters

| Name | Type |
| :------ | :------ |
| `val` | `number` |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### getRotate

▸ **getRotate**(): `number`

获取旋转角度

#### Returns

`number`

**`Since`**

1.0.0

___

### setLevel

▸ **setLevel**(`val`): [`MapStatus`](map.MapStatus.md)

设置地图显示级别

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `val` | `number` | 取值范围[minZoom,maxZoom] |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### getLevel

▸ **getLevel**(): `number`

获取地图显示级别

#### Returns

`number`

**`Since`**

1.0.0

___

### setOverlooking

▸ **setOverlooking**(`deg`): [`MapStatus`](map.MapStatus.md)

设置地图俯仰角

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `deg` | `number` | 取值范围[0,90] |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### setOverlookingPlus

▸ **setOverlookingPlus**(`plus`): [`MapStatus`](map.MapStatus.md)

设置地图俯仰角增量

#### Parameters

| Name | Type |
| :------ | :------ |
| `plus` | `number` |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### getOverlooking

▸ **getOverlooking**(): `number`

获取地图俯仰角

#### Returns

`number`

**`Since`**

1.0.0

___

### setCenterPoint

▸ **setCenterPoint**(`input`): [`MapStatus`](map.MapStatus.md)

设置地图中心点，百度地理坐标或者平面坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `input` | [`LatLng`](base.LatLng.md) \| [`Point`](base.Point.md) |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### getCenterPoint

▸ **getCenterPoint**(): [`LatLng`](base.LatLng.md)

获取地图地理坐标中心点

#### Returns

[`LatLng`](base.LatLng.md)

**`Since`**

1.0.0

___

### getCenterPointMC

▸ **getCenterPointMC**(): [`Point`](base.Point.md)

获取地图平面坐标中心点

#### Returns

[`Point`](base.Point.md)

**`Since`**

1.0.0

___

### getPtOffset

▸ **getPtOffset**(): `number`[]

获取锚点位置

#### Returns

`number`[]

**`Since`**

1.0.0

___

### setPtOffset

▸ **setPtOffset**(`ptOffset`): [`MapStatus`](map.MapStatus.md)

设置锚点位置

#### Parameters

| Name | Type |
| :------ | :------ |
| `ptOffset` | [`number`, `number`] |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### getGeoRound

▸ **getGeoRound**(): [`GeoBound`](map.GeoBound.md)

获取地理显示范围

#### Returns

[`GeoBound`](map.GeoBound.md)

**`Since`**

1.1.0

___

### setWinRound

▸ **setWinRound**(`winRound`): [`MapStatus`](map.MapStatus.md)

设置地图窗口范围

#### Parameters

| Name | Type |
| :------ | :------ |
| `winRound` | [`WinBound`](map.WinBound.md) |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.1.0

___

### getWinRound

▸ **getWinRound**(): [`WinBound`](map.WinBound.md)

获取地图窗口范围

#### Returns

[`WinBound`](map.WinBound.md)

**`Since`**

1.1.0

___

### setIsAnimate

▸ **setIsAnimate**(`aniAble`): [`MapStatus`](map.MapStatus.md)

设置是否启用动画显示

#### Parameters

| Name | Type |
| :------ | :------ |
| `aniAble` | `boolean` |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### setAnimationTime

▸ **setAnimationTime**(`aniTime`): [`MapStatus`](map.MapStatus.md)

动画持续时间

#### Parameters

| Name | Type |
| :------ | :------ |
| `aniTime` | `number` |

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Since`**

1.0.0

___

### getAnimationTime

▸ **getAnimationTime**(): `number`

动画持续时间

#### Returns

`number`

**`Since`**

1.1.0

___

### updateLevel

▸ **updateLevel**(): `void`

根据缩放级别限制进行调整

#### Returns

`void`

___

### parseFromBundle

▸ **parseFromBundle**(`statusObj`): `void`

解析 native 回传的数据

#### Parameters

| Name | Type |
| :------ | :------ |
| `statusObj` | [`MapStatusBundle`](../interfaces/map.MapStatusBundle.md) |

#### Returns

`void`

___

### toBundle

▸ **toBundle**(): [`MapStatusBundle`](../interfaces/map.MapStatusBundle.md)

结合map内容与本结构实例化数据进行native需求数据封装

#### Returns

[`MapStatusBundle`](../interfaces/map.MapStatusBundle.md)

___

### updateConfig

▸ **updateConfig**(`opts`): `void`

整体设置各项参数

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts` | [`IMapStatusOption`](../interfaces/map.IMapStatusOption.md) |

#### Returns

`void`

___

### refresh

▸ **refresh**(): `void`

#### Returns

`void`

___

### destroy

▸ **destroy**(): `void`

#### Returns

`void`

___

### toString

▸ **toString**(): `string`

#### Returns

`string`
