[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / WalkRideSensorManager

# Class: WalkRideSensorManager

[walkridecommon](../modules/walkridecommon.md).WalkRideSensorManager

步骑行传感器管理类

## Table of contents

### Constructors

- [constructor](walkridecommon.WalkRideSensorManager.md#constructor)

### Methods

- [getInstance](walkridecommon.WalkRideSensorManager.md#getinstance)
- [registerListener](walkridecommon.WalkRideSensorManager.md#registerlistener)
- [unRegisterListener](walkridecommon.WalkRideSensorManager.md#unregisterlistener)
- [setIsSupportSensor](walkridecommon.WalkRideSensorManager.md#setissupportsensor)
- [startSensor](walkridecommon.WalkRideSensorManager.md#startsensor)
- [stopSensor](walkridecommon.WalkRideSensorManager.md#stopsensor)
- [toDegrees](walkridecommon.WalkRideSensorManager.md#todegrees)
- [toRadians](walkridecommon.WalkRideSensorManager.md#toradians)

## Constructors

### constructor

• **new WalkRideSensorManager**(): [`WalkRideSensorManager`](walkridecommon.WalkRideSensorManager.md)

#### Returns

[`WalkRideSensorManager`](walkridecommon.WalkRideSensorManager.md)

## Methods

### getInstance

▸ **getInstance**(): [`WalkRideSensorManager`](walkridecommon.WalkRideSensorManager.md)

#### Returns

[`WalkRideSensorManager`](walkridecommon.WalkRideSensorManager.md)

___

### registerListener

▸ **registerListener**(`listener`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener` | `IWalkRideSensorListener` |

#### Returns

`void`

___

### unRegisterListener

▸ **unRegisterListener**(`listener`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener` | `IWalkRideSensorListener` |

#### Returns

`void`

___

### setIsSupportSensor

▸ **setIsSupportSensor**(`isSupportSensor`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `isSupportSensor` | `boolean` |

#### Returns

`void`

___

### startSensor

▸ **startSensor**(): `void`

#### Returns

`void`

___

### stopSensor

▸ **stopSensor**(): `void`

#### Returns

`void`

___

### toDegrees

▸ **toDegrees**(`angle`): `number`

弧度值转为角度值

#### Parameters

| Name | Type |
| :------ | :------ |
| `angle` | `number` |

#### Returns

`number`

___

### toRadians

▸ **toRadians**(`degree`): `number`

角度值转为弧度值

#### Parameters

| Name | Type |
| :------ | :------ |
| `degree` | `number` |

#### Returns

`number`
