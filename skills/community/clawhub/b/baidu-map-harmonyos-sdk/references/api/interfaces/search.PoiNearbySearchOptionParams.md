[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiNearbySearchOptionParams

# Interface: PoiNearbySearchOptionParams

[search](../modules/search.md).PoiNearbySearchOptionParams

## Table of contents

### Properties

- [keyword](search.PoiNearbySearchOptionParams.md#keyword)
- [location](search.PoiNearbySearchOptionParams.md#location)
- [radius](search.PoiNearbySearchOptionParams.md#radius)
- [pageNum](search.PoiNearbySearchOptionParams.md#pagenum)
- [pageCapacity](search.PoiNearbySearchOptionParams.md#pagecapacity)
- [sortType](search.PoiNearbySearchOptionParams.md#sorttype)
- [tag](search.PoiNearbySearchOptionParams.md#tag)
- [scope](search.PoiNearbySearchOptionParams.md#scope)
- [radiusLimit](search.PoiNearbySearchOptionParams.md#radiuslimit)
- [poiFilter](search.PoiNearbySearchOptionParams.md#poifilter)
- [isExtendAdcode](search.PoiNearbySearchOptionParams.md#isextendadcode)
- [languageType](search.PoiNearbySearchOptionParams.md#languagetype)
- [isShowPhotos](search.PoiNearbySearchOptionParams.md#isshowphotos)

## Properties

### keyword

• **keyword**: `string`

检索关键字，必须参数
支持多个关键字并集检索，不同关键字间以$符号分隔，最多支持10个关键字检索。如:”银行$酒店”

___

### location

• **location**: [`LatLng`](../classes/base.LatLng.md)

周边检索中心点，不支持多个点
必须参数

___

### radius

• **radius**: `number`

周边检索半径，单位为米
当半径过大，超过中心点所在城市边界时，会变为城市范围检索，检索范围为中心点所在城市
必须参数

___

### pageNum

• `Optional` **pageNum**: `number`

分页页码，默认为0
0代表第一页，1代表第二页，以此类推

___

### pageCapacity

• `Optional` **pageCapacity**: `number`

单页展示POI数量
默认为10条记录，最大返回20条。多关键字检索时，返回的记录数为关键字个数*mPageNum

___

### sortType

• `Optional` **sortType**: [`PoiSortType`](../enums/search.PoiSortType.md)

检索结果排序策略，默认按综合排序

___

### tag

• `Optional` **tag**: `string`

检索分类，
多个分类以","分割，默认空

___

### scope

• `Optional` **scope**: `number`

检索结果详细程度。
取值为1或空，则返回基本信息；取值为2，返回检索POI详细信息。
默认为1

___

### radiusLimit

• `Optional` **radiusLimit**: `boolean`

是否严格限定召回结果在设置检索半径范围内
true（是），false（否）
默认否

___

### poiFilter

• `Optional` **poiFilter**: [`PoiFilter`](../classes/search.PoiFilter.md)

检索过滤条件。
当scope取值为2时，可以设置filter进行排序
默认空

___

### isExtendAdcode

• `Optional` **isExtendAdcode**: `boolean`

是否召回行政区域编码，默认是

___

### languageType

• `Optional` **languageType**: `LanguageType`

检索语言类型
默认中文

___

### isShowPhotos

• `Optional` **isShowPhotos**: `boolean`

是否显示图片
