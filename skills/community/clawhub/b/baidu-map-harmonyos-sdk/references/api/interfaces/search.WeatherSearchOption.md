[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / WeatherSearchOption

# Interface: WeatherSearchOption

[search](../modules/search.md).WeatherSearchOption

天气请求数据
开通高级权限： http://lbsyun.baidu.com/apiconsole/fankui#?typeOne=产品需求&typeTwo=高级服务
国内行政区域编码表：https://mapopen-website-wiki.cdn.bcebos.com/cityList/weather_district_id.csv
海外行政区域编码表：https://mapopen-website-wiki.cdn.bcebos.com/cityList/weather_aboard_district_id.xlsx
天气取值对照表：https://mapopen-website-wiki.cdn.bcebos.com/cityList/百度地图天气取值对照表(0410).xlsx

## Table of contents

### Properties

- [serverType](search.WeatherSearchOption.md#servertype)
- [districtID](search.WeatherSearchOption.md#districtid)
- [location](search.WeatherSearchOption.md#location)
- [dataType](search.WeatherSearchOption.md#datatype)
- [languageType](search.WeatherSearchOption.md#languagetype)

## Properties

### serverType

• `Optional` **serverType**: `WeatherServerType`

天气服务类型，默认国内

___

### districtID

• `Optional` **districtID**: `string`

区县的行政区划编码，和location二选一

___

### location

• `Optional` **location**: [`LatLng`](../classes/base.LatLng.md)

经纬度，高级字段，需要申请高级权限

___

### dataType

• `Optional` **dataType**: [`WeatherDataType`](../enums/search.WeatherDataType.md)

请求数据类型，默认：WEATHER_DATA_TYPE_REAL_TIME

___

### languageType

• `Optional` **languageType**: `LanguageType`

语言类型，默认中文。目前仅支持海外天气服务行政区划显示英文。
