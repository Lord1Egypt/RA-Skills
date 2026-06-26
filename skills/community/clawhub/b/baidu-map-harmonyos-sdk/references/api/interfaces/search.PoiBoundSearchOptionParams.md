[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiBoundSearchOptionParams

# Interface: PoiBoundSearchOptionParams

[search](../modules/search.md).PoiBoundSearchOptionParams

## Table of contents

### Properties

- [bound](search.PoiBoundSearchOptionParams.md#bound)
- [keyword](search.PoiBoundSearchOptionParams.md#keyword)
- [pageNum](search.PoiBoundSearchOptionParams.md#pagenum)
- [pageCapacity](search.PoiBoundSearchOptionParams.md#pagecapacity)
- [tag](search.PoiBoundSearchOptionParams.md#tag)
- [scope](search.PoiBoundSearchOptionParams.md#scope)
- [poiFilter](search.PoiBoundSearchOptionParams.md#poifilter)
- [languageType](search.PoiBoundSearchOptionParams.md#languagetype)
- [isExtendAdcode](search.PoiBoundSearchOptionParams.md#isextendadcode)
- [isShowPhotos](search.PoiBoundSearchOptionParams.md#isshowphotos)

## Properties

### bound

• **bound**: [`LatLngBounds`](../classes/base.LatLngBounds.md)

检索矩形区域
必选参数

___

### keyword

• **keyword**: `string`

检索关键字。必须参数
支持多个关键字并集检索，不同关键字间以$符号分隔，最多支持10个关键字检索。如:”银行$酒店”

___

### pageNum

• `Optional` **pageNum**: `number`

分页页码
默认为0,0代表第一页，1代表第二页，以此类推

___

### pageCapacity

• `Optional` **pageCapacity**: `number`

单次返回POI数量，默认为10条记录，最大返回20条。
多关键字检索时，返回的记录数为关键字个数*mPageNum

___

### tag

• `Optional` **tag**: `string`

检索分类，
多个分类以","分割
默认为空

___

### scope

• `Optional` **scope**: `number`

检索结果详细程度。
取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息
默认为1

___

### poiFilter

• `Optional` **poiFilter**: ``null`` \| [`PoiFilter`](../classes/search.PoiFilter.md)

检索过滤条件。
当scope取值为2时，可以设置filter进行排序

___

### languageType

• `Optional` **languageType**: `LanguageType`

检索语言类型
默认中文

___

### isExtendAdcode

• `Optional` **isExtendAdcode**: `boolean`

是否召回行政区域编码,默认是

___

### isShowPhotos

• `Optional` **isShowPhotos**: `boolean`

是否显示图片
