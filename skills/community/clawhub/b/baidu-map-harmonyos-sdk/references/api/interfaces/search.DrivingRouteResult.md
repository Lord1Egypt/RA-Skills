[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / DrivingRouteResult

# Interface: DrivingRouteResult

[search](../modules/search.md).DrivingRouteResult

驾车路线结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`DrivingRouteResult`**

## Table of contents

### Properties

- [error](search.DrivingRouteResult.md#error)
- [status](search.DrivingRouteResult.md#status)
- [routeLines](search.DrivingRouteResult.md#routelines)
- [taxiInfos](search.DrivingRouteResult.md#taxiinfos)
- [suggestAddrInfo](search.DrivingRouteResult.md#suggestaddrinfo)

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

• `Optional` **routeLines**: [`DrivingRouteLine`](search.DrivingRouteLine.md)[]

所有规划路线方案

___

### taxiInfos

• `Optional` **taxiInfos**: [`TaxiInfo`](search.TaxiInfo.md)[]

打车信息

___

### suggestAddrInfo

• `Optional` **suggestAddrInfo**: [`SuggestAddrInfo`](search.SuggestAddrInfo.md)

路线建议搜索信息,当#error值为[ERRORNO#AMBIGUOUS_ROURE_ADDR](../enums/search.ERRORNO.md#ambiguous_roure_addr)时，建议信息不为空
