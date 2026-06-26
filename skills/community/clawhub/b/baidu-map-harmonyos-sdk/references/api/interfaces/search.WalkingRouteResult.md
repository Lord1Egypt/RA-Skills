[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / WalkingRouteResult

# Interface: WalkingRouteResult

[search](../modules/search.md).WalkingRouteResult

步行路线规划结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`WalkingRouteResult`**

## Table of contents

### Properties

- [error](search.WalkingRouteResult.md#error)
- [status](search.WalkingRouteResult.md#status)
- [routeLines](search.WalkingRouteResult.md#routelines)
- [taxiInfo](search.WalkingRouteResult.md#taxiinfo)
- [suggestAddrInfo](search.WalkingRouteResult.md#suggestaddrinfo)

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

### routeLines

• `Optional` **routeLines**: [`WalkingRouteLine`](search.WalkingRouteLine.md)[]

所有步行规划路线

___

### taxiInfo

• `Optional` **taxiInfo**: [`TaxiInfo`](search.TaxiInfo.md)

打车信息

___

### suggestAddrInfo

• `Optional` **suggestAddrInfo**: [`SuggestAddrInfo`](search.SuggestAddrInfo.md)

建议信息
