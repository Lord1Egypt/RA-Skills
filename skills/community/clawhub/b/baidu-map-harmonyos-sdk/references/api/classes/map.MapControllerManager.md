[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / MapControllerManager

# Class: MapControllerManager

[map](../modules/map.md).MapControllerManager

sdk MapController管理类

负责MapController的创建和销毁管理

## Table of contents

### Methods

- [getInstance](map.MapControllerManager.md#getinstance)
- [createMapController](map.MapControllerManager.md#createmapcontroller)
- [destroyMapController](map.MapControllerManager.md#destroymapcontroller)
- [getMainInstance](map.MapControllerManager.md#getmaininstance)
- [getInstanceCount](map.MapControllerManager.md#getinstancecount)
- [destroy](map.MapControllerManager.md#destroy)

## Methods

### getInstance

▸ **getInstance**(): [`MapControllerManager`](map.MapControllerManager.md)

#### Returns

[`MapControllerManager`](map.MapControllerManager.md)

___

### createMapController

▸ **createMapController**(`context`, `mapOptions`, `baselineMapOption`): [`MapController`](map.MapController.md)

获取MapController实例

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `context` | `Context` | 上下文 |
| `mapOptions` | [`MapOptions`](map.MapOptions.md) | SDK地图选项 |
| `baselineMapOption` | `default` | - |

#### Returns

[`MapController`](map.MapController.md)

SDK MapController实例

___

### destroyMapController

▸ **destroyMapController**(`mapController`): `void`

统一的销毁接口
自动判断传入的controller是主实例还是子实例，并执行相应的销毁逻辑

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `mapController` | [`MapController`](map.MapController.md) | 要销毁的MapController实例 |

#### Returns

`void`

___

### getMainInstance

▸ **getMainInstance**(): ``null`` \| [`MapController`](map.MapController.md)

获取主实例

#### Returns

``null`` \| [`MapController`](map.MapController.md)

主实例，如果不存在则返回null

___

### getInstanceCount

▸ **getInstanceCount**(): `number`

获取实例总数

#### Returns

`number`

实例总数（主实例 + 子实例）

___

### destroy

▸ **destroy**(): `void`

销毁Manager
SDK反初始化调用
只销毁持有的基线主地图实例，在执行销毁前需要保证所有地图组件已经销毁

#### Returns

`void`
