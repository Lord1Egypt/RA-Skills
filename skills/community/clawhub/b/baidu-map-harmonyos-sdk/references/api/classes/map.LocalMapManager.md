[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / LocalMapManager

# Class: LocalMapManager

[map](../modules/map.md).LocalMapManager

离线地图管理类

## Table of contents

### Methods

- [getInstance](map.LocalMapManager.md#getinstance)
- [init](map.LocalMapManager.md#init)
- [destroy](map.LocalMapManager.md#destroy)
- [registerListener](map.LocalMapManager.md#registerlistener)
- [removeListener](map.LocalMapManager.md#removelistener)
- [start](map.LocalMapManager.md#start)
- [resume](map.LocalMapManager.md#resume)
- [resumeAll](map.LocalMapManager.md#resumeall)
- [pause](map.LocalMapManager.md#pause)
- [pauseAll](map.LocalMapManager.md#pauseall)
- [delete](map.LocalMapManager.md#delete)
- [deleteAll](map.LocalMapManager.md#deleteall)
- [importMap](map.LocalMapManager.md#importmap)
- [update](map.LocalMapManager.md#update)
- [updateAll](map.LocalMapManager.md#updateall)
- [getHotCities](map.LocalMapManager.md#gethotcities)
- [getAllCities](map.LocalMapManager.md#getallcities)
- [getCitiesByName](map.LocalMapManager.md#getcitiesbyname)
- [getCityById](map.LocalMapManager.md#getcitybyid)
- [getUserResources](map.LocalMapManager.md#getuserresources)
- [autoDownloadRoadNetworkViaWifi](map.LocalMapManager.md#autodownloadroadnetworkviawifi)

## Methods

### getInstance

▸ **getInstance**(): [`LocalMapManager`](map.LocalMapManager.md)

获取Singleton。

#### Returns

[`LocalMapManager`](map.LocalMapManager.md)

singleton

___

### init

▸ **init**(`controller`): `boolean`

始化离线地图模块

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `controller` | `undefined` \| ``null`` \| [`MapController`](map.MapController.md) | 地图controller |

#### Returns

`boolean`

成功返回true，失败返回false

___

### destroy

▸ **destroy**(): `void`

释放离线地图模块

#### Returns

`void`

___

### registerListener

▸ **registerListener**(`listener`): `void`

注册监听器

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `listener` | [`LocalMapListener`](../interfaces/map.LocalMapListener.md) | 监听器 |

#### Returns

`void`

___

### removeListener

▸ **removeListener**(`listener`): `void`

移除监听器

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `listener` | [`LocalMapListener`](../interfaces/map.LocalMapListener.md) | 监听器 |

#### Returns

`void`

___

### start

▸ **start**(`cityId`): `boolean`

开始下载离线地图资源

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityId` | `number` | 城市ID |

#### Returns

`boolean`

成功返回true，失败返回false

___

### resume

▸ **resume**(`cityId`): `boolean`

重新开始下载指定城市

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityId` | `number` | 城市ID |

#### Returns

`boolean`

成功返回true，失败返回false

___

### resumeAll

▸ **resumeAll**(`type`): `boolean`

重新开始全部下载任务

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type` | `number` | 0：下载；1：更新；2：重启Wifi网络异常；3：重启网络异常 |

#### Returns

`boolean`

___

### pause

▸ **pause**(`cityId`): `boolean`

暂停指定城市的下载任务

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityId` | `number` | 城市ID |

#### Returns

`boolean`

成功返回true，失败返回false

___

### pauseAll

▸ **pauseAll**(`type`): `boolean`

暂停全部下载任务

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `type` | `number` | 0：批量暂停；1：WiFi网络异常批量暂停；2：卡异常批量暂停（离线路网type为2） |

#### Returns

`boolean`

___

### delete

▸ **delete**(`cityId`): `boolean`

删除指定城市下载任务

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityId` | `number` | 城市ID |

#### Returns

`boolean`

___

### deleteAll

▸ **deleteAll**(): `boolean`

删除全部下载任务

#### Returns

`boolean`

___

### importMap

▸ **importMap**(`deleteFailed`, `offImport`): `boolean`

导入离线地图

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `deleteFailed` | `boolean` | 是否删除导入失败的包 |
| `offImport` | `boolean` | 是否离线导入 |

#### Returns

`boolean`

成功返回YES，失败返回NO

___

### update

▸ **update**(`cityId`): `boolean`

更新指定城市的下载任务

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityId` | `number` | 城市ID |

#### Returns

`boolean`

成功返回YES，失败返回NO

___

### updateAll

▸ **updateAll**(): `boolean`

更新全部下载任务

#### Returns

`boolean`

成功返回YES，失败返回NO

___

### getHotCities

▸ **getHotCities**(): `Promise`\<``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]\>

获取热门城市列表

#### Returns

`Promise`\<``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]\>

热门城市列表

___

### getAllCities

▸ **getAllCities**(): `Promise`\<``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]\>

获取全部城市列表

#### Returns

`Promise`\<``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]\>

全部城市列表

___

### getCitiesByName

▸ **getCitiesByName**(`key`): ``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]

根据关键词查询城市

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `key` | ``null`` \| `string` | 关键词 |

#### Returns

``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]

城市信息

___

### getCityById

▸ **getCityById**(`cityId`): ``null`` \| [`LocalMapResource`](map.LocalMapResource.md)

根据城市ID提取用户下载的相关记录

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `cityId` | `number` | 城市ID |

#### Returns

``null`` \| [`LocalMapResource`](map.LocalMapResource.md)

离线地图信息

___

### getUserResources

▸ **getUserResources**(): `Promise`\<``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]\>

提取用户下载的所有记录(包含所有下载完成、未完成的记录)

#### Returns

`Promise`\<``null`` \| [`LocalMapResource`](map.LocalMapResource.md)[]\>

离线地图资源列表

___

### autoDownloadRoadNetworkViaWifi

▸ **autoDownloadRoadNetworkViaWifi**(`cityId`): `number`

wifi下自动下载离线路网信息，提升路况加载速度

#### Parameters

| Name | Type |
| :------ | :------ |
| `cityId` | `number` |

#### Returns

`number`
