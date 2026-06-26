[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [search](../modules/search.md) / PoiDetailInfo

# Interface: PoiDetailInfo

[search](../modules/search.md).PoiDetailInfo

poi详细信息

## Table of contents

### Properties

- [name](search.PoiDetailInfo.md#name)
- [location](search.PoiDetailInfo.md#location)
- [address](search.PoiDetailInfo.md#address)
- [province](search.PoiDetailInfo.md#province)
- [city](search.PoiDetailInfo.md#city)
- [area](search.PoiDetailInfo.md#area)
- [adCode](search.PoiDetailInfo.md#adcode)
- [telephone](search.PoiDetailInfo.md#telephone)
- [uid](search.PoiDetailInfo.md#uid)
- [streetId](search.PoiDetailInfo.md#streetid)
- [detail](search.PoiDetailInfo.md#detail)
- [distance](search.PoiDetailInfo.md#distance)
- [type](search.PoiDetailInfo.md#type)
- [tag](search.PoiDetailInfo.md#tag)
- [naviLocation](search.PoiDetailInfo.md#navilocation)
- [detailUrl](search.PoiDetailInfo.md#detailurl)
- [price](search.PoiDetailInfo.md#price)
- [shopHours](search.PoiDetailInfo.md#shophours)
- [overallRating](search.PoiDetailInfo.md#overallrating)
- [tasteRating](search.PoiDetailInfo.md#tasterating)
- [serviceRating](search.PoiDetailInfo.md#servicerating)
- [environmentRating](search.PoiDetailInfo.md#environmentrating)
- [facilityRating](search.PoiDetailInfo.md#facilityrating)
- [hygieneRating](search.PoiDetailInfo.md#hygienerating)
- [technologyRating](search.PoiDetailInfo.md#technologyrating)
- [imageNum](search.PoiDetailInfo.md#imagenum)
- [grouponNum](search.PoiDetailInfo.md#grouponnum)
- [discountNum](search.PoiDetailInfo.md#discountnum)
- [commentNum](search.PoiDetailInfo.md#commentnum)
- [favoriteNum](search.PoiDetailInfo.md#favoritenum)
- [checkinNum](search.PoiDetailInfo.md#checkinnum)
- [brand](search.PoiDetailInfo.md#brand)
- [contentTag](search.PoiDetailInfo.md#contenttag)
- [poiChildrenInfoList](search.PoiDetailInfo.md#poichildreninfolist)
- [label](search.PoiDetailInfo.md#label)
- [classifiedPoiTag](search.PoiDetailInfo.md#classifiedpoitag)
- [parentId](search.PoiDetailInfo.md#parentid)
- [newAlias](search.PoiDetailInfo.md#newalias)
- [photos](search.PoiDetailInfo.md#photos)

## Properties

### name

• `Optional` **name**: `string`

poi名称

___

### location

• `Optional` **location**: ``null`` \| [`LatLng`](../classes/base.LatLng.md)

poi经纬度坐标

___

### address

• `Optional` **address**: `string`

poi地址信息

___

### province

• `Optional` **province**: `string`

所属省份

___

### city

• `Optional` **city**: `string`

所属城市

___

### area

• `Optional` **area**: `string`

所属区县

___

### adCode

• `Optional` **adCode**: `number`

行政区划编码

___

### telephone

• `Optional` **telephone**: `string`

poi电话信息

___

### uid

• `Optional` **uid**: `string`

poi的唯一标示

___

### streetId

• `Optional` **streetId**: `string`

街景图id

___

### detail

• `Optional` **detail**: `number`

是否有详情页：1有，0没有

___

### distance

• `Optional` **distance**: `number`

距离中心点的距离，圆形区域检索时返回

___

### type

• `Optional` **type**: `string`

所属分类，如’hotel’、’cater’

___

### tag

• `Optional` **tag**: `string`

标签

___

### naviLocation

• `Optional` **naviLocation**: [`LatLng`](../classes/base.LatLng.md)

POI对应的导航引导点坐标。大型面状POI的导航引导点，一般为各类出入口，方便结合导航、路线规划等服务使用

___

### detailUrl

• `Optional` **detailUrl**: `string`

poi的详情页Url

___

### price

• `Optional` **price**: `number`

poi商户的价格

___

### shopHours

• `Optional` **shopHours**: `string`

营业时间

___

### overallRating

• `Optional` **overallRating**: `number`

总体评分

___

### tasteRating

• `Optional` **tasteRating**: `number`

口味评分

___

### serviceRating

• `Optional` **serviceRating**: `number`

服务评分

___

### environmentRating

• `Optional` **environmentRating**: `number`

环境评分

___

### facilityRating

• `Optional` **facilityRating**: `number`

星级（设备）评分

___

### hygieneRating

• `Optional` **hygieneRating**: `number`

卫生评分

___

### technologyRating

• `Optional` **technologyRating**: `number`

技术评分

___

### imageNum

• `Optional` **imageNum**: `number`

图片数

___

### grouponNum

• `Optional` **grouponNum**: `number`

团购数

___

### discountNum

• `Optional` **discountNum**: `number`

优惠数

___

### commentNum

• `Optional` **commentNum**: `number`

评论数

___

### favoriteNum

• `Optional` **favoriteNum**: `number`

收藏数

___

### checkinNum

• `Optional` **checkinNum**: `number`

签到数

___

### brand

• `Optional` **brand**: `string`

品牌

___

### contentTag

• `Optional` **contentTag**: `string`

标记内容

___

### poiChildrenInfoList

• `Optional` **poiChildrenInfoList**: [`PoiChildrenInfo`](search.PoiChildrenInfo.md)[]

POI子点列表，只有城市检索，周边检索，Sug检索（需要权限）支持
存储POI所有子点信息
V5.2.0版本新增字段，需要使用getter和setter方法操作

___

### label

• `Optional` **label**: `string`

标签

___

### classifiedPoiTag

• `Optional` **classifiedPoiTag**: `string`

标签等级

___

### parentId

• `Optional` **parentId**: `string`

父级ID

___

### newAlias

• `Optional` **newAlias**: `string`

别名

___

### photos

• `Optional` **photos**: `string`[]

图片url
