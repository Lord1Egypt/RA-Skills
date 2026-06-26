[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [walkridecommon](../modules/walkridecommon.md) / BDNaviService

# Class: BDNaviService

[walkridecommon](../modules/walkridecommon.md).BDNaviService

百度导航服务 - 整合步行和骑行导航能力

**`Since`**

1.0.0

## Implements

- [`IRouteNaviService`](../interfaces/walkridecommon.IRouteNaviService.md)

## Table of contents

### Constructors

- [constructor](walkridecommon.BDNaviService.md#constructor)

### Methods

- [setNaviType](walkridecommon.BDNaviService.md#setnavitype)
- [getNaviType](walkridecommon.BDNaviService.md#getnavitype)
- [initializer](walkridecommon.BDNaviService.md#initializer)
- [routePlanService](walkridecommon.BDNaviService.md#routeplanservice)
- [navigationService](walkridecommon.BDNaviService.md#navigationservice)

## Constructors

### constructor

• **new BDNaviService**(`naviType?`): [`BDNaviService`](walkridecommon.BDNaviService.md)

构造函数

#### Parameters

| Name | Type | Default value | Description |
| :------ | :------ | :------ | :------ |
| `naviType` | [`NaviType`](../enums/walkridecommon.NaviType.md) | `NaviType.WALK` | 默认导航类型，不传默认为步行导航 |

#### Returns

[`BDNaviService`](walkridecommon.BDNaviService.md)

## Methods

### setNaviType

▸ **setNaviType**(`naviType`): [`BDNaviService`](walkridecommon.BDNaviService.md)

设置导航类型

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `naviType` | [`NaviType`](../enums/walkridecommon.NaviType.md) | 导航类型 |

#### Returns

[`BDNaviService`](walkridecommon.BDNaviService.md)

当前实例，支持链式调用

___

### getNaviType

▸ **getNaviType**(): [`NaviType`](../enums/walkridecommon.NaviType.md)

获取当前导航类型

#### Returns

[`NaviType`](../enums/walkridecommon.NaviType.md)

当前导航类型

___

### initializer

▸ **initializer**(): `INavigationInitializer`

获取初始化服务

#### Returns

`INavigationInitializer`

初始化服务实例

**`Since`**

1.0.0

#### Implementation of

[IRouteNaviService](../interfaces/walkridecommon.IRouteNaviService.md).[initializer](../interfaces/walkridecommon.IRouteNaviService.md#initializer)

___

### routePlanService

▸ **routePlanService**(): [`IRoutePlanService`](../interfaces/walkridecommon.IRoutePlanService.md)

获取路线规划服务

#### Returns

[`IRoutePlanService`](../interfaces/walkridecommon.IRoutePlanService.md)

路线规划服务实例

**`Since`**

1.0.0

#### Implementation of

[IRouteNaviService](../interfaces/walkridecommon.IRouteNaviService.md).[routePlanService](../interfaces/walkridecommon.IRouteNaviService.md#routeplanservice)

___

### navigationService

▸ **navigationService**(): `INavigationService`

获取导航核心服务

#### Returns

`INavigationService`

导航核心服务实例

**`Since`**

1.0.0

#### Implementation of

[IRouteNaviService](../interfaces/walkridecommon.IRouteNaviService.md).[navigationService](../interfaces/walkridecommon.IRouteNaviService.md#navigationservice)
