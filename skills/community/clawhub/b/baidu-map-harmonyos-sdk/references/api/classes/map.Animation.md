[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / Animation

# Class: Animation

[map](../modules/map.md).Animation

## Hierarchy

- [`BmObject`](map.BmObject.md)

  ↳ **`Animation`**

  ↳↳ [`RotateAnimation`](map.RotateAnimation.md)

  ↳↳ [`AlphaAnimation`](map.AlphaAnimation.md)

  ↳↳ [`AnimationSet`](map.AnimationSet.md)

  ↳↳ [`ScaleAnimation`](map.ScaleAnimation.md)

  ↳↳ [`SingleScaleAnimation`](map.SingleScaleAnimation.md)

  ↳↳ [`Transformation`](map.Transformation.md)

  ↳↳ [`TrackAnimation`](map.TrackAnimation.md)

## Table of contents

### Constructors

- [constructor](map.Animation.md#constructor)

### Properties

- [bmAnimation](map.Animation.md#bmanimation)
- [isDestroyed](map.Animation.md#isdestroyed)

### Methods

- [setExtParam](map.Animation.md#setextparam)
- [getExtParam](map.Animation.md#getextparam)
- [start](map.Animation.md#start)
- [reset](map.Animation.md#reset)
- [pause](map.Animation.md#pause)
- [resume](map.Animation.md#resume)
- [cancel](map.Animation.md#cancel)
- [setDuration](map.Animation.md#setduration)
- [setStartDelay](map.Animation.md#setstartdelay)
- [setRepeatDelay](map.Animation.md#setrepeatdelay)
- [setRepeatMode](map.Animation.md#setrepeatmode)
- [setRepeatCount](map.Animation.md#setrepeatcount)
- [setFillMode](map.Animation.md#setfillmode)
- [setAnimationListener](map.Animation.md#setanimationlistener)
- [setInterpolator](map.Animation.md#setinterpolator)
- [setStartTime](map.Animation.md#setstarttime)
- [getRepeatMode](map.Animation.md#getrepeatmode)
- [getRepeatCount](map.Animation.md#getrepeatcount)
- [getDuration](map.Animation.md#getduration)
- [setTag](map.Animation.md#settag)
- [getTag](map.Animation.md#gettag)
- [setName](map.Animation.md#setname)
- [getName](map.Animation.md#getname)
- [destroy](map.Animation.md#destroy)

## Constructors

### constructor

• **new Animation**(`type`, `bmAnimation`): [`Animation`](map.Animation.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `type` | `number` |
| `bmAnimation` | `default` |

#### Returns

[`Animation`](map.Animation.md)

#### Overrides

[BmObject](map.BmObject.md).[constructor](map.BmObject.md#constructor)

## Properties

### bmAnimation

• **bmAnimation**: `default`

___

### isDestroyed

• **isDestroyed**: `boolean` = `false`

是否已经被销毁

**`Since`**

1.1.0

#### Inherited from

[BmObject](map.BmObject.md).[isDestroyed](map.BmObject.md#isdestroyed)

## Methods

### setExtParam

▸ **setExtParam**(`extParam`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `extParam` | `string` |

#### Returns

`void`

___

### getExtParam

▸ **getExtParam**(): `string`

#### Returns

`string`

___

### start

▸ **start**(): `boolean`

#### Returns

`boolean`

___

### reset

▸ **reset**(): `boolean`

#### Returns

`boolean`

___

### pause

▸ **pause**(): `boolean`

#### Returns

`boolean`

___

### resume

▸ **resume**(): `boolean`

#### Returns

`boolean`

___

### cancel

▸ **cancel**(): `boolean`

#### Returns

`boolean`

___

### setDuration

▸ **setDuration**(`durationMillis`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `durationMillis` | `number` |

#### Returns

`boolean`

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

___

### setRepeatDelay

▸ **setRepeatDelay**(`delayMillis`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `delayMillis` | `number` |

#### Returns

`boolean`

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

___

### setRepeatCount

▸ **setRepeatCount**(`repeatCount`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `repeatCount` | `number` |

#### Returns

`boolean`

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

___

### setAnimationListener

▸ **setAnimationListener**(`listener`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener` | [`AnimationListener`](../interfaces/map.AnimationListener.md) |

#### Returns

`void`

___

### setInterpolator

▸ **setInterpolator**(`i`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `i` | `default` |

#### Returns

`boolean`

___

### setStartTime

▸ **setStartTime**(`startTimeMillis`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `startTimeMillis` | `number` |

#### Returns

`boolean`

___

### getRepeatMode

▸ **getRepeatMode**(): `number`

#### Returns

`number`

___

### getRepeatCount

▸ **getRepeatCount**(): `number`

#### Returns

`number`

___

### getDuration

▸ **getDuration**(): `number`

#### Returns

`number`

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

[BmObject](map.BmObject.md).[setTag](map.BmObject.md#settag)

___

### getTag

▸ **getTag**(): `string`

#### Returns

`string`

#### Inherited from

[BmObject](map.BmObject.md).[getTag](map.BmObject.md#gettag)

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

[BmObject](map.BmObject.md).[setName](map.BmObject.md#setname)

___

### getName

▸ **getName**(): `string`

获取名称

#### Returns

`string`

**`Since`**

1.1.0

#### Inherited from

[BmObject](map.BmObject.md).[getName](map.BmObject.md#getname)

___

### destroy

▸ **destroy**(): `void`

仅适用用户主动触发的销毁

#### Returns

`void`

**`Since`**

1.1.0

#### Inherited from

[BmObject](map.BmObject.md).[destroy](map.BmObject.md#destroy)
