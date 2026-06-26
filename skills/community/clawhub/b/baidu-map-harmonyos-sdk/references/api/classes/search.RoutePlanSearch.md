[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / RoutePlanSearch

# Class: RoutePlanSearch

[search](../modules/search.md).RoutePlanSearch

**`Version`**

1.0

**`Description`**

路线规划

**`Date`**

2024-6-01

## Table of contents

### Methods

- [newInstance](search.RoutePlanSearch.md#newinstance)
- [bikingSearch](search.RoutePlanSearch.md#bikingsearch)
- [masstransitSearch](search.RoutePlanSearch.md#masstransitsearch)
- [transitSearch](search.RoutePlanSearch.md#transitsearch)
- [walkingSearch](search.RoutePlanSearch.md#walkingsearch)
- [drivingSearch](search.RoutePlanSearch.md#drivingsearch)
- [destroy](search.RoutePlanSearch.md#destroy)

## Methods

### newInstance

▸ **newInstance**(): [`RoutePlanSearch`](search.RoutePlanSearch.md)

获取RoutePlan检索实例

#### Returns

[`RoutePlanSearch`](search.RoutePlanSearch.md)

RoutePlan检索实例

___

### bikingSearch

▸ **bikingSearch**(`option`): `Promise`\<[`BikingRouteResult`](../interfaces/search.BikingRouteResult.md)\>

发起骑行路线规划

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`BikingRoutePlanOption`](../interfaces/search.BikingRoutePlanOption.md) |

#### Returns

`Promise`\<[`BikingRouteResult`](../interfaces/search.BikingRouteResult.md)\>

___

### masstransitSearch

▸ **masstransitSearch**(`option`): `Promise`\<[`MassTransitRouteResult`](../interfaces/search.MassTransitRouteResult.md)\>

发起跨城公共路线检索

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`MassTransitRoutePlanOption`](../interfaces/search.MassTransitRoutePlanOption.md) |

#### Returns

`Promise`\<[`MassTransitRouteResult`](../interfaces/search.MassTransitRouteResult.md)\>

___

### transitSearch

▸ **transitSearch**(`option`): `Promise`\<[`TransitRouteResult`](../interfaces/search.TransitRouteResult.md)\>

发起换乘路线规划

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`TransitRoutePlanOption`](../interfaces/search.TransitRoutePlanOption.md) |

#### Returns

`Promise`\<[`TransitRouteResult`](../interfaces/search.TransitRouteResult.md)\>

___

### walkingSearch

▸ **walkingSearch**(`option`): `Promise`\<[`WalkingRouteResult`](../interfaces/search.WalkingRouteResult.md)\>

发起步行路线规划

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`WalkingRoutePlanOption`](../interfaces/search.WalkingRoutePlanOption.md) |

#### Returns

`Promise`\<[`WalkingRouteResult`](../interfaces/search.WalkingRouteResult.md)\>

___

### drivingSearch

▸ **drivingSearch**(`option`): `Promise`\<[`DrivingRouteResult`](../interfaces/search.DrivingRouteResult.md)\>

发起驾车路线规划

#### Parameters

| Name | Type |
| :------ | :------ |
| `option` | [`DrivingRoutePlanOption`](../interfaces/search.DrivingRoutePlanOption.md) |

#### Returns

`Promise`\<[`DrivingRouteResult`](../interfaces/search.DrivingRouteResult.md)\>

___

### destroy

▸ **destroy**(): `void`

销毁RoutePlanSearch实例
调用此方法后，实例将无法再使用，所有进行中的请求回调都会被阻止

#### Returns

`void`
