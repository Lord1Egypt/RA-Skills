[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / LocalMapConstants

# Class: LocalMapConstants

[map](../modules/map.md).LocalMapConstants

离线地图资源包类型，和离线地图资源包下载状态的常量定义

## Table of contents

### Constructors

- [constructor](map.LocalMapConstants.md#constructor)

### Properties

- [RESOURCE\_TYPE\_CITY](map.LocalMapConstants.md#resource_type_city)
- [RESOURCE\_TYPE\_PROVINCE](map.LocalMapConstants.md#resource_type_province)
- [RESOURCE\_TYPE\_CHINA](map.LocalMapConstants.md#resource_type_china)
- [DOWNLOAD\_STATUS\_UNDEFINED](map.LocalMapConstants.md#download_status_undefined)
- [DOWNLOAD\_STATUS\_WAITING](map.LocalMapConstants.md#download_status_waiting)
- [DOWNLOAD\_STATUS\_DOWNLOADING](map.LocalMapConstants.md#download_status_downloading)
- [DOWNLOAD\_STATUS\_PAUSED](map.LocalMapConstants.md#download_status_paused)
- [DOWNLOAD\_STATUS\_NETWORK\_ERROR](map.LocalMapConstants.md#download_status_network_error)
- [DOWNLOAD\_STATUS\_WIFI\_ERROR](map.LocalMapConstants.md#download_status_wifi_error)
- [DOWNLOAD\_STATUS\_IO\_ERROR](map.LocalMapConstants.md#download_status_io_error)
- [DOWNLOAD\_STATUS\_MD5\_ERROR](map.LocalMapConstants.md#download_status_md5_error)
- [DOWNLOAD\_STATUS\_INSTALLING](map.LocalMapConstants.md#download_status_installing)
- [DOWNLOAD\_STATUS\_FINISHED](map.LocalMapConstants.md#download_status_finished)
- [DOWNLOAD\_STATUS\_EXPIRE](map.LocalMapConstants.md#download_status_expire)
- [MESSAGE\_FIRST\_LOCATE](map.LocalMapConstants.md#message_first_locate)
- [MESSAGE\_SECOND\_LOCATE](map.LocalMapConstants.md#message_second_locate)
- [MESSAGE\_VERSION\_UPDATE](map.LocalMapConstants.md#message_version_update)
- [MESSAGE\_TO\_IMPORT](map.LocalMapConstants.md#message_to_import)
- [MESSAGE\_IMPORT\_PROGRESS](map.LocalMapConstants.md#message_import_progress)
- [MESSAGE\_IMPORT\_FINISHED](map.LocalMapConstants.md#message_import_finished)
- [MESSAGE\_START\_DOWNLOAD](map.LocalMapConstants.md#message_start_download)
- [MESSAGE\_DOWNLOAD\_PROGRESS](map.LocalMapConstants.md#message_download_progress)
- [MESSAGE\_DOWNLOAD\_FINISHED](map.LocalMapConstants.md#message_download_finished)
- [MESSAGE\_DOWNLOAD\_STATUS\_CHANGED](map.LocalMapConstants.md#message_download_status_changed)
- [MESSAGE\_NETWORK\_ERROR](map.LocalMapConstants.md#message_network_error)
- [MESSAGE\_GET\_CFG\_SUCCESS](map.LocalMapConstants.md#message_get_cfg_success)
- [MESSAGE\_IO\_ERROR](map.LocalMapConstants.md#message_io_error)
- [NO\_NEED\_UPDATE](map.LocalMapConstants.md#no_need_update)
- [NEED\_UPDATE\_PACKAGE](map.LocalMapConstants.md#need_update_package)
- [EXPIRE\_SIXTY\_DAY\_PACKAGE](map.LocalMapConstants.md#expire_sixty_day_package)
- [EXPIRE\_NINETY\_DAY\_PACKAGE](map.LocalMapConstants.md#expire_ninety_day_package)
- [EXPIRE\_PACKAGE](map.LocalMapConstants.md#expire_package)
- [WILL\_DELETE](map.LocalMapConstants.md#will_delete)
- [ALREADY\_DELETE](map.LocalMapConstants.md#already_delete)
- [CHINA\_BASE\_AND\_HOT\_ID](map.LocalMapConstants.md#china_base_and_hot_id)
- [WORLD\_BASE\_AND\_HOT\_ID](map.LocalMapConstants.md#world_base_and_hot_id)
- [CHINA\_REGION\_ID](map.LocalMapConstants.md#china_region_id)
- [WORLD\_REGION\_ID](map.LocalMapConstants.md#world_region_id)

## Constructors

### constructor

• **new LocalMapConstants**(): [`LocalMapConstants`](map.LocalMapConstants.md)

#### Returns

[`LocalMapConstants`](map.LocalMapConstants.md)

## Properties

### RESOURCE\_TYPE\_CITY

▪ `Static` `Readonly` **RESOURCE\_TYPE\_CITY**: ``0``

离线地图资源包类型：城市

___

### RESOURCE\_TYPE\_PROVINCE

▪ `Static` `Readonly` **RESOURCE\_TYPE\_PROVINCE**: ``1``

离线地图资源包类型：省份

___

### RESOURCE\_TYPE\_CHINA

▪ `Static` `Readonly` **RESOURCE\_TYPE\_CHINA**: ``2``

离线地图资源包类型：全国

___

### DOWNLOAD\_STATUS\_UNDEFINED

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_UNDEFINED**: ``0``

离线地图资源包下载状态：未定义

___

### DOWNLOAD\_STATUS\_WAITING

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_WAITING**: ``2``

离线地图资源包下载状态：等待下载

___

### DOWNLOAD\_STATUS\_DOWNLOADING

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_DOWNLOADING**: ``1``

离线地图资源包下载状态：下载中

___

### DOWNLOAD\_STATUS\_PAUSED

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_PAUSED**: ``3``

离线地图资源包下载状态：已暂停

___

### DOWNLOAD\_STATUS\_NETWORK\_ERROR

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_NETWORK\_ERROR**: ``6``

离线地图资源包下载状态：网络异常中断

___

### DOWNLOAD\_STATUS\_WIFI\_ERROR

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_WIFI\_ERROR**: ``8``

离线地图资源包下载状态：WiFi连接异常中断

___

### DOWNLOAD\_STATUS\_IO\_ERROR

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_IO\_ERROR**: ``7``

离线地图资源包下载状态：文件读写异常中断

___

### DOWNLOAD\_STATUS\_MD5\_ERROR

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_MD5\_ERROR**: ``5``

离线地图资源包下载状态：文件MD5校验失败中断

___

### DOWNLOAD\_STATUS\_INSTALLING

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_INSTALLING**: ``10``

离线地图资源包下载状态：安装中

___

### DOWNLOAD\_STATUS\_FINISHED

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_FINISHED**: ``4``

离线地图资源包下载状态：下载完成

___

### DOWNLOAD\_STATUS\_EXPIRE

▪ `Static` `Readonly` **DOWNLOAD\_STATUS\_EXPIRE**: ``9``

离线地图资源包下载状态：过期

___

### MESSAGE\_FIRST\_LOCATE

▪ `Static` `Readonly` **MESSAGE\_FIRST\_LOCATE**: ``1``

离线地图消息：首次定位城市

___

### MESSAGE\_SECOND\_LOCATE

▪ `Static` `Readonly` **MESSAGE\_SECOND\_LOCATE**: ``2``

离线地图消息：二次定位城市

___

### MESSAGE\_VERSION\_UPDATE

▪ `Static` `Readonly` **MESSAGE\_VERSION\_UPDATE**: ``4``

离线地图消息：离线地图资源包有更新

___

### MESSAGE\_TO\_IMPORT

▪ `Static` `Readonly` **MESSAGE\_TO\_IMPORT**: ``101``

离线地图消息：检测到待导入的离线地图资源包

___

### MESSAGE\_IMPORT\_PROGRESS

▪ `Static` `Readonly` **MESSAGE\_IMPORT\_PROGRESS**: ``102``

离线地图消息：离线地图资源包导入进度

___

### MESSAGE\_IMPORT\_FINISHED

▪ `Static` `Readonly` **MESSAGE\_IMPORT\_FINISHED**: ``6``

离线地图消息：离线地图资源包导入成功

___

### MESSAGE\_START\_DOWNLOAD

▪ `Static` `Readonly` **MESSAGE\_START\_DOWNLOAD**: ``9``

离线地图消息：开始下载离线地图资源包

___

### MESSAGE\_DOWNLOAD\_PROGRESS

▪ `Static` `Readonly` **MESSAGE\_DOWNLOAD\_PROGRESS**: ``8``

离线地图消息：离线地图资源包下载进度更新
低八位：进度
右移八位： 城市id

___

### MESSAGE\_DOWNLOAD\_FINISHED

▪ `Static` `Readonly` **MESSAGE\_DOWNLOAD\_FINISHED**: ``12``

离线地图消息：离线地图资源包下载完成

___

### MESSAGE\_DOWNLOAD\_STATUS\_CHANGED

▪ `Static` `Readonly` **MESSAGE\_DOWNLOAD\_STATUS\_CHANGED**: ``0``

离线地图消息：离线地图资源包下载状态有变化（如：等待下载->下载中，下载中->暂停，暂停->下载中）

___

### MESSAGE\_NETWORK\_ERROR

▪ `Static` `Readonly` **MESSAGE\_NETWORK\_ERROR**: ``10``

离线地图消息：离线地图资源包下载因网络原因而中断

___

### MESSAGE\_GET\_CFG\_SUCCESS

▪ `Static` `Readonly` **MESSAGE\_GET\_CFG\_SUCCESS**: ``201``

离线地图消息：离线地图开机下载配置文件完成

___

### MESSAGE\_IO\_ERROR

▪ `Static` `Readonly` **MESSAGE\_IO\_ERROR**: ``-1``

离线地图消息：离线地图资源包下载因文件IO异常而中断

___

### NO\_NEED\_UPDATE

▪ `Static` `Readonly` **NO\_NEED\_UPDATE**: ``0``

离线地图更新状态：不需要更新

___

### NEED\_UPDATE\_PACKAGE

▪ `Static` `Readonly` **NEED\_UPDATE\_PACKAGE**: ``1``

离线地图更新状态：需要更新，小于60天未更新

___

### EXPIRE\_SIXTY\_DAY\_PACKAGE

▪ `Static` `Readonly` **EXPIRE\_SIXTY\_DAY\_PACKAGE**: ``2``

离线地图更新状态：需要更新，60-90天未更新

___

### EXPIRE\_NINETY\_DAY\_PACKAGE

▪ `Static` `Readonly` **EXPIRE\_NINETY\_DAY\_PACKAGE**: ``3``

离线地图更新状态：需要更新，超过90天未更新

___

### EXPIRE\_PACKAGE

▪ `Static` `Readonly` **EXPIRE\_PACKAGE**: ``4``

离线地图更新状态：已过期

___

### WILL\_DELETE

▪ `Static` `Readonly` **WILL\_DELETE**: ``5``

离线地图行政变更：即将删除失效离线包

___

### ALREADY\_DELETE

▪ `Static` `Readonly` **ALREADY\_DELETE**: ``6``

离线地图行政变更：已经删除失效离线包

___

### CHINA\_BASE\_AND\_HOT\_ID

▪ `Static` `Readonly` **CHINA\_BASE\_AND\_HOT\_ID**: ``-2``

国内基础包和热门城市ID

___

### WORLD\_BASE\_AND\_HOT\_ID

▪ `Static` `Readonly` **WORLD\_BASE\_AND\_HOT\_ID**: ``-3``

国际基础包和热门城市ID

___

### CHINA\_REGION\_ID

▪ `Static` `Readonly` **CHINA\_REGION\_ID**: ``-4``

国内按地区查找ID

___

### WORLD\_REGION\_ID

▪ `Static` `Readonly` **WORLD\_REGION\_ID**: ``-5``

国际按地区查找ID
