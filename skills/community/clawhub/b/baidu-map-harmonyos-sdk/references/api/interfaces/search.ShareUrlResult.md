[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / ShareUrlResult

# Interface: ShareUrlResult

[search](../modules/search.md).ShareUrlResult

返回给用户的搜索结果基类

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`ShareUrlResult`**

## Table of contents

### Properties

- [error](search.ShareUrlResult.md#error)
- [status](search.ShareUrlResult.md#status)
- [url](search.ShareUrlResult.md#url)
- [type](search.ShareUrlResult.md#type)

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

### url

• `Optional` **url**: `string`

共享URL

___

### type

• `Optional` **type**: `number`

url所包含数据的检索类型
