[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiChildrenInfo

# Interface: PoiChildrenInfo

[search](../modules/search.md).PoiChildrenInfo

POI子节点数据类，提供更准确的POI描述（城市检索，周边检索，Sug检索支持）

## Table of contents

### Properties

- [uid](search.PoiChildrenInfo.md#uid)
- [name](search.PoiChildrenInfo.md#name)
- [showName](search.PoiChildrenInfo.md#showname)
- [tag](search.PoiChildrenInfo.md#tag)
- [location](search.PoiChildrenInfo.md#location)
- [address](search.PoiChildrenInfo.md#address)
- [classifiedPoiTag](search.PoiChildrenInfo.md#classifiedpoitag)

## Properties

### uid

• `Optional` **uid**: `string`

POI子点ID

___

### name

• `Optional` **name**: `string`

POI子点名称

___

### showName

• `Optional` **showName**: `string`

POI子点简称

___

### tag

• `Optional` **tag**: `string`

POI子点类别

___

### location

• `Optional` **location**: [`LatLng`](../classes/base.LatLng.md)

POI子点坐标
Suggestion检索不支持该字段

___

### address

• `Optional` **address**: `string`

POI子点地址
仅城市检索，周边检索支持该字段，Sug检索无此字段

___

### classifiedPoiTag

• `Optional` **classifiedPoiTag**: `string`

POI子点类型
