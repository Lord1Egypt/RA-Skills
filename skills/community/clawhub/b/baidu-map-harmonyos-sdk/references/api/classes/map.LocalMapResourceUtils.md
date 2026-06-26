[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / LocalMapResourceUtils

# Class: LocalMapResourceUtils

[map](../modules/map.md).LocalMapResourceUtils

离线地图资源状态工具类

## Table of contents

### Constructors

- [constructor](map.LocalMapResourceUtils.md#constructor)

### Methods

- [getStatus](map.LocalMapResourceUtils.md#getstatus)
- [isWaiting](map.LocalMapResourceUtils.md#iswaiting)
- [isDownloading](map.LocalMapResourceUtils.md#isdownloading)
- [isStopedWithNetworkError](map.LocalMapResourceUtils.md#isstopedwithnetworkerror)
- [isStoped](map.LocalMapResourceUtils.md#isstoped)
- [isFinished](map.LocalMapResourceUtils.md#isfinished)
- [isExpired](map.LocalMapResourceUtils.md#isexpired)
- [isNotDownload](map.LocalMapResourceUtils.md#isnotdownload)
- [isNeedRedownload](map.LocalMapResourceUtils.md#isneedredownload)
- [isNeedUpdate](map.LocalMapResourceUtils.md#isneedupdate)
- [isNeedDelete](map.LocalMapResourceUtils.md#isneeddelete)
- [isCanResume](map.LocalMapResourceUtils.md#iscanresume)
- [isCanExpand](map.LocalMapResourceUtils.md#iscanexpand)
- [isPatchDownload](map.LocalMapResourceUtils.md#ispatchdownload)
- [setProvinceDownloadStatus](map.LocalMapResourceUtils.md#setprovincedownloadstatus)
- [needUpdate](map.LocalMapResourceUtils.md#needupdate)
- [hasUpdate](map.LocalMapResourceUtils.md#hasupdate)
- [formatDataSize](map.LocalMapResourceUtils.md#formatdatasize)
- [isBaseMapSource](map.LocalMapResourceUtils.md#isbasemapsource)
- [fromJsonStr](map.LocalMapResourceUtils.md#fromjsonstr)
- [fromJsonRecord](map.LocalMapResourceUtils.md#fromjsonrecord)

## Constructors

### constructor

• **new LocalMapResourceUtils**(): [`LocalMapResourceUtils`](map.LocalMapResourceUtils.md)

#### Returns

[`LocalMapResourceUtils`](map.LocalMapResourceUtils.md)

## Methods

### getStatus

▸ **getStatus**(`resource`): `number`

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | `number` \| [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`number`

___

### isWaiting

▸ **isWaiting**(`resource`): `boolean`

离线地图资源是否处于等待下载状态？

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | `cityMapItemStatusType` |

#### Returns

`boolean`

boolean

___

### isDownloading

▸ **isDownloading**(`resource`): `boolean`

离线地图资源是否处于下载中状态？安装中也是下载中

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | `cityMapItemStatusType` |

#### Returns

`boolean`

___

### isStopedWithNetworkError

▸ **isStopedWithNetworkError**(`resource`): `boolean`

离线地图资源下载任务是否由于网络错误处于停止状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | `cityMapItemStatusType` |

#### Returns

`boolean`

___

### isStoped

▸ **isStoped**(`resource`): `boolean`

离线地图资源下载任务是否处于停止状态（已暂停、网络异常、下载出错）？

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | `number` \| [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isFinished

▸ **isFinished**(`resource`): `boolean`

离线地图资源下载任务是否处于下载完成状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isExpired

▸ **isExpired**(`resource`): `boolean`

离线地图资源下载任务是否处于失效状态

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isNotDownload

▸ **isNotDownload**(`resource`): `boolean`

还未下载

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isNeedRedownload

▸ **isNeedRedownload**(`resource`): `boolean`

离线地图资源是否需要重新下载？

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isNeedUpdate

▸ **isNeedUpdate**(`resource`): `boolean`

离线地图资源下载任务是否需要更新版本？

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isNeedDelete

▸ **isNeedDelete**(`resource`): `boolean`

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isCanResume

▸ **isCanResume**(`resource`): `boolean`

离线地图资源下载任务是否可以重新启动？

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### isCanExpand

▸ **isCanExpand**(`resource`): `boolean`

城市列表页的Group，如果是省份条目则点击后展开显示下属城市，如果是全国和城市条目则点击后开始下载。

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`LocalMapResource`](map.LocalMapResource.md) |

#### Returns

`boolean`

___

### isPatchDownload

▸ **isPatchDownload**(`city`): `boolean`

是否增量下载，否则是全量

#### Parameters

| Name | Type |
| :------ | :------ |
| `city` | [`LocalMapResource`](map.LocalMapResource.md) |

#### Returns

`boolean`

___

### setProvinceDownloadStatus

▸ **setProvinceDownloadStatus**(`province`): `void`

省份的下载状态由该省份下所有城市的下载状态决定。

#### Parameters

| Name | Type |
| :------ | :------ |
| `province` | [`LocalMapResource`](map.LocalMapResource.md) |

#### Returns

`void`

___

### needUpdate

▸ **needUpdate**(`state`): `Promise`\<`boolean`\>

收到LocalMapConstants#MESSAGE_VERSION_UPDATE消息，判断离线地图是否需要更新

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `state` | `number` | com.baidu.platform.comapi.map.LocalMapListener#onGetLocalMapState(int type, int state) |

#### Returns

`Promise`\<`boolean`\>

___

### hasUpdate

▸ **hasUpdate**(`city`): `boolean`

判断指定城市离线地图数据是否有更新

#### Parameters

| Name | Type |
| :------ | :------ |
| `city` | [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md) |

#### Returns

`boolean`

___

### formatDataSize

▸ **formatDataSize**(`size`): `string`

格式化资源大小

#### Parameters

| Name | Type |
| :------ | :------ |
| `size` | `number` |

#### Returns

`string`

___

### isBaseMapSource

▸ **isBaseMapSource**(`city`): `boolean`

当前是否为全国基础包

#### Parameters

| Name | Type |
| :------ | :------ |
| `city` | [`LocalMapResource`](map.LocalMapResource.md) |

#### Returns

`boolean`

___

### fromJsonStr

▸ **fromJsonStr**(`raw`): ``null`` \| [`LocalMapResource`](map.LocalMapResource.md)

将JSON字符串转为离线地图资源包对象

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `raw` | ``null`` \| `string` | JSON字符串 |

#### Returns

``null`` \| [`LocalMapResource`](map.LocalMapResource.md)

___

### fromJsonRecord

▸ **fromJsonRecord**(`json`): [`LocalMapResource`](map.LocalMapResource.md)

将JSON对象转为离线地图资源包对象

#### Parameters

| Name | Type | Description |
| :------ | :------ | :------ |
| `json` | `Record`\<`string`, [`BMObject`](../modules/base.md#bmobject)\> | JSON对象 |

#### Returns

[`LocalMapResource`](map.LocalMapResource.md)

离线地图资源包对象
