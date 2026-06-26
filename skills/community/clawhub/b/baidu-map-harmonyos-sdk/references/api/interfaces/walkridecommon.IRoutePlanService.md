[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / IRoutePlanService

# Interface: IRoutePlanService

[walkridecommon](../modules/walkridecommon.md).IRoutePlanService

路线规划服务

**`Since`**

1.0.0

## Hierarchy

- `ILifecycleInternal`

  ↳ **`IRoutePlanService`**

## Table of contents

### Methods

- [interruptRoutePlan](walkridecommon.IRoutePlanService.md#interruptrouteplan)
- [routePlanWithRouteNode](walkridecommon.IRoutePlanService.md#routeplanwithroutenode)
- [displayRoutePlanResult](walkridecommon.IRoutePlanService.md#displayrouteplanresult)
- [naviCalcRoute](walkridecommon.IRoutePlanService.md#navicalcroute)
- [naviCalcRouteWithRouteBook](walkridecommon.IRoutePlanService.md#navicalcroutewithroutebook)
- [setRouteSelectCallback](walkridecommon.IRoutePlanService.md#setrouteselectcallback)
- [clearRouteSelectCallback](walkridecommon.IRoutePlanService.md#clearrouteselectcallback)
- [switchRoute](walkridecommon.IRoutePlanService.md#switchroute)
- [cancelRoutePlanDisplay](walkridecommon.IRoutePlanService.md#cancelrouteplandisplay)

## Methods

### interruptRoutePlan

▸ **interruptRoutePlan**(): `void`

中断路线规划

#### Returns

`void`

**`Since`**

1.0.0

___

### routePlanWithRouteNode

▸ **routePlanWithRouteNode**(`param`, `routePlanListener`): `void`

路线规划

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `param` | [`RoutePlanOption`](../classes/walkridecommon.RoutePlanOption.md) |  |
| `routePlanListener` | [`IRoutePlanListener`](walkridecommon.IRoutePlanListener.md) | 路线规划结果监听 |

#### Returns

`void`

**`Since`**

1.0.0

___

### displayRoutePlanResult

▸ **displayRoutePlanResult**(`multiRouteDisplayOption?`): `void`

展示多路线接口
展示数据基于该路线规划服务最近的一次路线检索结果

#### Parameters

| Name | Type |
| :------ | :------ |
| `multiRouteDisplayOption?` | [`MultiRouteDisplayOption`](../classes/walkridecommon.MultiRouteDisplayOption.md) |

#### Returns

`void`

**`Since`**

1.0.0

___

### naviCalcRoute

▸ **naviCalcRoute**(`routeIndex`): `Promise`\<`void`\>

导航算路

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `routeIndex` | `number` | 选择的路线 |

#### Returns

`Promise`\<`void`\>

**`Since`**

1.0.0

___

### naviCalcRouteWithRouteBook

▸ **naviCalcRouteWithRouteBook**(`routeData`, `routeParam?`): `Promise`\<`void`\>

路书导航算路

#### Parameters

| Name | Type |
| :------ | :------ |
| `routeData` | `ArrayBuffer` |
| `routeParam?` | [`RoutePlanOption`](../classes/walkridecommon.RoutePlanOption.md) |

#### Returns

`Promise`\<`void`\>

**`Since`**

1.0.0

___

### setRouteSelectCallback

▸ **setRouteSelectCallback**(`callback`): `void`

设置路线选择回调。
设置后会回调步骑行服务实例销毁前所有的路线选择

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `callback` | (`routeIndex`: `number`, `routeModel`: [`WalkPlanModel`](../classes/walkridecommon.WalkPlanModel.md)) => `void` | 路线选择回调函数，参数为选中的路线索引 |

#### Returns

`void`

___

### clearRouteSelectCallback

▸ **clearRouteSelectCallback**(): `void`

清除路线选择回调
移除已设置的路线选择回调函数

#### Returns

`void`

___

### switchRoute

▸ **switchRoute**(`routeIndex`): `Promise`\<`boolean`\>

切换路线

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `routeIndex` | `number` | 要切换到的路线索引 |

#### Returns

`Promise`\<`boolean`\>

___

### cancelRoutePlanDisplay

▸ **cancelRoutePlanDisplay**(): `void`

取消显示路线规划结果
清除已绘制的路线覆盖层
不会影响已配置的绘制参数

#### Returns

`void`
