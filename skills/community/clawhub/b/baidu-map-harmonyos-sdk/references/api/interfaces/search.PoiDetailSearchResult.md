[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiDetailSearchResult

# Interface: PoiDetailSearchResult

[search](../modules/search.md).PoiDetailSearchResult

CopyRight        Baidu

@Date:           2024/6/26

@Description:    POI详情检索结果
                 支持多个UID进行检索，以数组形式返回结果，
                 字段通过数组元素[PoiDetailInfo](search.PoiDetailInfo.md)进行获取

@Version: 1.0.0

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`PoiDetailSearchResult`**

## Table of contents

### Properties

- [poiDetailInfoList](search.PoiDetailSearchResult.md#poidetailinfolist)
- [error](search.PoiDetailSearchResult.md#error)
- [status](search.PoiDetailSearchResult.md#status)

## Properties

### poiDetailInfoList

• `Optional` **poiDetailInfoList**: [`PoiDetailInfo`](search.PoiDetailInfo.md)[]

POI详细信息列表

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
