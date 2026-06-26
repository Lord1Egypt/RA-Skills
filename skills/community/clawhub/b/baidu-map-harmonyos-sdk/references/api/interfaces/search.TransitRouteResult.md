[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / TransitRouteResult

# Interface: TransitRouteResult

[search](../modules/search.md).TransitRouteResult

公交路线规划结果封装

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`TransitRouteResult`**

## Table of contents

### Properties

- [error](search.TransitRouteResult.md#error)
- [status](search.TransitRouteResult.md#status)
- [taxiInfo](search.TransitRouteResult.md#taxiinfo)
- [routeLines](search.TransitRouteResult.md#routelines)
- [suggestAddrInfo](search.TransitRouteResult.md#suggestaddrinfo)

## Properties

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

___

### taxiInfo

• `Optional` **taxiInfo**: [`TaxiInfo`](search.TaxiInfo.md)

打车信息

___

### routeLines

• `Optional` **routeLines**: [`TransitRouteLine`](search.TransitRouteLine.md)[]

所有换乘路线方案

___

### suggestAddrInfo

• `Optional` **suggestAddrInfo**: [`SuggestAddrInfo`](search.SuggestAddrInfo.md)

建议信息,当#error 为 [ERRORNO#AMBIGUOUS_ROURE_ADDR](../enums/search.ERRORNO.md#ambiguous_roure_addr) 时
可通过此接口获取建议信息
