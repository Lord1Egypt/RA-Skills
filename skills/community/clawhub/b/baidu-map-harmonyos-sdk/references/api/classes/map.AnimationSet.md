[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / AnimationSet

# Class: AnimationSet

[map](../modules/map.md).AnimationSet

## Hierarchy

- [`Animation`](map.Animation.md)

  ↳ **`AnimationSet`**

## Table of contents

### Constructors

- [constructor](map.AnimationSet.md#constructor)

### Properties

- [bmAnimation](map.AnimationSet.md#bmanimation)
- [isDestroyed](map.AnimationSet.md#isdestroyed)

### Methods

- [setExtParam](map.AnimationSet.md#setextparam)
- [getExtParam](map.AnimationSet.md#getextparam)
- [start](map.AnimationSet.md#start)
- [reset](map.AnimationSet.md#reset)
- [pause](map.AnimationSet.md#pause)
- [resume](map.AnimationSet.md#resume)
- [cancel](map.AnimationSet.md#cancel)
- [setRepeatDelay](map.AnimationSet.md#setrepeatdelay)
- [setFillMode](map.AnimationSet.md#setfillmode)
- [setAnimationListener](map.AnimationSet.md#setanimationlistener)
- [setInterpolator](map.AnimationSet.md#setinterpolator)
- [setStartTime](map.AnimationSet.md#setstarttime)
- [getRepeatMode](map.AnimationSet.md#getrepeatmode)
- [getRepeatCount](map.AnimationSet.md#getrepeatcount)
- [getDuration](map.AnimationSet.md#getduration)
- [addAnimation](map.AnimationSet.md#addanimation)
- [setStartDelay](map.AnimationSet.md#setstartdelay)
- [setRepeatMode](map.AnimationSet.md#setrepeatmode)
- [setRepeatCount](map.AnimationSet.md#setrepeatcount)
- [setDuration](map.AnimationSet.md#setduration)
- [setTag](map.AnimationSet.md#settag)
- [getTag](map.AnimationSet.md#gettag)
- [setName](map.AnimationSet.md#setname)
- [getName](map.AnimationSet.md#getname)
- [destroy](map.AnimationSet.md#destroy)

## Constructors

### constructor

• **new AnimationSet**(): [`AnimationSet`](map.AnimationSet.md)

#### Returns

[`AnimationSet`](map.AnimationSet.md)

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

### addAnimation

▸ **addAnimation**(`animation`, `order`): `void`

order: 0:组合播放动画,1:按顺序播放动画

#### Parameters

| Name | Type |
| :------ | :------ |
| `animation` | [`Animation`](map.Animation.md) |
| `order` | `number` |

#### Returns

`void`

___

### setStartDelay

▸ **setStartDelay**(): `boolean`

#### Returns

`boolean`

**`Deprecated`**

到对应动画中单独设置 *

#### Overrides

[Animation](map.Animation.md).[setStartDelay](map.Animation.md#setstartdelay)

___

### setRepeatMode

▸ **setRepeatMode**(): `boolean`

#### Returns

`boolean`

**`Deprecated`**

到对应动画中单独设置 *

#### Overrides

[Animation](map.Animation.md).[setRepeatMode](map.Animation.md#setrepeatmode)

___

### setRepeatCount

▸ **setRepeatCount**(): `boolean`

#### Returns

`boolean`

**`Deprecated`**

到对应动画中单独设置 *

#### Overrides

[Animation](map.Animation.md).[setRepeatCount](map.Animation.md#setrepeatcount)

___

### setDuration

▸ **setDuration**(): `boolean`

#### Returns

`boolean`

**`Deprecated`**

到对应动画中单独设置 *

#### Overrides

[Animation](map.Animation.md).[setDuration](map.Animation.md#setduration)

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
