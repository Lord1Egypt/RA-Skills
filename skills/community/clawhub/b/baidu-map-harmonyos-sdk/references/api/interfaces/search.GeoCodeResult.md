[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / GeoCodeResult

# Interface: GeoCodeResult

[search](../modules/search.md).GeoCodeResult

返回给用户的搜索结果基类

## Hierarchy

- [`SearchResult`](search.SearchResult.md)

  ↳ **`GeoCodeResult`**

## Table of contents

### Properties

- [location](search.GeoCodeResult.md#location)
- [precise](search.GeoCodeResult.md#precise)
- [confidence](search.GeoCodeResult.md#confidence)
- [level](search.GeoCodeResult.md#level)
- [error](search.GeoCodeResult.md#error)
- [status](search.GeoCodeResult.md#status)

## Properties

### location

• `Optional` **location**: ``null`` \| [`LatLng`](../classes/base.LatLng.md)

经纬度坐标

___

### precise

• `Optional` **precise**: `number`

位置的附加信息，是否精确查找
1为精确查找，即准确打点；0为不精确，即模糊打点
（模糊打点无法保证准确度，不建议使用）

___

### confidence

• `Optional` **confidence**: `number`

可信度，描述打点准确度，大于80表示误差小于100m
该字段仅作参考，返回结果准确度主要参考precise参数

___

### level

• `Optional` **level**: `string`

能精确理解的地址类型
包含：UNKNOWN、国家、省、城市、区县、乡镇、村庄、道路、地产小区、商务大厦、
政府机构、交叉路口、商圈、生活服务、休闲娱乐、餐饮、宾馆、购物、金融、教育、
医疗 、工业园区 、旅游景点 、汽车服务、火车站、长途汽车站、桥 、
停车场/停车区、港口/码头、收费区/收费站、飞机场 、机场 、收费处/收费站 、加油站、绿地、门址

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
