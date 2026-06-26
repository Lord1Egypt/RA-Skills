[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / HeatMap

# Class: HeatMap

[map](../modules/map.md).HeatMap

## Table of contents

### Constructors

- [constructor](map.HeatMap.md#constructor)

### Properties

- [TILE\_DIM](map.HeatMap.md#tile_dim)
- [DEFAULT\_RADIUS](map.HeatMap.md#default_radius)
- [DEFAULT\_OPACITY](map.HeatMap.md#default_opacity)
- [DEFAULT\_GRADIENT](map.HeatMap.md#default_gradient)
- [MIN\_RADIUS](map.HeatMap.md#min_radius)
- [MAX\_RADIUS](map.HeatMap.md#max_radius)
- [DEFAULT\_MAX\_HIGH](map.HeatMap.md#default_max_high)
- [DEFAULT\_MIN\_LEVEL](map.HeatMap.md#default_min_level)
- [DEFAULT\_MAX\_LEVEL](map.HeatMap.md#default_max_level)
- [MAX\_ZOOM\_LEVEL](map.HeatMap.md#max_zoom_level)
- [DEFAULT\_MIN\_ZOOM](map.HeatMap.md#default_min_zoom)
- [DEFAULT\_MAX\_ZOOM](map.HeatMap.md#default_max_zoom)
- [SCREEN\_SIZE](map.HeatMap.md#screen_size)

### Methods

- [setWeightedData](map.HeatMap.md#setweighteddata)
- [setWeightedDatas](map.HeatMap.md#setweighteddatas)
- [updateMaxIntensity](map.HeatMap.md#updatemaxintensity)
- [updateMinIntensity](map.HeatMap.md#updateminintensity)
- [updateFrameAnimation](map.HeatMap.md#updateframeanimation)
- [updateRadius](map.HeatMap.md#updateradius)
- [updateGradient](map.HeatMap.md#updategradient)
- [updateOpacity](map.HeatMap.md#updateopacity)
- [updateMaxShowLevel](map.HeatMap.md#updatemaxshowlevel)
- [updateMinShowLevel](map.HeatMap.md#updateminshowlevel)
- [updateRadiusMeter](map.HeatMap.md#updateradiusmeter)
- [updateIsRadiusMeter](map.HeatMap.md#updateisradiusmeter)
- [updateMaxHigh](map.HeatMap.md#updatemaxhigh)
- [getMaxHigh](map.HeatMap.md#getmaxhigh)
- [isFrameAnimation](map.HeatMap.md#isframeanimation)
- [isInitAnimation](map.HeatMap.md#isinitanimation)
- [removeHeatMap](map.HeatMap.md#removeheatmap)
- [toBundle](map.HeatMap.md#tobundle)
- [updateData](map.HeatMap.md#updatedata)
- [updateWeightedData](map.HeatMap.md#updateweighteddata)
- [createBoundsFromxy](map.HeatMap.md#createboundsfromxy)
- [getData](map.HeatMap.md#getdata)

## Constructors

### constructor

• **new HeatMap**(`builder`): [`HeatMap`](map.HeatMap.md)

构造函数

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `builder` | `HeatMapOptions` | 构造参数对象 |

#### Returns

[`HeatMap`](map.HeatMap.md)

## Properties

### TILE\_DIM

▪ `Static` `Readonly` **TILE\_DIM**: ``256``

___

### DEFAULT\_RADIUS

▪ `Static` `Readonly` **DEFAULT\_RADIUS**: ``12``

___

### DEFAULT\_OPACITY

▪ `Static` `Readonly` **DEFAULT\_OPACITY**: ``0.6``

___

### DEFAULT\_GRADIENT

▪ `Static` `Readonly` **DEFAULT\_GRADIENT**: [`Gradient`](map.Gradient.md)

___

### MIN\_RADIUS

▪ `Static` `Readonly` **MIN\_RADIUS**: ``10``

___

### MAX\_RADIUS

▪ `Static` `Readonly` **MAX\_RADIUS**: ``50``

___

### DEFAULT\_MAX\_HIGH

▪ `Static` `Readonly` **DEFAULT\_MAX\_HIGH**: ``0``

___

### DEFAULT\_MIN\_LEVEL

▪ `Static` `Readonly` **DEFAULT\_MIN\_LEVEL**: ``4``

___

### DEFAULT\_MAX\_LEVEL

▪ `Static` `Readonly` **DEFAULT\_MAX\_LEVEL**: ``22``

___

### MAX\_ZOOM\_LEVEL

▪ `Static` `Readonly` **MAX\_ZOOM\_LEVEL**: ``23``

___

### DEFAULT\_MIN\_ZOOM

▪ `Static` `Readonly` **DEFAULT\_MIN\_ZOOM**: ``4``

___

### DEFAULT\_MAX\_ZOOM

▪ `Static` `Readonly` **DEFAULT\_MAX\_ZOOM**: ``11``

___

### SCREEN\_SIZE

▪ `Static` `Readonly` **SCREEN\_SIZE**: ``1280``

## Methods

### setWeightedData

▸ **setWeightedData**(`weightedData`): `void`

设置单帧热力图数据（带权重）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `weightedData` | [`WeightedLatLng`](base.WeightedLatLng.md)[] | 权重点数组，不能为空，不能包含 null |

#### Returns

`void`

void

**`Throws`**

Error 如果数据为空或包含 null

___

### setWeightedDatas

▸ **setWeightedDatas**(`weightedDatas`): `void`

设置多帧热力图数据（带权重）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `weightedDatas` | [`WeightedLatLng`](base.WeightedLatLng.md)[][] | 多帧权重点数组，不能为空，不能包含 null |

#### Returns

`void`

void

**`Throws`**

Error 如果数据为空或包含 null

___

### updateMaxIntensity

▸ **updateMaxIntensity**(`intensity`): `void`

更新最大权重

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `intensity` | `number` | 最大权重 |

#### Returns

`void`

void

___

### updateMinIntensity

▸ **updateMinIntensity**(`intensity`): `void`

更新最小权重

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `intensity` | `number` | 最小权重 |

#### Returns

`void`

void

___

### updateFrameAnimation

▸ **updateFrameAnimation**(`animation`): `void`

更新帧动画

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `animation` | [`HeatMapAnimation`](map.HeatMapAnimation.md) | 帧动画对象 |

#### Returns

`void`

void

___

### updateRadius

▸ **updateRadius**(`radius`): `void`

更新点半径

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `radius` | `number` | 点半径 |

#### Returns

`void`

void

___

### updateGradient

▸ **updateGradient**(`gradient`): `void`

更新渐变色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `gradient` | [`Gradient`](map.Gradient.md) | 渐变色对象 |

#### Returns

`void`

void

**`Throws`**

Error 如果 gradient 为空

___

### updateOpacity

▸ **updateOpacity**(`opacity`): `void`

更新透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `opacity` | `number` | 透明度 |

#### Returns

`void`

void

___

### updateMaxShowLevel

▸ **updateMaxShowLevel**(`maxLevel`): `void`

更新最大显示层级

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `maxLevel` | `number` | 最大层级 |

#### Returns

`void`

void

___

### updateMinShowLevel

▸ **updateMinShowLevel**(`minLevel`): `void`

更新最小显示层级

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `minLevel` | `number` | 最小层级 |

#### Returns

`void`

void

___

### updateRadiusMeter

▸ **updateRadiusMeter**(`radius`): `void`

更新点半径（米）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `radius` | `number` | 点半径（米） |

#### Returns

`void`

___

### updateIsRadiusMeter

▸ **updateIsRadiusMeter**(`isMeter`): `void`

是否设置米单位半径

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `isMeter` | `boolean` | 是否为米单位半径 |

#### Returns

`void`

___

### updateMaxHigh

▸ **updateMaxHigh**(`high`): `void`

更新热力图最大高度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `high` | `number` | 最大高度值 |

#### Returns

`void`

___

### getMaxHigh

▸ **getMaxHigh**(): `number`

获取最大高度

#### Returns

`number`

最大高度

___

### isFrameAnimation

▸ **isFrameAnimation**(): `boolean`

是否有帧动画

#### Returns

`boolean`

是否有帧动画

___

### isInitAnimation

▸ **isInitAnimation**(): `boolean`

是否有初始化动画

#### Returns

`boolean`

是否有初始化动画

___

### removeHeatMap

▸ **removeHeatMap**(): `void`

删除热力图

#### Returns

`void`

___

### toBundle

▸ **toBundle**(): `HeatMapBundle`

转为 Bundle（对象）

#### Returns

`HeatMapBundle`

对象

___

### updateData

▸ **updateData**(`data`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `data` | [`LatLng`](base.LatLng.md)[] |

#### Returns

`void`

___

### updateWeightedData

▸ **updateWeightedData**(`weightedData`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `weightedData` | [`WeightedLatLng`](base.WeightedLatLng.md)[] |

#### Returns

`void`

___

### createBoundsFromxy

▸ **createBoundsFromxy**(`minX`, `maxX`, `minY`, `maxY`): [`Bounds`](base.Bounds.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `minX` | `number` |
| `maxX` | `number` |
| `minY` | `number` |
| `maxY` | `number` |

#### Returns

[`Bounds`](base.Bounds.md)

___

### getData

▸ **getData**(): `string`

#### Returns

`string`
