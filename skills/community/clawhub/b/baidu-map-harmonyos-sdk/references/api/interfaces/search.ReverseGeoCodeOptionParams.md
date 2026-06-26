[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / ReverseGeoCodeOptionParams

# Interface: ReverseGeoCodeOptionParams

[search](../modules/search.md).ReverseGeoCodeOptionParams

反地理编码选项构造函数参数接口

## Table of contents

### Properties

- [pageSize](search.ReverseGeoCodeOptionParams.md#pagesize)
- [pageNum](search.ReverseGeoCodeOptionParams.md#pagenum)
- [location](search.ReverseGeoCodeOptionParams.md#location)
- [latestAdmin](search.ReverseGeoCodeOptionParams.md#latestadmin)
- [radius](search.ReverseGeoCodeOptionParams.md#radius)
- [poiType](search.ReverseGeoCodeOptionParams.md#poitype)
- [isExtensionsRoad](search.ReverseGeoCodeOptionParams.md#isextensionsroad)
- [languageType](search.ReverseGeoCodeOptionParams.md#languagetype)

## Properties

### pageSize

• `Optional` **pageSize**: `number`

单页展示POI数量，默认为10条记录，最大返回100条。

___

### pageNum

• `Optional` **pageNum**: `number`

分页页码
默认为0,0代表第一页，1代表第二页，以此类推

___

### location

• **location**: [`LatLng`](../classes/base.LatLng.md)

反地理编码位置坐标
必须参数

___

### latestAdmin

• `Optional` **latestAdmin**: `number`

是否获取最新版行政区划数据（仅对中国数据生效），1（访问），0（不访问）

___

### radius

• `Optional` **radius**: `number`

poi召回半径，允许设置区间为0-1000米，超过1000米按1000米召回
默认值为1000

___

### poiType

• `Optional` **poiType**: `string`

可以选择poi类型召回不同类型的poi，例如 酒店，如想召回多个POI类型数据，可以'|'分割
例如 酒店|房地产
http://lbsyun.baidu.com/index.php?title=lbscloud/poitags

___

### isExtensionsRoad

• `Optional` **isExtensionsRoad**: `boolean`

当取值为true时，召回坐标周围最近的3条道路数据。区别于行政区划中的street参数（street参数为行政区划中的街道，和普通道路不对应）。
默认 false

___

### languageType

• `Optional` **languageType**: `LanguageType`

检索语言类型
默认中文
