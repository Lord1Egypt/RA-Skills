[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / MockLocationPlugin

# Class: MockLocationPlugin

[walkridecommon](../modules/walkridecommon.md).MockLocationPlugin

## Implements

- [`ILocationPlugin`](../interfaces/walkridecommon.ILocationPlugin.md)

## Table of contents

### Constructors

- [constructor](walkridecommon.MockLocationPlugin.md#constructor)

### Methods

- [reloadTrack](walkridecommon.MockLocationPlugin.md#reloadtrack)
- [setTrack](walkridecommon.MockLocationPlugin.md#settrack)
- [destroy](walkridecommon.MockLocationPlugin.md#destroy)
- [init](walkridecommon.MockLocationPlugin.md#init)
- [unInit](walkridecommon.MockLocationPlugin.md#uninit)
- [startContinuousLocation](walkridecommon.MockLocationPlugin.md#startcontinuouslocation)
- [stopContinuousLocation](walkridecommon.MockLocationPlugin.md#stopcontinuouslocation)
- [getCurrentLocation](walkridecommon.MockLocationPlugin.md#getcurrentlocation)

## Constructors

### constructor

• **new MockLocationPlugin**(`trackDataStr`, `speed?`): [`MockLocationPlugin`](walkridecommon.MockLocationPlugin.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `trackDataStr` | `string` |
| `speed?` | `number` |

#### Returns

[`MockLocationPlugin`](walkridecommon.MockLocationPlugin.md)

## Methods

### reloadTrack

▸ **reloadTrack**(): `void`

重置轨迹索引到起点

#### Returns

`void`

___

### setTrack

▸ **setTrack**(`trackDataStr`, `speed?`): `void`

设置模拟轨迹

#### Parameters

| Name | Type |
| :------ | :------ |
| `trackDataStr` | `string` |
| `speed?` | `number` |

#### Returns

`void`

___

### destroy

▸ **destroy**(): `void`

销毁模拟轨迹插件

#### Returns

`void`

___

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
