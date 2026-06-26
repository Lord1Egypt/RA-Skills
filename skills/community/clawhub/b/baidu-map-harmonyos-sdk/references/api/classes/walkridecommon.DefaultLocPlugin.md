[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / DefaultLocPlugin

# Class: DefaultLocPlugin

[walkridecommon](../modules/walkridecommon.md).DefaultLocPlugin

## Implements

- [`ILocationPlugin`](../interfaces/walkridecommon.ILocationPlugin.md)

## Table of contents

### Constructors

- [constructor](walkridecommon.DefaultLocPlugin.md#constructor)

### Methods

- [init](walkridecommon.DefaultLocPlugin.md#init)
- [unInit](walkridecommon.DefaultLocPlugin.md#uninit)
- [startContinuousLocation](walkridecommon.DefaultLocPlugin.md#startcontinuouslocation)
- [stopContinuousLocation](walkridecommon.DefaultLocPlugin.md#stopcontinuouslocation)
- [getCurrentLocation](walkridecommon.DefaultLocPlugin.md#getcurrentlocation)

## Constructors

### constructor

• **new DefaultLocPlugin**(): [`DefaultLocPlugin`](walkridecommon.DefaultLocPlugin.md)

#### Returns

[`DefaultLocPlugin`](walkridecommon.DefaultLocPlugin.md)

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

#### Implementation of

[ILocationPlugin](../interfaces/walkridecommon.ILocationPlugin.md).[init](../interfaces/walkridecommon.ILocationPlugin.md#init)

___

### unInit

▸ **unInit**(): `void`

#### Returns

`void`

#### Implementation of

[ILocationPlugin](../interfaces/walkridecommon.ILocationPlugin.md).[unInit](../interfaces/walkridecommon.ILocationPlugin.md#uninit)

___

### startContinuousLocation

▸ **startContinuousLocation**(`callback`): `Promise`\<`boolean`\>

开始持续定位

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `callback` | (`location`: [`BMLocation`](walkridecommon.BMLocation.md)) => `void` | 位置变化回调 |

#### Returns

`Promise`\<`boolean`\>

是否成功开始定位的Promise

#### Implementation of

[ILocationPlugin](../interfaces/walkridecommon.ILocationPlugin.md).[startContinuousLocation](../interfaces/walkridecommon.ILocationPlugin.md#startcontinuouslocation)

___

### stopContinuousLocation

▸ **stopContinuousLocation**(): `Promise`\<`boolean`\>

停止持续定位

#### Returns

`Promise`\<`boolean`\>

是否成功停止定位的Promise

#### Implementation of

[ILocationPlugin](../interfaces/walkridecommon.ILocationPlugin.md).[stopContinuousLocation](../interfaces/walkridecommon.ILocationPlugin.md#stopcontinuouslocation)

___

### getCurrentLocation

▸ **getCurrentLocation**(): `Promise`\<[`BMLocation`](walkridecommon.BMLocation.md)\>

获取单次定位

#### Returns

`Promise`\<[`BMLocation`](walkridecommon.BMLocation.md)\>

定位结果Promise

#### Implementation of

[ILocationPlugin](../interfaces/walkridecommon.ILocationPlugin.md).[getCurrentLocation](../interfaces/walkridecommon.ILocationPlugin.md#getcurrentlocation)
