[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / IGuideSubStatusListener

# Interface: IGuideSubStatusListener

[walkridecommon](../modules/walkridecommon.md).IGuideSubStatusListener

诱导状态改变

## Table of contents

### Properties

- [onRouteFarAway](walkridecommon.IGuideSubStatusListener.md#onroutefaraway)
- [onRoutePlanYawing](walkridecommon.IGuideSubStatusListener.md#onrouteplanyawing)
- [onReRouteComplete](walkridecommon.IGuideSubStatusListener.md#onreroutecomplete)
- [onArriveDestNear](walkridecommon.IGuideSubStatusListener.md#onarrivedestnear)
- [onArriveDest](walkridecommon.IGuideSubStatusListener.md#onarrivedest)
- [onIndoorEnd](walkridecommon.IGuideSubStatusListener.md#onindoorend)
- [onFinalEnd](walkridecommon.IGuideSubStatusListener.md#onfinalend)

## Properties

### onRouteFarAway

• **onRouteFarAway**: (`msg`: [`DefaultMsg`](map.DefaultMsg.md)) => `void`

已经开始偏航

#### Type declaration

▸ (`msg`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `msg` | [`DefaultMsg`](map.DefaultMsg.md) |

##### Returns

`void`

___

### onRoutePlanYawing

• **onRoutePlanYawing**: (`msg`: [`DefaultMsg`](map.DefaultMsg.md)) => `void`

偏航规划中

#### Type declaration

▸ (`msg`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `msg` | [`DefaultMsg`](map.DefaultMsg.md) |

##### Returns

`void`

___

### onReRouteComplete

• **onReRouteComplete**: (`msg`: [`DefaultMsg`](map.DefaultMsg.md)) => `void`

偏航规划结束

#### Type declaration

▸ (`msg`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `msg` | [`DefaultMsg`](map.DefaultMsg.md) |

##### Returns

`void`

___

### onArriveDestNear

• **onArriveDestNear**: (`msg`: [`DefaultMsg`](map.DefaultMsg.md)) => `void`

接近目的地

#### Type declaration

▸ (`msg`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `msg` | [`DefaultMsg`](map.DefaultMsg.md) |

##### Returns

`void`

___

### onArriveDest

• **onArriveDest**: (`msg`: [`DefaultMsg`](map.DefaultMsg.md)) => `void`

到达目的地

#### Type declaration

▸ (`msg`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `msg` | [`DefaultMsg`](map.DefaultMsg.md) |

##### Returns

`void`

___

### onIndoorEnd

• **onIndoorEnd**: (`msg`: [`DefaultMsg`](map.DefaultMsg.md)) => `void`

到达室内目的地

#### Type declaration

▸ (`msg`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `msg` | [`DefaultMsg`](map.DefaultMsg.md) |

##### Returns

`void`

___

### onFinalEnd

• **onFinalEnd**: (`msg`: [`DefaultMsg`](map.DefaultMsg.md)) => `void`

到达最终目的地

#### Type declaration

▸ (`msg`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `msg` | [`DefaultMsg`](map.DefaultMsg.md) |

##### Returns

`void`
