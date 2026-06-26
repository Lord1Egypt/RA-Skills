[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / ReverseGeoCodeResult

# Interface: ReverseGeoCodeResult

[search](../modules/search.md).ReverseGeoCodeResult

反 Geo Code 结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`ReverseGeoCodeResult`**

## Table of contents

### Properties

- [businessCircle](search.ReverseGeoCodeResult.md#businesscircle)
- [address](search.ReverseGeoCodeResult.md#address)
- [addressDetail](search.ReverseGeoCodeResult.md#addressdetail)
- [location](search.ReverseGeoCodeResult.md#location)
- [cityCode](search.ReverseGeoCodeResult.md#citycode)
- [poiList](search.ReverseGeoCodeResult.md#poilist)
- [sematicDescription](search.ReverseGeoCodeResult.md#sematicdescription)
- [poiRegionsInfoList](search.ReverseGeoCodeResult.md#poiregionsinfolist)
- [roadInfoList](search.ReverseGeoCodeResult.md#roadinfolist)
- [adcode](search.ReverseGeoCodeResult.md#adcode)
- [error](search.ReverseGeoCodeResult.md#error)
- [status](search.ReverseGeoCodeResult.md#status)

## Properties

### businessCircle

• `Optional` **businessCircle**: `string`

商圈名称
如 "人民大学,中关村,苏州街"，一个坐标检索最多返回3个

___

### address

• `Optional` **address**: `string`

地址名称

___

### addressDetail

• `Optional` **addressDetail**: ``null`` \| [`AddressComponent`](search.AddressComponent.md)

层次化地址信息

___

### location

• `Optional` **location**: ``null`` \| [`LatLng`](../classes/base.LatLng.md)

地址坐标

___

### cityCode

• `Optional` **cityCode**: `number`

百度定义的城市id

___

### poiList

• `Optional` **poiList**: [`PoiInfo`](search.PoiInfo.md)[]

地址周边Poi信息，只有在type为MK_REVERSEGEOCODE时才有效

___

### sematicDescription

• `Optional` **sematicDescription**: `string`

当前位置结合POI的语义化结果描述

___

### poiRegionsInfoList

• `Optional` **poiRegionsInfoList**: [`PoiRegionsInfo`](search.PoiRegionsInfo.md)[]

请求中的坐标与POI对应的区域面（AOI）的归属关系信息
以数组形式返回

___

### roadInfoList

• `Optional` **roadInfoList**: [`RoadInfo`](search.RoadInfo.md)[]

召回坐标周围最近的3条道路信息

___

### adcode

• `Optional` **adcode**: `number`

行政区域编码

___

### error

• `Optional` **error**: [`ERRORNO`](../enums/search.ERRORNO.md)

检索结果错误码， 各错误值见[ERRORNO](../enums/search.ERRORNO.md)

#### Inherited from

[SearchResult](search.SearchResult.md).[error](search.SearchResult.md#error)

___

### status

• `Optional` **status**: `number`

检索结果状态码，各状态值请见
{https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-geocoding-abroad-base#%E6%9C%8D%E5%8A%A1%E7%8A%B6%E6%80%81%E7%A0%81}

#### Inherited from

[SearchResult](search.SearchResult.md).[status](search.SearchResult.md#status)
