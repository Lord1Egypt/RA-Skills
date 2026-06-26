[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / SuggestionResult

# Interface: SuggestionResult

[search](../modules/search.md).SuggestionResult

建议查询请求结果接口

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`SuggestionResult`**

## Table of contents

### Properties

- [error](search.SuggestionResult.md#error)
- [status](search.SuggestionResult.md#status)
- [suggestionList](search.SuggestionResult.md#suggestionlist)

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

### suggestionList

• `Optional` **suggestionList**: [`SuggestionInfo`](search.SuggestionInfo.md)[]

检索结果列表
