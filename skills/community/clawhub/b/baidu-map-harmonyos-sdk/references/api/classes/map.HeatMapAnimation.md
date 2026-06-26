[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / HeatMapAnimation

# Class: HeatMapAnimation

[map](../modules/map.md).HeatMapAnimation

## Table of contents

### Constructors

- [constructor](map.HeatMapAnimation.md#constructor)

### Methods

- [getDuration](map.HeatMapAnimation.md#getduration)
- [setDuration](map.HeatMapAnimation.md#setduration)
- [getAnimationType](map.HeatMapAnimation.md#getanimationtype)
- [setAnimationType](map.HeatMapAnimation.md#setanimationtype)
- [setAnimation](map.HeatMapAnimation.md#setanimation)
- [getIsAnimation](map.HeatMapAnimation.md#getisanimation)

## Constructors

### constructor

• **new HeatMapAnimation**(`isAnimation`, `duration`, `type`): [`HeatMapAnimation`](map.HeatMapAnimation.md)

动态热力图动画属性构造器

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `isAnimation` | `boolean` | 是否有动画 |
| `duration` | `number` | 动画时长 |
| `type` | [`AnimationType`](../enums/map.AnimationType.md) | 动画类型 |

#### Returns

[`HeatMapAnimation`](map.HeatMapAnimation.md)

## Methods

### getDuration

▸ **getDuration**(): `number`

获取动画时长

#### Returns

`number`

___

### setDuration

▸ **setDuration**(`duration`): `void`

设置动画时长

#### Parameters

| Name | Type |
| :------ | :------ |
| `duration` | `number` |

#### Returns

`void`

___

### getAnimationType

▸ **getAnimationType**(): `number`

获取动画类型（返回枚举的索引值）

#### Returns

`number`

___

### setAnimationType

▸ **setAnimationType**(`animationType`): `void`

设置动画类型

#### Parameters

| Name | Type |
| :------ | :------ |
| `animationType` | [`AnimationType`](../enums/map.AnimationType.md) |

#### Returns

`void`

___

### setAnimation

▸ **setAnimation**(`isAnimation`): `void`

设置是否开启动画

#### Parameters

| Name | Type |
| :------ | :------ |
| `isAnimation` | `boolean` |

#### Returns

`void`

___

### getIsAnimation

▸ **getIsAnimation**(): `boolean`

获取是否开启动画

#### Returns

`boolean`
