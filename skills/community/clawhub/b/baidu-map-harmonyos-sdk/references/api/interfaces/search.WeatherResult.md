[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / WeatherResult

# Interface: WeatherResult

[search](../modules/search.md).WeatherResult

天气检索结果

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`WeatherResult`**

## Table of contents

### Properties

- [error](search.WeatherResult.md#error)
- [status](search.WeatherResult.md#status)
- [realTimeWeather](search.WeatherResult.md#realtimeweather)
- [location](search.WeatherResult.md#location)
- [forecasts](search.WeatherResult.md#forecasts)
- [forecastHours](search.WeatherResult.md#forecasthours)
- [lifeIndexes](search.WeatherResult.md#lifeindexes)
- [weatherAlerts](search.WeatherResult.md#weatheralerts)

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

### realTimeWeather

• `Optional` **realTimeWeather**: [`WeatherSearchRealTime`](search.WeatherSearchRealTime.md)

天气实况数据

___

### location

• `Optional` **location**: [`WeatherSearchLocation`](search.WeatherSearchLocation.md)

地理位置信息

___

### forecasts

• `Optional` **forecasts**: [`WeatherSearchForecasts`](search.WeatherSearchForecasts.md)[]

未来若干天天预报数据

___

### forecastHours

• `Optional` **forecastHours**: [`WeatherSearchForecastForHours`](search.WeatherSearchForecastForHours.md)[]

未来24小时逐小时预报，高级字段

___

### lifeIndexes

• `Optional` **lifeIndexes**: [`WeatherLifeIndexes`](search.WeatherLifeIndexes.md)[]

生活指数数据，高级字段

___

### weatherAlerts

• `Optional` **weatherAlerts**: [`WeatherSearchAlerts`](search.WeatherSearchAlerts.md)[]

气象预警数据，高级字段
