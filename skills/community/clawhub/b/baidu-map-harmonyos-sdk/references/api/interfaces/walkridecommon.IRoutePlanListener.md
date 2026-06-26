[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / IRoutePlanListener

# Interface: IRoutePlanListener

[walkridecommon](../modules/walkridecommon.md).IRoutePlanListener

路线规划结果监听

**`Since`**

1.0.0

## Table of contents

### Methods

- [onRoutePlanStart](walkridecommon.IRoutePlanListener.md#onrouteplanstart)
- [onRoutePlanSuccess](walkridecommon.IRoutePlanListener.md#onrouteplansuccess)
- [onRoutePlanFail](walkridecommon.IRoutePlanListener.md#onrouteplanfail)

## Methods

### onRoutePlanStart

▸ **onRoutePlanStart**(): `void`

引擎开始路线规划

#### Returns

`void`

**`Since`**

1.0.0

___

### onRoutePlanSuccess

▸ **onRoutePlanSuccess**(`walkPlanModel`): `void`

正常规划成功

#### Parameters

| Name | Type |
| :------ | :------ |
| `walkPlanModel` | [`RoutePlanModel`](../classes/walkridecommon.RoutePlanModel.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### onRoutePlanFail

▸ **onRoutePlanFail**(`error`): `void`

正常规划失败

#### Parameters

| Name | Type |
| :------ | :------ |
| `error` | [`RoutePlanError`](../enums/walkridecommon.RoutePlanError.md) |

#### Returns

`void`

**`Since`**

1.0.0
