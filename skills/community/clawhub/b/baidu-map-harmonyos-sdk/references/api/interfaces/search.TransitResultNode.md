[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / TransitResultNode

# Interface: TransitResultNode

[search](../modules/search.md).TransitResultNode

公交路线规划结果点信息

## Table of contents

### Properties

- [cityId](search.TransitResultNode.md#cityid)
- [cityName](search.TransitResultNode.md#cityname)
- [location](search.TransitResultNode.md#location)
- [searchWord](search.TransitResultNode.md#searchword)

## Properties

### cityId

• `Optional` **cityId**: `number`

城市编号

___

### cityName

• `Optional` **cityName**: ``null`` \| `string`

城市名

___

### location

• `Optional` **location**: ``null`` \| [`LatLng`](../classes/base.LatLng.md)

坐标

___

### searchWord

• `Optional` **searchWord**: ``null`` \| `string`

检索时关键字（在检索词模糊，返回建议列表时才有。有路线结果时，该字段为空）
