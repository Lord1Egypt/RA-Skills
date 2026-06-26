[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / AnimationListener

# Interface: AnimationListener

[map](../modules/map.md).AnimationListener

## Table of contents

### Properties

- [onAnimationStart](map.AnimationListener.md#onanimationstart)
- [onAnimationEnd](map.AnimationListener.md#onanimationend)
- [onAnimationRepeat](map.AnimationListener.md#onanimationrepeat)

## Properties

### onAnimationStart

• **onAnimationStart**: (`animation`: [`Animation`](../classes/map.Animation.md)) => `void`

<p>Notifies the start of the animation.</p>

#### Type declaration

▸ (`animation`): `void`

##### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `animation` | [`Animation`](../classes/map.Animation.md) | The started animation. |

##### Returns

`void`

___

### onAnimationEnd

• **onAnimationEnd**: (`animation`: [`Animation`](../classes/map.Animation.md)) => `void`

<p>Notifies the end of the animation. This callback is not invoked
for animations with repeat count set to INFINITE.</p>

#### Type declaration

▸ (`animation`): `void`

##### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `animation` | [`Animation`](../classes/map.Animation.md) | The animation which reached its end. |

##### Returns

`void`

___

### onAnimationRepeat

• **onAnimationRepeat**: (`animation`: [`Animation`](../classes/map.Animation.md)) => `void`

<p>Notifies the repetition of the animation.</p>

#### Type declaration

▸ (`animation`): `void`

##### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `animation` | [`Animation`](../classes/map.Animation.md) | The animation which was repeated. |

##### Returns

`void`
