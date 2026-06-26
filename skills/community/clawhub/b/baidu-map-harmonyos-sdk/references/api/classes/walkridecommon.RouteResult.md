[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / RouteResult

# Class: RouteResult

[walkridecommon](../modules/walkridecommon.md).RouteResult

路线结果

**`Description`**

路线结果信息

## Table of contents

### Constructors

- [constructor](walkridecommon.RouteResult.md#constructor)

### Accessors

- [routeIndex](walkridecommon.RouteResult.md#routeindex)
- [distance](walkridecommon.RouteResult.md#distance)
- [duration](walkridecommon.RouteResult.md#duration)
- [positions](walkridecommon.RouteResult.md#positions)
- [lightCount](walkridecommon.RouteResult.md#lightcount)

### Methods

- [calculateTotalDistance](walkridecommon.RouteResult.md#calculatetotaldistance)
- [calculateEstimatedDuration](walkridecommon.RouteResult.md#calculateestimatedduration)

## Constructors

### constructor

• **new RouteResult**(): [`RouteResult`](walkridecommon.RouteResult.md)

#### Returns

[`RouteResult`](walkridecommon.RouteResult.md)

## Accessors

### routeIndex

• `get` **routeIndex**(): `number`

#### Returns

`number`

• `set` **routeIndex**(`index`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `index` | `number` |

#### Returns

`void`

___

### distance

• `get` **distance**(): `number`

#### Returns

`number`

• `set` **distance**(`distance`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `distance` | `number` |

#### Returns

`void`

___

### duration

• `get` **duration**(): `number`

#### Returns

`number`

• `set` **duration**(`duration`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `duration` | `number` |

#### Returns

`void`

___

### positions

• `get` **positions**(): [`LatLng`](base.LatLng.md)[]

#### Returns

[`LatLng`](base.LatLng.md)[]

• `set` **positions**(`positions`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `positions` | [`LatLng`](base.LatLng.md)[] |

#### Returns

`void`

___

### lightCount

• `get` **lightCount**(): `number`

#### Returns

`number`

• `set` **lightCount**(`count`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `count` | `number` |

#### Returns

`void`

## Methods

### calculateTotalDistance

▸ **calculateTotalDistance**(): `number`

计算总路程

#### Returns

`number`

___

### calculateEstimatedDuration

▸ **calculateEstimatedDuration**(): `number`

计算预计耗时

#### Returns

`number`
