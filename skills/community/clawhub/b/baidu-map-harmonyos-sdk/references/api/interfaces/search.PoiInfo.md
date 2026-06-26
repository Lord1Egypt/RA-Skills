[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiInfo

# Interface: PoiInfo

[search](../modules/search.md).PoiInfo

poi信息类

## Table of contents

### Properties

- [name](search.PoiInfo.md#name)
- [uid](search.PoiInfo.md#uid)
- [address](search.PoiInfo.md#address)
- [province](search.PoiInfo.md#province)
- [city](search.PoiInfo.md#city)
- [area](search.PoiInfo.md#area)
- [street\_id](search.PoiInfo.md#street_id)
- [phoneNum](search.PoiInfo.md#phonenum)
- [postCode](search.PoiInfo.md#postcode)
- [detail](search.PoiInfo.md#detail)
- [type](search.PoiInfo.md#type)
- [location](search.PoiInfo.md#location)
- [hasCaterDetails](search.PoiInfo.md#hascaterdetails)
- [isPano](search.PoiInfo.md#ispano)
- [tag](search.PoiInfo.md#tag)
- [adCode](search.PoiInfo.md#adcode)
- [poiDetailInfo](search.PoiInfo.md#poidetailinfo)
- [direction](search.PoiInfo.md#direction)
- [distance](search.PoiInfo.md#distance)
- [parentPoiInfo](search.PoiInfo.md#parentpoiinfo)

## Properties

### name

• `Optional` **name**: `string`

poi名称

___

### uid

• `Optional` **uid**: `string`

poi唯一标识
如果为isPano为true，可用此参数调用街景组件PanoramaService类
的requestPanoramaWithPoiUId方法检索街景数据

___

### address

• `Optional` **address**: `string`

poi地址信息

___

### province

• `Optional` **province**: `string`

poi所在省份

___

### city

• `Optional` **city**: `string`

poi所在城市

___

### area

• `Optional` **area**: `string`

poi所在行政区域

___

### street\_id

• `Optional` **street\_id**: `string`

poi对应的街景图id

___

### phoneNum

• `Optional` **phoneNum**: `string`

poi电话信息

___

### postCode

• `Optional` **postCode**: `string`

poi邮编

___

### detail

• `Optional` **detail**: `number`

poi是否有详情页

___

### type

• `Optional` **type**: [`POITYPE`](../enums/search.POITYPE.md)

poi类型，0：普通点，1：公交站，2：公交线路，3：地铁站，4：地铁线路,

___

### location

• `Optional` **location**: ``null`` \| [`LatLng`](../classes/base.LatLng.md)

poi坐标, 当ePoiType为2或4时，pt 为空

___

### hasCaterDetails

• `Optional` **hasCaterDetails**: `boolean`

poi点是否有美食类详情页面

___

### isPano

• `Optional` **isPano**: `boolean`

poi点附近是否有街景，可使用uid检索全景组件的全景数据

___

### tag

• `Optional` **tag**: `string`

poi分类，如："美食;中餐厅"

___

### adCode

• `Optional` **adCode**: `number`

行政区划编码

___

### poiDetailInfo

• `Optional` **poiDetailInfo**: ``null`` \| [`PoiDetailInfo`](search.PoiDetailInfo.md)

poi扩展信息

___

### direction

• `Optional` **direction**: `string`

RGC请求结果中，周边POI和请求坐标点的方向关系，比如“内”，“西”，“南”等。
判断时，取结果中的第一个POI的该参数即可，如果返回为“内”则说明经纬度坐标该POI所属的面内
V5.2.0版本开放

___

### distance

• `Optional` **distance**: `number`

RGC请求结果中，周边POI和请求坐标点的距离
distance = 0，说明经纬度位于POI所在的面内，但是也可能是POI的经纬度点
V5.2.0版本开放

___

### parentPoiInfo

• `Optional` **parentPoiInfo**: ``null`` \| [`ParentPoiInfo`](search.ParentPoiInfo.md)

RGC请求结果中，poi对应的主点poi信息（如，海底捞的主点为上地华联，
该字段则为上地华联的poi信息。如POI无主点，则无该字段为空）
