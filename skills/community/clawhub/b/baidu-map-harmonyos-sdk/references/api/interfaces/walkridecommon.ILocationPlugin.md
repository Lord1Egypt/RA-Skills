[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / ILocationPlugin

# Interface: ILocationPlugin

[walkridecommon](../modules/walkridecommon.md).ILocationPlugin

## Implemented by

- [`DefaultLocPlugin`](../classes/walkridecommon.DefaultLocPlugin.md)
- [`MockLocationPlugin`](../classes/walkridecommon.MockLocationPlugin.md)

## Table of contents

### Methods

- [init](walkridecommon.ILocationPlugin.md#init)
- [unInit](walkridecommon.ILocationPlugin.md#uninit)
- [startContinuousLocation](walkridecommon.ILocationPlugin.md#startcontinuouslocation)
- [stopContinuousLocation](walkridecommon.ILocationPlugin.md#stopcontinuouslocation)
- [getCurrentLocation](walkridecommon.ILocationPlugin.md#getcurrentlocation)

## Methods

### init

▸ **init**(`context`): `void`

初始化

#### Parameters

| Name | Type |
| :------ | :------ |
| `context` | `Context` |

#### Returns

`void`

___

### unInit

▸ **unInit**(): `void`

#### Returns

`void`

___

### startContinuousLocation

▸ **startContinuousLocation**(`callback`): `Promise`\<`boolean`\>

开始持续定位

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `callback` | (`location`: [`BMLocation`](../classes/walkridecommon.BMLocation.md)) => `void` | 位置变化回调 |

#### Returns

`Promise`\<`boolean`\>

是否成功开始定位的Promise

___

### stopContinuousLocation

▸ **stopContinuousLocation**(): `Promise`\<`boolean`\>

停止持续定位

#### Returns

`Promise`\<`boolean`\>

是否成功停止定位的Promise

___

### getCurrentLocation

▸ **getCurrentLocation**(): `Promise`\<[`BMLocation`](../classes/walkridecommon.BMLocation.md)\>

获取单次定位

#### Returns

`Promise`\<[`BMLocation`](../classes/walkridecommon.BMLocation.md)\>

定位结果Promise
