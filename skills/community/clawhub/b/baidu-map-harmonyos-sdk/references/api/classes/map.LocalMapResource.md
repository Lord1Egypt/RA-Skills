[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / LocalMapResource

# Class: LocalMapResource

[map](../modules/map.md).LocalMapResource

离线地图资源包

## Implements

- [`cityMapItemStatusModelInterface`](../interfaces/map.cityMapItemStatusModelInterface.md)

## Table of contents

### Constructors

- [constructor](map.LocalMapResource.md#constructor)

### Properties

- [id](map.LocalMapResource.md#id)
- [name](map.LocalMapResource.md#name)
- [extraName](map.LocalMapResource.md#extraname)
- [parentId](map.LocalMapResource.md#parentid)
- [cityCount](map.LocalMapResource.md#citycount)
- [pinyin](map.LocalMapResource.md#pinyin)
- [version](map.LocalMapResource.md#version)
- [formatVersion](map.LocalMapResource.md#formatversion)
- [center](map.LocalMapResource.md#center)
- [level](map.LocalMapResource.md#level)
- [mapsize](map.LocalMapResource.md#mapsize)
- [mappatchsize](map.LocalMapResource.md#mappatchsize)
- [searchsize](map.LocalMapResource.md#searchsize)
- [searchpatchsize](map.LocalMapResource.md#searchpatchsize)
- [mapoldsize](map.LocalMapResource.md#mapoldsize)
- [searcholdsize](map.LocalMapResource.md#searcholdsize)
- [downloadProgress](map.LocalMapResource.md#downloadprogress)
- [downloadStatus](map.LocalMapResource.md#downloadstatus)
- [dataType](map.LocalMapResource.md#datatype)
- [frc](map.LocalMapResource.md#frc)
- [type](map.LocalMapResource.md#type)
- [needUpdate](map.LocalMapResource.md#needupdate)
- [updateStatus](map.LocalMapResource.md#updatestatus)
- [children](map.LocalMapResource.md#children)

### Methods

- [toString](map.LocalMapResource.md#tostring)
- [toSearchCityString](map.LocalMapResource.md#tosearchcitystring)
- [toHotCityString](map.LocalMapResource.md#tohotcitystring)
- [toAllCityString](map.LocalMapResource.md#toallcitystring)
- [createFromObject](map.LocalMapResource.md#createfromobject)
- [updateDownloadStatus](map.LocalMapResource.md#updatedownloadstatus)

## Constructors

### constructor

• **new LocalMapResource**(): [`LocalMapResource`](map.LocalMapResource.md)

#### Returns

[`LocalMapResource`](map.LocalMapResource.md)

## Properties

### id

• **id**: `number` = `0`

城市ID

___

### name

• **name**: `string` = `''`

城市名称。

___

### extraName

• **extraName**: `string` = `''`

城市名称 别称

___

### parentId

• `Optional` **parentId**: `number` = `0`

省份城市ID

___

### cityCount

• `Optional` **cityCount**: `number` = `0`

省份城市中全部城市数量

___

### pinyin

• **pinyin**: `string` = `''`

城市名称的拼音。

___

### version

• **version**: `number` = `0`

数据版本号

#### Implementation of

[cityMapItemStatusModelInterface](../interfaces/map.cityMapItemStatusModelInterface.md).[version](../interfaces/map.cityMapItemStatusModelInterface.md#version)

___

### formatVersion

• **formatVersion**: `number` = `0`

格式版本号

___

### center

• **center**: `default`

城市中心点。

___

### level

• **level**: `number` = `0`

默认的缩放级别。

___

### mapsize

• **mapsize**: `number` = `0`

底图包新包原始文件大小。

___

### mappatchsize

• **mappatchsize**: `number` = `0`

底图包增量文件大小。

___

### searchsize

• **searchsize**: `number` = `0`

检索包新包原始文件大小。

___

### searchpatchsize

• **searchpatchsize**: `number` = `0`

检索包增量文件大小。

___

### mapoldsize

• **mapoldsize**: `number` = `0`

本地已下载地图包旧包大小。

___

### searcholdsize

• **searcholdsize**: `number` = `0`

本地已下载检索包旧包大小。

___

### downloadProgress

• **downloadProgress**: `number` = `0`

下载进度。

___

### downloadStatus

• **downloadStatus**: `number` = `0`

下载状态.

#### Implementation of

[cityMapItemStatusModelInterface](../interfaces/map.cityMapItemStatusModelInterface.md).[downloadStatus](../interfaces/map.cityMapItemStatusModelInterface.md#downloadstatus)

___

### dataType

• **dataType**: `number` = `0`

数据类型，0：国内纯离线包单个文件; 1：国际化数据包

___

### frc

• **frc**: `number` = `0`

区分国内外字段，0: 未知； 1: 国内；2: 国外

___

### type

• **type**: `number` = `0`

资源包类型cty，0: 国家；1：省份；城市：2

___

### needUpdate

• **needUpdate**: `boolean` = `false`

是否需要更新。

#### Implementation of

[cityMapItemStatusModelInterface](../interfaces/map.cityMapItemStatusModelInterface.md).[needUpdate](../interfaces/map.cityMapItemStatusModelInterface.md#needupdate)

___

### updateStatus

• **updateStatus**: `number` = `0`

离线包更新状态
0: 没有更新
1: 离线包非最新版本
2: 60-90 天未更新离线包
3: 90 天以上未离线包
4: 离线包已经失效

#### Implementation of

[cityMapItemStatusModelInterface](../interfaces/map.cityMapItemStatusModelInterface.md).[updateStatus](../interfaces/map.cityMapItemStatusModelInterface.md#updatestatus)

___

### children

• **children**: [`LocalMapResource`](map.LocalMapResource.md)[] = `[]`

省份的下辖城市。

## Methods

### toString

▸ **toString**(): `string`

#### Returns

`string`

___

### toSearchCityString

▸ **toSearchCityString**(): `string`

#### Returns

`string`

___

### toHotCityString

▸ **toHotCityString**(): `string`

#### Returns

`string`

___

### toAllCityString

▸ **toAllCityString**(): `string`

#### Returns

`string`

___

### createFromObject

▸ **createFromObject**(`obj`): [`LocalMapResource`](map.LocalMapResource.md)

将子线程透传对象转换成LocalMapResource 对象

#### Parameters

| Name | Type |
| :------ | :------ |
| `obj` | `Record`\<`string`, `ESObject`\> |

#### Returns

[`LocalMapResource`](map.LocalMapResource.md)

___

### updateDownloadStatus

▸ **updateDownloadStatus**(`resource`): `void`

#### Parameters

| Name | Type |
| :------ | :------ |
| `resource` | [`LocalMapResource`](map.LocalMapResource.md) |

#### Returns

`void`
