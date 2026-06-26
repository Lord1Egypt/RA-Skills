[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / SearchResult

# Interface: SearchResult

[search](../modules/search.md).SearchResult

返回给用户的搜索结果基类

## Hierarchy

- **`SearchResult`**

  ↳ [`ShareUrlResult`](search.ShareUrlResult.md)

  ↳ [`WeatherResult`](search.WeatherResult.md)

  ↳ [`PoiResult`](search.PoiResult.md)
  
  ↳ [`PoiDetailSearchResult`](search.PoiDetailSearchResult.md)

  ↳ [`PoiIndoorResult`](search.PoiIndoorResult.md)

  ↳ [`MassTransitRouteResult`](search.MassTransitRouteResult.md)

  ↳ [`RecommendStopResult`](search.RecommendStopResult.md)

  ↳ [`BikingRouteResult`](search.BikingRouteResult.md)

  ↳ [`DrivingRouteResult`](search.DrivingRouteResult.md)

  ↳ [`WalkingRouteResult`](search.WalkingRouteResult.md)

  ↳ [`TransitRouteResult`](search.TransitRouteResult.md)

  ↳ [`GeoCodeResult`](search.GeoCodeResult.md)

  ↳ [`ReverseGeoCodeResult`](search.ReverseGeoCodeResult.md)

  ↳ [`AoiResult`](search.AoiResult.md)

  ↳ [`BuildingResult`](search.BuildingResult.md)

  ↳ [`DistrictResult`](search.DistrictResult.md)

  ↳ [`BusLineResult`](search.BusLineResult.md)

  ↳ [`SuggestionResult`](search.SuggestionResult.md)

## Table of contents

### Properties

- [error](search.SearchResult.md#error)
- [status](search.SearchResult.md#status)

## Properties

### error

• `Optional` **error**: [`ERRORNO`](../enums/search.ERRORNO.md)

检索结果错误码， 各错误值见[ERRORNO](../enums/search.ERRORNO.md)

___

### status

• `Optional` **status**: `number`

检索结果状态码，各状态值请见
{https://lbs.baidu.com/faq/api?title=webapi/guide/webservice-geocoding-abroad-base#%E6%9C%8D%E5%8A%A1%E7%8A%B6%E6%80%81%E7%A0%81}
