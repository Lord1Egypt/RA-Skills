[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / HexagonMapBuilder

# Class: HexagonMapBuilder

[map](../modules/map.md).HexagonMapBuilder

## Table of contents

### Constructors

- [constructor](map.HexagonMapBuilder.md#constructor)

### Properties

- [data](map.HexagonMapBuilder.md#data)
- [radius](map.HexagonMapBuilder.md#radius)
- [gap](map.HexagonMapBuilder.md#gap)
- [hexagonType](map.HexagonMapBuilder.md#hexagontype)
- [gradient](map.HexagonMapBuilder.md#gradient)
- [opacity](map.HexagonMapBuilder.md#opacity)
- [maxIntensity](map.HexagonMapBuilder.md#maxintensity)
- [minIntensity](map.HexagonMapBuilder.md#minintensity)
- [maxShowLevel](map.HexagonMapBuilder.md#maxshowlevel)
- [minShowLevel](map.HexagonMapBuilder.md#minshowlevel)

### Methods

- [setData](map.HexagonMapBuilder.md#setdata)
- [weightedData](map.HexagonMapBuilder.md#weighteddata)
- [radiusValue](map.HexagonMapBuilder.md#radiusvalue)
- [gapValue](map.HexagonMapBuilder.md#gapvalue)
- [opacityValue](map.HexagonMapBuilder.md#opacityvalue)
- [maxIntensityValue](map.HexagonMapBuilder.md#maxintensityvalue)
- [minIntensityValue](map.HexagonMapBuilder.md#minintensityvalue)
- [setGradient](map.HexagonMapBuilder.md#setgradient)
- [setHexagonType](map.HexagonMapBuilder.md#sethexagontype)
- [minShowLevelValue](map.HexagonMapBuilder.md#minshowlevelvalue)
- [maxShowLevelValue](map.HexagonMapBuilder.md#maxshowlevelvalue)
- [build](map.HexagonMapBuilder.md#build)

## Constructors

### constructor

• **new HexagonMapBuilder**(): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

## Properties

### data

• **data**: [`WeightedLatLng`](base.WeightedLatLng.md)[] = `[]`

___

### radius

• **radius**: `number` = `200`

___

### gap

• **gap**: `number` = `5`

___

### hexagonType

• **hexagonType**: [`HexagonType`](../enums/map.HexagonType.md) = `HexagonType.VERTEX_UP`

___

### gradient

• **gradient**: [`Gradient`](map.Gradient.md)

___

### opacity

• **opacity**: `number` = `1`

___

### maxIntensity

• **maxIntensity**: `number` = `1.0`

___

### minIntensity

• **minIntensity**: `number` = `0.0`

___

### maxShowLevel

• **maxShowLevel**: `number` = `HexagonMap.DEFAULT_MAX_LEVEL`

___

### minShowLevel

• **minShowLevel**: `number` = `HexagonMap.DEFAULT_MIN_LEVEL`

## Methods

### setData

▸ **setData**(`data`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `data` | [`LatLng`](base.LatLng.md)[] |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### weightedData

▸ **weightedData**(`weightData`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `weightData` | [`WeightedLatLng`](base.WeightedLatLng.md)[] |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### radiusValue

▸ **radiusValue**(`radius`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `radius` | `number` |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### gapValue

▸ **gapValue**(`gap`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `gap` | `number` |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### opacityValue

▸ **opacityValue**(`opacity`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `opacity` | `number` |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### maxIntensityValue

▸ **maxIntensityValue**(`value`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `number` |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### minIntensityValue

▸ **minIntensityValue**(`value`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `value` | `number` |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### setGradient

▸ **setGradient**(`gradient`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `gradient` | [`Gradient`](map.Gradient.md) |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### setHexagonType

▸ **setHexagonType**(`type`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | [`HexagonType`](../enums/map.HexagonType.md) |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### minShowLevelValue

▸ **minShowLevelValue**(`level`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `level` | `number` |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### maxShowLevelValue

▸ **maxShowLevelValue**(`level`): [`HexagonMapBuilder`](map.HexagonMapBuilder.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `level` | `number` |

#### Returns

[`HexagonMapBuilder`](map.HexagonMapBuilder.md)

___

### build

▸ **build**(): [`HexagonMap`](map.HexagonMap.md)

#### Returns

[`HexagonMap`](map.HexagonMap.md)
