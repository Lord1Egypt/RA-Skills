[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / TrackAnimation

# Class: TrackAnimation

[map](../modules/map.md).TrackAnimation

## Hierarchy

- [`Animation`](map.Animation.md)

  ↳ **`TrackAnimation`**

## Table of contents

### Constructors

- [constructor](map.TrackAnimation.md#constructor)

### Properties

- [bmAnimation](map.TrackAnimation.md#bmanimation)
- [isDestroyed](map.TrackAnimation.md#isdestroyed)

### Methods

- [setExtParam](map.TrackAnimation.md#setextparam)
- [getExtParam](map.TrackAnimation.md#getextparam)
- [start](map.TrackAnimation.md#start)
- [reset](map.TrackAnimation.md#reset)
- [pause](map.TrackAnimation.md#pause)
- [resume](map.TrackAnimation.md#resume)
- [cancel](map.TrackAnimation.md#cancel)
- [setDuration](map.TrackAnimation.md#setduration)
- [setStartDelay](map.TrackAnimation.md#setstartdelay)
- [setRepeatDelay](map.TrackAnimation.md#setrepeatdelay)
- [setRepeatMode](map.TrackAnimation.md#setrepeatmode)
- [setRepeatCount](map.TrackAnimation.md#setrepeatcount)
- [setFillMode](map.TrackAnimation.md#setfillmode)
- [setAnimationListener](map.TrackAnimation.md#setanimationlistener)
- [setInterpolator](map.TrackAnimation.md#setinterpolator)
- [setStartTime](map.TrackAnimation.md#setstarttime)
- [getRepeatMode](map.TrackAnimation.md#getrepeatmode)
- [getRepeatCount](map.TrackAnimation.md#getrepeatcount)
- [getDuration](map.TrackAnimation.md#getduration)
- [setTrackPosRadio](map.TrackAnimation.md#settrackposradio)
- [setTrackPos](map.TrackAnimation.md#settrackpos)
- [setTrackLine](map.TrackAnimation.md#settrackline)
- [setTrackPath](map.TrackAnimation.md#settrackpath)
- [setTrackUpdateListener](map.TrackAnimation.md#settrackupdatelistener)
- [setSdkTrack](map.TrackAnimation.md#setsdktrack)
- [setTag](map.TrackAnimation.md#settag)
- [getTag](map.TrackAnimation.md#gettag)
- [setName](map.TrackAnimation.md#setname)
- [getName](map.TrackAnimation.md#getname)
- [destroy](map.TrackAnimation.md#destroy)

## Constructors

### constructor

• **new TrackAnimation**(`geoPath?`): [`TrackAnimation`](map.TrackAnimation.md)

#### Parameters

| Name | Type |
| :------ | :------ |
| `geoPath?` | [`LatLng`](base.LatLng.md)[] |

#### Returns

[`TrackAnimation`](map.TrackAnimation.md)

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

### setTrackPosRadio

▸ **setTrackPosRadio**(`fromRadio`, `toRadio?`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `fromRadio` | `number` |
| `toRadio?` | `number` |

#### Returns

`boolean`

___

### setTrackPos

▸ **setTrackPos**(`to`, `from?`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `to` | [`LatLng`](base.LatLng.md) \| [`Point`](base.Point.md) |
| `from?` | [`LatLng`](base.LatLng.md) \| [`Point`](base.Point.md) |

#### Returns

`boolean`

___

### setTrackLine

▸ **setTrackLine**(`trackLine`): `Promise`\<`boolean`\>

#### Parameters

| Name | Type |
| :------ | :------ |
| `trackLine` | ``null`` \| [`Overlay`](map.Overlay.md) |

#### Returns

`Promise`\<`boolean`\>

___

### setTrackPath

▸ **setTrackPath**(`geoPath`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `geoPath` | [`LatLng`](base.LatLng.md)[] |

#### Returns

`boolean`

___

### setTrackUpdateListener

▸ **setTrackUpdateListener**(`listener?`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `listener?` | [`TrackUpdateListener`](../interfaces/map.TrackUpdateListener.md) |

#### Returns

`void`

___

### setSdkTrack

▸ **setSdkTrack**(`track`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `track` | ``null`` \| `default` |

#### Returns

`boolean`

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
