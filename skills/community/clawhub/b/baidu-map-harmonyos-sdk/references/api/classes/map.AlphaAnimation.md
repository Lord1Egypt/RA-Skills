[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / AlphaAnimation

# Class: AlphaAnimation

[map](../modules/map.md).AlphaAnimation

## Hierarchy

- [`Animation`](map.Animation.md)

  ↳ **`AlphaAnimation`**

## Table of contents

### Constructors

- [constructor](map.AlphaAnimation.md#constructor)

### Properties

- [bmAnimation](map.AlphaAnimation.md#bmanimation)
- [isDestroyed](map.AlphaAnimation.md#isdestroyed)

### Methods

- [getAlpha](map.AlphaAnimation.md#getalpha)
- [setExtParam](map.AlphaAnimation.md#setextparam)
- [getExtParam](map.AlphaAnimation.md#getextparam)
- [start](map.AlphaAnimation.md#start)
- [reset](map.AlphaAnimation.md#reset)
- [pause](map.AlphaAnimation.md#pause)
- [resume](map.AlphaAnimation.md#resume)
- [cancel](map.AlphaAnimation.md#cancel)
- [setDuration](map.AlphaAnimation.md#setduration)
- [setStartDelay](map.AlphaAnimation.md#setstartdelay)
- [setRepeatDelay](map.AlphaAnimation.md#setrepeatdelay)
- [setRepeatMode](map.AlphaAnimation.md#setrepeatmode)
- [setRepeatCount](map.AlphaAnimation.md#setrepeatcount)
- [setFillMode](map.AlphaAnimation.md#setfillmode)
- [setAnimationListener](map.AlphaAnimation.md#setanimationlistener)
- [setInterpolator](map.AlphaAnimation.md#setinterpolator)
- [setStartTime](map.AlphaAnimation.md#setstarttime)
- [getRepeatMode](map.AlphaAnimation.md#getrepeatmode)
- [getRepeatCount](map.AlphaAnimation.md#getrepeatcount)
- [getDuration](map.AlphaAnimation.md#getduration)
- [setTag](map.AlphaAnimation.md#settag)
- [getTag](map.AlphaAnimation.md#gettag)
- [setName](map.AlphaAnimation.md#setname)
- [getName](map.AlphaAnimation.md#getname)
- [destroy](map.AlphaAnimation.md#destroy)

## Constructors

### constructor

• **new AlphaAnimation**(`alpha`): [`AlphaAnimation`](map.AlphaAnimation.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `alpha` | `number`[] |

#### Returns

[`AlphaAnimation`](map.AlphaAnimation.md)

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

### getAlpha

▸ **getAlpha**(): `number`[]

#### Returns

`number`[]

___

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
