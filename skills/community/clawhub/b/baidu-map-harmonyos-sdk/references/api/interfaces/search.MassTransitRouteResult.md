[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / MassTransitRouteResult

# Interface: MassTransitRouteResult

[search](../modules/search.md).MassTransitRouteResult

跨城公交线路规划结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`MassTransitRouteResult`**

## Table of contents

### Properties

- [error](search.MassTransitRouteResult.md#error)
- [status](search.MassTransitRouteResult.md#status)
- [origin](search.MassTransitRouteResult.md#origin)
- [destination](search.MassTransitRouteResult.md#destination)
- [massTaxiInfo](search.MassTransitRouteResult.md#masstaxiinfo)
- [total](search.MassTransitRouteResult.md#total)
- [routeLines](search.MassTransitRouteResult.md#routelines)
- [suggestAddrInfo](search.MassTransitRouteResult.md#suggestaddrinfo)

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

### origin

• `Optional` **origin**: [`TransitResultNode`](search.TransitResultNode.md)

起点

___

### destination

• `Optional` **destination**: [`TransitResultNode`](search.TransitResultNode.md)

终点

___

### massTaxiInfo

• `Optional` **massTaxiInfo**: [`TaxiInfo`](search.TaxiInfo.md)

打车信息

___

### total

• `Optional` **total**: `number`

所有路线总数

___

### routeLines

• `Optional` **routeLines**: [`MassTransitRouteLine`](search.MassTransitRouteLine.md)[]

获取所有换乘路线方案

___

### suggestAddrInfo

• `Optional` **suggestAddrInfo**: [`SuggestAddrInfo`](search.SuggestAddrInfo.md)

当#error 为 [ERRORNO#AMBIGUOUS_ROURE_ADDR](../enums/search.ERRORNO.md#ambiguous_roure_addr) 时
可通过此接口获取建议信息
