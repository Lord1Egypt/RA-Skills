[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiCitySearchOptionParams

# Interface: PoiCitySearchOptionParams

[search](../modules/search.md).PoiCitySearchOptionParams

## Table of contents

### Properties

- [city](search.PoiCitySearchOptionParams.md#city)
- [keyword](search.PoiCitySearchOptionParams.md#keyword)
- [pageNum](search.PoiCitySearchOptionParams.md#pagenum)
- [pageCapacity](search.PoiCitySearchOptionParams.md#pagecapacity)
- [isReturnAddr](search.PoiCitySearchOptionParams.md#isreturnaddr)
- [tag](search.PoiCitySearchOptionParams.md#tag)
- [scope](search.PoiCitySearchOptionParams.md#scope)
- [isCityLimit](search.PoiCitySearchOptionParams.md#iscitylimit)
- [poiFilter](search.PoiCitySearchOptionParams.md#poifilter)
- [isExtendAdcode](search.PoiCitySearchOptionParams.md#isextendadcode)
- [languageType](search.PoiCitySearchOptionParams.md#languagetype)
- [isShowPhotos](search.PoiCitySearchOptionParams.md#isshowphotos)

## Properties

### city

• **city**: `string`

检索行政区划区域。可输入行政区划名或对应cityCode
必须参数
如需严格限制召回数据在区域内，请设置isCityLimit参数为true

___

### keyword

• **keyword**: `string`

检索关键字，必须参数

___

### pageNum

• `Optional` **pageNum**: `number`

分页页码
默认为0,0代表第一页，1代表第二页，以此类推

___

### pageCapacity

• `Optional` **pageCapacity**: `number`

单页展示POI数量，默认为10条记录，最大返回20条。
多关键字检索时，返回的记录数为关键字个数*pageNum

___

### isReturnAddr

• `Optional` **isReturnAddr**: `boolean`

是否返回地址信息

___

### tag

• `Optional` **tag**: `string`

检索分类，
多个分类以","分割

___

### scope

• `Optional` **scope**: `number`

检索结果详细程度。
取值为 或空，则返回基本信息；取值为2，返回检索POI详细信息

___

### isCityLimit

• `Optional` **isCityLimit**: `boolean`

区域数据召回限制
为true时，仅返回city对应区域内数据

___

### poiFilter

• `Optional` **poiFilter**: [`PoiFilter`](../classes/search.PoiFilter.md)

检索过滤条件。
当scope取值为2时，可以设置filter进行排序

___

### isExtendAdcode

• `Optional` **isExtendAdcode**: `boolean`

是召回行政区域编码

___

### languageType

• `Optional` **languageType**: `LanguageType`

检索语言类型
默认中文

___

### isShowPhotos

• `Optional` **isShowPhotos**: `boolean`

是否显示图片
