[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / ScaleAnimation

# Class: ScaleAnimation

[map](../modules/map.md).ScaleAnimation

## Hierarchy

- [`Animation`](map.Animation.md)

  ↳ **`ScaleAnimation`**

## Table of contents

### Constructors

- [constructor](map.ScaleAnimation.md#constructor)

### Properties

- [bmAnimation](map.ScaleAnimation.md#bmanimation)
- [isDestroyed](map.ScaleAnimation.md#isdestroyed)

### Methods

- [setExtParam](map.ScaleAnimation.md#setextparam)
- [getExtParam](map.ScaleAnimation.md#getextparam)
- [start](map.ScaleAnimation.md#start)
- [reset](map.ScaleAnimation.md#reset)
- [pause](map.ScaleAnimation.md#pause)
- [resume](map.ScaleAnimation.md#resume)
- [cancel](map.ScaleAnimation.md#cancel)
- [setDuration](map.ScaleAnimation.md#setduration)
- [setStartDelay](map.ScaleAnimation.md#setstartdelay)
- [setRepeatDelay](map.ScaleAnimation.md#setrepeatdelay)
- [setRepeatMode](map.ScaleAnimation.md#setrepeatmode)
- [setRepeatCount](map.ScaleAnimation.md#setrepeatcount)
- [setFillMode](map.ScaleAnimation.md#setfillmode)
- [setAnimationListener](map.ScaleAnimation.md#setanimationlistener)
- [setInterpolator](map.ScaleAnimation.md#setinterpolator)
- [setStartTime](map.ScaleAnimation.md#setstarttime)
- [getRepeatMode](map.ScaleAnimation.md#getrepeatmode)
- [getRepeatCount](map.ScaleAnimation.md#getrepeatcount)
- [getDuration](map.ScaleAnimation.md#getduration)
- [getScale](map.ScaleAnimation.md#getscale)
- [setTag](map.ScaleAnimation.md#settag)
- [getTag](map.ScaleAnimation.md#gettag)
- [setName](map.ScaleAnimation.md#setname)
- [getName](map.ScaleAnimation.md#getname)
- [destroy](map.ScaleAnimation.md#destroy)

## Constructors

### constructor

• **new ScaleAnimation**(`scale`): [`ScaleAnimation`](map.ScaleAnimation.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `scale` | `number`[] |

#### Returns

[`ScaleAnimation`](map.ScaleAnimation.md)

#### Overrides

[Animation](map.Animation.md).[constructor](map.Animation.md#constructor)

## Properties

### bmAnimation

• **bmAnimation**: `default`

#### Inherited from

[Animation](map.Animation.md).[bmAnimation](map.Animation.md#bmanimation)

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

是否已经被销毁

**`Since`**

1.1.0

#### Inherited from

[Animation](map.Animation.md).[isDestroyed](map.Animation.md#isdestroyed)

## Methods

### setExtParam

▸ **setExtParam**(`extParam`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `extParam` | `string` |

#### Returns

`void`

#### Inherited from

[Animation](map.Animation.md).[setExtParam](map.Animation.md#setextparam)

___

### getExtParam

▸ **getExtParam**(): `string`

#### Returns

`string`

#### Inherited from

[Animation](map.Animation.md).[getExtParam](map.Animation.md#getextparam)

___

### start

▸ **start**(): `boolean`

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[start](map.Animation.md#start)

___

### reset

▸ **reset**(): `boolean`

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[reset](map.Animation.md#reset)

___

### pause

▸ **pause**(): `boolean`

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[pause](map.Animation.md#pause)

___

### resume

▸ **resume**(): `boolean`

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[resume](map.Animation.md#resume)

___

### cancel

▸ **cancel**(): `boolean`

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[cancel](map.Animation.md#cancel)

___

### setDuration

▸ **setDuration**(`durationMillis`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `durationMillis` | `number` |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setDuration](map.Animation.md#setduration)

___

### setStartDelay

▸ **setStartDelay**(`delayMillis`): `boolean`

When this animation should start relative to the start time. This is most
useful when composing complex animations using an BmAnimationSet
where some of the animations components start at different times.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `delayMillis` | `number` | When this Animation should start, in milliseconds from the start time of the root AnimationSet. |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setStartDelay](map.Animation.md#setstartdelay)

___

### setRepeatDelay

▸ **setRepeatDelay**(`delayMillis`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `delayMillis` | `number` |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setRepeatDelay](map.Animation.md#setrepeatdelay)

___

### setRepeatMode

▸ **setRepeatMode**(`repeatMode`): `boolean`

动画重复模式

#### Parameters

| Name | Type |
| :------ | :------ |
| `repeatMode` | [`MarkerRepeatMode`](../enums/map.SysEnum.MarkerRepeatMode.md) |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setRepeatMode](map.Animation.md#setrepeatmode)

___

### setRepeatCount

▸ **setRepeatCount**(`repeatCount`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `repeatCount` | `number` |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setRepeatCount](map.Animation.md#setrepeatcount)

___

### setFillMode

▸ **setFillMode**(`fillMode`): `boolean`

If fillEnabled is true, the animation will apply the value of fillBefore.
Otherwise, fillBefore is ignored and the animation
transformation is always applied until the animation ends.

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `fillMode` | `number` | #FILL_BEFORE or #FILL_AFTER |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setFillMode](map.Animation.md#setfillmode)

___

### setAnimationListener

▸ **setAnimationListener**(`listener`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener` | [`AnimationListener`](../interfaces/map.AnimationListener.md) |

#### Returns

`void`

#### Inherited from

[Animation](map.Animation.md).[setAnimationListener](map.Animation.md#setanimationlistener)

___

### setInterpolator

▸ **setInterpolator**(`i`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `i` | `default` |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setInterpolator](map.Animation.md#setinterpolator)

___

### setStartTime

▸ **setStartTime**(`startTimeMillis`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `startTimeMillis` | `number` |

#### Returns

`boolean`

#### Inherited from

[Animation](map.Animation.md).[setStartTime](map.Animation.md#setstarttime)

___

### getRepeatMode

▸ **getRepeatMode**(): `number`

#### Returns

`number`

#### Inherited from

[Animation](map.Animation.md).[getRepeatMode](map.Animation.md#getrepeatmode)

___

### getRepeatCount

▸ **getRepeatCount**(): `number`

#### Returns

`number`

#### Inherited from

[Animation](map.Animation.md).[getRepeatCount](map.Animation.md#getrepeatcount)

___

### getDuration

▸ **getDuration**(): `number`

#### Returns

`number`

#### Inherited from

[Animation](map.Animation.md).[getDuration](map.Animation.md#getduration)

___

### getScale

▸ **getScale**(): `number`[]

#### Returns

`number`[]

___

### setTag

▸ **setTag**(`tag`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `tag` | `string` |

#### Returns

`void`

#### Inherited from

[Animation](map.Animation.md).[setTag](map.Animation.md#settag)

___

### getTag

▸ **getTag**(): `string`

#### Returns

`string`

#### Inherited from

[Animation](map.Animation.md).[getTag](map.Animation.md#gettag)

___

### setName

▸ **setName**(`name`): `void`

设置名称

#### Parameters

| Name | Type |
| :------ | :------ |
| `name` | `string` |

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

[Animation](map.Animation.md).[setName](map.Animation.md#setname)

___

### getName

▸ **getName**(): `string`

获取名称

#### Returns

`string`

**`Since`**

1.1.0

#### Inherited from

[Animation](map.Animation.md).[getName](map.Animation.md#getname)

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

[Animation](map.Animation.md).[destroy](map.Animation.md#destroy)
