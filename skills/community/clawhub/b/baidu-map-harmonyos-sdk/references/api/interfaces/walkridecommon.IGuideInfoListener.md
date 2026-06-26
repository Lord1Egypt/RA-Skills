[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / IGuideInfoListener

# Interface: IGuideInfoListener

[walkridecommon](../modules/walkridecommon.md).IGuideInfoListener

行进过程中，诱导消息的改变

## Table of contents

### Properties

- [onSimpleGuideInfoUpdate](walkridecommon.IGuideInfoListener.md#onsimpleguideinfoupdate)
- [onRemainInfoUpdate](walkridecommon.IGuideInfoListener.md#onremaininfoupdate)
- [onSpeedUpdate](walkridecommon.IGuideInfoListener.md#onspeedupdate)
- [onMatchRouteInfo](walkridecommon.IGuideInfoListener.md#onmatchrouteinfo)
- [onTrafficLightUpdate](walkridecommon.IGuideInfoListener.md#ontrafficlightupdate)
- [onOutNaviInfo](walkridecommon.IGuideInfoListener.md#onoutnaviinfo)

## Properties

### onSimpleGuideInfoUpdate

• **onSimpleGuideInfoUpdate**: (`naviSimpleMapInfo`: `BWNaviSimpleMapInfo`) => `void`

更新诱导消息，比如“直行”

#### Type declaration

▸ (`naviSimpleMapInfo`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `naviSimpleMapInfo` | `BWNaviSimpleMapInfo` |

##### Returns

`void`

___

### onRemainInfoUpdate

• **onRemainInfoUpdate**: (`record`: `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\>) => `void`

目的地剩余距离时间更新

#### Type declaration

▸ (`record`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `record` | `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\> |

##### Returns

`void`

___

### onSpeedUpdate

• **onSpeedUpdate**: (`travelData`: `BWNaviTravelData`) => `void`

瞬时速度、行进距离更新

#### Type declaration

▸ (`travelData`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `travelData` | `BWNaviTravelData` |

##### Returns

`void`

___

### onMatchRouteInfo

• **onMatchRouteInfo**: (`record`: `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\>) => `void`

定位匹配路线信息

#### Type declaration

▸ (`record`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `record` | `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\> |

##### Returns

`void`

___

### onTrafficLightUpdate

• **onTrafficLightUpdate**: (`json`: `string`) => `void`

红绿灯发生改变

#### Type declaration

▸ (`json`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `json` | `string` |

##### Returns

`void`

___

### onOutNaviInfo

• **onOutNaviInfo**: (`record`: `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\>) => `void`

对外吐路线的图层信息
例如vivo手表的图层的信息

#### Type declaration

▸ (`record`): `void`

##### Parameters

| Name | Type |
| :------ | :------ |
| `record` | `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\> |

##### Returns

`void`
