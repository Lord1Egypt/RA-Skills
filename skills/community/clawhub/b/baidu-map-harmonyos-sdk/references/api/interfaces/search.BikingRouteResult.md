[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BikingRouteResult

# Interface: BikingRouteResult

[search](../modules/search.md).BikingRouteResult

骑行路径规划封装后的结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`BikingRouteResult`**

## Table of contents

### Properties

- [error](search.BikingRouteResult.md#error)
- [status](search.BikingRouteResult.md#status)
- [message](search.BikingRouteResult.md#message)
- [suggestAddrInfo](search.BikingRouteResult.md#suggestaddrinfo)
- [routeLines](search.BikingRouteResult.md#routelines)

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

### message

• `Optional` **message**: `string`

服务端返回的消息内容

___

### suggestAddrInfo

• `Optional` **suggestAddrInfo**: [`SuggestAddrInfo`](search.SuggestAddrInfo.md)

建议信息

error为[ERRORNO#AMBIGUOUS_ROURE_ADDR](../enums/search.ERRORNO.md#ambiguous_roure_addr)时可通过此接口获取建议信息

___

### routeLines

• `Optional` **routeLines**: [`BikingRouteLine`](search.BikingRouteLine.md)[]

获取所有骑行规划路线
