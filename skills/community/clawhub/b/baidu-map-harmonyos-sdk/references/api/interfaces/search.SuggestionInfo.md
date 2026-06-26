[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / SuggestionInfo

# Interface: SuggestionInfo

[search](../modules/search.md).SuggestionInfo

suggestion信息接口

## Table of contents

### Properties

- [key](search.SuggestionInfo.md#key)
- [city](search.SuggestionInfo.md#city)
- [district](search.SuggestionInfo.md#district)
- [pt](search.SuggestionInfo.md#pt)
- [uid](search.SuggestionInfo.md#uid)
- [tag](search.SuggestionInfo.md#tag)
- [address](search.SuggestionInfo.md#address)
- [adCode](search.SuggestionInfo.md#adcode)
- [poiChildrenInfoList](search.SuggestionInfo.md#poichildreninfolist)

## Properties

### key

• **key**: `string`

联想词名称

___

### city

• **city**: `string`

联想词city

___

### district

• **district**: `string`

联想结果所在行政区

___

### pt

• `Optional` **pt**: [`LatLng`](../classes/base.LatLng.md)

联想结果坐标点

___

### uid

• **uid**: `string`

联想结果uid

___

### tag

• **tag**: `string`

联想结果标签

___

### address

• **address**: `string`

联想结果地址

___

### adCode

• **adCode**: `number`

行政区划编码

___

### poiChildrenInfoList

• **poiChildrenInfoList**: [`PoiChildrenInfo`](search.PoiChildrenInfo.md)[]

联想词子点，以列表形式展示
V5.2.0版本新增字段，需要使用setter和getter方法操作
该字段需要申请权限
