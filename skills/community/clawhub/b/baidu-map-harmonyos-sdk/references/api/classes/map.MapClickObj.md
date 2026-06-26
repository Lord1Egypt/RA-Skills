[HarmonyNEXT地图SDK](../README.md) / [Modules](../modules.md) / [map](../modules/map.md) / MapClickObj

# Class: MapClickObj

[map](../modules/map.md).MapClickObj

## Table of contents

### Constructors

- [constructor](map.MapClickObj.md#constructor)

### Properties

- [routeType](map.MapClickObj.md#routetype)
- [routeId](map.MapClickObj.md#routeid)
- [segIndex](map.MapClickObj.md#segindex)
- [status](map.MapClickObj.md#status)
- [type](map.MapClickObj.md#type)
- [strUid](map.MapClickObj.md#struid)
- [pid](map.MapClickObj.md#pid)
- [strText](map.MapClickObj.md#strtext)
- [index](map.MapClickObj.md#index)
- [layerId](map.MapClickObj.md#layerid)
- [iconPath](map.MapClickObj.md#iconpath)
- [anim](map.MapClickObj.md#anim)
- [topicId](map.MapClickObj.md#topicid)
- [geoPt](map.MapClickObj.md#geopt)
- [geoZ](map.MapClickObj.md#geoz)
- [indoorPoi](map.MapClickObj.md#indoorpoi)
- [poiOnlineType](map.MapClickObj.md#poionlinetype)
- [bid](map.MapClickObj.md#bid)
- [clickAction](map.MapClickObj.md#clickaction)
- [exJson](map.MapClickObj.md#exjson)
- [statisticValue](map.MapClickObj.md#statisticvalue)
- [offset](map.MapClickObj.md#offset)
- [ssName](map.MapClickObj.md#ssname)
- [ssIndoorId](map.MapClickObj.md#ssindoorid)
- [ssPoiUid](map.MapClickObj.md#sspoiuid)
- [ssZ](map.MapClickObj.md#ssz)
- [ssRotation](map.MapClickObj.md#ssrotation)
- [ssPanoId](map.MapClickObj.md#sspanoid)
- [ssData](map.MapClickObj.md#ssdata)
- [ssType](map.MapClickObj.md#sstype)
- [streetArrowCenterX](map.MapClickObj.md#streetarrowcenterx)
- [streetArrowCenterY](map.MapClickObj.md#streetarrowcentery)
- [dynamicSrc](map.MapClickObj.md#dynamicsrc)
- [ad](map.MapClickObj.md#ad)
- [adstyle](map.MapClickObj.md#adstyle)
- [qid](map.MapClickObj.md#qid)
- [puid](map.MapClickObj.md#puid)
- [adLog](map.MapClickObj.md#adlog)
- [dysrc](map.MapClickObj.md#dysrc)
- [dystge](map.MapClickObj.md#dystge)
- [url](map.MapClickObj.md#url)
- [styleId](map.MapClickObj.md#styleid)
- [level](map.MapClickObj.md#level)
- [isAgg](map.MapClickObj.md#isagg)
- [tagName](map.MapClickObj.md#tagname)
- [tagSrcLog](map.MapClickObj.md#tagsrclog)
- [isDot](map.MapClickObj.md#isdot)

### Methods

- [parseMCarJsonObj](map.MapClickObj.md#parsemcarjsonobj)
- [parseNormalJsonObj](map.MapClickObj.md#parsenormaljsonobj)

## Constructors

### constructor

• **new MapClickObj**(): [`MapClickObj`](map.MapClickObj.md)

#### Returns

[`MapClickObj`](map.MapClickObj.md)

## Properties

### routeType

• **routeType**: `string`

驾车多路线

___

### routeId

• **routeId**: `number`

___

### segIndex

• **segIndex**: `number`

___

### status

• **status**: `number`

___

### type

• **type**: `number`

其它点击

___

### strUid

• **strUid**: `string`

___

### pid

• **pid**: `number`

___

### strText

• **strText**: `string`

___

### index

• **index**: `number`

___

### layerId

• **layerId**: `number`

___

### iconPath

• **iconPath**: `string`

___

### anim

• **anim**: `string`

___

### topicId

• **topicId**: `number`

___

### geoPt

• **geoPt**: `default`

___

### geoZ

• **geoZ**: `number`

___

### indoorPoi

• **indoorPoi**: `boolean`

___

### poiOnlineType

• **poiOnlineType**: `number`

___

### bid

• **bid**: `string`

___

### clickAction

• **clickAction**: `string`

___

### exJson

• **exJson**: `string`

___

### statisticValue

• **statisticValue**: `number`

___

### offset

• **offset**: `number`

___

### ssName

• **ssName**: `string`

___

### ssIndoorId

• **ssIndoorId**: `string`

___

### ssPoiUid

• **ssPoiUid**: `string`

___

### ssZ

• **ssZ**: `number`

___

### ssRotation

• **ssRotation**: `number`

___

### ssPanoId

• **ssPanoId**: `string`

___

### ssData

• **ssData**: `string`

___

### ssType

• **ssType**: `string`

___

### streetArrowCenterX

• **streetArrowCenterX**: `number`

___

### streetArrowCenterY

• **streetArrowCenterY**: `number`

___

### dynamicSrc

• **dynamicSrc**: `number`

动态底图增加type

0:检索点
1:父子点
3:推荐点
4:商业广告
5:检索多结果点
7:公交检索站点

___

### ad

• **ad**: `number`

___

### adstyle

• **adstyle**: `number`

___

### qid

• **qid**: `string`

___

### puid

• **puid**: `string`

___

### adLog

• **adLog**: `string`

___

### dysrc

• **dysrc**: `number`

___

### dystge

• **dystge**: `number`

___

### url

• **url**: `string`

___

### styleId

• **styleId**: `number`

___

### level

• **level**: `number`

___

### isAgg

• **isAgg**: `boolean`

___

### tagName

• **tagName**: `string`

___

### tagSrcLog

• **tagSrcLog**: `number`

___

### isDot

• **isDot**: `boolean`

## Methods

### parseMCarJsonObj

▸ **parseMCarJsonObj**(`jsonMcar`): ``null`` \| [`MapClickObj`](map.MapClickObj.md)

解析多路线点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `jsonMcar` | `object` |

#### Returns

``null`` \| [`MapClickObj`](map.MapClickObj.md)

___

### parseNormalJsonObj

▸ **parseNormalJsonObj**(`jsonObj`): ``null`` \| [`MapClickObj`](map.MapClickObj.md)

普通底图Poi点击

#### Parameters

| Name | Type |
| :------ | :------ |
| `jsonObj` | `object` |

#### Returns

``null`` \| [`MapClickObj`](map.MapClickObj.md)
