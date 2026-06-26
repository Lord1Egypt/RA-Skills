[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / HeatMapBuilder

# Class: HeatMapBuilder

[map](../modules/map.md).HeatMapBuilder

## Table of contents

### Constructors

- [constructor](map.HeatMapBuilder.md#constructor)

### Properties

- [data](map.HeatMapBuilder.md#data)
- [datas](map.HeatMapBuilder.md#datas)
- [radius](map.HeatMapBuilder.md#radius)
- [radiusMeter](map.HeatMapBuilder.md#radiusmeter)
- [isRadiusMeter](map.HeatMapBuilder.md#isradiusmeter)
- [maxShowLevel](map.HeatMapBuilder.md#maxshowlevel)
- [minShowLevel](map.HeatMapBuilder.md#minshowlevel)
- [maxHigh](map.HeatMapBuilder.md#maxhigh)
- [gradient](map.HeatMapBuilder.md#gradient)
- [opacity](map.HeatMapBuilder.md#opacity)
- [frameAnimation](map.HeatMapBuilder.md#frameanimation)
- [initAnimation](map.HeatMapBuilder.md#initanimation)
- [maxIntensity](map.HeatMapBuilder.md#maxintensity)
- [minIntensity](map.HeatMapBuilder.md#minintensity)
- [isSetMaxIntensity](map.HeatMapBuilder.md#issetmaxintensity)

### Methods

- [setData](map.HeatMapBuilder.md#setdata)
- [setDatas](map.HeatMapBuilder.md#setdatas)
- [radiusValue](map.HeatMapBuilder.md#radiusvalue)
- [radiusMeterValue](map.HeatMapBuilder.md#radiusmetervalue)
- [isRadiusMeterValue](map.HeatMapBuilder.md#isradiusmetervalue)
- [maxShowLevelValue](map.HeatMapBuilder.md#maxshowlevelvalue)
- [minShowLevelValue](map.HeatMapBuilder.md#minshowlevelvalue)
- [maxHighValue](map.HeatMapBuilder.md#maxhighvalue)
- [gradientValue](map.HeatMapBuilder.md#gradientvalue)
- [opacityValue](map.HeatMapBuilder.md#opacityvalue)
- [frameAnimationValue](map.HeatMapBuilder.md#frameanimationvalue)
- [initAnimationValue](map.HeatMapBuilder.md#initanimationvalue)
- [maxIntensityValue](map.HeatMapBuilder.md#maxintensityvalue)
- [minIntensityValue](map.HeatMapBuilder.md#minintensityvalue)
- [build](map.HeatMapBuilder.md#build)

## Constructors

### constructor

• **new HeatMapBuilder**(): [`HeatMapBuilder`](map.HeatMapBuilder.md)

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

## Properties

### data

• `Optional` **data**: [`WeightedLatLng`](base.WeightedLatLng.md)[]

___

### datas

• `Optional` **datas**: [`WeightedLatLng`](base.WeightedLatLng.md)[][]

___

### radius

• **radius**: `number` = `HeatMap.DEFAULT_RADIUS`

___

### radiusMeter

• **radiusMeter**: `number` = `HeatMap.DEFAULT_RADIUS`

___

### isRadiusMeter

• **isRadiusMeter**: `boolean` = `false`

___

### maxShowLevel

• **maxShowLevel**: `number` = `HeatMap.DEFAULT_MAX_LEVEL`

___

### minShowLevel

• **minShowLevel**: `number` = `HeatMap.DEFAULT_MIN_LEVEL`

___

### maxHigh

• **maxHigh**: `number` = `HeatMap.DEFAULT_MAX_HIGH`

___

### gradient

• **gradient**: [`Gradient`](map.Gradient.md) = `HeatMap.DEFAULT_GRADIENT`

___

### opacity

• **opacity**: `number` = `HeatMap.DEFAULT_OPACITY`

___

### frameAnimation

• **frameAnimation**: [`HeatMapAnimation`](map.HeatMapAnimation.md)

___

### initAnimation

• **initAnimation**: [`HeatMapAnimation`](map.HeatMapAnimation.md)

___

### maxIntensity

• **maxIntensity**: `number` = `1.0`

___

### minIntensity

• **minIntensity**: `number` = `0.0`

___

### isSetMaxIntensity

• **isSetMaxIntensity**: `boolean` = `false`

## Methods

### setData

▸ **setData**(`data`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置单帧热力图数据（带权重）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `data` | [`WeightedLatLng`](base.WeightedLatLng.md)[] | 权重点数组 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

this

___

### setDatas

▸ **setDatas**(`datas`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置多帧热力图数据（带权重）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `datas` | [`WeightedLatLng`](base.WeightedLatLng.md)[][] | 多帧权重点数组 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

this

___

### radiusValue

▸ **radiusValue**(`radius`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置热力图点半径

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `radius` | `number` | 点半径 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### radiusMeterValue

▸ **radiusMeterValue**(`radius`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置热力图点半径（米）

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `radius` | `number` | 点半径 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### isRadiusMeterValue

▸ **isRadiusMeterValue**(`isMeter`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置是否使用半径单位为米

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `isMeter` | `boolean` | 是否使用半径单位为米 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### maxShowLevelValue

▸ **maxShowLevelValue**(`level`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置最大显示级别

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `level` | `number` | 最大显示级别 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### minShowLevelValue

▸ **minShowLevelValue**(`level`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置最小显示级别

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `level` | `number` | 最小显示级别 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### maxHighValue

▸ **maxHighValue**(`high`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置最大高度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `high` | `number` | 最大高度 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### gradientValue

▸ **gradientValue**(`gradient`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置渐变色

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `gradient` | [`Gradient`](map.Gradient.md) | 渐变色 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### opacityValue

▸ **opacityValue**(`opacity`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置透明度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `opacity` | `number` | 透明度 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### frameAnimationValue

▸ **frameAnimationValue**(`animation`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置帧动画

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `animation` | [`HeatMapAnimation`](map.HeatMapAnimation.md) | 帧动画 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### initAnimationValue

▸ **initAnimationValue**(`animation`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置初始动画

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `animation` | [`HeatMapAnimation`](map.HeatMapAnimation.md) | 初始动画 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### maxIntensityValue

▸ **maxIntensityValue**(`intensity`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置最大强度 (maxIntensity为1时SDK内部自动计算每一层级的最大权值，非1时按照设置的maxIntensity最大权值绘制)

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `intensity` | `number` | 最大强度 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### minIntensityValue

▸ **minIntensityValue**(`intensity`): [`HeatMapBuilder`](map.HeatMapBuilder.md)

设置最小强度

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `intensity` | `number` | 最小强度 |

#### Returns

[`HeatMapBuilder`](map.HeatMapBuilder.md)

___

### build

▸ **build**(): [`HeatMap`](map.HeatMap.md)

构建热力图

#### Returns

[`HeatMap`](map.HeatMap.md)

热力图实例
