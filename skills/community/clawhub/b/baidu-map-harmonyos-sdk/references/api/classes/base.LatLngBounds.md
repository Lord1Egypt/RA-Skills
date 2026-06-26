[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [base](../modules/base.md) / LatLngBounds

# Class: LatLngBounds

[base](../modules/base.md).LatLngBounds

## Table of contents

### Constructors

- [constructor](base.LatLngBounds.md#constructor)

### Properties

- [northeast](base.LatLngBounds.md#northeast)
- [southwest](base.LatLngBounds.md#southwest)

### Accessors

- [center](base.LatLngBounds.md#center)

### Methods

- [contain](base.LatLngBounds.md#contain)

## Constructors

### constructor

• **new LatLngBounds**(`southwest`, `northeast`): [`LatLngBounds`](base.LatLngBounds.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `southwest` | [`LatLng`](base.LatLng.md) |
| `northeast` | [`LatLng`](base.LatLng.md) |

#### Returns

[`LatLngBounds`](base.LatLngBounds.md)

## Properties

### northeast

• `Readonly` **northeast**: [`LatLng`](base.LatLng.md)

该地理范围东北坐标

___

### southwest

• `Readonly` **southwest**: [`LatLng`](base.LatLng.md)

该地理范围西南坐标

## Accessors

### center

• `get` **center**(): [`LatLng`](base.LatLng.md)

获取该地理范围的中心地理坐标

#### Returns

[`LatLng`](base.LatLng.md)

该地理范围的中心地理坐标

• `set` **center**(`center`): `void`

设置该地理范围的中心地理坐标

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `center` | [`LatLng`](base.LatLng.md) | 该地理范围的中心地理坐标 |

#### Returns

`void`

## Methods

### contain

▸ **contain**(`point`): `boolean`

判断该地理范围是否包含一个地理位置

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `point` | [`LatLng`](base.LatLng.md) | 被判断的地理位置 |

#### Returns

`boolean`

该地理范围是否包含一个地理位置
