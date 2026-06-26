[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / RouteGuideUtil

# Class: RouteGuideUtil

[walkridecommon](../modules/walkridecommon.md).RouteGuideUtil

路线诱导工具类

## Table of contents

### Constructors

- [constructor](walkridecommon.RouteGuideUtil.md#constructor)

### Methods

- [buildSimpleGuideData](walkridecommon.RouteGuideUtil.md#buildsimpleguidedata)
- [getTrafficTextByTurnType](walkridecommon.RouteGuideUtil.md#gettraffictextbyturntype)
- [getWhiteTurnIconDrawableIdByType](walkridecommon.RouteGuideUtil.md#getwhiteturnicondrawableidbytype)

## Constructors

### constructor

• **new RouteGuideUtil**(): [`RouteGuideUtil`](walkridecommon.RouteGuideUtil.md)

#### Returns

[`RouteGuideUtil`](walkridecommon.RouteGuideUtil.md)

## Methods

### buildSimpleGuideData

▸ **buildSimpleGuideData**(`record`, `updateType`, `distance`, `time`): `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\>

构建简易诱导图数据

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `record` | `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\> | - |
| `updateType` | `number` | SimpleGuideUpdateType |
| `distance` | `number` | 总距离 |
| `time` | `number` | 总时间 |

#### Returns

`Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\>

data

___

### getTrafficTextByTurnType

▸ **getTrafficTextByTurnType**(`kind`): `any`

根据步行设施类型，获取步行设施提示文案

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `kind` | `number` | RouteGuideKind 路线详情项转向类型 |

#### Returns

`any`

提示文案

___

### getWhiteTurnIconDrawableIdByType

▸ **getWhiteTurnIconDrawableIdByType**(`kind`, `isWalk`, `bikeMode`): `any`

获取白色诱导图标

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `kind` | `number` | RouteGuideKind 路线详情项转向类型 |
| `isWalk` | `boolean` | 是否为步行 |
| `bikeMode` | `number` | 骑行模式 0: 自行车，1：电动车 |

#### Returns

`any`
