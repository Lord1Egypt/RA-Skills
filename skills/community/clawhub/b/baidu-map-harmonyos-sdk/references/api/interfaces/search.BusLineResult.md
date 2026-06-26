[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / BusLineResult

# Interface: BusLineResult

[search](../modules/search.md).BusLineResult

返回给用户的搜索结果基类

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`BusLineResult`**

## Table of contents

### Properties

- [busCompany](search.BusLineResult.md#buscompany)
- [busLineName](search.BusLineResult.md#buslinename)
- [isMonthTicket](search.BusLineResult.md#ismonthticket)
- [startTime](search.BusLineResult.md#starttime)
- [endTime](search.BusLineResult.md#endtime)
- [uid](search.BusLineResult.md#uid)
- [stations](search.BusLineResult.md#stations)
- [steps](search.BusLineResult.md#steps)
- [basePrice](search.BusLineResult.md#baseprice)
- [maxPrice](search.BusLineResult.md#maxprice)
- [lineDirection](search.BusLineResult.md#linedirection)
- [error](search.BusLineResult.md#error)
- [status](search.BusLineResult.md#status)

## Properties

### busCompany

• `Optional` **busCompany**: `string`

公交公司名称

___

### busLineName

• `Optional` **busLineName**: `string`

公交线路名称

___

### isMonthTicket

• `Optional` **isMonthTicket**: `boolean`

公交是线是否有月票

___

### startTime

• `Optional` **startTime**: `string`

公交路线首班车时间 格式 HH:mm，24 小时制，前导零；时区为线路所属城市本地时区。

___

### endTime

• `Optional` **endTime**: `string`

公交路线末班车时间 格式 HH:mm，24 小时制，前导零；时区为线路所属城市本地时区。

___

### uid

• `Optional` **uid**: `string`

公交线路uid

___

### stations

• `Optional` **stations**: [`BusStation`](search.BusStation.md)[]

所有公交站点信息

___

### steps

• `Optional` **steps**: [`BusStep`](search.BusStep.md)[]

封装分段坐标点，以便扩展

___

### basePrice

• `Optional` **basePrice**: `number`

公交起步价

___

### maxPrice

• `Optional` **maxPrice**: `number`

公交路线的最高票价

___

### lineDirection

• `Optional` **lineDirection**: `string`

公交路线方向

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
