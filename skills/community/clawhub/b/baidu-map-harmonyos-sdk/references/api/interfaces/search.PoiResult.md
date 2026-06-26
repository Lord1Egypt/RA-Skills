[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiResult

# Interface: PoiResult

[search](../modules/search.md).PoiResult

poi搜索结果。

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`PoiResult`**

## Table of contents

### Properties

- [currentPageNum](search.PoiResult.md#currentpagenum)
- [totalPageNum](search.PoiResult.md#totalpagenum)
- [currentPageCapacity](search.PoiResult.md#currentpagecapacity)
- [totalPoiNum](search.PoiResult.md#totalpoinum)
- [arrayPoiInfo](search.PoiResult.md#arraypoiinfo)
- [hasPoiAddr](search.PoiResult.md#haspoiaddr)
- [arrayAddrInfo](search.PoiResult.md#arrayaddrinfo)
- [arrayCityInfo](search.PoiResult.md#arraycityinfo)
- [error](search.PoiResult.md#error)
- [status](search.PoiResult.md#status)

## Properties

### currentPageNum

• `Optional` **currentPageNum**: `number`

当前分页编号
0-第一页；1-第二页，依此类推

___

### totalPageNum

• `Optional` **totalPageNum**: `number`

所有分页数

___

### currentPageCapacity

• `Optional` **currentPageCapacity**: `number`

单页可展示的POI数量

___

### totalPoiNum

• `Optional` **totalPoiNum**: `number`

结果所有POI数量

___

### arrayPoiInfo

• `Optional` **arrayPoiInfo**: [`PoiInfo`](search.PoiInfo.md)[]

POI信息列表
POI各字段在[PoiInfo](search.PoiInfo.md)中定义

___

### hasPoiAddr

• `Optional` **hasPoiAddr**: `boolean`

是否包含门址信息

___

### arrayAddrInfo

• `Optional` **arrayAddrInfo**: [`PoiAddrInfo`](search.PoiAddrInfo.md)[]

POI门址信息列表
门址各个字段在[PoiAddrInfo](search.PoiAddrInfo.md)中定义

___

### arrayCityInfo

• `Optional` **arrayCityInfo**: [`CityInfo`](search.CityInfo.md)[]

城市信息列表
城市检索，当前城市无结果，结果在其它城市时，返回其它城市信息

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
