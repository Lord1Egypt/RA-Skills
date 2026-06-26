[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / SuggestionSearchOption

# Interface: SuggestionSearchOption

[search](../modules/search.md).SuggestionSearchOption

建议查询请求参数接口

## Table of contents

### Properties

- [city](search.SuggestionSearchOption.md#city)
- [keyword](search.SuggestionSearchOption.md#keyword)
- [isExtendAdcode](search.SuggestionSearchOption.md#isextendadcode)
- [cityLimit](search.SuggestionSearchOption.md#citylimit)
- [location](search.SuggestionSearchOption.md#location)
- [hotWord](search.SuggestionSearchOption.md#hotword)

## Properties

### city

• **city**: ``null`` \| `string`

请求城市区域字段，必须参数
为null时，全国范围检索

___

### keyword

• **keyword**: `string`

检索关键字
必须参数

___

### isExtendAdcode

• `Optional` **isExtendAdcode**: `boolean`

是否获取行政区域编码

___

### cityLimit

• `Optional` **cityLimit**: `boolean`

设置是否限制城市范围
非必须参数，默认为false
取值为"true"时，仅返回city中指定城市检索结果（注：仅限大陆地区有效）

___

### location

• `Optional` **location**: [`LatLng`](../classes/base.LatLng.md)

检索坐标参数
非必须参数
会影响关键字不在设置城市范围内时的检索结果

___

### hotWord

• `Optional` **hotWord**: `boolean`

返回结果类型 true：热词
