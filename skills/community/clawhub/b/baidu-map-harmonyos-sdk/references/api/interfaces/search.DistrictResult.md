[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / DistrictResult

# Interface: DistrictResult

[search](../modules/search.md).DistrictResult

行政区域信息查询结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`DistrictResult`**

## Table of contents

### Properties

- [centerPt](search.DistrictResult.md#centerpt)
- [polylines](search.DistrictResult.md#polylines)
- [cityCode](search.DistrictResult.md#citycode)
- [cityName](search.DistrictResult.md#cityname)
- [error](search.DistrictResult.md#error)
- [status](search.DistrictResult.md#status)

## Properties

### centerPt

• `Optional` **centerPt**: ``null`` \| [`LatLng`](../classes/base.LatLng.md)

行政区域中心点

___

### polylines

• `Optional` **polylines**: [`LatLng`](../classes/base.LatLng.md)[][]

行政区域边界坐标点

___

### cityCode

• `Optional` **cityCode**: `number`

行政区域编码

___

### cityName

• `Optional` **cityName**: ``null`` \| `string`

行政区域名称

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
