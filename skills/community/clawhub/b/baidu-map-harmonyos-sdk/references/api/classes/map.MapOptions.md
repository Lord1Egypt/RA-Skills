[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / MapOptions

# Class: MapOptions

[map](../modules/map.md).MapOptions

地图配置类

**`Abstract`**

提供地图交互设置以及地图显示状态设置等

**`Since`**

1.0.0

**`Package`**

@bdmap/map

## Table of contents

### Constructors

- [constructor](map.MapOptions.md#constructor)

### Accessors

- [mapStatus](map.MapOptions.md#mapstatus)
- [rotateGesturesEnabled](map.MapOptions.md#rotategesturesenabled)
- [moveGesturesEnabled](map.MapOptions.md#movegesturesenabled)
- [overlookingGesturesEnabled](map.MapOptions.md#overlookinggesturesenabled)
- [zoomGesturesEnabled](map.MapOptions.md#zoomgesturesenabled)
- [showSatelliteMap](map.MapOptions.md#showsatellitemap)
- [showBaseIndoorMap](map.MapOptions.md#showbaseindoormap)
- [showTrafficMap](map.MapOptions.md#showtrafficmap)
- [showMapPoi](map.MapOptions.md#showmappoi)
- [showMapIndoorPoi](map.MapOptions.md#showmapindoorpoi)
- [touchNearly](map.MapOptions.md#touchnearly)
- [useMapCenterWhenPinch](map.MapOptions.md#usemapcenterwhenpinch)
- [zoomCenter](map.MapOptions.md#zoomcenter)
- [enableDBClickZoom](map.MapOptions.md#enabledbclickzoom)

### Methods

- [setBMapControl](map.MapOptions.md#setbmapcontrol)
- [getBundleOption](map.MapOptions.md#getbundleoption)
- [updateGestureEnable](map.MapOptions.md#updategestureenable)
- [updateGestureConfig](map.MapOptions.md#updategestureconfig)
- [refresh](map.MapOptions.md#refresh)
- [toString](map.MapOptions.md#tostring)

## Constructors

### constructor

• **new MapOptions**(`opts?`): [`MapOptions`](map.MapOptions.md)

如果opts为空，则默认IMapOption参数如下：
```Typescript
{
mapStatus: new MapStatus(
{
center: new LatLng(39.914935, 116.403119),
zoom: 6.0
}
),
gestures: {
zoom: true,
move: true,
rotate: true,
overlooking: true,
touchNearly: 12
},
shows: {
satelliteMap: SysEnum.ESatelliteLayerType.NONE,
indoorMap: false,
trafficMap: false
}
}
```

#### Parameters

| Name | Type |
| :------ | :------ |
| `opts?` | [`Nullable`](../modules/map.md#nullable)\<[`IMapOption`](../interfaces/map.IMapOption.md)\> |

#### Returns

[`MapOptions`](map.MapOptions.md)

**`Since`**

1.0.0

## Accessors

### mapStatus

• `get` **mapStatus**(): [`MapStatus`](map.MapStatus.md)

获取MapStatus实例对象

#### Returns

[`MapStatus`](map.MapStatus.md)

**`Default`**

```ts
默认中心点（39.914935, 116.403119）缩放等级为6级
```

**`Since`**

1.0.0

• `set` **mapStatus**(`mapStatus`): `void`

设置MapStatus实例对象

#### Parameters

| Name | Type |
| :------ | :------ |
| `mapStatus` | [`MapStatus`](map.MapStatus.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### rotateGesturesEnabled

• `get` **rotateGesturesEnabled**(): `boolean`

设置是否允许通过手势旋转地图

#### Returns

`boolean`

**`Since`**

1.0.0

• `set` **rotateGesturesEnabled**(`rotateEnabled`): `void`

获取是否允许通过手势旋转地图

#### Parameters

| Name | Type |
| :------ | :------ |
| `rotateEnabled` | `boolean` |

#### Returns

`void`

**`Default`**

```ts
true
```

**`Since`**

1.0.0

___

### moveGesturesEnabled

• `get` **moveGesturesEnabled**(): `boolean`

设置是否允许通过手势移动地图

#### Returns

`boolean`

**`Since`**

1.0.0

• `set` **moveGesturesEnabled**(`moveEnabled`): `void`

获取是否允许通过手势移动地图

#### Parameters

| Name | Type |
| :------ | :------ |
| `moveEnabled` | `boolean` |

#### Returns

`void`

**`Default`**

```ts
true
```

**`Since`**

1.0.0

___

### overlookingGesturesEnabled

• `get` **overlookingGesturesEnabled**(): `boolean`

设置是否允许通过手势俯仰地图

#### Returns

`boolean`

**`Since`**

1.0.0

• `set` **overlookingGesturesEnabled**(`overlookingEnabled`): `void`

获取是否允许通过手势俯仰地图

#### Parameters

| Name | Type |
| :------ | :------ |
| `overlookingEnabled` | `boolean` |

#### Returns

`void`

**`Default`**

```ts
true
```

**`Since`**

1.0.0

___

### zoomGesturesEnabled

• `get` **zoomGesturesEnabled**(): `boolean`

设置是否允许通过手势缩放地图

#### Returns

`boolean`

**`Since`**

1.0.0

• `set` **zoomGesturesEnabled**(`zoomGesturesEnabled`): `void`

获取是否允许通过手势缩放地图

#### Parameters

| Name | Type |
| :------ | :------ |
| `zoomGesturesEnabled` | `boolean` |

#### Returns

`void`

**`Default`**

```ts
true
```

**`Since`**

1.0.0

___

### showSatelliteMap

• `get` **showSatelliteMap**(): [`ESatelliteLayerType`](../enums/map.SysEnum.ESatelliteLayerType.md)

获取是否显示卫星图以及是否加载路网状态

#### Returns

[`ESatelliteLayerType`](../enums/map.SysEnum.ESatelliteLayerType.md)

**`Default`**

```ts
SysEnum.ESatelliteLayerType.NONE
```

**`Since`**

1.0.0

• `set` **showSatelliteMap**(`type`): `void`

设置是否显示卫星图以及是否加载路网状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`ESatelliteLayerType`](../enums/map.SysEnum.ESatelliteLayerType.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### showBaseIndoorMap

• `get` **showBaseIndoorMap**(): `boolean`

获取是否显示室内图状态

#### Returns

`boolean`

**`Default`**

```ts
false
```

**`Since`**

1.0.0

• `set` **showBaseIndoorMap**(`show`): `void`

设置是否显示室内图状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `show` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

___

### showTrafficMap

• `get` **showTrafficMap**(): `boolean`

获取显示交通拥堵路线图状态

#### Returns

`boolean`

**`Default`**

```ts
false
```

**`Since`**

1.0.0

• `set` **showTrafficMap**(`show`): `void`

设置是否显示交通拥堵路线图

#### Parameters

| Name | Type |
| :------ | :------ |
| `show` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

___

### showMapPoi

• `get` **showMapPoi**(): `boolean`

#### Returns

`boolean`

• `set` **showMapPoi**(`isShow`): `void`

控制是否显示底图默认标注, 默认显示

#### Parameters

| Name | Type |
| :------ | :------ |
| `isShow` | `boolean` |

#### Returns

`void`

**`Since`**

1.2.0

___

### showMapIndoorPoi

• `get` **showMapIndoorPoi**(): `boolean`

#### Returns

`boolean`

• `set` **showMapIndoorPoi**(`isShow`): `void`

设置是否显示室内图标注, 默认显示

#### Parameters

| Name | Type |
| :------ | :------ |
| `isShow` | `boolean` |

#### Returns

`void`

**`Since`**

1.2.0

___

### touchNearly

• `get` **touchNearly**(): `number`

获取点击坐标缓冲范围

#### Returns

`number`

**`Since`**

1.0.0

• `set` **touchNearly**(`dis`): `void`

设置点击坐标缓冲范围

#### Parameters

| Name | Type |
| :------ | :------ |
| `dis` | `number` |

#### Returns

`void`

**`Since`**

1.0.0

___

### useMapCenterWhenPinch

• `get` **useMapCenterWhenPinch**(): `boolean`

获取手势是否采用指定缩放中心点

#### Returns

`boolean`

**`Since`**

1.0.0

• `set` **useMapCenterWhenPinch**(`use`): `void`

设置手势是否采用指定缩放中心点

#### Parameters

| Name | Type |
| :------ | :------ |
| `use` | `boolean` |

#### Returns

`void`

**`Since`**

1.0.0

___

### zoomCenter

• `get` **zoomCenter**(): [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

获取指定缩放中心点

#### Returns

[`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\>

**`Since`**

1.0.0

• `set` **zoomCenter**(`center`): `void`

设置缩放中心点

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `center` | [`Nullable`](../modules/map.md#nullable)\<[`LatLng`](base.LatLng.md)\> | 缩放中心点地理坐标 |

#### Returns

`void`

**`Since`**

1.0.0

___

### enableDBClickZoom

• `get` **enableDBClickZoom**(): `boolean`

获取双击放大地图是否开启

#### Returns

`boolean`

**`Since`**

1.2.7

• `set` **enableDBClickZoom**(`enable`): `void`

设置双击放大地图是否开启

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `enable` | `boolean` | 是否开启 |

#### Returns

`void`

**`Since`**

1.2.7

## Methods

### setBMapControl

▸ **setBMapControl**(`ctr`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `ctr` | `default` |

#### Returns

`void`

___

### getBundleOption

▸ **getBundleOption**(): [`BundleOptions`](../interfaces/map.BundleOptions.md)

#### Returns

[`BundleOptions`](../interfaces/map.BundleOptions.md)

___

### updateGestureEnable

▸ **updateGestureEnable**(): `void`

#### Returns

`void`

___

### updateGestureConfig

▸ **updateGestureConfig**(): `void`

#### Returns

`void`

___

### refresh

▸ **refresh**(`updateMapStatus?`): `void`

#### Parameters

| Name | Type | Default value |
| :------ | :------ | :------ |
| `updateMapStatus` | `boolean` | `false` |

#### Returns

`void`

___

### toString

▸ **toString**(): `string`

#### Returns

`string`
