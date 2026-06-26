[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / WeightedLatLng

# Class: WeightedLatLng

[base](../modules/base.md).WeightedLatLng

带权值的经纬度位置点

## Table of contents

### Constructors

- [constructor](base.WeightedLatLng.md#constructor)

### Properties

- [DEFAULT\_INTENSITY](base.WeightedLatLng.md#default_intensity)
- [intensity](base.WeightedLatLng.md#intensity)
- [mLatLng](base.WeightedLatLng.md#mlatlng)

### Methods

- [createWithDefaultIntensity](base.WeightedLatLng.md#createwithdefaultintensity)
- [getPoint](base.WeightedLatLng.md#getpoint)
- [getIntensity](base.WeightedLatLng.md#getintensity)

## Constructors

### constructor

• **new WeightedLatLng**(`latLng`, `intensity?`): [`WeightedLatLng`](base.WeightedLatLng.md)

构造函数

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) | `undefined` | 地理位置 |
| `intensity` | `number` | `WeightedLatLng.DEFAULT_INTENSITY` | 权值，大于零；两个权值等于一的位置点等同于一个全职等于二的点。 |

#### Returns

[`WeightedLatLng`](base.WeightedLatLng.md)

## Properties

### DEFAULT\_INTENSITY

▪ `Static` `Readonly` **DEFAULT\_INTENSITY**: `number` = `1`

位置点默认权值

___

### intensity

• `Readonly` **intensity**: `number`

强度权值

___

### mLatLng

• `Readonly` **mLatLng**: [`LatLng`](base.LatLng.md)

地理位置

## Methods

### createWithDefaultIntensity

▸ **createWithDefaultIntensity**(`latLng`): [`WeightedLatLng`](base.WeightedLatLng.md)

构造函数，使用默认权值

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `latLng` | [`LatLng`](base.LatLng.md) | 地理位置 |

#### Returns

[`WeightedLatLng`](base.WeightedLatLng.md)

___

### getPoint

▸ **getPoint**(): [`Point`](base.Point.md)

#### Returns

[`Point`](base.Point.md)

___

### getIntensity

▸ **getIntensity**(): `number`

#### Returns

`number`
