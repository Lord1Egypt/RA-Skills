[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BuildingResult

# Interface: BuildingResult

[search](../modules/search.md).BuildingResult

返回给用户的搜索结果基类

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`BuildingResult`**

## Table of contents

### Properties

- [buildingList](search.BuildingResult.md#buildinglist)
- [relation](search.BuildingResult.md#relation)
- [error](search.BuildingResult.md#error)
- [status](search.BuildingResult.md#status)

## Properties

### buildingList

• `Optional` **buildingList**: [`BuildingInfo`](base.BuildingInfo.md)[]

建筑物检索信息列表

___

### relation

• `Optional` **relation**: `number`

建筑物与请求中坐标点的关系：
1：坐标点在建筑物内
0：坐标点在建筑物附近且小于请求中的半径

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
