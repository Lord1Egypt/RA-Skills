[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / TraceAnimationListener

# Interface: TraceAnimationListener

[map](../modules/map.md).TraceAnimationListener

轨迹动画监听器接口
用于监听轨迹动画的进度更新、位置更新及动画结束事件

## Table of contents

### Properties

- [onTraceAnimationUpdate](map.TraceAnimationListener.md#ontraceanimationupdate)
- [onTraceUpdatePosition](map.TraceAnimationListener.md#ontraceupdateposition)
- [onTraceAnimationFinish](map.TraceAnimationListener.md#ontraceanimationfinish)

## Properties

### onTraceAnimationUpdate

• **onTraceAnimationUpdate**: (`percent`: `number`) => `void`

轨迹动画更新进度回调

#### Type declaration

▸ (`percent`): `void`

##### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `percent` | `number` | 轨迹动画更新进度，取值范围 [0, 100]（0 表示开始，100 表示结束） |

##### Returns

`void`

___

### onTraceUpdatePosition

• **onTraceUpdatePosition**: (`position`: [`LatLng`](../classes/base.LatLng.md)) => `void`

轨迹动画当前位置更新回调

#### Type declaration

▸ (`position`): `void`

##### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `position` | [`LatLng`](../classes/base.LatLng.md) | 轨迹动画当前帧的位置坐标（经纬度信息） |

##### Returns

`void`

___

### onTraceAnimationFinish

• **onTraceAnimationFinish**: () => `void`

轨迹动画结束回调
当动画播放完成（包括正常结束、手动停止）时触发

#### Type declaration

▸ (): `void`

##### Returns

`void`
