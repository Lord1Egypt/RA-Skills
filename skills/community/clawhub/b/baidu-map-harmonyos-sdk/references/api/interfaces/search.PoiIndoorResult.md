[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiIndoorResult

# Interface: PoiIndoorResult

[search](../modules/search.md).PoiIndoorResult

室内POI搜索结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`PoiIndoorResult`**

## Table of contents

### Properties

- [arrayPoiInfo](search.PoiIndoorResult.md#arraypoiinfo)
- [poiNum](search.PoiIndoorResult.md#poinum)
- [pageNum](search.PoiIndoorResult.md#pagenum)
- [error](search.PoiIndoorResult.md#error)
- [status](search.PoiIndoorResult.md#status)

## Properties

### arrayPoiInfo

• `Optional` **arrayPoiInfo**: `PoiIndoorInfo`[]

室内poi检索结果的poi信息列表

___

### poiNum

• `Optional` **poiNum**: `number`

该poi个数

___

### pageNum

• `Optional` **pageNum**: `number`

该poi当前分页编号

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
