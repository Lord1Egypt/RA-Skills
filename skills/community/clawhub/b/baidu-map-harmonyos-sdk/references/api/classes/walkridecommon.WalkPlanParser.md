[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / WalkPlanParser

# Class: WalkPlanParser

[walkridecommon](../modules/walkridecommon.md).WalkPlanParser

步行方案解析工具类

**`Author`**

: zuozhixiang

**`Time`**

: 2024/11/28

**`Description`**

: 文件描述

## Table of contents

### Constructors

- [constructor](walkridecommon.WalkPlanParser.md#constructor)

### Methods

- [parse](walkridecommon.WalkPlanParser.md#parse)
- [isStepNeedSplit](walkridecommon.WalkPlanParser.md#isstepneedsplit)
- [getStarOrEndName](walkridecommon.WalkPlanParser.md#getstarorendname)
- [getStartOrEndPoint](walkridecommon.WalkPlanParser.md#getstartorendpoint)
- [updateStartEnd](walkridecommon.WalkPlanParser.md#updatestartend)

## Constructors

### constructor

• **new WalkPlanParser**(): [`WalkPlanParser`](walkridecommon.WalkPlanParser.md)

#### Returns

[`WalkPlanParser`](walkridecommon.WalkPlanParser.md)

## Methods

### parse

▸ **parse**(`walkPlan`): ``null`` \| [`WalkPlanModel`](walkridecommon.WalkPlanModel.md)

解析walkPlan pb数据

#### Parameters

| Name | Type |
| :------ | :------ |
| `walkPlan` | `WalkPlan` |

#### Returns

``null`` \| [`WalkPlanModel`](walkridecommon.WalkPlanModel.md)

___

### isStepNeedSplit

▸ **isStepNeedSplit**(`steps`, `mode`): `boolean`

判断某个Step是否需要拆分, 判断条件是遍历Step中每个Link的linkattr字段,
若linkAttr字段命中推行或者未验证路段, 则认为需要拆分

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `steps` | `ISteps` | Steps对象 |
| `mode` | `number` | 出行方式 |

#### Returns

`boolean`

boolean 是否需要拆分

___

### getStarOrEndName

▸ **getStarOrEndName**(`walkPlan`, `routeIndex`, `isEnd`): `string`

获取起点或终点目的地

#### Parameters

| Name | Type |
| :------ | :------ |
| `walkPlan` | `WalkPlan` |
| `routeIndex` | `number` |
| `isEnd` | `boolean` |

#### Returns

`string`

___

### getStartOrEndPoint

▸ **getStartOrEndPoint**(`walkPlan`, `routeIndex`, `isEnd`): `number`[]

获取起点或者终点坐标

#### Parameters

| Name | Type |
| :------ | :------ |
| `walkPlan` | `WalkPlan` |
| `routeIndex` | `number` |
| `isEnd` | `boolean` |

#### Returns

`number`[]

___

### updateStartEnd

▸ **updateStartEnd**(`walkPlan`, `walkPlanModel`): [`WalkPlanModel`](walkridecommon.WalkPlanModel.md)

使用 WalkPlan 中的起始和结束节点信息更新 WalkPlanModel。

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `walkPlan` | `WalkPlan` | 包含路线选项和详细信息的 WalkPlan 对象。 |
| `walkPlanModel` | [`WalkPlanModel`](walkridecommon.WalkPlanModel.md) | 需要更新的 WalkPlanModel 对象，包含起始和结束节点的数据。 |

#### Returns

[`WalkPlanModel`](walkridecommon.WalkPlanModel.md)

更新后的 WalkPlanModel 对象，包含新的起始和/或结束节点信息。
