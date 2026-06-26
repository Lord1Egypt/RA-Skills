[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / IRouteNaviService

# Interface: IRouteNaviService

[walkridecommon](../modules/walkridecommon.md).IRouteNaviService

步骑行导航服务抽象接口

**`Since`**

1.0.0

## Implemented by

- [`BDNaviService`](../classes/walkridecommon.BDNaviService.md)

## Table of contents

### Methods

- [initializer](walkridecommon.IRouteNaviService.md#initializer)
- [routePlanService](walkridecommon.IRouteNaviService.md#routeplanservice)
- [navigationService](walkridecommon.IRouteNaviService.md#navigationservice)

## Methods

### initializer

▸ **initializer**(): `INavigationInitializer`

初始化

#### Returns

`INavigationInitializer`

**`Since`**

1.0.0

___

### routePlanService

▸ **routePlanService**(): [`IRoutePlanService`](walkridecommon.IRoutePlanService.md)

路线规划服务

#### Returns

[`IRoutePlanService`](walkridecommon.IRoutePlanService.md)

**`Since`**

1.0.0

___

### navigationService

▸ **navigationService**(): `INavigationService`

导航核心服务

#### Returns

`INavigationService`

**`Since`**

1.0.0
