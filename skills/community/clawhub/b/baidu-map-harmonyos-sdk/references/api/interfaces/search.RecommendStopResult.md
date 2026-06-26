[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / RecommendStopResult

# Interface: RecommendStopResult

[search](../modules/search.md).RecommendStopResult

推荐上车点检索结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`RecommendStopResult`**

## Table of contents

### Properties

- [error](search.RecommendStopResult.md#error)
- [status](search.RecommendStopResult.md#status)
- [stationInfoList](search.RecommendStopResult.md#stationinfolist)
- [recommendStopInfoList](search.RecommendStopResult.md#recommendstopinfolist)

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

### stationInfoList

• `Optional` **stationInfoList**: [`RecommendStationInfo`](search.RecommendStationInfo.md)[]

场站上车点信息列表

___

### recommendStopInfoList

• `Optional` **recommendStopInfoList**: [`RecommendStopInfo`](search.RecommendStopInfo.md)[]

推荐上车点信息列表
